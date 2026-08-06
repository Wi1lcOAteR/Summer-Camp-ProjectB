from __future__ import annotations

import sys
from pathlib import Path

from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parents[3]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from projectb.api.app import create_app  # noqa: E402
from projectb.providers.mock import MockProvider  # noqa: E402
from projectb.providers.registry import ProviderRegistry  # noqa: E402
from projectb.repositories.provider_profiles import ProviderProfileRepository  # noqa: E402


def setup_app(tmp_path: Path) -> tuple[TestClient, dict[str, str], str, str, MockProvider]:
    registry = ProviderRegistry("test")
    mock = MockProvider()
    registry.register("profile-1", mock)
    app = create_app(
        database_path=tmp_path / "projectb.sqlite3",
        content_dir=tmp_path / "content",
        provider_registry=registry,
    )
    profiles = ProviderProfileRepository(app.state.database)
    profiles.add(
        profile_id="profile-1",
        adapter_id="mock",
        model_id="deterministic",
        budget_limit=1000,
        credential_ref="credential-ref",
        config_fingerprint="b" * 64,
        policy_fingerprint="c" * 64,
    )
    value = TestClient(app, base_url="http://127.0.0.1")
    session = value.get("/api/session")
    headers = {"origin": "http://127.0.0.1", "x-csrf-token": session.headers["x-csrf-token"]}
    course = value.post("/api/courses", json={"name": "OS", "timezone": "UTC"}, headers=headers).json()
    imported = value.post(
        f"/api/courses/{course['course_id']}/materials/import",
        files={"files": ("notes.txt", b"mutex\n", "text/plain")},
        headers=headers,
    ).json()["results"][0]
    sources = value.get(f"/api/materials/{imported['material_id']}/sources").json()["sources"]
    locator_id = sources[0]["locator_id"]
    concept = value.post(
        f"/api/courses/{course['course_id']}/concepts",
        json={"name": "Mutex", "evaluator_id": "os.mutex.v1"},
        headers=headers,
    ).json()
    value.post(
        f"/api/concepts/{concept['concept_id']}/mapping",
        json={"locator_ids": [locator_id], "decision": "confirmed"},
        headers=headers,
    )
    return value, headers, concept["concept_id"], locator_id, mock


def attempt_payload(concept_id: str, attempt_key: str, check_kind: str) -> dict[str, object]:
    return {
        "concept_id": concept_id,
        "attempt_key": attempt_key,
        "check_kind": check_kind,
        "variant_id": f"variant-{attempt_key}",
        "exercise": {"events": [{"thread_id": "t1", "action": "enter"}, {"thread_id": "t1", "action": "exit"}]},
        "answer": {"holds": True, "violation_index": None},
    }


def test_attempt_idempotency_and_mastery_routes(tmp_path: Path) -> None:
    value, headers, concept_id, _, _ = setup_app(tmp_path)
    first = value.post(
        "/api/learning/attempts",
        json=attempt_payload(concept_id, "iso", "isomorphic"),
        headers=headers,
    )
    duplicate = value.post(
        "/api/learning/attempts",
        json=attempt_payload(concept_id, "iso", "isomorphic"),
        headers=headers,
    )
    assert first.status_code == 200
    assert first.json() == duplicate.json()
    assert value.get(f"/api/concepts/{concept_id}/mastery").json()["state"] == "unknown"

    transfer = value.post(
        "/api/learning/attempts",
        json=attempt_payload(concept_id, "transfer", "transfer"),
        headers=headers,
    )
    assert transfer.status_code == 200
    assert value.get(f"/api/concepts/{concept_id}/mastery").json()["state"] == "demonstrated_now"


def test_preview_consent_execute_all_three_ports_and_authority_isolation(tmp_path: Path) -> None:
    value, headers, _, locator_id, mock = setup_app(tmp_path)
    database = value.app.state.database
    connection = database.connect()
    try:
        before = tuple(
            connection.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
            for table in ("coverage_decision", "learning_evidence", "mastery_estimate", "review_plan_revision")
        )
    finally:
        connection.close()

    payloads = {
        "explanation": {"locator_ids": [locator_id], "profile_id": "profile-1", "instruction": "Explain"},
        "practice": {
            "locator_ids": [locator_id],
            "profile_id": "profile-1",
            "evaluator_id": "os.mutex.v1",
            "variant_id": "provider-v1",
        },
        "feedback": {
            "locator_ids": [locator_id],
            "profile_id": "profile-1",
            "outcome": "partial",
            "rubric": [{"code": "mutex", "passed": False, "detail_code": "overlap"}],
        },
    }
    for index, (operation, payload) in enumerate(payloads.items(), start=1):
        preview = value.post(
            f"/api/providers/previews/{operation}",
            json={**payload, "max_tokens": 100, "max_cost_microusd": 200, "nonce": f"nonce-{index}"},
            headers=headers,
        )
        assert preview.status_code == 200
        preview_id = preview.json()["preview_id"]
        consent = value.post("/api/providers/consents", json={"preview_id": preview_id}, headers=headers)
        candidate = value.post(
            "/api/providers/execute",
            json={"preview_id": preview_id, "consent_id": consent.json()["consent_id"]},
            headers=headers,
        )
        assert candidate.status_code == 200
        assert candidate.json()["authoritative"] is False
    assert mock.network_count == 3

    connection = database.connect()
    try:
        after = tuple(
            connection.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
            for table in ("coverage_decision", "learning_evidence", "mastery_estimate", "review_plan_revision")
        )
    finally:
        connection.close()
    assert after == before


def test_feedback_rejects_raw_answer_and_consent_reuse(tmp_path: Path) -> None:
    value, headers, _, locator_id, mock = setup_app(tmp_path)
    rejected = value.post(
        "/api/providers/previews/feedback",
        json={
            "locator_ids": [locator_id],
            "profile_id": "profile-1",
            "outcome": "passed",
            "rubric": [],
            "answer": "must remain local",
            "max_tokens": 100,
            "max_cost_microusd": 100,
            "nonce": "nonce-reject",
        },
        headers=headers,
    )
    assert rejected.status_code == 422
    assert mock.network_count == 0

    preview = value.post(
        "/api/providers/previews/explanation",
        json={
            "locator_ids": [locator_id],
            "profile_id": "profile-1",
            "instruction": "Explain",
            "max_tokens": 100,
            "max_cost_microusd": 100,
            "nonce": "nonce-once",
        },
        headers=headers,
    ).json()
    consent = value.post("/api/providers/consents", json={"preview_id": preview["preview_id"]}, headers=headers).json()
    body = {"preview_id": preview["preview_id"], "consent_id": consent["consent_id"]}
    assert value.post("/api/providers/execute", json=body, headers=headers).status_code == 200
    assert value.post("/api/providers/execute", json=body, headers=headers).status_code == 409
    assert mock.network_count == 1
