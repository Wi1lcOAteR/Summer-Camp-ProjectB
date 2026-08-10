from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import httpx
import openai
import pytest


ROOT = Path(__file__).resolve().parents[3]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from projectb.domain.learning.evaluators.schemas import RubricItem  # noqa: E402
from projectb.providers.mock import MockProvider  # noqa: E402
from projectb.providers.openai_adapter import (  # noqa: E402
    OpenAIAdapter,
    load_provider_policy,
)
from projectb.providers.port import (  # noqa: E402
    ExplanationCandidate,
    ExplanationInput,
    FeedbackCandidate,
    FeedbackInput,
    PracticeCandidate,
    PracticeInput,
    ProviderError,
    SourceFragment,
)
from projectb.providers.registry import ProviderRegistry, RegistryError  # noqa: E402


POLICY_PATH = ROOT / "backend" / "projectb" / "providers" / "policy.v1.json"
EVIDENCE_PATH = ROOT / "docs" / "engineering" / "PROVIDER_POLICY_V1_P_EVIDENCE.md"
FRESH_NOW = datetime.fromisoformat("2026-08-09T12:00:00+08:00")
EXPECTED_EVIDENCE_HASH = "35a3f46e036563e3fc681df3190eb56336ab48b9d9817ad48f4d5df42230f076"
EXPECTED_REQUEST_FIELDS = {
    "background",
    "input",
    "instructions",
    "max_output_tokens",
    "model",
    "reasoning",
    "service_tier",
    "store",
    "text",
    "tools",
}

SOURCE = SourceFragment(
    locator_id="locator-1",
    material_version_id="version-1",
    content_hash="a" * 64,
    text="A mutex permits only one thread in the critical section.",
)


@dataclass
class CredentialProbe:
    reads: int = 0

    def read(self) -> str:
        self.reads += 1
        return "unit-test-credential"


def _completed_response(payload: dict[str, object]) -> httpx.Response:
    return httpx.Response(
        200,
        json={
            "id": "response-opaque",
            "object": "response",
            "created_at": 1,
            "model": "gpt-5.6-terra",
            "status": "completed",
            "output": [
                {
                    "id": "message-opaque",
                    "type": "message",
                    "role": "assistant",
                    "status": "completed",
                    "content": [
                        {
                            "type": "output_text",
                            "text": json.dumps(payload, separators=(",", ":")),
                            "annotations": [],
                        }
                    ],
                }
            ],
        },
    )


def _adapter(
    handler,
    *,
    credential: CredentialProbe | None = None,
    model_id: str = "gpt-5.6-terra",
    input_cap: int = 20_000,
    output_cap: int = 3_000,
    credential_configured: bool = True,
    now=lambda: FRESH_NOW,
    policy_path: Path = POLICY_PATH,
    evidence_path: Path = EVIDENCE_PATH,
) -> OpenAIAdapter:
    probe = credential or CredentialProbe()
    return OpenAIAdapter(
        model_id=model_id,
        input_token_cap=input_cap,
        output_token_cap=output_cap,
        credential_configured=credential_configured,
        credential_supplier=probe.read,
        transport=httpx.MockTransport(handler),
        policy_path=policy_path,
        evidence_path=evidence_path,
        utc_now=now,
    )


def test_policy_is_hash_bound_allowlisted_and_computes_exact_cost_ceiling() -> None:
    policy = load_provider_policy(POLICY_PATH, evidence_path=EVIDENCE_PATH, now=FRESH_NOW)

    assert policy.evidence_sha256 == EXPECTED_EVIDENCE_HASH
    assert len(policy.fingerprint) == 64
    assert policy.allowed_models == ("gpt-5.6-luna", "gpt-5.6-terra")
    assert policy.maximum_cost_microusd("gpt-5.6-terra", 20_000, 3_000) == 118_250
    assert policy.maximum_cost_microusd("gpt-5.6-luna", 20_000, 3_000) == 47_300
    assert policy.maximum_cost_microusd("gpt-5.6-terra", 1_000, 200) == 6_738


