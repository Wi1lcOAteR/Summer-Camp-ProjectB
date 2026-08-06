"""Reusable local-profile HTTP trust checks for later FastAPI routes."""

from __future__ import annotations

import hashlib
import hmac
import secrets
from collections.abc import Mapping
from typing import NamedTuple
from urllib.parse import urlsplit


SAFE_METHODS = frozenset({"GET", "HEAD", "OPTIONS"})
LOOPBACK_HOSTS = frozenset({"127.0.0.1", "localhost", "::1"})
FORWARDED_HEADERS = frozenset({"forwarded", "x-forwarded-for", "x-forwarded-host", "x-forwarded-proto"})


class AuthorizationReceipt(NamedTuple):
    request_id: str
    method: str


class HttpBoundaryError(ValueError):
    """A stable, value-free failure safe to return to an HTTP client."""

    def __init__(self, code: str, *, retryable: bool = False, next_action: str = "check_request") -> None:
        super().__init__(code)
        self.code = code
        self.retryable = retryable
        self.next_action = next_action
        self.request_id = secrets.token_hex(16)

    def to_payload(self) -> dict[str, object]:
        return {
            "error": {
                "code": self.code,
                "retryable": self.retryable,
                "next_action": self.next_action,
                "request_id": self.request_id,
            }
        }


class SessionCsrfProtector:
    """Issue stateless CSRF tokens whose MAC is bound to one opaque session ID."""

    def __init__(self, key: bytes) -> None:
        if len(key) < 32:
            raise ValueError("csrf_key_too_short")
        self._key = bytes(key)

    def issue(self, session_id: str) -> str:
        if not session_id:
            raise ValueError("session_id_required")
        nonce = secrets.token_urlsafe(24)
        signature = self._signature(session_id, nonce)
        return f"{nonce}.{signature}"

    def validate(self, session_id: str, token: str) -> bool:
        if not session_id or not token:
            return False
        nonce, separator, signature = token.partition(".")
        if not separator or not nonce or not signature or "." in signature:
            return False
        expected = self._signature(session_id, nonce)
        return hmac.compare_digest(signature, expected)

    def _signature(self, session_id: str, nonce: str) -> str:
        message = f"{session_id}\0{nonce}".encode("utf-8")
        return hmac.new(self._key, message, hashlib.sha256).hexdigest()


class LocalHttpPolicy:
    """Fail-closed Host, Origin, forwarding and CSRF policy for local mode."""

    def __init__(self, *, csrf: SessionCsrfProtector | None = None) -> None:
        self.csrf = csrf or SessionCsrfProtector(secrets.token_bytes(32))

    def validate_host(self, host: str) -> None:
        if not isinstance(host, str) or host.strip() != host or not host:
            raise HttpBoundaryError("invalid_host")
        try:
            parsed = urlsplit(f"http://{host}")
            port = parsed.port
        except ValueError:
            raise HttpBoundaryError("invalid_host") from None
        if (
            parsed.hostname is None
            or parsed.hostname.lower() not in LOOPBACK_HOSTS
            or parsed.username is not None
            or parsed.password is not None
            or parsed.path
            or parsed.query
            or parsed.fragment
            or (port is not None and not 1 <= port <= 65535)
        ):
            raise HttpBoundaryError("invalid_host")

    def validate_origin(self, origin: str) -> None:
        if not isinstance(origin, str) or origin.strip() != origin or not origin:
            raise HttpBoundaryError("invalid_origin")
        try:
            parsed = urlsplit(origin)
            port = parsed.port
        except ValueError:
            raise HttpBoundaryError("invalid_origin") from None
        if (
            parsed.scheme not in {"http", "https"}
            or parsed.hostname is None
            or parsed.hostname.lower() not in LOOPBACK_HOSTS
            or parsed.username is not None
            or parsed.password is not None
            or parsed.path
            or parsed.query
            or parsed.fragment
            or (port is not None and not 1 <= port <= 65535)
        ):
            raise HttpBoundaryError("invalid_origin")

    def authorize(
        self,
        *,
        method: str,
        host: str,
        origin: str | None = None,
        session_id: str | None = None,
        csrf_token: str | None = None,
        forwarded_headers: Mapping[str, str] | None = None,
    ) -> AuthorizationReceipt:
        normalized_method = method.upper()
        self.validate_host(host)
        if forwarded_headers and any(name.lower() in FORWARDED_HEADERS for name in forwarded_headers):
            raise HttpBoundaryError("forwarded_headers_forbidden")
        if origin is not None:
            self.validate_origin(origin)
        if normalized_method not in SAFE_METHODS:
            if origin is None:
                raise HttpBoundaryError("invalid_origin")
            if not session_id or not csrf_token:
                raise HttpBoundaryError("csrf_required", next_action="refresh_session")
            if not self.csrf.validate(session_id, csrf_token):
                raise HttpBoundaryError("csrf_invalid", next_action="refresh_session")
        return AuthorizationReceipt(request_id=secrets.token_hex(16), method=normalized_method)
