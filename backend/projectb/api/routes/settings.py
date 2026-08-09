from __future__ import annotations

from fastapi import APIRouter, Request

from projectb.security.credentials import CredentialError


router = APIRouter(tags=["settings"])


@router.get("/api/settings")
def settings(request: Request) -> dict[str, object]:
    published = request.app.state.published_settings
    if published is not None:
        return dict(published)
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
