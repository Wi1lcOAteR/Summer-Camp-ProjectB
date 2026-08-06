from __future__ import annotations

import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[3]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from projectb.domain.learning.evaluators.race import RaceEvaluator  # noqa: E402
from projectb.domain.learning.evaluators.registry import default_registry  # noqa: E402
from projectb.domain.learning.evaluators.schemas import (  # noqa: E402
    EvaluationRequest,
    RaceAnswer,
    RaceExercise,
    RaceStep,
)


def evaluate(steps: tuple[RaceStep, ...], answer: RaceAnswer):
    return RaceEvaluator().evaluate(
        EvaluationRequest(
            evaluator_id="os.race.v1",
            check_kind="transfer",
            variant_id="race-1",
            source_locator_ids=("locator-b", "locator-a"),
            exercise=RaceExercise(initial_value=0, steps=steps),
            answer=answer,
        )
    )


def test_lost_update_trace_detects_race_and_final_value_deterministically() -> None:
    steps = (
        RaceStep("a", "read", 0),
        RaceStep("b", "read", 0),
        RaceStep("a", "add", 1),
        RaceStep("a", "write", 1),
        RaceStep("b", "add", 1),
        RaceStep("b", "write", 1),
    )

    first = evaluate(steps, RaceAnswer(has_race=True, final_value=1))
    second = evaluate(steps, RaceAnswer(has_race=True, final_value=1))

    assert first == second
    assert first.outcome == "passed"
    assert first.source_locator_ids == ("locator-a", "locator-b")
    assert [item.code for item in first.rubric] == sorted(item.code for item in first.rubric)


def test_serial_updates_have_no_race_and_final_value_two() -> None:
    steps = (
        RaceStep("a", "read", 0),
        RaceStep("a", "add", 1),
        RaceStep("a", "write", 1),
        RaceStep("b", "read", 1),
        RaceStep("b", "add", 1),
        RaceStep("b", "write", 2),
    )

    assert evaluate(steps, RaceAnswer(has_race=False, final_value=2)).outcome == "passed"
    assert evaluate(steps, RaceAnswer(has_race=False, final_value=1)).outcome == "partial"
    assert evaluate(steps, RaceAnswer(has_race=True, final_value=1)).outcome == "incorrect"


@pytest.mark.parametrize(
    "steps",
    [
        (RaceStep("a", "add", 1),),
        (RaceStep("a", "read", 1),),
        (RaceStep("a", "read", 0), RaceStep("a", "write", 1)),
        (RaceStep("a", "read", 0), RaceStep("a", "add", 1)),
    ],
)
def test_invalid_or_incomplete_event_sequences_are_refused(steps: tuple[RaceStep, ...]) -> None:
    result = evaluate(steps, RaceAnswer(has_race=False, final_value=0))

    assert result.outcome == "refused"
    assert any(item.code == "trace_well_formed" and not item.passed for item in result.rubric)


def test_registry_contains_all_three_versioned_evaluators() -> None:
    registry = default_registry()

    assert [registry.get(evaluator_id).version for evaluator_id in ("os.mutex.v1", "os.race.v1", "os.deadlock.v1")] == [
        "1",
        "1",
        "1",
    ]
