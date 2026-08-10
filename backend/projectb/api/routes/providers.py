from __future__ import annotations

from dataclasses import asdict

from fastapi import APIRouter, Request
from pydantic import BaseModel, ConfigDict

from projectb.api.app_support import ApiError
from projectb.domain.learning.evaluators.schemas import RubricItem
from projectb.providers.port import ProviderError
from projectb.services.providers.consent import ConsentError, ConsentPreview, ConsentService


router = APIRouter(prefix="/api/providers", tags=["providers"])


class PreviewBase(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    locator_ids: list[str]
    profile_id: str
    max_tokens: int | None = None
    max_cost_microusd: int | None = None
    nonce: str


class ExplanationPreview(PreviewBase):
    instruction: str


class PracticePreview(PreviewBase):
    evaluator_id: str
    variant_id: str


class RubricPayload(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    code: str
    passed: bool
    detail_code: str


class FeedbackPreview(PreviewBase):
    outcome: str
    rubric: list[RubricPayload]


class PreviewReference(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    preview_id: str


class ExecutePayload(PreviewReference):
    consent_id: str


@router.post("/previews/explanation")
def preview_explanation(payload: ExplanationPreview, request: Request) -> dict[str, object]:
    service = _service(request)
    return _store(
        request,
        _consent_call(
            service.preview_explanation,
            locator_ids=tuple(payload.locator_ids),
            profile_id=payload.profile_id,
            instruction=payload.instruction,
            max_tokens=payload.max_tokens,
            max_cost_microusd=payload.max_cost_microusd,
            nonce=payload.nonce,
        ),
    )


@router.post("/previews/practice")
def preview_practice(payload: PracticePreview, request: Request) -> dict[str, object]:
    service = _service(request)
    return _store(
        request,
        _consent_call(
            service.preview_practice,
            locator_ids=tuple(payload.locator_ids),
            profile_id=payload.profile_id,
            evaluator_id=payload.evaluator_id,
            variant_id=payload.variant_id,
            max_tokens=payload.max_tokens,
            max_cost_microusd=payload.max_cost_microusd,
            nonce=payload.nonce,
        ),
    )


@router.post("/previews/feedback")
def preview_feedback(payload: FeedbackPreview, request: Request) -> dict[str, object]:
    service = _service(request)
    rubric = tuple(sorted((RubricItem(item.code, item.passed, item.detail_code) for item in payload.rubric), key=lambda item: item.code))
    return _store(
        request,
        _consent_call(
            service.preview_feedback,
            locator_ids=tuple(payload.locator_ids),
            profile_id=payload.profile_id,
            outcome=payload.outcome,
            rubric=rubric,
            max_tokens=payload.max_tokens,
            max_cost_microusd=payload.max_cost_microusd,
            nonce=payload.nonce,
        ),
    )


@router.post("/consents")
def grant_consent(payload: PreviewReference, request: Request) -> dict[str, object]:
    preview = _preview(request, payload.preview_id)
    try:
        return asdict(_service(request).grant(preview))
    except ConsentError as error:
        raise _api_error(error) from None
    except ProviderError as error:
        raise _provider_error(error) from None


@router.post("/execute")
def execute(payload: ExecutePayload, request: Request) -> dict[str, object]:
    preview = _preview(request, payload.preview_id)
    try:
        candidate = _service(request).execute(
            payload.consent_id,
            preview,
            request.app.state.provider_registry,
        )
    except ConsentError as error:
        raise _api_error(error) from None
    except ProviderError as error:
        raise _provider_error(error) from None
    return asdict(candidate)


def _store(request: Request, preview: ConsentPreview) -> dict[str, object]:
    preview_id = "preview-" + preview.request_hash
    request.app.state.provider_previews[preview_id] = preview
    return {
        "preview_id": preview_id,
        "operation": preview.operation,
        "profile_id": preview.profile_id,
        "adapter_id": preview.adapter_id,
        "model_id": preview.model_id,
        "policy_fingerprint": preview.policy_fingerprint,
        "config_fingerprint": preview.config_fingerprint,
        "input_token_cap": preview.input_token_cap,
        "max_tokens": preview.max_tokens,
        "max_cost_microusd": preview.max_cost_microusd,
        "sources": [asdict(source) for source in preview.request.sources],
    }


def _service(request: Request) -> ConsentService:
    return ConsentService(request.app.state.database, request.app.state.provider_registry)


def _preview(request: Request, preview_id: str) -> ConsentPreview:
    preview = request.app.state.provider_previews.get(preview_id)
    if not isinstance(preview, ConsentPreview):
        raise ApiError("preview_not_found", 404)
    return preview


def _consent_call(function, **kwargs):  # type: ignore[no-untyped-def]
    try:
        return function(**kwargs)
    except ConsentError as error:
        raise _api_error(error) from None
    except ProviderError as error:
        raise _provider_error(error) from None


def _provider_error(error: ProviderError) -> ApiError:
    return ApiError(error.code, 503, retryable=error.code in {"provider_timeout", "provider_error"})


def _api_error(error: ConsentError) -> ApiError:
    if error.code in {"consent_already_used", "consent_mismatch"}:
        return ApiError(error.code, 409)
    if error.code in {"consent_required", "provider_unconfigured"}:
        return ApiError(error.code, 403)
    if error.code in {"source_stale", "coverage_unconfirmed"}:
        return ApiError(error.code, 409)
    return ApiError(error.code, 400)
