from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from collections.abc import Mapping
from typing import Literal, TypeAlias


_SHA256 = re.compile(r"^[0-9a-f]{64}$")


def _require_text(value: str, field: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field}_required")


def _require_hash(value: str) -> None:
    if not _SHA256.fullmatch(value):
        raise ValueError("content_hash_invalid")


def _stable_id(prefix: str, payload: Mapping[str, object]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return f"{prefix}-{hashlib.sha256(encoded).hexdigest()}"


@dataclass(frozen=True, slots=True)
class ParserContract:
    parser_id: str
    parser_version: str
    extraction_contract_version: str

    def __post_init__(self) -> None:
        _require_text(self.parser_id, "parser_id")
        _require_text(self.parser_version, "parser_version")
        _require_text(self.extraction_contract_version, "extraction_contract_version")


@dataclass(frozen=True, slots=True)
class MaterialVersion:
    version_id: str
    material_id: str
    content_hash: str
    parser_id: str
    parser_version: str
    extraction_contract_version: str
    source_kind: Literal["pdf_page", "text_lines"]
    source_count: int

    def __post_init__(self) -> None:
        _require_text(self.version_id, "version_id")
        _require_text(self.material_id, "material_id")
        _require_hash(self.content_hash)
        ParserContract(self.parser_id, self.parser_version, self.extraction_contract_version)
        if self.source_kind not in {"pdf_page", "text_lines"}:
            raise ValueError("source_kind_invalid")
        if self.source_count < 1:
            raise ValueError("source_count_invalid")

    @classmethod
    def create(
        cls,
        *,
        material_id: str,
        content_hash: str,
        contract: ParserContract,
        source_kind: Literal["pdf_page", "text_lines"],
        source_count: int,
    ) -> MaterialVersion:
        _require_text(material_id, "material_id")
        _require_hash(content_hash)
        identity = {
            "content_hash": content_hash,
            "extraction_contract_version": contract.extraction_contract_version,
            "material_id": material_id,
            "parser_id": contract.parser_id,
            "parser_version": contract.parser_version,
        }
        return cls(
            version_id=_stable_id("version", identity),
            material_id=material_id,
            content_hash=content_hash,
            parser_id=contract.parser_id,
            parser_version=contract.parser_version,
            extraction_contract_version=contract.extraction_contract_version,
            source_kind=source_kind,
            source_count=source_count,
        )


@dataclass(frozen=True, slots=True)
class PdfPageLocator:
    locator_id: str
    material_id: str
    material_version_id: str
    content_hash: str
    page: int
    kind: Literal["pdf_page"] = "pdf_page"

    @classmethod
    def create(cls, version: MaterialVersion, page: int) -> PdfPageLocator:
        if version.source_kind != "pdf_page":
            raise ValueError("locator_kind_mismatch")
        if page < 1 or page > version.source_count:
            raise ValueError("page_out_of_bounds")
        identity = {
            "content_hash": version.content_hash,
            "kind": "pdf_page",
            "material_id": version.material_id,
            "material_version_id": version.version_id,
            "page": page,
        }
        return cls(
            _stable_id("locator", identity),
            version.material_id,
            version.version_id,
            version.content_hash,
            page,
        )


@dataclass(frozen=True, slots=True)
class TextLinesLocator:
    locator_id: str
    material_id: str
    material_version_id: str
    content_hash: str
    line_start: int
    line_end: int
    kind: Literal["text_lines"] = "text_lines"

    @classmethod
    def create(cls, version: MaterialVersion, line_start: int, line_end: int) -> TextLinesLocator:
        if version.source_kind != "text_lines":
            raise ValueError("locator_kind_mismatch")
        if line_start < 1 or line_end < line_start or line_end > version.source_count:
            raise ValueError("line_range_out_of_bounds")
        identity = {
            "content_hash": version.content_hash,
            "kind": "text_lines",
            "line_end": line_end,
            "line_start": line_start,
            "material_id": version.material_id,
            "material_version_id": version.version_id,
        }
        return cls(
            _stable_id("locator", identity),
            version.material_id,
            version.version_id,
            version.content_hash,
            line_start,
            line_end,
        )


SourceLocator: TypeAlias = PdfPageLocator | TextLinesLocator


@dataclass(frozen=True, slots=True)
class ExtractedSource:
    locator: SourceLocator
    text: str


@dataclass(frozen=True, slots=True)
class ExtractionResult:
    content_hash: str
    media_type: str
    version: MaterialVersion
    sources: tuple[ExtractedSource, ...]

    def __post_init__(self) -> None:
        _require_hash(self.content_hash)
        _require_text(self.media_type, "media_type")
        if self.version.content_hash != self.content_hash:
            raise ValueError("material_version_hash_mismatch")
        for source in self.sources:
            if source.locator.material_version_id != self.version.version_id:
                raise ValueError("locator_version_mismatch")
            if source.locator.content_hash != self.content_hash:
                raise ValueError("locator_hash_mismatch")
