from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from projectb.domain.materials.models import ExtractionResult


@dataclass(frozen=True, slots=True)
class PersistResult:
    status: str
    material_id: str
    version_id: str


class MaterialsRepository:
    def __init__(self, database: Any) -> None:
        self.database = database

    def version_exists(self, course_id: str, content_hash: str, version_id: str) -> bool:
        connection = self.database.connect()
        try:
            row = connection.execute(
                "SELECT 1 FROM material_version mv JOIN material m ON m.material_id = mv.material_id "
                "WHERE m.course_id = ? AND m.content_hash = ? AND mv.version_id = ?",
                (course_id, content_hash, version_id),
            ).fetchone()
            return row is not None
        finally:
            connection.close()

    def has_blob_reference(self, content_hash: str) -> bool:
        connection = self.database.connect()
        try:
            return connection.execute(
                "SELECT 1 FROM material_blob_ref WHERE content_hash = ? LIMIT 1", (content_hash,)
            ).fetchone() is not None
        finally:
            connection.close()

    def persist(
        self,
        *,
        course_id: str,
        filename: str,
        material_id: str,
        extraction: ExtractionResult,
        storage_ref: str,
        created_at: str,
    ) -> PersistResult:
        connection = self.database.connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            existing = connection.execute(
                "SELECT material_id FROM material WHERE course_id = ? AND content_hash = ?",
                (course_id, extraction.content_hash),
            ).fetchone()
            if existing is None:
                connection.execute(
                    "INSERT INTO material(material_id, course_id, filename, media_type, content_hash, status, created_at) "
                    "VALUES (?, ?, ?, ?, ?, 'ready', ?)",
                    (material_id, course_id, filename, extraction.media_type, extraction.content_hash, created_at),
                )
            else:
                material_id = str(existing[0])

            connection.execute(
                "INSERT INTO blob_object(content_hash, storage_ref, delete_pending) VALUES (?, ?, 0) "
                "ON CONFLICT(content_hash) DO UPDATE SET delete_pending = 0",
                (extraction.content_hash, storage_ref),
            )
            connection.execute(
                "INSERT OR IGNORE INTO material_blob_ref(material_id, content_hash) VALUES (?, ?)",
                (material_id, extraction.content_hash),
            )

            if connection.execute(
                "SELECT 1 FROM material_version WHERE version_id = ?", (extraction.version.version_id,)
            ).fetchone() is not None:
                connection.commit()
                return PersistResult("idempotent", material_id, extraction.version.version_id)

            locator_index = [self._source_payload(source) for source in extraction.sources]
            connection.execute(
                "INSERT INTO material_version(version_id, material_id, parser_id, parser_version, "
                "extraction_contract_version, extraction_status, locator_index_json, content_hash, created_at) "
                "VALUES (?, ?, ?, ?, ?, 'ready', ?, ?, ?)",
                (
                    extraction.version.version_id,
                    material_id,
                    extraction.version.parser_id,
                    extraction.version.parser_version,
                    extraction.version.extraction_contract_version,
                    json.dumps(locator_index, ensure_ascii=False, separators=(",", ":"), sort_keys=True),
                    extraction.content_hash,
                    created_at,
                ),
            )
            for source in extraction.sources:
                locator = source.locator
                if locator.kind == "pdf_page":
                    connection.execute(
                        "INSERT INTO source_locator(locator_id, material_version_id, content_hash, locator_kind, "
                        "page_start, page_end) VALUES (?, ?, ?, 'pdf_page', ?, ?)",
                        (locator.locator_id, locator.material_version_id, locator.content_hash, locator.page, locator.page),
                    )
                else:
                    connection.execute(
                        "INSERT INTO source_locator(locator_id, material_version_id, content_hash, locator_kind, "
                        "line_start, line_end) VALUES (?, ?, ?, 'text_lines', ?, ?)",
                        (
                            locator.locator_id,
                            locator.material_version_id,
                            locator.content_hash,
                            locator.line_start,
                            locator.line_end,
                        ),
                    )
            connection.commit()
            return PersistResult("imported", material_id, extraction.version.version_id)
        except BaseException:
            connection.rollback()
            raise
        finally:
            connection.close()

    @staticmethod
    def _source_payload(source: Any) -> dict[str, object]:
        locator = source.locator
        payload: dict[str, object] = {
            "content_hash": locator.content_hash,
            "kind": locator.kind,
            "locator_id": locator.locator_id,
            "material_version_id": locator.material_version_id,
            "text": source.text,
        }
        if locator.kind == "pdf_page":
            payload["page"] = locator.page
        else:
            payload["line_start"] = locator.line_start
            payload["line_end"] = locator.line_end
        return payload
