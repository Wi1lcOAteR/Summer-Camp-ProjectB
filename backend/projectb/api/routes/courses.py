from __future__ import annotations

from dataclasses import asdict

from fastapi import APIRouter, Request, status
from pydantic import BaseModel, ConfigDict

from projectb.api.app_support import ApiError
from projectb.repositories.courses import CourseError, CourseRepository


router = APIRouter(prefix="/api/courses", tags=["courses"])


class CourseCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    name: str
    timezone: str


@router.get("")
def list_courses(request: Request) -> dict[str, object]:
    courses = CourseRepository(request.app.state.database).list()
    return {"courses": [asdict(course) for course in courses]}


@router.post("", status_code=status.HTTP_201_CREATED)
def create_course(payload: CourseCreate, request: Request) -> dict[str, object]:
    try:
        course = CourseRepository(request.app.state.database).create(payload.name, payload.timezone)
    except CourseError as error:
        raise ApiError(error.code, 400) from None
    return asdict(course)
