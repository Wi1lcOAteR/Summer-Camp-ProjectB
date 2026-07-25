# T-02 Immutable Material Primitives and SourceLocator Proof Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Provide one immutable, provider-independent source contract that accepts only version-matched local locators and proves a remote text chunk belongs to one PDF page.

**Architecture:** Keep opaque IDs and M1 selection primitives in focused domain modules. Implement source errors, raw-byte hashing, locator models/catalog validation, and unique-page proof as separate modules behind the `projectb.domain.source` facade; no parser, database, provider, network, or UI code belongs in this task.

**Tech Stack:** CPython 3.14.6 standard library (`dataclasses`, `enum`, `hashlib`, `math`, `re`, `unicodedata`) with pytest 9.1.1, Ruff 0.15.22, and mypy 2.3.0 from T-01's locked backend environment.

---

### Task T-02: Define Immutable Material Primitives and SourceLocator Proof

> **Status: DRAFT / UNREVIEWED / NOT DISPATCHABLE.** This fragment specifies a focused `domain/source/` package and `prove_unique_pdf_page(chunk, pages, material_id, content_hash)`. The current formal `PLAN.md` instead owns a flat `domain/source.py`, a single locator test plus JSON fixture, and a proof signature without `material_id`. Those are incompatible dispatch contracts. A T-02 worker must stop if the root plan still contains either old contract; the worker has no authority to choose, merge, or reinterpret them.

**Coordinator prerequisite: atomic root-plan synchronization before dispatch.** If the coordinator adopts this fragment, one reviewed `PLAN.md` change must update all of the following together. A partial update keeps T-02 blocked:

1. Replace the T-02 `Files` block currently naming `domain/source.py`, `domain/errors.py`, `tests/unit/test_source_locator.py`, and `tests/fixtures/source_pages.json` with the exact 13 paths in this fragment's `Files` block.
2. Replace the domain ownership-map entry that names `source.py` with explicit ownership of `domain/source/__init__.py`, `errors.py`, `hashing.py`, `models.py`, and `proof.py`; retain exclusive T-02 ownership of `domain/types.py` and `domain/materials.py`.
3. Replace the three-argument proof declaration and every root-plan example/call with `prove_unique_pdf_page(chunk: str, pages: Sequence[PageText], material_id: MaterialId, content_hash: str) -> PdfPageLocator | SourceInsufficient`.
4. Replace the root-plan `Literal` enum shorthand with the exact `ProcessingMode`, `MaterialRole`, `MaterialReviewState`, and `MaterialUnitKind` `StrEnum` contracts below, including fixed `material-limits.v1` loading semantics.
5. Replace the old T-02 red/green snippets, fixture assumption, validation commands, expected test counts, review scope, staging list, and literal sample commit identity with this fragment's complete steps and commands.
6. Change T-02's concurrency wording from “no parallel edits to source.py” to exclusive ownership of every path listed here, and update every downstream import or function call that assumes the flat module or three-argument proof.
7. Update the T-02 ledger discovery hash to this fragment's post-review SHA-256. Keep the row `draft/unreviewed` until both independent reviewer records exist; a fragment hash alone is never PASS.
8. Remove T-02 from the G-03 eligible cold-start set while this prerequisite is incomplete, or complete this entire atomic synchronization and fresh plan review before presenting T-02 to a cold-start agent.

After that root-plan change, a fresh plan reviewer must verify the file list, ownership map, interface declarations, examples, commands, ledger hash/status, G-03 eligibility, and downstream imports as one consistent contract. Only then may the coordinator remove `NOT DISPATCHABLE` from the integrated plan. This fragment itself does not edit or authorize edits to `PLAN.md`.

**Files:**
- Create: `backend/src/projectb/domain/__init__.py`
- Create: `backend/src/projectb/domain/types.py`
- Create: `backend/src/projectb/domain/materials.py`
- Create: `backend/src/projectb/domain/source/__init__.py`
- Create: `backend/src/projectb/domain/source/errors.py`
- Create: `backend/src/projectb/domain/source/hashing.py`
- Create: `backend/src/projectb/domain/source/models.py`
- Create: `backend/src/projectb/domain/source/proof.py`
- Create: `backend/tests/unit/domain/test_domain_primitives.py`
- Create: `backend/tests/unit/domain/test_source_hashing.py`
- Create: `backend/tests/unit/domain/test_source_models.py`
- Create: `backend/tests/unit/domain/test_source_proof.py`
- Create: `backend/tests/unit/domain/test_source_exports.py`

**Dependencies / parallelism:** T-01 must be merged first. T-02 exclusively owns every file listed above while in progress; no M1/M2/M3/X2 task may edit them concurrently. Downstream tasks may start only from the reviewed T-02 commit and must consume the facade rather than duplicate hash, coordinate, normalization, or proof rules.

**Produced interfaces:**
- `raw_file_content_hash(raw_bytes: bytes) -> str` hashes the untouched input bytes and returns exactly 64 lowercase hexadecimal SHA-256 characters without a prefix.
- `normalize_source_text(value: str) -> str` applies Unicode NFKC, CRLF-to-LF conversion, soft-hyphen removal, whitespace collapse, and trim.
- `SourceLocator` is the exact four-branch union `PdfPageLocator | ImageLocator | TextLinesLocator | ManualEntryLocator`.
- PDF pages and text lines are 1-based. `Region` uses stored canonical orientation, a top-left origin, finite normalized values, and the SPEC bounds.
- `validate_source_locator(locator, catalog) -> None` rejects missing sources, stale hashes/versions, and out-of-range page/image/line references with stable non-sensitive codes.
- `prove_unique_pdf_page(chunk, pages, material_id, content_hash) -> PdfPageLocator | SourceInsufficient` succeeds only when at least 32 normalized code points occur as one continuous substring on exactly one page of that content hash.

- [ ] **Step 1: Write the failing raw-hash and normalization tests**

Create `backend/tests/unit/domain/test_source_hashing.py` with exactly:

```python
import pytest

from projectb.domain.source.errors import SourceContractError, SourceErrorCode
from projectb.domain.source.hashing import (
    normalize_source_text,
    raw_file_content_hash,
    validate_content_hash,
)


def test_raw_file_content_hash_matches_sha256_known_vector() -> None:
    assert raw_file_content_hash(b"abc") == (
        "ba7816bf8f01cfea414140de5dae2223"
        "b00361a396177a9cb410ff61f20015ad"
    )


def test_raw_file_content_hash_does_not_normalize_bytes() -> None:
    assert raw_file_content_hash(b"a\r\nb") != raw_file_content_hash(b"a\nb")


def test_source_text_normalization_uses_the_v1_pipeline() -> None:
    assert normalize_source_text("  Ａ\r\nB\u00ad\t C  ") == "A B C"


def test_validate_content_hash_accepts_exact_lowercase_hex() -> None:
    value = "0123456789abcdef" * 4
    assert validate_content_hash(value) == value


@pytest.mark.parametrize(
    "value",
    [
        "a" * 63,
        "a" * 65,
        "A" * 64,
        "sha256:" + ("a" * 64),
    ],
)
def test_validate_content_hash_rejects_noncanonical_values(value: str) -> None:
    with pytest.raises(SourceContractError) as caught:
        validate_content_hash(value)
    assert caught.value.code is SourceErrorCode.INVALID_CONTENT_HASH
```

- [ ] **Step 2: Run the hashing tests and capture the expected red result**

Run:

```powershell
$env:PYTHONPATH = (Resolve-Path 'backend/src').Path
python -m pytest backend/tests/unit/domain/test_source_hashing.py -q
```

Expected: exit code 2 with collection error `ModuleNotFoundError: No module named 'projectb.domain'`; no test passes.

- [ ] **Step 3: Create the domain package marker**

Create `backend/src/projectb/domain/__init__.py` with exactly:

```python
"""Provider-independent ProjectB domain contracts."""
```

- [ ] **Step 4: Create the initial source package marker**

Create `backend/src/projectb/domain/source/__init__.py` with exactly:

```python
"""Validated local source contracts."""
```

- [ ] **Step 5: Implement stable source error values**

Create `backend/src/projectb/domain/source/errors.py` with exactly:

```python
from dataclasses import dataclass
from enum import StrEnum


class SourceErrorCode(StrEnum):
    INVALID_CONTENT_HASH = "invalid_content_hash"
    INVALID_MATERIAL_LIMITS = "invalid_material_limits"
    INVALID_ID = "invalid_id"
    INVALID_PAGE = "invalid_page"
    INVALID_LINE_RANGE = "invalid_line_range"
    INVALID_REGION = "invalid_region"
    INVALID_KIND = "invalid_kind"
    INVALID_SHAPE = "invalid_shape"
    INVALID_CATALOG = "invalid_catalog"
    MATERIAL_NOT_FOUND = "material_not_found"
    STALE_CONTENT_HASH = "stale_content_hash"
    PAGE_OUT_OF_RANGE = "page_out_of_range"
    IMAGE_NOT_FOUND = "image_not_found"
    LINE_OUT_OF_RANGE = "line_out_of_range"
    ENTRY_NOT_FOUND = "entry_not_found"
    STALE_ENTRY_VERSION = "stale_entry_version"


class SourceContractError(ValueError):
    def __init__(self, code: SourceErrorCode) -> None:
        self.code = code
        super().__init__(code.value)


class SourceInsufficientReason(StrEnum):
    TOO_SHORT = "too_short"
    NO_MATCH = "no_match"
    AMBIGUOUS = "ambiguous"


@dataclass(frozen=True, slots=True)
class SourceInsufficient:
    reason: SourceInsufficientReason
```

