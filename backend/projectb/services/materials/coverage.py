from __future__ import annotations

from projectb.repositories.coverage import Concept, CoverageError, CoverageRepository


class CoverageService:
    def __init__(self, database: object) -> None:
        self.repository = CoverageRepository(database)

    def create_concept(self, course_id: str, name: str, *, evaluator_id: str | None = None) -> Concept:
        return self.repository.create_concept(course_id, name, evaluator_id)

    def record_decision(self, concept_id: str, locator_ids: list[str], decision: str) -> int:
        return self.repository.record_decision(concept_id, tuple(locator_ids), decision)

    def authorize(self, concept_id: str) -> tuple[str, ...]:
        return self.repository.authorize(concept_id)


__all__ = ["Concept", "CoverageError", "CoverageService"]
