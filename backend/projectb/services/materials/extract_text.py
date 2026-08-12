from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Literal, Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from projectb.domain.materials.models import (  # noqa: E402
    ExtractedSource,
    ExtractionResult,
    MaterialVersion,
    ParserContract,
    PdfPageLocator,
    TextLinesLocator,
)


TEXT_CONTRACT = ParserContract("utf8-text", "1", "1")

def _pdf_contract() -> ParserContract:
    return ParserContract(
        "pypdf+pypdfium2",
        "+".join((importlib.metadata.version("pypdf"), importlib.metadata.version("pypdfium2"))),
        "1",
    )
_BINARY_SIGNATURES = (b"%PDF-", b"PK\x03\x04", b"GIF87a", b"GIF89a", b"\x89PNG\r\n\x1a\n", b"\xff\xd8\xff")


class ExtractionError(Exception):
    def __init__(self, code: str, *, retryable: bool = False) -> None:
        super().__init__(code)
        self.code = code
        self.retryable = retryable


def _terminate_process_tree(pid: int) -> None:
    import psutil

    try:
        parent = psutil.Process(pid)
    except psutil.NoSuchProcess:
        return
    processes = parent.children(recursive=True) + [parent]
    for process in processes:
        try:
            process.terminate()
        except psutil.NoSuchProcess:
            pass
    _, alive = psutil.wait_procs(processes, timeout=2)
    for process in alive:
        try:
            process.kill()
        except psutil.NoSuchProcess:
            pass
    psutil.wait_procs(alive, timeout=2)


def run_terminable_worker(
    command: Sequence[str],
    *,
    output_path: Path,
    deadline_seconds: float,
) -> None:
    if deadline_seconds <= 0:
        raise ValueError("deadline_seconds_must_be_positive")
    output_path.unlink(missing_ok=True)
    creationflags = int(getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)) if os.name == "nt" else 0
    process = subprocess.Popen(
        list(command),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=creationflags,
    )
    try:
        exit_code = process.wait(timeout=deadline_seconds)
    except subprocess.TimeoutExpired as error:
        _terminate_process_tree(process.pid)
        output_path.unlink(missing_ok=True)
        raise ExtractionError("parse_timeout", retryable=True) from error
    if exit_code != 0:
        output_path.unlink(missing_ok=True)
        raise ExtractionError("content_unreadable")


def _pdfium_page_count(path: Path) -> int:
    from pypdfium2 import PdfDocument  # type: ignore[import-untyped]

    document = PdfDocument(path)
    try:
        return len(document)
    finally:
        document.close()


def _pypdf_pages(path: Path) -> list[str]:
    from pypdf import PdfReader

    reader = PdfReader(path, strict=True)
    if reader.is_encrypted:
        raise ExtractionError("content_unreadable")
    return [page.extract_text() or "" for page in reader.pages]


def extract_pdf_bytes(data: bytes, source_name: str = "material.pdf") -> list[str]:
    if not data.startswith(b"%PDF-"):
        raise ExtractionError("unsupported_type")
    handle, raw_path = tempfile.mkstemp(prefix="projectb-pdf-", suffix=".pdf")
    path = Path(raw_path)
    try:
        with os.fdopen(handle, "wb") as stream:
            stream.write(data)
        try:
            validated_count = _pdfium_page_count(path)
            pages = _pypdf_pages(path)
        except ExtractionError:
            raise
        except Exception as error:
            raise ExtractionError("content_unreadable") from error
        if validated_count != len(pages) or validated_count < 1:
            raise ExtractionError("content_unreadable")
        if not any(page.strip() for page in pages):
            raise ExtractionError("unsupported_scanned_pdf")
        return pages
    finally:
        path.unlink(missing_ok=True)


