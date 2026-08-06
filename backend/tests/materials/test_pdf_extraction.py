from __future__ import annotations

import hashlib
import importlib.metadata
import sys
import time
from pathlib import Path

import psutil
import pytest
from pypdf import PdfWriter


ROOT = Path(__file__).resolve().parents[3]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from projectb.services.materials.extract_text import (  # noqa: E402
    ExtractionError,
    extract_material,
    run_terminable_worker,
)


FIXTURES = Path(__file__).parents[1] / "fixtures" / "materials"


def test_digital_pdf_has_stable_page_sources_and_raw_hash() -> None:
    source = FIXTURES / "digital.pdf"
    first = extract_material(source, material_id="material-pdf")
    second = extract_material(source, material_id="material-pdf")

    assert first == second
    assert first.content_hash == hashlib.sha256(source.read_bytes()).hexdigest()
    assert [part.locator.page for part in first.sources] == [1, 2]
    assert first.version.parser_id == "pypdf+pypdfium2"
    assert first.version.parser_version == "+".join(
        (importlib.metadata.version("pypdf"), importlib.metadata.version("pypdfium2"))
    )
    assert "Mutex" in first.sources[0].text
    assert "Deadlock" in first.sources[1].text


def test_scanned_encrypted_and_disguised_pdfs_fail_before_result(tmp_path: Path) -> None:
    with pytest.raises(ExtractionError, match="unsupported_scanned_pdf"):
        extract_material(FIXTURES / "scanned.pdf", material_id="material-scan")

    encrypted = tmp_path / "encrypted.pdf"
    writer = PdfWriter()
    writer.add_blank_page(width=200, height=200)
    writer.encrypt("temporary-password")
    with encrypted.open("wb") as stream:
        writer.write(stream)
    with pytest.raises(ExtractionError, match="content_unreadable"):
        extract_material(encrypted, material_id="material-encrypted")

    disguised = tmp_path / "disguised.pdf"
    disguised.write_text("plain text", encoding="utf-8")
    with pytest.raises(ExtractionError, match="unsupported_type"):
        extract_material(disguised, material_id="material-disguised")


def test_pdf_validator_rejects_page_count_disagreement(monkeypatch: pytest.MonkeyPatch) -> None:
    from projectb.services.materials import extract_text

    monkeypatch.setattr(extract_text, "_pdfium_page_count", lambda _: 2)
    monkeypatch.setattr(extract_text, "_pypdf_pages", lambda _: ["only one"])

    with pytest.raises(ExtractionError, match="content_unreadable"):
        extract_text.extract_pdf_bytes(b"%PDF-1.7\n", "synthetic.pdf")


def test_timeout_terminates_process_tree_and_removes_partial_output(tmp_path: Path) -> None:
    output = tmp_path / "partial.json"
    child_pid = tmp_path / "child.pid"
    script = (
        "import pathlib,subprocess,sys,time;"
        "child=subprocess.Popen([sys.executable,'-c','import time;time.sleep(60)']);"
        "pathlib.Path(sys.argv[1]).write_text(str(child.pid),encoding='ascii');"
        "pathlib.Path(sys.argv[2]).write_text('partial',encoding='ascii');"
        "time.sleep(60)"
    )

    started = time.monotonic()
    with pytest.raises(ExtractionError, match="parse_timeout") as caught:
        run_terminable_worker(
            [sys.executable, "-c", script, str(child_pid), str(output)],
            output_path=output,
            deadline_seconds=0.5,
        )

    assert time.monotonic() - started < 10
    assert caught.value.retryable is True
    assert not output.exists()
    pid = int(child_pid.read_text(encoding="ascii"))
    for _ in range(40):
        if not psutil.pid_exists(pid):
            break
        try:
            if psutil.Process(pid).status() == psutil.STATUS_ZOMBIE:
                break
        except psutil.NoSuchProcess:
            break
        time.sleep(0.05)
    assert not psutil.pid_exists(pid) or psutil.Process(pid).status() == psutil.STATUS_ZOMBIE


def test_worker_error_is_stable_and_does_not_expose_stderr(tmp_path: Path) -> None:
    output = tmp_path / "result.json"
    marker = "sensitive-worker-detail"
    command = [sys.executable, "-c", f"import sys;sys.stderr.write('{marker}');sys.exit(9)"]

    with pytest.raises(ExtractionError, match="content_unreadable") as caught:
        run_terminable_worker(command, output_path=output, deadline_seconds=5)

    assert marker not in str(caught.value)
    assert not output.exists()
