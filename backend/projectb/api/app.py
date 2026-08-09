from __future__ import annotations

import secrets
from collections.abc import Mapping
from contextlib import nullcontext
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Protocol

from fastapi import APIRouter, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse

from projectb.api.app_support import ApiError
from projectb.api.routes import courses, credentials, learning, materials, providers, review, settings
from projectb.api.static import mount_static
from projectb.providers.registry import ProviderRegistry
from projectb.security.http import AuthorizationReceipt, HttpBoundaryError, LocalHttpPolicy, SessionCsrfProtector
from projectb.security.credentials import CredentialService
from projectb.storage.content_store import ContentStore
from projectb.storage.db import Database


LOCAL_ROUTE_CAPABILITIES = frozenset(
    {"courses", "materials", "upload", "learning", "providers", "review", "credentials", "settings"}
)


@dataclass(frozen=True, slots=True)
class CookieContract:
    name: str = "projectb_session"
    httponly: bool = True
    samesite: Literal["lax", "strict", "none"] = "strict"
    secure: bool = False


class HttpPolicy(Protocol):
    csrf: SessionCsrfProtector

    def authorize(
        self,
        *,
        method: str,
        host: str,
        origin: str | None = None,
        session_id: str | None = None,
        csrf_token: str | None = None,
        forwarded_headers: Mapping[str, str] | None = None,
    ) -> AuthorizationReceipt: ...


def _validated_published_settings(
    published: Mapping[str, object] | None,
    *,
    profile_name: str,
) -> dict[str, object] | None:
    if published is None:
        return None
    value = dict(published)
    if set(value) != {"profile", "bind_host", "provider_mode", "provider_configured"}:
        raise ValueError("published_settings_invalid")
    profile = value["profile"]
    bind_host = value["bind_host"]
    if (
        profile not in {"local", "demo"}
        or profile != profile_name
        or (profile == "local" and bind_host != "127.0.0.1")
        or (profile == "demo" and bind_host != "0.0.0.0")
        or value["provider_mode"] not in {"L", "L+P"}
        or type(value["provider_configured"]) is not bool
    ):
        raise ValueError("published_settings_invalid")
    return value


def _error_payload(code: str, retryable: bool, next_action: str, request_id: str) -> dict[str, object]:
    return {
        "error": {
            "code": code,
            "retryable": retryable,
            "next_action": next_action,
            "request_id": request_id,
        }
    }


