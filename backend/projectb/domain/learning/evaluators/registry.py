from __future__ import annotations

from projectb.domain.learning.evaluators.base import Evaluator
from projectb.domain.learning.evaluators.mutex import MutexEvaluator


class ExplanationOnlyError(RuntimeError):
    pass


class EvaluatorNotFoundError(LookupError):
    pass


class EvaluatorRegistry:
    def __init__(self, evaluators: tuple[Evaluator, ...]) -> None:
        self._evaluators = {evaluator.evaluator_id: evaluator for evaluator in evaluators}
        if len(self._evaluators) != len(evaluators):
            raise ValueError("duplicate_evaluator_id")

    def get(self, evaluator_id: str) -> Evaluator:
        try:
            return self._evaluators[evaluator_id]
        except KeyError:
            raise EvaluatorNotFoundError("evaluator_not_found") from None

    def for_concept(self, evaluator_id: str | None) -> Evaluator:
        if evaluator_id is None:
            raise ExplanationOnlyError("explanation_only")
        return self.get(evaluator_id)


def default_registry() -> EvaluatorRegistry:
    return EvaluatorRegistry((MutexEvaluator(),))
