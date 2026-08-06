from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import pytest
from pypdf import PdfWriter


ROOT = Path(__file__).resolve().parents[3]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from projectb.domain.materials.models import (  # noqa: E402
    ExtractedSource,
    ExtractionResult,
    MaterialVersion,
    ParserContract,
    PdfPageLocator,
    TextLinesLocator,
)
from projectb.services.materials.extract_text import ExtractionError, extract_material  # noqa: E402
from projectb.services.materials.importer import (  # noqa: E402
    MAX_BATCH_BYTES,
    MAX_BATCH_FILES,
    MAX_FILE_BYTES,
    MAX_PDF_PAGES,
    MAX_TEXT_CODEPOINTS,
    ImportPolicyError,
    MaterialImporter,
    preflight_batch,
)
from projectb.storage.content_store import ContentStore  # noqa: E402
from projectb.storage.db import Database  # noqa: E402


def make_importer(tmp_path: Path, *, extractor=extract_material) -> tuple[MaterialImporter, Database, ContentStore]:
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
    return MaterialImporter(database, store, extractor=extractor), database, store


def table_count(database: Database, table: str) -> int:
    connection = database.connect()
    try:
        return int(connection.execute(f"SELECT count(*) FROM {table}").fetchone()[0])
    finally:
        connection.close()


def write_sparse(path: Path, size: int) -> Path:
    with path.open("wb") as stream:
        stream.truncate(size)
    return path


def test_exact_policy_constants_and_batch_file_count_boundaries(tmp_path: Path) -> None:
    assert (MAX_BATCH_FILES, MAX_FILE_BYTES, MAX_BATCH_BYTES) == (5, 20 * 1024**2, 50 * 1024**2)
    assert (MAX_PDF_PAGES, MAX_TEXT_CODEPOINTS) == (200, 1_000_000)
    files = [write_sparse(tmp_path / f"{index}.txt", 1) for index in range(MAX_BATCH_FILES + 1)]

    preflight_batch(files[: MAX_BATCH_FILES - 1])
    preflight_batch(files[:MAX_BATCH_FILES])
    with pytest.raises(ImportPolicyError, match="batch_file_limit"):
        preflight_batch(files)


def test_file_and_batch_byte_limit_minus_exact_plus_one(tmp_path: Path) -> None:
    for delta in (-1, 0):
        preflight_batch([write_sparse(tmp_path / f"single-{delta}.txt", MAX_FILE_BYTES + delta)])
    with pytest.raises(ImportPolicyError, match="file_too_large"):
        preflight_batch([write_sparse(tmp_path / "single-plus.txt", MAX_FILE_BYTES + 1)])

    exact = [
        write_sparse(tmp_path / "total-a.txt", MAX_FILE_BYTES),
        write_sparse(tmp_path / "total-b.txt", MAX_FILE_BYTES),
        write_sparse(tmp_path / "total-c.txt", MAX_BATCH_BYTES - 2 * MAX_FILE_BYTES),
    ]
    preflight_batch(exact)
    exact[-1] = write_sparse(tmp_path / "total-plus.txt", exact[-1].stat().st_size + 1)
    with pytest.raises(ImportPolicyError, match="batch_byte_limit"):
        preflight_batch(exact)


def test_text_import_is_atomic_and_same_contract_is_idempotent(tmp_path: Path) -> None:
    importer, database, store = make_importer(tmp_path)
    source = tmp_path / "notes.txt"
    source.write_text("mutex\nrace\ndeadlock\n", encoding="utf-8")

    first = importer.import_batch("course-1", [source])[0]
    second = importer.import_batch("course-1", [source])[0]

    assert first.status == "imported"
    assert second.status == "idempotent"
    assert (first.material_id, first.version_id) == (second.material_id, second.version_id)
    assert table_count(database, "material") == 1
    assert table_count(database, "material_version") == 1
    assert table_count(database, "source_locator") == 3
    assert table_count(database, "blob_object") == 1
    assert store.path_for(first.content_hash).read_bytes() == source.read_bytes()


def upgraded_extractor(path: Path, *, material_id: str, deadline_seconds: float = 30) -> ExtractionResult:
    original = extract_material(path, material_id=material_id, deadline_seconds=deadline_seconds)
    contract = ParserContract(original.version.parser_id, original.version.parser_version + ".next", "1")
    version = MaterialVersion.create(
        material_id=material_id,
        content_hash=original.content_hash,
        contract=contract,
        source_kind=original.version.source_kind,
        source_count=original.version.source_count,
    )
    sources: list[ExtractedSource] = []
    for source in original.sources:
        if source.locator.kind == "pdf_page":
            locator = PdfPageLocator.create(version, source.locator.page)
        else:
            locator = TextLinesLocator.create(version, source.locator.line_start, source.locator.line_end)
        sources.append(ExtractedSource(locator, source.text))
    return ExtractionResult(original.content_hash, original.media_type, version, tuple(sources))


def test_same_hash_new_parser_adds_version_without_copying_blob(tmp_path: Path) -> None:
    importer, database, _ = make_importer(tmp_path)
    source = tmp_path / "notes.md"
    source.write_text("# Mutex\n\nOne lock.\n", encoding="utf-8")
    first = importer.import_batch("course-1", [source])[0]
    upgraded = MaterialImporter(importer.database, importer.store, extractor=upgraded_extractor)

    second = upgraded.import_batch("course-1", [source])[0]

    assert second.status == "imported"
    assert second.material_id == first.material_id
    assert second.version_id != first.version_id
    assert table_count(database, "material") == 1
    assert table_count(database, "material_version") == 2
    assert table_count(database, "blob_object") == 1


