from __future__ import annotations

from dataclasses import dataclass

from projectb.domain.learning.evaluators.schemas import (
    EvaluationRequest,
    EvaluationResult,
    Outcome,
    RaceAnswer,
    RaceExercise,
    RubricItem,
)


@dataclass(slots=True)
class _Transaction:
    phase: str
    local_value: int


class RaceEvaluator:
    evaluator_id = "os.race.v1"
    version = "1"

    def evaluate(self, request: EvaluationRequest) -> EvaluationResult:
        if request.evaluator_id != self.evaluator_id:
            raise ValueError("evaluator_mismatch")
        if not isinstance(request.exercise, RaceExercise) or not isinstance(request.answer, RaceAnswer):
            raise ValueError("race_schema_invalid")

        shared = request.exercise.initial_value
        transactions: dict[str, _Transaction] = {}
        well_formed = bool(request.exercise.steps)
        has_race = False
        for step in request.exercise.steps:
            transaction = transactions.get(step.thread_id)
            if step.action == "read":
                if transaction is not None or step.value != shared:
                    well_formed = False
                    continue
                if transactions:
                    has_race = True
                transactions[step.thread_id] = _Transaction("read", step.value)
            elif step.action == "add":
                if transaction is None or transaction.phase != "read":
                    well_formed = False
                    continue
                transaction.local_value += step.value
                transaction.phase = "add"
            elif transaction is None or transaction.phase != "add" or step.value != transaction.local_value:
                well_formed = False
            else:
                shared = step.value
                del transactions[step.thread_id]
        if transactions:
            well_formed = False

        race_matches = request.answer.has_race == has_race
        final_matches = request.answer.final_value == shared
        rubric = tuple(
            sorted(
                (
                    RubricItem("final_value_matches", final_matches, "final_value_replayed"),
                    RubricItem("race_classification_matches", race_matches, "overlap_checked"),
                    RubricItem("trace_well_formed", well_formed, "read_add_write_checked"),
                ),
                key=lambda item: item.code,
            )
        )
        outcome: Outcome
        if not well_formed:
            outcome = "refused"
        elif race_matches and final_matches:
            outcome = "passed"
        elif race_matches or final_matches:
            outcome = "partial"
        else:
            outcome = "incorrect"
        return EvaluationResult(
            self.evaluator_id,
            self.version,
            request.check_kind,
            request.variant_id,
            request.source_locator_ids,
            outcome,
            rubric,
        )
