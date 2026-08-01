# Domain Primitives and Source Contracts Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build immutable material primitives, strict local source locators, deterministic unique-page proof, and one provider-independent public source facade.

**Architecture:** Implement five strictly sequential dispatch units. T-02A owns common errors, opaque IDs, fixed material limits, and material primitives; T-02B1 owns only raw-byte hashing and v1 normalization; T-02B2A owns locator/catalog/mapping validation; T-02B2B is the first owner of `source/__init__.py` and publishes the reviewed contracts through the B-stage facade; T-02C adds four-argument unique-page proof plus the final facade. Every authority-bearing container and member is validated at runtime, and every public boundary returns `projectb.domain.errors.SourceContractError` with a stable code instead of leaking built-in type errors.

**Tech Stack:** CPython 3.14.6 standard library (`collections.abc`, `dataclasses`, `enum`, `hashlib`, `math`, `re`, `typing`, `unicodedata`), pytest 9.1.1, Ruff 0.15.22, and mypy 2.3.0 from the T-01 locked backend environment.

---

## Coordinator Integration Gate

Before any cold-start or implementation dispatch, the coordinator must re-read the current root `PLAN.md` `### Task Group T-02B2 (not dispatchable)` plus its T-02/T-01F3 child entries and this file from one consistent repository snapshot. Compare task IDs, dependency edges, ownership paths, the deferred-to-published facade transition, the four-argument proof signature, review scope, and ledger row, and record the observed comparison. The coordinator must not infer or claim that the root currently has a flat `domain/source.py` file, a three-argument proof, or any other historical shape; those are only compatibility risks to check. Dispatch is blocked unless that same-snapshot comparison explicitly records `T-01F3 -> T-02A -> T-02B1 -> T-02B2A -> T-02B2B -> T-02C`, with no stale fragment/hash substituted for the reviewed root entry.

Each unit uses a different fresh implementation subagent and a worktree based on the reviewed dependency commit. T-02A, T-02B1, T-02B2A, T-02B2B, and T-02C are strictly sequential: B1 starts from A's reviewed commit, B2A starts from B1, B2B starts from B2A, and C starts from B2B. After each unit, the coordinator dispatches two additional fresh reviewers with distinct identities, resolves every Critical or Important finding, records the implementation commit, and only then dispatches the next unit.

Review packets for both reviewers contain the complete `SPEC.md`, the complete formal root task for the current unit after same-snapshot integration, this complete plan, the exact staged diff, the worker identity, focused/full verification output, Ruff output, mypy output, and scanner output. The SPEC reviewer checks only the clauses listed for that unit; the second reviewer checks correctness, maintainability, security, tests, and licenses. Neither reviewer receives conversation history or may be the worker.

## Runtime and Evidence Contract

Every unit's Step 0 executes this complete block in its own fresh shell, followed immediately by that unit's exact `Initialize-DomainUnit` call. Nothing is inherited from another unit. The coordinator supplies absolute `PROJECTB_PYTHON_EXE` and `PROJECTB_POWERSHELL_EXE` paths plus `PROJECTB_AGENT_ID`, `PROJECTB_UNIT_ID`, `PROJECTB_BASE_COMMIT`, and `PROJECTB_WORKTREE_ROOT`. Git alone is resolved through `Get-Command -CommandType Application` and then treated as an absolute application leaf. Runtime probes are bounded to ten seconds and expose no child output in failure messages.

```powershell
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Invoke-CheckedNative {
    param(
        [Parameter(Mandatory)][string]$FilePath,
        [Parameter(Mandatory)][string[]]$ArgumentList
    )

    $output = @(& $FilePath @ArgumentList)
    $exitCode = $LASTEXITCODE
    if ($exitCode -ne 0) {
        throw "native command failed with exit code $exitCode"
    }
    return $output
}

function Invoke-ExpectedNativeExit {
    param(
        [Parameter(Mandatory)][string]$FilePath,
        [Parameter(Mandatory)][string[]]$ArgumentList,
        [Parameter(Mandatory)][int]$ExpectedExitCode
    )

    $output = @(& $FilePath @ArgumentList)
    $exitCode = $LASTEXITCODE
    if ($exitCode -ne $ExpectedExitCode) {
        throw "native command returned unexpected exit code $exitCode"
    }
    return $output
}

function Invoke-CheckedPython {
    param([Parameter(Mandatory)][string[]]$ArgumentList)
    Invoke-CheckedNative -FilePath $PythonExe -ArgumentList $ArgumentList
}

function Invoke-CheckedPowerShell {
    param([Parameter(Mandatory)][string[]]$ArgumentList)
    Invoke-CheckedNative -FilePath $PowerShellExe -ArgumentList $ArgumentList
}

function Invoke-BoundedNativeProbe {
    param(
        [Parameter(Mandatory)][string]$FilePath,
        [Parameter(Mandatory)][string[]]$ArgumentList,
        [ValidateRange(1, 30)][int]$TimeoutSeconds = 10
    )

    $job = Start-Job -ScriptBlock {
        param([string]$ProbeFilePath, [string[]]$ProbeArgumentList)
        $probeOutput = @(& $ProbeFilePath @ProbeArgumentList)
        [pscustomobject]@{
            ExitCode = $LASTEXITCODE
            Output = $probeOutput
        }
    } -ArgumentList $FilePath, $ArgumentList
    try {
        $completed = Wait-Job -Job $job -Timeout $TimeoutSeconds
        if ($null -eq $completed) {
            Stop-Job -Job $job -ErrorAction SilentlyContinue
            throw 'runtime probe timed out'
        }
        $result = @(Receive-Job -Job $job -ErrorAction SilentlyContinue)
        if ($result.Count -ne 1 -or $result[0].ExitCode -ne 0) {
            throw 'runtime probe failed'
        }
        return @($result[0].Output)
    }
    finally {
        Remove-Job -Job $job -Force -ErrorAction SilentlyContinue
    }
}

$GitExe = (Get-Command git -CommandType Application -ErrorAction Stop).Source
$PythonExe = $env:PROJECTB_PYTHON_EXE
$PowerShellExe = $env:PROJECTB_POWERSHELL_EXE
foreach ($pair in @(
    @('Git', $GitExe),
    @('Python', $PythonExe),
    @('PowerShell', $PowerShellExe)
)) {
    if ([string]::IsNullOrWhiteSpace($pair[1]) -or
        -not [IO.Path]::IsPathFullyQualified($pair[1]) -or
        -not (Test-Path -LiteralPath $pair[1] -PathType Leaf)) {
        throw "$($pair[0]) executable must be an absolute existing leaf"
    }
}

$pythonVersionOutput = @(Invoke-BoundedNativeProbe -FilePath $PythonExe -ArgumentList @(
    '-c', 'import platform; print(platform.python_version())'
))
if ($pythonVersionOutput.Count -ne 1 -or $pythonVersionOutput[0].Trim() -ne '3.14.6') {
    throw 'domain units require CPython 3.14.6'
}
$powerShellVersionOutput = @(Invoke-BoundedNativeProbe -FilePath $PowerShellExe -ArgumentList @(
    '-NoProfile', '-Command', '$PSVersionTable.PSVersion.ToString()'
))
if ($powerShellVersionOutput.Count -ne 1) {
    throw 'PowerShell version output must contain exactly one line'
}
$powerShellVersion = $powerShellVersionOutput[0].Trim()
$parsedPowerShellVersion = $null
if ([string]::IsNullOrWhiteSpace($powerShellVersion) -or
    -not [Version]::TryParse($powerShellVersion, [ref]$parsedPowerShellVersion)) {
    throw 'PowerShell version output is empty or malformed'
}

function Assert-ExactStagedPaths {
    param([Parameter(Mandatory)][string[]]$ExpectedPaths)

    $actual = @(
        Invoke-CheckedNative -FilePath $GitExe -ArgumentList @(
            'diff', '--cached', '--name-only'
        ) | Where-Object { $_ } | ForEach-Object { $_ -replace '\\', '/' } |
            Sort-Object
    )
    $expected = @(
        $ExpectedPaths | ForEach-Object { $_ -replace '\\', '/' } | Sort-Object
    )
    if (($actual | Sort-Object -Unique).Count -ne $actual.Count) {
        throw 'duplicate staged path detected'
    }
    $delta = @(Compare-Object -ReferenceObject $expected -DifferenceObject $actual)
    if ($actual.Count -ne $expected.Count -or $delta.Count -ne 0) {
        throw 'staged path set mismatch'
    }
}

function Get-CheckedIndexTree {
    $treeOutput = @(Invoke-CheckedNative -FilePath $GitExe -ArgumentList @(
        'write-tree'
    ))
    if ($treeOutput.Count -ne 1 -or $treeOutput[0].Trim() -notmatch '^[0-9a-f]{40}$') {
        throw 'git write-tree must return one lowercase 40-hex tree ID'
    }
    return $treeOutput[0].Trim()
}

function Initialize-DomainUnit {
    param(
        [Parameter(Mandatory)][string]$ExpectedUnitId,
        [Parameter(Mandatory)][string[]]$ExpectedPaths
    )

    foreach ($name in @(
        'PROJECTB_AGENT_ID',
        'PROJECTB_UNIT_ID',
        'PROJECTB_BASE_COMMIT',
        'PROJECTB_WORKTREE_ROOT'
    )) {
        if ([string]::IsNullOrWhiteSpace([Environment]::GetEnvironmentVariable($name))) {
            throw "$name is required"
        }
    }
    if ($env:PROJECTB_AGENT_ID -notmatch '^[A-Za-z0-9][A-Za-z0-9._-]{1,63}$') {
        throw 'PROJECTB_AGENT_ID is invalid'
    }
    if ($env:PROJECTB_UNIT_ID -ne $ExpectedUnitId) {
        throw 'wrong dispatch unit'
    }
    if ($env:PROJECTB_BASE_COMMIT -notmatch '^[0-9a-f]{40}$') {
        throw 'PROJECTB_BASE_COMMIT must be one lowercase 40-hex SHA'
    }
    if (-not [IO.Path]::IsPathFullyQualified($env:PROJECTB_WORKTREE_ROOT) -or
        -not (Test-Path -LiteralPath $env:PROJECTB_WORKTREE_ROOT -PathType Container)) {
        throw 'PROJECTB_WORKTREE_ROOT must be an absolute existing directory'
    }
    $resolvedRoot = (Resolve-Path -LiteralPath '.').Path.TrimEnd('\', '/')
    $declaredRoot = (Resolve-Path -LiteralPath $env:PROJECTB_WORKTREE_ROOT).Path.TrimEnd('\', '/')
    if (-not $resolvedRoot.Equals($declaredRoot, [StringComparison]::OrdinalIgnoreCase)) {
        throw 'current directory is not PROJECTB_WORKTREE_ROOT'
    }
    $gitRoot = @(Invoke-CheckedNative -FilePath $GitExe -ArgumentList @(
        'rev-parse', '--show-toplevel'
    ))
    if ($gitRoot.Count -ne 1 -or
        -not $gitRoot[0].Trim().Replace('/', '\').Equals(
            $resolvedRoot.Replace('/', '\'),
            [StringComparison]::OrdinalIgnoreCase
        )) {
        throw 'Git top-level does not match PROJECTB_WORKTREE_ROOT'
    }
    $head = @(Invoke-CheckedNative -FilePath $GitExe -ArgumentList @('rev-parse', 'HEAD'))
    if ($head.Count -ne 1 -or $head[0].Trim() -ne $env:PROJECTB_BASE_COMMIT) {
        throw 'worktree HEAD does not match the reviewed predecessor'
    }
    foreach ($relativePath in $ExpectedPaths) {
        if ([IO.Path]::IsPathFullyQualified($relativePath) -or
            $relativePath -match '(^|[\\/])\.\.([\\/]|$)') {
            throw 'owned path must be repository-relative and cannot traverse parents'
        }
        $candidate = [IO.Path]::GetFullPath((Join-Path $resolvedRoot $relativePath))
        $rootPrefix = $resolvedRoot + [IO.Path]::DirectorySeparatorChar
        if (-not $candidate.StartsWith($rootPrefix, [StringComparison]::OrdinalIgnoreCase)) {
            throw 'owned path escapes PROJECTB_WORKTREE_ROOT'
        }
    }
    $status = @(Invoke-CheckedNative -FilePath $GitExe -ArgumentList @(
        'status', '--porcelain=v1', '--untracked-files=all'
    ))
    if ($status.Count -ne 0) {
        throw 'unit worktree must start with a clean index and allowed scope'
    }
    $env:PYTHONPATH = (Resolve-Path -LiteralPath 'backend/src').Path
}
```

Every unit-specific Step 0 below supplies the exact dispatch ID and ownership array to this block. A path outside that array, a dirty starting index/worktree, a mismatched HEAD/base, or a wrong worktree root stops the unit before its red test. Every later native success command uses `Invoke-CheckedNative`; intentional red commands use `Invoke-ExpectedNativeExit`; every Git operation uses the absolute `$GitExe` through those wrappers.

Every unit separately runs red tests, green implementation, focused regression, refactor/format, full domain/entry verification, scanner, staged-set comparison, two fresh reviews, commit, and hash capture. Counts are not future expectations. Commit and hash capture remain separate checked commands, and hash evidence must contain exactly one lowercase 40-hex value.

### Task T-02A: Common Errors, Opaque IDs, and Material Primitives

**Goal:** Establish the immutable common domain vocabulary and fixed `material-limits.v1` contract without depending on source parsing or proof code.

**Dependencies / parallelism:** T-01F3 must be reviewed and merged. T-02A owns only the five paths below and cannot run beside edits to them. T-02B1, T-02B2A, T-02B2B, and T-02C wait for T-02A's reviewed commit.

**Files:**
- Create: `backend/src/projectb/domain/__init__.py`
- Create: `backend/src/projectb/domain/errors.py`
- Create: `backend/src/projectb/domain/types.py`
- Create: `backend/src/projectb/domain/materials.py`
- Create: `backend/tests/unit/domain/test_domain_primitives.py`

**Produced interfaces:** `SourceErrorCode`, `SourceContractError`, `SourceInsufficientReason`, `SourceInsufficient`, opaque ID NewTypes, `validate_opaque_id`, `validate_content_hash`, four exact `StrEnum` classes, fixed `MaterialLimits`, strict `material_limits_from_mapping`, immutable `SelectedFile`, and immutable `MaterialUnit`.

- [ ] **Step A0: Establish the complete T-02A runtime, base, worktree, and ownership prelude**

Execute the complete Runtime and Evidence Contract block above in this fresh T-02A shell, then run:

```powershell
Initialize-DomainUnit -ExpectedUnitId 'T-02A' -ExpectedPaths @(
    'backend/src/projectb/domain/__init__.py'
    'backend/src/projectb/domain/errors.py'
    'backend/src/projectb/domain/materials.py'
    'backend/src/projectb/domain/types.py'
    'backend/tests/unit/domain/test_domain_primitives.py'
)
```

Expected: exit code 0 only when the absolute runtimes and Git application are valid, bounded probes pass, unit/base/worktree/HEAD all match coordinator metadata, every owned path remains inside the worktree, and the starting worktree/index is clean.

- [ ] **Step A1A: Create the failing stable-error and material-enum tests**

Create `backend/tests/unit/domain/test_domain_primitives.py` with this exact first slice:

