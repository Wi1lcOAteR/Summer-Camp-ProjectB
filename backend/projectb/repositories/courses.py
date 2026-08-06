from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


class CourseError(RuntimeError):
    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


@dataclass(frozen=True, slots=True)
class Course:
    course_id: str
    name: str
    timezone: str
    created_at: str


class CourseRepository:
    def __init__(self, database: Any) -> None:
        self.database = database

    def create(self, name: str, timezone: str) -> Course:
        normalized = name.strip()
        if not normalized or len(normalized) > 120:
            raise CourseError("course_name_invalid")
        try:
            ZoneInfo(timezone)
        except (ZoneInfoNotFoundError, ValueError):
            raise CourseError("timezone_invalid") from None
        course = Course(
            f"course-{uuid4().hex}",
            normalized,
            timezone,
            datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        )
        connection = self.database.connect()
        try:
            connection.execute(
                "INSERT INTO course(course_id, name, timezone, created_at) VALUES (?, ?, ?, ?)",
                (course.course_id, course.name, course.timezone, course.created_at),
            )
        finally:
            connection.close()
        return course

    def list(self) -> tuple[Course, ...]:
        connection = self.database.connect()
        try:
            return tuple(
                Course(str(row[0]), str(row[1]), str(row[2]), str(row[3]))
                for row in connection.execute(
                    "SELECT course_id, name, timezone, created_at FROM course ORDER BY created_at, course_id"
                )
            )
        finally:
            connection.close()

    def exists(self, course_id: str) -> bool:
        connection = self.database.connect()
        try:
            return connection.execute("SELECT 1 FROM course WHERE course_id = ?", (course_id,)).fetchone() is not None
        finally:
            connection.close()
