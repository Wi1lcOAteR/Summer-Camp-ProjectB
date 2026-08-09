from __future__ import annotations

import asyncio
import _socket
import os
import sys
import shutil
import socket
import subprocess
import time
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient


ROOT = Path(__file__).resolve().parents[3]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from projectb.profiles import demo  # noqa: E402
from projectb.security.http import HttpBoundaryError, SessionCsrfProtector  # noqa: E402


_DEMO_LOOP = asyncio.new_event_loop()
_SOCKET_FUNCTIONS = {
    (socket, name): getattr(socket, name)
    for name in ("create_connection", "getaddrinfo", "gethostbyname", "gethostbyname_ex", "gethostbyaddr", "getnameinfo")
}
_SOCKET_METHODS = {
    name: getattr(socket.socket, name)
    for name in ("connect", "connect_ex", "sendto", "sendmsg")
    if hasattr(socket.socket, name)
}
_PROCESS_FUNCTIONS = {
    (owner, name): getattr(owner, name)
    for owner, names in (
        (subprocess, ("Popen", "run", "call", "check_call", "check_output")),
        (
            os,
            (
                "system",
                "popen",
                "execl",
                "execle",
                "execlp",
                "execlpe",
                "execv",
                "execve",
                "execvp",
                "execvpe",
                "fork",
                "forkpty",
                "posix_spawn",
                "posix_spawnp",
                "spawnl",
                "spawnle",
                "spawnlp",
                "spawnlpe",
                "spawnv",
                "spawnve",
                "spawnvp",
                "spawnvpe",
                "startfile",
            ),
        ),
    )
    for name in names
    if hasattr(owner, name)
}


@pytest.fixture(autouse=True)
def isolate_process_guard() -> None:
    yield
    for (owner, name), original in _SOCKET_FUNCTIONS.items():
        setattr(owner, name, original)
    for name, original in _SOCKET_METHODS.items():
        setattr(socket.socket, name, original)
    for (owner, name), original in _PROCESS_FUNCTIONS.items():
        setattr(owner, name, original)
    demo._EGRESS_GUARD_INSTALLED = False


def test_demo_origin_is_exact_https_or_explicit_fixed_local_smoke() -> None:
    resolve_demo_http_config = demo.resolve_demo_http_config
    local = resolve_demo_http_config({"PROJECTB_DEMO_LOCAL_SMOKE": "1"})
    assert local.origin == "http://127.0.0.1:7860"
    assert local.host == "127.0.0.1:7860"
    assert local.secure_cookie is False

    public = resolve_demo_http_config({"PROJECTB_PUBLIC_ORIGIN": "https://demo.example.test:8443"})
    assert public.origin == "https://demo.example.test:8443"
    assert public.host == "demo.example.test:8443"
    assert public.secure_cookie is True

    invalid = (
        {},
        {"PROJECTB_DEMO_LOCAL_SMOKE": "true"},
        {"PROJECTB_PUBLIC_ORIGIN": "http://demo.example.test"},
        {"PROJECTB_PUBLIC_ORIGIN": "https://*.example.test"},
        {"PROJECTB_PUBLIC_ORIGIN": "https://demo.example.test/path"},
        {"PROJECTB_PUBLIC_ORIGIN": "https://user@demo.example.test"},
        {
            "PROJECTB_DEMO_LOCAL_SMOKE": "1",
            "PROJECTB_PUBLIC_ORIGIN": "https://demo.example.test",
        },
    )
    for environment in invalid:
        with pytest.raises(ValueError, match="demo_http_config_invalid"):
            resolve_demo_http_config(environment)


def test_demo_policy_enforces_exact_host_origin_forwarding_and_session_csrf() -> None:
    config = demo.resolve_demo_http_config({"PROJECTB_PUBLIC_ORIGIN": "https://demo.example.test"})
    csrf = SessionCsrfProtector(b"d" * 32)
    policy = demo.DemoHttpPolicy(config, csrf=csrf)

    assert policy.authorize(method="GET", host="demo.example.test").method == "GET"
    csrf_receipt = csrf.issue("session-a")
    assert policy.authorize(
        method="POST",
        host="demo.example.test",
        origin="https://demo.example.test",
        session_id="session-a",
        csrf_token=csrf_receipt,
    ).method == "POST"

    rejected = (
        {"method": "GET", "host": "other.example.test"},
        {
            "method": "POST",
            "host": "demo.example.test",
            "origin": "https://other.example.test",
            "session_id": "session-a",
            "csrf_token": csrf_receipt,
        },
        {
            "method": "GET",
            "host": "demo.example.test",
            "forwarded_headers": {"x-forwarded-proto": "https"},
        },
        {
            "method": "POST",
            "host": "demo.example.test",
            "origin": "https://demo.example.test",
            "session_id": "session-b",
            "csrf_token": csrf_receipt,
        },
    )
    for request in rejected:
        with pytest.raises(HttpBoundaryError):
            policy.authorize(**request)