```python
from dataclasses import FrozenInstanceError
from enum import StrEnum

import pytest

from projectb.domain import errors, materials
from projectb.domain.types import (
    MaterialId,
    UnitId,
    validate_content_hash,
    validate_opaque_id,
)

HASH = "a" * 64


class ForeignRole(StrEnum):
    LECTURE = "lecture"


def test_source_contract_error_exposes_only_its_stable_code() -> None:
    error = errors.SourceContractError(errors.SourceErrorCode.INVALID_SHAPE)
    assert error.code is errors.SourceErrorCode.INVALID_SHAPE
    assert str(error) == "invalid_shape"


@pytest.mark.parametrize("invalid_code", [None, "invalid_shape", ForeignRole.LECTURE])
def test_source_contract_error_normalizes_invalid_codes_to_stable_shape(
    invalid_code: object,
) -> None:
    error = errors.SourceContractError(invalid_code)  # type: ignore[arg-type]
    assert error.code is errors.SourceErrorCode.INVALID_SHAPE
    assert str(error) == "invalid_shape"


@pytest.mark.parametrize("invalid_reason", [None, "too_short", ForeignRole.LECTURE])
def test_source_insufficient_rejects_invalid_reasons_with_stable_error(
    invalid_reason: object,
) -> None:
    with pytest.raises(errors.SourceContractError) as caught:
        errors.SourceInsufficient(invalid_reason)  # type: ignore[arg-type]
    assert caught.value.code is errors.SourceErrorCode.INVALID_SHAPE


@pytest.mark.parametrize(
    ("validator", "value"),
    [(validate_opaque_id, None), (validate_content_hash, b"a" * 64)],
)
def test_shared_scalar_validators_reject_invalid_types_as_invalid_shape(
    validator: object,
    value: object,
) -> None:
    with pytest.raises(errors.SourceContractError) as caught:
        validator(value)  # type: ignore[operator]
    assert caught.value.code is errors.SourceErrorCode.INVALID_SHAPE


def test_material_enums_match_the_confirmed_v1_contract() -> None:
    assert [item.value for item in materials.ProcessingMode] == ["L", "P", "F"]
    assert [item.value for item in materials.MaterialRole] == [
        "lecture",
        "past_paper",
        "teacher_focus",
    ]
    assert [item.value for item in materials.MaterialReviewState] == [
        "accepted",
        "needs_user_review",
    ]
    assert [item.value for item in materials.MaterialUnitKind] == [
        "pdf_page",
        "image",
        "text_lines",
        "manual_entry",
    ]
```

- [ ] **Step A1B: Append the failing fixed material-limits tests**

Append exactly to `backend/tests/unit/domain/test_domain_primitives.py`:

```python


def test_material_limits_are_the_fixed_v1_values() -> None:
    limits = materials.MaterialLimits()
    assert limits.version == materials.MATERIAL_LIMITS_VERSION == "material-limits.v1"
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


@pytest.mark.parametrize(
    "payload",
    [
        None,
        True,
        "material-limits.v1",
        [],
        {},
        {"version": "material-limits.v2"},
        {"version": "material-limits.v1", "pdf_max_bytes": True},
        {"version": "material-limits.v1", "pdf_max_bytes": 0},
        {"version": "material-limits.v1", "pdf_max_bytes": -1},
        {"version": "material-limits.v1", "pdf_max_bytes": 256 * 1024 * 1024},
        {"version": "material-limits.v1", "pdf_max_bytes": (256 * 1024 * 1024) + 1},
    ],
)
def test_material_limits_reject_non_mapping_version_errors_and_all_overrides(
    payload: object,
) -> None:
    with pytest.raises(errors.SourceContractError) as caught:
        materials.material_limits_from_mapping(payload)
    assert caught.value.code is errors.SourceErrorCode.INVALID_MATERIAL_LIMITS
```

- [ ] **Step A2: Run the first T-02A slice and capture red evidence**

Run:

```powershell
$env:PYTHONPATH = (Resolve-Path 'backend/src' -ErrorAction SilentlyContinue).Path
Invoke-ExpectedNativeExit -FilePath $PythonExe -ExpectedExitCode 2 -ArgumentList @(
    '-m', 'pytest', '-c', 'backend/pyproject.toml',
    'backend/tests/unit/domain/test_domain_primitives.py', '-q'
)
```

Expected: exit code 2 with a collection error because `projectb.domain` does not exist; no test passes.

- [ ] **Step A3: Create the domain package marker**

Create `backend/src/projectb/domain/__init__.py` with exactly:

```python
"""Provider-independent ProjectB domain contracts."""
```

- [ ] **Step A4: Create the common stable error contract**

Create `backend/src/projectb/domain/errors.py` with exactly:

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
        code_value: object = code
        if not isinstance(code_value, SourceErrorCode):
            code_value = SourceErrorCode.INVALID_SHAPE
        self.code: SourceErrorCode = code_value
        super().__init__(code_value.value)


class SourceInsufficientReason(StrEnum):
    TOO_SHORT = "too_short"
    NO_MATCH = "no_match"
    AMBIGUOUS = "ambiguous"


@dataclass(frozen=True, slots=True)
class SourceInsufficient:
    reason: SourceInsufficientReason

    def __post_init__(self) -> None:
        reason_value: object = self.reason
        if not isinstance(reason_value, SourceInsufficientReason):
            raise SourceContractError(SourceErrorCode.INVALID_SHAPE)


__all__ = [
    "SourceContractError",
    "SourceErrorCode",
    "SourceInsufficient",
    "SourceInsufficientReason",
]
```

- [ ] **Step A5: Create opaque IDs and shared scalar validators**

Create `backend/src/projectb/domain/types.py` with exactly:

```python
import re
from typing import NewType

from projectb.domain.errors import SourceContractError, SourceErrorCode

CourseId = NewType("CourseId", str)
EntryId = NewType("EntryId", str)
ImageId = NewType("ImageId", str)
MaterialId = NewType("MaterialId", str)
UnitId = NewType("UnitId", str)

_CONTENT_HASH = re.compile(r"[0-9a-f]{64}\Z")


def validate_opaque_id(value: object) -> str:
    if not isinstance(value, str):
        raise SourceContractError(SourceErrorCode.INVALID_SHAPE)
    if not value or value.strip() != value:
        raise SourceContractError(SourceErrorCode.INVALID_ID)
    return value


def validate_content_hash(value: object) -> str:
    if not isinstance(value, str):
        raise SourceContractError(SourceErrorCode.INVALID_SHAPE)
    if _CONTENT_HASH.fullmatch(value) is None:
        raise SourceContractError(SourceErrorCode.INVALID_CONTENT_HASH)
    return value


__all__ = [
    "CourseId",
    "EntryId",
    "ImageId",
    "MaterialId",
    "UnitId",
    "validate_content_hash",
    "validate_opaque_id",
]
```

- [ ] **Step A6A: Create fixed material enums and immutable v1 limit values**

Create `backend/src/projectb/domain/materials.py` with this exact first slice:

```python
from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import StrEnum
from typing import cast

from projectb.domain.errors import SourceContractError, SourceErrorCode
from projectb.domain.types import (
    MaterialId,
    UnitId,
    validate_content_hash,
    validate_opaque_id,
)

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
```

- [ ] **Step A6B: Append the strict v1 loader and shared text validator**

Append exactly to `backend/src/projectb/domain/materials.py`:

```python


def material_limits_from_mapping(payload: object) -> MaterialLimits:
    if not isinstance(payload, Mapping):
        raise SourceContractError(SourceErrorCode.INVALID_MATERIAL_LIMITS)
    mapping = cast(Mapping[object, object], payload)
    if set(mapping) != {"version"}:
        raise SourceContractError(SourceErrorCode.INVALID_MATERIAL_LIMITS)
    if mapping.get("version") != MATERIAL_LIMITS_VERSION:
        raise SourceContractError(SourceErrorCode.INVALID_MATERIAL_LIMITS)
    return MaterialLimits()


def _validate_text(value: object) -> str:
    if not isinstance(value, str) or not value or value.strip() != value:
        raise SourceContractError(SourceErrorCode.INVALID_SHAPE)
    return value
```

- [ ] **Step A7: Run the fixed error, enum, and limits slice green**

Run:

```powershell
$env:PYTHONPATH = (Resolve-Path 'backend/src').Path
Invoke-CheckedPython -ArgumentList @('-m', 'pytest', '-c', 'backend/pyproject.toml', 'backend/tests/unit/domain/test_domain_primitives.py', '-q')
```

Expected: exit code 0; the stable-error, enum, and fixed-limit behavior assertions pass. Record only the observed output from this run.

- [ ] **Step A8: Append the failing SelectedFile tests to the primitives test file**

Append exactly to `backend/tests/unit/domain/test_domain_primitives.py`:

```python


def test_selected_file_is_immutable_and_contains_no_local_path() -> None:
    selected = materials.SelectedFile(
        material_id=MaterialId("material-1"),
        display_name="lecture.pdf",
        role=materials.MaterialRole.LECTURE,
        content_hash=HASH,
        size_bytes=128,
        review_state=materials.MaterialReviewState.ACCEPTED,
    )
    assert not hasattr(selected, "path")
    with pytest.raises(FrozenInstanceError):
        selected.size_bytes = 256  # type: ignore[misc]


@pytest.mark.parametrize(
    ("field", "value", "code"),
    [
        ("material_id", MaterialId(""), errors.SourceErrorCode.INVALID_ID),
        ("display_name", "", errors.SourceErrorCode.INVALID_SHAPE),
        ("role", "lecture", errors.SourceErrorCode.INVALID_SHAPE),
        ("role", ForeignRole.LECTURE, errors.SourceErrorCode.INVALID_SHAPE),
        ("content_hash", "A" * 64, errors.SourceErrorCode.INVALID_CONTENT_HASH),
        ("size_bytes", -1, errors.SourceErrorCode.INVALID_SHAPE),
        ("size_bytes", True, errors.SourceErrorCode.INVALID_SHAPE),
        ("review_state", "accepted", errors.SourceErrorCode.INVALID_SHAPE),
        (
            "review_state",
            ForeignRole.LECTURE,
            errors.SourceErrorCode.INVALID_SHAPE,
        ),
    ],
)
def test_selected_file_rejects_invalid_or_foreign_authority_values(
    field: str,
    value: object,
    code: errors.SourceErrorCode,
) -> None:
    values: dict[str, object] = {
        "material_id": MaterialId("material-1"),
        "display_name": "lecture.pdf",
        "role": materials.MaterialRole.LECTURE,
        "content_hash": HASH,
        "size_bytes": 128,
        "review_state": materials.MaterialReviewState.ACCEPTED,
    }
    values[field] = value
    with pytest.raises(errors.SourceContractError) as caught:
        materials.SelectedFile(**values)
    assert caught.value.code is code
```

- [ ] **Step A9: Run the SelectedFile slice and capture red evidence**

Run:

```powershell
$env:PYTHONPATH = (Resolve-Path 'backend/src').Path
Invoke-ExpectedNativeExit -FilePath $PythonExe -ExpectedExitCode 1 -ArgumentList @(
    '-m', 'pytest', '-c', 'backend/pyproject.toml',
    'backend/tests/unit/domain/test_domain_primitives.py', '-q'
)
```

Expected: exit code 1 because `projectb.domain.materials.SelectedFile` is absent; the already implemented stable-error, enum, and limit assertions remain green. Record the observed failure set instead of a planned count.

- [ ] **Step A10: Append the strict immutable SelectedFile implementation**

Append exactly to `backend/src/projectb/domain/materials.py`:

```python


@dataclass(frozen=True, slots=True)
class SelectedFile:
    material_id: MaterialId
    display_name: str
    role: MaterialRole
    content_hash: str
    size_bytes: int
    review_state: MaterialReviewState

    def __post_init__(self) -> None:
        material_id_value: object = self.material_id
        display_name_value: object = self.display_name
        role_value: object = self.role
        content_hash_value: object = self.content_hash
        size_bytes_value: object = self.size_bytes
        review_state_value: object = self.review_state
        validate_opaque_id(material_id_value)
        _validate_text(display_name_value)
        if not isinstance(role_value, MaterialRole):
            raise SourceContractError(SourceErrorCode.INVALID_SHAPE)
        if not isinstance(review_state_value, MaterialReviewState):
            raise SourceContractError(SourceErrorCode.INVALID_SHAPE)
        validate_content_hash(content_hash_value)
        if type(size_bytes_value) is not int or size_bytes_value < 0:
            raise SourceContractError(SourceErrorCode.INVALID_SHAPE)
```

- [ ] **Step A11: Run the SelectedFile slice green**

Run:

```powershell
$env:PYTHONPATH = (Resolve-Path 'backend/src').Path
Invoke-CheckedPython -ArgumentList @('-m', 'pytest', '-c', 'backend/pyproject.toml', 'backend/tests/unit/domain/test_domain_primitives.py', '-q')
```

Expected: exit code 0; the SelectedFile immutability and invalid-authority assertions pass together with the earlier slice.

- [ ] **Step A12A: Append the failing valid immutable MaterialUnit case**

Append exactly to `backend/tests/unit/domain/test_domain_primitives.py`:

```python


def test_material_unit_is_immutable_and_uses_one_based_ordinals() -> None:
    unit = materials.MaterialUnit(
        unit_id=UnitId("unit-1"),
        material_id=MaterialId("material-1"),
        content_hash=HASH,
        kind=materials.MaterialUnitKind.PDF_PAGE,
        ordinal=1,
        parser_version="parser-v1",
        quality_flags=frozenset({"text_present"}),
    )
    assert unit.ordinal == 1
    with pytest.raises(FrozenInstanceError):
        unit.ordinal = 2  # type: ignore[misc]
```

- [ ] **Step A12B: Append the failing MaterialUnit runtime-boundary matrix**

Append exactly to `backend/tests/unit/domain/test_domain_primitives.py`:

```python


@pytest.mark.parametrize(
    ("field", "value", "code"),
    [
        ("unit_id", UnitId(""), errors.SourceErrorCode.INVALID_ID),
        ("material_id", MaterialId(""), errors.SourceErrorCode.INVALID_ID),
        ("content_hash", "A" * 64, errors.SourceErrorCode.INVALID_CONTENT_HASH),
        ("kind", "pdf_page", errors.SourceErrorCode.INVALID_SHAPE),
        ("kind", ForeignRole.LECTURE, errors.SourceErrorCode.INVALID_SHAPE),
        ("ordinal", 0, errors.SourceErrorCode.INVALID_PAGE),
        ("ordinal", True, errors.SourceErrorCode.INVALID_PAGE),
        ("parser_version", "", errors.SourceErrorCode.INVALID_SHAPE),
        ("quality_flags", "text_present", errors.SourceErrorCode.INVALID_SHAPE),
        ("quality_flags", ["text_present"], errors.SourceErrorCode.INVALID_SHAPE),
        ("quality_flags", frozenset({1}), errors.SourceErrorCode.INVALID_SHAPE),
        ("quality_flags", frozenset({""}), errors.SourceErrorCode.INVALID_SHAPE),
        (
            "quality_flags",
            frozenset({" text_present"}),
            errors.SourceErrorCode.INVALID_SHAPE,
        ),
    ],
)
def test_material_unit_rejects_invalid_containers_members_and_enums(
    field: str,
    value: object,
    code: errors.SourceErrorCode,
) -> None:
    values: dict[str, object] = {
        "unit_id": UnitId("unit-1"),
        "material_id": MaterialId("material-1"),
        "content_hash": HASH,
        "kind": materials.MaterialUnitKind.PDF_PAGE,
        "ordinal": 1,
        "parser_version": "parser-v1",
        "quality_flags": frozenset({"text_present"}),
    }
    values[field] = value
    with pytest.raises(errors.SourceContractError) as caught:
        materials.MaterialUnit(**values)
    assert caught.value.code is code
