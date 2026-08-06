from __future__ import annotations

import secrets
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from projectb.api.app_support import ApiError
from projectb.api.routes import courses, materials
from projectb.api.static import mount_static
from projectb.security.http import HttpBoundaryError, LocalHttpPolicy
from projectb.storage.content_store import ContentStore
from projectb.storage.db import Database


def _error_payload(code: str, retryable: bool, next_action: str, request_id: str) -> dict[str, object]:
    return {
        "error": {
            "code": code,
            "retryable": retryable,
            "next_action": next_action,
            "request_id": request_id,
        }
    }


def create_app(*, database_path: Path, content_dir: Path, static_dir: Path | None = None) -> FastAPI:
    database = Database(database_path)
    database.initialize()
    content_store = ContentStore(content_dir)
    policy = LocalHttpPolicy()
    app = FastAPI(title="ProjectB", docs_url=None, redoc_url=None, openapi_url=None)
    app.state.database = database
    app.state.content_store = content_store

    @app.middleware("http")
    async def local_trust(request: Request, call_next):  # type: ignore[no-untyped-def]
        forwarded = {
            name: value
            for name, value in request.headers.items()
            if name.lower() in {"forwarded", "x-forwarded-for", "x-forwarded-host", "x-forwarded-proto"}
        }
        session_id = request.cookies.get("projectb_session")
        try:
            receipt = policy.authorize(
                method=request.method,
                host=request.headers.get("host", ""),
                origin=request.headers.get("origin"),
                session_id=session_id,
                csrf_token=request.headers.get("x-csrf-token"),
                forwarded_headers=forwarded,
            )
        except HttpBoundaryError as error:
            response = JSONResponse(error.to_payload(), status_code=403)
            response.headers["x-request-id"] = error.request_id
            return response
        request.state.request_id = receipt.request_id
        response = await call_next(request)
        response.headers["x-request-id"] = receipt.request_id
        if request.method in {"GET", "HEAD", "OPTIONS"}:
            if not session_id:
                session_id = secrets.token_urlsafe(24)
                response.set_cookie(
                    "projectb_session",
                    session_id,
                    httponly=True,
                    samesite="strict",
                    secure=False,
                )
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

    app.include_router(courses.router)
    app.include_router(materials.router)
    if static_dir is not None:
        mount_static(app, static_dir, private_roots=(content_dir, database_path))
    return app
