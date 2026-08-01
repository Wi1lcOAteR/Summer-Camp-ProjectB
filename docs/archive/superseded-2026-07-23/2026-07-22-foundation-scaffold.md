# Reproducible Foundation and Canonical Test Runner Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the reproducible ProjectB foundation as ten independently reviewed and committed units with disjoint ownership: locked toolchain, backend health scaffold, frontend manifest/lock contracts, minimal React app, fail-closed staged scanner, absolute executable resolution, exact runtime/frontend/config/raw-lock contracts, gate model/execution, formal registries, and the canonical CLI.

**Architecture:** Ten short-lived worktrees own disjoint paths. T-01A establishes the only dependency/runtime baseline; T-01B, T-01C1, and T-01D branch from that reviewed commit and may run in parallel; T-01C2 follows C1; T-01E1 consumes A+C1; T-01E2 consumes E1+C1; T-01F1 consumes B+C2+D+E1+E2; T-01F2 follows F1; T-01F3 follows F2 and supplies `scripts/test_all.py`. Raw-byte locks, strict text decoding, exact executable resolution, immutable frontend configuration contracts, and three-state owner gates are separated into deterministic helpers with focused tests.

**Tech Stack:** CPython 3.14.6, FastAPI 0.139.2, Pydantic 2.13.4, pytest 9.1.1, Ruff 0.15.22, mypy 2.3.0, Node.js 24.18.0, npm 11.16.0, React/React DOM 19.2.7, Vite 8.1.5, TypeScript 7.0.2, Vitest 4.1.10, Node built-in test runner, and Windows PowerShell 5.1 or PowerShell 7.

---

## Status And Dispatch Boundary

This is the formal implementation plan for root task T-01, identified by its stable `### Task Group T-01 (not dispatchable)` heading and child IDs in the full root `PLAN.md`. It supersedes the frozen failed fragment as execution guidance, but it does not edit that fragment and does not authorize implementation by itself. No code, test, build, scan, review, or commit described below is claimed as executed.

Dispatch remains forbidden until G-01 is PASS, G-02A is PASS, G-03 cold-start validation has completed, the student has explicitly approved implementation, and G-04 has created the relevant worktree. Each unit uses a fresh worker and two different fresh reviewers. A unit is integrated only after its focused/full verification, scanner, SPEC review, quality review, exact staged-path check, and commit all have current evidence.

## Dependency And Integration Order

```text
T-01A
  +--> T-01B --------------------------+
  +--> T-01C1 --> T-01C2 --------------+
  +--> T-01D --------------------------+--> T-01F1 --> T-01F2 --> T-01F3
             \--> T-01E1 --> T-01E2 ---+
```

- T-01B, T-01C1, and T-01D branch from the reviewed T-01A commit and may run concurrently because their files do not overlap.
- T-01C2 branches only from reviewed T-01C1 and owns exactly the four React application paths; it never edits `frontend/package.json` or any C1 path.
- T-01E1 branches from reviewed T-01A and T-01C1; T-01E2 follows both reviewed E1 and C1.
- T-01F1 branches only after reviewed T-01B, T-01C2, T-01D, T-01E1, and T-01E2 commits are integrated. F2 and F3 are strictly sequenced package facade/CLI layers.
- The coordinator records each unit commit/reviews in `PLAN.md` and `AGENT_LOG.md`; workers never edit those shared ledgers from feature worktrees.

## Exact Path Ownership Map

| Unit | Exact owned paths | Count |
| --- | --- | ---: |
| T-01A | `.gitignore`; `backend/pyproject.toml`; `backend/requirements-windows-x64.lock`; `backend/tests/unit/test_toolchain_contract.py` | 4 |
| T-01B | `backend/src/projectb/__init__.py`; `backend/src/projectb/api/__init__.py`; `backend/src/projectb/api/app.py`; `backend/tests/unit/test_health.py` | 4 |
| T-01C1 | `frontend/package.json`; `frontend/.npmrc`; `frontend/tsconfig.json`; `frontend/vitest.contract.json`; `frontend/vite.config.contract.json`; `frontend/vite.config.ts`; `frontend/package-lock.json`; `scripts/frontend_lock_contract.mjs`; `scripts/materialize_frontend_lock.mjs`; `scripts/tests/frontend_contract.test.mjs`; `scripts/tests/frontend_lock_contract.test.mjs` | 11 |
| T-01C2 | `frontend/index.html`; `frontend/src/main.tsx`; `frontend/src/app/App.tsx`; `frontend/src/app/App.test.tsx` | 4 |
| T-01D | `scripts/secret_scan/__init__.py`; `scripts/secret_scan/encoding.py`; `scripts/secret_scan/paths.py`; `scripts/secret_scan/rules.py`; `scripts/scan_secrets.py`; `scripts/scan_secrets.ps1`; `backend/tests/unit/test_secret_scanner.py` | 7 |
| T-01E1 | `scripts/projectb_test_runner/__init__.py`; `scripts/projectb_test_runner/executables.py`; `backend/tests/unit/test_runner_executables.py` | 3 |
| T-01E2 | `scripts/projectb_test_runner/contracts.py`; `scripts/projectb_test_runner/locks.py`; `scripts/projectb_test_runner/runtime.py`; `backend/tests/unit/test_runner_contracts.py`; `backend/tests/unit/test_runner_locks.py`; `backend/tests/unit/test_runner_runtime.py` | 6 |
| T-01F1 | `scripts/projectb_test_runner/gate_model.py`; `scripts/projectb_test_runner/gate_run.py`; `backend/tests/unit/test_runner_gates.py` | 3 |
| T-01F2 | `scripts/projectb_test_runner/core_registry.py`; `scripts/projectb_test_runner/deferred_registry.py`; `scripts/projectb_test_runner/registry.py`; `backend/tests/unit/test_runner_registry.py` | 4 |
| T-01F3 | `scripts/projectb_test_runner/runner.py`; `scripts/test_all.py`; `backend/tests/unit/test_runner_cli.py` | 3 |

The ten stage sets are pairwise disjoint and their union is exactly these 49 paths. Package facades are sequenced by dependency and are not edited by another unit.

## Review And Identity Rule For Every Unit

For each unit, the worker sets `PROJECTB_AGENT_ID` to the literal runtime identity assigned by the coordinator. The SPEC reviewer and quality reviewer are fresh sessions, differ from the worker and each other, and set the unit-specific review variables named in that task. Reviewers receive `SPEC.md`, the full root `PLAN.md` with the stable T-01 heading and explicit task ID, this plan, the base commit ID, the exact owned-path diff, and the focused/full output. They extract the root task by heading/ID, never by line number, and never use the frozen fragment as a substitute.

Any Critical or Important finding is resolved through a new failing focused test, an observed red run for the expected reason, the minimum fix, a green focused run, and the task's full reverify command. The original reviewer verifies its findings. A task does not stage or commit while either review has an unresolved Critical or Important issue.

## Required Fail-Closed Command Prelude

G-02A commit `22b516af7b6f4896c6127e75b2585435e407a3c0` owns dependency, license, and lock evidence only. It does **not** own host executable identities, and this plan must not add a worker-owned runtime manifest to G-02A. The immutable G-02A tree is `48419151b360619f14d141c062d34bee0719a638`; the reviewed baseline and two source locks have blob IDs `da7362a0d09a1318ae20bf767b648ecf34e76475`, `1078db073060e01051bebd1f2250ab55b0cec3d2`, and `c2c53ae64a720b84eb7ee7c56483070bcfa2cdb8`. Every unit proves those paths exist in that exact evidence tree and that its base commit carries the same blobs. A mutable base-commit path can never substitute for the G-02A tree.

The root plan exports exactly four executable paths: `PROJECTB_PYTHON_EXE`, `PROJECTB_NODE_EXE`, `PROJECTB_NPM_CMD`, and `PROJECTB_POWERSHELL_EXE`. Cryptographic executable provenance belongs to G-04, not G-02A or a T-01 worker. Before this detailed plan can receive cross-plan PASS or dispatch any unit, the coordinator must atomically amend root G-04 and `docs/engineering/WORKTREE_MAP.md` so each unit row contains four coordinator-owned runtime attestations, one each for Python, Node, npm, and PowerShell, with exact `path`, lowercase `sha256`, exact `version`, and `provenance` fields; the G-04 validator must compare every row to the four exported paths and revalidate each leaf before dispatch. Until that root amendment is reviewed, this plan remains **BLOCKED FOR CROSS-PLAN PASS**. The prelude below still checks path shape, leaf name, reparse components, captures a per-run hash for drift detection, and enforces exact versions, but it does not misrepresent those observations as coordinator provenance.

Git is a coordinator control-plane dependency rather than a fifth application runtime. The prelude resolves the current shell's `git.exe` application once, validates that absolute leaf and its path components, captures its hash for same-run drift detection, and thereafter invokes only the resolved absolute path. No T-01 file records or approves a Git runtime identity. A missing variable, non-fully-qualified runtime path, wrong leaf name, reparse component, same-run hash drift, version mismatch, timeout, or non-allowed exit code aborts the unit. No unit chains native commands behind one final exit check or uses a bare Python, Node, npm, PowerShell, or Git invocation after resolution.

```powershell
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$WorktreeRoot = $env:PROJECTB_WORKTREE_ROOT
$BaseCommit = $env:PROJECTB_BASE_COMMIT
$G02aEvidenceCommit = "22b516af7b6f4896c6127e75b2585435e407a3c0"
$G02aEvidenceTree = "48419151b360619f14d141c062d34bee0719a638"
$G02aEvidenceFiles = @(
    @("docs/engineering/DEPENDENCY_BASELINE.md", "da7362a0d09a1318ae20bf767b648ecf34e76475"),
    @("docs/engineering/locks/python-3.14.6-windows-x64.lock", "1078db073060e01051bebd1f2250ab55b0cec3d2"),
    @("docs/engineering/locks/frontend-package-lock.json", "c2c53ae64a720b84eb7ee7c56483070bcfa2cdb8")
)
$PythonExe = $env:PROJECTB_PYTHON_EXE
$NodeExe = $env:PROJECTB_NODE_EXE
$NpmCmd = $env:PROJECTB_NPM_CMD
$PowerShellExe = $env:PROJECTB_POWERSHELL_EXE

if ([string]::IsNullOrWhiteSpace($WorktreeRoot) -or
    [string]::IsNullOrWhiteSpace($BaseCommit) -or
    [string]::IsNullOrWhiteSpace($PythonExe) -or
    [string]::IsNullOrWhiteSpace($NodeExe) -or
    [string]::IsNullOrWhiteSpace($NpmCmd) -or
    [string]::IsNullOrWhiteSpace($PowerShellExe)) {
    throw "coordinator worktree/base metadata and four runtime paths are required"
}
$WorktreeRoot = (Resolve-Path -LiteralPath $WorktreeRoot -ErrorAction Stop).Path

function Test-FullyQualifiedPath {
    param([Parameter(Mandatory)][string]$Path)
    return [IO.Path]::IsPathRooted($Path) -and
        $Path -notmatch "^[A-Za-z]:[^\\/]" -and
        $Path -notmatch "(^|[\\/])\.\.([\\/]|$)"
}

function Assert-LowerHex {
    param([Parameter(Mandatory)][string]$Value, [Parameter(Mandatory)][int]$Length, [Parameter(Mandatory)][string]$Name)
    if ($Value -notmatch "^[0-9a-f]{$Length}$") { throw "$Name must be lowercase hex of length $Length" }
}

function Assert-NoReparseComponents {
    param([Parameter(Mandatory)][string]$Path, [Parameter(Mandatory)][string]$Label)
    $current = [IO.Path]::GetPathRoot($Path)
    foreach ($part in $Path.Substring($current.Length).Split(@("\", "/"), [StringSplitOptions]::RemoveEmptyEntries)) {
        $current = Join-Path $current $part
        $item = Get-Item -LiteralPath $current -Force -ErrorAction Stop
        if (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
            throw "$Label executable path contains a reparse component"
        }
    }
}

Assert-LowerHex -Value $BaseCommit -Length 40 -Name "PROJECTB_BASE_COMMIT"
Assert-LowerHex -Value $G02aEvidenceCommit -Length 40 -Name "fixed G-02A evidence commit"
Assert-LowerHex -Value $G02aEvidenceTree -Length 40 -Name "fixed G-02A evidence tree"

$runtimeContracts = @(
    @("Python", $PythonExe, @("python.exe")),
    @("Node", $NodeExe, @("node.exe")),
    @("Npm", $NpmCmd, @("npm.cmd")),
    @("PowerShell", $PowerShellExe, @("pwsh.exe", "powershell.exe"))
)
$runtimeObservations = @{}
foreach ($contract in $runtimeContracts) {
    $label = [string]$contract[0]
    $path = [string]$contract[1]
    $allowedNames = @($contract[2])
    if (!(Test-FullyQualifiedPath -Path $path) -or
        !(Test-Path -LiteralPath $path -PathType Leaf) -or
        [IO.Path]::GetFileName($path).ToLowerInvariant() -notin @(
            $allowedNames | ForEach-Object { $_.ToLowerInvariant() }
        )) {
        throw "$label executable path/leaf is invalid"
    }
    Assert-NoReparseComponents -Path $path -Label $label
    $resolved = (Resolve-Path -LiteralPath $path -ErrorAction Stop).Path
    $runtimeObservations[$label] = [pscustomobject]@{
        Path = $resolved
        Sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $resolved).Hash.ToLowerInvariant()
        Size = (Get-Item -LiteralPath $resolved -Force).Length
    }
}
$PythonExe = $runtimeObservations["Python"].Path
$NodeExe = $runtimeObservations["Node"].Path
$NpmCmd = $runtimeObservations["Npm"].Path
$PowerShellExe = $runtimeObservations["PowerShell"].Path

$gitCommand = Get-Command -Name "git.exe" -CommandType Application -ErrorAction Stop |
    Select-Object -First 1
$GitExe = [string]$gitCommand.Source
if (!(Test-FullyQualifiedPath -Path $GitExe) -or
    !(Test-Path -LiteralPath $GitExe -PathType Leaf) -or
    [IO.Path]::GetFileName($GitExe).ToLowerInvariant() -ne "git.exe") {
    throw "Git control-plane executable is not an absolute git.exe leaf"
}
Assert-NoReparseComponents -Path $GitExe -Label "Git"
$GitExe = (Resolve-Path -LiteralPath $GitExe -ErrorAction Stop).Path
$GitObservation = [pscustomobject]@{
    Path = $GitExe
    Sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $GitExe).Hash.ToLowerInvariant()
    Size = (Get-Item -LiteralPath $GitExe -Force).Length
}
$ObservedExecutableIdentities = @($runtimeObservations.Values) + @($GitObservation)

function Assert-ObservedExecutableUnchanged {
    param([Parameter(Mandatory)][string]$Path)
    $identity = @($ObservedExecutableIdentities | Where-Object {
        [string]$_.Path -eq $Path
    })
    if ($identity.Count -ne 1) { throw "native executable was not observed by the prelude" }
    Assert-NoReparseComponents -Path $Path -Label "Native"
    $item = Get-Item -LiteralPath $Path -Force -ErrorAction Stop
    $hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $Path).Hash.ToLowerInvariant()
    if ($item.Length -ne $identity[0].Size -or $hash -ne $identity[0].Sha256) {
        throw "native executable changed after prelude resolution"
    }
}

if ($null -eq ("ProjectB.NativeJob" -as [type])) {
    Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
namespace ProjectB {
    public static class NativeJob {
        [DllImport("kernel32.dll", CharSet = CharSet.Unicode)]
        public static extern IntPtr CreateJobObject(IntPtr attributes, string name);
        [DllImport("kernel32.dll", SetLastError = true)]
        public static extern bool AssignProcessToJobObject(IntPtr job, IntPtr process);
        [DllImport("kernel32.dll", SetLastError = true)]
        public static extern bool TerminateJobObject(IntPtr job, uint exitCode);
        [DllImport("kernel32.dll", SetLastError = true)]
        public static extern bool CloseHandle(IntPtr handle);
    }
}
'@
}

function Get-SanitizedChildEnvironment {
    $allowed = @(
        "SYSTEMROOT", "WINDIR", "TEMP", "TMP", "USERPROFILE", "HOME",
        "LOCALAPPDATA", "APPDATA", "PROGRAMDATA", "COMSPEC", "PATHEXT"
    )
    $clean = @{}
    foreach ($name in $allowed) {
        $value = [Environment]::GetEnvironmentVariable($name)
        if (![string]::IsNullOrWhiteSpace($value)) { $clean[$name] = $value }
    }
    $clean["PYTHONNOUSERSITE"] = "1"
    $clean["PYTHONSAFEPATH"] = "1"
    $clean["GIT_CONFIG_NOSYSTEM"] = "1"
    $clean["GIT_TERMINAL_PROMPT"] = "0"
    $clean["PROJECTB_CONTROL_GIT_EXE"] = $GitExe
    return $clean
}

function Invoke-BoundedNative {
    param(
        [Parameter(Mandatory)][string]$FilePath,
        [string[]]$ArgumentList = @(),
        [ValidateRange(1, 3600)][int]$TimeoutSeconds = 600,
        [string]$WorkingDirectory = (Get-Location).Path
    )
    if (!(Test-FullyQualifiedPath -Path $FilePath) -or
        !(Test-Path -LiteralPath $FilePath -PathType Leaf)) {
        throw "native executable must be an absolute existing leaf"
    }
    Assert-ObservedExecutableUnchanged -Path $FilePath
    $payload = @{
        filePath = $FilePath
        argumentList = @($ArgumentList)
        workingDirectory = (Resolve-Path -LiteralPath $WorkingDirectory).Path
    } | ConvertTo-Json -Compress -Depth 4
    $payloadBase64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($payload))
    $childTemplate = @'
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$json = [Text.Encoding]::UTF8.GetString(
    [Convert]::FromBase64String("__PROJECTB_PAYLOAD_BASE64__")
)
$payload = $json | ConvertFrom-Json
Set-Location -LiteralPath ([string]$payload.workingDirectory)
$arguments = @($payload.argumentList | ForEach-Object { [string]$_ })
& ([string]$payload.filePath) @arguments
$nativeExitCode = $LASTEXITCODE
exit $nativeExitCode
'@
    $childScript = $childTemplate.Replace("__PROJECTB_PAYLOAD_BASE64__", $payloadBase64)
    $encodedScript = [Convert]::ToBase64String(
        [Text.Encoding]::Unicode.GetBytes($childScript)
    )
    $startInfo = New-Object Diagnostics.ProcessStartInfo
    $startInfo.FileName = $PowerShellExe
    $startInfo.Arguments = "-NoProfile -NonInteractive -EncodedCommand $encodedScript"
    $startInfo.UseShellExecute = $false
    $startInfo.CreateNoWindow = $true
    $startInfo.RedirectStandardOutput = $true
    $startInfo.RedirectStandardError = $true
    $startInfo.EnvironmentVariables.Clear()
    foreach ($entry in (Get-SanitizedChildEnvironment).GetEnumerator()) {
        $startInfo.EnvironmentVariables[$entry.Key] = $entry.Value
    }
    $process = New-Object Diagnostics.Process
    $process.StartInfo = $startInfo
    if (!$process.Start()) { throw "native wrapper process did not start" }
    $job = [ProjectB.NativeJob]::CreateJobObject([IntPtr]::Zero, $null)
    if ($job -eq [IntPtr]::Zero -or
        ![ProjectB.NativeJob]::AssignProcessToJobObject($job, $process.Handle)) {
        try { $process.Kill() } catch { }
        if ($job -ne [IntPtr]::Zero) { [void][ProjectB.NativeJob]::CloseHandle($job) }
        $process.Dispose()
        throw "native command could not be isolated in a Windows Job Object"
    }
    $stdoutTask = $process.StandardOutput.ReadToEndAsync()
    $stderrTask = $process.StandardError.ReadToEndAsync()
    if (!$process.WaitForExit($TimeoutSeconds * 1000)) {
        [void][ProjectB.NativeJob]::TerminateJobObject($job, 124)
        $process.WaitForExit()
        [void][ProjectB.NativeJob]::CloseHandle($job)
        $process.Dispose()
        throw "native command timed out; isolated process tree terminated"
    }
    $stdout = $stdoutTask.GetAwaiter().GetResult()
    $stderr = $stderrTask.GetAwaiter().GetResult()
    if ($stderr -match "^#< CLIXML" -and $stderr -match 'S="progress"' -and
        $stderr -notmatch 'S="Error"') {
        $stderr = ""
    }
    $exitCode = $process.ExitCode
    [void][ProjectB.NativeJob]::CloseHandle($job)
    $process.Dispose()
    return [pscustomobject]@{
        ExitCode = $exitCode
        CapturedStdout = $stdout
        CapturedStderr = $stderr
        StdoutLength = $stdout.Length
        StderrLength = $stderr.Length
    }
}

function Invoke-CheckedNative {
    param(
        [Parameter(Mandatory)][string]$FilePath,
        [string[]]$ArgumentList = @(),
        [int[]]$AllowedExitCodes = @(0),
        [ValidateRange(1, 3600)][int]$TimeoutSeconds = 600,
        [string]$FailureMessage = "native command failed",
        [string]$WorkingDirectory = (Get-Location).Path
    )
    $result = Invoke-BoundedNative -FilePath $FilePath -ArgumentList $ArgumentList `
        -TimeoutSeconds $TimeoutSeconds -WorkingDirectory $WorkingDirectory
    if ($AllowedExitCodes -notcontains $result.ExitCode) {
        throw "$FailureMessage (exit=$($result.ExitCode))"
    }
    [Console]::Out.WriteLine(
        "NATIVE_COMMAND_PASS exit=$($result.ExitCode) stdout_chars=$($result.StdoutLength) stderr_chars=$($result.StderrLength)"
    )
}

function Invoke-CheckedNativeText {
    param(
        [Parameter(Mandatory)][string]$FilePath,
        [string[]]$ArgumentList = @(),
        [int[]]$AllowedExitCodes = @(0),
        [ValidateRange(1, 3600)][int]$TimeoutSeconds = 60,
        [string]$FailureMessage = "native command failed",
        [string]$WorkingDirectory = (Get-Location).Path
    )
    $result = Invoke-BoundedNative -FilePath $FilePath -ArgumentList $ArgumentList `
        -TimeoutSeconds $TimeoutSeconds -WorkingDirectory $WorkingDirectory
    if ($AllowedExitCodes -notcontains $result.ExitCode) {
        throw "$FailureMessage (exit=$($result.ExitCode))"
    }
    if ($result.CapturedStderr.Length -ne 0 -or $result.CapturedStdout.Length -gt 65536) {
        throw "$FailureMessage (captured output does not satisfy the private-text contract)"
    }
    return $result.CapturedStdout.Trim()
}

function Invoke-CheckedGit {
    param(
        [Parameter(Mandatory)][string[]]$ArgumentList,
        [int[]]$AllowedExitCodes = @(0),
        [string]$FailureMessage = "git command failed"
    )
    Invoke-CheckedNative -FilePath $GitExe -ArgumentList $ArgumentList `
        -AllowedExitCodes $AllowedExitCodes -TimeoutSeconds 120 `
        -FailureMessage $FailureMessage
}

function Invoke-CheckedGitText {
    param(
        [Parameter(Mandatory)][string[]]$ArgumentList,
        [int[]]$AllowedExitCodes = @(0),
        [string]$FailureMessage = "git command failed"
    )
    Invoke-CheckedNativeText -FilePath $GitExe -ArgumentList $ArgumentList `
        -AllowedExitCodes $AllowedExitCodes -TimeoutSeconds 120 `
        -FailureMessage $FailureMessage
}

$UnitOwnedPaths = @{
    "T-01A" = @(".gitignore", "backend/pyproject.toml", "backend/requirements-windows-x64.lock", "backend/tests/unit/test_toolchain_contract.py")
    "T-01B" = @("backend/src/projectb/__init__.py", "backend/src/projectb/api/__init__.py", "backend/src/projectb/api/app.py", "backend/tests/unit/test_health.py")
    "T-01C1" = @("frontend/package.json", "frontend/.npmrc", "frontend/tsconfig.json", "frontend/vitest.contract.json", "frontend/vite.config.contract.json", "frontend/vite.config.ts", "frontend/package-lock.json", "scripts/frontend_lock_contract.mjs", "scripts/materialize_frontend_lock.mjs", "scripts/tests/frontend_contract.test.mjs", "scripts/tests/frontend_lock_contract.test.mjs")
    "T-01C2" = @("frontend/index.html", "frontend/src/main.tsx", "frontend/src/app/App.tsx", "frontend/src/app/App.test.tsx")
    "T-01D" = @("scripts/secret_scan/__init__.py", "scripts/secret_scan/encoding.py", "scripts/secret_scan/paths.py", "scripts/secret_scan/rules.py", "scripts/scan_secrets.py", "scripts/scan_secrets.ps1", "backend/tests/unit/test_secret_scanner.py")
    "T-01E1" = @("scripts/projectb_test_runner/__init__.py", "scripts/projectb_test_runner/executables.py", "backend/tests/unit/test_runner_executables.py")
    "T-01E2" = @("scripts/projectb_test_runner/contracts.py", "scripts/projectb_test_runner/locks.py", "scripts/projectb_test_runner/runtime.py", "backend/tests/unit/test_runner_contracts.py", "backend/tests/unit/test_runner_locks.py", "backend/tests/unit/test_runner_runtime.py")
    "T-01F1" = @("scripts/projectb_test_runner/gate_model.py", "scripts/projectb_test_runner/gate_run.py", "backend/tests/unit/test_runner_gates.py")
    "T-01F2" = @("scripts/projectb_test_runner/core_registry.py", "scripts/projectb_test_runner/deferred_registry.py", "scripts/projectb_test_runner/registry.py", "backend/tests/unit/test_runner_registry.py")
    "T-01F3" = @("scripts/projectb_test_runner/runner.py", "scripts/test_all.py", "backend/tests/unit/test_runner_cli.py")
}

function Assert-G02AEvidenceBinding {
    $resolvedEvidenceCommit = Invoke-CheckedGitText -ArgumentList @(
        "rev-parse", "--verify", "$G02aEvidenceCommit^{commit}"
    ) -FailureMessage "G-02A evidence commit is unavailable"
    $resolvedEvidenceTree = Invoke-CheckedGitText -ArgumentList @(
        "rev-parse", "--verify", "$G02aEvidenceCommit^{tree}"
    ) -FailureMessage "G-02A evidence tree is unavailable"
    if ($resolvedEvidenceCommit -ne $G02aEvidenceCommit -or
        $resolvedEvidenceTree -ne $G02aEvidenceTree) {
        throw "G-02A commit/tree differs from the reviewed immutable evidence"
    }
    Invoke-CheckedGit -ArgumentList @(
        "merge-base", "--is-ancestor", $G02aEvidenceCommit, $BaseCommit
    ) -FailureMessage "reviewed G-02A evidence is not an ancestor of the unit base"
    foreach ($record in $G02aEvidenceFiles) {
        $relative = [string]$record[0]
        $expectedBlob = [string]$record[1]
        $treeBlob = Invoke-CheckedGitText -ArgumentList @(
            "rev-parse", "--verify", "$G02aEvidenceTree`:$relative"
        ) -FailureMessage "G-02A evidence tree lacks a required blob"
        $commitTreeBlob = Invoke-CheckedGitText -ArgumentList @(
            "rev-parse", "--verify", "$G02aEvidenceCommit^{tree}:$relative"
        ) -FailureMessage "G-02A commit tree lacks a required blob"
        $baseBlob = Invoke-CheckedGitText -ArgumentList @(
            "rev-parse", "--verify", "$BaseCommit`:$relative"
        ) -FailureMessage "unit base lacks a required G-02A blob"
        $localBlob = Invoke-CheckedGitText -ArgumentList @(
            "hash-object", "--no-filters", "--", $relative
        ) -FailureMessage "worktree G-02A evidence bytes are unavailable"
        foreach ($blob in @($treeBlob, $commitTreeBlob, $baseBlob, $localBlob)) {
            Assert-LowerHex -Value $blob -Length 40 -Name "G-02A evidence blob"
            if ($blob -ne $expectedBlob) {
                throw "G-02A evidence path is not the reviewed immutable blob"
            }
        }
    }
}

