from __future__ import annotations

from fastapi import APIRouter, Request
from pydantic import BaseModel, ConfigDict

from projectb.api.app_support import ApiError
from projectb.security.credentials import CredentialError


router = APIRouter(prefix="/api/credentials", tags=["credentials"])


class CredentialUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    value: str


def _service(request: Request):  # type: ignore[no-untyped-def]
    service = request.app.state.credential_service
    if service is None:
        raise ApiError("credential_unavailable", 503, retryable=True, next_action="check_platform")
    return service


def _payload(status) -> dict[str, object]:  # type: ignore[no-untyped-def]
    return {"configured": bool(status.configured), "updated_at": status.updated_at}


@router.get("/provider")
def credential_status(request: Request) -> dict[str, object]:
    try:
        return _payload(_service(request).status())
    except CredentialError as error:
        raise ApiError(error.code, 503, retryable=True) from None


@router.put("/provider")
def credential_update(payload: CredentialUpdate, request: Request) -> dict[str, object]:
    try:
        return _payload(_service(request).update(payload.value))
    except CredentialError as error:
        status = 400 if error.code == "credential_invalid" else 503
        raise ApiError(error.code, status, retryable=status == 503) from None


@router.delete("/provider")
def credential_clear(request: Request) -> dict[str, object]:
    try:
        payload = _payload(_service(request).clear())
        controller = request.app.state.provider_controller
        if controller is not None:
            controller.disable()
        return payload
    except CredentialError as error:
        raise ApiError(error.code, 503, retryable=True) from None
    except RuntimeError as error:
        raise ApiError(str(error), 503, retryable=True) from None
