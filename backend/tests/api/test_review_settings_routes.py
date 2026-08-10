from __future__ import annotations

import json
import sys
import threading
from datetime import datetime
from pathlib import Path

import httpx
from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parents[3]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from projectb.api.app import create_app  # noqa: E402
from projectb.profiles.local import create_local_app  # noqa: E402
from projectb.providers import openai_adapter  # noqa: E402
from projectb.security.credentials import CredentialService  # noqa: E402


class FakeCredentialBackend:
    name = "fake"

    def __init__(self) -> None:
        self.value: str | None = None
        self.reads = 0

    def has_secret(self, target: str) -> bool:
        return self.value is not None

    def get_secret(self, target: str) -> str | None:
        self.reads += 1
        return self.value

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


def _local_client(
    tmp_path: Path,
    backend: FakeCredentialBackend,
    *,
    utc_now=None,  # type: ignore[no-untyped-def]
) -> tuple[TestClient, dict[str, str]]:
    def no_network(request: httpx.Request) -> httpx.Response:
        raise AssertionError("provider network must not run during settings lifecycle")

    app = create_local_app(
        tmp_path,
        credential_service=CredentialService(backend, target="provider-openai"),
        provider_transport=httpx.MockTransport(no_network),
        utc_now=utc_now or (lambda: datetime.fromisoformat("2026-08-09T12:00:00+08:00")),
    )
    client = TestClient(app, base_url="http://127.0.0.1")
    session = client.get("/api/session")
    headers = {"origin": "http://127.0.0.1", "x-csrf-token": session.headers["x-csrf-token"]}
    return client, headers


def test_explicit_openai_enable_persists_and_restarts_without_secret_in_config(tmp_path: Path) -> None:
    backend = FakeCredentialBackend()
    client, headers = _local_client(tmp_path, backend)
    assert client.get("/api/settings").json()["provider_mode"] == "L"

    blocked = client.post(
        "/api/settings/provider",
        json={"model_id": "gpt-5.6-terra"},
        headers=headers,
    )
    assert blocked.status_code == 409
    assert blocked.json()["error"]["code"] == "credential_unconfigured"

    client.put("/api/credentials/provider", json={"value": "unit-test-credential"}, headers=headers)
    enabled = client.post(
        "/api/settings/provider",
        json={"model_id": "gpt-5.6-terra"},
        headers=headers,
    )
    assert enabled.status_code == 200
    settings = enabled.json()
    assert settings["provider_mode"] == "L+P"
    assert settings["provider_configured"] is True
    assert settings["provider_profile"]["adapter_id"] == "openai"
    assert settings["provider_profile"]["model_id"] == "gpt-5.6-terra"
    assert settings["provider_profile"]["input_token_cap"] == 20_000
    assert settings["provider_profile"]["output_token_cap"] == 3_000
    assert settings["provider_profile"]["max_cost_microusd"] == 118_250
    profile_id = settings["provider_profile"]["profile_id"]
    assert client.app.state.provider_registry.resolve(profile_id) is not None

    config_text = (tmp_path / "provider.json").read_text(encoding="utf-8")
    assert "unit-test-credential" not in config_text
    assert json.loads(config_text)["enabled"] is True

    restarted, _ = _local_client(tmp_path, backend)
    restarted_settings = restarted.get("/api/settings").json()
    assert restarted_settings == settings
    assert restarted.app.state.provider_registry.resolve(profile_id) is not None


def test_disable_and_credential_clear_both_return_persisted_local_mode(tmp_path: Path) -> None:
    backend = FakeCredentialBackend()
    client, headers = _local_client(tmp_path, backend)
    client.put("/api/credentials/provider", json={"value": "unit-test-credential"}, headers=headers)
    enabled = client.post(
        "/api/settings/provider",
        json={"model_id": "gpt-5.6-luna"},
        headers=headers,
    ).json()
    profile_id = enabled["provider_profile"]["profile_id"]

    disabled = client.delete("/api/settings/provider", headers=headers)
    assert disabled.json()["provider_mode"] == "L"
    assert client.app.state.provider_registry.resolve(profile_id) is None
    assert json.loads((tmp_path / "provider.json").read_text(encoding="utf-8")) == {
        "enabled": False,
        "schema_version": 1,
    }

    client.post("/api/settings/provider", json={"model_id": "gpt-5.6-luna"}, headers=headers)
    cleared = client.delete("/api/credentials/provider", headers=headers)
    assert cleared.json()["configured"] is False
    assert client.get("/api/settings").json()["provider_mode"] == "L"
    assert client.app.state.provider_registry.resolve(profile_id) is None

    restarted, _ = _local_client(tmp_path, backend)
    assert restarted.get("/api/settings").json()["provider_mode"] == "L"


