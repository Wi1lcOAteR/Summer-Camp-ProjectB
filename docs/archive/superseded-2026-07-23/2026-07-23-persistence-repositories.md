# Persistence Repositories Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the owner-scoped, restart-safe SQLite persistence boundary for ProjectB as three strictly sequential dispatch units covering schema migration, course/material version history, and learning/remote/tombstone history.

**Architecture:** T-03A is the sole migration owner and publishes `Database`, stable repository errors, strict canonical JSON, and every table later T-03/T-08/M1/M2/M3/X2 work may consume. T-03B and T-03C add repository behavior without changing the migration: immutable version rows are append-only, current rows use optimistic versions, all reads enforce owner scope, and tombstones retain only non-reconstructive metadata.

**Tech Stack:** CPython 3.14.6 standard library (`contextlib`, `dataclasses`, `datetime`, `json`, `pathlib`, `sqlite3`, `typing`), SQLite from CPython with foreign keys and STRICT tables, pytest 9.1.1, Ruff 0.15.22, and mypy 2.3.0 from the reviewed T-01 environment.

---

## Status and Dispatch Boundary

This plan covers exactly root dispatch units `T-03A`, `T-03B`, and `T-03C` under the non-dispatchable root Task Group `T-03`. It does not cover T-02, T-04, T-08, M1, M2, M3, X2, API, UI, CI, process gates, or coordinator ledger updates. It changes no production file during Stage B and records no test, review, or commit as executed.

This revision is bound to root `PLAN.md` SHA-256 `4BCFE8470DE57C0DD54004935285CAAD5CD9D1AFF0AA7370CC4E098887745F08` and predecessor detailed-plan SHA-256 `2F67280FED1C7F5337837B5CB08E9099F09D5236A19B124B2D3C007C301B8810`. Those hashes identify the authoring inputs, not implementation evidence or a review PASS.

**Required root amendment, deliberately not performed here:** the bound root T-03C `Reviews` row lists only AC-06, AC-07, AC-17, AC-30, AC-35, and AC-40 even though T-03C also owns persistence behavior needed by AC-25, AC-26, AC-27, AC-28, AC-29, AC-31, and AC-50. Before this detailed plan may receive a Stage-B PASS or enter cold-start validation, the coordinator must amend root T-03C to require the exact set `AC-06, AC-07, AC-17, AC-25, AC-26, AC-27, AC-28, AC-29, AC-30, AC-31, AC-35, AC-40, AC-50`, re-freeze root `PLAN.md`, and review this plan against that new root hash. This plan neither edits nor silently overrides the authoritative root ledger.

Dispatch remains prohibited until the complete formal plan set has passed review, G-03 cold-start validation has completed, the student has approved implementation, and G-04 has created the unit worktree. At execution time three different fresh workers run strictly in this order:

```text
reviewed T-02C commit -> T-03A -> reviewed T-03A commit -> T-03B
                    -> reviewed T-03B commit -> T-03C
```

Each worker receives the complete confirmed `SPEC.md`, current root `PLAN.md`, this complete plan, the reviewed predecessor commit, and only that unit's ownership list. After the worker reaches a staged green patch, two other fresh sessions perform the SPEC and quality reviews. The worker, SPEC reviewer, and quality reviewer must be three non-empty, pairwise-distinct identities. No T-03B worktree is created before T-03A's commit and reviews are recorded; no T-03C worktree is created before T-03B's commit and reviews are recorded.

## Exact Path Ownership Map

| Unit | Exact owned paths | Ownership rule |
| --- | --- | --- |
| T-03A | `backend/src/projectb/infrastructure/sqlite.py`; `backend/src/projectb/infrastructure/migrations/001_initial.sql`; `backend/tests/integration/test_sqlite_schema.py` | Sole migration owner. No other unit in this plan may edit these paths. |
| T-03B | `backend/src/projectb/infrastructure/repositories/course_repo.py`; `backend/src/projectb/infrastructure/repositories/material_repo.py`; `backend/tests/integration/test_course_material_repositories.py` | Consumes T-03A schema. It creates no migration and no learning/remote behavior. |
| T-03C | `backend/src/projectb/infrastructure/repositories/learning_repo.py`; `backend/src/projectb/infrastructure/repositories/remote_repo.py`; `backend/tests/integration/test_learning_remote_repositories.py` | Consumes the reviewed T-03A schema. A missing column/table blocks the unit and returns to a separately reviewed migration-owner task. |

The three sets are pairwise disjoint. Later serialized handoffs are outside this plan: `material_repo.py` passes from T-03B to M1-02B/M1-02C/M1-04; `learning_repo.py` passes from T-03C to M3-02B; `remote_repo.py` passes from T-03C to X2-03A/B/C and then M1-04. Those later owners may extend repository methods but must not edit `001_initial.sql` without a new coordinator-approved migration unit.

## Locked Public Contracts

T-03 consumes the reviewed T-02C terminal facade and does not redefine it. Material persistence accepts the exact T-02A `SelectedFile`, `MaterialRole`, `MaterialReviewState`, `CourseId`, `MaterialId`, and raw 64-character lowercase content hash contracts. Source locators remain serialized only by their later domain owner; T-03 does not invent a second locator representation.

`backend/src/projectb/infrastructure/sqlite.py` publishes:

```python
type RepositoryErrorCode = Literal[
    "state_inconsistent",
    "owner_forbidden",
    "not_found",
]

class RepositoryError(RuntimeError):
    code: RepositoryErrorCode

class Database:
    @classmethod
    def open(cls, path: Path) -> "Database": ...
    def migrate(self) -> None: ...
    def transaction(self) -> Iterator[None]: ...
    def close(self) -> None: ...

def canonical_json(payload: Mapping[str, object]) -> str: ...
def parse_json_object(raw: str) -> dict[str, JsonValue]: ...
```

The ellipses above document signatures only; the executable task below supplies the complete implementation and contains no ellipsis token. `RepositoryError` exposes only one of the three stable codes. SQLite messages, SQL text, paths, payload values, provider references, and owner IDs are never copied into its public message.

Canonical JSON is UTF-8 JSON text with sorted object keys, compact separators, `ensure_ascii=False`, and `allow_nan=False`. It converts non-string sequences to arrays, rejects non-string/blank keys, non-finite floats, unsupported objects, and any nested key exactly equal (case-insensitively) to `api_key`, `token`, `secret`, `password`, `credential`, `credential_value`, `local_path`, `path`, `body`, `course_body`, `audit_body`, `answer`, `answer_text`, `provider_object_id`, or `provider_file_id`. `scope_token`, `credential_ref`, opaque storage references, hashes, IDs, reason codes, and whitelisted metadata remain legal because they are not secret values or reconstructive body fields.

Every repository timestamp accepts only the canonical 20-byte UTC form `YYYY-MM-DDTHH:MM:SSZ`. Offsets, fractional seconds, missing seconds, lowercase separators, unpadded components, impossible dates, and booleans/non-strings are `state_inconsistent`; this makes lexical timestamp ordering deterministic.

## Locked Schema Contract

`001_initial.sql` creates these STRICT tables: `schema_migrations`, `courses`, `course_versions`, `materials`, `material_versions`, `material_batches`, `material_batch_files`, `material_units`, `authority_records`, `authority_versions`, `attempts`, `consent_records`, `learning_evidence`, `learning_plan_revisions`, `remote_objects`, `remote_object_versions`, `remote_jobs`, `remote_job_versions`, `durable_jobs`, `tombstones`, and `audit_events`. Every authoritative table has `owner_id`; course-bound rows carry `course_id`; append-only tables have update/delete denial triggers. The schema contains no local path, course body, answer, API key, credential value, secret, or audit body column.

`material_units` and `durable_jobs` are schema reservations only in T-03. M1 owns parsed-unit persistence behavior and T-08 owns durable-job claim/lease/progress behavior. T-03B exposes only batch creation, file membership, and file-state persistence; it never reads files or invokes a parser. T-03C exposes only protected Attempt references and immutable reads; it never stores an answer or evaluates one. `authority_records`/`authority_versions` reserve versioned storage for later confirmed coverage, mastery, review-goal, review-task, and study-focus entities without allowing later feature workers to silently add a migration. No T-03 repository exposes arbitrary SQL or arbitrary table names.

## Task T-03A: Idempotent SQLite Schema and Migration Boundary

**Goal:** Create the only initial migration, the database transaction wrapper, stable repository errors, and strict serialization primitives.

**Dependencies / parallelism:** Requires the reviewed T-02C commit. Runs alone. T-03B and T-03C wait for both reviews and the recorded T-03A commit.

**Files:**
- Create: `backend/src/projectb/infrastructure/sqlite.py`
- Create: `backend/src/projectb/infrastructure/migrations/001_initial.sql`
- Create: `backend/tests/integration/test_sqlite_schema.py`

- [ ] **Step A1: Validate the T-03A runtime, identity, base commit, and exact worktree**

Run exactly from the T-03A worktree:

```powershell
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Test-AbsoluteExistingLeaf {
    param([Parameter(Mandatory)][string]$Value)
    if ([string]::IsNullOrWhiteSpace($Value) -or
        $Value -notmatch '^(?:[A-Za-z]:[\\/]|\\\\[^\\/]+[\\/][^\\/]+[\\/])') {
        return $false
    }
    try { $null = [IO.Path]::GetFullPath($Value) } catch { return $false }
    return Test-Path -LiteralPath $Value -PathType Leaf
}

if (-not ('ProjectBProcessTree' -as [type])) {
    Add-Type -TypeDefinition @'
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Runtime.InteropServices;
public static class ProjectBProcessTree {
    [StructLayout(LayoutKind.Sequential)] struct BasicInfo {
        public IntPtr Reserved1, Peb, Reserved20, Reserved21, ProcessId, ParentProcessId;
    }
    [DllImport("ntdll.dll")] static extern int NtQueryInformationProcess(
        IntPtr handle, int kind, ref BasicInfo info, int length, out int returned);
    public static int[] Descendants(int root) {
        var map = new Dictionary<int, List<int>>();
        foreach (var process in Process.GetProcesses()) {
            try {
                var info = new BasicInfo(); int returned;
                if (NtQueryInformationProcess(process.Handle, 0, ref info,
                    Marshal.SizeOf(typeof(BasicInfo)), out returned) != 0) continue;
                int parent = info.ParentProcessId.ToInt32();
                if (!map.ContainsKey(parent)) map[parent] = new List<int>();
                map[parent].Add(process.Id);
            } catch { } finally { process.Dispose(); }
        }
        var result = new List<int>(); var queue = new Queue<int>(); queue.Enqueue(root);
        while (queue.Count > 0) {
            int parent = queue.Dequeue(); List<int> children;
            if (!map.TryGetValue(parent, out children)) continue;
            foreach (int child in children) { result.Add(child); queue.Enqueue(child); }
        }
        return result.ToArray();
    }
}
'@
}

```

- [ ] **Step A1.1: Define bounded non-privileged process-tree cleanup**

Continue in the same checked PowerShell session:

```powershell
function Stop-NativeProcessTree {
    param([Parameter(Mandatory)][Diagnostics.Process]$Process)
    $rootId = $Process.Id
    $descendants = @([ProjectBProcessTree]::Descendants($rootId))
    Stop-Process -Id $rootId -Force -ErrorAction SilentlyContinue
    $descendants += @([ProjectBProcessTree]::Descendants($rootId))
    $targets = @($descendants | Sort-Object -Unique)
    if ($targets -contains $PID) { throw 'native timeout tree included the host process' }
    [array]::Reverse($targets)
    foreach ($target in $targets) {
        Stop-Process -Id $target -Force -ErrorAction SilentlyContinue
    }
    $deadline = [Diagnostics.Stopwatch]::StartNew()
    do {
        $alive = @(@($rootId) + $targets | Where-Object {
            Get-Process -Id $_ -ErrorAction SilentlyContinue
        })
        if ($alive.Count -gt 0) { Start-Sleep -Milliseconds 25 }
    } while ($alive.Count -gt 0 -and $deadline.ElapsedMilliseconds -lt 5000)
    if ($alive.Count -gt 0) { throw 'native command timeout cleanup failed' }
}

function ConvertTo-NativeArgument {
    param([Parameter(Mandatory)][AllowEmptyString()][string]$Value)
    if ($Value.Length -gt 0 -and $Value -notmatch '[\s"]') { return $Value }
    $builder = [Text.StringBuilder]::new()
    [void]$builder.Append('"')
    $slashes = 0
    foreach ($character in $Value.ToCharArray()) {
        if ($character -eq '\') { $slashes++; continue }
        if ($character -eq '"') {
            [void]$builder.Append(('\' * (($slashes * 2) + 1)))
            [void]$builder.Append('"')
            $slashes = 0
            continue
        }
        if ($slashes -gt 0) { [void]$builder.Append(('\' * $slashes)); $slashes = 0 }
        [void]$builder.Append($character)
    }
    if ($slashes -gt 0) { [void]$builder.Append(('\' * ($slashes * 2))) }
    [void]$builder.Append('"')
    return $builder.ToString()
}

```

- [ ] **Step A1.2: Define `Invoke-NativeProcess`**

Continue in the same checked PowerShell session:

```powershell
function Invoke-NativeProcess {
    param(
        [Parameter(Mandatory)][string]$FilePath,
        [Parameter(Mandatory)][AllowEmptyCollection()][AllowEmptyString()][string[]]$ArgumentList,
        [ValidateRange(1, 3600)][int]$TimeoutSeconds = 600
    )
    if (-not (Test-AbsoluteExistingLeaf -Value $FilePath)) {
        throw 'native executable must be an absolute existing leaf'
    }
    $start = [Diagnostics.ProcessStartInfo]::new()
    $start.FileName = $FilePath
    $start.Arguments = (($ArgumentList | ForEach-Object {
        ConvertTo-NativeArgument -Value $_
    }) -join ' ')
    $start.UseShellExecute = $false
    $start.CreateNoWindow = $true
    $start.RedirectStandardOutput = $true
    $start.RedirectStandardError = $true
    $process = [Diagnostics.Process]::new()
    $process.StartInfo = $start
    try {
        try {
            if (-not $process.Start()) { throw 'start returned false' }
        } catch {
            throw 'native command launch failed'
        }
        $stdoutTask = $process.StandardOutput.ReadToEndAsync()
        $stderrTask = $process.StandardError.ReadToEndAsync()
        if (-not $process.WaitForExit($TimeoutSeconds * 1000)) {
            Stop-NativeProcessTree -Process $process
            $process.WaitForExit()
            throw "native command timed out after $TimeoutSeconds seconds"
        }
        $process.WaitForExit()
        $stdout = $stdoutTask.Result.TrimEnd([char[]]"`r`n")
        $null = $stderrTask.Result
        $lines = if ($stdout.Length -eq 0) { @() } else { @($stdout -split "`r?`n") }
        return [pscustomobject]@{ ExitCode = $process.ExitCode; Stdout = $lines }
    } finally {
        $process.Dispose()
    }
}
```

- [ ] **Step A1.3: Define `Invoke-CheckedNative` through `Invoke-ExpectedNativeExit`**

Continue in the same checked PowerShell session:

```powershell

function Invoke-CheckedNative {
    param(
        [Parameter(Mandatory)][string]$FilePath,
        [Parameter(Mandatory)][AllowEmptyCollection()][AllowEmptyString()][string[]]$ArgumentList,
        [ValidateRange(1, 3600)][int]$TimeoutSeconds = 600
    )
    $result = Invoke-NativeProcess -FilePath $FilePath -ArgumentList $ArgumentList `
        -TimeoutSeconds $TimeoutSeconds
    if ($result.ExitCode -ne 0) {
        throw "native command failed with exit code $($result.ExitCode)"
    }
    return @($result.Stdout)
}

function Invoke-ExpectedNativeExit {
    param(
        [Parameter(Mandatory)][string]$FilePath,
        [Parameter(Mandatory)][AllowEmptyCollection()][AllowEmptyString()][string[]]$ArgumentList,
        [Parameter(Mandatory)][int]$ExpectedExitCode,
        [ValidateRange(1, 3600)][int]$TimeoutSeconds = 600
    )
    $result = Invoke-NativeProcess -FilePath $FilePath -ArgumentList $ArgumentList `
        -TimeoutSeconds $TimeoutSeconds
    if ($result.ExitCode -ne $ExpectedExitCode) {
        throw "native command returned unexpected exit code $($result.ExitCode)"
    }
    return @($result.Stdout)
}

$GitExe = (Get-Command git -CommandType Application -ErrorAction Stop).Source
if (-not (Test-AbsoluteExistingLeaf -Value $GitExe)) {
    throw 'git executable must be an absolute existing leaf'
}
$PythonExe = $env:PROJECTB_PYTHON_EXE
$PowerShellExe = $env:PROJECTB_POWERSHELL_EXE
foreach ($pair in @(@('Python', $PythonExe), @('PowerShell', $PowerShellExe))) {
    if (-not (Test-AbsoluteExistingLeaf -Value $pair[1])) {
        throw "$($pair[0]) executable must be an absolute existing leaf"
    }
}
```

- [ ] **Step A1.4: Define `Assert-NativeWrapperContract`**

Continue in the same checked PowerShell session:

```powershell
function Assert-NativeWrapperContract {
    param([Parameter(Mandatory)][string]$PythonPath)
    $empty = @(Invoke-CheckedNative -FilePath $PythonPath -ArgumentList @('-c', ''))
    if ($empty.Count -ne 0) { throw 'empty native output was not preserved' }
    $multiline = @(Invoke-CheckedNative -FilePath $PythonPath -ArgumentList @(
        '-c', "print('first'); print('second')"
    ))
    if ($multiline.Count -ne 2 -or $multiline[0] -ne 'first' -or
        $multiline[1] -ne 'second') {
        throw 'multiline native output was malformed'
    }
    $marker = 'sensitive-child-output-must-not-surface'
    $failure = $null
    try {
        Invoke-CheckedNative -FilePath $PythonPath -ArgumentList @(
            '-c', "import sys; print('$marker'); sys.exit(7)"
        ) -TimeoutSeconds 10
    } catch { $failure = $_.Exception.Message }
    if ($failure -ne 'native command failed with exit code 7' -or
        $failure.Contains($marker)) {
        throw 'nonzero diagnostics were not sanitized'
    }
    $wrongExecutable = (Resolve-Path -LiteralPath 'PLAN.md').Path
    $failure = $null
    try {
        Invoke-CheckedNative -FilePath $wrongExecutable -ArgumentList @() -TimeoutSeconds 10
    } catch { $failure = $_.Exception.Message }
    if ($failure -ne 'native command launch failed') {
        throw 'wrong executable did not fail closed'
    }
    $probeRoot = Join-Path ([IO.Path]::GetTempPath()) (
        'projectb-native-probe-' + [guid]::NewGuid().ToString('N')
    )
    [IO.Directory]::CreateDirectory($probeRoot) | Out-Null
    $pidFile = Join-Path $probeRoot 'child.pid'
    $probe = "import pathlib,subprocess,sys,time; " +
        "child=subprocess.Popen([sys.executable,'-c','import time; time.sleep(30)']); " +
        "pathlib.Path(sys.argv[1]).write_text(str(child.pid),encoding='ascii'); time.sleep(30)"
    $failure = $null
    try {
        Invoke-CheckedNative -FilePath $PythonPath -ArgumentList @('-c', $probe, $pidFile) `
            -TimeoutSeconds 1
    } catch { $failure = $_.Exception.Message }
    if ($failure -ne 'native command timed out after 1 seconds' -or
        -not (Test-Path -LiteralPath $pidFile -PathType Leaf)) {
        throw 'native timeout probe failed'
    }
    $childPid = [int]([IO.File]::ReadAllText($pidFile).Trim())
    Start-Sleep -Milliseconds 250
    if (Get-Process -Id $childPid -ErrorAction SilentlyContinue) {
        throw 'native timeout left a descendant process running'
    }
    [IO.File]::Delete($pidFile)
    [IO.Directory]::Delete($probeRoot)
}
```

- [ ] **Step A1.5: Run the bounded native-wrapper contract probe**

Continue in the same checked PowerShell session:

```powershell
Assert-NativeWrapperContract -PythonPath $PythonExe
$pythonVersion = @(Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    '-c', 'import platform; print(platform.python_version())'
))
if ($pythonVersion.Count -ne 1 -or $pythonVersion[0].Trim() -ne '3.14.6') {
    throw 'T-03A requires CPython 3.14.6'
}
$ruffVersion = @(Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    '-m', 'ruff', '--version'
))
$mypyVersion = @(Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    '-m', 'mypy', '--version'
))
$pytestVersion = @(Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    '-m', 'pytest', '--version'
))
if ($ruffVersion.Count -ne 1 -or $ruffVersion[0].Trim() -ne 'ruff 0.15.22') {
    throw 'T-03A requires Ruff 0.15.22'
}
if ($mypyVersion.Count -ne 1 -or $mypyVersion[0].Trim() -notmatch '^mypy 2\.3\.0(?: |$)') {
    throw 'T-03A requires mypy 2.3.0'
}
if ($pytestVersion.Count -ne 1 -or $pytestVersion[0].Trim() -ne 'pytest 9.1.1') {
    throw 'T-03A requires pytest 9.1.1'
}
$powerShellOutput = @(Invoke-CheckedNative -FilePath $PowerShellExe -ArgumentList @(
    '-NoProfile', '-Command', '$PSVersionTable.PSVersion.ToString()'
))
if ($powerShellOutput.Count -ne 1) { throw 'PowerShell version output must be one line' }
$powerShellVersion = $powerShellOutput[0].Trim()
$parsedPowerShellVersion = $null
if (-not [Version]::TryParse($powerShellVersion, [ref]$parsedPowerShellVersion)) {
    throw 'PowerShell version is not parseable'
}
foreach ($name in @('PROJECTB_AGENT_ID', 'PROJECTB_UNIT_ID', 'PROJECTB_BASE_COMMIT', 'PROJECTB_WORKTREE_ROOT')) {
    if ([string]::IsNullOrWhiteSpace([Environment]::GetEnvironmentVariable($name))) {
        throw "$name is required"
    }
}
if ($env:PROJECTB_AGENT_ID -notmatch '^[A-Za-z0-9][A-Za-z0-9._-]{1,63}$') {
    throw 'PROJECTB_AGENT_ID is invalid'
}
```

- [ ] **Step A1.6: Define `Assert-ExactStagedPaths`**

Continue in the same checked PowerShell session:

```powershell
if ($env:PROJECTB_UNIT_ID -ne 'T-03A') { throw 'wrong dispatch unit' }
if ($env:PROJECTB_BASE_COMMIT -notmatch '^[0-9a-f]{40}$') { throw 'invalid predecessor SHA' }
$resolvedRoot = (Resolve-Path -LiteralPath '.').Path
if ($resolvedRoot -ne (Resolve-Path -LiteralPath $env:PROJECTB_WORKTREE_ROOT).Path) {
    throw 'wrong worktree root'
}
$head = @(Invoke-CheckedNative -FilePath $GitExe -ArgumentList @('rev-parse', 'HEAD'))
if ($head.Count -ne 1 -or $head[0] -notmatch '^[0-9a-f]{40}$' -or
    $head[0].Trim() -ne $env:PROJECTB_BASE_COMMIT) {
    throw 'worktree HEAD does not match reviewed predecessor'
}
$status = @(Invoke-CheckedNative -FilePath $GitExe -ArgumentList @('status', '--porcelain'))
if ($status.Count -ne 0) { throw 'T-03A worktree must start clean' }
$env:PYTHONPATH = (Resolve-Path -LiteralPath 'backend/src').Path
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
```

Expected: exit code 0, CPython reports exactly `3.14.6`, the worktree is at the coordinator-supplied reviewed T-02C commit, and no bare interpreter lookup is used.

- [ ] **Step A2: Create the failing migration and transaction test slice**

Create `backend/tests/integration/test_sqlite_schema.py` with exactly:

```python
from __future__ import annotations

import sqlite3

import pytest
from projectb.infrastructure.sqlite import (
    Database,
    RepositoryError,
    canonical_json,
)

EXPECTED_TABLES = {
    "audit_events",
    "authority_records",
    "authority_versions",
    "consent_records",
    "course_versions",
    "courses",
    "durable_jobs",
    "learning_evidence",
    "learning_plan_revisions",
    "material_batch_files",
    "material_batches",
    "material_units",
    "material_versions",
    "materials",
    "remote_job_versions",
    "remote_jobs",
    "remote_object_versions",
    "remote_objects",
    "schema_migrations",
    "tombstones",
    "attempts",
}

```

- [ ] **Step A2.2: Append `database` through `table_names`**

Append exactly to `backend/tests/integration/test_sqlite_schema.py`:

```python
FORBIDDEN_COLUMNS = {
    "answer",
    "answer_text",
    "api_key",
    "audit_body",
    "body",
    "course_body",
    "credential_value",
    "local_path",
    "password",
    "path",
    "provider_file_id",
    "provider_object_id",
    "secret",
    "token",
}


@pytest.fixture
def database(tmp_path):
    db = Database.open(tmp_path / "projectb.sqlite3")
    db.migrate()
    try:
        yield db
    finally:
        db.close()


def table_names(database: Database) -> set[str]:
    rows = database.fetch_all(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%'"
    )
    return {str(row["name"]) for row in rows}


```

- [ ] **Step A2.3: Append `test_migration_is_repeatable_and_checksum_bound` through `test_transaction_rolls_back_the_complete_write_set`**

Append exactly to `backend/tests/integration/test_sqlite_schema.py`:

```python
def test_migration_is_repeatable_and_checksum_bound(tmp_path) -> None:
    path = tmp_path / "state.sqlite3"
    db = Database.open(path)
    db.migrate()
    first_tables = table_names(db)
    db.migrate()
    assert table_names(db) == first_tables == EXPECTED_TABLES
    rows = db.fetch_all("SELECT version, name, checksum FROM schema_migrations ORDER BY version")
    assert len(rows) == 1
    assert tuple(rows[0])[:2] == (1, "001_initial.sql")
    assert len(str(rows[0]["checksum"])) == 64
    db.execute("UPDATE schema_migrations SET checksum = ? WHERE version = 1", ("0" * 64,))
    db.close()

    reopened = Database.open(path)
    with pytest.raises(RepositoryError) as caught:
        reopened.migrate()
    assert caught.value.code == "state_inconsistent"
    reopened.close()


def test_transaction_rolls_back_the_complete_write_set(database: Database) -> None:
    with pytest.raises(RuntimeError, match="force rollback"):
        with database.transaction():
            database.execute(
                "INSERT INTO courses(course_id, owner_id, active_version, created_at_utc, "
                "updated_at_utc) "
                "VALUES (?, ?, ?, ?, ?)",
                (
                    "course-rollback",
                    "owner-1",
                    1,
                    "2026-07-23T00:00:00Z",
                    "2026-07-23T00:00:00Z",
                ),
            )
            raise RuntimeError("force rollback")
    assert (
        database.fetch_one(
            "SELECT course_id FROM courses WHERE course_id = ?", ("course-rollback",)
        )
        is None
    )


```

- [ ] **Step A2.4: Append `test_nested_transaction_fails_closed`**

Append exactly to `backend/tests/integration/test_sqlite_schema.py`:

```python
def test_nested_transaction_fails_closed(database: Database) -> None:
    with database.transaction():
        with pytest.raises(RepositoryError) as caught:
            with database.transaction():
                database.fetch_one("SELECT 1")
    assert caught.value.code == "state_inconsistent"
```

- [ ] **Step A3A: Append owner, foreign-key, and append-only schema tests**

Append exactly to `backend/tests/integration/test_sqlite_schema.py`:

```python


def test_every_authoritative_table_has_owner_scope(database: Database) -> None:
    unscoped = {"schema_migrations"}
    for table in EXPECTED_TABLES - unscoped:
        columns = {
            str(row["name"]).casefold()
            for row in database.fetch_all(f'PRAGMA table_info("{table}")')
        }
        assert "owner_id" in columns, table
        assert columns.isdisjoint(FORBIDDEN_COLUMNS), table


def test_foreign_keys_and_append_only_triggers_are_enforced(database: Database) -> None:
    assert database.fetch_one("PRAGMA foreign_keys")[0] == 1
    with pytest.raises(sqlite3.IntegrityError):
        database.execute(
            "INSERT INTO materials(material_id, owner_id, course_id, role, content_hash, "
            "active_version, created_at_utc, updated_at_utc) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                "material-orphan",
                "owner-1",
                "missing-course",
                "lecture",
                "a" * 64,
                1,
                "2026-07-23T00:00:00Z",
                "2026-07-23T00:00:00Z",
            ),
        )

```

- [ ] **Step A3A.2: Append `test_sqlite_schema.py` continuation slice 2**

Append exactly to `backend/tests/integration/test_sqlite_schema.py`:

```python
    with database.transaction():
        database.execute(
            "INSERT INTO courses(course_id, owner_id, active_version, created_at_utc, "
            "updated_at_utc) "
            "VALUES (?, ?, ?, ?, ?)",
            ("course-1", "owner-1", 1, "2026-07-23T00:00:00Z", "2026-07-23T00:00:00Z"),
        )
        database.execute(
            "INSERT INTO course_versions(course_id, owner_id, version, payload_json, "
            "created_at_utc) "
            "VALUES (?, ?, ?, ?, ?)",
            ("course-1", "owner-1", 1, "{}", "2026-07-23T00:00:00Z"),
        )
    with pytest.raises(sqlite3.IntegrityError, match="append_only"):
        database.execute(
            "UPDATE course_versions SET payload_json = ? WHERE course_id = ? AND version = 1",
            ('{"changed":true}', "course-1"),
        )
    with pytest.raises(sqlite3.IntegrityError, match="append_only"):
        database.execute(
            "DELETE FROM course_versions WHERE course_id = ? AND version = 1",
            ("course-1",),
        )


```

- [ ] **Step A3B: Append durable-job and downstream reservation tests**

Append exactly to `backend/tests/integration/test_sqlite_schema.py`:

```python
def test_durable_job_constraints_reject_invalid_state_and_progress(
    database: Database,
) -> None:
    with database.transaction():
        database.execute(
            "INSERT INTO courses(course_id, owner_id, active_version, created_at_utc, "
            "updated_at_utc) "
            "VALUES (?, ?, ?, ?, ?)",
            (
                "course-jobs",
                "owner-1",
                1,
                "2026-07-23T00:00:00Z",
                "2026-07-23T00:00:00Z",
            ),
        )
    base = (
        "job-1",
        "owner-1",
        "course-jobs",
        "local_import",
        "idem-1",
        "payload-ref-1",
        0,
        1,
        0,
        "2026-07-23T00:00:00Z",
        "2026-07-23T00:00:00Z",
    )
    statement = (
        "INSERT INTO durable_jobs(job_id, owner_id, course_id, kind, idempotency_key, "
        "payload_ref, "
        "state, completed_units, total_units, cancel_requested, created_at_utc, updated_at_utc) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    )
    with pytest.raises(sqlite3.IntegrityError):
        database.execute(statement, (*base[:6], "unknown", *base[6:]))
    with pytest.raises(sqlite3.IntegrityError):
        database.execute(
            statement,
            (*base[:6], "queued", 2, 1, *base[8:]),
        )


```

- [ ] **Step A3B.2: Append `test_reserved_schema_has_job_lease_batch_file_and_protected_attempt_fields`**

Append exactly to `backend/tests/integration/test_sqlite_schema.py`:

```python
def test_reserved_schema_has_job_lease_batch_file_and_protected_attempt_fields(
    database: Database,
) -> None:
    database.execute(
        "INSERT INTO courses(course_id, owner_id, active_version, created_at_utc, "
        "updated_at_utc) "
        "VALUES (?, ?, ?, ?, ?)",
        ("course-jobs", "owner-1", 1, "2026-07-23T00:00:00Z", "2026-07-23T00:00:00Z"),
    )
    expected_columns = {
        "durable_jobs": {
            "worker_id",
            "lease_until_utc",
            "last_heartbeat_utc",
            "payload_ref",
            "cancel_requested",
        },
        "material_batches": {"batch_id", "course_id", "mode", "created_at_utc"},
        "material_batch_files": {
            "batch_file_id",
            "batch_id",
            "material_id",
            "content_hash",
            "role",
            "state",
            "error_code",
        },
        "attempts": {
            "attempt_id",
            "course_id",
            "concept_id",
            "attempt_key",
            "response_ref",
            "submitted_at_utc",
        },
    }
    for table, required in expected_columns.items():
        actual = {str(row["name"]) for row in database.fetch_all(f'PRAGMA table_info("{table}")')}
        assert required <= actual, table
        assert actual.isdisjoint(FORBIDDEN_COLUMNS), table

```

- [ ] **Step A3B.3: Append `test_sqlite_schema.py` continuation slice 3**

Append exactly to `backend/tests/integration/test_sqlite_schema.py`:

```python
    with pytest.raises(sqlite3.IntegrityError):
        database.execute(
            "INSERT INTO durable_jobs(job_id, owner_id, course_id, kind, idempotency_key, "
            "payload_ref, state, completed_units, total_units, worker_id, lease_until_utc, "
            "cancel_requested, created_at_utc, updated_at_utc) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NULL, ?, ?, ?)",
            (
                "job-bad-lease",
                "owner-1",
                "course-jobs",
                "local_import",
                "idem-bad-lease",
                "payload-ref-1",
                "running",
                0,
                1,
                "worker-1",
                0,
                "2026-07-23T00:00:00Z",
                "2026-07-23T00:00:00Z",
            ),
        )


```

- [ ] **Step A3C: Append canonical JSON rejection and stability tests**

Append exactly to `backend/tests/integration/test_sqlite_schema.py`:

```python
@pytest.mark.parametrize(
    "payload",
    [
        {"body": "private course text"},
        {"nested": {"api_key": "synthetic-value"}},
        {"score": float("nan")},
        {"items": [object()]},
    ],
)
def test_canonical_json_rejects_forbidden_or_non_json_values(
    payload: dict[str, object],
) -> None:
    with pytest.raises(RepositoryError) as caught:
        canonical_json(payload)
    assert caught.value.code == "state_inconsistent"


def test_canonical_json_is_stable_and_keeps_whitelisted_references() -> None:
    left = canonical_json(
        {
            "scope_token": "scope-fingerprint",
            "credential_ref": "winvault-profile-1",
            "ids": ("b", "a"),
            "metadata": {"z": 2, "a": 1},
        }
    )
    right = canonical_json(
        {
            "metadata": {"a": 1, "z": 2},
            "ids": ["b", "a"],
            "credential_ref": "winvault-profile-1",
            "scope_token": "scope-fingerprint",
        }
    )
    assert left == right
    assert left == (
        '{"credential_ref":"winvault-profile-1","ids":["b","a"],'
        '"metadata":{"a":1,"z":2},"scope_token":"scope-fingerprint"}'
    )


```

- [ ] **Step A3D: Append canonical UTC and redacted migration-failure tests**

Append exactly to `backend/tests/integration/test_sqlite_schema.py`:

```python
@pytest.mark.parametrize(
    "value",
    [
        "2026-07-23T00:00Z",
        "2026-07-23T00:00:00.000Z",
        "2026-07-23T00:00:00+00:00",
        "2026-7-23T00:00:00Z",
        "2026-07-23t00:00:00Z",
    ],
)
def test_database_contract_rejects_noncanonical_utc(value: str) -> None:
    from projectb.infrastructure.sqlite import require_utc

    with pytest.raises(RepositoryError) as caught:
        require_utc(value)
    assert caught.value.code == "state_inconsistent"


@pytest.mark.parametrize("bad_hash", ["g" * 64, "A" * 64, ("0" * 63) + "-"])
def test_migration_rejects_nonhex_64_byte_hashes_on_direct_insert(
    database: Database, bad_hash: str
) -> None:
    with pytest.raises(sqlite3.IntegrityError):
        database.execute(
            "INSERT INTO schema_migrations(version, name, checksum, applied_at_utc) "
            "VALUES (?, ?, ?, ?)",
            (2, "synthetic-invalid.sql", bad_hash, "2026-07-23T00:00:00Z"),
        )
    database.execute(
        "INSERT INTO courses(course_id, owner_id, active_version, created_at_utc, "
        "updated_at_utc) "
        "VALUES (?, ?, 1, ?, ?)",
        ("hash-course", "owner-1", "2026-07-23T00:00:00Z", "2026-07-23T00:00:00Z"),
    )
```

- [ ] **Step A3D.2: Append `test_migration_rejects_noncanonical_utc_on_direct_insert_and_update`**

Append exactly to `backend/tests/integration/test_sqlite_schema.py`:

```python
    with pytest.raises(sqlite3.IntegrityError):
        database.execute(
            "INSERT INTO materials(material_id, owner_id, course_id, role, content_hash, "
            "active_version, created_at_utc, updated_at_utc) VALUES (?, ?, ?, ?, ?, 1, ?, ?)",
            (
                "invalid-hash-material",
                "owner-1",
                "hash-course",
                "lecture",
                bad_hash,
                "2026-07-23T00:00:00Z",
                "2026-07-23T00:00:00Z",
            ),
        )


@pytest.mark.parametrize(
    "bad_utc",
    [
        "2026-07-23T00:00:00+00:00",
        "2026-07-23T00:00:00.000Z",
        "2026-02-30T00:00:00Z",
    ],
)
def test_migration_rejects_noncanonical_utc_on_direct_insert_and_update(
    database: Database, bad_utc: str
) -> None:
    with pytest.raises(sqlite3.IntegrityError):
        database.execute(
            "INSERT INTO courses(course_id, owner_id, active_version, created_at_utc, "
            "updated_at_utc) VALUES (?, ?, 1, ?, ?)",
            ("invalid-time-course", "owner-1", bad_utc, "2026-07-23T00:00:00Z"),
        )
    database.execute(
        "INSERT OR IGNORE INTO courses(course_id, owner_id, active_version, created_at_utc, "
        "updated_at_utc) VALUES (?, ?, 1, ?, ?)",
        (
            "valid-time-course",
            "owner-1",
            "2026-07-23T00:00:00Z",
            "2026-07-23T00:00:00Z",
        ),
```

- [ ] **Step A3D.3: Append `test_migration_sqlite_errors_are_redacted` through `test_open_rejects_a_malformed_sqlite_file_without_leaking_engine_text`**

Append exactly to `backend/tests/integration/test_sqlite_schema.py`:

```python
    )
    with pytest.raises(sqlite3.IntegrityError):
        database.execute(
            "UPDATE courses SET tombstoned_at_utc = ? WHERE course_id = ?",
            (bad_utc, "valid-time-course"),
        )


def test_migration_sqlite_errors_are_redacted(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    database = Database.open(tmp_path / "redacted.sqlite3")
    database.migrate()

    def fail_fetch(self, statement: str, parameters=()):
        raise sqlite3.DatabaseError("synthetic private/path/value")

    monkeypatch.setattr(Database, "fetch_one", fail_fetch)
    with pytest.raises(RepositoryError) as caught:
        database.migrate()
    assert caught.value.code == "state_inconsistent"
    assert str(caught.value) == "state_inconsistent"
    assert caught.value.__cause__ is None
    assert caught.value.__suppress_context__ is True
    database.close()


def test_open_rejects_a_malformed_sqlite_file_without_leaking_engine_text(
    tmp_path,
) -> None:
    path = tmp_path / "malformed.sqlite3"
    path.write_bytes(b"synthetic-not-a-sqlite-database")
    with pytest.raises(RepositoryError) as caught:
        Database.open(path)
    assert caught.value.code == "state_inconsistent"
    assert str(caught.value) == "state_inconsistent"
    assert caught.value.__cause__ is None
```

- [ ] **Step A4: Run the T-03A focused test and capture the expected red result**

Run:

```powershell
Invoke-ExpectedNativeExit -FilePath $PythonExe -ArgumentList @(
    '-m', 'pytest', '-c', 'backend/pyproject.toml',
    'backend/tests/integration/test_sqlite_schema.py', '-q'
) -ExpectedExitCode 2
```

Expected: exit code 2 with collection failing because `projectb.infrastructure.sqlite` does not exist. No assertion is expected to pass, and no fixed test count is predicted.

- [ ] **Step A5A: Create stable repository errors and scalar validators**

Create `backend/src/projectb/infrastructure/sqlite.py` with exactly:

```python
from __future__ import annotations

import hashlib
import json
import math
import sqlite3
from collections.abc import Iterator, Mapping, Sequence
from contextlib import contextmanager, suppress
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Literal, cast

from projectb.domain.errors import SourceContractError
from projectb.domain.types import validate_content_hash, validate_opaque_id

type RepositoryErrorCode = Literal[
    "state_inconsistent",
    "owner_forbidden",
    "not_found",
]
type JsonValue = None | bool | int | float | str | list["JsonValue"] | dict[str, "JsonValue"]

_ERROR_CODES: frozenset[str] = frozenset({"state_inconsistent", "owner_forbidden", "not_found"})
_FORBIDDEN_JSON_KEYS: frozenset[str] = frozenset(
    {
        "answer",
        "answer_text",
        "api_key",
        "audit_body",
        "body",
        "course_body",
        "credential",
        "credential_value",
        "local_path",
        "password",
        "path",
        "provider_file_id",
        "provider_object_id",
        "secret",
        "token",
    }
)


```

- [ ] **Step A5A.2: Append `RepositoryError` through `require_utc`**

Append exactly to `backend/src/projectb/infrastructure/sqlite.py`:

```python
class RepositoryError(RuntimeError):
    def __init__(self, code: RepositoryErrorCode) -> None:
        if code not in _ERROR_CODES:
            raise ValueError("invalid repository error code")
        self.code = code
        super().__init__(code)


def require_opaque_id(value: object) -> str:
    try:
        return validate_opaque_id(value)
    except SourceContractError as error:
        raise RepositoryError("state_inconsistent") from error


def require_content_hash(value: object) -> str:
    try:
        return validate_content_hash(value)
    except SourceContractError as error:
        raise RepositoryError("state_inconsistent") from error


def require_version(value: object) -> int:
    if type(value) is not int or value < 1:
        raise RepositoryError("state_inconsistent")
    return value


def require_utc(value: object) -> str:
    if not isinstance(value, str) or len(value) != 20:
        raise RepositoryError("state_inconsistent")
    try:
        parsed = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as error:
        raise RepositoryError("state_inconsistent") from error
    if parsed.strftime("%Y-%m-%dT%H:%M:%SZ") != value:
        raise RepositoryError("state_inconsistent")
    return value


```

- [ ] **Step A5B: Append canonical JSON normalization and parsing**

Append exactly to `backend/src/projectb/infrastructure/sqlite.py`:

```python
def _normalize_json(value: object) -> JsonValue:
    if value is None or isinstance(value, (bool, str)):
        return value
    if type(value) is int:
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise RepositoryError("state_inconsistent")
        return value
    if isinstance(value, Mapping):
        normalized: dict[str, JsonValue] = {}
        for key, member in value.items():
            if not isinstance(key, str) or not key or key.strip() != key:
                raise RepositoryError("state_inconsistent")
            if key.casefold() in _FORBIDDEN_JSON_KEYS:
                raise RepositoryError("state_inconsistent")
            normalized[key] = _normalize_json(member)
        return normalized
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_normalize_json(member) for member in value]
    raise RepositoryError("state_inconsistent")


def canonical_json(payload: Mapping[str, object]) -> str:
    if not isinstance(payload, Mapping):
        raise RepositoryError("state_inconsistent")
    normalized = _normalize_json(payload)
    if not isinstance(normalized, dict):
        raise RepositoryError("state_inconsistent")
    return json.dumps(
        normalized,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )


```

- [ ] **Step A5B.2: Append `parse_json_object`**

Append exactly to `backend/src/projectb/infrastructure/sqlite.py`:

```python
def parse_json_object(raw: str) -> dict[str, JsonValue]:
    if not isinstance(raw, str):
        raise RepositoryError("state_inconsistent")
    try:
        loaded = json.loads(raw)
    except (TypeError, ValueError) as error:
        raise RepositoryError("state_inconsistent") from error
    normalized = _normalize_json(loaded)
    if not isinstance(normalized, dict):
        raise RepositoryError("state_inconsistent")
    return normalized
```

- [ ] **Step A6A: Append database open/query primitives**

Append exactly to `backend/src/projectb/infrastructure/sqlite.py`:

```python


@dataclass(slots=True)
class Database:
    _connection: sqlite3.Connection
    _path: Path

    @classmethod
    def open(cls, path: Path) -> Database:
        if not isinstance(path, Path):
            raise RepositoryError("state_inconsistent")
        path.parent.mkdir(parents=True, exist_ok=True)
        connection: sqlite3.Connection | None = None
        try:
            connection = sqlite3.connect(path, isolation_level=None)
            connection.row_factory = sqlite3.Row
            connection.execute("PRAGMA foreign_keys = ON")
            connection.execute("PRAGMA busy_timeout = 5000")
            connection.execute("PRAGMA schema_version").fetchone()
        except sqlite3.Error:
            if connection is not None:
                with suppress(sqlite3.Error):
                    connection.close()
            raise RepositoryError("state_inconsistent") from None
        if connection is None:
            raise RepositoryError("state_inconsistent")
        return cls(connection, path)

    def execute(
        self,
        statement: str,
        parameters: Sequence[object] = (),
    ) -> sqlite3.Cursor:
        if not isinstance(statement, str) or not statement.strip():
            raise RepositoryError("state_inconsistent")
        return self._connection.execute(statement, tuple(parameters))

```

- [ ] **Step A6A.2: Append `fetch_one` through `fetch_all`**

Append exactly to `backend/src/projectb/infrastructure/sqlite.py`:

```python
    def fetch_one(
        self,
        statement: str,
        parameters: Sequence[object] = (),
    ) -> sqlite3.Row | None:
        return cast(sqlite3.Row | None, self.execute(statement, parameters).fetchone())

    def fetch_all(
        self,
        statement: str,
        parameters: Sequence[object] = (),
    ) -> tuple[sqlite3.Row, ...]:
        return cast(
            tuple[sqlite3.Row, ...],
            tuple(self.execute(statement, parameters).fetchall()),
        )

```

- [ ] **Step A6B: Append transaction, migration, close, and exports**

Append exactly to `backend/src/projectb/infrastructure/sqlite.py`:

```python
    @contextmanager
    def transaction(self) -> Iterator[None]:
        if self._connection.in_transaction:
            raise RepositoryError("state_inconsistent")
        self._connection.execute("BEGIN IMMEDIATE")
        try:
            yield
        except BaseException:
            self._connection.rollback()
            raise
        else:
            self._connection.commit()

    def migrate(self) -> None:
        try:
            migration_path = Path(__file__).with_name("migrations") / "001_initial.sql"
            script = migration_path.read_text(encoding="utf-8")
            checksum = hashlib.sha256(script.encode("utf-8")).hexdigest()
            marker_table = self.fetch_one(
                "SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'schema_migrations'"
            )
            existing = (
                None
                if marker_table is None
                else self.fetch_one("SELECT checksum FROM schema_migrations WHERE version = 1")
            )
            if existing is not None:
                if str(existing["checksum"]) != checksum:
                    raise RepositoryError("state_inconsistent")
                return
            self._connection.executescript("BEGIN IMMEDIATE;\n" + script + "\nCOMMIT;")
            with self.transaction():
                self.execute(
                    "INSERT OR IGNORE INTO schema_migrations"
                    "(version, name, checksum, applied_at_utc) VALUES (?, ?, ?, ?)",
                    (1, "001_initial.sql", checksum, "2026-07-23T00:00:00Z"),
                )
                row = self.fetch_one("SELECT checksum FROM schema_migrations WHERE version = 1")
```

- [ ] **Step A6B.2: Append `close`**

Append exactly to `backend/src/projectb/infrastructure/sqlite.py`:

```python
                if row is None or str(row["checksum"]) != checksum:
                    raise RepositoryError("state_inconsistent")
        except RepositoryError:
            raise
        except (OSError, UnicodeError, sqlite3.Error):
            if self._connection.in_transaction:
                with suppress(sqlite3.Error):
                    self._connection.rollback()
            raise RepositoryError("state_inconsistent") from None

    def close(self) -> None:
        self._connection.close()


__all__ = [
    "Database",
    "JsonValue",
    "RepositoryError",
    "RepositoryErrorCode",
    "canonical_json",
    "parse_json_object",
    "require_content_hash",
    "require_opaque_id",
    "require_utc",
    "require_version",
]
```

- [ ] **Step A7A: Create migration marker, course, and material version schema**

Create `backend/src/projectb/infrastructure/migrations/001_initial.sql` with exactly:

```sql
CREATE TABLE IF NOT EXISTS schema_migrations (
    version INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    checksum TEXT NOT NULL CHECK(length(checksum) = 64 AND checksum NOT GLOB '*[^0-9a-f]*'),
    applied_at_utc TEXT NOT NULL CHECK(unixepoch(applied_at_utc) IS NOT NULL AND applied_at_utc = strftime('%Y-%m-%dT%H:%M:%SZ', unixepoch(applied_at_utc), 'unixepoch'))
) STRICT;

CREATE TABLE IF NOT EXISTS courses (
    course_id TEXT PRIMARY KEY,
    owner_id TEXT NOT NULL,
    active_version INTEGER NOT NULL CHECK(active_version >= 1),
    tombstoned_at_utc TEXT CHECK(tombstoned_at_utc IS NULL OR (unixepoch(tombstoned_at_utc) IS NOT NULL AND tombstoned_at_utc = strftime('%Y-%m-%dT%H:%M:%SZ', unixepoch(tombstoned_at_utc), 'unixepoch'))),
    created_at_utc TEXT NOT NULL CHECK(unixepoch(created_at_utc) IS NOT NULL AND created_at_utc = strftime('%Y-%m-%dT%H:%M:%SZ', unixepoch(created_at_utc), 'unixepoch')),
    updated_at_utc TEXT NOT NULL CHECK(unixepoch(updated_at_utc) IS NOT NULL AND updated_at_utc = strftime('%Y-%m-%dT%H:%M:%SZ', unixepoch(updated_at_utc), 'unixepoch')),
    UNIQUE(course_id, owner_id)
) STRICT;

CREATE TABLE IF NOT EXISTS course_versions (
    course_id TEXT NOT NULL,
    owner_id TEXT NOT NULL,
    version INTEGER NOT NULL CHECK(version >= 1),
    payload_json TEXT NOT NULL CHECK(json_valid(payload_json)),
    created_at_utc TEXT NOT NULL CHECK(unixepoch(created_at_utc) IS NOT NULL AND created_at_utc = strftime('%Y-%m-%dT%H:%M:%SZ', unixepoch(created_at_utc), 'unixepoch')),
    PRIMARY KEY(course_id, version),
    FOREIGN KEY(course_id, owner_id) REFERENCES courses(course_id, owner_id)
) STRICT;

CREATE TABLE IF NOT EXISTS materials (
    material_id TEXT PRIMARY KEY,
    owner_id TEXT NOT NULL,
    course_id TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('lecture', 'past_paper', 'teacher_focus')),
    content_hash TEXT NOT NULL CHECK(length(content_hash) = 64 AND content_hash NOT GLOB '*[^0-9a-f]*'),
    active_version INTEGER NOT NULL CHECK(active_version >= 1),
    tombstoned_at_utc TEXT CHECK(tombstoned_at_utc IS NULL OR (unixepoch(tombstoned_at_utc) IS NOT NULL AND tombstoned_at_utc = strftime('%Y-%m-%dT%H:%M:%SZ', unixepoch(tombstoned_at_utc), 'unixepoch'))),
    created_at_utc TEXT NOT NULL CHECK(unixepoch(created_at_utc) IS NOT NULL AND created_at_utc = strftime('%Y-%m-%dT%H:%M:%SZ', unixepoch(created_at_utc), 'unixepoch')),
    updated_at_utc TEXT NOT NULL CHECK(unixepoch(updated_at_utc) IS NOT NULL AND updated_at_utc = strftime('%Y-%m-%dT%H:%M:%SZ', unixepoch(updated_at_utc), 'unixepoch')),
    UNIQUE(material_id, owner_id),
    FOREIGN KEY(course_id, owner_id) REFERENCES courses(course_id, owner_id)
) STRICT;

```

- [ ] **Step A7A.2: Append migration statements slice 2**

Append exactly to `backend/src/projectb/infrastructure/migrations/001_initial.sql`:

```sql
CREATE TABLE IF NOT EXISTS material_versions (
    material_id TEXT NOT NULL,
    owner_id TEXT NOT NULL,
    course_id TEXT NOT NULL,
    version INTEGER NOT NULL CHECK(version >= 1),
    role TEXT NOT NULL CHECK(role IN ('lecture', 'past_paper', 'teacher_focus')),
    content_hash TEXT NOT NULL CHECK(length(content_hash) = 64 AND content_hash NOT GLOB '*[^0-9a-f]*'),
    payload_json TEXT NOT NULL CHECK(json_valid(payload_json)),
    created_at_utc TEXT NOT NULL CHECK(unixepoch(created_at_utc) IS NOT NULL AND created_at_utc = strftime('%Y-%m-%dT%H:%M:%SZ', unixepoch(created_at_utc), 'unixepoch')),
    PRIMARY KEY(material_id, version),
    FOREIGN KEY(material_id, owner_id) REFERENCES materials(material_id, owner_id),
    FOREIGN KEY(course_id, owner_id) REFERENCES courses(course_id, owner_id)
) STRICT;

```

- [ ] **Step A7B: Append material batch and per-file state schema**

Append exactly to `backend/src/projectb/infrastructure/migrations/001_initial.sql`:

```sql
CREATE TABLE IF NOT EXISTS material_batches (
    batch_id TEXT PRIMARY KEY,
    owner_id TEXT NOT NULL,
    course_id TEXT NOT NULL,
    mode TEXT NOT NULL CHECK(mode IN ('L', 'P', 'F')),
    state TEXT NOT NULL CHECK(state IN (
        'open', 'processing', 'completed', 'partial_failed', 'cancelled'
    )),
    created_at_utc TEXT NOT NULL CHECK(unixepoch(created_at_utc) IS NOT NULL AND created_at_utc = strftime('%Y-%m-%dT%H:%M:%SZ', unixepoch(created_at_utc), 'unixepoch')),
    updated_at_utc TEXT NOT NULL CHECK(unixepoch(updated_at_utc) IS NOT NULL AND updated_at_utc = strftime('%Y-%m-%dT%H:%M:%SZ', unixepoch(updated_at_utc), 'unixepoch')),
    UNIQUE(batch_id, owner_id),
    FOREIGN KEY(course_id, owner_id) REFERENCES courses(course_id, owner_id)
) STRICT;

CREATE TABLE IF NOT EXISTS material_batch_files (
    batch_file_id TEXT PRIMARY KEY,
    owner_id TEXT NOT NULL,
    batch_id TEXT NOT NULL,
    material_id TEXT,
    content_hash TEXT NOT NULL CHECK(length(content_hash) = 64 AND content_hash NOT GLOB '*[^0-9a-f]*'),
    role TEXT NOT NULL CHECK(role IN ('lecture', 'past_paper', 'teacher_focus')),
    state TEXT NOT NULL CHECK(state IN (
        'inspected', 'queued', 'processing', 'ready', 'failed', 'cancelled'
    )),
    error_code TEXT,
    created_at_utc TEXT NOT NULL CHECK(unixepoch(created_at_utc) IS NOT NULL AND created_at_utc = strftime('%Y-%m-%dT%H:%M:%SZ', unixepoch(created_at_utc), 'unixepoch')),
    updated_at_utc TEXT NOT NULL CHECK(unixepoch(updated_at_utc) IS NOT NULL AND updated_at_utc = strftime('%Y-%m-%dT%H:%M:%SZ', unixepoch(updated_at_utc), 'unixepoch')),
    UNIQUE(batch_file_id, owner_id),
    UNIQUE(owner_id, batch_id, content_hash, role),
    CHECK(state != 'ready' OR material_id IS NOT NULL),
    FOREIGN KEY(batch_id, owner_id) REFERENCES material_batches(batch_id, owner_id),
    FOREIGN KEY(material_id, owner_id) REFERENCES materials(material_id, owner_id)
) STRICT;

```

- [ ] **Step A7C: Append material-unit and generic authority reservations**

Append exactly to `backend/src/projectb/infrastructure/migrations/001_initial.sql`:

```sql
CREATE TABLE IF NOT EXISTS material_units (
    unit_id TEXT PRIMARY KEY,
    owner_id TEXT NOT NULL,
    material_id TEXT NOT NULL,
    content_hash TEXT NOT NULL CHECK(length(content_hash) = 64 AND content_hash NOT GLOB '*[^0-9a-f]*'),
    kind TEXT NOT NULL CHECK(kind IN ('pdf_page', 'image', 'text_lines', 'manual_entry')),
    ordinal INTEGER NOT NULL CHECK(ordinal >= 1),
    parser_version TEXT NOT NULL,
    quality_flags_json TEXT NOT NULL CHECK(json_valid(quality_flags_json)),
    raw_storage_ref TEXT,
    normalized_storage_ref TEXT,
    invalidated_at_utc TEXT CHECK(invalidated_at_utc IS NULL OR (unixepoch(invalidated_at_utc) IS NOT NULL AND invalidated_at_utc = strftime('%Y-%m-%dT%H:%M:%SZ', unixepoch(invalidated_at_utc), 'unixepoch'))),
    created_at_utc TEXT NOT NULL CHECK(unixepoch(created_at_utc) IS NOT NULL AND created_at_utc = strftime('%Y-%m-%dT%H:%M:%SZ', unixepoch(created_at_utc), 'unixepoch')),
    UNIQUE(unit_id, owner_id),
    FOREIGN KEY(material_id, owner_id) REFERENCES materials(material_id, owner_id)
) STRICT;

CREATE TABLE IF NOT EXISTS authority_records (
    entity_id TEXT PRIMARY KEY,
    owner_id TEXT NOT NULL,
    course_id TEXT NOT NULL,
    entity_kind TEXT NOT NULL CHECK(entity_kind IN (
        'coverage_decision', 'mastery_estimate', 'review_goal', 'review_task', 'study_focus'
    )),
    active_version INTEGER NOT NULL CHECK(active_version >= 1),
    tombstoned_at_utc TEXT CHECK(tombstoned_at_utc IS NULL OR (unixepoch(tombstoned_at_utc) IS NOT NULL AND tombstoned_at_utc = strftime('%Y-%m-%dT%H:%M:%SZ', unixepoch(tombstoned_at_utc), 'unixepoch'))),
    created_at_utc TEXT NOT NULL CHECK(unixepoch(created_at_utc) IS NOT NULL AND created_at_utc = strftime('%Y-%m-%dT%H:%M:%SZ', unixepoch(created_at_utc), 'unixepoch')),
    updated_at_utc TEXT NOT NULL CHECK(unixepoch(updated_at_utc) IS NOT NULL AND updated_at_utc = strftime('%Y-%m-%dT%H:%M:%SZ', unixepoch(updated_at_utc), 'unixepoch')),
    UNIQUE(entity_id, owner_id),
    FOREIGN KEY(course_id, owner_id) REFERENCES courses(course_id, owner_id)
) STRICT;

CREATE TABLE IF NOT EXISTS authority_versions (
    entity_id TEXT NOT NULL,
    owner_id TEXT NOT NULL,
    course_id TEXT NOT NULL,
    entity_kind TEXT NOT NULL,
    version INTEGER NOT NULL CHECK(version >= 1),
    payload_json TEXT NOT NULL CHECK(json_valid(payload_json)),
    created_at_utc TEXT NOT NULL CHECK(unixepoch(created_at_utc) IS NOT NULL AND created_at_utc = strftime('%Y-%m-%dT%H:%M:%SZ', unixepoch(created_at_utc), 'unixepoch')),
    PRIMARY KEY(entity_id, version),
    FOREIGN KEY(entity_id, owner_id) REFERENCES authority_records(entity_id, owner_id),
    FOREIGN KEY(course_id, owner_id) REFERENCES courses(course_id, owner_id)
) STRICT;
```

- [ ] **Step A8A: Append exact-F consent, protected Attempt, and evidence tables**

Append exactly to `backend/src/projectb/infrastructure/migrations/001_initial.sql`:

```sql

CREATE TABLE IF NOT EXISTS consent_records (
    consent_id TEXT PRIMARY KEY,
    owner_id TEXT NOT NULL,
    course_id TEXT NOT NULL,
    mode TEXT NOT NULL CHECK(mode = 'F'),
    payload_scope_json TEXT NOT NULL CHECK(json_valid(payload_scope_json)),
    profile_ref TEXT NOT NULL,
    config_fingerprint TEXT NOT NULL CHECK(length(config_fingerprint) = 64 AND config_fingerprint NOT GLOB '*[^0-9a-f]*'),
    capability_snapshot_id TEXT NOT NULL,
    policy_snapshot_id TEXT NOT NULL,
    revoked_at_utc TEXT CHECK(revoked_at_utc IS NULL OR (unixepoch(revoked_at_utc) IS NOT NULL AND revoked_at_utc = strftime('%Y-%m-%dT%H:%M:%SZ', unixepoch(revoked_at_utc), 'unixepoch'))),
    created_at_utc TEXT NOT NULL CHECK(unixepoch(created_at_utc) IS NOT NULL AND created_at_utc = strftime('%Y-%m-%dT%H:%M:%SZ', unixepoch(created_at_utc), 'unixepoch')),
    UNIQUE(consent_id, owner_id),
    FOREIGN KEY(course_id, owner_id) REFERENCES courses(course_id, owner_id)
) STRICT;

CREATE TABLE IF NOT EXISTS attempts (
    attempt_id TEXT PRIMARY KEY,
    owner_id TEXT NOT NULL,
    course_id TEXT NOT NULL,
    concept_id TEXT NOT NULL,
    attempt_key TEXT NOT NULL,
    explanation_session_id TEXT,
    review_task_id TEXT,
    response_ref TEXT NOT NULL,
    started_at_utc TEXT NOT NULL CHECK(unixepoch(started_at_utc) IS NOT NULL AND started_at_utc = strftime('%Y-%m-%dT%H:%M:%SZ', unixepoch(started_at_utc), 'unixepoch')),
    submitted_at_utc TEXT NOT NULL CHECK(unixepoch(submitted_at_utc) IS NOT NULL AND submitted_at_utc = strftime('%Y-%m-%dT%H:%M:%SZ', unixepoch(submitted_at_utc), 'unixepoch')),
    UNIQUE(attempt_id, owner_id),
    UNIQUE(owner_id, course_id, attempt_key),
    FOREIGN KEY(course_id, owner_id) REFERENCES courses(course_id, owner_id)
) STRICT;

```

- [ ] **Step A8A.2: Append migration statements slice 2**

Append exactly to `backend/src/projectb/infrastructure/migrations/001_initial.sql`:

```sql
CREATE TABLE IF NOT EXISTS learning_evidence (
    evidence_id TEXT PRIMARY KEY,
    owner_id TEXT NOT NULL,
    course_id TEXT NOT NULL,
    concept_id TEXT NOT NULL,
    attempt_id TEXT NOT NULL,
    attempt_key TEXT NOT NULL,
    occurred_at_utc TEXT NOT NULL CHECK(unixepoch(occurred_at_utc) IS NOT NULL AND occurred_at_utc = strftime('%Y-%m-%dT%H:%M:%SZ', unixepoch(occurred_at_utc), 'unixepoch')),
    evidence_version TEXT NOT NULL CHECK(evidence_version = 'learning-evidence.v1'),
    payload_json TEXT NOT NULL CHECK(json_valid(payload_json)),
    UNIQUE(evidence_id, owner_id),
    UNIQUE(owner_id, course_id, attempt_key),
    FOREIGN KEY(course_id, owner_id) REFERENCES courses(course_id, owner_id),
    FOREIGN KEY(attempt_id, owner_id) REFERENCES attempts(attempt_id, owner_id)
) STRICT;

```

- [ ] **Step A8B: Append learning-plan and remote-object tables**

Append exactly to `backend/src/projectb/infrastructure/migrations/001_initial.sql`:

```sql
CREATE TABLE IF NOT EXISTS learning_plan_revisions (
    revision_id TEXT PRIMARY KEY,
    owner_id TEXT NOT NULL,
    course_id TEXT NOT NULL,
    revision_number INTEGER NOT NULL CHECK(revision_number >= 1),
    parent_revision_id TEXT,
    reverts_revision_id TEXT,
    plan_input_hash TEXT NOT NULL CHECK(length(plan_input_hash) = 64 AND plan_input_hash NOT GLOB '*[^0-9a-f]*'),
    policy_version TEXT NOT NULL,
    payload_json TEXT NOT NULL CHECK(json_valid(payload_json)),
    created_at_utc TEXT NOT NULL CHECK(unixepoch(created_at_utc) IS NOT NULL AND created_at_utc = strftime('%Y-%m-%dT%H:%M:%SZ', unixepoch(created_at_utc), 'unixepoch')),
    UNIQUE(revision_id, owner_id),
    UNIQUE(owner_id, course_id, revision_number),
    FOREIGN KEY(course_id, owner_id) REFERENCES courses(course_id, owner_id)
) STRICT;

CREATE TABLE IF NOT EXISTS remote_objects (
    object_id TEXT PRIMARY KEY,
    owner_id TEXT NOT NULL,
    course_id TEXT NOT NULL,
    material_id TEXT NOT NULL,
    consent_id TEXT,
    object_kind TEXT NOT NULL CHECK(object_kind IN ('file', 'association', 'vector_store')),
    state TEXT NOT NULL CHECK(state IN (
        'awaiting_consent', 'uploading', 'indexing', 'ready', 'failed',
        'delete_requested', 'deleted', 'delete_incomplete', 'source_disabled'
    )),
    active_version INTEGER NOT NULL CHECK(active_version >= 1),
    config_fingerprint TEXT NOT NULL CHECK(length(config_fingerprint) = 64 AND config_fingerprint NOT GLOB '*[^0-9a-f]*'),
    scope_token TEXT CHECK(scope_token IS NULL OR (length(scope_token) = 64 AND scope_token NOT GLOB '*[^0-9a-f]*')),
    provider_ref TEXT,
    tombstoned_at_utc TEXT CHECK(tombstoned_at_utc IS NULL OR (unixepoch(tombstoned_at_utc) IS NOT NULL AND tombstoned_at_utc = strftime('%Y-%m-%dT%H:%M:%SZ', unixepoch(tombstoned_at_utc), 'unixepoch'))),
    created_at_utc TEXT NOT NULL CHECK(unixepoch(created_at_utc) IS NOT NULL AND created_at_utc = strftime('%Y-%m-%dT%H:%M:%SZ', unixepoch(created_at_utc), 'unixepoch')),
    updated_at_utc TEXT NOT NULL CHECK(unixepoch(updated_at_utc) IS NOT NULL AND updated_at_utc = strftime('%Y-%m-%dT%H:%M:%SZ', unixepoch(updated_at_utc), 'unixepoch')),
    UNIQUE(object_id, owner_id),
    CHECK(
        (state = 'awaiting_consent' AND consent_id IS NULL AND scope_token IS NULL AND provider_ref IS NULL)
        OR (state != 'awaiting_consent' AND consent_id IS NOT NULL)
    ),
    FOREIGN KEY(course_id, owner_id) REFERENCES courses(course_id, owner_id),
    FOREIGN KEY(material_id, owner_id) REFERENCES materials(material_id, owner_id),
    FOREIGN KEY(consent_id, owner_id) REFERENCES consent_records(consent_id, owner_id)
) STRICT;

```

- [ ] **Step A8B.2: Append migration statements slice 2**

Append exactly to `backend/src/projectb/infrastructure/migrations/001_initial.sql`:

```sql
CREATE TABLE IF NOT EXISTS remote_object_versions (
    object_id TEXT NOT NULL,
    owner_id TEXT NOT NULL,
    course_id TEXT NOT NULL,
    version INTEGER NOT NULL CHECK(version >= 1),
    state TEXT NOT NULL,
    config_fingerprint TEXT NOT NULL CHECK(length(config_fingerprint) = 64 AND config_fingerprint NOT GLOB '*[^0-9a-f]*'),
    payload_json TEXT NOT NULL CHECK(json_valid(payload_json)),
    created_at_utc TEXT NOT NULL CHECK(unixepoch(created_at_utc) IS NOT NULL AND created_at_utc = strftime('%Y-%m-%dT%H:%M:%SZ', unixepoch(created_at_utc), 'unixepoch')),
    PRIMARY KEY(object_id, version),
    FOREIGN KEY(object_id, owner_id) REFERENCES remote_objects(object_id, owner_id),
    FOREIGN KEY(course_id, owner_id) REFERENCES courses(course_id, owner_id)
) STRICT;

```

- [ ] **Step A8C: Append remote-job current and version tables**

Append exactly to `backend/src/projectb/infrastructure/migrations/001_initial.sql`:

```sql
CREATE TABLE IF NOT EXISTS remote_jobs (
    job_id TEXT PRIMARY KEY,
    owner_id TEXT NOT NULL,
    course_id TEXT NOT NULL,
    object_id TEXT,
    idempotency_key TEXT NOT NULL,
    state TEXT NOT NULL CHECK(state IN (
        'queued', 'running', 'cancelling', 'cancelled', 'succeeded', 'failed', 'recovery_required'
    )),
    active_version INTEGER NOT NULL CHECK(active_version >= 1),
    completed_units INTEGER NOT NULL CHECK(completed_units >= 0),
    total_units INTEGER NOT NULL CHECK(total_units >= 0 AND completed_units <= total_units),
    error_code TEXT,
    created_at_utc TEXT NOT NULL CHECK(unixepoch(created_at_utc) IS NOT NULL AND created_at_utc = strftime('%Y-%m-%dT%H:%M:%SZ', unixepoch(created_at_utc), 'unixepoch')),
    updated_at_utc TEXT NOT NULL CHECK(unixepoch(updated_at_utc) IS NOT NULL AND updated_at_utc = strftime('%Y-%m-%dT%H:%M:%SZ', unixepoch(updated_at_utc), 'unixepoch')),
    UNIQUE(job_id, owner_id),
    UNIQUE(owner_id, course_id, idempotency_key),
    FOREIGN KEY(course_id, owner_id) REFERENCES courses(course_id, owner_id),
    FOREIGN KEY(object_id, owner_id) REFERENCES remote_objects(object_id, owner_id)
) STRICT;

CREATE TABLE IF NOT EXISTS remote_job_versions (
    job_id TEXT NOT NULL,
    owner_id TEXT NOT NULL,
    course_id TEXT NOT NULL,
    version INTEGER NOT NULL CHECK(version >= 1),
    state TEXT NOT NULL,
    completed_units INTEGER NOT NULL,
    total_units INTEGER NOT NULL,
    error_code TEXT,
    payload_json TEXT NOT NULL CHECK(json_valid(payload_json)),
    created_at_utc TEXT NOT NULL CHECK(unixepoch(created_at_utc) IS NOT NULL AND created_at_utc = strftime('%Y-%m-%dT%H:%M:%SZ', unixepoch(created_at_utc), 'unixepoch')),
    PRIMARY KEY(job_id, version),
    FOREIGN KEY(job_id, owner_id) REFERENCES remote_jobs(job_id, owner_id),
    FOREIGN KEY(course_id, owner_id) REFERENCES courses(course_id, owner_id)
) STRICT;
```

- [ ] **Step A9A: Append durable-job lease reservation**

Append exactly to `backend/src/projectb/infrastructure/migrations/001_initial.sql`:

```sql

CREATE TABLE IF NOT EXISTS durable_jobs (
    job_id TEXT PRIMARY KEY,
    owner_id TEXT NOT NULL,
    course_id TEXT NOT NULL,
    kind TEXT NOT NULL CHECK(kind IN (
        'local_import', 'remote_upload', 'remote_index', 'remote_reconcile', 'remote_delete'
    )),
    idempotency_key TEXT NOT NULL,
    payload_ref TEXT NOT NULL,
    state TEXT NOT NULL CHECK(state IN (
        'queued', 'running', 'cancelling', 'cancelled', 'succeeded', 'failed', 'recovery_required'
    )),
    completed_units INTEGER NOT NULL CHECK(completed_units >= 0),
    total_units INTEGER NOT NULL CHECK(total_units >= 0 AND completed_units <= total_units),
    worker_id TEXT,
    lease_until_utc TEXT CHECK(lease_until_utc IS NULL OR (unixepoch(lease_until_utc) IS NOT NULL AND lease_until_utc = strftime('%Y-%m-%dT%H:%M:%SZ', unixepoch(lease_until_utc), 'unixepoch'))),
    last_heartbeat_utc TEXT CHECK(last_heartbeat_utc IS NULL OR (unixepoch(last_heartbeat_utc) IS NOT NULL AND last_heartbeat_utc = strftime('%Y-%m-%dT%H:%M:%SZ', unixepoch(last_heartbeat_utc), 'unixepoch'))),
    cancel_requested INTEGER NOT NULL CHECK(cancel_requested IN (0, 1)),
    error_code TEXT,
    created_at_utc TEXT NOT NULL CHECK(unixepoch(created_at_utc) IS NOT NULL AND created_at_utc = strftime('%Y-%m-%dT%H:%M:%SZ', unixepoch(created_at_utc), 'unixepoch')),
    updated_at_utc TEXT NOT NULL CHECK(unixepoch(updated_at_utc) IS NOT NULL AND updated_at_utc = strftime('%Y-%m-%dT%H:%M:%SZ', unixepoch(updated_at_utc), 'unixepoch')),
    UNIQUE(job_id, owner_id),
    UNIQUE(owner_id, kind, idempotency_key),
    CHECK(
        (worker_id IS NULL AND lease_until_utc IS NULL)
        OR (worker_id IS NOT NULL AND lease_until_utc IS NOT NULL)
    ),
    FOREIGN KEY(course_id, owner_id) REFERENCES courses(course_id, owner_id)
) STRICT;

```

- [ ] **Step A9B: Append tombstone, audit, and index schema**

Append exactly to `backend/src/projectb/infrastructure/migrations/001_initial.sql`:

```sql
CREATE TABLE IF NOT EXISTS tombstones (
    tombstone_id TEXT PRIMARY KEY,
    owner_id TEXT NOT NULL,
    entity_kind TEXT NOT NULL,
    entity_id TEXT NOT NULL,
    reason_code TEXT NOT NULL,
    metadata_json TEXT NOT NULL CHECK(json_valid(metadata_json)),
    created_at_utc TEXT NOT NULL CHECK(unixepoch(created_at_utc) IS NOT NULL AND created_at_utc = strftime('%Y-%m-%dT%H:%M:%SZ', unixepoch(created_at_utc), 'unixepoch')),
    UNIQUE(owner_id, entity_kind, entity_id)
) STRICT;

CREATE TABLE IF NOT EXISTS audit_events (
    event_id TEXT PRIMARY KEY,
    owner_id TEXT NOT NULL,
    event_kind TEXT NOT NULL,
    subject_id TEXT NOT NULL,
    outcome_code TEXT NOT NULL,
    metadata_json TEXT NOT NULL CHECK(json_valid(metadata_json)),
    occurred_at_utc TEXT NOT NULL CHECK(unixepoch(occurred_at_utc) IS NOT NULL AND occurred_at_utc = strftime('%Y-%m-%dT%H:%M:%SZ', unixepoch(occurred_at_utc), 'unixepoch')),
    UNIQUE(event_id, owner_id)
) STRICT;

CREATE UNIQUE INDEX IF NOT EXISTS ux_material_identity_active
ON materials(owner_id, course_id, content_hash, role)
WHERE tombstoned_at_utc IS NULL;

```

- [ ] **Step A9B.2: Append migration statements slice 2**

Append exactly to `backend/src/projectb/infrastructure/migrations/001_initial.sql`:

```sql
CREATE INDEX IF NOT EXISTS ix_course_versions_history
ON course_versions(owner_id, course_id, version);
CREATE INDEX IF NOT EXISTS ix_material_versions_history
ON material_versions(owner_id, material_id, version);
CREATE INDEX IF NOT EXISTS ix_material_batches_course_state
ON material_batches(owner_id, course_id, state, created_at_utc);
CREATE INDEX IF NOT EXISTS ix_material_batch_files_state
ON material_batch_files(owner_id, batch_id, state, batch_file_id);
CREATE INDEX IF NOT EXISTS ix_material_units_active
ON material_units(owner_id, material_id, invalidated_at_utc, ordinal);
CREATE INDEX IF NOT EXISTS ix_authority_versions_history
ON authority_versions(owner_id, course_id, entity_kind, entity_id, version);
CREATE INDEX IF NOT EXISTS ix_evidence_course_time
ON learning_evidence(owner_id, course_id, occurred_at_utc, evidence_id);
CREATE INDEX IF NOT EXISTS ix_attempts_course_time
ON attempts(owner_id, course_id, submitted_at_utc, attempt_id);
CREATE INDEX IF NOT EXISTS ix_plan_course_revision
ON learning_plan_revisions(owner_id, course_id, revision_number);
CREATE INDEX IF NOT EXISTS ix_remote_objects_course_state
ON remote_objects(owner_id, course_id, state);
CREATE INDEX IF NOT EXISTS ix_remote_jobs_course_state
ON remote_jobs(owner_id, course_id, state);
CREATE INDEX IF NOT EXISTS ix_durable_jobs_recovery
ON durable_jobs(owner_id, state, updated_at_utc);
CREATE INDEX IF NOT EXISTS ix_tombstones_entity
ON tombstones(owner_id, entity_kind, entity_id);
CREATE INDEX IF NOT EXISTS ix_audit_owner_time
ON audit_events(owner_id, occurred_at_utc, event_id);
```

- [ ] **Step A10: Append all append-only denial triggers**

Append exactly to `backend/src/projectb/infrastructure/migrations/001_initial.sql`:

```sql

CREATE TRIGGER IF NOT EXISTS course_versions_no_update
BEFORE UPDATE ON course_versions BEGIN SELECT RAISE(ABORT, 'append_only'); END;
CREATE TRIGGER IF NOT EXISTS course_versions_no_delete
BEFORE DELETE ON course_versions BEGIN SELECT RAISE(ABORT, 'append_only'); END;
CREATE TRIGGER IF NOT EXISTS material_versions_no_update
BEFORE UPDATE ON material_versions BEGIN SELECT RAISE(ABORT, 'append_only'); END;
CREATE TRIGGER IF NOT EXISTS material_versions_no_delete
BEFORE DELETE ON material_versions BEGIN SELECT RAISE(ABORT, 'append_only'); END;
CREATE TRIGGER IF NOT EXISTS authority_versions_no_update
BEFORE UPDATE ON authority_versions BEGIN SELECT RAISE(ABORT, 'append_only'); END;
CREATE TRIGGER IF NOT EXISTS authority_versions_no_delete
BEFORE DELETE ON authority_versions BEGIN SELECT RAISE(ABORT, 'append_only'); END;
CREATE TRIGGER IF NOT EXISTS consent_records_no_update
BEFORE UPDATE ON consent_records BEGIN SELECT RAISE(ABORT, 'append_only'); END;
CREATE TRIGGER IF NOT EXISTS consent_records_no_delete
BEFORE DELETE ON consent_records BEGIN SELECT RAISE(ABORT, 'append_only'); END;
CREATE TRIGGER IF NOT EXISTS attempts_no_update
BEFORE UPDATE ON attempts BEGIN SELECT RAISE(ABORT, 'append_only'); END;
CREATE TRIGGER IF NOT EXISTS attempts_no_delete
BEFORE DELETE ON attempts BEGIN SELECT RAISE(ABORT, 'append_only'); END;
CREATE TRIGGER IF NOT EXISTS learning_evidence_no_update
BEFORE UPDATE ON learning_evidence BEGIN SELECT RAISE(ABORT, 'append_only'); END;
CREATE TRIGGER IF NOT EXISTS learning_evidence_no_delete
BEFORE DELETE ON learning_evidence BEGIN SELECT RAISE(ABORT, 'append_only'); END;
CREATE TRIGGER IF NOT EXISTS learning_plan_revisions_no_update
BEFORE UPDATE ON learning_plan_revisions BEGIN SELECT RAISE(ABORT, 'append_only'); END;
CREATE TRIGGER IF NOT EXISTS learning_plan_revisions_no_delete
BEFORE DELETE ON learning_plan_revisions BEGIN SELECT RAISE(ABORT, 'append_only'); END;
CREATE TRIGGER IF NOT EXISTS remote_object_versions_no_update
BEFORE UPDATE ON remote_object_versions BEGIN SELECT RAISE(ABORT, 'append_only'); END;
CREATE TRIGGER IF NOT EXISTS remote_object_versions_no_delete
BEFORE DELETE ON remote_object_versions BEGIN SELECT RAISE(ABORT, 'append_only'); END;
CREATE TRIGGER IF NOT EXISTS remote_job_versions_no_update
BEFORE UPDATE ON remote_job_versions BEGIN SELECT RAISE(ABORT, 'append_only'); END;
CREATE TRIGGER IF NOT EXISTS remote_job_versions_no_delete
BEFORE DELETE ON remote_job_versions BEGIN SELECT RAISE(ABORT, 'append_only'); END;
CREATE TRIGGER IF NOT EXISTS tombstones_no_update
BEFORE UPDATE ON tombstones BEGIN SELECT RAISE(ABORT, 'append_only'); END;
CREATE TRIGGER IF NOT EXISTS tombstones_no_delete
BEFORE DELETE ON tombstones BEGIN SELECT RAISE(ABORT, 'append_only'); END;
CREATE TRIGGER IF NOT EXISTS audit_events_no_update
BEFORE UPDATE ON audit_events BEGIN SELECT RAISE(ABORT, 'append_only'); END;
CREATE TRIGGER IF NOT EXISTS audit_events_no_delete
BEFORE DELETE ON audit_events BEGIN SELECT RAISE(ABORT, 'append_only'); END;
```

- [ ] **Step A11: Run the complete T-03A focused test green**

Run:

```powershell
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    '-m', 'pytest', '-c', 'backend/pyproject.toml',
    'backend/tests/integration/test_sqlite_schema.py', '-q'
)
```

Expected: exit code 0; migration repeatability/checksum, transaction rollback, owner/column, foreign-key, trigger, durable-job constraint, and canonical JSON assertions all pass. Record only the observed result, not a predicted pass count.

- [ ] **Step A12: Format the T-03A Python paths without changing behavior**

Run:

```powershell
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    '-m', 'ruff', 'format', '--config', 'backend/pyproject.toml',
    'backend/src/projectb/infrastructure/sqlite.py',
    'backend/tests/integration/test_sqlite_schema.py'
)
```

Expected: exit code 0. Rerunning Step A11 still exits 0.

- [ ] **Step A13: Run focused regression, integration regression, and the canonical full entry**

Run:

```powershell
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    '-m', 'pytest', '-c', 'backend/pyproject.toml',
    'backend/tests/integration/test_sqlite_schema.py', '-q'
)
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    '-m', 'pytest', '-c', 'backend/pyproject.toml',
    'backend/tests/integration', '-q'
)
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @('scripts/test_all.py')
```

Expected: each command exits 0. Results are recorded exactly as observed; this plan predicts no fixed suite count.

- [ ] **Step A14: Run T-03A Ruff and mypy gates**

Run:

```powershell
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    '-m', 'ruff', 'format', '--check', '--config', 'backend/pyproject.toml',
    'backend/src/projectb/infrastructure/sqlite.py',
    'backend/tests/integration/test_sqlite_schema.py'
)
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    '-m', 'ruff', 'check', '--config', 'backend/pyproject.toml',
    '--extend-select', 'I,E501',
    'backend/src/projectb/infrastructure/sqlite.py',
    'backend/tests/integration/test_sqlite_schema.py'
)
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    '-m', 'mypy', '--config-file', 'backend/pyproject.toml', '--warn-redundant-casts',
    'backend/src/projectb/infrastructure/sqlite.py'
)
```

Expected: both commands exit 0 with no diagnostic. A diagnostic requires a test-preserving fix and repetition of Steps A11-A14.

- [ ] **Step A15: Stage exactly the T-03A ownership set**

Run:

```powershell
Invoke-CheckedNative -FilePath $GitExe -ArgumentList @(
    'add', '--',
    'backend/src/projectb/infrastructure/sqlite.py',
    'backend/src/projectb/infrastructure/migrations/001_initial.sql',
    'backend/tests/integration/test_sqlite_schema.py'
)
Assert-ExactStagedPaths -ExpectedPaths @(
    'backend/src/projectb/infrastructure/migrations/001_initial.sql'
    'backend/src/projectb/infrastructure/sqlite.py'
    'backend/tests/integration/test_sqlite_schema.py'
)
Invoke-CheckedNative -FilePath $GitExe -ArgumentList @('diff', '--cached', '--check')
$reviewTree = @(Invoke-CheckedNative -FilePath $GitExe -ArgumentList @('write-tree'))
if ($reviewTree.Count -ne 1 -or $reviewTree[0] -notmatch '^[0-9a-f]{40}$') {
    throw 'T-03A review tree must be one lowercase 40-hex line'
}
$env:PROJECTB_REVIEW_TREE = $reviewTree[0]
$expectedReviewPaths = @(
    'backend/src/projectb/infrastructure/migrations/001_initial.sql'
    'backend/src/projectb/infrastructure/sqlite.py'
    'backend/tests/integration/test_sqlite_schema.py'
)
foreach ($name in @('PROJECTB_ROOT_PLAN_SHA256', 'PROJECTB_DETAILED_PLAN_SHA256')) {
    $value = [Environment]::GetEnvironmentVariable($name)
    if ($value -notmatch '^[0-9A-Fa-f]{64}$') { throw "$name must be one 64-hex hash" }
}
$rootPlanSha = (Get-FileHash -Algorithm SHA256 -LiteralPath 'PLAN.md').Hash.ToLowerInvariant()
$detailedPlanPath = 'docs/superpowers/plans/2026-07-23-persistence-repositories.md'
$detailedPlanSha = (
    Get-FileHash -Algorithm SHA256 -LiteralPath $detailedPlanPath
).Hash.ToLowerInvariant()
if ($rootPlanSha -ne $env:PROJECTB_ROOT_PLAN_SHA256.ToLowerInvariant() -or
    $detailedPlanSha -ne $env:PROJECTB_DETAILED_PLAN_SHA256.ToLowerInvariant()) {
    throw 'review packet plan hash mismatch'
}
```

- [ ] **Step A15.2: Build the exact staged-content review packet**

Continue in the same checked PowerShell session:

```powershell
$blobRows = foreach ($path in ($expectedReviewPaths | Sort-Object)) {
    $stage = @(Invoke-CheckedNative -FilePath $GitExe -ArgumentList @(
        'ls-files', '--stage', '--', $path
    ))
    if ($stage.Count -ne 1) { throw 'review packet requires one stage-zero blob per path' }
    $match = [regex]::Match(
        $stage[0], '^(?<mode>100644|100755) (?<blob>[0-9a-f]{40}) 0\t(?<path>.+)$'
    )
    if (-not $match.Success -or
        ($match.Groups['path'].Value -replace '\\', '/') -ne $path) {
        throw 'review packet staged blob row is malformed'
    }
    "blob=$path|$($match.Groups['mode'].Value)|$($match.Groups['blob'].Value)"
}
$script:ProjectBReviewPacket = @(
    "root-plan-sha256=$rootPlanSha"
    "detailed-plan-sha256=$detailedPlanSha"
    "base-commit=$($env:PROJECTB_BASE_COMMIT)"
    "review-tree=$($env:PROJECTB_REVIEW_TREE)"
) + $blobRows
$packetBytes = [Text.Encoding]::UTF8.GetBytes(
    (($script:ProjectBReviewPacket -join "`n") + "`n")
)
$sha256 = [Security.Cryptography.SHA256]::Create()
try {
    $env:PROJECTB_REVIEW_PACKET_SHA256 = -join (
        $sha256.ComputeHash($packetBytes) | ForEach-Object { $_.ToString('x2') }
    )
} finally {
    $sha256.Dispose()
}
```

Expected: exit code 0; exactly three paths are staged, the staged diff has no whitespace error, and the in-memory packet binds current root/detailed-plan hashes, predecessor commit, whole-index tree, and each exact stage-zero blob by path/mode/blob ID. Do not write the packet or staged diff to an untracked file.

- [ ] **Step A16: Run the committed scanner against the staged T-03A patch**

Run:

```powershell
Invoke-CheckedNative -FilePath $PowerShellExe -ArgumentList @(
    '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File',
    'scripts/scan_secrets.ps1', '-PythonExe', $PythonExe, '--staged'
)
```

Expected: exit code 0 with no secret value output. Any suspected credential stops the unit without echoing the value.

- [ ] **Step A17: Request the fresh T-03A SPEC review**

The coordinator supplies a fresh non-worker reviewer with SPEC Sections 5.1, 6, 7, 8 and AC-06, AC-07, AC-15, AC-17, AC-27, AC-30, AC-35, AC-40; root T-03/T-03A; this complete plan; predecessor SHA; exact staged diff; every canonical line in `$script:ProjectBReviewPacket`; checked `PROJECTB_REVIEW_PACKET_SHA256` and `PROJECTB_REVIEW_TREE`; and observed red/green/regression/Ruff/mypy/scanner output. The PASS record names that exact packet hash and tree. Record the canonical identity in `PROJECTB_SPEC_REVIEWER_ID`, its tree in `PROJECTB_SPEC_REVIEW_TREE`, and its packet hash in `PROJECTB_SPEC_REVIEW_PACKET_SHA256`.

Expected: `SPEC REVIEW: PASS` with no unresolved Critical or Important finding. The reviewer confirms owner scope, no reconstructive/secret columns, append-only history, complete worker/lease/payload-ref durable-job reservation, material batch/file-state reservation, protected Attempt reference storage, restart repeatability, and that T-03A claims persistence prerequisites rather than full downstream AC completion.

- [ ] **Step A18: Request the different fresh T-03A quality review**

The coordinator gives the same canonical packet lines, packet SHA-256, exact staged diff, and checked tree to another fresh reviewer and records `PROJECTB_QUALITY_REVIEWER_ID`, `PROJECTB_QUALITY_REVIEW_TREE`, and `PROJECTB_QUALITY_REVIEW_PACKET_SHA256`. The PASS record names that packet hash and tree. The reviewer checks SQLite transaction/foreign-key behavior, checksum mismatch handling, direct-insert lowercase-hex and canonical-UTC constraints, STRICT constraints, indexes, triggers, canonical JSON recursion, exception redaction, path ownership, tests, standard-library license impact, and Windows/PyInstaller resource-path risk.

Expected: `QUALITY REVIEW: PASS` with no unresolved Critical or Important finding. Any finding returns to a new failing test and repeats Steps A11-A18.

- [ ] **Step A19: Validate all three T-03A identities**

Run:

```powershell
$identities = @(
    $env:PROJECTB_AGENT_ID
    $env:PROJECTB_SPEC_REVIEWER_ID
    $env:PROJECTB_QUALITY_REVIEWER_ID
)
foreach ($identity in $identities) {
    if ([string]::IsNullOrWhiteSpace($identity) -or
        $identity -notmatch '^[A-Za-z0-9][A-Za-z0-9._-]{1,63}$') {
        throw 'invalid T-03A worker/reviewer identity'
    }
}
if (($identities | Sort-Object -Unique).Count -ne 3) {
    throw 'T-03A worker and reviewers must be pairwise distinct'
}
foreach ($tree in @(
    $env:PROJECTB_REVIEW_TREE
    $env:PROJECTB_SPEC_REVIEW_TREE
    $env:PROJECTB_QUALITY_REVIEW_TREE
)) {
    if ($tree -notmatch '^[0-9a-f]{40}$' -or $tree -ne $env:PROJECTB_REVIEW_TREE) {
        throw 'T-03A reviews must bind to the exact staged tree'
    }
}
foreach ($packetSha in @(
    $env:PROJECTB_REVIEW_PACKET_SHA256
    $env:PROJECTB_SPEC_REVIEW_PACKET_SHA256
    $env:PROJECTB_QUALITY_REVIEW_PACKET_SHA256
)) {
    if ($packetSha -notmatch '^[0-9a-f]{64}$' -or
        $packetSha -ne $env:PROJECTB_REVIEW_PACKET_SHA256) {
        throw 'T-03A reviews must bind to the exact cached-content packet'
    }
}
```

Expected: exit code 0 with three valid, distinct identities.

- [ ] **Step A20: Recheck the exact patch accepted by both reviewers**

Run:

```powershell
Assert-ExactStagedPaths -ExpectedPaths @(
    'backend/src/projectb/infrastructure/migrations/001_initial.sql'
    'backend/src/projectb/infrastructure/sqlite.py'
    'backend/tests/integration/test_sqlite_schema.py'
)
Invoke-CheckedNative -FilePath $GitExe -ArgumentList @('diff', '--cached', '--check')
Invoke-CheckedNative -FilePath $PowerShellExe -ArgumentList @(
    '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File',
    'scripts/scan_secrets.ps1', '-PythonExe', $PythonExe, '--staged'
)
$currentTree = @(Invoke-CheckedNative -FilePath $GitExe -ArgumentList @('write-tree'))
if ($currentTree.Count -ne 1 -or $currentTree[0] -ne $env:PROJECTB_REVIEW_TREE) {
    throw 'T-03A staged tree changed after review'
}
```

Expected: all commands exit 0 and the staged tree is exactly the tree named by both reviews. Any edit returns to Step A15, recaptures/scans the tree, and repeats both reviews.

- [ ] **Step A21: Commit the reviewed T-03A unit**

Run:

```powershell
Invoke-CheckedNative -FilePath $GitExe -ArgumentList @(
    'commit', '-m',
    "feat(T-03A): add idempotent SQLite schema [agent: $env:PROJECTB_AGENT_ID]"
)
```

Expected: exit code 0 with a `feat(T-03A)` subject containing the validated worker identity.

- [ ] **Step A22: Capture the T-03A commit for coordinator evidence**

Run:

```powershell
$commitHash = @(Invoke-CheckedNative -FilePath $GitExe -ArgumentList @('rev-parse', 'HEAD'))
if ($commitHash.Count -ne 1 -or $commitHash[0] -notmatch '^[0-9a-f]{40}$') {
    throw 'T-03A commit hash must be one lowercase 40-hex line'
}
$committedTree = @(
    Invoke-CheckedNative -FilePath $GitExe -ArgumentList @('rev-parse', 'HEAD^{tree}')
)
if ($committedTree.Count -ne 1 -or $committedTree[0] -ne $env:PROJECTB_REVIEW_TREE) {
    throw 'T-03A committed tree differs from the reviewed tree'
}
$commitHash[0]
```

Expected: exit code 0 with one observed 40-character lowercase hexadecimal commit hash. The coordinator records the hash and review evidence before creating T-03B's worktree.

**T-03A completion standard:** The exact three-path unit has observed red and green evidence, focused/integration/full regression, Ruff/mypy/scanner/staged-set evidence, two fresh PASS reviews, and one recorded worker commit. The migration is the sole reviewed schema owner and no downstream repository task has begun.

## Task T-03B: Owner-Scoped Course and Material Version Repositories

**Goal:** Add only the course and material repository behavior on top of the reviewed T-03A schema. Every write is owner-scoped and serialized inside one transaction; immutable version rows are append-only; the active row is advanced only after the new version is durable; identical retries return the existing version; stale or conflicting writes fail with a stable `RepositoryError` code.

**Dependencies / parallelism:** Requires the reviewed T-03A commit and T-02C terminal domain contracts. Runs alone after T-03A. T-03C cannot start until the T-03B worker commit, both fresh reviews, and the recorded hash exist. This unit never edits `sqlite.py` or `001_initial.sql`.

**Files:**
- Create: `backend/src/projectb/infrastructure/repositories/course_repo.py`
- Create: `backend/src/projectb/infrastructure/repositories/material_repo.py`
- Create: `backend/tests/integration/test_course_material_repositories.py`

**Locked T-03B interface:** `CourseRepository.put_versioned(owner_id, course_id, payload, expected_version, created_at_utc)`, `get_active(owner_id, course_id)`, `list_history(owner_id, course_id)`, and `tombstone(owner_id, course_id, reason_code, created_at_utc)`; `MaterialRepository.put_versioned(owner_id, course_id, selected_file, payload, expected_version, created_at_utc)`, `get_active(owner_id, material_id)`, `list_history(owner_id, material_id)`, and `tombstone(owner_id, material_id, reason_code, created_at_utc)`. It also publishes metadata-only `create_batch`, `get_batch`, `put_batch_file`, and `list_batch_files`; these methods store opaque membership, hashes, roles, and optimistic file state but never inspect, parse, normalize, enqueue, or authorize a file. `put_versioned` returns an immutable version record, `get_active` returns the current version record, and `list_history` returns ascending immutable version records. `expected_version=None` is required for a first write. A new payload requires `expected_version` equal to the active version; an exact retry of the already-active payload returns that active record even when it carries the immediately preceding expected version. A missing entity is `not_found`, an existing entity owned by another owner is `owner_forbidden`, and a stale, tombstoned, identity-changing, invalid, or partially persisted state is `state_inconsistent`.

### T-03B data and ownership invariants

- Course payloads are canonical JSON metadata. The repository never accepts or reconstructs a course body, local path, answer, credential, or provider secret; `canonical_json` is the shared T-03A gate.
- A course's `course_id` and `owner_id` never change. A course's version rows are keyed by `(course_id, version)`, are never updated or deleted, and are read in numeric version order.
- A material's `material_id`, `owner_id`, `course_id`, `role`, and 64-character lowercase `content_hash` never change. The active unique index means one live material represents each `(owner_id, course_id, content_hash, role)` identity. A different material ID with the same live identity is a deterministic duplicate and returns the existing record without adding a version.
- A material with `needs_user_review` may be stored as an imported candidate, but this repository never promotes it to authority or remote use; later application services enforce that gate.
- A batch is metadata-only and starts `open`. Each membership row contains one opaque batch-file ID, raw content hash, exact role, optional resolved material ID, redacted error code, and file state. `put_batch_file` is optimistic and idempotent; M1 owns inspection/parser/job orchestration and decides which legal state to request.
- `tombstone` updates only the mutable current row and appends one generic, non-reconstructive `tombstones` row. It never removes version history. Repeating the same tombstone is idempotent; changing its reason is `state_inconsistent`; an active read after tombstoning is `not_found`.
- All mutation methods use `Database.transaction()` (`BEGIN IMMEDIATE`) and catch raw SQLite integrity errors before they cross the repository boundary. No method accepts a table name or arbitrary SQL.

- [ ] **Step B1: Validate the T-03B runtime, identity, predecessor, and exact worktree**

Run exactly from the T-03B worktree:

```powershell
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Test-AbsoluteExistingLeaf {
    param([Parameter(Mandatory)][string]$Value)
    if ([string]::IsNullOrWhiteSpace($Value) -or
        $Value -notmatch '^(?:[A-Za-z]:[\\/]|\\\\[^\\/]+[\\/][^\\/]+[\\/])') {
        return $false
    }
    try { $null = [IO.Path]::GetFullPath($Value) } catch { return $false }
    return Test-Path -LiteralPath $Value -PathType Leaf
}

if (-not ('ProjectBProcessTree' -as [type])) {
    Add-Type -TypeDefinition @'
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Runtime.InteropServices;
public static class ProjectBProcessTree {
    [StructLayout(LayoutKind.Sequential)] struct BasicInfo {
        public IntPtr Reserved1, Peb, Reserved20, Reserved21, ProcessId, ParentProcessId;
    }
    [DllImport("ntdll.dll")] static extern int NtQueryInformationProcess(
        IntPtr handle, int kind, ref BasicInfo info, int length, out int returned);
    public static int[] Descendants(int root) {
        var map = new Dictionary<int, List<int>>();
        foreach (var process in Process.GetProcesses()) {
            try {
                var info = new BasicInfo(); int returned;
                if (NtQueryInformationProcess(process.Handle, 0, ref info,
                    Marshal.SizeOf(typeof(BasicInfo)), out returned) != 0) continue;
                int parent = info.ParentProcessId.ToInt32();
                if (!map.ContainsKey(parent)) map[parent] = new List<int>();
                map[parent].Add(process.Id);
            } catch { } finally { process.Dispose(); }
        }
        var result = new List<int>(); var queue = new Queue<int>(); queue.Enqueue(root);
        while (queue.Count > 0) {
            int parent = queue.Dequeue(); List<int> children;
            if (!map.TryGetValue(parent, out children)) continue;
            foreach (int child in children) { result.Add(child); queue.Enqueue(child); }
        }
        return result.ToArray();
    }
}
'@
}

```

- [ ] **Step B1.1: Define bounded non-privileged process-tree cleanup**

Continue in the same checked PowerShell session:

```powershell
function Stop-NativeProcessTree {
    param([Parameter(Mandatory)][Diagnostics.Process]$Process)
    $rootId = $Process.Id
    $descendants = @([ProjectBProcessTree]::Descendants($rootId))
    Stop-Process -Id $rootId -Force -ErrorAction SilentlyContinue
    $descendants += @([ProjectBProcessTree]::Descendants($rootId))
    $targets = @($descendants | Sort-Object -Unique)
    if ($targets -contains $PID) { throw 'native timeout tree included the host process' }
    [array]::Reverse($targets)
    foreach ($target in $targets) {
        Stop-Process -Id $target -Force -ErrorAction SilentlyContinue
    }
    $deadline = [Diagnostics.Stopwatch]::StartNew()
    do {
        $alive = @(@($rootId) + $targets | Where-Object {
            Get-Process -Id $_ -ErrorAction SilentlyContinue
        })
        if ($alive.Count -gt 0) { Start-Sleep -Milliseconds 25 }
    } while ($alive.Count -gt 0 -and $deadline.ElapsedMilliseconds -lt 5000)
    if ($alive.Count -gt 0) { throw 'native command timeout cleanup failed' }
}

function ConvertTo-NativeArgument {
    param([Parameter(Mandatory)][AllowEmptyString()][string]$Value)
    if ($Value.Length -gt 0 -and $Value -notmatch '[\s"]') { return $Value }
    $builder = [Text.StringBuilder]::new()
    [void]$builder.Append('"')
    $slashes = 0
    foreach ($character in $Value.ToCharArray()) {
        if ($character -eq '\') { $slashes++; continue }
        if ($character -eq '"') {
            [void]$builder.Append(('\' * (($slashes * 2) + 1)))
            [void]$builder.Append('"')
            $slashes = 0
            continue
        }
        if ($slashes -gt 0) { [void]$builder.Append(('\' * $slashes)); $slashes = 0 }
        [void]$builder.Append($character)
    }
    if ($slashes -gt 0) { [void]$builder.Append(('\' * ($slashes * 2))) }
    [void]$builder.Append('"')
    return $builder.ToString()
}

```

- [ ] **Step B1.2: Define `Invoke-NativeProcess`**

Continue in the same checked PowerShell session:

```powershell
function Invoke-NativeProcess {
    param(
        [Parameter(Mandatory)][string]$FilePath,
        [Parameter(Mandatory)][AllowEmptyCollection()][AllowEmptyString()][string[]]$ArgumentList,
        [ValidateRange(1, 3600)][int]$TimeoutSeconds = 600
    )
    if (-not (Test-AbsoluteExistingLeaf -Value $FilePath)) {
        throw 'native executable must be an absolute existing leaf'
    }
    $start = [Diagnostics.ProcessStartInfo]::new()
    $start.FileName = $FilePath
    $start.Arguments = (($ArgumentList | ForEach-Object {
        ConvertTo-NativeArgument -Value $_
    }) -join ' ')
    $start.UseShellExecute = $false
    $start.CreateNoWindow = $true
    $start.RedirectStandardOutput = $true
    $start.RedirectStandardError = $true
    $process = [Diagnostics.Process]::new()
    $process.StartInfo = $start
    try {
        try {
            if (-not $process.Start()) { throw 'start returned false' }
        } catch {
            throw 'native command launch failed'
        }
        $stdoutTask = $process.StandardOutput.ReadToEndAsync()
        $stderrTask = $process.StandardError.ReadToEndAsync()
        if (-not $process.WaitForExit($TimeoutSeconds * 1000)) {
            Stop-NativeProcessTree -Process $process
            $process.WaitForExit()
            throw "native command timed out after $TimeoutSeconds seconds"
        }
        $process.WaitForExit()
        $stdout = $stdoutTask.Result.TrimEnd([char[]]"`r`n")
        $null = $stderrTask.Result
        $lines = if ($stdout.Length -eq 0) { @() } else { @($stdout -split "`r?`n") }
        return [pscustomobject]@{ ExitCode = $process.ExitCode; Stdout = $lines }
    } finally {
        $process.Dispose()
    }
}
```

- [ ] **Step B1.3: Define `Invoke-CheckedNative` through `Invoke-ExpectedNativeExit`**

Continue in the same checked PowerShell session:

```powershell

function Invoke-CheckedNative {
    param(
        [Parameter(Mandatory)][string]$FilePath,
        [Parameter(Mandatory)][AllowEmptyCollection()][AllowEmptyString()][string[]]$ArgumentList,
        [ValidateRange(1, 3600)][int]$TimeoutSeconds = 600
    )
    $result = Invoke-NativeProcess -FilePath $FilePath -ArgumentList $ArgumentList `
        -TimeoutSeconds $TimeoutSeconds
    if ($result.ExitCode -ne 0) {
        throw "native command failed with exit code $($result.ExitCode)"
    }
    return @($result.Stdout)
}

function Invoke-ExpectedNativeExit {
    param(
        [Parameter(Mandatory)][string]$FilePath,
        [Parameter(Mandatory)][AllowEmptyCollection()][AllowEmptyString()][string[]]$ArgumentList,
        [Parameter(Mandatory)][int]$ExpectedExitCode,
        [ValidateRange(1, 3600)][int]$TimeoutSeconds = 600
    )
    $result = Invoke-NativeProcess -FilePath $FilePath -ArgumentList $ArgumentList `
        -TimeoutSeconds $TimeoutSeconds
    if ($result.ExitCode -ne $ExpectedExitCode) {
        throw "native command returned unexpected exit code $($result.ExitCode)"
    }
    return @($result.Stdout)
}

$GitExe = (Get-Command git -CommandType Application -ErrorAction Stop).Source
if (-not (Test-AbsoluteExistingLeaf -Value $GitExe)) {
    throw 'git executable must be an absolute existing leaf'
}
$PythonExe = $env:PROJECTB_PYTHON_EXE
$PowerShellExe = $env:PROJECTB_POWERSHELL_EXE
foreach ($pair in @(@('Python', $PythonExe), @('PowerShell', $PowerShellExe))) {
    if (-not (Test-AbsoluteExistingLeaf -Value $pair[1])) {
        throw "$($pair[0]) executable must be an absolute existing leaf"
    }
}
```

- [ ] **Step B1.4: Define `Assert-NativeWrapperContract`**

Continue in the same checked PowerShell session:

```powershell
function Assert-NativeWrapperContract {
    param([Parameter(Mandatory)][string]$PythonPath)
    $empty = @(Invoke-CheckedNative -FilePath $PythonPath -ArgumentList @('-c', ''))
    if ($empty.Count -ne 0) { throw 'empty native output was not preserved' }
    $multiline = @(Invoke-CheckedNative -FilePath $PythonPath -ArgumentList @(
        '-c', "print('first'); print('second')"
    ))
    if ($multiline.Count -ne 2 -or $multiline[0] -ne 'first' -or
        $multiline[1] -ne 'second') {
        throw 'multiline native output was malformed'
    }
    $marker = 'sensitive-child-output-must-not-surface'
    $failure = $null
    try {
        Invoke-CheckedNative -FilePath $PythonPath -ArgumentList @(
            '-c', "import sys; print('$marker'); sys.exit(7)"
        ) -TimeoutSeconds 10
    } catch { $failure = $_.Exception.Message }
    if ($failure -ne 'native command failed with exit code 7' -or
        $failure.Contains($marker)) {
        throw 'nonzero diagnostics were not sanitized'
    }
    $wrongExecutable = (Resolve-Path -LiteralPath 'PLAN.md').Path
    $failure = $null
    try {
        Invoke-CheckedNative -FilePath $wrongExecutable -ArgumentList @() -TimeoutSeconds 10
    } catch { $failure = $_.Exception.Message }
    if ($failure -ne 'native command launch failed') {
        throw 'wrong executable did not fail closed'
    }
    $probeRoot = Join-Path ([IO.Path]::GetTempPath()) (
        'projectb-native-probe-' + [guid]::NewGuid().ToString('N')
    )
    [IO.Directory]::CreateDirectory($probeRoot) | Out-Null
    $pidFile = Join-Path $probeRoot 'child.pid'
    $probe = "import pathlib,subprocess,sys,time; " +
        "child=subprocess.Popen([sys.executable,'-c','import time; time.sleep(30)']); " +
        "pathlib.Path(sys.argv[1]).write_text(str(child.pid),encoding='ascii'); time.sleep(30)"
    $failure = $null
    try {
        Invoke-CheckedNative -FilePath $PythonPath -ArgumentList @('-c', $probe, $pidFile) `
            -TimeoutSeconds 1
    } catch { $failure = $_.Exception.Message }
    if ($failure -ne 'native command timed out after 1 seconds' -or
        -not (Test-Path -LiteralPath $pidFile -PathType Leaf)) {
        throw 'native timeout probe failed'
    }
    $childPid = [int]([IO.File]::ReadAllText($pidFile).Trim())
    Start-Sleep -Milliseconds 250
    if (Get-Process -Id $childPid -ErrorAction SilentlyContinue) {
        throw 'native timeout left a descendant process running'
    }
    [IO.File]::Delete($pidFile)
    [IO.Directory]::Delete($probeRoot)
}
```

- [ ] **Step B1.5: Run the bounded native-wrapper contract probe**

Continue in the same checked PowerShell session:

```powershell
Assert-NativeWrapperContract -PythonPath $PythonExe
$pythonVersion = @(Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    '-c', 'import platform; print(platform.python_version())'
))
if ($pythonVersion.Count -ne 1 -or $pythonVersion[0].Trim() -ne '3.14.6') {
    throw 'T-03B requires CPython 3.14.6'
}
$ruffVersion = @(Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    '-m', 'ruff', '--version'
))
$mypyVersion = @(Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    '-m', 'mypy', '--version'
))
$pytestVersion = @(Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    '-m', 'pytest', '--version'
))
if ($ruffVersion.Count -ne 1 -or $ruffVersion[0].Trim() -ne 'ruff 0.15.22') {
    throw 'T-03B requires Ruff 0.15.22'
}
if ($mypyVersion.Count -ne 1 -or $mypyVersion[0].Trim() -notmatch '^mypy 2\.3\.0(?: |$)') {
    throw 'T-03B requires mypy 2.3.0'
}
if ($pytestVersion.Count -ne 1 -or $pytestVersion[0].Trim() -ne 'pytest 9.1.1') {
    throw 'T-03B requires pytest 9.1.1'
}
$powerShellOutput = @(Invoke-CheckedNative -FilePath $PowerShellExe -ArgumentList @(
    '-NoProfile', '-Command', '$PSVersionTable.PSVersion.ToString()'
))
if ($powerShellOutput.Count -ne 1) { throw 'PowerShell version output must be one line' }
$powerShellVersion = $powerShellOutput[0].Trim()
$parsedPowerShellVersion = $null
if (-not [Version]::TryParse($powerShellVersion, [ref]$parsedPowerShellVersion)) {
    throw 'PowerShell version is not parseable'
}
foreach ($name in @('PROJECTB_AGENT_ID', 'PROJECTB_UNIT_ID', 'PROJECTB_BASE_COMMIT', 'PROJECTB_WORKTREE_ROOT')) {
    if ([string]::IsNullOrWhiteSpace([Environment]::GetEnvironmentVariable($name))) {
        throw "$name is required"
    }
}
if ($env:PROJECTB_AGENT_ID -notmatch '^[A-Za-z0-9][A-Za-z0-9._-]{1,63}$') {
    throw 'PROJECTB_AGENT_ID is invalid'
}
```

- [ ] **Step B1.6: Define `Assert-ExactStagedPaths`**

Continue in the same checked PowerShell session:

```powershell
if ($env:PROJECTB_UNIT_ID -ne 'T-03B') { throw 'wrong dispatch unit' }
if ($env:PROJECTB_BASE_COMMIT -notmatch '^[0-9a-f]{40}$') { throw 'T-03B predecessor SHA is invalid' }
$head = @(Invoke-CheckedNative -FilePath $GitExe -ArgumentList @('rev-parse', 'HEAD'))
if ($head.Count -ne 1 -or $head[0] -notmatch '^[0-9a-f]{40}$' -or
    $head[0].Trim() -ne $env:PROJECTB_BASE_COMMIT) {
    throw 'T-03B worktree is not at the reviewed T-03A commit'
}
$resolvedRoot = (Resolve-Path -LiteralPath '.').Path
if ($resolvedRoot -ne (Resolve-Path -LiteralPath $env:PROJECTB_WORKTREE_ROOT).Path) {
    throw 'wrong worktree root'
}
$status = @(Invoke-CheckedNative -FilePath $GitExe -ArgumentList @('status', '--porcelain'))
if ($status.Count -ne 0) { throw 'T-03B worktree must start clean' }
$allowed = @(
    'backend/src/projectb/infrastructure/repositories/course_repo.py'
    'backend/src/projectb/infrastructure/repositories/material_repo.py'
    'backend/tests/integration/test_course_material_repositories.py'
)
$tracked = @(
    Invoke-CheckedNative -FilePath $GitExe -ArgumentList (@('ls-files', '--') + $allowed)
)
if ($tracked.Count -ne 0) { throw 'T-03B owned paths already exist in the predecessor' }
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
$env:PYTHONPATH = (Resolve-Path -LiteralPath 'backend/src').Path
```

Expected: exit code 0, CPython reports exactly `3.14.6`, the worktree is clean at the reviewed T-03A SHA, and no migration or database-wrapper path is owned by this worker.

- [ ] **Step B2A: Create repository fixtures and course behavior tests**

Create `backend/tests/integration/test_course_material_repositories.py` with exactly:

```python
from __future__ import annotations

import json

import pytest
from projectb.domain.materials import MaterialReviewState, MaterialRole, SelectedFile
from projectb.domain.types import CourseId, MaterialId
from projectb.infrastructure.repositories.course_repo import CourseRepository
from projectb.infrastructure.repositories.material_repo import MaterialRepository
from projectb.infrastructure.sqlite import Database, RepositoryError

OWNER_A = "owner-a"
OWNER_B = "owner-b"
COURSE_ID = CourseId("course-a")
HASH = "a" * 64
CREATED = "2026-07-23T00:00:00Z"
UPDATED = "2026-07-23T00:01:00Z"


@pytest.fixture
def database(tmp_path):
    database = Database.open(tmp_path / "course-material.sqlite3")
    database.migrate()
    try:
        yield database
    finally:
        database.close()


@pytest.fixture
def course(database: Database) -> CourseRepository:
    repository = CourseRepository(database)
    repository.put_versioned(
        OWNER_A,
        COURSE_ID,
        {"title": "Concurrency", "course_ref": "local-course-a"},
        expected_version=None,
        created_at_utc=CREATED,
    )
    return repository


```

- [ ] **Step B2A.2: Append `selected` through `test_course_versions_are_append_only_and_idempotent`**

Append exactly to `backend/tests/integration/test_course_material_repositories.py`:

```python
def selected(
    material_id: str = "material-a",
    role: MaterialRole = MaterialRole.LECTURE,
    content_hash: str = HASH,
) -> SelectedFile:
    return SelectedFile(
        material_id=MaterialId(material_id),
        display_name="lecture.pdf",
        role=role,
        content_hash=content_hash,
        size_bytes=128,
        review_state=MaterialReviewState.ACCEPTED,
    )


def assert_code(code: str, operation) -> None:
    with pytest.raises(RepositoryError) as caught:
        operation()
    assert caught.value.code == code


def test_course_versions_are_append_only_and_idempotent(
    course: CourseRepository,
) -> None:
    first = course.get_active(OWNER_A, COURSE_ID)
    assert first.version == 1
    same = course.put_versioned(
        OWNER_A,
        COURSE_ID,
        {"title": "Concurrency", "course_ref": "local-course-a"},
        expected_version=1,
        created_at_utc=UPDATED,
    )
    assert same == first
    second = course.put_versioned(
        OWNER_A,
        COURSE_ID,
        {"title": "Concurrency II", "course_ref": "local-course-a"},
        expected_version=1,
        created_at_utc=UPDATED,
```

- [ ] **Step B2A.3: Append `test_course_material_repositories.py` continuation slice 3**

Append exactly to `backend/tests/integration/test_course_material_repositories.py`:

```python
    )
    assert second.version == 2
    assert (
        course.put_versioned(
            OWNER_A,
            COURSE_ID,
            {"title": "Concurrency II", "course_ref": "local-course-a"},
            expected_version=1,
            created_at_utc=UPDATED,
        )
        == second
    )
    assert [item.version for item in course.list_history(OWNER_A, COURSE_ID)] == [1, 2]
    assert json.loads(second.payload_json)["title"] == "Concurrency II"
    assert_code(
        "state_inconsistent",
        lambda: course.put_versioned(
            OWNER_A,
            COURSE_ID,
            {"title": "stale"},
            expected_version=1,
            created_at_utc=UPDATED,
        ),
    )


```

- [ ] **Step B2A.4: Append `test_course_owner_scope_and_tombstone_preserve_history`**

Append exactly to `backend/tests/integration/test_course_material_repositories.py`:

```python
def test_course_owner_scope_and_tombstone_preserve_history(
    course: CourseRepository,
) -> None:
    assert_code("owner_forbidden", lambda: course.get_active(OWNER_B, COURSE_ID))
    assert_code(
        "owner_forbidden",
        lambda: course.put_versioned(
            OWNER_B,
            COURSE_ID,
            {"title": "cross-owner"},
            expected_version=1,
            created_at_utc=UPDATED,
        ),
    )
    course.tombstone(OWNER_A, COURSE_ID, "user_deleted", UPDATED)
    assert_code("not_found", lambda: course.get_active(OWNER_A, COURSE_ID))
    assert [item.version for item in course.list_history(OWNER_A, COURSE_ID)] == [1]
    course.tombstone(OWNER_A, COURSE_ID, "user_deleted", UPDATED)
    assert_code(
        "state_inconsistent",
        lambda: course.tombstone(OWNER_A, COURSE_ID, "different_reason", UPDATED),
    )


```

- [ ] **Step B2B: Append material identity, owner, tombstone, and redaction tests**

Append exactly to `backend/tests/integration/test_course_material_repositories.py`:

```python
def test_material_duplicate_hash_role_returns_existing_and_versions_material(
    database: Database, course: CourseRepository
) -> None:
    repository = MaterialRepository(database)
    first = repository.put_versioned(
        OWNER_A,
        COURSE_ID,
        selected(),
        {"display_name": "lecture.pdf", "review_state": "accepted"},
        expected_version=None,
        created_at_utc=CREATED,
    )
    duplicate = repository.put_versioned(
        OWNER_A,
        COURSE_ID,
        selected("material-duplicate"),
        {"display_name": "renamed.pdf", "review_state": "accepted"},
        expected_version=None,
        created_at_utc=UPDATED,
    )
    assert duplicate.material_id == first.material_id
    changed = repository.put_versioned(
        OWNER_A,
        COURSE_ID,
        selected(),
        {"display_name": "lecture.pdf", "review_state": "accepted", "batch": 2},
        expected_version=1,
        created_at_utc=UPDATED,
    )
    assert changed.version == 2
    assert (
        repository.put_versioned(
            OWNER_A,
            COURSE_ID,
            selected(),
            {"display_name": "lecture.pdf", "review_state": "accepted", "batch": 2},
            expected_version=1,
            created_at_utc=UPDATED,
        )
        == changed
    )
    assert [item.version for item in repository.list_history(OWNER_A, first.material_id)] == [1, 2]


```

- [ ] **Step B2B.2: Append `test_material_identity_conflicts_owner_scope_and_tombstone`**

Append exactly to `backend/tests/integration/test_course_material_repositories.py`:

```python
def test_material_identity_conflicts_owner_scope_and_tombstone(
    database: Database, course: CourseRepository
) -> None:
    repository = MaterialRepository(database)
    repository.put_versioned(
        OWNER_A,
        COURSE_ID,
        selected(),
        {"display_name": "lecture.pdf", "review_state": "accepted"},
        expected_version=None,
        created_at_utc=CREATED,
    )
    assert_code(
        "state_inconsistent",
        lambda: repository.put_versioned(
            OWNER_A,
            COURSE_ID,
            selected(role=MaterialRole.PAST_PAPER),
            {"display_name": "lecture.pdf"},
            expected_version=1,
            created_at_utc=UPDATED,
        ),
    )
    assert_code(
        "owner_forbidden",
        lambda: repository.get_active(OWNER_B, MaterialId("material-a")),
    )
    repository.tombstone(OWNER_A, MaterialId("material-a"), "user_deleted", UPDATED)
    assert_code("not_found", lambda: repository.get_active(OWNER_A, MaterialId("material-a")))
    assert [
        item.version for item in repository.list_history(OWNER_A, MaterialId("material-a"))
    ] == [1]


```

- [ ] **Step B2B.3: Append `test_material_payload_rejects_body_and_path_without_partial_write`**

Append exactly to `backend/tests/integration/test_course_material_repositories.py`:

```python
def test_material_payload_rejects_body_and_path_without_partial_write(
    database: Database, course: CourseRepository
) -> None:
    repository = MaterialRepository(database)
    assert_code(
        "state_inconsistent",
        lambda: repository.put_versioned(
            OWNER_A,
            COURSE_ID,
            selected(),
            {"path": "C:/private/lecture.pdf"},
            expected_version=None,
            created_at_utc=CREATED,
        ),
    )
    assert_code("not_found", lambda: repository.get_active(OWNER_A, MaterialId("material-a")))
```

- [ ] **Step B3A: Append active-row rollback assertions**

Append exactly to `backend/tests/integration/test_course_material_repositories.py`:

```python


def test_material_write_rolls_back_when_the_active_update_cannot_commit(
    database: Database, course: CourseRepository, monkeypatch: pytest.MonkeyPatch
) -> None:
    repository = MaterialRepository(database)
    repository.put_versioned(
        OWNER_A,
        COURSE_ID,
        selected(),
        {"display_name": "lecture.pdf", "review_state": "accepted"},
        expected_version=None,
        created_at_utc=CREATED,
    )
    original_execute = Database.execute
    calls = 0

    def fail_on_active_update(self, statement: str, parameters=()):
        nonlocal calls
        if statement.startswith("UPDATE materials SET active_version"):
            calls += 1
            raise RuntimeError("forced active-row failure")
        return original_execute(self, statement, parameters)

    monkeypatch.setattr(Database, "execute", fail_on_active_update)
    with pytest.raises(RuntimeError, match="forced active-row failure"):
        repository.put_versioned(
            OWNER_A,
            COURSE_ID,
            selected(),
            {"display_name": "lecture-v2.pdf", "review_state": "accepted"},
            expected_version=1,
            created_at_utc=UPDATED,
        )
    assert calls == 1
    assert repository.get_active(OWNER_A, MaterialId("material-a")).version == 1
    assert [
        item.version for item in repository.list_history(OWNER_A, MaterialId("material-a"))
    ] == [1]


```

- [ ] **Step B3B: Append restart persistence assertions**

Append exactly to `backend/tests/integration/test_course_material_repositories.py`:

```python
def test_reopening_database_keeps_course_and_material_history(tmp_path) -> None:
    path = tmp_path / "restart.sqlite3"
    first_database = Database.open(path)
    first_database.migrate()
    first_course = CourseRepository(first_database)
    first_material = MaterialRepository(first_database)
    first_course.put_versioned(
        OWNER_A,
        COURSE_ID,
        {"title": "Restart"},
        expected_version=None,
        created_at_utc=CREATED,
    )
    first_material.put_versioned(
        OWNER_A,
        COURSE_ID,
        selected(),
        {"display_name": "lecture.pdf", "review_state": "accepted"},
        expected_version=None,
        created_at_utc=CREATED,
    )
    first_database.close()

    second_database = Database.open(path)
    second_database.migrate()
    try:
        assert CourseRepository(second_database).get_active(OWNER_A, COURSE_ID).version == 1
        assert (
            MaterialRepository(second_database)
            .get_active(OWNER_A, MaterialId("material-a"))
            .version
            == 1
        )
    finally:
        second_database.close()


```

- [ ] **Step B3C: Append batch membership and independent file-state tests**

Append exactly to `backend/tests/integration/test_course_material_repositories.py`:

```python
def test_material_batch_membership_keeps_independent_file_state(
    database: Database, course: CourseRepository
) -> None:
    repository = MaterialRepository(database)
    repository.put_versioned(
        OWNER_A,
        COURSE_ID,
        selected(),
        {"display_name": "lecture.pdf", "review_state": "accepted"},
        expected_version=None,
        created_at_utc=CREATED,
    )
    batch = repository.create_batch(OWNER_A, COURSE_ID, "batch-a", "L", created_at_utc=CREATED)
    assert batch.state == "open"
    ready = repository.put_batch_file(
        OWNER_A,
        "batch-a",
        "batch-file-a",
        HASH,
        MaterialRole.LECTURE,
        "ready",
        material_id=MaterialId("material-a"),
        error_code=None,
        expected_state=None,
        updated_at_utc=UPDATED,
    )
    failed = repository.put_batch_file(
        OWNER_A,
        "batch-a",
        "batch-file-b",
        "b" * 64,
        MaterialRole.LECTURE,
        "failed",
        material_id=None,
        error_code="parser_failed",
        expected_state=None,
        updated_at_utc=UPDATED,
    )
```

- [ ] **Step B3C.2: Append `test_course_material_repositories.py` continuation slice 2**

Append exactly to `backend/tests/integration/test_course_material_repositories.py`:

```python
    assert ready.material_id == MaterialId("material-a")
    assert failed.error_code == "parser_failed"
    assert [item.state for item in repository.list_batch_files(OWNER_A, "batch-a")] == [
        "ready",
        "failed",
    ]
    assert_code("owner_forbidden", lambda: repository.get_batch(OWNER_B, "batch-a"))


```

- [ ] **Step B3D: Append optimistic batch-file and redacted-error tests**

Append exactly to `backend/tests/integration/test_course_material_repositories.py`:

```python
def test_material_batch_file_update_is_optimistic_and_rejects_unsafe_error_code(
    database: Database, course: CourseRepository
) -> None:
    repository = MaterialRepository(database)
    repository.create_batch(OWNER_A, COURSE_ID, "batch-a", "L", created_at_utc=CREATED)
    repository.put_batch_file(
        OWNER_A,
        "batch-a",
        "batch-file-a",
        HASH,
        MaterialRole.LECTURE,
        "inspected",
        material_id=None,
        error_code=None,
        expected_state=None,
        updated_at_utc=CREATED,
    )
    failed = repository.put_batch_file(
        OWNER_A,
        "batch-a",
        "batch-file-a",
        HASH,
        MaterialRole.LECTURE,
        "failed",
        material_id=None,
        error_code="parser_failed",
        expected_state="inspected",
        updated_at_utc=UPDATED,
    )
    assert failed.state == "failed"
    assert_code(
        "state_inconsistent",
        lambda: repository.put_batch_file(
            OWNER_A,
            "batch-a",
            "batch-file-a",
            HASH,
            MaterialRole.LECTURE,
            "failed",
            material_id=None,
            error_code="C:/private/input.pdf",
            expected_state="failed",
            updated_at_utc=UPDATED,
        ),
    )
```

Expected red behavior after Steps B2-B3: collection fails because both repository modules are absent; after the modules exist, the rollback test initially fails until the transaction and exception boundary are implemented. The tests intentionally assert observed failures, not a predicted count.

- [ ] **Step B4: Run the T-03B focused tests and capture the expected red result**

Run:

```powershell
$env:PYTHONPATH = (Resolve-Path 'backend/src').Path
Invoke-ExpectedNativeExit -FilePath $PythonExe -ArgumentList @(
    '-m', 'pytest', '-c', 'backend/pyproject.toml',
    'backend/tests/integration/test_course_material_repositories.py', '-q'
) -ExpectedExitCode 2
```

Expected: exit code 2 during collection because `projectb.infrastructure.repositories.course_repo` and `material_repo` do not yet exist. Save the complete red output as evidence; do not weaken or delete a failing assertion.

- [ ] **Step B5A: Create course record and validation helpers**

Create `backend/src/projectb/infrastructure/repositories/course_repo.py` with exactly:

```python
from __future__ import annotations

import sqlite3
from collections.abc import Mapping
from dataclasses import dataclass

from projectb.domain.types import CourseId
from projectb.infrastructure.sqlite import (
    Database,
    JsonValue,
    RepositoryError,
    canonical_json,
    parse_json_object,
    require_opaque_id,
    require_utc,
    require_version,
)


@dataclass(frozen=True, slots=True)
class CourseVersion:
    course_id: CourseId
    owner_id: str
    version: int
    payload_json: str
    created_at_utc: str

    @property
    def payload(self) -> dict[str, JsonValue]:
        return parse_json_object(self.payload_json)


def _reason_code(value: object) -> str:
    if not isinstance(value, str) or not value or value.strip() != value:
        raise RepositoryError("state_inconsistent")
    if len(value) > 64 or any(
        character not in "abcdefghijklmnopqrstuvwxyz0123456789_-" for character in value
    ):
        raise RepositoryError("state_inconsistent")
    return value


```

- [ ] **Step B5B: Append course repository row adapters**

Append exactly to `backend/src/projectb/infrastructure/repositories/course_repo.py`:

```python
class CourseRepository:
    def __init__(self, database: Database) -> None:
        self._database = database

    @staticmethod
    def _version(row: sqlite3.Row) -> CourseVersion:
        return CourseVersion(
            course_id=CourseId(str(row["course_id"])),
            owner_id=str(row["owner_id"]),
            version=int(row["version"]),
            payload_json=str(row["payload_json"]),
            created_at_utc=str(row["created_at_utc"]),
        )

    def _course_row(self, course_id: CourseId) -> sqlite3.Row | None:
        return self._database.fetch_one(
            "SELECT course_id, owner_id, active_version, tombstoned_at_utc "
            "FROM courses WHERE course_id = ?",
            (str(course_id),),
        )

    @staticmethod
    def _check_owner(row: sqlite3.Row, owner_id: str) -> None:
        if str(row["owner_id"]) != owner_id:
            raise RepositoryError("owner_forbidden")

    def _active_version(
        self, course_id: CourseId, owner_id: str, active_version: int
    ) -> CourseVersion:
        row = self._database.fetch_one(
            "SELECT course_id, owner_id, version, payload_json, created_at_utc "
            "FROM course_versions WHERE course_id = ? AND owner_id = ? AND version = ?",
            (str(course_id), owner_id, active_version),
        )
        if row is None:
            raise RepositoryError("state_inconsistent")
        return self._version(row)

```

- [ ] **Step B5C: Append optimistic course version writes**

Append exactly to `backend/src/projectb/infrastructure/repositories/course_repo.py`:

```python
    def put_versioned(
        self,
        owner_id: str,
        course_id: CourseId,
        payload: Mapping[str, object],
        *,
        expected_version: int | None,
        created_at_utc: str,
    ) -> CourseVersion:
        owner_id = require_opaque_id(owner_id)
        course_id = CourseId(require_opaque_id(course_id))
        if expected_version is not None:
            require_version(expected_version)
        created_at_utc = require_utc(created_at_utc)
        payload_json = canonical_json(payload)
        try:
            with self._database.transaction():
                current = self._course_row(course_id)
                if current is None:
                    if expected_version is not None:
                        raise RepositoryError("state_inconsistent")
                    self._database.execute(
                        "INSERT INTO courses(course_id, owner_id, active_version, "
                        "created_at_utc, "
                        "updated_at_utc) "
                        "VALUES (?, ?, 1, ?, ?)",
                        (str(course_id), owner_id, created_at_utc, created_at_utc),
                    )
                    self._database.execute(
                        "INSERT INTO course_versions(course_id, owner_id, version, "
                        "payload_json, "
                        "created_at_utc) "
                        "VALUES (?, ?, 1, ?, ?)",
                        (str(course_id), owner_id, payload_json, created_at_utc),
                    )
                    return self._active_version(course_id, owner_id, 1)
                self._check_owner(current, owner_id)
                if current["tombstoned_at_utc"] is not None:
```

- [ ] **Step B5C.2: Append `course_repo.py` continuation slice 2**

Append exactly to `backend/src/projectb/infrastructure/repositories/course_repo.py`:

```python
                    raise RepositoryError("state_inconsistent")
                active_version = int(current["active_version"])
                active = self._active_version(course_id, owner_id, active_version)
                if active.payload_json == payload_json:
                    allowed_retry_versions: set[int | None] = {active_version}
                    if active_version == 1:
                        allowed_retry_versions.add(None)
                    else:
                        allowed_retry_versions.add(active_version - 1)
                    if expected_version not in allowed_retry_versions:
                        raise RepositoryError("state_inconsistent")
                    return active
                if expected_version != active_version:
                    raise RepositoryError("state_inconsistent")
                next_version = active_version + 1
                self._database.execute(
                    "INSERT INTO course_versions(course_id, owner_id, version, payload_json, "
                    "created_at_utc) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (
                        str(course_id),
                        owner_id,
                        next_version,
                        payload_json,
                        created_at_utc,
                    ),
                )
                self._database.execute(
                    "UPDATE courses SET active_version = ?, updated_at_utc = ? "
                    "WHERE course_id = ? AND owner_id = ? AND active_version = ?",
                    (
                        next_version,
                        created_at_utc,
                        str(course_id),
                        owner_id,
                        active_version,
                    ),
                )
                return self._active_version(course_id, owner_id, next_version)
        except RepositoryError:
            raise
        except sqlite3.IntegrityError as error:
            raise RepositoryError("state_inconsistent") from error

```

- [ ] **Step B5D: Append course active/history/tombstone reads and exports**

Append exactly to `backend/src/projectb/infrastructure/repositories/course_repo.py`:

```python
    def get_active(self, owner_id: str, course_id: CourseId) -> CourseVersion:
        owner_id = require_opaque_id(owner_id)
        course_id = CourseId(require_opaque_id(course_id))
        row = self._course_row(course_id)
        if row is None:
            raise RepositoryError("not_found")
        self._check_owner(row, owner_id)
        if row["tombstoned_at_utc"] is not None:
            raise RepositoryError("not_found")
        return self._active_version(course_id, owner_id, int(row["active_version"]))

    def list_history(self, owner_id: str, course_id: CourseId) -> tuple[CourseVersion, ...]:
        owner_id = require_opaque_id(owner_id)
        course_id = CourseId(require_opaque_id(course_id))
        row = self._course_row(course_id)
        if row is None:
            raise RepositoryError("not_found")
        self._check_owner(row, owner_id)
        rows = self._database.fetch_all(
            "SELECT course_id, owner_id, version, payload_json, created_at_utc "
            "FROM course_versions WHERE course_id = ? AND owner_id = ? ORDER BY version",
            (str(course_id), owner_id),
        )
        if not rows:
            raise RepositoryError("state_inconsistent")
        return tuple(self._version(item) for item in rows)

```

- [ ] **Step B5D.2: Append `tombstone`**

Append exactly to `backend/src/projectb/infrastructure/repositories/course_repo.py`:

```python
    def tombstone(
        self, owner_id: str, course_id: CourseId, reason_code: str, created_at_utc: str
    ) -> None:
        owner_id = require_opaque_id(owner_id)
        course_id = CourseId(require_opaque_id(course_id))
        reason_code = _reason_code(reason_code)
        created_at_utc = require_utc(created_at_utc)
        tombstone_id = f"course:{course_id}"
        with self._database.transaction():
            row = self._course_row(course_id)
            if row is None:
                raise RepositoryError("not_found")
            self._check_owner(row, owner_id)
            existing = self._database.fetch_one(
                "SELECT reason_code FROM tombstones WHERE owner_id = ? AND entity_kind = "
                "'course' "
                "AND entity_id = ?",
                (owner_id, str(course_id)),
            )
            if existing is not None:
                if str(existing["reason_code"]) != reason_code:
                    raise RepositoryError("state_inconsistent")
                return
            self._database.execute(
                "UPDATE courses SET tombstoned_at_utc = ?, updated_at_utc = ? WHERE course_id = "
                "? "
                "AND owner_id = ?",
                (created_at_utc, created_at_utc, str(course_id), owner_id),
            )
            self._database.execute(
                "INSERT INTO tombstones(tombstone_id, owner_id, entity_kind, entity_id, "
                "reason_code, metadata_json, created_at_utc) "
                "VALUES (?, ?, 'course', ?, ?, ?, ?)",
                (
                    tombstone_id,
                    owner_id,
                    str(course_id),
                    reason_code,
                    canonical_json({"reason_code": reason_code}),
                    created_at_utc,
                ),
            )


__all__ = ["CourseRepository", "CourseVersion"]
```

The implementation must not catch or print payloads, SQL, filesystem paths, owner IDs, or raw provider values. The narrow SQLite catch is only for an integrity exception; all domain validation errors remain the stable repository codes.

- [ ] **Step B6A: Create material and batch record types plus validation domains**

Create `backend/src/projectb/infrastructure/repositories/material_repo.py` with exactly:

```python
from __future__ import annotations

import sqlite3
from collections.abc import Mapping
from dataclasses import dataclass

from projectb.domain.materials import MaterialRole, SelectedFile
from projectb.domain.types import CourseId, MaterialId
from projectb.infrastructure.sqlite import (
    Database,
    JsonValue,
    RepositoryError,
    canonical_json,
    parse_json_object,
    require_content_hash,
    require_opaque_id,
    require_utc,
    require_version,
)


@dataclass(frozen=True, slots=True)
class MaterialVersion:
    material_id: MaterialId
    owner_id: str
    course_id: CourseId
    version: int
    role: MaterialRole
    content_hash: str
    payload_json: str
    created_at_utc: str

    @property
    def payload(self) -> dict[str, JsonValue]:
        return parse_json_object(self.payload_json)


```

- [ ] **Step B6A.2: Append `MaterialBatchRecord` through `MaterialBatchFileRecord`**

Append exactly to `backend/src/projectb/infrastructure/repositories/material_repo.py`:

```python
@dataclass(frozen=True, slots=True)
class MaterialBatchRecord:
    batch_id: str
    owner_id: str
    course_id: CourseId
    mode: str
    state: str
    created_at_utc: str
    updated_at_utc: str


@dataclass(frozen=True, slots=True)
class MaterialBatchFileRecord:
    batch_file_id: str
    owner_id: str
    batch_id: str
    material_id: MaterialId | None
    content_hash: str
    role: MaterialRole
    state: str
    error_code: str | None
    created_at_utc: str
    updated_at_utc: str


_BATCH_MODES = {"L", "P", "F"}
_BATCH_FILE_STATES = {
    "inspected",
    "queued",
    "processing",
    "ready",
    "failed",
    "cancelled",
}


```

- [ ] **Step B6A.3: Append `_reason_code`**

Append exactly to `backend/src/projectb/infrastructure/repositories/material_repo.py`:

```python
def _reason_code(value: object) -> str:
    if not isinstance(value, str) or not value or value.strip() != value:
        raise RepositoryError("state_inconsistent")
    if len(value) > 64 or any(
        character not in "abcdefghijklmnopqrstuvwxyz0123456789_-" for character in value
    ):
        raise RepositoryError("state_inconsistent")
    return value


```

- [ ] **Step B6B: Append material repository row adapters**

Append exactly to `backend/src/projectb/infrastructure/repositories/material_repo.py`:

```python
class MaterialRepository:
    def __init__(self, database: Database) -> None:
        self._database = database

    @staticmethod
    def _version(row: sqlite3.Row) -> MaterialVersion:
        try:
            role = MaterialRole(str(row["role"]))
        except ValueError as error:
            raise RepositoryError("state_inconsistent") from error
        return MaterialVersion(
            material_id=MaterialId(str(row["material_id"])),
            owner_id=str(row["owner_id"]),
            course_id=CourseId(str(row["course_id"])),
            version=int(row["version"]),
            role=role,
            content_hash=str(row["content_hash"]),
            payload_json=str(row["payload_json"]),
            created_at_utc=str(row["created_at_utc"]),
        )

    def _material_row(self, material_id: MaterialId) -> sqlite3.Row | None:
        return self._database.fetch_one(
            "SELECT material_id, owner_id, course_id, role, content_hash, active_version, "
            "tombstoned_at_utc "
            "FROM materials WHERE material_id = ?",
            (str(material_id),),
        )

    def _course_row(self, course_id: CourseId) -> sqlite3.Row | None:
        return self._database.fetch_one(
            "SELECT owner_id, tombstoned_at_utc FROM courses WHERE course_id = ?",
            (str(course_id),),
        )

```

- [ ] **Step B6B.2: Append `_batch_row` through `_batch_file`**

Append exactly to `backend/src/projectb/infrastructure/repositories/material_repo.py`:

```python
    def _batch_row(self, batch_id: str) -> sqlite3.Row | None:
        return self._database.fetch_one(
            "SELECT batch_id, owner_id, course_id, mode, state, created_at_utc, updated_at_utc "
            "FROM material_batches WHERE batch_id = ?",
            (batch_id,),
        )

    @staticmethod
    def _batch(row: sqlite3.Row) -> MaterialBatchRecord:
        return MaterialBatchRecord(
            batch_id=str(row["batch_id"]),
            owner_id=str(row["owner_id"]),
            course_id=CourseId(str(row["course_id"])),
            mode=str(row["mode"]),
            state=str(row["state"]),
            created_at_utc=str(row["created_at_utc"]),
            updated_at_utc=str(row["updated_at_utc"]),
        )

    @staticmethod
    def _batch_file(row: sqlite3.Row) -> MaterialBatchFileRecord:
        try:
            role = MaterialRole(str(row["role"]))
        except ValueError as error:
            raise RepositoryError("state_inconsistent") from error
        return MaterialBatchFileRecord(
            batch_file_id=str(row["batch_file_id"]),
            owner_id=str(row["owner_id"]),
            batch_id=str(row["batch_id"]),
            material_id=(
                None if row["material_id"] is None else MaterialId(str(row["material_id"]))
            ),
            content_hash=str(row["content_hash"]),
            role=role,
            state=str(row["state"]),
            error_code=None if row["error_code"] is None else str(row["error_code"]),
            created_at_utc=str(row["created_at_utc"]),
            updated_at_utc=str(row["updated_at_utc"]),
        )

```

- [ ] **Step B6B.3: Append `_check_owner` through `_active_version`**

Append exactly to `backend/src/projectb/infrastructure/repositories/material_repo.py`:

```python
    @staticmethod
    def _check_owner(row: sqlite3.Row, owner_id: str) -> None:
        if str(row["owner_id"]) != owner_id:
            raise RepositoryError("owner_forbidden")

    def _active_version(
        self, material_id: MaterialId, owner_id: str, active_version: int
    ) -> MaterialVersion:
        row = self._database.fetch_one(
            "SELECT material_id, owner_id, course_id, version, role, content_hash, "
            "payload_json, "
            "created_at_utc "
            "FROM material_versions WHERE material_id = ? AND owner_id = ? AND version = ?",
            (str(material_id), owner_id, active_version),
        )
        if row is None:
            raise RepositoryError("state_inconsistent")
        return self._version(row)

```

- [ ] **Step B6C: Append versioned material writes**

Append exactly to `backend/src/projectb/infrastructure/repositories/material_repo.py`:

```python
    def put_versioned(
        self,
        owner_id: str,
        course_id: CourseId,
        selected_file: SelectedFile,
        payload: Mapping[str, object],
        *,
        expected_version: int | None,
        created_at_utc: str,
    ) -> MaterialVersion:
        owner_id = require_opaque_id(owner_id)
        course_id = CourseId(require_opaque_id(course_id))
        if not isinstance(selected_file, SelectedFile):
            raise RepositoryError("state_inconsistent")
        material_id = MaterialId(require_opaque_id(selected_file.material_id))
        content_hash = require_content_hash(selected_file.content_hash)
        if not isinstance(selected_file.role, MaterialRole):
            raise RepositoryError("state_inconsistent")
        if expected_version is not None:
            require_version(expected_version)
        created_at_utc = require_utc(created_at_utc)
        payload_json = canonical_json(payload)
        role = selected_file.role.value
        try:
            with self._database.transaction():
                course = self._course_row(course_id)
                if course is None:
                    raise RepositoryError("not_found")
                self._check_owner(course, owner_id)
                if course["tombstoned_at_utc"] is not None:
                    raise RepositoryError("state_inconsistent")

```

- [ ] **Step B6C.2: Append `material_repo.py` continuation slice 2**

Append exactly to `backend/src/projectb/infrastructure/repositories/material_repo.py`:

```python
                current = self._material_row(material_id)
                if current is not None:
                    self._check_owner(current, owner_id)
                    if (
                        str(current["course_id"]) != str(course_id)
                        or str(current["role"]) != role
                        or str(current["content_hash"]) != content_hash
                    ):
                        raise RepositoryError("state_inconsistent")
                    if current["tombstoned_at_utc"] is not None:
                        raise RepositoryError("state_inconsistent")
                    active_version = int(current["active_version"])
                    active = self._active_version(material_id, owner_id, active_version)
                    if active.payload_json == payload_json:
                        allowed_retry_versions: set[int | None] = {active_version}
                        if active_version == 1:
                            allowed_retry_versions.add(None)
                        else:
                            allowed_retry_versions.add(active_version - 1)
                        if expected_version not in allowed_retry_versions:
                            raise RepositoryError("state_inconsistent")
                        return active
                    if expected_version != active_version:
                        raise RepositoryError("state_inconsistent")
                    next_version = active_version + 1
                    self._database.execute(
                        "INSERT INTO material_versions(material_id, owner_id, course_id, "
                        "version, "
                        "role, content_hash, payload_json, created_at_utc) "
                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                        (
                            str(material_id),
                            owner_id,
                            str(course_id),
                            next_version,
                            role,
                            content_hash,
                            payload_json,
```

- [ ] **Step B6C.3: Append `material_repo.py` continuation slice 3**

Append exactly to `backend/src/projectb/infrastructure/repositories/material_repo.py`:

```python
                            created_at_utc,
                        ),
                    )
                    self._database.execute(
                        "UPDATE materials SET active_version = ?, updated_at_utc = ? "
                        "WHERE material_id = ? AND owner_id = ? AND active_version = ?",
                        (
                            next_version,
                            created_at_utc,
                            str(material_id),
                            owner_id,
                            active_version,
                        ),
                    )
                    return self._active_version(material_id, owner_id, next_version)

                duplicate = self._database.fetch_one(
                    "SELECT material_id, owner_id, active_version FROM materials "
                    "WHERE owner_id = ? AND course_id = ? AND content_hash = ? AND role = ? AND "
                    "tombstoned_at_utc IS NULL",
                    (owner_id, str(course_id), content_hash, role),
                )
                if duplicate is not None:
                    if expected_version is not None:
                        raise RepositoryError("state_inconsistent")
                    return self._active_version(
                        MaterialId(str(duplicate["material_id"])),
                        owner_id,
                        int(duplicate["active_version"]),
                    )
                if expected_version is not None:
                    raise RepositoryError("state_inconsistent")
                self._database.execute(
                    "INSERT INTO materials(material_id, owner_id, course_id, role, "
                    "content_hash, "
                    "active_version, created_at_utc, updated_at_utc) "
                    "VALUES (?, ?, ?, ?, ?, 1, ?, ?)",
                    (
```

- [ ] **Step B6C.4: Append `material_repo.py` continuation slice 4**

Append exactly to `backend/src/projectb/infrastructure/repositories/material_repo.py`:

```python
                        str(material_id),
                        owner_id,
                        str(course_id),
                        role,
                        content_hash,
                        created_at_utc,
                        created_at_utc,
                    ),
                )
                self._database.execute(
                    "INSERT INTO material_versions(material_id, owner_id, course_id, version, "
                    "role, "
                    "content_hash, payload_json, created_at_utc) "
                    "VALUES (?, ?, ?, 1, ?, ?, ?, ?)",
                    (
                        str(material_id),
                        owner_id,
                        str(course_id),
                        role,
                        content_hash,
                        payload_json,
                        created_at_utc,
                    ),
                )
                return self._active_version(material_id, owner_id, 1)
        except RepositoryError:
            raise
        except sqlite3.IntegrityError as error:
            raise RepositoryError("state_inconsistent") from error

```

- [ ] **Step B6D: Append batch creation and owner-scoped batch reads**

Append exactly to `backend/src/projectb/infrastructure/repositories/material_repo.py`:

```python
    def create_batch(
        self,
        owner_id: str,
        course_id: CourseId,
        batch_id: str,
        mode: str,
        *,
        created_at_utc: str,
    ) -> MaterialBatchRecord:
        owner_id = require_opaque_id(owner_id)
        course_id = CourseId(require_opaque_id(course_id))
        batch_id = require_opaque_id(batch_id)
        if not isinstance(mode, str) or mode not in _BATCH_MODES:
            raise RepositoryError("state_inconsistent")
        created_at_utc = require_utc(created_at_utc)
        proposed = MaterialBatchRecord(
            batch_id, owner_id, course_id, mode, "open", created_at_utc, created_at_utc
        )
        try:
            with self._database.transaction():
                course = self._course_row(course_id)
                if course is None:
                    raise RepositoryError("not_found")
                self._check_owner(course, owner_id)
                if course["tombstoned_at_utc"] is not None:
                    raise RepositoryError("state_inconsistent")
                existing = self._batch_row(batch_id)
                if existing is not None:
                    self._check_owner(existing, owner_id)
                    record = self._batch(existing)
                    if record != proposed:
                        raise RepositoryError("state_inconsistent")
                    return record
                self._database.execute(
                    "INSERT INTO material_batches(batch_id, owner_id, course_id, mode, state, "
                    "created_at_utc, updated_at_utc) VALUES (?, ?, ?, ?, 'open', ?, ?)",
                    (
                        batch_id,
```

- [ ] **Step B6D.2: Append `get_batch`**

Append exactly to `backend/src/projectb/infrastructure/repositories/material_repo.py`:

```python
                        owner_id,
                        str(course_id),
                        mode,
                        created_at_utc,
                        created_at_utc,
                    ),
                )
                return proposed
        except RepositoryError:
            raise
        except sqlite3.IntegrityError as error:
            raise RepositoryError("state_inconsistent") from error

    def get_batch(self, owner_id: str, batch_id: str) -> MaterialBatchRecord:
        owner_id = require_opaque_id(owner_id)
        batch_id = require_opaque_id(batch_id)
        row = self._batch_row(batch_id)
        if row is None:
            raise RepositoryError("not_found")
        self._check_owner(row, owner_id)
        return self._batch(row)

```

- [ ] **Step B6E: Append optimistic batch-file membership and state persistence**

Append exactly to `backend/src/projectb/infrastructure/repositories/material_repo.py`:

```python
    def put_batch_file(
        self,
        owner_id: str,
        batch_id: str,
        batch_file_id: str,
        content_hash: str,
        role: MaterialRole,
        state: str,
        *,
        material_id: MaterialId | None,
        error_code: str | None,
        expected_state: str | None,
        updated_at_utc: str,
    ) -> MaterialBatchFileRecord:
        owner_id = require_opaque_id(owner_id)
        batch_id = require_opaque_id(batch_id)
        batch_file_id = require_opaque_id(batch_file_id)
        content_hash = require_content_hash(content_hash)
        if not isinstance(role, MaterialRole):
            raise RepositoryError("state_inconsistent")
        if not isinstance(state, str) or state not in _BATCH_FILE_STATES:
            raise RepositoryError("state_inconsistent")
        if expected_state is not None and (
            not isinstance(expected_state, str) or expected_state not in _BATCH_FILE_STATES
        ):
            raise RepositoryError("state_inconsistent")
        material_id = None if material_id is None else MaterialId(require_opaque_id(material_id))
        error_code = None if error_code is None else _reason_code(error_code)
        if state == "ready" and material_id is None:
            raise RepositoryError("state_inconsistent")
        updated_at_utc = require_utc(updated_at_utc)
        try:
            with self._database.transaction():
                batch_row = self._batch_row(batch_id)
                if batch_row is None:
                    raise RepositoryError("not_found")
                self._check_owner(batch_row, owner_id)
                if material_id is not None:
```

- [ ] **Step B6E.2: Append `material_repo.py` continuation slice 2**

Append exactly to `backend/src/projectb/infrastructure/repositories/material_repo.py`:

```python
                    material = self._material_row(material_id)
                    if material is None:
                        raise RepositoryError("not_found")
                    self._check_owner(material, owner_id)
                    if (
                        str(material["course_id"]) != str(batch_row["course_id"])
                        or material["tombstoned_at_utc"] is not None
                    ):
                        raise RepositoryError("state_inconsistent")
                current = self._database.fetch_one(
                    "SELECT batch_file_id, owner_id, batch_id, material_id, content_hash, role, "
                    "state, error_code, created_at_utc, updated_at_utc "
                    "FROM material_batch_files WHERE batch_file_id = ?",
                    (batch_file_id,),
                )
                if current is None:
                    if expected_state is not None:
                        raise RepositoryError("state_inconsistent")
                    self._database.execute(
                        "INSERT INTO material_batch_files(batch_file_id, owner_id, batch_id, "
                        "material_id, content_hash, role, state, error_code, created_at_utc, "
                        "updated_at_utc) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (
                            batch_file_id,
                            owner_id,
                            batch_id,
                            None if material_id is None else str(material_id),
                            content_hash,
                            role.value,
                            state,
                            error_code,
                            updated_at_utc,
                            updated_at_utc,
                        ),
                    )
                else:
                    self._check_owner(current, owner_id)
                    if (
```

- [ ] **Step B6E.3: Append `material_repo.py` continuation slice 3**

Append exactly to `backend/src/projectb/infrastructure/repositories/material_repo.py`:

```python
                        str(current["batch_id"]) != batch_id
                        or str(current["content_hash"]) != content_hash
                        or str(current["role"]) != role.value
                    ):
                        raise RepositoryError("state_inconsistent")
                    existing = self._batch_file(current)
                    if (
                        existing.state == state
                        and existing.material_id == material_id
                        and existing.error_code == error_code
                    ):
                        return existing
                    if expected_state != existing.state:
                        raise RepositoryError("state_inconsistent")
                    cursor = self._database.execute(
                        "UPDATE material_batch_files SET material_id = ?, state = ?, error_code "
                        "= "
                        "?, "
                        "updated_at_utc = ? WHERE batch_file_id = ? AND owner_id = ? AND state "
                        "= ?",
                        (
                            None if material_id is None else str(material_id),
                            state,
                            error_code,
                            updated_at_utc,
                            batch_file_id,
                            owner_id,
                            existing.state,
                        ),
                    )
                    if cursor.rowcount != 1:
                        raise RepositoryError("state_inconsistent")
                row = self._database.fetch_one(
                    "SELECT batch_file_id, owner_id, batch_id, material_id, content_hash, role, "
                    "state, error_code, created_at_utc, updated_at_utc "
                    "FROM material_batch_files WHERE batch_file_id = ?",
                    (batch_file_id,),
                )
                if row is None:
                    raise RepositoryError("state_inconsistent")
                return self._batch_file(row)
        except RepositoryError:
            raise
        except sqlite3.IntegrityError as error:
            raise RepositoryError("state_inconsistent") from error
```

- [ ] **Step B6E.4: Append `list_batch_files`**

Append exactly to `backend/src/projectb/infrastructure/repositories/material_repo.py`:

```python

    def list_batch_files(self, owner_id: str, batch_id: str) -> tuple[MaterialBatchFileRecord, ...]:
        owner_id = require_opaque_id(owner_id)
        batch_id = require_opaque_id(batch_id)
        batch = self._batch_row(batch_id)
        if batch is None:
            raise RepositoryError("not_found")
        self._check_owner(batch, owner_id)
        rows = self._database.fetch_all(
            "SELECT batch_file_id, owner_id, batch_id, material_id, content_hash, role, state, "
            "error_code, created_at_utc, updated_at_utc FROM material_batch_files "
            "WHERE owner_id = ? AND batch_id = ? ORDER BY batch_file_id",
            (owner_id, batch_id),
        )
        return tuple(self._batch_file(row) for row in rows)

```

- [ ] **Step B6F: Append material active/history/tombstone reads and exports**

Append exactly to `backend/src/projectb/infrastructure/repositories/material_repo.py`:

```python
    def get_active(self, owner_id: str, material_id: MaterialId) -> MaterialVersion:
        owner_id = require_opaque_id(owner_id)
        material_id = MaterialId(require_opaque_id(material_id))
        row = self._material_row(material_id)
        if row is None:
            raise RepositoryError("not_found")
        self._check_owner(row, owner_id)
        if row["tombstoned_at_utc"] is not None:
            raise RepositoryError("not_found")
        return self._active_version(material_id, owner_id, int(row["active_version"]))

    def list_history(self, owner_id: str, material_id: MaterialId) -> tuple[MaterialVersion, ...]:
        owner_id = require_opaque_id(owner_id)
        material_id = MaterialId(require_opaque_id(material_id))
        row = self._material_row(material_id)
        if row is None:
            raise RepositoryError("not_found")
        self._check_owner(row, owner_id)
        rows = self._database.fetch_all(
            "SELECT material_id, owner_id, course_id, version, role, content_hash, "
            "payload_json, "
            "created_at_utc "
            "FROM material_versions WHERE material_id = ? AND owner_id = ? ORDER BY version",
            (str(material_id), owner_id),
        )
        if not rows:
            raise RepositoryError("state_inconsistent")
        return tuple(self._version(item) for item in rows)

```

- [ ] **Step B6F.2: Append `tombstone`**

Append exactly to `backend/src/projectb/infrastructure/repositories/material_repo.py`:

```python
    def tombstone(
        self,
        owner_id: str,
        material_id: MaterialId,
        reason_code: str,
        created_at_utc: str,
    ) -> None:
        owner_id = require_opaque_id(owner_id)
        material_id = MaterialId(require_opaque_id(material_id))
        reason_code = _reason_code(reason_code)
        created_at_utc = require_utc(created_at_utc)
        with self._database.transaction():
            row = self._material_row(material_id)
            if row is None:
                raise RepositoryError("not_found")
            self._check_owner(row, owner_id)
            existing = self._database.fetch_one(
                "SELECT reason_code FROM tombstones WHERE owner_id = ? AND entity_kind = "
                "'material' "
                "AND entity_id = ?",
                (owner_id, str(material_id)),
            )
            if existing is not None:
                if str(existing["reason_code"]) != reason_code:
                    raise RepositoryError("state_inconsistent")
                return
            self._database.execute(
                "UPDATE materials SET tombstoned_at_utc = ?, updated_at_utc = ? WHERE "
                "material_id = "
                "? AND owner_id = ?",
                (created_at_utc, created_at_utc, str(material_id), owner_id),
            )
            self._database.execute(
                "INSERT INTO tombstones(tombstone_id, owner_id, entity_kind, entity_id, "
                "reason_code, metadata_json, created_at_utc) "
                "VALUES (?, ?, 'material', ?, ?, ?, ?)",
                (
                    f"material:{material_id}",
                    owner_id,
                    str(material_id),
                    reason_code,
                    canonical_json({"reason_code": reason_code}),
                    created_at_utc,
                ),
            )
```

- [ ] **Step B6F.3: Append `material_repo.py` continuation slice 3**

Append exactly to `backend/src/projectb/infrastructure/repositories/material_repo.py`:

```python


__all__ = [
    "MaterialBatchFileRecord",
    "MaterialBatchRecord",
    "MaterialRepository",
    "MaterialVersion",
]
```

The implementation must import `SelectedFile` and `MaterialRole` from T-02; it must not duplicate or weaken their validation. It must not write `selected_file.display_name`, a filesystem path, or file bytes into a separate database column. The caller's canonical metadata payload is the only persisted version payload.

- [ ] **Step B7: Run the focused T-03B tests green**

Run:

```powershell
$env:PYTHONPATH = (Resolve-Path 'backend/src').Path
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    '-m', 'pytest', '-c', 'backend/pyproject.toml',
    'backend/tests/integration/test_course_material_repositories.py', '-q'
)
```

Expected: exit code 0. The observed report must cover first-write/version-2 behavior, idempotent retries, duplicate content-hash identity, owner-forbidden reads/writes, stale-version rejection, rollback, restart, tombstone history, and forbidden body/path rejection. If a test fails, add or correct a focused test before changing implementation.

- [ ] **Step B8: Format only the two T-03B Python production files and the focused test**

Run:

```powershell
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    '-m', 'ruff', 'format', '--config', 'backend/pyproject.toml',
    'backend/src/projectb/infrastructure/repositories/course_repo.py',
    'backend/src/projectb/infrastructure/repositories/material_repo.py',
    'backend/tests/integration/test_course_material_repositories.py'
)
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    '-m', 'pytest', '-c', 'backend/pyproject.toml',
    'backend/tests/integration/test_course_material_repositories.py', '-q'
)
```

Expected: Ruff reports formatting success and the focused test remains green. Formatting may not change imports, public names, SQL semantics, or the owned path set.

- [ ] **Step B9: Run T-03B integration and full regression entries**

Run:

```powershell
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    '-m', 'pytest', '-c', 'backend/pyproject.toml',
    'backend/tests/integration/test_course_material_repositories.py',
    'backend/tests/integration/test_sqlite_schema.py', '-q'
)
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    '-m', 'pytest', '-c', 'backend/pyproject.toml', 'backend/tests/integration', '-q'
)
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @('scripts/test_all.py')
```

Expected: all three commands exit 0. The schema test must still pass from the unchanged T-03A migration, and the canonical full entry must be the exact command supplied by the reviewed foundation plan. Record observed output and duration.

- [ ] **Step B10: Run static gates and inspect the exact diff**

Run:

```powershell
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    '-m', 'ruff', 'format', '--check', '--config', 'backend/pyproject.toml',
    'backend/src/projectb/infrastructure/repositories/course_repo.py',
    'backend/src/projectb/infrastructure/repositories/material_repo.py',
    'backend/tests/integration/test_course_material_repositories.py'
)
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    '-m', 'ruff', 'check', '--config', 'backend/pyproject.toml',
    '--extend-select', 'I,E501',
    'backend/src/projectb/infrastructure/repositories/course_repo.py',
    'backend/src/projectb/infrastructure/repositories/material_repo.py',
    'backend/tests/integration/test_course_material_repositories.py'
)
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    '-m', 'mypy', '--config-file', 'backend/pyproject.toml', '--warn-redundant-casts',
    'backend/src/projectb/infrastructure/repositories/course_repo.py',
    'backend/src/projectb/infrastructure/repositories/material_repo.py'
)
Invoke-CheckedNative -FilePath $GitExe -ArgumentList @('diff', '--check')
Invoke-CheckedNative -FilePath $GitExe -ArgumentList @('diff', '--stat')
$forbiddenDiff = @(Invoke-CheckedNative -FilePath $GitExe -ArgumentList @(
    'diff', '--',
    'backend/src/projectb/infrastructure/sqlite.py',
    'backend/src/projectb/infrastructure/migrations/001_initial.sql'
))
if ($forbiddenDiff.Count -ne 0) { throw 'T-03B changed a T-03A-owned path' }
```

Expected: Ruff and mypy exit 0, `git diff --check` exits 0, the stat contains only the three T-03B files, and the final diff command prints no output. Any migration or sqlite-wrapper byte is a blocking ownership violation.

- [ ] **Step B11: Stage exactly the T-03B ownership set**

Run:

```powershell
Invoke-CheckedNative -FilePath $GitExe -ArgumentList @(
    'add', '--',
    'backend/src/projectb/infrastructure/repositories/course_repo.py',
    'backend/src/projectb/infrastructure/repositories/material_repo.py',
    'backend/tests/integration/test_course_material_repositories.py'
)
Assert-ExactStagedPaths -ExpectedPaths @(
    'backend/src/projectb/infrastructure/repositories/course_repo.py'
    'backend/src/projectb/infrastructure/repositories/material_repo.py'
    'backend/tests/integration/test_course_material_repositories.py'
)
Invoke-CheckedNative -FilePath $GitExe -ArgumentList @('diff', '--cached', '--check')
$reviewTree = @(Invoke-CheckedNative -FilePath $GitExe -ArgumentList @('write-tree'))
if ($reviewTree.Count -ne 1 -or $reviewTree[0] -notmatch '^[0-9a-f]{40}$') {
    throw 'T-03B review tree must be one lowercase 40-hex line'
}
$env:PROJECTB_REVIEW_TREE = $reviewTree[0]
$expectedReviewPaths = @(
    'backend/src/projectb/infrastructure/repositories/course_repo.py'
    'backend/src/projectb/infrastructure/repositories/material_repo.py'
    'backend/tests/integration/test_course_material_repositories.py'
)
foreach ($name in @('PROJECTB_ROOT_PLAN_SHA256', 'PROJECTB_DETAILED_PLAN_SHA256')) {
    $value = [Environment]::GetEnvironmentVariable($name)
    if ($value -notmatch '^[0-9A-Fa-f]{64}$') { throw "$name must be one 64-hex hash" }
}
$rootPlanSha = (Get-FileHash -Algorithm SHA256 -LiteralPath 'PLAN.md').Hash.ToLowerInvariant()
$detailedPlanPath = 'docs/superpowers/plans/2026-07-23-persistence-repositories.md'
$detailedPlanSha = (
    Get-FileHash -Algorithm SHA256 -LiteralPath $detailedPlanPath
).Hash.ToLowerInvariant()
if ($rootPlanSha -ne $env:PROJECTB_ROOT_PLAN_SHA256.ToLowerInvariant() -or
    $detailedPlanSha -ne $env:PROJECTB_DETAILED_PLAN_SHA256.ToLowerInvariant()) {
    throw 'review packet plan hash mismatch'
}
```

- [ ] **Step B11.2: Build the exact staged-content review packet**

Continue in the same checked PowerShell session:

```powershell
$blobRows = foreach ($path in ($expectedReviewPaths | Sort-Object)) {
    $stage = @(Invoke-CheckedNative -FilePath $GitExe -ArgumentList @(
        'ls-files', '--stage', '--', $path
    ))
    if ($stage.Count -ne 1) { throw 'review packet requires one stage-zero blob per path' }
    $match = [regex]::Match(
        $stage[0], '^(?<mode>100644|100755) (?<blob>[0-9a-f]{40}) 0\t(?<path>.+)$'
    )
    if (-not $match.Success -or
        ($match.Groups['path'].Value -replace '\\', '/') -ne $path) {
        throw 'review packet staged blob row is malformed'
    }
    "blob=$path|$($match.Groups['mode'].Value)|$($match.Groups['blob'].Value)"
}
$script:ProjectBReviewPacket = @(
    "root-plan-sha256=$rootPlanSha"
    "detailed-plan-sha256=$detailedPlanSha"
    "base-commit=$($env:PROJECTB_BASE_COMMIT)"
    "review-tree=$($env:PROJECTB_REVIEW_TREE)"
) + $blobRows
$packetBytes = [Text.Encoding]::UTF8.GetBytes(
    (($script:ProjectBReviewPacket -join "`n") + "`n")
)
$sha256 = [Security.Cryptography.SHA256]::Create()
try {
    $env:PROJECTB_REVIEW_PACKET_SHA256 = -join (
        $sha256.ComputeHash($packetBytes) | ForEach-Object { $_.ToString('x2') }
    )
} finally {
    $sha256.Dispose()
}
```

Expected: exit code 0 and exactly the three listed paths are staged. No untracked migration, source, plan, log, or generated file may be staged.

- [ ] **Step B12: Run the committed scanner against the staged T-03B patch**

Run:

```powershell
Invoke-CheckedNative -FilePath $PowerShellExe -ArgumentList @(
    '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File',
    'scripts/scan_secrets.ps1', '-PythonExe', $PythonExe, '--staged'
)
```

Expected: exit code 0 with no secret value output. A suspected credential, path/body leak, or provider reference in ordinary payload/logging stops the unit without echoing the value.

- [ ] **Step B13: Request the fresh T-03B SPEC review**

The coordinator gives a fresh non-worker reviewer the confirmed `SPEC.md` sections covering AC-06, AC-15, AC-17, AC-30, the complete T-03/T-03B contract, this plan, predecessor SHA, exact staged diff, every canonical line in `$script:ProjectBReviewPacket`, checked `PROJECTB_REVIEW_PACKET_SHA256` and `PROJECTB_REVIEW_TREE`, and observed red/green/regression/static/scanner output. The PASS record names that exact packet hash and tree. Record `PROJECTB_SPEC_REVIEWER_ID`, `PROJECTB_SPEC_REVIEW_TREE`, and `PROJECTB_SPEC_REVIEW_PACKET_SHA256`.

Expected: `SPEC REVIEW: PASS` with no unresolved Critical or Important finding. The reviewer checks AC-06, AC-15, AC-17, AC-30; version immutability; content-hash/role uniqueness; owner isolation; stale-write behavior; metadata-only batch membership/file state; candidate review-state boundaries; tombstone semantics; and absence of body/path/secret persistence.

- [ ] **Step B14: Request the different fresh T-03B quality review**

Give the same canonical packet lines, packet SHA-256, exact staged diff, and checked tree to a second fresh reviewer and record `PROJECTB_QUALITY_REVIEWER_ID`, `PROJECTB_QUALITY_REVIEW_TREE`, and `PROJECTB_QUALITY_REVIEW_PACKET_SHA256`. The PASS record names that packet hash and tree. The reviewer checks transaction rollback when the active-row update fails, SQLite integrity-error redaction, optimistic concurrency under `BEGIN IMMEDIATE`, stable history order, duplicate identity behavior, index use, restart behavior, exact imports, and standard-library/license impact.

Expected: `QUALITY REVIEW: PASS` with no unresolved Critical or Important finding. Every finding returns to a new failing test and repeats Steps B7-B14; no reviewer edits the worker patch directly.

- [ ] **Step B15: Validate all three T-03B identities**

Run:

```powershell
$identities = @(
    $env:PROJECTB_AGENT_ID
    $env:PROJECTB_SPEC_REVIEWER_ID
    $env:PROJECTB_QUALITY_REVIEWER_ID
)
foreach ($identity in $identities) {
    if ([string]::IsNullOrWhiteSpace($identity) -or
        $identity -notmatch '^[A-Za-z0-9][A-Za-z0-9._-]{1,63}$') {
        throw 'invalid T-03B worker/reviewer identity'
    }
}
if (($identities | Sort-Object -Unique).Count -ne 3) {
    throw 'T-03B worker and reviewers must be pairwise distinct'
}
foreach ($tree in @(
    $env:PROJECTB_REVIEW_TREE
    $env:PROJECTB_SPEC_REVIEW_TREE
    $env:PROJECTB_QUALITY_REVIEW_TREE
)) {
    if ($tree -notmatch '^[0-9a-f]{40}$' -or $tree -ne $env:PROJECTB_REVIEW_TREE) {
        throw 'T-03B reviews must bind to the exact staged tree'
    }
}
foreach ($packetSha in @(
    $env:PROJECTB_REVIEW_PACKET_SHA256
    $env:PROJECTB_SPEC_REVIEW_PACKET_SHA256
    $env:PROJECTB_QUALITY_REVIEW_PACKET_SHA256
)) {
    if ($packetSha -notmatch '^[0-9a-f]{64}$' -or
        $packetSha -ne $env:PROJECTB_REVIEW_PACKET_SHA256) {
        throw 'T-03B reviews must bind to the exact cached-content packet'
    }
}
```

Expected: exit code 0 with three valid, distinct identities.

- [ ] **Step B16: Recheck the exact bytes accepted by both reviewers**

Run:

```powershell
Assert-ExactStagedPaths -ExpectedPaths @(
    'backend/src/projectb/infrastructure/repositories/course_repo.py'
    'backend/src/projectb/infrastructure/repositories/material_repo.py'
    'backend/tests/integration/test_course_material_repositories.py'
)
Invoke-CheckedNative -FilePath $GitExe -ArgumentList @('diff', '--cached', '--check')
Invoke-CheckedNative -FilePath $PowerShellExe -ArgumentList @(
    '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File',
    'scripts/scan_secrets.ps1', '-PythonExe', $PythonExe, '--staged'
)
$currentTree = @(Invoke-CheckedNative -FilePath $GitExe -ArgumentList @('write-tree'))
if ($currentTree.Count -ne 1 -or $currentTree[0] -ne $env:PROJECTB_REVIEW_TREE) {
    throw 'T-03B staged tree changed after review'
}
```

Expected: all commands exit 0 and the staged tree is exactly the tree named by both reviews. Any edit returns to Step B11, recaptures/scans the tree, and repeats both reviews.

- [ ] **Step B17: Commit the reviewed T-03B unit**

Run:

```powershell
Invoke-CheckedNative -FilePath $GitExe -ArgumentList @(
    'commit', '-m',
    "feat(T-03B): add course and material repositories [agent: $env:PROJECTB_AGENT_ID]"
)
```

Expected: exit code 0 with a `feat(T-03B)` subject containing the validated worker identity. The commit must contain only the three T-03B paths.

- [ ] **Step B18: Capture the T-03B commit for the serialized handoff**

Run:

```powershell
$commitHash = @(Invoke-CheckedNative -FilePath $GitExe -ArgumentList @('rev-parse', 'HEAD'))
if ($commitHash.Count -ne 1 -or $commitHash[0] -notmatch '^[0-9a-f]{40}$') {
    throw 'T-03B commit hash must be one lowercase 40-hex line'
}
$committedTree = @(
    Invoke-CheckedNative -FilePath $GitExe -ArgumentList @('rev-parse', 'HEAD^{tree}')
)
if ($committedTree.Count -ne 1 -or $committedTree[0] -ne $env:PROJECTB_REVIEW_TREE) {
    throw 'T-03B committed tree differs from the reviewed tree'
}
$commitHash[0]
```

Expected: exit code 0 with one observed 40-character lowercase hexadecimal commit hash. The coordinator records the hash, review identities, observed test evidence, and scanner result before creating the T-03C worktree.

**T-03B completion standard:** The exact three-path unit has observed red and green evidence, focused/schema/integration/full regression, Ruff/mypy/scanner/staged-set evidence, two fresh PASS reviews, and one recorded worker commit. Course/material versions remain readable after restart, duplicate imports are deterministic, and no migration byte changed.

## Task T-03C: Learning, Remote Lifecycle, Audit, and Tombstone Repositories

**Goal:** Complete T-03 persistence by appending exact LearningEvidence and plan histories, persisting consent and remote object/job state with optimistic versions, writing whitelist-only audit metadata, and tombstoning deleted remote objects without retaining a usable provider reference in current state or version history.

**Dependencies / parallelism:** Requires the reviewed T-03B commit. Runs alone and is the terminal T-03 dispatch. A missing or incompatible T-03A column/table is a blocking schema defect returned to the coordinator; this worker never edits `sqlite.py` or `001_initial.sql`. T-04A, T-05A, T-06, M1, M2, M3, and X2 consumers wait for both T-03C reviews and the recorded commit.

**Files:**
- Create: `backend/src/projectb/infrastructure/repositories/learning_repo.py`
- Create: `backend/src/projectb/infrastructure/repositories/remote_repo.py`
- Create: `backend/tests/integration/test_learning_remote_repositories.py`

### Locked T-03C public contracts

`LearningRepository` publishes:

```python
def append_attempt(
    self,
    owner_id: str,
    course_id: CourseId,
    attempt_id: str,
    concept_id: str,
    attempt_key: str,
    response_ref: str,
    *,
    explanation_session_id: str | None,
    review_task_id: str | None,
    started_at_utc: str,
    submitted_at_utc: str,
) -> AttemptRecord: ...
def get_attempt(self, owner_id: str, attempt_id: str) -> AttemptRecord: ...
def list_attempts(
    self, owner_id: str, course_id: CourseId
) -> tuple[AttemptRecord, ...]: ...
def append_evidence(
    self, owner_id: str, payload: Mapping[str, object]
) -> LearningEvidenceRecord: ...
def list_evidence(
    self, owner_id: str, course_id: CourseId
) -> tuple[LearningEvidenceRecord, ...]: ...
def append_plan_revision(
    self,
    owner_id: str,
    course_id: CourseId,
    revision_id: str,
    revision_number: int,
    parent_revision_id: str | None,
    reverts_revision_id: str | None,
    plan_input_hash: str,
    policy_version: str,
    payload: Mapping[str, object],
    *,
    expected_latest_number: int | None,
    created_at_utc: str,
) -> PlanRevisionRecord: ...
def get_latest_plan(self, owner_id: str, course_id: CourseId) -> PlanRevisionRecord: ...
def list_plan_revisions(
    self, owner_id: str, course_id: CourseId
) -> tuple[PlanRevisionRecord, ...]: ...
```

`RemoteRepository` publishes `append_consent`, `get_consent`, `revoke_consent`, `put_object_versioned`, `get_active_object`, `list_usable_objects`, `list_object_history`, `put_job_versioned`, `get_active_job`, `list_job_history`, `tombstone_object`, and `get_tombstone` with the literal signatures in the complete implementation below. `AuditRepository` publishes `record` and `list_for_owner`. The overview ellipses above are signature-only; every executable slice below is concrete and names all imports and helpers it uses.

### Locked T-03C invariants

- LearningEvidence accepts exactly the SPEC LearningEvidence v1 key set. Required and optional opaque IDs are validated; enums are exact; rubric items and locator IDs are sorted and unique; `attempt_key` is course-unique; evidence is immutable and stores no answer text. A duplicate evidence ID or attempt key returns the existing row only when canonical payloads are identical.
- A protected Attempt row contains only opaque IDs, one safe `response_ref`, and canonical UTC timestamps. It contains no response/answer/body column. Evidence must name an existing same-owner/same-course Attempt with the same attempt key; T-03 never dereferences or evaluates the protected response.
- Plan revisions form one append-only, gap-free course sequence. Revision 1 has no parent; every later revision names the current latest revision as parent, carries the latest expected number, and may name an older same-course revision in `reverts_revision_id`. Reversion appends a new revision; no row is rewritten.
- Remote consent mode is exactly `F`. Consent scope has exactly `adapter_id`, `provider_profile_id`, `config_fingerprint`, `capability_snapshot_id`, `policy_snapshot_id`, and a non-empty sorted `materials` array. Each material scope has exactly `material_id`, `content_hash`, and `role`, and must match a live material in the same owner/course. The scope values must match the consent columns. Revocation appends a consent tombstone rather than updating the append-only consent row.
- `provider_ref` in SQLite is only an opaque reference to protected local storage; it is never a raw provider object/file ID, credential, or secret. The public parameter is named `protected_ref`. Scope tokens/config fingerprints are lowercase SHA-256 values. Neither value enters version payloads, audit metadata, exceptions, tombstones, or ordinary logs.
- Remote object states are exactly `awaiting_consent`, `uploading`, `indexing`, `ready`, `failed`, `delete_requested`, `deleted`, `delete_incomplete`, and `source_disabled`; remote job states are exactly `queued`, `running`, `cancelling`, `cancelled`, `succeeded`, `failed`, and `recovery_required`. `awaiting_consent` has `consent_id=None`, no scope token, and no protected reference. The one transition to uploading binds an active exact F consent; later consent identity is immutable. Revocation clears every matching current scope token immediately and permanently: every later transition, including `delete_requested`, `delete_incomplete`, `source_disabled`, retries, and reopen/restart paths, must persist `scope_token=None`. A revoked consent can never authorize a new upload/index/ready transition or regain a token in any state. Cleanup may retain only the pre-existing protected reference needed for deletion.
- `deleted` can be reached only through `tombstone_object` from `delete_requested` after validation of a persisted, same-owner/same-course/same-object `remote_delete` reconciliation job whose current state is `succeeded`, result is exactly `provider_deleted` or `provider_expired`, and `object_version` equals the current `delete_requested` version. A caller-supplied reason, an absent/running/failed job, a mismatched object/version, or arbitrary success payload is insufficient. The tombstone appends a final `deleted` history version containing only reason code plus the opaque reconciliation job ID, clears `provider_ref` and `scope_token` in the mutable current row, and appends generic non-reconstructive metadata. `get_active_object` then returns `not_found`, while `list_object_history` remains owner-scoped and readable.
- Audit event kind, outcome, subject-ID alphabet/length, metadata keys, and every metadata value use literal bounded domains in `remote_repo.py`. Counts/durations have numeric caps; booleans are exact; modes/states/job kinds/sources/error codes/reason codes are enumerated. Arbitrary maps, unhashable values, paths, bodies, answers, provider refs, scope tokens, secret-shaped strings, and credentials are rejected before a row is inserted.

- [ ] **Step C1: Validate the T-03C runtime, identity, predecessor, and exact worktree**

Run exactly from the T-03C worktree and keep this checked PowerShell session for all later C steps:

```powershell
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Test-AbsoluteExistingLeaf {
    param([Parameter(Mandatory)][string]$Value)
    if ([string]::IsNullOrWhiteSpace($Value) -or
        $Value -notmatch '^(?:[A-Za-z]:[\\/]|\\\\[^\\/]+[\\/][^\\/]+[\\/])') {
        return $false
    }
    try { $null = [IO.Path]::GetFullPath($Value) } catch { return $false }
    return Test-Path -LiteralPath $Value -PathType Leaf
}

if (-not ('ProjectBProcessTree' -as [type])) {
    Add-Type -TypeDefinition @'
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Runtime.InteropServices;
public static class ProjectBProcessTree {
    [StructLayout(LayoutKind.Sequential)] struct BasicInfo {
        public IntPtr Reserved1, Peb, Reserved20, Reserved21, ProcessId, ParentProcessId;
    }
    [DllImport("ntdll.dll")] static extern int NtQueryInformationProcess(
        IntPtr handle, int kind, ref BasicInfo info, int length, out int returned);
    public static int[] Descendants(int root) {
        var map = new Dictionary<int, List<int>>();
        foreach (var process in Process.GetProcesses()) {
            try {
                var info = new BasicInfo(); int returned;
                if (NtQueryInformationProcess(process.Handle, 0, ref info,
                    Marshal.SizeOf(typeof(BasicInfo)), out returned) != 0) continue;
                int parent = info.ParentProcessId.ToInt32();
                if (!map.ContainsKey(parent)) map[parent] = new List<int>();
                map[parent].Add(process.Id);
            } catch { } finally { process.Dispose(); }
        }
        var result = new List<int>(); var queue = new Queue<int>(); queue.Enqueue(root);
        while (queue.Count > 0) {
            int parent = queue.Dequeue(); List<int> children;
            if (!map.TryGetValue(parent, out children)) continue;
            foreach (int child in children) { result.Add(child); queue.Enqueue(child); }
        }
        return result.ToArray();
    }
}
'@
}

```

- [ ] **Step C1.1: Define bounded non-privileged process-tree cleanup**

Continue in the same checked PowerShell session:

```powershell
function Stop-NativeProcessTree {
    param([Parameter(Mandatory)][Diagnostics.Process]$Process)
    $rootId = $Process.Id
    $descendants = @([ProjectBProcessTree]::Descendants($rootId))
    Stop-Process -Id $rootId -Force -ErrorAction SilentlyContinue
    $descendants += @([ProjectBProcessTree]::Descendants($rootId))
    $targets = @($descendants | Sort-Object -Unique)
    if ($targets -contains $PID) { throw 'native timeout tree included the host process' }
    [array]::Reverse($targets)
    foreach ($target in $targets) {
        Stop-Process -Id $target -Force -ErrorAction SilentlyContinue
    }
    $deadline = [Diagnostics.Stopwatch]::StartNew()
    do {
        $alive = @(@($rootId) + $targets | Where-Object {
            Get-Process -Id $_ -ErrorAction SilentlyContinue
        })
        if ($alive.Count -gt 0) { Start-Sleep -Milliseconds 25 }
    } while ($alive.Count -gt 0 -and $deadline.ElapsedMilliseconds -lt 5000)
    if ($alive.Count -gt 0) { throw 'native command timeout cleanup failed' }
}

function ConvertTo-NativeArgument {
    param([Parameter(Mandatory)][AllowEmptyString()][string]$Value)
    if ($Value.Length -gt 0 -and $Value -notmatch '[\s"]') { return $Value }
    $builder = [Text.StringBuilder]::new()
    [void]$builder.Append('"')
    $slashes = 0
    foreach ($character in $Value.ToCharArray()) {
        if ($character -eq '\') { $slashes++; continue }
        if ($character -eq '"') {
            [void]$builder.Append(('\' * (($slashes * 2) + 1)))
            [void]$builder.Append('"')
            $slashes = 0
            continue
        }
        if ($slashes -gt 0) { [void]$builder.Append(('\' * $slashes)); $slashes = 0 }
        [void]$builder.Append($character)
    }
    if ($slashes -gt 0) { [void]$builder.Append(('\' * ($slashes * 2))) }
    [void]$builder.Append('"')
    return $builder.ToString()
}

```

- [ ] **Step C1.2: Define `Invoke-NativeProcess`**

Continue in the same checked PowerShell session:

```powershell
function Invoke-NativeProcess {
    param(
        [Parameter(Mandatory)][string]$FilePath,
        [Parameter(Mandatory)][AllowEmptyCollection()][AllowEmptyString()][string[]]$ArgumentList,
        [ValidateRange(1, 3600)][int]$TimeoutSeconds = 600
    )
    if (-not (Test-AbsoluteExistingLeaf -Value $FilePath)) {
        throw 'native executable must be an absolute existing leaf'
    }
    $start = [Diagnostics.ProcessStartInfo]::new()
    $start.FileName = $FilePath
    $start.Arguments = (($ArgumentList | ForEach-Object {
        ConvertTo-NativeArgument -Value $_
    }) -join ' ')
    $start.UseShellExecute = $false
    $start.CreateNoWindow = $true
    $start.RedirectStandardOutput = $true
    $start.RedirectStandardError = $true
    $process = [Diagnostics.Process]::new()
    $process.StartInfo = $start
    try {
        try {
            if (-not $process.Start()) { throw 'start returned false' }
        } catch {
            throw 'native command launch failed'
        }
        $stdoutTask = $process.StandardOutput.ReadToEndAsync()
        $stderrTask = $process.StandardError.ReadToEndAsync()
        if (-not $process.WaitForExit($TimeoutSeconds * 1000)) {
            Stop-NativeProcessTree -Process $process
            $process.WaitForExit()
            throw "native command timed out after $TimeoutSeconds seconds"
        }
        $process.WaitForExit()
        $stdout = $stdoutTask.Result.TrimEnd([char[]]"`r`n")
        $null = $stderrTask.Result
        $lines = if ($stdout.Length -eq 0) { @() } else { @($stdout -split "`r?`n") }
        return [pscustomobject]@{ ExitCode = $process.ExitCode; Stdout = $lines }
    } finally {
        $process.Dispose()
    }
}
```

- [ ] **Step C1.3: Define `Invoke-CheckedNative` through `Invoke-ExpectedNativeExit`**

Continue in the same checked PowerShell session:

```powershell

function Invoke-CheckedNative {
    param(
        [Parameter(Mandatory)][string]$FilePath,
        [Parameter(Mandatory)][AllowEmptyCollection()][AllowEmptyString()][string[]]$ArgumentList,
        [ValidateRange(1, 3600)][int]$TimeoutSeconds = 600
    )
    $result = Invoke-NativeProcess -FilePath $FilePath -ArgumentList $ArgumentList `
        -TimeoutSeconds $TimeoutSeconds
    if ($result.ExitCode -ne 0) {
        throw "native command failed with exit code $($result.ExitCode)"
    }
    return @($result.Stdout)
}

function Invoke-ExpectedNativeExit {
    param(
        [Parameter(Mandatory)][string]$FilePath,
        [Parameter(Mandatory)][AllowEmptyCollection()][AllowEmptyString()][string[]]$ArgumentList,
        [Parameter(Mandatory)][int]$ExpectedExitCode,
        [ValidateRange(1, 3600)][int]$TimeoutSeconds = 600
    )
    $result = Invoke-NativeProcess -FilePath $FilePath -ArgumentList $ArgumentList `
        -TimeoutSeconds $TimeoutSeconds
    if ($result.ExitCode -ne $ExpectedExitCode) {
        throw "native command returned unexpected exit code $($result.ExitCode)"
    }
    return @($result.Stdout)
}

$GitExe = (Get-Command git -CommandType Application -ErrorAction Stop).Source
if (-not (Test-AbsoluteExistingLeaf -Value $GitExe)) {
    throw 'git executable must be an absolute existing leaf'
}
$PythonExe = $env:PROJECTB_PYTHON_EXE
$PowerShellExe = $env:PROJECTB_POWERSHELL_EXE
foreach ($pair in @(@('Python', $PythonExe), @('PowerShell', $PowerShellExe))) {
    if (-not (Test-AbsoluteExistingLeaf -Value $pair[1])) {
        throw "$($pair[0]) executable must be an absolute existing leaf"
    }
}
```

- [ ] **Step C1.4: Define `Assert-NativeWrapperContract`**

Continue in the same checked PowerShell session:

```powershell
function Assert-NativeWrapperContract {
    param([Parameter(Mandatory)][string]$PythonPath)
    $empty = @(Invoke-CheckedNative -FilePath $PythonPath -ArgumentList @('-c', ''))
    if ($empty.Count -ne 0) { throw 'empty native output was not preserved' }
    $multiline = @(Invoke-CheckedNative -FilePath $PythonPath -ArgumentList @(
        '-c', "print('first'); print('second')"
    ))
    if ($multiline.Count -ne 2 -or $multiline[0] -ne 'first' -or
        $multiline[1] -ne 'second') {
        throw 'multiline native output was malformed'
    }
    $marker = 'sensitive-child-output-must-not-surface'
    $failure = $null
    try {
        Invoke-CheckedNative -FilePath $PythonPath -ArgumentList @(
            '-c', "import sys; print('$marker'); sys.exit(7)"
        ) -TimeoutSeconds 10
    } catch { $failure = $_.Exception.Message }
    if ($failure -ne 'native command failed with exit code 7' -or
        $failure.Contains($marker)) {
        throw 'nonzero diagnostics were not sanitized'
    }
    $wrongExecutable = (Resolve-Path -LiteralPath 'PLAN.md').Path
    $failure = $null
    try {
        Invoke-CheckedNative -FilePath $wrongExecutable -ArgumentList @() -TimeoutSeconds 10
    } catch { $failure = $_.Exception.Message }
    if ($failure -ne 'native command launch failed') {
        throw 'wrong executable did not fail closed'
    }
    $probeRoot = Join-Path ([IO.Path]::GetTempPath()) (
        'projectb-native-probe-' + [guid]::NewGuid().ToString('N')
    )
    [IO.Directory]::CreateDirectory($probeRoot) | Out-Null
    $pidFile = Join-Path $probeRoot 'child.pid'
    $probe = "import pathlib,subprocess,sys,time; " +
        "child=subprocess.Popen([sys.executable,'-c','import time; time.sleep(30)']); " +
        "pathlib.Path(sys.argv[1]).write_text(str(child.pid),encoding='ascii'); time.sleep(30)"
    $failure = $null
    try {
        Invoke-CheckedNative -FilePath $PythonPath -ArgumentList @('-c', $probe, $pidFile) `
            -TimeoutSeconds 1
    } catch { $failure = $_.Exception.Message }
    if ($failure -ne 'native command timed out after 1 seconds' -or
        -not (Test-Path -LiteralPath $pidFile -PathType Leaf)) {
        throw 'native timeout probe failed'
    }
    $childPid = [int]([IO.File]::ReadAllText($pidFile).Trim())
    Start-Sleep -Milliseconds 250
    if (Get-Process -Id $childPid -ErrorAction SilentlyContinue) {
        throw 'native timeout left a descendant process running'
    }
    [IO.File]::Delete($pidFile)
    [IO.Directory]::Delete($probeRoot)
}
```

- [ ] **Step C1.5: Run the bounded native-wrapper contract probe**

Continue in the same checked PowerShell session:

```powershell
Assert-NativeWrapperContract -PythonPath $PythonExe
$pythonVersion = @(Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    '-c', 'import platform; print(platform.python_version())'
))
if ($pythonVersion.Count -ne 1 -or $pythonVersion[0].Trim() -ne '3.14.6') {
    throw 'T-03C requires CPython 3.14.6'
}
$ruffVersion = @(Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    '-m', 'ruff', '--version'
))
$mypyVersion = @(Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    '-m', 'mypy', '--version'
))
$pytestVersion = @(Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    '-m', 'pytest', '--version'
))
if ($ruffVersion.Count -ne 1 -or $ruffVersion[0].Trim() -ne 'ruff 0.15.22') {
    throw 'T-03C requires Ruff 0.15.22'
}
if ($mypyVersion.Count -ne 1 -or $mypyVersion[0].Trim() -notmatch '^mypy 2\.3\.0(?: |$)') {
    throw 'T-03C requires mypy 2.3.0'
}
if ($pytestVersion.Count -ne 1 -or $pytestVersion[0].Trim() -ne 'pytest 9.1.1') {
    throw 'T-03C requires pytest 9.1.1'
}
$powerShellOutput = @(Invoke-CheckedNative -FilePath $PowerShellExe -ArgumentList @(
    '-NoProfile', '-Command', '$PSVersionTable.PSVersion.ToString()'
))
if ($powerShellOutput.Count -ne 1) { throw 'PowerShell version output must be one line' }
$parsedPowerShellVersion = $null
if (-not [Version]::TryParse($powerShellOutput[0].Trim(), [ref]$parsedPowerShellVersion)) {
    throw 'PowerShell version is not parseable'
}
foreach ($name in @('PROJECTB_AGENT_ID', 'PROJECTB_UNIT_ID', 'PROJECTB_BASE_COMMIT', 'PROJECTB_WORKTREE_ROOT')) {
    if ([string]::IsNullOrWhiteSpace([Environment]::GetEnvironmentVariable($name))) {
        throw "$name is required"
    }
}
if ($env:PROJECTB_AGENT_ID -notmatch '^[A-Za-z0-9][A-Za-z0-9._-]{1,63}$') {
    throw 'PROJECTB_AGENT_ID is invalid'
}
if ($env:PROJECTB_UNIT_ID -ne 'T-03C') { throw 'wrong dispatch unit' }
```

- [ ] **Step C1.6: Define `Assert-ExactStagedPaths`**

Continue in the same checked PowerShell session:

```powershell
if ($env:PROJECTB_BASE_COMMIT -notmatch '^[0-9a-f]{40}$') { throw 'invalid predecessor SHA' }
$head = @(Invoke-CheckedNative -FilePath $GitExe -ArgumentList @('rev-parse', 'HEAD'))
if ($head.Count -ne 1 -or $head[0] -notmatch '^[0-9a-f]{40}$' -or
    $head[0].Trim() -ne $env:PROJECTB_BASE_COMMIT) {
    throw 'T-03C worktree is not at the reviewed T-03B commit'
}
$resolvedRoot = (Resolve-Path -LiteralPath '.').Path
if ($resolvedRoot -ne (Resolve-Path -LiteralPath $env:PROJECTB_WORKTREE_ROOT).Path) {
    throw 'wrong worktree root'
}
$status = @(Invoke-CheckedNative -FilePath $GitExe -ArgumentList @('status', '--porcelain'))
if ($status.Count -ne 0) { throw 'T-03C worktree must start clean' }
$allowed = @(
    'backend/src/projectb/infrastructure/repositories/learning_repo.py'
    'backend/src/projectb/infrastructure/repositories/remote_repo.py'
    'backend/tests/integration/test_learning_remote_repositories.py'
)
$tracked = @(
    Invoke-CheckedNative -FilePath $GitExe -ArgumentList (@('ls-files', '--') + $allowed)
)
if ($tracked.Count -ne 0) { throw 'T-03C owned paths already exist in the predecessor' }
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
$env:PYTHONPATH = (Resolve-Path -LiteralPath 'backend/src').Path
```

Expected: exit code 0, checked runtime probes produce one valid line each, the worktree is clean at the reviewed T-03B SHA, all owned paths are new, and the staging helper enumerates the whole index without a pathspec.

- [ ] **Step C2: Create the failing learning/remote repository test foundation**

Create `backend/tests/integration/test_learning_remote_repositories.py` with exactly:

```python
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest
from projectb.domain.materials import MaterialReviewState, MaterialRole, SelectedFile
from projectb.domain.types import CourseId, MaterialId
from projectb.infrastructure.repositories.course_repo import CourseRepository
from projectb.infrastructure.repositories.learning_repo import LearningRepository
from projectb.infrastructure.repositories.material_repo import MaterialRepository
from projectb.infrastructure.repositories.remote_repo import (
    AuditRepository,
    RemoteRepository,
)
from projectb.infrastructure.sqlite import Database, RepositoryError

OWNER_A = "owner-a"
OWNER_B = "owner-b"
COURSE_ID = CourseId("course-a")
CREATED = "2026-07-23T00:00:00Z"
UPDATED = "2026-07-23T00:01:00Z"
LATER = "2026-07-23T00:02:00Z"
CONFIG_HASH = "b" * 64
SCOPE_TOKEN = hashlib.sha256(
    b"course-a|material-a|" + (b"a" * 64) + b"|consent-a|" + (b"b" * 64)
).hexdigest()


```

- [ ] **Step C2.2: Append `database` through `assert_code`**

Append exactly to `backend/tests/integration/test_learning_remote_repositories.py`:

```python
@pytest.fixture
def database(tmp_path):
    database = Database.open(tmp_path / "learning-remote.sqlite3")
    database.migrate()
    CourseRepository(database).put_versioned(
        OWNER_A,
        COURSE_ID,
        {"title": "Concurrency"},
        expected_version=None,
        created_at_utc=CREATED,
    )
    MaterialRepository(database).put_versioned(
        OWNER_A,
        COURSE_ID,
        SelectedFile(
            material_id=MaterialId("material-a"),
            display_name="synthetic.pdf",
            role=MaterialRole.LECTURE,
            content_hash="a" * 64,
            size_bytes=128,
            review_state=MaterialReviewState.ACCEPTED,
        ),
        {"display_name": "synthetic.pdf", "review_state": "accepted"},
        expected_version=None,
        created_at_utc=CREATED,
    )
    try:
        yield database
    finally:
        database.close()


def assert_code(code: str, operation) -> None:
    with pytest.raises(RepositoryError) as caught:
        operation()
    assert caught.value.code == code


```

- [ ] **Step C2.3: Append `evidence`**

Append exactly to `backend/tests/integration/test_learning_remote_repositories.py`:

```python
def evidence(
    evidence_id: str = "evidence-a", attempt_key: str = "attempt-key-a"
) -> dict[str, object]:
    return {
        "evidence_id": evidence_id,
        "course_id": str(COURSE_ID),
        "concept_id": "concept-race",
        "attempt_id": "attempt-a",
        "explanation_session_id": None,
        "review_task_id": None,
        "attempt_key": attempt_key,
        "origin": "student_attempt",
        "evaluator_type": "mutex_race_oracle",
        "evaluator_version": "mutex-race.v1",
        "check_kind": "isomorphic",
        "outcome": "partial",
        "rubric_results": [
            {"criterion_id": "event_completeness", "status": "pass"},
            {
                "criterion_id": "thread_order",
                "status": "fail",
                "error_code": "bad_order",
            },
        ],
        "source_locator_ids": ["locator-a", "locator-b"],
        "trace_seed": 7,
        "variant_id": "variant-a",
        "occurred_at_utc": LATER,
        "evidence_version": "learning-evidence.v1",
    }


```

- [ ] **Step C2.4: Append `append_attempt` through `consent_scope`**

Append exactly to `backend/tests/integration/test_learning_remote_repositories.py`:

```python
def append_attempt(repository: LearningRepository):
    return repository.append_attempt(
        OWNER_A,
        COURSE_ID,
        "attempt-a",
        "concept-race",
        "attempt-key-a",
        "protected-response-a",
        explanation_session_id=None,
        review_task_id=None,
        started_at_utc=CREATED,
        submitted_at_utc=UPDATED,
    )


def consent_scope() -> dict[str, object]:
    return {
        "adapter_id": "openai",
        "provider_profile_id": "profile-a",
        "config_fingerprint": CONFIG_HASH,
        "capability_snapshot_id": "capability-a",
        "policy_snapshot_id": "policy-a",
        "materials": [
            {
                "material_id": "material-a",
                "content_hash": "a" * 64,
                "role": "lecture",
            }
        ],
    }
```

- [ ] **Step C3A: Append LearningEvidence exactness and idempotency tests**

Append exactly to `backend/tests/integration/test_learning_remote_repositories.py`:

```python


def test_learning_evidence_is_exact_append_only_and_attempt_idempotent(
    database: Database,
) -> None:
    repository = LearningRepository(database)
    append_attempt(repository)
    first = repository.append_evidence(OWNER_A, evidence())
    assert first.evidence_id == "evidence-a"
    assert repository.append_evidence(OWNER_A, evidence()) == first
    assert [item.evidence_id for item in repository.list_evidence(OWNER_A, COURSE_ID)] == [
        "evidence-a"
    ]
    assert_code(
        "state_inconsistent",
        lambda: repository.append_evidence(OWNER_A, evidence("evidence-b", "attempt-key-a")),
    )
    assert_code("owner_forbidden", lambda: repository.list_evidence(OWNER_B, COURSE_ID))


def test_learning_evidence_rejects_unsorted_or_answer_bearing_payloads(
    database: Database,
) -> None:
    repository = LearningRepository(database)
    append_attempt(repository)
    unsorted = evidence()
    unsorted["source_locator_ids"] = ["locator-b", "locator-a"]
    assert_code("state_inconsistent", lambda: repository.append_evidence(OWNER_A, unsorted))
    answer_bearing = evidence()
    answer_bearing["answer_text"] = "synthetic answer"
    assert_code(
        "state_inconsistent",
        lambda: repository.append_evidence(OWNER_A, answer_bearing),
    )
    assert repository.list_evidence(OWNER_A, COURSE_ID) == ()


```

- [ ] **Step C3B: Append protected Attempt reference and redaction tests**

Append exactly to `backend/tests/integration/test_learning_remote_repositories.py`:

```python
def test_protected_attempts_store_only_an_opaque_response_reference(
    database: Database,
) -> None:
    repository = LearningRepository(database)
    first = append_attempt(repository)
    assert first.response_ref == "protected-response-a"
    assert append_attempt(repository) == first
    assert repository.get_attempt(OWNER_A, "attempt-a") == first
    assert repository.list_attempts(OWNER_A, COURSE_ID) == (first,)
    assert_code("owner_forbidden", lambda: repository.get_attempt(OWNER_B, "attempt-a"))
    assert_code(
        "state_inconsistent",
        lambda: repository.append_attempt(
            OWNER_A,
            COURSE_ID,
            "attempt-b",
            "concept-race",
            "attempt-key-b",
            "C:/private/answer.txt",
            explanation_session_id=None,
            review_task_id=None,
            started_at_utc=CREATED,
            submitted_at_utc=UPDATED,
        ),
    )
    columns = {
        str(row["name"]).casefold() for row in database.fetch_all('PRAGMA table_info("attempts")')
    }
    assert "response_ref" in columns
    assert columns.isdisjoint({"answer", "answer_text", "body", "response_body"})


```

- [ ] **Step C3C: Append gap-free plan revision and revert tests**

Append exactly to `backend/tests/integration/test_learning_remote_repositories.py`:

```python
def test_plan_revisions_are_gap_free_idempotent_and_revert_by_append(
    database: Database,
) -> None:
    repository = LearningRepository(database)
    first = repository.append_plan_revision(
        OWNER_A,
        COURSE_ID,
        "revision-a",
        1,
        None,
        None,
        "d" * 64,
        "review-policy.v1",
        {"reason_codes": ["new_coverage"], "task_ids": ["task-a"]},
        expected_latest_number=None,
        created_at_utc=CREATED,
    )
    assert (
        repository.append_plan_revision(
            OWNER_A,
            COURSE_ID,
            "revision-a",
            1,
            None,
            None,
            "d" * 64,
            "review-policy.v1",
            {"reason_codes": ["new_coverage"], "task_ids": ["task-a"]},
            expected_latest_number=None,
            created_at_utc=CREATED,
        )
        == first
    )
```

- [ ] **Step C3C.2: Append `test_learning_remote_repositories.py` continuation slice 2**

Append exactly to `backend/tests/integration/test_learning_remote_repositories.py`:

```python
    second = repository.append_plan_revision(
        OWNER_A,
        COURSE_ID,
        "revision-b",
        2,
        "revision-a",
        "revision-a",
        "e" * 64,
        "review-policy.v1",
        {"reason_codes": ["user_revert"], "task_ids": ["task-b"]},
        expected_latest_number=1,
        created_at_utc=UPDATED,
    )
    assert second.reverts_revision_id == "revision-a"
    assert repository.get_latest_plan(OWNER_A, COURSE_ID) == second
    assert [
        item.revision_number for item in repository.list_plan_revisions(OWNER_A, COURSE_ID)
    ] == [1, 2]
    assert_code(
        "state_inconsistent",
        lambda: repository.append_plan_revision(
            OWNER_A,
            COURSE_ID,
            "revision-c",
            4,
            "revision-b",
            None,
            "f" * 64,
            "review-policy.v1",
            {"task_ids": []},
            expected_latest_number=2,
            created_at_utc=LATER,
        ),
    )
```

- [ ] **Step C4A: Append remote test helpers**

Append exactly to `backend/tests/integration/test_learning_remote_repositories.py`:

```python


def append_consent(repository: RemoteRepository):
    return repository.append_consent(
        OWNER_A,
        COURSE_ID,
        "consent-a",
        "F",
        consent_scope(),
        "profile-a",
        CONFIG_HASH,
        "capability-a",
        "policy-a",
        CREATED,
    )


def put_object(
    repository: RemoteRepository,
    *,
    state: str,
    expected_version: int | None,
    created_at_utc: str,
    scope_token: str | None,
    protected_ref: str | None,
):
    return repository.put_object_versioned(
        OWNER_A,
        COURSE_ID,
        "remote-object-a",
        MaterialId("material-a"),
        None if state == "awaiting_consent" else "consent-a",
        "file",
        state,
        CONFIG_HASH,
        scope_token,
        protected_ref,
        {"operation": state},
        expected_version=expected_version,
        created_at_utc=created_at_utc,
    )


```

- [ ] **Step C4A.2: Append `complete_delete_reconciliation`**

Append exactly to `backend/tests/integration/test_learning_remote_repositories.py`:

```python
def complete_delete_reconciliation(
    repository: RemoteRepository,
    *,
    object_version: int,
    result: str = "provider_deleted",
    job_id: str = "remote-delete-a",
):
    repository.put_job_versioned(
        OWNER_A,
        COURSE_ID,
        job_id,
        "remote-object-a",
        f"remote-delete:{job_id}",
        "queued",
        0,
        1,
        None,
        {"job_kind": "remote_delete", "object_version": object_version},
        expected_version=None,
        created_at_utc="2026-07-23T00:05:00Z",
    )
    repository.put_job_versioned(
        OWNER_A,
        COURSE_ID,
        job_id,
        "remote-object-a",
        f"remote-delete:{job_id}",
        "running",
        0,
        1,
        None,
        {"job_kind": "remote_delete", "object_version": object_version},
        expected_version=1,
        created_at_utc="2026-07-23T00:06:00Z",
    )
```

- [ ] **Step C4A.3: Append `test_learning_remote_repositories.py` continuation slice 3**

Append exactly to `backend/tests/integration/test_learning_remote_repositories.py`:

```python
    return repository.put_job_versioned(
        OWNER_A,
        COURSE_ID,
        job_id,
        "remote-object-a",
        f"remote-delete:{job_id}",
        "succeeded",
        1,
        1,
        None,
        {
            "job_kind": "remote_delete",
            "object_version": object_version,
            "observed_at_utc": "2026-07-23T00:07:00Z",
            "reconciliation_result": result,
        },
        expected_version=2,
        created_at_utc="2026-07-23T00:07:00Z",
    )


```

- [ ] **Step C4B: Append exact-F consent, revocation, and scope mismatch tests**

Append exactly to `backend/tests/integration/test_learning_remote_repositories.py`:

```python
def test_consent_revocation_is_append_only_and_blocks_new_remote_state(
    database: Database,
) -> None:
    repository = RemoteRepository(database)
    awaiting = put_object(
        repository,
        state="awaiting_consent",
        expected_version=None,
        created_at_utc=CREATED,
        scope_token=None,
        protected_ref=None,
    )
    assert awaiting.consent_id is None
    consent = append_consent(repository)
    assert consent.revoked_at_utc is None
    assert append_consent(repository) == consent
    revoked = repository.revoke_consent(OWNER_A, "consent-a", UPDATED)
    assert revoked.revoked_at_utc == UPDATED
    assert_code(
        "state_inconsistent",
        lambda: put_object(
            repository,
            state="uploading",
            expected_version=1,
            created_at_utc=LATER,
            scope_token=SCOPE_TOKEN,
            protected_ref="protected-ref-a",
        ),
    )


```

- [ ] **Step C4B.2: Append `test_consent_is_f_only_and_scope_must_match_material_identity`**

Append exactly to `backend/tests/integration/test_learning_remote_repositories.py`:

```python
def test_consent_is_f_only_and_scope_must_match_material_identity(
    database: Database,
) -> None:
    repository = RemoteRepository(database)
    assert_code(
        "state_inconsistent",
        lambda: repository.append_consent(
            OWNER_A,
            COURSE_ID,
            "consent-local",
            "L",
            consent_scope(),
            "profile-a",
            CONFIG_HASH,
            "capability-a",
            "policy-a",
            CREATED,
        ),
    )
    missing_role = consent_scope()
    missing_role["materials"] = [{"material_id": "material-a", "content_hash": "a" * 64}]
    assert_code(
        "state_inconsistent",
        lambda: repository.append_consent(
            OWNER_A,
            COURSE_ID,
            "consent-missing-role",
            "F",
            missing_role,
            "profile-a",
            CONFIG_HASH,
            "capability-a",
            "policy-a",
            CREATED,
        ),
    )
    wrong_hash = consent_scope()
    wrong_hash["materials"] = [
        {"material_id": "material-a", "content_hash": "f" * 64, "role": "lecture"}
```

- [ ] **Step C4B.3: Append `test_learning_remote_repositories.py` continuation slice 3**

Append exactly to `backend/tests/integration/test_learning_remote_repositories.py`:

```python
    ]
    assert_code(
        "state_inconsistent",
        lambda: repository.append_consent(
            OWNER_A,
            COURSE_ID,
            "consent-wrong-hash",
            "F",
            wrong_hash,
            "profile-a",
            CONFIG_HASH,
            "capability-a",
            "policy-a",
            CREATED,
        ),
    )


```

- [ ] **Step C4C: Append remote-object lifecycle and tombstone tests**

Append exactly to `backend/tests/integration/test_learning_remote_repositories.py`:

```python
def test_remote_object_history_tombstone_and_current_reference_cleanup(
    database: Database,
) -> None:
    repository = RemoteRepository(database)
    append_consent(repository)
    first = put_object(
        repository,
        state="awaiting_consent",
        expected_version=None,
        created_at_utc=CREATED,
        scope_token=None,
        protected_ref=None,
    )
    assert first.version == 1
    uploading = put_object(
        repository,
        state="uploading",
        expected_version=1,
        created_at_utc=UPDATED,
        scope_token=SCOPE_TOKEN,
        protected_ref="protected-ref-a",
    )
    indexing = put_object(
        repository,
        state="indexing",
        expected_version=2,
        created_at_utc=LATER,
        scope_token=SCOPE_TOKEN,
        protected_ref="protected-ref-a",
    )
    ready = put_object(
        repository,
        state="ready",
        expected_version=3,
        created_at_utc="2026-07-23T00:03:00Z",
        scope_token=SCOPE_TOKEN,
        protected_ref="protected-ref-a",
    )
```

- [ ] **Step C4C.2: Append `test_learning_remote_repositories.py` continuation slice 2**

Append exactly to `backend/tests/integration/test_learning_remote_repositories.py`:

```python
    assert uploading.version == 2 and indexing.version == 3 and ready.version == 4
    assert (
        put_object(
            repository,
            state="ready",
            expected_version=3,
            created_at_utc="2026-07-23T00:03:00Z",
            scope_token=SCOPE_TOKEN,
            protected_ref="protected-ref-a",
        )
        == ready
    )
    put_object(
        repository,
        state="delete_requested",
        expected_version=4,
        created_at_utc="2026-07-23T00:04:00Z",
        scope_token=None,
        protected_ref="protected-ref-a",
    )
    complete_delete_reconciliation(repository, object_version=5)
    tombstone = repository.tombstone_object(
        OWNER_A,
        "remote-object-a",
        "remote-delete-a",
        "provider_deleted",
        "2026-07-23T00:08:00Z",
    )
    assert tombstone.reason_code == "provider_deleted"
    assert_code("not_found", lambda: repository.get_active_object(OWNER_A, "remote-object-a"))
    history = repository.list_object_history(OWNER_A, "remote-object-a")
    assert [item.state for item in history] == [
        "awaiting_consent",
        "uploading",
        "indexing",
        "ready",
        "delete_requested",
        "deleted",
```

- [ ] **Step C4C.3: Append `test_tombstone_rejects_reason_only_or_unreconciled_provider_deletion`**

Append exactly to `backend/tests/integration/test_learning_remote_repositories.py`:

```python
    ]
    assert all("protected-ref-a" not in item.payload_json for item in history)
    current = database.fetch_one(
        "SELECT provider_ref, scope_token, state FROM remote_objects WHERE object_id = ?",
        ("remote-object-a",),
    )
    assert current is not None
    assert current["provider_ref"] is None and current["scope_token"] is None
    assert current["state"] == "deleted"
    metadata = json.loads(tombstone.metadata_json)
    assert metadata == {"reconciliation_job_id": "remote-delete-a", "status": "deleted"}
    assert_code(
        "owner_forbidden",
        lambda: repository.list_object_history(OWNER_B, "remote-object-a"),
    )


def test_tombstone_rejects_reason_only_or_unreconciled_provider_deletion(
    database: Database,
) -> None:
    repository = RemoteRepository(database)
    put_object(
        repository,
        state="awaiting_consent",
        expected_version=None,
        created_at_utc=CREATED,
        scope_token=None,
        protected_ref=None,
    )
    append_consent(repository)
    put_object(
        repository,
        state="uploading",
        expected_version=1,
        created_at_utc=UPDATED,
        scope_token=SCOPE_TOKEN,
        protected_ref="protected-ref-a",
    )
```

- [ ] **Step C4C.4: Append `test_learning_remote_repositories.py` continuation slice 4**

Append exactly to `backend/tests/integration/test_learning_remote_repositories.py`:

```python
    put_object(
        repository,
        state="indexing",
        expected_version=2,
        created_at_utc=LATER,
        scope_token=SCOPE_TOKEN,
        protected_ref="protected-ref-a",
    )
    put_object(
        repository,
        state="ready",
        expected_version=3,
        created_at_utc="2026-07-23T00:03:00Z",
        scope_token=SCOPE_TOKEN,
        protected_ref="protected-ref-a",
    )
    put_object(
        repository,
        state="delete_requested",
        expected_version=4,
        created_at_utc="2026-07-23T00:04:00Z",
        scope_token=None,
        protected_ref="protected-ref-a",
    )
    assert_code(
        "state_inconsistent",
        lambda: repository.tombstone_object(
            OWNER_A,
            "remote-object-a",
            "missing-reconciliation-job",
            "provider_deleted",
            "2026-07-23T00:08:00Z",
        ),
    )
```

- [ ] **Step C4C.5: Append `test_learning_remote_repositories.py` continuation slice 5**

Append exactly to `backend/tests/integration/test_learning_remote_repositories.py`:

```python
    repository.put_job_versioned(
        OWNER_A,
        COURSE_ID,
        "remote-delete-running",
        "remote-object-a",
        "remote-delete:running",
        "queued",
        0,
        1,
        None,
        {"job_kind": "remote_delete", "object_version": 5},
        expected_version=None,
        created_at_utc="2026-07-23T00:05:00Z",
    )
    repository.put_job_versioned(
        OWNER_A,
        COURSE_ID,
        "remote-delete-running",
        "remote-object-a",
        "remote-delete:running",
        "running",
        0,
        1,
        None,
        {"job_kind": "remote_delete", "object_version": 5},
        expected_version=1,
        created_at_utc="2026-07-23T00:06:00Z",
    )
    assert_code(
        "state_inconsistent",
        lambda: repository.tombstone_object(
            OWNER_A,
            "remote-object-a",
            "remote-delete-running",
            "provider_deleted",
            "2026-07-23T00:08:00Z",
        ),
    )
```

- [ ] **Step C4C.6: Append `test_learning_remote_repositories.py` continuation slice 6**

Append exactly to `backend/tests/integration/test_learning_remote_repositories.py`:

```python
    complete_delete_reconciliation(
        repository,
        object_version=4,
        job_id="remote-delete-wrong-version",
    )
    assert_code(
        "state_inconsistent",
        lambda: repository.tombstone_object(
            OWNER_A,
            "remote-object-a",
            "remote-delete-wrong-version",
            "provider_deleted",
            "2026-07-23T00:08:00Z",
        ),
    )


```

- [ ] **Step C4D: Append revocation token-invalidation and cleanup tests**

Append exactly to `backend/tests/integration/test_learning_remote_repositories.py`:

```python
def test_revocation_permanently_blocks_scope_token_reissue_across_cleanup_restart(
    database: Database,
) -> None:
    repository = RemoteRepository(database)
    put_object(
        repository,
        state="awaiting_consent",
        expected_version=None,
        created_at_utc=CREATED,
        scope_token=None,
        protected_ref=None,
    )
    append_consent(repository)
    put_object(
        repository,
        state="uploading",
        expected_version=1,
        created_at_utc=UPDATED,
        scope_token=SCOPE_TOKEN,
        protected_ref="protected-ref-a",
    )
    put_object(
        repository,
        state="indexing",
        expected_version=2,
        created_at_utc=LATER,
        scope_token=SCOPE_TOKEN,
        protected_ref="protected-ref-a",
    )
    put_object(
        repository,
        state="ready",
        expected_version=3,
        created_at_utc="2026-07-23T00:03:00Z",
        scope_token=SCOPE_TOKEN,
        protected_ref="protected-ref-a",
    )
    repository.revoke_consent(OWNER_A, "consent-a", "2026-07-23T00:04:00Z")
```

- [ ] **Step C4D.2: Append `test_learning_remote_repositories.py` continuation slice 2**

Append exactly to `backend/tests/integration/test_learning_remote_repositories.py`:

```python
    current = repository.get_active_object(OWNER_A, "remote-object-a")
    assert current.scope_token is None
    assert current.protected_ref == "protected-ref-a"
    assert repository.list_usable_objects(OWNER_A, COURSE_ID) == ()
    deleting = put_object(
        repository,
        state="delete_requested",
        expected_version=4,
        created_at_utc="2026-07-23T00:05:00Z",
        scope_token=None,
        protected_ref="protected-ref-a",
    )
    assert deleting.state == "delete_requested"
    assert_code(
        "state_inconsistent",
        lambda: put_object(
            repository,
            state="delete_incomplete",
            expected_version=5,
            created_at_utc="2026-07-23T00:06:00Z",
            scope_token=SCOPE_TOKEN,
            protected_ref="protected-ref-a",
        ),
    )
    incomplete = put_object(
        repository,
        state="delete_incomplete",
        expected_version=5,
        created_at_utc="2026-07-23T00:06:00Z",
        scope_token=None,
        protected_ref="protected-ref-a",
    )
    assert incomplete.version == 6 and incomplete.scope_token is None
```

- [ ] **Step C4D.3: Append `test_learning_remote_repositories.py` continuation slice 3**

Append exactly to `backend/tests/integration/test_learning_remote_repositories.py`:

```python
    for state in ("delete_incomplete", "delete_requested", "source_disabled"):
        assert_code(
            "state_inconsistent",
            lambda state=state: put_object(
                repository,
                state=state,
                expected_version=6,
                created_at_utc="2026-07-23T00:07:00Z",
                scope_token=SCOPE_TOKEN,
                protected_ref="protected-ref-a",
            ),
        )
    database_row = database.fetch_one("PRAGMA database_list")
    assert database_row is not None
    path = Path(str(database_row["file"]))
    database.close()
    reopened = Database.open(path)
    try:
        reopened.migrate()
        restarted = RemoteRepository(reopened)
        current = restarted.get_active_object(OWNER_A, "remote-object-a")
        assert current.state == "delete_incomplete" and current.scope_token is None
        assert_code(
            "state_inconsistent",
            lambda: put_object(
                restarted,
                state="delete_requested",
                expected_version=6,
                created_at_utc="2026-07-23T00:08:00Z",
                scope_token=SCOPE_TOKEN,
                protected_ref="protected-ref-a",
            ),
        )
        persisted = reopened.fetch_one(
            "SELECT state, scope_token FROM remote_objects WHERE object_id = ?",
            ("remote-object-a",),
        )
        assert persisted is not None
        assert persisted["state"] == "delete_incomplete"
        assert persisted["scope_token"] is None
    finally:
        reopened.close()


```

- [ ] **Step C4E: Append remote-job version and monotonic-progress tests**

Append exactly to `backend/tests/integration/test_learning_remote_repositories.py`:

```python
def test_remote_jobs_are_versioned_progress_monotonic_and_idempotent(
    database: Database,
) -> None:
    repository = RemoteRepository(database)
    first = repository.put_job_versioned(
        OWNER_A,
        COURSE_ID,
        "remote-job-a",
        None,
        "remote-upload:course-a",
        "queued",
        0,
        2,
        None,
        {"job_kind": "upload"},
        expected_version=None,
        created_at_utc=CREATED,
    )
    duplicate = repository.put_job_versioned(
        OWNER_A,
        COURSE_ID,
        "remote-job-duplicate",
        None,
        "remote-upload:course-a",
        "queued",
        0,
        2,
        None,
        {"job_kind": "upload"},
        expected_version=None,
        created_at_utc=CREATED,
    )
    assert duplicate.job_id == first.job_id
```

- [ ] **Step C4E.2: Append `test_learning_remote_repositories.py` continuation slice 2**

Append exactly to `backend/tests/integration/test_learning_remote_repositories.py`:

```python
    running = repository.put_job_versioned(
        OWNER_A,
        COURSE_ID,
        "remote-job-a",
        None,
        "remote-upload:course-a",
        "running",
        1,
        2,
        None,
        {"job_kind": "upload"},
        expected_version=1,
        created_at_utc=UPDATED,
    )
    assert running.version == 2
    assert_code(
        "state_inconsistent",
        lambda: repository.put_job_versioned(
            OWNER_A,
            COURSE_ID,
            "remote-job-a",
            None,
            "remote-upload:course-a",
            "running",
            0,
            2,
            None,
            {"job_kind": "upload"},
            expected_version=2,
            created_at_utc=LATER,
        ),
    )
    assert [item.version for item in repository.list_job_history(OWNER_A, "remote-job-a")] == [1, 2]


```

- [ ] **Step C4F: Append bounded audit-domain and redaction tests**

Append exactly to `backend/tests/integration/test_learning_remote_repositories.py`:

```python
def test_audit_repository_is_whitelist_only_and_idempotent(database: Database) -> None:
    repository = AuditRepository(database)
    first = repository.record(
        OWNER_A,
        "audit-a",
        "remote_delete",
        "remote-object-a",
        "accepted",
        {"duration_ms": 12, "state": "delete_requested"},
        CREATED,
    )
    assert (
        repository.record(
            OWNER_A,
            "audit-a",
            "remote_delete",
            "remote-object-a",
            "accepted",
            {"duration_ms": 12, "state": "delete_requested"},
            CREATED,
        )
        == first
    )
    assert_code(
        "state_inconsistent",
        lambda: repository.record(
            OWNER_A,
            "audit-b",
            "remote_delete",
            "remote-object-a",
            "rejected",
            {"body": "synthetic private value"},
            UPDATED,
        ),
    )
```

- [ ] **Step C4F.2: Append `test_learning_remote_repositories.py` continuation slice 2**

Append exactly to `backend/tests/integration/test_learning_remote_repositories.py`:

```python
    for index, unsafe_metadata in enumerate(
        (
            {"state": "C:/private/input.pdf"},
            {"error_code": "secret-value"},
            {"duration_ms": 3_600_001},
            {"count": -1},
            {"retryable": "yes"},
            {"source": ["provider"]},
        )
    ):
        assert_code(
            "state_inconsistent",
            lambda index=index, unsafe_metadata=unsafe_metadata: repository.record(
                OWNER_A,
                f"audit-unsafe-{index}",
                "remote_delete",
                "remote-object-a",
                "rejected",
                unsafe_metadata,
                UPDATED,
            ),
        )
    assert_code(
        "state_inconsistent",
        lambda: repository.record(
            OWNER_A,
            "audit-unsafe-subject",
            "remote_delete",
            "C:/private/input.pdf",
            "rejected",
            {"state": "failed"},
            UPDATED,
        ),
    )
    assert [item.event_id for item in repository.list_for_owner(OWNER_A)] == ["audit-a"]
```

- [ ] **Step C5: Append failing restart and migration-ownership tests**

Append exactly to `backend/tests/integration/test_learning_remote_repositories.py`:

```python


def test_learning_and_remote_rows_reopen_without_history_rewrite(tmp_path) -> None:
    path = tmp_path / "restart.sqlite3"
    first_database = Database.open(path)
    first_database.migrate()
    CourseRepository(first_database).put_versioned(
        OWNER_A,
        COURSE_ID,
        {"title": "Restart"},
        expected_version=None,
        created_at_utc=CREATED,
    )
    MaterialRepository(first_database).put_versioned(
        OWNER_A,
        COURSE_ID,
        SelectedFile(
            material_id=MaterialId("material-a"),
            display_name="synthetic.pdf",
            role=MaterialRole.LECTURE,
            content_hash="a" * 64,
            size_bytes=128,
            review_state=MaterialReviewState.ACCEPTED,
        ),
        {"display_name": "synthetic.pdf", "review_state": "accepted"},
        expected_version=None,
        created_at_utc=CREATED,
    )
    learning = LearningRepository(first_database)
    append_attempt(learning)
    learning.append_evidence(OWNER_A, evidence())
    append_consent(RemoteRepository(first_database))
    first_database.close()

```

- [ ] **Step C5.2: Append `test_learning_remote_repositories.py` continuation slice 2**

Append exactly to `backend/tests/integration/test_learning_remote_repositories.py`:

```python
    second_database = Database.open(path)
    second_database.migrate()
    try:
        assert len(LearningRepository(second_database).list_evidence(OWNER_A, COURSE_ID)) == 1
        assert (
            RemoteRepository(second_database).get_consent(OWNER_A, "consent-a").consent_id
            == "consent-a"
        )
        assert (
            second_database.fetch_one("SELECT COUNT(*) AS count FROM schema_migrations")["count"]
            == 1
        )
    finally:
        second_database.close()
```

Expected red behavior after Steps C2-C5: collection exits 2 because `learning_repo` and `remote_repo` do not exist. All values are synthetic identifiers/hashes; the test contains no private courseware, live provider reference, external account data, or credential.

- [ ] **Step C6: Run the T-03C focused tests and capture the expected red result**

Run:

```powershell
Invoke-ExpectedNativeExit -FilePath $PythonExe -ArgumentList @(
    '-m', 'pytest', '-c', 'backend/pyproject.toml',
    'backend/tests/integration/test_learning_remote_repositories.py', '-q'
) -ExpectedExitCode 2
```

Expected: checked exit code 2 during collection for the named absent repository modules. Any environment, predecessor, migration, fixture, or runtime failure is the wrong red cause and blocks implementation.

- [ ] **Step C7A: Create learning record types and validation helpers**

Create `backend/src/projectb/infrastructure/repositories/learning_repo.py` with exactly:

```python
from __future__ import annotations

import sqlite3
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from projectb.domain.types import CourseId
from projectb.infrastructure.sqlite import (
    Database,
    JsonValue,
    RepositoryError,
    canonical_json,
    parse_json_object,
    require_content_hash,
    require_opaque_id,
    require_utc,
    require_version,
)

_EVIDENCE_KEYS = {
    "evidence_id",
    "course_id",
    "concept_id",
    "attempt_id",
    "explanation_session_id",
    "review_task_id",
    "attempt_key",
    "origin",
    "evaluator_type",
    "evaluator_version",
    "check_kind",
    "outcome",
    "rubric_results",
    "source_locator_ids",
    "trace_seed",
    "variant_id",
    "occurred_at_utc",
```

- [ ] **Step C7A.2: Append `AttemptRecord` through `LearningEvidenceRecord`**

Append exactly to `backend/src/projectb/infrastructure/repositories/learning_repo.py`:

```python
    "evidence_version",
}
_ORIGINS = {"student_attempt", "system_source_repair"}
_CHECK_KINDS = {"starting_probe", "isomorphic", "transfer", "delayed_variant"}
_OUTCOMES = {
    "incorrect",
    "partial",
    "demonstrated_now",
    "refused",
    "source_insufficient",
    "skipped",
}
_RUBRIC_STATUSES = {"pass", "fail", "not_applicable"}


@dataclass(frozen=True, slots=True)
class AttemptRecord:
    attempt_id: str
    owner_id: str
    course_id: CourseId
    concept_id: str
    attempt_key: str
    explanation_session_id: str | None
    review_task_id: str | None
    response_ref: str
    started_at_utc: str
    submitted_at_utc: str


@dataclass(frozen=True, slots=True)
class LearningEvidenceRecord:
    evidence_id: str
    owner_id: str
    course_id: CourseId
    concept_id: str
    attempt_id: str
    attempt_key: str
    occurred_at_utc: str
    evidence_version: str
    payload_json: str

```

- [ ] **Step C7A.3: Append `payload` through `_code`**

Append exactly to `backend/src/projectb/infrastructure/repositories/learning_repo.py`:

```python
    @property
    def payload(self) -> dict[str, JsonValue]:
        return parse_json_object(self.payload_json)


@dataclass(frozen=True, slots=True)
class PlanRevisionRecord:
    revision_id: str
    owner_id: str
    course_id: CourseId
    revision_number: int
    parent_revision_id: str | None
    reverts_revision_id: str | None
    plan_input_hash: str
    policy_version: str
    payload_json: str
    created_at_utc: str

    @property
    def payload(self) -> dict[str, JsonValue]:
        return parse_json_object(self.payload_json)


def _text(value: object) -> str:
    if not isinstance(value, str) or not value or value.strip() != value:
        raise RepositoryError("state_inconsistent")
    return value


def _code(value: object) -> str:
    value = _text(value)
    if len(value) > 64 or any(
        character not in "abcdefghijklmnopqrstuvwxyz0123456789_.:-" for character in value
    ):
        raise RepositoryError("state_inconsistent")
    return value


```

- [ ] **Step C7A.4: Append `_optional_id` through `_validate_evidence_payload`**

Append exactly to `backend/src/projectb/infrastructure/repositories/learning_repo.py`:

```python
def _optional_id(value: object) -> str | None:
    if value is None:
        return None
    return require_opaque_id(value)


def _mapping(value: object) -> Mapping[object, object]:
    if not isinstance(value, Mapping):
        raise RepositoryError("state_inconsistent")
    return value


def _sequence(value: object) -> Sequence[object]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        raise RepositoryError("state_inconsistent")
    return value


def _validate_evidence_payload(
    payload: Mapping[str, object],
) -> tuple[str, CourseId, str, str, str, str, str, str]:
    if set(payload) != _EVIDENCE_KEYS:
        raise RepositoryError("state_inconsistent")
    evidence_id = require_opaque_id(payload["evidence_id"])
    course_id = CourseId(require_opaque_id(payload["course_id"]))
    concept_id = require_opaque_id(payload["concept_id"])
    attempt_id = require_opaque_id(payload["attempt_id"])
    _optional_id(payload["explanation_session_id"])
    _optional_id(payload["review_task_id"])
    attempt_key = require_opaque_id(payload["attempt_key"])
    origin = _text(payload["origin"])
    if origin not in _ORIGINS:
        raise RepositoryError("state_inconsistent")
    _code(payload["evaluator_type"])
    _code(payload["evaluator_version"])
    check_kind = _text(payload["check_kind"])
    if check_kind not in _CHECK_KINDS:
        raise RepositoryError("state_inconsistent")
    outcome = _text(payload["outcome"])
    if outcome not in _OUTCOMES:
        raise RepositoryError("state_inconsistent")

```

- [ ] **Step C7A.5: Append `learning_repo.py` continuation slice 5**

Append exactly to `backend/src/projectb/infrastructure/repositories/learning_repo.py`:

```python
    criterion_ids: list[str] = []
    for raw_item in _sequence(payload["rubric_results"]):
        item = _mapping(raw_item)
        if set(item) not in (
            {"criterion_id", "status"},
            {"criterion_id", "status", "error_code"},
        ):
            raise RepositoryError("state_inconsistent")
        criterion_id = _code(item.get("criterion_id"))
        status = _text(item.get("status"))
        if status not in _RUBRIC_STATUSES:
            raise RepositoryError("state_inconsistent")
        if "error_code" in item:
            _code(item.get("error_code"))
        criterion_ids.append(criterion_id)
    if criterion_ids != sorted(criterion_ids) or len(set(criterion_ids)) != len(criterion_ids):
        raise RepositoryError("state_inconsistent")

    locator_ids = [require_opaque_id(item) for item in _sequence(payload["source_locator_ids"])]
    if locator_ids != sorted(locator_ids) or len(set(locator_ids)) != len(locator_ids):
        raise RepositoryError("state_inconsistent")
    trace_seed = payload["trace_seed"]
    if trace_seed is not None and not (
        (type(trace_seed) is int and trace_seed >= 0)
        or (isinstance(trace_seed, str) and bool(trace_seed) and trace_seed.strip() == trace_seed)
    ):
        raise RepositoryError("state_inconsistent")
    _optional_id(payload["variant_id"])
    occurred_at_utc = require_utc(payload["occurred_at_utc"])
    if _text(payload["evidence_version"]) != "learning-evidence.v1":
        raise RepositoryError("state_inconsistent")
    payload_json = canonical_json(payload)
    return (
        evidence_id,
        course_id,
        concept_id,
        attempt_id,
        attempt_key,
        occurred_at_utc,
        "learning-evidence.v1",
        payload_json,
    )


```

- [ ] **Step C7B: Append the learning repository row adapters**

Append exactly to `backend/src/projectb/infrastructure/repositories/learning_repo.py`:

```python
class LearningRepository:
    def __init__(self, database: Database) -> None:
        self._database = database

    def _course(self, owner_id: str, course_id: CourseId) -> sqlite3.Row:
        row = self._database.fetch_one(
            "SELECT owner_id, tombstoned_at_utc FROM courses WHERE course_id = ?",
            (str(course_id),),
        )
        if row is None:
            raise RepositoryError("not_found")
        if str(row["owner_id"]) != owner_id:
            raise RepositoryError("owner_forbidden")
        if row["tombstoned_at_utc"] is not None:
            raise RepositoryError("state_inconsistent")
        return row

    @staticmethod
    def _attempt(row: sqlite3.Row) -> AttemptRecord:
        return AttemptRecord(
            attempt_id=str(row["attempt_id"]),
            owner_id=str(row["owner_id"]),
            course_id=CourseId(str(row["course_id"])),
            concept_id=str(row["concept_id"]),
            attempt_key=str(row["attempt_key"]),
            explanation_session_id=(
                None
                if row["explanation_session_id"] is None
                else str(row["explanation_session_id"])
            ),
            review_task_id=(None if row["review_task_id"] is None else str(row["review_task_id"])),
            response_ref=str(row["response_ref"]),
            started_at_utc=str(row["started_at_utc"]),
            submitted_at_utc=str(row["submitted_at_utc"]),
        )

```

- [ ] **Step C7B.2: Append `_evidence` through `_revision`**

Append exactly to `backend/src/projectb/infrastructure/repositories/learning_repo.py`:

```python
    @staticmethod
    def _evidence(row: sqlite3.Row) -> LearningEvidenceRecord:
        return LearningEvidenceRecord(
            evidence_id=str(row["evidence_id"]),
            owner_id=str(row["owner_id"]),
            course_id=CourseId(str(row["course_id"])),
            concept_id=str(row["concept_id"]),
            attempt_id=str(row["attempt_id"]),
            attempt_key=str(row["attempt_key"]),
            occurred_at_utc=str(row["occurred_at_utc"]),
            evidence_version=str(row["evidence_version"]),
            payload_json=str(row["payload_json"]),
        )

    @staticmethod
    def _revision(row: sqlite3.Row) -> PlanRevisionRecord:
        return PlanRevisionRecord(
            revision_id=str(row["revision_id"]),
            owner_id=str(row["owner_id"]),
            course_id=CourseId(str(row["course_id"])),
            revision_number=int(row["revision_number"]),
            parent_revision_id=(
                None if row["parent_revision_id"] is None else str(row["parent_revision_id"])
            ),
            reverts_revision_id=(
                None if row["reverts_revision_id"] is None else str(row["reverts_revision_id"])
            ),
            plan_input_hash=str(row["plan_input_hash"]),
            policy_version=str(row["policy_version"]),
            payload_json=str(row["payload_json"]),
            created_at_utc=str(row["created_at_utc"]),
        )

```

- [ ] **Step C7C: Append protected Attempt persistence and reads**

Append exactly to `backend/src/projectb/infrastructure/repositories/learning_repo.py`:

```python
    def append_attempt(
        self,
        owner_id: str,
        course_id: CourseId,
        attempt_id: str,
        concept_id: str,
        attempt_key: str,
        response_ref: str,
        *,
        explanation_session_id: str | None,
        review_task_id: str | None,
        started_at_utc: str,
        submitted_at_utc: str,
    ) -> AttemptRecord:
        owner_id = require_opaque_id(owner_id)
        course_id = CourseId(require_opaque_id(course_id))
        attempt_id = require_opaque_id(attempt_id)
        concept_id = require_opaque_id(concept_id)
        attempt_key = require_opaque_id(attempt_key)
        response_ref = _code(response_ref)
        explanation_session_id = _optional_id(explanation_session_id)
        review_task_id = _optional_id(review_task_id)
        started_at_utc = require_utc(started_at_utc)
        submitted_at_utc = require_utc(submitted_at_utc)
        if submitted_at_utc < started_at_utc:
            raise RepositoryError("state_inconsistent")
        proposed = AttemptRecord(
            attempt_id,
            owner_id,
            course_id,
            concept_id,
            attempt_key,
            explanation_session_id,
            review_task_id,
            response_ref,
            started_at_utc,
            submitted_at_utc,
        )
```

- [ ] **Step C7C.2: Append `learning_repo.py` continuation slice 2**

Append exactly to `backend/src/projectb/infrastructure/repositories/learning_repo.py`:

```python
        try:
            with self._database.transaction():
                self._course(owner_id, course_id)
                existing = self._database.fetch_one(
                    "SELECT attempt_id, owner_id, course_id, concept_id, attempt_key, "
                    "explanation_session_id, review_task_id, response_ref, started_at_utc, "
                    "submitted_at_utc FROM attempts WHERE attempt_id = ?",
                    (attempt_id,),
                )
                if existing is not None:
                    if str(existing["owner_id"]) != owner_id:
                        raise RepositoryError("owner_forbidden")
                    record = self._attempt(existing)
                    if record != proposed:
                        raise RepositoryError("state_inconsistent")
                    return record
                duplicate = self._database.fetch_one(
                    "SELECT attempt_id, owner_id, course_id, concept_id, attempt_key, "
                    "explanation_session_id, review_task_id, response_ref, started_at_utc, "
                    "submitted_at_utc FROM attempts WHERE owner_id = ? AND course_id = ? "
                    "AND attempt_key = ?",
                    (owner_id, str(course_id), attempt_key),
                )
                if duplicate is not None:
                    record = self._attempt(duplicate)
                    if record != proposed:
                        raise RepositoryError("state_inconsistent")
                    return record
                self._database.execute(
                    "INSERT INTO attempts(attempt_id, owner_id, course_id, concept_id, "
                    "attempt_key, "
                    "explanation_session_id, review_task_id, response_ref, started_at_utc, "
                    "submitted_at_utc) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        attempt_id,
                        owner_id,
                        str(course_id),
                        concept_id,
```

- [ ] **Step C7C.3: Append `get_attempt` through `list_attempts`**

Append exactly to `backend/src/projectb/infrastructure/repositories/learning_repo.py`:

```python
                        attempt_key,
                        explanation_session_id,
                        review_task_id,
                        response_ref,
                        started_at_utc,
                        submitted_at_utc,
                    ),
                )
                return proposed
        except RepositoryError:
            raise
        except sqlite3.IntegrityError as error:
            raise RepositoryError("state_inconsistent") from error

    def get_attempt(self, owner_id: str, attempt_id: str) -> AttemptRecord:
        owner_id = require_opaque_id(owner_id)
        attempt_id = require_opaque_id(attempt_id)
        row = self._database.fetch_one(
            "SELECT attempt_id, owner_id, course_id, concept_id, attempt_key, "
            "explanation_session_id, review_task_id, response_ref, started_at_utc, "
            "submitted_at_utc FROM attempts WHERE attempt_id = ?",
            (attempt_id,),
        )
        if row is None:
            raise RepositoryError("not_found")
        if str(row["owner_id"]) != owner_id:
            raise RepositoryError("owner_forbidden")
        return self._attempt(row)

    def list_attempts(self, owner_id: str, course_id: CourseId) -> tuple[AttemptRecord, ...]:
        owner_id = require_opaque_id(owner_id)
        course_id = CourseId(require_opaque_id(course_id))
        self._course(owner_id, course_id)
        rows = self._database.fetch_all(
            "SELECT attempt_id, owner_id, course_id, concept_id, attempt_key, "
            "explanation_session_id, review_task_id, response_ref, started_at_utc, "
            "submitted_at_utc FROM attempts WHERE owner_id = ? AND course_id = ? "
            "ORDER BY submitted_at_utc, attempt_id",
            (owner_id, str(course_id)),
        )
        return tuple(self._attempt(row) for row in rows)

```

- [ ] **Step C7D: Append LearningEvidence persistence and reads**

Append exactly to `backend/src/projectb/infrastructure/repositories/learning_repo.py`:

```python
    def append_evidence(
        self, owner_id: str, payload: Mapping[str, object]
    ) -> LearningEvidenceRecord:
        owner_id = require_opaque_id(owner_id)
        (
            evidence_id,
            course_id,
            concept_id,
            attempt_id,
            attempt_key,
            occurred_at_utc,
            evidence_version,
            payload_json,
        ) = _validate_evidence_payload(payload)
        try:
            with self._database.transaction():
                self._course(owner_id, course_id)
                attempt = self._database.fetch_one(
                    "SELECT owner_id, course_id, concept_id, attempt_key, submitted_at_utc "
                    "FROM attempts WHERE attempt_id = ?",
                    (attempt_id,),
                )
                if attempt is None:
                    raise RepositoryError("state_inconsistent")
                if str(attempt["owner_id"]) != owner_id:
                    raise RepositoryError("owner_forbidden")
                if (
                    str(attempt["course_id"]) != str(course_id)
                    or str(attempt["concept_id"]) != concept_id
                    or str(attempt["attempt_key"]) != attempt_key
                    or occurred_at_utc < str(attempt["submitted_at_utc"])
                ):
                    raise RepositoryError("state_inconsistent")
                existing = self._database.fetch_one(
                    "SELECT evidence_id, owner_id, course_id, concept_id, attempt_id, "
                    "attempt_key, "
                    "occurred_at_utc, evidence_version, payload_json FROM learning_evidence "
                    "WHERE evidence_id = ?",
```

- [ ] **Step C7D.2: Append `learning_repo.py` continuation slice 2**

Append exactly to `backend/src/projectb/infrastructure/repositories/learning_repo.py`:

```python
                    (evidence_id,),
                )
                if existing is not None:
                    if str(existing["owner_id"]) != owner_id:
                        raise RepositoryError("owner_forbidden")
                    record = self._evidence(existing)
                    if record.payload_json != payload_json:
                        raise RepositoryError("state_inconsistent")
                    return record
                attempted = self._database.fetch_one(
                    "SELECT evidence_id, owner_id, course_id, concept_id, attempt_id, "
                    "attempt_key, "
                    "occurred_at_utc, evidence_version, payload_json FROM learning_evidence "
                    "WHERE owner_id = ? AND course_id = ? AND attempt_key = ?",
                    (owner_id, str(course_id), attempt_key),
                )
                if attempted is not None:
                    record = self._evidence(attempted)
                    if record.payload_json != payload_json:
                        raise RepositoryError("state_inconsistent")
                    return record
                self._database.execute(
                    "INSERT INTO learning_evidence(evidence_id, owner_id, course_id, "
                    "concept_id, "
                    "attempt_id, attempt_key, occurred_at_utc, evidence_version, payload_json) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        evidence_id,
                        owner_id,
                        str(course_id),
                        concept_id,
                        attempt_id,
                        attempt_key,
                        occurred_at_utc,
                        evidence_version,
                        payload_json,
                    ),
                )
```

- [ ] **Step C7D.3: Append `list_evidence`**

Append exactly to `backend/src/projectb/infrastructure/repositories/learning_repo.py`:

```python
                row = self._database.fetch_one(
                    "SELECT evidence_id, owner_id, course_id, concept_id, attempt_id, "
                    "attempt_key, "
                    "occurred_at_utc, evidence_version, payload_json FROM learning_evidence "
                    "WHERE evidence_id = ?",
                    (evidence_id,),
                )
                if row is None:
                    raise RepositoryError("state_inconsistent")
                return self._evidence(row)
        except RepositoryError:
            raise
        except sqlite3.IntegrityError as error:
            raise RepositoryError("state_inconsistent") from error

    def list_evidence(
        self, owner_id: str, course_id: CourseId
    ) -> tuple[LearningEvidenceRecord, ...]:
        owner_id = require_opaque_id(owner_id)
        course_id = CourseId(require_opaque_id(course_id))
        self._course(owner_id, course_id)
        rows = self._database.fetch_all(
            "SELECT evidence_id, owner_id, course_id, concept_id, attempt_id, attempt_key, "
            "occurred_at_utc, evidence_version, payload_json FROM learning_evidence "
            "WHERE owner_id = ? AND course_id = ? ORDER BY occurred_at_utc, evidence_id",
            (owner_id, str(course_id)),
        )
        return tuple(self._evidence(row) for row in rows)

```

- [ ] **Step C7E: Append plan revision persistence, reads, and exports**

Append exactly to `backend/src/projectb/infrastructure/repositories/learning_repo.py`:

```python
    def append_plan_revision(
        self,
        owner_id: str,
        course_id: CourseId,
        revision_id: str,
        revision_number: int,
        parent_revision_id: str | None,
        reverts_revision_id: str | None,
        plan_input_hash: str,
        policy_version: str,
        payload: Mapping[str, object],
        *,
        expected_latest_number: int | None,
        created_at_utc: str,
    ) -> PlanRevisionRecord:
        owner_id = require_opaque_id(owner_id)
        course_id = CourseId(require_opaque_id(course_id))
        revision_id = require_opaque_id(revision_id)
        revision_number = require_version(revision_number)
        parent_revision_id = _optional_id(parent_revision_id)
        reverts_revision_id = _optional_id(reverts_revision_id)
        plan_input_hash = require_content_hash(plan_input_hash)
        policy_version = _code(policy_version)
        if expected_latest_number is not None:
            require_version(expected_latest_number)
        created_at_utc = require_utc(created_at_utc)
        payload_json = canonical_json(payload)
        proposed = PlanRevisionRecord(
            revision_id,
            owner_id,
            course_id,
            revision_number,
            parent_revision_id,
            reverts_revision_id,
            plan_input_hash,
            policy_version,
            payload_json,
            created_at_utc,
```

- [ ] **Step C7E.2: Append `learning_repo.py` continuation slice 2**

Append exactly to `backend/src/projectb/infrastructure/repositories/learning_repo.py`:

```python
        )
        try:
            with self._database.transaction():
                self._course(owner_id, course_id)
                existing = self._database.fetch_one(
                    "SELECT revision_id, owner_id, course_id, revision_number, "
                    "parent_revision_id, "
                    "reverts_revision_id, plan_input_hash, policy_version, payload_json, "
                    "created_at_utc "
                    "FROM learning_plan_revisions WHERE revision_id = ?",
                    (revision_id,),
                )
                if existing is not None:
                    if str(existing["owner_id"]) != owner_id:
                        raise RepositoryError("owner_forbidden")
                    record = self._revision(existing)
                    if record != proposed:
                        raise RepositoryError("state_inconsistent")
                    return record
                latest = self._database.fetch_one(
                    "SELECT revision_id, revision_number FROM learning_plan_revisions "
                    "WHERE owner_id = ? AND course_id = ? ORDER BY revision_number DESC LIMIT 1",
                    (owner_id, str(course_id)),
                )
                if latest is None:
                    if revision_number != 1 or parent_revision_id is not None:
                        raise RepositoryError("state_inconsistent")
                    if expected_latest_number is not None:
                        raise RepositoryError("state_inconsistent")
                else:
                    latest_number = int(latest["revision_number"])
                    if (
                        expected_latest_number != latest_number
                        or revision_number != latest_number + 1
                        or parent_revision_id != str(latest["revision_id"])
                    ):
                        raise RepositoryError("state_inconsistent")
                if reverts_revision_id is not None:
```

- [ ] **Step C7E.3: Append `learning_repo.py` continuation slice 3**

Append exactly to `backend/src/projectb/infrastructure/repositories/learning_repo.py`:

```python
                    reverted = self._database.fetch_one(
                        "SELECT revision_id FROM learning_plan_revisions "
                        "WHERE revision_id = ? AND owner_id = ? AND course_id = ?",
                        (reverts_revision_id, owner_id, str(course_id)),
                    )
                    if reverted is None:
                        raise RepositoryError("state_inconsistent")
                self._database.execute(
                    "INSERT INTO learning_plan_revisions(revision_id, owner_id, course_id, "
                    "revision_number, parent_revision_id, reverts_revision_id, plan_input_hash, "
                    "policy_version, payload_json, created_at_utc) VALUES (?, ?, ?, ?, ?, ?, ?, "
                    "?, "
                    "?, ?)",
                    (
                        revision_id,
                        owner_id,
                        str(course_id),
                        revision_number,
                        parent_revision_id,
                        reverts_revision_id,
                        plan_input_hash,
                        policy_version,
                        payload_json,
                        created_at_utc,
                    ),
                )
                return proposed
        except RepositoryError:
            raise
        except sqlite3.IntegrityError as error:
            raise RepositoryError("state_inconsistent") from error

```

- [ ] **Step C7E.4: Append `get_latest_plan` through `list_plan_revisions`**

Append exactly to `backend/src/projectb/infrastructure/repositories/learning_repo.py`:

```python
    def get_latest_plan(self, owner_id: str, course_id: CourseId) -> PlanRevisionRecord:
        owner_id = require_opaque_id(owner_id)
        course_id = CourseId(require_opaque_id(course_id))
        self._course(owner_id, course_id)
        row = self._database.fetch_one(
            "SELECT revision_id, owner_id, course_id, revision_number, parent_revision_id, "
            "reverts_revision_id, plan_input_hash, policy_version, payload_json, created_at_utc "
            "FROM learning_plan_revisions WHERE owner_id = ? AND course_id = ? "
            "ORDER BY revision_number DESC LIMIT 1",
            (owner_id, str(course_id)),
        )
        if row is None:
            raise RepositoryError("not_found")
        return self._revision(row)

    def list_plan_revisions(
        self, owner_id: str, course_id: CourseId
    ) -> tuple[PlanRevisionRecord, ...]:
        owner_id = require_opaque_id(owner_id)
        course_id = CourseId(require_opaque_id(course_id))
        self._course(owner_id, course_id)
        rows = self._database.fetch_all(
            "SELECT revision_id, owner_id, course_id, revision_number, parent_revision_id, "
            "reverts_revision_id, plan_input_hash, policy_version, payload_json, created_at_utc "
            "FROM learning_plan_revisions WHERE owner_id = ? AND course_id = ? ORDER BY "
            "revision_number",
            (owner_id, str(course_id)),
        )
        return tuple(self._revision(row) for row in rows)


__all__ = [
    "AttemptRecord",
    "LearningEvidenceRecord",
    "LearningRepository",
    "PlanRevisionRecord",
]
```

This file must remain independent of M2/M3 implementation modules. It validates and stores the confirmed persistence shape but never computes rubric outcomes, mastery, due dates, plan IDs, or policy decisions.

- [ ] **Step C8A: Create remote contracts, state domains, and validation helpers**

Create `backend/src/projectb/infrastructure/repositories/remote_repo.py` with exactly:

```python
from __future__ import annotations

import hashlib
import sqlite3
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from projectb.domain.types import CourseId, MaterialId
from projectb.infrastructure.sqlite import (
    Database,
    JsonValue,
    RepositoryError,
    canonical_json,
    parse_json_object,
    require_content_hash,
    require_opaque_id,
    require_utc,
    require_version,
)

_MATERIAL_ROLES = {"lecture", "past_paper", "teacher_focus"}
_CONSENT_MODES = {"F"}
_CONSENT_SCOPE_KEYS = {
    "adapter_id",
    "provider_profile_id",
    "config_fingerprint",
    "capability_snapshot_id",
    "policy_snapshot_id",
    "materials",
}
_OBJECT_KINDS = {"file", "association", "vector_store"}
_OBJECT_STATES = {
    "awaiting_consent",
    "uploading",
    "indexing",
    "ready",
    "failed",
```

- [ ] **Step C8A.2: Append `remote_repo.py` continuation slice 2**

Append exactly to `backend/src/projectb/infrastructure/repositories/remote_repo.py`:

```python
    "delete_requested",
    "deleted",
    "delete_incomplete",
    "source_disabled",
}
_OBJECT_TRANSITIONS = {
    "awaiting_consent": {"uploading"},
    "uploading": {"indexing", "failed", "delete_requested", "source_disabled"},
    "indexing": {"ready", "failed", "delete_requested", "source_disabled"},
    "ready": {"delete_requested", "source_disabled"},
    "failed": {"uploading", "delete_requested", "source_disabled"},
    "delete_requested": {"delete_incomplete"},
    "delete_incomplete": {"delete_requested"},
    "source_disabled": {"delete_requested"},
    "deleted": set(),
}
_JOB_STATES = {
    "queued",
    "running",
    "cancelling",
    "cancelled",
    "succeeded",
    "failed",
    "recovery_required",
}
_JOB_TRANSITIONS = {
    "queued": {"running", "cancelling", "cancelled", "failed"},
    "running": {"cancelling", "succeeded", "failed", "recovery_required"},
    "cancelling": {"cancelled", "failed", "recovery_required"},
    "cancelled": set(),
    "succeeded": set(),
    "failed": {"queued", "recovery_required"},
    "recovery_required": {"queued", "running", "failed"},
}
_AUDIT_METADATA_KEYS = {
    "count",
    "duration_ms",
    "error_code",
```

- [ ] **Step C8A.3: Append `remote_repo.py` continuation slice 3**

Append exactly to `backend/src/projectb/infrastructure/repositories/remote_repo.py`:

```python
    "job_kind",
    "mode",
    "reason_code",
    "retryable",
    "source",
    "state",
}
_AUDIT_EVENT_KINDS = {
    "consent_revoked",
    "learning_evidence",
    "material_batch",
    "plan_revision",
    "remote_delete",
    "remote_state",
}
_AUDIT_OUTCOMES = {"accepted", "rejected", "succeeded", "failed"}
_AUDIT_ERROR_CODES = {
    "cancelled",
    "credential_unavailable",
    "delete_incomplete",
    "not_found",
    "owner_forbidden",
    "provider_scope_violation",
    "source_insufficient",
    "state_inconsistent",
    "timeout",
}
_AUDIT_REASON_CODES = {
    "config_changed",
    "consent_revoked",
    "mode_changed",
    "policy_changed",
    "profile_changed",
    "provider_deleted",
    "user_deleted",
}
_AUDIT_JOB_KINDS = {
    "local_import",
```

- [ ] **Step C8A.4: Append `ConsentRecord` through `RemoteObjectVersion`**

Append exactly to `backend/src/projectb/infrastructure/repositories/remote_repo.py`:

```python
    "remote_delete",
    "remote_index",
    "remote_reconcile",
    "remote_upload",
    "upload",
}
_AUDIT_SOURCES = {"local", "provider", "system"}


@dataclass(frozen=True, slots=True)
class ConsentRecord:
    consent_id: str
    owner_id: str
    course_id: CourseId
    mode: str
    payload_scope_json: str
    profile_ref: str
    config_fingerprint: str
    capability_snapshot_id: str
    policy_snapshot_id: str
    revoked_at_utc: str | None
    created_at_utc: str

    @property
    def payload_scope(self) -> dict[str, JsonValue]:
        return parse_json_object(self.payload_scope_json)


@dataclass(frozen=True, slots=True)
class RemoteObjectVersion:
    object_id: str
    owner_id: str
    course_id: CourseId
    version: int
    state: str
    config_fingerprint: str
    payload_json: str
    created_at_utc: str

```

- [ ] **Step C8A.5: Append `payload` through `RemoteJobVersion`**

Append exactly to `backend/src/projectb/infrastructure/repositories/remote_repo.py`:

```python
    @property
    def payload(self) -> dict[str, JsonValue]:
        return parse_json_object(self.payload_json)


@dataclass(frozen=True, slots=True)
class RemoteObjectRecord:
    object_id: str
    owner_id: str
    course_id: CourseId
    material_id: MaterialId
    consent_id: str | None
    object_kind: str
    state: str
    version: int
    config_fingerprint: str
    scope_token: str | None
    protected_ref: str | None
    payload_json: str
    created_at_utc: str


@dataclass(frozen=True, slots=True)
class RemoteJobVersion:
    job_id: str
    owner_id: str
    course_id: CourseId
    version: int
    state: str
    completed_units: int
    total_units: int
    error_code: str | None
    payload_json: str
    created_at_utc: str


```

- [ ] **Step C8A.6: Append `RemoteJobRecord` through `AuditEvent`**

Append exactly to `backend/src/projectb/infrastructure/repositories/remote_repo.py`:

```python
@dataclass(frozen=True, slots=True)
class RemoteJobRecord:
    job_id: str
    owner_id: str
    course_id: CourseId
    object_id: str | None
    idempotency_key: str
    state: str
    version: int
    completed_units: int
    total_units: int
    error_code: str | None
    payload_json: str
    created_at_utc: str


@dataclass(frozen=True, slots=True)
class TombstoneRecord:
    tombstone_id: str
    owner_id: str
    entity_kind: str
    entity_id: str
    reason_code: str
    metadata_json: str
    created_at_utc: str


@dataclass(frozen=True, slots=True)
class AuditEvent:
    event_id: str
    owner_id: str
    event_kind: str
    subject_id: str
    outcome_code: str
    metadata_json: str
    occurred_at_utc: str


```

- [ ] **Step C8A.7: Append `_text` through `_nonnegative`**

Append exactly to `backend/src/projectb/infrastructure/repositories/remote_repo.py`:

```python
def _text(value: object) -> str:
    if not isinstance(value, str) or not value or value.strip() != value:
        raise RepositoryError("state_inconsistent")
    return value


def _code(value: object) -> str:
    value = _text(value)
    if len(value) > 96 or any(
        character not in "abcdefghijklmnopqrstuvwxyz0123456789_.:-" for character in value
    ):
        raise RepositoryError("state_inconsistent")
    return value


def _optional_id(value: object) -> str | None:
    if value is None:
        return None
    return require_opaque_id(value)


def _mapping(value: object) -> Mapping[object, object]:
    if not isinstance(value, Mapping):
        raise RepositoryError("state_inconsistent")
    return value


def _sequence(value: object) -> Sequence[object]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        raise RepositoryError("state_inconsistent")
    return value


def _nonnegative(value: object) -> int:
    if type(value) is not int or value < 0:
        raise RepositoryError("state_inconsistent")
    return value


```

- [ ] **Step C8A.8: Append `_expected_scope_token` through `_scope_json`**

Append exactly to `backend/src/projectb/infrastructure/repositories/remote_repo.py`:

```python
def _expected_scope_token(
    course_id: CourseId,
    material_id: MaterialId,
    content_hash: str,
    consent_id: str,
    config_fingerprint: str,
) -> str:
    canonical = "|".join(
        (str(course_id), str(material_id), content_hash, consent_id, config_fingerprint)
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _scope_json(
    payload: Mapping[str, object],
    profile_ref: str,
    config_fingerprint: str,
    capability_snapshot_id: str,
    policy_snapshot_id: str,
) -> str:
    if set(payload) != _CONSENT_SCOPE_KEYS:
        raise RepositoryError("state_inconsistent")
    if (
        _text(payload["provider_profile_id"]) != profile_ref
        or require_content_hash(payload["config_fingerprint"]) != config_fingerprint
        or require_opaque_id(payload["capability_snapshot_id"]) != capability_snapshot_id
        or require_opaque_id(payload["policy_snapshot_id"]) != policy_snapshot_id
    ):
        raise RepositoryError("state_inconsistent")
    _code(payload["adapter_id"])
    material_ids: list[str] = []
    for raw_material in _sequence(payload["materials"]):
        material = _mapping(raw_material)
        if set(material) != {"material_id", "content_hash", "role"}:
            raise RepositoryError("state_inconsistent")
        material_ids.append(require_opaque_id(material.get("material_id")))
        require_content_hash(material.get("content_hash"))
        role = _text(material.get("role"))
        if role not in _MATERIAL_ROLES:
            raise RepositoryError("state_inconsistent")
```

- [ ] **Step C8A.9: Append `_audit_metadata_json`**

Append exactly to `backend/src/projectb/infrastructure/repositories/remote_repo.py`:

```python
    if not material_ids:
        raise RepositoryError("state_inconsistent")
    if material_ids != sorted(material_ids) or len(set(material_ids)) != len(material_ids):
        raise RepositoryError("state_inconsistent")
    return canonical_json(payload)


def _audit_metadata_json(metadata: Mapping[str, object]) -> str:
    if not set(metadata).issubset(_AUDIT_METADATA_KEYS):
        raise RepositoryError("state_inconsistent")
    for key, value in metadata.items():
        if key == "count":
            if _nonnegative(value) > 1_000_000:
                raise RepositoryError("state_inconsistent")
        elif key == "duration_ms":
            if _nonnegative(value) > 3_600_000:
                raise RepositoryError("state_inconsistent")
        elif key == "retryable":
            if type(value) is not bool:
                raise RepositoryError("state_inconsistent")
        elif key == "mode":
            if _text(value) not in {"L", "P", "F"}:
                raise RepositoryError("state_inconsistent")
        elif key == "error_code":
            if _text(value) not in _AUDIT_ERROR_CODES:
                raise RepositoryError("state_inconsistent")
        elif key == "reason_code":
            if _text(value) not in _AUDIT_REASON_CODES:
                raise RepositoryError("state_inconsistent")
        elif key == "job_kind":
            if _text(value) not in _AUDIT_JOB_KINDS:
                raise RepositoryError("state_inconsistent")
        elif key == "source":
            if _text(value) not in _AUDIT_SOURCES:
                raise RepositoryError("state_inconsistent")
        elif key == "state":
            if _text(value) not in (_OBJECT_STATES | _JOB_STATES):
                raise RepositoryError("state_inconsistent")
        else:
            raise RepositoryError("state_inconsistent")
    return canonical_json(metadata)


```

- [ ] **Step C8B: Append consent row adapters and exact-F consent creation**

Append exactly to `backend/src/projectb/infrastructure/repositories/remote_repo.py`:

```python
class RemoteRepository:
    def __init__(self, database: Database) -> None:
        self._database = database

    def _course(self, owner_id: str, course_id: CourseId) -> sqlite3.Row:
        row = self._database.fetch_one(
            "SELECT owner_id, tombstoned_at_utc FROM courses WHERE course_id = ?",
            (str(course_id),),
        )
        if row is None:
            raise RepositoryError("not_found")
        if str(row["owner_id"]) != owner_id:
            raise RepositoryError("owner_forbidden")
        if row["tombstoned_at_utc"] is not None:
            raise RepositoryError("state_inconsistent")
        return row

    def _consent_row(self, consent_id: str) -> sqlite3.Row | None:
        return self._database.fetch_one(
            "SELECT c.consent_id, c.owner_id, c.course_id, c.mode, c.payload_scope_json, "
            "c.profile_ref, c.config_fingerprint, c.capability_snapshot_id, "
            "c.policy_snapshot_id, "
            "t.created_at_utc AS revoked_marker_utc, c.created_at_utc "
            "FROM consent_records c LEFT JOIN tombstones t ON t.owner_id = c.owner_id "
            "AND t.entity_kind = 'consent' AND t.entity_id = c.consent_id WHERE c.consent_id = "
            "?",
            (consent_id,),
        )

```

- [ ] **Step C8B.2: Append `_consent` through `append_consent`**

Append exactly to `backend/src/projectb/infrastructure/repositories/remote_repo.py`:

```python
    @staticmethod
    def _consent(row: sqlite3.Row) -> ConsentRecord:
        return ConsentRecord(
            consent_id=str(row["consent_id"]),
            owner_id=str(row["owner_id"]),
            course_id=CourseId(str(row["course_id"])),
            mode=str(row["mode"]),
            payload_scope_json=str(row["payload_scope_json"]),
            profile_ref=str(row["profile_ref"]),
            config_fingerprint=str(row["config_fingerprint"]),
            capability_snapshot_id=str(row["capability_snapshot_id"]),
            policy_snapshot_id=str(row["policy_snapshot_id"]),
            revoked_at_utc=(
                None if row["revoked_marker_utc"] is None else str(row["revoked_marker_utc"])
            ),
            created_at_utc=str(row["created_at_utc"]),
        )

    def append_consent(
        self,
        owner_id: str,
        course_id: CourseId,
        consent_id: str,
        mode: str,
        payload_scope: Mapping[str, object],
        profile_ref: str,
        config_fingerprint: str,
        capability_snapshot_id: str,
        policy_snapshot_id: str,
        created_at_utc: str,
```

- [ ] **Step C8B.3: Append `remote_repo.py` continuation slice 3**

Append exactly to `backend/src/projectb/infrastructure/repositories/remote_repo.py`:

```python
    ) -> ConsentRecord:
        owner_id = require_opaque_id(owner_id)
        course_id = CourseId(require_opaque_id(course_id))
        consent_id = require_opaque_id(consent_id)
        mode = _text(mode)
        if mode not in _CONSENT_MODES:
            raise RepositoryError("state_inconsistent")
        profile_ref = require_opaque_id(profile_ref)
        config_fingerprint = require_content_hash(config_fingerprint)
        capability_snapshot_id = require_opaque_id(capability_snapshot_id)
        policy_snapshot_id = require_opaque_id(policy_snapshot_id)
        created_at_utc = require_utc(created_at_utc)
        payload_scope_json = _scope_json(
            payload_scope,
            profile_ref,
            config_fingerprint,
            capability_snapshot_id,
            policy_snapshot_id,
        )
        proposed = ConsentRecord(
            consent_id,
            owner_id,
            course_id,
            mode,
            payload_scope_json,
            profile_ref,
            config_fingerprint,
            capability_snapshot_id,
            policy_snapshot_id,
            None,
            created_at_utc,
        )
        try:
            with self._database.transaction():
                self._course(owner_id, course_id)
                for raw_material in _sequence(payload_scope["materials"]):
                    scoped = _mapping(raw_material)
                    scoped_material_id = require_opaque_id(scoped.get("material_id"))
```

- [ ] **Step C8B.4: Append `remote_repo.py` continuation slice 4**

Append exactly to `backend/src/projectb/infrastructure/repositories/remote_repo.py`:

```python
                    scoped_hash = require_content_hash(scoped.get("content_hash"))
                    scoped_role = _text(scoped.get("role"))
                    material = self._database.fetch_one(
                        "SELECT owner_id, course_id, content_hash, role, tombstoned_at_utc "
                        "FROM materials WHERE material_id = ?",
                        (scoped_material_id,),
                    )
                    if material is None:
                        raise RepositoryError("state_inconsistent")
                    if str(material["owner_id"]) != owner_id:
                        raise RepositoryError("owner_forbidden")
                    if (
                        str(material["course_id"]) != str(course_id)
                        or str(material["content_hash"]) != scoped_hash
                        or str(material["role"]) != scoped_role
                        or material["tombstoned_at_utc"] is not None
                    ):
                        raise RepositoryError("state_inconsistent")
                existing = self._consent_row(consent_id)
                if existing is not None:
                    if str(existing["owner_id"]) != owner_id:
                        raise RepositoryError("owner_forbidden")
                    record = self._consent(existing)
                    if record != proposed:
                        raise RepositoryError("state_inconsistent")
                    return record
                self._database.execute(
                    "INSERT INTO consent_records(consent_id, owner_id, course_id, mode, "
                    "payload_scope_json, profile_ref, config_fingerprint, "
                    "capability_snapshot_id, "
                    "policy_snapshot_id, created_at_utc) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        consent_id,
                        owner_id,
                        str(course_id),
                        mode,
                        payload_scope_json,
                        profile_ref,
```

- [ ] **Step C8B.5: Append `get_consent`**

Append exactly to `backend/src/projectb/infrastructure/repositories/remote_repo.py`:

```python
                        config_fingerprint,
                        capability_snapshot_id,
                        policy_snapshot_id,
                        created_at_utc,
                    ),
                )
                return proposed
        except RepositoryError:
            raise
        except sqlite3.IntegrityError as error:
            raise RepositoryError("state_inconsistent") from error

    def get_consent(self, owner_id: str, consent_id: str) -> ConsentRecord:
        owner_id = require_opaque_id(owner_id)
        consent_id = require_opaque_id(consent_id)
        row = self._consent_row(consent_id)
        if row is None:
            raise RepositoryError("not_found")
        if str(row["owner_id"]) != owner_id:
            raise RepositoryError("owner_forbidden")
        return self._consent(row)

```

- [ ] **Step C8C: Append consent revocation, token invalidation, and scope matching**

Append exactly to `backend/src/projectb/infrastructure/repositories/remote_repo.py`:

```python
    def revoke_consent(self, owner_id: str, consent_id: str, revoked_at_utc: str) -> ConsentRecord:
        owner_id = require_opaque_id(owner_id)
        consent_id = require_opaque_id(consent_id)
        revoked_at_utc = require_utc(revoked_at_utc)
        with self._database.transaction():
            row = self._consent_row(consent_id)
            if row is None:
                raise RepositoryError("not_found")
            if str(row["owner_id"]) != owner_id:
                raise RepositoryError("owner_forbidden")
            if row["revoked_marker_utc"] is None:
                self._database.execute(
                    "INSERT INTO tombstones(tombstone_id, owner_id, entity_kind, entity_id, "
                    "reason_code, metadata_json, created_at_utc) VALUES (?, ?, 'consent', ?, ?, "
                    "?, "
                    "?)",
                    (
                        f"consent:{consent_id}",
                        owner_id,
                        consent_id,
                        "consent_revoked",
                        canonical_json({"status": "revoked"}),
                        revoked_at_utc,
                    ),
                )
            elif str(row["revoked_marker_utc"]) != revoked_at_utc:
                raise RepositoryError("state_inconsistent")
            self._database.execute(
                "UPDATE remote_objects SET scope_token = NULL, updated_at_utc = ? "
                "WHERE owner_id = ? AND consent_id = ? AND tombstoned_at_utc IS NULL",
                (revoked_at_utc, owner_id, consent_id),
            )
            updated = self._consent_row(consent_id)
            if updated is None:
                raise RepositoryError("state_inconsistent")
            return self._consent(updated)

```

- [ ] **Step C8C.2: Append `_active_consent`**

Append exactly to `backend/src/projectb/infrastructure/repositories/remote_repo.py`:

```python
    def _active_consent(
        self,
        owner_id: str,
        consent_id: str,
        course_id: CourseId,
        config_fingerprint: str,
        material_id: MaterialId,
        content_hash: str,
        role: str,
    ) -> ConsentRecord:
        record = self.get_consent(owner_id, consent_id)
        if (
            record.course_id != course_id
            or record.config_fingerprint != config_fingerprint
            or record.revoked_at_utc is not None
        ):
            raise RepositoryError("state_inconsistent")
        matches = 0
        for raw_material in _sequence(record.payload_scope["materials"]):
            material = _mapping(raw_material)
            if (
                material.get("material_id") == str(material_id)
                and material.get("content_hash") == content_hash
                and material.get("role") == role
            ):
                matches += 1
        if matches != 1:
            raise RepositoryError("state_inconsistent")
        return record

```

- [ ] **Step C8D: Append remote-object row adapters**

Append exactly to `backend/src/projectb/infrastructure/repositories/remote_repo.py`:

```python
    def _object_row(self, object_id: str) -> sqlite3.Row | None:
        return self._database.fetch_one(
            "SELECT object_id, owner_id, course_id, material_id, consent_id, object_kind, "
            "state, "
            "active_version, config_fingerprint, scope_token, provider_ref, tombstoned_at_utc "
            "FROM remote_objects WHERE object_id = ?",
            (object_id,),
        )

    @staticmethod
    def _object_version(row: sqlite3.Row) -> RemoteObjectVersion:
        return RemoteObjectVersion(
            object_id=str(row["object_id"]),
            owner_id=str(row["owner_id"]),
            course_id=CourseId(str(row["course_id"])),
            version=int(row["version"]),
            state=str(row["state"]),
            config_fingerprint=str(row["config_fingerprint"]),
            payload_json=str(row["payload_json"]),
            created_at_utc=str(row["created_at_utc"]),
        )

    def _active_object(self, row: sqlite3.Row) -> RemoteObjectRecord:
        version_row = self._database.fetch_one(
            "SELECT object_id, owner_id, course_id, version, state, config_fingerprint, "
            "payload_json, created_at_utc FROM remote_object_versions "
            "WHERE object_id = ? AND owner_id = ? AND version = ?",
            (str(row["object_id"]), str(row["owner_id"]), int(row["active_version"])),
        )
        if version_row is None:
            raise RepositoryError("state_inconsistent")
        version = self._object_version(version_row)
        return RemoteObjectRecord(
            object_id=str(row["object_id"]),
            owner_id=str(row["owner_id"]),
            course_id=CourseId(str(row["course_id"])),
            material_id=MaterialId(str(row["material_id"])),
            consent_id=None if row["consent_id"] is None else str(row["consent_id"]),
```

- [ ] **Step C8D.2: Append `remote_repo.py` continuation slice 2**

Append exactly to `backend/src/projectb/infrastructure/repositories/remote_repo.py`:

```python
            object_kind=str(row["object_kind"]),
            state=str(row["state"]),
            version=int(row["active_version"]),
            config_fingerprint=str(row["config_fingerprint"]),
            scope_token=None if row["scope_token"] is None else str(row["scope_token"]),
            protected_ref=None if row["provider_ref"] is None else str(row["provider_ref"]),
            payload_json=version.payload_json,
            created_at_utc=version.created_at_utc,
        )

```

- [ ] **Step C8D2: Append remote-object write validation and canonicalization**

Append exactly to `backend/src/projectb/infrastructure/repositories/remote_repo.py`:

```python
    def put_object_versioned(
        self,
        owner_id: str,
        course_id: CourseId,
        object_id: str,
        material_id: MaterialId,
        consent_id: str | None,
        object_kind: str,
        state: str,
        config_fingerprint: str,
        scope_token: str | None,
        protected_ref: str | None,
        payload: Mapping[str, object],
        *,
        expected_version: int | None,
        created_at_utc: str,
    ) -> RemoteObjectRecord:
        owner_id = require_opaque_id(owner_id)
        course_id = CourseId(require_opaque_id(course_id))
        object_id = require_opaque_id(object_id)
        material_id = MaterialId(require_opaque_id(material_id))
        consent_id = _optional_id(consent_id)
        object_kind = _text(object_kind)
        state = _text(state)
        if object_kind not in _OBJECT_KINDS or state not in _OBJECT_STATES or state == "deleted":
            raise RepositoryError("state_inconsistent")
        config_fingerprint = require_content_hash(config_fingerprint)
        scope_token = None if scope_token is None else require_content_hash(scope_token)
        protected_ref = _optional_id(protected_ref)
        if state == "awaiting_consent" and (
            consent_id is not None or scope_token is not None or protected_ref is not None
        ):
            raise RepositoryError("state_inconsistent")
        if state != "awaiting_consent" and consent_id is None:
            raise RepositoryError("state_inconsistent")
        if state in {"uploading", "indexing", "ready"} and (
            scope_token is None or protected_ref is None
        ):
```

- [ ] **Step C8D2.2: Append `remote_repo.py` continuation slice 2**

Append exactly to `backend/src/projectb/infrastructure/repositories/remote_repo.py`:

```python
            raise RepositoryError("state_inconsistent")
        if state in {"delete_requested", "delete_incomplete", "source_disabled"} and (
            scope_token is not None
        ):
            raise RepositoryError("state_inconsistent")
        if expected_version is not None:
            require_version(expected_version)
        created_at_utc = require_utc(created_at_utc)
        payload_json = canonical_json(payload)
```

- [ ] **Step C8D3: Append remote-object owner/material/consent transaction setup**

Append exactly to `backend/src/projectb/infrastructure/repositories/remote_repo.py`:

```python
        try:
            with self._database.transaction():
                self._course(owner_id, course_id)
                material = self._database.fetch_one(
                    "SELECT owner_id, course_id, content_hash, role, tombstoned_at_utc "
                    "FROM materials WHERE material_id = ?",
                    (str(material_id),),
                )
                if material is None:
                    raise RepositoryError("not_found")
                if str(material["owner_id"]) != owner_id:
                    raise RepositoryError("owner_forbidden")
                if (
                    str(material["course_id"]) != str(course_id)
                    or material["tombstoned_at_utc"] is not None
                ):
                    raise RepositoryError("state_inconsistent")
                content_hash = str(material["content_hash"])
                role = str(material["role"])
```

- [ ] **Step C8D4: Append remote-object insert/version/update transaction branches**

Append exactly to `backend/src/projectb/infrastructure/repositories/remote_repo.py`:

```python
                current = self._object_row(object_id)
                if current is None:
                    if (
                        expected_version is not None
                        or state != "awaiting_consent"
                        or consent_id is not None
                    ):
                        raise RepositoryError("state_inconsistent")
                    self._database.execute(
                        "INSERT INTO remote_objects(object_id, owner_id, course_id, "
                        "material_id, "
                        "consent_id, object_kind, state, active_version, config_fingerprint, "
                        "scope_token, provider_ref, created_at_utc, updated_at_utc) "
                        "VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?, ?, ?, ?, ?)",
                        (
                            object_id,
                            owner_id,
                            str(course_id),
                            str(material_id),
                            consent_id,
                            object_kind,
                            state,
                            config_fingerprint,
                            scope_token,
                            protected_ref,
                            created_at_utc,
                            created_at_utc,
                        ),
                    )
                    self._database.execute(
                        "INSERT INTO remote_object_versions(object_id, owner_id, course_id, "
                        "version, "
                        "state, config_fingerprint, payload_json, created_at_utc) "
                        "VALUES (?, ?, ?, 1, ?, ?, ?, ?)",
                        (
                            object_id,
                            owner_id,
                            str(course_id),
```

- [ ] **Step C8D4.2: Append `remote_repo.py` continuation slice 2**

Append exactly to `backend/src/projectb/infrastructure/repositories/remote_repo.py`:

```python
                            state,
                            config_fingerprint,
                            payload_json,
                            created_at_utc,
                        ),
                    )
                    inserted = self._object_row(object_id)
                    if inserted is None:
                        raise RepositoryError("state_inconsistent")
                    return self._active_object(inserted)
                if str(current["owner_id"]) != owner_id:
                    raise RepositoryError("owner_forbidden")
                if current["tombstoned_at_utc"] is not None:
                    raise RepositoryError("state_inconsistent")
                immutable = (
                    str(current["course_id"]),
                    str(current["material_id"]),
                    str(current["object_kind"]),
                    str(current["config_fingerprint"]),
                )
                proposed_immutable = (
                    str(course_id),
                    str(material_id),
                    object_kind,
                    config_fingerprint,
                )
                if immutable != proposed_immutable:
                    raise RepositoryError("state_inconsistent")
                active = self._active_object(current)
                bound_consent_id = (
                    None if current["consent_id"] is None else str(current["consent_id"])
                )
                if bound_consent_id is not None and consent_id != bound_consent_id:
                    raise RepositoryError("state_inconsistent")
                if bound_consent_id is not None:
                    bound_consent = self.get_consent(owner_id, bound_consent_id)
                    if bound_consent.revoked_at_utc is not None and scope_token is not None:
                        raise RepositoryError("state_inconsistent")
```

- [ ] **Step C8D4.3: Append `remote_repo.py` continuation slice 3**

Append exactly to `backend/src/projectb/infrastructure/repositories/remote_repo.py`:

```python
                if bound_consent_id is None and active.state != "awaiting_consent":
                    raise RepositoryError("state_inconsistent")
                if bound_consent_id is None and state not in {
                    "awaiting_consent",
                    "uploading",
                }:
                    raise RepositoryError("state_inconsistent")
                if state in {"uploading", "indexing", "ready"}:
                    if consent_id is None:
                        raise RepositoryError("state_inconsistent")
                    self._active_consent(
                        owner_id,
                        consent_id,
                        course_id,
                        config_fingerprint,
                        material_id,
                        content_hash,
                        role,
                    )
                    if scope_token != _expected_scope_token(
                        course_id,
                        material_id,
                        content_hash,
                        consent_id,
                        config_fingerprint,
                    ):
                        raise RepositoryError("state_inconsistent")
                if (
                    active.state == state
                    and active.consent_id == consent_id
                    and active.scope_token == scope_token
                    and active.protected_ref == protected_ref
                    and active.payload_json == payload_json
                ):
                    allowed: set[int | None] = {active.version, active.version - 1}
                    if active.version == 1:
                        allowed.add(None)
                    if expected_version not in allowed:
```

- [ ] **Step C8D4.4: Append `remote_repo.py` continuation slice 4**

Append exactly to `backend/src/projectb/infrastructure/repositories/remote_repo.py`:

```python
                        raise RepositoryError("state_inconsistent")
                    return active
                if (
                    expected_version != active.version
                    or state not in _OBJECT_TRANSITIONS[active.state]
                ):
                    raise RepositoryError("state_inconsistent")
                next_version = active.version + 1
                self._database.execute(
                    "INSERT INTO remote_object_versions(object_id, owner_id, course_id, "
                    "version, "
                    "state, config_fingerprint, payload_json, created_at_utc) VALUES (?, ?, ?, "
                    "?, "
                    "?, ?, ?, ?)",
                    (
                        object_id,
                        owner_id,
                        str(course_id),
                        next_version,
                        state,
                        config_fingerprint,
                        payload_json,
                        created_at_utc,
                    ),
                )
                cursor = self._database.execute(
                    "UPDATE remote_objects SET consent_id = ?, state = ?, active_version = ?, "
                    "scope_token = ?, provider_ref = ?, updated_at_utc = ? "
                    "WHERE object_id = ? AND owner_id = ? "
                    "AND active_version = ?",
                    (
                        consent_id,
                        state,
                        next_version,
                        scope_token,
                        protected_ref,
                        created_at_utc,
                        object_id,
```

- [ ] **Step C8D4.5: Append `remote_repo.py` continuation slice 5**

Append exactly to `backend/src/projectb/infrastructure/repositories/remote_repo.py`:

```python
                        owner_id,
                        active.version,
                    ),
                )
                if cursor.rowcount != 1:
                    raise RepositoryError("state_inconsistent")
                updated = self._object_row(object_id)
                if updated is None:
                    raise RepositoryError("state_inconsistent")
                return self._active_object(updated)
        except RepositoryError:
            raise
        except sqlite3.IntegrityError as error:
            raise RepositoryError("state_inconsistent") from error

```

- [ ] **Step C8E: Append active, usable, and history object reads**

Append exactly to `backend/src/projectb/infrastructure/repositories/remote_repo.py`:

```python
    def get_active_object(self, owner_id: str, object_id: str) -> RemoteObjectRecord:
        owner_id = require_opaque_id(owner_id)
        object_id = require_opaque_id(object_id)
        row = self._object_row(object_id)
        if row is None:
            raise RepositoryError("not_found")
        if str(row["owner_id"]) != owner_id:
            raise RepositoryError("owner_forbidden")
        if row["tombstoned_at_utc"] is not None or str(row["state"]) == "deleted":
            raise RepositoryError("not_found")
        return self._active_object(row)

    def list_usable_objects(
        self, owner_id: str, course_id: CourseId
    ) -> tuple[RemoteObjectRecord, ...]:
        owner_id = require_opaque_id(owner_id)
        course_id = CourseId(require_opaque_id(course_id))
        self._course(owner_id, course_id)
        rows = self._database.fetch_all(
            "SELECT object_id, owner_id, course_id, material_id, consent_id, object_kind, "
            "state, "
            "active_version, config_fingerprint, scope_token, provider_ref, tombstoned_at_utc "
            "FROM remote_objects WHERE owner_id = ? AND course_id = ? AND state = 'ready' "
            "AND scope_token IS NOT NULL AND provider_ref IS NOT NULL AND tombstoned_at_utc IS "
            "NULL "
            "ORDER BY object_id",
            (owner_id, str(course_id)),
        )
        usable: list[RemoteObjectRecord] = []
        for row in rows:
            record = self._active_object(row)
            if record.consent_id is None or record.scope_token is None:
                raise RepositoryError("state_inconsistent")
            material = self._database.fetch_one(
                "SELECT content_hash, role FROM materials WHERE material_id = ? AND owner_id = ?",
                (str(record.material_id), owner_id),
            )
            if material is None:
```

- [ ] **Step C8E.2: Append `list_object_history`**

Append exactly to `backend/src/projectb/infrastructure/repositories/remote_repo.py`:

```python
                raise RepositoryError("state_inconsistent")
            consent = self.get_consent(owner_id, record.consent_id)
            if consent.revoked_at_utc is not None:
                continue
            if record.scope_token != _expected_scope_token(
                course_id,
                record.material_id,
                str(material["content_hash"]),
                record.consent_id,
                record.config_fingerprint,
            ):
                raise RepositoryError("state_inconsistent")
            self._active_consent(
                owner_id,
                record.consent_id,
                course_id,
                record.config_fingerprint,
                record.material_id,
                str(material["content_hash"]),
                str(material["role"]),
            )
            usable.append(record)
        return tuple(usable)

    def list_object_history(self, owner_id: str, object_id: str) -> tuple[RemoteObjectVersion, ...]:
        owner_id = require_opaque_id(owner_id)
        object_id = require_opaque_id(object_id)
        row = self._object_row(object_id)
        if row is None:
            raise RepositoryError("not_found")
        if str(row["owner_id"]) != owner_id:
            raise RepositoryError("owner_forbidden")
        rows = self._database.fetch_all(
            "SELECT object_id, owner_id, course_id, version, state, config_fingerprint, "
            "payload_json, created_at_utc FROM remote_object_versions "
            "WHERE object_id = ? AND owner_id = ? ORDER BY version",
            (object_id, owner_id),
        )
        return tuple(self._object_version(item) for item in rows)

```

- [ ] **Step C8F: Append remote-job row adapters**

Append exactly to `backend/src/projectb/infrastructure/repositories/remote_repo.py`:

```python
    @staticmethod
    def _job_version(row: sqlite3.Row) -> RemoteJobVersion:
        return RemoteJobVersion(
            job_id=str(row["job_id"]),
            owner_id=str(row["owner_id"]),
            course_id=CourseId(str(row["course_id"])),
            version=int(row["version"]),
            state=str(row["state"]),
            completed_units=int(row["completed_units"]),
            total_units=int(row["total_units"]),
            error_code=None if row["error_code"] is None else str(row["error_code"]),
            payload_json=str(row["payload_json"]),
            created_at_utc=str(row["created_at_utc"]),
        )

    def _job_row(self, job_id: str) -> sqlite3.Row | None:
        return self._database.fetch_one(
            "SELECT job_id, owner_id, course_id, object_id, idempotency_key, state, "
            "active_version, "
            "completed_units, total_units, error_code FROM remote_jobs WHERE job_id = ?",
            (job_id,),
        )

    def _active_job(self, row: sqlite3.Row) -> RemoteJobRecord:
        version_row = self._database.fetch_one(
            "SELECT job_id, owner_id, course_id, version, state, completed_units, total_units, "
            "error_code, payload_json, created_at_utc FROM remote_job_versions "
            "WHERE job_id = ? AND owner_id = ? AND version = ?",
            (str(row["job_id"]), str(row["owner_id"]), int(row["active_version"])),
        )
        if version_row is None:
            raise RepositoryError("state_inconsistent")
        version = self._job_version(version_row)
        return RemoteJobRecord(
            job_id=str(row["job_id"]),
            owner_id=str(row["owner_id"]),
            course_id=CourseId(str(row["course_id"])),
            object_id=None if row["object_id"] is None else str(row["object_id"]),
```

- [ ] **Step C8F.2: Append `remote_repo.py` continuation slice 2**

Append exactly to `backend/src/projectb/infrastructure/repositories/remote_repo.py`:

```python
            idempotency_key=str(row["idempotency_key"]),
            state=version.state,
            version=version.version,
            completed_units=version.completed_units,
            total_units=version.total_units,
            error_code=version.error_code,
            payload_json=version.payload_json,
            created_at_utc=version.created_at_utc,
        )

```

- [ ] **Step C8G: Append remote-job write validation and canonicalization**

Append exactly to `backend/src/projectb/infrastructure/repositories/remote_repo.py`:

```python
    def put_job_versioned(
        self,
        owner_id: str,
        course_id: CourseId,
        job_id: str,
        object_id: str | None,
        idempotency_key: str,
        state: str,
        completed_units: int,
        total_units: int,
        error_code: str | None,
        payload: Mapping[str, object],
        *,
        expected_version: int | None,
        created_at_utc: str,
    ) -> RemoteJobRecord:
        owner_id = require_opaque_id(owner_id)
        course_id = CourseId(require_opaque_id(course_id))
        job_id = require_opaque_id(job_id)
        object_id = _optional_id(object_id)
        idempotency_key = require_opaque_id(idempotency_key)
        state = _text(state)
        if state not in _JOB_STATES:
            raise RepositoryError("state_inconsistent")
        completed_units = _nonnegative(completed_units)
        total_units = _nonnegative(total_units)
        if completed_units > total_units:
            raise RepositoryError("state_inconsistent")
        error_code = None if error_code is None else _code(error_code)
        if expected_version is not None:
            require_version(expected_version)
        created_at_utc = require_utc(created_at_utc)
        payload_json = canonical_json(payload)
```

- [ ] **Step C8G2: Append remote-job idempotent insert/version/update transaction branches**

Append exactly to `backend/src/projectb/infrastructure/repositories/remote_repo.py`:

```python
        try:
            with self._database.transaction():
                self._course(owner_id, course_id)
                if object_id is not None:
                    object_row = self._object_row(object_id)
                    if object_row is None:
                        raise RepositoryError("not_found")
                    if str(object_row["owner_id"]) != owner_id:
                        raise RepositoryError("owner_forbidden")
                    if str(object_row["course_id"]) != str(course_id):
                        raise RepositoryError("state_inconsistent")
                current = self._job_row(job_id)
                if current is None:
                    duplicate = self._database.fetch_one(
                        "SELECT job_id FROM remote_jobs WHERE owner_id = ? AND course_id = ? "
                        "AND idempotency_key = ?",
                        (owner_id, str(course_id), idempotency_key),
                    )
                    if duplicate is not None:
                        duplicate_row = self._job_row(str(duplicate["job_id"]))
                        if duplicate_row is None:
                            raise RepositoryError("state_inconsistent")
                        record = self._active_job(duplicate_row)
                        if (
                            record.object_id != object_id
                            or record.state != state
                            or record.completed_units != completed_units
                            or record.total_units != total_units
                            or record.error_code != error_code
                            or record.payload_json != payload_json
                        ):
                            raise RepositoryError("state_inconsistent")
                        return record
                    if expected_version is not None or state != "queued":
                        raise RepositoryError("state_inconsistent")
                    self._database.execute(
                        "INSERT INTO remote_jobs(job_id, owner_id, course_id, object_id, "
                        "idempotency_key, state, active_version, completed_units, total_units, "
```

- [ ] **Step C8G2.2: Append `remote_repo.py` continuation slice 2**

Append exactly to `backend/src/projectb/infrastructure/repositories/remote_repo.py`:

```python
                        "error_code, created_at_utc, updated_at_utc) "
                        "VALUES (?, ?, ?, ?, ?, ?, 1, ?, ?, ?, ?, ?)",
                        (
                            job_id,
                            owner_id,
                            str(course_id),
                            object_id,
                            idempotency_key,
                            state,
                            completed_units,
                            total_units,
                            error_code,
                            created_at_utc,
                            created_at_utc,
                        ),
                    )
                    self._database.execute(
                        "INSERT INTO remote_job_versions(job_id, owner_id, course_id, version, "
                        "state, "
                        "completed_units, total_units, error_code, payload_json, "
                        "created_at_utc) "
                        "VALUES (?, ?, ?, 1, ?, ?, ?, ?, ?, ?)",
                        (
                            job_id,
                            owner_id,
                            str(course_id),
                            state,
                            completed_units,
                            total_units,
                            error_code,
                            payload_json,
                            created_at_utc,
                        ),
                    )
                    inserted = self._job_row(job_id)
                    if inserted is None:
                        raise RepositoryError("state_inconsistent")
                    return self._active_job(inserted)
```

- [ ] **Step C8G2.3: Append `remote_repo.py` continuation slice 3**

Append exactly to `backend/src/projectb/infrastructure/repositories/remote_repo.py`:

```python
                if str(current["owner_id"]) != owner_id:
                    raise RepositoryError("owner_forbidden")
                if (
                    str(current["course_id"]) != str(course_id)
                    or (None if current["object_id"] is None else str(current["object_id"]))
                    != object_id
                    or str(current["idempotency_key"]) != idempotency_key
                ):
                    raise RepositoryError("state_inconsistent")
                active = self._active_job(current)
                if (
                    active.state == state
                    and active.completed_units == completed_units
                    and active.total_units == total_units
                    and active.error_code == error_code
                    and active.payload_json == payload_json
                ):
                    allowed: set[int | None] = {active.version, active.version - 1}
                    if active.version == 1:
                        allowed.add(None)
                    if expected_version not in allowed:
                        raise RepositoryError("state_inconsistent")
                    return active
                if (
                    expected_version != active.version
                    or state not in _JOB_TRANSITIONS[active.state]
                    or completed_units < active.completed_units
                    or total_units != active.total_units
                ):
                    raise RepositoryError("state_inconsistent")
                next_version = active.version + 1
                self._database.execute(
                    "INSERT INTO remote_job_versions(job_id, owner_id, course_id, version, "
                    "state, "
                    "completed_units, total_units, error_code, payload_json, created_at_utc) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        job_id,
```

- [ ] **Step C8G2.4: Append `remote_repo.py` continuation slice 4**

Append exactly to `backend/src/projectb/infrastructure/repositories/remote_repo.py`:

```python
                        owner_id,
                        str(course_id),
                        next_version,
                        state,
                        completed_units,
                        total_units,
                        error_code,
                        payload_json,
                        created_at_utc,
                    ),
                )
                cursor = self._database.execute(
                    "UPDATE remote_jobs SET state = ?, active_version = ?, completed_units = ?, "
                    "total_units = ?, error_code = ?, updated_at_utc = ? "
                    "WHERE job_id = ? AND owner_id = ? AND active_version = ?",
                    (
                        state,
                        next_version,
                        completed_units,
                        total_units,
                        error_code,
                        created_at_utc,
                        job_id,
                        owner_id,
                        active.version,
                    ),
                )
                if cursor.rowcount != 1:
                    raise RepositoryError("state_inconsistent")
                updated = self._job_row(job_id)
                if updated is None:
                    raise RepositoryError("state_inconsistent")
                return self._active_job(updated)
        except RepositoryError:
            raise
        except sqlite3.IntegrityError as error:
            raise RepositoryError("state_inconsistent") from error

```

- [ ] **Step C8H: Append remote-job active and history reads**

Append exactly to `backend/src/projectb/infrastructure/repositories/remote_repo.py`:

```python
    def get_active_job(self, owner_id: str, job_id: str) -> RemoteJobRecord:
        owner_id = require_opaque_id(owner_id)
        job_id = require_opaque_id(job_id)
        row = self._job_row(job_id)
        if row is None:
            raise RepositoryError("not_found")
        if str(row["owner_id"]) != owner_id:
            raise RepositoryError("owner_forbidden")
        return self._active_job(row)

    def list_job_history(self, owner_id: str, job_id: str) -> tuple[RemoteJobVersion, ...]:
        owner_id = require_opaque_id(owner_id)
        job_id = require_opaque_id(job_id)
        row = self._job_row(job_id)
        if row is None:
            raise RepositoryError("not_found")
        if str(row["owner_id"]) != owner_id:
            raise RepositoryError("owner_forbidden")
        rows = self._database.fetch_all(
            "SELECT job_id, owner_id, course_id, version, state, completed_units, total_units, "
            "error_code, payload_json, created_at_utc FROM remote_job_versions "
            "WHERE job_id = ? AND owner_id = ? ORDER BY version",
            (job_id, owner_id),
        )
        return tuple(self._job_version(item) for item in rows)

```

- [ ] **Step C8I: Append remote-object tombstone persistence**

Append exactly to `backend/src/projectb/infrastructure/repositories/remote_repo.py`:

```python
    @staticmethod
    def _tombstone(row: sqlite3.Row) -> TombstoneRecord:
        return TombstoneRecord(
            tombstone_id=str(row["tombstone_id"]),
            owner_id=str(row["owner_id"]),
            entity_kind=str(row["entity_kind"]),
            entity_id=str(row["entity_id"]),
            reason_code=str(row["reason_code"]),
            metadata_json=str(row["metadata_json"]),
            created_at_utc=str(row["created_at_utc"]),
        )

    def tombstone_object(
        self,
        owner_id: str,
        object_id: str,
        reconciliation_job_id: str,
        reason_code: str,
        created_at_utc: str,
    ) -> TombstoneRecord:
        owner_id = require_opaque_id(owner_id)
        object_id = require_opaque_id(object_id)
        reconciliation_job_id = require_opaque_id(reconciliation_job_id)
        reason_code = _code(reason_code)
        created_at_utc = require_utc(created_at_utc)
        with self._database.transaction():
            current = self._object_row(object_id)
            if current is None:
                raise RepositoryError("not_found")
            if str(current["owner_id"]) != owner_id:
                raise RepositoryError("owner_forbidden")
            existing = self._database.fetch_one(
                "SELECT tombstone_id, owner_id, entity_kind, entity_id, reason_code, "
                "metadata_json, "
                "created_at_utc FROM tombstones WHERE owner_id = ? AND entity_kind = "
                "'remote_object' "
                "AND entity_id = ?",
                (owner_id, object_id),
```

- [ ] **Step C8I.2: Append `remote_repo.py` continuation slice 2**

Append exactly to `backend/src/projectb/infrastructure/repositories/remote_repo.py`:

```python
            )
            if existing is not None:
                record = self._tombstone(existing)
                metadata = parse_json_object(record.metadata_json)
                if (
                    record.reason_code != reason_code
                    or record.created_at_utc != created_at_utc
                    or metadata
                    != {
                        "reconciliation_job_id": reconciliation_job_id,
                        "status": "deleted",
                    }
                ):
                    raise RepositoryError("state_inconsistent")
                return record
            if str(current["state"]) != "delete_requested":
                raise RepositoryError("state_inconsistent")
            active = self._active_object(current)
            job_row = self._job_row(reconciliation_job_id)
            if job_row is None:
                raise RepositoryError("state_inconsistent")
            if str(job_row["owner_id"]) != owner_id:
                raise RepositoryError("owner_forbidden")
            reconciliation = self._active_job(job_row)
            evidence = parse_json_object(reconciliation.payload_json)
            if (
                reconciliation.course_id != active.course_id
                or reconciliation.object_id != object_id
                or reconciliation.state != "succeeded"
                or set(evidence)
                != {
                    "job_kind",
                    "object_version",
                    "observed_at_utc",
                    "reconciliation_result",
                }
                or evidence.get("job_kind") != "remote_delete"
                or type(evidence.get("object_version")) is not int
```

- [ ] **Step C8I.3: Append `remote_repo.py` continuation slice 3**

Append exactly to `backend/src/projectb/infrastructure/repositories/remote_repo.py`:

```python
                or evidence.get("object_version") != active.version
                or evidence.get("reconciliation_result")
                not in {"provider_deleted", "provider_expired"}
            ):
                raise RepositoryError("state_inconsistent")
            observed_at_utc = require_utc(evidence.get("observed_at_utc"))
            if observed_at_utc > created_at_utc or reason_code != evidence.get(
                "reconciliation_result"
            ):
                raise RepositoryError("state_inconsistent")
            next_version = active.version + 1
            self._database.execute(
                "INSERT INTO remote_object_versions(object_id, owner_id, course_id, version, "
                "state, "
                "config_fingerprint, payload_json, created_at_utc) VALUES (?, ?, ?, ?, "
                "'deleted', "
                "?, ?, ?)",
                (
                    object_id,
                    owner_id,
                    str(active.course_id),
                    next_version,
                    active.config_fingerprint,
                    canonical_json(
                        {
                            "reason_code": reason_code,
                            "reconciliation_job_id": reconciliation_job_id,
                        }
                    ),
                    created_at_utc,
                ),
            )
            cursor = self._database.execute(
                "UPDATE remote_objects SET state = 'deleted', active_version = ?, scope_token = "
                "NULL, "
                "provider_ref = NULL, tombstoned_at_utc = ?, updated_at_utc = ? "
                "WHERE object_id = ? AND owner_id = ? AND active_version = ?",
                (
```

- [ ] **Step C8I.4: Append `remote_repo.py` continuation slice 4**

Append exactly to `backend/src/projectb/infrastructure/repositories/remote_repo.py`:

```python
                    next_version,
                    created_at_utc,
                    created_at_utc,
                    object_id,
                    owner_id,
                    active.version,
                ),
            )
            if cursor.rowcount != 1:
                raise RepositoryError("state_inconsistent")
            self._database.execute(
                "INSERT INTO tombstones(tombstone_id, owner_id, entity_kind, entity_id, "
                "reason_code, "
                "metadata_json, created_at_utc) VALUES (?, ?, 'remote_object', ?, ?, ?, ?)",
                (
                    f"remote_object:{object_id}",
                    owner_id,
                    object_id,
                    reason_code,
                    canonical_json(
                        {
                            "reconciliation_job_id": reconciliation_job_id,
                            "status": "deleted",
                        }
                    ),
                    created_at_utc,
                ),
            )
            row = self._database.fetch_one(
                "SELECT tombstone_id, owner_id, entity_kind, entity_id, reason_code, "
                "metadata_json, "
                "created_at_utc FROM tombstones WHERE owner_id = ? AND entity_kind = "
                "'remote_object' "
                "AND entity_id = ?",
                (owner_id, object_id),
            )
            if row is None:
                raise RepositoryError("state_inconsistent")
            return self._tombstone(row)

```

- [ ] **Step C8I.5: Append `get_tombstone`**

Append exactly to `backend/src/projectb/infrastructure/repositories/remote_repo.py`:

```python
    def get_tombstone(self, owner_id: str, object_id: str) -> TombstoneRecord:
        owner_id = require_opaque_id(owner_id)
        object_id = require_opaque_id(object_id)
        current = self._object_row(object_id)
        if current is None:
            raise RepositoryError("not_found")
        if str(current["owner_id"]) != owner_id:
            raise RepositoryError("owner_forbidden")
        row = self._database.fetch_one(
            "SELECT tombstone_id, owner_id, entity_kind, entity_id, reason_code, metadata_json, "
            "created_at_utc FROM tombstones WHERE owner_id = ? AND entity_kind = "
            "'remote_object' "
            "AND entity_id = ?",
            (owner_id, object_id),
        )
        if row is None:
            raise RepositoryError("not_found")
        return self._tombstone(row)


```

- [ ] **Step C8J: Append bounded audit persistence and module exports**

Append exactly to `backend/src/projectb/infrastructure/repositories/remote_repo.py`:

```python
class AuditRepository:
    def __init__(self, database: Database) -> None:
        self._database = database

    @staticmethod
    def _event(row: sqlite3.Row) -> AuditEvent:
        return AuditEvent(
            event_id=str(row["event_id"]),
            owner_id=str(row["owner_id"]),
            event_kind=str(row["event_kind"]),
            subject_id=str(row["subject_id"]),
            outcome_code=str(row["outcome_code"]),
            metadata_json=str(row["metadata_json"]),
            occurred_at_utc=str(row["occurred_at_utc"]),
        )

    def record(
        self,
        owner_id: str,
        event_id: str,
        event_kind: str,
        subject_id: str,
        outcome_code: str,
        metadata: Mapping[str, object],
        occurred_at_utc: str,
```

- [ ] **Step C8J.2: Append `remote_repo.py` continuation slice 2**

Append exactly to `backend/src/projectb/infrastructure/repositories/remote_repo.py`:

```python
    ) -> AuditEvent:
        owner_id = require_opaque_id(owner_id)
        event_id = require_opaque_id(event_id)
        event_kind = _text(event_kind)
        if event_kind not in _AUDIT_EVENT_KINDS:
            raise RepositoryError("state_inconsistent")
        subject_id = _code(subject_id)
        outcome_code = _text(outcome_code)
        if outcome_code not in _AUDIT_OUTCOMES:
            raise RepositoryError("state_inconsistent")
        metadata_json = _audit_metadata_json(metadata)
        occurred_at_utc = require_utc(occurred_at_utc)
        proposed = AuditEvent(
            event_id,
            owner_id,
            event_kind,
            subject_id,
            outcome_code,
            metadata_json,
            occurred_at_utc,
        )
        try:
            with self._database.transaction():
                existing = self._database.fetch_one(
                    "SELECT event_id, owner_id, event_kind, subject_id, outcome_code, "
                    "metadata_json, "
                    "occurred_at_utc FROM audit_events WHERE event_id = ?",
                    (event_id,),
                )
                if existing is not None:
                    if str(existing["owner_id"]) != owner_id:
                        raise RepositoryError("owner_forbidden")
                    record = self._event(existing)
                    if record != proposed:
                        raise RepositoryError("state_inconsistent")
                    return record
                self._database.execute(
                    "INSERT INTO audit_events(event_id, owner_id, event_kind, subject_id, "
```

- [ ] **Step C8J.3: Append `list_for_owner`**

Append exactly to `backend/src/projectb/infrastructure/repositories/remote_repo.py`:

```python
                    "outcome_code, "
                    "metadata_json, occurred_at_utc) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (
                        event_id,
                        owner_id,
                        event_kind,
                        subject_id,
                        outcome_code,
                        metadata_json,
                        occurred_at_utc,
                    ),
                )
                return proposed
        except RepositoryError:
            raise
        except sqlite3.IntegrityError as error:
            raise RepositoryError("state_inconsistent") from error

    def list_for_owner(self, owner_id: str) -> tuple[AuditEvent, ...]:
        owner_id = require_opaque_id(owner_id)
        rows = self._database.fetch_all(
            "SELECT event_id, owner_id, event_kind, subject_id, outcome_code, metadata_json, "
            "occurred_at_utc FROM audit_events WHERE owner_id = ? ORDER BY occurred_at_utc, "
            "event_id",
            (owner_id,),
        )
        return tuple(self._event(row) for row in rows)


__all__ = [
    "AuditEvent",
    "AuditRepository",
    "ConsentRecord",
    "RemoteJobRecord",
    "RemoteJobVersion",
    "RemoteObjectRecord",
    "RemoteObjectVersion",
    "RemoteRepository",
    "TombstoneRecord",
]
```

The implementation deliberately does not import an SDK, make network calls, encrypt data itself, or interpret a protected reference. X2 and later provider lifecycle units own adapter calls and protected-reference storage; this repository only enforces that raw provider IDs cannot enter canonical payload/history/audit/tombstone fields.

- [ ] **Step C9: Run the focused T-03C tests green**

Run:

```powershell
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    '-m', 'pytest', '-c', 'backend/pyproject.toml',
    'backend/tests/integration/test_learning_remote_repositories.py', '-q'
)
```

Expected: exit code 0. Record the observed test count and duration. The evidence must include exact evidence validation/idempotency, gap-free plan revisions, consent revocation, object/job versioning, transition rejection, provider-reference cleanup, non-reconstructive history, whitelist audit, owner isolation, and restart behavior.

- [ ] **Step C10: Format the exact T-03C Python set and rerun focused tests**

Run:

```powershell
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    '-m', 'ruff', 'format', '--config', 'backend/pyproject.toml',
    'backend/src/projectb/infrastructure/repositories/learning_repo.py',
    'backend/src/projectb/infrastructure/repositories/remote_repo.py',
    'backend/tests/integration/test_learning_remote_repositories.py'
)
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    '-m', 'pytest', '-c', 'backend/pyproject.toml',
    'backend/tests/integration/test_learning_remote_repositories.py', '-q'
)
```

Expected: both independently checked commands exit 0. Formatting changes no public name, state set, transition, SQL statement, ownership path, or security behavior.

- [ ] **Step C11: Run schema, repository, integration, and canonical full regression**

Run:

```powershell
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    '-m', 'pytest', '-c', 'backend/pyproject.toml',
    'backend/tests/integration/test_learning_remote_repositories.py',
    'backend/tests/integration/test_course_material_repositories.py',
    'backend/tests/integration/test_sqlite_schema.py', '-q'
)
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    '-m', 'pytest', '-c', 'backend/pyproject.toml', 'backend/tests/integration', '-q'
)
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @('scripts/test_all.py')
```

Expected: each command independently exits 0. Earlier schema/course/material assertions remain unchanged and green; the full runner is the reviewed T-01F3 canonical entry. Record actual counts and durations rather than copying a planned count.

- [ ] **Step C12: Run configured static gates and prove migration/database-wrapper bytes are untouched**

Run:

```powershell
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    '-m', 'ruff', 'format', '--check', '--config', 'backend/pyproject.toml',
    'backend/src/projectb/infrastructure/repositories/learning_repo.py',
    'backend/src/projectb/infrastructure/repositories/remote_repo.py',
    'backend/tests/integration/test_learning_remote_repositories.py'
)
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    '-m', 'ruff', 'check', '--config', 'backend/pyproject.toml',
    '--extend-select', 'I,E501',
    'backend/src/projectb/infrastructure/repositories/learning_repo.py',
    'backend/src/projectb/infrastructure/repositories/remote_repo.py',
    'backend/tests/integration/test_learning_remote_repositories.py'
)
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    '-m', 'mypy', '--config-file', 'backend/pyproject.toml', '--warn-redundant-casts',
    'backend/src/projectb/infrastructure/repositories/learning_repo.py',
    'backend/src/projectb/infrastructure/repositories/remote_repo.py'
)
Invoke-CheckedNative -FilePath $GitExe -ArgumentList @('diff', '--check')
Invoke-CheckedNative -FilePath $GitExe -ArgumentList @('diff', '--stat')
$forbiddenDiff = @(Invoke-CheckedNative -FilePath $GitExe -ArgumentList @(
    'diff', '--',
    'backend/src/projectb/infrastructure/sqlite.py',
    'backend/src/projectb/infrastructure/migrations/001_initial.sql',
    'backend/src/projectb/infrastructure/repositories/course_repo.py',
    'backend/src/projectb/infrastructure/repositories/material_repo.py'
))
if ($forbiddenDiff.Count -ne 0) { throw 'T-03C changed a predecessor-owned path' }
```

Expected: Ruff/mypy/diff checks exit 0, the stat names only the three T-03C paths, and the captured forbidden diff is empty. Any schema deficiency is reported to the coordinator rather than repaired in this unit.

- [ ] **Step C13: Stage exactly the T-03C ownership set and inspect the whole index**

Run:

```powershell
Invoke-CheckedNative -FilePath $GitExe -ArgumentList @(
    'add', '--',
    'backend/src/projectb/infrastructure/repositories/learning_repo.py',
    'backend/src/projectb/infrastructure/repositories/remote_repo.py',
    'backend/tests/integration/test_learning_remote_repositories.py'
)
Assert-ExactStagedPaths -ExpectedPaths @(
    'backend/src/projectb/infrastructure/repositories/learning_repo.py'
    'backend/src/projectb/infrastructure/repositories/remote_repo.py'
    'backend/tests/integration/test_learning_remote_repositories.py'
)
Invoke-CheckedNative -FilePath $GitExe -ArgumentList @('diff', '--cached', '--check')
$reviewTree = @(Invoke-CheckedNative -FilePath $GitExe -ArgumentList @('write-tree'))
if ($reviewTree.Count -ne 1 -or $reviewTree[0] -notmatch '^[0-9a-f]{40}$') {
    throw 'T-03C review tree must be one lowercase 40-hex line'
}
$env:PROJECTB_REVIEW_TREE = $reviewTree[0]
$expectedReviewPaths = @(
    'backend/src/projectb/infrastructure/repositories/learning_repo.py'
    'backend/src/projectb/infrastructure/repositories/remote_repo.py'
    'backend/tests/integration/test_learning_remote_repositories.py'
)
foreach ($name in @('PROJECTB_ROOT_PLAN_SHA256', 'PROJECTB_DETAILED_PLAN_SHA256')) {
    $value = [Environment]::GetEnvironmentVariable($name)
    if ($value -notmatch '^[0-9A-Fa-f]{64}$') { throw "$name must be one 64-hex hash" }
}
$rootPlanSha = (Get-FileHash -Algorithm SHA256 -LiteralPath 'PLAN.md').Hash.ToLowerInvariant()
$detailedPlanPath = 'docs/superpowers/plans/2026-07-23-persistence-repositories.md'
$detailedPlanSha = (
    Get-FileHash -Algorithm SHA256 -LiteralPath $detailedPlanPath
).Hash.ToLowerInvariant()
if ($rootPlanSha -ne $env:PROJECTB_ROOT_PLAN_SHA256.ToLowerInvariant() -or
    $detailedPlanSha -ne $env:PROJECTB_DETAILED_PLAN_SHA256.ToLowerInvariant()) {
    throw 'review packet plan hash mismatch'
}
```

- [ ] **Step C13.2: Build the exact staged-content review packet**

Continue in the same checked PowerShell session:

```powershell
$blobRows = foreach ($path in ($expectedReviewPaths | Sort-Object)) {
    $stage = @(Invoke-CheckedNative -FilePath $GitExe -ArgumentList @(
        'ls-files', '--stage', '--', $path
    ))
    if ($stage.Count -ne 1) { throw 'review packet requires one stage-zero blob per path' }
    $match = [regex]::Match(
        $stage[0], '^(?<mode>100644|100755) (?<blob>[0-9a-f]{40}) 0\t(?<path>.+)$'
    )
    if (-not $match.Success -or
        ($match.Groups['path'].Value -replace '\\', '/') -ne $path) {
        throw 'review packet staged blob row is malformed'
    }
    "blob=$path|$($match.Groups['mode'].Value)|$($match.Groups['blob'].Value)"
}
$script:ProjectBReviewPacket = @(
    "root-plan-sha256=$rootPlanSha"
    "detailed-plan-sha256=$detailedPlanSha"
    "base-commit=$($env:PROJECTB_BASE_COMMIT)"
    "review-tree=$($env:PROJECTB_REVIEW_TREE)"
) + $blobRows
$packetBytes = [Text.Encoding]::UTF8.GetBytes(
    (($script:ProjectBReviewPacket -join "`n") + "`n")
)
$sha256 = [Security.Cryptography.SHA256]::Create()
try {
    $env:PROJECTB_REVIEW_PACKET_SHA256 = -join (
        $sha256.ComputeHash($packetBytes) | ForEach-Object { $_.ToString('x2') }
    )
} finally {
    $sha256.Dispose()
}
```

Expected: all operations independently exit 0. `Assert-ExactStagedPaths` reads the entire index without a pathspec, rejects duplicate output, and proves exactly three paths with no extra staged secret, ledger, migration, generated, or unrelated file.

- [ ] **Step C14: Run the committed scanner against the exact staged T-03C patch**

Run:

```powershell
Invoke-CheckedNative -FilePath $PowerShellExe -ArgumentList @(
    '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File',
    'scripts/scan_secrets.ps1', '-PythonExe', $PythonExe, '--staged'
)
```

Expected: checked exit code 0 with no raw suspected value in output. Any suspected credential, private course content, local path, answer, raw provider ID/reference, or secret-shaped payload blocks the unit and is reported without reproducing the value.

- [ ] **Step C15: Request the fresh T-03C SPEC review**

The coordinator gives a fresh non-worker reviewer the confirmed SPEC LearningEvidence v1, protected Attempt boundary, plan revision semantics, X1/X2 consent/remote/deletion boundary, exactly AC-06, AC-07, AC-17, AC-25, AC-26, AC-27, AC-28, AC-29, AC-30, AC-31, AC-35, AC-40, and AC-50, root T-03/T-03C, this plan, predecessor SHA, exact staged diff, every canonical line in `$script:ProjectBReviewPacket`, checked `PROJECTB_REVIEW_PACKET_SHA256` and `PROJECTB_REVIEW_TREE`, and observed red/green/regression/static/scanner evidence. The PASS record names that exact packet hash and tree. Record `PROJECTB_SPEC_REVIEWER_ID`, `PROJECTB_SPEC_REVIEW_TREE`, and `PROJECTB_SPEC_REVIEW_PACKET_SHA256`.

Expected: findings-first review followed by `SPEC REVIEW: PASS` only after all Critical and Important findings are resolved. The reviewer checks that T-03C persists but does not invent learning authority, consent revocation is append-only, remote states cannot bypass consent, deleted current references are cleared, history/tombstones are non-reconstructive, and audit is whitelist-only.

- [ ] **Step C16: Request the different fresh T-03C quality/security/license review**

Give the same canonical packet lines, packet SHA-256, exact staged diff, and checked tree to a different fresh reviewer and record `PROJECTB_QUALITY_REVIEWER_ID`, `PROJECTB_QUALITY_REVIEW_TREE`, and `PROJECTB_QUALITY_REVIEW_PACKET_SHA256`. The PASS record names that packet hash and tree. The reviewer checks exact field validation, unhashable/untrusted-type failures, stable exceptions, optimistic version/idempotency behavior, irreversible consent-token invalidation, provider deletion evidence reconciliation, transition maps, rollback ordering, index use, cross-owner reads, append-only triggers, protected-reference isolation, restart behavior, path ownership, tests, and dependency/license impact.

Expected: findings-first review followed by `QUALITY REVIEW: PASS` with no unresolved Critical or Important issue. A finding returns to a new failing test and repeats Steps C9-C16; reviewers do not edit worker files.

- [ ] **Step C17: Validate all three T-03C identities**

Run:

```powershell
$identities = @(
    $env:PROJECTB_AGENT_ID
    $env:PROJECTB_SPEC_REVIEWER_ID
    $env:PROJECTB_QUALITY_REVIEWER_ID
)
foreach ($identity in $identities) {
    if ([string]::IsNullOrWhiteSpace($identity) -or
        $identity -notmatch '^[A-Za-z0-9][A-Za-z0-9._-]{1,63}$') {
        throw 'invalid T-03C worker/reviewer identity'
    }
}
if (($identities | Sort-Object -Unique).Count -ne 3) {
    throw 'T-03C worker and reviewers must be pairwise distinct'
}
foreach ($tree in @(
    $env:PROJECTB_REVIEW_TREE
    $env:PROJECTB_SPEC_REVIEW_TREE
    $env:PROJECTB_QUALITY_REVIEW_TREE
)) {
    if ($tree -notmatch '^[0-9a-f]{40}$' -or $tree -ne $env:PROJECTB_REVIEW_TREE) {
        throw 'T-03C reviews must bind to the exact staged tree'
    }
}
foreach ($packetSha in @(
    $env:PROJECTB_REVIEW_PACKET_SHA256
    $env:PROJECTB_SPEC_REVIEW_PACKET_SHA256
    $env:PROJECTB_QUALITY_REVIEW_PACKET_SHA256
)) {
    if ($packetSha -notmatch '^[0-9a-f]{64}$' -or
        $packetSha -ne $env:PROJECTB_REVIEW_PACKET_SHA256) {
        throw 'T-03C reviews must bind to the exact cached-content packet'
    }
}
```

Expected: exit code 0 with three valid, non-empty, pairwise-distinct canonical identities.

- [ ] **Step C18: Recheck the exact staged bytes after all review-driven edits**

Run:

```powershell
Assert-ExactStagedPaths -ExpectedPaths @(
    'backend/src/projectb/infrastructure/repositories/learning_repo.py'
    'backend/src/projectb/infrastructure/repositories/remote_repo.py'
    'backend/tests/integration/test_learning_remote_repositories.py'
)
Invoke-CheckedNative -FilePath $GitExe -ArgumentList @('diff', '--cached', '--check')
Invoke-CheckedNative -FilePath $PowerShellExe -ArgumentList @(
    '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File',
    'scripts/scan_secrets.ps1', '-PythonExe', $PythonExe, '--staged'
)
$currentTree = @(Invoke-CheckedNative -FilePath $GitExe -ArgumentList @('write-tree'))
if ($currentTree.Count -ne 1 -or $currentTree[0] -ne $env:PROJECTB_REVIEW_TREE) {
    throw 'T-03C staged tree changed after review'
}
```

Expected: every operation independently exits 0; the staged tree and whole-index path set are exactly those named by both reviewers. Any edit returns to Step C13, recaptures/scans the tree, and repeats both reviews.

- [ ] **Step C19: Commit only the reviewed T-03C unit**

Run:

```powershell
Invoke-CheckedNative -FilePath $GitExe -ArgumentList @(
    'commit', '-m',
    "feat(T-03C): add learning and remote repositories [agent: $env:PROJECTB_AGENT_ID]"
)
```

Expected: checked exit code 0 with a `feat(T-03C)` subject containing the validated worker identity. A rejected commit is terminal for this step; no later command may mask it.

- [ ] **Step C20: Capture and validate the terminal T-03C commit hash**

Run:

```powershell
$commitHash = @(Invoke-CheckedNative -FilePath $GitExe -ArgumentList @('rev-parse', 'HEAD'))
if ($commitHash.Count -ne 1 -or $commitHash[0] -notmatch '^[0-9a-f]{40}$') {
    throw 'T-03C commit hash must be one lowercase 40-hex line'
}
$committedTree = @(
    Invoke-CheckedNative -FilePath $GitExe -ArgumentList @('rev-parse', 'HEAD^{tree}')
)
if ($committedTree.Count -ne 1 -or $committedTree[0] -ne $env:PROJECTB_REVIEW_TREE) {
    throw 'T-03C committed tree differs from the reviewed tree'
}
$commitHash[0]
```

Expected: checked `rev-parse` success and exactly one lowercase 40-hex result. The coordinator records the hash, evidence, reviewer identities, and handoffs in root `PLAN.md` and `AGENT_LOG.md`; the worker does not edit those shared ledgers.

**T-03C completion standard:** The exact three-path unit has observed red and green evidence, focused/prerequisite/integration/full regression, configured Ruff/mypy, whole-index staging, staged scanner, two fresh PASS reviews, and one validated commit hash. Learning/plan/remote/audit histories reopen after restart, owner-forbidden access is stable, consent and version rows remain append-only, and final remote deletion leaves no usable protected reference or scope token in current state, history, audit, or tombstone metadata.

---

## Coordinator-Only P01 Closure

After T-03C is reviewed and committed, the coordinator, not a worker, verifies that the observed predecessor chain is `T-02C -> T-03A -> T-03B -> T-03C`, that each child commit contains only its literal three-path ownership set, and that no migration modification appears after T-03A. The coordinator then updates only the authoritative root ledger/process records in its own owned checkpoint; this plan does not prescribe or preclaim those edits.

The terminal handoffs are:

| Reviewed producer | Consumer | Stable handoff |
| --- | --- | --- |
| T-03A | T-08 and all repository units | `Database`, stable repository errors, canonical JSON, complete initial schema, durable-job reservation |
| T-03B | M1-02B/M1-02C/M1-04 | Course/material active and append-only history, duplicate content-hash/role identity |
| T-03C | T-04A/T-04C, T-05A, T-06, M1/M2/M3, X2 | Owner-scoped evidence/plan/consent/remote/job/audit/tombstone persistence |

No handoff permits a consumer to weaken stable error codes, persist a path/body/answer/secret/raw provider ID, rewrite append-only history, reuse revoked consent, or edit `001_initial.sql` without a new coordinator-approved migration dispatch.
