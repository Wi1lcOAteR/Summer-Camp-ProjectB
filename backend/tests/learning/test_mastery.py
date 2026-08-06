from __future__ import annotations

import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[3]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from projectb.services.learning.mastery import MasteryError, MasteryService  # noqa: E402
from projectb.storage.db import Database  # noqa: E402


def setup_database(tmp_path: Path) -> tuple[Database, str]:
    database = Database(tmp_path / "projectb.sqlite3")
    database.initialize()
    connection = database.connect()
    try:
        connection.execute(
            "INSERT INTO course(course_id, name, timezone, created_at) VALUES (?, ?, ?, ?)",
            ("course-1", "Concurrency", "Asia/Shanghai", "2026-08-06T00:00:00Z"),
        )
        connection.execute(
            "INSERT INTO knowledge_concept(concept_id, course_id, name, evaluator_id, version, state, created_at) "
            "VALUES (?, ?, ?, ?, 1, 'active', ?)",
            ("concept-1", "course-1", "Mutex", "os.mutex.v1", "2026-08-06T00:00:00Z"),
        )
    finally:
        connection.close()
    return database, "concept-1"


def add_evidence(
    database: Database,
    identifier: str,
    *,
    check_kind: str,
    outcome: str,
    variant_id: str,
    created_at: str,
) -> str:
    attempt_id = f"attempt-{identifier}"
    evidence_id = f"evidence-{identifier}"
    connection = database.connect()
    try:
        connection.execute(
            "INSERT INTO attempt(attempt_id, attempt_key, concept_id, check_kind, variant_id, answer_json, "
            "status, created_at, updated_at) VALUES (?, ?, 'concept-1', ?, ?, '{}', 'evaluated', ?, ?)",
            (attempt_id, f"key-{identifier}", check_kind, variant_id, created_at, created_at),
        )
        connection.execute(
            "INSERT INTO learning_evidence(evidence_id, attempt_id, course_id, concept_id, evaluator_id, "
            "evaluator_version, check_kind, outcome, rubric_json, source_ids_json, evidence_version, "
            "idempotency_key, created_at) VALUES (?, ?, 'course-1', 'concept-1', 'os.mutex.v1', '1', ?, ?, "
            "'[]', '[]', 1, ?, ?)",
            (evidence_id, attempt_id, check_kind, outcome, f"idem-{identifier}", created_at),
        )
    finally:
        connection.close()
    return evidence_id


def test_isomorphic_and_transfer_passes_are_required_for_demonstrated(tmp_path: Path) -> None:
    database, concept_id = setup_database(tmp_path)
    service = MasteryService(database)
    iso = add_evidence(
        database,
        "iso",
        check_kind="isomorphic",
        outcome="passed",
        variant_id="iso-1",
        created_at="2026-08-06T14:00:00Z",
    )
    assert service.derive(concept_id).state == "unknown"
    transfer = add_evidence(
        database,
        "transfer",
        check_kind="transfer",
        outcome="passed",
        variant_id="transfer-1",
        created_at="2026-08-06T14:30:00Z",
    )

    result = service.derive(concept_id, evidence_ids=(transfer, iso))
    assert result.state == "demonstrated_now"
    assert len(result.evidence_input_hash) == 64


def test_delayed_variant_requires_later_course_local_day_and_distinct_variant(tmp_path: Path) -> None:
    database, concept_id = setup_database(tmp_path)
    add_evidence(
        database,
        "iso",
        check_kind="isomorphic",
        outcome="passed",
        variant_id="base-1",
        created_at="2026-08-06T15:00:00Z",
    )
    add_evidence(
        database,
        "transfer",
        check_kind="transfer",
        outcome="passed",
        variant_id="base-2",
        created_at="2026-08-06T15:10:00Z",
    )
    add_evidence(
        database,
        "same-day",
        check_kind="delayed_variant",
        outcome="passed",
        variant_id="delayed-1",
        created_at="2026-08-06T15:30:00Z",
    )
    service = MasteryService(database)
    assert service.derive(concept_id).state == "demonstrated_now"

    add_evidence(
        database,
        "next-day-same-variant",
        check_kind="delayed_variant",
        outcome="passed",
        variant_id="base-2",
        created_at="2026-08-06T16:20:00Z",
    )
    assert service.derive(concept_id).state == "demonstrated_now"
    add_evidence(
        database,
        "next-day",
        check_kind="delayed_variant",
        outcome="passed",
        variant_id="delayed-2",
        created_at="2026-08-06T16:30:00Z",
    )
    assert service.derive(concept_id).state == "retained"


def test_ignored_outcomes_do_not_lower_mastery(tmp_path: Path) -> None:
    database, concept_id = setup_database(tmp_path)
    for identifier, kind, outcome, when in (
        ("iso", "isomorphic", "passed", "2026-08-05T10:00:00Z"),
        ("transfer", "transfer", "passed", "2026-08-05T11:00:00Z"),
        ("delayed", "delayed_variant", "passed", "2026-08-06T10:00:00Z"),
        ("failure", "transfer", "incorrect", "2026-08-06T11:00:00Z"),
        ("skipped", "delayed_variant", "skipped", "2026-08-06T12:00:00Z"),
    ):
        add_evidence(database, identifier, check_kind=kind, outcome=outcome, variant_id=identifier, created_at=when)

    assert MasteryService(database).derive(concept_id).state == "retained"


def test_complete_history_order_is_stable_and_omission_fails_closed(tmp_path: Path) -> None:
    database, concept_id = setup_database(tmp_path)
    first = add_evidence(
        database,
        "first",
        check_kind="isomorphic",
        outcome="passed",
        variant_id="v1",
        created_at="2026-08-06T10:00:00Z",
    )
    second = add_evidence(
        database,
        "second",
        check_kind="transfer",
        outcome="passed",
        variant_id="v2",
        created_at="2026-08-06T11:00:00Z",
    )
    service = MasteryService(database)

    ordered = service.derive(concept_id, evidence_ids=(first, second))
    shuffled = service.derive(concept_id, evidence_ids=(second, first))

    assert ordered == shuffled
    with pytest.raises(MasteryError, match="incomplete_evidence_history"):
        service.derive(concept_id, evidence_ids=(first,))
    connection = database.connect()
    try:
        assert connection.execute("SELECT count(*) FROM mastery_estimate").fetchone()[0] == 1
        assert connection.execute("SELECT created_at FROM mastery_estimate").fetchone()[0].endswith("Z")
    finally:
        connection.close()
