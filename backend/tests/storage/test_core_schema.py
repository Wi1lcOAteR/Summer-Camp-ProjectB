"""F-02 red/green contract for the core SQLite schema and unit of work."""

from __future__ import annotations

import importlib.util
import sqlite3
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[3]


def load_module(relative: str):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_fresh_and_existing_database_migrations_are_idempotent(tmp_path: Path) -> None:
    db_module = load_module("backend/projectb/storage/db.py")
    database = db_module.Database(tmp_path / "projectb.sqlite3")

    database.initialize()
    first = database.connect()
    try:
        migration_rows = first.execute("SELECT migration_id FROM schema_migrations").fetchall()
        tables = {
            row[0]
            for row in first.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%'"
            )
        }
    finally:
        first.close()

    database.initialize()
    second = database.connect()
    try:
        assert [row[0] for row in migration_rows] == ["001_core"]
        assert {
            "course",
            "material",
            "material_version",
            "blob_object",
            "material_blob_ref",
            "source_locator",
            "knowledge_concept",
            "coverage_decision",
            "provider_profile",
            "consent_record",
            "audit_event",
            "schema_migrations",
        } <= tables
        assert [row[0] for row in second.execute("SELECT migration_id FROM schema_migrations")] == ["001_core"]
    finally:
        second.close()


def test_core_uniqueness_and_discriminated_locator_constraints(tmp_path: Path) -> None:
    db_module = load_module("backend/projectb/storage/db.py")
    database = db_module.Database(tmp_path / "projectb.sqlite3")
    database.initialize()
    connection = database.connect()
    try:
        connection.execute(
            "INSERT INTO course(course_id, name, timezone, created_at) VALUES (?, ?, ?, ?)",
            ("course-1", "Concurrency", "Asia/Shanghai", "2026-08-06T00:00:00Z"),
        )
        connection.execute(
            "INSERT INTO material(material_id, course_id, filename, media_type, content_hash, status, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            ("material-1", "course-1", "notes.txt", "text/plain", "a" * 64, "ready", "2026-08-06T00:00:00Z"),
        )
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute(
                "INSERT INTO material(material_id, course_id, filename, media_type, content_hash, status, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                ("material-duplicate", "course-1", "other.txt", "text/plain", "a" * 64, "ready", "2026-08-06T00:00:00Z"),
            )
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute(
                "INSERT INTO material(material_id, course_id, filename, media_type, content_hash, status, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                ("material-uppercase", "course-1", "upper.txt", "text/plain", "A" * 64, "ready", "2026-08-06T00:00:00Z"),
            )
        connection.execute(
            "INSERT INTO material_version(version_id, material_id, parser_id, parser_version, "
            "extraction_contract_version, extraction_status, locator_index_json, content_hash, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ("version-1", "material-1", "txt", "1", "1", "ready", "{}", "a" * 64, "2026-08-06T00:00:00Z"),
        )
        connection.execute(
            "INSERT INTO source_locator(locator_id, material_version_id, content_hash, locator_kind, "
            "page_start, page_end) VALUES (?, ?, ?, ?, ?, ?)",
            ("locator-page", "version-1", "a" * 64, "pdf_page", 1, 1),
        )
        connection.execute(
            "INSERT INTO source_locator(locator_id, material_version_id, content_hash, locator_kind, "
            "line_start, line_end) VALUES (?, ?, ?, ?, ?, ?)",
            ("locator-lines", "version-1", "a" * 64, "text_lines", 1, 4),
        )
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute(
                "INSERT INTO source_locator(locator_id, material_version_id, content_hash, locator_kind, "
                "page_start, line_start) VALUES (?, ?, ?, ?, ?, ?)",
                ("locator-invalid", "version-1", "a" * 64, "pdf_page", 1, 1),
            )
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute(
                "INSERT INTO source_locator(locator_id, material_version_id, content_hash, locator_kind, "
                "page_start, page_end) VALUES (?, ?, ?, ?, ?, ?)",
                ("locator-page-range", "version-1", "a" * 64, "pdf_page", 1, 2),
            )
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute(
                "INSERT INTO source_locator(locator_id, material_version_id, content_hash, locator_kind, "
                "page_start, page_end) VALUES (?, ?, ?, ?, ?, ?)",
                ("locator-wrong-hash", "version-1", "c" * 64, "pdf_page", 2, 2),
            )
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute(
                "UPDATE material SET content_hash = ? WHERE material_id = ?",
                ("b" * 64, "material-1"),
            )
    finally:
        connection.close()


