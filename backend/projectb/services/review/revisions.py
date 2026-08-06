from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from projectb.domain.review.planner import ReviewPolicy, ReviewSeed
from projectb.repositories.review_plans import ReviewPlanRepository, StoredReviewTask, StoredRevision


class RevisionError(RuntimeError):
    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


@dataclass(frozen=True, slots=True)
class RevisionDiff:
    added: tuple[str, ...]
    removed: tuple[str, ...]
    changed: tuple[str, ...]
    retained: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ReviewRevision:
    revision_id: str
    course_id: str
    input_hash: str
    parent_revision_id: str | None
    created_at: str
    tasks: tuple[StoredReviewTask, ...]
    diff: RevisionDiff


class RevisionService:
    def __init__(self, database: Any) -> None:
        self.repository = ReviewPlanRepository(database)

    def generate(
        self,
        course_id: str,
        policy: ReviewPolicy,
        seeds: tuple[ReviewSeed, ...],
        *,
        generated_at: datetime,
    ) -> ReviewRevision:
        plan = policy.plan(seeds, generated_at=generated_at)
        created_at = self._utc(generated_at)
        with self.repository.locked() as connection:
            timezone = self.repository.course_timezone(connection, course_id)
            if timezone is None:
                raise RevisionError("course_not_found")
            if timezone != policy.timezone:
                raise RevisionError("course_timezone_mismatch")
            existing = self.repository.find_revision_id(connection, course_id, plan.input_hash)
            if existing is not None:
                revision_id = existing
            else:
                parent = self.repository.latest_revision_id(connection, course_id)
                revision_id = "revision-" + hashlib.sha256(f"{course_id}:{plan.input_hash}".encode()).hexdigest()
                self.repository.insert_revision(
                    connection,
                    revision_id=revision_id,
                    course_id=course_id,
                    mode=policy.mode,
                    timezone=policy.timezone,
                    budget_minutes=policy.daily_budget_minutes,
                    exam_date=None if policy.exam_date is None else policy.exam_date.isoformat(),
                    input_hash=plan.input_hash,
                    parent_revision_id=parent,
                    created_at=created_at,
                )
                completed = self.repository.completed_identities(connection, course_id)
                for task in plan.tasks:
                    if (task.concept_id, task.due_local_date.isoformat()) in completed:
                        continue
                    task_id = "task-" + hashlib.sha256(f"{revision_id}:{task.task_key}".encode()).hexdigest()
                    self.repository.insert_task(
                        connection,
                        task_id=task_id,
                        revision_id=revision_id,
                        concept_id=task.concept_id,
                        due_local_date=task.due_local_date.isoformat(),
                        source_refs=task.source_refs,
                        evidence_refs=task.evidence_refs,
                        created_at=created_at,
                    )
        return self._revision(revision_id)

    def diff(self, before_revision_id: str, after_revision_id: str) -> RevisionDiff:
        before = self.repository.load_revision(before_revision_id)
        after = self.repository.load_revision(after_revision_id)
        if before is None or after is None:
            raise RevisionError("revision_not_found")
        if before.course_id != after.course_id:
            raise RevisionError("revision_course_mismatch")
        return self._diff(before, after)

    def skip_task(self, task_id: str) -> StoredReviewTask:
        return self._set_status(task_id, "skipped", None)

    def recover_task(self, task_id: str) -> StoredReviewTask:
        task = self.repository.load_task(task_id)
        if task is None:
            raise RevisionError("task_not_found")
        if task.status == "completed":
            raise RevisionError("completed_task_immutable")
        return self._set_status(task_id, "pending", None)

    def complete_task(self, task_id: str, *, completed_at: str) -> StoredReviewTask:
        try:
            parsed = datetime.fromisoformat(completed_at.replace("Z", "+00:00"))
        except ValueError:
            raise RevisionError("completed_at_invalid") from None
        if not completed_at.endswith("Z") or parsed.tzinfo is None:
            raise RevisionError("completed_at_invalid")
        return self._set_status(task_id, "completed", completed_at)

    def _set_status(self, task_id: str, status: str, completed_at: str | None) -> StoredReviewTask:
        with self.repository.locked() as connection:
            row = connection.execute("SELECT status FROM review_task WHERE task_id = ?", (task_id,)).fetchone()
            if row is None:
                raise RevisionError("task_not_found")
            if str(row[0]) == "completed":
                raise RevisionError("completed_task_immutable")
            connection.execute(
                "UPDATE review_task SET status = ?, completed_at = ? WHERE task_id = ?",
                (status, completed_at, task_id),
            )
        task = self.repository.load_task(task_id)
        if task is None:
            raise RevisionError("task_not_found")
        return task

    def _revision(self, revision_id: str) -> ReviewRevision:
        stored = self.repository.load_revision(revision_id)
        if stored is None:
            raise RevisionError("revision_not_found")
        if stored.parent_revision_id is None:
            empty = StoredRevision("", stored.course_id, "continuous", stored.timezone, 30, None, "", None, "", ())
            diff = self._diff(empty, stored)
        else:
            parent = self.repository.load_revision(stored.parent_revision_id)
            if parent is None:
                raise RevisionError("revision_parent_missing")
            diff = self._diff(parent, stored)
        return ReviewRevision(
            stored.revision_id,
            stored.course_id,
            stored.input_hash,
            stored.parent_revision_id,
            stored.created_at,
            stored.tasks,
            diff,
        )

    @staticmethod
    def _diff(before: StoredRevision, after: StoredRevision) -> RevisionDiff:
        before_tasks = {RevisionService._task_key(task): task for task in before.tasks}
        after_tasks = {RevisionService._task_key(task): task for task in after.tasks}
        before_keys = set(before_tasks)
        after_keys = set(after_tasks)
        shared = before_keys & after_keys
        changed = {
            key
            for key in shared
            if RevisionService._task_content(before_tasks[key]) != RevisionService._task_content(after_tasks[key])
        }
        return RevisionDiff(
            tuple(sorted(after_keys - before_keys)),
            tuple(sorted(before_keys - after_keys)),
            tuple(sorted(changed)),
            tuple(sorted(shared - changed)),
        )

    @staticmethod
    def _task_key(task: StoredReviewTask) -> str:
        return f"{task.concept_id}@{task.due_local_date}"

    @staticmethod
    def _task_content(task: StoredReviewTask) -> tuple[object, ...]:
        return (task.duration_minutes, task.source_refs, task.evidence_refs)

    @staticmethod
    def _utc(value: datetime) -> str:
        if value.tzinfo is None:
            raise RevisionError("generated_at_invalid")
        return value.astimezone(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")