- [ ] **Step 6: Implement raw-byte hashing and text normalization**

Create `backend/src/projectb/domain/source/hashing.py` with exactly:

```python
import hashlib
import re
import unicodedata

from projectb.domain.source.errors import SourceContractError, SourceErrorCode


_CONTENT_HASH = re.compile(r"[0-9a-f]{64}\Z")


def raw_file_content_hash(raw_bytes: bytes) -> str:
    if not isinstance(raw_bytes, bytes):
        raise TypeError("raw_bytes must be bytes")
    return hashlib.sha256(raw_bytes).hexdigest()


def validate_content_hash(value: str) -> str:
    if not isinstance(value, str) or _CONTENT_HASH.fullmatch(value) is None:
        raise SourceContractError(SourceErrorCode.INVALID_CONTENT_HASH)
    return value


def normalize_source_text(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError("value must be str")
    normalized = unicodedata.normalize("NFKC", value)
    normalized = normalized.replace("\r\n", "\n").replace("\u00ad", "")
    return " ".join(normalized.split())
```

- [ ] **Step 7: Run the hashing tests and capture the green result**

Run:

```powershell
$env:PYTHONPATH = (Resolve-Path 'backend/src').Path
python -m pytest backend/tests/unit/domain/test_source_hashing.py -q
```

Expected: exit code 0 with `8 passed`.

- [ ] **Step 7B: Format the hashing slice under green tests**

Run:

```powershell
python -m ruff format --config backend/pyproject.toml backend/src/projectb/domain/source/errors.py backend/src/projectb/domain/source/hashing.py backend/tests/unit/domain/test_source_hashing.py
```

Expected: exit code 0; Ruff reports the three files formatted or already formatted and changes no behavior.

- [ ] **Step 7C: Re-run hashing tests after the refactor step**

Run:

```powershell
$env:PYTHONPATH = (Resolve-Path 'backend/src').Path
python -m pytest backend/tests/unit/domain/test_source_hashing.py -q
```

Expected: exit code 0 with `8 passed`.

- [ ] **Step 8A: Create the material enum and fixed-limits tests**

Create `backend/tests/unit/domain/test_domain_primitives.py` with this exact first slice:

```python
from dataclasses import FrozenInstanceError

import pytest

from projectb.domain.materials import (
    MATERIAL_LIMITS_VERSION,
    MaterialLimits,
    MaterialReviewState,
    MaterialRole,
    MaterialUnit,
    MaterialUnitKind,
    ProcessingMode,
    SelectedFile,
    material_limits_from_mapping,
)
from projectb.domain.source.errors import SourceContractError, SourceErrorCode
from projectb.domain.types import MaterialId, UnitId


HASH = "a" * 64


def test_material_enums_match_the_confirmed_v1_contract() -> None:
    assert [item.value for item in ProcessingMode] == ["L", "P", "F"]
    assert [item.value for item in MaterialRole] == [
        "lecture",
        "past_paper",
        "teacher_focus",
    ]
    assert [item.value for item in MaterialReviewState] == [
        "accepted",
        "needs_user_review",
    ]
    assert [item.value for item in MaterialUnitKind] == [
        "pdf_page",
        "image",
        "text_lines",
        "manual_entry",
    ]


def test_material_limits_match_spec_section_m1() -> None:
    limits = MaterialLimits()
    assert limits.version == MATERIAL_LIMITS_VERSION == "material-limits.v1"
    assert limits.pdf_max_bytes == 256 * 1024 * 1024
    assert limits.pdf_max_pages == 2_000
    assert limits.image_max_bytes == 20 * 1024 * 1024
    assert limits.image_max_pixels == 50_000_000
    assert limits.text_max_bytes == 2 * 1024 * 1024
    assert limits.manual_min_code_points == 1
    assert limits.manual_max_code_points == 10_000
    assert limits.batch_max_files == 50
    assert limits.batch_max_bytes == 1024 * 1024 * 1024
    assert limits.batch_max_pdf_pages == 5_000


def test_material_limits_reject_a_wrong_contract_version() -> None:
    with pytest.raises(SourceContractError) as caught:
        material_limits_from_mapping({"version": "material-limits.v2"})
    assert caught.value.code is SourceErrorCode.INVALID_MATERIAL_LIMITS


def test_material_limits_require_the_contract_version() -> None:
    with pytest.raises(SourceContractError) as caught:
        material_limits_from_mapping({})
    assert caught.value.code is SourceErrorCode.INVALID_MATERIAL_LIMITS


@pytest.mark.parametrize(
    "value",
    [True, 0, -1, 256 * 1024 * 1024, (256 * 1024 * 1024) + 1],
)
def test_material_limits_reject_every_runtime_v1_override(value: object) -> None:
    with pytest.raises(SourceContractError) as caught:
        material_limits_from_mapping(
            {
                "version": "material-limits.v1",
                "pdf_max_bytes": value,
            }
        )
    assert caught.value.code is SourceErrorCode.INVALID_MATERIAL_LIMITS
```

- [ ] **Step 8B: Append the immutable selected-file tests**

Append exactly:

```python


def test_selected_file_is_immutable_and_contains_no_local_path() -> None:
    selected = SelectedFile(
        material_id=MaterialId("material-1"),
        display_name="lecture.pdf",
        role=MaterialRole.LECTURE,
        content_hash=HASH,
        size_bytes=128,
        review_state=MaterialReviewState.ACCEPTED,
    )
    assert not hasattr(selected, "path")
    with pytest.raises(FrozenInstanceError):
        selected.size_bytes = 256  # type: ignore[misc]


@pytest.mark.parametrize(
    ("field", "value", "code"),
    [
        ("material_id", MaterialId(""), SourceErrorCode.INVALID_ID),
        ("display_name", "", SourceErrorCode.INVALID_SHAPE),
        ("content_hash", "A" * 64, SourceErrorCode.INVALID_CONTENT_HASH),
        ("size_bytes", -1, SourceErrorCode.INVALID_SHAPE),
        ("role", "lecture", SourceErrorCode.INVALID_SHAPE),
        ("role", MaterialUnitKind.PDF_PAGE, SourceErrorCode.INVALID_SHAPE),
        ("review_state", "accepted", SourceErrorCode.INVALID_SHAPE),
        ("review_state", MaterialRole.LECTURE, SourceErrorCode.INVALID_SHAPE),
    ],
)
def test_selected_file_rejects_invalid_values(
    field: str,
    value: object,
    code: SourceErrorCode,
) -> None:
    values: dict[str, object] = {
        "material_id": MaterialId("material-1"),
        "display_name": "lecture.pdf",
        "role": MaterialRole.LECTURE,
        "content_hash": HASH,
        "size_bytes": 128,
        "review_state": MaterialReviewState.ACCEPTED,
    }
    values[field] = value
    with pytest.raises(SourceContractError) as caught:
        SelectedFile(**values)
    assert caught.value.code is code
```

- [ ] **Step 8C: Append the material-unit boundary tests**

Append exactly:

```python


def test_material_unit_uses_a_one_based_ordinal() -> None:
    unit = MaterialUnit(
        unit_id=UnitId("unit-1"),
        material_id=MaterialId("material-1"),
        content_hash=HASH,
        kind=MaterialUnitKind.PDF_PAGE,
        ordinal=1,
        parser_version="parser-v1",
        quality_flags=frozenset({"text_present"}),
    )
    assert unit.ordinal == 1
    with pytest.raises(SourceContractError) as caught:
        MaterialUnit(
            unit_id=UnitId("unit-0"),
            material_id=MaterialId("material-1"),
            content_hash=HASH,
            kind=MaterialUnitKind.PDF_PAGE,
            ordinal=0,
            parser_version="parser-v1",
        )
    assert caught.value.code is SourceErrorCode.INVALID_PAGE


@pytest.mark.parametrize(
    ("kind", "quality_flags"),
    [
        ("pdf_page", frozenset({"text_present"})),
        (MaterialRole.LECTURE, frozenset({"text_present"})),
        (MaterialUnitKind.PDF_PAGE, "text_present"),
        (MaterialUnitKind.PDF_PAGE, frozenset({1})),
    ],
)
def test_material_unit_rejects_raw_kind_or_string_quality_flags(
    kind: object,
    quality_flags: object,
) -> None:
    with pytest.raises(SourceContractError) as caught:
        MaterialUnit(
            unit_id=UnitId("unit-1"),
            material_id=MaterialId("material-1"),
            content_hash=HASH,
            kind=kind,
            ordinal=1,
            parser_version="parser-v1",
            quality_flags=quality_flags,
        )
    assert caught.value.code is SourceErrorCode.INVALID_SHAPE
```

**Complete `test_domain_primitives.py` reference after Steps 8A–8C:**

Create `backend/tests/unit/domain/test_domain_primitives.py` with exactly:

