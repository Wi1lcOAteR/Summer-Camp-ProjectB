from __future__ import annotations

import sys
from datetime import UTC, date, datetime
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[3]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from projectb.domain.review.planner import (  # noqa: E402
    PlannerError,
    ReviewPolicy,
    ReviewSeed,
)


NOW = datetime(2026, 8, 6, 8, tzinfo=UTC)


def seed(
    concept_id: str = "concept-1",
    *,
    mastery: str = "unknown",
    weakness: int = 2,
    requested_on: date = date(2026, 8, 6),
    eligibility: str = "ready",
    evidence: str = "evidence-1",
) -> ReviewSeed:
    return ReviewSeed(
        concept_id=concept_id,
        mastery_state=mastery,
        weakness=weakness,
        requested_local_date=requested_on,
        source_refs=(f"source-{concept_id}",),
        evidence_refs=(evidence,),
        eligibility=eligibility,
    )


@pytest.mark.parametrize(
    ("kwargs", "code"),
    [
        ({"mode": "weekly"}, "mode_invalid"),
        ({"timezone": "Mars/Olympus"}, "timezone_invalid"),
        ({"daily_budget_minutes": 5}, "budget_invalid"),
        ({"daily_budget_minutes": 11}, "budget_invalid"),
        ({"daily_budget_minutes": 125}, "budget_invalid"),
        ({"mode": "finals"}, "exam_date_required"),
    ],
)
def test_policy_rejects_invalid_mode_timezone_budget_and_missing_exam(kwargs: dict[str, object], code: str) -> None:
    with pytest.raises(PlannerError, match=code):
        ReviewPolicy(**kwargs)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("mastery", "expected"),
    [
        ("unknown", [1, 2, 4, 7, 15]),
        ("demonstrated_now", [1, 3, 6, 11, 23]),
        ("retained", [1, 3, 7, 14, 30]),
    ],
)
def test_finals_uses_exact_mastery_interval_tables(mastery: str, expected: list[int]) -> None:
    policy = ReviewPolicy(mode="finals", exam_date=date(2026, 9, 30), daily_budget_minutes=120)
    plan = policy.plan((seed(mastery=mastery),), generated_at=NOW)

    assert [(task.due_local_date - date(2026, 8, 6)).days for task in plan.tasks] == expected


def test_continuous_uses_base_intervals_and_default_budget() -> None:
    policy = ReviewPolicy()
    plan = policy.plan(tuple(seed(f"concept-{number}") for number in range(1, 6)), generated_at=NOW)

    first_day = [task for task in plan.tasks if task.due_local_date == date(2026, 8, 7)]
    assert policy.daily_budget_minutes == 30
    assert len(first_day) == 3
    assert {task.duration_minutes for task in plan.tasks} == {10}
    assert sorted({(task.due_local_date - date(2026, 8, 6)).days for task in plan.tasks}) == [1, 3, 7, 14, 30]


def test_duplicate_concept_day_keeps_weakest_evidence() -> None:
    policy = ReviewPolicy(daily_budget_minutes=120)
    strong = seed(weakness=1, evidence="strong")
    weak = seed(weakness=9, evidence="weak")

    plan = policy.plan((strong, weak), generated_at=NOW)

    assert len(plan.tasks) == 5
    assert all(task.weakness == 9 and task.evidence_refs == ("weak",) for task in plan.tasks)


def test_daily_budget_priority_is_weakness_then_request_date_then_concept_id() -> None:
    seeds = (
        seed("concept-z", weakness=5, requested_on=date(2026, 8, 5)),
        seed("concept-b", weakness=5, requested_on=date(2026, 8, 4)),
        seed("concept-a", weakness=5, requested_on=date(2026, 8, 4)),
        seed("concept-weak", weakness=8, requested_on=date(2026, 8, 6)),
    )

    first_day = ReviewPolicy(daily_budget_minutes=20).plan(seeds, generated_at=NOW).tasks[:2]

    assert [task.concept_id for task in first_day] == ["concept-weak", "concept-a"]


def test_stale_sources_and_system_errors_are_excluded_not_weakened() -> None:
    plan = ReviewPolicy().plan(
        (
            seed("ready", weakness=1),
            seed("stale", weakness=99, eligibility="stale_source"),
            seed("error", weakness=99, eligibility="system_error"),
        ),
        generated_at=NOW,
    )

    assert {task.concept_id for task in plan.tasks} == {"ready"}


def test_continuous_horizon_and_finals_cutoff_and_archive() -> None:
    continuous = ReviewPolicy(daily_budget_minutes=120).plan((seed(),), generated_at=NOW)
    assert max(task.due_local_date for task in continuous.tasks) == date(2026, 9, 5)

    finals = ReviewPolicy(
        mode="finals", exam_date=date(2026, 8, 10), daily_budget_minutes=120
    ).plan((seed(mastery="retained"),), generated_at=NOW)
    assert [task.due_local_date for task in finals.tasks] == [date(2026, 8, 7), date(2026, 8, 9)]
    assert finals.archived is False

    past = ReviewPolicy(mode="finals", exam_date=date(2026, 8, 5)).plan((seed(),), generated_at=NOW)
    assert past.archived is True
    assert past.tasks == ()


def test_normalized_input_order_produces_identical_hash_and_tasks() -> None:
    policy = ReviewPolicy(mode="finals", exam_date=date(2026, 9, 1), daily_budget_minutes=40)
    inputs = (seed("concept-b", evidence="b"), seed("concept-a", evidence="a"))

    first = policy.plan(inputs, generated_at=NOW)
    second = policy.plan(tuple(reversed(inputs)), generated_at=NOW)

    assert first == second
    assert len(first.input_hash) == 64
