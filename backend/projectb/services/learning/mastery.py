from __future__ import annotations

import hashlib
import json
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from projectb.repositories.mastery import (
    MasteryEstimate,
    MasteryEvidence,
    MasteryHistory,
    MasteryRepository,
    MasteryRepositoryError,
)


class MasteryError(RuntimeError):
    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


class MasteryService:
    def __init__(self, database: Any) -> None:
        self.repository = MasteryRepository(database)

    def derive(self, concept_id: str, *, evidence_ids: tuple[str, ...] | None = None) -> MasteryEstimate:
        try:
            with self.repository.locked() as connection:
                history = self.repository.load_history(connection, concept_id)
                self._require_complete_history(history, evidence_ids)
                state = self._derive_state(history)
                input_hash = self._input_hash(history)
                estimate_id = "estimate-" + hashlib.sha256(
                    f"{concept_id}:{input_hash}:v1".encode("utf-8")
                ).hexdigest()
                return self.repository.get_or_append(
                    connection,
                    estimate_id=estimate_id,
                    concept_id=concept_id,
                    state=state,
                    evidence_input_hash=input_hash,
                )
        except MasteryRepositoryError as error:
            raise MasteryError(error.code) from None

    @staticmethod
    def _require_complete_history(history: MasteryHistory, evidence_ids: tuple[str, ...] | None) -> None:
        if evidence_ids is None:
            return
        actual = {item.evidence_id for item in history.evidence}
        supplied = set(evidence_ids)
        if len(evidence_ids) != len(supplied) or supplied != actual:
            raise MasteryError("incomplete_evidence_history")

    @classmethod
    def _derive_state(cls, history: MasteryHistory) -> str:
        try:
            timezone = ZoneInfo(history.course_timezone)
        except (ZoneInfoNotFoundError, ValueError):
            raise MasteryError("course_timezone_invalid") from None

        isomorphic = [
            item for item in history.evidence if item.check_kind == "isomorphic" and item.outcome == "passed"
        ]
        transfer = [
            item for item in history.evidence if item.check_kind == "transfer" and item.outcome == "passed"
        ]
        if not isomorphic or not transfer:
            return "unknown"

        delayed = [
            item
            for item in history.evidence
            if item.check_kind == "delayed_variant" and item.outcome == "passed"
        ]
        for iso in isomorphic:
            iso_time = cls._timestamp(iso)
            for transferred in transfer:
                transfer_time = cls._timestamp(transferred)
                demonstrated_at = max(iso_time, transfer_time)
                baseline_variants = {iso.variant_id, transferred.variant_id}
                for candidate in delayed:
                    candidate_time = cls._timestamp(candidate)
                    if (
                        candidate_time.astimezone(timezone).date()
                        > demonstrated_at.astimezone(timezone).date()
                        and candidate.variant_id not in baseline_variants
                    ):
                        return "retained"
        return "demonstrated_now"

    @staticmethod
    def _timestamp(evidence: MasteryEvidence) -> datetime:
        try:
            timestamp = datetime.fromisoformat(evidence.created_at.replace("Z", "+00:00"))
        except ValueError:
            raise MasteryError("evidence_timestamp_invalid") from None
        if timestamp.tzinfo is None or not evidence.created_at.endswith("Z"):
            raise MasteryError("evidence_timestamp_invalid")
        return timestamp

    @staticmethod
    def _input_hash(history: MasteryHistory) -> str:
        try:
            evidence = [
                {
                    "attempt_id": item.attempt_id,
                    "check_kind": item.check_kind,
                    "concept_id": item.concept_id,
                    "course_id": item.course_id,
                    "created_at": item.created_at,
                    "evaluator_id": item.evaluator_id,
                    "evaluator_version": item.evaluator_version,
                    "evidence_id": item.evidence_id,
                    "evidence_version": item.evidence_version,
                    "idempotency_key": item.idempotency_key,
                    "outcome": item.outcome,
                    "rubric": json.loads(item.rubric_json),
                    "source_ids": json.loads(item.source_ids_json),
                    "variant_id": item.variant_id,
                }
                for item in history.evidence
            ]
        except json.JSONDecodeError:
            raise MasteryError("evidence_payload_invalid") from None
        payload = {
            "concept_id": history.concept_id,
            "course_timezone": history.course_timezone,
            "derivation_version": 1,
            "evidence": evidence,
        }
        canonical = json.dumps(payload, ensure_ascii=True, separators=(",", ":"), sort_keys=True)
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


__all__ = ["MasteryError", "MasteryEstimate", "MasteryService"]