def test_local_registry_starts_in_l_and_only_accepts_configured_builtin_openai() -> None:
    local = ProviderRegistry("local")
    assert local.resolve("profile-p") is None

    with pytest.raises(RegistryError, match="mock_not_allowed"):
        local.register("profile-p", MockProvider())

    class ArbitraryProvider:
        def generate_explanation(self, request):  # type: ignore[no-untyped-def]
            raise AssertionError("not called")

        def generate_practice_candidate(self, request):  # type: ignore[no-untyped-def]
            raise AssertionError("not called")

        def generate_feedback_wording(self, request):  # type: ignore[no-untyped-def]
            raise AssertionError("not called")

    with pytest.raises(RegistryError, match="dynamic_adapter_not_allowed"):
        local.register("profile-p", ArbitraryProvider())

    valid = _adapter(lambda request: _completed_response({"text": "unused"}))
    local.register("profile-p", valid)
    assert local.resolve("profile-p") is valid
    assert valid.maximum_cost_microusd == 118_250


def test_local_registry_rejects_openai_subclasses_as_dynamic_adapters() -> None:
    class DerivedOpenAIAdapter(OpenAIAdapter):
        pass

    derived = DerivedOpenAIAdapter(
        model_id="gpt-5.6-terra",
        input_token_cap=20_000,
        output_token_cap=3_000,
        credential_configured=True,
        credential_supplier=lambda: "unit-test-credential",
        transport=httpx.MockTransport(lambda request: _completed_response({"text": "unused"})),
        policy_path=POLICY_PATH,
        evidence_path=EVIDENCE_PATH,
        utc_now=lambda: FRESH_NOW,
    )

    with pytest.raises(RegistryError, match="dynamic_adapter_not_allowed"):
        ProviderRegistry("local").register("profile-p", derived)


@pytest.mark.parametrize("environment", ["", "LOCAL", "production"])
def test_registry_rejects_unknown_runtime_environments(environment: str) -> None:
    with pytest.raises(RegistryError, match="environment_invalid"):
        ProviderRegistry(environment)  # type: ignore[arg-type]


def test_registry_rejects_duplicate_profile_without_replacing_original() -> None:
    registry = ProviderRegistry("local")
    original = _adapter(lambda request: _completed_response({"text": "original"}))
    replacement = _adapter(lambda request: _completed_response({"text": "replacement"}))
    registry.register("profile-p", original)

    with pytest.raises(RegistryError, match="profile_already_registered"):
        registry.register("profile-p", replacement)
    assert registry.resolve("profile-p") is original


@pytest.mark.parametrize(
    ("overrides", "code"),
    [
        ({"credential_configured": False}, "credential_unconfigured"),
        ({"model_id": "unreviewed-model"}, "model_not_allowed"),
        ({"input_cap": 20_001}, "input_cap_invalid"),
        ({"output_cap": 3_001}, "output_cap_invalid"),
    ],
)
def test_local_registry_rejects_unreviewed_openai_configuration(overrides: dict[str, Any], code: str) -> None:
    adapter = _adapter(lambda request: _completed_response({"text": "unused"}), **overrides)

    with pytest.raises(RegistryError, match=code):
        ProviderRegistry("local").register("profile-p", adapter)


