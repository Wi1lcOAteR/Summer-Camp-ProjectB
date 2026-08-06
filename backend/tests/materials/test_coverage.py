from __future__ import annotations

import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[3]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from projectb.services.materials.coverage import CoverageError, CoverageService  # noqa: E402
from projectb.services.materials.delete import MaterialDeletionService  # noqa: E402
from projectb.services.materials.importer import MaterialImporter  # noqa: E402
from projectb.storage.content_store import ContentStore  # noqa: E402
from projectb.storage.db import Database  # noqa: E402
from test_importer import upgraded_extractor  # noqa: E402


def setup_system(tmp_path: Path) -> tuple[Database, ContentStore, MaterialImporter, CoverageService]:
    database = Database(tmp_path / "projectb.sqlite3")
    database.initialize()
    connection = database.connect()
    try:
        connection.executemany(
            "INSERT INTO course(course_id, name, timezone, created_at) VALUES (?, ?, ?, ?)",
            [
                ("course-1", "Concurrency", "UTC", "2026-08-06T00:00:00Z"),
                ("course-2", "Operating Systems", "UTC", "2026-08-06T00:00:00Z"),
            ],
        )
    finally:
        connection.close()
    store = ContentStore(tmp_path / "content")
    return database, store, MaterialImporter(database, store), CoverageService(database)


def locator_ids(database: Database, material_id: str) -> tuple[str, ...]:
    connection = database.connect()
    try:
        return tuple(
            row[0]
            for row in connection.execute(
                "SELECT sl.locator_id FROM source_locator sl "
                "JOIN material_version mv ON mv.version_id = sl.material_version_id "
                "WHERE mv.material_id = ? ORDER BY sl.locator_id",
                (material_id,),
            )
        )
    finally:
        connection.close()


def test_multiple_concepts_require_latest_explicit_confirmation(tmp_path: Path) -> None:
    database, _, importer, coverage = setup_system(tmp_path)
    source = tmp_path / "notes.txt"
    source.write_text("mutex\nrace\n", encoding="utf-8")
    imported = importer.import_batch("course-1", [source])[0]
    locators = locator_ids(database, imported.material_id or "")
    mutex = coverage.create_concept("course-1", "Mutex", evaluator_id="os.mutex.v1")
    race = coverage.create_concept("course-1", "Race", evaluator_id="os.race.v1")

    coverage.record_decision(mutex.concept_id, [locators[0]], "confirmed")
    coverage.record_decision(race.concept_id, [locators[1]], "rejected")

    assert coverage.authorize(mutex.concept_id) == (locators[0],)
    with pytest.raises(CoverageError, match="coverage_unconfirmed"):
        coverage.authorize(race.concept_id)
    coverage.record_decision(mutex.concept_id, [locators[0]], "rejected")
    with pytest.raises(CoverageError, match="coverage_unconfirmed"):
        coverage.authorize(mutex.concept_id)


def test_parser_upgrade_makes_old_locator_stale_until_reconfirmed(tmp_path: Path) -> None:
    database, store, importer, coverage = setup_system(tmp_path)
    source = tmp_path / "notes.md"
    source.write_text("# Mutex\n", encoding="utf-8")
    first = importer.import_batch("course-1", [source])[0]
    old_locator = locator_ids(database, first.material_id or "")[0]
    concept = coverage.create_concept("course-1", "Mutex")
    coverage.record_decision(concept.concept_id, [old_locator], "confirmed")
    assert coverage.authorize(concept.concept_id) == (old_locator,)

    upgraded = MaterialImporter(database, store, extractor=upgraded_extractor)
    upgraded.import_batch("course-1", [source])

    with pytest.raises(CoverageError, match="source_stale"):
        coverage.authorize(concept.concept_id)
    current_locator = next(locator for locator in locator_ids(database, first.material_id or "") if locator != old_locator)
    coverage.record_decision(concept.concept_id, [current_locator], "confirmed")
    assert coverage.authorize(concept.concept_id) == (current_locator,)


def test_material_delete_invalidates_future_use_but_preserves_decision_history(tmp_path: Path) -> None:
    database, store, importer, coverage = setup_system(tmp_path)
    source = tmp_path / "notes.txt"
    source.write_text("deadlock\n", encoding="utf-8")
    imported = importer.import_batch("course-1", [source])[0]
    locator = locator_ids(database, imported.material_id or "")[0]
    concept = coverage.create_concept("course-1", "Deadlock", evaluator_id="os.deadlock.v1")
    coverage.record_decision(concept.concept_id, [locator], "confirmed")

    result = MaterialDeletionService(database, store).delete(imported.material_id or "")

    assert result.status == "deleted"
    with pytest.raises(CoverageError, match="source_stale"):
        coverage.authorize(concept.concept_id)
    connection = database.connect()
    try:
        assert connection.execute("SELECT count(*) FROM coverage_decision").fetchone()[0] == 1
        assert connection.execute("SELECT count(*) FROM knowledge_concept").fetchone()[0] == 1
        assert connection.execute("SELECT count(*) FROM source_locator").fetchone()[0] == 0
    finally:
        connection.close()


def test_shared_blob_survives_first_course_delete_and_last_delete_removes_it(tmp_path: Path) -> None:
    database, store, importer, _ = setup_system(tmp_path)
    source = tmp_path / "shared.txt"
    source.write_text("shared\n", encoding="utf-8")
    first = importer.import_batch("course-1", [source])[0]
    second = importer.import_batch("course-2", [source])[0]
    blob = store.path_for(first.content_hash or "")
    deletion = MaterialDeletionService(database, store)

    assert deletion.delete(first.material_id or "").status == "deleted"
    assert blob.is_file()
    assert deletion.delete(second.material_id or "").status == "deleted"
    assert not blob.exists()
    connection = database.connect()
    try:
        assert connection.execute("SELECT count(*) FROM blob_object").fetchone()[0] == 0
        assert connection.execute("SELECT count(*) FROM material_blob_ref").fetchone()[0] == 0
    finally:
        connection.close()


def test_failed_final_blob_delete_leaves_retryable_tombstone(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    database, store, importer, _ = setup_system(tmp_path)
    source = tmp_path / "single.txt"
    source.write_text("single\n", encoding="utf-8")
    imported = importer.import_batch("course-1", [source])[0]
    deletion = MaterialDeletionService(database, store)
    real_remove = store.remove
    monkeypatch.setattr(store, "remove", lambda _: (_ for _ in ()).throw(OSError("locked")))

    failed = deletion.delete(imported.material_id or "")

    assert (failed.status, failed.retryable) == ("delete_pending", True)
    connection = database.connect()
    try:
        assert connection.execute(
            "SELECT delete_pending FROM blob_object WHERE content_hash = ?", (imported.content_hash,)
        ).fetchone()[0] == 1
        assert connection.execute("SELECT count(*) FROM material").fetchone()[0] == 0
    finally:
        connection.close()

    monkeypatch.setattr(store, "remove", real_remove)
    retried = deletion.retry_pending(imported.content_hash or "")
    assert retried.status == "deleted"
    assert not store.path_for(imported.content_hash or "").exists()