def test_concurrent_enable_and_disable_leave_runtime_and_disk_disabled(
    tmp_path: Path,
    monkeypatch,
) -> None:  # type: ignore[no-untyped-def]
    backend = FakeCredentialBackend()
    backend.value = "unit-test-credential"
    client, _ = _local_client(tmp_path, backend)
    controller = client.app.state.provider_controller
    original_write = controller._write_config
    enable_paused = threading.Event()
    release_enable = threading.Event()
    disable_write_seen = threading.Event()
    outcomes: dict[str, dict[str, object]] = {}
    failures: list[BaseException] = []

    def interleaved_write(value: dict[str, object]) -> None:
        if value.get("enabled") is True:
            enable_paused.set()
            assert release_enable.wait(timeout=2)
        elif threading.current_thread().name == "disable-provider":
            disable_write_seen.set()
        original_write(value)

    def invoke(name: str, operation) -> None:  # type: ignore[no-untyped-def]
        try:
            outcomes[name] = operation()
        except BaseException as error:
            failures.append(error)

    monkeypatch.setattr(controller, "_write_config", interleaved_write)
    enable_thread = threading.Thread(
        target=invoke,
        args=("enable", lambda: controller.enable("gpt-5.6-terra")),
        name="enable-provider",
    )
    enable_thread.start()
    assert enable_paused.wait(timeout=2)
    disable_thread = threading.Thread(
        target=invoke,
        args=("disable", controller.disable),
        name="disable-provider",
    )
    disable_thread.start()
    disable_write_seen.wait(timeout=1)
    release_enable.set()
    enable_thread.join(timeout=2)
    disable_thread.join(timeout=2)

    assert failures == []
    assert not enable_thread.is_alive()
    assert not disable_thread.is_alive()
    assert outcomes["enable"]["provider_mode"] == "L+P"
    assert outcomes["disable"]["provider_mode"] == "L"
    assert controller.snapshot()["provider_mode"] == "L"
    assert json.loads((tmp_path / "provider.json").read_text(encoding="utf-8")) == {
        "enabled": False,
        "schema_version": 1,
    }


def test_policy_expiry_after_enable_degrades_settings_to_local_without_provider(tmp_path: Path) -> None:
    backend = FakeCredentialBackend()
    observed_now = [datetime.fromisoformat("2026-08-09T12:00:00+08:00")]
    client, headers = _local_client(tmp_path, backend, utc_now=lambda: observed_now[0])
    client.put("/api/credentials/provider", json={"value": "unit-test-credential"}, headers=headers)
    enabled = client.post(
        "/api/settings/provider",
        json={"model_id": "gpt-5.6-terra"},
        headers=headers,
    ).json()
    profile_id = enabled["provider_profile"]["profile_id"]

    observed_now[0] = datetime.fromisoformat("2026-08-25T00:00:00+08:00")
    expired = client.get("/api/settings")

    assert expired.status_code == 200
    assert expired.json()["provider_mode"] == "L"
    assert expired.json()["provider_profile"] is None
    assert client.app.state.provider_registry.resolve(profile_id) is None


def test_evidence_hash_mismatch_after_enable_degrades_settings_to_local(
    tmp_path: Path,
    monkeypatch,
) -> None:  # type: ignore[no-untyped-def]
    backend = FakeCredentialBackend()
    client, headers = _local_client(tmp_path, backend)
    client.put("/api/credentials/provider", json={"value": "unit-test-credential"}, headers=headers)
    enabled = client.post(
        "/api/settings/provider",
        json={"model_id": "gpt-5.6-terra"},
        headers=headers,
    ).json()
    profile_id = enabled["provider_profile"]["profile_id"]
    backend.reads = 0

    monkeypatch.setattr(openai_adapter, "_canonical_text_sha256", lambda _path: "0" * 64)
    mismatched = client.get("/api/settings")

    assert mismatched.status_code == 200
    assert mismatched.json()["provider_mode"] == "L"
    assert mismatched.json()["provider_profile"] is None
    assert client.app.state.provider_registry.resolve(profile_id) is None
    assert backend.reads == 0


def test_expired_policy_enable_returns_retryable_unavailable_without_secret_read(tmp_path: Path) -> None:
    backend = FakeCredentialBackend()
    client, headers = _local_client(
        tmp_path,
        backend,
        utc_now=lambda: datetime.fromisoformat("2026-08-25T00:00:00+08:00"),
    )
    client.put("/api/credentials/provider", json={"value": "unit-test-credential"}, headers=headers)

    response = client.post(
        "/api/settings/provider",
        json={"model_id": "gpt-5.6-terra"},
        headers=headers,
    )

    assert response.status_code == 503
    assert response.json()["error"]["code"] == "provider_unavailable"
    assert response.json()["error"]["retryable"] is True
    assert backend.reads == 0


def test_credential_clear_maps_provider_config_failure_after_secret_is_removed(
    tmp_path: Path,
    monkeypatch,
) -> None:  # type: ignore[no-untyped-def]
    backend = FakeCredentialBackend()
    client, headers = _local_client(tmp_path, backend)
    client.put("/api/credentials/provider", json={"value": "unit-test-credential"}, headers=headers)
    enabled = client.post(
        "/api/settings/provider",
        json={"model_id": "gpt-5.6-terra"},
        headers=headers,
    ).json()
    profile_id = enabled["provider_profile"]["profile_id"]

    def unavailable_config(_value) -> None:  # type: ignore[no-untyped-def]
        raise OSError("config unavailable")

    monkeypatch.setattr(client.app.state.provider_controller, "_write_config", unavailable_config)
    response = client.delete("/api/credentials/provider", headers=headers)

    assert response.status_code == 503
    assert response.json()["error"]["code"] == "provider_config_unavailable"
    assert response.json()["error"]["retryable"] is True
    assert backend.value is None
    assert client.app.state.provider_registry.resolve(profile_id) is None