def test_material_delete_preserves_shared_blob_and_removes_last_reference(tmp_path: Path) -> None:
    db_module = load_module("backend/projectb/storage/db.py")
    uow_module = load_module("backend/projectb/repositories/uow.py")
    database = db_module.Database(tmp_path / "projectb.sqlite3")
    database.initialize()
    with uow_module.UnitOfWork(database) as unit:
        unit.add_course("course-1", "Concurrency", "Asia/Shanghai", "2026-08-06T00:00:00Z")
        unit.add_course("course-2", "Locks", "Asia/Shanghai", "2026-08-06T00:00:00Z")
        unit.add_material("material-1", "course-1", "one.txt", "text/plain", "b" * 64, "ready", "2026-08-06T00:00:00Z")
        unit.add_material("material-2", "course-2", "two.txt", "text/plain", "b" * 64, "ready", "2026-08-06T00:00:00Z")
        unit.add_blob("b" * 64, "objects/b")
        unit.attach_blob("material-1", "b" * 64)
        unit.attach_blob("material-2", "b" * 64)
        unit.conn.execute(
            "INSERT INTO material_version(version_id, material_id, parser_id, parser_version, "
            "extraction_contract_version, extraction_status, locator_index_json, content_hash, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ("version-delete", "material-1", "txt", "1", "1", "ready", "{}", "b" * 64, "2026-08-06T00:00:00Z"),
        )

    with uow_module.UnitOfWork(database) as unit:
        unit.delete_material("material-1")
    connection = database.connect()
    try:
        shared = connection.execute(
            "SELECT delete_pending FROM blob_object WHERE content_hash = ?", ("b" * 64,)
        ).fetchone()
        assert shared is not None and shared[0] == 0
        assert connection.execute("SELECT 1 FROM material WHERE material_id = ?", ("material-1",)).fetchone() is None
        assert connection.execute("SELECT 1 FROM material_version WHERE version_id = ?", ("version-delete",)).fetchone() is None
    finally:
        connection.close()

    with uow_module.UnitOfWork(database) as unit:
        unit.delete_material("material-2")
    connection = database.connect()
    try:
        tombstone = connection.execute(
            "SELECT storage_ref, delete_pending FROM blob_object WHERE content_hash = ?", ("b" * 64,)
        ).fetchone()
        assert tombstone is not None and tuple(tombstone) == ("objects/b", 1)
    finally:
        connection.close()

    with uow_module.UnitOfWork(database) as unit:
        unit.add_material("material-3", "course-1", "three.txt", "text/plain", "b" * 64, "ready", "2026-08-06T00:00:00Z")
        unit.attach_blob("material-3", "b" * 64)
    connection = database.connect()
    try:
        assert connection.execute(
            "SELECT delete_pending FROM blob_object WHERE content_hash = ?", ("b" * 64,)
        ).fetchone()[0] == 0
    finally:
        connection.close()


