"""F-04 contract for local HTTP trust and session-bound CSRF."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[3]


def load_http_module():
    path = ROOT / "backend/projectb/security/http.py"
    spec = importlib.util.spec_from_file_location("projectb_http", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_local_policy_accepts_only_loopback_hosts_and_origins() -> None:
    http = load_http_module()
    policy = http.LocalHttpPolicy()

    for host in ("127.0.0.1:8000", "localhost:5173", "[::1]:4173"):
        policy.validate_host(host)
    for origin in ("http://127.0.0.1:5173", "http://localhost:4173", "https://[::1]:8443"):
        policy.validate_origin(origin)

    for host in ("0.0.0.0:8000", "192.168.1.2:8000", "localhost.example:8000", "localhost/path"):
        with pytest.raises(http.HttpBoundaryError) as error:
            policy.validate_host(host)
        assert error.value.code == "invalid_host"
    for origin in ("null", "https://example.test", "http://localhost.example:4173", "http://user@localhost:4173"):
        with pytest.raises(http.HttpBoundaryError) as error:
            policy.validate_origin(origin)
        assert error.value.code == "invalid_origin"


def test_unsafe_methods_require_session_bound_csrf_and_origin() -> None:
    http = load_http_module()
    csrf = http.SessionCsrfProtector(b"k" * 32)
    policy = http.LocalHttpPolicy(csrf=csrf)
    csrf_receipt = csrf.issue("session-a")

    receipt = policy.authorize(**{
        "method": "POST",
        "host": "127.0.0.1:8000",
        "origin": "http://localhost:5173",
        "session_id": "session-a",
        "csrf_token": csrf_receipt,
    })
    assert receipt.request_id and receipt.method == "POST"

    for session_id, candidate in (("session-b", csrf_receipt), ("session-a", None), ("session-a", "invalid")):
        with pytest.raises(http.HttpBoundaryError) as error:
            policy.authorize(**{
                "method": "DELETE",
                "host": "localhost:8000",
                "origin": "http://localhost:5173",
                "session_id": session_id,
                "csrf_token": candidate,
            })
        assert error.value.code in {"csrf_required", "csrf_invalid"}


def test_safe_methods_skip_csrf_but_all_methods_reject_untrusted_forwarding() -> None:
    http = load_http_module()
    policy = http.LocalHttpPolicy(csrf=http.SessionCsrfProtector(b"s" * 32))

    receipt = policy.authorize(method="GET", host="[::1]:8000")
    assert receipt.method == "GET"
    with pytest.raises(http.HttpBoundaryError) as error:
        policy.authorize(method="GET", host="localhost:8000", forwarded_headers={"x-forwarded-host": "evil.test"})
    assert error.value.code == "forwarded_headers_forbidden"


def test_error_payload_is_stable_and_never_echoes_untrusted_values() -> None:
    http = load_http_module()
    hostile = "C:/private/answers-do-not-echo.txt"

    with pytest.raises(http.HttpBoundaryError) as captured:
        http.LocalHttpPolicy().validate_host(hostile)
    payload = captured.value.to_payload()
    rendered = repr(payload)

    assert set(payload["error"]) == {"code", "retryable", "next_action", "request_id"}
    assert payload["error"]["code"] == "invalid_host"
    assert hostile not in rendered

    with pytest.raises(http.HttpBoundaryError) as malformed:
        http.LocalHttpPolicy().validate_host("localhost:not-a-port")
    assert malformed.value.__cause__ is None
