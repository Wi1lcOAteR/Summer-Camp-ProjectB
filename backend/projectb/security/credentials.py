"""Value-free credential lifecycle backed by Windows Credential Manager."""

from __future__ import annotations

import hashlib
import secrets
import sys
from collections.abc import Callable
from datetime import UTC, datetime
from threading import RLock
from typing import NamedTuple, Protocol

from projectb.observability.audit import build_audit_record


class CredentialError(RuntimeError):
    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


class CredentialStatus(NamedTuple):
    configured: bool
    updated_at: str | None


class CredentialBackend(Protocol):
    name: str

    def has_secret(self, target: str) -> bool: ...

    def get_secret(self, target: str) -> str | None: ...

    def set_secret(self, target: str, value: str) -> None: ...

    def delete_secret(self, target: str) -> None: ...


class WindowsCredentialBackend:
    """Use WinVault directly instead of whichever global keyring is selected."""

    name = "winvault"

    def __init__(self, *, service_name: str = "ProjectB") -> None:
        if sys.platform != "win32":
            raise CredentialError("credential_backend_unsupported")
        from keyring.backends.Windows import WinVaultKeyring

        self._service_name = service_name
        self._status_service_name = f"{service_name}.status"
        self._vault = WinVaultKeyring()

    def has_secret(self, target: str) -> bool:
        return self._vault.get_password(self._status_service_name, target) == "configured-v1"

    def get_secret(self, target: str) -> str | None:
        return self._vault.get_password(self._service_name, target)

    def set_secret(self, target: str, value: str) -> None:
        from keyring.errors import PasswordDeleteError

        self._vault.set_password(self._status_service_name, target, "configured-v1")
        try:
            self._vault.set_password(self._service_name, target, value)
        except Exception:
            try:
                self._vault.delete_password(self._status_service_name, target)
            except PasswordDeleteError:
                pass
            raise

    def delete_secret(self, target: str) -> None:
        from keyring.errors import PasswordDeleteError

        for service_name in (self._status_service_name, self._service_name):
            try:
                self._vault.delete_password(service_name, target)
            except PasswordDeleteError:
                pass


class CredentialService:
    """Expose status/update/clear without a plaintext read operation."""

    def __init__(
        self,
        backend: CredentialBackend,
        *,
        target: str,
        audit_sink: Callable[[dict[str, object]], None] | None = None,
        utc_now: Callable[[], datetime] | None = None,
    ) -> None:
        if not target or len(target) > 128 or any(character.isspace() or character in "/\\" for character in target):
            raise CredentialError("credential_target_invalid")
        self._backend = backend
        self._target = target
        self._audit_sink = audit_sink
        self._utc_now = utc_now or (lambda: datetime.now(UTC))
        self._updated_at: str | None = None
        self._fingerprint = hashlib.sha256(f"{backend.name}:{target}".encode()).hexdigest()
        self._lock = RLock()

    def status(self) -> CredentialStatus:
        with self._lock:
            try:
                configured = self._backend.has_secret(self._target)
            except Exception:
                raise CredentialError("credential_unavailable") from None
            updated_at = self._updated_at
        self._emit_audit(self._build_audit("credential.status", configured))
        return CredentialStatus(configured=configured, updated_at=updated_at)

    def read_for_provider(self) -> str:
        """Return the secret only to the in-process provider adapter."""

        with self._lock:
            try:
                value = self._backend.get_secret(self._target)
            except Exception:
                raise CredentialError("credential_unavailable") from None
        if not isinstance(value, str) or not value or len(value) > 4096 or "\0" in value:
            raise CredentialError("credential_unconfigured")
        return value

    def update(self, value: str) -> CredentialStatus:
        if not isinstance(value, str) or not value or len(value) > 4096 or "\0" in value:
            raise CredentialError("credential_invalid")
        updated_at = self._format_utc(self._utc_now())
        audit_record = self._build_audit("credential.update", True)
        with self._lock:
            try:
                self._backend.set_secret(self._target, value)
            except Exception:
                raise CredentialError("credential_unavailable") from None
            self._updated_at = updated_at
        self._emit_audit(audit_record)
        return CredentialStatus(configured=True, updated_at=self._updated_at)

    def clear(self) -> CredentialStatus:
        updated_at = self._format_utc(self._utc_now())
        audit_record = self._build_audit("credential.clear", False)
        with self._lock:
            try:
                self._backend.delete_secret(self._target)
            except Exception:
                raise CredentialError("credential_unavailable") from None
            self._updated_at = updated_at
        self._emit_audit(audit_record)
        return CredentialStatus(configured=False, updated_at=self._updated_at)

    @staticmethod
    def _format_utc(value: datetime) -> str:
        if value.tzinfo is None:
            raise CredentialError("credential_clock_invalid")
        return value.astimezone(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")

    def _build_audit(self, action: str, configured: bool) -> dict[str, object] | None:
        if self._audit_sink is None:
            return None
        return build_audit_record(
            actor="local",
            action=action,
            result="configured" if configured else "unconfigured",
            opaque_refs=("credential-profile",),
            fingerprint=self._fingerprint,
            request_id=secrets.token_hex(16),
            error_code=None,
        )

    def _emit_audit(self, record: dict[str, object] | None) -> None:
        if record is None or self._audit_sink is None:
            return
        try:
            self._audit_sink(record)
        except Exception:
            # Credential mutation is already authoritative; audit transport
            # failure must not report the opposite state to the caller.
            return
