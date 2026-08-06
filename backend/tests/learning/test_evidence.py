from __future__ import annotations

import json
import sqlite3
import sys
from dataclasses import asdict
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[3]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from projectb.domain.learning.evaluators.schemas import MutexAnswer, MutexEvent, MutexExercise  # noqa: E402
from projectb.services.learning.attempts import AttemptError, AttemptService  # noqa: E402
from projectb.services.materials.coverage import CoverageService  # noqa: E402
from projectb.services.materials.importer import MaterialImporter  # noqa: E402
from projectb.storage.content_store import ContentStore  # noqa: E402
from projectb.storage.db import Database  # noqa: E402


def setup_attempt(tmp_path: Path, *, evaluator_id: str | None = "os.mutex.v1", feedback=None):
    database = Database(tmp_path / "projectb.sqlite3")
    database.initialize()
    connection = database.connect()
    try:
        connection.execute(
            "INSERT INTO course(course_id, name, timezone, created_at) VALUES (?, ?, ?, ?)",
            ("course-1", "Concurrency", "UTC", "2026-08-06T00:00:00Z"),
        )
    finally:
        connection.close()
    source = tmp_path / "notes.txt"
    source.write_text("mutex\n", encoding="utf-8")
    imported = MaterialImporter(database, ContentStore(tmp_path / "content")).import_batch("course-1", [source])[0]
    connection = database.connect()
    try:
        locator = connection.execute(
            "SELECT sl.locator_id FROM source_locator sl JOIN material_version mv "
            "ON mv.version_id = sl.material_version_id WHERE mv.material_id = ?",
            (imported.material_id,),
        ).fetchone()[0]
    finally:
        connection.close()
    coverage = CoverageService(database)
    concept = coverage.create_concept("course-1", "Mutex", evaluator_id=evaluator_id)
    coverage.record_decision(concept.concept_id, [locator], "confirmed")
    return database, imported, concept, AttemptService(database, feedback_wording=feedback)


def valid_exercise() -> MutexExercise:
    return MutexExercise((MutexEvent("a", "enter"), MutexEvent("a", "exit")))


def test_append_evidence_is_source_bound_structured_and_immutable(tmp_path: Path) -> None:
    database, _, concept, service = setup_attempt(tmp_path)

    evidence = service.submit(
        concept_id=concept.concept_id,
        attempt_key="attempt-key-1",
        check_kind="isomorphic",
        variant_id="mutex-1",
        exercise=valid_exercise(),
        answer=MutexAnswer(holds=True),
    )

    assert evidence.outcome == "passed"
    assert evidence.evaluator_id == "os.mutex.v1"
    assert evidence.evaluator_version == "1"
    assert evidence.source_locator_ids == tuple(sorted(evidence.source_locator_ids))
    connection = database.connect()
    try:
        attempt = connection.execute("SELECT answer_json, status FROM attempt").fetchone()
        stored = connection.execute("SELECT rubric_json, source_ids_json, evidence_version FROM learning_evidence").fetchone()
        assert json.loads(attempt[0]) == asdict(MutexAnswer(holds=True))
        assert attempt[1] == "evaluated"
        assert json.loads(stored[0]) == [asdict(item) for item in evidence.rubric]
        assert tuple(json.loads(stored[1])) == evidence.source_locator_ids
        assert stored[2] == 1
        with pytest.raises(sqlite3.IntegrityError, match="learning_evidence_immutable"):
            connection.execute("UPDATE learning_evidence SET outcome = 'incorrect'")
        with pytest.raises(sqlite3.IntegrityError, match="learning_evidence_immutable"):
            connection.execute("DELETE FROM learning_evidence")
    finally:
        connection.close()


def test_duplicate_attempt_key_returns_one_stable_evidence(tmp_path: Path) -> None:
    database, _, concept, service = setup_attempt(tmp_path)
    arguments = dict(
        concept_id=concept.concept_id,
        attempt_key="attempt-key-duplicate",
        check_kind="transfer",
        variant_id="mutex-transfer",
        exercise=valid_exercise(),
        answer=MutexAnswer(holds=True),
    )

    first = service.submit(**arguments)
    second = service.submit(**arguments)

    assert first == second
    connection = database.connect()
    try:
        assert connection.execute("SELECT count(*) FROM attempt").fetchone()[0] == 1
        assert connection.execute("SELECT count(*) FROM learning_evidence").fetchone()[0] == 1
    finally:
        connection.close()


def test_stale_source_and_explanation_only_cannot_append(tmp_path: Path) -> None:
    database, imported, concept, service = setup_attempt(tmp_path)
    connection = database.connect()
    try:
        connection.execute("DELETE FROM material WHERE material_id = ?", (imported.material_id,))
    finally:
        connection.close()

    with pytest.raises(AttemptError, match="source_stale"):
        service.submit(
            concept_id=concept.concept_id,
            attempt_key="stale",
            check_kind="isomorphic",
            variant_id="stale",
            exercise=valid_exercise(),
            answer=MutexAnswer(holds=True),
        )
    connection = database.connect()
    try:
        assert connection.execute("SELECT count(*) FROM attempt").fetchone()[0] == 0
    finally:
        connection.close()

    other_database, _, other_concept, other_service = setup_attempt(tmp_path / "other", evaluator_id=None)
    with pytest.raises(AttemptError, match="explanation_only"):
        other_service.submit(
            concept_id=other_concept.concept_id,
            attempt_key="explanation-only",
            check_kind="isomorphic",
            variant_id="none",
            exercise=valid_exercise(),
            answer=MutexAnswer(holds=True),
        )
    connection = other_database.connect()
    try:
        assert connection.execute("SELECT count(*) FROM attempt").fetchone()[0] == 0
    finally:
        connection.close()


def test_provider_failure_cannot_change_evidence_or_receive_answer(tmp_path: Path) -> None:
    captured: list[str] = []
    private_answer = "student-private-answer"

    def failing_feedback(payload: object) -> str:
        captured.append(repr(payload))
        raise RuntimeError("provider unavailable")

    database, _, concept, service = setup_attempt(tmp_path, feedback=failing_feedback)
    evidence = service.submit(
        concept_id=concept.concept_id,
        attempt_key="provider-failure",
        check_kind="isomorphic",
        variant_id="provider-safe-variant",
        exercise=valid_exercise(),
        answer=MutexAnswer(holds=True, rationale=private_answer),
    )

    assert evidence.outcome == "passed"
    assert all(private_answer not in item for item in captured)
    assert private_answer not in repr(evidence)
    connection = database.connect()
    try:
        assert connection.execute("SELECT count(*) FROM learning_evidence").fetchone()[0] == 1
    finally:
        connection.close()
