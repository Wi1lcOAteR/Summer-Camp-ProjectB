from __future__ import annotations

import json
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class StoredReviewTask:
    task_id: str
    revision_id: str
    concept_id: str
    due_local_date: str
    duration_minutes: int
    status: str
    source_refs: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    completed_at: str | None
    created_at: str


@dataclass(frozen=True, slots=True)
class StoredRevision:
    revision_id: str
    course_id: str
    mode: str
    timezone: str
    budget_minutes: int
    exam_date: str | None
    input_hash: str
    parent_revision_id: str | None
    created_at: str
    tasks: tuple[StoredReviewTask, ...]


class ReviewPlanRepository:
    def __init__(self, database: Any) -> None:
        self.database = database

    @contextmanager
    def locked(self) -> Iterator[sqlite3.Connection]:
        connection = self.database.connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            yield connection
            connection.commit()
        except BaseException:
            connection.rollback()
            raise
        finally:
            connection.close()

    @staticmethod
    def course_timezone(connection: sqlite3.Connection, course_id: str) -> str | None:
        row = connection.execute("SELECT timezone FROM course WHERE course_id = ?", (course_id,)).fetchone()
        return None if row is None else str(row[0])

    @staticmethod
    def find_revision_id(connection: sqlite3.Connection, course_id: str, input_hash: str) -> str | None:
        row = connection.execute(
            "SELECT revision_id FROM review_plan_revision WHERE course_id = ? AND input_hash = ?",
            (course_id, input_hash),
        ).fetchone()
        return None if row is None else str(row[0])

    @staticmethod
    def latest_revision_id(connection: sqlite3.Connection, course_id: str) -> str | None:
        row = connection.execute(
            "SELECT revision_id FROM review_plan_revision WHERE course_id = ? ORDER BY rowid DESC LIMIT 1",
            (course_id,),
        ).fetchone()
        return None if row is None else str(row[0])

    @staticmethod
    def completed_identities(connection: sqlite3.Connection, course_id: str) -> set[tuple[str, str]]:
        return {
            (str(row[0]), str(row[1]))
            for row in connection.execute(
                "SELECT rt.concept_id, rt.due_local_date FROM review_task rt "
                "JOIN review_plan_revision rp ON rp.revision_id = rt.revision_id "
                "WHERE rp.course_id = ? AND rt.status = 'completed'",
                (course_id,),
            )
        }

    @staticmethod
    def insert_revision(
        connection: sqlite3.Connection,
        *,
        revision_id: str,
        course_id: str,
        mode: str,
        timezone: str,
        budget_minutes: int,
        exam_date: str | None,
        input_hash: str,
        parent_revision_id: str | None,
        created_at: str,
    ) -> None:
        connection.execute(
            "INSERT INTO review_plan_revision(revision_id, course_id, mode, timezone, budget_minutes, exam_date, "
            "input_hash, parent_revision_id, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                revision_id,
                course_id,
                mode,
                timezone,
                budget_minutes,
                exam_date,
                input_hash,
                parent_revision_id,
                created_at,
            ),
        )

    @staticmethod
    def insert_task(
        connection: sqlite3.Connection,
        *,
        task_id: str,
        revision_id: str,
        concept_id: str,
        due_local_date: str,
        source_refs: tuple[str, ...],
        evidence_refs: tuple[str, ...],
        created_at: str,
    ) -> None:
        connection.execute(
            "INSERT INTO review_task(task_id, revision_id, concept_id, due_local_date, duration_minutes, status, "
            "source_refs_json, evidence_refs_json, completed_at, created_at) "
            "VALUES (?, ?, ?, ?, 10, 'pending', ?, ?, NULL, ?)",
            (
                task_id,
                revision_id,
                concept_id,
                due_local_date,
                json.dumps(source_refs, separators=(",", ":")),
                json.dumps(evidence_refs, separators=(",", ":")),
                created_at,
            ),
        )

    def load_revision(self, revision_id: str) -> StoredRevision | None:
        connection = self.database.connect()
        try:
            row = connection.execute(
                "SELECT revision_id, course_id, mode, timezone, budget_minutes, exam_date, input_hash, "
                "parent_revision_id, created_at FROM review_plan_revision WHERE revision_id = ?",
                (revision_id,),
            ).fetchone()
            if row is None:
                return None
            tasks = tuple(
                self._task(task)
                for task in connection.execute(
                    "SELECT task_id, revision_id, concept_id, due_local_date, duration_minutes, status, "
                    "source_refs_json, evidence_refs_json, completed_at, created_at FROM review_task "
                    "WHERE revision_id = ? ORDER BY due_local_date, concept_id, task_id",
                    (revision_id,),
                )
            )
            return StoredRevision(
                str(row[0]),
                str(row[1]),
                str(row[2]),
                str(row[3]),
                int(row[4]),
                None if row[5] is None else str(row[5]),
                str(row[6]),
                None if row[7] is None else str(row[7]),
                str(row[8]),
                tasks,
            )
        finally:
            connection.close()

    def load_task(self, task_id: str) -> StoredReviewTask | None:
        connection = self.database.connect()
        try:
            row = connection.execute(
                "SELECT task_id, revision_id, concept_id, due_local_date, duration_minutes, status, "
                "source_refs_json, evidence_refs_json, completed_at, created_at FROM review_task WHERE task_id = ?",
                (task_id,),
            ).fetchone()
            return None if row is None else self._task(row)
        finally:
            connection.close()

    @staticmethod
    def _task(row: Any) -> StoredReviewTask:
        return StoredReviewTask(
            str(row[0]),
            str(row[1]),
            str(row[2]),
            str(row[3]),
            int(row[4]),
            str(row[5]),
            tuple(json.loads(row[6])),
            tuple(json.loads(row[7])),
            None if row[8] is None else str(row[8]),
            str(row[9]),
        )