```python
from dataclasses import FrozenInstanceError

import pytest

from projectb.domain.materials import (
    MATERIAL_LIMITS_VERSION,
    MaterialLimits,
    MaterialReviewState,
    MaterialRole,
    MaterialUnit,
    MaterialUnitKind,
    ProcessingMode,
    SelectedFile,
    material_limits_from_mapping,
)
from projectb.domain.source.errors import SourceContractError, SourceErrorCode
from projectb.domain.types import MaterialId, UnitId


HASH = "a" * 64


def test_material_enums_match_the_confirmed_v1_contract() -> None:
    assert [item.value for item in ProcessingMode] == ["L", "P", "F"]
    assert [item.value for item in MaterialRole] == [
        "lecture",
        "past_paper",
        "teacher_focus",
    ]
    assert [item.value for item in MaterialReviewState] == [
        "accepted",
        "needs_user_review",
    ]
    assert [item.value for item in MaterialUnitKind] == [
        "pdf_page",
        "image",
        "text_lines",
        "manual_entry",
    ]


def test_material_limits_match_spec_section_m1() -> None:
    limits = MaterialLimits()
    assert limits.version == MATERIAL_LIMITS_VERSION == "material-limits.v1"
    assert limits.pdf_max_bytes == 256 * 1024 * 1024
    assert limits.pdf_max_pages == 2_000
    assert limits.image_max_bytes == 20 * 1024 * 1024
    assert limits.image_max_pixels == 50_000_000
    assert limits.text_max_bytes == 2 * 1024 * 1024
    assert limits.manual_min_code_points == 1
    assert limits.manual_max_code_points == 10_000
    assert limits.batch_max_files == 50
    assert limits.batch_max_bytes == 1024 * 1024 * 1024
    assert limits.batch_max_pdf_pages == 5_000


def test_material_limits_reject_a_wrong_contract_version() -> None:
    with pytest.raises(SourceContractError) as caught:
        material_limits_from_mapping({"version": "material-limits.v2"})
    assert caught.value.code is SourceErrorCode.INVALID_MATERIAL_LIMITS


def test_material_limits_require_the_contract_version() -> None:
    with pytest.raises(SourceContractError) as caught:
        material_limits_from_mapping({})
    assert caught.value.code is SourceErrorCode.INVALID_MATERIAL_LIMITS


@pytest.mark.parametrize(
    "value",
    [True, 0, -1, 256 * 1024 * 1024, (256 * 1024 * 1024) + 1],
)
def test_material_limits_reject_every_runtime_v1_override(value: object) -> None:
    with pytest.raises(SourceContractError) as caught:
        material_limits_from_mapping(
            {
                "version": "material-limits.v1",
                "pdf_max_bytes": value,
            }
        )
    assert caught.value.code is SourceErrorCode.INVALID_MATERIAL_LIMITS


def test_selected_file_is_immutable_and_contains_no_local_path() -> None:
    selected = SelectedFile(
        material_id=MaterialId("material-1"),
        display_name="lecture.pdf",
        role=MaterialRole.LECTURE,
        content_hash=HASH,
        size_bytes=128,
        review_state=MaterialReviewState.ACCEPTED,
    )
    assert not hasattr(selected, "path")
    with pytest.raises(FrozenInstanceError):
        selected.size_bytes = 256  # type: ignore[misc]


@pytest.mark.parametrize(
    ("field", "value", "code"),
    [
        ("material_id", MaterialId(""), SourceErrorCode.INVALID_ID),
        ("display_name", "", SourceErrorCode.INVALID_SHAPE),
        ("content_hash", "A" * 64, SourceErrorCode.INVALID_CONTENT_HASH),
        ("size_bytes", -1, SourceErrorCode.INVALID_SHAPE),
        ("role", "lecture", SourceErrorCode.INVALID_SHAPE),
        ("role", MaterialUnitKind.PDF_PAGE, SourceErrorCode.INVALID_SHAPE),
        ("review_state", "accepted", SourceErrorCode.INVALID_SHAPE),
        ("review_state", MaterialRole.LECTURE, SourceErrorCode.INVALID_SHAPE),
    ],
)
def test_selected_file_rejects_invalid_values(
    field: str,
    value: object,
    code: SourceErrorCode,
) -> None:
    values: dict[str, object] = {
        "material_id": MaterialId("material-1"),
        "display_name": "lecture.pdf",
        "role": MaterialRole.LECTURE,
        "content_hash": HASH,
        "size_bytes": 128,
        "review_state": MaterialReviewState.ACCEPTED,
    }
    values[field] = value
    with pytest.raises(SourceContractError) as caught:
        SelectedFile(**values)
    assert caught.value.code is code


def test_material_unit_uses_a_one_based_ordinal() -> None:
    unit = MaterialUnit(
        unit_id=UnitId("unit-1"),
        material_id=MaterialId("material-1"),
        content_hash=HASH,
        kind=MaterialUnitKind.PDF_PAGE,
        ordinal=1,
        parser_version="parser-v1",
        quality_flags=frozenset({"text_present"}),
    )
    assert unit.ordinal == 1
    with pytest.raises(SourceContractError) as caught:
        MaterialUnit(
            unit_id=UnitId("unit-0"),
            material_id=MaterialId("material-1"),
            content_hash=HASH,
            kind=MaterialUnitKind.PDF_PAGE,
            ordinal=0,
            parser_version="parser-v1",
        )
    assert caught.value.code is SourceErrorCode.INVALID_PAGE


@pytest.mark.parametrize(
    ("kind", "quality_flags"),
    [
        ("pdf_page", frozenset({"text_present"})),
        (MaterialRole.LECTURE, frozenset({"text_present"})),
        (MaterialUnitKind.PDF_PAGE, "text_present"),
        (MaterialUnitKind.PDF_PAGE, frozenset({1})),
    ],
)
def test_material_unit_rejects_raw_kind_or_string_quality_flags(
    kind: object,
    quality_flags: object,
) -> None:
    with pytest.raises(SourceContractError) as caught:
        MaterialUnit(
            unit_id=UnitId("unit-1"),
            material_id=MaterialId("material-1"),
            content_hash=HASH,
            kind=kind,
            ordinal=1,
            parser_version="parser-v1",
            quality_flags=quality_flags,
        )
    assert caught.value.code is SourceErrorCode.INVALID_SHAPE
```

- [ ] **Step 9: Run the material-primitives tests and capture the expected red result**

Run:

```powershell
$env:PYTHONPATH = (Resolve-Path 'backend/src').Path
python -m pytest backend/tests/unit/domain/test_domain_primitives.py -q
```

Expected: exit code 2 with collection error `ModuleNotFoundError: No module named 'projectb.domain.materials'`; no test passes.

- [ ] **Step 10: Implement the opaque ID types**

Create `backend/src/projectb/domain/types.py` with exactly:

```python
from typing import NewType


CourseId = NewType("CourseId", str)
EntryId = NewType("EntryId", str)
ImageId = NewType("ImageId", str)
MaterialId = NewType("MaterialId", str)
UnitId = NewType("UnitId", str)


__all__ = ["CourseId", "EntryId", "ImageId", "MaterialId", "UnitId"]
```

- [ ] **Step 11A: Implement the fixed v1 enums and material-limits loader**

Create `backend/src/projectb/domain/materials.py` with this exact first slice:

```python
from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import StrEnum

from projectb.domain.source.errors import SourceContractError, SourceErrorCode
from projectb.domain.source.hashing import validate_content_hash
from projectb.domain.types import MaterialId, UnitId


MATERIAL_LIMITS_VERSION = "material-limits.v1"


class ProcessingMode(StrEnum):
    LOCAL = "L"
    PAGE_REMOTE = "P"
    FULL_REMOTE = "F"


class MaterialRole(StrEnum):
    LECTURE = "lecture"
    PAST_PAPER = "past_paper"
    TEACHER_FOCUS = "teacher_focus"


class MaterialReviewState(StrEnum):
    ACCEPTED = "accepted"
    NEEDS_USER_REVIEW = "needs_user_review"


class MaterialUnitKind(StrEnum):
    PDF_PAGE = "pdf_page"
    IMAGE = "image"
    TEXT_LINES = "text_lines"
    MANUAL_ENTRY = "manual_entry"


@dataclass(frozen=True, slots=True)
class MaterialLimits:
    version: str = field(default=MATERIAL_LIMITS_VERSION, init=False)
    pdf_max_bytes: int = field(default=256 * 1024 * 1024, init=False)
    pdf_max_pages: int = field(default=2_000, init=False)
    image_max_bytes: int = field(default=20 * 1024 * 1024, init=False)
    image_max_pixels: int = field(default=50_000_000, init=False)
    text_max_bytes: int = field(default=2 * 1024 * 1024, init=False)
    manual_min_code_points: int = field(default=1, init=False)
    manual_max_code_points: int = field(default=10_000, init=False)
    batch_max_files: int = field(default=50, init=False)
    batch_max_bytes: int = field(default=1024 * 1024 * 1024, init=False)
    batch_max_pdf_pages: int = field(default=5_000, init=False)


def material_limits_from_mapping(payload: Mapping[str, object]) -> MaterialLimits:
    if set(payload) != {"version"}:
        raise SourceContractError(SourceErrorCode.INVALID_MATERIAL_LIMITS)
    if payload["version"] != MATERIAL_LIMITS_VERSION:
        raise SourceContractError(SourceErrorCode.INVALID_MATERIAL_LIMITS)
    return MaterialLimits()
```