function Assert-UnitContext {
    param([Parameter(Mandatory)][string]$UnitId)

    if (!$UnitOwnedPaths.ContainsKey($UnitId) -or $env:PROJECTB_UNIT_ID -ne $UnitId) {
        throw "PROJECTB_UNIT_ID does not match a declared T-01 unit"
    }
    if (!(Test-FullyQualifiedPath -Path $WorktreeRoot)) {
        throw "PROJECTB_WORKTREE_ROOT is not fully qualified"
    }
    Set-Location -LiteralPath $WorktreeRoot
    $gitTopLevel = Invoke-CheckedGitText -ArgumentList @("rev-parse", "--show-toplevel") `
        -FailureMessage "Git top-level lookup failed"
    $resolvedTopLevel = (Resolve-Path -LiteralPath $gitTopLevel -ErrorAction Stop).Path
    if (![IO.Path]::GetFullPath($resolvedTopLevel).Equals(
            [IO.Path]::GetFullPath($WorktreeRoot),
            [StringComparison]::OrdinalIgnoreCase)) {
        throw "Git top-level differs from PROJECTB_WORKTREE_ROOT"
    }
    $resolvedBase = Invoke-CheckedGitText -ArgumentList @(
        "rev-parse", "--verify", "$BaseCommit^{commit}"
    ) -FailureMessage "PROJECTB_BASE_COMMIT is unavailable"
    $head = Invoke-CheckedGitText -ArgumentList @("rev-parse", "--verify", "HEAD") `
        -FailureMessage "HEAD lookup failed"
    Assert-LowerHex -Value $resolvedBase -Length 40 -Name "resolved base commit"
    Assert-LowerHex -Value $head -Length 40 -Name "HEAD"
    if ($resolvedBase -ne $BaseCommit -or $head -ne $BaseCommit) {
        throw "unit HEAD must equal its exact declared base commit before work starts"
    }
    Assert-G02AEvidenceBinding
    $owned = @($UnitOwnedPaths[$UnitId])
    $ownedStatus = Invoke-CheckedGitText -ArgumentList (
        @("status", "--porcelain=v1", "-z", "--untracked-files=all", "--") + $owned
    ) -FailureMessage "owned-scope status lookup failed"
    if (![string]::IsNullOrEmpty($ownedStatus)) {
        throw "unit-owned scope is not clean before its first edit"
    }
    Invoke-CheckedGit -ArgumentList @("diff", "--cached", "--quiet", "--") `
        -FailureMessage "unit worktree begins with a nonempty staged index"
}

function Assert-ValidIdentity {
    param(
        [Parameter(Mandatory)][string]$Role,
        [Parameter(Mandatory)][string]$Identity
    )
    if ($Identity -notmatch "^[A-Za-z0-9][A-Za-z0-9._-]{1,63}$") {
        throw "$Role identity does not match the canonical syntax"
    }
}

function Assert-ThreeDistinctIdentities {
    param(
        [Parameter(Mandatory)][string]$UnitId,
        [Parameter(Mandatory)][string[]]$Identities
    )
    if ($Identities.Count -ne 3) { throw "$UnitId requires exactly three identities" }
    for ($index = 0; $index -lt $Identities.Count; $index++) {
        Assert-ValidIdentity -Role "$UnitId role $index" -Identity $Identities[$index]
    }
    if (($Identities | Sort-Object -Unique).Count -ne 3) {
        throw "$UnitId worker and reviewers must be distinct"
    }
}

function Get-StagedTreeId {
    $tree = Invoke-CheckedGitText -ArgumentList @("write-tree") `
        -FailureMessage "unable to bind the staged tree"
    if ($tree -notmatch "^[0-9a-f]{40}$") { throw "invalid staged tree ID" }
    return $tree
}

function Assert-ReviewBinding {
    param(
        [Parameter(Mandatory)][string]$UnitId,
        [Parameter(Mandatory)][string[]]$Identities,
        [Parameter(Mandatory)][string]$SpecTreeId,
        [Parameter(Mandatory)][string]$QualityTreeId
    )
    Assert-ThreeDistinctIdentities -UnitId $UnitId -Identities $Identities
    Assert-LowerHex -Value $SpecTreeId -Length 40 -Name "$UnitId SPEC review tree"
    Assert-LowerHex -Value $QualityTreeId -Length 40 -Name "$UnitId quality review tree"
    $currentTree = Get-StagedTreeId
    if ($SpecTreeId -ne $currentTree -or $QualityTreeId -ne $currentTree) {
        throw "$UnitId reviews do not bind the current staged tree"
    }
}

function Assert-CommittedTreeBinding {
    param(
        [Parameter(Mandatory)][string]$UnitId,
        [Parameter(Mandatory)][string]$ExpectedTreeId
    )
    $committedTree = Invoke-CheckedGitText -ArgumentList @("rev-parse", "HEAD^{tree}") `
        -FailureMessage "$UnitId committed tree lookup failed"
    Assert-LowerHex -Value $committedTree -Length 40 -Name "$UnitId committed tree"
    Assert-LowerHex -Value $ExpectedTreeId -Length 40 -Name "$UnitId expected tree"
    if ($committedTree -ne $ExpectedTreeId) {
        throw "$UnitId committed tree differs from the reviewed staged tree"
    }
}

function Assert-ExactStagedPaths {
    param([Parameter(Mandatory)][string[]]$ExpectedPaths)

    $expected = @($ExpectedPaths | Sort-Object -Unique)
    if ($ExpectedPaths.Count -eq 0 -or $expected.Count -ne $ExpectedPaths.Count) {
        throw "expected staged path set must be nonempty and unique"
    }
    $text = Invoke-CheckedGitText -ArgumentList @("diff", "--cached", "--name-only") `
        -FailureMessage "unable to inspect the complete Git index"
    [string[]]$actual = @()
    if (![string]::IsNullOrWhiteSpace($text)) {
        $actual = @($text -split "`r?`n" | Where-Object { $_ -ne "" } | Sort-Object -Unique)
    }
    if ($actual.Count -eq 0) { throw "complete staged index is empty" }
    $missing = @(Compare-Object -ReferenceObject $expected -DifferenceObject $actual `
        | Where-Object SideIndicator -eq "<=")
    $extra = @(Compare-Object -ReferenceObject $expected -DifferenceObject $actual `
        | Where-Object SideIndicator -eq "=>")
    if ($actual.Count -ne $expected.Count -or $missing.Count -ne 0 -or $extra.Count -ne 0) {
        $missingText = $missing.InputObject -join ","
        $extraText = $extra.InputObject -join ","
        throw "complete staged index differs; missing=$missingText; extra=$extraText"
    }
}

function Export-ReviewedStagedDiff {
    param(
        [Parameter(Mandatory)][string]$UnitId,
        [Parameter(Mandatory)][string]$ExpectedTreeId
    )
    Assert-LowerHex -Value $ExpectedTreeId -Length 40 -Name "$UnitId staged tree"
    if ((Get-StagedTreeId) -ne $ExpectedTreeId) {
        throw "$UnitId staged tree changed before reviewer artifact creation"
    }
    $result = Invoke-BoundedNative -FilePath $GitExe -ArgumentList @(
        "diff", "--cached", "--binary", "--full-index", "--no-ext-diff"
    ) -TimeoutSeconds 120 -WorkingDirectory $WorktreeRoot
    if ($result.ExitCode -ne 0 -or $result.CapturedStderr.Length -ne 0) {
        throw "unable to create redacted staged reviewer artifact"
    }
    $gitDirectory = Invoke-CheckedGitText -ArgumentList @("rev-parse", "--git-dir") `
        -FailureMessage "unable to locate private reviewer artifact directory"
    $packetRoot = Join-Path (Resolve-Path -LiteralPath $gitDirectory).Path "projectb-review-packets"
    [IO.Directory]::CreateDirectory($packetRoot) | Out-Null
    $packetPath = Join-Path $packetRoot "$UnitId-$ExpectedTreeId.patch"
    [IO.File]::WriteAllText(
        $packetPath,
        $result.CapturedStdout,
        (New-Object Text.UTF8Encoding($false))
    )
    return [pscustomobject]@{
        UnitId = $UnitId
        TreeId = $ExpectedTreeId
        ArtifactPath = $packetPath
        ArtifactSha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $packetPath).Hash.ToLowerInvariant()
        CharacterCount = $result.CapturedStdout.Length
    }
}

if ($env:PROJECTB_PYTHON_VERSION -ne "3.14.6" -or
    $env:PROJECTB_NODE_VERSION -ne "v24.18.0" -or
    $env:PROJECTB_NPM_VERSION -ne "11.16.0" -or
    $env:PROJECTB_POWERSHELL_VERSION -ne "7.6.1") {
    throw "G-04 runtime version metadata is missing or weakened"
}
if ((Invoke-CheckedNativeText -FilePath $PythonExe -ArgumentList @("--version") `
        -TimeoutSeconds 30 -FailureMessage "Python version command failed") -ne "Python $env:PROJECTB_PYTHON_VERSION") { throw "Python version mismatch" }
if ((Invoke-CheckedNativeText -FilePath $NodeExe -ArgumentList @("--version") `
        -TimeoutSeconds 30 -FailureMessage "Node version command failed") -ne $env:PROJECTB_NODE_VERSION) { throw "Node version mismatch" }
if ((Invoke-CheckedNativeText -FilePath $NpmCmd -ArgumentList @("--version") `
        -TimeoutSeconds 30 -FailureMessage "npm version command failed") -ne $env:PROJECTB_NPM_VERSION) { throw "npm version mismatch" }
$psVersion = Invoke-CheckedNativeText -FilePath $PowerShellExe `
    -ArgumentList @("-NoProfile", "-Command", '$PSVersionTable.PSVersion.ToString()') `
    -TimeoutSeconds 30 -FailureMessage "PowerShell version command failed"
if ($psVersion -ne $env:PROJECTB_POWERSHELL_VERSION) { throw "PowerShell version mismatch" }
Assert-ValidIdentity -Role "worker" -Identity $env:PROJECTB_AGENT_ID
```

The four runtime paths above are the root contract. Their hashes, exact versions, and provenance remain coordinator-owned G-04 metadata and must be validated by the atomically amended G-04 map before this prelude can be used as dispatch evidence. The observed hashes in this prelude detect same-run replacement only; they are not an approval source. Each unit repeats the final reviewed prelude in Step 1, calls `Assert-UnitContext` with its literal unit ID before editing, invokes every external command through the bounded wrapper, compares the whole staged index by count plus two `Compare-Object` set differences, validates identities against the exact regex, and binds both final reviews to the current staged Git tree ID.

After the root/G-04 amendment is reviewed and before the first unit dispatch, run the prelude against disposable worktrees and retain only redacted pass/fail summaries. The negative matrix must mutate each of `PROJECTB_UNIT_ID`, `PROJECTB_BASE_COMMIT`, `PROJECTB_WORKTREE_ROOT`, Git top-level, HEAD, an owned untracked path, and the staged index; each mutation must fail before the first edit. Separately mutate each fixed G-02A tree/blob reference, each base-commit evidence path, each local evidence byte stream, every one of the four coordinator runtime paths, every G-04 hash/version/provenance field, and each runtime leaf after initial observation. A fake `python.exe` that prints exactly `Python 3.14.6` must fail the G-04 attestation check; changing a base path while leaving the G-02A commit untouched must fail the evidence blob comparison. For process isolation, launch a child that continuously updates a disposable heartbeat and records its PID, force a one-second timeout, then prove the PID no longer exists and the heartbeat stops changing. Inject a sentinel in inherited `PATH`, `PYTHONPATH`, `NODE_OPTIONS`, stdout, and stderr; prove the child cannot read the environment sentinels and neither exception text nor retained wrapper output contains either stream sentinel. Failure of any negative keeps all ten units blocked.

Before T-01D exists, units A, B, C1, C2, E1, and E2 use this bootstrap helper after staging. It reads only Git index blobs through the approved absolute Git leaf, validates an exact stage-0 regular-file set, uses bounded subprocesses and a sanitized environment, decodes UTF-8/UTF-16 BOM variants strictly, rejects undecodable or NUL-bearing content, and emits neither paths nor matched values. Once reviewed T-01D is integrated, every later unit invokes `scripts/scan_secrets.py --staged --git-exe $GitExe` through `Invoke-CheckedNative`.

```powershell
function Invoke-BootstrapStagedSecretScan {
    param([Parameter(Mandatory)][string[]]$ExpectedPaths)

    if ($ExpectedPaths.Count -eq 0) { throw "bootstrap staged scan requires paths" }
    $scanProgram = @'
import codecs
import os
import re
import subprocess
import sys
from pathlib import Path

import psutil


def abort() -> None:
    print("BOOTSTRAP_STAGED_SCAN_OPERATIONAL_FAILURE", file=sys.stderr)
    raise SystemExit(2)


git_executable = Path(sys.argv[1])
expected = sys.argv[2:]
if not expected or len(expected) != len(set(expected)):
    abort()
if not git_executable.is_absolute() or not git_executable.is_file():
    abort()
safe_environment = {
    key: value
    for key in ("SYSTEMROOT", "WINDIR", "TEMP", "TMP", "USERPROFILE", "HOME")
    if (value := os.environ.get(key))
}
safe_environment["GIT_CONFIG_NOSYSTEM"] = "1"
safe_environment["GIT_TERMINAL_PROMPT"] = "0"


def terminate_process_tree(process: subprocess.Popen[bytes]) -> None:
    try:
        descendants = psutil.Process(process.pid).children(recursive=True)
    except psutil.Error:
        descendants = []
    for child in reversed(descendants):
        try:
            child.kill()
        except psutil.Error:
            continue
    try:
        process.kill()
    except OSError:
        pass
    psutil.wait_procs(descendants, timeout=5.0)


def run_git(arguments: list[str]) -> subprocess.CompletedProcess[bytes]:
    try:
        process = subprocess.Popen(
            [str(git_executable), *arguments],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=safe_environment,
        )
        stdout, stderr = process.communicate(timeout=30)
    except subprocess.TimeoutExpired:
        terminate_process_tree(process)
        abort()
    except OSError:
        abort()
    return subprocess.CompletedProcess(
        [str(git_executable), *arguments],
        process.returncode if process.returncode is not None else 127,
        stdout,
        stderr,
    )


index = run_git(["ls-files", "--stage", "-z", "--", *expected])
if index.returncode != 0:
    abort()
records = []
for raw_record in index.stdout.split(b"\0"):
    if not raw_record:
        continue
    try:
        metadata, raw_path = raw_record.split(b"\t", 1)
        mode, object_id, stage = metadata.decode("ascii").split(" ")
        path = raw_path.decode("utf-8", "strict")
    except (UnicodeError, ValueError):
        abort()
    if mode not in {"100644", "100755"} or stage != "0":
        abort()
    records.append((object_id, path))
if sorted(path for _, path in records) != sorted(expected):
    abort()

patterns = (
    re.compile(r"sk-(?:proj-)?[A-Za-z0-9_-]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN (?:[A-Z0-9][A-Z0-9 -]* )?PRIVATE KEY(?: BLOCK)?-----"),
    re.compile(
        r"(?:^|[^A-Za-z])(?:api[_-]?key|token|password|secret)\s*[:=]\s*['\"][^'\"]{8,}",
        re.IGNORECASE | re.MULTILINE,
    ),
)
for object_id, _ in records:
    blob = run_git(["cat-file", "blob", object_id])
    if blob.returncode != 0:
        abort()
    data = blob.stdout
    try:
        if data.startswith(codecs.BOM_UTF8):
            text = data.decode("utf-8-sig", "strict")
        elif data.startswith(codecs.BOM_UTF16_LE):
            text = data[len(codecs.BOM_UTF16_LE):].decode("utf-16-le", "strict")
        elif data.startswith(codecs.BOM_UTF16_BE):
            text = data[len(codecs.BOM_UTF16_BE):].decode("utf-16-be", "strict")
        else:
            if b"\0" in data:
                abort()
            text = data.decode("utf-8", "strict")
    except UnicodeError:
        abort()
    if any(pattern.search(text) for pattern in patterns):
        raise SystemExit(1)
raise SystemExit(0)
'@
    $arguments = @("-c", $scanProgram, $GitExe) + $ExpectedPaths
    $scan = Invoke-BoundedNative -FilePath $PythonExe -ArgumentList $arguments `
        -TimeoutSeconds 120
    $scanCode = $scan.ExitCode
    if ($scanCode -eq 1) { throw "credential-shaped content detected in staged Git index" }
    if ($scanCode -ne 0) { throw "bootstrap staged scan failed operationally" }
}

function Invoke-FinalPrecommitValidation {
    param(
        [Parameter(Mandatory)][string]$UnitId,
        [Parameter(Mandatory)][string[]]$ExpectedPaths,
        [Parameter(Mandatory)][string[]]$Identities,
        [Parameter(Mandatory)][string]$SpecTreeId,
        [Parameter(Mandatory)][string]$QualityTreeId,
        [Parameter(Mandatory)][ValidateSet("bootstrap", "canonical")][string]$ScannerMode
    )
    Assert-ReviewBinding -UnitId $UnitId -Identities $Identities `
        -SpecTreeId $SpecTreeId -QualityTreeId $QualityTreeId
    Assert-ExactStagedPaths -ExpectedPaths $ExpectedPaths
    Invoke-CheckedGit -ArgumentList @("diff", "--cached", "--check") `
        -FailureMessage "$UnitId final staged diff check failed"
    if ($ScannerMode -eq "bootstrap") {
        Invoke-BootstrapStagedSecretScan -ExpectedPaths $ExpectedPaths
    } else {
        Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
            "scripts/scan_secrets.py", "--staged", "--git-exe", $GitExe
        ) -TimeoutSeconds 300 -FailureMessage "$UnitId final staged scanner failed"
    }
}
```

## Mandatory Final Stage And Review Binding

Every task's earlier review steps prepare reviewer scope and prompts only; they do not dispatch the two formal reviewers. The task first stages exactly its owned paths, checks the whole index, runs the applicable staged scanner, and records `Get-StagedTreeId`. Only then `Export-ReviewedStagedDiff` captures the exact `git diff --cached --binary --full-index` stream into a private artifact and emits only its tree ID, path, character count, and SHA-256; raw stdout/stderr is never forwarded to the console, exception, or retained command log. Two fresh reviewers receive that artifact and tree ID through their private packets. They set their task-specific reviewer ID and `*_REVIEW_TREE` variables to the reviewed tree. Any implementation, test, formatting, or staging edit invalidates both approvals: return to the stage step and repeat both reviews. Immediately before commit, the task runs `Assert-ReviewBinding`, reasserts the whole index, reruns checked `git diff --cached --check`, reruns the staged scanner, and only then runs the checked commit and hash lookup. `Assert-CommittedTreeBinding` then requires `HEAD^{tree}` to equal the reviewed staged tree. No review of a worktree diff or an earlier tree is completion evidence.

### Task T-01A: Lock Toolchain, Quality Configuration, And Raw Python Closure

**Unit prelude:** Run the complete Required Fail-Closed Command Prelude before Step 1 and reuse the four verified runtime paths. `$GitExe` is a separately resolved coordinator control-plane path used only by scan/stage wrappers.

**Goal:** Establish the exact Python project metadata, explicit Ruff/mypy configuration, raw-byte Python lock, and editable-install ignore rule consumed by every later unit.

**Dependencies / parallelism:** Requires G-01, G-02A, G-03 approval, and a G-04 worktree. No other T-01 unit runs before its reviewed commit. T-01B/C/D may branch from its commit.

**Files:**
- Modify: `.gitignore`
- Create: `backend/pyproject.toml`
- Create by raw-byte copy: `backend/requirements-windows-x64.lock`
- Test: `backend/tests/unit/test_toolchain_contract.py`

**Acceptance:** The manifest exactly pins the G-02A direct dependency sets; Ruff and mypy settings are explicit; the production Python lock is byte-identical to the evidence lock whose raw SHA-256 is `246083f8b210c3e33904f3057dfd48e7d8db548804d11fa5b087ecb291ad0fc6`; no newline normalization occurs.

- [ ] **Step 1: Verify the assigned runtime and worker identity**

Run:

```powershell
Assert-UnitContext -UnitId "T-01A"
Assert-ValidIdentity -Role "T-01A worker" -Identity $env:PROJECTB_AGENT_ID
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @("--version") `
    -TimeoutSeconds 30 -FailureMessage "T-01A Python invocation failed"
```

Expected: the identity check exits 0 and Python prints exactly `Python 3.14.6`.

- [ ] **Step 2: Write the failing toolchain contract test**

Create `backend/tests/unit/test_toolchain_contract.py`:

```python
import hashlib
import tomllib
import unittest
from pathlib import Path
from typing import Any

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
EXPECTED_RUNTIME_DEPENDENCIES = [
    "fastapi==0.139.2",
    "uvicorn==0.51.0",
    "pydantic==2.13.4",
    "httpx==0.28.1",
    "openai==2.46.0",
    "pypdf==6.14.2",
    "pypdfium2==5.12.1",
    "Pillow==12.3.0",
    "keyring==25.7.0",
    "tzdata==2026.3",
    "python-multipart==0.0.32",
    "psutil==7.2.2",
]
EXPECTED_OPTIONAL_DEPENDENCIES = {
    "test": ["httpx2==2.7.0", "pytest==9.1.1"],
    "quality": ["ruff==0.15.22", "mypy==2.3.0", "types-psutil==7.2.2.20260518"],
    "build": ["pyinstaller==6.21.0"],
}
EXPECTED_LOCK_SHA256 = "246083f8b210c3e33904f3057dfd48e7d8db548804d11fa5b087ecb291ad0fc6"
EXPECTED_LOCK_BLOB_SHA1 = "1078db073060e01051bebd1f2250ab55b0cec3d2"


class ToolchainContractTests(unittest.TestCase):
    def manifest(self) -> dict[str, Any]:
        path = REPOSITORY_ROOT / "backend" / "pyproject.toml"
        with path.open("rb") as stream:
            return tomllib.load(stream)

    def test_manifest_uses_exact_direct_dependencies(self) -> None:
        manifest = self.manifest()
        project = manifest["project"]
        self.assertEqual(project["requires-python"], "==3.14.*")
        self.assertEqual(project["dependencies"], EXPECTED_RUNTIME_DEPENDENCIES)
        self.assertEqual(project["optional-dependencies"], EXPECTED_OPTIONAL_DEPENDENCIES)

    def test_quality_configuration_is_explicit(self) -> None:
        manifest = self.manifest()
        self.assertEqual(
            manifest["tool"]["ruff"],
            {
                "target-version": "py314",
                "line-length": 100,
                "src": ["src", "tests", "../scripts"],
                "lint": {"select": ["B", "E", "F", "I", "UP"]},
            },
        )
        self.assertEqual(
            manifest["tool"]["mypy"],
            {
                "python_version": "3.14",
                "strict": True,
                "warn_unreachable": True,
                "show_error_codes": True,
            },
        )

    def test_python_lock_is_a_raw_byte_copy(self) -> None:
        source = REPOSITORY_ROOT / "docs/engineering/locks/python-3.14.6-windows-x64.lock"
        target = REPOSITORY_ROOT / "backend/requirements-windows-x64.lock"
        source_bytes = source.read_bytes()
        target_bytes = target.read_bytes()
        self.assertEqual(hashlib.sha256(source_bytes).hexdigest(), EXPECTED_LOCK_SHA256)
        header = f"blob {len(source_bytes)}\0".encode("ascii")
        self.assertEqual(
            hashlib.sha1(header + source_bytes).hexdigest(),
            EXPECTED_LOCK_BLOB_SHA1,
        )
        self.assertEqual(target_bytes, source_bytes)

    def test_editable_install_metadata_is_ignored_once(self) -> None:
        lines = (REPOSITORY_ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
        self.assertEqual(lines.count("*.egg-info/"), 1)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Run the toolchain contract red**

Run the test through `Invoke-CheckedNative` with `$PythonExe`, arguments `@("backend/tests/unit/test_toolchain_contract.py")`, and a 300-second timeout.

Expected: nonzero exit because at least one required T-01A artifact is absent; the accepted red reason is a missing manifest, production lock, or ignore rule, not a Python import/runtime error.

- [ ] **Step 4: Add the exact Python manifest**

Create `backend/pyproject.toml`:

```toml
[build-system]
requires = ["setuptools==83.0.0"]
build-backend = "setuptools.build_meta"

[project]
name = "projectb"
version = "0.1.0"
description = "Local-first course learning workbench"
requires-python = "==3.14.*"
dependencies = [
    "fastapi==0.139.2",
    "uvicorn==0.51.0",
    "pydantic==2.13.4",
    "httpx==0.28.1",
    "openai==2.46.0",
    "pypdf==6.14.2",
    "pypdfium2==5.12.1",
    "Pillow==12.3.0",
    "keyring==25.7.0",
    "tzdata==2026.3",
    "python-multipart==0.0.32",
    "psutil==7.2.2",
]

[project.optional-dependencies]
test = ["httpx2==2.7.0", "pytest==9.1.1"]
quality = ["ruff==0.15.22", "mypy==2.3.0", "types-psutil==7.2.2.20260518"]
build = ["pyinstaller==6.21.0"]

[tool.setuptools]
package-dir = {"" = "src"}

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
addopts = "-W error --strict-config --strict-markers"
testpaths = ["tests"]

[tool.ruff]
target-version = "py314"
line-length = 100
src = ["src", "tests", "../scripts"]

[tool.ruff.lint]
select = ["B", "E", "F", "I", "UP"]

[tool.mypy]
python_version = "3.14"
strict = true
warn_unreachable = true
show_error_codes = true
```

- [ ] **Step 5: Copy and verify the Python lock without text decoding**

Run:

```powershell
New-Item -ItemType Directory -Force backend | Out-Null
$sourcePath = Resolve-Path "docs/engineering/locks/python-3.14.6-windows-x64.lock"
$targetPath = Join-Path (Resolve-Path .) "backend/requirements-windows-x64.lock"
[IO.File]::WriteAllBytes($targetPath, [IO.File]::ReadAllBytes($sourcePath))
$sourceHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $sourcePath).Hash.ToLowerInvariant()
$targetHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $targetPath).Hash.ToLowerInvariant()
if ($sourceHash -ne "246083f8b210c3e33904f3057dfd48e7d8db548804d11fa5b087ecb291ad0fc6") {
    throw "G-02A Python lock raw SHA-256 mismatch"
}
if ($sourceHash -ne $targetHash) {
    throw "Production Python lock raw SHA-256 mismatch"
}
```

Expected: both raw SHA-256 values are identical and the command exits 0.

- [ ] **Step 6: Add the exact editable-install ignore increment**

Append this block to `.gitignore` only when the pattern is absent:

```gitignore
# Python editable-install metadata
*.egg-info/
```

Run through PowerShell's in-process matcher: `Select-String -LiteralPath .gitignore -Pattern '^\*\.egg-info/$'`.

Expected: exactly one matching line.

- [ ] **Step 7: Run the toolchain contract green**

Run the test through `Invoke-CheckedNative` with `$PythonExe`, arguments `@("backend/tests/unit/test_toolchain_contract.py")`, and a 300-second timeout.

Expected: every toolchain contract test passes and the command exits 0.

- [ ] **Step 8: Install the locked closure and reverify explicit quality config**

Run:

```powershell
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "-m", "pip", "install", "--require-hashes", "-r", "backend/requirements-windows-x64.lock"
) -TimeoutSeconds 1800 -FailureMessage "T-01A locked install failed"
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "-m", "pip", "install", "--no-deps", "-e", "backend[test,quality,build]"
) -TimeoutSeconds 600 -FailureMessage "T-01A editable install failed"
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @("-m", "pip", "check") `
    -TimeoutSeconds 300 -FailureMessage "T-01A pip check failed"
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "-m", "pytest", "backend/tests/unit/test_toolchain_contract.py", "-q"
) -TimeoutSeconds 300 -FailureMessage "T-01A focused tests failed"
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "-m", "ruff", "check", "--config", "backend/pyproject.toml",
    "backend/tests/unit/test_toolchain_contract.py"
) -TimeoutSeconds 300 -FailureMessage "T-01A Ruff failed"
```

Expected: installation uses only the hashed closure; `pip check` reports no broken requirements; every focused test passes; Ruff exits 0 using the explicit config path.

- [ ] **Step 9: Prepare the T-01A SPEC review packet without dispatching**

Prepare `SPEC.md`, the full root `PLAN.md` selected by stable T-01 heading/ID, this plan's T-01A section, the literal base commit ID, Step 7-8 output, and the SPEC questions for AC-10, G-02A consumption, raw-byte identity, and T-01A acceptance. Do not dispatch until Step 11 has produced the final staged diff and tree ID.

- [ ] **Step 10: Prepare the T-01A quality review packet without dispatching**

Prepare the distinct quality review questions for dependency reproducibility, TOML correctness, test quality, raw hash handling, Ruff/mypy explicitness, license evidence, and staged-scope safety. Do not dispatch until the final staged tree exists.

- [ ] **Step 11: Stage exactly four paths and run the bootstrap staged-secret scan**

Run:

```powershell
$paths = @(
    ".gitignore",
    "backend/pyproject.toml",
    "backend/requirements-windows-x64.lock",
    "backend/tests/unit/test_toolchain_contract.py"
)
Invoke-CheckedGit -ArgumentList (@("add", "--") + $paths) -FailureMessage "T-01A git add failed"
Invoke-CheckedGit -ArgumentList @("diff", "--cached", "--check") -FailureMessage "T-01A staged diff check failed"
Invoke-BootstrapStagedSecretScan -ExpectedPaths $paths
Assert-ExactStagedPaths -ExpectedPaths $paths
$reviewTree = Get-StagedTreeId
$reviewTree
$reviewPacket = Export-ReviewedStagedDiff -UnitId $env:PROJECTB_UNIT_ID `
    -ExpectedTreeId $reviewTree
$reviewPacket
```

Expected: whitespace and bootstrap scan pass, and the exact four-path comparison succeeds. The scan captures filenames only and never emits matched values.

- [ ] **Step 12: Run both staged-tree reviews, revalidate, and commit T-01A**

Run:

```powershell
$ids = @(
    $env:PROJECTB_AGENT_ID,
    $env:PROJECTB_T01A_SPEC_REVIEW_ID,
    $env:PROJECTB_T01A_QUALITY_REVIEW_ID
)
Invoke-FinalPrecommitValidation -UnitId "T-01A" -ExpectedPaths $paths -Identities $ids `
    -SpecTreeId $env:PROJECTB_T01A_SPEC_REVIEW_TREE `
    -QualityTreeId $env:PROJECTB_T01A_QUALITY_REVIEW_TREE -ScannerMode "bootstrap"
Invoke-CheckedGit -ArgumentList @("commit", "-m", "build(T-01A): lock Python toolchain and quality config [agent: $env:PROJECTB_AGENT_ID]") `
    -FailureMessage "T-01A commit failed"
