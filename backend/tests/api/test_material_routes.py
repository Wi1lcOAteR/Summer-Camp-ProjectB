from __future__ import annotations

import sys
from pathlib import Path

from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parents[3]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from projectb.api.app import create_app  # noqa: E402


def client(tmp_path: Path) -> tuple[TestClient, Path]:
    static_dir = tmp_path / "web"
    static_dir.mkdir()
    (static_dir / "index.html").write_text("<main>ProjectB WebUI</main>", encoding="utf-8")
    content_dir = tmp_path / "private-content"
    app = create_app(
        database_path=tmp_path / "projectb.sqlite3",
        content_dir=content_dir,
        static_dir=static_dir,
    )
    return TestClient(app, base_url="http://127.0.0.1"), content_dir


def unsafe_headers(value: TestClient) -> dict[str, str]:
    response = value.get("/api/session")
    return {
        "origin": "http://127.0.0.1",
        "x-csrf-token": response.headers["x-csrf-token"],
    }


def create_course(value: TestClient, headers: dict[str, str]) -> str:
    response = value.post(
        "/api/courses",
        json={"name": "Operating Systems", "timezone": "Asia/Shanghai"},
        headers=headers,
    )
    assert response.status_code == 201
    return str(response.json()["course_id"])


def test_trust_middleware_rejects_non_loopback_forwarding_and_missing_csrf(tmp_path: Path) -> None:
    value, _ = client(tmp_path)

    assert value.get("/api/session", headers={"host": "example.test"}).status_code == 403
    assert value.get("/api/session", headers={"x-forwarded-host": "127.0.0.1"}).status_code == 403
    missing = value.post(
        "/api/courses",
        json={"name": "OS", "timezone": "UTC"},
        headers={"origin": "http://127.0.0.1"},
    )
    assert missing.status_code == 403
    assert missing.json()["error"]["code"] == "csrf_required"
    assert missing.headers["x-request-id"]


def test_course_import_source_mapping_and_delete_flow(tmp_path: Path) -> None:
    value, _ = client(tmp_path)
    headers = unsafe_headers(value)
    course_id = create_course(value, headers)

    imported = value.post(
        f"/api/courses/{course_id}/materials/import",
        files={"files": ("notes.txt", b"mutex\nrace\n", "text/plain")},
        headers=headers,
    )
    assert imported.status_code == 200
    outcome = imported.json()["results"][0]
    assert outcome["status"] == "imported"
    assert "path" not in outcome
    material_id = outcome["material_id"]
    listed = value.get(f"/api/courses/{course_id}/materials")
    assert listed.json()["materials"][0]["filename"] == "notes.txt"

    sources = value.get(f"/api/materials/{material_id}/sources")
    assert sources.status_code == 200
    assert [source["text"] for source in sources.json()["sources"]] == ["mutex", "race"]
    locator_id = sources.json()["sources"][0]["locator_id"]

    concept = value.post(
        f"/api/courses/{course_id}/concepts",
        json={"name": "Mutex", "evaluator_id": "os.mutex.v1"},
        headers=headers,
    )
    assert concept.status_code == 201
    concept_id = concept.json()["concept_id"]
    mapped = value.post(
        f"/api/concepts/{concept_id}/mapping",
        json={"locator_ids": [locator_id], "decision": "confirmed"},
        headers=headers,
    )
    assert mapped.json() == {"version": 1, "decision": "confirmed"}

    concepts = value.get(f"/api/courses/{course_id}/concepts")
    assert concepts.status_code == 200
    assert concepts.json()["concepts"] == [
        {
            "concept_id": concept_id,
            "name": "Mutex",
            "evaluator_id": "os.mutex.v1",
            "state": "active",
            "version": 1,
            "coverage": {
                "decision": "confirmed",
                "locator_ids": [locator_id],
                "source_status": "current",
                "version": 1,
            },
        }
    ]

    deleted = value.delete(f"/api/materials/{material_id}", headers=headers)
    assert deleted.status_code == 200
    assert deleted.json()["status"] == "deleted"
    assert value.get(f"/api/materials/{material_id}/sources").status_code == 404
    assert value.get(f"/api/courses/{course_id}/concepts").json()["concepts"][0]["coverage"]["source_status"] == "stale"


def test_import_limits_return_stable_value_free_errors(tmp_path: Path) -> None:
    value, _ = client(tmp_path)
    headers = unsafe_headers(value)
    course_id = create_course(value, headers)
    too_many = [("files", (f"{index}.txt", b"x", "text/plain")) for index in range(6)]

    response = value.post(f"/api/courses/{course_id}/materials/import", files=too_many, headers=headers)

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "batch_file_limit"
    assert set(response.json()["error"]) == {"code", "retryable", "next_action", "request_id"}


def test_static_files_are_confined_and_private_content_is_never_served(tmp_path: Path) -> None:
    value, content_dir = client(tmp_path)
    content_dir.mkdir(exist_ok=True)
    (content_dir / "private.txt").write_text("private material", encoding="utf-8")

    assert value.get("/").text == "<main>ProjectB WebUI</main>"
    assert value.get("/private.txt").status_code == 404
    assert value.get("/%2e%2e/private-content/private.txt").status_code in {400, 404}
