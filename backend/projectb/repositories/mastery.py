from __future__ import annotations

import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any


class MasteryRepositoryError(RuntimeError):
    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


@dataclass(frozen=True, slots=True)
class MasteryEvidence:
    evidence_id: str
    attempt_id: str
    course_id: str
    concept_id: str
    evaluator_id: str
    evaluator_version: str
    check_kind: str
    outcome: str
    rubric_json: str
    source_ids_json: str
    evidence_version: int
    idempotency_key: str
    created_at: str
    variant_id: str


@dataclass(frozen=True, slots=True)
class MasteryHistory:
    concept_id: str
    course_timezone: str
    evidence: tuple[MasteryEvidence, ...]


@dataclass(frozen=True, slots=True)
class MasteryEstimate:
    estimate_id: str
    concept_id: str
    state: str
    evidence_input_hash: str
    created_at: str


class MasteryRepository:
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

    def load_history(self, connection: sqlite3.Connection, concept_id: str) -> MasteryHistory:
        concept = connection.execute(
            "SELECT c.timezone FROM knowledge_concept kc "
            "JOIN course c ON c.course_id = kc.course_id WHERE kc.concept_id = ?",
            (concept_id,),
        ).fetchone()
        if concept is None:
            raise MasteryRepositoryError("concept_not_found")
        rows = connection.execute(
            "SELECT le.evidence_id, le.attempt_id, le.course_id, le.concept_id, le.evaluator_id, "
            "le.evaluator_version, le.check_kind, le.outcome, le.rubric_json, le.source_ids_json, "
            "le.evidence_version, le.idempotency_key, le.created_at, a.variant_id "
            "FROM learning_evidence le JOIN attempt a ON a.attempt_id = le.attempt_id "
            "WHERE le.concept_id = ? ORDER BY le.evidence_id",
            (concept_id,),
        ).fetchall()
        evidence = tuple(
            MasteryEvidence(
                evidence_id=str(row[0]),
                attempt_id=str(row[1]),
                course_id=str(row[2]),
                concept_id=str(row[3]),
                evaluator_id=str(row[4]),
                evaluator_version=str(row[5]),
                check_kind=str(row[6]),
                outcome=str(row[7]),
                rubric_json=str(row[8]),
                source_ids_json=str(row[9]),
                evidence_version=int(row[10]),
                idempotency_key=str(row[11]),
                created_at=str(row[12]),
                variant_id=str(row[13]),
            )
            for row in rows
        )
        return MasteryHistory(concept_id, str(concept[0]), evidence)

    def get_or_append(
        self,
        connection: sqlite3.Connection,
        *,
        estimate_id: str,
        concept_id: str,
        state: str,
        evidence_input_hash: str,
    ) -> MasteryEstimate:
        created_at = datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")
        connection.execute(
            "INSERT OR IGNORE INTO mastery_estimate(estimate_id, concept_id, derived_state, "
            "evidence_input_hash, created_at) VALUES (?, ?, ?, ?, ?)",
            (estimate_id, concept_id, state, evidence_input_hash, created_at),
        )
        row = connection.execute(
            "SELECT estimate_id, concept_id, derived_state, evidence_input_hash, created_at "
            "FROM mastery_estimate WHERE concept_id = ? AND evidence_input_hash = ?",
            (concept_id, evidence_input_hash),
        ).fetchone()
        if row is None:
            raise MasteryRepositoryError("mastery_persistence_failed")
        return MasteryEstimate(
            estimate_id=str(row[0]),
            concept_id=str(row[1]),
            state=str(row[2]),
            evidence_input_hash=str(row[3]),
            created_at=str(row[4]),
        )


__all__ = [
    "MasteryEstimate",
    "MasteryEvidence",
    "MasteryHistory",
    "MasteryRepository",
    "MasteryRepositoryError",
]
