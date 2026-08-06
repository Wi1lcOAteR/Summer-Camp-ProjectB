from __future__ import annotations

import json
import sys
from dataclasses import replace
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[3]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from projectb.domain.learning.evaluators.schemas import RubricItem  # noqa: E402
from projectb.providers.mock import MockProvider  # noqa: E402
from projectb.providers.port import ExplanationInput, ProviderError  # noqa: E402
from projectb.providers.registry import ProviderRegistry  # noqa: E402
from projectb.repositories.provider_profiles import ProviderProfileRepository  # noqa: E402
from projectb.services.providers.consent import ConsentError, ConsentService  # noqa: E402
from projectb.storage.db import Database  # noqa: E402


def setup_system(tmp_path: Path) -> tuple[Database, ConsentService, ProviderRegistry, MockProvider]:
    database = Database(tmp_path / "projectb.sqlite3")
    database.initialize()
    locator_index = json.dumps(
        [
            {
                "locator_id": "locator-1",
                "material_version_id": "version-1",
                "content_hash": "a" * 64,
                "kind": "text_lines",
                "line_start": 1,
                "line_end": 1,
                "text": "Mutex protects a critical section.",
            },
            {
                "locator_id": "locator-2",
                "material_version_id": "version-1",
                "content_hash": "a" * 64,
                "kind": "text_lines",
                "line_start": 2,
                "line_end": 2,
                "text": "This line has not been confirmed.",
            },
        ],
        separators=(",", ":"),
    )
    connection = database.connect()
    try:
        connection.execute(
            "INSERT INTO course(course_id, name, timezone, created_at) VALUES ('course-1', 'OS', 'UTC', ?) ",
            ("2026-08-06T00:00:00Z",),
        )
        connection.execute(
            "INSERT INTO material(material_id, course_id, filename, media_type, content_hash, status, created_at) "
            "VALUES ('material-1', 'course-1', 'notes.txt', 'text/plain', ?, 'ready', ?)",
            ("a" * 64, "2026-08-06T00:00:00Z"),
        )
        connection.execute(
            "INSERT INTO material_version(version_id, material_id, parser_id, parser_version, "
            "extraction_contract_version, extraction_status, locator_index_json, content_hash, created_at) "
            "VALUES ('version-1', 'material-1', 'text', '1', '1', 'ready', ?, ?, ?)",
            (locator_index, "a" * 64, "2026-08-06T00:00:00Z"),
        )
        connection.execute(
            "INSERT INTO source_locator(locator_id, material_version_id, content_hash, locator_kind, "
            "line_start, line_end) VALUES ('locator-1', 'version-1', ?, 'text_lines', 1, 1)",
            ("a" * 64,),
        )
        connection.execute(
            "INSERT INTO source_locator(locator_id, material_version_id, content_hash, locator_kind, "
            "line_start, line_end) VALUES ('locator-2', 'version-1', ?, 'text_lines', 2, 2)",
            ("a" * 64,),
        )
        connection.execute(
            "INSERT INTO knowledge_concept(concept_id, course_id, name, evaluator_id, version, state, created_at) "
            "VALUES ('concept-1', 'course-1', 'Mutex', 'os.mutex.v1', 1, 'active', ?)",
            ("2026-08-06T00:00:00Z",),
        )
        connection.execute(
            "INSERT INTO coverage_decision(decision_id, concept_id, locator_ids_json, decision, version, confirmed_at) "
            "VALUES ('decision-1', 'concept-1', '[\"locator-1\"]', 'confirmed', 1, ?)",
            ("2026-08-06T00:00:00Z",),
        )
    finally:
        connection.close()
    profiles = ProviderProfileRepository(database)
    profiles.add(
        profile_id="profile-1",
        adapter_id="mock",
        model_id="deterministic",
        budget_limit=1000,
        credential_ref="credential-ref",
        config_fingerprint="b" * 64,
        policy_fingerprint="c" * 64,
    )
    registry = ProviderRegistry("test")
    mock = MockProvider()
    registry.register("profile-1", mock)
    return database, ConsentService(database), registry, mock


def authority_counts(database: Database) -> dict[str, int]:
    connection = database.connect()
    try:
        return {
            table: int(connection.execute(f"SELECT count(*) FROM {table}").fetchone()[0])
            for table in ("coverage_decision", "learning_evidence", "mastery_estimate", "review_plan_revision")
        }
    finally:
        connection.close()


def test_no_matching_consent_means_zero_calls_and_exact_match_is_single_use(tmp_path: Path) -> None:
    database, service, registry, mock = setup_system(tmp_path)
    preview = service.preview_explanation(
        locator_ids=("locator-1",),
        profile_id="profile-1",
        instruction="Explain mutex",
        max_tokens=200,
        max_cost_microusd=500,
        nonce="nonce-1",
    )
    with pytest.raises(ConsentError, match="consent_required"):
        service.execute("missing", preview, registry)
    assert mock.network_count == 0
    before = authority_counts(database)

    consent = service.grant(preview)
    candidate = service.execute(consent.consent_id, preview, registry)
    assert candidate.authoritative is False
    assert mock.network_count == 1
    with pytest.raises(ConsentError, match="consent_already_used"):
        service.execute(consent.consent_id, preview, registry)
    assert mock.network_count == 1

    assert authority_counts(database) == before