$commitHash = Invoke-CheckedGitText -ArgumentList @("rev-parse", "HEAD") -FailureMessage "T-01A hash lookup failed"
Assert-CommittedTreeBinding -UnitId "T-01A" -ExpectedTreeId $env:PROJECTB_T01A_SPEC_REVIEW_TREE
if ($commitHash -notmatch "^[0-9a-f]{40}$") { throw "T-01A did not produce a full commit hash" }
$commitHash
```

Expected: one four-path T-01A commit and its actual hash. The coordinator records the hash/reviews before dispatching B/C/D.

### Task T-01B: Add The Typed Backend Health Scaffold

**Unit prelude:** Run the complete Required Fail-Closed Command Prelude before Step 1 and reuse the four verified runtime paths. `$GitExe` is a separately resolved coordinator control-plane path used only by scan/stage wrappers.

**Goal:** Add the smallest bootable FastAPI package and typed profile-labelled health endpoint.

**Dependencies / parallelism:** Requires the reviewed T-01A commit. May run in parallel with T-01C1 and T-01D. Owns no manifest, frontend, scanner, or runner file.

**Files:**
- Create: `backend/src/projectb/__init__.py`
- Create: `backend/src/projectb/api/__init__.py`
- Create: `backend/src/projectb/api/app.py`
- Test: `backend/tests/unit/test_health.py`

**Acceptance:** `create_app(profile: str = "local") -> FastAPI`; `GET /api/health` returns status 200 and exactly `{"status":"ok","profile":"local"}` for the module app; no network/provider call occurs.

- [ ] **Step 1: Verify T-01A and install its locked environment**

Run:

```powershell
Assert-UnitContext -UnitId "T-01B"
Assert-ValidIdentity -Role "T-01B worker" -Identity $env:PROJECTB_AGENT_ID
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @("--version") `
    -TimeoutSeconds 30 -FailureMessage "T-01B Python invocation failed"
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "-m", "pip", "install", "--require-hashes", "-r", "backend/requirements-windows-x64.lock"
) -TimeoutSeconds 1800 -FailureMessage "T-01B locked install failed"
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "-m", "pip", "install", "--no-deps", "-e", "backend[test,quality,build]"
) -TimeoutSeconds 600 -FailureMessage "T-01B editable install failed"
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "backend/tests/unit/test_toolchain_contract.py"
) -TimeoutSeconds 300 -FailureMessage "T-01B foundation contract failed"
```

Expected: Python is 3.14.6 and the four T-01A contract tests pass.

- [ ] **Step 2: Write the failing health test**

Create `backend/tests/unit/test_health.py`:

```python
from fastapi.testclient import TestClient
from projectb.api.app import create_app


def test_health_reports_local_profile() -> None:
    response = TestClient(create_app("local")).get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "profile": "local"}
```

- [ ] **Step 3: Run the health test red**

Run the red through `Invoke-CheckedNative` with `$PythonExe`, arguments `@("-m", "pytest", "backend/tests/unit/test_health.py", "-q")`, and a 300-second timeout.

Expected: collection fails because `projectb.api.app` is absent. A dependency or runtime failure is not acceptable red evidence.

- [ ] **Step 4: Add the minimal package and health implementation**

Create `backend/src/projectb/__init__.py`:

```python
__version__ = "0.1.0"
```

Create `backend/src/projectb/api/__init__.py`:

```python
"""ProjectB HTTP boundary."""
```

Create `backend/src/projectb/api/app.py`:

```python
from fastapi import FastAPI


def create_app(profile: str = "local") -> FastAPI:
    app = FastAPI()

    @app.get("/api/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "profile": profile}

    return app


app = create_app()
```

- [ ] **Step 5: Run the minimal health implementation green**

Run the green through `Invoke-CheckedNative` with `$PythonExe`, arguments `@("-m", "pytest", "backend/tests/unit/test_health.py", "-q")`, and a 300-second timeout.

Expected: the focused health test passes.

- [ ] **Step 6: Refactor the response into an explicit schema**

Replace `backend/src/projectb/api/app.py` with:

```python
from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict


class HealthResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    status: str
    profile: str


def create_app(profile: str = "local") -> FastAPI:
    app = FastAPI()

    @app.get("/api/health", response_model=HealthResponse)
    def health() -> HealthResponse:
        return HealthResponse(status="ok", profile=profile)

    return app


app = create_app()
```

- [ ] **Step 7: Reverify health, Ruff, and mypy with explicit config paths**

Run:

```powershell
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "-m", "pytest", "backend/tests/unit/test_toolchain_contract.py",
    "backend/tests/unit/test_health.py", "-q"
) -TimeoutSeconds 300 -FailureMessage "T-01B regression tests failed"
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "-m", "ruff", "check", "--config", "backend/pyproject.toml",
    "backend/src/projectb", "backend/tests/unit/test_health.py"
) -TimeoutSeconds 300 -FailureMessage "T-01B Ruff failed"
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "-m", "mypy", "--config-file", "backend/pyproject.toml", "backend/src/projectb"
) -TimeoutSeconds 300 -FailureMessage "T-01B mypy failed"
```

Expected: every focused backend test passes; Ruff and mypy both exit 0.

- [ ] **Step 8: Prepare the T-01B SPEC review packet without dispatching**

Prepare the formal inputs and questions for the health/profile contract, local-only boundary, AC-10 foundation role, and file ownership. Do not dispatch until Step 10 has produced the exact staged diff and tree ID.

- [ ] **Step 9: Prepare the T-01B quality review packet without dispatching**

Prepare the distinct quality questions for FastAPI lifecycle, schema correctness, test quality, import/package boundaries, static analysis, dependency/license use, and absence of network behavior. Do not dispatch before final staging.

- [ ] **Step 10: Stage exactly four paths and run the bootstrap staged-secret scan**

Run:

```powershell
$paths = @(
    "backend/src/projectb/__init__.py",
    "backend/src/projectb/api/__init__.py",
    "backend/src/projectb/api/app.py",
    "backend/tests/unit/test_health.py"
)
Invoke-CheckedGit -ArgumentList (@("add", "--") + $paths) -FailureMessage "T-01B git add failed"
Invoke-CheckedGit -ArgumentList @("diff", "--cached", "--check") -FailureMessage "T-01B staged diff check failed"
Invoke-BootstrapStagedSecretScan -ExpectedPaths $paths
Assert-ExactStagedPaths -ExpectedPaths $paths
$reviewTree = Get-StagedTreeId
$reviewTree
$reviewPacket = Export-ReviewedStagedDiff -UnitId $env:PROJECTB_UNIT_ID `
    -ExpectedTreeId $reviewTree
$reviewPacket
```

Expected: scan/whitespace checks pass and exactly four paths are staged.

- [ ] **Step 11: Run both staged-tree reviews, revalidate, and commit T-01B**

Run:

```powershell
$ids = @(
    $env:PROJECTB_AGENT_ID,
    $env:PROJECTB_T01B_SPEC_REVIEW_ID,
    $env:PROJECTB_T01B_QUALITY_REVIEW_ID
)
Invoke-FinalPrecommitValidation -UnitId "T-01B" -ExpectedPaths $paths -Identities $ids `
    -SpecTreeId $env:PROJECTB_T01B_SPEC_REVIEW_TREE `
    -QualityTreeId $env:PROJECTB_T01B_QUALITY_REVIEW_TREE -ScannerMode "bootstrap"
Invoke-CheckedGit -ArgumentList @("commit", "-m", "feat(T-01B): add typed backend health scaffold [agent: $env:PROJECTB_AGENT_ID]") `
    -FailureMessage "T-01B commit failed"
$commitHash = Invoke-CheckedGitText -ArgumentList @("rev-parse", "HEAD") -FailureMessage "T-01B hash lookup failed"
Assert-CommittedTreeBinding -UnitId "T-01B" -ExpectedTreeId $env:PROJECTB_T01B_SPEC_REVIEW_TREE
if ($commitHash -notmatch "^[0-9a-f]{40}$") { throw "T-01B did not produce a full commit hash" }
$commitHash
```

Expected: one four-path T-01B commit and its actual hash.

### Task T-01C1: Add The Frontend Manifest, Config, And Complete Lock Materialization

**Unit prelude:** Run the complete Required Fail-Closed Command Prelude before Step 1 and reuse the four verified runtime paths. `$GitExe` is a separately resolved coordinator control-plane path used only by scan/stage wrappers.

**Goal:** Add exact npm/Vite/Vitest contracts and deterministically materialize the complete G-02A npm closure without creating application entry files.

**Dependencies / parallelism:** Requires the reviewed T-01A commit. May run in parallel with T-01B and T-01D. T-01C2 and T-01E1 depend on its reviewed commit.

**Files:**
- Create: `frontend/package.json`
- Create: `frontend/.npmrc`
- Create: `frontend/tsconfig.json`
- Create: `frontend/vitest.contract.json`
- Create: `frontend/vite.config.contract.json`
- Create: `frontend/vite.config.ts`
- Generate: `frontend/package-lock.json`
- Create: `scripts/frontend_lock_contract.mjs`
- Create: `scripts/materialize_frontend_lock.mjs`
- Test: `scripts/tests/frontend_contract.test.mjs`
- Test: `scripts/tests/frontend_lock_contract.test.mjs`

**Acceptance:** Package commands are exact and include owner-ready `e2e`; Vitest includes both `*.test.ts` and `*.test.tsx`; Vite config matches raw SHA-256 `219863494626f9af96f27257aae1b112d9d2f001e9d42de40f3c6d1c43633242` and its structured contract; npm source raw SHA is `071826d575cbcc472020a7df984e2e8f2410a75c1782550c5ddfeed268af3c2f`; the production npm lock is a byte-for-byte copy of that reviewed source; `--check` rematerializes all 166 non-root entries into an independent temporary directory and compares complete bytes without writing the production lock.

- [ ] **Step 1: Run the required prelude and verify T-01A/C1 worker identity**

Run:

```powershell
Assert-UnitContext -UnitId "T-01C1"
Assert-ValidIdentity -Role "T-01C1 worker" -Identity $env:PROJECTB_AGENT_ID
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "backend/tests/unit/test_toolchain_contract.py"
) -TimeoutSeconds 300 -FailureMessage "T-01C1 foundation contract failed"
Invoke-CheckedNative -FilePath $NodeExe -ArgumentList @("--version") `
    -TimeoutSeconds 30 -FailureMessage "T-01C1 Node invocation failed"
Invoke-CheckedNative -FilePath $NpmCmd -ArgumentList @("--version") `
    -TimeoutSeconds 30 -FailureMessage "T-01C1 npm invocation failed"
```

Expected: the four A tests pass; Node prints `v24.18.0`; npm prints `11.16.0`.

- [ ] **Step 2: Write the failing manifest and immutable Vite contract tests**

Create `scripts/tests/frontend_contract.test.mjs`:

```javascript
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { test } from "node:test";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "../..");
const expectedScripts = {
  dev: "vite --host 127.0.0.1",
  test: "vitest run",
  "test:lock": "node --test ../scripts/tests/frontend_lock_contract.test.mjs",
  build: "tsc --noEmit && vite build",
  preview: "vite preview --host 127.0.0.1",
  e2e: "playwright test",
};
const expectedVitest = {
  environment: "jsdom",
  globals: true,
  include: ["src/**/*.test.ts", "src/**/*.test.tsx"],
};
const expectedVite = `import react from "@vitejs/plugin-react";
import { defineConfig } from "vitest/config";

import testContract from "./vitest.contract.json";

export default defineConfig({
  plugins: [react()],
  server: {
    host: "127.0.0.1",
    port: 5173,
    strictPort: true,
  },
  preview: {
    host: "127.0.0.1",
    port: 4173,
    strictPort: true,
  },
  test: testContract,
});
`;
const expectedViteSha256 =
  "219863494626f9af96f27257aae1b112d9d2f001e9d42de40f3c6d1c43633242";

async function readJson(relativePath) {
  return JSON.parse(await readFile(resolve(root, relativePath), "utf8"));
}

test("package scripts are exact and owner-executable", async () => {
  const manifest = await readJson("frontend/package.json");
  assert.deepEqual(manifest.scripts, expectedScripts);
  assert.equal(manifest.engines.node, "24.18.0");
  assert.equal(manifest.engines.npm, "11.16.0");
});

test("Vitest structured contract includes TypeScript and TSX tests", async () => {
  assert.deepEqual(await readJson("frontend/vitest.contract.json"), expectedVitest);
});

test("Vite executable config matches the immutable byte contract", async () => {
  const bytes = await readFile(resolve(root, "frontend/vite.config.ts"));
  const contract = await readJson("frontend/vite.config.contract.json");
  assert.equal(bytes.toString("utf8"), expectedVite);
  assert.equal(createHash("sha256").update(bytes).digest("hex"), expectedViteSha256);
  assert.deepEqual(contract, {
    algorithm: "sha256",
    sha256: expectedViteSha256,
    bytes: 376,
    testContract: "vitest.contract.json",
  });
});
```

- [ ] **Step 3: Run the frontend contract tests red**

Run the red through `Invoke-CheckedNative` with `$NodeExe`, arguments `@("--test", "scripts/tests/frontend_contract.test.mjs")`, and a 600-second timeout.

Expected: all three subtests are discovered and the command exits nonzero because the frontend contract files are absent.

- [ ] **Step 4: Add the exact package manifest and npm policy**

Create `frontend/package.json`:

```json
{
  "name": "projectb-web",
  "version": "0.1.0",
  "private": true,
  "license": "UNLICENSED",
  "type": "module",
  "packageManager": "npm@11.16.0",
  "engines": {
    "node": "24.18.0",
    "npm": "11.16.0"
  },
  "scripts": {
    "dev": "vite --host 127.0.0.1",
    "test": "vitest run",
    "test:lock": "node --test ../scripts/tests/frontend_lock_contract.test.mjs",
    "build": "tsc --noEmit && vite build",
    "preview": "vite preview --host 127.0.0.1",
    "e2e": "playwright test"
  },
  "dependencies": {
    "lucide-react": "1.25.0",
    "react": "19.2.7",
    "react-dom": "19.2.7"
  },
  "devDependencies": {
    "@axe-core/playwright": "4.12.1",
    "@playwright/test": "1.61.1",
    "@testing-library/dom": "10.4.1",
    "@testing-library/react": "16.3.2",
    "@testing-library/user-event": "14.6.1",
    "@types/node": "24.13.3",
    "@types/react": "19.2.17",
    "@types/react-dom": "19.2.3",
    "@vitejs/plugin-react": "6.0.3",
    "jsdom": "29.1.1",
    "typescript": "7.0.2",
    "vite": "8.1.5",
    "vitest": "4.1.10"
  }
}
```

Create `frontend/.npmrc`:

```ini
engine-strict=true
ignore-scripts=true
audit=true
fund=false
save-exact=true
package-lock=true
```

- [ ] **Step 5: Add strict TypeScript and structured Vitest contracts**

Create `frontend/tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2023",
    "useDefineForClassFields": true,
    "lib": ["ES2023", "DOM", "DOM.Iterable"],
    "allowJs": false,
    "skipLibCheck": false,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "forceConsistentCasingInFileNames": true,
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "types": ["node"]
  },
  "include": ["src", "vite.config.ts"]
}
```

Create `frontend/vitest.contract.json`:

```json
{
  "environment": "jsdom",
  "globals": true,
  "include": ["src/**/*.test.ts", "src/**/*.test.tsx"]
}
```

- [ ] **Step 6: Add the immutable Vite byte contract and executable config**

Create `frontend/vite.config.contract.json`:

```json
{
  "algorithm": "sha256",
  "sha256": "219863494626f9af96f27257aae1b112d9d2f001e9d42de40f3c6d1c43633242",
  "bytes": 376,
  "testContract": "vitest.contract.json"
}
```

Create `frontend/vite.config.ts` with LF line endings and a final LF:

```typescript
import react from "@vitejs/plugin-react";
import { defineConfig } from "vitest/config";

import testContract from "./vitest.contract.json";

export default defineConfig({
  plugins: [react()],
  server: {
    host: "127.0.0.1",
    port: 5173,
    strictPort: true,
  },
  preview: {
    host: "127.0.0.1",
    port: 4173,
    strictPort: true,
  },
  test: testContract,
});
```

- [ ] **Step 7: Run the frontend contract tests green**

Run the green through `Invoke-CheckedNative` with `$NodeExe`, arguments `@("--test", "scripts/tests/frontend_contract.test.mjs")`, and a 600-second timeout.

Expected: every frontend manifest/config contract test passes.

- [ ] **Step 8: Write the failing complete-lock materializer tests**

Create `scripts/tests/frontend_lock_contract.test.mjs`:

```javascript
import assert from "node:assert/strict";
import { mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { test } from "node:test";

import { runMaterializer } from "../materialize_frontend_lock.mjs";

const root = resolve(import.meta.dirname, "../..");
const source = resolve(root, "docs/engineering/locks/frontend-package-lock.json");
const manifest = resolve(root, "frontend/package.json");
const approvedNode = resolve(process.env.PROJECTB_NODE_EXE ?? "");

assert.equal(resolve(process.execPath), approvedNode, "test child must use approved Node leaf");

function run(mode, sourcePath, outputPath) {
  try {
    runMaterializer([
      mode,
      "--source", sourcePath,
      "--manifest", manifest,
      "--output", outputPath,
    ]);
    return { status: 0, stderr: "" };
  } catch (error) {
    return { status: 2, stderr: `FRONTEND_LOCK_ERROR ${error.message}` };
  }
}

test("write and check compare the complete materialized output", async () => {
  const directory = await mkdtemp(join(tmpdir(), "projectb-lock-test-"));
  try {
    const output = join(directory, "package-lock.json");
    const written = run("--write", source, output);
    assert.equal(written.status, 0, written.stderr);
    const expected = await readFile(output);
    const checked = run("--check", source, output);
    assert.equal(checked.status, 0, checked.stderr);
    await writeFile(output, Buffer.concat([expected, Buffer.from(" ")]));
    assert.equal(run("--check", source, output).status, 2);
  } finally {
    await rm(directory, { recursive: true, force: true });
  }
});

test("a raw-byte change to the G-02A source is rejected", async () => {
  const directory = await mkdtemp(join(tmpdir(), "projectb-lock-source-"));
  try {
    const changedSource = join(directory, "source.json");
    await writeFile(changedSource, Buffer.concat([await readFile(source), Buffer.from("\n")]));
    const result = run("--write", changedSource, join(directory, "output.json"));
    assert.equal(result.status, 2);
    assert.match(result.stderr, /raw SHA-256 mismatch/);
  } finally {
    await rm(directory, { recursive: true, force: true });
  }
});
```

- [ ] **Step 9: Run the lock materializer tests red**

Run the red through `Invoke-CheckedNative` with `$NodeExe`, arguments `@("--test", "scripts/tests/frontend_lock_contract.test.mjs")`, and a 900-second timeout.

Expected: both tests are discovered and fail because the materializer modules are absent.

- [ ] **Step 10: Implement the pure complete-lock transformation**

Create `scripts/frontend_lock_contract.mjs`:

```javascript
import { createHash } from "node:crypto";
import { TextDecoder } from "node:util";

export const EXPECTED_SOURCE_SHA256 =
  "071826d575cbcc472020a7df984e2e8f2410a75c1782550c5ddfeed268af3c2f";
export const EXPECTED_SOURCE_BLOB_SHA1 =
  "c2c53ae64a720b84eb7ee7c56483070bcfa2cdb8";
export const EXPECTED_NON_ROOT_PACKAGES = 166;

export function rawSha256(bytes) {
  return createHash("sha256").update(bytes).digest("hex");
}

export function rawGitBlobSha1(bytes) {
  const header = Buffer.from(`blob ${bytes.length}\0`, "ascii");
  return createHash("sha1").update(header).update(bytes).digest("hex");
}

function parseStrictJson(bytes, label) {
  let text;
  try {
    text = new TextDecoder("utf-8", { fatal: true }).decode(bytes);
  } catch (error) {
    throw new Error(`${label} is not strict UTF-8: ${error.message}`);
  }
  return JSON.parse(text);
}

function sortedRecord(record) {
  if (record === undefined || record === null || Array.isArray(record)) {
    throw new Error("dependency record is missing or invalid");
  }
  return Object.fromEntries(
    Object.entries(record).sort(([left], [right]) => left.localeCompare(right)),
  );
}

function assertSameRecord(label, actual, expected) {
  if (JSON.stringify(sortedRecord(actual)) !== JSON.stringify(sortedRecord(expected))) {
    throw new Error(`${label} differs from the G-02A root dependency record`);
  }
}

export function materializeLock(sourceBytes, manifestBytes) {
  if (rawSha256(sourceBytes) !== EXPECTED_SOURCE_SHA256) {
    throw new Error("G-02A frontend lock raw SHA-256 mismatch");
  }
  if (rawGitBlobSha1(sourceBytes) !== EXPECTED_SOURCE_BLOB_SHA1) {
    throw new Error("G-02A frontend lock immutable blob mismatch");
  }
  const sourceLock = parseStrictJson(sourceBytes, "source lock");
  const manifest = parseStrictJson(manifestBytes, "frontend manifest");
  const sourceRoot = sourceLock.packages?.[""];
  if (sourceRoot === undefined) {
    throw new Error("G-02A frontend lock has no root package record");
  }
  assertSameRecord("dependencies", manifest.dependencies, sourceRoot.dependencies);
  assertSameRecord("devDependencies", manifest.devDependencies, sourceRoot.devDependencies);

  const nonRootCount = Object.keys(sourceLock.packages).filter(
    (key) => key !== "",
  ).length;
  if (nonRootCount !== EXPECTED_NON_ROOT_PACKAGES) {
    throw new Error("G-02A frontend closure package count mismatch");
  }
  const bytes = Buffer.from(sourceBytes);
  return { bytes, nonRootCount, sha256: rawSha256(bytes) };
}
```

- [ ] **Step 11: Implement `--write` and independent-temporary-directory `--check`**

Create `scripts/materialize_frontend_lock.mjs`:

```javascript
import { mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import { materializeLock } from "./frontend_lock_contract.mjs";

const scriptDirectory = dirname(fileURLToPath(import.meta.url));
const repositoryRoot = resolve(scriptDirectory, "..");

function parseArguments(argv) {
  const options = {
    mode: null,
    source: resolve(repositoryRoot, "docs/engineering/locks/frontend-package-lock.json"),
    manifest: resolve(repositoryRoot, "frontend/package.json"),
    output: resolve(repositoryRoot, "frontend/package-lock.json"),
  };
  for (let index = 0; index < argv.length; index += 1) {
    const argument = argv[index];
    if (argument === "--write" || argument === "--check") {
      if (options.mode !== null) throw new Error("choose exactly one mode");
      options.mode = argument;
      continue;
    }
    if (["--source", "--manifest", "--output"].includes(argument)) {
      const value = argv[index + 1];
      if (value === undefined) throw new Error(`${argument} requires a path`);
      options[argument.slice(2)] = resolve(value);
      index += 1;
      continue;
    }
    throw new Error(`unknown argument: ${argument}`);
  }
  if (options.mode === null) throw new Error("choose exactly one mode");
  return options;
}

function checkCompleteOutput(outputPath, expectedBytes) {
  const directory = mkdtempSync(join(tmpdir(), "projectb-lock-check-"));
  try {
    const independentOutput = join(directory, "package-lock.json");
    writeFileSync(independentOutput, expectedBytes);
    const rematerialized = readFileSync(independentOutput);
    const actual = readFileSync(outputPath);
    if (!actual.equals(rematerialized)) {
      throw new Error("materialized output raw bytes differ");
    }
  } finally {
    rmSync(directory, { recursive: true, force: true });
  }
}

export function runMaterializer(argv) {
  const options = parseArguments(argv);
  const result = materializeLock(
    readFileSync(options.source),
    readFileSync(options.manifest),
  );
  if (options.mode === "--write") {
    writeFileSync(options.output, result.bytes);
    if (!readFileSync(options.output).equals(result.bytes)) {
      throw new Error("written lock differs from materialized bytes");
    }
  } else {
    checkCompleteOutput(options.output, result.bytes);
  }
  return { options, result };
}

if (process.argv[1] !== undefined && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    const { options, result } = runMaterializer(process.argv.slice(2));
    process.stdout.write(
      `FRONTEND_LOCK_OK mode=${options.mode.slice(2)} packages=${result.nonRootCount} sha256=${result.sha256}\n`,
    );
  } catch (error) {
    process.stderr.write(`FRONTEND_LOCK_ERROR ${error.message}\n`);
    process.exitCode = 2;
  }
}
```

- [ ] **Step 12: Run the complete-lock tests green**

Run the green through `Invoke-CheckedNative` with `$NodeExe`, arguments `@("--test", "scripts/tests/frontend_lock_contract.test.mjs")`, and a 900-second timeout.

Expected: every complete-lock materializer test passes.

- [ ] **Step 13: Materialize the production lock and install with the resolved npm executable**

Run:

```powershell
Invoke-CheckedNative -FilePath $NodeExe -ArgumentList @(
    "scripts/materialize_frontend_lock.mjs", "--write"
) -TimeoutSeconds 900 -FailureMessage "T-01C1 lock materialization failed"
$before = (Get-FileHash -Algorithm SHA256 -LiteralPath frontend/package-lock.json).Hash
Invoke-CheckedNative -FilePath $NodeExe -ArgumentList @(
    "scripts/materialize_frontend_lock.mjs", "--check"
) -TimeoutSeconds 900 -FailureMessage "T-01C1 lock check failed"
$after = (Get-FileHash -Algorithm SHA256 -LiteralPath frontend/package-lock.json).Hash
if ($before -ne $after) { throw "Lock check modified the production output" }
Invoke-CheckedNative -FilePath $NpmCmd -ArgumentList @(
    "--prefix", "frontend", "ci", "--engine-strict", "--ignore-scripts"
) -TimeoutSeconds 1800 -FailureMessage "T-01C1 npm ci failed"
```

Expected: both materializer commands report 166 packages; hashes match; the resolved npm `ci` command exits 0 without lock mutation.

- [ ] **Step 14: Reverify the complete C1 contract and lock behavior**

Run:

```powershell
Invoke-CheckedNative -FilePath $NodeExe -ArgumentList @(
    "--test", "scripts/tests/frontend_contract.test.mjs"
) -TimeoutSeconds 600 -FailureMessage "T-01C1 frontend contract tests failed"
Invoke-CheckedNative -FilePath $NodeExe -ArgumentList @(
    "--test", "scripts/tests/frontend_lock_contract.test.mjs"
) -TimeoutSeconds 900 -FailureMessage "T-01C1 lock contract tests failed"
Invoke-CheckedNative -FilePath $NodeExe -ArgumentList @(
    "scripts/materialize_frontend_lock.mjs", "--check"
) -TimeoutSeconds 900 -FailureMessage "T-01C1 final lock check failed"
```

Expected: the contract tests pass, 166 non-root lock entries are checked in an independent temporary directory, and the production lock hash is unchanged.

- [ ] **Step 15: Prepare both C1 review packets without dispatching**

Prepare the shared formal inputs and distinct questions: SPEC checks dependency/config/lock acceptance and ownership; quality checks raw bytes, temporary-directory isolation, npm safety, and secret handling. Do not dispatch until Step 16 has produced the exact staged diff and tree ID.

- [ ] **Step 16: Stage exactly 11 C1 paths and scan Git-index content**

Run the required prelude, then:

```powershell
$paths = @(
    "frontend/package.json", "frontend/.npmrc", "frontend/tsconfig.json",
    "frontend/vitest.contract.json", "frontend/vite.config.contract.json",
    "frontend/vite.config.ts", "frontend/package-lock.json",
    "scripts/frontend_lock_contract.mjs", "scripts/materialize_frontend_lock.mjs",
    "scripts/tests/frontend_contract.test.mjs", "scripts/tests/frontend_lock_contract.test.mjs"
)
Invoke-CheckedGit -ArgumentList (@("add", "--") + $paths) -FailureMessage "T-01C1 git add failed"
Invoke-CheckedGit -ArgumentList @("diff", "--cached", "--check") -FailureMessage "T-01C1 staged diff check failed"
Invoke-BootstrapStagedSecretScan -ExpectedPaths $paths
Assert-ExactStagedPaths -ExpectedPaths $paths
$reviewTree = Get-StagedTreeId
$reviewTree
$reviewPacket = Export-ReviewedStagedDiff -UnitId $env:PROJECTB_UNIT_ID `
    -ExpectedTreeId $reviewTree
$reviewPacket
```

The scan reads index blobs (`--cached`) and never worktree bytes.

- [ ] **Step 17: Run both staged-tree reviews, revalidate, and commit C1**

Run:

```powershell
$ids = @($env:PROJECTB_AGENT_ID, $env:PROJECTB_T01C1_SPEC_REVIEW_ID, $env:PROJECTB_T01C1_QUALITY_REVIEW_ID)
Invoke-FinalPrecommitValidation -UnitId "T-01C1" -ExpectedPaths $paths -Identities $ids `
    -SpecTreeId $env:PROJECTB_T01C1_SPEC_REVIEW_TREE `
    -QualityTreeId $env:PROJECTB_T01C1_QUALITY_REVIEW_TREE -ScannerMode "bootstrap"
Invoke-CheckedGit -ArgumentList @("commit", "-m", "build(T-01C1): materialize frontend lock and config contracts [agent: $env:PROJECTB_AGENT_ID]") `
    -FailureMessage "T-01C1 commit failed"
$commitHash = Invoke-CheckedGitText -ArgumentList @("rev-parse", "HEAD") -FailureMessage "T-01C1 hash lookup failed"
Assert-CommittedTreeBinding -UnitId "T-01C1" -ExpectedTreeId $env:PROJECTB_T01C1_SPEC_REVIEW_TREE
if ($commitHash -notmatch "^[0-9a-f]{40}$") { throw "T-01C1 did not produce a full commit hash" }
$commitHash
```

Expected: one reviewed 11-path C1 commit and its actual hash.

### Task T-01C2: Add The Minimal React Application

**Unit prelude:** Run the complete Required Fail-Closed Command Prelude before Step 1 and reuse the four verified runtime paths. `$GitExe` is a separately resolved coordinator control-plane path used only by scan/stage wrappers.

**Goal:** Add exactly one renderable React application and its focused test on top of reviewed C1. This unit must not modify any C1 path, especially `frontend/package.json`.