def create_app(
    *,
    database_path: Path,
    content_dir: Path,
    static_dir: Path | None = None,
    provider_registry: ProviderRegistry | None = None,
    credential_service: CredentialService | None = None,
    profile_name: str = "local",
    http_policy: HttpPolicy | None = None,
    cookie_contract: CookieContract | None = None,
    route_capabilities: frozenset[str] | None = None,
    published_settings: Mapping[str, object] | None = None,
    profile_router: APIRouter | None = None,
) -> FastAPI:
    database = Database(database_path)
    database.initialize()
    content_store = ContentStore(content_dir)
    policy = http_policy or LocalHttpPolicy()
    cookie = cookie_contract or CookieContract()
    capabilities = LOCAL_ROUTE_CAPABILITIES if route_capabilities is None else frozenset(route_capabilities)
    app = FastAPI(title="ProjectB", docs_url=None, redoc_url=None, openapi_url=None)
    app.state.database = database
    app.state.content_store = content_store
    app.state.provider_registry = provider_registry or ProviderRegistry("local")
    app.state.provider_previews = {}
    app.state.credential_service = credential_service
    app.state.profile_name = profile_name
    app.state.published_settings = _validated_published_settings(published_settings, profile_name=profile_name)
    session_manager = getattr(policy, "sessions", None)
    if session_manager is not None:
        app.router.on_shutdown.append(session_manager.close)

    @app.middleware("http")
    async def local_trust(request: Request, call_next):  # type: ignore[no-untyped-def]
        forwarded = {
            name: value
            for name, value in request.headers.items()
            if name.lower() in {"forwarded", "x-forwarded-for", "x-forwarded-host", "x-forwarded-proto"}
        }
        presented_session_id = request.cookies.get(cookie.name)
        session_manager = getattr(policy, "sessions", None)
        lease = None
        session_id = presented_session_id
        reservation_pending = False
        try:
            if session_manager is not None:
                preflight = getattr(policy, "preflight", None)
                if preflight is None:
                    raise RuntimeError("session_policy_preflight_missing")
                preflight(
                    host=request.headers.get("host", ""),
                    origin=request.headers.get("origin"),
                    forwarded_headers=forwarded,
                )
                lease = session_manager.reserve(presented_session_id)
                reservation_pending = lease is not None
                session_id = lease.session_id if lease is not None else None
            receipt = policy.authorize(
                method=request.method,
                host=request.headers.get("host", ""),
                origin=request.headers.get("origin"),
                session_id=session_id,
                csrf_token=request.headers.get("x-csrf-token"),
                forwarded_headers=forwarded,
            )
            if session_manager is not None and lease is None:
                lease = session_manager.create(reserve=True)
                reservation_pending = True
                session_id = lease.session_id
            scope = (
                session_manager.scope(session_id, reserved=True)
                if session_manager is not None
                else nullcontext()
            )
            with scope:
                reservation_pending = False
                request.state.request_id = receipt.request_id
                response = await call_next(request)
        except HttpBoundaryError as error:
            if session_manager is not None and reservation_pending and lease is not None:
                session_manager.release(lease)
            response = JSONResponse(error.to_payload(), status_code=403)
            response.headers["x-request-id"] = error.request_id
            return response
        except BaseException:
            if session_manager is not None and reservation_pending and lease is not None:
                session_manager.release(lease)
            raise
        response.headers["x-request-id"] = receipt.request_id
        if request.method in {"GET", "HEAD", "OPTIONS"}:
            if lease is not None and lease.created:
                response.set_cookie(
                    cookie.name,
                    session_id,
                    httponly=cookie.httponly,
                    samesite=cookie.samesite,
                    secure=cookie.secure,
                )
            elif not session_id:
                session_id = secrets.token_urlsafe(24)
                response.set_cookie(
                    cookie.name,
                    session_id,
                    httponly=cookie.httponly,
                    samesite=cookie.samesite,
                    secure=cookie.secure,
                )
            if not isinstance(session_id, str) or not session_id:
                raise RuntimeError("session_id_missing")
            response.headers["x-csrf-token"] = policy.csrf.issue(session_id)
        return response

    @app.exception_handler(ApiError)
    async def api_error(request: Request, error: ApiError) -> JSONResponse:
        request_id = getattr(request.state, "request_id", secrets.token_hex(16))
        return JSONResponse(
            _error_payload(error.code, error.retryable, error.next_action, request_id),
            status_code=error.status_code,
        )

    @app.exception_handler(RequestValidationError)
    async def invalid_request(request: Request, _: RequestValidationError) -> JSONResponse:
        request_id = getattr(request.state, "request_id", secrets.token_hex(16))
        return JSONResponse(_error_payload("invalid_request", False, "check_request", request_id), status_code=422)

    @app.get("/api/session")
    def session() -> dict[str, str]:
        return {"status": "ready"}

    if "courses" in capabilities:
        app.include_router(courses.router)
    if "materials" in capabilities:
        if "upload" in capabilities:
            app.include_router(materials.router)
        else:
            material_routes = APIRouter()
            material_routes.routes.extend(
                route for route in materials.router.routes if getattr(route, "name", None) != "import_materials"
            )
            app.include_router(material_routes)
    if "learning" in capabilities:
        app.include_router(learning.router)
    if "providers" in capabilities:
        app.include_router(providers.router)
    if "review" in capabilities:
        app.include_router(review.router)
    if "credentials" in capabilities:
        app.include_router(credentials.router)
    if "settings" in capabilities:
        app.include_router(settings.router)
    if profile_router is not None:
        app.include_router(profile_router)
    if static_dir is not None:
        static_index = static_dir.resolve(strict=True) / "index.html"

        @app.api_route(
            "/api/{unmatched_path:path}",
            methods=["GET", "HEAD", "OPTIONS", "POST", "PUT", "PATCH", "DELETE"],
        )
        async def unmatched_api(unmatched_path: str) -> JSONResponse:
            return JSONResponse({"detail": "Not Found"}, status_code=404)

        @app.middleware("http")
        async def webui_history_fallback(request: Request, call_next):  # type: ignore[no-untyped-def]
            response = await call_next(request)
            route_name = Path(request.url.path).name
            if (
                response.status_code == 404
                and request.method in {"GET", "HEAD"}
                and not request.url.path.startswith("/api/")
                and "." not in route_name
                and static_index.is_file()
            ):
                fallback = FileResponse(static_index)
                for header_name in ("x-request-id", "x-csrf-token", "set-cookie"):
                    header_value = response.headers.get(header_name)
                    if header_value is not None:
                        fallback.headers[header_name] = header_value
                return fallback
            return response

        mount_static(app, static_dir, private_roots=(content_dir, database_path))
    return app
