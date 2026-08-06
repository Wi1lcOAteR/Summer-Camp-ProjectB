"""F-05 contract for value-free credential lifecycle and WinVault cleanup."""

from __future__ import annotations

import importlib
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from uuid import uuid4

import pytest


ROOT = Path(__file__).resolve().parents[3]


def load_credentials_module():
    backend_root = str(ROOT / "backend")
    if backend_root not in sys.path:
        sys.path.insert(0, backend_root)
    return importlib.import_module("projectb.security.credentials")


class FakeBackend:
    name = "fake"

    def __init__(self) -> None:
        self.values: dict[str, str] = {}

    def has_secret(self, target: str) -> bool:
        return target in self.values

    def set_secret(self, target: str, value: str) -> None:
        self.values[target] = value

    def delete_secret(self, target: str) -> None:
        self.values.pop(target, None)


class FailingBackend(FakeBackend):
    def __init__(self, operation: str, message: str) -> None:
        super().__init__()
        self.operation = operation
        self.message = message

    def has_secret(self, target: str) -> bool:
        if self.operation == "status":
            raise RuntimeError(self.message)
        return super().has_secret(target)

    def set_secret(self, target: str, value: str) -> None:
        if self.operation == "update":
            raise RuntimeError(self.message)
        super().set_secret(target, value)

    def delete_secret(self, target: str) -> None:
        if self.operation == "clear":
            raise RuntimeError(self.message)
        super().delete_secret(target)


def test_first_run_update_status_and_clear_never_return_plaintext() -> None:
    credentials = load_credentials_module()
    backend = FakeBackend()
    events: list[dict[str, object]] = []
    instants = iter(
        (
            datetime(2026, 8, 6, 10, 0, tzinfo=UTC),
            datetime(2026, 8, 6, 10, 0, tzinfo=UTC) + timedelta(minutes=1),
            datetime(2026, 8, 6, 10, 0, tzinfo=UTC) + timedelta(minutes=2),
        )
    )
    service = credentials.CredentialService(
        backend,
        target="profile-local",
        audit_sink=events.append,
        utc_now=lambda: next(instants),
    )
    private_value = "temporary-value-" + "x" * 12

    first_status = service.status()
    assert first_status._fields == ("configured", "updated_at")
    assert first_status == (False, None)
    updated_status = service.update(private_value)
    assert updated_status == (True, "2026-08-06T10:00:00Z")
    replacement_status = service.update(private_value + "-replacement")
    assert replacement_status == (True, "2026-08-06T10:01:00Z")
    assert service.status() == replacement_status
    cleared_status = service.clear()
    assert cleared_status == (False, "2026-08-06T10:02:00Z")

    rendered = repr(events) + repr(service.status())
    assert private_value not in rendered
    assert {event["action"] for event in events} == {"credential.status", "credential.update", "credential.clear"}
    assert all(set(event) == {"actor", "action", "result", "opaque_refs", "fingerprint", "request_id", "error_code"} for event in events)


@pytest.mark.parametrize("value", ["", "contains\x00nul", "x" * 4097])
def test_update_rejects_invalid_values_without_writing_or_auditing(value: str) -> None:
    credentials = load_credentials_module()
    backend = FakeBackend()
    events: list[dict[str, object]] = []
    service = credentials.CredentialService(backend, target="profile-local", audit_sink=events.append)

    with pytest.raises(credentials.CredentialError) as error:
        service.update(value)
    assert error.value.code == "credential_invalid"
    assert backend.values == {}
    assert events == []


@pytest.mark.parametrize("operation", ["status", "update", "clear"])
def test_backend_failures_use_stable_redacted_error(operation: str) -> None:
    credentials = load_credentials_module()
    sensitive = "-".join(("sk", "z" * 24))
    service = credentials.CredentialService(FailingBackend(operation, sensitive), target="profile-local")

    with pytest.raises(credentials.CredentialError) as error:
        getattr(service, operation)(*("value",) if operation == "update" else ())

    assert error.value.code == "credential_unavailable"
    assert sensitive not in str(error.value)


def test_audit_uses_fixed_reference_and_sink_failure_does_not_misreport_mutation() -> None:
    credentials = load_credentials_module()
    backend = FakeBackend()
    events: list[dict[str, object]] = []
    credential_target = "-".join(("sk", "y" * 24))

    service = credentials.CredentialService(backend, target=credential_target, audit_sink=events.append)
    service.update("value")
    assert credential_target not in repr(events)
    assert events[-1]["opaque_refs"] == ["credential-profile"]

    def unavailable_sink(record: dict[str, object]) -> None:
        raise RuntimeError("audit unavailable")

    service = credentials.CredentialService(backend, target=credential_target, audit_sink=unavailable_sink)
    assert service.update("replacement").configured is True
    assert credential_target in backend.values
    assert service.clear().configured is False
    assert credential_target not in backend.values


@pytest.mark.skipif(sys.platform != "win32", reason="WinVault integration requires Windows")
@pytest.mark.windows
def test_windows_vault_uses_disposable_target_and_guaranteed_cleanup() -> None:
    credentials = load_credentials_module()
    target = "test-" + uuid4().hex
    backend = credentials.WindowsCredentialBackend(service_name="ProjectB-Test")
    service = credentials.CredentialService(backend, target=target)

    try:
        service.clear()
        assert service.status().configured is False
        assert service.update("temporary-" + uuid4().hex).configured is True
        assert service.update("replacement-" + uuid4().hex).configured is True
        assert service.status().configured is True
    finally:
        service.clear()

    assert service.status().configured is False
