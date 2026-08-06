from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from projectb.storage.content_store import ContentStore


@dataclass(frozen=True, slots=True)
class DeletionResult:
    status: str
    retryable: bool = False


class MaterialDeletionService:
    def __init__(self, database: Any, store: ContentStore) -> None:
        self.database = database
        self.store = store

    def delete(self, material_id: str) -> DeletionResult:
        connection = self.database.connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            hashes = tuple(
                row[0]
                for row in connection.execute(
                    "SELECT content_hash FROM material_blob_ref WHERE material_id = ?", (material_id,)
                )
            )
            connection.execute("DELETE FROM material WHERE material_id = ?", (material_id,))
            for content_hash in hashes:
                connection.execute(
                    "UPDATE blob_object SET delete_pending = 1 WHERE content_hash = ? "
                    "AND NOT EXISTS (SELECT 1 FROM material_blob_ref WHERE content_hash = ?)",
                    (content_hash, content_hash),
                )
            connection.commit()
        except BaseException:
            connection.rollback()
            raise
        finally:
            connection.close()

        pending = False
        for content_hash in hashes:
            if self._is_pending(str(content_hash)):
                try:
                    self._remove_final_blob(str(content_hash))
                except Exception:
                    pending = True
        return DeletionResult("delete_pending" if pending else "deleted", retryable=pending)

    def retry_pending(self, content_hash: str) -> DeletionResult:
        if not self._is_pending(content_hash):
            return DeletionResult("deleted")
        try:
            self._remove_final_blob(content_hash)
        except Exception:
            return DeletionResult("delete_pending", retryable=True)
        return DeletionResult("deleted")

    def _is_pending(self, content_hash: str) -> bool:
        connection = self.database.connect()
        try:
            row = connection.execute(
                "SELECT delete_pending FROM blob_object WHERE content_hash = ?", (content_hash,)
            ).fetchone()
            return row is not None and int(row[0]) == 1
        finally:
            connection.close()

    def _remove_final_blob(self, content_hash: str) -> None:
        connection = self.database.connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            pending = connection.execute(
                "SELECT 1 FROM blob_object WHERE content_hash = ? AND delete_pending = 1 "
                "AND NOT EXISTS (SELECT 1 FROM material_blob_ref WHERE content_hash = ?)",
                (content_hash, content_hash),
            ).fetchone()
            if pending is None:
                connection.commit()
                return
            self.store.remove(content_hash)
            connection.execute(
                "DELETE FROM blob_object WHERE content_hash = ? AND delete_pending = 1 "
                "AND NOT EXISTS (SELECT 1 FROM material_blob_ref WHERE content_hash = ?)",
                (content_hash, content_hash),
            )
            connection.commit()
        except BaseException:
            connection.rollback()
            raise
        finally:
            connection.close()
