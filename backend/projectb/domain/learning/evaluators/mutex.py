from __future__ import annotations

from projectb.domain.learning.evaluators.schemas import (
    EvaluationRequest,
    EvaluationResult,
    MutexAnswer,
    MutexExercise,
    Outcome,
    RubricItem,
)


class MutexEvaluator:
    evaluator_id = "os.mutex.v1"
    version = "1"

    def evaluate(self, request: EvaluationRequest) -> EvaluationResult:
        if request.evaluator_id != self.evaluator_id:
            raise ValueError("evaluator_mismatch")
        if not isinstance(request.exercise, MutexExercise) or not isinstance(request.answer, MutexAnswer):
            raise ValueError("mutex_schema_invalid")

        active: set[str] = set()
        well_formed = bool(request.exercise.events)
        first_conflict: int | None = None
        for index, event in enumerate(request.exercise.events, start=1):
            if event.action == "enter":
                if event.thread_id in active:
                    well_formed = False
                    continue
                if active and first_conflict is None:
                    first_conflict = index
                active.add(event.thread_id)
            elif event.thread_id not in active:
                well_formed = False
            else:
                active.remove(event.thread_id)
        if active:
            well_formed = False

        holds = first_conflict is None
        classification_matches = request.answer.holds == holds
        witness_matches = (
            request.answer.violation_index is None
            if holds
            else request.answer.violation_index == first_conflict
        )
        rubric = tuple(
            sorted(
                (
                    RubricItem("classification_matches", classification_matches, "classification_checked"),
                    RubricItem("trace_well_formed", well_formed, "trace_checked"),
                    RubricItem("witness_matches", witness_matches, "first_conflict_checked"),
                ),
                key=lambda item: item.code,
            )
        )
        outcome: Outcome
        if not well_formed:
            outcome = "refused"
        elif classification_matches and witness_matches:
            outcome = "passed"
        elif classification_matches:
            outcome = "partial"
        else:
            outcome = "incorrect"
        return EvaluationResult(
            evaluator_id=self.evaluator_id,
            evaluator_version=self.version,
            check_kind=request.check_kind,
            variant_id=request.variant_id,
            source_locator_ids=request.source_locator_ids,
            outcome=outcome,
            rubric=rubric,
        )
