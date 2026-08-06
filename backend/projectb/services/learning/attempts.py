from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import asdict, dataclass, is_dataclass
from typing import Any

from projectb.domain.learning.evaluators.registry import (
    EvaluatorNotFoundError,
    ExplanationOnlyError,
    default_registry,
)
from projectb.domain.learning.evaluators.schemas import CheckKind, EvaluationRequest, RubricItem
from projectb.repositories.coverage import CoverageError, CoverageRepository
from projectb.repositories.evidence import EvidenceConflictError, EvidenceRecord, EvidenceRepository


class AttemptError(RuntimeError):
    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


@dataclass(frozen=True, slots=True)
class FeedbackPayload:
    evaluator_id: str
    evaluator_version: str
    outcome: str
    rubric: tuple[RubricItem, ...]
    source_locator_ids: tuple[str, ...]


class AttemptService:
    def __init__(
        self,
        database: Any,
        *,
        feedback_wording: Callable[[FeedbackPayload], str] | None = None,
    ) -> None:
        self.database = database
        self.coverage = CoverageRepository(database)
        self.evidence = EvidenceRepository(database)
        self.registry = default_registry()
        self.feedback_wording = feedback_wording

    def submit(
        self,
        *,
        concept_id: str,
        attempt_key: str,
        check_kind: CheckKind,
        variant_id: str,
        exercise: object,
        answer: object,
    ) -> EvidenceRecord:
        if not attempt_key.strip() or len(attempt_key) > 128:
            raise AttemptError("attempt_key_invalid")
        if not is_dataclass(answer) or isinstance(answer, type):
            raise AttemptError("answer_schema_invalid")
        answer_json = json.dumps(asdict(answer), ensure_ascii=False, separators=(",", ":"), sort_keys=True)
        try:
            existing = self.evidence.find_by_attempt_key(
                attempt_key,
                concept_id=concept_id,
                check_kind=check_kind,
                variant_id=variant_id,
                answer_json=answer_json,
            )
        except EvidenceConflictError as error:
            raise AttemptError(str(error)) from None
        if existing is not None:
            return existing

        course_id, evaluator_id = self._concept_context(concept_id)
        try:
            source_locator_ids = self.coverage.authorize(concept_id)
            evaluator = self.registry.for_concept(evaluator_id)
        except (CoverageError, ExplanationOnlyError, EvaluatorNotFoundError) as error:
            raise AttemptError(str(error)) from None
        request = EvaluationRequest(
            evaluator_id=evaluator.evaluator_id,
            check_kind=check_kind,
            variant_id=variant_id,
            source_locator_ids=source_locator_ids,
            exercise=exercise,
            answer=answer,
        )
        try:
            evaluation = evaluator.evaluate(request)
        except ValueError as error:
            raise AttemptError(str(error)) from None
        if evaluation.evaluator_id != evaluator.evaluator_id or evaluation.evaluator_version != evaluator.version:
            raise AttemptError("evaluator_contract_mismatch")
        record = self.evidence.append(
            attempt_key=attempt_key,
            course_id=course_id,
            concept_id=concept_id,
            check_kind=check_kind,
            variant_id=variant_id,
            answer_json=answer_json,
            evaluation=evaluation,
        )
        if self.feedback_wording is not None:
            payload = FeedbackPayload(
                evaluation.evaluator_id,
                evaluation.evaluator_version,
                evaluation.outcome,
                evaluation.rubric,
                evaluation.source_locator_ids,
            )
            try:
                self.feedback_wording(payload)
            except Exception:
                pass
        return record

    def _concept_context(self, concept_id: str) -> tuple[str, str | None]:
        connection = self.database.connect()
        try:
            row = connection.execute(
                "SELECT course_id, evaluator_id FROM knowledge_concept WHERE concept_id = ?", (concept_id,)
            ).fetchone()
            if row is None:
                raise AttemptError("concept_not_found")
            return str(row[0]), None if row[1] is None else str(row[1])
        finally:
            connection.close()
