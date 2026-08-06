from __future__ import annotations

from typing import Protocol

from projectb.domain.learning.evaluators.schemas import EvaluationRequest, EvaluationResult


class Evaluator(Protocol):
    evaluator_id: str
    version: str

    def evaluate(self, request: EvaluationRequest) -> EvaluationResult: ...