```

- [ ] **Step A13: Run the MaterialUnit slice and capture red evidence**

Run:

```powershell
$env:PYTHONPATH = (Resolve-Path 'backend/src').Path
Invoke-ExpectedNativeExit -FilePath $PythonExe -ExpectedExitCode 1 -ArgumentList @(
    '-m', 'pytest', '-c', 'backend/pyproject.toml',
    'backend/tests/unit/domain/test_domain_primitives.py', '-q'
)
```

Expected: exit code 1 because `projectb.domain.materials.MaterialUnit` is absent; all earlier behavior remains green. Record the observed failure set instead of a planned count.

- [ ] **Step A14A: Append the strict immutable MaterialUnit implementation**

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
    quality_flags: frozenset[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        unit_id_value: object = self.unit_id
        material_id_value: object = self.material_id
        content_hash_value: object = self.content_hash
        kind_value: object = self.kind
        ordinal_value: object = self.ordinal
        parser_version_value: object = self.parser_version
        quality_flags_value: object = self.quality_flags
        validate_opaque_id(unit_id_value)
        validate_opaque_id(material_id_value)
        validate_content_hash(content_hash_value)
        if not isinstance(kind_value, MaterialUnitKind):
            raise SourceContractError(SourceErrorCode.INVALID_SHAPE)
        if type(ordinal_value) is not int or ordinal_value < 1:
            raise SourceContractError(SourceErrorCode.INVALID_PAGE)
        _validate_text(parser_version_value)
        if not isinstance(quality_flags_value, frozenset):
            raise SourceContractError(SourceErrorCode.INVALID_SHAPE)
        quality_flags = cast(frozenset[object], quality_flags_value)
        if any(
            not isinstance(flag, str) or not flag or flag.strip() != flag
            for flag in quality_flags
        ):
            raise SourceContractError(SourceErrorCode.INVALID_SHAPE)
```

- [ ] **Step A14B: Append the material module export list**

Append exactly to `backend/src/projectb/domain/materials.py`:

```python


__all__ = [
    "MATERIAL_LIMITS_VERSION",
    "MaterialLimits",
    "MaterialReviewState",
    "MaterialRole",
    "MaterialUnit",
    "MaterialUnitKind",
    "ProcessingMode",
    "SelectedFile",
    "material_limits_from_mapping",
]
```

- [ ] **Step A15: Run all T-02A tests green**

Run:

```powershell
$env:PYTHONPATH = (Resolve-Path 'backend/src').Path
Invoke-CheckedPython -ArgumentList @('-m', 'pytest', '-c', 'backend/pyproject.toml', 'backend/tests/unit/domain/test_domain_primitives.py', '-q')
```

Expected: exit code 0; every primitive behavior assertion in the focused file passes.

- [ ] **Step A16: Format only the T-02A files under green tests**

Run:

```powershell
Invoke-CheckedPython -ArgumentList @('-m', 'ruff', 'format', '--config', 'backend/pyproject.toml', 'backend/src/projectb/domain/__init__.py', 'backend/src/projectb/domain/errors.py', 'backend/src/projectb/domain/types.py', 'backend/src/projectb/domain/materials.py', 'backend/tests/unit/domain/test_domain_primitives.py')
```

Expected: exit code 0; Ruff reports all five files formatted or already formatted and changes no behavior.

- [ ] **Step A17: Re-run T-02A tests after refactoring**

Run:

```powershell
$env:PYTHONPATH = (Resolve-Path 'backend/src').Path
Invoke-CheckedPython -ArgumentList @('-m', 'pytest', '-c', 'backend/pyproject.toml', 'backend/tests/unit/domain/test_domain_primitives.py', '-q')
```

Expected: exit code 0; formatting changed no tested behavior.

- [ ] **Step A18: Run Ruff with the locked backend configuration**

Run:

```powershell
Invoke-CheckedPython -ArgumentList @('-m', 'ruff', 'check', '--config', 'backend/pyproject.toml', 'backend/src/projectb/domain/__init__.py', 'backend/src/projectb/domain/errors.py', 'backend/src/projectb/domain/types.py', 'backend/src/projectb/domain/materials.py', 'backend/tests/unit/domain/test_domain_primitives.py')
```

Expected: exit code 0 with `All checks passed!`.

- [ ] **Step A19: Run mypy with the locked backend configuration**

Run:

```powershell
$env:PYTHONPATH = (Resolve-Path 'backend/src').Path
Invoke-CheckedPython -ArgumentList @('-m', 'mypy', '--config-file', 'backend/pyproject.toml', 'backend/src/projectb/domain/errors.py', 'backend/src/projectb/domain/types.py', 'backend/src/projectb/domain/materials.py')
```

Expected: exit code 0 with no issues in the three checked source files.

- [ ] **Step A20: Run the repository one-command verification entry**

Run:

```powershell
Invoke-CheckedPython -ArgumentList @('scripts/test_all.py')
```

Expected: exit code 0; the canonical registry executes every active gate and reports unopened later-owner gates as unavailable rather than PASS. Record the observed gate summary.

- [ ] **Step A21: Run the project secret scanner separately**

Run:

```powershell
Invoke-CheckedPowerShell -ArgumentList @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', 'scripts/scan_secrets.ps1', '-PythonExe', $PythonExe)
```

Expected: exit code 0 with no credential finding and no file-content disclosure.

- [ ] **Step A22: Validate the fresh T-02A worker identity**

Run:

```powershell
if ([string]::IsNullOrWhiteSpace($env:PROJECTB_AGENT_ID)) {
    throw 'PROJECTB_AGENT_ID must identify the fresh T-02A worker'
}
if ($env:PROJECTB_AGENT_ID -notmatch '^[A-Za-z0-9][A-Za-z0-9._-]{1,63}$') {
    throw 'PROJECTB_AGENT_ID contains unsupported characters'
}
```

Expected: exit code 0; unset, blank, or malformed identities stop before staging and review.

- [ ] **Step A23: Stage exactly the T-02A ownership set**

Run:

```powershell
Invoke-CheckedNative -FilePath $GitExe -ArgumentList @(
    'add', '--',
    'backend/src/projectb/domain/__init__.py',
    'backend/src/projectb/domain/errors.py',
    'backend/src/projectb/domain/types.py',
    'backend/src/projectb/domain/materials.py',
    'backend/tests/unit/domain/test_domain_primitives.py'
)
if ($LASTEXITCODE -ne 0) {
    throw 'T-02A git add failed'
}
```

Expected: exit code 0; only the five literal T-02A paths are added to the index.

- [ ] **Step A24: Check the staged T-02A patch**

Run:

```powershell
Invoke-CheckedNative -FilePath $GitExe -ArgumentList @('diff', '--cached', '--check')
if ($LASTEXITCODE -ne 0) {
    throw 'T-02A staged diff check failed'
}
```

Expected: exit code 0 with no output.

- [ ] **Step A25: Assert the exact staged T-02A path set**

Run:

```powershell
Assert-ExactStagedPaths -ExpectedPaths @(
    'backend/src/projectb/domain/__init__.py'
    'backend/src/projectb/domain/errors.py'
    'backend/src/projectb/domain/materials.py'
    'backend/src/projectb/domain/types.py'
    'backend/tests/unit/domain/test_domain_primitives.py'
)
Invoke-CheckedPowerShell -ArgumentList @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', 'scripts/scan_secrets.ps1', '-PythonExe', $PythonExe, '--staged')
$env:PROJECTB_REVIEWED_TREE = Get-CheckedIndexTree
$env:PROJECTB_REVIEWED_TREE
```

Expected: exit code 0 and exactly one lowercase 40-hex index tree ID. A missing, extra, renamed, or unstaged path throws before tree capture and stops review.

- [ ] **Step A26: Request the fresh T-02A SPEC review**

The coordinator gives a fresh non-worker reviewer the complete packet defined above, requires the review record to state `REVIEWED TREE: $env:PROJECTB_REVIEWED_TREE`, and records the reviewer's canonical identity in `$env:PROJECTB_SPEC_REVIEWER_ID`. Match the root T-02A scope exactly: review SPEC §3 M1 plus the common-contract portions of AC-01, AC-03, AC-12, and AC-15: role vocabulary, fixed v1 input-limit values, raw-content-hash shape prerequisite, and the data-model immutability needed by `Material`/`MaterialUnit`. These are data contracts consumed by later workflows; this unit does not claim end-to-end completion of those acceptance criteria. PASS requires fixed `material-limits.v1`, rejection of non-mappings and every v1 override, exact `StrEnum` membership, strict enum runtime identity, immutable records, member-validated `quality_flags`, and stable non-sensitive errors for malformed error codes and insufficient reasons.

Expected: `SPEC REVIEW: PASS` explicitly bound to the captured tree ID, with no unresolved Critical or Important finding and a non-empty reviewer identity distinct from `$env:PROJECTB_AGENT_ID`. Any edit invalidates both reviews and repeats Steps A23-A27, including a new tree capture.

- [ ] **Step A27: Request the different fresh T-02A quality review**

The coordinator gives the complete packet and the exact `REVIEWED TREE: $env:PROJECTB_REVIEWED_TREE` binding to a second fresh reviewer and records that reviewer's canonical identity in `$env:PROJECTB_QUALITY_REVIEWER_ID`. This reviewer must differ from the worker and SPEC reviewer and checks runtime container/member validation, bool-vs-int handling, frozen dataclasses, B010/UP040 exposure, deterministic tests, standard-library-only production code, error redaction, test quality, and dependency/license impact.

Expected: `QUALITY REVIEW: PASS` explicitly bound to the same captured tree ID. Any finding or edit invalidates both reviews and repeats Steps A23-A27 with a newly captured tree.

- [ ] **Step A28: Validate the three T-02A identities are non-empty and distinct**

Run:

```powershell
$identities = @(
    $env:PROJECTB_AGENT_ID
    $env:PROJECTB_SPEC_REVIEWER_ID
    $env:PROJECTB_QUALITY_REVIEWER_ID
)
foreach ($identity in $identities) {
    if ([string]::IsNullOrWhiteSpace($identity)) {
        throw 'T-02A worker and reviewer identities must all be non-empty'
    }
    if ($identity -notmatch '^[A-Za-z0-9][A-Za-z0-9._-]{1,63}$') {
        throw 'T-02A worker or reviewer identity contains unsupported characters'
    }
}
if (($identities | Sort-Object -Unique).Count -ne 3) {
    throw 'T-02A worker, SPEC reviewer, and quality reviewer must be distinct'
}
```

Expected: exit code 0 with three valid pairwise-distinct identities.

- [ ] **Step A29: Recheck the reviewed staged patch**

Run:

```powershell
Invoke-CheckedNative -FilePath $GitExe -ArgumentList @('diff', '--cached', '--check')
if ($LASTEXITCODE -ne 0) {
    throw 'T-02A reviewed staged diff check failed'
}
Assert-ExactStagedPaths -ExpectedPaths @(
    'backend/src/projectb/domain/__init__.py'
    'backend/src/projectb/domain/errors.py'
    'backend/src/projectb/domain/materials.py'
    'backend/src/projectb/domain/types.py'
    'backend/tests/unit/domain/test_domain_primitives.py'
)
Invoke-CheckedPowerShell -ArgumentList @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', 'scripts/scan_secrets.ps1', '-PythonExe', $PythonExe, '--staged')
$currentTree = Get-CheckedIndexTree
if ($env:PROJECTB_REVIEWED_TREE -notmatch '^[0-9a-f]{40}$' -or
    $currentTree -ne $env:PROJECTB_REVIEWED_TREE) {
    throw 'T-02A index tree changed after review; both reviews are invalid'
}
```

Expected: exit code 0 only when the immediately pre-commit index tree exactly equals the tree ID named by both reviewers.

- [ ] **Step A30: Commit T-02A with the validated worker identity**

Run:

```powershell
Invoke-CheckedNative -FilePath $GitExe -ArgumentList @(
    'commit', '-m',
    "feat(T-02A): add immutable material primitives [agent: $env:PROJECTB_AGENT_ID]"
)
if ($LASTEXITCODE -ne 0) {
    throw 'T-02A commit failed'
}
$committedTree = @(Invoke-CheckedNative -FilePath $GitExe -ArgumentList @(
    'rev-parse', 'HEAD^{tree}'
))
if ($committedTree.Count -ne 1 -or
    $committedTree[0].Trim() -ne $env:PROJECTB_REVIEWED_TREE) {
    throw 'T-02A committed tree differs from the reviewed tree'
}
```

Expected: exit code 0 and a `feat(T-02A)` commit subject containing the reviewed worker identity.

- [ ] **Step A31: Capture the T-02A commit hash**

Run:

```powershell
$commitHash = @(Invoke-CheckedNative -FilePath $GitExe -ArgumentList @(
    'rev-parse', 'HEAD'
))
if ($LASTEXITCODE -ne 0) {
    throw 'T-02A hash capture failed'
}
if ($commitHash.Count -ne 1 -or $commitHash[0] -notmatch '^[0-9a-f]{40}$') {
    throw 'T-02A hash must be one lowercase 40-character hexadecimal value'
}
$commitHash[0]
```

Expected: exit code 0 with one 40-character lowercase hexadecimal commit hash. The coordinator records this hash and both reviewer identities/outcomes before creating the T-02B1 worktree from it.

**T-02A completion standard:** The fresh focused run exits 0 with every declared behavior assertion, Ruff/mypy/full-entry/scanner exit 0, two independent fresh reviewers report PASS, the automatic five-path staged-set assertion exits 0, and the identity-bound commit/hash is recorded. No T-02B1 work begins before that evidence is recorded.

### Task T-02B1: Define Raw Hashing and Source-text Normalization

**Goal:** Establish only the raw-file identity and deterministic text-normalization primitives, including stable invalid-shape errors, while leaving the public source facade absent for T-02B2B.

**Dependencies / parallelism:** Start a new worktree from the reviewed T-02A commit. T-02B1 owns only the two paths below. T-02B2A starts only from the reviewed T-02B1 commit and is the first task allowed to add locator/catalog modules; T-02B2B alone creates the facade afterward.

**Files:**
- Create: `backend/src/projectb/domain/source/hashing.py`
- Create: `backend/tests/unit/domain/test_source_hashing.py`

**Produced interfaces:** `raw_file_content_hash(raw_bytes: bytes) -> str` and `normalize_source_text(value: str) -> str`, importable only from `projectb.domain.source.hashing` until T-02B2B creates the explicit package facade. The test consumes T-02A's `validate_content_hash` directly from `projectb.domain.types`.

- [ ] **Step B1-0: Establish the complete T-02B1 runtime, base, worktree, and ownership prelude**

Execute the complete Runtime and Evidence Contract block above in this fresh T-02B1 shell, then run:

```powershell
Initialize-DomainUnit -ExpectedUnitId 'T-02B1' -ExpectedPaths @(
    'backend/src/projectb/domain/source/hashing.py'
    'backend/tests/unit/domain/test_source_hashing.py'
)
```

Expected: exit code 0 only for the clean T-02B1 worktree at the reviewed T-02A base with the exact two-path ownership scope.

- [ ] **Step B1-1: Create the failing raw-hash and normalization tests**

Create `backend/tests/unit/domain/test_source_hashing.py` with exactly:

```python
import pytest

from projectb.domain.errors import SourceContractError, SourceErrorCode
from projectb.domain.source.hashing import (
    normalize_source_text,
    raw_file_content_hash,
)
from projectb.domain.types import validate_content_hash


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


@pytest.mark.parametrize(
    "value",
    [None, bytearray(b"abc"), memoryview(b"abc"), "abc", True],
)
def test_raw_file_content_hash_rejects_invalid_runtime_types(value: object) -> None:
    with pytest.raises(SourceContractError) as caught:
        raw_file_content_hash(value)
    assert caught.value.code is SourceErrorCode.INVALID_SHAPE


@pytest.mark.parametrize("value", [None, b"abc", 1, True])
def test_normalize_source_text_rejects_invalid_runtime_types(value: object) -> None:
    with pytest.raises(SourceContractError) as caught:
        normalize_source_text(value)
    assert caught.value.code is SourceErrorCode.INVALID_SHAPE
```

- [ ] **Step B1-2: Run the hashing slice and capture red evidence**

Run:

