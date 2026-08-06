from __future__ import annotations

import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[3]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from projectb.domain.learning.evaluators.mutex import MutexEvaluator  # noqa: E402
from projectb.domain.learning.evaluators.registry import (  # noqa: E402
    ExplanationOnlyError,
    default_registry,
)
from projectb.domain.learning.evaluators.schemas import (  # noqa: E402
    EvaluationRequest,
    MutexAnswer,
    MutexEvent,
    MutexExercise,
)


def request(events: tuple[MutexEvent, ...], answer: MutexAnswer, sources: tuple[str, ...]) -> EvaluationRequest:
    return EvaluationRequest(
        evaluator_id="os.mutex.v1",
        check_kind="isomorphic",
        variant_id="mutex-variant-1",
        source_locator_ids=sources,
        exercise=MutexExercise(events),
        answer=answer,
    )


def test_valid_mutex_trace_passes_with_stable_sorted_rubric() -> None:
    evaluator = MutexEvaluator()
    evaluation = request(
        (
            MutexEvent("thread-a", "enter"),
            MutexEvent("thread-a", "exit"),
            MutexEvent("thread-b", "enter"),
            MutexEvent("thread-b", "exit"),
        ),
        MutexAnswer(holds=True),
        ("locator-b", "locator-a"),
    )

    first = evaluator.evaluate(evaluation)
    second = evaluator.evaluate(evaluation)

    assert first == second
    assert first.outcome == "passed"
    assert first.source_locator_ids == ("locator-a", "locator-b")
    assert [item.code for item in first.rubric] == sorted(item.code for item in first.rubric)
    assert all(item.passed for item in first.rubric)


def test_violation_requires_correct_first_conflict_witness() -> None:
    evaluator = MutexEvaluator()
    events = (
        MutexEvent("thread-a", "enter"),
        MutexEvent("thread-b", "enter"),
        MutexEvent("thread-a", "exit"),
        MutexEvent("thread-b", "exit"),
    )

    passed = evaluator.evaluate(request(events, MutexAnswer(holds=False, violation_index=2), ("locator-a",)))
    partial = evaluator.evaluate(request(events, MutexAnswer(holds=False, violation_index=3), ("locator-a",)))
    incorrect = evaluator.evaluate(request(events, MutexAnswer(holds=True), ("locator-a",)))

    assert passed.outcome == "passed"
    assert partial.outcome == "partial"
    assert incorrect.outcome == "incorrect"
    assert passed.rubric[-1].code == "witness_matches"


@pytest.mark.parametrize(
    "events",
    [
        (MutexEvent("thread-a", "exit"),),
        (MutexEvent("thread-a", "enter"), MutexEvent("thread-a", "enter")),
        (MutexEvent("thread-a", "enter"),),
    ],
)
def test_malformed_or_incomplete_trace_is_refused(events: tuple[MutexEvent, ...]) -> None:
    result = MutexEvaluator().evaluate(request(events, MutexAnswer(holds=True), ("locator-a",)))

    assert result.outcome == "refused"
    assert any(item.code == "trace_well_formed" and not item.passed for item in result.rubric)


def test_registry_is_versioned_and_explanation_only_is_blocked() -> None:
    registry = default_registry()

    assert registry.get("os.mutex.v1").version == "1"
    with pytest.raises(ExplanationOnlyError, match="explanation_only"):
        registry.for_concept(None)


def test_source_binding_is_required_deduplicated_and_order_independent() -> None:
    events = (MutexEvent("thread-a", "enter"), MutexEvent("thread-a", "exit"))
    evaluator = MutexEvaluator()

    ordered = evaluator.evaluate(request(events, MutexAnswer(holds=True), ("locator-a", "locator-b")))
    shuffled = evaluator.evaluate(
        request(events, MutexAnswer(holds=True), ("locator-b", "locator-a", "locator-a"))
    )

    assert ordered == shuffled
    with pytest.raises(ValueError, match="source_locator_required"):
        request(events, MutexAnswer(holds=True), ())
