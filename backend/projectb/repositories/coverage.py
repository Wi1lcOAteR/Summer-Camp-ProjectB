from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4


class CoverageError(RuntimeError):
    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


@dataclass(frozen=True, slots=True)
class Concept:
    concept_id: str
    course_id: str
    name: str
    evaluator_id: str | None
    version: int
    state: str


class CoverageRepository:
    def __init__(self, database: Any) -> None:
        self.database = database

    def create_concept(self, course_id: str, name: str, evaluator_id: str | None) -> Concept:
        if not name.strip():
            raise CoverageError("concept_name_required")
        concept = Concept(
            concept_id=f"concept-{uuid4().hex}",
            course_id=course_id,
            name=name.strip(),
            evaluator_id=evaluator_id,
            version=1,
            state="active" if evaluator_id else "explanation_only",
        )
        connection = self.database.connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            connection.execute(
                "INSERT INTO knowledge_concept(concept_id, course_id, name, evaluator_id, version, state, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    concept.concept_id,
                    concept.course_id,
                    concept.name,
                    concept.evaluator_id,
                    concept.version,
                    concept.state,
                    self._now(),
                ),
            )
            connection.commit()
            return concept
        except BaseException:
            connection.rollback()
            raise
        finally:
            connection.close()

    def record_decision(self, concept_id: str, locator_ids: tuple[str, ...], decision: str) -> int:
        if decision not in {"confirmed", "rejected"}:
            raise CoverageError("coverage_decision_invalid")
        if not locator_ids or len(set(locator_ids)) != len(locator_ids):
            raise CoverageError("locator_selection_invalid")
        connection = self.database.connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            concept = connection.execute(
                "SELECT course_id FROM knowledge_concept WHERE concept_id = ?", (concept_id,)
            ).fetchone()
            if concept is None:
                raise CoverageError("concept_not_found")
            self._require_current_locators(connection, str(concept[0]), locator_ids)
            version = int(
                connection.execute(
                    "SELECT coalesce(max(version), 0) + 1 FROM coverage_decision WHERE concept_id = ?", (concept_id,)
                ).fetchone()[0]
            )
            connection.execute(
                "INSERT INTO coverage_decision(decision_id, concept_id, locator_ids_json, decision, version, confirmed_at) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (
                    f"decision-{uuid4().hex}",
                    concept_id,
                    json.dumps(locator_ids, separators=(",", ":")),
                    decision,
                    version,
                    self._now(),
                ),
            )
            connection.commit()
            return version
        except BaseException:
            connection.rollback()
            raise
        finally:
            connection.close()

    def authorize(self, concept_id: str) -> tuple[str, ...]:
        connection = self.database.connect()
        try:
            row = connection.execute(
                "SELECT kc.course_id, cd.locator_ids_json, cd.decision FROM knowledge_concept kc "
                "LEFT JOIN coverage_decision cd ON cd.concept_id = kc.concept_id "
                "AND cd.version = (SELECT max(latest.version) FROM coverage_decision latest WHERE latest.concept_id = kc.concept_id) "
                "WHERE kc.concept_id = ?",
                (concept_id,),
            ).fetchone()
            if row is None:
                raise CoverageError("concept_not_found")
            if row[2] != "confirmed":
                raise CoverageError("coverage_unconfirmed")
            try:
                locator_ids = tuple(json.loads(row[1]))
            except (TypeError, json.JSONDecodeError):
                raise CoverageError("coverage_invalid") from None
            self._require_current_locators(connection, str(row[0]), locator_ids)
            return locator_ids
        finally:
            connection.close()

    @staticmethod
    def _require_current_locators(connection: Any, course_id: str, locator_ids: tuple[str, ...]) -> None:
        for locator_id in locator_ids:
            row = connection.execute(
                "SELECT m.course_id, mv.rowid, "
                "(SELECT max(current.rowid) FROM material_version current WHERE current.material_id = mv.material_id) "
                "FROM source_locator sl JOIN material_version mv ON mv.version_id = sl.material_version_id "
                "JOIN material m ON m.material_id = mv.material_id WHERE sl.locator_id = ?",
                (locator_id,),
            ).fetchone()
            if row is None or str(row[0]) != course_id or int(row[1]) != int(row[2]):
                raise CoverageError("source_stale")

    @staticmethod
    def _now() -> str:
        return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")