```powershell
$env:PYTHONPATH = (Resolve-Path 'backend/src').Path
Invoke-ExpectedNativeExit -FilePath $PythonExe -ExpectedExitCode 2 -ArgumentList @(
    '-m', 'pytest', '-c', 'backend/pyproject.toml',
    'backend/tests/unit/domain/test_source_hashing.py', '-q'
)
```

Expected: exit code 2 with a collection error because `projectb.domain.source.hashing` does not exist; no test passes.

- [ ] **Step B1-3: Implement raw-byte hashing and v1 text normalization**

Create `backend/src/projectb/domain/source/hashing.py` with exactly:

```python
import hashlib
import unicodedata

from projectb.domain.errors import SourceContractError, SourceErrorCode
from projectb.domain.types import validate_content_hash


def raw_file_content_hash(raw_bytes: bytes) -> str:
    raw_value: object = raw_bytes
    if not isinstance(raw_value, bytes):
        raise SourceContractError(SourceErrorCode.INVALID_SHAPE)
    return hashlib.sha256(raw_value).hexdigest()


def normalize_source_text(value: str) -> str:
    text_value: object = value
    if not isinstance(text_value, str):
        raise SourceContractError(SourceErrorCode.INVALID_SHAPE)
    normalized = unicodedata.normalize("NFKC", text_value)
    normalized = normalized.replace("\r\n", "\n").replace("\u00ad", "")
    return " ".join(normalized.split())


__all__ = [
    "normalize_source_text",
    "raw_file_content_hash",
    "validate_content_hash",
]
```

- [ ] **Step B1-4: Run the hashing slice green**

Run:

```powershell
$env:PYTHONPATH = (Resolve-Path 'backend/src').Path
Invoke-CheckedPython -ArgumentList @('-m', 'pytest', '-c', 'backend/pyproject.toml', 'backend/tests/unit/domain/test_source_hashing.py', '-q')
```

Expected: exit code 0; known-byte, normalization, invalid-type, and canonical-hash assertions all pass. Record the observed output.

- [ ] **Step B1-5: Format the B1 files under green tests**

Run:

```powershell
Invoke-CheckedPython -ArgumentList @('-m', 'ruff', 'format', '--config', 'backend/pyproject.toml', 'backend/src/projectb/domain/source/hashing.py', 'backend/tests/unit/domain/test_source_hashing.py')
```

Expected: exit code 0; only the two B1 paths are formatted and behavior is unchanged.

- [ ] **Step B1-6: Re-run B1 focused and full-domain verification**

Run:

```powershell
$env:PYTHONPATH = (Resolve-Path 'backend/src').Path
Invoke-CheckedPython -ArgumentList @('-m', 'pytest', '-c', 'backend/pyproject.toml', 'backend/tests/unit/domain/test_source_hashing.py', '-q')
Invoke-CheckedPython -ArgumentList @('-m', 'pytest', '-c', 'backend/pyproject.toml', 'backend/tests/unit/domain', '-q')
Invoke-CheckedPython -ArgumentList @('-m', 'ruff', 'check', '--config', 'backend/pyproject.toml', 'backend/src/projectb/domain/source/hashing.py', 'backend/tests/unit/domain/test_source_hashing.py')
Invoke-CheckedPython -ArgumentList @('-m', 'mypy', '--config-file', 'backend/pyproject.toml', 'backend/src/projectb/domain/source/hashing.py')
Invoke-CheckedPython -ArgumentList @('scripts/test_all.py')
```

Expected: every command exits 0; assertions, configured lint/type checks, and the canonical entry pass. Record observed test and gate summaries without converting them into fixed future counts.

- [ ] **Step B1-7: Run the project scanner separately**

Run:

```powershell
Invoke-CheckedPowerShell -ArgumentList @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', 'scripts/scan_secrets.ps1', '-PythonExe', $PythonExe)
```

Expected: exit code 0 with no credential finding and no file-content disclosure.

- [ ] **Step B1-8: Validate identity, stage, and assert the exact B1 path set**

Run:

```powershell
if ([string]::IsNullOrWhiteSpace($env:PROJECTB_AGENT_ID)) {
    throw 'PROJECTB_AGENT_ID must identify the fresh T-02B1 worker'
}
if ($env:PROJECTB_AGENT_ID -notmatch '^[A-Za-z0-9][A-Za-z0-9._-]{1,63}$') {
    throw 'PROJECTB_AGENT_ID contains unsupported characters'
}
Invoke-CheckedNative -FilePath $GitExe -ArgumentList @(
    'add', '--',
    'backend/src/projectb/domain/source/hashing.py',
    'backend/tests/unit/domain/test_source_hashing.py'
)
if ($LASTEXITCODE -ne 0) {
    throw 'git add failed'
}
Assert-ExactStagedPaths -ExpectedPaths @(
    'backend/src/projectb/domain/source/hashing.py'
    'backend/tests/unit/domain/test_source_hashing.py'
)
Invoke-CheckedPowerShell -ArgumentList @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', 'scripts/scan_secrets.ps1', '-PythonExe', $PythonExe, '--staged')
$env:PROJECTB_REVIEWED_TREE = Get-CheckedIndexTree
$env:PROJECTB_REVIEWED_TREE
```

Expected: exit code 0 and one lowercase 40-hex index tree ID; any ownership mismatch stops before review.

- [ ] **Step B1-9: Check the staged B1 patch**

Run:

```powershell
Invoke-CheckedNative -FilePath $GitExe -ArgumentList @('diff', '--cached', '--check')
if ($LASTEXITCODE -ne 0) {
    throw 'staged diff check failed'
}
```

Expected: exit code 0 with no output.

- [ ] **Step B1-10: Request the fresh T-02B1 SPEC review**

The coordinator gives a fresh non-worker reviewer the complete same-snapshot packet, requires `REVIEWED TREE: $env:PROJECTB_REVIEWED_TREE` in the review record, and records the canonical identity in `$env:PROJECTB_SPEC_REVIEWER_ID`. Match the root T-02B1 scope exactly: check the raw-identity/normalization portions of AC-03 and AC-37 against SPEC §3 M1 raw-file content-hash identity and SPEC §3 X2 mode-F normalization rule 4. This unit supports those prerequisites and does not claim locator matching, source viewing, or end-to-end completion of either acceptance criterion.

Expected: `SPEC REVIEW: PASS` bound to the captured tree ID. Any edit invalidates both reviews and repeats Steps B1-8 through B1-11 with a new tree.

- [ ] **Step B1-11: Request the different fresh T-02B1 quality review**

The coordinator gives the packet with the exact `REVIEWED TREE: $env:PROJECTB_REVIEWED_TREE` binding to a second fresh reviewer and records the canonical identity in `$env:PROJECTB_QUALITY_REVIEWER_ID`. This reviewer checks invalid-type red tests, `SourceContractError(INVALID_SHAPE)`, byte/text separation, deterministic Unicode handling, standard-library-only code, absence of a prematurely owned facade, redaction, test quality, and dependency/license impact.

Expected: `QUALITY REVIEW: PASS` bound to the same captured tree ID. Any finding or edit invalidates both reviews and repeats Steps B1-8 through B1-11.

- [ ] **Step B1-12: Validate all B1 identities are non-empty and distinct**

Run:

```powershell
$identities = @(
    $env:PROJECTB_AGENT_ID
    $env:PROJECTB_SPEC_REVIEWER_ID
    $env:PROJECTB_QUALITY_REVIEWER_ID
)
foreach ($identity in $identities) {
    if ([string]::IsNullOrWhiteSpace($identity)) {
        throw 'T-02B1 worker and reviewer identities must all be non-empty'
    }
    if ($identity -notmatch '^[A-Za-z0-9][A-Za-z0-9._-]{1,63}$') {
        throw 'T-02B1 worker or reviewer identity contains unsupported characters'
    }
}
if (($identities | Sort-Object -Unique).Count -ne 3) {
    throw 'T-02B1 worker, SPEC reviewer, and quality reviewer must be distinct'
}
```

Expected: exit code 0 with three pairwise-distinct identities.

- [ ] **Step B1-13: Recheck the reviewed staged patch**

Run:

```powershell
Invoke-CheckedNative -FilePath $GitExe -ArgumentList @('diff', '--cached', '--check')
if ($LASTEXITCODE -ne 0) {
    throw 'reviewed staged diff check failed'
}
Assert-ExactStagedPaths -ExpectedPaths @(
    'backend/src/projectb/domain/source/hashing.py'
    'backend/tests/unit/domain/test_source_hashing.py'
)
Invoke-CheckedPowerShell -ArgumentList @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', 'scripts/scan_secrets.ps1', '-PythonExe', $PythonExe, '--staged')
$currentTree = Get-CheckedIndexTree
if ($env:PROJECTB_REVIEWED_TREE -notmatch '^[0-9a-f]{40}$' -or
    $currentTree -ne $env:PROJECTB_REVIEWED_TREE) {
    throw 'T-02B1 index tree changed after review; both reviews are invalid'
}
```

Expected: exit code 0 only when the immediately pre-commit index tree equals the tree reviewed by both reviewers.

- [ ] **Step B1-14: Commit T-02B1**

Run:

```powershell
Invoke-CheckedNative -FilePath $GitExe -ArgumentList @(
    'commit', '-m',
    "feat(T-02B1): add source hashing and normalization [agent: $env:PROJECTB_AGENT_ID]"
)
if ($LASTEXITCODE -ne 0) {
    throw 'T-02B1 commit failed'
}
$committedTree = @(Invoke-CheckedNative -FilePath $GitExe -ArgumentList @(
    'rev-parse', 'HEAD^{tree}'
))
if ($committedTree.Count -ne 1 -or
    $committedTree[0].Trim() -ne $env:PROJECTB_REVIEWED_TREE) {
    throw 'T-02B1 committed tree differs from the reviewed tree'
}
```

Expected: exit code 0 and a `feat(T-02B1)` subject containing the reviewed worker identity.

- [ ] **Step B1-15: Capture the T-02B1 commit hash**

Run:

```powershell
$commitHash = @(Invoke-CheckedNative -FilePath $GitExe -ArgumentList @(
    'rev-parse', 'HEAD'
))
if ($LASTEXITCODE -ne 0) {
    throw 'T-02B1 hash capture failed'
}
if ($commitHash.Count -ne 1 -or $commitHash[0] -notmatch '^[0-9a-f]{40}$') {
    throw 'T-02B1 hash must be one lowercase 40-character hexadecimal value'
}
$commitHash[0]
```

Expected: exit code 0 with one observed 40-character lowercase hexadecimal hash. The coordinator records it and both reviewer identities/outcomes before dispatching T-02B2A.

**T-02B1 completion standard:** The two owned paths provide raw-byte SHA-256, v1 normalization, and stable invalid-shape errors; focused/full commands, refactor checks, scanner, exact staged-set comparison, two fresh reviews, commit, and hash evidence all exit successfully. No facade, locator, or catalog code is included.

### Task T-02B2A: Locators and Catalog/Mapping Validation

**Goal:** Consume B1's hashing contract and add the four immutable locator branches, strict catalog/member validation, and mapping dispatch without creating the public source facade or adding proof behavior.

**Dependencies / parallelism:** Start a new worktree from the reviewed T-02B1 commit. T-02B2A owns only `models.py` and its test file. T-02B2B starts only from the reviewed T-02B2A commit and is the sole B-stage facade owner.

**Files:**
- Create: `backend/src/projectb/domain/source/models.py`
- Create: `backend/tests/unit/domain/test_source_models.py`

**Produced interfaces:** `Region`, `PdfPageLocator`, `ImageLocator`, `TextLinesLocator`, `ManualEntryLocator`, `SourceLocator`, `MaterialSource`, `ManualSource`, `SourceCatalog`, `source_locator_from_mapping`, and `validate_source_locator`. They remain importable from `projectb.domain.source.models` until T-02B2B publishes the reviewed facade.

- [ ] **Step B2A-0: Establish the complete T-02B2A runtime, base, worktree, and ownership prelude**

Execute the complete Runtime and Evidence Contract block above in this fresh T-02B2A shell, then run:

```powershell
Initialize-DomainUnit -ExpectedUnitId 'T-02B2A' -ExpectedPaths @(
    'backend/src/projectb/domain/source/models.py'
    'backend/tests/unit/domain/test_source_models.py'
)
```

Expected: exit code 0 only for the clean T-02B2A worktree at the reviewed T-02B1 base with the exact two-path ownership scope.

- [ ] **Step B2A-1: Create the failing four-branch mapping-parser matrix**

Create `backend/tests/unit/domain/test_source_models.py` with this exact first slice:

```python
from dataclasses import FrozenInstanceError

import pytest

from projectb.domain.errors import SourceContractError, SourceErrorCode
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
```

- [ ] **Step B2A-2: Append unknown, mixed, and non-Mapping parser tests**

Append exactly to `backend/tests/unit/domain/test_source_models.py`:

```python


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


@pytest.mark.parametrize("payload", [None, True, "pdf_page", []])
def test_mapping_parser_rejects_non_mapping_payloads(payload: object) -> None:
    with pytest.raises(SourceContractError) as caught:
        source_locator_from_mapping(payload)
    assert caught.value.code is SourceErrorCode.INVALID_SHAPE
```

- [ ] **Step B2A-3: Append the failing immutable locator boundary tests**

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
```

- [ ] **Step B2A-4: Append the failing Region boundary tests**

Append exactly to `backend/tests/unit/domain/test_source_models.py`:

```python


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
        (True, 0, 0.5, 0.5),
        ("0", 0, 0.5, 0.5),
    ],
)
def test_region_rejects_foreign_nonfinite_or_out_of_bounds_members(
    x: object,
    y: object,
    width: object,
    height: object,
) -> None:
    with pytest.raises(SourceContractError) as caught:
        Region(x=x, y=y, width=width, height=height)
    assert caught.value.code is SourceErrorCode.INVALID_REGION
```

- [ ] **Step B2A-5: Append the failing MaterialSource container/member tests**

Append exactly to `backend/tests/unit/domain/test_source_models.py`:

```python


def material_source() -> MaterialSource:
    return MaterialSource(
        material_id=MaterialId("material-1"),
        content_hash=HASH,
        page_count=2,
        image_ids=frozenset({ImageId("image-1")}),
        line_count=4,
    )


def test_material_source_keeps_a_valid_frozen_image_id_set() -> None:
    source = material_source()
    assert source.image_ids == frozenset({ImageId("image-1")})


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("page_count", True),
        ("line_count", True),
        ("image_ids", "image-1"),
        ("image_ids", (ImageId("image-1"),)),
        ("image_ids", frozenset({1})),
    ],
)
def test_material_source_rejects_invalid_containers_and_members(
    field: str,
    value: object,
) -> None:
    values: dict[str, object] = {
        "material_id": MaterialId("material-1"),
        "content_hash": HASH,
        "page_count": 2,
        "image_ids": frozenset({ImageId("image-1")}),
        "line_count": 4,
    }
    values[field] = value
    with pytest.raises(SourceContractError) as caught:
        MaterialSource(**values)
    assert caught.value.code is SourceErrorCode.INVALID_CATALOG
```

- [ ] **Step B2A-6: Append the matching-catalog and catalog-container tests**

Append exactly to `backend/tests/unit/domain/test_source_models.py`:

```python


def test_catalog_accepts_matching_pdf_image_text_and_manual_locators() -> None:
    catalog = SourceCatalog(
        materials=(material_source(),),
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
    ("materials_value", "manual_value"),
    [
        ("material-1", ()),
        ((), "entry-1"),
        ((ManualSource(EntryId("entry-1"), 1),), ()),
        ((), (material_source(),)),
    ],
)
def test_catalog_rejects_string_containers_and_foreign_members(
    materials_value: object,
    manual_value: object,
) -> None:
    with pytest.raises(SourceContractError) as caught:
        SourceCatalog(materials=materials_value, manual_entries=manual_value)
    assert caught.value.code is SourceErrorCode.INVALID_CATALOG