def test_two_courses_share_one_blob_with_independent_materials(tmp_path: Path) -> None:
    importer, database, _ = make_importer(tmp_path)
    source = tmp_path / "shared.txt"
    source.write_text("shared bytes\n", encoding="utf-8")

    first = importer.import_batch("course-1", [source])[0]
    second = importer.import_batch("course-2", [source])[0]

    assert first.material_id != second.material_id
    assert first.content_hash == second.content_hash
    assert table_count(database, "material") == 2
    assert table_count(database, "material_blob_ref") == 2
    assert table_count(database, "blob_object") == 1


def test_mixed_batch_preserves_successful_siblings_and_cleans_failure(tmp_path: Path) -> None:
    importer, database, store = make_importer(tmp_path)
    good_a = tmp_path / "a.txt"
    bad = tmp_path / "bad.txt"
    good_b = tmp_path / "b.md"
    good_a.write_text("mutex\n", encoding="utf-8")
    bad.write_bytes(b"invalid\xff")
    good_b.write_text("race\n", encoding="utf-8")

    results = importer.import_batch("course-1", [good_a, bad, good_b])

    assert [result.status for result in results] == ["imported", "failed", "imported"]
    assert results[1].error_code == "content_unreadable"
    assert table_count(database, "material") == 2
    assert table_count(database, "material_version") == 2
    assert not any(store.staging_dir.iterdir())


@pytest.mark.parametrize("count, succeeds", [(MAX_TEXT_CODEPOINTS - 1, True), (MAX_TEXT_CODEPOINTS, True), (MAX_TEXT_CODEPOINTS + 1, False)])
def test_text_codepoint_boundaries(tmp_path: Path, count: int, succeeds: bool) -> None:
    importer, database, _ = make_importer(tmp_path)
    source = tmp_path / f"text-{count}.txt"
    source.write_text("x" * count, encoding="utf-8")

    result = importer.import_batch("course-1", [source])[0]

    assert (result.status == "imported") is succeeds
    assert result.error_code == (None if succeeds else "text_too_large")
    assert table_count(database, "material") == int(succeeds)


@pytest.mark.parametrize("pages, succeeds", [(MAX_PDF_PAGES - 1, True), (MAX_PDF_PAGES, True), (MAX_PDF_PAGES + 1, False)])
def test_pdf_page_boundaries(tmp_path: Path, pages: int, succeeds: bool) -> None:
    def counted_pdf(_: Path, *, material_id: str, deadline_seconds: float = 30) -> ExtractionResult:
        content_hash = hashlib.sha256(_.read_bytes()).hexdigest()
        version = MaterialVersion.create(
            material_id=material_id,
            content_hash=content_hash,
            contract=ParserContract("test-pdf", "1", "1"),
            source_kind="pdf_page",
            source_count=pages,
        )
        sources = tuple(ExtractedSource(PdfPageLocator.create(version, page), "text") for page in range(1, pages + 1))
        return ExtractionResult(content_hash, "application/pdf", version, sources)

    importer, database, _ = make_importer(tmp_path, extractor=counted_pdf)
    source = tmp_path / f"pages-{pages}.pdf"
    writer = PdfWriter()
    writer.add_blank_page(width=20, height=20)
    with source.open("wb") as stream:
        writer.write(stream)

    result = importer.import_batch("course-1", [source])[0]

    assert (result.status == "imported") is succeeds
    assert result.error_code == (None if succeeds else "pdf_page_limit")
    assert table_count(database, "material") == int(succeeds)


def test_timeout_leaves_no_database_or_content_bytes(tmp_path: Path) -> None:
    def timeout_extractor(path: Path, *, material_id: str, deadline_seconds: float = 30) -> ExtractionResult:
        raise ExtractionError("parse_timeout", retryable=True)

    importer, database, store = make_importer(tmp_path, extractor=timeout_extractor)
    source = tmp_path / "timeout.txt"
    source.write_text("data", encoding="utf-8")

    result = importer.import_batch("course-1", [source])[0]

    assert (result.status, result.error_code, result.retryable) == ("failed", "parse_timeout", True)
    assert table_count(database, "material") == 0
    assert list(store.objects_dir.rglob("*")) == []
    assert not any(store.staging_dir.iterdir())


def test_source_change_during_extraction_fails_without_authoritative_write(tmp_path: Path) -> None:
    def changing_extractor(path: Path, *, material_id: str, deadline_seconds: float = 30) -> ExtractionResult:
        path.write_text("changed during extraction", encoding="utf-8")
        return extract_material(path, material_id=material_id, deadline_seconds=deadline_seconds)

    importer, database, store = make_importer(tmp_path, extractor=changing_extractor)
    source = tmp_path / "changing.txt"
    source.write_text("original", encoding="utf-8")

    result = importer.import_batch("course-1", [source])[0]

    assert (result.status, result.error_code, result.retryable) == ("failed", "content_changed", True)
    assert table_count(database, "material") == 0
    assert list(store.objects_dir.rglob("*")) == []
    assert not any(store.staging_dir.iterdir())