- [ ] **Step 11B: Append the selected-file boundary**

Append exactly to `backend/src/projectb/domain/materials.py`:

```python


def _require_id(value: str) -> None:
    if not isinstance(value, str) or not value or value.strip() != value:
        raise SourceContractError(SourceErrorCode.INVALID_ID)


def _require_text(value: str) -> None:
    if not isinstance(value, str) or not value or value.strip() != value:
        raise SourceContractError(SourceErrorCode.INVALID_SHAPE)


@dataclass(frozen=True, slots=True)
class SelectedFile:
    material_id: MaterialId
    display_name: str
    role: MaterialRole
    content_hash: str
    size_bytes: int
    review_state: MaterialReviewState

    def __post_init__(self) -> None:
        _require_id(self.material_id)
        _require_text(self.display_name)
        if not isinstance(self.role, MaterialRole):
            raise SourceContractError(SourceErrorCode.INVALID_SHAPE)
        if not isinstance(self.review_state, MaterialReviewState):
            raise SourceContractError(SourceErrorCode.INVALID_SHAPE)
        validate_content_hash(self.content_hash)
        if type(self.size_bytes) is not int or self.size_bytes < 0:
            raise SourceContractError(SourceErrorCode.INVALID_SHAPE)
```

- [ ] **Step 11C: Append the material-unit boundary**

Append exactly to `backend/src/projectb/domain/materials.py`:

```python


@dataclass(frozen=True, slots=True)
class MaterialUnit:
    unit_id: UnitId
    material_id: MaterialId
    content_hash: str
    kind: MaterialUnitKind
    ordinal: int
    parser_version: str
    quality_flags: frozenset[str] = frozenset()

    def __post_init__(self) -> None:
        _require_id(self.unit_id)
        _require_id(self.material_id)
        validate_content_hash(self.content_hash)
        _require_text(self.parser_version)
        if not isinstance(self.kind, MaterialUnitKind):
            raise SourceContractError(SourceErrorCode.INVALID_SHAPE)
        if type(self.ordinal) is not int or self.ordinal < 1:
            raise SourceContractError(SourceErrorCode.INVALID_PAGE)
        if not isinstance(self.quality_flags, frozenset):
            raise SourceContractError(SourceErrorCode.INVALID_SHAPE)
        quality_flags = frozenset(self.quality_flags)
        if any(
            not isinstance(flag, str) or not flag or flag.strip() != flag
            for flag in quality_flags
        ):
            raise SourceContractError(SourceErrorCode.INVALID_SHAPE)
        object.__setattr__(self, "quality_flags", quality_flags)
```

- [ ] **Step 12: Run the material-primitives tests and capture the green result**

Run:

```powershell
$env:PYTHONPATH = (Resolve-Path 'backend/src').Path
python -m pytest backend/tests/unit/domain/test_domain_primitives.py -q
```

Expected: exit code 0 with `21 passed`.

- [ ] **Step 12B: Format the material slice under green tests**

Run:

```powershell
python -m ruff format --config backend/pyproject.toml backend/src/projectb/domain/types.py backend/src/projectb/domain/materials.py backend/tests/unit/domain/test_domain_primitives.py
```

Expected: exit code 0; Ruff reports the three files formatted or already formatted and changes no behavior.

- [ ] **Step 12C: Re-run material tests after the refactor step**

Run:

```powershell
$env:PYTHONPATH = (Resolve-Path 'backend/src').Path
python -m pytest backend/tests/unit/domain/test_domain_primitives.py -q
```

Expected: exit code 0 with `21 passed`.

- [ ] **Step 13A: Create the failing discriminated-locator parsing tests**

Create `backend/tests/unit/domain/test_source_models.py` with this exact first slice:

```python
from dataclasses import FrozenInstanceError

import pytest

from projectb.domain.source.errors import SourceContractError, SourceErrorCode
from projectb.domain.source.models import (
    ImageLocator,
    ManualEntryLocator,
    ManualSource,
    MaterialSource,
    PdfPageLocator,
    Region,
    SourceCatalog,
    TextLinesLocator,
    source_locator_from_mapping,
    validate_source_locator,
)
from projectb.domain.types import EntryId, ImageId, MaterialId


HASH = "a" * 64
STALE_HASH = "b" * 64


@pytest.mark.parametrize(
    ("payload", "expected_type", "expected_kind"),
    [
        (
            {
                "kind": "pdf_page",
                "material_id": "material-1",
                "content_hash": HASH,
                "page": 1,
                "region": {"x": 0, "y": 0, "width": 1, "height": 1},
            },
            PdfPageLocator,
            "pdf_page",
        ),
        (
            {
                "kind": "image",
                "material_id": "material-1",
                "content_hash": HASH,
                "image_id": "image-1",
            },
            ImageLocator,
            "image",
        ),
        (
            {
                "kind": "text_lines",
                "material_id": "material-1",
                "content_hash": HASH,
                "line_start": 1,
                "line_end": 2,
            },
            TextLinesLocator,
            "text_lines",
        ),
        (
            {"kind": "manual_entry", "entry_id": "entry-1", "version": 1},
            ManualEntryLocator,
            "manual_entry",
        ),
    ],
)
def test_mapping_parser_builds_each_discriminated_branch(
    payload: dict[str, object],
    expected_type: type[object],
    expected_kind: str,
) -> None:
    locator = source_locator_from_mapping(payload)
    assert isinstance(locator, expected_type)
    assert locator.kind == expected_kind


def test_mapping_parser_rejects_unknown_kind() -> None:
    with pytest.raises(SourceContractError) as caught:
        source_locator_from_mapping({"kind": "web_url", "url": "https://invalid"})
    assert caught.value.code is SourceErrorCode.INVALID_KIND


def test_mapping_parser_rejects_mixed_branch_fields() -> None:
    with pytest.raises(SourceContractError) as caught:
        source_locator_from_mapping(
            {
                "kind": "pdf_page",
                "material_id": "material-1",
                "content_hash": HASH,
                "page": 1,
                "line_start": 1,
            }
        )
    assert caught.value.code is SourceErrorCode.INVALID_SHAPE
```

- [ ] **Step 13B: Append the failing immutable-coordinate tests**

Append exactly to `backend/tests/unit/domain/test_source_models.py`:

```python


def test_locator_values_are_immutable() -> None:
    locator = PdfPageLocator(MaterialId("material-1"), HASH, 1)
    with pytest.raises(FrozenInstanceError):
        locator.page = 2  # type: ignore[misc]


def test_pdf_pages_and_text_lines_are_one_based() -> None:
    with pytest.raises(SourceContractError) as page_error:
        PdfPageLocator(MaterialId("material-1"), HASH, 0)
    assert page_error.value.code is SourceErrorCode.INVALID_PAGE
    with pytest.raises(SourceContractError) as line_error:
        TextLinesLocator(MaterialId("material-1"), HASH, 0, 1)
    assert line_error.value.code is SourceErrorCode.INVALID_LINE_RANGE
    with pytest.raises(SourceContractError) as order_error:
        TextLinesLocator(MaterialId("material-1"), HASH, 2, 1)
    assert order_error.value.code is SourceErrorCode.INVALID_LINE_RANGE


@pytest.mark.parametrize(
    "content_hash",
    ["a" * 63, "a" * 65, "A" * 64, "sha256:" + ("a" * 64)],
)
def test_locators_reject_noncanonical_content_hash(content_hash: str) -> None:
    with pytest.raises(SourceContractError) as caught:
        PdfPageLocator(MaterialId("material-1"), content_hash, 1)
    assert caught.value.code is SourceErrorCode.INVALID_CONTENT_HASH


def test_region_accepts_finite_normalized_top_left_bounds() -> None:
    assert Region(x=0, y=0, width=1, height=1) == Region(
        x=0.0,
        y=0.0,
        width=1.0,
        height=1.0,
    )


def test_locator_rejects_a_non_region_object() -> None:
    values: dict[str, object] = {
        "material_id": MaterialId("material-1"),
        "content_hash": HASH,
        "page": 1,
        "region": {"x": 0, "y": 0, "width": 1, "height": 1},
    }
    with pytest.raises(SourceContractError) as caught:
        PdfPageLocator(**values)
    assert caught.value.code is SourceErrorCode.INVALID_REGION


@pytest.mark.parametrize(
    ("x", "y", "width", "height"),
    [
        (-0.1, 0, 0.5, 0.5),
        (0, -0.1, 0.5, 0.5),
        (1, 0, 0.1, 0.1),
        (0, 1, 0.1, 0.1),
        (0, 0, 0, 0.5),
        (0, 0, 0.5, 0),
        (0.75, 0, 0.5, 0.5),
        (0, 0.75, 0.5, 0.5),
        (float("nan"), 0, 0.5, 0.5),
        (0, float("inf"), 0.5, 0.5),
    ],
)
def test_region_rejects_nonfinite_or_out_of_bounds_values(
    x: float,
    y: float,
    width: float,
    height: float,
) -> None:
    with pytest.raises(SourceContractError) as caught:
        Region(x=x, y=y, width=width, height=height)
    assert caught.value.code is SourceErrorCode.INVALID_REGION
```