**Dependencies / parallelism:** Requires the reviewed T-01C1 commit. May run in parallel with T-01B and T-01D after C1; T-01F1 depends on this reviewed commit.

**Files:**
- Create: `frontend/index.html`
- Create: `frontend/src/main.tsx`
- Create: `frontend/src/app/App.tsx`
- Test: `frontend/src/app/App.test.tsx`

**Acceptance:** The focused React test renders the stable heading and the C1 production build succeeds; no package/config/lock/script file is edited.

- [ ] **Step 1: Run the required prelude and verify C1/C2 worker identity**

Run the required prelude, then:

```powershell
Assert-UnitContext -UnitId "T-01C2"
Assert-ValidIdentity -Role "T-01C2 worker" -Identity $env:PROJECTB_AGENT_ID
Invoke-CheckedNative -FilePath $NodeExe -ArgumentList @("--version") `
    -TimeoutSeconds 30 -FailureMessage "T-01C2 Node invocation failed"
Invoke-CheckedNative -FilePath $NpmCmd -ArgumentList @("--version") `
    -TimeoutSeconds 30 -FailureMessage "T-01C2 npm invocation failed"
Invoke-CheckedNative -FilePath $NodeExe -ArgumentList @(
    "--test", "scripts/tests/frontend_contract.test.mjs",
    "scripts/tests/frontend_lock_contract.test.mjs"
) -TimeoutSeconds 600 -FailureMessage "T-01C2 C1 contracts failed"
```

The shared context assertion proves the four owned paths and complete staged index are clean before writing code.

- [ ] **Step 2: Write the failing React render test**

Create `frontend/src/app/App.test.tsx`:

```tsx
import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";

import { App } from "./App";

afterEach(() => cleanup());

describe("App", () => {
  it("renders the ProjectB product name", () => {
    render(<App />);
    expect(screen.getByRole("heading", { level: 1, name: "ProjectB" })).toBeTruthy();
  });
});
```

Run the red through `Invoke-CheckedNative` with `$NpmCmd`, arguments `@("--prefix", "frontend", "run", "test", "--", "src/app/App.test.tsx")`, and a 600-second timeout.

Expected: one test file is discovered and fails because `App.tsx` is absent.

- [ ] **Step 3: Add the minimal React app and run its focused test green**

Create `frontend/src/app/App.tsx`:

```tsx
export function App() {
  return (
    <main>
      <h1>ProjectB</h1>
    </main>
  );
}
```

Run the green through `Invoke-CheckedNative` with `$NpmCmd`, arguments `@("--prefix", "frontend", "run", "test", "--", "src/app/App.test.tsx")`, and a 600-second timeout.

Expected: the focused React render test passes.

- [ ] **Step 4: Run the production build red before adding entry files**

Run the build through `Invoke-CheckedNative` with `$NpmCmd`, arguments `@("--prefix", "frontend", "run", "build")`, and a 900-second timeout.

Expected: nonzero exit because `frontend/index.html` is absent; a TypeScript/Vite contract error is not acceptable red evidence.

- [ ] **Step 5: Add the Vite document and React bootstrap**

Create `frontend/index.html`:

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>ProjectB</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

Create `frontend/src/main.tsx`:

```tsx
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import { App } from "./app/App";

const rootElement = document.getElementById("root");
if (rootElement === null) throw new Error("ProjectB root element is missing");

createRoot(rootElement).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
```

- [ ] **Step 6: Reverify C2 focused and full frontend behavior**

Run:

```powershell
Invoke-CheckedNative -FilePath $NpmCmd -ArgumentList @(
    "--prefix", "frontend", "run", "test", "--", "src/app/App.test.tsx"
) -TimeoutSeconds 600 -FailureMessage "T-01C2 focused frontend test failed"
Invoke-CheckedNative -FilePath $NpmCmd -ArgumentList @(
    "--prefix", "frontend", "run", "test"
) -TimeoutSeconds 900 -FailureMessage "T-01C2 frontend tests failed"
Invoke-CheckedNative -FilePath $NpmCmd -ArgumentList @(
    "--prefix", "frontend", "run", "build"
) -TimeoutSeconds 900 -FailureMessage "T-01C2 frontend build failed"
```

Expected: the focused test passes, the full frontend test command passes, and the production build exits 0.

- [ ] **Step 7: Prepare the T-01C2 SPEC review packet without dispatching**

Prepare the formal inputs and questions for the minimal WebUI entry, render contract, build behavior, and strict path ownership. Do not dispatch until Step 9 has produced the exact staged diff and tree ID.

- [ ] **Step 8: Prepare the T-01C2 quality review packet without dispatching**

Prepare the distinct quality questions for React bootstrap correctness, null-root failure, test isolation, accessibility, build output, and proof that `frontend/package.json` was not changed. Do not dispatch before final staging.

- [ ] **Step 9: Stage exactly four C2 paths and scan Git-index content**

Run:

```powershell
$paths = @(
    "frontend/index.html", "frontend/src/main.tsx",
    "frontend/src/app/App.tsx", "frontend/src/app/App.test.tsx"
)
Invoke-CheckedGit -ArgumentList (@("add", "--") + $paths) -FailureMessage "T-01C2 git add failed"
Invoke-CheckedGit -ArgumentList @("diff", "--cached", "--check") -FailureMessage "T-01C2 staged diff check failed"
Invoke-BootstrapStagedSecretScan -ExpectedPaths $paths
Assert-ExactStagedPaths -ExpectedPaths $paths
$reviewTree = Get-StagedTreeId
$reviewTree
$reviewPacket = Export-ReviewedStagedDiff -UnitId $env:PROJECTB_UNIT_ID `
    -ExpectedTreeId $reviewTree
$reviewPacket
```

Expected: scan/whitespace checks pass and exactly four C2 paths are staged; the scan reads index blobs rather than worktree bytes.

- [ ] **Step 10: Run both staged-tree reviews, revalidate, and commit T-01C2**

Run:

```powershell
$ids = @(
    $env:PROJECTB_AGENT_ID,
    $env:PROJECTB_T01C2_SPEC_REVIEW_ID,
    $env:PROJECTB_T01C2_QUALITY_REVIEW_ID
)
Invoke-FinalPrecommitValidation -UnitId "T-01C2" -ExpectedPaths $paths -Identities $ids `
    -SpecTreeId $env:PROJECTB_T01C2_SPEC_REVIEW_TREE `
    -QualityTreeId $env:PROJECTB_T01C2_QUALITY_REVIEW_TREE -ScannerMode "bootstrap"
Invoke-CheckedGit -ArgumentList @("commit", "-m", "build(T-01C2): add minimal tested frontend [agent: $env:PROJECTB_AGENT_ID]") `
    -FailureMessage "T-01C2 commit failed"
$commitHash = Invoke-CheckedGitText -ArgumentList @("rev-parse", "HEAD") -FailureMessage "T-01C2 hash lookup failed"
Assert-CommittedTreeBinding -UnitId "T-01C2" -ExpectedTreeId $env:PROJECTB_T01C2_SPEC_REVIEW_TREE
if ($commitHash -notmatch "^[0-9a-f]{40}$") { throw "T-01C2 did not produce a full commit hash" }
$commitHash
```

Expected: one four-path T-01C2 commit and its actual hash.

### Task T-01D: Add The Fail-Closed Strict Secret Scanner

**Unit prelude:** Run the complete Required Fail-Closed Command Prelude before Step 1 and reuse the four verified runtime paths. `$GitExe` is a separately resolved coordinator control-plane path used only by scan/stage wrappers.

**Goal:** Add a redacting scanner that handles the complete allowed-text inventory, strict BOM-aware decoding, path containment, and reparse/symlink rejection with deterministic 0/1/2 exit codes.

**Dependencies / parallelism:** Requires the reviewed T-01A commit. May run in parallel with T-01B and T-01C1. T-01F1 depends on its reviewed commit; T-01E1/E2 do not.

**Files:**
- Create: `scripts/secret_scan/__init__.py`
- Create: `scripts/secret_scan/encoding.py`
- Create: `scripts/secret_scan/paths.py`
- Create: `scripts/secret_scan/rules.py`
- Create: `scripts/scan_secrets.py`
- Create: `scripts/scan_secrets.ps1`
- Test: `backend/tests/unit/test_secret_scanner.py`

**Acceptance:** Normal mode scans tracked plus untracked/nonignored worktree files. `--staged` parses `git ls-files --stage -z` through the approved `$GitExe`, accepts only stage-0 regular modes `100644`/`100755`, reads each object ID with `git cat-file blob`, and never reads worktree bytes; malformed index/blob data or symlink mode `120000` exits 2. Tracked `.env`/`.env.*` are scanned even when force-added. `.lock`, `.sql`, `.sh`, `.bat`, and `.cmd` are included; UTF-8-BOM, UTF-16-LE-BOM, and UTF-16-BE-BOM have separate tests; broad RSA/EC/DSA/OPENSSH/ENCRYPTED/generic private-key headers match. A redacted finding exits 1; clean text exits 0; values and raw paths are never printed. Every scanner invocation uses the bounded native wrapper and passes `--git-exe $GitExe`.

- [ ] **Step 1: Verify T-01A and worker identity**

Run:

```powershell
Assert-UnitContext -UnitId "T-01D"
Assert-ValidIdentity -Role "T-01D worker" -Identity $env:PROJECTB_AGENT_ID
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @("--version") `
    -TimeoutSeconds 30 -FailureMessage "T-01D Python invocation failed"
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "-m", "pip", "install", "--require-hashes", "-r", "backend/requirements-windows-x64.lock"
) -TimeoutSeconds 1800 -FailureMessage "T-01D locked install failed"
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "-m", "pip", "install", "--no-deps", "-e", "backend[test,quality,build]"
) -TimeoutSeconds 600 -FailureMessage "T-01D editable install failed"
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "backend/tests/unit/test_toolchain_contract.py"
) -TimeoutSeconds 300 -FailureMessage "T-01D foundation contract failed"
```

Expected: Python is 3.14.6 and all 4 T-01A contract tests pass.

- [ ] **Step 2a: Write scanner harness, clean-file, encoding, and redaction tests**

Create `backend/tests/unit/test_secret_scanner.py`:

```python
import importlib
import os
import stat
import subprocess
import sys
import time
from pathlib import Path

import psutil
import pytest
import scripts.secret_scan.paths as secret_paths
from scripts.secret_scan.paths import PathSecurityError

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
SCANNER = REPOSITORY_ROOT / "scripts" / "scan_secrets.py"
TEXT_EXTENSIONS = (".lock", ".sql", ".sh", ".bat", ".cmd")
PYTHON_EXE = Path(os.environ["PROJECTB_PYTHON_EXE"]).resolve(strict=True)
GIT_EXE = Path(os.environ["PROJECTB_CONTROL_GIT_EXE"]).resolve(strict=True)
SAFE_ENVIRONMENT = {
    key: value
    for key in ("SYSTEMROOT", "WINDIR", "TEMP", "TMP", "USERPROFILE", "HOME")
    if (value := os.environ.get(key))
}
SAFE_ENVIRONMENT["GIT_CONFIG_NOSYSTEM"] = "1"


def marker() -> str:
    return "PROJECTB_SYNTHETIC_" + "CREDENTIAL_MARKER"


def private_key_header(prefix: str = "") -> str:
    qualifier = f"{prefix} " if prefix else ""
    return "".join(("-----BEGIN ", qualifier, "PRIVATE", " KEY-----"))


def terminate_process_tree(process: subprocess.Popen[str]) -> None:
    try:
        descendants = psutil.Process(process.pid).children(recursive=True)
    except psutil.Error:
        descendants = []
    for child in reversed(descendants):
        try:
            child.kill()
        except psutil.Error:
            continue
    try:
        process.kill()
    except OSError:
        pass
    psutil.wait_procs(descendants, timeout=5.0)


def run_process(
    command: list[str],
    *,
    cwd: Path | None = None,
    input_text: str | None = None,
    check: bool = False,
) -> subprocess.CompletedProcess[str]:
    process = subprocess.Popen(
        command,
        cwd=cwd,
        stdin=subprocess.PIPE if input_text is not None else None,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=SAFE_ENVIRONMENT,
    )
    try:
        stdout, stderr = process.communicate(input=input_text, timeout=60)
    except subprocess.TimeoutExpired:
        terminate_process_tree(process)
        raise
    result = subprocess.CompletedProcess(command, process.returncode, stdout, stderr)
    if check:
        result.check_returncode()
    return result


def run_scanner(root: Path, candidate: Path | None = None) -> subprocess.CompletedProcess[str]:
    assert Path(sys.executable).resolve(strict=True) == PYTHON_EXE
    command = [
        str(PYTHON_EXE),
        str(SCANNER),
        "--root",
        str(root),
        "--git-exe",
        str(GIT_EXE),
    ]
    if candidate is not None:
        command.extend(["--candidate", str(candidate)])
    return run_process(command)


def combined(result: subprocess.CompletedProcess[str]) -> str:
    return result.stdout + result.stderr


def test_clean_utf8_text_exits_zero(tmp_path: Path) -> None:
    (tmp_path / "clean.txt").write_text("ordinary project text", encoding="utf-8")
    assert run_scanner(tmp_path).returncode == 0


def test_repository_scans_itself_without_fixture_false_positive() -> None:
    result = run_scanner(REPOSITORY_ROOT)
    assert result.returncode == 0, combined(result)


def test_utf8_marker_is_redacted_and_exits_one(tmp_path: Path) -> None:
    value = marker()
    (tmp_path / "finding.py").write_text(value, encoding="utf-8")
    result = run_scanner(tmp_path)
    assert result.returncode == 1
    assert "rule=synthetic-marker" in combined(result)
    assert value not in combined(result)


def test_utf8_bom_marker_is_detected_without_value_output(tmp_path: Path) -> None:
    value = marker()
    (tmp_path / "finding.txt").write_bytes(b"\xef\xbb\xbf" + value.encode("utf-8"))
    result = run_scanner(tmp_path)
    assert result.returncode == 1
    assert "rule=synthetic-marker" in combined(result)
    assert value not in combined(result)


def test_utf16le_bom_marker_is_detected_without_value_output(tmp_path: Path) -> None:
    value = marker()
    (tmp_path / "finding.txt").write_bytes(b"\xff\xfe" + value.encode("utf-16-le"))
    result = run_scanner(tmp_path)
    assert result.returncode == 1
    assert "rule=synthetic-marker" in combined(result)
    assert value not in combined(result)


def test_utf16be_bom_marker_is_detected_without_value_output(tmp_path: Path) -> None:
    value = marker()
    (tmp_path / "finding.txt").write_bytes(b"\xfe\xff" + value.encode("utf-16-be"))
    result = run_scanner(tmp_path)
    assert result.returncode == 1
    assert "rule=synthetic-marker" in combined(result)
    assert value not in combined(result)

```

- [ ] **Step 2b: Append malformed-input, in-process path/CLI boundary, extension, and key-header tests**

Append to `backend/tests/unit/test_secret_scanner.py`:

```python


def test_malformed_allowed_text_exits_two(tmp_path: Path) -> None:
    (tmp_path / "malformed.txt").write_bytes(b"\x80")
    result = run_scanner(tmp_path)
    assert result.returncode == 2
    assert "kind=invalid_encoding" in combined(result)


def test_no_bom_nul_exits_two(tmp_path: Path) -> None:
    (tmp_path / "nul.sql").write_bytes(b"left\x00right")
    result = run_scanner(tmp_path)
    assert result.returncode == 2
    assert "kind=nul_without_bom" in combined(result)


def test_explicit_directory_read_failure_exits_two(tmp_path: Path) -> None:
    unreadable = tmp_path / "unreadable.txt"
    unreadable.mkdir()
    result = run_scanner(tmp_path, unreadable)
    assert result.returncode == 2
    assert "kind=read_failure" in combined(result)


