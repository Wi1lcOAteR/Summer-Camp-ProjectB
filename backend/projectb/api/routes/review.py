from __future__ import annotations

from dataclasses import asdict
from datetime import date, datetime
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Request
from pydantic import BaseModel, ConfigDict

from projectb.api.app_support import ApiError
from projectb.domain.review.planner import PlannerError, ReviewPolicy, ReviewSeed
from projectb.repositories.coverage import CoverageError, CoverageRepository
from projectb.services.learning.mastery import MasteryService
from projectb.services.review.revisions import RevisionError, RevisionService


router = APIRouter(prefix="/api/review", tags=["review"])


class RevisionPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")
    course_id: str
    mode: str
    timezone: str
    daily_budget_minutes: int = 30
    exam_date: date | None = None
    generated_at: datetime


class CompletionPayload(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    completed_at: str


@router.post("/revisions")
def generate_revision(payload: RevisionPayload, request: Request) -> dict[str, object]:
    try:
        policy = ReviewPolicy(
            mode=payload.mode,  # type: ignore[arg-type]
            timezone=payload.timezone,
            daily_budget_minutes=payload.daily_budget_minutes,
            exam_date=payload.exam_date,
        )
        seeds = _authoritative_seeds(request, payload.course_id, payload.timezone, payload.generated_at)
        revision = RevisionService(request.app.state.database).generate(
            payload.course_id,
            policy,
            seeds,
            generated_at=payload.generated_at,
        )
    except (PlannerError, RevisionError) as error:
        status = 404 if error.code in {"course_not_found", "task_not_found"} else 400
        raise ApiError(error.code, status) from None
    return asdict(revision)


def _authoritative_seeds(
    request: Request,
    course_id: str,
    timezone: str,
    generated_at: datetime,
) -> tuple[ReviewSeed, ...]:
    database = request.app.state.database
    connection = database.connect()
    try:
        concept_ids = tuple(
            str(row[0])
            for row in connection.execute(
                "SELECT concept_id FROM knowledge_concept WHERE course_id = ? ORDER BY concept_id",
                (course_id,),
            )
        )
    finally:
        connection.close()
    local_generated = generated_at.astimezone(ZoneInfo(timezone)).date()
    weakness = {"unknown": 2, "demonstrated_now": 1, "retained": 0}
    seeds: list[ReviewSeed] = []
    for concept_id in concept_ids:
        try:
            sources = CoverageRepository(database).authorize(concept_id)
            eligibility = "ready"
        except CoverageError:
            sources = ()
            eligibility = "stale_source"
        mastery = MasteryService(database).derive(concept_id)
        connection = database.connect()
        try:
            evidence_rows = connection.execute(
                "SELECT evidence_id, created_at FROM learning_evidence WHERE concept_id = ? "
                "ORDER BY created_at, evidence_id",
                (concept_id,),
            ).fetchall()
        finally:
            connection.close()
        evidence_refs = tuple(str(row[0]) for row in evidence_rows)
        requested = local_generated
        if evidence_rows:
            requested = datetime.fromisoformat(str(evidence_rows[-1][1]).replace("Z", "+00:00")).astimezone(
                ZoneInfo(timezone)
            ).date()
        seeds.append(
            ReviewSeed(
                concept_id,
                mastery.state,  # type: ignore[arg-type]
                weakness[mastery.state],
                requested,
                sources,
                evidence_refs,
                eligibility,  # type: ignore[arg-type]
            )
        )
    return tuple(seeds)


@router.post("/tasks/{task_id}/skip")
def skip_task(task_id: str, request: Request) -> dict[str, object]:
    return _task_call(request, "skip_task", task_id)


@router.post("/tasks/{task_id}/recover")
def recover_task(task_id: str, request: Request) -> dict[str, object]:
    return _task_call(request, "recover_task", task_id)


@router.post("/tasks/{task_id}/complete")
def complete_task(task_id: str, payload: CompletionPayload, request: Request) -> dict[str, object]:
    return _task_call(request, "complete_task", task_id, completed_at=payload.completed_at)


def _task_call(request: Request, method: str, task_id: str, **kwargs: object) -> dict[str, object]:
    try:
        task = getattr(RevisionService(request.app.state.database), method)(task_id, **kwargs)
    except RevisionError as error:
        status = 409 if error.code == "completed_task_immutable" else 404 if error.code == "task_not_found" else 400
        raise ApiError(error.code, status) from None
    return asdict(task)
