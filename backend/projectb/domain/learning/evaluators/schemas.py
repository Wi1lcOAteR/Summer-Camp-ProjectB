from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


CheckKind = Literal["starting_probe", "isomorphic", "transfer", "delayed_variant"]
Outcome = Literal["incorrect", "partial", "passed", "refused", "source_insufficient", "skipped"]


@dataclass(frozen=True, slots=True)
class MutexEvent:
    thread_id: str
    action: Literal["enter", "exit"]

    def __post_init__(self) -> None:
        if not self.thread_id.strip():
            raise ValueError("thread_id_required")
        if self.action not in {"enter", "exit"}:
            raise ValueError("mutex_action_invalid")


@dataclass(frozen=True, slots=True)
class MutexExercise:
    events: tuple[MutexEvent, ...]


@dataclass(frozen=True, slots=True)
class MutexAnswer:
    holds: bool
    violation_index: int | None = None

    def __post_init__(self) -> None:
        if self.violation_index is not None and self.violation_index < 1:
            raise ValueError("violation_index_invalid")


@dataclass(frozen=True, slots=True)
class EvaluationRequest:
    evaluator_id: str
    check_kind: CheckKind
    variant_id: str
    source_locator_ids: tuple[str, ...]
    exercise: object
    answer: object

    def __post_init__(self) -> None:
        if not self.evaluator_id.strip():
            raise ValueError("evaluator_id_required")
        if self.check_kind not in {"starting_probe", "isomorphic", "transfer", "delayed_variant"}:
            raise ValueError("check_kind_invalid")
        if not self.variant_id.strip():
            raise ValueError("variant_id_required")
        normalized = tuple(sorted(set(self.source_locator_ids)))
        if not normalized or any(not locator.strip() for locator in normalized):
            raise ValueError("source_locator_required")
        object.__setattr__(self, "source_locator_ids", normalized)


@dataclass(frozen=True, slots=True)
class RubricItem:
    code: str
    passed: bool
    detail_code: str


@dataclass(frozen=True, slots=True)
class EvaluationResult:
    evaluator_id: str
    evaluator_version: str
    check_kind: CheckKind
    variant_id: str
    source_locator_ids: tuple[str, ...]
    outcome: Outcome
    rubric: tuple[RubricItem, ...]