def test_reparse_component_is_rejected_by_inventory_in_process(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    target = tmp_path / "target"
    target.mkdir()
    (target / "linked.txt").write_text("clean", encoding="utf-8")
    link = tmp_path / "linked"
    link.mkdir()
    real_lstat = os.lstat

    def fake_lstat(path: os.PathLike[str] | str) -> os.stat_result:
        observed = real_lstat(path)
        if Path(path) == link:
            values = list(observed)
            values[0] = stat.S_IFLNK | stat.S_IRUSR
            return os.stat_result(values)
        return observed

    monkeypatch.setattr(secret_paths.os, "lstat", fake_lstat)
    with pytest.raises(PathSecurityError) as captured:
        secret_paths.candidate_paths(tmp_path, [], GIT_EXE)
    assert captured.value.kind == "reparse_path"


def test_cli_reparse_error_is_exit_two_and_redacted_in_process(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.syspath_prepend(str(REPOSITORY_ROOT / "scripts"))
    scanner_module = importlib.import_module("scan_secrets")
    candidate = tmp_path / "linked.txt"
    candidate.write_text("clean", encoding="utf-8")

    def reject_reparse(_root: Path, _candidate: Path) -> Path:
        raise scanner_module.PathSecurityError("reparse_path")

    monkeypatch.setattr(scanner_module, "assert_secure_file", reject_reparse)
    exit_code = scanner_module.main(
        [
            "--root",
            str(tmp_path),
            "--candidate",
            str(candidate),
            "--git-exe",
            str(GIT_EXE),
        ]
    )
    output = capsys.readouterr().out
    assert exit_code == 2
    assert "kind=reparse_path" in output
    assert "path_sha256=" in output
    assert str(candidate) not in output


@pytest.mark.parametrize("extension", TEXT_EXTENSIONS)
def test_required_text_extension_is_scanned(tmp_path: Path, extension: str) -> None:
    value = marker()
    (tmp_path / f"finding{extension}").write_text(value, encoding="utf-8")
    result = run_scanner(tmp_path)
    assert result.returncode == 1
    assert value not in combined(result)


@pytest.mark.parametrize("header", ("RSA", "EC", "DSA", "OPENSSH", "ENCRYPTED"))
def test_private_key_header_families_are_detected(tmp_path: Path, header: str) -> None:
    (tmp_path / f"key-{header}.txt").write_text(
        private_key_header(header), encoding="utf-8"
    )
    result = run_scanner(tmp_path)
    assert result.returncode == 1
    assert "rule=private-key-header" in combined(result)


def test_generic_private_key_header_is_detected(tmp_path: Path) -> None:
    (tmp_path / "generic-key.txt").write_text(
        private_key_header(), encoding="utf-8"
    )
    result = run_scanner(tmp_path)
    assert result.returncode == 1
    assert "rule=private-key-header" in combined(result)

```

- [ ] **Step 2c: Append bounded Git and staged-index tests**

Append to `backend/tests/unit/test_secret_scanner.py`:

```python


def git_repo(root: Path) -> None:
    run_process([str(GIT_EXE), "init", "--quiet"], cwd=root, check=True)
    run_process(
        [str(GIT_EXE), "config", "user.email", "test@example.invalid"],
        cwd=root,
        check=True,
    )
    run_process(
        [str(GIT_EXE), "config", "user.name", "ProjectB Test"],
        cwd=root,
        check=True,
    )


def test_git_timeout_terminates_descendant_process(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    pid_file = tmp_path / "git-child.pid"
    heartbeat = tmp_path / "git-heartbeat.txt"
    child = (
        "import os,time; from pathlib import Path; "
        f"Path({str(pid_file)!r}).write_text(str(os.getpid())); "
        f"p=Path({str(heartbeat)!r}); "
        "[(p.write_text(str(i)), time.sleep(0.05)) for i in range(400)]"
    )
    parent = (
        "import subprocess,sys,time; "
        f"subprocess.Popen([sys.executable, '-c', {child!r}]); time.sleep(30)"
    )
    monkeypatch.setattr(secret_paths, "GIT_TIMEOUT_SECONDS", 0.5)
    with pytest.raises(PathSecurityError, match="inventory_failure"):
        secret_paths.run_git(tmp_path, PYTHON_EXE, ["-c", parent])
    for _ in range(20):
        if pid_file.is_file() and heartbeat.is_file():
            break
        time.sleep(0.05)
    child_pid = int(pid_file.read_text(encoding="utf-8"))
    previous = heartbeat.read_text(encoding="utf-8")
    time.sleep(0.2)
    assert not psutil.pid_exists(child_pid)
    assert heartbeat.read_text(encoding="utf-8") == previous


def test_staged_secret_is_found_after_worktree_is_cleaned(tmp_path: Path) -> None:
    git_repo(tmp_path)
    value = marker()
    path = tmp_path / "tracked.txt"
    path.write_text(value, encoding="utf-8")
    run_process([str(GIT_EXE), "add", "tracked.txt"], cwd=tmp_path, check=True)
    path.write_text("clean", encoding="utf-8")
    result = run_scanner(tmp_path)
    assert result.returncode == 0
    staged = run_process(
        [
            str(PYTHON_EXE),
            str(SCANNER),
            "--root",
            str(tmp_path),
            "--staged",
            "--git-exe",
            str(GIT_EXE),
        ],
    )
    assert staged.returncode == 1


def test_staged_malformed_bytes_are_exit_two(tmp_path: Path) -> None:
    git_repo(tmp_path)
    path = tmp_path / "malformed.txt"
    path.write_bytes(b"\x80")
    run_process([str(GIT_EXE), "add", "malformed.txt"], cwd=tmp_path, check=True)
    result = run_process(
        [
            str(PYTHON_EXE),
            str(SCANNER),
            "--root",
            str(tmp_path),
            "--staged",
            "--git-exe",
            str(GIT_EXE),
        ],
    )
    assert result.returncode == 2


def test_staged_symlink_index_mode_is_exit_two(tmp_path: Path) -> None:
    git_repo(tmp_path)
    blob = run_process(
        [str(GIT_EXE), "hash-object", "-w", "--stdin"],
        cwd=tmp_path,
        input_text="target.txt",
        check=True,
    ).stdout.strip()
    run_process(
        [
            str(GIT_EXE),
            "update-index",
            "--add",
            "--cacheinfo",
            f"120000,{blob},linked.txt",
        ],
        cwd=tmp_path,
        check=True,
    )
    result = run_process(
        [
            str(PYTHON_EXE),
            str(SCANNER),
            "--root",
            str(tmp_path),
            "--staged",
            "--git-exe",
            str(GIT_EXE),
        ],
    )
    assert result.returncode == 2


def test_tracked_env_is_scanned_even_when_forced(tmp_path: Path) -> None:
    git_repo(tmp_path)
    path = tmp_path / ".env"
    path.write_text(marker(), encoding="utf-8")
    run_process([str(GIT_EXE), "add", "-f", ".env"], cwd=tmp_path, check=True)
    result = run_process(
        [
            str(PYTHON_EXE),
            str(SCANNER),
            "--root",
            str(tmp_path),
            "--staged",
            "--git-exe",
            str(GIT_EXE),
        ],
    )
    assert result.returncode == 1
```

- [ ] **Step 3: Run all scanner tests red**

Run the red through `Invoke-CheckedNative` with `$PythonExe`, arguments `@("-m", "pytest", "backend/tests/unit/test_secret_scanner.py", "-q")`, and a 600-second timeout.

Expected: the complete scanner boundary suite is collected and exits nonzero because the scanner entry is absent. A junction-creation permission error is an environment blocker, not acceptable red evidence.

- [ ] **Step 4: Create the scanner package marker**

Create `scripts/secret_scan/__init__.py`:

```python
"""Strict ProjectB repository scanning helpers."""
```

- [ ] **Step 5: Implement strict BOM-aware decoding and no-BOM NUL rejection**

Create `scripts/secret_scan/encoding.py`:

```python
from pathlib import Path


class TextDecodeError(RuntimeError):
    def __init__(self, kind: str) -> None:
        super().__init__(kind)
        self.kind = kind


def decode_project_bytes(data: bytes) -> str:
    if data.startswith((b"\xff\xfe\x00\x00", b"\x00\x00\xfe\xff")):
        raise TextDecodeError("invalid_encoding")
    try:
        if data.startswith(b"\xef\xbb\xbf"):
            return data[3:].decode("utf-8", errors="strict")
        if data.startswith(b"\xff\xfe"):
            return data[2:].decode("utf-16-le", errors="strict")
        if data.startswith(b"\xfe\xff"):
            return data[2:].decode("utf-16-be", errors="strict")
        if b"\x00" in data:
            raise TextDecodeError("nul_without_bom")
        return data.decode("utf-8", errors="strict")
    except UnicodeDecodeError as error:
        raise TextDecodeError("invalid_encoding") from error


def decode_project_text(path: Path) -> str:
    try:
        return decode_project_bytes(path.read_bytes())
    except OSError as error:
        raise TextDecodeError("read_failure") from error
```

- [ ] **Step 6a: Implement containment, reparse rejection, and text eligibility**

Create `scripts/secret_scan/paths.py`:

```python
import os
import stat
import subprocess
from dataclasses import dataclass
from pathlib import Path

import psutil

REPARSE_POINT_ATTRIBUTE = 0x400
GIT_TIMEOUT_SECONDS = 30.0
ALLOWED_EXTENSIONS = frozenset(
    {
        ".bat", ".cfg", ".cmd", ".css", ".csv", ".html", ".ini", ".js",
        ".json", ".jsx", ".lock", ".md", ".mjs", ".ps1", ".psm1", ".py",
        ".sh", ".sql", ".toml", ".ts", ".tsx", ".txt", ".xml", ".yaml",
        ".yml",
    }
)
ALLOWED_NAMES = frozenset(
    {
        ".dockerignore",
        ".env.example",
        ".gitignore",
        ".npmrc",
        "Dockerfile",
        "LICENSE",
        "Makefile",
        "NOTICE",
    }
)


class PathSecurityError(RuntimeError):
    def __init__(self, kind: str) -> None:
        super().__init__(kind)
        self.kind = kind


def absolute_without_resolving(path: Path) -> Path:
    return Path(os.path.abspath(os.fspath(path)))


def is_reparse_or_symlink(path: Path) -> bool:
    try:
        metadata = os.lstat(path)
    except OSError as error:
        raise PathSecurityError("read_failure") from error
    attributes = getattr(metadata, "st_file_attributes", 0)
    return stat.S_ISLNK(metadata.st_mode) or bool(attributes & REPARSE_POINT_ATTRIBUTE)


def assert_secure_file(root: Path, candidate: Path) -> Path:
    root_absolute = absolute_without_resolving(root)
    candidate_absolute = absolute_without_resolving(candidate)
    try:
        common = Path(os.path.commonpath((root_absolute, candidate_absolute)))
    except ValueError as error:
        raise PathSecurityError("path_escape") from error
    if os.path.normcase(common) != os.path.normcase(root_absolute):
        raise PathSecurityError("path_escape")

    chain = list(reversed(root_absolute.parents)) + [root_absolute]
    current = root_absolute
    for part in candidate_absolute.relative_to(root_absolute).parts:
        current /= part
        chain.append(current)
    seen: set[Path] = set()
    for component in chain:
        if component in seen:
            continue
        seen.add(component)
        if is_reparse_or_symlink(component):
            raise PathSecurityError("reparse_path")
    if not candidate_absolute.is_file():
        raise PathSecurityError("read_failure")
    return candidate_absolute


def is_allowed_text(path: Path) -> bool:
    name = path.name.lower()
    return (
        name == ".env"
        or name.startswith(".env.")
        or path.name in ALLOWED_NAMES
        or path.suffix.lower() in ALLOWED_EXTENSIONS
    )

```

- [ ] **Step 6b: Append staged-blob records and bounded Git execution**

Append to `scripts/secret_scan/paths.py`:

```python


@dataclass(frozen=True)
class StagedBlob:
    path: Path
    mode: str
    data: bytes


def approved_git_executable(candidate: Path) -> Path:
    if not candidate.is_absolute() or candidate.name.casefold() != "git.exe":
        raise PathSecurityError("inventory_failure")
    try:
        resolved = candidate.resolve(strict=True)
    except OSError as error:
        raise PathSecurityError("inventory_failure") from error
    if not resolved.is_file():
        raise PathSecurityError("inventory_failure")
    return resolved


def git_environment() -> dict[str, str]:
    environment = {
        key: value
        for key in ("SYSTEMROOT", "WINDIR", "TEMP", "TMP", "USERPROFILE", "HOME")
        if (value := os.environ.get(key))
    }
    environment["GIT_CONFIG_NOSYSTEM"] = "1"
    environment["GIT_TERMINAL_PROMPT"] = "0"
    return environment


def terminate_process_tree(process: subprocess.Popen[bytes]) -> None:
    try:
        parent = psutil.Process(process.pid)
        descendants = parent.children(recursive=True)
    except psutil.Error:
        descendants = []
    for child in reversed(descendants):
        try:
            child.kill()
        except psutil.Error:
            continue
    try:
        process.kill()
    except OSError:
        pass
    psutil.wait_procs(descendants, timeout=5.0)
    try:
        process.wait(timeout=5.0)
    except subprocess.TimeoutExpired:
        pass


def run_git(root: Path, git: Path, arguments: list[str]) -> subprocess.CompletedProcess[bytes]:
    try:
        process = subprocess.Popen(
            [str(git), *arguments],
            cwd=root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=git_environment(),
        )
    except OSError as error:
        raise PathSecurityError("inventory_failure") from error
    try:
        stdout, stderr = process.communicate(timeout=GIT_TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired as error:
        terminate_process_tree(process)
        raise PathSecurityError("inventory_failure") from error
    return subprocess.CompletedProcess(
        [str(git), *arguments],
        process.returncode if process.returncode is not None else 127,
        stdout,
        stderr,
    )

```

- [ ] **Step 6c: Append Git, staged, filesystem, and explicit inventories**

Append to `scripts/secret_scan/paths.py`:

```python


def git_inventory(root: Path, git_executable: Path) -> list[Path]:
    git = approved_git_executable(git_executable)
    result = run_git(
        root=root,
        git=git,
        arguments=[
            "-c", "core.quotepath=false", "ls-files", "-z", "--cached",
            "--others", "--exclude-standard",
        ],
    )
    if result.returncode != 0:
        raise PathSecurityError("inventory_failure")
    return [root / os.fsdecode(item) for item in result.stdout.split(b"\x00") if item]


def staged_inventory(root: Path, git_executable: Path) -> list[StagedBlob]:
    git = approved_git_executable(git_executable)
    listing = run_git(
        root,
        git,
        ["-c", "core.quotepath=false", "ls-files", "--stage", "-z"],
    )
    if listing.returncode != 0:
        raise PathSecurityError("inventory_failure")
    blobs: list[StagedBlob] = []
    for record in (item for item in listing.stdout.split(b"\x00") if item):
        try:
            metadata, raw_path = record.split(b"\t", 1)
            mode, object_id, stage = metadata.decode("ascii").split(" ")
        except (UnicodeError, ValueError) as error:
            raise PathSecurityError("index_record") from error
        if stage != "0" or mode not in {"100644", "100755"}:
            raise PathSecurityError("index_mode")
        decoded_path = os.fsdecode(raw_path)
        relative_path = Path(decoded_path)
        if relative_path.is_absolute() or ".." in relative_path.parts:
            raise PathSecurityError("path_escape")
        content = run_git(root, git, ["cat-file", "blob", object_id])
        if content.returncode != 0:
            raise PathSecurityError("index_blob")
        blobs.append(StagedBlob(root / relative_path, mode, content.stdout))
    return blobs


def filesystem_inventory(root: Path) -> list[Path]:
    paths: list[Path] = []
    for directory, names, files in os.walk(root, topdown=True, followlinks=False):
        base = Path(directory)
        for name in names:
            child = base / name
            if is_reparse_or_symlink(child):
                raise PathSecurityError("reparse_path")
        paths.extend(base / name for name in files)
    return paths


def candidate_paths(root: Path, explicit: list[Path], git_executable: Path) -> list[Path]:
    root_absolute = absolute_without_resolving(root)
    if explicit:
        return [path if path.is_absolute() else root_absolute / path for path in explicit]
    if (root_absolute / ".git").exists():
        return git_inventory(root_absolute, git_executable)
    return filesystem_inventory(root_absolute)
```

- [ ] **Step 7: Implement value-free rule matching**

Create `scripts/secret_scan/rules.py`:

```python
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class SecretRule:
    identifier: str
    pattern: re.Pattern[str]


def secret_rules() -> tuple[SecretRule, ...]:
    synthetic = "PROJECTB_SYNTHETIC_" + "CREDENTIAL_MARKER"
    return (
        SecretRule("synthetic-marker", re.compile(re.escape(synthetic))),
        SecretRule(
            "openai-key-shape",
            re.compile(r"(?<![A-Za-z0-9])sk-(?:proj-)?[A-Za-z0-9_-]{20,}"),
        ),
        SecretRule(
            "aws-access-key-shape",
            re.compile(r"(?<![A-Z0-9])AKIA[0-9A-Z]{16}(?![A-Z0-9])"),
        ),
        SecretRule(
            "private-key-header",
            re.compile(r"-----BEGIN (?:[A-Z0-9]+ )*PRIVATE KEY-----"),
        ),
        SecretRule(
            "credential-assignment",
            re.compile(
                r"(?:api[_-]?key|token|password|secret)\s*[:=]\s*[\"'][^\"']{8,}",
                re.IGNORECASE,
            ),
        ),
    )


def matched_rule_ids(text: str) -> tuple[str, ...]:
    return tuple(rule.identifier for rule in secret_rules() if rule.pattern.search(text))
```

- [ ] **Step 8: Implement fail-closed scanner orchestration**

Create `scripts/scan_secrets.py`:

```python
import argparse
import hashlib
from collections.abc import Sequence
from pathlib import Path

from secret_scan.encoding import TextDecodeError, decode_project_bytes, decode_project_text
from secret_scan.paths import (
    PathSecurityError,
    assert_secure_file,
    candidate_paths,
    is_allowed_text,
    staged_inventory,
)
from secret_scan.rules import matched_rule_ids

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def path_fingerprint(path: Path) -> str:
    return hashlib.sha256(str(path).encode("utf-8", errors="surrogatepass")).hexdigest()


def parse_arguments(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scan ProjectB text without value output")
    parser.add_argument("--root", type=Path, default=REPOSITORY_ROOT)
    parser.add_argument("--candidate", type=Path, action="append", default=[])
    parser.add_argument("--staged", action="store_true")
    parser.add_argument("--git-exe", type=Path, required=True)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    arguments = parse_arguments(argv)
    has_error = False
    has_finding = False
    scanned = 0
    try:
        if arguments.staged and arguments.candidate:
            raise PathSecurityError("staged_candidate_conflict")
        inventory: list[tuple[Path, bytes | None]]
        if arguments.staged:
            inventory = [
                (item.path, item.data)
                for item in staged_inventory(arguments.root, arguments.git_exe)
            ]
        else:
            inventory = [
                (path, None)
                for path in candidate_paths(
                    arguments.root,
                    arguments.candidate,
                    arguments.git_exe,
                )
            ]
    except PathSecurityError as error:
        print(f"SECRET_SCAN_ERROR kind={error.kind}")
        return 2

    for candidate, staged_data in sorted(inventory, key=lambda value: str(value[0]).casefold()):
        fingerprint = path_fingerprint(candidate)
        try:
            if not is_allowed_text(candidate):
                continue
            if staged_data is not None:
                text = decode_project_bytes(staged_data)
            else:
                text = decode_project_text(assert_secure_file(arguments.root, candidate))
        except (PathSecurityError, TextDecodeError) as error:
            print(f"SECRET_SCAN_ERROR kind={error.kind} path_sha256={fingerprint}")
            has_error = True
            continue
        scanned += 1
        for rule_id in matched_rule_ids(text):
            print(f"SECRET_SCAN_FINDING rule={rule_id} path_sha256={fingerprint}")
            has_finding = True
    if has_error:
        return 2
    if has_finding:
        return 1
    print(f"SECRET_SCAN_OK files={scanned}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 9: Add the argument-safe PowerShell wrapper**

Create `scripts/scan_secrets.ps1`:

```powershell
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$PythonExe,
    [Parameter(Mandatory = $true)]
    [string]$GitExe,
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$ScannerArguments
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
function Test-FullyQualifiedPath {
    param([Parameter(Mandatory)][string]$Path)
    return [IO.Path]::IsPathRooted($Path) -and $Path -notmatch "^[A-Za-z]:[^\\/]"
}
foreach ($executable in @($PythonExe, $GitExe)) {
    if (!(Test-FullyQualifiedPath -Path $executable) -or
        !(Test-Path -LiteralPath $executable -PathType Leaf)) {
        [Console]::Error.WriteLine("SECRET_SCAN_WRAPPER_ERROR kind=invalid_executable")
        exit 2
    }
}
$payload = [pscustomobject]@{
    Executable = $PythonExe
    Arguments = @(
        (Join-Path $PSScriptRoot "scan_secrets.py"),
        "--git-exe",
        $GitExe
    ) + $ScannerArguments
}
$job = Start-Job -ScriptBlock {
    param($Invocation)
    $output = & ([string]$Invocation.Executable) @([string[]]$Invocation.Arguments) `
        2>&1 | Out-String
    $code = $LASTEXITCODE
    [pscustomobject]@{ ExitCode = $code; Output = $output }
} -ArgumentList $payload
try {
    if (!(Wait-Job -Job $job -Timeout 300)) {
        Stop-Job -Job $job
        [Console]::Error.WriteLine("SECRET_SCAN_WRAPPER_ERROR kind=timeout")
        exit 2
    }
    $result = Receive-Job -Job $job
} finally {
    Remove-Job -Job $job -Force
}
if ($result.ExitCode -notin @(0, 1, 2)) {
    [Console]::Error.WriteLine("SECRET_SCAN_WRAPPER_ERROR kind=child_failure")
    exit 2
}
[Console]::Out.Write($result.Output)
exit $result.ExitCode
```

- [ ] **Step 10: Run all scanner tests green**

Run the green through `Invoke-CheckedNative` with `$PythonExe`, arguments `@("-m", "pytest", "backend/tests/unit/test_secret_scanner.py", "-q")`, and a 600-second timeout.

Expected: every scanner boundary test passes.

- [ ] **Step 11: Refactor-check scanner syntax, static analysis, and actual repository scan**

Run:

```powershell
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "-m", "ruff", "check", "--config", "backend/pyproject.toml",
    "scripts/secret_scan", "scripts/scan_secrets.py",
    "backend/tests/unit/test_secret_scanner.py"
) -TimeoutSeconds 300 -FailureMessage "T-01D Ruff failed"
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "-m", "mypy", "--config-file", "backend/pyproject.toml",
    "scripts/secret_scan", "scripts/scan_secrets.py"
) -TimeoutSeconds 300 -FailureMessage "T-01D mypy failed"
$tokens = $null
$parseErrors = $null
[void][Management.Automation.Language.Parser]::ParseFile(
    (Resolve-Path scripts/scan_secrets.ps1), [ref]$tokens, [ref]$parseErrors
)
if ($parseErrors.Count -ne 0) { throw "PowerShell wrapper syntax error" }
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "scripts/scan_secrets.py", "--git-exe", $GitExe
) -TimeoutSeconds 300 -FailureMessage "T-01D repository self-scan failed"
```

Expected: Ruff/mypy/PowerShell parsing exit clean; scanner prints `SECRET_SCAN_OK` with a positive file count and exits 0.

- [ ] **Step 12: Prepare the T-01D SPEC packet; do not dispatch before staging**

Prepare these inputs and questions, but dispatch only after Step 14 produces the exact staged diff and tree ID.

- [ ] **Step 13: Prepare the T-01D quality/security packet; do not dispatch**

Prepare questions covering the full matrix, absolute bounded commands, dynamic fixtures, and repository self-scan; dispatch only after final staging.

- [ ] **Step 14: Stage exactly seven paths and scan the Git index**

Run:

```powershell
$paths = @(
    "scripts/secret_scan/__init__.py", "scripts/secret_scan/encoding.py",
    "scripts/secret_scan/paths.py", "scripts/secret_scan/rules.py",
    "scripts/scan_secrets.py", "scripts/scan_secrets.ps1",
    "backend/tests/unit/test_secret_scanner.py"
)
Invoke-CheckedGit -ArgumentList (@("add", "--") + $paths) -FailureMessage "T-01D git add failed"
Invoke-CheckedGit -ArgumentList @("diff", "--cached", "--check") -FailureMessage "T-01D staged diff check failed"
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "scripts/scan_secrets.py", "--staged", "--git-exe", $GitExe
) -TimeoutSeconds 300 -FailureMessage "T-01D staged scanner failed"
Assert-ExactStagedPaths -ExpectedPaths $paths
$reviewTree = Get-StagedTreeId
$reviewTree
$reviewPacket = Export-ReviewedStagedDiff -UnitId $env:PROJECTB_UNIT_ID `
    -ExpectedTreeId $reviewTree
$reviewPacket
```

Expected: scanner exits 0, whitespace check passes, and exactly seven paths are staged.

- [ ] **Step 15: Run both staged-tree reviews, revalidate, and commit T-01D**

Run:

```powershell
$ids = @(
    $env:PROJECTB_AGENT_ID,
    $env:PROJECTB_T01D_SPEC_REVIEW_ID,
    $env:PROJECTB_T01D_QUALITY_REVIEW_ID
)
Invoke-FinalPrecommitValidation -UnitId "T-01D" -ExpectedPaths $paths -Identities $ids `
    -SpecTreeId $env:PROJECTB_T01D_SPEC_REVIEW_TREE `
    -QualityTreeId $env:PROJECTB_T01D_QUALITY_REVIEW_TREE -ScannerMode "canonical"
Invoke-CheckedGit -ArgumentList @("commit", "-m", "feat(T-01D): add strict fail-closed secret scanner [agent: $env:PROJECTB_AGENT_ID]") `
    -FailureMessage "T-01D commit failed"
$commitHash = Invoke-CheckedGitText -ArgumentList @("rev-parse", "HEAD") -FailureMessage "T-01D hash lookup failed"
Assert-CommittedTreeBinding -UnitId "T-01D" -ExpectedTreeId $env:PROJECTB_T01D_SPEC_REVIEW_TREE
if ($commitHash -notmatch "^[0-9a-f]{40}$") { throw "T-01D did not produce a full commit hash" }
$commitHash
```

Expected: one seven-path T-01D commit and its actual hash.

### Task T-01E1: Resolve Absolute Executable Paths

**Unit prelude:** Run the complete Required Fail-Closed Command Prelude before Step 1. E1 consumes exactly the four root runtime path variables; Git remains a coordinator control-plane executable and is not part of E1.

**Cross-plan gate:** E1 cannot dispatch until root G-04 and `docs/engineering/WORKTREE_MAP.md` are atomically amended and reviewed with one coordinator-owned `path`/lowercase `sha256`/exact `version`/`provenance` attestation for each of Python, Node, npm, and PowerShell. The G-04 validator must compare those four attestations to the four root exports before every unit. T-01 workers may observe bytes for same-run drift detection but may not approve their own executables.

**Goal:** Resolve exactly the four coordinator-exported Python, Node, Windows `npm.cmd`, and PowerShell paths to canonical absolute leaf files without PATH lookup or child-process execution.

**Dependencies / parallelism:** Requires reviewed T-01A and T-01C1 commits. It may run while T-01B, T-01C2, or T-01D is still active because it owns disjoint paths. T-01E2 and T-01F1 depend on its reviewed commit.

**Files:**
- Create: `scripts/projectb_test_runner/__init__.py`
- Create: `scripts/projectb_test_runner/executables.py`
- Test: `backend/tests/unit/test_runner_executables.py`

**Acceptance:** Resolution reads only `PROJECTB_PYTHON_EXE`, `PROJECTB_NODE_EXE`, `PROJECTB_NPM_CMD`, and `PROJECTB_POWERSHELL_EXE`. It checks exact allowed leaf names, canonical path, existing regular files, and every lexical component from filesystem anchor through leaf with `lstat`, so a symlink, junction, or other Windows reparse point in any parent fails closed. Nonabsolute, missing, directory, parent-alias, wrong-name, or PATH-only values fail closed. The immutable result contains only the four canonical paths. E1 still owns exactly three paths and does not execute a version command.

- [ ] **Step 1: Run the required prelude and verify reviewed A+C1 inputs**

Run:

```powershell
Assert-UnitContext -UnitId "T-01E1"
Assert-ValidIdentity -Role "T-01E1 worker" -Identity $env:PROJECTB_AGENT_ID
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @("--version") `
    -TimeoutSeconds 30 -FailureMessage "T-01E1 Python invocation failed"
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "backend/tests/unit/test_toolchain_contract.py"
) -TimeoutSeconds 300 -FailureMessage "T-01E1 foundation contract failed"
Invoke-CheckedNative -FilePath $NodeExe -ArgumentList @(
    "--test", "scripts/tests/frontend_contract.test.mjs"
) -TimeoutSeconds 600 -FailureMessage "T-01E1 frontend contract failed"
Invoke-CheckedNative -FilePath $NodeExe -ArgumentList @(
    "--test", "scripts/tests/frontend_lock_contract.test.mjs"
) -TimeoutSeconds 900 -FailureMessage "T-01E1 frontend lock contract failed"
```

Expected: the exact Python, Node, and npm versions are observed and every reviewed A/C1 contract test passes.

- [ ] **Step 2a: Write success and invalid-value resolution tests**

Create `backend/tests/unit/test_runner_executables.py`:

```python
import os
import stat
from pathlib import Path

import pytest
from scripts.projectb_test_runner.executables import (
    ExecutableResolutionError,
    resolve_windows_executables,
)

CONTRACTS = (
    ("PROJECTB_PYTHON_EXE", "python.exe"),
    ("PROJECTB_NODE_EXE", "node.exe"),
    ("PROJECTB_NPM_CMD", "npm.cmd"),
    ("PROJECTB_POWERSHELL_EXE", "pwsh.exe"),
)


def make_environment(tmp_path: Path) -> dict[str, str]:
    environment: dict[str, str] = {}
    for variable, leaf in CONTRACTS:
        executable = tmp_path / leaf
        executable.write_bytes(variable.encode("ascii"))
        environment[variable] = str(executable)
    return environment


def test_resolves_exactly_four_canonical_absolute_leaf_files(tmp_path: Path) -> None:
    environment = make_environment(tmp_path)
    result = resolve_windows_executables(environment)
    assert result.python == str(Path(environment["PROJECTB_PYTHON_EXE"]).resolve())
    assert result.node == str(Path(environment["PROJECTB_NODE_EXE"]).resolve())
    assert result.npm == str(Path(environment["PROJECTB_NPM_CMD"]).resolve())
    assert result.powershell == str(
        Path(environment["PROJECTB_POWERSHELL_EXE"]).resolve()
    )
    assert tuple(result.__dataclass_fields__) == (
        "python",
        "node",
        "npm",
        "powershell",
    )


@pytest.mark.parametrize("variable", tuple(item[0] for item in CONTRACTS))
@pytest.mark.parametrize(
    "kind",
    ("unset", "relative", "missing", "directory", "parent_alias"),
)
def test_invalid_exported_values_fail_closed(
    tmp_path: Path,
    variable: str,
    kind: str,
) -> None:
    environment = make_environment(tmp_path)
    if kind == "unset":
        del environment[variable]
    elif kind == "relative":
        environment[variable] = "tool.exe"
    elif kind == "missing":
        environment[variable] = str(tmp_path / "missing.exe")
    elif kind == "directory":
        directory = tmp_path / "directory"
        directory.mkdir()
        environment[variable] = str(directory)
    else:
        leaf = Path(environment[variable]).name
        child = tmp_path / "child"
        child.mkdir()
        environment[variable] = str(child / ".." / leaf)
    with pytest.raises(ExecutableResolutionError, match=variable):
        resolve_windows_executables(environment)


def test_path_only_discovery_is_never_used(tmp_path: Path) -> None:
    with pytest.raises(ExecutableResolutionError, match="PROJECTB_PYTHON_EXE"):
        resolve_windows_executables({"PATH": str(tmp_path)})

```

- [ ] **Step 2b: Append wrong-leaf and reparse-component tests**

Append the following complete cases to `backend/tests/unit/test_runner_executables.py`:

```python


@pytest.mark.parametrize(
    ("variable", "wrong_name"),
    (
        ("PROJECTB_PYTHON_EXE", "python-wrapper.exe"),
        ("PROJECTB_NODE_EXE", "node-wrapper.exe"),
        ("PROJECTB_NPM_CMD", "npm.exe"),
        ("PROJECTB_POWERSHELL_EXE", "shell.exe"),
    ),
)
def test_each_runtime_requires_its_exact_leaf(
    tmp_path: Path,
    variable: str,
    wrong_name: str,
) -> None:
    environment = make_environment(tmp_path)
    replacement = tmp_path / wrong_name
    replacement.write_bytes(b"replacement")
    environment[variable] = str(replacement)
    with pytest.raises(ExecutableResolutionError, match=variable):
        resolve_windows_executables(environment)


@pytest.mark.parametrize("component_kind", ("leaf", "parent"))
def test_symlink_mode_on_any_component_is_rejected(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    component_kind: str,
) -> None:
    environment = make_environment(tmp_path)
    leaf = Path(environment["PROJECTB_PYTHON_EXE"])
    blocked = leaf if component_kind == "leaf" else leaf.parent
    real_lstat = os.lstat

    def fake_lstat(path: os.PathLike[str] | str) -> os.stat_result:
        observed = real_lstat(path)
        if Path(path) == blocked:
            values = list(observed)
            values[0] = stat.S_IFLNK | stat.S_IRUSR
            return os.stat_result(values)
        return observed

    monkeypatch.setattr(os, "lstat", fake_lstat)
    with pytest.raises(ExecutableResolutionError, match="PROJECTB_PYTHON_EXE"):
        resolve_windows_executables(environment)


def test_windows_reparse_attribute_on_parent_is_rejected(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    environment = make_environment(tmp_path)
    blocked = Path(environment["PROJECTB_PYTHON_EXE"]).parent
    real_lstat = os.lstat

    class ReparseMetadata:
        def __init__(self, observed: os.stat_result) -> None:
            self.st_mode = observed.st_mode
            self.st_file_attributes = 0x400

    def fake_lstat(path: os.PathLike[str] | str) -> os.stat_result:
        observed = real_lstat(path)
        if Path(path) == blocked:
            return ReparseMetadata(observed)  # type: ignore[return-value]
        return observed

    monkeypatch.setattr(os, "lstat", fake_lstat)
    with pytest.raises(ExecutableResolutionError, match="PROJECTB_PYTHON_EXE"):
        resolve_windows_executables(environment)
```

- [ ] **Step 3: Run executable-resolution tests red**

Run the red through `Invoke-CheckedNative` with `$PythonExe`, arguments `@("-m", "pytest", "backend/tests/unit/test_runner_executables.py", "-q")`, and a 300-second timeout.

Expected: the executable-resolution suite is collected and import fails because the runner package is absent.

- [ ] **Step 4a: Implement the package marker and path-component safeguards**

Create `scripts/projectb_test_runner/__init__.py`:

```python
"""Fail-closed ProjectB test-runner support."""
```

Create `scripts/projectb_test_runner/executables.py`:

```python
import os
import stat
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path


class ExecutableResolutionError(RuntimeError):
    """A required runtime path cannot be resolved safely."""


@dataclass(frozen=True)
class Executables:
    python: str
    node: str
    npm: str
    powershell: str


RUNTIME_CONTRACTS = (
    ("python", "PROJECTB_PYTHON_EXE", ("python.exe",)),
    ("node", "PROJECTB_NODE_EXE", ("node.exe",)),
    ("npm", "PROJECTB_NPM_CMD", ("npm.cmd",)),
    (
        "powershell",
        "PROJECTB_POWERSHELL_EXE",
        ("pwsh.exe", "powershell.exe"),
    ),
)
REPARSE_POINT_ATTRIBUTE = 0x400


def iter_path_components(path: Path) -> tuple[Path, ...]:
    if not path.parts:
        return ()
    current = Path(path.parts[0])
    components = [current]
    for part in path.parts[1:]:
        current = current / part
        components.append(current)
    return tuple(components)


def reject_reparse_components(candidate: Path, variable: str) -> None:
    for component in iter_path_components(candidate):
        try:
            metadata = os.lstat(component)
        except OSError as error:
            raise ExecutableResolutionError(
                f"executable is missing: {variable}"
            ) from error
        attributes = getattr(metadata, "st_file_attributes", 0)
        if stat.S_ISLNK(metadata.st_mode) or bool(
            attributes & REPARSE_POINT_ATTRIBUTE
        ):
            raise ExecutableResolutionError(
                f"executable path contains a reparse component: {variable}"
            )

```

- [ ] **Step 4b: Append absolute-leaf resolution and the four-field constructor**

Append to `scripts/projectb_test_runner/executables.py`:

```python

def resolve_absolute_leaf(
    raw: object,
    *,
    variable: str,
    expected_names: tuple[str, ...],
) -> str:
    if not isinstance(raw, str) or not raw.strip():
        raise ExecutableResolutionError(f"missing executable path: {variable}")
    candidate = Path(raw)
    if not candidate.is_absolute() or ".." in candidate.parts:
        raise ExecutableResolutionError(
            f"executable must be an unaliased absolute path: {variable}"
        )
    reject_reparse_components(candidate, variable)
    try:
        resolved = candidate.resolve(strict=True)
    except OSError as error:
        raise ExecutableResolutionError(
            f"executable is missing: {variable}"
        ) from error
    if not resolved.is_file():
        raise ExecutableResolutionError(
            f"executable is not a leaf file: {variable}"
        )
    expected = {name.casefold() for name in expected_names}
    if resolved.name.casefold() not in expected:
        raise ExecutableResolutionError(
            f"executable has the wrong filename: {variable}"
        )
    return str(resolved)


def resolve_windows_executables(
    environment: Mapping[str, str] | None = None,
) -> Executables:
    source = os.environ if environment is None else environment
    resolved = {
        field: resolve_absolute_leaf(
            source.get(variable),
            variable=variable,
            expected_names=expected_names,
        )
        for field, variable, expected_names in RUNTIME_CONTRACTS
    }
    return Executables(
        python=resolved["python"],
        node=resolved["node"],
        npm=resolved["npm"],
        powershell=resolved["powershell"],
    )
```

- [ ] **Step 5: Run executable-resolution tests green**

Run the green through `Invoke-CheckedNative` with `$PythonExe`, arguments `@("-m", "pytest", "backend/tests/unit/test_runner_executables.py", "-q")`, and a 300-second timeout.

Expected: the complete executable-resolution matrix passes.

- [ ] **Step 6: Reverify the three-path E1 unit**

```powershell
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "-m", "pytest", "backend/tests/unit/test_runner_executables.py", "-q"
) -TimeoutSeconds 300 -FailureMessage "T-01E1 focused tests failed"
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "-m", "ruff", "check", "--config", "backend/pyproject.toml",
    "scripts/projectb_test_runner/__init__.py",
    "scripts/projectb_test_runner/executables.py",
    "backend/tests/unit/test_runner_executables.py"
) -TimeoutSeconds 300 -FailureMessage "T-01E1 Ruff failed"
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "-m", "mypy", "--config-file", "backend/pyproject.toml",
    "scripts/projectb_test_runner/__init__.py",
    "scripts/projectb_test_runner/executables.py"
) -TimeoutSeconds 300 -FailureMessage "T-01E1 mypy failed"
```

Expected: the invalid-path matrix passes; Ruff and mypy exit 0.

- [ ] **Step 7: Prepare both T-01E1 packets; do not dispatch before staging**

Prepare both packets with Step 6 output and questions covering all-component reparse checks, the four root runtime paths, and the reviewed G-04 attestations. Explicitly record that E1 neither owns Git nor self-approves executable hashes. Dispatch only after Step 8 stages the exact tree.

- [ ] **Step 8: Stage E1, run both staged-tree reviews, revalidate, and commit**

```powershell
$paths = @(
    "scripts/projectb_test_runner/__init__.py",
    "scripts/projectb_test_runner/executables.py",
    "backend/tests/unit/test_runner_executables.py"
)
Invoke-CheckedGit -ArgumentList (@("add", "--") + $paths) -FailureMessage "T-01E1 git add failed"
Invoke-CheckedGit -ArgumentList @("diff", "--cached", "--check") -FailureMessage "T-01E1 staged diff check failed"
Invoke-BootstrapStagedSecretScan -ExpectedPaths $paths
Assert-ExactStagedPaths -ExpectedPaths $paths
$reviewTree = Get-StagedTreeId
$reviewTree
$reviewPacket = Export-ReviewedStagedDiff -UnitId $env:PROJECTB_UNIT_ID `
    -ExpectedTreeId $reviewTree
$reviewPacket
$ids = @($env:PROJECTB_AGENT_ID, $env:PROJECTB_T01E1_SPEC_REVIEW_ID, $env:PROJECTB_T01E1_QUALITY_REVIEW_ID)
Invoke-FinalPrecommitValidation -UnitId "T-01E1" -ExpectedPaths $paths -Identities $ids `
    -SpecTreeId $env:PROJECTB_T01E1_SPEC_REVIEW_TREE `
    -QualityTreeId $env:PROJECTB_T01E1_QUALITY_REVIEW_TREE -ScannerMode "bootstrap"
Invoke-CheckedGit -ArgumentList @("commit", "-m", "test(T-01E1): resolve absolute test tools [agent: $env:PROJECTB_AGENT_ID]") `
    -FailureMessage "T-01E1 commit failed"
$commitHash = Invoke-CheckedGitText -ArgumentList @("rev-parse", "HEAD") -FailureMessage "T-01E1 hash lookup failed"
Assert-CommittedTreeBinding -UnitId "T-01E1" -ExpectedTreeId $env:PROJECTB_T01E1_SPEC_REVIEW_TREE
if ($commitHash -notmatch "^[0-9a-f]{40}$") { throw "T-01E1 did not produce a full commit hash" }
$commitHash
```

Expected: one reviewed three-path E1 commit and its observed hash.

### Task T-01E2: Enforce Exact Runtime, Frontend, Quality, And Raw-Lock Contracts

**Unit prelude:** Run the complete Required Fail-Closed Command Prelude before Step 1. Reuse the four E1-verified runtime paths; `$GitExe` remains available only to the coordinator wrappers and is not part of `Executables` or the application runtime contract.

**Goal:** Invoke every resolved executable for its own exact version, reject weakened frontend/package/config/quality contracts, and enforce raw-byte Python/npm lock identity.

**Dependencies / parallelism:** Requires reviewed T-01C1 and T-01E1 commits. It owns only the six paths below and never edits the E1 package facade, resolver, or E1 test.

**Files:**
- Create: `scripts/projectb_test_runner/contracts.py`
- Create: `scripts/projectb_test_runner/locks.py`
- Create: `scripts/projectb_test_runner/runtime.py`
- Test: `backend/tests/unit/test_runner_contracts.py`
- Test: `backend/tests/unit/test_runner_locks.py`
- Test: `backend/tests/unit/test_runner_runtime.py`

**Acceptance:** The reviewed G-04 preflight first attests the four E1 paths; E2 then observes each leaf's path/hash/size for same-run drift detection and invokes only that observation with a fixed 10-second timeout, a minimal allowlisted environment without `PATH`, `PYTHONPATH`, or `NODE_OPTIONS`, and before/after byte checks. Empty, ambiguous, multiline, malformed, wrong-version, exact-output fake-wrapper, nonzero, unavailable, replaced, or timed-out results fail closed; error text never includes observed child output. The package script mapping must equal the canonical mapping exactly, so extra lifecycle or wrapper scripts are rejected. Both Vitest suffixes, immutable Vite raw bytes, explicit Ruff/mypy settings, immutable G-02A lock blob IDs/raw hashes, and production raw bytes fail closed. These same-run observations are never described as executable approval or G-02A evidence.

- [ ] **Step 1: Write failing anti-weakening frontend and quality tests**

Run the complete shared prelude before creating the test below:

```powershell
Assert-UnitContext -UnitId "T-01E2"
Assert-ValidIdentity -Role "T-01E2 worker" -Identity $env:PROJECTB_AGENT_ID
```

Create `backend/tests/unit/test_runner_contracts.py`:

```python
import json
import shutil
from pathlib import Path

import pytest
from scripts.projectb_test_runner.contracts import ContractError, verify_repository_contracts

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]


def contract_fixture(tmp_path: Path) -> Path:
    frontend = tmp_path / "frontend"
    backend = tmp_path / "backend"
    frontend.mkdir()
    backend.mkdir()
    for name in (
        "package.json",
        "vitest.contract.json",
        "vite.config.contract.json",
        "vite.config.ts",
    ):
        shutil.copyfile(REPOSITORY_ROOT / "frontend" / name, frontend / name)
    shutil.copyfile(REPOSITORY_ROOT / "backend" / "pyproject.toml", backend / "pyproject.toml")
    return tmp_path


def test_checked_in_repository_contracts_pass() -> None:
    verify_repository_contracts(REPOSITORY_ROOT)


def test_no_op_package_test_script_is_rejected(tmp_path: Path) -> None:
    root = contract_fixture(tmp_path)
    path = root / "frontend/package.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    manifest["scripts"]["test"] = 'node -e "process.exit(0)"'
    path.write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(ContractError, match="script:test"):
        verify_repository_contracts(root)


def test_extra_lifecycle_or_wrapper_script_is_rejected(tmp_path: Path) -> None:
    root = contract_fixture(tmp_path)
    path = root / "frontend/package.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    manifest["scripts"]["pretest"] = "node ../scripts/unreviewed-wrapper.mjs"
    path.write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(ContractError, match="script set"):
        verify_repository_contracts(root)


def test_missing_plain_typescript_pattern_is_rejected(tmp_path: Path) -> None:
    root = contract_fixture(tmp_path)
    path = root / "frontend/vitest.contract.json"
    contract = json.loads(path.read_text(encoding="utf-8"))
    contract["include"] = ["src/**/*.test.tsx"]
    path.write_text(json.dumps(contract), encoding="utf-8")
    with pytest.raises(ContractError, match="Vitest"):
        verify_repository_contracts(root)


def test_vite_comment_or_dead_code_changes_raw_contract(tmp_path: Path) -> None:
    root = contract_fixture(tmp_path)
    path = root / "frontend/vite.config.ts"
    path.write_bytes(path.read_bytes() + b"// dead code\n")
    with pytest.raises(ContractError, match="Vite raw"):
        verify_repository_contracts(root)


def test_weakened_ruff_selection_is_rejected(tmp_path: Path) -> None:
    root = contract_fixture(tmp_path)
    path = root / "backend/pyproject.toml"
    text = path.read_text(encoding="utf-8").replace(
        'select = ["B", "E", "F", "I", "UP"]', 'select = ["E", "F"]'
    )
    path.write_text(text, encoding="utf-8")
    with pytest.raises(ContractError, match="Ruff"):
        verify_repository_contracts(root)


def test_weakened_mypy_strictness_is_rejected(tmp_path: Path) -> None:
    root = contract_fixture(tmp_path)
    path = root / "backend/pyproject.toml"
    text = path.read_text(encoding="utf-8").replace("strict = true", "strict = false")
    path.write_text(text, encoding="utf-8")
    with pytest.raises(ContractError, match="mypy"):
        verify_repository_contracts(root)
```

- [ ] **Step 2: Run anti-weakening contract tests red**

Run the red through `Invoke-CheckedNative` with `$PythonExe`, arguments `@("-m", "pytest", "backend/tests/unit/test_runner_contracts.py", "-q")`, and a 300-second timeout.

Expected: the anti-weakening contract suite is collected and import fails because `contracts.py` is absent.

- [ ] **Step 3: Implement exact structured and raw-byte contract validation**

Create `scripts/projectb_test_runner/contracts.py`:

```python
import hashlib
import json
import tomllib
from pathlib import Path
from typing import Any


class ContractError(RuntimeError):
    """A checked-in verification contract is missing or weakened."""


EXPECTED_SCRIPTS = {
    "dev": "vite --host 127.0.0.1",
    "test": "vitest run",
    "test:lock": "node --test ../scripts/tests/frontend_lock_contract.test.mjs",
    "build": "tsc --noEmit && vite build",
    "preview": "vite preview --host 127.0.0.1",
    "e2e": "playwright test",
}
EXPECTED_VITEST = {
    "environment": "jsdom",
    "globals": True,
    "include": ["src/**/*.test.ts", "src/**/*.test.tsx"],
}
EXPECTED_VITE_SHA256 = "219863494626f9af96f27257aae1b112d9d2f001e9d42de40f3c6d1c43633242"
EXPECTED_VITE_CONTRACT = {
    "algorithm": "sha256",
    "sha256": EXPECTED_VITE_SHA256,
    "bytes": 376,
    "testContract": "vitest.contract.json",
}
EXPECTED_RUFF = {
    "target-version": "py314",
    "line-length": 100,
    "src": ["src", "tests", "../scripts"],
    "lint": {"select": ["B", "E", "F", "I", "UP"]},
}
EXPECTED_MYPY = {
    "python_version": "3.14",
    "strict": True,
    "warn_unreachable": True,
    "show_error_codes": True,
}


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ContractError(f"invalid JSON contract: {path.name}") from error
    if not isinstance(value, dict):
        raise ContractError(f"JSON contract is not an object: {path.name}")
    return value


def verify_frontend_contract(root: Path) -> None:
    frontend = root / "frontend"
    scripts = load_json(frontend / "package.json").get("scripts")
    if not isinstance(scripts, dict):
        raise ContractError("package scripts are missing")
    if set(scripts) != set(EXPECTED_SCRIPTS):
        raise ContractError("package script set differs from the canonical set")
    for name, expected in EXPECTED_SCRIPTS.items():
        if scripts.get(name) != expected:
            raise ContractError(f"script:{name} differs from the canonical command")
    if load_json(frontend / "vitest.contract.json") != EXPECTED_VITEST:
        raise ContractError("Vitest structured contract is missing or weakened")
    contract = load_json(frontend / "vite.config.contract.json")
    if contract != EXPECTED_VITE_CONTRACT:
        raise ContractError("Vite structured contract is missing or weakened")
    try:
        vite_bytes = (frontend / "vite.config.ts").read_bytes()
    except OSError as error:
        raise ContractError("Vite config is unreadable") from error
    if len(vite_bytes) != 376 or hashlib.sha256(vite_bytes).hexdigest() != EXPECTED_VITE_SHA256:
        raise ContractError("Vite raw byte contract differs")


def verify_quality_contract(root: Path) -> None:
    try:
        with (root / "backend/pyproject.toml").open("rb") as stream:
            manifest = tomllib.load(stream)
    except (OSError, tomllib.TOMLDecodeError) as error:
        raise ContractError("Python quality config is unreadable") from error
    tool = manifest.get("tool")
    if not isinstance(tool, dict):
        raise ContractError("Python tool config is missing")
    if tool.get("ruff") != EXPECTED_RUFF:
        raise ContractError("Ruff config is missing or weakened")
    if tool.get("mypy") != EXPECTED_MYPY:
        raise ContractError("mypy config is missing or weakened")


def verify_repository_contracts(root: Path) -> None:
    verify_frontend_contract(root)
    verify_quality_contract(root)
```

- [ ] **Step 4: Run anti-weakening contract tests green**

Run the green through `Invoke-CheckedNative` with `$PythonExe`, arguments `@("-m", "pytest", "backend/tests/unit/test_runner_contracts.py", "-q")`, and a 300-second timeout.

Expected: every anti-weakening contract test passes.

- [ ] **Step 5: Write failing raw-lock contract tests**

Create `backend/tests/unit/test_runner_locks.py`:

```python
import shutil
from hashlib import sha256
from pathlib import Path

import pytest
from scripts.projectb_test_runner.contracts import ContractError
from scripts.projectb_test_runner.locks import (
    EXPECTED_NPM_SOURCE_BLOB_SHA1,
    EXPECTED_NPM_SOURCE_SHA256,
    EXPECTED_PYTHON_LOCK_BLOB_SHA1,
    EXPECTED_PYTHON_LOCK_SHA256,
    assert_raw_copy,
    raw_git_blob_sha1,
    raw_sha256,
    verify_lock_contract,
)

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]


def test_identical_raw_copy_passes(tmp_path: Path) -> None:
    source = tmp_path / "source.lock"
    target = tmp_path / "target.lock"
    source.write_bytes(b"one\ntwo\n")
    target.write_bytes(source.read_bytes())
    assert_raw_copy(source, target, sha256(source.read_bytes()).hexdigest())


def test_line_ending_change_fails_raw_copy(tmp_path: Path) -> None:
    source = tmp_path / "source.lock"
    target = tmp_path / "target.lock"
    source.write_bytes(b"one\ntwo\n")
    target.write_bytes(b"one\r\ntwo\r\n")
    with pytest.raises(ContractError, match="raw bytes"):
        assert_raw_copy(source, target, sha256(source.read_bytes()).hexdigest())


def test_evidence_locks_have_expected_raw_hashes() -> None:
    python_lock = REPOSITORY_ROOT / "docs/engineering/locks/python-3.14.6-windows-x64.lock"
    npm_lock = REPOSITORY_ROOT / "docs/engineering/locks/frontend-package-lock.json"
    assert raw_sha256(python_lock) == EXPECTED_PYTHON_LOCK_SHA256
    assert raw_sha256(npm_lock) == EXPECTED_NPM_SOURCE_SHA256
    assert raw_git_blob_sha1(python_lock) == EXPECTED_PYTHON_LOCK_BLOB_SHA1
    assert raw_git_blob_sha1(npm_lock) == EXPECTED_NPM_SOURCE_BLOB_SHA1


def test_production_npm_lock_mutation_fails_raw_copy(tmp_path: Path) -> None:
    for relative in (
        "docs/engineering/locks",
        "backend",
        "frontend",
    ):
        (tmp_path / relative).mkdir(parents=True, exist_ok=True)
    copies = (
        (
            "docs/engineering/locks/python-3.14.6-windows-x64.lock",
            "docs/engineering/locks/python-3.14.6-windows-x64.lock",
        ),
        (
            "backend/requirements-windows-x64.lock",
            "backend/requirements-windows-x64.lock",
        ),
        (
            "docs/engineering/locks/frontend-package-lock.json",
            "docs/engineering/locks/frontend-package-lock.json",
        ),
        ("frontend/package-lock.json", "frontend/package-lock.json"),
    )
    for source, target in copies:
        shutil.copyfile(REPOSITORY_ROOT / source, tmp_path / target)
    production = tmp_path / "frontend/package-lock.json"
    production.write_bytes(production.read_bytes() + b"\n")
    with pytest.raises(ContractError, match="production lock raw bytes"):
        verify_lock_contract(tmp_path)
```

- [ ] **Step 6: Run raw-lock contract tests red**

Run the red through `Invoke-CheckedNative` with `$PythonExe`, arguments `@("-m", "pytest", "backend/tests/unit/test_runner_locks.py", "-q")`, and a 300-second timeout.

Expected: the raw-lock suite is collected and import fails because `locks.py` is absent.

- [ ] **Step 7: Implement raw lock identity validation**

Create `scripts/projectb_test_runner/locks.py`:

```python
from hashlib import sha1, sha256
from pathlib import Path

from .contracts import ContractError

EXPECTED_PYTHON_LOCK_SHA256 = "246083f8b210c3e33904f3057dfd48e7d8db548804d11fa5b087ecb291ad0fc6"
EXPECTED_NPM_SOURCE_SHA256 = "071826d575cbcc472020a7df984e2e8f2410a75c1782550c5ddfeed268af3c2f"
EXPECTED_PYTHON_LOCK_BLOB_SHA1 = "1078db073060e01051bebd1f2250ab55b0cec3d2"
EXPECTED_NPM_SOURCE_BLOB_SHA1 = "c2c53ae64a720b84eb7ee7c56483070bcfa2cdb8"


def read_bytes(path: Path) -> bytes:
    try:
        return path.read_bytes()
    except OSError as error:
        raise ContractError(f"required lock is unreadable: {path.name}") from error


def raw_sha256(path: Path) -> str:
    return sha256(read_bytes(path)).hexdigest()


def raw_git_blob_sha1(path: Path) -> str:
    data = read_bytes(path)
    header = f"blob {len(data)}\0".encode("ascii")
    return sha1(header + data).hexdigest()


def assert_raw_copy(
    source: Path,
    target: Path,
    expected_source_hash: str,
    expected_source_blob: str | None = None,
) -> None:
    source_bytes = read_bytes(source)
    target_bytes = read_bytes(target)
    if sha256(source_bytes).hexdigest() != expected_source_hash:
        raise ContractError(f"source lock raw SHA-256 mismatch: {source.name}")
    if (
        expected_source_blob is not None
        and raw_git_blob_sha1(source) != expected_source_blob
    ):
        raise ContractError(f"source lock G-02A blob mismatch: {source.name}")
    if source_bytes != target_bytes:
        raise ContractError(f"production lock raw bytes differ: {target.name}")


def verify_lock_contract(root: Path) -> None:
    assert_raw_copy(
        root / "docs/engineering/locks/python-3.14.6-windows-x64.lock",
        root / "backend/requirements-windows-x64.lock",
        EXPECTED_PYTHON_LOCK_SHA256,
        EXPECTED_PYTHON_LOCK_BLOB_SHA1,
    )
    assert_raw_copy(
        root / "docs/engineering/locks/frontend-package-lock.json",
        root / "frontend/package-lock.json",
        EXPECTED_NPM_SOURCE_SHA256,
        EXPECTED_NPM_SOURCE_BLOB_SHA1,
    )
    for required in (
        root / "scripts/frontend_lock_contract.mjs",
        root / "scripts/materialize_frontend_lock.mjs",
    ):
        if not required.is_file():
            raise ContractError(f"required npm lock artifact is missing: {required.name}")
```

- [ ] **Step 8: Run raw-lock contract tests green**

Run the green through `Invoke-CheckedNative` with `$PythonExe`, arguments `@("-m", "pytest", "backend/tests/unit/test_runner_locks.py", "-q")`, and a 300-second timeout.

Expected: every raw-lock contract test passes.

#### T-01E2 Exact-Runtime Contract

- [ ] **Step 9a: Write observation, argv, and sanitized-environment tests**

Create `backend/tests/unit/test_runner_runtime.py`:

```python
import subprocess
import sys
import time
from pathlib import Path

import psutil
import pytest
from scripts.projectb_test_runner.executables import Executables
from scripts.projectb_test_runner.runtime import (
    RUNTIME_COMMAND_TIMEOUT_SECONDS,
    ExecutableObservation,
    RuntimeContractError,
    assert_exact_version,
    capture_version,
    observe_executable,
    verify_exact_runtimes,
)


def make_tools(tmp_path: Path) -> Executables:
    paths: dict[str, str] = {}
    for field, name in (
        ("python", "python.exe"),
        ("node", "node.exe"),
        ("npm", "npm.cmd"),
        ("powershell", "pwsh.exe"),
    ):
        executable = tmp_path / name
        executable.write_bytes(f"runtime-{field}".encode("ascii"))
        paths[field] = str(executable.resolve())
    return Executables(**paths)


class FakeProcess:
    def __init__(self, returncode: int, stdout: str, stderr: str) -> None:
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
        self.pid = 12345

    def communicate(self, timeout: float) -> tuple[str, str]:
        assert timeout == RUNTIME_COMMAND_TIMEOUT_SECONDS
        return self.stdout, self.stderr


def test_exact_version_rejects_patch_drift() -> None:
    assert_exact_version("Node.js", "v24.18.0", "v24.18.0")
    with pytest.raises(RuntimeContractError, match="Node.js"):
        assert_exact_version("Node.js", "v24.18.1", "v24.18.0")


def test_capture_uses_observed_path_argv_and_sanitized_environment(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    tools = make_tools(tmp_path)
    npm = observe_executable(tools.npm)
    observed: list[list[str]] = []

    def fake_popen(command: list[str], **kwargs: object) -> FakeProcess:
        observed.append(command)
        assert kwargs["shell"] is False
        assert kwargs["stdout"] is subprocess.PIPE
        assert kwargs["stderr"] is subprocess.PIPE
        environment = kwargs["env"]
        assert isinstance(environment, dict)
        assert "PATH" not in environment
        assert "PYTHONPATH" not in environment
        assert "NODE_OPTIONS" not in environment
        return FakeProcess(0, "11.16.0\n", "")

    monkeypatch.setattr(subprocess, "Popen", fake_popen)
    assert capture_version(npm, ("--version",)) == "11.16.0"
    assert observed == [[tools.npm, "--version"]]

```

- [ ] **Step 9b: Append malformed-output, timeout, and argument-vector tests**

Append to `backend/tests/unit/test_runner_runtime.py`:

```python


@pytest.mark.parametrize(
    ("stdout", "stderr"),
    (("", ""), ("v24.18.0\nwrapper\n", ""), ("v24.18.0", "warning")),
)
def test_capture_rejects_empty_multiline_or_ambiguous_output(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    stdout: str,
    stderr: str,
) -> None:
    def fake_popen(command: list[str], **kwargs: object) -> FakeProcess:
        del command
        del kwargs
        return FakeProcess(0, stdout, stderr)

    monkeypatch.setattr(subprocess, "Popen", fake_popen)
    observation = observe_executable(make_tools(tmp_path).node)
    with pytest.raises(RuntimeContractError, match="version output"):
        capture_version(observation, ("--version",))


def test_capture_rejects_nonzero_exit(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_popen(command: list[str], **kwargs: object) -> FakeProcess:
        del command
        del kwargs
        return FakeProcess(9, "v24.18.0", "failed")

    monkeypatch.setattr(subprocess, "Popen", fake_popen)
    observation = observe_executable(make_tools(tmp_path).node)
    with pytest.raises(RuntimeContractError, match="failed"):
        capture_version(observation, ("--version",))


def test_runtime_timeout_terminates_descendant_process(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import scripts.projectb_test_runner.runtime as runtime

    executable = Path(sys.executable).resolve(strict=True)
    observation = observe_executable(str(executable))
    pid_file = tmp_path / "runtime-child.pid"
    heartbeat = tmp_path / "runtime-heartbeat.txt"
    child = (
        "import os,time; from pathlib import Path; "
        f"Path({str(pid_file)!r}).write_text(str(os.getpid())); "
        f"p=Path({str(heartbeat)!r}); "
        "[(p.write_text(str(i)), time.sleep(0.05)) for i in range(400)]"
    )
    parent = (
        "import subprocess,sys,time; "
        f"subprocess.Popen([sys.executable, '-c', {child!r}]); time.sleep(30)"
    )
    monkeypatch.setattr(runtime, "RUNTIME_COMMAND_TIMEOUT_SECONDS", 0.5)
    with pytest.raises(RuntimeContractError, match="timed out"):
        capture_version(observation, ("-c", parent))
    for _ in range(20):
        if pid_file.is_file() and heartbeat.is_file():
            break
        time.sleep(0.05)
    child_pid = int(pid_file.read_text(encoding="utf-8"))
    previous = heartbeat.read_text(encoding="utf-8")
    time.sleep(0.2)
    assert not psutil.pid_exists(child_pid)
    assert heartbeat.read_text(encoding="utf-8") == previous


def test_capture_rejects_a_mutable_or_shell_string_argument_vector(
    tmp_path: Path,
) -> None:
    observation = observe_executable(make_tools(tmp_path).node)
    with pytest.raises(RuntimeContractError, match="argument vector"):
        capture_version(observation, "--version")  # type: ignore[arg-type]
    with pytest.raises(RuntimeContractError, match="argument vector"):
        capture_version(observation, ["--version"])  # type: ignore[arg-type]

```

- [ ] **Step 9c: Append four-runtime and replacement-drift tests**

Append to `backend/tests/unit/test_runner_runtime.py`:

```python


def test_verify_invokes_each_of_the_four_resolved_paths(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    tools = make_tools(tmp_path)
    observed: list[tuple[str, tuple[str, ...]]] = []
    answers = iter(("Python 3.14.6", "v24.18.0", "11.16.0", "7.6.1"))

    def fake_capture(
        executable: ExecutableObservation,
        arguments: tuple[str, ...],
    ) -> str:
        observed.append((executable.path, arguments))
        return next(answers)

    monkeypatch.setenv("PROJECTB_POWERSHELL_VERSION", "7.6.1")
    verify_exact_runtimes(tools, capture=fake_capture)
    assert observed == [
        (tools.python, ("--version",)),
        (tools.node, ("--version",)),
        (tools.npm, ("--version",)),
        (
            tools.powershell,
            ("-NoProfile", "-Command", "$PSVersionTable.PSVersion.ToString()"),
        ),
    ]


@pytest.mark.parametrize("reported", ("Python 3.14.5", "wrapper: Python 3.14.6"))
def test_wrong_or_fake_python_output_is_rejected(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    reported: str,
) -> None:
    tools = make_tools(tmp_path)
    monkeypatch.setenv("PROJECTB_POWERSHELL_VERSION", "7.6.1")
    with pytest.raises(RuntimeContractError, match="CPython") as failure:
        verify_exact_runtimes(
            tools,
            capture=lambda executable, arguments: reported,
        )
    assert reported not in str(failure.value)


def test_replacement_after_observation_fails_before_execution(tmp_path: Path) -> None:
    tools = make_tools(tmp_path)
    observation = observe_executable(tools.python)
    Path(tools.python).write_bytes(b"replacement-wrapper")
    with pytest.raises(RuntimeContractError, match="changed"):
        capture_version(observation, ("--version",))


def test_replacement_during_capture_fails_after_execution(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    tools = make_tools(tmp_path)

    def mutating_capture(
        executable: ExecutableObservation,
        arguments: tuple[str, ...],
    ) -> str:
        del arguments
        Path(executable.path).write_bytes(b"replacement-wrapper")
        return "Python 3.14.6"

    monkeypatch.setenv("PROJECTB_POWERSHELL_VERSION", "7.6.1")
    with pytest.raises(RuntimeContractError, match="changed"):
        verify_exact_runtimes(tools, capture=mutating_capture)
```

- [ ] **Step 10: Run exact-runtime tests red**

Run the red through `Invoke-CheckedNative` with `$PythonExe`, arguments `@("-m", "pytest", "backend/tests/unit/test_runner_runtime.py", "-q")`, and a 300-second timeout.

Expected: the exact-runtime suite is collected and import fails because `runtime.py` is absent.

- [ ] **Step 11a: Implement observations, environment filtering, and tree termination**

Create `scripts/projectb_test_runner/runtime.py`:

```python
import hashlib
import os
import subprocess
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path

import psutil

from .executables import Executables


class RuntimeContractError(RuntimeError):
    """A resolved executable does not satisfy the exact runtime contract."""


@dataclass(frozen=True)
class ExecutableObservation:
    path: str
    sha256: str
    size: int


Capture = Callable[[ExecutableObservation, tuple[str, ...]], str]
RUNTIME_COMMAND_TIMEOUT_SECONDS = 10.0
RUNTIME_ENVIRONMENT_KEYS = (
    "SYSTEMROOT",
    "WINDIR",
    "TEMP",
    "TMP",
    "USERPROFILE",
    "HOME",
)


def sanitized_runtime_environment(
    source: Mapping[str, str] | None = None,
) -> dict[str, str]:
    observed = os.environ if source is None else source
    environment = {
        key: value for key in RUNTIME_ENVIRONMENT_KEYS if (value := observed.get(key))
    }
    environment["PYTHONNOUSERSITE"] = "1"
    environment["PYTHONSAFEPATH"] = "1"
    return environment


def observe_executable(path: str) -> ExecutableObservation:
    candidate = Path(path)
    try:
        data = candidate.read_bytes()
    except OSError as error:
        raise RuntimeContractError("runtime executable is unreadable") from error
    return ExecutableObservation(
        path=str(candidate),
        sha256=hashlib.sha256(data).hexdigest(),
        size=len(data),
    )


def assert_observation_unchanged(observation: ExecutableObservation) -> None:
    current = observe_executable(observation.path)
    if current != observation:
        raise RuntimeContractError("runtime executable changed during verification")


def assert_exact_version(label: str, observed: str, expected: str) -> None:
    if observed.strip() != expected:
        raise RuntimeContractError(f"{label} version mismatch")


def terminate_process_tree(process: subprocess.Popen[str]) -> None:
    try:
        parent = psutil.Process(process.pid)
        descendants = parent.children(recursive=True)
    except psutil.Error:
        descendants = []
    for child in reversed(descendants):
        try:
            child.kill()
        except psutil.Error:
            continue
    try:
        process.kill()
    except OSError:
        pass
    psutil.wait_procs(descendants, timeout=5.0)
    try:
        process.wait(timeout=5.0)
    except subprocess.TimeoutExpired:
        pass

```

- [ ] **Step 11b: Append bounded version capture with before/after checks**

Append to `scripts/projectb_test_runner/runtime.py`:

```python


def capture_version(
    observation: ExecutableObservation,
    arguments: tuple[str, ...],
) -> str:
    if (
        not isinstance(arguments, tuple)
        or not arguments
        or any(
            not isinstance(item, str) or not item or "\x00" in item
            for item in arguments
        )
    ):
        raise RuntimeContractError(
            "runtime argument vector must be a fixed nonempty tuple"
        )
    assert_observation_unchanged(observation)
    try:
        process = subprocess.Popen(
            [observation.path, *arguments],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            shell=False,
            env=sanitized_runtime_environment(),
        )
    except OSError as error:
        raise RuntimeContractError("runtime command is unavailable") from error
    try:
        stdout, stderr = process.communicate(
            timeout=RUNTIME_COMMAND_TIMEOUT_SECONDS
        )
    except subprocess.TimeoutExpired as error:
        terminate_process_tree(process)
        raise RuntimeContractError("runtime command timed out") from error
    if process.returncode != 0:
        raise RuntimeContractError("runtime command failed")
    outputs = [
        value.strip()
        for value in (stdout, stderr)
        if value is not None and value.strip()
    ]
    if len(outputs) != 1 or "\n" in outputs[0] or "\r" in outputs[0]:
        raise RuntimeContractError("runtime version output is malformed")
    assert_observation_unchanged(observation)
    return outputs[0]

```

- [ ] **Step 11c: Append exact four-runtime verification**

Append to `scripts/projectb_test_runner/runtime.py`:

```python


def verify_one_runtime(
    label: str,
    observation: ExecutableObservation,
    arguments: tuple[str, ...],
    expected: str,
    capture: Capture,
) -> None:
    assert_observation_unchanged(observation)
    observed = capture(observation, arguments)
    assert_observation_unchanged(observation)
    assert_exact_version(label, observed, expected)


def verify_exact_runtimes(
    executables: Executables,
    *,
    capture: Capture = capture_version,
) -> None:
    powershell_version = os.environ.get(
        "PROJECTB_POWERSHELL_VERSION", ""
    ).strip()
    if not powershell_version:
        raise RuntimeContractError("PROJECTB_POWERSHELL_VERSION is required")
    python = observe_executable(executables.python)
    node = observe_executable(executables.node)
    npm = observe_executable(executables.npm)
    powershell = observe_executable(executables.powershell)
    verify_one_runtime(
        "CPython", python, ("--version",), "Python 3.14.6", capture
    )
    verify_one_runtime("Node.js", node, ("--version",), "v24.18.0", capture)
    verify_one_runtime("npm", npm, ("--version",), "11.16.0", capture)
    verify_one_runtime(
        "PowerShell",
        powershell,
        ("-NoProfile", "-Command", "$PSVersionTable.PSVersion.ToString()"),
        powershell_version,
        capture,
    )
```

- [ ] **Step 12: Run exact-runtime tests green**

Run the green through `Invoke-CheckedNative` with `$PythonExe`, arguments `@("-m", "pytest", "backend/tests/unit/test_runner_runtime.py", "-q")`, and a 300-second timeout.

Expected: every exact-runtime test passes.

- [ ] **Step 13: Reverify the six-path T-01E2 unit**

Run:

```powershell
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "-m", "pytest", "backend/tests/unit/test_runner_contracts.py",
    "backend/tests/unit/test_runner_locks.py",
    "backend/tests/unit/test_runner_runtime.py", "-q"
) -TimeoutSeconds 600 -FailureMessage "T-01E2 focused tests failed"
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "-m", "ruff", "check", "--config", "backend/pyproject.toml",
    "scripts/projectb_test_runner/contracts.py",
    "scripts/projectb_test_runner/locks.py",
    "scripts/projectb_test_runner/runtime.py",
    "backend/tests/unit/test_runner_contracts.py",
    "backend/tests/unit/test_runner_locks.py",
    "backend/tests/unit/test_runner_runtime.py"
) -TimeoutSeconds 300 -FailureMessage "T-01E2 Ruff failed"
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "-m", "mypy", "--config-file", "backend/pyproject.toml",
    "scripts/projectb_test_runner/contracts.py",
    "scripts/projectb_test_runner/locks.py",
    "scripts/projectb_test_runner/runtime.py"
) -TimeoutSeconds 300 -FailureMessage "T-01E2 mypy failed"
```

Expected: the repository, raw-lock, and exact-runtime contracts pass; Ruff and mypy exit 0.

- [ ] **Step 14: Prepare both T-01E2 packets; do not dispatch before staging**

Prepare both packets with the complete identity, sanitized-environment, redaction, fake-wrapper, timeout, and contract matrix. Dispatch only after Step 15 stages the exact tree.

- [ ] **Step 15: Stage E2, run both staged-tree reviews, revalidate, and commit**

Run the required prelude, then:

```powershell
$paths = @(
    "scripts/projectb_test_runner/contracts.py",
    "scripts/projectb_test_runner/locks.py",
    "scripts/projectb_test_runner/runtime.py",
    "backend/tests/unit/test_runner_contracts.py",
    "backend/tests/unit/test_runner_locks.py",
    "backend/tests/unit/test_runner_runtime.py"
)
Invoke-CheckedGit -ArgumentList (@("add", "--") + $paths) -FailureMessage "T-01E2 git add failed"
Invoke-CheckedGit -ArgumentList @("diff", "--cached", "--check") -FailureMessage "T-01E2 staged diff check failed"
Invoke-BootstrapStagedSecretScan -ExpectedPaths $paths
Assert-ExactStagedPaths -ExpectedPaths $paths
$reviewTree = Get-StagedTreeId
$reviewTree
$reviewPacket = Export-ReviewedStagedDiff -UnitId $env:PROJECTB_UNIT_ID `
    -ExpectedTreeId $reviewTree
$reviewPacket
$ids = @($env:PROJECTB_AGENT_ID, $env:PROJECTB_T01E2_SPEC_REVIEW_ID, $env:PROJECTB_T01E2_QUALITY_REVIEW_ID)
Invoke-FinalPrecommitValidation -UnitId "T-01E2" -ExpectedPaths $paths -Identities $ids `
    -SpecTreeId $env:PROJECTB_T01E2_SPEC_REVIEW_TREE `
    -QualityTreeId $env:PROJECTB_T01E2_QUALITY_REVIEW_TREE -ScannerMode "bootstrap"
Invoke-CheckedGit -ArgumentList @("commit", "-m", "test(T-01E2): validate runner locks and contracts [agent: $env:PROJECTB_AGENT_ID]") `
    -FailureMessage "T-01E2 commit failed"
$commitHash = Invoke-CheckedGitText -ArgumentList @("rev-parse", "HEAD") -FailureMessage "T-01E2 hash lookup failed"
Assert-CommittedTreeBinding -UnitId "T-01E2" -ExpectedTreeId $env:PROJECTB_T01E2_SPEC_REVIEW_TREE
if ($commitHash -notmatch "^[0-9a-f]{40}$") { throw "T-01E2 did not produce a full commit hash" }
$commitHash
```

Expected: one reviewed six-path E2 commit and its actual hash.

### Task T-01F1: Add Gate Modeling And Fail-Fast Execution

**Unit prelude:** Run the complete Required Fail-Closed Command Prelude before Step 1. Gate commands may use only the four E1 runtime paths; coordinator scan/stage wrappers continue to use the separate `$GitExe` control-plane path.

**Goal:** Add the tested gate model, activation-manifest validation, inventory, rendering, and fail-fast execution primitives.

**Dependencies / parallelism:** Requires reviewed T-01B, T-01C2, T-01D, T-01E1, and T-01E2 integrated on top of T-01A/C1. T-01F2 depends on its reviewed commit.

**Files:**
- Create: `scripts/projectb_test_runner/gate_model.py`
- Create: `scripts/projectb_test_runner/gate_run.py`
- Test: `backend/tests/unit/test_runner_gates.py`

**Acceptance:** Immutable `Gate`, `GateState`, and `GateResult` records match the root interface. Every activation/required path remains contained under the repository root and every existing component is rejected if it is a symlink, junction, or Windows reparse point. Every command begins with one of the four G-04-attested, E1-resolved paths; F1 captures a same-run observation during inventory and rechecks it immediately before and after execution. Absent owners, active owners, malformed activation, partial ownership, fail-fast propagation, list rows, and summary rows have deterministic tested semantics. Child environment is allowlisted; stdout/stderr is captured and never forwarded or embedded in summaries. Each child has a fixed 60-second timeout whose failure kills its complete descendant tree and is represented only by the redacted status `failed:124`; the negative test proves no descendant PID or heartbeat survives.

- [ ] **Step 1: Verify integrated A-E behavior and exact executables**

Run:

```powershell
Assert-UnitContext -UnitId "T-01F1"
Assert-ValidIdentity -Role "T-01F1 worker" -Identity $env:PROJECTB_AGENT_ID
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @("--version") `
    -TimeoutSeconds 30 -FailureMessage "T-01F1 Python invocation failed"
Invoke-CheckedNative -FilePath $NodeExe -ArgumentList @("--version") `
    -TimeoutSeconds 30 -FailureMessage "T-01F1 Node invocation failed"
Invoke-CheckedNative -FilePath $NpmCmd -ArgumentList @("--version") `
    -TimeoutSeconds 30 -FailureMessage "T-01F1 npm invocation failed"
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "-m", "pytest", "backend/tests/unit/test_toolchain_contract.py",
    "backend/tests/unit/test_health.py", "backend/tests/unit/test_secret_scanner.py",
    "backend/tests/unit/test_runner_executables.py",
    "backend/tests/unit/test_runner_contracts.py",
    "backend/tests/unit/test_runner_locks.py",
    "backend/tests/unit/test_runner_runtime.py", "-q"
) -TimeoutSeconds 900 -FailureMessage "T-01F1 integrated Python tests failed"
Invoke-CheckedNative -FilePath $NodeExe -ArgumentList @(
    "--test", "scripts/tests/frontend_contract.test.mjs",
    "scripts/tests/frontend_lock_contract.test.mjs"
) -TimeoutSeconds 900 -FailureMessage "T-01F1 Node contracts failed"
Invoke-CheckedNative -FilePath $NpmCmd -ArgumentList @(
    "--prefix", "frontend", "run", "test"
) -TimeoutSeconds 900 -FailureMessage "T-01F1 frontend tests failed"
Invoke-CheckedNative -FilePath $NpmCmd -ArgumentList @(
    "--prefix", "frontend", "run", "build"
) -TimeoutSeconds 900 -FailureMessage "T-01F1 frontend build failed"
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "scripts/scan_secrets.py", "--git-exe", $GitExe
) -TimeoutSeconds 300 -FailureMessage "T-01F1 repository scan failed"
```

Expected: the exact runtime versions are observed; every integrated backend, Node, and Vitest test passes; the production build and scanner exit 0.

- [ ] **Step 2a: Write failing gate-state, marker, and containment tests**

Create `backend/tests/unit/test_runner_gates.py`:

```python
import json
import os
import shutil
import stat
import sys
import time
from pathlib import Path

