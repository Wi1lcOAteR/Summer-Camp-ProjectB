from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from projectb.domain.learning.evaluators.deadlock import DeadlockEvaluator  # noqa: E402
from projectb.domain.learning.evaluators.schemas import (  # noqa: E402
    DeadlockAnswer,
    DeadlockExercise,
    EvaluationRequest,
    ResourceClaim,
)


def evaluate(exercise: DeadlockExercise, answer: DeadlockAnswer):
    return DeadlockEvaluator().evaluate(
        EvaluationRequest(
            evaluator_id="os.deadlock.v1",
            check_kind="isomorphic",
            variant_id="deadlock-1",
            source_locator_ids=("locator-a",),
            exercise=exercise,
            answer=answer,
        )
    )


def test_two_thread_hold_wait_cycle_is_detected_with_rotation_independent_answer() -> None:
    exercise = DeadlockExercise(
        holds=(ResourceClaim("thread-a", "lock-1"), ResourceClaim("thread-b", "lock-2")),
        waits=(ResourceClaim("thread-a", "lock-2"), ResourceClaim("thread-b", "lock-1")),
    )

    first = evaluate(exercise, DeadlockAnswer(has_deadlock=True, cycle=("thread-b", "thread-a")))
    second = evaluate(exercise, DeadlockAnswer(has_deadlock=True, cycle=("thread-a", "thread-b")))

    assert first == second
    assert first.outcome == "passed"
    assert [item.code for item in first.rubric] == sorted(item.code for item in first.rubric)


def test_acyclic_wait_chain_has_progress_and_no_deadlock() -> None:
    exercise = DeadlockExercise(
        holds=(ResourceClaim("thread-b", "lock-2"),),
        waits=(ResourceClaim("thread-a", "lock-2"), ResourceClaim("thread-b", "lock-3")),
    )

    assert evaluate(exercise, DeadlockAnswer(has_deadlock=False)).outcome == "passed"
    assert evaluate(exercise, DeadlockAnswer(has_deadlock=True, cycle=("thread-a", "thread-b"))).outcome == "incorrect"


def test_correct_classification_with_wrong_cycle_is_partial() -> None:
    exercise = DeadlockExercise(
        holds=(ResourceClaim("a", "r1"), ResourceClaim("b", "r2")),
        waits=(ResourceClaim("a", "r2"), ResourceClaim("b", "r1")),
    )

    assert evaluate(exercise, DeadlockAnswer(has_deadlock=True, cycle=("a",))).outcome == "partial"


def test_any_valid_cycle_is_accepted_when_graph_contains_multiple_cycles() -> None:
    exercise = DeadlockExercise(
        holds=(
            ResourceClaim("a", "r1"),
            ResourceClaim("b", "r2"),
            ResourceClaim("c", "r3"),
            ResourceClaim("d", "r4"),
        ),
        waits=(
            ResourceClaim("a", "r2"),
            ResourceClaim("b", "r1"),
            ResourceClaim("c", "r4"),
            ResourceClaim("d", "r3"),
        ),
    )

    assert evaluate(exercise, DeadlockAnswer(has_deadlock=True, cycle=("c", "d"))).outcome == "passed"


def test_duplicate_resource_holder_is_refused() -> None:
    exercise = DeadlockExercise(
        holds=(ResourceClaim("a", "r1"), ResourceClaim("b", "r1")),
        waits=(ResourceClaim("a", "r2"),),
    )

    result = evaluate(exercise, DeadlockAnswer(has_deadlock=False))
    assert result.outcome == "refused"
    assert any(item.code == "graph_well_formed" and not item.passed for item in result.rubric)