```

- [ ] **Step B2A-7: Append the duplicate catalog identity tests**

Append exactly to `backend/tests/unit/domain/test_source_models.py`:

```python


def test_catalog_rejects_duplicate_material_ids() -> None:
    with pytest.raises(SourceContractError) as caught:
        SourceCatalog(materials=(material_source(), material_source()))
    assert caught.value.code is SourceErrorCode.INVALID_CATALOG


def test_catalog_rejects_duplicate_manual_entry_ids() -> None:
    with pytest.raises(SourceContractError) as caught:
        SourceCatalog(
            manual_entries=(
                ManualSource(EntryId("entry-1"), 1),
                ManualSource(EntryId("entry-1"), 2),
            )
        )
    assert caught.value.code is SourceErrorCode.INVALID_CATALOG
```

- [ ] **Step B2A-8: Append the missing, stale, and out-of-range locator matrix**

Append exactly to `backend/tests/unit/domain/test_source_models.py`:

```python


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
        materials=(material_source(),),
        manual_entries=(ManualSource(EntryId("entry-1"), 3),),
    )
    with pytest.raises(SourceContractError) as caught:
        validate_source_locator(locator, catalog)
    assert caught.value.code is expected_code
```

- [ ] **Step B2A-9: Append the foreign catalog and locator tests**

Append exactly to `backend/tests/unit/domain/test_source_models.py`:

```python


def test_locator_validation_rejects_a_foreign_catalog() -> None:
    with pytest.raises(SourceContractError) as caught:
        validate_source_locator(
            PdfPageLocator(MaterialId("material-1"), HASH, 1),
            object(),
        )
    assert caught.value.code is SourceErrorCode.INVALID_CATALOG


def test_locator_validation_rejects_a_foreign_locator() -> None:
    catalog = SourceCatalog(materials=(material_source(),))
    with pytest.raises(SourceContractError) as caught:
        validate_source_locator(object(), catalog)
    assert caught.value.code is SourceErrorCode.INVALID_KIND
```

- [ ] **Step B2A-10: Run the locator/catalog test file and capture red evidence**

Run:

```powershell
$env:PYTHONPATH = (Resolve-Path 'backend/src').Path
Invoke-ExpectedNativeExit -FilePath $PythonExe -ExpectedExitCode 2 -ArgumentList @(
    '-m', 'pytest', '-c', 'backend/pyproject.toml',
    'backend/tests/unit/domain/test_source_models.py', '-q'
)
```

Expected: exit code 2 with a collection error because `projectb.domain.source.models` does not exist; no model test passes.

- [ ] **Step B2A-11: Implement model helpers and immutable Region**

Create `backend/src/projectb/domain/source/models.py` with this exact first slice:

```python
import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Literal, cast

from projectb.domain.errors import SourceContractError, SourceErrorCode
from projectb.domain.types import (
    EntryId,
    ImageId,
    MaterialId,
    validate_content_hash,
    validate_opaque_id,
)


def _require_positive_int(value: object, code: SourceErrorCode) -> int:
    if type(value) is not int or value < 1:
        raise SourceContractError(code)
    return value


@dataclass(frozen=True, slots=True)
class Region:
    x: float
    y: float
    width: float
    height: float

    def __post_init__(self) -> None:
        region_values: tuple[tuple[str, object], ...] = (
            ("x", self.x),
            ("y", self.y),
            ("width", self.width),
            ("height", self.height),
        )
        for name, value in region_values:
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise SourceContractError(SourceErrorCode.INVALID_REGION)
            normalized = float(value)
            if not math.isfinite(normalized):
                raise SourceContractError(SourceErrorCode.INVALID_REGION)
            object.__setattr__(self, name, normalized)
        if not (0 <= self.x < 1 and 0 <= self.y < 1):
            raise SourceContractError(SourceErrorCode.INVALID_REGION)
        if not (0 < self.width <= 1 - self.x):
            raise SourceContractError(SourceErrorCode.INVALID_REGION)
        if not (0 < self.height <= 1 - self.y):
            raise SourceContractError(SourceErrorCode.INVALID_REGION)
```

- [ ] **Step B2A-12: Append immutable PDF-page and image locator records**

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
        material_id_value: object = self.material_id
        content_hash_value: object = self.content_hash
        page_value: object = self.page
        region_value: object = self.region
        validate_opaque_id(material_id_value)
        validate_content_hash(content_hash_value)
        _require_positive_int(page_value, SourceErrorCode.INVALID_PAGE)
        if region_value is not None and not isinstance(region_value, Region):
            raise SourceContractError(SourceErrorCode.INVALID_REGION)


@dataclass(frozen=True, slots=True)
class ImageLocator:
    material_id: MaterialId
    content_hash: str
    image_id: ImageId
    region: Region | None = None
    kind: Literal["image"] = field(default="image", init=False)

    def __post_init__(self) -> None:
        material_id_value: object = self.material_id
        content_hash_value: object = self.content_hash
        image_id_value: object = self.image_id
        region_value: object = self.region
        validate_opaque_id(material_id_value)
        validate_content_hash(content_hash_value)
        validate_opaque_id(image_id_value)
        if region_value is not None and not isinstance(region_value, Region):
            raise SourceContractError(SourceErrorCode.INVALID_REGION)
```

- [ ] **Step B2A-13: Append text/manual locators and the exact union**

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
        material_id_value: object = self.material_id
        content_hash_value: object = self.content_hash
        line_start_value: object = self.line_start
        line_end_value: object = self.line_end
        validate_opaque_id(material_id_value)
        validate_content_hash(content_hash_value)
        line_start = _require_positive_int(
            line_start_value,
            SourceErrorCode.INVALID_LINE_RANGE,
        )
        line_end = _require_positive_int(
            line_end_value,
            SourceErrorCode.INVALID_LINE_RANGE,
        )
        if line_end < line_start:
            raise SourceContractError(SourceErrorCode.INVALID_LINE_RANGE)


@dataclass(frozen=True, slots=True)
class ManualEntryLocator:
    entry_id: EntryId
    version: int
    kind: Literal["manual_entry"] = field(default="manual_entry", init=False)

    def __post_init__(self) -> None:
        entry_id_value: object = self.entry_id
        version_value: object = self.version
        validate_opaque_id(entry_id_value)
        _require_positive_int(version_value, SourceErrorCode.INVALID_SHAPE)


type SourceLocator = PdfPageLocator | ImageLocator | TextLinesLocator | ManualEntryLocator
```

- [ ] **Step B2A-14: Append strict MaterialSource and ManualSource records**

Append exactly to `backend/src/projectb/domain/source/models.py`:

```python


@dataclass(frozen=True, slots=True)
class MaterialSource:
    material_id: MaterialId
    content_hash: str
    page_count: int = 0
    image_ids: frozenset[ImageId] = field(default_factory=frozenset)
    line_count: int = 0

    def __post_init__(self) -> None:
        material_id_value: object = self.material_id
        content_hash_value: object = self.content_hash
        page_count_value: object = self.page_count
        image_ids_value: object = self.image_ids
        line_count_value: object = self.line_count
        validate_opaque_id(material_id_value)
        validate_content_hash(content_hash_value)
        if type(page_count_value) is not int or page_count_value < 0:
            raise SourceContractError(SourceErrorCode.INVALID_CATALOG)
        if type(line_count_value) is not int or line_count_value < 0:
            raise SourceContractError(SourceErrorCode.INVALID_CATALOG)
        if not isinstance(image_ids_value, frozenset):
            raise SourceContractError(SourceErrorCode.INVALID_CATALOG)
        image_ids = cast(frozenset[object], image_ids_value)
        for image_id in image_ids:
            try:
                validate_opaque_id(image_id)
            except SourceContractError as error:
                raise SourceContractError(SourceErrorCode.INVALID_CATALOG) from error


@dataclass(frozen=True, slots=True)
class ManualSource:
    entry_id: EntryId
    version: int

    def __post_init__(self) -> None:
        entry_id_value: object = self.entry_id
        version_value: object = self.version
        validate_opaque_id(entry_id_value)
        _require_positive_int(version_value, SourceErrorCode.INVALID_CATALOG)
```

- [ ] **Step B2A-15: Append strict SourceCatalog container validation**

Append exactly to `backend/src/projectb/domain/source/models.py`:

```python


@dataclass(frozen=True, slots=True)
class SourceCatalog:
    materials: Sequence[MaterialSource] = ()
    manual_entries: Sequence[ManualSource] = ()

    def __post_init__(self) -> None:
        materials_value: object = self.materials
        manual_entries_value: object = self.manual_entries
        if isinstance(materials_value, (str, bytes, bytearray)) or not isinstance(
            materials_value,
            Sequence,
        ):
            raise SourceContractError(SourceErrorCode.INVALID_CATALOG)
        if isinstance(manual_entries_value, (str, bytes, bytearray)) or not isinstance(
            manual_entries_value,
            Sequence,
        ):
            raise SourceContractError(SourceErrorCode.INVALID_CATALOG)
        materials_list: list[MaterialSource] = []
        for item_value in materials_value:
            if not isinstance(item_value, MaterialSource):
                raise SourceContractError(SourceErrorCode.INVALID_CATALOG)
            materials_list.append(item_value)
        manual_entries_list: list[ManualSource] = []
        for item_value in manual_entries_value:
            if not isinstance(item_value, ManualSource):
                raise SourceContractError(SourceErrorCode.INVALID_CATALOG)
            manual_entries_list.append(item_value)
        materials = tuple(materials_list)
        manual_entries = tuple(manual_entries_list)
        if len({item.material_id for item in materials}) != len(materials):
            raise SourceContractError(SourceErrorCode.INVALID_CATALOG)
        if len({item.entry_id for item in manual_entries}) != len(manual_entries):
            raise SourceContractError(SourceErrorCode.INVALID_CATALOG)
        object.__setattr__(self, "materials", materials)
        object.__setattr__(self, "manual_entries", manual_entries)
```

- [ ] **Step B2A-16: Append fail-closed locator-to-catalog validation**

Append exactly to `backend/src/projectb/domain/source/models.py`:

```python


def validate_source_locator(locator: object, catalog: object) -> None:
    if not isinstance(catalog, SourceCatalog):
        raise SourceContractError(SourceErrorCode.INVALID_CATALOG)
    if isinstance(locator, ManualEntryLocator):
        manual_source = next(
            (item for item in catalog.manual_entries if item.entry_id == locator.entry_id),
            None,
        )
        if manual_source is None:
            raise SourceContractError(SourceErrorCode.ENTRY_NOT_FOUND)
        if manual_source.version != locator.version:
            raise SourceContractError(SourceErrorCode.STALE_ENTRY_VERSION)
        return
    if not isinstance(locator, (PdfPageLocator, ImageLocator, TextLinesLocator)):
        raise SourceContractError(SourceErrorCode.INVALID_KIND)
    material_source = next(
        (item for item in catalog.materials if item.material_id == locator.material_id),
        None,
    )
    if material_source is None:
        raise SourceContractError(SourceErrorCode.MATERIAL_NOT_FOUND)
    if material_source.content_hash != locator.content_hash:
        raise SourceContractError(SourceErrorCode.STALE_CONTENT_HASH)
    if isinstance(locator, PdfPageLocator) and locator.page > material_source.page_count:
        raise SourceContractError(SourceErrorCode.PAGE_OUT_OF_RANGE)
    if (
        isinstance(locator, ImageLocator)
        and locator.image_id not in material_source.image_ids
    ):
        raise SourceContractError(SourceErrorCode.IMAGE_NOT_FOUND)
    if (
        isinstance(locator, TextLinesLocator)
        and locator.line_end > material_source.line_count
    ):
        raise SourceContractError(SourceErrorCode.LINE_OUT_OF_RANGE)
```

- [ ] **Step B2A-17: Append strict mapping parser helpers**

Append exactly to `backend/src/projectb/domain/source/models.py`:

```python


def _require_keys(payload: Mapping[object, object], expected: set[str]) -> None:
    if set(payload) != expected:
        raise SourceContractError(SourceErrorCode.INVALID_SHAPE)


def _string(payload: Mapping[object, object], key: str) -> str:
    value = payload[key]
    if not isinstance(value, str) or not value or value.strip() != value:
        raise SourceContractError(SourceErrorCode.INVALID_SHAPE)
    return value


def _integer(payload: Mapping[object, object], key: str) -> int:
    value = payload[key]
    if type(value) is not int:
        raise SourceContractError(SourceErrorCode.INVALID_SHAPE)
    return value


def _number(payload: Mapping[object, object], key: str) -> float:
    value = payload[key]
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise SourceContractError(SourceErrorCode.INVALID_REGION)
    return float(value)


def _region(value: object) -> Region | None:
    if value is None:
        return None
    if not isinstance(value, Mapping):
        raise SourceContractError(SourceErrorCode.INVALID_REGION)
    region = cast(Mapping[object, object], value)
    _require_keys(region, {"x", "y", "width", "height"})
    return Region(
        x=_number(region, "x"),
        y=_number(region, "y"),
        width=_number(region, "width"),
        height=_number(region, "height"),
    )
```

- [ ] **Step B2A-18: Append PDF-page and image mapping branches**

Append exactly to `backend/src/projectb/domain/source/models.py`:

```python


def _pdf_page_from_mapping(mapping: Mapping[object, object]) -> PdfPageLocator:
    allowed = {"kind", "material_id", "content_hash", "page"}
    if "region" in mapping:
        allowed.add("region")
    _require_keys(mapping, allowed)
    return PdfPageLocator(
        material_id=MaterialId(_string(mapping, "material_id")),
        content_hash=_string(mapping, "content_hash"),
        page=_integer(mapping, "page"),
        region=_region(mapping.get("region")),
    )


def _image_from_mapping(mapping: Mapping[object, object]) -> ImageLocator:
    allowed = {"kind", "material_id", "content_hash", "image_id"}
    if "region" in mapping:
        allowed.add("region")
    _require_keys(mapping, allowed)
    return ImageLocator(
        material_id=MaterialId(_string(mapping, "material_id")),
        content_hash=_string(mapping, "content_hash"),
        image_id=ImageId(_string(mapping, "image_id")),
        region=_region(mapping.get("region")),
    )
```

- [ ] **Step B2A-19: Append text/manual mapping branches and model exports**

Append exactly to `backend/src/projectb/domain/source/models.py`:

```python
def _text_lines_from_mapping(mapping: Mapping[object, object]) -> TextLinesLocator:
    _require_keys(
        mapping,
        {"kind", "material_id", "content_hash", "line_start", "line_end"},
    )
    return TextLinesLocator(
        material_id=MaterialId(_string(mapping, "material_id")),
        content_hash=_string(mapping, "content_hash"),
        line_start=_integer(mapping, "line_start"),
        line_end=_integer(mapping, "line_end"),
    )


def _manual_entry_from_mapping(
    mapping: Mapping[object, object],
) -> ManualEntryLocator:
    _require_keys(mapping, {"kind", "entry_id", "version"})
    return ManualEntryLocator(
        entry_id=EntryId(_string(mapping, "entry_id")),
        version=_integer(mapping, "version"),
    )


def source_locator_from_mapping(payload: object) -> SourceLocator:
    if not isinstance(payload, Mapping):
        raise SourceContractError(SourceErrorCode.INVALID_SHAPE)
    mapping = cast(Mapping[object, object], payload)
    kind = mapping.get("kind")
    if kind == "pdf_page":
        return _pdf_page_from_mapping(mapping)
    if kind == "image":
        return _image_from_mapping(mapping)
    if kind == "text_lines":
        return _text_lines_from_mapping(mapping)
    if kind == "manual_entry":
        return _manual_entry_from_mapping(mapping)
    raise SourceContractError(SourceErrorCode.INVALID_KIND)