def test_uow_commits_and_rolls_back_as_one_transaction(tmp_path: Path) -> None:
    db_module = load_module("backend/projectb/storage/db.py")
    uow_module = load_module("backend/projectb/repositories/uow.py")
    database = db_module.Database(tmp_path / "projectb.sqlite3")
    database.initialize()

    with pytest.raises(RuntimeError):
        with uow_module.UnitOfWork(database) as unit:
            unit.add_course("rollback", "No commit", "UTC", "2026-08-06T00:00:00Z")
            raise RuntimeError("force rollback")

    connection = database.connect()
    try:
        assert connection.execute("SELECT 1 FROM course WHERE course_id = ?", ("rollback",)).fetchone() is None
    finally:
        connection.close()

    with uow_module.UnitOfWork(database) as unit:
        unit.add_course("commit", "Committed", "UTC", "2026-08-06T00:00:00Z")
    connection = database.connect()
    try:
        assert connection.execute("SELECT name FROM course WHERE course_id = ?", ("commit",)).fetchone()[0] == "Committed"
    finally:
        connection.close()


def test_failed_migration_rolls_back_schema_and_ledger(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    db_module = load_module("backend/projectb/storage/db.py")
    migrations = tmp_path / "migrations"
    migrations.mkdir()
    (migrations / "999_broken.sql").write_text(
        "CREATE TABLE partial_table(value TEXT);\nINSERT INTO missing_table(value) VALUES ('x');\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(db_module, "MIGRATION_DIR", migrations)
    database = db_module.Database(tmp_path / "broken.sqlite3")

    with pytest.raises(sqlite3.OperationalError):
        database.initialize()

    connection = database.connect()
    try:
        assert connection.execute(
            "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'partial_table'"
        ).fetchone() is None
        assert connection.execute("SELECT migration_id FROM schema_migrations").fetchall() == []
    finally:
        connection.close()


def test_uow_closes_connection_when_begin_fails() -> None:
    uow_module = load_module("backend/projectb/repositories/uow.py")

    class FailingConnection:
        closed = False

        def execute(self, _: str) -> None:
            raise sqlite3.OperationalError("database busy")

        def close(self) -> None:
            self.closed = True

    connection = FailingConnection()

    class FakeDatabase:
        def connect(self) -> FailingConnection:
            return connection

    unit = uow_module.UnitOfWork(FakeDatabase())
    with pytest.raises(sqlite3.OperationalError):
        unit.__enter__()
    assert connection.closed
    assert unit.connection is None


def test_immutable_versions_consents_and_audit_events(tmp_path: Path) -> None:
    db_module = load_module("backend/projectb/storage/db.py")
    database = db_module.Database(tmp_path / "projectb.sqlite3")
    database.initialize()
    connection = database.connect()
    try:
        connection.execute(
            "INSERT INTO provider_profile(profile_id, adapter_id, model_id, budget_limit, credential_ref, "
            "config_fingerprint, policy_fingerprint, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            ("profile-1", "mock", "deterministic", 0, "ref-only", "cfg", "policy", "2026-08-06T00:00:00Z"),
        )
        connection.execute(
            "INSERT INTO audit_event(event_id, actor, action, result, opaque_refs_json, fingerprint, error_code, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            ("audit-1", "local", "create", "ok", "{}", "fp", None, "2026-08-06T00:00:00Z"),
        )
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute("UPDATE audit_event SET result = 'changed' WHERE event_id = 'audit-1'")
        connection.execute(
            "INSERT INTO course(course_id, name, timezone, created_at) VALUES (?, ?, ?, ?)",
            ("course-1", "Concurrency", "UTC", "2026-08-06T00:00:00Z"),
        )
        connection.execute(
            "INSERT INTO knowledge_concept(concept_id, course_id, name, evaluator_id, version, state, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            ("concept-1", "course-1", "mutex", "mutex-v1", 1, "active", "2026-08-06T00:00:00Z"),
        )
        connection.execute(
            "INSERT INTO coverage_decision(decision_id, concept_id, locator_ids_json, decision, version, confirmed_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            ("decision-1", "concept-1", "[]", "confirmed", 1, "2026-08-06T00:00:00Z"),
        )
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute("UPDATE coverage_decision SET decision = 'rejected' WHERE decision_id = 'decision-1'")
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute("DELETE FROM coverage_decision WHERE decision_id = 'decision-1'")

    finally:
        connection.close()
