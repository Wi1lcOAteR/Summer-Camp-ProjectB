from __future__ import annotations

from dataclasses import asdict
from typing import Any

from fastapi import APIRouter, Request
from pydantic import BaseModel, ConfigDict

from projectb.api.app_support import ApiError
from projectb.domain.learning.evaluators.schemas import (
    DeadlockAnswer,
    DeadlockExercise,
    MutexAnswer,
    MutexEvent,
    MutexExercise,
    RaceAnswer,
    RaceExercise,
    RaceStep,
    ResourceClaim,
)
from projectb.services.learning.attempts import AttemptError, AttemptService
from projectb.services.learning.mastery import MasteryError, MasteryService


router = APIRouter(tags=["learning"])


class AttemptPayload(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    concept_id: str
    attempt_key: str
    check_kind: str
    variant_id: str
    exercise: dict[str, Any]
    answer: dict[str, Any]


@router.post("/api/learning/attempts")
def submit_attempt(payload: AttemptPayload, request: Request) -> dict[str, object]:
    evaluator_id = _evaluator_id(request, payload.concept_id)
    try:
        exercise, answer = _schemas(evaluator_id, payload.exercise, payload.answer)
        record = AttemptService(request.app.state.database).submit(
            concept_id=payload.concept_id,
            attempt_key=payload.attempt_key,
            check_kind=payload.check_kind,  # type: ignore[arg-type]
            variant_id=payload.variant_id,
            exercise=exercise,
            answer=answer,
        )
    except (AttemptError, ValueError, TypeError, KeyError) as error:
        code = error.code if isinstance(error, AttemptError) else "invalid_attempt"
        status = 409 if code == "idempotency_conflict" else 400
        raise ApiError(code, status) from None
    data = asdict(record)
    data["rubric"] = [asdict(item) for item in record.rubric]
    return data


@router.get("/api/concepts/{concept_id}/mastery")
def mastery(concept_id: str, request: Request) -> dict[str, object]:
    try:
        return asdict(MasteryService(request.app.state.database).derive(concept_id))
    except MasteryError as error:
        status = 404 if error.code == "concept_not_found" else 400
        raise ApiError(error.code, status) from None


def _evaluator_id(request: Request, concept_id: str) -> str:
    connection = request.app.state.database.connect()
    try:
        row = connection.execute(
            "SELECT evaluator_id FROM knowledge_concept WHERE concept_id = ?",
            (concept_id,),
        ).fetchone()
    finally:
        connection.close()
    if row is None:
        raise ApiError("concept_not_found", 404)
    if row[0] is None:
        raise ApiError("explanation_only", 400)
    return str(row[0])


def _schemas(evaluator_id: str, exercise: dict[str, Any], answer: dict[str, Any]) -> tuple[object, object]:
    if evaluator_id == "os.mutex.v1":
        return (
            MutexExercise(tuple(MutexEvent(**item) for item in exercise["events"])),
            MutexAnswer(**answer),
        )
    if evaluator_id == "os.race.v1":
        return (
            RaceExercise(int(exercise["initial_value"]), tuple(RaceStep(**item) for item in exercise["steps"])),
            RaceAnswer(**answer),
        )
    if evaluator_id == "os.deadlock.v1":
        return (
            DeadlockExercise(
                tuple(ResourceClaim(**item) for item in exercise["holds"]),
                tuple(ResourceClaim(**item) for item in exercise["waits"]),
            ),
            DeadlockAnswer(**answer),
        )
    raise ValueError("evaluator_not_supported")
