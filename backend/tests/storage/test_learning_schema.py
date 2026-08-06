"""F-03 contract for append-only learning and review-plan persistence."""

from __future__ import annotations

import importlib.util
import sqlite3
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[3]


def load_database_module():
    path = ROOT / "backend/projectb/storage/db.py"
    spec = importlib.util.spec_from_file_location("projectb_db", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def database(tmp_path: Path):
    module = load_database_module()
    value = module.Database(tmp_path / "projectb.sqlite3")
    value.initialize()
    return value


def seed_course_and_concept(connection: sqlite3.Connection) -> None:
    connection.execute(
        "INSERT INTO course(course_id, name, timezone, created_at) VALUES (?, ?, ?, ?)",
        ("course-1", "Concurrency", "Asia/Shanghai", "2026-08-06T00:00:00Z"),
    )
    connection.execute(
        "INSERT INTO knowledge_concept(concept_id, course_id, name, evaluator_id, version, state, created_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        ("concept-1", "course-1", "mutex", "mutex-v1", 1, "active", "2026-08-06T00:00:00Z"),
    )


def insert_revision(
    connection: sqlite3.Connection,
    revision_id: str,
    course_id: str = "course-1",
    *,
    mode: str = "continuous",
    exam_date: str | None = None,
    input_hash: str = "d" * 64,
    parent_revision_id: str | None = None,
    budget_minutes: int = 60,
) -> None:
    connection.execute(
        "INSERT INTO review_plan_revision(revision_id, course_id, mode, timezone, budget_minutes, exam_date, "
        "input_hash, parent_revision_id, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            revision_id,
            course_id,
            mode,
            "Asia/Shanghai",
            budget_minutes,
            exam_date,
            input_hash,
            parent_revision_id,
            "2026-08-06T00:00:00Z",
        ),
    )


def test_learning_migration_is_ordered_and_idempotent(tmp_path: Path) -> None:
    value = database(tmp_path)
    value.initialize()
    connection = value.connect()
    try:
        assert [row[0] for row in connection.execute("SELECT migration_id FROM schema_migrations ORDER BY migration_id")] == [
            "001_core",
            "002_learning",
        ]
        tables = {
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%'"
            )
        }
        assert {
            "attempt",
            "learning_evidence",
            "mastery_estimate",
            "review_plan_revision",
            "review_task",
        } <= tables
    finally:
        connection.close()


def test_learning_evidence_is_append_only_and_idempotent(tmp_path: Path) -> None:
    value = database(tmp_path)
    connection = value.connect()
    try:
        seed_course_and_concept(connection)
        connection.execute(
            "INSERT INTO attempt(attempt_id, attempt_key, concept_id, check_kind, variant_id, answer_json, status, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ("attempt-1", "attempt-key-1", "concept-1", "isomorphic", "mutex-basic", "{}", "evaluated", "2026-08-06T00:00:00Z", "2026-08-06T00:00:00Z"),
        )
        for attempt_id, attempt_key, check_kind in (
            ("attempt-duplicate", "attempt-key-1", "transfer"),
            ("attempt-invalid-kind", "attempt-key-2", "freeform"),
        ):
            with pytest.raises(sqlite3.IntegrityError):
                connection.execute(
                    "INSERT INTO attempt(attempt_id, attempt_key, concept_id, check_kind, variant_id, answer_json, status, created_at, updated_at) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (attempt_id, attempt_key, "concept-1", check_kind, "variant", "{}", "submitted", "2026-08-06T00:00:00Z", "2026-08-06T00:00:00Z"),
                )
        evidence = (
            "evidence-1", "attempt-1", "course-1", "concept-1", "mutex-v1", "1",
            "isomorphic", "passed", "{}", "[]", 1, "idem-1", "2026-08-06T00:00:00Z",
        )
        connection.execute(
            "INSERT INTO learning_evidence(evidence_id, attempt_id, course_id, concept_id, evaluator_id, evaluator_version, "
            "check_kind, outcome, rubric_json, source_ids_json, evidence_version, idempotency_key, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            evidence,
        )
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute(
                "INSERT INTO learning_evidence(evidence_id, attempt_id, course_id, concept_id, evaluator_id, evaluator_version, "
                "check_kind, outcome, rubric_json, source_ids_json, evidence_version, idempotency_key, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                ("evidence-2", *evidence[1:11], "idem-1", evidence[-1]),
            )
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute(
                "INSERT INTO learning_evidence(evidence_id, attempt_id, course_id, concept_id, evaluator_id, evaluator_version, "
                "check_kind, outcome, rubric_json, source_ids_json, evidence_version, idempotency_key, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                ("evidence-same-attempt", *evidence[1:11], "idem-2", evidence[-1]),
            )
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute(
                "INSERT INTO learning_evidence(evidence_id, attempt_id, course_id, concept_id, evaluator_id, evaluator_version, "
                "check_kind, outcome, rubric_json, source_ids_json, evidence_version, idempotency_key, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                ("evidence-invalid-time", *evidence[1:11], "idem-invalid-time", "not-a-dateZ"),
            )
        for field, value in (("check_kind", "unknown_check"), ("outcome", "unknown_outcome")):
            with pytest.raises(sqlite3.IntegrityError):
                connection.execute(
                    "INSERT INTO learning_evidence(evidence_id, attempt_id, course_id, concept_id, evaluator_id, evaluator_version, "
                    "check_kind, outcome, rubric_json, source_ids_json, evidence_version, idempotency_key, created_at) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (f"evidence-invalid-{field}", *evidence[1:6],
                     value if field == "check_kind" else evidence[6],
                     value if field == "outcome" else evidence[7], evidence[8], evidence[9], evidence[10],
                     f"idem-invalid-{field}", evidence[-1]),
                )
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute("UPDATE learning_evidence SET outcome = 'incorrect' WHERE evidence_id = 'evidence-1'")
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute("DELETE FROM learning_evidence WHERE evidence_id = 'evidence-1'")
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute("DELETE FROM attempt WHERE attempt_id = 'attempt-1'")
    finally:
        connection.close()


