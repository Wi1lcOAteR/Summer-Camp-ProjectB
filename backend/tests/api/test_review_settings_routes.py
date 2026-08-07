from __future__ import annotations

import sys
from pathlib import Path

from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parents[3]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from projectb.api.app import create_app  # noqa: E402
from projectb.security.credentials import CredentialService  # noqa: E402


class FakeCredentialBackend:
    name = "fake"

    def __init__(self) -> None:
        self.value: str | None = None

    def has_secret(self, target: str) -> bool:
        return self.value is not None

    def set_secret(self, target: str, value: str) -> None:
        self.value = value

    def delete_secret(self, target: str) -> None:
        self.value = None


def setup_client(tmp_path: Path) -> tuple[TestClient, dict[str, str], FakeCredentialBackend]:
    backend = FakeCredentialBackend()
    app = create_app(
        database_path=tmp_path / "projectb.sqlite3",
        content_dir=tmp_path / "content",
        credential_service=CredentialService(backend, target="profile-local"),
    )
    value = TestClient(app, base_url="http://127.0.0.1")
    session = value.get("/api/session")
    headers = {"origin": "http://127.0.0.1", "x-csrf-token": session.headers["x-csrf-token"]}
    return value, headers, backend


def test_credential_routes_are_value_free_across_first_run_update_and_clear(tmp_path: Path) -> None:
    value, headers, backend = setup_client(tmp_path)
    private_value = "temporary-private-value"

    assert value.get("/api/credentials/provider").json() == {"configured": False, "updated_at": None}
    updated = value.put(
        "/api/credentials/provider",
        json={"value": private_value},
        headers=headers,
    )
    assert set(updated.json()) == {"configured", "updated_at"}
    assert updated.json()["configured"] is True
    assert private_value not in repr(updated.json())
    assert backend.value == private_value
    cleared = value.delete("/api/credentials/provider", headers=headers)
    assert cleared.json()["configured"] is False
    assert backend.value is None


def test_review_revision_and_task_recovery_routes(tmp_path: Path) -> None:
    value, headers, _ = setup_client(tmp_path)
    course = value.post("/api/courses", json={"name": "OS", "timezone": "UTC"}, headers=headers).json()
    concept = value.post(
        f"/api/courses/{course['course_id']}/concepts",
        json={"name": "Mutex", "evaluator_id": "os.mutex.v1"},
        headers=headers,
    ).json()
    imported = value.post(
        f"/api/courses/{course['course_id']}/materials/import",
        files={"files": ("notes.txt", b"mutex\n", "text/plain")},
        headers=headers,
    ).json()["results"][0]
    locator_id = value.get(f"/api/materials/{imported['material_id']}/sources").json()["sources"][0]["locator_id"]
    value.post(
        f"/api/concepts/{concept['concept_id']}/mapping",
        json={"locator_ids": [locator_id], "decision": "confirmed"},
        headers=headers,
    )
    value.post(
        "/api/learning/attempts",
        json={
            "concept_id": concept["concept_id"],
            "attempt_key": "review-evidence",
            "check_kind": "isomorphic",
            "variant_id": "v1",
            "exercise": {"events": [{"thread_id": "t1", "action": "enter"}, {"thread_id": "t1", "action": "exit"}]},
            "answer": {"holds": True, "violation_index": None},
        },
        headers=headers,
    )
    payload = {
        "course_id": course["course_id"],
        "mode": "continuous",
        "timezone": "UTC",
        "daily_budget_minutes": 30,
        "generated_at": "2026-08-06T08:00:00Z",
    }
    first = value.post("/api/review/revisions", json=payload, headers=headers)
    duplicate = value.post("/api/review/revisions", json=payload, headers=headers)
    assert first.status_code == 200
    assert first.json() == duplicate.json()
    task_id = first.json()["tasks"][0]["task_id"]

    assert value.post(f"/api/review/tasks/{task_id}/skip", headers=headers).json()["status"] == "skipped"
    assert value.post(f"/api/review/tasks/{task_id}/recover", headers=headers).json()["status"] == "pending"
    completed = value.post(
        f"/api/review/tasks/{task_id}/complete",
        json={"completed_at": "2026-08-07T09:00:00Z"},
        headers=headers,
    )
    assert completed.json()["status"] == "completed"
    assert value.post(f"/api/review/tasks/{task_id}/recover", headers=headers).status_code == 409
    overridden = value.post(
        "/api/review/revisions",
        json={**payload, "seeds": [{"concept_id": concept["concept_id"], "mastery_state": "retained"}]},
        headers=headers,
    )
    assert overridden.status_code == 422


def test_settings_publish_local_profile_without_secret_or_mock(tmp_path: Path) -> None:
    value, _, _ = setup_client(tmp_path)

    settings = value.get("/api/settings").json()

    assert settings == {
        "profile": "local",
        "bind_host": "127.0.0.1",
        "provider_mode": "L",
        "provider_configured": False,
    }