- [ ] **Step 13C: Append the failing catalog-validation tests**

Append exactly to `backend/tests/unit/domain/test_source_models.py`:

```python


def test_catalog_accepts_matching_pdf_image_text_and_manual_locators() -> None:
    catalog = SourceCatalog(
        materials=(
            MaterialSource(
                material_id=MaterialId("material-1"),
                content_hash=HASH,
                page_count=2,
                image_ids=frozenset({ImageId("image-1")}),
                line_count=4,
            ),
        ),
        manual_entries=(ManualSource(EntryId("entry-1"), 3),),
    )
    locators = (
        PdfPageLocator(MaterialId("material-1"), HASH, 2),
        ImageLocator(MaterialId("material-1"), HASH, ImageId("image-1")),
        TextLinesLocator(MaterialId("material-1"), HASH, 2, 4),
        ManualEntryLocator(EntryId("entry-1"), 3),
    )
    for locator in locators:
        assert validate_source_locator(locator, catalog) is None


@pytest.mark.parametrize(
    ("locator", "expected_code"),
    [
        (
            PdfPageLocator(MaterialId("missing"), HASH, 1),
            SourceErrorCode.MATERIAL_NOT_FOUND,
        ),
        (
            PdfPageLocator(MaterialId("material-1"), STALE_HASH, 1),
            SourceErrorCode.STALE_CONTENT_HASH,
        ),
        (
            PdfPageLocator(MaterialId("material-1"), HASH, 3),
            SourceErrorCode.PAGE_OUT_OF_RANGE,
        ),
        (
            ImageLocator(MaterialId("material-1"), HASH, ImageId("missing")),
            SourceErrorCode.IMAGE_NOT_FOUND,
        ),
        (
            TextLinesLocator(MaterialId("material-1"), HASH, 4, 5),
            SourceErrorCode.LINE_OUT_OF_RANGE,
        ),
        (
            ManualEntryLocator(EntryId("missing"), 1),
            SourceErrorCode.ENTRY_NOT_FOUND,
        ),
        (
            ManualEntryLocator(EntryId("entry-1"), 2),
            SourceErrorCode.STALE_ENTRY_VERSION,
        ),
    ],
)
def test_catalog_rejects_missing_stale_or_out_of_range_locators(
    locator: object,
    expected_code: SourceErrorCode,
) -> None:
    catalog = SourceCatalog(
        materials=(
            MaterialSource(
                material_id=MaterialId("material-1"),
                content_hash=HASH,
                page_count=2,
                image_ids=frozenset({ImageId("image-1")}),
                line_count=4,
            ),
        ),
        manual_entries=(ManualSource(EntryId("entry-1"), 3),),
    )
    with pytest.raises(SourceContractError) as caught:
        validate_source_locator(locator, catalog)
    assert caught.value.code is expected_code
```

- [ ] **Step 14: Run the locator-model tests and capture the expected red result**

Run:

```powershell
$env:PYTHONPATH = (Resolve-Path 'backend/src').Path
python -m pytest backend/tests/unit/domain/test_source_models.py -q
```

Expected: exit code 2 with collection error `ModuleNotFoundError: No module named 'projectb.domain.source.models'`; no test passes.

- [ ] **Step 15A: Implement coordinate helpers and the immutable Region**

Create `backend/src/projectb/domain/source/models.py` with this exact first slice:

```python
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
import math
from typing import Literal, cast

from projectb.domain.source.errors import SourceContractError, SourceErrorCode
from projectb.domain.source.hashing import validate_content_hash
from projectb.domain.types import EntryId, ImageId, MaterialId


def _require_id(value: str) -> None:
    if not isinstance(value, str) or not value or value.strip() != value:
        raise SourceContractError(SourceErrorCode.INVALID_ID)


def _require_positive_int(value: int, code: SourceErrorCode) -> None:
    if type(value) is not int or value < 1:
        raise SourceContractError(code)


@dataclass(frozen=True, slots=True)
class Region:
    x: float
    y: float
    width: float
    height: float

    def __post_init__(self) -> None:
        for name in ("x", "y", "width", "height"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise SourceContractError(SourceErrorCode.INVALID_REGION)
            value = float(value)
            if not math.isfinite(value):
                raise SourceContractError(SourceErrorCode.INVALID_REGION)
            object.__setattr__(self, name, value)
        if not (0 <= self.x < 1 and 0 <= self.y < 1):
            raise SourceContractError(SourceErrorCode.INVALID_REGION)
        if not (0 < self.width <= 1 - self.x):
            raise SourceContractError(SourceErrorCode.INVALID_REGION)
        if not (0 < self.height <= 1 - self.y):
            raise SourceContractError(SourceErrorCode.INVALID_REGION)
```

- [ ] **Step 15B: Append PDF-page and image locator records**

Append exactly to `backend/src/projectb/domain/source/models.py`:

```python


@dataclass(frozen=True, slots=True)
class PdfPageLocator:
    material_id: MaterialId
    content_hash: str
    page: int
    region: Region | None = None
    kind: Literal["pdf_page"] = field(default="pdf_page", init=False)

    def __post_init__(self) -> None:
        _require_id(self.material_id)
        validate_content_hash(self.content_hash)
        _require_positive_int(self.page, SourceErrorCode.INVALID_PAGE)
        if self.region is not None and not isinstance(self.region, Region):
            raise SourceContractError(SourceErrorCode.INVALID_REGION)


@dataclass(frozen=True, slots=True)
class ImageLocator:
    material_id: MaterialId
    content_hash: str
    image_id: ImageId
    region: Region | None = None
    kind: Literal["image"] = field(default="image", init=False)

    def __post_init__(self) -> None:
        _require_id(self.material_id)
        validate_content_hash(self.content_hash)
        _require_id(self.image_id)
        if self.region is not None and not isinstance(self.region, Region):
            raise SourceContractError(SourceErrorCode.INVALID_REGION)
```

- [ ] **Step 15C: Append text-line and manual-entry locator records**

Append exactly to `backend/src/projectb/domain/source/models.py`:

```python


@dataclass(frozen=True, slots=True)
class TextLinesLocator:
    material_id: MaterialId
    content_hash: str
    line_start: int
    line_end: int
    kind: Literal["text_lines"] = field(default="text_lines", init=False)

    def __post_init__(self) -> None:
        _require_id(self.material_id)
        validate_content_hash(self.content_hash)
        _require_positive_int(self.line_start, SourceErrorCode.INVALID_LINE_RANGE)
        _require_positive_int(self.line_end, SourceErrorCode.INVALID_LINE_RANGE)
        if self.line_end < self.line_start:
            raise SourceContractError(SourceErrorCode.INVALID_LINE_RANGE)


@dataclass(frozen=True, slots=True)
class ManualEntryLocator:
    entry_id: EntryId
    version: int
    kind: Literal["manual_entry"] = field(default="manual_entry", init=False)

    def __post_init__(self) -> None:
        _require_id(self.entry_id)
        _require_positive_int(self.version, SourceErrorCode.INVALID_SHAPE)


type SourceLocator = PdfPageLocator | ImageLocator | TextLinesLocator | ManualEntryLocator
```

- [ ] **Step 15D: Append immutable catalog records**

Append exactly to `backend/src/projectb/domain/source/models.py`:

```python


@dataclass(frozen=True, slots=True)
class MaterialSource:
    material_id: MaterialId
    content_hash: str
    page_count: int = 0
    image_ids: frozenset[ImageId] = frozenset()
    line_count: int = 0

    def __post_init__(self) -> None:
        _require_id(self.material_id)
        validate_content_hash(self.content_hash)
        if type(self.page_count) is not int or self.page_count < 0:
            raise SourceContractError(SourceErrorCode.INVALID_CATALOG)
        if type(self.line_count) is not int or self.line_count < 0:
            raise SourceContractError(SourceErrorCode.INVALID_CATALOG)
        image_ids = frozenset(self.image_ids)
        for image_id in image_ids:
            _require_id(image_id)
        object.__setattr__(self, "image_ids", image_ids)


@dataclass(frozen=True, slots=True)
class ManualSource:
    entry_id: EntryId
    version: int

    def __post_init__(self) -> None:
        _require_id(self.entry_id)
        _require_positive_int(self.version, SourceErrorCode.INVALID_CATALOG)


@dataclass(frozen=True, slots=True)
class SourceCatalog:
    materials: Sequence[MaterialSource] = ()
    manual_entries: Sequence[ManualSource] = ()

    def __post_init__(self) -> None:
        materials = tuple(self.materials)
        manual_entries = tuple(self.manual_entries)
        if len({item.material_id for item in materials}) != len(materials):
            raise SourceContractError(SourceErrorCode.INVALID_CATALOG)
        if len({item.entry_id for item in manual_entries}) != len(manual_entries):
            raise SourceContractError(SourceErrorCode.INVALID_CATALOG)
        object.__setattr__(self, "materials", materials)
        object.__setattr__(self, "manual_entries", manual_entries)
```

- [ ] **Step 15E: Append fail-closed catalog validation**

