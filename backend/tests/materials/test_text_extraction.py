from __future__ import annotations

import hashlib
import sys
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[3]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from projectb.domain.materials.models import (  # noqa: E402
    MaterialVersion,
    ParserContract,
    PdfPageLocator,
    TextLinesLocator,
)
from projectb.services.materials import extract_text  # noqa: E402
from projectb.services.materials.extract_text import ExtractionError, extract_material  # noqa: E402


FIXTURES = Path(__file__).parents[1] / "fixtures" / "materials"


def test_text_hashes_raw_bytes_and_normalizes_lines(tmp_path: Path) -> None:
    raw = b"mutex\r\nrace\rdeadlock\n"
    source = tmp_path / "notes.txt"
    source.write_bytes(raw)

    result = extract_material(source, material_id="material-text")

    assert result.content_hash == hashlib.sha256(raw).hexdigest()
    assert [part.text for part in result.sources] == ["mutex", "race", "deadlock"]
    assert [(part.locator.line_start, part.locator.line_end) for part in result.sources] == [
        (1, 1),
        (2, 2),
        (3, 3),
    ]
    assert all(part.locator.content_hash == result.content_hash for part in result.sources)
    assert all(part.locator.material_version_id == result.version.version_id for part in result.sources)


def test_frozen_extraction_dispatches_to_executable_worker(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    source = tmp_path / "notes.txt"
    source.write_text("mutex\n", encoding="utf-8")
    captured: list[str] = []
    captured_outputs: list[Path] = []

    monkeypatch.setattr(extract_text.sys, "frozen", True, raising=False)
    monkeypatch.setattr(extract_text.sys, "executable", "ProjectB.exe")

    def capture(command: list[str], *, output_path: Path, deadline_seconds: float) -> None:
        captured.extend(command)
        captured_outputs.append(output_path)
        output_path.write_text(
            '{"ok":true,"result":{"content_hash":"' + ("a" * 64)
            + '","media_type":"text/plain","contract":["utf8-text","1","1"],"texts":["mutex"]}}',
            encoding="utf-8",
        )

    monkeypatch.setattr(extract_text, "run_terminable_worker", capture)

    result = extract_material(source, material_id="material-frozen")

    assert captured[:3] == ["ProjectB.exe", "--material-worker", str(source)]
    assert Path(captured[3]) == captured_outputs[0]
    assert result.sources[0].text == "mutex"


@pytest.mark.parametrize("name", ["notes.txt", "notes.md"])
def test_committed_text_fixtures_extract_deterministically(name: str) -> None:
    first = extract_material(FIXTURES / name, material_id="material-notes")
    second = extract_material(FIXTURES / name, material_id="material-notes")

    assert first == second
    assert len(first.sources) == 3
    assert all(source.locator.kind == "text_lines" for source in first.sources)


def test_invalid_utf8_and_disguised_text_fail_closed(tmp_path: Path) -> None:
    invalid = tmp_path / "invalid.txt"
    invalid.write_bytes(b"valid\xffinvalid")
    disguised = tmp_path / "disguised.md"
    disguised.write_bytes(b"%PDF-1.7\nnot markdown")
    disguised_archive = tmp_path / "archive.txt"
    disguised_archive.write_bytes(b"PK\x03\x04not plain text")

    with pytest.raises(ExtractionError, match="content_unreadable") as invalid_error:
        extract_material(invalid, material_id="material-invalid")
    with pytest.raises(ExtractionError, match="unsupported_type") as disguised_error:
        extract_material(disguised, material_id="material-disguised")
    with pytest.raises(ExtractionError, match="unsupported_type"):
        extract_material(disguised_archive, material_id="material-archive")

    assert invalid_error.value.retryable is False
    assert disguised_error.value.retryable is False


def test_material_version_is_immutable_and_parser_upgrade_gets_new_identity() -> None:
    content_hash = "a" * 64
    old = MaterialVersion.create(
        material_id="material-1",
        content_hash=content_hash,
        contract=ParserContract("text", "1", "1"),
        source_kind="text_lines",
        source_count=2,
    )
    upgraded = MaterialVersion.create(
        material_id="material-1",
        content_hash=content_hash,
        contract=ParserContract("text", "2", "1"),
        source_kind="text_lines",
        source_count=2,
    )
    locator = TextLinesLocator.create(old, 1, 2)

    assert old.version_id != upgraded.version_id
    assert locator.material_version_id == old.version_id
    with pytest.raises(FrozenInstanceError):
        old.parser_version = "2"  # type: ignore[misc]


def test_locator_bounds_and_version_hash_are_validated() -> None:
    version = MaterialVersion.create(
        material_id="material-1",
        content_hash="b" * 64,
        contract=ParserContract("pdf", "1", "1"),
        source_kind="pdf_page",
        source_count=1,
    )
    text_version = MaterialVersion.create(
        material_id="material-2",
        content_hash="c" * 64,
        contract=ParserContract("text", "1", "1"),
        source_kind="text_lines",
        source_count=3,
    )

    assert PdfPageLocator.create(version, 1).page == 1
    assert TextLinesLocator.create(text_version, 1, 3).line_end == 3
    with pytest.raises(ValueError, match="page_out_of_bounds"):
        PdfPageLocator.create(version, 0)
    with pytest.raises(ValueError, match="page_out_of_bounds"):
        PdfPageLocator.create(version, 2)
    with pytest.raises(ValueError, match="locator_kind_mismatch"):
        TextLinesLocator.create(version, 1, 1)
    with pytest.raises(ValueError, match="line_range_out_of_bounds"):
        TextLinesLocator.create(text_version, 3, 2)
    with pytest.raises(ValueError, match="line_range_out_of_bounds"):
        TextLinesLocator.create(text_version, 1, 4)
    with pytest.raises(ValueError, match="content_hash"):
        MaterialVersion.create(
            material_id="material-1",
            content_hash="NOT-A-HASH",
            contract=ParserContract("text", "1", "1"),
            source_kind="text_lines",
            source_count=1,
        )
