from __future__ import annotations

import hashlib
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from projectb.domain.materials.models import ExtractionResult
from projectb.repositories.materials import MaterialsRepository
from projectb.services.materials.extract_text import ExtractionError, extract_material
from projectb.storage.content_store import ContentStore, ContentStoreError


MAX_BATCH_FILES = 5
MAX_FILE_BYTES = 20 * 1024**2
MAX_BATCH_BYTES = 50 * 1024**2
MAX_PDF_PAGES = 200
MAX_TEXT_CODEPOINTS = 1_000_000


class ImportPolicyError(RuntimeError):
    def __init__(self, code: str, *, retryable: bool = False) -> None:
        super().__init__(code)
        self.code = code
        self.retryable = retryable


@dataclass(frozen=True, slots=True)
class ImportOutcome:
    path: str
    status: str
    content_hash: str | None = None
    material_id: str | None = None
    version_id: str | None = None
    error_code: str | None = None
    retryable: bool = False


Extractor = Callable[..., ExtractionResult]


def preflight_batch(paths: Sequence[Path]) -> None:
    if len(paths) > MAX_BATCH_FILES:
        raise ImportPolicyError("batch_file_limit")
    total = 0
    for path in paths:
        try:
            size = Path(path).stat().st_size
        except OSError:
            raise ImportPolicyError("content_unreadable", retryable=True) from None
        if size > MAX_FILE_BYTES:
            raise ImportPolicyError("file_too_large")
        total += size
    if total > MAX_BATCH_BYTES:
        raise ImportPolicyError("batch_byte_limit")


class MaterialImporter:
    def __init__(self, database: object, store: ContentStore, *, extractor: Extractor = extract_material) -> None:
        self.database = database
        self.store = store
        self.extractor = extractor
        self.repository = MaterialsRepository(database)

    def import_batch(self, course_id: str, paths: Sequence[Path]) -> tuple[ImportOutcome, ...]:
        normalized = tuple(Path(path) for path in paths)
        preflight_batch(normalized)
        snapshots = tuple(self._content_snapshot(path) for path in normalized)
        if sum(size for _, size in snapshots) > MAX_BATCH_BYTES:
            raise ImportPolicyError("batch_byte_limit")
        return tuple(
            self._import_one(course_id, path, content_hash)
            for path, (content_hash, _) in zip(normalized, snapshots, strict=True)
        )

    def _import_one(self, course_id: str, path: Path, initial_hash: str) -> ImportOutcome:
        staged: Path | None = None
        promoted = False
        content_hash: str | None = None
        try:
            material_id = self._material_id(course_id, initial_hash)
            extraction = self.extractor(path, material_id=material_id, deadline_seconds=30)
            content_hash = extraction.content_hash
            if content_hash != initial_hash:
                raise ContentStoreError("content_hash_changed")
            self._validate_extraction(path, extraction)
            if self.repository.version_exists(course_id, content_hash, extraction.version.version_id) and self.store.exists(
                content_hash
            ):
                return ImportOutcome(
                    path.name, "idempotent", content_hash, material_id, extraction.version.version_id
                )
            staged = self.store.stage(path, content_hash)
            promoted = self.store.promote(staged, content_hash)
            if promoted:
                staged = None
            persisted = self.repository.persist(
                course_id=course_id,
                filename=path.name,
                material_id=material_id,
                extraction=extraction,
                storage_ref=self.store.storage_ref(content_hash),
                created_at=datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
            )
            if not self.store.exists(content_hash):
                if staged is None:
                    staged = self.store.stage(path, content_hash)
                restored = self.store.promote(staged, content_hash)
                promoted = promoted or restored
                if restored:
                    staged = None
                if not self.store.exists(content_hash):
                    raise ContentStoreError("content_restore_failed")
            return ImportOutcome(
                path.name,
                persisted.status,
                content_hash,
                persisted.material_id,
                persisted.version_id,
            )
        except (ExtractionError, ImportPolicyError) as error:
            return ImportOutcome(path.name, "failed", error_code=error.code, retryable=error.retryable)
        except ContentStoreError:
            return ImportOutcome(path.name, "failed", error_code="content_changed", retryable=True)
        except Exception:
            return ImportOutcome(path.name, "failed", error_code="import_failed", retryable=True)
        finally:
            self.store.discard(staged)
            if promoted and content_hash is not None and not self.repository.has_blob_reference(content_hash):
                self.store.remove(content_hash)

    @staticmethod
    def _material_id(course_id: str, content_hash: str) -> str:
        identity = hashlib.sha256(f"{course_id}:{content_hash}".encode()).hexdigest()
        return f"material-{identity}"

    @staticmethod
    def _content_snapshot(path: Path) -> tuple[str, int]:
        digest = hashlib.sha256()
        size = 0
        try:
            with path.open("rb") as stream:
                while chunk := stream.read(1024 * 1024):
                    size += len(chunk)
                    if size > MAX_FILE_BYTES:
                        raise ImportPolicyError("file_too_large")
                    digest.update(chunk)
        except OSError:
            raise ImportPolicyError("content_unreadable", retryable=True) from None
        return digest.hexdigest(), size

    @staticmethod
    def _validate_extraction(path: Path, extraction: ExtractionResult) -> None:
        if extraction.media_type == "application/pdf":
            if extraction.version.source_count > MAX_PDF_PAGES:
                raise ImportPolicyError("pdf_page_limit")
            return
        try:
            raw = path.read_bytes()
            decoded = raw.decode("utf-8", errors="strict")
        except (OSError, UnicodeDecodeError):
            raise ImportPolicyError("content_unreadable") from None
        normalized = decoded.replace("\r\n", "\n").replace("\r", "\n")
        if len(normalized) > MAX_TEXT_CODEPOINTS:
            raise ImportPolicyError("text_too_large")