def _extract_sync(path: Path) -> dict[str, Any]:
    try:
        raw = path.read_bytes()
    except OSError as error:
        raise ExtractionError("content_unreadable", retryable=True) from error
    content_hash = hashlib.sha256(raw).hexdigest()
    suffix = path.suffix.lower()
    if suffix in {".txt", ".md"}:
        if b"\0" in raw or raw.startswith(_BINARY_SIGNATURES):
            raise ExtractionError("unsupported_type")
        try:
            decoded = raw.decode("utf-8", errors="strict")
        except UnicodeDecodeError as error:
            raise ExtractionError("content_unreadable") from error
        normalized = decoded.replace("\r\n", "\n").replace("\r", "\n")
        lines = normalized.splitlines()
        if not any(line.strip() for line in lines):
            raise ExtractionError("content_unreadable")
        return {
            "content_hash": content_hash,
            "media_type": "text/markdown" if suffix == ".md" else "text/plain",
            "contract": list((TEXT_CONTRACT.parser_id, TEXT_CONTRACT.parser_version, TEXT_CONTRACT.extraction_contract_version)),
            "texts": lines,
        }
    if suffix == ".pdf":
        pages = extract_pdf_bytes(raw, path.name)
        contract = _pdf_contract()
        return {
            "content_hash": content_hash,
            "media_type": "application/pdf",
            "contract": list((contract.parser_id, contract.parser_version, contract.extraction_contract_version)),
            "texts": pages,
        }
    raise ExtractionError("unsupported_type")


def _write_worker_result(path: Path, output_path: Path) -> int:
    try:
        payload: dict[str, Any] = {"ok": True, "result": _extract_sync(path)}
    except ExtractionError as error:
        payload = {"ok": False, "error": {"code": error.code, "retryable": error.retryable}}
    try:
        output_path.write_text(json.dumps(payload, sort_keys=True), encoding="utf-8")
    except OSError:
        return 1
    return 0


def _decode_result(payload: dict[str, Any], material_id: str) -> ExtractionResult:
    if not payload.get("ok"):
        error = payload.get("error", {})
        raise ExtractionError(str(error.get("code", "content_unreadable")), retryable=bool(error.get("retryable")))
    raw = payload["result"]
    contract = ParserContract(*raw["contract"])
    source_kind: Literal["pdf_page", "text_lines"] = (
        "pdf_page" if raw["media_type"] == "application/pdf" else "text_lines"
    )
    version = MaterialVersion.create(
        material_id=material_id,
        content_hash=raw["content_hash"],
        contract=contract,
        source_kind=source_kind,
        source_count=len(raw["texts"]),
    )
    sources: list[ExtractedSource] = []
    for index, text in enumerate(raw["texts"], start=1):
        locator = (
            PdfPageLocator.create(version, index)
            if raw["media_type"] == "application/pdf"
            else TextLinesLocator.create(version, index, index)
        )
        sources.append(ExtractedSource(locator, text))
    return ExtractionResult(raw["content_hash"], raw["media_type"], version, tuple(sources))


def extract_material(
    path: Path,
    *,
    material_id: str,
    deadline_seconds: float = 30,
) -> ExtractionResult:
    source = Path(path)
    handle, output_name = tempfile.mkstemp(prefix="projectb-extraction-", suffix=".json")
    os.close(handle)
    output_path = Path(output_name)
    output_path.unlink(missing_ok=True)
    command = [sys.executable, str(Path(__file__).resolve()), "--worker", str(source), str(output_path)]
    try:
        run_terminable_worker(command, output_path=output_path, deadline_seconds=deadline_seconds)
        try:
            payload = json.loads(output_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ExtractionError("content_unreadable") from error
        return _decode_result(payload, material_id)
    finally:
        output_path.unlink(missing_ok=True)


def _main() -> int:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("path", type=Path)
    parser.add_argument("output", type=Path)
    arguments = parser.parse_args()
    if not arguments.worker:
        return 2
    return _write_worker_result(arguments.path, arguments.output)


if __name__ == "__main__":
    raise SystemExit(_main())