__all__ = [
    "ImageLocator",
    "ManualEntryLocator",
    "ManualSource",
    "MaterialSource",
    "PdfPageLocator",
    "Region",
    "SourceCatalog",
    "SourceLocator",
    "TextLinesLocator",
    "source_locator_from_mapping",
    "validate_source_locator",
]
```

- [ ] **Step B2A-20: Run the locator and catalog slice green**

Run:

```powershell
$env:PYTHONPATH = (Resolve-Path 'backend/src').Path
Invoke-CheckedPython -ArgumentList @('-m', 'pytest', '-c', 'backend/pyproject.toml', 'backend/tests/unit/domain/test_source_models.py', '-q')
```

Expected: exit code 0; every locator, region, catalog, mapping, and stale/missing/out-of-range behavior assertion passes. Record observed output.

- [ ] **Step B2A-21: Format and re-run the focused model suite**

```powershell
Invoke-CheckedPython -ArgumentList @('-m', 'ruff', 'format', '--config', 'backend/pyproject.toml', 'backend/src/projectb/domain/source/models.py', 'backend/tests/unit/domain/test_source_models.py')
$env:PYTHONPATH = (Resolve-Path 'backend/src').Path
Invoke-CheckedPython -ArgumentList @('-m', 'pytest', '-c', 'backend/pyproject.toml', 'backend/tests/unit/domain/test_source_models.py', '-q')
```

Expected: formatting exits 0 and every model test remains green.

- [ ] **Step B2A-22: Run cumulative domain, Ruff, mypy, and canonical verification**

```powershell
$env:PYTHONPATH = (Resolve-Path 'backend/src').Path
Invoke-CheckedPython -ArgumentList @('-m', 'pytest', '-c', 'backend/pyproject.toml', 'backend/tests/unit/domain', '-q')
Invoke-CheckedPython -ArgumentList @('-m', 'ruff', 'check', '--config', 'backend/pyproject.toml', 'backend/src/projectb/domain', 'backend/tests/unit/domain')
Invoke-CheckedPython -ArgumentList @('-m', 'mypy', '--config-file', 'backend/pyproject.toml', 'backend/src/projectb/domain')
Invoke-CheckedPython -ArgumentList @('scripts/test_all.py')
```

Expected: all current domain behavior and active canonical gates pass; unavailable later-owner gates remain unavailable rather than PASS.

- [ ] **Step B2A-23: Run the project scanner before staging**

```powershell
Invoke-CheckedPowerShell -ArgumentList @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', 'scripts/scan_secrets.ps1', '-PythonExe', $PythonExe)
```

Expected: exit code 0 with no credential finding and no file-content disclosure.

- [ ] **Step B2A-24: Validate the worker identity and stage exactly two paths**

```powershell
if ([string]::IsNullOrWhiteSpace($env:PROJECTB_AGENT_ID) -or $env:PROJECTB_AGENT_ID -notmatch '^[A-Za-z0-9][A-Za-z0-9._-]{1,63}$') {
    throw 'PROJECTB_AGENT_ID must identify the fresh T-02B2A worker'
}
Invoke-CheckedNative -FilePath $GitExe -ArgumentList @(
    'add', '--',
    'backend/src/projectb/domain/source/models.py',
    'backend/tests/unit/domain/test_source_models.py'
)
if ($LASTEXITCODE -ne 0) {
    throw 'T-02B2A git add failed'
}
Invoke-CheckedNative -FilePath $GitExe -ArgumentList @('diff', '--cached', '--check')
if ($LASTEXITCODE -ne 0) {
    throw 'T-02B2A staged diff check failed'
}
Assert-ExactStagedPaths -ExpectedPaths @(
    'backend/src/projectb/domain/source/models.py'
    'backend/tests/unit/domain/test_source_models.py'
)
Invoke-CheckedPowerShell -ArgumentList @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', 'scripts/scan_secrets.ps1', '-PythonExe', $PythonExe, '--staged')
$env:PROJECTB_REVIEWED_TREE = Get-CheckedIndexTree
$env:PROJECTB_REVIEWED_TREE
```

Expected: only the two T-02B2A paths are staged and scanned, followed by one lowercase 40-hex index tree ID; any mismatch fails before review.

- [ ] **Step B2A-25: Obtain the fresh SPEC review**

Bind the SPEC review record to `REVIEWED TREE: $env:PROJECTB_REVIEWED_TREE`. Match the root T-02B2A scope exactly: the reviewer checks the locator/catalog portions of AC-03, AC-12, AC-13, AC-14, and AC-37 against SPEC section 3 M2's exact four-way `SourceLocator` union, one-based page/line rules, finite normalized `Region`, strict runtime container/member validation, and hash/version catalog prerequisites. This unit does not claim public-facade, explanation-opening, or unique-page-proof behavior. Record `PROJECTB_SPEC_REVIEWER_ID` only after all Critical/Important findings are fixed on that exact tree. Any edit invalidates both reviews and repeats Steps B2A-24 through B2A-26 with a new tree.

- [ ] **Step B2A-26: Obtain the distinct fresh quality/security review**

The second reviewer records the same `REVIEWED TREE: $env:PROJECTB_REVIEWED_TREE` and checks Mapping/Sequence runtime boundaries, string/foreign-member rejection, immutable copies, bool-vs-int handling, deterministic tests, stable errors, standard-library-only production code, and license impact. Record `PROJECTB_QUALITY_REVIEWER_ID` only after all Critical/Important findings are fixed on that exact tree. Any edit invalidates both reviews and repeats Steps B2A-24 through B2A-26.

- [ ] **Step B2A-27: Validate identities and recheck the reviewed index**

```powershell
$identities = @($env:PROJECTB_AGENT_ID, $env:PROJECTB_SPEC_REVIEWER_ID, $env:PROJECTB_QUALITY_REVIEWER_ID)
if ($identities.Where({ [string]::IsNullOrWhiteSpace($_) -or $_ -notmatch '^[A-Za-z0-9][A-Za-z0-9._-]{1,63}$' }).Count -ne 0 -or ($identities | Sort-Object -Unique).Count -ne 3) {
    throw 'T-02B2A requires three valid pairwise-distinct identities'
}
Invoke-CheckedNative -FilePath $GitExe -ArgumentList @('diff', '--cached', '--check')
if ($LASTEXITCODE -ne 0) {
    throw 'T-02B2A reviewed staged diff check failed'
}
Assert-ExactStagedPaths -ExpectedPaths @(
    'backend/src/projectb/domain/source/models.py'
    'backend/tests/unit/domain/test_source_models.py'
)
Invoke-CheckedPowerShell -ArgumentList @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', 'scripts/scan_secrets.ps1', '-PythonExe', $PythonExe, '--staged')
$currentTree = Get-CheckedIndexTree
if ($env:PROJECTB_REVIEWED_TREE -notmatch '^[0-9a-f]{40}$' -or
    $currentTree -ne $env:PROJECTB_REVIEWED_TREE) {
    throw 'T-02B2A index tree changed after review; both reviews are invalid'
}
```

Expected: the exact two-path index remains clean and its immediately pre-commit tree equals the tree named by both reviewers.

- [ ] **Step B2A-28: Commit the reviewed T-02B2A index**

```powershell
Invoke-CheckedNative -FilePath $GitExe -ArgumentList @(
    'commit', '-m',
    "feat(T-02B2A): add strict source models [agent: $env:PROJECTB_AGENT_ID]"
)
if ($LASTEXITCODE -ne 0) {
    throw 'T-02B2A commit failed'
}
$committedTree = @(Invoke-CheckedNative -FilePath $GitExe -ArgumentList @(
    'rev-parse', 'HEAD^{tree}'
))
if ($committedTree.Count -ne 1 -or
    $committedTree[0].Trim() -ne $env:PROJECTB_REVIEWED_TREE) {
    throw 'T-02B2A committed tree differs from the reviewed tree'
}
```

Expected: the identity-bound two-path commit exits 0. No hash command runs when commit creation fails.

- [ ] **Step B2A-29: Capture and validate the T-02B2A hash**

```powershell
$commitHash = @(Invoke-CheckedNative -FilePath $GitExe -ArgumentList @(
    'rev-parse', 'HEAD'
))
if ($LASTEXITCODE -ne 0) {
    throw 'T-02B2A hash capture failed'
}
if ($commitHash.Count -ne 1 -or $commitHash[0] -notmatch '^[0-9a-f]{40}$') {
    throw 'T-02B2A hash must be one lowercase 40-character hexadecimal value'
}
$commitHash[0]
```

Expected: exactly one 40-character lowercase hexadecimal hash is recorded with both review outcomes before B2B begins.

**T-02B2A completion standard:** Model/mapping tests, cumulative verification, static checks, worktree and staged scans, exact path assertion, two independent reviews, commit, and hash all have current evidence. The public source facade remains absent and deferred to T-02B2B.

### Task T-02B2B: Publish the Reviewed B-stage Source Facade

**Goal:** Re-export the reviewed B1 hashing and B2A model/mapping contracts through `projectb.domain.source` without changing their behavior or adding proof code.

**Dependencies / parallelism:** Start a fresh worktree from the reviewed T-02B2A commit. This unit is the first owner and creator of the sequential source facade and owns its focused export test. T-02C waits for the reviewed T-02B2B commit.

**Files:**
- Create: `backend/src/projectb/domain/source/__init__.py`
- Create: `backend/tests/unit/domain/test_source_exports.py`

**Produced interface:** the B-stage `projectb.domain.source` facade re-exports all B1 and B2A public contracts. It exports no proof symbol.

- [ ] **Step B2B-0: Establish the complete T-02B2B runtime, base, worktree, and ownership prelude**

Execute the complete Runtime and Evidence Contract block above in this fresh T-02B2B shell, then run:

```powershell
Initialize-DomainUnit -ExpectedUnitId 'T-02B2B' -ExpectedPaths @(
    'backend/src/projectb/domain/source/__init__.py'
    'backend/tests/unit/domain/test_source_exports.py'
)
```

Expected: exit code 0 only for the clean T-02B2B worktree at the reviewed T-02B2A base with the exact facade/export-test ownership scope.

- [ ] **Step B2B-1: Create the failing B-stage facade test**

Create `backend/tests/unit/domain/test_source_exports.py`:

```python
from projectb.domain.types import MaterialId


def test_source_facade_exports_the_b_stage_contract() -> None:
    from projectb.domain import source
    from projectb.domain.source import (
        PdfPageLocator as ExportedPdfPageLocator,
    )
    from projectb.domain.source import (
        raw_file_content_hash,
    )
    from projectb.domain.source import (
        source_locator_from_mapping as exported_parser,
    )

    assert source.__all__ == [
        "ImageLocator",
        "ManualEntryLocator",
        "ManualSource",
        "MaterialSource",
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
        "raw_file_content_hash",
        "source_locator_from_mapping",
        "validate_content_hash",
        "validate_source_locator",
    ]
    assert not hasattr(source, "PageText")

    content_hash = raw_file_content_hash(b"source")
    locator = exported_parser(
        {
            "kind": "pdf_page",
            "material_id": "material-1",
            "content_hash": content_hash,
            "page": 1,
        }
    )
    assert locator == ExportedPdfPageLocator(
        MaterialId("material-1"),
        content_hash,
        1,
    )
```

- [ ] **Step B2B-2: Run the B-stage facade case and capture red evidence**

Run:

```powershell
$env:PYTHONPATH = (Resolve-Path 'backend/src').Path
Invoke-ExpectedNativeExit -FilePath $PythonExe -ExpectedExitCode 1 -ArgumentList @(
    '-m', 'pytest', '-c', 'backend/pyproject.toml',
    'backend/tests/unit/domain/test_source_exports.py', '-q'
)
```

Expected: exit code 1 because the package facade is absent and therefore has no `__all__` or `PdfPageLocator` export.

- [ ] **Step B2B-3: Create the complete B-stage source facade**

Create `backend/src/projectb/domain/source/__init__.py` with exactly:

```python
"""Validated local source contracts."""