def test_rejected_requests_do_not_allocate_seed_or_refresh_sessions(tmp_path: Path) -> None:
    now = [0.0]
    session_root = tmp_path / "sessions"
    app = demo.create_demo_app(
        session_root=session_root,
        environment={"PROJECTB_DEMO_LOCAL_SMOKE": "1"},
        clock=lambda: now[0],
    )
    baseline_paths = set(session_root.iterdir())

    async def exercise() -> None:
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://127.0.0.1:7860",
        ) as value:
            assert (await value.get("/api/session", headers={"host": "invalid.example"})).status_code == 403
            assert (await value.post(
                "/api/courses",
                json={"name": "Rejected", "timezone": "UTC"},
                headers={"origin": "http://127.0.0.1:7860"},
            )).status_code == 403
            assert set(session_root.iterdir()) == baseline_paths

            assert (await value.get("/api/session")).status_code == 200
            original_session = value.cookies.get("projectb_session")
            assert original_session
            original_path = session_root / original_session
            now[0] = 1700.0
            assert (await value.get(
                "/api/session",
                headers={"x-forwarded-host": "127.0.0.1:7860"},
            )).status_code == 403
            now[0] = 1801.0
            assert (await value.get("/api/session")).status_code == 200
            assert value.cookies.get("projectb_session") != original_session
            assert not original_path.exists()

    _DEMO_LOOP.run_until_complete(exercise())


def test_demo_sessions_expire_after_idle_or_absolute_ttl_and_cleanup(tmp_path: Path) -> None:
    now = [0.0]
    manager = demo.DemoSessionManager(tmp_path, clock=lambda: now[0])

    first = manager.acquire(None)
    first_path = tmp_path / first.session_id
    assert first.created is True
    assert first_path.is_dir()

    now[0] = 1801.0
    idle_replacement = manager.acquire(first.session_id)
    assert idle_replacement.created is True
    assert idle_replacement.session_id != first.session_id
    assert not first_path.exists()

    absolute = idle_replacement
    for timestamp in (3500.0, 5200.0, 6900.0, 8600.0):
        now[0] = timestamp
        assert manager.acquire(absolute.session_id).created is False
    absolute_path = tmp_path / absolute.session_id
    now[0] = 9002.0
    absolute_replacement = manager.acquire(absolute.session_id)
    assert absolute_replacement.created is True
    assert absolute_replacement.session_id != absolute.session_id
    assert not absolute_path.exists()


def test_demo_sessions_are_cleaned_without_later_request_traffic(tmp_path: Path) -> None:
    now = [0.0]
    manager = demo.DemoSessionManager(
        tmp_path,
        clock=lambda: now[0],
        cleanup_interval_seconds=0.01,
    )
    try:
        lease = manager.acquire(None)
        session_path = tmp_path / lease.session_id
        now[0] = 1801.0
        deadline = time.monotonic() + 1.0
        while session_path.exists() and time.monotonic() < deadline:
            time.sleep(0.01)
        assert not session_path.exists()
    finally:
        manager.close()


def test_expired_session_is_not_deleted_while_request_lease_is_active(tmp_path: Path) -> None:
    now = [0.0]
    manager = demo.DemoSessionManager(
        tmp_path,
        clock=lambda: now[0],
        cleanup_interval_seconds=None,
    )
    lease = manager.acquire(None)
    session_path = tmp_path / lease.session_id

    with manager.scope(lease.session_id):
        now[0] = 1801.0
        manager.cleanup_expired()
        assert session_path.exists()

    manager.cleanup_expired()
    assert not session_path.exists()


def test_reserved_session_survives_cleanup_between_lookup_and_scope(tmp_path: Path) -> None:
    now = [0.0]
    manager = demo.DemoSessionManager(
        tmp_path,
        clock=lambda: now[0],
        cleanup_interval_seconds=None,
    )
    lease = manager.acquire(None)
    session_path = tmp_path / lease.session_id

    now[0] = 1799.0
    reserved = manager.reserve(lease.session_id)
    assert reserved is not None
    now[0] = 1801.0
    manager.cleanup_expired()
    assert session_path.exists()

    with manager.scope(reserved.session_id, reserved=True):
        assert session_path.exists()
    now[0] = 3602.0
    manager.cleanup_expired()
    assert not session_path.exists()


def test_failed_session_deletion_is_retained_and_retried(tmp_path: Path) -> None:
    now = [0.0]
    attempts = [0]

    def delete_tree(path: Path) -> None:
        attempts[0] += 1
        if attempts[0] == 1:
            raise OSError("synthetic_delete_failure")
        shutil.rmtree(path)

    manager = demo.DemoSessionManager(
        tmp_path,
        clock=lambda: now[0],
        cleanup_interval_seconds=None,
        delete_tree=delete_tree,
    )
    lease = manager.acquire(None)
    session_path = tmp_path / lease.session_id
    now[0] = 1801.0

    manager.cleanup_expired()
    assert session_path.exists()
    assert manager.pending_deletion_count == 1
    manager.cleanup_expired()
    assert not session_path.exists()
    assert manager.pending_deletion_count == 0
    assert attempts[0] == 2


