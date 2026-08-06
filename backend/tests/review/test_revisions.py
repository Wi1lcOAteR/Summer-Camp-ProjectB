from __future__ import annotations

import sys
from datetime import UTC, date, datetime
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[3]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from projectb.domain.review.planner import ReviewPolicy, ReviewSeed  # noqa: E402
from projectb.services.review.revisions import RevisionError, RevisionService  # noqa: E402
from projectb.storage.db import Database  # noqa: E402


NOW = datetime(2026, 8, 6, 8, tzinfo=UTC)


def setup_database(tmp_path: Path) -> Database:
    database = Database(tmp_path / "projectb.sqlite3")
    database.initialize()
    connection = database.connect()
    try:
        connection.execute(
            "INSERT INTO course(course_id, name, timezone, created_at) VALUES ('course-1', 'OS', 'UTC', ?)",
            ("2026-08-06T00:00:00Z",),
        )
        for number in range(1, 5):
            connection.execute(
                "INSERT INTO knowledge_concept(concept_id, course_id, name, evaluator_id, version, state, created_at) "
                "VALUES (?, 'course-1', ?, 'os.mutex.v1', 1, 'active', ?)",
                (f"concept-{number}", f"Concept {number}", "2026-08-06T00:00:00Z"),
            )
    finally:
        connection.close()
    return database


def seed(concept_id: str = "concept-1", *, evidence: str = "evidence-1", eligibility: str = "ready") -> ReviewSeed:
    return ReviewSeed(
        concept_id=concept_id,
        mastery_state="unknown",
        weakness=2,
        requested_local_date=date(2026, 8, 6),
        source_refs=(f"source-{concept_id}",),
        evidence_refs=(evidence,),
        eligibility=eligibility,  # type: ignore[arg-type]
    )


def test_equal_input_hash_returns_existing_revision(tmp_path: Path) -> None:
    database = setup_database(tmp_path)
    service = RevisionService(database)
    policy = ReviewPolicy()

    first = service.generate("course-1", policy, (seed(),), generated_at=NOW)
    second = service.generate("course-1", policy, (seed(),), generated_at=NOW)

    assert first == second
    connection = database.connect()
    try:
        assert connection.execute("SELECT count(*) FROM review_plan_revision").fetchone()[0] == 1
        assert connection.execute("SELECT count(*) FROM review_task").fetchone()[0] == 5
    finally:
        connection.close()


def test_changed_input_appends_parent_revision_and_stable_diff(tmp_path: Path) -> None:
    database = setup_database(tmp_path)
    service = RevisionService(database)
    inputs = tuple(seed(f"concept-{number}", evidence=f"e-{number}") for number in range(1, 5))
    first = service.generate("course-1", ReviewPolicy(daily_budget_minutes=20), inputs, generated_at=NOW)
    second = service.generate("course-1", ReviewPolicy(daily_budget_minutes=30), inputs, generated_at=NOW)

    assert second.parent_revision_id == first.revision_id
    assert second.diff.added
    assert second.diff == service.diff(first.revision_id, second.revision_id)


def test_same_task_slot_with_changed_evidence_is_reported_as_changed(tmp_path: Path) -> None:
    service = RevisionService(setup_database(tmp_path))
    first = service.generate("course-1", ReviewPolicy(), (seed(evidence="old"),), generated_at=NOW)
    second = service.generate("course-1", ReviewPolicy(), (seed(evidence="new"),), generated_at=NOW)

    assert second.diff.added == ()
    assert second.diff.removed == ()
    assert len(second.diff.changed) == len(first.tasks)
    assert second.diff.retained == ()


def test_completed_task_is_preserved_and_not_recreated_in_new_revision(tmp_path: Path) -> None:
    database = setup_database(tmp_path)
    service = RevisionService(database)
    first = service.generate("course-1", ReviewPolicy(), (seed(),), generated_at=NOW)
    completed = first.tasks[0]
    service.complete_task(completed.task_id, completed_at="2026-08-07T09:00:00Z")

    second = service.generate(
        "course-1",
        ReviewPolicy(),
        (seed(evidence="evidence-new"),),
        generated_at=NOW,
    )

    assert (completed.concept_id, completed.due_local_date) not in {
        (task.concept_id, task.due_local_date) for task in second.tasks
    }
    connection = database.connect()
    try:
        row = connection.execute(
            "SELECT status, completed_at FROM review_task WHERE task_id = ?", (completed.task_id,)
        ).fetchone()
        assert tuple(row) == ("completed", "2026-08-07T09:00:00Z")
    finally:
        connection.close()


def test_skipped_task_can_recover_but_completed_task_cannot(tmp_path: Path) -> None:
    service = RevisionService(setup_database(tmp_path))
    revision = service.generate("course-1", ReviewPolicy(), (seed(),), generated_at=NOW)
    task = revision.tasks[0]

    service.skip_task(task.task_id)
    assert service.recover_task(task.task_id).status == "pending"
    service.complete_task(task.task_id, completed_at="2026-08-07T09:00:00Z")
    with pytest.raises(RevisionError, match="completed_task_immutable"):
        service.recover_task(task.task_id)


def test_stale_source_creates_revision_that_removes_future_tasks(tmp_path: Path) -> None:
    service = RevisionService(setup_database(tmp_path))
    first = service.generate("course-1", ReviewPolicy(), (seed(),), generated_at=NOW)
    second = service.generate(
        "course-1",
        ReviewPolicy(),
        (seed(eligibility="stale_source"),),
        generated_at=NOW,
    )

    assert second.tasks == ()
    assert len(second.diff.removed) == len(first.tasks)
    assert second.parent_revision_id == first.revision_id
