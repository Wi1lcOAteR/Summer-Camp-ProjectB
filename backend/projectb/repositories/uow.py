"""Small explicit transaction boundary for core repositories."""

from __future__ import annotations

import sqlite3
from typing import Any


class UnitOfWork:
    def __init__(self, database: Any) -> None:
        self.database = database
        self.connection: sqlite3.Connection | None = None

    def __enter__(self) -> "UnitOfWork":
        connection = self.database.connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
        except BaseException:
            connection.close()
            raise
        self.connection = connection
        return self

    def __exit__(self, exception_type: object, exception: object, traceback: object) -> None:
        assert self.connection is not None
        try:
            if exception_type is None:
                self.connection.commit()
            else:
                self.connection.rollback()
        finally:
            self.connection.close()
            self.connection = None

    @property
    def conn(self) -> sqlite3.Connection:
        if self.connection is None:
            raise RuntimeError("unit_of_work_not_started")
        return self.connection

    def add_course(self, course_id: str, name: str, timezone: str, created_at: str) -> None:
        self.conn.execute(
            "INSERT INTO course(course_id, name, timezone, created_at) VALUES (?, ?, ?, ?)",
            (course_id, name, timezone, created_at),
        )

    def add_material(
        self,
        material_id: str,
        course_id: str,
        filename: str,
        media_type: str,
        content_hash: str,
        status: str,
        created_at: str,
    ) -> None:
        self.conn.execute(
            "INSERT INTO material(material_id, course_id, filename, media_type, content_hash, status, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (material_id, course_id, filename, media_type, content_hash, status, created_at),
        )

    def add_blob(self, content_hash: str, storage_ref: str) -> None:
        self.conn.execute(
            "INSERT INTO blob_object(content_hash, storage_ref) VALUES (?, ?)",
            (content_hash, storage_ref),
        )

    def attach_blob(self, material_id: str, content_hash: str) -> None:
        self.conn.execute(
            "INSERT INTO material_blob_ref(material_id, content_hash) VALUES (?, ?)",
            (material_id, content_hash),
        )
        self.conn.execute(
            "UPDATE blob_object SET delete_pending = 0 WHERE content_hash = ?",
            (content_hash,),
        )

    def delete_material(self, material_id: str) -> None:
        hashes = [
            row[0]
            for row in self.conn.execute(
                "SELECT content_hash FROM material_blob_ref WHERE material_id = ?", (material_id,)
            )
        ]
        self.conn.execute("DELETE FROM material WHERE material_id = ?", (material_id,))
        for content_hash in hashes:
            self.conn.execute(
                "UPDATE blob_object SET delete_pending = 1 WHERE content_hash = ? "
                "AND NOT EXISTS (SELECT 1 FROM material_blob_ref WHERE content_hash = ?)",
                (content_hash, content_hash),
            )
