"""Mock-only public demo profile."""

from __future__ import annotations

import errno
import hashlib
import json
import os
import secrets
import shutil
import socket
import subprocess
import sys
import threading
import tempfile
import time
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping
from urllib.parse import urlsplit

from fastapi import APIRouter, FastAPI, Request

from projectb.api.app import CookieContract, create_app
from projectb.providers.mock import MockProvider
from projectb.providers.port import ExplanationInput, SourceFragment
from projectb.providers.registry import ProviderRegistry
from projectb.repositories.courses import CourseRepository
from projectb.security.http import HttpBoundaryError, LocalHttpPolicy, SessionCsrfProtector
from projectb.services.materials.coverage import CoverageService
from projectb.services.materials.importer import MaterialImporter
from projectb.storage.content_store import ContentStore
from projectb.storage.db import Database


FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "demo"
DEMO_IDLE_SECONDS = 30 * 60
DEMO_ABSOLUTE_SECONDS = 2 * 60 * 60
DEMO_BIND_HOST = "0.0.0.0"
DEMO_DEFAULT_PORT = 7860
_EGRESS_GUARD_LOCK = threading.Lock()
_EGRESS_GUARD_INSTALLED = False
_EGRESS_AUDIT_INSTALLED = False
_DENIED_AUDIT_EVENTS = frozenset(
    {
        "os.exec",
        "os.fork",
        "os.forkpty",
        "os.posix_spawn",
        "socket.connect",
        "socket.getaddrinfo",
        "socket.gethostbyaddr",
        "socket.gethostbyname",
        "socket.getnameinfo",
        "socket.sendmsg",
        "socket.sendto",
        "subprocess.Popen",
    }
)
_ORIGINAL_SUBPROCESS_POPEN = subprocess.Popen
_ORIGINAL_PROCESS_FUNCTIONS = {
    (owner, name): getattr(owner, name)
    for owner, names in (
        (subprocess, ("run", "call", "check_call", "check_output")),
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


class DemoEgressDenied(PermissionError):
    pass


def _guard_create_connection(address, *args, **kwargs):  # type: ignore[no-untyped-def]
    raise DemoEgressDenied("demo_egress_denied")


def _guard_connect(value, address):  # type: ignore[no-untyped-def]
    raise DemoEgressDenied("demo_egress_denied")


def _guard_connect_ex(value, address):  # type: ignore[no-untyped-def]
    raise DemoEgressDenied("demo_egress_denied")


def _guard_sendto(value, data, address, *args):  # type: ignore[no-untyped-def]
    raise DemoEgressDenied("demo_egress_denied")


def _guard_sendmsg(value, buffers, *args, **kwargs):  # type: ignore[no-untyped-def]
    raise DemoEgressDenied("demo_egress_denied")


def _guard_getaddrinfo(host, *args, **kwargs):  # type: ignore[no-untyped-def]
    raise DemoEgressDenied("demo_egress_denied")


def _guard_gethostbyname(host):  # type: ignore[no-untyped-def]
    raise DemoEgressDenied("demo_egress_denied")


def _guard_gethostbyname_ex(host):  # type: ignore[no-untyped-def]
    raise DemoEgressDenied("demo_egress_denied")


def _guard_gethostbyaddr(host):  # type: ignore[no-untyped-def]
    raise DemoEgressDenied("demo_egress_denied")


def _guard_getnameinfo(address, *args, **kwargs):  # type: ignore[no-untyped-def]
    raise DemoEgressDenied("demo_egress_denied")


def _guard_popen(command, *args, **kwargs):  # type: ignore[no-untyped-def]
    raise DemoEgressDenied("demo_egress_denied")


def _deny_process(*args, **kwargs):  # type: ignore[no-untyped-def]
    raise DemoEgressDenied("demo_egress_denied")


def _guard_audit_event(event: str, args: tuple[object, ...]) -> None:
    if _EGRESS_GUARD_INSTALLED and event in _DENIED_AUDIT_EVENTS:
        raise DemoEgressDenied("demo_egress_denied")


def install_demo_egress_guard() -> None:
    global _EGRESS_AUDIT_INSTALLED, _EGRESS_GUARD_INSTALLED
    with _EGRESS_GUARD_LOCK:
        if _EGRESS_GUARD_INSTALLED:
            return
        if not _EGRESS_AUDIT_INSTALLED:
            sys.addaudithook(_guard_audit_event)
            _EGRESS_AUDIT_INSTALLED = True
        socket.create_connection = _guard_create_connection
        socket.getaddrinfo = _guard_getaddrinfo
        socket.gethostbyname = _guard_gethostbyname
        socket.gethostbyname_ex = _guard_gethostbyname_ex
        socket.gethostbyaddr = _guard_gethostbyaddr
        socket.getnameinfo = _guard_getnameinfo
        setattr(socket.socket, "connect", _guard_connect)
        setattr(socket.socket, "connect_ex", _guard_connect_ex)
        setattr(socket.socket, "sendto", _guard_sendto)
        if hasattr(socket.socket, "sendmsg"):
            setattr(socket.socket, "sendmsg", _guard_sendmsg)
        setattr(subprocess, "Popen", _guard_popen)
        for (owner, name) in _ORIGINAL_PROCESS_FUNCTIONS:
            setattr(owner, name, _deny_process)
        _EGRESS_GUARD_INSTALLED = True


@dataclass(frozen=True, slots=True)
class DemoHttpConfig:
    origin: str
    host: str
    secure_cookie: bool


@dataclass(frozen=True, slots=True)
class DemoProfile:
    name: str = "demo"
    bind_host: str = DEMO_BIND_HOST
    default_port: int = DEMO_DEFAULT_PORT


@dataclass(frozen=True, slots=True)
class DemoSessionLease:
    session_id: str
    created: bool
    reserved: bool = False


@dataclass(slots=True)
class _DemoSessionState:
    root: Path
    database: Database
    content_store: ContentStore
    created_at: float
    last_seen: float
    active_leases: int = 0


@dataclass(frozen=True, slots=True)
class _FixtureTemplate:
    database: bytes
    content_files: tuple[tuple[Path, bytes], ...]


_FIXTURE_TEMPLATE_LOCK = threading.Lock()
_FIXTURE_TEMPLATE: _FixtureTemplate | None = None


class _SessionProxy:
    def __init__(self, manager: DemoSessionManager, attribute: str) -> None:
        self._manager = manager
        self._attribute = attribute

    def __getattr__(self, name: str):  # type: ignore[no-untyped-def]
        return getattr(getattr(self._manager.current(), self._attribute), name)


class DemoSessionManager:
    """Own isolated, temporary storage selected through a request context."""

    def __init__(
        self,
        root: Path,
        *,
        clock: Callable[[], float] = time.monotonic,
        idle_seconds: int = DEMO_IDLE_SECONDS,
        absolute_seconds: int = DEMO_ABSOLUTE_SECONDS,
        cleanup_interval_seconds: float | None = 5.0,
        delete_tree: Callable[[Path], None] | None = None,
        remove_root_on_close: bool = False,
    ) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self._clock = clock
        self._idle_seconds = idle_seconds
        self._absolute_seconds = absolute_seconds
        self._delete_tree = delete_tree or (lambda path: shutil.rmtree(path))
        self._remove_root_on_close = remove_root_on_close
        self._template = _fixture_template()
        self._sessions: dict[str, _DemoSessionState] = {}
        self._pending_deletions: dict[str, _DemoSessionState] = {}
        self._lock = threading.RLock()
        self._stop_cleanup = threading.Event()
        self._cleanup_thread: threading.Thread | None = None
        self._current: ContextVar[_DemoSessionState | None] = ContextVar("projectb_demo_session", default=None)
        self.database = _SessionProxy(self, "database")
        self.content_store = _SessionProxy(self, "content_store")
        _verified_fixture_paths()
        if cleanup_interval_seconds is not None:
            if cleanup_interval_seconds <= 0:
                raise ValueError("cleanup_interval_invalid")
            self._cleanup_thread = threading.Thread(
                target=self._cleanup_loop,
                args=(cleanup_interval_seconds,),
                name="projectb-demo-cleanup",
                daemon=True,
            )
            self._cleanup_thread.start()

    def acquire(self, candidate: str | None) -> DemoSessionLease:
        lease = self.lookup(candidate)
        if lease is not None:
            with self._lock:
                state = self._sessions.get(lease.session_id)
                if state is not None:
                    state.last_seen = self._clock()
            return lease
        return self.create()

    def lookup(self, candidate: str | None) -> DemoSessionLease | None:
        now = self._clock()
        with self._lock:
            self._cleanup_expired(now)
            state = self._sessions.get(candidate or "")
            if state is not None:
                return DemoSessionLease(candidate or "", False)
        return None

    def reserve(self, candidate: str | None) -> DemoSessionLease | None:
        now = self._clock()
        with self._lock:
            self._cleanup_expired(now)
            state = self._sessions.get(candidate or "")
            if state is None:
                return None
            state.active_leases += 1
            return DemoSessionLease(candidate or "", False, True)

    def release(self, lease: DemoSessionLease) -> None:
        if not lease.reserved:
            return
        with self._lock:
            state = self._sessions.get(lease.session_id)
            if state is None or state.active_leases <= 0:
                raise RuntimeError("demo_session_reservation_missing")
            state.active_leases -= 1

    def create(self, *, reserve: bool = False) -> DemoSessionLease:
        now = self._clock()
        with self._lock:
            session_id = secrets.token_urlsafe(24)
            while session_id in self._sessions:
                session_id = secrets.token_urlsafe(24)
            session_root = self.root / session_id
            session_root.mkdir()
            try:
                database_path = session_root / "projectb.sqlite3"
                database_path.write_bytes(self._template.database)
                content_store = ContentStore(session_root / "content")
                for relative, content in self._template.content_files:
                    destination = content_store.root / relative
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    destination.write_bytes(content)
                database = Database(database_path)
                database.initialize()
                state = _DemoSessionState(
                    root=session_root,
                    database=database,
                    content_store=content_store,
                    created_at=now,
                    last_seen=now,
                    active_leases=1 if reserve else 0,
                )
            except BaseException:
                shutil.rmtree(session_root, ignore_errors=True)
                raise
            self._sessions[session_id] = state
            return DemoSessionLease(session_id, True, reserve)

    @contextmanager
    def scope(self, session_id: str, *, reserved: bool = False) -> Iterator[None]:
        with self._lock:
            state = self._sessions.get(session_id)
            if state is not None:
                if reserved and state.active_leases <= 0:
                    raise RuntimeError("demo_session_reservation_missing")
                state.last_seen = self._clock()
                if not reserved:
                    state.active_leases += 1
        if state is None:
            raise RuntimeError("demo_session_missing")
        context_receipt = self._current.set(state)
        try:
            yield
        finally:
            self._current.reset(context_receipt)
            with self._lock:
                state.active_leases -= 1

    def current(self) -> _DemoSessionState:
        state = self._current.get()
        if state is None:
            raise RuntimeError("demo_session_context_missing")
        return state

    def cleanup_expired(self) -> None:
        with self._lock:
            self._cleanup_expired(self._clock())

    @property
    def pending_deletion_count(self) -> int:
        with self._lock:
            return len(self._pending_deletions)

    def close(self) -> None:
        self._stop_cleanup.set()
        if self._cleanup_thread is not None:
            self._cleanup_thread.join(timeout=1.0)
        with self._lock:
            if any(state.active_leases for state in self._sessions.values()):
                raise RuntimeError("demo_session_cleanup_active")
            for session_id, state in tuple(self._sessions.items()):
                self._pending_deletions[session_id] = state
                self._sessions.pop(session_id)
            self._cleanup_expired(self._clock())
            if self._pending_deletions:
                raise RuntimeError("demo_session_cleanup_failed")
            if self._remove_root_on_close:
                try:
                    shutil.rmtree(self.root)
                except FileNotFoundError:
                    pass
                except OSError as error:
                    try:
                        retained_mount_is_empty = (
                            error.errno == errno.EROFS
                            and self.root.is_dir()
                            and next(self.root.iterdir(), None) is None
                        )
                    except OSError:
                        retained_mount_is_empty = False
                    if not retained_mount_is_empty:
                        raise RuntimeError("demo_session_root_cleanup_failed") from error

    def _cleanup_loop(self, interval_seconds: float) -> None:
        while not self._stop_cleanup.wait(interval_seconds):
            self.cleanup_expired()

    def _cleanup_expired(self, now: float) -> None:
        expired = [
            session_id
            for session_id, state in self._sessions.items()
            if state.active_leases == 0
            and (now - state.last_seen >= self._idle_seconds or now - state.created_at >= self._absolute_seconds)
        ]
        for session_id in expired:
            state = self._sessions.pop(session_id)
            self._pending_deletions[session_id] = state
        for session_id, state in tuple(self._pending_deletions.items()):
            try:
                self._delete_tree(state.root)
            except OSError:
                continue
            self._pending_deletions.pop(session_id, None)


def _verified_fixture_paths() -> dict[str, Path]:
    try:
        manifest = json.loads((FIXTURE_ROOT / "fixtures.manifest.json").read_text(encoding="utf-8"))
        fixtures = manifest["fixtures"]
    except (OSError, KeyError, TypeError, json.JSONDecodeError):
        raise RuntimeError("demo_fixture_manifest_invalid") from None
    if manifest.get("schema_version") != 1 or not isinstance(fixtures, list) or not 1 <= len(fixtures) <= 20:
        raise RuntimeError("demo_fixture_manifest_invalid")
    verified: dict[str, Path] = {}
    for fixture in fixtures:
        if not isinstance(fixture, dict) or fixture.get("license") != "CC0-1.0":
            raise RuntimeError("demo_fixture_manifest_invalid")
        relative = Path(str(fixture.get("path", "")))
        if relative.parts != (relative.name,) or not relative.name:
            raise RuntimeError("demo_fixture_manifest_invalid")
        path = FIXTURE_ROOT / relative
        try:
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
        except OSError:
            raise RuntimeError("demo_fixture_manifest_invalid") from None
        if digest != fixture.get("sha256"):
            raise RuntimeError("demo_fixture_manifest_invalid")
        verified[relative.name] = path
    if set(verified) != {"course.json", "materials.md"}:
        raise RuntimeError("demo_fixture_manifest_invalid")
    return verified


def _seed_session(state: _DemoSessionState) -> None:
    fixtures = _verified_fixture_paths()
    try:
        course_fixture = json.loads(fixtures["course.json"].read_text(encoding="utf-8"))
        course_data = course_fixture["course"]
        concepts = course_fixture["concepts"]
    except (OSError, KeyError, TypeError, json.JSONDecodeError):
        raise RuntimeError("demo_fixture_invalid") from None
    course = CourseRepository(state.database).create(str(course_data["name"]), str(course_data["timezone"]))
    outcome = MaterialImporter(state.database, state.content_store).import_batch(
        course.course_id,
        [fixtures["materials.md"]],
    )[0]
    if outcome.status not in {"imported", "idempotent"} or outcome.version_id is None:
        raise RuntimeError("demo_fixture_import_failed")
    connection = state.database.connect()
    try:
        locator_ids = [
            str(row[0])
            for row in connection.execute(
                "SELECT locator_id FROM source_locator WHERE material_version_id = ? ORDER BY rowid",
                (outcome.version_id,),
            )
        ]
    finally:
        connection.close()
    if not locator_ids or not isinstance(concepts, list):
        raise RuntimeError("demo_fixture_invalid")
    coverage = CoverageService(state.database)
    for concept_data in concepts:
        if not isinstance(concept_data, dict):
            raise RuntimeError("demo_fixture_invalid")
        concept = coverage.create_concept(
            course.course_id,
            str(concept_data["name"]),
            evaluator_id=str(concept_data["evaluator_id"]),
        )
        coverage.record_decision(concept.concept_id, locator_ids, "confirmed")


def _fixture_template() -> _FixtureTemplate:
    global _FIXTURE_TEMPLATE
    with _FIXTURE_TEMPLATE_LOCK:
        if _FIXTURE_TEMPLATE is not None:
            return _FIXTURE_TEMPLATE
        root = Path(tempfile.mkdtemp(prefix="projectb-demo-template-"))
        try:
            database = Database(root / "projectb.sqlite3")
            database.initialize()
            content_store = ContentStore(root / "content")
            _seed_session(
                _DemoSessionState(
                    root=root,
                    database=database,
                    content_store=content_store,
                    created_at=0.0,
                    last_seen=0.0,
                )
            )
            content_files = tuple(
                (path.relative_to(content_store.root), path.read_bytes())
                for path in sorted(content_store.root.rglob("*"))
                if path.is_file()
            )
            _FIXTURE_TEMPLATE = _FixtureTemplate(
                database=(root / "projectb.sqlite3").read_bytes(),
                content_files=content_files,
            )
            return _FIXTURE_TEMPLATE
        finally:
            shutil.rmtree(root, ignore_errors=True)


class DemoHttpPolicy(LocalHttpPolicy):
    """Exact-origin public/demo-smoke policy with the shared CSRF contract."""

    def __init__(
        self,
        config: DemoHttpConfig,
        *,
        csrf: SessionCsrfProtector | None = None,
        sessions: DemoSessionManager | None = None,
    ) -> None:
        super().__init__(csrf=csrf)
        self.config = config
        self.sessions = sessions

    def validate_host(self, host: str) -> None:
        if host != self.config.host:
            raise HttpBoundaryError("invalid_host")

    def validate_origin(self, origin: str) -> None:
        if origin != self.config.origin:
            raise HttpBoundaryError("invalid_origin")

    def preflight(
        self,
        *,
        host: str,
        origin: str | None,
        forwarded_headers: Mapping[str, str] | None,
    ) -> None:
        super().authorize(
            method="GET",
            host=host,
            origin=origin,
            forwarded_headers=forwarded_headers,
        )


def resolve_demo_http_config(environment: Mapping[str, str]) -> DemoHttpConfig:
    """Resolve one fail-closed demo trust boundary from explicit environment."""

    local_flag = environment.get("PROJECTB_DEMO_LOCAL_SMOKE")
    public_origin = environment.get("PROJECTB_PUBLIC_ORIGIN")
    if local_flag is not None:
        if local_flag != "1" or public_origin is not None:
            raise ValueError("demo_http_config_invalid")
        return DemoHttpConfig("http://127.0.0.1:7860", "127.0.0.1:7860", False)
    if public_origin is None or not public_origin or public_origin.strip() != public_origin:
        raise ValueError("demo_http_config_invalid")
    try:
        parsed = urlsplit(public_origin)
        port = parsed.port
    except ValueError:
        raise ValueError("demo_http_config_invalid") from None
    if (
        parsed.scheme != "https"
        or parsed.hostname is None
        or "*" in parsed.hostname
        or parsed.username is not None
        or parsed.password is not None
        or parsed.path
        or parsed.query
        or parsed.fragment
        or not parsed.netloc
        or (port is not None and not 1 <= port <= 65535)
        or public_origin != f"https://{parsed.netloc}"
    ):
        raise ValueError("demo_http_config_invalid")
    return DemoHttpConfig(public_origin, parsed.netloc, True)


demo_router = APIRouter(tags=["demo"])


@demo_router.get("/api/demo/fixture-explanation")
def fixture_explanation(request: Request) -> dict[str, object]:
    connection = request.app.state.database.connect()
    try:
        row = connection.execute(
            "SELECT sl.locator_id, sl.material_version_id, sl.content_hash, mv.locator_index_json "
            "FROM source_locator sl JOIN material_version mv ON mv.version_id = sl.material_version_id "
            "ORDER BY sl.rowid LIMIT 1"
        ).fetchone()
    finally:
        connection.close()
    if row is None:
        raise RuntimeError("demo_fixture_missing")
    try:
        index = json.loads(str(row[3]))
        text = next(item["text"] for item in index if item["locator_id"] == str(row[0]))
    except (KeyError, TypeError, StopIteration, json.JSONDecodeError):
        raise RuntimeError("demo_fixture_invalid") from None
    provider = request.app.state.provider_registry.resolve("demo-mock")
    if not isinstance(provider, MockProvider):
        raise RuntimeError("demo_mock_missing")
    candidate = provider.generate_explanation(
        ExplanationInput(
            (
                SourceFragment(
                    locator_id=str(row[0]),
                    material_version_id=str(row[1]),
                    content_hash=str(row[2]),
                    text=str(text),
                ),
            ),
            "Explain the confirmed synthetic source.",
        )
    )
    return {
        "text": candidate.text,
        "authoritative": candidate.authoritative,
        "source_locator_id": str(row[0]),
    }


def create_demo_app(
    *,
    session_root: Path | None = None,
    static_dir: Path | None = None,
    environment: Mapping[str, str] | None = None,
    clock: Callable[[], float] = time.monotonic,
) -> FastAPI:
    config = resolve_demo_http_config(os.environ if environment is None else environment)
    _fixture_template()
    install_demo_egress_guard()
    root = Path(session_root) if session_root is not None else Path(tempfile.mkdtemp(prefix="projectb-demo-"))
    sessions = DemoSessionManager(root, clock=clock, remove_root_on_close=True)
    provider_registry = ProviderRegistry("demo")
    provider_registry.register("demo-mock", MockProvider())
    app = create_app(
        database_path=Path(":memory:"),
        content_dir=root / ".assembly-content",
        static_dir=static_dir,
        provider_registry=provider_registry,
        credential_service=None,
        profile_name="demo",
        http_policy=DemoHttpPolicy(config, sessions=sessions),
        cookie_contract=CookieContract(samesite="lax", secure=config.secure_cookie),
        route_capabilities=frozenset({"courses", "materials", "learning", "review", "settings"}),
        published_settings={
            "profile": "demo",
            "bind_host": DEMO_BIND_HOST,
            "provider_mode": "L",
            "provider_configured": False,
        },
        profile_router=demo_router,
    )
    app.state.database = sessions.database
    app.state.content_store = sessions.content_store
    app.state.demo_sessions = sessions
    return app