Append exactly to `backend/src/projectb/domain/source/models.py`:

```python


def validate_source_locator(locator: object, catalog: SourceCatalog) -> None:
    if isinstance(locator, ManualEntryLocator):
        source = next(
            (item for item in catalog.manual_entries if item.entry_id == locator.entry_id),
            None,
        )
        if source is None:
            raise SourceContractError(SourceErrorCode.ENTRY_NOT_FOUND)
        if source.version != locator.version:
            raise SourceContractError(SourceErrorCode.STALE_ENTRY_VERSION)
        return

    if not isinstance(locator, (PdfPageLocator, ImageLocator, TextLinesLocator)):
        raise SourceContractError(SourceErrorCode.INVALID_KIND)
    source = next(
        (item for item in catalog.materials if item.material_id == locator.material_id),
        None,
    )
    if source is None:
        raise SourceContractError(SourceErrorCode.MATERIAL_NOT_FOUND)
    if source.content_hash != locator.content_hash:
        raise SourceContractError(SourceErrorCode.STALE_CONTENT_HASH)
    if isinstance(locator, PdfPageLocator) and locator.page > source.page_count:
        raise SourceContractError(SourceErrorCode.PAGE_OUT_OF_RANGE)
    if isinstance(locator, ImageLocator) and locator.image_id not in source.image_ids:
        raise SourceContractError(SourceErrorCode.IMAGE_NOT_FOUND)
    if isinstance(locator, TextLinesLocator) and locator.line_end > source.line_count:
        raise SourceContractError(SourceErrorCode.LINE_OUT_OF_RANGE)
```

- [ ] **Step 15F: Append strict mapping-parser helpers**

Append exactly to `backend/src/projectb/domain/source/models.py`:

```python


def _require_keys(payload: Mapping[str, object], expected: set[str]) -> None:
    if set(payload) != expected:
        raise SourceContractError(SourceErrorCode.INVALID_SHAPE)


def _string(payload: Mapping[str, object], key: str) -> str:
    value = payload[key]
    if not isinstance(value, str) or not value or value.strip() != value:
        raise SourceContractError(SourceErrorCode.INVALID_SHAPE)
    return value


def _integer(payload: Mapping[str, object], key: str) -> int:
    value = payload[key]
    if type(value) is not int:
        raise SourceContractError(SourceErrorCode.INVALID_SHAPE)
    return cast(int, value)


def _number(payload: Mapping[str, object], key: str) -> float:
    value = payload[key]
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise SourceContractError(SourceErrorCode.INVALID_REGION)
    return float(value)


def _region(value: object) -> Region | None:
    if value is None:
        return None
    if not isinstance(value, Mapping):
        raise SourceContractError(SourceErrorCode.INVALID_REGION)
    region = cast(Mapping[str, object], value)
    _require_keys(region, {"x", "y", "width", "height"})
    return Region(
        x=_number(region, "x"),
        y=_number(region, "y"),
        width=_number(region, "width"),
        height=_number(region, "height"),
    )
```

- [ ] **Step 15G: Append the exact discriminated mapping parser**

Append exactly to `backend/src/projectb/domain/source/models.py`:

```python


def source_locator_from_mapping(payload: Mapping[str, object]) -> SourceLocator:
    kind = payload.get("kind")
    if kind == "pdf_page":
        allowed = {"kind", "material_id", "content_hash", "page"}
        if "region" in payload:
            allowed.add("region")
        _require_keys(payload, allowed)
        return PdfPageLocator(
            material_id=MaterialId(_string(payload, "material_id")),
            content_hash=_string(payload, "content_hash"),
            page=_integer(payload, "page"),
            region=_region(payload.get("region")),
        )
    if kind == "image":
        allowed = {"kind", "material_id", "content_hash", "image_id"}
        if "region" in payload:
            allowed.add("region")
        _require_keys(payload, allowed)
        return ImageLocator(
            material_id=MaterialId(_string(payload, "material_id")),
            content_hash=_string(payload, "content_hash"),
            image_id=ImageId(_string(payload, "image_id")),
            region=_region(payload.get("region")),
        )
    if kind == "text_lines":
        _require_keys(
            payload,
            {"kind", "material_id", "content_hash", "line_start", "line_end"},
        )
        return TextLinesLocator(
            material_id=MaterialId(_string(payload, "material_id")),
            content_hash=_string(payload, "content_hash"),
            line_start=_integer(payload, "line_start"),
            line_end=_integer(payload, "line_end"),
        )
    if kind == "manual_entry":
        _require_keys(payload, {"kind", "entry_id", "version"})
        return ManualEntryLocator(
            entry_id=EntryId(_string(payload, "entry_id")),
            version=_integer(payload, "version"),
        )
    raise SourceContractError(SourceErrorCode.INVALID_KIND)
```

- [ ] **Step 16: Run the locator-model tests and capture the green result**

Run:

```powershell
$env:PYTHONPATH = (Resolve-Path 'backend/src').Path
python -m pytest backend/tests/unit/domain/test_source_models.py -q
```

Expected: exit code 0 with `32 passed`.

- [ ] **Step 16B: Format the locator-model slice under green tests**

Run:

```powershell
python -m ruff format --config backend/pyproject.toml backend/src/projectb/domain/source/models.py backend/tests/unit/domain/test_source_models.py
```

Expected: exit code 0; Ruff reports the two files formatted or already formatted and changes no behavior.

- [ ] **Step 16C: Re-run locator-model tests after the refactor step**

Run:

```powershell
$env:PYTHONPATH = (Resolve-Path 'backend/src').Path
python -m pytest backend/tests/unit/domain/test_source_models.py -q
```

Expected: exit code 0 with `32 passed`.

- [ ] **Step 17A: Create the failing unique-span and length-boundary tests**

Create `backend/tests/unit/domain/test_source_proof.py` with this exact first slice:

```python
import pytest

from projectb.domain.source.errors import (
    SourceContractError,
    SourceErrorCode,
    SourceInsufficient,
    SourceInsufficientReason,
)
from projectb.domain.source.models import PdfPageLocator
from projectb.domain.source.proof import PageText, prove_unique_pdf_page
from projectb.domain.types import MaterialId


HASH = "a" * 64
MATERIAL_ID = MaterialId("material-1")
UNIQUE_SPAN = "shared counter update needs one critical section"


def page(number: int, text: str) -> PageText:
    return PageText(
        material_id=MATERIAL_ID,
        content_hash=HASH,
        page=number,
        text=text,
    )


def test_unique_normalized_span_maps_to_one_page() -> None:
    pages = (
        page(24, "unrelated preface"),
        page(
            25,
            "Header shared counter\r\nupdate needs one criti\u00adcal section footer",
        ),
    )
    assert prove_unique_pdf_page(UNIQUE_SPAN, pages, MATERIAL_ID, HASH) == (
        PdfPageLocator(MATERIAL_ID, HASH, 25)
    )


def test_exactly_32_normalized_code_points_are_eligible() -> None:
    span = "x" * 32
    assert prove_unique_pdf_page(
        span,
        (page(1, span),),
        MATERIAL_ID,
        HASH,
    ) == PdfPageLocator(MATERIAL_ID, HASH, 1)


def test_31_normalized_code_points_are_too_short() -> None:
    result = prove_unique_pdf_page(
        "x" * 31,
        (page(1, "x" * 31),),
        MATERIAL_ID,
        HASH,
    )
    assert result == SourceInsufficient(SourceInsufficientReason.TOO_SHORT)
```

- [ ] **Step 17B: Append the failing ambiguity and no-match tests**

Append exactly to `backend/tests/unit/domain/test_source_proof.py`:

```python


def test_span_on_two_pages_is_ambiguous() -> None:
    pages = (
        page(1, UNIQUE_SPAN),
        page(2, UNIQUE_SPAN),
    )
    assert prove_unique_pdf_page(UNIQUE_SPAN, pages, MATERIAL_ID, HASH) == (
        SourceInsufficient(SourceInsufficientReason.AMBIGUOUS)
    )


def test_cross_page_span_has_no_match() -> None:
    chunk = "left half of a cross page span right half"
    pages = (
        page(1, "left half of a cross page span"),
        page(2, "right half"),
    )
    assert prove_unique_pdf_page(chunk, pages, MATERIAL_ID, HASH) == (
        SourceInsufficient(SourceInsufficientReason.NO_MATCH)
    )


def test_visual_only_claim_has_no_text_match() -> None:
    chunk = "diagram arrows establish ordering between these events"
    assert prove_unique_pdf_page(
        chunk,
        (page(1, ""),),
        MATERIAL_ID,
        HASH,
    ) == SourceInsufficient(SourceInsufficientReason.NO_MATCH)


def test_absent_span_has_no_match() -> None:
    chunk = "this sufficiently long source span is absent"
    assert prove_unique_pdf_page(
        chunk,
        (page(1, "different page text"),),
        MATERIAL_ID,
        HASH,
    ) == SourceInsufficient(SourceInsufficientReason.NO_MATCH)
```

- [ ] **Step 17C: Append the failing catalog-binding tests**

Append exactly to `backend/tests/unit/domain/test_source_proof.py`:

