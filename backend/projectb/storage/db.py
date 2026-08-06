"""SQLite connection and deterministic migration entry point for ProjectB."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any


MIGRATION_DIR = Path(__file__).with_name("migrations")


def migration_statements(script: str) -> list[str]:
    statements: list[str] = []
    buffer: list[str] = []
    for line in script.splitlines(keepends=True):
        buffer.append(line)
        candidate = "".join(buffer).strip()
        if candidate and sqlite3.complete_statement(candidate):
            statements.append(candidate)
            buffer.clear()
    if "".join(buffer).strip():
        raise ValueError("migration_incomplete_statement")
    return statements


class Database:
    """Own one SQLite file and apply migrations before repositories use it."""

    def __init__(self, path: str | Path) -> None:
        self.path = str(path)

    def connect(self) -> sqlite3.Connection:
        if self.path != ":memory:":
            Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.path, isolation_level=None, timeout=5)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def initialize(self) -> None:
        connection = self.connect()
        try:
            connection.execute(
                "CREATE TABLE IF NOT EXISTS schema_migrations ("
                "migration_id TEXT PRIMARY KEY, applied_at TEXT NOT NULL"
                ")"
            )
            for migration in sorted(MIGRATION_DIR.glob("*.sql")):
                migration_id = migration.stem
                connection.execute("BEGIN IMMEDIATE")
                try:
                    applied = connection.execute(
                        "SELECT 1 FROM schema_migrations WHERE migration_id = ?", (migration_id,)
                    ).fetchone()
                    if applied is None:
                        for statement in migration_statements(migration.read_text(encoding="utf-8")):
                            connection.execute(statement)
                        connection.execute(
                            "INSERT INTO schema_migrations(migration_id, applied_at) VALUES (?, strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))",
                            (migration_id,),
                        )
                    connection.commit()
                except BaseException:
                    connection.rollback()
                    raise
        finally:
            connection.close()

    def unit_of_work(self) -> Any:
        """Return a context manager without importing repositories at module load time."""
        from backend.projectb.repositories.uow import UnitOfWork

        return UnitOfWork(self)