import psutil
import pytest
import scripts.projectb_test_runner.gate_model as gate_model
from scripts.projectb_test_runner.executables import Executables
from scripts.projectb_test_runner.gate_model import (
    ActivationManifest,
    Gate,
    GateContractError,
    resolve_gate,
)
from scripts.projectb_test_runner.gate_run import (
    execute_inventory,
    inventory_registry,
    run_subprocess,
)
from scripts.projectb_test_runner.runtime import (
    ExecutableObservation,
    RuntimeContractError,
    observe_executable,
)

MARKER_PAYLOAD = {
    "contractVersion": 1,
    "gate": "future-check",
    "owner": "OWNER-01",
    "state": "active",
}


def current_test_observation() -> ExecutableObservation:
    executable = Path(sys.executable).resolve(strict=True)
    return observe_executable(str(executable))


@pytest.fixture(autouse=True)
def approved_test_runtime(monkeypatch: pytest.MonkeyPatch) -> None:
    executable = Path(sys.executable).resolve(strict=True)
    tools = Executables(
        str(executable),
        str(executable),
        str(executable),
        str(executable),
    )
    monkeypatch.setattr(gate_model, "resolve_windows_executables", lambda: tools)


def future_gate(tmp_path: Path) -> Gate:
    sentinel = tmp_path / "ran.txt"
    return Gate(
        name="future-check",
        owner="OWNER-01",
        command=(
            sys.executable,
            "-c",
            f"from pathlib import Path; Path({str(sentinel)!r}).write_text('ran')",
        ),
        required_paths=("owner/ready.json", "owner/check.py"),
        activation_paths=("owner/ready.json",),
        activation_manifest=ActivationManifest("owner/ready.json", MARKER_PAYLOAD),
    )