def test_demo_app_denies_outbound_connections_process_wide(tmp_path: Path) -> None:
    demo.create_demo_app(
        session_root=tmp_path / "sessions",
        environment={"PROJECTB_DEMO_LOCAL_SMOKE": "1"},
    )

    with pytest.raises(demo.DemoEgressDenied, match="demo_egress_denied"):
        socket.create_connection(("203.0.113.1", 443), timeout=0.01)
    connection = socket.socket()
    try:
        with pytest.raises(demo.DemoEgressDenied, match="demo_egress_denied"):
            connection.connect(("203.0.113.1", 443))
    finally:
        connection.close()


def test_demo_egress_guard_denies_low_level_socket_connections(tmp_path: Path) -> None:
    demo.create_demo_app(
        session_root=tmp_path / "sessions",
        environment={"PROJECTB_DEMO_LOCAL_SMOKE": "1"},
    )

    connection = _socket.socket()
    try:
        with pytest.raises(demo.DemoEgressDenied, match="demo_egress_denied"):
            connection.connect(("127.0.0.1", 9))
    finally:
        connection.close()


def test_demo_egress_guard_denies_name_resolution_and_datagrams(tmp_path: Path) -> None:
    demo.create_demo_app(
        session_root=tmp_path / "sessions",
        environment={"PROJECTB_DEMO_LOCAL_SMOKE": "1"},
    )

    with pytest.raises(demo.DemoEgressDenied, match="demo_egress_denied"):
        socket.getaddrinfo("example.invalid", 443)
    with pytest.raises(demo.DemoEgressDenied, match="demo_egress_denied"):
        socket.gethostbyname("example.invalid")
    datagram = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        with pytest.raises(demo.DemoEgressDenied, match="demo_egress_denied"):
            datagram.sendto(b"blocked", ("203.0.113.1", 53))
        if hasattr(datagram, "sendmsg"):
            with pytest.raises(demo.DemoEgressDenied, match="demo_egress_denied"):
                datagram.sendmsg([b"blocked"], [], 0, ("203.0.113.1", 53))
    finally:
        datagram.close()


def test_demo_egress_guard_denies_loopback_outbound_paths(tmp_path: Path) -> None:
    demo.create_demo_app(
        session_root=tmp_path / "sessions",
        environment={"PROJECTB_DEMO_LOCAL_SMOKE": "1"},
    )

    with pytest.raises(demo.DemoEgressDenied, match="demo_egress_denied"):
        socket.create_connection(("127.0.0.1", 9), timeout=0.01)
    with pytest.raises(demo.DemoEgressDenied, match="demo_egress_denied"):
        socket.getaddrinfo("127.0.0.1", 7860)
    datagram = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        with pytest.raises(demo.DemoEgressDenied, match="demo_egress_denied"):
            datagram.sendto(b"blocked", ("127.0.0.1", 7860))
    finally:
        datagram.close()


def test_demo_egress_guard_denies_post_bootstrap_python_processes(tmp_path: Path) -> None:
    demo.create_demo_app(
        session_root=tmp_path / "sessions",
        environment={"PROJECTB_DEMO_LOCAL_SMOKE": "1"},
    )

    command = [sys.executable, "-c", "pass"]
    with pytest.raises(demo.DemoEgressDenied, match="demo_egress_denied"):
        subprocess.run(command, check=True)
    with pytest.raises(demo.DemoEgressDenied, match="demo_egress_denied"):
        subprocess.Popen(command)
    with pytest.raises(demo.DemoEgressDenied, match="demo_egress_denied"):
        os.system("exit /b 0")
    with pytest.raises(demo.DemoEgressDenied, match="demo_egress_denied"):
        os.execv(str(tmp_path / "missing-executable"), ["missing-executable"])

    guarded_names = {
        "execl",
        "execle",
        "execlp",
        "execlpe",
        "execv",
        "execve",
        "execvp",
        "execvpe",
        "fork",
        "forkpty",
        "posix_spawn",
        "posix_spawnp",
    }
    for name in guarded_names:
        if hasattr(os, name):
            assert getattr(os, name) is demo._deny_process


def test_demo_session_seed_uses_bootstrap_template_without_post_guard_process(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    app = demo.create_demo_app(
        session_root=tmp_path / "sessions",
        environment={"PROJECTB_DEMO_LOCAL_SMOKE": "1"},
    )

    def unexpected_process(*args: object, **kwargs: object) -> None:
        raise AssertionError("post_bootstrap_process_started")

    monkeypatch.setattr(demo, "_ORIGINAL_SUBPROCESS_POPEN", unexpected_process)
    async def exercise() -> None:
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://127.0.0.1:7860",
        ) as client:
            assert (await client.get("/api/session")).status_code == 200

    _DEMO_LOOP.run_until_complete(exercise())