def test_request_mismatch_and_stale_source_fail_before_provider_call(tmp_path: Path) -> None:
    database, service, registry, mock = setup_system(tmp_path)
    preview = service.preview_practice(
        locator_ids=("locator-1",),
        profile_id="profile-1",
        evaluator_id="os.mutex.v1",
        variant_id="variant-1",
        max_tokens=300,
        max_cost_microusd=700,
        nonce="nonce-2",
    )
    consent = service.grant(preview)
    changed = service.preview_practice(
        locator_ids=("locator-1",),
        profile_id="profile-1",
        evaluator_id="os.mutex.v1",
        variant_id="variant-2",
        max_tokens=300,
        max_cost_microusd=700,
        nonce="nonce-2",
    )
    with pytest.raises(ConsentError, match="consent_mismatch"):
        service.execute(consent.consent_id, changed, registry)
    assert mock.network_count == 0

    connection = database.connect()
    try:
        connection.execute(
            "INSERT INTO material_version(version_id, material_id, parser_id, parser_version, "
            "extraction_contract_version, extraction_status, locator_index_json, content_hash, created_at) "
            "VALUES ('version-2', 'material-1', 'text', '2', '1', 'ready', '[]', ?, ?)",
            ("a" * 64, "2026-08-06T01:00:00Z"),
        )
    finally:
        connection.close()
    with pytest.raises(ConsentError, match="source_stale"):
        service.execute(consent.consent_id, preview, registry)
    assert mock.network_count == 0


def test_feedback_preview_contains_only_rubric_and_confirmed_source(tmp_path: Path) -> None:
    _, service, registry, mock = setup_system(tmp_path)
    preview = service.preview_feedback(
        locator_ids=("locator-1",),
        profile_id="profile-1",
        outcome="partial",
        rubric=(RubricItem("mutual_exclusion", False, "overlap"),),
        max_tokens=100,
        max_cost_microusd=200,
        nonce="nonce-3",
    )
    consent = service.grant(preview)
    service.execute(consent.consent_id, preview, registry)

    assert "student" not in mock.last_request_text.lower()
    assert "overlap" in mock.last_request_text


def test_budget_policy_and_nonce_are_bound(tmp_path: Path) -> None:
    _, service, registry, mock = setup_system(tmp_path)
    preview = service.preview_explanation(
        locator_ids=("locator-1",),
        profile_id="profile-1",
        instruction="Explain",
        max_tokens=200,
        max_cost_microusd=500,
        nonce="nonce-4",
    )
    consent = service.grant(preview)
    changed = service.preview_explanation(
        locator_ids=("locator-1",),
        profile_id="profile-1",
        instruction="Explain",
        max_tokens=201,
        max_cost_microusd=500,
        nonce="nonce-4",
    )
    with pytest.raises(ConsentError, match="consent_mismatch"):
        service.execute(consent.consent_id, changed, registry)
    assert mock.network_count == 0


def test_reconstructed_preview_cannot_reuse_hash_for_changed_payload(tmp_path: Path) -> None:
    _, service, registry, mock = setup_system(tmp_path)
    preview = service.preview_explanation(
        locator_ids=("locator-1",),
        profile_id="profile-1",
        instruction="Explain",
        max_tokens=200,
        max_cost_microusd=500,
        nonce="nonce-5",
    )
    consent = service.grant(preview)
    changed = replace(preview, request=ExplanationInput(preview.request.sources, "Different instruction"))  # type: ignore[union-attr]

    with pytest.raises(ConsentError, match="consent_mismatch"):
        service.execute(consent.consent_id, changed, registry)
    assert mock.network_count == 0


def test_unconfirmed_current_locator_cannot_enter_preview(tmp_path: Path) -> None:
    _, service, _, mock = setup_system(tmp_path)

    with pytest.raises(ConsentError, match="coverage_unconfirmed"):
        service.preview_explanation(
            locator_ids=("locator-2",),
            profile_id="profile-1",
            instruction="Explain",
            max_tokens=200,
            max_cost_microusd=500,
            nonce="nonce-6",
        )
    assert mock.network_count == 0


@pytest.mark.parametrize("mode", ["schema", "timeout", "error"])
def test_provider_failure_is_isolated_and_spends_consent(tmp_path: Path, mode: str) -> None:
    database, service, registry, _ = setup_system(tmp_path)
    failing = MockProvider(mode=mode)  # type: ignore[arg-type]
    registry.register("profile-1", failing)
    preview = service.preview_explanation(
        locator_ids=("locator-1",),
        profile_id="profile-1",
        instruction="Explain",
        max_tokens=200,
        max_cost_microusd=500,
        nonce=f"nonce-{mode}",
    )
    consent = service.grant(preview)
    before = authority_counts(database)

    with pytest.raises(ProviderError, match=f"provider_{mode}"):
        service.execute(consent.consent_id, preview, registry)
    with pytest.raises(ConsentError, match="consent_already_used"):
        service.execute(consent.consent_id, preview, registry)

    assert failing.network_count == 1
    assert authority_counts(database) == before