def test_absent_owner_is_explicitly_unavailable(tmp_path: Path) -> None:
    resolution = resolve_gate(tmp_path, future_gate(tmp_path))
    assert resolution.status == "not_available_until:OWNER-01"


def test_malformed_activation_manifest_is_hard_failure(tmp_path: Path) -> None:
    owner = tmp_path / "owner"
    owner.mkdir()
    (owner / "ready.json").write_text('{"state":"active"}', encoding="utf-8")
    (owner / "check.py").write_text("# executable owner check", encoding="utf-8")
    with pytest.raises(GateContractError, match="activation manifest"):
        resolve_gate(tmp_path, future_gate(tmp_path))


def test_activated_owner_with_missing_check_is_hard_failure(tmp_path: Path) -> None:
    owner = tmp_path / "owner"
    owner.mkdir()
    (owner / "ready.json").write_text(json.dumps(MARKER_PAYLOAD), encoding="utf-8")
    with pytest.raises(GateContractError, match="owner/check.py"):
        resolve_gate(tmp_path, future_gate(tmp_path))


@pytest.mark.parametrize("blocked_name", ("ready.json", "check.py"))
def test_activation_and_required_path_reparse_components_fail_closed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    blocked_name: str,
) -> None:
    owner = tmp_path / "owner"
    owner.mkdir()
    (owner / "ready.json").write_text(json.dumps(MARKER_PAYLOAD), encoding="utf-8")
    (owner / "check.py").write_text("# check", encoding="utf-8")
    blocked = owner / blocked_name
    real_lstat = os.lstat

    def fake_lstat(path: os.PathLike[str] | str) -> os.stat_result:
        observed = real_lstat(path)
        if Path(path) == blocked:
            values = list(observed)
            values[0] = stat.S_IFLNK | stat.S_IRUSR
            return os.stat_result(values)
        return observed

    monkeypatch.setattr(os, "lstat", fake_lstat)
    with pytest.raises(GateContractError, match="reparse"):
        resolve_gate(tmp_path, future_gate(tmp_path))


def test_activation_path_cannot_escape_repository_root(tmp_path: Path) -> None:
    gate = Gate(
        "escape",
        "OWNER-01",
        (sys.executable, "--version"),
        ("required.txt",),
        activation_paths=("../outside",),
    )
    with pytest.raises(GateContractError, match="invalid gate path"):
        resolve_gate(tmp_path, gate)

```

- [ ] **Step 2b: Append activation, fail-fast, output, and environment tests**

Append to `backend/tests/unit/test_runner_gates.py`:

```python


def test_fully_activated_owner_executes(tmp_path: Path) -> None:
    owner = tmp_path / "owner"
    owner.mkdir()
    (owner / "ready.json").write_text(json.dumps(MARKER_PAYLOAD), encoding="utf-8")
    (owner / "check.py").write_text("# executable owner check", encoding="utf-8")
    inventory = inventory_registry(tmp_path, (future_gate(tmp_path),))
    code, results = execute_inventory(tmp_path, inventory)
    assert code == 0
    assert results[0].status == "pass"
    assert (tmp_path / "ran.txt").read_text(encoding="utf-8") == "ran"


def test_first_failure_prevents_later_active_command(tmp_path: Path) -> None:
    required = tmp_path / "required.txt"
    required.write_text("ready", encoding="utf-8")
    registry = (
        Gate(
            "first",
            "T-01F1",
            (sys.executable, "-c", "raise SystemExit(7)"),
            ("required.txt",),
        ),
        Gate(
            "second",
            "T-01F1",
            (sys.executable, "-c", "raise SystemExit(0)"),
            ("required.txt",),
        ),
    )
    code, results = execute_inventory(tmp_path, inventory_registry(tmp_path, registry))
    assert code == 7
    assert [result.status for result in results] == [
        "failed:7",
        "not_run_after_failure:first",
    ]


def test_child_output_is_captured_and_never_forwarded(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    (tmp_path / "required.txt").write_text("ready", encoding="utf-8")
    gate = Gate(
        "redacted",
        "T-01F1",
        (
            sys.executable,
            "-c",
            "import sys; print('SYNTHETIC_STDOUT_SECRET'); "
            "print('SYNTHETIC_STDERR_SECRET', file=sys.stderr)",
        ),
        ("required.txt",),
    )
    code, results = execute_inventory(tmp_path, inventory_registry(tmp_path, (gate,)))
    assert code == 0
    assert results[0].status == "pass"
    captured = capsys.readouterr()
    assert "SYNTHETIC_STDOUT_SECRET" not in captured.out
    assert "SYNTHETIC_STDERR_SECRET" not in captured.err


def test_child_environment_is_allowlisted(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    for key in ("PATH", "PYTHONPATH", "NODE_OPTIONS"):
        monkeypatch.setenv(key, "SYNTHETIC_ENV_SECRET")
    program = (
        "import os; raise SystemExit(9 if any(os.environ.get(key) == "
        "'SYNTHETIC_ENV_SECRET' for key in ('PATH','PYTHONPATH','NODE_OPTIONS')) else 0)"
    )
    assert run_subprocess(
        (sys.executable, "-c", program),
        tmp_path,
        current_test_observation(),
    ) == 0

```

- [ ] **Step 2c: Append timeout-tree and executable-drift tests**

Append to `backend/tests/unit/test_runner_gates.py`:

```python


def test_timeout_terminates_complete_process_tree(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import scripts.projectb_test_runner.gate_run as gate_run

    pid_file = tmp_path / "child.pid"
    heartbeat = tmp_path / "heartbeat.txt"
    child = (
        "import os,time; from pathlib import Path; "
        f"Path({str(pid_file)!r}).write_text(str(os.getpid())); "
        f"p=Path({str(heartbeat)!r}); "
        "[(p.write_text(str(i)), time.sleep(0.05)) for i in range(400)]"
    )
    parent = (
        "import subprocess,sys,time; "
        f"subprocess.Popen([sys.executable, '-c', {child!r}]); time.sleep(30)"
    )
    monkeypatch.setattr(gate_run, "COMMAND_TIMEOUT_SECONDS", 0.5)
    assert run_subprocess(
        (sys.executable, "-c", parent),
        tmp_path,
        current_test_observation(),
    ) == 124
    for _ in range(20):
        if pid_file.is_file() and heartbeat.is_file():
            break
        time.sleep(0.05)
    child_pid = int(pid_file.read_text(encoding="utf-8"))
    previous = heartbeat.read_text(encoding="utf-8")
    time.sleep(0.2)
    assert not psutil.pid_exists(child_pid)
    assert heartbeat.read_text(encoding="utf-8") == previous


def test_executable_observation_is_rechecked_immediately_before_execution(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    executable = tmp_path / "python.exe"
    shutil.copyfile(sys.executable, executable)
    tools = Executables(
        str(executable),
        str(executable),
        str(executable),
        str(executable),
    )
    monkeypatch.setattr(gate_model, "resolve_windows_executables", lambda: tools)
    required = tmp_path / "required.txt"
    required.write_text("ready", encoding="utf-8")
    gate = Gate("identity", "T-01F1", (str(executable), "--version"), ("required.txt",))
    inventory = inventory_registry(tmp_path, (gate,))
    executable.write_bytes(b"mutated-after-inventory")

    with pytest.raises(RuntimeContractError, match="changed"):
        execute_inventory(tmp_path, inventory)
```

- [ ] **Step 3: Run gate-state tests red**

Run the red through `Invoke-CheckedNative` with `$PythonExe`, arguments `@("-m", "pytest", "backend/tests/unit/test_runner_gates.py", "-q")`, and a 300-second timeout.

Expected: the gate-state suite is collected and import fails because the gate modules are absent.

- [ ] **Step 4a: Implement gate records and contained path validation**

Create `scripts/projectb_test_runner/gate_model.py`:

```python
import json
import os
import stat
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from .executables import Executables, resolve_windows_executables
from .runtime import (
    ExecutableObservation,
    assert_observation_unchanged,
    observe_executable,
)


class GateContractError(RuntimeError):
    """A formal gate definition or activated owner contract is incomplete."""


@dataclass(frozen=True)
class ActivationManifest:
    path: str
    expected: Mapping[str, object]


@dataclass(frozen=True)
class Gate:
    name: str
    owner: str
    command: tuple[str, ...]
    required_paths: tuple[str, ...]
    activation_paths: tuple[str, ...] = ()
    activation_manifest: ActivationManifest | None = None

    def __post_init__(self) -> None:
        if not self.name or not self.owner or not self.command or not self.required_paths:
            raise ValueError("gate name, owner, command, and required paths are mandatory")


@dataclass(frozen=True)
class GateState:
    gate: Gate
    status: str
    executable_observation: ExecutableObservation | None = None

    @property
    def active(self) -> bool:
        return self.status == "active"


REPARSE_POINT_ATTRIBUTE = 0x400


def reject_contract_reparse_components(root: Path, candidate: Path) -> None:
    descendants = (
        root.joinpath(*candidate.parts[:index])
        for index in range(1, len(candidate.parts) + 1)
    )
    components = (root, *descendants)
    for current in components:
        try:
            metadata = os.lstat(current)
        except FileNotFoundError:
            break
        except OSError as error:
            raise GateContractError("gate path metadata is unavailable") from error
        attributes = getattr(metadata, "st_file_attributes", 0)
        if stat.S_ISLNK(metadata.st_mode) or bool(attributes & REPARSE_POINT_ATTRIBUTE):
            raise GateContractError("gate path contains a reparse component")


def contract_path(root: Path, relative: str) -> Path:
    path = PurePosixPath(relative)
    if path.is_absolute() or not path.parts or ".." in path.parts:
        raise GateContractError(f"invalid gate path: {relative}")
    absolute_root = Path(os.path.abspath(root))
    reject_contract_reparse_components(absolute_root, Path(*path.parts))
    try:
        resolved_root = absolute_root.resolve(strict=True)
    except OSError as error:
        raise GateContractError("gate root is unavailable") from error
    if os.path.normcase(resolved_root) != os.path.normcase(absolute_root):
        raise GateContractError("gate root resolution changed containment")
    candidate = resolved_root.joinpath(*path.parts)
    if not candidate.is_relative_to(resolved_root):
        raise GateContractError("gate path escapes the repository root")
    return candidate

```

- [ ] **Step 4b: Append executable observation, activation, and state resolution**

Append to `scripts/projectb_test_runner/gate_model.py`:

```python


def validated_executable(
    command: tuple[str, ...],
    executables: Executables | None = None,
) -> ExecutableObservation:
    if not command or not command[0] or "\x00" in command[0]:
        raise GateContractError("gate command has no executable")
    executable = Path(command[0])
    if not executable.is_absolute() or ".." in executable.parts:
        raise GateContractError("gate executable is not absolute")
    resolved = resolve_windows_executables() if executables is None else executables
    allowed = {
        resolved.python,
        resolved.node,
        resolved.npm,
        resolved.powershell,
    }
    if str(executable) not in allowed:
        raise GateContractError("gate executable is not one of the four E1 paths")
    observation = observe_executable(str(executable))
    assert_observation_unchanged(observation)
    return observation


def validate_activation_manifest(root: Path, manifest: ActivationManifest) -> None:
    path = contract_path(root, manifest.path)
    try:
        observed = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise GateContractError("activation manifest is unreadable") from error
    if observed != dict(manifest.expected):
        raise GateContractError("activation manifest differs from the formal contract")


def resolve_gate(
    root: Path,
    gate: Gate,
    executables: Executables | None = None,
) -> GateState:
    activation_exists = [contract_path(root, item).exists() for item in gate.activation_paths]
    if gate.activation_paths and not any(activation_exists):
        return GateState(gate, f"not_available_until:{gate.owner}")
    missing = [
        item for item in gate.required_paths if not contract_path(root, item).is_file()
    ]
    if missing:
        raise GateContractError(
            f"gate={gate.name} owner={gate.owner} activated-but-missing={','.join(missing)}"
        )
    if gate.activation_manifest is not None:
        validate_activation_manifest(root, gate.activation_manifest)
    identity = validated_executable(gate.command, executables)
    return GateState(gate, "active", identity)
```

- [ ] **Step 5a: Implement inventory records and process-tree termination**

Create `scripts/projectb_test_runner/gate_run.py`:

```python
import subprocess
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path

import psutil

from .executables import Executables
from .gate_model import Gate, GateState, resolve_gate
from .runtime import (
    ExecutableObservation,
    assert_observation_unchanged,
    sanitized_runtime_environment,
)

CommandRunner = Callable[[Sequence[str], Path, ExecutableObservation], int]
COMMAND_TIMEOUT_SECONDS = 60.0


@dataclass(frozen=True)
class GateResult:
    name: str
    owner: str
    status: str


def inventory_registry(
    root: Path,
    registry: tuple[Gate, ...],
    executables: Executables | None = None,
) -> tuple[GateState, ...]:
    return tuple(resolve_gate(root, gate, executables) for gate in registry)


def terminate_process_tree(process: subprocess.Popen[str]) -> None:
    try:
        parent = psutil.Process(process.pid)
        descendants = parent.children(recursive=True)
    except psutil.Error:
        descendants = []
    for child in reversed(descendants):
        try:
            child.kill()
        except psutil.Error:
            continue
    try:
        process.kill()
    except OSError:
        pass
    psutil.wait_procs(descendants, timeout=5.0)
    try:
        process.wait(timeout=5.0)
    except subprocess.TimeoutExpired:
        pass

```

- [ ] **Step 5b: Append bounded, redacted child execution**

Append to `scripts/projectb_test_runner/gate_run.py`:

```python


def run_subprocess(
    command: Sequence[str],
    root: Path,
    observation: ExecutableObservation,
) -> int:
    fixed_command = tuple(command)
    invalid_item = any(
        not isinstance(item, str) or "\x00" in item for item in fixed_command
    )
    if not fixed_command or invalid_item:
        return 127
    if fixed_command[0] != observation.path:
        return 127
    assert_observation_unchanged(observation)
    try:
        process = subprocess.Popen(
            fixed_command,
            cwd=root,
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=sanitized_runtime_environment(),
        )
    except OSError:
        return 127
    try:
        process.communicate(timeout=COMMAND_TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired:
        terminate_process_tree(process)
        return 124
    assert_observation_unchanged(observation)
    return process.returncode if process.returncode is not None else 127

```

- [ ] **Step 5c: Append fail-fast execution and shared rendering**

Append to `scripts/projectb_test_runner/gate_run.py`:

```python


def execute_inventory(
    root: Path,
    inventory: tuple[GateState, ...],
    command_runner: CommandRunner = run_subprocess,
) -> tuple[int, tuple[GateResult, ...]]:
    results: list[GateResult] = []
    failed_name: str | None = None
    failed_code = 0
    for resolution in inventory:
        gate = resolution.gate
        if not resolution.active:
            results.append(GateResult(gate.name, gate.owner, resolution.status))
        elif failed_name is not None:
            results.append(
                GateResult(gate.name, gate.owner, f"not_run_after_failure:{failed_name}")
            )
        else:
            if resolution.executable_observation is None:
                raise RuntimeError("active gate has no executable observation")
            return_code = command_runner(
                gate.command,
                root,
                resolution.executable_observation,
            )
            if return_code == 0:
                results.append(GateResult(gate.name, gate.owner, "pass"))
            else:
                failed_name = gate.name
                failed_code = return_code
                results.append(GateResult(gate.name, gate.owner, f"failed:{return_code}"))
    return failed_code, tuple(results)


def list_lines(inventory: tuple[GateState, ...]) -> tuple[str, ...]:
    return tuple(
        f"LIST gate={item.gate.name} owner={item.gate.owner} status={item.status}"
        for item in inventory
    )


def summary_lines(results: tuple[GateResult, ...]) -> tuple[str, ...]:
    return tuple(
        f"SUMMARY gate={item.name} owner={item.owner} status={item.status}"
        for item in results
    )
```

- [ ] **Step 6: Run gate-state tests green**

Run the green through `Invoke-CheckedNative` with `$PythonExe`, arguments `@("-m", "pytest", "backend/tests/unit/test_runner_gates.py", "-q")`, and a 300-second timeout.

Expected: every gate-state test passes.

- [ ] **Step 7: Reverify T-01F1 and prepare two undispatched packets**

Run the checked verification and prepare the distinct packets, but dispatch only after Step 8 stages the exact tree.

```powershell
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "-m", "pytest", "backend/tests/unit/test_runner_gates.py", "-q"
) -FailureMessage "T-01F1 focused tests failed"
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "-m", "ruff", "check", "--config", "backend/pyproject.toml",
    "scripts/projectb_test_runner/gate_model.py",
    "scripts/projectb_test_runner/gate_run.py",
    "backend/tests/unit/test_runner_gates.py"
) -FailureMessage "T-01F1 Ruff check failed"
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "-m", "mypy", "--config-file", "backend/pyproject.toml",
    "scripts/projectb_test_runner/gate_model.py",
    "scripts/projectb_test_runner/gate_run.py"
) -FailureMessage "T-01F1 mypy check failed"
```

- [ ] **Step 8: Stage and scan exactly the three T-01F1 paths**

```powershell
$paths = @(
    "scripts/projectb_test_runner/gate_model.py",
    "scripts/projectb_test_runner/gate_run.py",
    "backend/tests/unit/test_runner_gates.py"
)
Invoke-CheckedGit -ArgumentList (@("add", "--") + $paths) -FailureMessage "T-01F1 git add failed"
Invoke-CheckedGit -ArgumentList @("diff", "--cached", "--check") -FailureMessage "T-01F1 staged diff check failed"
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "scripts/scan_secrets.py", "--staged", "--git-exe", $GitExe
) -TimeoutSeconds 300 -FailureMessage "T-01F1 staged scanner failed"
Assert-ExactStagedPaths -ExpectedPaths $paths
$reviewTree = Get-StagedTreeId
$reviewTree
$reviewPacket = Export-ReviewedStagedDiff -UnitId $env:PROJECTB_UNIT_ID `
    -ExpectedTreeId $reviewTree
$reviewPacket
```

- [ ] **Step 9: Run both staged-tree reviews, revalidate, and commit T-01F1**

```powershell
$ids = @($env:PROJECTB_AGENT_ID, $env:PROJECTB_T01F1_SPEC_REVIEW_ID, $env:PROJECTB_T01F1_QUALITY_REVIEW_ID)
Invoke-FinalPrecommitValidation -UnitId "T-01F1" -ExpectedPaths $paths -Identities $ids `
    -SpecTreeId $env:PROJECTB_T01F1_SPEC_REVIEW_TREE `
    -QualityTreeId $env:PROJECTB_T01F1_QUALITY_REVIEW_TREE -ScannerMode "canonical"
Invoke-CheckedGit -ArgumentList @("commit", "-m", "test(T-01F1): add gate execution primitives [agent: $env:PROJECTB_AGENT_ID]") `
    -FailureMessage "T-01F1 commit failed"
$commitHash = Invoke-CheckedGitText -ArgumentList @("rev-parse", "HEAD") -FailureMessage "T-01F1 hash lookup failed"
Assert-CommittedTreeBinding -UnitId "T-01F1" -ExpectedTreeId $env:PROJECTB_T01F1_SPEC_REVIEW_TREE
if ($commitHash -notmatch "^[0-9a-f]{40}$") { throw "T-01F1 did not produce a full commit hash" }
$commitHash
```

### Task T-01F2: Define Core, Deferred, And Formal Registries

**Unit prelude:** Run the complete Required Fail-Closed Command Prelude before Step 1. Registry gate executables use only the four E1 runtime paths; the secret-scan gate receives the separately resolved coordinator `$GitExe` through the sanitized `PROJECTB_CONTROL_GIT_EXE` handoff.

**Goal:** Define one duplicate-checked 17-gate registry with truthful core/deferred ownership and exact activation rules.

**Dependencies / parallelism:** Requires the reviewed T-01F1 commit. T-01F3 depends on its reviewed commit.

**Files:**
- Create: `scripts/projectb_test_runner/core_registry.py`
- Create: `scripts/projectb_test_runner/deferred_registry.py`
- Create: `scripts/projectb_test_runner/registry.py`
- Test: `backend/tests/unit/test_runner_registry.py`

**Acceptance:** The registry contains exactly 17 unique ordered gates. CI-01 remains `not_available_until:CI-01` until terminal owner CI-01C creates `docs/engineering/gates/CI-01.ready`; after activation, both CI gates require that marker plus all six CI-owned implementation/evidence paths and never depend on `scripts/scan_secrets.py`. Split QA-01A and QA-01C groups expose terminal owners QA-01A2 and QA-01C2 and activate only from their terminal-child paths, so an earlier child commit remains unavailable instead of becoming a partial-owner failure. G-02C2 reads only `docs/engineering/gates/G-02C.ready` as its activation marker, and only G-02C2 owns/writes that exact JSON.

- [ ] **Step 1: Write the failing complete-registry tests**

Run the complete shared prelude before creating the test below:

```powershell
Assert-UnitContext -UnitId "T-01F2"
Assert-ValidIdentity -Role "T-01F2 worker" -Identity $env:PROJECTB_AGENT_ID
```

Create `backend/tests/unit/test_runner_registry.py`:

```python
from scripts.projectb_test_runner.deferred_registry import CI01_MARKER, G02C_MARKER
from scripts.projectb_test_runner.executables import resolve_windows_executables
from scripts.projectb_test_runner.registry import build_registry

EXPECTED_GATE_OWNERS = (
    ("evidence-baseline", "G-02A"),
    ("evidence-provider", "G-02B"),
    ("frontend-contract-tests", "T-01C1"),
    ("frontend-lock-materialization", "T-01C1"),
    ("backend-tests", "T-01F3"),
    ("backend-ruff", "T-01F3"),
    ("backend-mypy", "T-01F3"),
    ("frontend-tests", "T-01C2"),
    ("frontend-build", "T-01C2"),
    ("secret-scan", "T-01D"),
    ("evidence-distribution", "G-02C2"),
    ("browser-e2e", "QA-01A2"),
    ("artifact-redaction", "QA-01C2"),
    ("windows-distribution-contract", "DIST-01"),
    ("oci-distribution-contract", "DIST-02"),
    ("license-scan", "CI-01"),
    ("ci-contract", "CI-01"),
)


def test_registry_has_exactly_17_unique_owned_gates() -> None:
    registry = build_registry(resolve_windows_executables())
    assert tuple((gate.name, gate.owner) for gate in registry) == EXPECTED_GATE_OWNERS
    assert len({gate.name for gate in registry}) == 17


def test_every_registered_command_has_a_resolved_executable() -> None:
    registry = build_registry(resolve_windows_executables())
    assert all(gate.command[0] for gate in registry)
    assert all(gate.command[0].lower().endswith((".exe", ".cmd")) for gate in registry)


def test_g02c_marker_payload_is_exact() -> None:
    assert G02C_MARKER == {
        "contractVersion": 1,
        "gate": "evidence-distribution",
        "owner": "G-02C2",
        "state": "active",
    }


def test_ci01_marker_payload_is_exact() -> None:
    assert CI01_MARKER == {
        "contractVersion": 1,
        "gateOwner": "CI-01",
        "terminalOwner": "CI-01C",
        "state": "active",
    }


def test_ci01_activation_uses_only_ci01_owned_paths() -> None:
    registry = build_registry(resolve_windows_executables())
    ci_gates = [gate for gate in registry if gate.owner == "CI-01"]
    expected_owner_paths = {
        "scripts/verify_licenses.py",
        "scripts/verify_ci_contract.py",
        "backend/tests/integration/test_ci_contract.py",
        ".gitlab-ci.yml",
        ".github/workflows/ci.yml",
        "docs/engineering/CI-01_EVIDENCE.md",
        "docs/engineering/gates/CI-01.ready",
    }
    assert len(ci_gates) == 2
    assert all(set(gate.required_paths) == expected_owner_paths for gate in ci_gates)
    assert all(
        gate.activation_paths == ("docs/engineering/gates/CI-01.ready",)
        for gate in ci_gates
    )
    assert all(gate.activation_manifest is not None for gate in ci_gates)


def test_g02c_activation_reads_only_its_owned_marker() -> None:
    registry = build_registry(resolve_windows_executables())
    gate = next(item for item in registry if item.owner == "G-02C2")
    assert gate.activation_paths == ("docs/engineering/gates/G-02C.ready",)


def test_split_qa_groups_activate_only_from_their_terminal_child_path() -> None:
    registry = build_registry(resolve_windows_executables())
    browser = next(item for item in registry if item.name == "browser-e2e")
    redaction = next(item for item in registry if item.name == "artifact-redaction")
    assert browser.activation_paths == ("frontend/e2e/responsive.spec.ts",)
    assert redaction.activation_paths == ("scripts/check_artifact_redaction.py",)
```

- [ ] **Step 2: Run complete-registry tests red**

Run the red through `Invoke-CheckedNative` with `$PythonExe`, arguments `@("-m", "pytest", "backend/tests/unit/test_runner_registry.py", "-q")`, and a 300-second timeout.

Expected: the complete-registry suite is collected and import fails because registry modules are absent.

- [ ] **Step 3: Define all always-active gates with explicit config commands**

Create `scripts/projectb_test_runner/core_registry.py`:

```python
from .executables import Executables
from .gate_model import Gate


def core_gates(
    executables: Executables,
    control_git_executable: str,
) -> tuple[Gate, ...]:
    return (
        Gate(
            "evidence-baseline",
            "G-02A",
            (
                executables.powershell,
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                "scripts/verify_evidence.ps1",
            ),
            ("scripts/verify_evidence.ps1",),
        ),
        Gate(
            "evidence-provider",
            "G-02B",
            (
                executables.powershell, "-NoProfile", "-ExecutionPolicy", "Bypass",
                "-File", "scripts/verify_evidence.ps1", "-RequireProviderReady",
            ),
            ("scripts/verify_evidence.ps1",),
        ),
        Gate(
            "frontend-contract-tests",
            "T-01C1",
            (
                executables.node, "--test", "scripts/tests/frontend_contract.test.mjs",
                "scripts/tests/frontend_lock_contract.test.mjs",
            ),
            (
                "scripts/tests/frontend_contract.test.mjs",
                "scripts/tests/frontend_lock_contract.test.mjs",
            ),
        ),
        Gate(
            "frontend-lock-materialization",
            "T-01C1",
            (executables.node, "scripts/materialize_frontend_lock.mjs", "--check"),
            (
                "scripts/frontend_lock_contract.mjs", "scripts/materialize_frontend_lock.mjs",
                "docs/engineering/locks/frontend-package-lock.json", "frontend/package.json",
                "frontend/package-lock.json",
            ),
        ),
        Gate(
            "backend-tests",
            "T-01F3",
            (executables.python, "-m", "pytest", "backend/tests", "-q"),
            ("backend/pyproject.toml", "backend/tests/unit/test_runner_cli.py"),
        ),
        Gate(
            "backend-ruff",
            "T-01F3",
            (
                executables.python, "-m", "ruff", "check", "--config",
                "backend/pyproject.toml", "backend/src", "backend/tests",
                "scripts/projectb_test_runner", "scripts/secret_scan", "scripts/scan_secrets.py",
                "scripts/test_all.py",
            ),
            ("backend/pyproject.toml", "scripts/test_all.py"),
        ),
        Gate(
            "backend-mypy",
            "T-01F3",
            (
                executables.python, "-m", "mypy", "--config-file",
                "backend/pyproject.toml", "backend/src", "scripts/projectb_test_runner",
                "scripts/secret_scan", "scripts/scan_secrets.py",
            ),
            ("backend/pyproject.toml", "scripts/projectb_test_runner/contracts.py"),
        ),
        Gate(
            "frontend-tests",
            "T-01C2",
            (executables.npm, "--prefix", "frontend", "run", "test"),
            (
                "frontend/package.json", "frontend/vitest.contract.json",
                "frontend/vite.config.contract.json", "frontend/src/app/App.test.tsx",
            ),
        ),
        Gate(
            "frontend-build",
            "T-01C2",
            (executables.npm, "--prefix", "frontend", "run", "build"),
            ("frontend/package.json", "frontend/tsconfig.json", "frontend/index.html"),
        ),
        Gate(
            "secret-scan",
            "T-01D",
            (
                executables.powershell, "-NoProfile", "-ExecutionPolicy", "Bypass",
                "-File", "scripts/scan_secrets.ps1", "-PythonExe", executables.python,
                "-GitExe", control_git_executable,
            ),
            (
                "scripts/scan_secrets.py", "scripts/scan_secrets.ps1",
                "scripts/secret_scan/encoding.py", "scripts/secret_scan/paths.py",
                "scripts/secret_scan/rules.py",
            ),
        ),
    )
```

- [ ] **Step 4: Define all deferred owner gates and exact activation JSON**

Create `scripts/projectb_test_runner/deferred_registry.py`:

```python
from .executables import Executables
from .gate_model import ActivationManifest, Gate

G02C_MARKER = {
    "contractVersion": 1,
    "gate": "evidence-distribution",
    "owner": "G-02C2",
    "state": "active",
}
CI01_MARKER = {
    "contractVersion": 1,
    "gateOwner": "CI-01",
    "terminalOwner": "CI-01C",
    "state": "active",
}


def deferred_gates(executables: Executables) -> tuple[Gate, ...]:
    qa01a = (
        "frontend/playwright.config.ts",
        "frontend/e2e/core_workflow.spec.ts",
        "frontend/e2e/responsive.spec.ts",
    )
    qa01c = (
        "scripts/check_artifact_redaction.py",
        "backend/tests/integration/test_input_fixture_matrix.py",
        "backend/tests/fixtures/input_matrix/manifest.json",
        "backend/tests/fixtures/input_matrix/build_fixtures.py",
    )
    dist01 = (
        "packaging/windows/build.ps1", "packaging/windows/freezer-manifest.json",
        "packaging/windows/smoke_test.ps1",
        "backend/tests/integration/test_windows_distribution_contract.py",
        "docs/engineering/DIST-01_EVIDENCE.md",
    )
    dist02 = (
        "packaging/oci/Dockerfile", "packaging/oci/entrypoint.sh",
        "packaging/oci/smoke_test.ps1",
        "backend/tests/integration/test_oci_distribution_contract.py",
        "docs/engineering/DIST-02_EVIDENCE.md",
    )
    ci01 = (
        "scripts/verify_licenses.py",
        "scripts/verify_ci_contract.py", "backend/tests/integration/test_ci_contract.py",
        ".gitlab-ci.yml", ".github/workflows/ci.yml", "docs/engineering/CI-01_EVIDENCE.md",
    )
    ci01_ready = "docs/engineering/gates/CI-01.ready"
    return (
        Gate(
            "evidence-distribution",
            "G-02C2",
            (
                executables.powershell, "-NoProfile", "-ExecutionPolicy", "Bypass",
                "-File", "scripts/verify_evidence.ps1", "-RequireDistributionReady",
            ),
            ("docs/engineering/gates/G-02C.ready", "scripts/verify_evidence.ps1"),
            ("docs/engineering/gates/G-02C.ready",),
            ActivationManifest("docs/engineering/gates/G-02C.ready", G02C_MARKER),
        ),
        Gate(
            "browser-e2e", "QA-01A2",
            (executables.npm, "--prefix", "frontend", "run", "e2e"),
            ("frontend/package.json", *qa01a), ("frontend/e2e/responsive.spec.ts",),
        ),
        Gate(
            "artifact-redaction", "QA-01C2",
            (executables.python, "scripts/check_artifact_redaction.py", "artifacts/qa"),
            qa01c, ("scripts/check_artifact_redaction.py",),
        ),
        Gate(
            "windows-distribution-contract", "DIST-01",
            (
                executables.python, "-m", "pytest",
                "backend/tests/integration/test_windows_distribution_contract.py", "-q",
            ),
            dist01, dist01,
        ),
        Gate(
            "oci-distribution-contract", "DIST-02",
            (
                executables.python, "-m", "pytest",
                "backend/tests/integration/test_oci_distribution_contract.py", "-q",
            ),
            dist02, dist02,
        ),
        Gate(
            "license-scan", "CI-01",
            (executables.python, "scripts/verify_licenses.py", "--strict"),
            (*ci01, ci01_ready), (ci01_ready,),
            ActivationManifest(ci01_ready, CI01_MARKER),
        ),
        Gate(
            "ci-contract", "CI-01",
            (executables.python, "scripts/verify_ci_contract.py"),
            (*ci01, ci01_ready), (ci01_ready,),
            ActivationManifest(ci01_ready, CI01_MARKER),
        ),
    )
```

The G-02C2 owner creates `docs/engineering/gates/G-02C.ready` only after its strict distribution validator passes and both G-02C2 reviews clear. The file content is exactly:

```json
{
  "contractVersion": 1,
  "gate": "evidence-distribution",
  "owner": "G-02C2",
  "state": "active"
}
```

Premature, malformed, or partial activation is an exit-2 contract failure.

Terminal owner CI-01C creates `docs/engineering/gates/CI-01.ready` only after the license inventory, CI schema/YAML parity, Windows/OCI artifact policy, canonical local run, and both CI-01C reviews pass. Earlier CI-01A/CI-01B commits must leave the marker absent, so partially implemented CI remains `not_available_until:CI-01`. Its exact JSON is:

```json
{
  "contractVersion": 1,
  "gateOwner": "CI-01",
  "terminalOwner": "CI-01C",
  "state": "active"
}
```

- [ ] **Step 5: Compose and duplicate-check the formal registry**

Create `scripts/projectb_test_runner/registry.py`:

```python
import os
from pathlib import Path

from .core_registry import core_gates
from .deferred_registry import deferred_gates
from .executables import Executables
from .gate_model import Gate


def control_git_path() -> str:
    raw = os.environ.get("PROJECTB_CONTROL_GIT_EXE", "")
    candidate = Path(raw)
    if (
        not candidate.is_absolute()
        or not candidate.is_file()
        or candidate.name.casefold() != "git.exe"
    ):
        raise RuntimeError("PROJECTB_CONTROL_GIT_EXE must be an absolute git.exe leaf")
    return str(candidate.resolve(strict=True))


def build_registry(executables: Executables) -> tuple[Gate, ...]:
    registry = core_gates(executables, control_git_path()) + deferred_gates(executables)
    names = [gate.name for gate in registry]
    if len(names) != 17 or len(set(names)) != 17:
        raise RuntimeError("formal gate registry must contain 17 unique names")
    return registry
```

- [ ] **Step 6: Run complete-registry tests green**

Run the green through `Invoke-CheckedNative` with `$PythonExe`, arguments `@("-m", "pytest", "backend/tests/unit/test_runner_registry.py", "-q")`, and a 300-second timeout.

Expected: every complete-registry contract test passes.

- [ ] **Step 7: Reverify T-01F2 and prepare two undispatched packets**

Run the checked verification and prepare both packets, but dispatch only after Step 8 stages the exact tree.

```powershell
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "-m", "pytest", "backend/tests/unit/test_runner_gates.py",
    "backend/tests/unit/test_runner_registry.py", "-q"
) -FailureMessage "T-01F2 focused tests failed"
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "-m", "ruff", "check", "--config", "backend/pyproject.toml",
    "scripts/projectb_test_runner/core_registry.py",
    "scripts/projectb_test_runner/deferred_registry.py",
    "scripts/projectb_test_runner/registry.py",
    "backend/tests/unit/test_runner_registry.py"
) -FailureMessage "T-01F2 Ruff check failed"
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "-m", "mypy", "--config-file", "backend/pyproject.toml",
    "scripts/projectb_test_runner/core_registry.py",
    "scripts/projectb_test_runner/deferred_registry.py",
    "scripts/projectb_test_runner/registry.py"
) -FailureMessage "T-01F2 mypy check failed"
```

- [ ] **Step 8: Stage and scan exactly the four T-01F2 paths**

```powershell
$paths = @(
    "scripts/projectb_test_runner/core_registry.py",
    "scripts/projectb_test_runner/deferred_registry.py",
    "scripts/projectb_test_runner/registry.py",
    "backend/tests/unit/test_runner_registry.py"
)
Invoke-CheckedGit -ArgumentList (@("add", "--") + $paths) -FailureMessage "T-01F2 git add failed"
Invoke-CheckedGit -ArgumentList @("diff", "--cached", "--check") -FailureMessage "T-01F2 staged diff check failed"
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "scripts/scan_secrets.py", "--staged", "--git-exe", $GitExe
) -TimeoutSeconds 300 -FailureMessage "T-01F2 staged scanner failed"
Assert-ExactStagedPaths -ExpectedPaths $paths
$reviewTree = Get-StagedTreeId
$reviewTree
$reviewPacket = Export-ReviewedStagedDiff -UnitId $env:PROJECTB_UNIT_ID `
    -ExpectedTreeId $reviewTree
$reviewPacket
```