def test_three_ports_send_only_exact_governed_responses_payloads() -> None:
    seen: list[tuple[httpx.Request, dict[str, object]]] = []
    responses = iter(
        [
            {"text": "Mutex serializes critical-section entry."},
            {"prompt": "Which event ordering preserves mutual exclusion?"},
            {"text": "Review the overlapping critical-section events."},
        ]
    )

    def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        seen.append((request, body))
        return _completed_response(next(responses))

    credential = CredentialProbe()
    adapter = _adapter(handler, credential=credential)
    explanation = adapter.generate_explanation(ExplanationInput((SOURCE,), "Explain the invariant."))
    practice = adapter.generate_practice_candidate(PracticeInput((SOURCE,), "os.mutex.v1", "variant-1"))
    feedback = adapter.generate_feedback_wording(
        FeedbackInput((SOURCE,), "partial", (RubricItem("mutual_exclusion", False, "overlap"),))
    )

    assert explanation == ExplanationCandidate("Mutex serializes critical-section entry.")
    assert practice == PracticeCandidate(
        "os.mutex.v1",
        "variant-1",
        "Which event ordering preserves mutual exclusion?",
    )
    assert feedback == FeedbackCandidate("Review the overlapping critical-section events.")
    assert credential.reads == 3
    assert len(seen) == 3

    for request, body in seen:
        assert request.method == "POST"
        assert str(request.url) == "https://api.openai.com/v1/responses"
        assert set(body) == EXPECTED_REQUEST_FIELDS
        assert body["model"] == "gpt-5.6-terra"
        assert body["store"] is False
        assert body["background"] is False
        assert body["tools"] == []
        assert body["service_tier"] == "default"
        assert body["reasoning"] == {"effort": "low"}
        assert body["max_output_tokens"] == 3_000
        assert body["text"]["format"]["type"] == "json_schema"  # type: ignore[index]
        assert body["text"]["format"]["strict"] is True  # type: ignore[index]
        assert body["text"]["format"]["schema"]["additionalProperties"] is False  # type: ignore[index]
        assert request.extensions["timeout"] == {
            "connect": 60.0,
            "read": 60.0,
            "write": 60.0,
            "pool": 60.0,
        }
        serialized = json.dumps(body, ensure_ascii=False)
        assert SOURCE.text in serialized
        assert "input_file" not in serialized
        assert "input_image" not in serialized
        assert "file_id" not in serialized
        assert "file_data" not in serialized
        assert "previous_response_id" not in serialized

    feedback_body = seen[2][1]
    assert "overlap" in str(feedback_body["input"])
    assert "student answer" not in json.dumps(feedback_body).lower()


def test_openai_sdk_drives_responses_with_injected_http_zero_retries_and_sixty_seconds(monkeypatch) -> None:
    constructed: list[dict[str, object]] = []
    requests: list[httpx.Request] = []
    real_openai = openai.OpenAI

    def observe_openai(**kwargs):  # type: ignore[no-untyped-def]
        constructed.append(kwargs)
        return real_openai(**kwargs)

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return _completed_response({"text": "SDK candidate"})

    monkeypatch.setattr(openai, "OpenAI", observe_openai)
    http_client = httpx.Client(
        transport=httpx.MockTransport(handler),
        timeout=httpx.Timeout(60.0),
        follow_redirects=False,
    )
    try:
        adapter = OpenAIAdapter(
            model_id="gpt-5.6-terra",
            input_token_cap=20_000,
            output_token_cap=3_000,
            credential_configured=True,
            credential_supplier=lambda: "unit-test-credential",
            http_client=http_client,
            policy_path=POLICY_PATH,
            evidence_path=EVIDENCE_PATH,
            utc_now=lambda: FRESH_NOW,
        )
        assert adapter.generate_explanation(ExplanationInput((SOURCE,), "Explain.")) == ExplanationCandidate(
            "SDK candidate"
        )
    finally:
        http_client.close()

    assert len(constructed) == 1
    assert constructed[0]["http_client"] is http_client
    assert constructed[0]["max_retries"] == 0
    assert constructed[0]["timeout"] == 60.0
    assert str(constructed[0]["base_url"]) == "https://api.openai.com/v1"
    assert len(requests) == 1
    assert requests[0].url.path == "/v1/responses"
    assert requests[0].headers["x-stainless-lang"] == "python"
    assert requests[0].headers["x-stainless-retry-count"] == "0"


@pytest.mark.parametrize(
    ("response", "code"),
    [
        (httpx.Response(200, json={"status": "incomplete", "output": []}), "provider_incomplete"),
        (
            httpx.Response(
                200,
                json={
                    "status": "completed",
                    "output": [
                        {
                            "type": "message",
                            "content": [{"type": "refusal", "refusal": "Cannot comply"}],
                        }
                    ],
                },
            ),
            "provider_refusal",
        ),
        (_completed_response({"text": "ok", "unexpected": True}), "provider_schema"),
        (httpx.Response(503, json={"error": {"message": "redacted upstream"}}), "provider_error"),
    ],
)
def test_response_failures_are_non_authoritative_and_never_retried(response: httpx.Response, code: str) -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        return response

    with pytest.raises(ProviderError, match=code):
        _adapter(handler).generate_explanation(ExplanationInput((SOURCE,), "Explain."))
    assert calls == 1