from projectb.domain.errors import (
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

__all__ = [
    "ImageLocator",
    "ManualEntryLocator",
    "ManualSource",
    "MaterialSource",
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
    "raw_file_content_hash",
    "source_locator_from_mapping",
    "validate_content_hash",
    "validate_source_locator",
]
```

- [ ] **Step B2B-4: Run the B-stage export test green**

Run:

```powershell
$env:PYTHONPATH = (Resolve-Path 'backend/src').Path
Invoke-CheckedPython -ArgumentList @('-m', 'pytest', '-c', 'backend/pyproject.toml', 'backend/tests/unit/domain/test_source_exports.py', '-q')
```

Expected: exit code 0; the B-stage public export assertion passes.

- [ ] **Step B2B-5: Format only the two T-02B2B files under green tests**

Run:

```powershell
Invoke-CheckedPython -ArgumentList @('-m', 'ruff', 'format', '--config', 'backend/pyproject.toml', 'backend/src/projectb/domain/source/__init__.py', 'backend/tests/unit/domain/test_source_exports.py')
```

Expected: exit code 0; Ruff reports only the two T-02B2B files formatted or already formatted and changes no behavior.

- [ ] **Step B2B-6: Re-run the B-stage export test after refactoring**

Run:

```powershell
$env:PYTHONPATH = (Resolve-Path 'backend/src').Path
Invoke-CheckedPython -ArgumentList @('-m', 'pytest', '-c', 'backend/pyproject.toml', 'backend/tests/unit/domain/test_source_exports.py', '-q')
```

Expected: exit code 0; formatting changed no B-stage facade behavior.

- [ ] **Step B2B-7: Run the cumulative A+B1+B2 domain suite**

Run:

```powershell
$env:PYTHONPATH = (Resolve-Path 'backend/src').Path
Invoke-CheckedPython -ArgumentList @('-m', 'pytest', '-c', 'backend/pyproject.toml', 'backend/tests/unit/domain', '-q')
```

Expected: exit code 0; the complete domain suite available at the B2 checkpoint passes. Record observed output without a fixed count.

- [ ] **Step B2B-8: Run Ruff with the locked backend configuration**

Run:

```powershell
Invoke-CheckedPython -ArgumentList @('-m', 'ruff', 'check', '--config', 'backend/pyproject.toml', 'backend/src/projectb/domain', 'backend/tests/unit/domain')
```

Expected: exit code 0 with `All checks passed!`.

- [ ] **Step B2B-9: Run mypy with the locked backend configuration**

Run:

```powershell
$env:PYTHONPATH = (Resolve-Path 'backend/src').Path
Invoke-CheckedPython -ArgumentList @('-m', 'mypy', '--config-file', 'backend/pyproject.toml', 'backend/src/projectb/domain')
```

Expected: exit code 0 with no issues in the A+B domain source files.

- [ ] **Step B2B-10: Run the repository one-command verification entry**

Run:

```powershell
Invoke-CheckedPython -ArgumentList @('scripts/test_all.py')
```

Expected: exit code 0; every active canonical gate passes and unopened later-owner gates remain unavailable rather than PASS. Record the observed gate summary.

- [ ] **Step B2B-11: Run the project secret scanner separately**

Run:

```powershell
Invoke-CheckedPowerShell -ArgumentList @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', 'scripts/scan_secrets.ps1', '-PythonExe', $PythonExe)
```

Expected: exit code 0 with no credential finding and no file-content disclosure.

- [ ] **Step B2B-12: Validate the fresh T-02B2B worker identity**

Run:

```powershell
if ([string]::IsNullOrWhiteSpace($env:PROJECTB_AGENT_ID)) {
    throw 'PROJECTB_AGENT_ID must identify the fresh T-02B2B worker'
}
if ($env:PROJECTB_AGENT_ID -notmatch '^[A-Za-z0-9][A-Za-z0-9._-]{1,63}$') {
    throw 'PROJECTB_AGENT_ID contains unsupported characters'
}
```

Expected: exit code 0; unset, blank, or malformed identities stop before staging and review.

- [ ] **Step B2B-13: Stage exactly the T-02B2B ownership set**

Run:

```powershell
Invoke-CheckedNative -FilePath $GitExe -ArgumentList @(
    'add', '--',
    'backend/src/projectb/domain/source/__init__.py',
    'backend/tests/unit/domain/test_source_exports.py'
)
if ($LASTEXITCODE -ne 0) {
    throw 'T-02B2B git add failed'
}
```

Expected: exit code 0; only the two literal T-02B2B paths are added to the index.

- [ ] **Step B2B-14: Check the staged T-02B2B patch**

Run:

```powershell
Invoke-CheckedNative -FilePath $GitExe -ArgumentList @('diff', '--cached', '--check')
if ($LASTEXITCODE -ne 0) {
    throw 'T-02B2B staged diff check failed'
}
```

Expected: exit code 0 with no output.

- [ ] **Step B2B-15: Assert the exact staged T-02B2B path set and scan the index**

Run:

```powershell
Assert-ExactStagedPaths -ExpectedPaths @(
    'backend/src/projectb/domain/source/__init__.py'
    'backend/tests/unit/domain/test_source_exports.py'
)
Invoke-CheckedPowerShell -ArgumentList @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', 'scripts/scan_secrets.ps1', '-PythonExe', $PythonExe, '--staged')
$env:PROJECTB_REVIEWED_TREE = Get-CheckedIndexTree
$env:PROJECTB_REVIEWED_TREE
```

Expected: exit code 0 and one lowercase 40-hex index tree ID. Any ownership mismatch blocks review before tree capture.

- [ ] **Step B2B-16: Request the fresh T-02B2B SPEC review**

The coordinator gives a fresh non-worker reviewer the complete packet, requires `REVIEWED TREE: $env:PROJECTB_REVIEWED_TREE` in the review record, and records the reviewer's canonical identity in `$env:PROJECTB_SPEC_REVIEWER_ID`. Match the root T-02B2B scope exactly: check the public-boundary portions of AC-03 and AC-37 while publishing the already reviewed B1/B2A contracts through the provider-independent `projectb.domain.source` facade, with no proof symbol and no API/UI behavior claim. PASS requires the exact ordered export set, no hidden behavior change, no internal leakage, and no import cycle.

Expected: `SPEC REVIEW: PASS` bound to the captured tree ID. Any edit invalidates both reviews and repeats Steps B2B-13 through B2B-17 with a new tree.

- [ ] **Step B2B-17: Request the different fresh T-02B2B quality review**

The coordinator gives the complete packet with the same `REVIEWED TREE: $env:PROJECTB_REVIEWED_TREE` binding to a second fresh reviewer and records that reviewer's canonical identity in `$env:PROJECTB_QUALITY_REVIEWER_ID`. This reviewer must differ from the worker and SPEC reviewer and checks facade imports, `__all__` completeness, import-cycle risk, deterministic focused coverage, error redaction, standard-library-only production code, and dependency/license impact.

Expected: `QUALITY REVIEW: PASS` bound to the same tree ID. Any finding or edit invalidates both reviews and repeats Steps B2B-13 through B2B-17.

- [ ] **Step B2B-18: Validate the three T-02B2B identities are non-empty and distinct**

Run:

```powershell
$identities = @(
    $env:PROJECTB_AGENT_ID
    $env:PROJECTB_SPEC_REVIEWER_ID
    $env:PROJECTB_QUALITY_REVIEWER_ID
)
foreach ($identity in $identities) {
    if ([string]::IsNullOrWhiteSpace($identity)) {
        throw 'T-02B2B worker and reviewer identities must all be non-empty'
    }
    if ($identity -notmatch '^[A-Za-z0-9][A-Za-z0-9._-]{1,63}$') {
        throw 'T-02B2B worker or reviewer identity contains unsupported characters'
    }
}
if (($identities | Sort-Object -Unique).Count -ne 3) {
    throw 'T-02B2B worker, SPEC reviewer, and quality reviewer must be distinct'
}
```

Expected: exit code 0 with three valid pairwise-distinct identities.

- [ ] **Step B2B-19: Recheck the reviewed staged patch and staged scan**

Run:

```powershell
Invoke-CheckedNative -FilePath $GitExe -ArgumentList @('diff', '--cached', '--check')
if ($LASTEXITCODE -ne 0) {
    throw 'T-02B2B reviewed staged diff check failed'
}
Assert-ExactStagedPaths -ExpectedPaths @(
    'backend/src/projectb/domain/source/__init__.py'
    'backend/tests/unit/domain/test_source_exports.py'
)
Invoke-CheckedPowerShell -ArgumentList @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', 'scripts/scan_secrets.ps1', '-PythonExe', $PythonExe, '--staged')
$currentTree = Get-CheckedIndexTree
if ($env:PROJECTB_REVIEWED_TREE -notmatch '^[0-9a-f]{40}$' -or
    $currentTree -ne $env:PROJECTB_REVIEWED_TREE) {
    throw 'T-02B2B index tree changed after review; both reviews are invalid'
}
```

Expected: exit code 0 only when the immediately pre-commit tree equals the tree reviewed by both reviewers.

- [ ] **Step B2B-20: Commit T-02B2B with the validated worker identity**

Run:

```powershell
Invoke-CheckedNative -FilePath $GitExe -ArgumentList @(
    'commit', '-m',
    "feat(T-02B2B): publish source model facade [agent: $env:PROJECTB_AGENT_ID]"
)
if ($LASTEXITCODE -ne 0) {
    throw 'T-02B2B commit failed'
}
$committedTree = @(Invoke-CheckedNative -FilePath $GitExe -ArgumentList @(
    'rev-parse', 'HEAD^{tree}'
))
if ($committedTree.Count -ne 1 -or
    $committedTree[0].Trim() -ne $env:PROJECTB_REVIEWED_TREE) {
    throw 'T-02B2B committed tree differs from the reviewed tree'
}
```

Expected: exit code 0 and a `feat(T-02B2B)` commit subject containing the reviewed worker identity.

- [ ] **Step B2B-21: Capture the T-02B2B commit hash**

Run:

```powershell
$commitHash = @(Invoke-CheckedNative -FilePath $GitExe -ArgumentList @(
    'rev-parse', 'HEAD'
))
if ($LASTEXITCODE -ne 0) {
    throw 'T-02B2B hash capture failed'
}
if ($commitHash.Count -ne 1 -or $commitHash[0] -notmatch '^[0-9a-f]{40}$') {
    throw 'T-02B2B hash must be one lowercase 40-character hexadecimal value'
}
$commitHash[0]
```

Expected: exit code 0 with one observed 40-character lowercase hexadecimal commit hash. The coordinator records this hash and both reviewer identities/outcomes before creating the T-02C worktree from it.

**T-02B2B completion standard:** The focused export and cumulative domain commands exit 0, Ruff/mypy/full-entry/worktree-and-index scanners exit 0, two independent fresh reviewers report PASS, the automatic two-path staged-set assertion exits 0, and the identity-bound commit/hash is recorded. No T-02C work begins before that evidence is recorded.

### Task T-02C: Unique-Page Proof and Final Source Facade

**Goal:** Prove a normalized remote chunk belongs to exactly one page of one raw file and publish that proof through the final `projectb.domain.source` facade.

**Dependencies / parallelism:** Start a new worktree from the reviewed T-02B2B commit. T-02C owns `proof.py`, the proof test, the final-facade test, and the one declared sequential modification to the B2B-owned facade. No other task edits `domain/source/__init__.py` concurrently.

**Files:**
- Create: `backend/src/projectb/domain/source/proof.py`
- Modify: `backend/src/projectb/domain/source/__init__.py`
- Create: `backend/tests/unit/domain/test_source_proof.py`
- Modify: `backend/tests/unit/domain/test_source_exports.py`

**Produced interfaces:** immutable `PageText`, `MINIMUM_NORMALIZED_CODE_POINTS = 32`, and `prove_unique_pdf_page(chunk: str, pages: Sequence[PageText], material_id: MaterialId, content_hash: str) -> PdfPageLocator | SourceInsufficient`, all exported through the final source facade. The `pages` argument is the complete ordered directory for one verified raw file: its page numbers must be exactly `1..len(pages)`, so a returned locator is necessarily within the represented page count without adding a fifth argument.

- [ ] **Step C0: Establish the complete T-02C runtime, base, worktree, and ownership prelude**

Execute the complete Runtime and Evidence Contract block above in this fresh T-02C shell, then run:

```powershell
Initialize-DomainUnit -ExpectedUnitId 'T-02C' -ExpectedPaths @(
    'backend/src/projectb/domain/source/__init__.py'
    'backend/src/projectb/domain/source/proof.py'
    'backend/tests/unit/domain/test_source_exports.py'
    'backend/tests/unit/domain/test_source_proof.py'
)
```

Expected: exit code 0 only for the clean T-02C worktree at the reviewed T-02B2B base with the exact four-path proof/facade ownership scope.

- [ ] **Step C1A: Create the failing PageText member-validation tests**

Create `backend/tests/unit/domain/test_source_proof.py` with this exact first slice:

```python
import pytest

from projectb.domain.errors import (
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


@pytest.mark.parametrize(
    ("field", "value", "code"),
    [
        ("material_id", MaterialId(""), SourceErrorCode.INVALID_ID),
        ("material_id", 1, SourceErrorCode.INVALID_SHAPE),
        ("content_hash", "A" * 64, SourceErrorCode.INVALID_CONTENT_HASH),
        ("content_hash", b"a" * 64, SourceErrorCode.INVALID_SHAPE),
        ("page", 0, SourceErrorCode.INVALID_PAGE),
        ("page", True, SourceErrorCode.INVALID_PAGE),
        ("text", 1, SourceErrorCode.INVALID_SHAPE),
    ],
)
def test_page_text_rejects_invalid_runtime_members(
    field: str,
    value: object,
    code: SourceErrorCode,
) -> None:
    values: dict[str, object] = {
        "material_id": MATERIAL_ID,
        "content_hash": HASH,
        "page": 1,
        "text": UNIQUE_SPAN,
    }
    values[field] = value
    with pytest.raises(SourceContractError) as caught:
        PageText(**values)
    assert caught.value.code is code
```

- [ ] **Step C1B: Append the failing proof container and chunk tests**

Append exactly to `backend/tests/unit/domain/test_source_proof.py`:

```python


@pytest.mark.parametrize("pages", [None, True, "page text"])
def test_proof_rejects_non_sequence_and_string_page_containers(pages: object) -> None:
    with pytest.raises(SourceContractError) as caught:
        prove_unique_pdf_page(UNIQUE_SPAN, pages, MATERIAL_ID, HASH)
    assert caught.value.code is SourceErrorCode.INVALID_CATALOG


def test_proof_rejects_a_foreign_page_member() -> None:
    with pytest.raises(SourceContractError) as caught:
        prove_unique_pdf_page(UNIQUE_SPAN, (object(),), MATERIAL_ID, HASH)
    assert caught.value.code is SourceErrorCode.INVALID_CATALOG


def test_proof_rejects_a_non_string_chunk() -> None:
    with pytest.raises(SourceContractError) as caught:
        prove_unique_pdf_page(1, (page(1, UNIQUE_SPAN),), MATERIAL_ID, HASH)
    assert caught.value.code is SourceErrorCode.INVALID_SHAPE


@pytest.mark.parametrize(
    ("material_id", "content_hash"),
    [(1, HASH), (MATERIAL_ID, b"a" * 64)],
)
def test_proof_rejects_invalid_identity_argument_types(
    material_id: object,
    content_hash: object,
) -> None:
    with pytest.raises(SourceContractError) as caught:
        prove_unique_pdf_page(
            UNIQUE_SPAN,
            (page(1, UNIQUE_SPAN),),
            material_id,
            content_hash,
        )
    assert caught.value.code is SourceErrorCode.INVALID_SHAPE
```

- [ ] **Step C2: Append the failing unique-span and length-boundary tests**

Append exactly to `backend/tests/unit/domain/test_source_proof.py`:

```python


def test_unique_normalized_span_maps_to_one_page() -> None:
    pages = (
        page(1, "unrelated preface"),
        page(
            2,
            "Header shared counter\r\nupdate needs one criti\u00adcal section footer",
        ),
    )
    assert prove_unique_pdf_page(UNIQUE_SPAN, pages, MATERIAL_ID, HASH) == (
        PdfPageLocator(MATERIAL_ID, HASH, 2)
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

- [ ] **Step C3: Append the failing ambiguity and no-match tests**

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


def test_empty_page_sequence_has_no_match() -> None:
    assert prove_unique_pdf_page(UNIQUE_SPAN, (), MATERIAL_ID, HASH) == (
        SourceInsufficient(SourceInsufficientReason.NO_MATCH)
    )
```

- [ ] **Step C4: Append the failing complete-page-directory and binding tests**

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
    "pages",
    [
        (page(999, UNIQUE_SPAN),),
        (page(1, "first"), page(3, UNIQUE_SPAN)),
        (page(2, UNIQUE_SPAN), page(1, "first")),
    ],
)
def test_page_directory_must_be_complete_contiguous_and_ordered(
    pages: tuple[PageText, ...],
) -> None:
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

- [ ] **Step C5: Run the proof test file and capture red evidence**

Run:

```powershell
$env:PYTHONPATH = (Resolve-Path 'backend/src').Path
Invoke-ExpectedNativeExit -FilePath $PythonExe -ExpectedExitCode 2 -ArgumentList @(
    '-m', 'pytest', '-c', 'backend/pyproject.toml',
    'backend/tests/unit/domain/test_source_proof.py', '-q'
)
```

Expected: exit code 2 with a collection error because `projectb.domain.source.proof` does not exist; no proof test passes.

- [ ] **Step C6: Implement immutable PageText input validation**

Create `backend/src/projectb/domain/source/proof.py` with this exact first slice:

```python
from collections.abc import Sequence
from dataclasses import dataclass

from projectb.domain.errors import (
    SourceContractError,
    SourceErrorCode,
    SourceInsufficient,
    SourceInsufficientReason,
)
from projectb.domain.source.hashing import normalize_source_text
from projectb.domain.source.models import PdfPageLocator
from projectb.domain.types import (
    MaterialId,
    validate_content_hash,
    validate_opaque_id,
)

MINIMUM_NORMALIZED_CODE_POINTS = 32


@dataclass(frozen=True, slots=True)
class PageText:
    material_id: MaterialId
    content_hash: str
    page: int
    text: str

    def __post_init__(self) -> None:
        material_id_value: object = self.material_id
        content_hash_value: object = self.content_hash
        page_value: object = self.page
        text_value: object = self.text
        validate_opaque_id(material_id_value)
        validate_content_hash(content_hash_value)
        if type(page_value) is not int or page_value < 1:
            raise SourceContractError(SourceErrorCode.INVALID_PAGE)
        if not isinstance(text_value, str):
            raise SourceContractError(SourceErrorCode.INVALID_SHAPE)
```

- [ ] **Step C7: Append deterministic four-argument unique-page proof**

Append exactly to `backend/src/projectb/domain/source/proof.py`:

```python


def prove_unique_pdf_page(
    chunk: str,
    pages: Sequence[PageText],
    material_id: MaterialId,
    content_hash: str,
) -> PdfPageLocator | SourceInsufficient:
    chunk_value: object = chunk
    pages_value: object = pages
    material_id_value: object = material_id
    content_hash_value: object = content_hash
    if not isinstance(chunk_value, str):
        raise SourceContractError(SourceErrorCode.INVALID_SHAPE)
    validated_material_id = MaterialId(validate_opaque_id(material_id_value))
    validated_content_hash = validate_content_hash(content_hash_value)
    if isinstance(pages_value, (str, bytes, bytearray)) or not isinstance(
        pages_value,
        Sequence,
    ):
        raise SourceContractError(SourceErrorCode.INVALID_CATALOG)
    page_list: list[PageText] = []
    for page_value in pages_value:
        if not isinstance(page_value, PageText):
            raise SourceContractError(SourceErrorCode.INVALID_CATALOG)
        page_list.append(page_value)
    page_records = tuple(page_list)
    for page in page_records:
        if page.material_id != validated_material_id:
            raise SourceContractError(SourceErrorCode.INVALID_CATALOG)
        if page.content_hash != validated_content_hash:
            raise SourceContractError(SourceErrorCode.STALE_CONTENT_HASH)
    page_numbers = [page.page for page in page_records]
    if page_numbers != list(range(1, len(page_records) + 1)):
        raise SourceContractError(SourceErrorCode.INVALID_CATALOG)
    normalized_chunk = normalize_source_text(chunk_value)
    if len(normalized_chunk) < MINIMUM_NORMALIZED_CODE_POINTS:
        return SourceInsufficient(SourceInsufficientReason.TOO_SHORT)
    matches = tuple(
        page.page
        for page in page_records
        if normalized_chunk in normalize_source_text(page.text)
    )
    if not matches:
        return SourceInsufficient(SourceInsufficientReason.NO_MATCH)
    if len(matches) != 1:
        return SourceInsufficient(SourceInsufficientReason.AMBIGUOUS)
    return PdfPageLocator(
        material_id=validated_material_id,
        content_hash=validated_content_hash,
        page=matches[0],
    )


__all__ = [
    "MINIMUM_NORMALIZED_CODE_POINTS",
    "PageText",
    "prove_unique_pdf_page",
]
```

- [ ] **Step C8: Run all proof tests green**

Run:

```powershell
$env:PYTHONPATH = (Resolve-Path 'backend/src').Path
Invoke-CheckedPython -ArgumentList @('-m', 'pytest', '-c', 'backend/pyproject.toml', 'backend/tests/unit/domain/test_source_proof.py', '-q')
```

Expected: exit code 0; every PageText, public-argument, proof-boundary, and unique-page assertion passes. Record the observed result without a fixed count.

- [ ] **Step C9: Replace the B-stage export test with the failing final-facade test**

Replace `backend/tests/unit/domain/test_source_exports.py` with exactly:

```python
from projectb.domain import source
from projectb.domain.source import (
    PageText,
    PdfPageLocator,
    prove_unique_pdf_page,
    raw_file_content_hash,
    source_locator_from_mapping,
)
from projectb.domain.types import MaterialId


def test_source_facade_exports_the_complete_downstream_contract() -> None:
    assert source.__all__ == [
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
    material_id = MaterialId("material-1")
    content_hash = raw_file_content_hash(b"source")
    locator = source_locator_from_mapping(
        {
            "kind": "pdf_page",
            "material_id": material_id,
            "content_hash": content_hash,
            "page": 1,
        }
    )
    assert locator == PdfPageLocator(material_id, content_hash, 1)
    assert prove_unique_pdf_page(
        "x" * 32,
        (
            PageText(
                material_id=material_id,
                content_hash=content_hash,
                page=1,
                text="x" * 32,
            ),
        ),
        material_id,
        content_hash,
    ) == locator
```

- [ ] **Step C10: Run the final-facade test and capture red evidence**

Run:

```powershell
$env:PYTHONPATH = (Resolve-Path 'backend/src').Path
Invoke-ExpectedNativeExit -FilePath $PythonExe -ExpectedExitCode 2 -ArgumentList @(
    '-m', 'pytest', '-c', 'backend/pyproject.toml',
    'backend/tests/unit/domain/test_source_exports.py', '-q'
)
```

Expected: exit code 2 with a collection error containing `cannot import name 'PageText' from 'projectb.domain.source'`; no facade test passes.

- [ ] **Step C11: Replace the B-stage facade with the complete proof facade**

Replace `backend/src/projectb/domain/source/__init__.py` with exactly:

```python
"""Validated local source contracts."""

from projectb.domain.errors import (
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

- [ ] **Step C12: Run all T-02C focused tests green**

Run:

```powershell
$env:PYTHONPATH = (Resolve-Path 'backend/src').Path
Invoke-CheckedPython -ArgumentList @('-m', 'pytest', '-c', 'backend/pyproject.toml', 'backend/tests/unit/domain/test_source_proof.py', 'backend/tests/unit/domain/test_source_exports.py', '-q')
```

Expected: exit code 0; every T-02C proof and final-facade assertion passes.

- [ ] **Step C13: Format only the T-02C files under green tests**

Run:

```powershell
Invoke-CheckedPython -ArgumentList @('-m', 'ruff', 'format', '--config', 'backend/pyproject.toml', 'backend/src/projectb/domain/source/proof.py', 'backend/src/projectb/domain/source/__init__.py', 'backend/tests/unit/domain/test_source_proof.py', 'backend/tests/unit/domain/test_source_exports.py')
```

Expected: exit code 0; Ruff reports all four files formatted or already formatted and changes no behavior.

- [ ] **Step C14: Re-run T-02C focused tests after refactoring**

Run:

```powershell
$env:PYTHONPATH = (Resolve-Path 'backend/src').Path
Invoke-CheckedPython -ArgumentList @('-m', 'pytest', '-c', 'backend/pyproject.toml', 'backend/tests/unit/domain/test_source_proof.py', 'backend/tests/unit/domain/test_source_exports.py', '-q')
```

Expected: exit code 0; formatting changed no T-02C behavior.

- [ ] **Step C15: Run the complete cumulative domain suite**

Run:

```powershell
$env:PYTHONPATH = (Resolve-Path 'backend/src').Path
Invoke-CheckedPython -ArgumentList @('-m', 'pytest', '-c', 'backend/pyproject.toml', 'backend/tests/unit/domain', '-q')
```

Expected: exit code 0; the complete domain suite available at the C checkpoint passes. Record the observed result without a fixed count.

- [ ] **Step C16: Run Ruff with the locked backend configuration**

Run:

```powershell
Invoke-CheckedPython -ArgumentList @('-m', 'ruff', 'check', '--config', 'backend/pyproject.toml', 'backend/src/projectb/domain', 'backend/tests/unit/domain')
```

Expected: exit code 0 with `All checks passed!`.

- [ ] **Step C17: Run mypy with the locked backend configuration**

Run:

```powershell
$env:PYTHONPATH = (Resolve-Path 'backend/src').Path
Invoke-CheckedPython -ArgumentList @('-m', 'mypy', '--config-file', 'backend/pyproject.toml', 'backend/src/projectb/domain')
```

Expected: exit code 0 with no issues in the complete T-02 domain source contract.

- [ ] **Step C18: Run the repository one-command verification entry**

Run:

```powershell
Invoke-CheckedPython -ArgumentList @('scripts/test_all.py')
```

Expected: exit code 0; every active canonical gate passes, the frontend build and scanner succeed, and later owner gates remain explicitly unavailable rather than PASS. Record the observed gate summary.

- [ ] **Step C19: Run the project secret scanner separately**

Run:

```powershell
Invoke-CheckedPowerShell -ArgumentList @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', 'scripts/scan_secrets.ps1', '-PythonExe', $PythonExe)
```

Expected: exit code 0 with no credential finding and no file-content disclosure.

- [ ] **Step C20: Validate the fresh T-02C worker identity**

Run:

```powershell
if ([string]::IsNullOrWhiteSpace($env:PROJECTB_AGENT_ID)) {
    throw 'PROJECTB_AGENT_ID must identify the fresh T-02C worker'
}
if ($env:PROJECTB_AGENT_ID -notmatch '^[A-Za-z0-9][A-Za-z0-9._-]{1,63}$') {
    throw 'PROJECTB_AGENT_ID contains unsupported characters'
}
```

Expected: exit code 0; unset, blank, or malformed identities stop before staging and review.

- [ ] **Step C21: Stage exactly the T-02C ownership set**

Run:

```powershell
Invoke-CheckedNative -FilePath $GitExe -ArgumentList @(
    'add', '--',
    'backend/src/projectb/domain/source/proof.py',
    'backend/src/projectb/domain/source/__init__.py',
    'backend/tests/unit/domain/test_source_proof.py',
    'backend/tests/unit/domain/test_source_exports.py'
)
if ($LASTEXITCODE -ne 0) {
    throw 'T-02C git add failed'
}
```

Expected: exit code 0; only the four literal T-02C paths are added to the index.

- [ ] **Step C22: Check the staged T-02C patch**

Run:

```powershell
Invoke-CheckedNative -FilePath $GitExe -ArgumentList @('diff', '--cached', '--check')
if ($LASTEXITCODE -ne 0) {
    throw 'T-02C staged diff check failed'
}
```

Expected: exit code 0 with no output.

- [ ] **Step C23: Assert the exact staged T-02C path set**

Run:

```powershell
Assert-ExactStagedPaths -ExpectedPaths @(
    'backend/src/projectb/domain/source/__init__.py'
    'backend/src/projectb/domain/source/proof.py'
    'backend/tests/unit/domain/test_source_exports.py'
    'backend/tests/unit/domain/test_source_proof.py'
)
Invoke-CheckedPowerShell -ArgumentList @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', 'scripts/scan_secrets.ps1', '-PythonExe', $PythonExe, '--staged')
$env:PROJECTB_REVIEWED_TREE = Get-CheckedIndexTree
$env:PROJECTB_REVIEWED_TREE
```

Expected: exit code 0 and one lowercase 40-hex index tree ID. A missing, extra, renamed, or unstaged path blocks review before tree capture.

- [ ] **Step C24: Request the fresh T-02C SPEC review**

The coordinator gives a fresh non-worker reviewer the complete packet, requires `REVIEWED TREE: $env:PROJECTB_REVIEWED_TREE` in the review record, and records the reviewer's canonical identity in `$env:PROJECTB_SPEC_REVIEWER_ID`. Match the root T-02C scope exactly: check AC-03 and AC-37 against SPEC §3 X2 rule 4. The exact four-argument signature includes `material_id` and `content_hash`; `pages` is a complete ordered page directory numbered exactly `1..N`; and a v1-normalized chunk has at least 32 code points and continuously matches exactly one page bound to that material/hash. Duplicate, sparse, out-of-order, out-of-range, wrong-material, and stale-hash directories fail with stable catalog errors; zero matches, multiple matches, cross-page spans, too-short chunks, and visual-only cases return `source_insufficient`. The unit supplies prerequisites and does not claim source opening/display, File Search request filtering, result allowlisting, or end-to-end completion of AC-03/AC-37.

Expected: `SPEC REVIEW: PASS` bound to the captured tree ID. Any edit invalidates both reviews and repeats Steps C21-C25 with a newly captured tree.

- [ ] **Step C25: Request the different fresh T-02C quality review**

The coordinator gives the complete packet with the same `REVIEWED TREE: $env:PROJECTB_REVIEWED_TREE` binding to a second fresh reviewer and records that reviewer's canonical identity in `$env:PROJECTB_QUALITY_REVIEWER_ID`. This reviewer must differ from the worker and SPEC reviewer and checks PageText/pages container/member validation, string-sequence rejection, exact contiguous `1..N` directory validation, duplicate/sparse/out-of-order page handling, proof-result page bounds, hash/material binding, deterministic normalization, facade type consistency, error redaction, B010/UP040, standard-library-only production code, tests, and dependency/license impact.

Expected: `QUALITY REVIEW: PASS` bound to the same tree ID. Any finding or edit invalidates both reviews and repeats Steps C21-C25.

- [ ] **Step C26: Validate the three T-02C identities are non-empty and distinct**

Run:

```powershell
$identities = @(
    $env:PROJECTB_AGENT_ID
    $env:PROJECTB_SPEC_REVIEWER_ID
    $env:PROJECTB_QUALITY_REVIEWER_ID
)
foreach ($identity in $identities) {
    if ([string]::IsNullOrWhiteSpace($identity)) {
        throw 'T-02C worker and reviewer identities must all be non-empty'
    }
    if ($identity -notmatch '^[A-Za-z0-9][A-Za-z0-9._-]{1,63}$') {
        throw 'T-02C worker or reviewer identity contains unsupported characters'
    }
}
if (($identities | Sort-Object -Unique).Count -ne 3) {
    throw 'T-02C worker, SPEC reviewer, and quality reviewer must be distinct'
}
```

Expected: exit code 0 with three valid pairwise-distinct identities.

- [ ] **Step C27: Recheck the reviewed staged patch**

Run:

```powershell
Invoke-CheckedNative -FilePath $GitExe -ArgumentList @('diff', '--cached', '--check')
if ($LASTEXITCODE -ne 0) {
    throw 'T-02C reviewed staged diff check failed'
}
Assert-ExactStagedPaths -ExpectedPaths @(
    'backend/src/projectb/domain/source/__init__.py'
    'backend/src/projectb/domain/source/proof.py'
    'backend/tests/unit/domain/test_source_exports.py'
    'backend/tests/unit/domain/test_source_proof.py'
)
Invoke-CheckedPowerShell -ArgumentList @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', 'scripts/scan_secrets.ps1', '-PythonExe', $PythonExe, '--staged')
$currentTree = Get-CheckedIndexTree
if ($env:PROJECTB_REVIEWED_TREE -notmatch '^[0-9a-f]{40}$' -or
    $currentTree -ne $env:PROJECTB_REVIEWED_TREE) {
    throw 'T-02C index tree changed after review; both reviews are invalid'
}
```

Expected: exit code 0 only when the immediately pre-commit tree equals the tree reviewed by both reviewers.

- [ ] **Step C28: Commit T-02C with the validated worker identity**

Run:

```powershell
Invoke-CheckedNative -FilePath $GitExe -ArgumentList @(
    'commit', '-m',
    "feat(T-02C): add unique-page source proof [agent: $env:PROJECTB_AGENT_ID]"
)
if ($LASTEXITCODE -ne 0) {
    throw 'T-02C commit failed'
}
$committedTree = @(Invoke-CheckedNative -FilePath $GitExe -ArgumentList @(
    'rev-parse', 'HEAD^{tree}'
))
if ($committedTree.Count -ne 1 -or
    $committedTree[0].Trim() -ne $env:PROJECTB_REVIEWED_TREE) {
    throw 'T-02C committed tree differs from the reviewed tree'
}
```

Expected: exit code 0 and a `feat(T-02C)` commit subject containing the reviewed worker identity.

- [ ] **Step C29: Capture the T-02C commit hash**

Run:

```powershell
$commitHash = @(Invoke-CheckedNative -FilePath $GitExe -ArgumentList @(
    'rev-parse', 'HEAD'
))
if ($LASTEXITCODE -ne 0) {
    throw 'T-02C hash capture failed'
}
if ($commitHash.Count -ne 1 -or $commitHash[0] -notmatch '^[0-9a-f]{40}$') {
    throw 'T-02C hash must be one lowercase 40-character hexadecimal value'
}
$commitHash[0]
```

Expected: exit code 0 with one 40-character lowercase hexadecimal commit hash. The coordinator records this hash and both reviewer identities/outcomes before allowing downstream T-03/M1/M2/M3/X2 work to consume the facade.

**T-02C completion standard:** The focused and cumulative domain commands exit 0 with every declared proof/facade assertion, including complete ordered `1..N` page-directory enforcement, Ruff/mypy/full-entry/scanner exit 0, two independent fresh reviewers report PASS, the automatic four-path staged-set assertion exits 0, and the identity-bound commit/hash is recorded. The final facade exposes the exact four locator branches and the four-argument proof without provider, parser, database, network, UI, or private courseware dependencies.

## Execution Handoff

After the coordinator passes the same-snapshot Integration Gate, execute this plan with `superpowers:subagent-driven-development` in the strict chain `T-01F3 -> T-02A -> T-02B1 -> T-02B2A -> T-02B2B -> T-02C`. Dispatch one fresh implementation subagent per unit, complete both fresh reviews, record the commit/hash, and only then create the next unit's worktree from that reviewed commit. Do not dispatch these units in parallel and do not use a unit's worker as either reviewer for that unit.