```python


def test_duplicate_page_numbers_are_an_invalid_catalog() -> None:
    pages = (
        page(1, UNIQUE_SPAN),
        page(1, "different text"),
    )
    with pytest.raises(SourceContractError) as caught:
        prove_unique_pdf_page(UNIQUE_SPAN, pages, MATERIAL_ID, HASH)
    assert caught.value.code is SourceErrorCode.INVALID_CATALOG


@pytest.mark.parametrize(
    ("page_record", "expected_code"),
    [
        (
            PageText(MaterialId("other-material"), HASH, 1, UNIQUE_SPAN),
            SourceErrorCode.INVALID_CATALOG,
        ),
        (
            PageText(MATERIAL_ID, "b" * 64, 1, UNIQUE_SPAN),
            SourceErrorCode.STALE_CONTENT_HASH,
        ),
    ],
)
def test_page_text_must_belong_to_the_requested_raw_file(
    page_record: PageText,
    expected_code: SourceErrorCode,
) -> None:
    with pytest.raises(SourceContractError) as caught:
        prove_unique_pdf_page(UNIQUE_SPAN, (page_record,), MATERIAL_ID, HASH)
    assert caught.value.code is expected_code
```

- [ ] **Step 18: Run the proof tests and capture the expected red result**

Run:

```powershell
$env:PYTHONPATH = (Resolve-Path 'backend/src').Path
python -m pytest backend/tests/unit/domain/test_source_proof.py -q
```

Expected: exit code 2 with collection error `ModuleNotFoundError: No module named 'projectb.domain.source.proof'`; no test passes.

- [ ] **Step 19A: Implement immutable page-text input validation**

Create `backend/src/projectb/domain/source/proof.py` with this exact first slice:

```python
from collections.abc import Sequence
from dataclasses import dataclass

from projectb.domain.source.errors import (
    SourceContractError,
    SourceErrorCode,
    SourceInsufficient,
    SourceInsufficientReason,
)
from projectb.domain.source.hashing import normalize_source_text, validate_content_hash
from projectb.domain.source.models import PdfPageLocator
from projectb.domain.types import MaterialId


MINIMUM_NORMALIZED_CODE_POINTS = 32


@dataclass(frozen=True, slots=True)
class PageText:
    material_id: MaterialId
    content_hash: str
    page: int
    text: str

    def __post_init__(self) -> None:
        if (
            not isinstance(self.material_id, str)
            or not self.material_id
            or self.material_id.strip() != self.material_id
        ):
            raise SourceContractError(SourceErrorCode.INVALID_ID)
        validate_content_hash(self.content_hash)
        if type(self.page) is not int or self.page < 1:
            raise SourceContractError(SourceErrorCode.INVALID_PAGE)
        if not isinstance(self.text, str):
            raise SourceContractError(SourceErrorCode.INVALID_SHAPE)
```

- [ ] **Step 19B: Append deterministic unique-page proof**

Append exactly to `backend/src/projectb/domain/source/proof.py`:

```python


def prove_unique_pdf_page(
    chunk: str,
    pages: Sequence[PageText],
    material_id: MaterialId,
    content_hash: str,
) -> PdfPageLocator | SourceInsufficient:
    if not isinstance(material_id, str) or not material_id or material_id.strip() != material_id:
        raise SourceContractError(SourceErrorCode.INVALID_ID)
    validate_content_hash(content_hash)
    for page in pages:
        if page.material_id != material_id:
            raise SourceContractError(SourceErrorCode.INVALID_CATALOG)
        if page.content_hash != content_hash:
            raise SourceContractError(SourceErrorCode.STALE_CONTENT_HASH)
    normalized_chunk = normalize_source_text(chunk)
    if len(normalized_chunk) < MINIMUM_NORMALIZED_CODE_POINTS:
        return SourceInsufficient(SourceInsufficientReason.TOO_SHORT)

    page_numbers = [page.page for page in pages]
    if len(page_numbers) != len(set(page_numbers)):
        raise SourceContractError(SourceErrorCode.INVALID_CATALOG)
    matches = tuple(
        page.page
        for page in pages
        if normalized_chunk in normalize_source_text(page.text)
    )
    if not matches:
        return SourceInsufficient(SourceInsufficientReason.NO_MATCH)
    if len(matches) != 1:
        return SourceInsufficient(SourceInsufficientReason.AMBIGUOUS)
    return PdfPageLocator(
        material_id=material_id,
        content_hash=content_hash,
        page=matches[0],
    )
```

- [ ] **Step 20: Run the proof tests and capture the green result**

Run:

```powershell
$env:PYTHONPATH = (Resolve-Path 'backend/src').Path
python -m pytest backend/tests/unit/domain/test_source_proof.py -q
```

Expected: exit code 0 with `10 passed`.

- [ ] **Step 20B: Format the proof slice under green tests**

Run:

```powershell
python -m ruff format --config backend/pyproject.toml backend/src/projectb/domain/source/proof.py backend/tests/unit/domain/test_source_proof.py
```

Expected: exit code 0; Ruff reports the two files formatted or already formatted and changes no behavior.

- [ ] **Step 20C: Re-run proof tests after the refactor step**

Run:

```powershell
$env:PYTHONPATH = (Resolve-Path 'backend/src').Path
python -m pytest backend/tests/unit/domain/test_source_proof.py -q
```

Expected: exit code 0 with `10 passed`.

- [ ] **Step 21: Write the failing public-facade test**

Create `backend/tests/unit/domain/test_source_exports.py` with exactly:

```python
from projectb.domain.source import (
    PageText,
    PdfPageLocator,
    prove_unique_pdf_page,
    raw_file_content_hash,
    source_locator_from_mapping,
)
from projectb.domain.types import MaterialId


def test_source_facade_exports_the_stable_downstream_contract() -> None:
    content_hash = raw_file_content_hash(b"source")
    locator = source_locator_from_mapping(
        {
            "kind": "pdf_page",
            "material_id": "material-1",
            "content_hash": content_hash,
            "page": 1,
        }
    )
    assert locator == PdfPageLocator(MaterialId("material-1"), content_hash, 1)
    assert prove_unique_pdf_page(
        "x" * 32,
        (
            PageText(
                material_id=MaterialId("material-1"),
                content_hash=content_hash,
                page=1,
                text="x" * 32,
            ),
        ),
        MaterialId("material-1"),
        content_hash,
    ) == locator
```

- [ ] **Step 22: Run the facade test and capture the expected red result**

Run:

```powershell
$env:PYTHONPATH = (Resolve-Path 'backend/src').Path
python -m pytest backend/tests/unit/domain/test_source_exports.py -q
```

Expected: exit code 2 with collection error containing `cannot import name 'PageText' from 'projectb.domain.source'`; no test passes.

- [ ] **Step 23: Publish the complete source facade**

Replace `backend/src/projectb/domain/source/__init__.py` with exactly:

```python
"""Validated local source contracts."""

from projectb.domain.source.errors import (
    SourceContractError,
    SourceErrorCode,
    SourceInsufficient,
    SourceInsufficientReason,
)
from projectb.domain.source.hashing import (
    normalize_source_text,
    raw_file_content_hash,
    validate_content_hash,
)
from projectb.domain.source.models import (
    ImageLocator,
    ManualEntryLocator,
    ManualSource,
    MaterialSource,
    PdfPageLocator,
    Region,
    SourceCatalog,
    SourceLocator,
    TextLinesLocator,
    source_locator_from_mapping,
    validate_source_locator,
)
from projectb.domain.source.proof import (
    MINIMUM_NORMALIZED_CODE_POINTS,
    PageText,
    prove_unique_pdf_page,
)


__all__ = [
    "ImageLocator",
    "MINIMUM_NORMALIZED_CODE_POINTS",
    "ManualEntryLocator",
    "ManualSource",
    "MaterialSource",
    "PageText",
    "PdfPageLocator",
    "Region",
    "SourceCatalog",
    "SourceContractError",
    "SourceErrorCode",
    "SourceInsufficient",
    "SourceInsufficientReason",
    "SourceLocator",
    "TextLinesLocator",
    "normalize_source_text",
    "prove_unique_pdf_page",
    "raw_file_content_hash",
    "source_locator_from_mapping",
    "validate_content_hash",
    "validate_source_locator",
]
```

- [ ] **Step 24: Run the complete focused T-02 suite**

Run:

```powershell
$env:PYTHONPATH = (Resolve-Path 'backend/src').Path
python -m pytest backend/tests/unit/domain -q
```

Expected: exit code 0 with `72 passed`.

- [ ] **Step 24B: Format the published facade under the focused green suite**

Run:

```powershell
python -m ruff format --config backend/pyproject.toml backend/src/projectb/domain/source/__init__.py backend/tests/unit/domain/test_source_exports.py
```

Expected: exit code 0; Ruff reports the two files formatted or already formatted and changes no behavior.

- [ ] **Step 24C: Re-run the complete focused suite after all refactor steps**

Run:

```powershell
$env:PYTHONPATH = (Resolve-Path 'backend/src').Path
python -m pytest backend/tests/unit/domain -q
```

Expected: exit code 0 with `72 passed`.

- [ ] **Step 25: Run Ruff on every T-02 source and test file**

Run:

```powershell
python -m ruff check --config backend/pyproject.toml backend/src/projectb/domain backend/tests/unit/domain
```

