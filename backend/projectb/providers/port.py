from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal, Protocol, TypeAlias

from projectb.domain.learning.evaluators.schemas import Outcome, RubricItem


HASH_PATTERN = re.compile(r"^[0-9a-f]{64}$")


class ProviderError(RuntimeError):
    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


@dataclass(frozen=True, slots=True)
class ProviderBinding:
    adapter_id: str
    model_id: str
    input_token_cap: int
    output_token_cap: int
    max_cost_microusd: int
    credential_ref: str
    config_fingerprint: str
    policy_fingerprint: str


@dataclass(frozen=True, slots=True)
class SourceFragment:
    locator_id: str
    material_version_id: str
    content_hash: str
    text: str

    def __post_init__(self) -> None:
        if not self.locator_id.strip() or not self.material_version_id.strip():
            raise ValueError("source_identity_invalid")
        if HASH_PATTERN.fullmatch(self.content_hash) is None:
            raise ValueError("source_hash_invalid")
        if not self.text.strip():
            raise ValueError("source_text_empty")


def _validate_sources(sources: tuple[SourceFragment, ...]) -> None:
    if not sources or len({source.locator_id for source in sources}) != len(sources):
        raise ValueError("source_selection_invalid")


@dataclass(frozen=True, slots=True)
class ExplanationInput:
    sources: tuple[SourceFragment, ...]
    instruction: str

    def __post_init__(self) -> None:
        _validate_sources(self.sources)
        if not self.instruction.strip():
            raise ValueError("instruction_required")


@dataclass(frozen=True, slots=True)
class PracticeInput:
    sources: tuple[SourceFragment, ...]
    evaluator_id: str
    variant_id: str

    def __post_init__(self) -> None:
        _validate_sources(self.sources)
        if not self.evaluator_id.strip() or not self.variant_id.strip():
            raise ValueError("practice_identity_invalid")


@dataclass(frozen=True, slots=True)
class FeedbackInput:
    sources: tuple[SourceFragment, ...]
    outcome: Outcome
    rubric: tuple[RubricItem, ...]

    def __post_init__(self) -> None:
        _validate_sources(self.sources)
        if self.outcome not in {"incorrect", "partial", "passed", "refused", "source_insufficient", "skipped"}:
            raise ValueError("outcome_invalid")
        if tuple(sorted(self.rubric, key=lambda item: item.code)) != self.rubric:
            raise ValueError("rubric_order_invalid")


@dataclass(frozen=True, slots=True)
class ExplanationCandidate:
    text: str
    authoritative: Literal[False] = False


@dataclass(frozen=True, slots=True)
class PracticeCandidate:
    evaluator_id: str
    variant_id: str
    prompt: str
    authoritative: Literal[False] = False


@dataclass(frozen=True, slots=True)
class FeedbackCandidate:
    text: str
    authoritative: Literal[False] = False


ProviderInput: TypeAlias = ExplanationInput | PracticeInput | FeedbackInput
ProviderCandidate: TypeAlias = ExplanationCandidate | PracticeCandidate | FeedbackCandidate
ProviderOperation: TypeAlias = Literal[
    "generate_explanation",
    "generate_practice_candidate",
    "generate_feedback_wording",
]


class ProviderPort(Protocol):
    def generate_explanation(self, request: ExplanationInput) -> ExplanationCandidate: ...

    def generate_practice_candidate(self, request: PracticeInput) -> PracticeCandidate: ...

    def generate_feedback_wording(self, request: FeedbackInput) -> FeedbackCandidate: ...
