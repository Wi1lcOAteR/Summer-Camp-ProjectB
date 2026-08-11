"""F-05 contract for value-free credential lifecycle and WinVault cleanup."""

from __future__ import annotations

import importlib
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime, timedelta
from pathlib import Path
from threading import Barrier, Event, Lock, RLock
from types import ModuleType
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


class CountingVault:
    def __init__(self) -> None:
        self.values: dict[tuple[str, str], str] = {}
        self.reads: list[tuple[str, str]] = []

    def get_password(self, service: str, target: str) -> str | None:
        self.reads.append((service, target))
        return self.values.get((service, target))

    def set_password(self, service: str, target: str, value: str) -> None:
        self.values[(service, target)] = value

    def delete_password(self, service: str, target: str) -> None:
        self.values.pop((service, target), None)


class FakePasswordDeleteError(Exception):
    pass


def install_fake_keyring(
    monkeypatch: pytest.MonkeyPatch,
    factory,
) -> ModuleType:  # type: ignore[no-untyped-def]
    keyring = ModuleType("keyring")
    keyring.__path__ = []  # type: ignore[attr-defined]
    backends = ModuleType("keyring.backends")
    backends.__path__ = []  # type: ignore[attr-defined]
    windows = ModuleType("keyring.backends.Windows")
    windows.WinVaultKeyring = factory  # type: ignore[attr-defined]
    errors = ModuleType("keyring.errors")
    errors.PasswordDeleteError = FakePasswordDeleteError  # type: ignore[attr-defined]
    keyring.backends = backends  # type: ignore[attr-defined]
    keyring.errors = errors  # type: ignore[attr-defined]
    backends.Windows = windows  # type: ignore[attr-defined]
    for name, module in (
        ("keyring", keyring),
        ("keyring.backends", backends),
        ("keyring.backends.Windows", windows),
        ("keyring.errors", errors),
    ):
        monkeypatch.setitem(sys.modules, name, module)
    return windows


def windows_backend(credentials, monkeypatch: pytest.MonkeyPatch, factory):  # type: ignore[no-untyped-def]
    monkeypatch.setattr(credentials.sys, "platform", "win32")
    install_fake_keyring(monkeypatch, factory)
    return credentials.WindowsCredentialBackend()


def test_windows_vault_initializes_once_for_concurrent_callers(monkeypatch: pytest.MonkeyPatch) -> None:
    credentials = load_credentials_module()
    barrier = Barrier(8)
    factory_started = Event()
    release_factory = Event()
    constructions = 0

    class ObservedLock:
        def __init__(self) -> None:
            self._lock = RLock()
            self._counter_lock = Lock()
            self.attempts = 0
            self.all_attempted = Event()

        def __enter__(self):  # type: ignore[no-untyped-def]
            with self._counter_lock:
                self.attempts += 1
                if self.attempts == 8:
                    self.all_attempted.set()
            self._lock.acquire()
            return self

        def __exit__(self, *args):  # type: ignore[no-untyped-def]
            self._lock.release()

    def factory() -> CountingVault:
        nonlocal constructions
        constructions += 1
        factory_started.set()
        assert release_factory.wait(5)
        return CountingVault()

    backend = windows_backend(credentials, monkeypatch, factory)
    observed_lock = ObservedLock()
    backend._vault_lock = observed_lock

    def read_status() -> bool:
        barrier.wait(timeout=5)
        return backend.has_secret("provider-openai")

    try:
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = [executor.submit(read_status) for _ in range(8)]
            assert factory_started.wait(5)
            assert observed_lock.all_attempted.wait(5)
            release_factory.set()
            assert [future.result(timeout=5) for future in futures] == [False] * 8
    finally:
        release_factory.set()

    assert constructions == 1


def test_windows_vault_import_failure_leaves_initialization_retryable(monkeypatch: pytest.MonkeyPatch) -> None:
    credentials = load_credentials_module()
    constructions = 0

    def factory() -> CountingVault:
        nonlocal constructions
        constructions += 1
        return CountingVault()

    monkeypatch.setattr(credentials.sys, "platform", "win32")
    windows = install_fake_keyring(monkeypatch, factory)
    del windows.WinVaultKeyring  # type: ignore[attr-defined]
    backend = credentials.WindowsCredentialBackend()

    with pytest.raises(ImportError):
        backend.has_secret("provider-openai")

    windows.WinVaultKeyring = factory  # type: ignore[attr-defined]
    assert backend.has_secret("provider-openai") is False
    assert constructions == 1


def test_windows_vault_constructor_failure_leaves_initialization_retryable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    credentials = load_credentials_module()
    attempts = 0

    def factory() -> CountingVault:
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise RuntimeError("vault unavailable")
        return CountingVault()

    backend = windows_backend(credentials, monkeypatch, factory)

    with pytest.raises(RuntimeError, match="vault unavailable"):
        backend.has_secret("provider-openai")

    assert backend.has_secret("provider-openai") is False
    assert attempts == 2


@pytest.mark.parametrize("cleanup_error", [False, True])
def test_windows_secret_write_failure_rolls_back_marker_and_preserves_error(
    monkeypatch: pytest.MonkeyPatch,
    cleanup_error: bool,
) -> None:
    credentials = load_credentials_module()
    secret_error = RuntimeError("secret write failed")

    class FailingSecretVault(CountingVault):
        def __init__(self) -> None:
            super().__init__()
            self.deletes: list[tuple[str, str]] = []

        def set_password(self, service: str, target: str, value: str) -> None:
            if service == "ProjectB":
                raise secret_error
            super().set_password(service, target, value)

        def delete_password(self, service: str, target: str) -> None:
            self.deletes.append((service, target))
            if cleanup_error:
                raise FakePasswordDeleteError("marker already absent")
            super().delete_password(service, target)

    vault = FailingSecretVault()
    backend = windows_backend(credentials, monkeypatch, lambda: vault)

    with pytest.raises(RuntimeError, match="secret write failed") as caught:
        backend.set_secret("provider-openai", "private-value")

    assert caught.value is secret_error
    assert vault.deletes == [("ProjectB.status", "provider-openai")]
    if not cleanup_error:
        assert ("ProjectB.status", "provider-openai") not in vault.values


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


def test_windows_status_uses_separate_value_free_marker() -> None:
    credentials = load_credentials_module()
    vault = CountingVault()
    backend = object.__new__(credentials.WindowsCredentialBackend)
    backend._service_name = "ProjectB"
    backend._status_service_name = "ProjectB.status"
    backend._vault = vault
    target = "provider-openai"
    vault.values[("ProjectB", target)] = "plaintext-provider-value"
    vault.values[("ProjectB.status", target)] = "configured-v1"

    assert backend.has_secret(target) is True
    assert vault.reads == [("ProjectB.status", target)]


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
