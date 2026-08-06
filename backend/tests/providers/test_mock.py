from __future__ import annotations

import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[3]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from projectb.domain.learning.evaluators.schemas import RubricItem  # noqa: E402
from projectb.providers.mock import MockProvider  # noqa: E402
from projectb.providers.port import (  # noqa: E402
    ExplanationInput,
    FeedbackInput,
    PracticeInput,
    ProviderError,
    SourceFragment,
)
from projectb.providers.registry import ProviderRegistry, RegistryError  # noqa: E402


SOURCE = SourceFragment(
    locator_id="locator-1",
    material_version_id="version-1",
    content_hash="a" * 64,
    text="A mutex permits only one thread in the critical section.",
)


def test_mock_implements_exactly_three_deterministic_candidate_ports() -> None:
    provider = MockProvider()
    explanation = ExplanationInput((SOURCE,), "Explain mutex")
    practice = PracticeInput((SOURCE,), "os.mutex.v1", "variant-1")
    feedback = FeedbackInput(
        (SOURCE,),
        "passed",
        (RubricItem("mutual_exclusion", True, "holds"),),
    )

    assert provider.generate_explanation(explanation) == provider.generate_explanation(explanation)
    assert provider.generate_practice_candidate(practice) == provider.generate_practice_candidate(practice)
    assert provider.generate_feedback_wording(feedback) == provider.generate_feedback_wording(feedback)
    assert provider.network_count == 6
    assert explanation.sources[0].text in provider.last_request_text
    for candidate in (
        provider.generate_explanation(explanation),
        provider.generate_practice_candidate(practice),
        provider.generate_feedback_wording(feedback),
    ):
        assert candidate.authoritative is False


def test_feedback_contract_cannot_accept_the_original_answer() -> None:
    with pytest.raises(TypeError):
        FeedbackInput(  # type: ignore[call-arg]
            sources=(SOURCE,),
            outcome="passed",
            rubric=(),
            answer="student private answer",
        )


@pytest.mark.parametrize("mode", ["schema", "timeout", "error"])
def test_mock_failure_modes_are_stable(mode: str) -> None:
    provider = MockProvider(mode=mode)
    with pytest.raises(ProviderError, match=f"provider_{mode}"):
        provider.generate_explanation(ExplanationInput((SOURCE,), "Explain"))


def test_registry_local_has_zero_provider_and_rejects_mock() -> None:
    local = ProviderRegistry("local")
    assert local.resolve("profile-1") is None
    with pytest.raises(RegistryError, match="mock_not_allowed"):
        local.register("profile-1", MockProvider())

    demo = ProviderRegistry("demo")
    injected = MockProvider()
    demo.register("profile-1", injected)
    assert demo.resolve("profile-1") is injected