- [ ] **Step 9: Run both staged-tree reviews, revalidate, and commit T-01F2**

```powershell
$ids = @($env:PROJECTB_AGENT_ID, $env:PROJECTB_T01F2_SPEC_REVIEW_ID, $env:PROJECTB_T01F2_QUALITY_REVIEW_ID)
Invoke-FinalPrecommitValidation -UnitId "T-01F2" -ExpectedPaths $paths -Identities $ids `
    -SpecTreeId $env:PROJECTB_T01F2_SPEC_REVIEW_TREE `
    -QualityTreeId $env:PROJECTB_T01F2_QUALITY_REVIEW_TREE -ScannerMode "canonical"
Invoke-CheckedGit -ArgumentList @("commit", "-m", "test(T-01F2): add owner-aware gate registries [agent: $env:PROJECTB_AGENT_ID]") `
    -FailureMessage "T-01F2 commit failed"
$commitHash = Invoke-CheckedGitText -ArgumentList @("rev-parse", "HEAD") -FailureMessage "T-01F2 hash lookup failed"
Assert-CommittedTreeBinding -UnitId "T-01F2" -ExpectedTreeId $env:PROJECTB_T01F2_SPEC_REVIEW_TREE
if ($commitHash -notmatch "^[0-9a-f]{40}$") { throw "T-01F2 did not produce a full commit hash" }
$commitHash
```

### Task T-01F3: Add The Canonical Runner And CLI Shim

**Unit prelude:** Run the complete Required Fail-Closed Command Prelude before Step 1. The runner resolves the four E1 runtime paths and consumes the sanitized `PROJECTB_CONTROL_GIT_EXE` only while building the secret-scan gate.

**Goal:** Compose E1/E2 preflight and F1/F2 registry behavior into the only canonical `scripts/test_all.py` entry.

**Dependencies / parallelism:** Requires the reviewed T-01F2 commit. It is terminal and owns only the three paths below.

**Files:**
- Create: `scripts/projectb_test_runner/runner.py`
- Create: `scripts/test_all.py`
- Test: `backend/tests/unit/test_runner_cli.py`

**Acceptance:** `--list` and execution use one registry, contract failures return 2, child failures propagate, all 17 summary rows are emitted exactly once, and no unavailable owner command runs.

- [ ] **Step 1: Write failing CLI list/summary and partial-owner tests**

Run the complete shared prelude before creating the test below:

```powershell
Assert-UnitContext -UnitId "T-01F3"
Assert-ValidIdentity -Role "T-01F3 worker" -Identity $env:PROJECTB_AGENT_ID
```

Create `backend/tests/unit/test_runner_cli.py`:

```python
import json
import sys
from pathlib import Path

import pytest
from scripts.projectb_test_runner.executables import Executables
from scripts.projectb_test_runner.gate_model import ActivationManifest, Gate
from scripts.projectb_test_runner.runner import main


def row_keys(output: str, prefix: str) -> tuple[tuple[str, str], ...]:
    rows: list[tuple[str, str]] = []
    for line in output.splitlines():
        if line.startswith(prefix):
            fields = dict(field.split("=", 1) for field in line.split()[1:])
            rows.append((fields["gate"], fields["owner"]))
    return tuple(rows)


def make_test_tools() -> Executables:
    executable = Path(sys.executable).resolve(strict=True)
    return Executables(
        str(executable),
        str(executable),
        str(executable),
        str(executable),
    )


def test_list_and_summary_share_one_ordered_registry(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    (tmp_path / "core.txt").write_text("ready", encoding="utf-8")
    registry = (
        Gate(
            "core",
            "T-01F1",
            (sys.executable, "-c", "raise SystemExit(0)"),
            ("core.txt",),
        ),
        Gate(
            "future",
            "OWNER-02",
            (sys.executable, "-c", "raise SystemExit(0)"),
            ("future/ready.json",),
            ("future/ready.json",),
        ),
    )
    executables = make_test_tools()

    def no_preflight(root: Path, tools: Executables) -> None:
        del root, tools

    assert main(
        ["--list"],
        repository_root=tmp_path,
        executables=executables,
        registry=registry,
        preflight=no_preflight,
    ) == 0
    listed = capsys.readouterr().out
    assert main(
        [],
        repository_root=tmp_path,
        executables=executables,
        registry=registry,
        preflight=no_preflight,
    ) == 0
    summarized = capsys.readouterr().out
    assert row_keys(listed, "LIST ") == row_keys(summarized, "SUMMARY ")
    assert "not_available_until:OWNER-02" in listed
    assert "not_available_until:OWNER-02" in summarized


def test_list_fails_on_activated_but_missing_owner(tmp_path: Path) -> None:
    marker = tmp_path / "owner/ready.json"
    marker.parent.mkdir()
    marker.write_text(json.dumps({"state": "active"}), encoding="utf-8")
    gate = Gate(
        "future",
        "OWNER-03",
        (sys.executable, "-c", "raise SystemExit(0)"),
        ("owner/ready.json", "owner/check.py"),
        ("owner/ready.json",),
        ActivationManifest("owner/ready.json", {"state": "active"}),
    )
    tools = make_test_tools()
    assert main(
        ["--list"],
        repository_root=tmp_path,
        executables=tools,
        registry=(gate,),
        preflight=lambda root, resolved: None,
    ) == 2


def test_active_child_failure_is_propagated(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    (tmp_path / "required.txt").write_text("ready", encoding="utf-8")
    gate = Gate(
        "failed", "T-01F1", (sys.executable, "-c", "raise SystemExit(9)"),
        ("required.txt",),
    )
    tools = make_test_tools()
    assert main(
        [],
        repository_root=tmp_path,
        executables=tools,
        registry=(gate,),
        preflight=lambda root, resolved: None,
    ) == 9
    assert "status=failed:9" in capsys.readouterr().out
```

- [ ] **Step 2: Run CLI tests red**

Run the red through `Invoke-CheckedNative` with `$PythonExe`, arguments `@("-m", "pytest", "backend/tests/unit/test_runner_cli.py", "-q")`, and a 300-second timeout.

Expected: the CLI suite is collected and import fails because `runner.py` is absent.

- [ ] **Step 3: Implement exact preflight, list, execution, and final summary**

Create `scripts/projectb_test_runner/runner.py`:

```python
import argparse
from collections.abc import Callable, Sequence
from pathlib import Path

from .contracts import ContractError, verify_repository_contracts
from .executables import (
    ExecutableResolutionError,
    Executables,
    resolve_windows_executables,
)
from .gate_model import Gate, GateContractError
from .gate_run import (
    CommandRunner,
    execute_inventory,
    inventory_registry,
    list_lines,
    run_subprocess,
    summary_lines,
)
from .locks import verify_lock_contract
from .registry import build_registry
from .runtime import RuntimeContractError, verify_exact_runtimes

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
Preflight = Callable[[Path, Executables], None]


def perform_preflight(root: Path, executables: Executables) -> None:
    verify_exact_runtimes(executables)
    verify_repository_contracts(root)
    verify_lock_contract(root)


def parse_arguments(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run canonical ProjectB gates")
    parser.add_argument("--list", action="store_true")
    return parser.parse_args(argv)


def main(
    argv: Sequence[str] | None = None,
    *,
    repository_root: Path = REPOSITORY_ROOT,
    executables: Executables | None = None,
    registry: tuple[Gate, ...] | None = None,
    preflight: Preflight = perform_preflight,
    command_runner: CommandRunner = run_subprocess,
) -> int:
    arguments = parse_arguments(argv)
    try:
        resolved = resolve_windows_executables() if executables is None else executables
        selected = build_registry(resolved) if registry is None else registry
        preflight(repository_root, resolved)
        inventory = inventory_registry(repository_root, selected, resolved)
    except (
        ContractError,
        ExecutableResolutionError,
        GateContractError,
        RuntimeContractError,
        RuntimeError,
        OSError,
        ValueError,
    ) as error:
        print(f"TEST_ALL_CONTRACT_ERROR type={type(error).__name__}")
        return 2
    if arguments.list:
        for line in list_lines(inventory):
            print(line)
        return 0
    exit_code, results = execute_inventory(
        repository_root, inventory, command_runner=command_runner
    )
    for line in summary_lines(results):
        print(line)
    if exit_code != 0:
        print(f"TEST_ALL_FAIL code={exit_code}")
        return exit_code
    print("TEST_ALL_PASS")
    return 0
```

- [ ] **Step 4: Create the canonical import-safe entry shim**

Create `scripts/test_all.py`:

```python
import sys
from importlib import import_module
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

main = import_module("scripts.projectb_test_runner.runner").main


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 5: Run CLI tests green**

Run the green through `Invoke-CheckedNative` with `$PythonExe`, arguments `@("-m", "pytest", "backend/tests/unit/test_runner_cli.py", "-q")`, and a 300-second timeout.

Expected: every CLI contract test passes.

- [ ] **Step 5b: Prove warning-clean pytest collection**

```powershell
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "-W", "error", "-m", "pytest", "--collect-only", "-q",
    "backend/tests/unit/test_runner_cli.py"
) -TimeoutSeconds 300 -FailureMessage "T-01F3 warning-clean collection failed"
```

Expected: collection exits 0 with no `PytestReturnNotNoneWarning` or other warning. The helper is named `make_test_tools`, so pytest never collects it as a test.

- [ ] **Step 6: Reverify all focused T-01F1/F2/F3 tests and static analysis**

Run:

```powershell
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "-m", "pytest", "backend/tests/unit/test_runner_gates.py",
    "backend/tests/unit/test_runner_registry.py",
    "backend/tests/unit/test_runner_cli.py", "-q"
) -TimeoutSeconds 900 -FailureMessage "T-01F3 focused tests failed"
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "-m", "ruff", "check", "--config", "backend/pyproject.toml",
    "scripts/projectb_test_runner", "scripts/test_all.py",
    "backend/tests/unit/test_runner_gates.py",
    "backend/tests/unit/test_runner_registry.py",
    "backend/tests/unit/test_runner_cli.py"
) -TimeoutSeconds 300 -FailureMessage "T-01F3 Ruff failed"
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "-m", "mypy", "--config-file", "backend/pyproject.toml",
    "scripts/projectb_test_runner"
) -TimeoutSeconds 300 -FailureMessage "T-01F3 mypy failed"
```

Expected: every focused T-01F test passes; Ruff and mypy exit 0.

- [ ] **Step 7: Verify the actual 17-row registry listing**

Run the listing through `Invoke-CheckedNative` with `$PythonExe`, arguments `@("scripts/test_all.py", "--list")`, and a 900-second timeout.

Expected: exactly 17 `LIST` rows in declared order. The 10 core rows are `active`; each wholly absent deferred owner is reported with its literal owner ID. `G-02C2` is `not_available_until:G-02C2` while its marker is absent. Any partial deferred owner exits 2.

- [ ] **Step 8: Run the canonical entry and verify the complete summary**

Run the canonical entry through `Invoke-CheckedNative` with `$PythonExe`, arguments `@("scripts/test_all.py")`, and a 1800-second timeout.

Expected: every active gate passes; all 17 gates appear once in `SUMMARY` in list order; absent deferred owners retain `not_available_until:` status; final line is `TEST_ALL_PASS`. No remote, provider, browser E2E, distribution build, or deployment command runs while its owner is unavailable.

- [ ] **Step 9: Prepare the T-01F3 SPEC packet; do not dispatch before staging**

Prepare these complete inputs and questions, but dispatch only after Step 11 produces the exact staged diff and tree ID; the frozen fragment remains prohibited.

- [ ] **Step 10: Prepare the T-01F3 quality/security packet; do not dispatch**

Prepare the distinct quality/security questions, but dispatch only after final staging.

- [ ] **Step 11: Stage exactly three F3 paths, run the canonical staged scanner, and inspect the diff**

Run:

```powershell
$paths = @(
    "scripts/projectb_test_runner/runner.py",
    "scripts/test_all.py",
    "backend/tests/unit/test_runner_cli.py"
)
Invoke-CheckedGit -ArgumentList (@("add", "--") + $paths) -FailureMessage "T-01F3 git add failed"
Invoke-CheckedGit -ArgumentList @("diff", "--cached", "--check") -FailureMessage "T-01F3 staged diff check failed"
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "scripts/scan_secrets.py", "--staged", "--git-exe", $GitExe
) -TimeoutSeconds 300 -FailureMessage "T-01F3 staged scanner failed"
Assert-ExactStagedPaths -ExpectedPaths $paths
$reviewTree = Get-StagedTreeId
$reviewTree
$reviewPacket = Export-ReviewedStagedDiff -UnitId $env:PROJECTB_UNIT_ID `
    -ExpectedTreeId $reviewTree
$reviewPacket
```

Expected: scanner and whitespace checks exit 0 and exactly three F3 paths are staged.

- [ ] **Step 12: Run both staged-tree reviews, revalidate, and commit T-01F3**

Run:

```powershell
$ids = @(
    $env:PROJECTB_AGENT_ID,
    $env:PROJECTB_T01F3_SPEC_REVIEW_ID,
    $env:PROJECTB_T01F3_QUALITY_REVIEW_ID
)
Invoke-FinalPrecommitValidation -UnitId "T-01F3" -ExpectedPaths $paths -Identities $ids `
    -SpecTreeId $env:PROJECTB_T01F3_SPEC_REVIEW_TREE `
    -QualityTreeId $env:PROJECTB_T01F3_QUALITY_REVIEW_TREE -ScannerMode "canonical"
Invoke-CheckedGit -ArgumentList @("commit", "-m", "test(T-01F3): publish canonical project test entry [agent: $env:PROJECTB_AGENT_ID]") `
    -FailureMessage "T-01F3 commit failed"
$commitHash = Invoke-CheckedGitText -ArgumentList @("rev-parse", "HEAD") -FailureMessage "T-01F3 hash lookup failed"
Assert-CommittedTreeBinding -UnitId "T-01F3" -ExpectedTreeId $env:PROJECTB_T01F3_SPEC_REVIEW_TREE
if ($commitHash -notmatch "^[0-9a-f]{40}$") { throw "T-01F3 did not produce a full commit hash" }
$commitHash
```

Expected: one three-path F3 commit and its actual hash. The coordinator records all ten unit hashes and 20 review identities before marking root T-01 complete.

## Root T-01 Completion Standard

Root T-01 is complete only after all ten reviewed commits are integrated in dependency order, the path-map union is exactly 49 files, every task's recorded red/green/refactor/focused/full/scan/commit/hash evidence is distinct and current, and bounded checked invocations of `scripts/test_all.py --list` and `scripts/test_all.py` cover the same 17 gates. Scanner and raw-lock proofs must pass, and the coordinator synchronizes `PLAN.md`/`AGENT_LOG.md`. No local result is remote CI, distribution, deployment, or public-WebUI evidence; those owners remain explicitly unavailable until their own reviewed tasks activate.