def test_mastery_estimates_are_hash_bound_derived_snapshots(tmp_path: Path) -> None:
    value = database(tmp_path)
    connection = value.connect()
    try:
        seed_course_and_concept(connection)
        connection.execute(
            "INSERT INTO mastery_estimate(estimate_id, concept_id, derived_state, evidence_input_hash, created_at) "
            "VALUES (?, ?, ?, ?, ?)",
            ("estimate-1", "concept-1", "demonstrated_now", "c" * 64, "2026-08-06T00:00:00Z"),
        )
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute(
                "INSERT INTO mastery_estimate(estimate_id, concept_id, derived_state, evidence_input_hash, created_at) "
                "VALUES (?, ?, ?, ?, ?)",
                ("estimate-2", "concept-1", "demonstrated_now", "c" * 64, "2026-08-06T00:00:00Z"),
            )
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute(
                "INSERT INTO mastery_estimate(estimate_id, concept_id, derived_state, evidence_input_hash, created_at) "
                "VALUES (?, ?, ?, ?, ?)",
            ("estimate-upper", "concept-1", "demonstrated_now", "C" * 64, "2026-08-06T00:00:00Z"),
            )
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute("UPDATE mastery_estimate SET derived_state = 'retained' WHERE estimate_id = 'estimate-1'")
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute("DELETE FROM mastery_estimate WHERE estimate_id = 'estimate-1'")
    finally:
        connection.close()


def test_review_revision_rejects_invalid_mode_date_hash_and_parentage(tmp_path: Path) -> None:
    value = database(tmp_path)
    connection = value.connect()
    try:
        seed_course_and_concept(connection)
        connection.execute(
            "INSERT INTO course(course_id, name, timezone, created_at) VALUES (?, ?, ?, ?)",
            ("course-2", "Operating Systems", "Asia/Shanghai", "2026-08-06T00:00:00Z"),
        )
        insert_revision(connection, "revision-parent")

        invalid_revisions = [
            ("revision-continuous-date", "course-1", "continuous", "2026-08-30", "e" * 64, None),
            ("revision-finals-no-date", "course-1", "finals", None, "f" * 64, None),
            ("revision-mode", "course-1", "weekly", None, "a" * 64, None),
            ("revision-upper-hash", "course-1", "continuous", None, "A" * 64, None),
            ("revision-cross-course", "course-2", "continuous", None, "b" * 64, "revision-parent"),
        ]
        for revision_id, course_id, mode, exam_date, input_hash, parent_revision_id in invalid_revisions:
            with pytest.raises(sqlite3.IntegrityError):
                insert_revision(
                    connection,
                    revision_id,
                    course_id,
                    mode=mode,
                    exam_date=exam_date,
                    input_hash=input_hash,
                    parent_revision_id=parent_revision_id,
                )

        with pytest.raises(sqlite3.IntegrityError):
            connection.execute(
                "UPDATE review_plan_revision SET budget_minutes = 30 WHERE revision_id = 'revision-parent'"
            )
        for budget in (5, 11, 121):
            with pytest.raises(sqlite3.IntegrityError):
                insert_revision(connection, f"revision-budget-{budget}", input_hash=str(budget) * 64, budget_minutes=budget)
    finally:
        connection.close()


