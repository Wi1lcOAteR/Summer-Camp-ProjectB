from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from typing import Any

from projectb.domain.learning.evaluators.schemas import Outcome, RubricItem
from projectb.providers.port import (
    ExplanationInput,
    FeedbackInput,
    PracticeInput,
    ProviderCandidate,
    ProviderInput,
    ProviderOperation,
    SourceFragment,
)
from projectb.providers.registry import ProviderRegistry
from projectb.repositories.provider_profiles import ProviderProfileError, ProviderProfileRepository


OPAQUE_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")


class ConsentError(RuntimeError):
    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


@dataclass(frozen=True, slots=True)
class ConsentPreview:
    operation: ProviderOperation
    profile_id: str
    policy_fingerprint: str
    max_tokens: int
    max_cost_microusd: int
    nonce: str
    request: ProviderInput
    request_hash: str


@dataclass(frozen=True, slots=True)
class ConsentRecord:
    consent_id: str
    request_hash: str
    profile_id: str
    created_at: str


class ConsentService:
    def __init__(self, database: Any) -> None:
        self.database = database
        self.profiles = ProviderProfileRepository(database)

    def preview_explanation(
        self,
        *,
        locator_ids: tuple[str, ...],
        profile_id: str,
        instruction: str,
        max_tokens: int,
        max_cost_microusd: int,
        nonce: str,
    ) -> ConsentPreview:
        request = ExplanationInput(self._sources(locator_ids), instruction)
        return self._preview("generate_explanation", profile_id, request, max_tokens, max_cost_microusd, nonce)

    def preview_practice(
        self,
        *,
        locator_ids: tuple[str, ...],
        profile_id: str,
        evaluator_id: str,
        variant_id: str,
        max_tokens: int,
        max_cost_microusd: int,
        nonce: str,
    ) -> ConsentPreview:
        request = PracticeInput(self._sources(locator_ids), evaluator_id, variant_id)
        return self._preview("generate_practice_candidate", profile_id, request, max_tokens, max_cost_microusd, nonce)

    def preview_feedback(
        self,
        *,
        locator_ids: tuple[str, ...],
        profile_id: str,
        outcome: Outcome,
        rubric: tuple[RubricItem, ...],
        max_tokens: int,
        max_cost_microusd: int,
        nonce: str,
    ) -> ConsentPreview:
        request = FeedbackInput(self._sources(locator_ids), outcome, rubric)
        return self._preview("generate_feedback_wording", profile_id, request, max_tokens, max_cost_microusd, nonce)

    def grant(self, preview: ConsentPreview) -> ConsentRecord:
        if self._request_hash(preview) != preview.request_hash:
            raise ConsentError("consent_mismatch")
        profile = self._profile(preview.profile_id)
        if profile.policy_fingerprint != preview.policy_fingerprint or preview.max_cost_microusd > profile.budget_limit:
            raise ConsentError("consent_policy_mismatch")
        consent_id = "consent-" + hashlib.sha256(f"{preview.nonce}:{preview.request_hash}".encode()).hexdigest()
        source_metadata = {
            "max_cost_microusd": preview.max_cost_microusd,
            "max_tokens": preview.max_tokens,
            "nonce": preview.nonce,
            "operation": preview.operation,
            "source_hashes": {source.locator_id: source.content_hash for source in preview.request.sources},
            "versions": {source.locator_id: source.material_version_id for source in preview.request.sources},
        }
        created_at = self._now()
        connection = self.database.connect()
        try:
            connection.execute(
                "INSERT OR IGNORE INTO consent_record(consent_id, port, locator_ids_json, source_hashes_json, "
                "preview_hash, profile_id, policy_fingerprint, budget_limit, created_at) "
                "VALUES (?, 'P', ?, ?, ?, ?, ?, ?, ?)",
                (
                    consent_id,
                    json.dumps(sorted(source.locator_id for source in preview.request.sources), separators=(",", ":")),
                    json.dumps(source_metadata, ensure_ascii=True, separators=(",", ":"), sort_keys=True),
                    preview.request_hash,
                    preview.profile_id,
                    preview.policy_fingerprint,
                    preview.max_cost_microusd,
                    created_at,
                ),
            )
        finally:
            connection.close()
        return ConsentRecord(consent_id, preview.request_hash, preview.profile_id, created_at)

    def execute(
        self,
        consent_id: str,
        preview: ConsentPreview,
        registry: ProviderRegistry,
    ) -> ProviderCandidate:
        if self._request_hash(preview) != preview.request_hash:
            raise ConsentError("consent_mismatch")
        connection = self.database.connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute(
                "SELECT locator_ids_json, source_hashes_json, preview_hash, profile_id, policy_fingerprint, "
                "budget_limit FROM consent_record WHERE consent_id = ?",
                (consent_id,),
            ).fetchone()
            if row is None:
                raise ConsentError("consent_required")
            expected = self._record_identity(preview)
            observed = (str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]), int(row[5]))
            if observed != expected:
                raise ConsentError("consent_mismatch")
            current_sources = self._sources_with_connection(connection, tuple(source.locator_id for source in preview.request.sources))
            if current_sources != preview.request.sources:
                raise ConsentError("source_stale")
            consumed = connection.execute(
                "SELECT 1 FROM audit_event WHERE action = 'provider_consent_consumed' "
                "AND opaque_refs_json = ? LIMIT 1",
                (json.dumps([consent_id], separators=(",", ":")),),
            ).fetchone()
            if consumed is not None:
                raise ConsentError("consent_already_used")
            provider = registry.resolve(preview.profile_id)
            if provider is None:
                raise ConsentError("provider_unconfigured")
            event_id = "audit-" + hashlib.sha256(consent_id.encode()).hexdigest()
            connection.execute(
                "INSERT INTO audit_event(event_id, actor, action, result, opaque_refs_json, fingerprint, "
                "error_code, created_at) VALUES (?, 'user', 'provider_consent_consumed', 'accepted', ?, ?, NULL, ?)",
                (event_id, json.dumps([consent_id], separators=(",", ":")), preview.request_hash, self._now()),
            )
            connection.commit()
        except BaseException:
            connection.rollback()
            raise
        finally:
            connection.close()

        if preview.operation == "generate_explanation":
            assert isinstance(preview.request, ExplanationInput)
            return provider.generate_explanation(preview.request)
        if preview.operation == "generate_practice_candidate":
            assert isinstance(preview.request, PracticeInput)
            return provider.generate_practice_candidate(preview.request)
        assert isinstance(preview.request, FeedbackInput)
        return provider.generate_feedback_wording(preview.request)

    def _preview(
        self,
        operation: ProviderOperation,
        profile_id: str,
        request: ProviderInput,
        max_tokens: int,
        max_cost_microusd: int,
        nonce: str,
    ) -> ConsentPreview:
        profile = self._profile(profile_id)
        if OPAQUE_PATTERN.fullmatch(nonce) is None:
            raise ConsentError("nonce_invalid")
        if type(max_tokens) is not int or max_tokens <= 0 or type(max_cost_microusd) is not int or max_cost_microusd < 0:
            raise ConsentError("budget_invalid")
        if max_cost_microusd > profile.budget_limit:
            raise ConsentError("budget_exceeded")
        provisional = ConsentPreview(
            operation,
            profile_id,
            profile.policy_fingerprint,
            max_tokens,
            max_cost_microusd,
            nonce,
            request,
            "",
        )
        request_hash = self._request_hash(provisional)
        return ConsentPreview(operation, profile_id, profile.policy_fingerprint, max_tokens, max_cost_microusd, nonce, request, request_hash)

    @staticmethod
    def _request_hash(preview: ConsentPreview) -> str:
        identity = {
            "max_cost_microusd": preview.max_cost_microusd,
            "max_tokens": preview.max_tokens,
            "nonce": preview.nonce,
            "operation": preview.operation,
            "policy_fingerprint": preview.policy_fingerprint,
            "profile_id": preview.profile_id,
            "request": asdict(preview.request),
        }
        canonical = json.dumps(identity, ensure_ascii=True, separators=(",", ":"), sort_keys=True)
        return hashlib.sha256(canonical.encode()).hexdigest()

    def _record_identity(self, preview: ConsentPreview) -> tuple[str, str, str, str, str, int]:
        metadata = {
            "max_cost_microusd": preview.max_cost_microusd,
            "max_tokens": preview.max_tokens,
            "nonce": preview.nonce,
            "operation": preview.operation,
            "source_hashes": {source.locator_id: source.content_hash for source in preview.request.sources},
            "versions": {source.locator_id: source.material_version_id for source in preview.request.sources},
        }
        return (
            json.dumps(sorted(source.locator_id for source in preview.request.sources), separators=(",", ":")),
            json.dumps(metadata, ensure_ascii=True, separators=(",", ":"), sort_keys=True),
            preview.request_hash,
            preview.profile_id,
            preview.policy_fingerprint,
            preview.max_cost_microusd,
        )

    def _profile(self, profile_id: str):
        try:
            return self.profiles.get(profile_id)
        except ProviderProfileError as error:
            raise ConsentError(error.code) from None

    def _sources(self, locator_ids: tuple[str, ...]) -> tuple[SourceFragment, ...]:
        connection = self.database.connect()
        try:
            return self._sources_with_connection(connection, locator_ids)
        finally:
            connection.close()

    @staticmethod
    def _sources_with_connection(connection: Any, locator_ids: tuple[str, ...]) -> tuple[SourceFragment, ...]:
        if not locator_ids or len(set(locator_ids)) != len(locator_ids):
            raise ConsentError("source_selection_invalid")
        sources: list[SourceFragment] = []
        for locator_id in sorted(locator_ids):
            row = connection.execute(
                "SELECT sl.content_hash, mv.version_id, mv.locator_index_json, mv.rowid, "
                "(SELECT max(current.rowid) FROM material_version current WHERE current.material_id = mv.material_id) "
                "FROM source_locator sl JOIN material_version mv ON mv.version_id = sl.material_version_id "
                "WHERE sl.locator_id = ?",
                (locator_id,),
            ).fetchone()
            if row is None or int(row[3]) != int(row[4]):
                raise ConsentError("source_stale")
            decisions = connection.execute(
                "SELECT cd.locator_ids_json FROM coverage_decision cd "
                "WHERE cd.decision = 'confirmed' AND cd.version = "
                "(SELECT max(latest.version) FROM coverage_decision latest WHERE latest.concept_id = cd.concept_id)"
            ).fetchall()
            try:
                confirmed = any(locator_id in json.loads(decision[0]) for decision in decisions)
            except (TypeError, json.JSONDecodeError):
                raise ConsentError("coverage_invalid") from None
            if not confirmed:
                raise ConsentError("coverage_unconfirmed")
            try:
                index = json.loads(row[2])
                item = next(entry for entry in index if entry.get("locator_id") == locator_id)
                text = item["text"]
            except (TypeError, ValueError, KeyError, StopIteration, json.JSONDecodeError):
                raise ConsentError("source_stale") from None
            sources.append(SourceFragment(locator_id, str(row[1]), str(row[0]), str(text)))
        return tuple(sources)

    @staticmethod
    def _now() -> str:
        return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")
