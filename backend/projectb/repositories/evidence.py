from __future__ import annotations

import hashlib
import json
import sqlite3
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from typing import Any

from projectb.domain.learning.evaluators.schemas import EvaluationResult, RubricItem


class EvidenceConflictError(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class EvidenceRecord:
    evidence_id: str
    attempt_id: str
    course_id: str
    concept_id: str
    evaluator_id: str
    evaluator_version: str
    check_kind: str
    outcome: str
    rubric: tuple[RubricItem, ...]
    source_locator_ids: tuple[str, ...]
    evidence_version: int
    created_at: str


class EvidenceRepository:
    def __init__(self, database: Any) -> None:
        self.database = database

    def find_by_attempt_key(
        self,
        attempt_key: str,
        *,
        concept_id: str | None = None,
        check_kind: str | None = None,
        variant_id: str | None = None,
        answer_json: str | None = None,
    ) -> EvidenceRecord | None:
        connection = self.database.connect()
        try:
            row = connection.execute(
                "SELECT le.evidence_id, a.attempt_id, le.course_id, le.concept_id, le.evaluator_id, "
                "le.evaluator_version, le.check_kind, le.outcome, le.rubric_json, le.source_ids_json, "
                "le.evidence_version, le.created_at, a.concept_id, a.check_kind, a.variant_id, a.answer_json "
                "FROM attempt a JOIN learning_evidence le ON le.attempt_id = a.attempt_id WHERE a.attempt_key = ?",
                (attempt_key,),
            ).fetchone()
            if row is None:
                return None
            expected = (concept_id, check_kind, variant_id, answer_json)
            actual = (str(row[12]), str(row[13]), str(row[14]), str(row[15]))
            if any(value is not None for value in expected) and expected != actual:
                raise EvidenceConflictError("idempotency_conflict")
            rubric = tuple(RubricItem(**item) for item in json.loads(row[8]))
            return EvidenceRecord(
                evidence_id=str(row[0]),
                attempt_id=str(row[1]),
                course_id=str(row[2]),
                concept_id=str(row[3]),
                evaluator_id=str(row[4]),
                evaluator_version=str(row[5]),
                check_kind=str(row[6]),
                outcome=str(row[7]),
                rubric=rubric,
                source_locator_ids=tuple(json.loads(row[9])),
                evidence_version=int(row[10]),
                created_at=str(row[11]),
            )
        finally:
            connection.close()

    def append(
        self,
        *,
        attempt_key: str,
        course_id: str,
        concept_id: str,
        check_kind: str,
        variant_id: str,
        answer_json: str,
        evaluation: EvaluationResult,
    ) -> EvidenceRecord:
        attempt_id = "attempt-" + hashlib.sha256(attempt_key.encode()).hexdigest()
        evidence_id = "evidence-" + hashlib.sha256((attempt_key + ":v1").encode()).hexdigest()
        created_at = datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")
        rubric_json = json.dumps(
            [asdict(item) for item in evaluation.rubric], ensure_ascii=True, separators=(",", ":"), sort_keys=True
        )
        source_json = json.dumps(evaluation.source_locator_ids, separators=(",", ":"))
        connection = self.database.connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            connection.execute(
                "INSERT INTO attempt(attempt_id, attempt_key, concept_id, check_kind, variant_id, answer_json, "
                "status, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, 'evaluated', ?, ?)",
                (attempt_id, attempt_key, concept_id, check_kind, variant_id, answer_json, created_at, created_at),
            )
            connection.execute(
                "INSERT INTO learning_evidence(evidence_id, attempt_id, course_id, concept_id, evaluator_id, "
                "evaluator_version, check_kind, outcome, rubric_json, source_ids_json, evidence_version, "
                "idempotency_key, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?)",
                (
                    evidence_id,
                    attempt_id,
                    course_id,
                    concept_id,
                    evaluation.evaluator_id,
                    evaluation.evaluator_version,
                    check_kind,
                    evaluation.outcome,
                    rubric_json,
                    source_json,
                    attempt_key,
                    created_at,
                ),
            )
            connection.commit()
        except sqlite3.IntegrityError:
            connection.rollback()
            existing = self.find_by_attempt_key(
                attempt_key,
                concept_id=concept_id,
                check_kind=check_kind,
                variant_id=variant_id,
                answer_json=answer_json,
            )
            if existing is not None:
                return existing
            raise
        except BaseException:
            connection.rollback()
            raise
        finally:
            connection.close()
        record = self.find_by_attempt_key(attempt_key)
        assert record is not None
        return record
