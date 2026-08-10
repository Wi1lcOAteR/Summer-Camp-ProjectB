from __future__ import annotations

from fastapi import APIRouter, Request
from pydantic import BaseModel, ConfigDict

from projectb.api.app_support import ApiError
from projectb.security.credentials import CredentialError


router = APIRouter(tags=["settings"])


class ProviderEnable(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    model_id: str


@router.get("/api/settings")
def settings(request: Request) -> dict[str, object]:
    published = request.app.state.published_settings
    if published is not None:
        return dict(published)
    controller = request.app.state.provider_controller
    if controller is not None:
        return controller.snapshot()
    service = request.app.state.credential_service
    configured = False
    if service is not None:
        try:
            configured = bool(service.status().configured)
        except CredentialError:
            configured = False
    return {
        "profile": request.app.state.profile_name,
        "bind_host": "127.0.0.1",
        "provider_mode": "L",
        "provider_configured": configured,
    }


@router.post("/api/settings/provider")
def enable_provider(payload: ProviderEnable, request: Request) -> dict[str, object]:
    controller = request.app.state.provider_controller
    if controller is None:
        raise ApiError("provider_unavailable", 403)
    try:
        return controller.enable(payload.model_id)
    except RuntimeError as error:
        code = str(error)
        if code in {"credential_unconfigured", "provider_config_mismatch"}:
            raise ApiError(code, 409) from None
        if code in {"credential_unavailable", "provider_config_unavailable", "provider_unavailable"}:
            raise ApiError(code, 503, retryable=True) from None
        raise ApiError(code, 400) from None


@router.delete("/api/settings/provider")
def disable_provider(request: Request) -> dict[str, object]:
    controller = request.app.state.provider_controller
    if controller is None:
        raise ApiError("provider_unavailable", 403)
    try:
        return controller.disable()
    except RuntimeError as error:
        raise ApiError(str(error), 503, retryable=True) from None