def test_timeout_is_one_attempt_with_stable_error() -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        raise httpx.ReadTimeout("simulated", request=request)

    with pytest.raises(ProviderError, match="provider_timeout"):
        _adapter(handler).generate_explanation(ExplanationInput((SOURCE,), "Explain."))
    assert calls == 1


def test_stale_policy_fails_before_credential_read_or_network() -> None:
    now = [FRESH_NOW]
    calls = 0
    credential = CredentialProbe()

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        return _completed_response({"text": "must not be returned"})

    adapter = _adapter(handler, credential=credential, now=lambda: now[0])
    now[0] = datetime.fromisoformat("2026-08-25T00:00:00+08:00")

    with pytest.raises(ProviderError, match="provider_unavailable"):
        adapter.generate_explanation(ExplanationInput((SOURCE,), "Explain."))
    assert credential.reads == 0
    assert calls == 0


def test_missing_or_changed_evidence_fails_before_credential_or_network(tmp_path: Path) -> None:
    changed_evidence = tmp_path / "evidence.md"
    changed_evidence.write_text("not the reviewed evidence", encoding="utf-8")
    missing_policy = tmp_path / "missing-policy.json"

    for policy_path, evidence_path in (
        (POLICY_PATH, changed_evidence),
        (missing_policy, EVIDENCE_PATH),
    ):
        calls = 0
        credential = CredentialProbe()

        def handler(request: httpx.Request) -> httpx.Response:
            nonlocal calls
            calls += 1
            return _completed_response({"text": "must not be returned"})

        adapter = _adapter(
            handler,
            credential=credential,
            policy_path=policy_path,
            evidence_path=evidence_path,
        )
        with pytest.raises(ProviderError, match="provider_unavailable"):
            adapter.generate_explanation(ExplanationInput((SOURCE,), "Explain."))
        assert credential.reads == 0
        assert calls == 0


@pytest.mark.parametrize(
    ("section", "field", "value"),
    [
        (("evidence",), "expires_at", "2026-09-25T00:00:00+08:00"),
        (("models", "gpt-5.6-terra"), "input_rate_per_million_usd", "0.01"),
    ],
)
def test_policy_expiry_or_pricing_drift_fails_closed(
    tmp_path: Path,
    section: tuple[str, ...],
    field: str,
    value: str,
) -> None:
    document = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
    target = document
    for part in section:
        target = target[part]
    target[field] = value
    changed_policy = tmp_path / "policy.v1.json"
    changed_policy.write_text(json.dumps(document), encoding="utf-8")

    with pytest.raises(ProviderError, match="provider_unavailable"):
        load_provider_policy(changed_policy, evidence_path=EVIDENCE_PATH, now=FRESH_NOW)


def test_oversize_input_fails_before_credential_or_network() -> None:
    calls = 0
    credential = CredentialProbe()

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        return _completed_response({"text": "must not be returned"})

    adapter = _adapter(handler, credential=credential, input_cap=20)
    oversized = SourceFragment("locator-long", "version-1", "b" * 64, "x" * 100)

    with pytest.raises(ProviderError, match="provider_input_too_large"):
        adapter.generate_explanation(ExplanationInput((oversized,), "Explain."))
    assert credential.reads == 0
    assert calls == 0


def test_complete_billed_input_respects_cap_before_credential_or_network() -> None:
    calls = 0
    credential = CredentialProbe()

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        return _completed_response({"text": "must not be returned"})

    adapter = _adapter(handler, credential=credential, input_cap=500)

    with pytest.raises(ProviderError, match="provider_input_too_large"):
        adapter.generate_explanation(ExplanationInput((SOURCE,), "Explain the invariant."))
    assert credential.reads == 0
    assert calls == 0
