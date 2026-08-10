from __future__ import annotations

import asyncio
import errno
import hashlib
import json
import os
import socket
import subprocess
import sys
from pathlib import Path

from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
import pytest


ROOT = Path(__file__).resolve().parents[3]
FIXTURES = ROOT / "backend" / "projectb" / "demo"
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from projectb.api import app as app_module  # noqa: E402
from projectb.profiles import demo  # noqa: E402
from projectb.profiles.registry import get_profile  # noqa: E402
from projectb.providers.mock import MockProvider  # noqa: E402


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


def test_demo_profile_module_exists() -> None:
    import projectb.profiles.demo  # noqa: F401


def test_demo_fixtures_are_small_synthetic_cc0_and_hash_bound() -> None:
    manifest = json.loads((FIXTURES / "fixtures.manifest.json").read_text(encoding="utf-8"))

    assert manifest["schema_version"] == 1
    assert 1 <= len(manifest["fixtures"]) <= 20
    for fixture in manifest["fixtures"]:
        relative = Path(fixture["path"])
        assert relative.parts == (relative.name,)
        assert fixture["license"] == "CC0-1.0"
        content = (FIXTURES / relative).read_bytes()
        assert hashlib.sha256(content).hexdigest() == fixture["sha256"]


def test_create_app_preserves_local_defaults_and_accepts_demo_owned_contract(tmp_path: Path) -> None:
    local = TestClient(
        app_module.create_app(
            database_path=tmp_path / "local.sqlite3",
            content_dir=tmp_path / "local-content",
        ),
        base_url="http://127.0.0.1",
    )
    local_session = local.get("/api/session")
    assert "SameSite=strict" in local_session.headers["set-cookie"]
    assert "Secure" not in local_session.headers["set-cookie"]
    assert local.get("/api/settings").json() == {
        "profile": "local",
        "bind_host": "127.0.0.1",
        "provider_mode": "L",
        "provider_configured": False,
    }
    assert local.get("/api/credentials/provider").status_code == 503

    config = demo.resolve_demo_http_config({"PROJECTB_PUBLIC_ORIGIN": "https://demo.example.test"})
    published = {
        "profile": "demo",
        "bind_host": "0.0.0.0",
        "provider_mode": "L",
        "provider_configured": False,
    }
    demo_client = TestClient(
        app_module.create_app(
            database_path=tmp_path / "demo.sqlite3",
            content_dir=tmp_path / "demo-content",
            http_policy=demo.DemoHttpPolicy(config),
            cookie_contract=app_module.CookieContract(samesite="lax", secure=True),
            route_capabilities=frozenset({"courses", "materials", "learning", "review", "settings"}),
            published_settings=published,
            profile_name="demo",
        ),
        base_url=config.origin,
    )
    session = demo_client.get("/api/session")
    assert "HttpOnly" in session.headers["set-cookie"]
    assert "SameSite=lax" in session.headers["set-cookie"]
    assert "Secure" in session.headers["set-cookie"]
    assert demo_client.get("/api/settings").json() == published
    assert demo_client.get("/api/credentials/provider").status_code == 404
    assert demo_client.get("/api/providers/execute").status_code == 404
    assert demo_client.post(
        "/api/courses/missing/materials/import",
        headers={"origin": config.origin, "x-csrf-token": session.headers["x-csrf-token"]},
    ).status_code == 404

    with pytest.raises(ValueError, match="published_settings_invalid"):
        app_module.create_app(
            database_path=tmp_path / "invalid-demo.sqlite3",
            content_dir=tmp_path / "invalid-demo-content",
            published_settings={
                "profile": "demo",
                "bind_host": "127.0.0.1",
                "provider_mode": "L",
                "provider_configured": False,
            },
        )


def test_demo_app_seeds_fixture_and_isolates_state_between_sessions(tmp_path: Path) -> None:
    environment = {"PROJECTB_DEMO_LOCAL_SMOKE": "1"}
    app = demo.create_demo_app(session_root=tmp_path / "sessions", environment=environment)
    async def exercise() -> None:
        transport = ASGITransport(app=app)
        async with (
            AsyncClient(transport=transport, base_url="http://127.0.0.1:7860") as first,
            AsyncClient(transport=transport, base_url="http://127.0.0.1:7860") as second,
        ):
            first_session = await first.get("/api/session")
            await second.get("/api/session")
            assert isinstance(app.state.provider_registry.resolve("demo-mock"), MockProvider)
            assert (await first.get("/api/settings")).json() == {
                "profile": "demo",
                "bind_host": "0.0.0.0",
                "provider_mode": "L",
                "provider_configured": False,
            }
            first_courses = (await first.get("/api/courses")).json()["courses"]
            second_courses = (await second.get("/api/courses")).json()["courses"]
            assert [course["name"] for course in first_courses] == ["Concurrent Systems Demo"]
            assert [course["name"] for course in second_courses] == ["Concurrent Systems Demo"]

            created = await first.post(
                "/api/courses",
                json={"name": "Private scratch course", "timezone": "UTC"},
                headers={
                    "origin": "http://127.0.0.1:7860",
                    "x-csrf-token": first_session.headers["x-csrf-token"],
                },
            )
            assert created.status_code == 201
            assert len((await first.get("/api/courses")).json()["courses"]) == 2
            assert [course["name"] for course in (await second.get("/api/courses")).json()["courses"]] == [
                "Concurrent Systems Demo"
            ]

    _DEMO_LOOP.run_until_complete(exercise())