def test_learning_foreign_keys_restrict_concept_and_course_deletion(tmp_path: Path) -> None:
    value = database(tmp_path)
    connection = value.connect()
    try:
        seed_course_and_concept(connection)
        insert_revision(connection, "revision-fk", input_hash="3" * 64)
        connection.execute(
            "INSERT INTO attempt(attempt_id, attempt_key, concept_id, check_kind, variant_id, answer_json, status, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ("attempt-fk", "attempt-key-fk", "concept-1", "isomorphic", "v1", "{}", "submitted", "2026-08-06T00:00:00Z", "2026-08-06T00:00:00Z"),
        )
        connection.execute(
            "INSERT INTO mastery_estimate(estimate_id, concept_id, derived_state, evidence_input_hash, created_at) "
            "VALUES (?, ?, ?, ?, ?)",
            ("estimate-fk", "concept-1", "unknown", "4" * 64, "2026-08-06T00:00:00Z"),
        )
        connection.execute(
            "INSERT INTO review_task(task_id, revision_id, concept_id, due_local_date, duration_minutes, status, "
            "source_refs_json, evidence_refs_json, completed_at, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ("task-fk", "revision-fk", "concept-1", "2026-08-07", 10, "pending", "[]", "[]", None, "2026-08-06T00:00:00Z"),
        )
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute("DELETE FROM knowledge_concept WHERE concept_id = 'concept-1'")
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute("DELETE FROM course WHERE course_id = 'course-1'")
    finally:
        connection.close()


def test_pending_and_empty_review_revisions_can_be_removed(tmp_path: Path) -> None:
    value = database(tmp_path)
    connection = value.connect()
    try:
        seed_course_and_concept(connection)
        insert_revision(connection, "revision-empty", input_hash="1" * 64)
        connection.execute("DELETE FROM review_plan_revision WHERE revision_id = 'revision-empty'")
        assert connection.execute(
            "SELECT 1 FROM review_plan_revision WHERE revision_id = 'revision-empty'"
        ).fetchone() is None

        insert_revision(connection, "revision-pending", input_hash="2" * 64)
        connection.execute(
            "INSERT INTO review_task(task_id, revision_id, concept_id, due_local_date, duration_minutes, status, "
            "source_refs_json, evidence_refs_json, completed_at, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                "task-pending",
                "revision-pending",
                "concept-1",
                "2026-08-07",
                10,
                "pending",
                "[]",
                "[]",
                None,
                "2026-08-06T01:00:00Z",
            ),
        )
        connection.execute("DELETE FROM review_plan_revision WHERE revision_id = 'revision-pending'")
        assert connection.execute("SELECT 1 FROM review_task WHERE task_id = 'task-pending'").fetchone() is None
    finally:
        connection.close()


def test_review_revision_parentage_and_completed_task_protection(tmp_path: Path) -> None:
    value = database(tmp_path)
    connection = value.connect()
    try:
        seed_course_and_concept(connection)
        connection.execute(
            "INSERT INTO review_plan_revision(revision_id, course_id, mode, timezone, budget_minutes, exam_date, "
            "input_hash, parent_revision_id, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ("revision-1", "course-1", "continuous", "Asia/Shanghai", 60, None, "d" * 64, None, "2026-08-06T00:00:00Z"),
        )
        connection.execute(
            "INSERT INTO review_plan_revision(revision_id, course_id, mode, timezone, budget_minutes, exam_date, "
            "input_hash, parent_revision_id, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ("revision-2", "course-1", "finals", "Asia/Shanghai", 120, "2026-08-30", "e" * 64, "revision-1", "2026-08-06T01:00:00Z"),
        )
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute("DELETE FROM review_plan_revision WHERE revision_id = 'revision-1'")
        connection.execute(
            "INSERT INTO review_task(task_id, revision_id, concept_id, due_local_date, duration_minutes, status, "
            "source_refs_json, evidence_refs_json, completed_at, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ("task-1", "revision-2", "concept-1", "2026-08-07", 10, "pending", "[]", "[]", None, "2026-08-06T01:00:00Z"),
        )
        connection.execute(
            "UPDATE review_task SET status = 'completed', completed_at = ? WHERE task_id = 'task-1'",
            ("2026-08-07T02:00:00Z",),
        )
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute("UPDATE review_task SET duration_minutes = 10 WHERE task_id = 'task-1'")
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute("DELETE FROM review_task WHERE task_id = 'task-1'")
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute("DELETE FROM review_plan_revision WHERE revision_id = 'revision-2'")
    finally:
        connection.close()