Expected: exit code 0 with `All checks passed!`.

- [ ] **Step 26: Run mypy on the published domain contract**

Run:

```powershell
$env:PYTHONPATH = (Resolve-Path 'backend/src').Path
python -m mypy --config-file backend/pyproject.toml backend/src/projectb/domain
```

Expected: exit code 0 with `Success: no issues found in 8 source files`.

- [ ] **Step 27: Run the repository's one-command verification entry**

Run:

```powershell
python scripts/test_all.py
```

Expected: exit code 0; the backend run reports the T-01 health test plus all 72 T-02 tests passing, the frontend production build passes, the project secret scan passes, and gates owned by later tasks remain explicitly reported as unavailable rather than PASS.

- [ ] **Step 28: Run the project secret scanner separately**

Run:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/scan_secrets.ps1
```

Expected: exit code 0 with no credential finding; the scanner must inspect the new tracked and untracked T-02 files without printing file contents.

- [ ] **Step 29: Validate the worker identity before review and commit**

Run:

```powershell
if ([string]::IsNullOrWhiteSpace($env:PROJECTB_AGENT_ID)) {
    throw 'PROJECTB_AGENT_ID must identify the fresh T-02 worker'
}
if ($env:PROJECTB_AGENT_ID -notmatch '^[A-Za-z0-9._-]{1,64}$') {
    throw 'PROJECTB_AGENT_ID contains unsupported characters'
}
```

Expected: exit code 0 and a non-empty stable worker identity; unset, blank, or malformed values stop before review and commit.

- [ ] **Step 30: Stage exactly the T-02 implementation paths**

Run:

```powershell
git add -- backend/src/projectb/domain/__init__.py backend/src/projectb/domain/types.py backend/src/projectb/domain/materials.py backend/src/projectb/domain/source/__init__.py backend/src/projectb/domain/source/errors.py backend/src/projectb/domain/source/hashing.py backend/src/projectb/domain/source/models.py backend/src/projectb/domain/source/proof.py backend/tests/unit/domain/test_domain_primitives.py backend/tests/unit/domain/test_source_hashing.py backend/tests/unit/domain/test_source_models.py backend/tests/unit/domain/test_source_proof.py backend/tests/unit/domain/test_source_exports.py
```

Expected: exit code 0; only the 13 literal paths in the command are added to the index.

- [ ] **Step 31: Check the staged patch for whitespace errors**

Run:

```powershell
git diff --cached --check
```

Expected: exit code 0 with no output.

- [ ] **Step 32: Verify the exact staged path set**

Run:

```powershell
$expected = @(
    'backend/src/projectb/domain/__init__.py'
    'backend/src/projectb/domain/materials.py'
    'backend/src/projectb/domain/source/__init__.py'
    'backend/src/projectb/domain/source/errors.py'
    'backend/src/projectb/domain/source/hashing.py'
    'backend/src/projectb/domain/source/models.py'
    'backend/src/projectb/domain/source/proof.py'
    'backend/src/projectb/domain/types.py'
    'backend/tests/unit/domain/test_domain_primitives.py'
    'backend/tests/unit/domain/test_source_exports.py'
    'backend/tests/unit/domain/test_source_hashing.py'
    'backend/tests/unit/domain/test_source_models.py'
    'backend/tests/unit/domain/test_source_proof.py'
)
$actual = @(git diff --cached --name-only | Sort-Object)
$gitExit = $LASTEXITCODE
if ($gitExit -ne 0) {
    throw 'git diff --cached --name-only failed'
}
$difference = @(Compare-Object -ReferenceObject $expected -DifferenceObject $actual)
if ($difference.Count -ne 0) {
    throw 'staged paths differ from the exact T-02 ownership set'
}
```

Expected: exit code 0; the index contains exactly the 13 sorted paths above and no plan, credential, private courseware, generated cache, or unrelated file.

- [ ] **Step 33: Dispatch a fresh SPEC-compliance reviewer**

The coordinator dispatches a fresh reviewer who did not implement T-02. Give that reviewer only the exact staged T-02 diff, the validated worker identity from `$env:PROJECTB_AGENT_ID`, `SPEC.md` lines 57–65, line 77, lines 182–184, AC-03, and AC-37. The reviewer reports a non-empty canonical identity; after verifying it, the coordinator records it in `$env:PROJECTB_SPEC_REVIEWER_ID`. Record the pair `worker_id` / `spec_reviewer_id` and `SPEC REVIEW: PASS` in the coordinator handoff only when every statement below is true:

1. The hash is computed from untouched bytes and every locator hash accepts only 64 lowercase hexadecimal characters without a prefix.
2. The fixed `material-limits.v1` loader rejects absent or wrong versions and every runtime override, including boolean, zero, negative, and changed positive values.
3. `SelectedFile.role`, `SelectedFile.review_state`, and `MaterialUnit.kind` require the exact enum class; `quality_flags` rejects strings and non-string members.
4. The four locator branches have no mixed or unknown-field path; PDF pages and text lines start at 1.
5. Regions use finite top-left normalized coordinates and enforce `0 <= x < 1`, `0 <= y < 1`, `0 < width <= 1-x`, `0 < height <= 1-y`.
6. Unique-page proof applies the exact normalization pipeline, accepts 32 normalized code points, rejects 31, and fails closed for zero-page, multiple-page, cross-page, and visual-only evidence.
7. Catalog validation rejects deleted/missing material, stale content hash or manual version, and invalid page/image/line references before any downstream authority write.

Expected: all seven statements have direct passing tests; any mismatch is Critical and blocks the next step. The worker may not self-approve this gate.

- [ ] **Step 34: Dispatch a different fresh quality/security/license reviewer**

The coordinator dispatches a second fresh reviewer whose identity differs from both the worker and the Step 33 reviewer. Give that reviewer the exact staged files, the validated worker identity, the SPEC reviewer identity, focused/full test output, Ruff output, mypy output, scanner output, and T-01 dependency/license baseline. The reviewer reports a non-empty canonical identity; after verifying it, the coordinator records it in `$env:PROJECTB_QUALITY_REVIEWER_ID`. Record the three identities and `QUALITY REVIEW: PASS` only when every statement below is true:

1. Public values are immutable frozen dataclasses or immutable enum/NewType values; catalog inputs are copied to tuples/frozensets.
2. Error strings contain only stable codes and never echo page text, paths, display names, IDs, hashes, student answers, or secrets.
3. Tests are deterministic and make zero network/provider calls; fixtures are synthetic strings authored in this task and contain no private courseware.
4. Production code uses only the CPython standard library; pytest remains the already-reviewed MIT test dependency, so T-02 adds no package or third-party code/asset license obligation.
5. The source package exposes one contract facade and does not duplicate normalization, hashing, or proof logic in downstream-facing modules.
6. Ruff used `backend/pyproject.toml`, mypy used the same explicit configuration, and neither check omitted a T-02 source path.

Expected: all six statements pass. A Critical security, correctness, test, or license finding returns the task to the relevant red/green step; after the fix, rerun Steps 24C–34 so both reviewers inspect the final staged patch. The worker, SPEC reviewer, and quality reviewer must remain three distinct identities.

- [ ] **Step 35: Validate all three recorded identities**

Run:

```powershell
$identities = @(
    $env:PROJECTB_AGENT_ID
    $env:PROJECTB_SPEC_REVIEWER_ID
    $env:PROJECTB_QUALITY_REVIEWER_ID
)
foreach ($identity in $identities) {
    if ([string]::IsNullOrWhiteSpace($identity)) {
        throw 'worker and reviewer identities must all be non-empty'
    }
    if ($identity -notmatch '^[A-Za-z0-9._-]{1,64}$') {
        throw 'worker or reviewer identity contains unsupported characters'
    }
}
if (($identities | Sort-Object -Unique).Count -ne 3) {
    throw 'worker, SPEC reviewer, and quality reviewer must be distinct'
}
```

Expected: exit code 0; all three canonical identities are non-empty, valid, and pairwise distinct.

- [ ] **Step 36: Recheck the reviewed staged patch**

Run:

```powershell
git diff --cached --check
```

Expected: exit code 0 with no output; this is the same staged patch accepted by both reviewers.

- [ ] **Step 37: Commit the reviewed T-02 change with the worker identity**

Run:

```powershell
git commit -m "feat(T-02): add immutable source locator proof [agent: $env:PROJECTB_AGENT_ID]"
```

Expected: exit code 0; the commit subject includes the same worker identity reviewed in Steps 33–35.

- [ ] **Step 38: Record the reviewed implementation commit hash**

Run:

```powershell
git rev-parse HEAD
```

Expected: exit code 0 with one 40-character lowercase hexadecimal commit hash. The coordinator records that hash plus the separate reviewer identities/outcomes in `PLAN.md` and `AGENT_LOG.md` only after the prerequisite atomic root-plan integration is reviewed.

**Completion standard:** The focused 72-test suite, Ruff, mypy, repository verification entry, secret scan, two independent fresh-reviewer gates, and identity-bound commit all pass from the T-02 worktree. This draft still remains unreviewed and not dispatchable until the coordinator resolves its file-layout/proof-signature differences and atomically integrates the chosen contract into formal `PLAN.md` and its ownership/status ledgers.