def test_demo_app_shutdown_removes_ephemeral_session_root(tmp_path: Path) -> None:
    session_root = tmp_path / "sessions"
    app = demo.create_demo_app(
        session_root=session_root,
        environment={"PROJECTB_DEMO_LOCAL_SMOKE": "1"},
    )

    async def exercise() -> None:
        async with app.router.lifespan_context(app):
            async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://127.0.0.1:7860",
            ) as client:
                assert (await client.get("/api/session")).status_code == 200
                assert any(session_root.iterdir())

    _DEMO_LOOP.run_until_complete(exercise())
    assert not session_root.exists()


def test_demo_shutdown_accepts_only_an_empty_read_only_mount_root(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session_root = tmp_path / "mounted-sessions"
    sessions = demo.DemoSessionManager(
        session_root,
        cleanup_interval_seconds=None,
        remove_root_on_close=True,
    )
    sentinel = session_root / "restart-marker"
    sentinel.write_text("ephemeral", encoding="utf-8")

    def remove_mount_contents_then_reject_root(path: Path) -> None:
        assert Path(path) == session_root
        sentinel.unlink()
        raise OSError(errno.EROFS, "read-only mount root")

    monkeypatch.setattr(demo.shutil, "rmtree", remove_mount_contents_then_reject_root)
    sessions.close()

    assert session_root.is_dir()
    assert not any(session_root.iterdir())


def test_demo_shutdown_rejects_read_only_mount_root_with_residual_content(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session_root = tmp_path / "mounted-sessions"
    sessions = demo.DemoSessionManager(
        session_root,
        cleanup_interval_seconds=None,
        remove_root_on_close=True,
    )
    (session_root / "residual").write_text("must not be ignored", encoding="utf-8")

    def reject_mount_root(path: Path) -> None:
        assert Path(path) == session_root
        raise OSError(errno.EROFS, "read-only mount root")

    monkeypatch.setattr(demo.shutil, "rmtree", reject_mount_root)
    with pytest.raises(RuntimeError, match="demo_session_root_cleanup_failed"):
        sessions.close()


def test_demo_mock_runs_through_read_only_fixture_explanation_path(tmp_path: Path) -> None:
    app = demo.create_demo_app(
        session_root=tmp_path / "sessions",
        environment={"PROJECTB_DEMO_LOCAL_SMOKE": "1"},
    )

    async def exercise() -> None:
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://127.0.0.1:7860",
        ) as client:
            response = await client.get("/api/demo/fixture-explanation")
            assert response.status_code == 200
            assert response.json() == {
                "text": "Mock explanation: Explain the confirmed synthetic source.",
                "authoritative": False,
                "source_locator_id": response.json()["source_locator_id"],
            }
            assert response.json()["source_locator_id"]
            assert (await client.post(
                "/api/providers/execute",
                headers={
                    "origin": "http://127.0.0.1:7860",
                    "x-csrf-token": response.headers["x-csrf-token"],
                },
            )).status_code == 404

    _DEMO_LOOP.run_until_complete(exercise())
    provider = app.state.provider_registry.resolve("demo-mock")
    assert isinstance(provider, MockProvider)
    assert provider.network_count == 1


def test_demo_static_app_falls_back_only_for_webui_routes(tmp_path: Path) -> None:
    static_dir = tmp_path / "web"
    static_dir.mkdir()
    (static_dir / "index.html").write_text("<main>Demo WebUI</main>", encoding="utf-8")
    app = demo.create_demo_app(
        session_root=tmp_path / "sessions",
        static_dir=static_dir,
        environment={"PROJECTB_DEMO_LOCAL_SMOKE": "1"},
    )

    async def exercise() -> None:
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://127.0.0.1:7860",
        ) as client:
            webui = await client.get("/import")
            assert webui.status_code == 200
            assert webui.text == "<main>Demo WebUI</main>"
            assert webui.headers["x-csrf-token"]
            first_session = client.cookies.get("projectb_session")
            assert first_session
            assert (await client.get("/api/settings")).status_code == 200
            assert client.cookies.get("projectb_session") == first_session
            assert (await client.get("/api/missing")).status_code == 404
            assert (await client.get("/missing.txt")).status_code == 404

    _DEMO_LOOP.run_until_complete(exercise())


def test_profile_registry_publishes_demo_without_changing_local_defaults() -> None:
    local = get_profile("local")
    registered_demo = get_profile("demo")

    assert (local.name, local.bind_host, local.default_port) == ("local", "127.0.0.1", 4173)
    assert (registered_demo.name, registered_demo.bind_host, registered_demo.default_port) == (
        "demo",
        "0.0.0.0",
        7860,
    )
