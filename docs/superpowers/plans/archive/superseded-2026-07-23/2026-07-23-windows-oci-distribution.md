# Windows and OCI Distribution Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a reproducible Windows x64 single-file `ProjectB.exe` and a locked `linux/amd64` OCI demo image while preserving ProjectB's local-data, loopback, mock-only, no-secret, no-upload, no-private-persistence, and no-provider-egress boundaries.

**Architecture:** DIST-01 builds the reviewed local application and frontend into one PyInstaller executable, keeps every mutable byte under an external application-data root, and proves startup/readiness/health/credential-status/graceful-shutdown behavior on both the build host and a clean Windows x64 host. DIST-02 consumes the reviewed demo profile and the DIST-01 resource-layout contract, builds the frontend in a digest-pinned Node stage, runs the backend in the digest-pinned Python image as a non-root user, installs a process-wide outbound-network deny hook, and validates local OCI behavior without publishing or deploying anything.

**Tech Stack:** CPython 3.14.6, Node.js 24.18.0/npm 11.16.0, PyInstaller 6.21.0, PowerShell 5.1 or 7, Docker/BuildKit with OCI images, `node:24.18.0-bookworm-slim` linux/amd64 manifest `sha256:d45d78e7929b46875bbd4e29bea672d5bc48186c6c3588306521c815e78352d6`, `python:3.14.6-slim-bookworm` linux/amd64 manifest `sha256:f70215e5dbe2a47dee6d23f9c6d358bf3c148f59cce2fd165b61118e9d80f2bb`, pytest 9.1.1, Ruff 0.15.22, and mypy 2.3.0.

---

## Status and Dispatch Boundary

This plan covers exactly root dispatch units `DIST-01` and `DIST-02`. It does not cover G-02C2, D-025, CI-01, DOC-01, DEPLOY-01, FIN-01, release publication, signing, account creation, registry mutation, remote push, public deployment, or external-browser evidence. It is Stage B planning input only: no implementation, test, build, clean-machine run, Docker run, review, commit, public URL, or distribution PASS is claimed here.

The authoring input is root `PLAN.md` SHA-256 `5536BC38402EFE250CF4BEF8ACC44CA91AF0B0A4B10CDD80902A3D632AE71A91` and `docs/engineering/DETAILED_PLAN_AUTHORING_CONTRACT.md` SHA-256 `B93F949DE36CD89C7101160F237D4FEBCD7305F411C55B20429D62A282DBBFEF`. The superseded detailed-plan hash `CB497CFCD2F2F07F2535FFDD120EB3A8BA93647066635BB3D733D8E341F4114A` is not PASS evidence. These hashes identify the immutable authoring snapshot only. Final cross-plan PASS is blocked until the coordinator supplies reviewed terminal hashes for every direct predecessor, rebases this plan to the then-current root hash, and obtains two fresh reviews on the same bytes.

The following predecessor interfaces are intentionally not guessed:

- DIST-01 requires reviewed terminal hashes for QA-01C2, QA-02C, API-04B, API-REG-01, the production frontend build, and G-02A. The predecessor set must expose `create_app(profile="local")`, `GET /api/health` with exactly `{"status":"ok","profile":"local"}`, `GET /api/settings/credentials/{profile_id}/status` with a value-free unconfigured result, and startup-time creation of `projectb.sqlite3` beneath `PROJECTB_DATA_ROOT`.
- DIST-02 requires reviewed terminal hashes for DEMO-01C2, DIST-01, QA-01C2, DEMO-REG-01, and G-02C2 exactly as root `PLAN.md` declares. D-025 and G-02C2 are currently blocked, so DIST-02 implementation dispatch is blocked even though this host-independent plan can be authored offline.
- The official Docker Library Node metadata used while authoring gives the exact linux/amd64 manifest above, but that row is not yet in the coordinator-owned distribution evidence ledger. Before DIST-02 review may PASS, G-02 evidence must bind that digest, source snapshot, license/notices, and compatibility without silently mutating this plan.
- `backend/requirements-windows-x64.lock` is a hard Windows architecture artifact and DIST-02 must never install, copy, rename, filter, or reinterpret it on Linux. Before cross-plan PASS, the coordinator must amend root `PLAN.md` and G-02A with a named owner for a separately resolved, hash-locked `packaging/oci/requirements-linux-amd64.lock`, record exact linux/amd64 compatibility and license evidence, and re-review this plan. DIST-02 consumes that committed path read-only; it does not stage the lock in its seven-path commit and never falls back to unpinned resolution.

No worker may treat these blocks as permission to edit a predecessor. A mismatch returns to the owning plan and forces a new root/subplan snapshot review.

## Dependency and Integration Order

```text
QA-01C2 + QA-02C + API-04B + API-REG-01 + G-02A
                         |
                      DIST-01
                         |
DEMO-01C2 + DEMO-REG-01 + QA-01C2 + G-02C2
                         |
                      DIST-02
                         |
                  CI-01A / CI-01B
                         |
                 DEPLOY-01 (external)
```

- DIST-01 runs only after all five direct predecessors have recorded commit/review evidence. It owns no application launcher, API, frontend source, dependency lock, user data, release, or signing path.
- DIST-02 runs only after reviewed DIST-01 and all other declared predecessors, including G-02C2. It serially modifies the DEMO-01A-owned `demo/profile.json`; no demo-profile or fixture edit may run in parallel.
- CI-01A consumes both distribution artifacts and inventories. CI-01B/CI-01C later own CI workflow execution. DEPLOY-01 alone may push an image, mutate a host, expose a URL, or record an external-browser observation.

## Exact Path Ownership and Handoffs

| Unit | Exact owned paths | Ownership rule |
| --- | --- | --- |
| DIST-01 | `packaging/windows/build.ps1`; `packaging/windows/freezer-manifest.json`; `packaging/windows/smoke_test.ps1`; `backend/tests/integration/test_windows_distribution_contract.py`; `docs/engineering/DIST-01_EVIDENCE.md` | Five-path unit. Build outputs under `dist/` and temporary smoke data are untracked evidence inputs, never staged. |
| DIST-02 | `packaging/oci/Dockerfile`; `packaging/oci/entrypoint.sh`; `.dockerignore`; `packaging/oci/smoke_test.ps1`; `backend/tests/integration/test_oci_distribution_contract.py`; `docs/engineering/DIST-02_EVIDENCE.md`; conditional `demo/profile.json` handoff | Six required paths plus one conditional profile path. `demo/profile.json` is included in the staged set only when DIST-02 applies an explicitly permitted additive handoff edit; if the reviewed profile is already byte-identical at unit start, it remains read-only and is excluded. Local images, containers, SBOM copies, and smoke artifacts are untracked. |

The two owned sets are pairwise disjoint. `demo/profile.json` is handed DEMO-01A -> DIST-02 and then frozen for deployment; DIST-02 may add only the reviewed runtime/distribution fields shown below and may not change session, quota, fixture, provider, or capability semantics. `.dockerignore` is first published by DIST-02 and later consumed without modification by CI/deployment. Evidence files pass read-only to CI-01A/DOC-01/FIN-01A1.

## Frozen Distribution Contracts

### DIST-01 Windows contract

- The only user-facing build artifact is `dist/ProjectB.exe`. It is a PE32+ Windows x64 PyInstaller 6.21.0 one-file executable with version `0.1.0`; no sidecar runtime, DLL, static directory, Python, Node, Docker, test, credential, private fixture, or user database is distributed beside it.
- The embedded launcher is generated deterministically by `build.ps1`, imports only the reviewed `create_app(profile="local")` factory, serves frontend resources from the frozen `_MEIPASS/projectb_static` directory, and binds exactly `127.0.0.1` on an explicit port. It accepts only `--port`, `--data-root`, `--ready-file`, `--shutdown-file`, and `--no-browser`.
- `--data-root`, `--ready-file`, and `--shutdown-file` must be absolute. Mutable SQLite, cache, material, log, ready, and shutdown bytes are outside the executable directory. The default application-data location is `%LOCALAPPDATA%\ProjectB`; smoke tests always pass an isolated explicit root.
- The ready file is atomically written UTF-8 JSON with exactly `schemaVersion`, `status`, `profile`, `scheme`, `host`, `port`, and `pid`; values are `1`, `"ready"`, `"local"`, `"http"`, `"127.0.0.1"`, the selected port, and the current PID. It contains no token, course field, file path, or credential status.
- Creating the shutdown marker requests Uvicorn graceful shutdown. The process must exit 0 within ten seconds, close the listener, remove no user data, and leave neither ready/shutdown control file nor a child process. Forced termination is failure evidence.
- Stable script/result codes are `dist_invalid_argument`, `dist_input_drift`, `dist_build_failed`, `dist_artifact_invalid`, `dist_start_failed`, `dist_ready_timeout`, `dist_health_failed`, `dist_credential_status_failed`, `dist_sqlite_failed`, `dist_bind_violation`, `dist_shutdown_timeout`, `dist_residue_found`, and `dist_evidence_invalid`. Errors expose a code/count/exit status only; child output, paths, response bodies, environment values, and matched scanner text are not echoed.
- Evidence schema version 1 binds the source commit, Python/Node/npm/PyInstaller versions, two lock hashes, Windows version/architecture, artifact SHA-256 and size, Authenticode status (`signed_valid`, `unsigned`, or `invalid`), SmartScreen observation (`warning_observed`, `no_warning_observed`, or `not_observed`), build-host smoke, clean-host smoke, runtime-absence checks, exact command IDs, start/end UTC, and redacted residue counts. A clean-host PASS requires an actual Windows x64 host with no installed Python, Node, or Docker and a non-`not_observed` SmartScreen result.

### DIST-02 OCI contract

- The builder is exactly `node:24.18.0-bookworm-slim` linux/amd64 manifest `sha256:d45d78e7929b46875bbd4e29bea672d5bc48186c6c3588306521c815e78352d6`. The final image is exactly `python:3.14.6-slim-bookworm` linux/amd64 manifest `sha256:f70215e5dbe2a47dee6d23f9c6d358bf3c148f59cce2fd165b61118e9d80f2bb`. Floating tags, implicit architecture, unpinned package install, remote `ADD`, and install scripts are rejected.
- The final runtime user/group is `10001:10001`; it has no shell-selected credential store, no Docker volume, no production adapter selection, no arbitrary upload/path/URL capability, and no persistent data directory. Runtime state is exactly `/tmp/projectb-demo`, supplied by a 64 MiB `tmpfs` in the one documented `docker run` command.
- `PROJECTB_PROFILE=demo`, `PROJECTB_PROVIDER_ADAPTER=deterministic.mock`, `PROJECTB_EGRESS_POLICY=deny`, and `PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring` are immutable image defaults validated again by `entrypoint.sh`. Any credential-shaped environment name, production adapter, changed data root, non-deny egress policy, positional argument, or root UID exits with a stable code before app import.
- The embedded OCI launcher installs a Python audit hook before importing the app. `socket.getaddrinfo`, `socket.connect`, and `socket.connect_ex` reject every non-loopback IP/hostname with `demo_egress_denied`; Unix-domain sockets and loopback health traffic remain allowed. The demo API must independently keep upload, credential, production adapter, and provider paths unregistered/forbidden.
- `demo/profile.json` schema version 1 fixes 30-minute idle TTL, two-hour absolute TTL, one active course, twenty fixture materials, two concurrent jobs, 64 MiB state, sixty requests per IP per minute, caller-scoped reset, opaque session IDs, synthetic CC0 fixtures, deterministic mock, no credentials, no upload/path/URL, no production adapter, no private persistence, and restart-clears-state.
- The image installs only `packaging/oci/requirements-linux-amd64.lock` with `--require-hashes`; any Windows lock reference or unpinned install is a contract failure. It includes `licenses/sbom.spdx.json` with SPDX 2.3 package records for Python and Debian runtime packages, dependency baseline/Linux-lock provenance, and copied installed license/notice files. DIST-02 checks the SBOM, fixture license metadata, image config, build context, image history, labels, and final filesystem without claiming CI-01's later full compatibility verdict.
- Stable script/result codes are `oci_invalid_argument`, `oci_engine_failed`, `oci_contract_invalid`, `oci_image_invalid`, `oci_history_rejected`, `oci_sbom_invalid`, `oci_start_failed`, `oci_ready_timeout`, `oci_profile_failed`, `oci_isolation_failed`, `oci_quota_failed`, `oci_capability_leak`, `oci_shutdown_timeout`, `oci_cleanup_failed`, and `oci_evidence_invalid`.
- DIST-02 evidence always records `publicUrl.status=not_executed` and `deployment.status=not_executed`. It never creates a registry, host, account, subscription, payment method, public URL, or external-browser result. DEPLOY-01 alone replaces those values in later evidence bound to immutable candidate C.

## Fail-Closed Runtime Prelude

Every dispatch executes this complete prelude in its own worktree before the first file edit and keeps the same PowerShell session for the unit. It validates all root runtime metadata, invokes every native process with a timeout and sanitized output, compares the whole Git index, stores the full binary staged diff only in a current-user ACL directory, and binds both reviews plus the commit to one tree.

```powershell
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$RootPlanSha = $env:PROJECTB_ROOT_PLAN_SHA256
$DetailedPlanSha = $env:PROJECTB_DETAILED_PLAN_SHA256
$UnitId = $env:PROJECTB_UNIT_ID
$BaseCommit = $env:PROJECTB_BASE_COMMIT
$WorktreeRoot = $env:PROJECTB_WORKTREE_ROOT
$PythonExe = $env:PROJECTB_PYTHON_EXE
$NodeExe = $env:PROJECTB_NODE_EXE
$NpmCmd = $env:PROJECTB_NPM_CMD
$PowerShellExe = $env:PROJECTB_POWERSHELL_EXE
$DockerExe = $env:PROJECTB_DOCKER_EXE
$HumanModifications = $env:PROJECTB_HUMAN_MODIFICATIONS

if ($RootPlanSha -cne "5536BC38402EFE250CF4BEF8ACC44CA91AF0B0A4B10CDD80902A3D632AE71A91" -or
    $DetailedPlanSha -notmatch "^[0-9A-Fa-f]{64}$" -or
    $UnitId -notmatch "^(DIST-01|DIST-02)$" -or
    $BaseCommit -notmatch "^[0-9a-f]{40}$" -or
    $env:PROJECTB_AGENT_ID -notmatch "^[A-Za-z0-9][A-Za-z0-9._-]{1,63}$" -or
    [string]::IsNullOrWhiteSpace($HumanModifications) -or
    $HumanModifications.Length -gt 256 -or
    $HumanModifications -match "[\r\n]" -or
    $HumanModifications -match "(?i)(api[_-]?key|token|password|secret|credential)\s*[:=]") {
    throw "distribution context metadata invalid"
}
if ([string]::IsNullOrWhiteSpace($WorktreeRoot) -or
    -not [IO.Path]::IsPathFullyQualified($WorktreeRoot) -or
    -not (Test-Path -LiteralPath $WorktreeRoot -PathType Container)) {
    throw "distribution worktree root invalid"
}
$WorktreeRoot = (Resolve-Path -LiteralPath $WorktreeRoot -ErrorAction Stop).Path

function Assert-AbsoluteLeaf {
    param([Parameter(Mandatory)][string]$Path,[Parameter(Mandatory)][string]$Label)
    if ([string]::IsNullOrWhiteSpace($Path) -or
        -not [IO.Path]::IsPathFullyQualified($Path) -or
        -not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        throw "$Label runtime is not an absolute existing leaf"
    }
    $current = [IO.Path]::GetPathRoot($Path)
    foreach ($part in $Path.Substring($current.Length).Split(
        @("\", "/"), [StringSplitOptions]::RemoveEmptyEntries
    )) {
        $current = Join-Path $current $part
        $item = Get-Item -LiteralPath $current -Force -ErrorAction Stop
        if (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
            throw "$Label runtime path contains a reparse component"
        }
    }
}

Assert-AbsoluteLeaf -Path $PythonExe -Label "python"
Assert-AbsoluteLeaf -Path $NodeExe -Label "node"
Assert-AbsoluteLeaf -Path $NpmCmd -Label "npm"
Assert-AbsoluteLeaf -Path $PowerShellExe -Label "powershell"
Assert-AbsoluteLeaf -Path $DockerExe -Label "docker"
if ([IO.Path]::GetFileName($DockerExe).ToLowerInvariant() -ne "docker.exe") {
    throw "docker executable leaf is not allowlisted"
}
$gitCommand = Get-Command git.exe -CommandType Application -ErrorAction Stop |
    Select-Object -First 1
$GitExe = $gitCommand.Source
Assert-AbsoluteLeaf -Path $GitExe -Label "git"
if ([IO.Path]::GetFileName($GitExe).ToLowerInvariant() -ne "git.exe") {
    throw "git control-plane leaf invalid"
}

function ConvertTo-SafeArgument {
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

function Stop-NativeTree {
    param([Parameter(Mandatory)][Diagnostics.Process]$Process)
    $rootId = $Process.Id
    $descendants = New-Object Collections.Generic.List[int]
    $queue = New-Object Collections.Generic.Queue[int]
    $queue.Enqueue($rootId)
    while ($queue.Count -gt 0) {
        $parent = $queue.Dequeue()
        $children = @(Get-CimInstance Win32_Process -Filter "ParentProcessId=$parent" `
            -ErrorAction SilentlyContinue)
        foreach ($child in $children) {
            $childId = [int]$child.ProcessId
            $descendants.Add($childId)
            $queue.Enqueue($childId)
        }
    }
    foreach ($childId in @($descendants.ToArray() | Sort-Object -Descending)) {
        Stop-Process -Id $childId -Force -ErrorAction SilentlyContinue
    }
    Stop-Process -Id $rootId -Force -ErrorAction SilentlyContinue
    $deadline = [Diagnostics.Stopwatch]::StartNew()
    do {
        $alive = @(Get-Process -Id (@($rootId) + $descendants.ToArray()) `
            -ErrorAction SilentlyContinue)
        if ($alive.Count -gt 0) { Start-Sleep -Milliseconds 25 }
    } while ($alive.Count -gt 0 -and $deadline.ElapsedMilliseconds -lt 5000)
    if ($alive.Count -gt 0) { throw "native process-tree cleanup failed" }
}

function ConvertTo-RedactedDiagnostic {
    param([AllowEmptyString()][string]$Text,[int]$MaximumCharacters = 8192)
    $value = $Text.Replace($WorktreeRoot, "[WORKTREE]")
    $value = $value -replace '(?i)sk-(?:proj-)?[A-Za-z0-9_-]{12,}', '[REDACTED]'
    $value = $value -replace '(?i)(api[_-]?key|token|password|secret|private[_-]?key)\s*[:=]\s*\S+', '$1=[REDACTED]'
    if ($value.Length -gt $MaximumCharacters) {
        $value = $value.Substring(0, $MaximumCharacters) + "[TRUNCATED]"
    }
    return $value
}

function Invoke-BoundedNative {
    param(
        [Parameter(Mandatory)][string]$FilePath,
        [AllowEmptyCollection()][string[]]$ArgumentList = @(),
        [ValidateRange(1,3600)][int]$TimeoutSeconds = 300,
        [ValidateRange(1024,4194304)][int]$MaximumOutputCharacters = 8192
    )
    Assert-AbsoluteLeaf -Path $FilePath -Label "native"
    $start = [Diagnostics.ProcessStartInfo]::new()
    $start.FileName = $FilePath
    $start.Arguments = (($ArgumentList | ForEach-Object {
        ConvertTo-SafeArgument -Value ([string]$_)
    }) -join ' ')
    $start.WorkingDirectory = $WorktreeRoot
    $start.UseShellExecute = $false
    $start.CreateNoWindow = $true
    $start.RedirectStandardOutput = $true
    $start.RedirectStandardError = $true
    $allowedEnvironment = @(
        "SystemRoot", "WINDIR", "TEMP", "TMP", "LOCALAPPDATA", "USERPROFILE", "HOME"
    )
    $start.EnvironmentVariables.Clear()
    foreach ($key in $allowedEnvironment) {
        $value = [Environment]::GetEnvironmentVariable($key)
        if (-not [string]::IsNullOrWhiteSpace($value)) {
            $start.EnvironmentVariables[$key] = $value
        }
    }
    $runtimePath = @(
        Split-Path -Parent $PythonExe
        Split-Path -Parent $NodeExe
        Split-Path -Parent $NpmCmd
        Split-Path -Parent $PowerShellExe
        Split-Path -Parent $GitExe
        (Join-Path $env:SystemRoot "System32")
    ) | Sort-Object -Unique
    $start.EnvironmentVariables["PATH"] = $runtimePath -join ';'
    foreach ($key in @(
        "PROJECTB_PYTHON_EXE", "PROJECTB_NODE_EXE", "PROJECTB_NPM_CMD",
        "PROJECTB_POWERSHELL_EXE", "PROJECTB_WORKTREE_ROOT", "PROJECTB_UNIT_ID",
        "PROJECTB_BASE_COMMIT", "PROJECTB_ROOT_PLAN_SHA256",
        "PROJECTB_DETAILED_PLAN_SHA256", "PROJECTB_AGENT_ID",
        "PROJECTB_HUMAN_MODIFICATIONS", "PROJECTB_DOCKER_EXE",
        "PROJECTB_DEMO_T04_TRANSPORT", "DOCKER_CONFIG"
    )) {
        $value = [Environment]::GetEnvironmentVariable($key)
        if (-not [string]::IsNullOrWhiteSpace($value)) {
            $start.EnvironmentVariables[$key] = $value
        }
    }
    $process = [Diagnostics.Process]::new()
    $process.StartInfo = $start
    try {
        try {
            if (-not $process.Start()) { throw "native launch failed" }
        } catch {
            throw "native launch failed"
        }
        $stdoutTask = $process.StandardOutput.ReadToEndAsync()
        $stderrTask = $process.StandardError.ReadToEndAsync()
        if (-not $process.WaitForExit($TimeoutSeconds * 1000)) {
            Stop-NativeTree -Process $process
            throw "native command timed out"
        }
        $stdout = ConvertTo-RedactedDiagnostic `
            -Text $stdoutTask.GetAwaiter().GetResult() `
            -MaximumCharacters $MaximumOutputCharacters
        $stderr = ConvertTo-RedactedDiagnostic `
            -Text $stderrTask.GetAwaiter().GetResult() `
            -MaximumCharacters $MaximumOutputCharacters
        return [pscustomobject]@{
            ExitCode = $process.ExitCode
            Stdout = $stdout
            Stderr = $stderr
        }
    } finally {
        $process.Dispose()
    }
}

function Invoke-CheckedNative {
    param(
        [Parameter(Mandatory)][string]$FilePath,
        [AllowEmptyCollection()][string[]]$ArgumentList = @(),
        [ValidateRange(1,3600)][int]$TimeoutSeconds = 300,
        [string]$FailureCode = "native_failed"
    )
    $result = Invoke-BoundedNative -FilePath $FilePath -ArgumentList $ArgumentList `
        -TimeoutSeconds $TimeoutSeconds
    if ($result.ExitCode -ne 0) { throw "$FailureCode exit=$($result.ExitCode)" }
    return $result
}

function Invoke-CheckedGit {
    param([Parameter(Mandatory)][string[]]$Arguments)
    return Invoke-CheckedNative -FilePath $GitExe -ArgumentList $Arguments `
        -TimeoutSeconds 120 -FailureCode "git_failed"
}

function Get-ImmutableBlobSha256 {
    param(
        [Parameter(Mandatory)][ValidatePattern('^[0-9a-f]{40}$')][string]$Commit,
        [Parameter(Mandatory)][ValidatePattern('^[A-Za-z0-9._/-]+$')][string]$Path
    )
    $start = [Diagnostics.ProcessStartInfo]::new()
    $start.FileName = $GitExe
    $start.Arguments = "cat-file blob " + (ConvertTo-SafeArgument -Value ("$Commit`:$Path"))
    $start.WorkingDirectory = $WorktreeRoot
    $start.UseShellExecute = $false
    $start.CreateNoWindow = $true
    $start.RedirectStandardOutput = $true
    $start.RedirectStandardError = $true
    $process = [Diagnostics.Process]::new()
    $process.StartInfo = $start
    $bytes = $null
    try {
        if (-not $process.Start()) { throw "immutable blob launch failed" }
        $buffer = New-Object IO.MemoryStream
        try {
            $process.StandardOutput.BaseStream.CopyTo($buffer)
            if (-not $process.WaitForExit(120000)) {
                Stop-NativeTree -Process $process
                throw "immutable blob timed out"
            }
            $stderr = $process.StandardError.ReadToEnd()
            if ($process.ExitCode -ne 0 -or $stderr.Length -gt 8192 -or
                $buffer.Length -gt 16777216) {
                throw "immutable blob read failed"
            }
            $bytes = $buffer.ToArray()
        } finally {
            $buffer.Dispose()
        }
    } finally {
        $process.Dispose()
    }
    $hash = [Security.Cryptography.SHA256]::Create()
    try {
        return ([BitConverter]::ToString($hash.ComputeHash($bytes))).Replace("-", "").ToUpperInvariant()
    } finally {
        $hash.Dispose()
    }
}

$immutableRootSha = Get-ImmutableBlobSha256 -Commit $BaseCommit -Path "PLAN.md"
$immutableContractSha = Get-ImmutableBlobSha256 -Commit $BaseCommit -Path "docs/engineering/DETAILED_PLAN_AUTHORING_CONTRACT.md"
$immutableDetailedSha = Get-ImmutableBlobSha256 -Commit $BaseCommit -Path "docs/superpowers/plans/2026-07-23-windows-oci-distribution.md"
if ($immutableRootSha -cne $RootPlanSha -or
    $immutableContractSha -cne "B93F949DE36CD89C7101160F237D4FEBCD7305F411C55B20429D62A282DBBFEF" -or
    $immutableDetailedSha -cne $DetailedPlanSha.ToUpperInvariant()) {
    throw "immutable plan hash binding invalid"
}

function Assert-ExactStagedPaths {
    param([Parameter(Mandatory)][string[]]$ExpectedPaths)
    $result = Invoke-CheckedGit -Arguments @("diff", "--cached", "--name-only")
    $actual = @($result.Stdout -split "\r?\n" | Where-Object { $_ } |
        ForEach-Object { $_ -replace '\\', '/' } | Sort-Object)
    $expected = @($ExpectedPaths | ForEach-Object { $_ -replace '\\', '/' } | Sort-Object)
    if (($actual | Sort-Object -Unique).Count -ne $actual.Count -or
        $actual.Count -ne $expected.Count -or
        @(Compare-Object -ReferenceObject $expected -DifferenceObject $actual).Count -ne 0) {
        throw "whole-index staged path mismatch"
    }
}

function Assert-UnitStart {
    param([Parameter(Mandatory)][string]$ExpectedUnit)
    if ($UnitId -ne $ExpectedUnit) { throw "unit identity mismatch" }
    $top = (Invoke-CheckedGit -Arguments @("rev-parse", "--show-toplevel")).Stdout.Trim()
    if ((Resolve-Path -LiteralPath $top).Path -ne $WorktreeRoot) {
        throw "git top-level does not match worktree"
    }
    $head = (Invoke-CheckedGit -Arguments @("rev-parse", "HEAD")).Stdout.Trim()
    if ($head -ne $BaseCommit) { throw "HEAD does not equal reviewed base" }
    $gitDir = (Invoke-CheckedGit -Arguments @("rev-parse", "--git-dir")).Stdout.Trim()
    $commonDir = (Invoke-CheckedGit -Arguments @("rev-parse", "--git-common-dir")).Stdout.Trim()
    if ([IO.Path]::GetFullPath((Join-Path $WorktreeRoot $gitDir)) -eq
        [IO.Path]::GetFullPath((Join-Path $WorktreeRoot $commonDir))) {
        throw "distribution unit is not in an isolated worktree"
    }
    $branch = (Invoke-CheckedGit -Arguments @("symbolic-ref", "--short", "HEAD")).Stdout.Trim()
    if ($branch -notmatch '^codex/') { throw "distribution branch name invalid" }
    $status = (Invoke-CheckedGit -Arguments @(
        "status", "--porcelain=v1", "--untracked-files=all"
    )).Stdout.Trim()
    if ($status) { throw "distribution worktree is not clean at unit start" }
}

function Set-PrivateAcl {
    param([Parameter(Mandatory)][string]$Path)
    $acl = Get-Acl -LiteralPath $Path
    $acl.SetAccessRuleProtection($true, $false)
    $identity = [Security.Principal.WindowsIdentity]::GetCurrent().Name
    $rule = [Security.AccessControl.FileSystemAccessRule]::new(
        $identity, "FullControl", "ContainerInherit,ObjectInherit", "None", "Allow"
    )
    $acl.SetAccessRule($rule)
    Set-Acl -LiteralPath $Path -AclObject $acl
}

function Get-ReviewPacket {
    param([Parameter(Mandatory)][string[]]$ExpectedPaths)
    Invoke-CheckedGit -Arguments (@("add", "--") + $ExpectedPaths) | Out-Null
    Assert-ExactStagedPaths -ExpectedPaths $ExpectedPaths
    Invoke-CheckedGit -Arguments @("diff", "--cached", "--check") | Out-Null
    Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
        "scripts/scan_secrets.py", "--staged", "--git-exe", $GitExe
    ) -TimeoutSeconds 300 -FailureCode "staged_scanner_failed" | Out-Null
    $tree = (Invoke-CheckedGit -Arguments @("write-tree")).Stdout.Trim()
    if ($tree -notmatch '^[0-9a-f]{40}$') { throw "review tree id invalid" }
    $reviewRoot = Join-Path $env:TEMP (
        "projectb-review-$UnitId-" + [guid]::NewGuid().ToString('N')
    )
    [IO.Directory]::CreateDirectory($reviewRoot) | Out-Null
    Set-PrivateAcl -Path $reviewRoot
    $packetPath = Join-Path $reviewRoot "staged.diff"
    $start = [Diagnostics.ProcessStartInfo]::new()
    $start.FileName = $GitExe
    $start.Arguments = "diff --cached --binary --full-index"
    $start.WorkingDirectory = $WorktreeRoot
    $start.UseShellExecute = $false
    $start.CreateNoWindow = $true
    $start.RedirectStandardOutput = $true
    $start.RedirectStandardError = $true
    $process = [Diagnostics.Process]::new()
    $process.StartInfo = $start
    try {
        if (-not $process.Start()) { throw "private review packet launch failed" }
        $stdoutTask = $process.StandardOutput.ReadToEndAsync()
        $stderrTask = $process.StandardError.ReadToEndAsync()
        if (-not $process.WaitForExit(120000)) {
            Stop-NativeTree -Process $process
            throw "private review packet timed out"
        }
        $raw = $stdoutTask.GetAwaiter().GetResult()
        $null = $stderrTask.GetAwaiter().GetResult()
        if ($process.ExitCode -ne 0 -or [string]::IsNullOrWhiteSpace($raw) -or
            $raw.Length -gt 4194304) {
            throw "private review packet invalid"
        }
    } finally {
        $process.Dispose()
    }
    [IO.File]::WriteAllText($packetPath, $raw, [Text.UTF8Encoding]::new($false))
    $digest = (Get-FileHash -LiteralPath $packetPath -Algorithm SHA256).Hash.ToLowerInvariant()
    return [pscustomobject]@{ Path=$packetPath; TreeId=$tree; PacketSha256=$digest }
}

function Read-ReviewReceipt {
    param(
        [Parameter(Mandatory)][string]$Path,
        [Parameter(Mandatory)][string]$Role,
        [Parameter(Mandatory)][object]$Packet
    )
    if (-not [IO.Path]::IsPathFullyQualified($Path) -or
        -not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        throw "$Role review receipt missing"
    }
    $raw = [IO.File]::ReadAllText($Path)
    if ($raw.Length -gt 1048576) { throw "$Role review receipt too large" }
    $receipt = $raw | ConvertFrom-Json
    if ($receipt.result -ne "PASS" -or
        $receipt.unit_id -ne $UnitId -or
        $receipt.worker_id -ne $env:PROJECTB_AGENT_ID -or
        $receipt.human_modifications -ne $HumanModifications -or
        $receipt.root_plan_sha256 -ne $RootPlanSha -or
        $receipt.detailed_plan_sha256 -ne $DetailedPlanSha -or
        $receipt.tree_id -ne $Packet.TreeId -or
        $receipt.packet_sha256 -ne $Packet.PacketSha256 -or
        $receipt.reviewer_id -notmatch '^[A-Za-z0-9][A-Za-z0-9._-]{1,63}$' -or
        $receipt.reviewer_id -eq $env:PROJECTB_AGENT_ID) {
        throw "$Role review receipt binding invalid"
    }
    return $receipt
}

function Complete-ReviewedUnit {
    param(
        [Parameter(Mandatory)][string[]]$ExpectedPaths,
        [Parameter(Mandatory)][object]$Packet,
        [Parameter(Mandatory)][string]$CommitMessage
    )
    $spec = Read-ReviewReceipt -Path $env:PROJECTB_SPEC_REVIEW_RECEIPT `
        -Role "SPEC" -Packet $Packet
    $quality = Read-ReviewReceipt -Path $env:PROJECTB_QUALITY_REVIEW_RECEIPT `
        -Role "quality" -Packet $Packet
    if ($spec.reviewer_id -eq $quality.reviewer_id) {
        throw "distribution reviewers are not distinct"
    }
    Assert-ExactStagedPaths -ExpectedPaths $ExpectedPaths
    Invoke-CheckedGit -Arguments @("diff", "--cached", "--check") | Out-Null
    Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
        "scripts/scan_secrets.py", "--staged", "--git-exe", $GitExe
    ) -TimeoutSeconds 300 -FailureCode "staged_scanner_failed" | Out-Null
    $currentTree = (Invoke-CheckedGit -Arguments @("write-tree")).Stdout.Trim()
    if ($currentTree -ne $Packet.TreeId) { throw "reviewed tree changed" }
    $commitSubject = "$CommitMessage [agent=$($env:PROJECTB_AGENT_ID) human=$HumanModifications]"
    if ($commitSubject.Length -gt 500 -or $commitSubject -match "[\r\n]") {
        throw "distribution commit metadata invalid"
    }
    Invoke-CheckedGit -Arguments @("commit", "-m", $commitSubject) | Out-Null
    $head = (Invoke-CheckedGit -Arguments @("rev-parse", "HEAD")).Stdout.Trim()
    $headTree = (Invoke-CheckedGit -Arguments @("rev-parse", "HEAD^{tree}")).Stdout.Trim()
    if ($head -notmatch '^[0-9a-f]{40}$' -or $headTree -ne $Packet.TreeId) {
        throw "committed tree differs from reviewed tree"
    }
    return $head
}
```

Every review receipt is produced by a fresh session and contains `result`, `unit_id`, `worker_id`, `human_modifications`, `root_plan_sha256`, `detailed_plan_sha256`, `tree_id`, `packet_sha256`, `reviewer_id`, and findings. The commit helper appends the validated worker agent ID and human-modification declaration to the commit subject; a human edit after packet capture invalidates both receipts and requires a new scan, packet, tree, and reviews. Reviewers never edit worker files.

## Task DIST-01: Windows x64 Single-File Distribution

**Goal:** Build and prove one versioned `ProjectB.exe` that serves the reviewed local WebUI on loopback, writes only to an external data root, and runs on a clean Windows x64 host without Python, Node, or Docker.

**Dependencies / parallelism:** Requires reviewed QA-01C2, QA-02C, API-04B, API-REG-01, production frontend, and G-02A commits. It runs alone with respect to dependency locks, application startup, frontend build/base path, and packaging. DIST-02 waits for its reviewed commit.

**Files:**
- Create: `packaging/windows/build.ps1`
- Create: `packaging/windows/freezer-manifest.json`
- Create: `packaging/windows/smoke_test.ps1`
- Create: `backend/tests/integration/test_windows_distribution_contract.py`
- Create: `docs/engineering/DIST-01_EVIDENCE.md`

**Expected first failure:** the contract test fails because all five owned paths are absent; an interpreter, import, dependency, or permission failure is invalid red evidence.

- [ ] **Step W1: Execute the prelude and verify the exact predecessor chain**

Run the complete prelude, then:

```powershell
Assert-UnitStart -ExpectedUnit "DIST-01"
$requiredPredecessors = @(
    $env:PROJECTB_QA01C2_COMMIT
    $env:PROJECTB_QA02C_COMMIT
    $env:PROJECTB_API04B_COMMIT
    $env:PROJECTB_APIREG01_COMMIT
    $env:PROJECTB_G02A_COMMIT
)
foreach ($predecessor in $requiredPredecessors) {
    if ($predecessor -notmatch '^[0-9a-f]{40}$') {
        throw "DIST-01 predecessor hash missing"
    }
    $check = Invoke-BoundedNative -FilePath $GitExe -ArgumentList @(
        "merge-base", "--is-ancestor", $predecessor, $BaseCommit
    ) -TimeoutSeconds 120
    if ($check.ExitCode -ne 0) { throw "DIST-01 predecessor not integrated" }
}
if ($env:PROJECTB_SMOKE_DATA_ROOT -and
    (-not [IO.Path]::IsPathFullyQualified($env:PROJECTB_SMOKE_DATA_ROOT))) {
    throw "DIST-01 smoke data root must be absolute"
}
```

Expected: every hash is a reviewed ancestor and the owned worktree is completely clean. A missing predecessor blocks this unit; the worker does not infer a hash from a filename or ledger text.

- [ ] **Step W2: Write the complete failing Windows contract test**

Create `backend/tests/integration/test_windows_distribution_contract.py` with exactly:

```python
from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

import pytest


ROOT = Path(__file__).resolve().parents[3]
MANIFEST_PATH = ROOT / "packaging/windows/freezer-manifest.json"
BUILD_PATH = ROOT / "packaging/windows/build.ps1"
SMOKE_PATH = ROOT / "packaging/windows/smoke_test.ps1"
EVIDENCE_PATH = ROOT / "docs/engineering/DIST-01_EVIDENCE.md"


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def load_evidence(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    matches = re.findall(r"```json\n(.*?)\n```", text, flags=re.DOTALL)
    assert len(matches) == 1
    payload = json.loads(matches[0])
    assert isinstance(payload, dict)
    return payload


def test_manifest_locks_one_file_windows_x64_contract() -> None:
    manifest = load_json(MANIFEST_PATH)
    assert manifest == {
        "schemaVersion": 1,
        "application": {
            "name": "ProjectB",
            "version": "0.1.0",
            "artifact": "ProjectB.exe",
            "architecture": "windows-x64",
            "oneFile": True,
            "console": False,
        },
        "runtime": {
            "python": "3.14.6",
            "freezer": "PyInstaller==6.21.0",
            "bindHost": "127.0.0.1",
            "defaultDataRoot": "%LOCALAPPDATA%\\ProjectB",
            "frontendResourceRoot": "projectb_static",
        },
        "inputs": {
            "pythonLock": "backend/requirements-windows-x64.lock",
            "pythonLockSha256": (
                "246083f8b210c3e33904f3057dfd48e7d8db548804d11fa5b087ecb291ad0fc6"
            ),
            "frontendLock": "frontend/package-lock.json",
            "frontendLockSha256": (
                "071826d575cbcc472020a7df984e2e8f2410a75c1782550c5ddfeed268af3c2f"
            ),
        },
        "freezer": {
            "hiddenImports": ["keyring.backends.Windows"],
            "collectData": ["keyring", "pypdfium2"],
            "collectBinaries": ["pypdfium2"],
            "excludedModules": [
                "projectb.infrastructure.providers.mock",
                "pytest",
                "mypy",
                "ruff",
            ],
        },
        "evidence": {
            "dependencyBaseline": "docs/engineering/DEPENDENCY_BASELINE.md",
            "distributionBaseline": "docs/engineering/DISTRIBUTION_EVIDENCE.md",
            "pyinstallerLicense": (
                "GPL-2.0-or-later WITH Bootloader-exception"
            ),
        },
    }


@pytest.mark.parametrize(
    "required",
    [
        "--onefile",
        "--noupx",
        "--noconfirm",
        "--clean",
        "projectb_static",
        "keyring.backends.Windows",
        "pypdfium2",
        "frontend/package-lock.json",
        "backend/requirements-windows-x64.lock",
        "PROJECTB_BASE_COMMIT",
        "ProjectB.exe",
    ],
)
def test_build_script_contains_locked_inputs_and_output_checks(required: str) -> None:
    assert required in BUILD_PATH.read_text(encoding="utf-8")


def test_build_script_excludes_private_and_development_content() -> None:
    text = BUILD_PATH.read_text(encoding="utf-8")
    assert "--exclude-module" in text
    assert "projectb.infrastructure.providers.mock" in text
    assert "Get-ChildItem" in text
    assert "dist_artifact_invalid" in text
    assert ".env" not in text
    assert "courseware" not in text.lower()


@pytest.mark.parametrize(
    "required",
    [
        "EnvironmentKind",
        "CleanWindowsX64",
        "Get-AuthenticodeSignature",
        "SmartScreenObservation",
        "/api/health",
        "/api/settings/credentials/smoke-unconfigured/status",
        "projectb.sqlite3",
        "Get-NetTCPConnection",
        "shutdown.request",
        "dist_shutdown_timeout",
        "DIST-01_EVIDENCE.md",
    ],
)
def test_smoke_script_covers_clean_host_and_runtime_boundaries(required: str) -> None:
    assert required in SMOKE_PATH.read_text(encoding="utf-8")


def test_scripts_never_accept_a_secret_argument_or_echo_child_output() -> None:
    combined = BUILD_PATH.read_text(encoding="utf-8") + SMOKE_PATH.read_text(
        encoding="utf-8"
    )
    forbidden_parameters = ["ApiKey", "Token", "Password", "Secret", "CredentialValue"]
    for parameter in forbidden_parameters:
        assert re.search(rf"\[.*?\]\s*\${parameter}\b", combined) is None
    assert "throw $stderr" not in combined
    assert "throw $stdout" not in combined
    assert "Write-Host $stderr" not in combined
    assert "Write-Host $stdout" not in combined


def test_initial_evidence_is_truthful_and_schema_bound() -> None:
    evidence = load_evidence(EVIDENCE_PATH)
    assert evidence["schemaVersion"] == 1
    assert evidence["unitId"] == "DIST-01"
    assert evidence["status"] == "not_executed"
    assert evidence["artifact"]["status"] == "not_executed"
    assert evidence["buildHostSmoke"]["status"] == "not_executed"
    assert evidence["cleanWindowsSmoke"]["status"] == "not_executed"
    assert evidence["publication"]["status"] == "not_executed"
    assert "credential" not in json.dumps(evidence).lower()


def test_supplied_artifact_is_one_amd64_pe_file() -> None:
    supplied = os.environ.get("PROJECTB_DIST01_ARTIFACT")
    if supplied is None:
        return
    artifact = Path(supplied)
    assert artifact.is_file()
    assert artifact.name == "ProjectB.exe"
    data = artifact.read_bytes()
    assert data[:2] == b"MZ"
    pe_offset = int.from_bytes(data[0x3C:0x40], "little")
    assert data[pe_offset : pe_offset + 4] == b"PE\x00\x00"
    machine = int.from_bytes(data[pe_offset + 4 : pe_offset + 6], "little")
    assert machine == 0x8664
```

- [ ] **Step W3: Run the focused red test and preserve the named absence**

```powershell
$red = Invoke-BoundedNative -FilePath $PythonExe -ArgumentList @(
    "-m", "pytest", "backend/tests/integration/test_windows_distribution_contract.py", "-q"
) -TimeoutSeconds 180
if ($red.ExitCode -eq 0) { throw "DIST-01 red unexpectedly passed" }
if (($red.Stdout + $red.Stderr) -notmatch 'freezer-manifest|build.ps1|smoke_test|DIST-01_EVIDENCE') {
    throw "DIST-01 red failed for the wrong reason"
}
```

Expected: nonzero because an owned distribution file is missing. Preserve the sanitized exit/result summary; do not create a dummy PE file.

- [ ] **Step W4: Write the frozen freezer manifest**

Create `packaging/windows/freezer-manifest.json` with exactly:

```json
{
  "schemaVersion": 1,
  "application": {
    "name": "ProjectB",
    "version": "0.1.0",
    "artifact": "ProjectB.exe",
    "architecture": "windows-x64",
    "oneFile": true,
    "console": false
  },
  "runtime": {
    "python": "3.14.6",
    "freezer": "PyInstaller==6.21.0",
    "bindHost": "127.0.0.1",
    "defaultDataRoot": "%LOCALAPPDATA%\\ProjectB",
    "frontendResourceRoot": "projectb_static"
  },
  "inputs": {
    "pythonLock": "backend/requirements-windows-x64.lock",
    "pythonLockSha256": "246083f8b210c3e33904f3057dfd48e7d8db548804d11fa5b087ecb291ad0fc6",
    "frontendLock": "frontend/package-lock.json",
    "frontendLockSha256": "071826d575cbcc472020a7df984e2e8f2410a75c1782550c5ddfeed268af3c2f"
  },
  "freezer": {
    "hiddenImports": [
      "keyring.backends.Windows"
    ],
    "collectData": [
      "keyring",
      "pypdfium2"
    ],
    "collectBinaries": [
      "pypdfium2"
    ],
    "excludedModules": [
      "projectb.infrastructure.providers.mock",
      "pytest",
      "mypy",
      "ruff"
    ]
  },
  "evidence": {
    "dependencyBaseline": "docs/engineering/DEPENDENCY_BASELINE.md",
    "distributionBaseline": "docs/engineering/DISTRIBUTION_EVIDENCE.md",
    "pyinstallerLicense": "GPL-2.0-or-later WITH Bootloader-exception"
  }
}
```

- [ ] **Step W5: Write the complete bounded Windows build script**

Create `packaging/windows/build.ps1` with exactly:

```powershell
[CmdletBinding()]
param(
    [switch]$Clean,
    [ValidateNotNullOrEmpty()][string]$OutputDirectory = "dist"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Stop-Build {
    param([Parameter(Mandatory)][string]$Code)
    throw $Code
}

function ConvertTo-Argument {
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

function Stop-ProcessTree {
    param([Parameter(Mandatory)][Diagnostics.Process]$Process)
    $children = @(Get-CimInstance Win32_Process -Filter "ParentProcessId=$($Process.Id)" `
        -ErrorAction SilentlyContinue)
    foreach ($child in $children) {
        Stop-Process -Id ([int]$child.ProcessId) -Force -ErrorAction SilentlyContinue
    }
    Stop-Process -Id $Process.Id -Force -ErrorAction SilentlyContinue
}

function Assert-ChildPath {
    param(
        [Parameter(Mandatory)][string]$Parent,
        [Parameter(Mandatory)][string]$Candidate
    )
    $parentFull = (Resolve-Path -LiteralPath $Parent -ErrorAction Stop).Path.TrimEnd('\') + '\'
    $candidateFull = [IO.Path]::GetFullPath($Candidate)
    if (-not $candidateFull.StartsWith($parentFull, [StringComparison]::OrdinalIgnoreCase)) {
        Stop-Smoke "dist_invalid_argument"
    }
    $current = [IO.Path]::GetPathRoot($parentFull)
    foreach ($part in $parentFull.Substring($current.Length).Split(
        @('\', '/'), [StringSplitOptions]::RemoveEmptyEntries
    )) {
        $current = Join-Path $current $part
        $item = Get-Item -LiteralPath $current -Force -ErrorAction Stop
        if (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
            Stop-Smoke "dist_invalid_argument"
        }
    }
    return $candidateFull
}

function Stop-ProcessTree {
    param([Parameter(Mandatory)][Diagnostics.Process]$Process)
    $children = @(Get-CimInstance Win32_Process -Filter "ParentProcessId=$($Process.Id)" `
        -ErrorAction SilentlyContinue)
    foreach ($child in $children) {
        Stop-Process -Id ([int]$child.ProcessId) -Force -ErrorAction SilentlyContinue
    }
    Stop-Process -Id $Process.Id -Force -ErrorAction SilentlyContinue
}

function Invoke-Tool {
    param(
        [Parameter(Mandatory)][string]$FilePath,
        [Parameter(Mandatory)][AllowEmptyCollection()][string[]]$Arguments,
        [ValidateRange(1,3600)][int]$TimeoutSeconds,
        [Parameter(Mandatory)][string]$FailureCode
    )
    if (-not [IO.Path]::IsPathFullyQualified($FilePath) -or
        -not (Test-Path -LiteralPath $FilePath -PathType Leaf)) {
        Stop-Build "dist_invalid_argument"
    }
    $start = [Diagnostics.ProcessStartInfo]::new()
    $start.FileName = $FilePath
    $start.Arguments = (($Arguments | ForEach-Object {
        ConvertTo-Argument -Value ([string]$_)
    }) -join ' ')
    $start.UseShellExecute = $false
    $start.CreateNoWindow = $true
    $start.RedirectStandardOutput = $true
    $start.RedirectStandardError = $true
    $process = [Diagnostics.Process]::new()
    $process.StartInfo = $start
    try {
        if (-not $process.Start()) { Stop-Build $FailureCode }
        $stdoutTask = $process.StandardOutput.ReadToEndAsync()
        $stderrTask = $process.StandardError.ReadToEndAsync()
        if (-not $process.WaitForExit($TimeoutSeconds * 1000)) {
            Stop-ProcessTree -Process $process
            Stop-Build $FailureCode
        }
        $null = $stdoutTask.GetAwaiter().GetResult()
        $null = $stderrTask.GetAwaiter().GetResult()
        if ($process.ExitCode -ne 0) { Stop-Build $FailureCode }
    } finally {
        $process.Dispose()
    }
}

function Get-CanonicalTextHash {
    param([Parameter(Mandatory)][string]$Path)
    $text = [IO.File]::ReadAllText($Path, [Text.UTF8Encoding]::new($false, $true))
    $canonical = $text.Replace("`r`n", "`n").Replace("`r", "`n")
    $bytes = [Text.Encoding]::UTF8.GetBytes($canonical)
    $hash = [Security.Cryptography.SHA256]::Create()
    try {
        return ([BitConverter]::ToString($hash.ComputeHash($bytes))).Replace("-", "").ToLowerInvariant()
    } finally {
        $hash.Dispose()
    }
}

function Assert-ChildPath {
    param(
        [Parameter(Mandatory)][string]$Parent,
        [Parameter(Mandatory)][string]$Candidate
    )
    $parentFull = [IO.Path]::GetFullPath($Parent).TrimEnd('\') + '\'
    $candidateFull = [IO.Path]::GetFullPath($Candidate)
    if (-not $candidateFull.StartsWith($parentFull, [StringComparison]::OrdinalIgnoreCase)) {
        Stop-Build "dist_invalid_argument"
    }
    $current = [IO.Path]::GetPathRoot($parentFull)
    foreach ($part in $parentFull.Substring($current.Length).Split(
        @('\', '/'), [StringSplitOptions]::RemoveEmptyEntries
    )) {
        $current = Join-Path $current $part
        $item = Get-Item -LiteralPath $current -Force -ErrorAction Stop
        if (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
            Stop-Build "dist_invalid_argument"
        }
    }
    return $candidateFull
}

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = (Resolve-Path -LiteralPath (Join-Path $scriptRoot "../..")).Path
Set-Location -LiteralPath $projectRoot
$manifestPath = Join-Path $projectRoot "packaging/windows/freezer-manifest.json"
$manifest = Get-Content -Raw -LiteralPath $manifestPath -Encoding UTF8 | ConvertFrom-Json
if ($manifest.schemaVersion -ne 1 -or $manifest.application.artifact -ne "ProjectB.exe" -or
    $manifest.application.architecture -ne "windows-x64" -or
    $manifest.runtime.freezer -ne "PyInstaller==6.21.0") {
    Stop-Build "dist_input_drift"
}

$pythonExe = $env:PROJECTB_PYTHON_EXE
$npmCmd = $env:PROJECTB_NPM_CMD
foreach ($tool in @($pythonExe, $npmCmd)) {
    if ([string]::IsNullOrWhiteSpace($tool) -or
        -not [IO.Path]::IsPathFullyQualified($tool) -or
        -not (Test-Path -LiteralPath $tool -PathType Leaf)) {
        Stop-Build "dist_invalid_argument"
    }
}
$sourceCommit = $env:PROJECTB_BASE_COMMIT
if ($sourceCommit -notmatch '^[0-9a-f]{40}$') { Stop-Build "dist_invalid_argument" }

$pythonLock = Join-Path $projectRoot ([string]$manifest.inputs.pythonLock)
$frontendLock = Join-Path $projectRoot ([string]$manifest.inputs.frontendLock)
if ((Get-CanonicalTextHash -Path $pythonLock) -ne $manifest.inputs.pythonLockSha256 -or
    (Get-CanonicalTextHash -Path $frontendLock) -ne $manifest.inputs.frontendLockSha256) {
    Stop-Build "dist_input_drift"
}

$outputRoot = if ([IO.Path]::IsPathFullyQualified($OutputDirectory)) {
    Assert-ChildPath -Parent $projectRoot -Candidate $OutputDirectory
} else {
    Assert-ChildPath -Parent $projectRoot -Candidate (Join-Path $projectRoot $OutputDirectory)
}
if ($outputRoot -eq $projectRoot) { Stop-Build "dist_invalid_argument" }
if (Test-Path -LiteralPath $outputRoot) {
    $outputItem = Get-Item -LiteralPath $outputRoot -Force
    if (($outputItem.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
        Stop-Build "dist_invalid_argument"
    }
}
if ($Clean -and (Test-Path -LiteralPath $outputRoot)) {
    $verifiedOutput = Assert-ChildPath -Parent $projectRoot -Candidate $outputRoot
    Remove-Item -LiteralPath $verifiedOutput -Recurse -Force
}
[IO.Directory]::CreateDirectory($outputRoot) | Out-Null

Invoke-Tool -FilePath $npmCmd -Arguments @(
    "--prefix", "frontend", "ci", "--engine-strict", "--ignore-scripts"
) -TimeoutSeconds 1200 -FailureCode "dist_build_failed"
Invoke-Tool -FilePath $npmCmd -Arguments @(
    "--prefix", "frontend", "run", "build"
) -TimeoutSeconds 1200 -FailureCode "dist_build_failed"
$frontendDist = Join-Path $projectRoot "frontend/dist"
if (-not (Test-Path -LiteralPath (Join-Path $frontendDist "index.html") -PathType Leaf)) {
    Stop-Build "dist_build_failed"
}

Invoke-Tool -FilePath $pythonExe -Arguments @("-m", "PyInstaller", "--version") `
    -TimeoutSeconds 60 -FailureCode "dist_input_drift"
$versionResult = & $pythonExe -m PyInstaller --version 2>$null
$versionExit = $LASTEXITCODE
if ($versionExit -ne 0 -or @($versionResult).Count -ne 1 -or
    ([string]$versionResult).Trim() -ne "6.21.0") {
    Stop-Build "dist_input_drift"
}

$temporaryParent = [IO.Path]::GetFullPath([IO.Path]::GetTempPath()).TrimEnd('\')
$temporaryRoot = Join-Path $temporaryParent (
    "projectb-dist01-" + [guid]::NewGuid().ToString("N")
)
[void](Assert-ChildPath -Parent $temporaryParent -Candidate $temporaryRoot)
[IO.Directory]::CreateDirectory($temporaryRoot) | Out-Null
try {
    $launcherPath = Join-Path $temporaryRoot "projectb_windows_launcher.py"
    $launcher = @'
from __future__ import annotations

import argparse
import asyncio
import json
import os
import pathlib
import sys
import webbrowser

import uvicorn

from projectb.api.app import create_app


def absolute_path(value: str) -> pathlib.Path:
    candidate = pathlib.Path(value)
    if not candidate.is_absolute():
        raise argparse.ArgumentTypeError("absolute_path_required")
    return candidate.resolve(strict=False)


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="ProjectB.exe")
    parser.add_argument("--port", required=True, type=int, choices=range(1, 65536))
    parser.add_argument("--data-root", required=True, type=absolute_path)
    parser.add_argument("--ready-file", required=True, type=absolute_path)
    parser.add_argument("--shutdown-file", required=True, type=absolute_path)
    parser.add_argument("--no-browser", action="store_true")
    return parser.parse_args()


def within(parent: pathlib.Path, child: pathlib.Path) -> bool:
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False


def atomic_json(path: pathlib.Path, payload: dict[str, object]) -> None:
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(payload, sort_keys=True, separators=(",", ":")),
        encoding="utf-8",
    )
    temporary.replace(path)


async def run() -> int:
    parsed = arguments()
    data_root: pathlib.Path = parsed.data_root
    ready_file: pathlib.Path = parsed.ready_file
    shutdown_file: pathlib.Path = parsed.shutdown_file
    if not within(data_root, ready_file) or not within(data_root, shutdown_file):
        return 64
    data_root.mkdir(parents=True, exist_ok=True)
    ready_file.parent.mkdir(parents=True, exist_ok=True)
    shutdown_file.parent.mkdir(parents=True, exist_ok=True)
    ready_file.unlink(missing_ok=True)
    shutdown_file.unlink(missing_ok=True)
    static_root = pathlib.Path(getattr(sys, "_MEIPASS", pathlib.Path(__file__).parent))
    static_root = static_root / "projectb_static"
    if not (static_root / "index.html").is_file():
        return 70
    os.environ["PROJECTB_DATA_ROOT"] = str(data_root)
    os.environ["PROJECTB_STATIC_ROOT"] = str(static_root)
    os.environ["PROJECTB_PROFILE"] = "local"
    config = uvicorn.Config(
        create_app(profile="local"),
        host="127.0.0.1",
        port=parsed.port,
        access_log=False,
        log_level="warning",
    )
    server = uvicorn.Server(config)
    server.install_signal_handlers = lambda: None
    serve_task = asyncio.create_task(server.serve())
    for _ in range(600):
        if server.started or serve_task.done():
            break
        await asyncio.sleep(0.05)
    if not server.started or serve_task.done():
        server.should_exit = True
        await asyncio.gather(serve_task, return_exceptions=True)
        return 70
    atomic_json(
        ready_file,
        {
            "host": "127.0.0.1",
            "pid": os.getpid(),
            "port": parsed.port,
            "profile": "local",
            "schemaVersion": 1,
            "scheme": "http",
            "status": "ready",
        },
    )
    if not parsed.no_browser:
        webbrowser.open(f"http://127.0.0.1:{parsed.port}/", new=1, autoraise=True)
    while not shutdown_file.exists() and not serve_task.done():
        await asyncio.sleep(0.10)
    if shutdown_file.exists():
        server.should_exit = True
    try:
        await asyncio.wait_for(serve_task, timeout=10.0)
    except TimeoutError:
        return 71
    finally:
        ready_file.unlink(missing_ok=True)
        shutdown_file.unlink(missing_ok=True)
    return 0


def main() -> int:
    try:
        return asyncio.run(run())
    except (OSError, RuntimeError, ValueError):
        return 70


if __name__ == "__main__":
    raise SystemExit(main())
'@
    [IO.File]::WriteAllText(
        $launcherPath, $launcher.Replace("`r`n", "`n"), [Text.UTF8Encoding]::new($false)
    )

    $versionPath = Join-Path $temporaryRoot "version_info.txt"
    $versionInfo = @"
VSVersionInfo(
  ffi=FixedFileInfo(filevers=(0, 1, 0, 0), prodvers=(0, 1, 0, 0),
    mask=0x3f, flags=0x0, OS=0x40004, fileType=0x1, subtype=0x0, date=(0, 0)),
  kids=[StringFileInfo([StringTable('040904B0', [
    StringStruct('CompanyName', 'ProjectB student project'),
    StringStruct('FileDescription', 'ProjectB local learning WebUI'),
    StringStruct('FileVersion', '0.1.0'),
    StringStruct('InternalName', 'ProjectB'),
    StringStruct('OriginalFilename', 'ProjectB.exe'),
    StringStruct('ProductName', 'ProjectB'),
    StringStruct('ProductVersion', '0.1.0'),
    StringStruct('PrivateBuild', '$sourceCommit')
  ])]), VarFileInfo([VarStruct('Translation', [1033, 1200])])]
)
"@
    [IO.File]::WriteAllText(
        $versionPath, $versionInfo.Replace("`r`n", "`n"), [Text.UTF8Encoding]::new($false)
    )

    $arguments = @(
        "-m", "PyInstaller", "--noconfirm", "--clean", "--onefile", "--windowed",
        "--noupx", "--name", "ProjectB", "--distpath", $outputRoot,
        "--workpath", (Join-Path $temporaryRoot "work"),
        "--specpath", (Join-Path $temporaryRoot "spec"),
        "--paths", (Join-Path $projectRoot "backend/src"),
        "--add-data", "$frontendDist;projectb_static",
        "--version-file", $versionPath
    )
    foreach ($name in @($manifest.freezer.hiddenImports)) {
        $arguments += @("--hidden-import", [string]$name)
    }
    foreach ($name in @($manifest.freezer.collectData)) {
        $arguments += @("--collect-data", [string]$name)
    }
    foreach ($name in @($manifest.freezer.collectBinaries)) {
        $arguments += @("--collect-binaries", [string]$name)
    }
    foreach ($name in @($manifest.freezer.excludedModules)) {
        $arguments += @("--exclude-module", [string]$name)
    }
    $arguments += $launcherPath
    Invoke-Tool -FilePath $pythonExe -Arguments $arguments -TimeoutSeconds 1800 `
        -FailureCode "dist_build_failed"
} finally {
    if (Test-Path -LiteralPath $temporaryRoot) {
        $verifiedTemporaryRoot = Assert-ChildPath -Parent $temporaryParent -Candidate $temporaryRoot
        Remove-Item -LiteralPath $verifiedTemporaryRoot -Recurse -Force
    }
}

$files = @(Get-ChildItem -LiteralPath $outputRoot -File -Recurse -Force)
$artifact = Join-Path $outputRoot "ProjectB.exe"
if (-not (Test-Path -LiteralPath $artifact -PathType Leaf)) {
    Stop-Build "dist_artifact_invalid"
}
$artifactFull = (Resolve-Path -LiteralPath $artifact).Path
if ($files.Count -ne 1 -or $files[0].FullName -ne $artifactFull) {
    Stop-Build "dist_artifact_invalid"
}
$stream = [IO.File]::OpenRead($artifact)
try {
    $reader = [IO.BinaryReader]::new($stream)
    if ([Text.Encoding]::ASCII.GetString($reader.ReadBytes(2)) -ne "MZ") {
        Stop-Build "dist_artifact_invalid"
    }
    $stream.Position = 0x3c
    $peOffset = $reader.ReadInt32()
    $stream.Position = $peOffset
    if ([Text.Encoding]::ASCII.GetString($reader.ReadBytes(4)) -ne "PE`0`0" -or
        $reader.ReadUInt16() -ne 0x8664) {
        Stop-Build "dist_artifact_invalid"
    }
} finally {
    $stream.Dispose()
}
$summary = [ordered]@{
    schemaVersion = 1
    artifact = "ProjectB.exe"
    sha256 = (Get-FileHash -LiteralPath $artifact -Algorithm SHA256).Hash.ToLowerInvariant()
    sizeBytes = (Get-Item -LiteralPath $artifact).Length
    sourceCommit = $sourceCommit
}
$summary | ConvertTo-Json -Compress
```

The one direct `& $pythonExe -m PyInstaller --version` probe is immediately followed by a captured `$LASTEXITCODE`; all other native calls are individually bounded and checked. The output directory is resolved beneath the repository before recursive cleanup, and the temporary build root is a newly generated path.

- [ ] **Step W6: Write the complete clean-host smoke and evidence script**

Create `packaging/windows/smoke_test.ps1` with exactly:

```powershell
[CmdletBinding()]
param(
    [Parameter(Mandatory)][string]$ExePath,
    [Parameter(Mandatory)][string]$DataRoot,
    [ValidateSet("BuildHost", "CleanWindowsX64")][string]$EnvironmentKind = "BuildHost",
    [ValidateSet("NotObserved", "WarningObserved", "NoWarningObserved")]
    [string]$SmartScreenObservation = "NotObserved",
    [string]$EvidencePath,
    [Parameter(Mandatory)][ValidatePattern('^[0-9a-f]{40}$')]
    [string]$ExpectedSourceCommit,
    [ValidateRange(15,120)][int]$StartupTimeoutSeconds = 45
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Stop-Smoke {
    param([Parameter(Mandatory)][string]$Code)
    throw $Code
}

function Assert-ChildPath {
    param(
        [Parameter(Mandatory)][string]$Parent,
        [Parameter(Mandatory)][string]$Candidate
    )
    if (-not [IO.Path]::IsPathFullyQualified($Parent) -or
        -not (Test-Path -LiteralPath $Parent -PathType Container)) {
        Stop-Smoke "dist_invalid_argument"
    }
    $parentItem = Get-Item -LiteralPath $Parent -Force -ErrorAction Stop
    if (($parentItem.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
        Stop-Smoke "dist_invalid_argument"
    }
    $parentFull = [IO.Path]::GetFullPath($parentItem.FullName).TrimEnd('\') + '\'
    $candidateFull = [IO.Path]::GetFullPath($Candidate)
    if (-not $candidateFull.StartsWith($parentFull, [StringComparison]::OrdinalIgnoreCase)) {
        Stop-Smoke "dist_invalid_argument"
    }
    $current = [IO.Path]::GetPathRoot($parentFull)
    foreach ($part in $parentFull.Substring($current.Length).Split(
        @('\', '/'), [StringSplitOptions]::RemoveEmptyEntries
    )) {
        $current = Join-Path $current $part
        if (Test-Path -LiteralPath $current) {
            $item = Get-Item -LiteralPath $current -Force -ErrorAction Stop
            if (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
                Stop-Smoke "dist_invalid_argument"
            }
        }
    }
    return $candidateFull
}

function Stop-ProcessTree {
    param([Parameter(Mandatory)][Diagnostics.Process]$Process)
    $rootId = $Process.Id
    $descendants = New-Object 'System.Collections.Generic.List[int]'
    $queue = New-Object 'System.Collections.Generic.Queue[int]'
    $queue.Enqueue($rootId)
    while ($queue.Count -gt 0) {
        $parentId = $queue.Dequeue()
        foreach ($child in @(Get-CimInstance Win32_Process -Filter "ParentProcessId=$parentId" `
            -ErrorAction SilentlyContinue)) {
            $childId = [int]$child.ProcessId
            if (-not $descendants.Contains($childId)) {
                $descendants.Add($childId)
                $queue.Enqueue($childId)
            }
        }
    }
    foreach ($childId in @($descendants.ToArray() | Sort-Object -Descending)) {
        Stop-Process -Id $childId -Force -ErrorAction SilentlyContinue
    }
    Stop-Process -Id $rootId -Force -ErrorAction SilentlyContinue
    $deadline = [Diagnostics.Stopwatch]::StartNew()
    do {
        $alive = @(Get-Process -Id (@($rootId) + $descendants.ToArray()) `
            -ErrorAction SilentlyContinue)
        if ($alive.Count -gt 0) { Start-Sleep -Milliseconds 25 }
    } while ($alive.Count -gt 0 -and $deadline.ElapsedMilliseconds -lt 5000)
    if ($alive.Count -gt 0) { Stop-Smoke "dist_process_tree_cleanup_failed" }
}

function ConvertTo-Argument {
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

function Get-DirectorySnapshot {
    param([Parameter(Mandatory)][string]$Path)
    $rootItem = Get-Item -LiteralPath $Path -Force -ErrorAction Stop
    if (-not $rootItem.PSIsContainer -or
        ($rootItem.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
        Stop-Smoke "dist_residue_found"
    }
    $rootFull = [IO.Path]::GetFullPath($rootItem.FullName).TrimEnd('\')
    $result = [ordered]@{}
    $stack = New-Object 'System.Collections.Generic.Stack[System.IO.DirectoryInfo]'
    $stack.Push([IO.DirectoryInfo]$rootItem)
    while ($stack.Count -gt 0) {
        $directory = $stack.Pop()
        foreach ($item in @(Get-ChildItem -LiteralPath $directory.FullName -Force |
            Sort-Object FullName)) {
            if (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
                Stop-Smoke "dist_residue_found"
            }
            $relative = $item.FullName.Substring($rootFull.Length).TrimStart('\', '/')
            if ($item.PSIsContainer) {
                $stack.Push([IO.DirectoryInfo]$item)
                $result[$relative + '/'] = "directory"
            } else {
                $result[$relative] = (Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
            }
        }
    }
    return $result
}

function Test-SameSnapshot {
    param([Parameter(Mandatory)][object]$Before,[Parameter(Mandatory)][object]$After)
    $beforeJson = $Before | ConvertTo-Json -Compress
    $afterJson = $After | ConvertTo-Json -Compress
    return $beforeJson -ceq $afterJson
}

function Get-FreeLoopbackPort {
    $listener = [Net.Sockets.TcpListener]::new([Net.IPAddress]::Loopback, 0)
    try {
        $listener.Start()
        return ([Net.IPEndPoint]$listener.LocalEndpoint).Port
    } finally {
        $listener.Stop()
    }
}

function Get-ExistingEvidence {
    param([Parameter(Mandatory)][string]$Path)
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { return $null }
    $text = [IO.File]::ReadAllText($Path)
    $matches = [regex]::Matches($text, '(?ms)^```json\r?\n(?<json>.*?)\r?\n```\r?$')
    if ($matches.Count -ne 1) { return $null }
    try { return $matches[0].Groups['json'].Value | ConvertFrom-Json } catch { return $null }
}

function Write-Evidence {
    param([Parameter(Mandatory)][string]$Path,[Parameter(Mandatory)][object]$Payload)
    $json = $Payload | ConvertTo-Json -Depth 12
    $document = @(
        "# DIST-01 Evidence"
        ""
        '```json'
        $json
        '```'
        ""
    ) -join [Environment]::NewLine
    [IO.File]::WriteAllText($Path, $document, [Text.UTF8Encoding]::new($false))
}

function Assert-NoInstalledDeveloperRuntime {
    $present = New-Object Collections.Generic.List[string]
    foreach ($name in @("python.exe", "python3.exe", "py.exe", "node.exe", "docker.exe")) {
        $command = Get-Command $name -CommandType Application -ErrorAction SilentlyContinue |
            Select-Object -First 1
        if ($null -ne $command -and (Test-Path -LiteralPath $command.Source -PathType Leaf)) {
            $present.Add($name)
        }
    }
    if ($present.Count -ne 0) { Stop-Smoke "dist_evidence_invalid" }
    return [ordered]@{ pythonAbsent=$true; nodeAbsent=$true; dockerAbsent=$true }
}

function Assert-SafeJsonObject {
    param([Parameter(Mandatory)][object]$Value)
    $serialized = $Value | ConvertTo-Json -Compress -Depth 12
    if ($serialized -match '(?i)api[_-]?key|token|password|secret|course[_-]?body|local[_-]?path') {
        Stop-Smoke "dist_credential_status_failed"
    }
}

if (-not [IO.Path]::IsPathFullyQualified($ExePath) -or
    -not [IO.Path]::IsPathFullyQualified($DataRoot) -or
    -not (Test-Path -LiteralPath $ExePath -PathType Leaf) -or
    [IO.Path]::GetFileName($ExePath) -ne "ProjectB.exe") {
    Stop-Smoke "dist_invalid_argument"
}
$ExePath = (Resolve-Path -LiteralPath $ExePath).Path
$exeCurrent = [IO.Path]::GetPathRoot($ExePath)
foreach ($part in $ExePath.Substring($exeCurrent.Length).Split(
    @('\', '/'), [StringSplitOptions]::RemoveEmptyEntries
)) {
    $exeCurrent = Join-Path $exeCurrent $part
    $exeItem = Get-Item -LiteralPath $exeCurrent -Force -ErrorAction Stop
    if (($exeItem.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
        Stop-Smoke "dist_invalid_argument"
    }
}
$DataRoot = [IO.Path]::GetFullPath($DataRoot)
if (Test-Path -LiteralPath $DataRoot) { Stop-Smoke "dist_invalid_argument" }
$dataParent = Split-Path -Parent $DataRoot
if (-not (Test-Path -LiteralPath $dataParent -PathType Container)) {
    Stop-Smoke "dist_invalid_argument"
}
$dataParentItem = Get-Item -LiteralPath $dataParent -Force
if (($dataParentItem.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
    Stop-Smoke "dist_invalid_argument"
}
[void](Assert-ChildPath -Parent $dataParent -Candidate $DataRoot)
$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = (Resolve-Path -LiteralPath (Join-Path $scriptRoot "../..")).Path
if ([string]::IsNullOrWhiteSpace($EvidencePath)) {
    $EvidencePath = Join-Path $projectRoot "docs/engineering/DIST-01_EVIDENCE.md"
}
if (-not [IO.Path]::IsPathFullyQualified($EvidencePath)) {
    $EvidencePath = [IO.Path]::GetFullPath((Join-Path $projectRoot $EvidencePath))
}
if (Test-Path -LiteralPath $EvidencePath -PathType Leaf) {
    $evidenceItem = Get-Item -LiteralPath $EvidencePath -Force
    if (($evidenceItem.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
        Stop-Smoke "dist_evidence_invalid"
    }
}
if ($EnvironmentKind -eq "CleanWindowsX64" -and
    $SmartScreenObservation -eq "NotObserved") {
    Stop-Smoke "dist_evidence_invalid"
}

$runtimeAbsence = [ordered]@{
    pythonAbsent = $false
    nodeAbsent = $false
    dockerAbsent = $false
}
if ($EnvironmentKind -eq "CleanWindowsX64") {
    $runtimeAbsence = Assert-NoInstalledDeveloperRuntime
}

$startedAt = [DateTimeOffset]::UtcNow
$existingEvidence = Get-ExistingEvidence -Path $EvidencePath
$buildHostSmoke = [ordered]@{ status="not_executed"; resultCode="not_executed" }
$cleanWindowsSmoke = [ordered]@{ status="not_executed"; resultCode="not_executed" }
if ($null -ne $existingEvidence) {
    if ($null -ne $existingEvidence.buildHostSmoke) {
        $buildHostSmoke = $existingEvidence.buildHostSmoke
    }
    if ($null -ne $existingEvidence.cleanWindowsSmoke) {
        $cleanWindowsSmoke = $existingEvidence.cleanWindowsSmoke
    }
}

[IO.Directory]::CreateDirectory($DataRoot) | Out-Null
$controlRoot = Assert-ChildPath -Parent $DataRoot -Candidate (Join-Path $DataRoot "control")
[IO.Directory]::CreateDirectory($controlRoot) | Out-Null
$readyFile = Join-Path $controlRoot "ready.json"
$shutdownFile = Join-Path $controlRoot "shutdown.request"
$stdoutFile = Join-Path $controlRoot "stdout.txt"
$stderrFile = Join-Path $controlRoot "stderr.txt"
$port = Get-FreeLoopbackPort
$exeDirectory = Split-Path -Parent $ExePath
$beforeSnapshot = Get-DirectorySnapshot -Path $exeDirectory
$process = $null
$httpClient = $null
try {
    $start = [Diagnostics.ProcessStartInfo]::new()
    $start.FileName = $ExePath
    $start.Arguments = (@(
        "--port", [string]$port,
        "--data-root", $DataRoot,
        "--ready-file", $readyFile,
        "--shutdown-file", $shutdownFile,
        "--no-browser"
    ) | ForEach-Object { ConvertTo-Argument -Value ([string]$_) }) -join ' '
    $start.WorkingDirectory = $exeDirectory
    $start.UseShellExecute = $false
    $start.CreateNoWindow = $true
    $start.RedirectStandardOutput = $false
    $start.RedirectStandardError = $false
    foreach ($name in @($start.EnvironmentVariables.Keys)) {
        if ($name -match '(?i)(API.?KEY|TOKEN|PASSWORD|SECRET|CREDENTIAL)') {
            $start.EnvironmentVariables.Remove($name)
        }
    }
    $start.EnvironmentVariables["PROJECTB_PROFILE"] = "local"
    $start.EnvironmentVariables["PROJECTB_DATA_ROOT"] = $DataRoot
    $process = [Diagnostics.Process]::new()
    $process.StartInfo = $start
    if (-not $process.Start()) { Stop-Smoke "dist_start_failed" }

    $deadline = [Diagnostics.Stopwatch]::StartNew()
    while (-not (Test-Path -LiteralPath $readyFile -PathType Leaf) -and
        -not $process.HasExited -and
        $deadline.Elapsed.TotalSeconds -lt $StartupTimeoutSeconds) {
        Start-Sleep -Milliseconds 100
    }
    if (-not (Test-Path -LiteralPath $readyFile -PathType Leaf) -or $process.HasExited) {
        Stop-Smoke "dist_ready_timeout"
    }
    $ready = Get-Content -Raw -LiteralPath $readyFile -Encoding UTF8 | ConvertFrom-Json
    if ($ready.schemaVersion -ne 1 -or $ready.status -ne "ready" -or
        $ready.profile -ne "local" -or $ready.scheme -ne "http" -or
        $ready.host -ne "127.0.0.1" -or $ready.port -ne $port -or
        $ready.pid -isnot [int]) {
        Stop-Smoke "dist_ready_timeout"
    }
    if (-not [Environment]::Is64BitOperatingSystem) {
        Stop-Smoke "dist_architecture_failed"
    }
    Assert-SafeJsonObject -Value $ready

    $handler = [Net.Http.HttpClientHandler]::new()
    $handler.UseProxy = $false
    $httpClient = [Net.Http.HttpClient]::new($handler)
    $httpClient.Timeout = [TimeSpan]::FromSeconds(10)
    $healthRaw = $httpClient.GetStringAsync(
        "http://127.0.0.1:$port/api/health"
    ).GetAwaiter().GetResult()
    $health = $healthRaw | ConvertFrom-Json
    if ($health.status -ne "ok" -or $health.profile -ne "local" -or
        @($health.psobject.Properties).Count -ne 2) {
        Stop-Smoke "dist_health_failed"
    }
    Assert-SafeJsonObject -Value $health

    $credentialRaw = $httpClient.GetStringAsync(
        "http://127.0.0.1:$port/api/settings/credentials/smoke-unconfigured/status"
    ).GetAwaiter().GetResult()
    $credentialStatus = $credentialRaw | ConvertFrom-Json
    if ($credentialStatus.configured -ne $false) {
        Stop-Smoke "dist_credential_status_failed"
    }
    Assert-SafeJsonObject -Value $credentialStatus

    $databasePath = Join-Path $DataRoot "projectb.sqlite3"
    if (-not (Test-Path -LiteralPath $databasePath -PathType Leaf)) {
        Stop-Smoke "dist_sqlite_failed"
    }
    $databaseStream = [IO.File]::Open(
        $databasePath, [IO.FileMode]::Open, [IO.FileAccess]::Read,
        [IO.FileShare]::ReadWrite -bor [IO.FileShare]::Delete
    )
    try {
        $header = New-Object byte[] 16
        if ($databaseStream.Read($header, 0, 16) -ne 16 -or
            [Text.Encoding]::ASCII.GetString($header) -ne "SQLite format 3`0") {
            Stop-Smoke "dist_sqlite_failed"
        }
    } finally {
        $databaseStream.Dispose()
    }

    $listeners = @(Get-NetTCPConnection -State Listen -OwningProcess ([int]$ready.pid) `
        -ErrorAction Stop)
    if ($listeners.Count -ne 1 -or $listeners[0].LocalPort -ne $port -or
        $listeners[0].LocalAddress -notin @("127.0.0.1", "::1")) {
        Stop-Smoke "dist_bind_violation"
    }

    [IO.File]::WriteAllText($shutdownFile, "shutdown`n", [Text.UTF8Encoding]::new($false))
    if (-not $process.WaitForExit(10000)) { Stop-Smoke "dist_shutdown_timeout" }
    if ($process.ExitCode -ne 0) { Stop-Smoke "dist_shutdown_timeout" }
    Start-Sleep -Milliseconds 250
    if (Get-Process -Id ([int]$ready.pid) -ErrorAction SilentlyContinue) {
        Stop-Smoke "dist_shutdown_timeout"
    }
    if (Test-Path -LiteralPath $readyFile -or Test-Path -LiteralPath $shutdownFile) {
        Stop-Smoke "dist_residue_found"
    }
    $afterSnapshot = Get-DirectorySnapshot -Path $exeDirectory
    if (-not (Test-SameSnapshot -Before $beforeSnapshot -After $afterSnapshot)) {
        Stop-Smoke "dist_residue_found"
    }
    $dataSnapshot = Get-DirectorySnapshot -Path $DataRoot
    $mutableFiles = @($dataSnapshot.Keys | Where-Object {
        $_ -notlike "control/*" -and $_ -notlike "control\\*" -and $_ -notlike "*/"
    })
    if ($mutableFiles.Count -ne 1 -or $mutableFiles[0] -ne "projectb.sqlite3") {
        Stop-Smoke "dist_residue_found"
    }

    $smokeRecord = [ordered]@{
        status = "pass"
        resultCode = "ok"
        environmentKind = $EnvironmentKind
        windowsX64 = [Environment]::Is64BitOperatingSystem
        runtimeAbsence = $runtimeAbsence
        smartScreenObservation = $SmartScreenObservation.ToLowerInvariant()
        listenerCount = $listeners.Count
        residueCount = $mutableFiles.Count
    }
    if ($EnvironmentKind -eq "BuildHost") { $buildHostSmoke = $smokeRecord }
    if ($EnvironmentKind -eq "CleanWindowsX64") { $cleanWindowsSmoke = $smokeRecord }
} finally {
    if ($null -ne $httpClient) { $httpClient.Dispose() }
    if ($null -ne $process) {
        Stop-ProcessTree -Process $process
        $process.Dispose()
    }
    foreach ($path in @($stdoutFile, $stderrFile, $readyFile, $shutdownFile)) {
        Remove-Item -LiteralPath $path -Force -ErrorAction SilentlyContinue
    }
    if (Test-Path -LiteralPath $controlRoot) {
        $verifiedControlRoot = Assert-ChildPath -Parent $DataRoot -Candidate $controlRoot
        Remove-Item -LiteralPath $verifiedControlRoot -Recurse -Force -ErrorAction SilentlyContinue
    }
}

$signature = Get-AuthenticodeSignature -LiteralPath $ExePath
$signatureState = switch ($signature.Status.ToString()) {
    "Valid" { "signed_valid" }
    "NotSigned" { "unsigned" }
    default { "invalid" }
}
$smartScreenState = switch ($SmartScreenObservation) {
    "WarningObserved" { "warning_observed" }
    "NoWarningObserved" { "no_warning_observed" }
    default { "not_observed" }
}
$overall = if ($buildHostSmoke.status -eq "pass" -and
    $cleanWindowsSmoke.status -eq "pass") { "pass" } else { "partial" }
$artifact = Get-Item -LiteralPath $ExePath
$payload = [ordered]@{
    schemaVersion = 1
    unitId = "DIST-01"
    status = $overall
    sourceCommit = $ExpectedSourceCommit
    buildInputs = [ordered]@{
        python = "3.14.6"
        node = "24.18.0"
        npm = "11.16.0"
        pyinstaller = "6.21.0"
        pythonLockSha256 = "246083f8b210c3e33904f3057dfd48e7d8db548804d11fa5b087ecb291ad0fc6"
        frontendLockSha256 = "071826d575cbcc472020a7df984e2e8f2410a75c1782550c5ddfeed268af3c2f"
    }
    artifact = [ordered]@{
        status = "pass"
        name = "ProjectB.exe"
        architecture = "windows-x64"
        sha256 = (Get-FileHash -LiteralPath $ExePath -Algorithm SHA256).Hash.ToLowerInvariant()
        sizeBytes = $artifact.Length
        signature = $signatureState
        smartScreen = $smartScreenState
    }
    buildHostSmoke = $buildHostSmoke
    cleanWindowsSmoke = $cleanWindowsSmoke
    commands = @(
        "windows-build-v1"
        "windows-smoke-build-host-v1"
        "windows-smoke-clean-host-v1"
    )
    timing = [ordered]@{
        startedAtUtc = $startedAt.ToString("o")
        finishedAtUtc = [DateTimeOffset]::UtcNow.ToString("o")
    }
    publication = [ordered]@{ status="not_executed" }
}
Write-Evidence -Path $EvidencePath -Payload $payload
if ($overall -ne "pass") { Stop-Smoke "dist_evidence_invalid" }
```

The clean host runs the exact same artifact produced on the build host. `SmartScreenObservation` is a factual operator observation; it never signs the artifact and never turns `NotSigned` into success text. The script refuses a pre-existing data root and cleans only the control directory it created.

- [ ] **Step W7: Write the truthful initial DIST-01 evidence record**

Create `docs/engineering/DIST-01_EVIDENCE.md` with exactly:

````markdown
# DIST-01 Evidence

```json
{
  "schemaVersion": 1,
  "unitId": "DIST-01",
  "status": "not_executed",
  "sourceCommit": "not_executed",
  "buildInputs": {
    "python": "3.14.6",
    "node": "24.18.0",
    "npm": "11.16.0",
    "pyinstaller": "6.21.0",
    "pythonLockSha256": "246083f8b210c3e33904f3057dfd48e7d8db548804d11fa5b087ecb291ad0fc6",
    "frontendLockSha256": "071826d575cbcc472020a7df984e2e8f2410a75c1782550c5ddfeed268af3c2f"
  },
  "artifact": {
    "status": "not_executed",
    "name": "ProjectB.exe",
    "architecture": "windows-x64",
    "sha256": "not_executed",
    "sizeBytes": 0,
    "signature": "not_executed",
    "smartScreen": "not_observed"
  },
  "buildHostSmoke": {
    "status": "not_executed",
    "resultCode": "not_executed"
  },
  "cleanWindowsSmoke": {
    "status": "not_executed",
    "resultCode": "not_executed"
  },
  "commands": [],
  "timing": {
    "startedAtUtc": "not_executed",
    "finishedAtUtc": "not_executed"
  },
  "publication": {
    "status": "not_executed"
  }
}
```
````

- [ ] **W8. Run the focused green test and keep the first passing transcript.**

```powershell
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "-m", "pytest",
    "backend/tests/integration/test_windows_distribution_contract.py", "-q"
) -TimeoutSeconds 300 -FailureCode "dist01_contract_green_failed" | Out-Null
```

The worker records only the command, UTC start/end, exit code, and redacted final status in `DIST-01_EVIDENCE.md`. Raw child output stays in the private worker transcript and is never copied into the repository. A green result before W2 has produced the required red result is invalid TDD evidence.

- [ ] **W9. Build the one-file artifact on the implementation worktree.**

```powershell
$buildResult = Invoke-CheckedNative -FilePath $PowerShellExe -ArgumentList @(
    "-NoLogo", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass",
    "-File", (Join-Path $WorktreeRoot "packaging/windows/build.ps1"),
    "-Clean",
    "-OutputDirectory", (Join-Path $WorktreeRoot "dist")
) -TimeoutSeconds 1800 -FailureCode "dist01_build_failed"
$artifactPath = Join-Path $WorktreeRoot "dist/ProjectB.exe"
if (-not (Test-Path -LiteralPath $artifactPath -PathType Leaf)) {
    throw "dist01 artifact missing"
}
```

Expected result: exactly one regular PE file named `ProjectB.exe`; no runtime directory, installer, archive, adjacent Python DLL, frontend folder, lock file, fixture, database, credential, or build transcript under `dist/`. `dist/` remains ignored and must never appear in the staged path set.

- [ ] **W10. Run the build-host smoke test with a fresh external data root.**

```powershell
$buildHostData = Join-Path $env:TEMP ("projectb-dist01-buildhost-" + [guid]::NewGuid().ToString("N"))
$buildHostTempRoot = [IO.Path]::GetFullPath($env:TEMP).TrimEnd('\')
if (-not [IO.Path]::GetFullPath($buildHostData).StartsWith(
    $buildHostTempRoot + '\', [StringComparison]::OrdinalIgnoreCase)) {
    throw "dist01_buildhost_data_containment_failed"
}
[IO.Directory]::CreateDirectory($buildHostData) | Out-Null
try {
    $buildHostResult = Invoke-CheckedNative -FilePath $PowerShellExe -ArgumentList @(
        "-NoLogo", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass",
        "-File", (Join-Path $WorktreeRoot "packaging/windows/smoke_test.ps1"),
        "-ExePath", $artifactPath,
        "-DataRoot", $buildHostData,
        "-EnvironmentKind", "BuildHost",
        "-EvidencePath", (Join-Path $WorktreeRoot "docs/engineering/DIST-01_EVIDENCE.md"),
        "-ExpectedSourceCommit", $BaseCommit
    ) -TimeoutSeconds 300 -FailureCode "dist01_buildhost_smoke_failed"
} finally {
    if (Test-Path -LiteralPath $buildHostData) {
        $resolvedBuildHostData = (Resolve-Path -LiteralPath $buildHostData).Path
        if (-not $resolvedBuildHostData.StartsWith(
            $buildHostTempRoot + '\', [StringComparison]::OrdinalIgnoreCase)) {
            throw "dist01_buildhost_data_containment_failed"
        }
        Remove-Item -LiteralPath $resolvedBuildHostData -Recurse -Force
    }
}
```

The worker removes only the newly created `$buildHostData` after its hash-free contents and outcome have been captured. Do not delete or reuse an existing user directory. A failure code is evidence, not a reason to weaken the ready-file, loopback, credential-status, SQLite, shutdown, or residue assertions.

- [ ] **W11. Perform the clean Windows x64 host acceptance gate.**

This is a real host gate, not an emulation label. The clean host has Windows x64, no installed Python, Node, npm, Docker CLI, or Docker Desktop, and receives only the reviewed `ProjectB.exe`, `smoke_test.ps1`, the expected source commit, an empty parent directory, and a newly named non-existing data-root path beneath that parent. The smoke script rejects an already existing data-root path so a typo cannot mutate user data. The worker or human operator launches exactly:

```powershell
& $env:PROJECTB_POWERSHELL_EXE -NoLogo -NoProfile -NonInteractive `
    -ExecutionPolicy Bypass -File $env:PROJECTB_DIST01_SMOKE_SCRIPT `
    -ExePath $env:PROJECTB_DIST01_EXE `
    -DataRoot $env:PROJECTB_DIST01_EMPTY_DATA_ROOT `
    -EnvironmentKind CleanWindowsX64 `
    -SmartScreenObservation NoWarningObserved `
    -EvidencePath $env:PROJECTB_DIST01_EVIDENCE `
    -ExpectedSourceCommit $env:PROJECTB_BASE_COMMIT
if ($LASTEXITCODE -ne 0) { throw "dist01_cleanhost_smoke_failed" }
```

All environment variables are absolute paths or the 40-hex reviewed base commit and are checked by the script before use. Change `NoWarningObserved` to `WarningObserved` only when the Windows UI actually displayed a SmartScreen warning; never infer either value from Authenticode status. Transfer the returned evidence through an approved local channel, validate its JSON schema and artifact hash on the implementation host, and replace only the fenced JSON in `DIST-01_EVIDENCE.md`. After evidence validation, delete only the newly created data-root path beneath the prevalidated empty parent; do not clean a broad parent or an existing user directory. Until this command actually runs, keep `cleanWindowsSmoke.status = "not_executed"` and DIST-01 cannot be marked complete.

- [ ] **W12. Run the focused and project-wide verification commands.**

```powershell
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "-m", "pytest", "backend/tests/integration/test_windows_distribution_contract.py", "-q"
) -TimeoutSeconds 300 -FailureCode "dist01_contract_regression_failed" | Out-Null
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "-m", "ruff", "check", "--config", "backend/pyproject.toml",
    "backend/tests/integration/test_windows_distribution_contract.py"
) -TimeoutSeconds 300 -FailureCode "dist01_ruff_failed" | Out-Null
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "-m", "mypy", "--config-file", "backend/pyproject.toml", "backend/src"
) -TimeoutSeconds 600 -FailureCode "dist01_mypy_failed" | Out-Null
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "scripts/test_all.py", "--profile", "local"
) -TimeoutSeconds 1800 -FailureCode "dist01_full_suite_failed" | Out-Null
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "scripts/scan_secrets.py", "--worktree", "--git-exe", $GitExe
) -TimeoutSeconds 300 -FailureCode "dist01_worktree_scanner_failed" | Out-Null
```

The evidence document lists each command and fresh exit status. It must not paste secrets, paths outside the project, raw environment values, or arbitrary application output. Any changed production dependency or application contract sends the unit back to W1 and invalidates the preceding build and clean-host result.

- [ ] **W13. Stage only the DIST-01 unit and capture the immutable review packet.**

```powershell
$dist01Paths = @(
    "packaging/windows/build.ps1",
    "packaging/windows/freezer-manifest.json",
    "packaging/windows/smoke_test.ps1",
    "backend/tests/integration/test_windows_distribution_contract.py",
    "docs/engineering/DIST-01_EVIDENCE.md"
)
$packet = Get-ReviewPacket -ExpectedPaths $dist01Paths
```

`Get-ReviewPacket` stages the whole owned path set, rejects every extra staged path, runs `git diff --cached --check`, performs the staged credential scan, binds the Git tree ID, and writes a binary/full-index diff into a private ACL-restricted temporary directory. The worker sends reviewers the packet path, packet SHA-256, tree ID, root/detailed plan hashes, dependency commit table, and verification summary; reviewers do not read mutable worktree files.

- [ ] **W14. Obtain a fresh specification-compliance review.**

The fresh reviewer checks the complete packet against `SPEC.md`, root DIST-01, AC-07, AC-11, AC-40, AC-43, the dependency table, and the frozen Windows contract in this plan. The findings-first response must explicitly cover:

- one-file Windows x64 output and clean-host runtime absence;
- loopback-only bind, external data root, SQLite persistence, unconfigured credential status, and graceful shutdown;
- exact Python/npm lock provenance and dependency-license notices;
- honest Authenticode, SmartScreen, build-host, and clean-host evidence states;
- absence of secrets, user courseware, runtime sidecars, and unowned paths.

The reviewer writes a private JSON receipt with all fields required by `Read-ReviewReceipt`. Any finding other than PASS returns the worker to the first affected step; after any edit W13-W15 are repeated with a new packet and tree.

- [ ] **W15. Obtain a distinct fresh quality/security/license review.**

The second reviewer must have a different reviewer identity and fresh session. It checks PowerShell quoting, absolute executable provenance, reparse containment, native exit handling, timeout/process-tree cleanup, cleanup scope, evidence parsing, redaction, PE architecture, resource inclusion, PyInstaller exclusions, supply-chain hashes, PyInstaller Bootloader Exception, bundled notices, test strength, and whether the clean-host procedure is reproducible. It also verifies no output or exception can disclose raw credential data. The same immutable packet binding and edit invalidation rules apply.

- [ ] **W16. Commit exactly the twice-reviewed tree.**

```powershell
$dist01Commit = Complete-ReviewedUnit -ExpectedPaths $dist01Paths `
    -Packet $packet -CommitMessage "feat(distribution): add reviewed Windows x64 package"
if ((Invoke-CheckedGit -Arguments @("rev-parse", "HEAD^{tree}")).Stdout.Trim() -ne
    $packet.TreeId) {
    throw "dist01 committed tree mismatch"
}
```

Record the returned commit only after the helper proves receipt bindings, reviewer distinctness, exact staged paths, a fresh staged scan, unchanged reviewed tree, successful commit, and `HEAD^{tree}` equality. The coordinator, not this worker, updates root `PLAN.md` and `AGENT_LOG.md` after consuming the reviewed commit.

### DIST-01 Completion Standard

DIST-01 is complete only when W1-W16 are all checked, the clean Windows x64 smoke really ran, both fresh reviewers returned PASS for the same staged tree, the commit tree equals the reviewed tree, and `DIST-01_EVIDENCE.md` contains fresh build-host and clean-host records for the identical artifact SHA-256. An unsigned executable or observed SmartScreen warning may be an honestly documented release limitation only if the root acceptance criteria permit it; it may never be represented as signed or warning-free.

## Task DIST-02: OCI Demo Distribution

**Goal:** Build and locally prove a deterministic, non-production OCI image that serves the demo WebUI as a non-root user, has no credential or courseware ingress, denies non-loopback egress, exposes only the reviewed demo profile, and produces reproducible image/SBOM/evidence metadata without publishing anything externally.

**Dependencies / parallelism:** Requires the reviewed DIST-01 commit, API-REG-01, DEMO-01C2, DEMO-REG-01, QA-01C2, and G-02C2. It is serial with DEMO-01A because it modifies the handed-off `demo/profile.json`; it is serial with CI-01A because CI consumes the image and evidence. It may not start until the coordinator has amended the root plan and G-02A dependency baseline with a named owner and SHA-256 for `packaging/oci/requirements-linux-amd64.lock`, and until DEMO-01C2/T-04 has supplied the exact session/CSRF transport receipt declared in D1. The existing `backend/requirements-windows-x64.lock` is a Windows-only architecture artifact and is never read, copied, renamed, or installed by this task. Missing Linux lock, Node digest, API-REG-01, or DEMO/T-04 transport evidence is a hard stop, not permission to use an unpinned `pip install` or infer a route.

**Files:**
- Create: `packaging/oci/Dockerfile`
- Create: `packaging/oci/entrypoint.sh`
- Create: `.dockerignore`
- Create: `packaging/oci/smoke_test.ps1`
- Create: `backend/tests/integration/test_oci_distribution_contract.py`
- Create: `docs/engineering/DIST-02_EVIDENCE.md`
- Modify, only through the DEMO-01A handoff and then freeze: `demo/profile.json`

### Frozen DIST-02 Handoff and Profile

Before D4, the worker verifies that the DEMO-01A reviewed tree supplies the following exact profile semantics. The worker may add the `distribution`, `persistence`, and `notice` objects shown below only if the predecessor review receipt explicitly permits those additive fields; it may not change session, limits, fixture, provider, or capability values. A mismatch is reported to the coordinator and the unit stops without editing `demo/profile.json`. The exact session transport is a reviewed `projectb_session` cookie plus a single-use `X-CSRF-Token` response header echoed in the same request header with exact `Origin`; this is a DEMO-01C2/T-04 predecessor contract, not an assumption made by DIST-02.

```json
{
  "schemaVersion": 1,
  "profileId": "demo",
  "session": {
    "idleTtlSeconds": 1800,
    "absoluteTtlSeconds": 7200,
    "id": "opaque",
    "reset": "caller_scoped"
  },
  "limits": {
    "activeCourses": 1,
    "materials": 20,
    "concurrentJobs": 2,
    "stateBytes": 67108864,
    "requestsPerIpPerMinute": 60
  },
  "fixtures": [
    {
      "id": "course-os-synthetic-v1",
      "path": "fixtures/course_os.json",
      "license": "CC0-1.0",
      "provenance": "project-generated"
    },
    {
      "id": "materials-os-synthetic-v1",
      "path": "fixtures/materials.json",
      "license": "CC0-1.0",
      "provenance": "project-generated"
    }
  ],
  "provider": {
    "adapterId": "deterministic.mock",
    "network": "disabled",
    "credentials": "disabled",
    "production": false
  },
  "capabilities": {
    "allowUpload": false,
    "allowPathInput": false,
    "allowUrlInput": false,
    "allowCredentialInput": false,
    "allowExternalProvider": false
  },
  "distribution": {
    "runtime": "oci",
    "architecture": "linux/amd64",
    "publicUrl": "not_executed"
  },
  "persistence": {
    "kind": "ephemeral",
    "root": "/tmp/projectb-demo",
    "clearOnRestart": true
  },
  "notice": {
    "data": "synthetic-demo-only",
    "model": "deterministic-mock"
  }
}
```

The profile endpoint returns a non-secret banner/profile contract without disclosing filesystem paths, credentials, host environment, or provider secrets. `POST /api/demo/session/reset` resets only the caller's opaque session. Fixture-ID-only workflow routes remain owned by DEMO-01B/DEMO-01C2; DIST-02 consumes their reviewed route and payload contract read-only and does not invent a second fixture endpoint. Path, URL, upload, arbitrary JSON, credential-shaped fields, and provider IDs must be rejected with a stable 4xx code. If DEMO-01C2 has not published a stable route/payload in its reviewed evidence, the OCI smoke records the workflow as predecessor-delegated and D2/D-025 remains blocked rather than guessing.

### D1. Re-run the fail-closed prelude and dependency gate

```powershell
Assert-UnitStart -ExpectedUnit "DIST-02"
$expectedTransport = "session-cookie:projectb_session;csrf-response-header:X-CSRF-Token;csrf-request-header:X-CSRF-Token;origin:exact"
if ($env:PROJECTB_DEMO_T04_TRANSPORT -cne $expectedTransport) {
    throw "oci_demo_t04_transport_unbound"
}
$expectedLinuxLock = Join-Path $WorktreeRoot "packaging/oci/requirements-linux-amd64.lock"
if (-not (Test-Path -LiteralPath $expectedLinuxLock -PathType Leaf)) {
    throw "oci_linux_lock_owner_missing"
}
$linuxLockText = [IO.File]::ReadAllText($expectedLinuxLock)
if ($linuxLockText -match "requirements-windows-x64|win32|win_amd64" -or
    $linuxLockText -notmatch "--hash=sha256:") {
    throw "oci_linux_lock_architecture_invalid"
}
$linuxLockSha = (Get-FileHash -LiteralPath $expectedLinuxLock -Algorithm SHA256).Hash.ToLowerInvariant()
if ($env:PROJECTB_LINUX_LOCK_SHA256 -notmatch "^[0-9a-f]{64}$" -or
    $linuxLockSha -ne $env:PROJECTB_LINUX_LOCK_SHA256.ToLowerInvariant()) {
    throw "oci_linux_lock_hash_unbound"
}
if ($env:PROJECTB_LINUX_LOCK_OWNER -notmatch "^[A-Za-z0-9][A-Za-z0-9._-]{1,63}$") {
    throw "oci_linux_lock_owner_missing"
}
foreach ($name in @(
    "PROJECTB_DEMO_01C2_COMMIT",
    "PROJECTB_DIST_01_COMMIT",
    "PROJECTB_APIREG01_COMMIT",
    "PROJECTB_QA_01C2_COMMIT",
    "PROJECTB_DEMO_REG_01_COMMIT",
    "PROJECTB_G02C2_COMMIT"
)) {
    if ([Environment]::GetEnvironmentVariable($name) -notmatch "^[0-9a-f]{40}$") {
        throw "oci_predecessor_hash_unbound"
    }
}
$dependencyBaseline = [IO.File]::ReadAllText(
    (Join-Path $WorktreeRoot "docs/engineering/DEPENDENCY_BASELINE.md")
)
if ($dependencyBaseline -notmatch
    "d45d78e7929b46875bbd4e29bea672d5bc48186c6c3588306521c815e78352d6") {
    throw "oci_node_digest_unowned"
}
if ($dependencyBaseline -notmatch "linux/amd64[^\r\n]*d45d78e7929b46875bbd4e29bea672d5bc48186c6c3588306521c815e78352d6" -or
    $dependencyBaseline -notmatch "G-02A[^\r\n]*verified") {
    throw "oci_node_digest_unowned"
}
if ((Get-Content -Raw -LiteralPath (Join-Path $WorktreeRoot "backend/requirements-windows-x64.lock")) -match
    "requirements-linux-amd64") {
    throw "windows_lock_cross_reference_invalid"
}
```

The named Linux lock owner must have supplied the root/G-02A baseline hash before this step is attempted. D1 does not create or stage that lock. It records the exact hash in the private worker transcript and in the evidence provenance object only; the coordinator updates the root baseline and task dependency table. A missing owner, missing hash, Windows marker, or hashless line stops the task before any Docker context or source edit.

### D2. Write the smallest failing OCI contract test first

Create `backend/tests/integration/test_oci_distribution_contract.py` with deterministic text/JSON assertions. The first run must fail because the six implementation/evidence files do not exist. The test must not build an image, contact a registry, read user courseware, invoke a model, or inspect a developer machine. It uses only repository-relative paths and standard-library parsing.

```python
from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OCI = ROOT / "packaging" / "oci"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_oci_files_and_profile_exist() -> None:
    for path in (
        OCI / "Dockerfile",
        OCI / "entrypoint.sh",
        OCI / "smoke_test.ps1",
        ROOT / ".dockerignore",
        ROOT / "docs/engineering/DIST-02_EVIDENCE.md",
        ROOT / "demo/profile.json",
    ):
        assert path.is_file(), path


def test_dockerfile_is_digest_pinned_and_uses_linux_lock_only() -> None:
    text = read_text(OCI / "Dockerfile")
    assert "node:24.18.0-bookworm-slim@sha256:d45d78e7929b46875bbd4e29bea672d5bc48186c6c3588306521c815e78352d6" in text
    assert "python:3.14.6-slim-bookworm@sha256:f70215e5dbe2a47dee6d23f9c6d358bf3c148f59cce2fd165b61118e9d80f2bb" in text
    assert "requirements-linux-amd64.lock" in text
    assert "requirements-windows-x64.lock" not in text
    assert re.search(r"pip\s+install[^\n]*--require-hashes", text)
    assert "pip install -r" not in text
    for source in re.findall(
        r"^FROM\s+(?:--platform=[^\s]+\s+)?([^\s]+)",
        text,
        flags=re.MULTILINE,
    ):
        assert re.search(r"@sha256:[0-9a-f]{64}$", source), source
    assert "ADD http" not in text.lower()
    assert "ARG API_KEY" not in text and "ARG TOKEN" not in text


def test_runtime_is_non_root_and_demo_locked() -> None:
    dockerfile = read_text(OCI / "Dockerfile")
    entrypoint = read_text(OCI / "entrypoint.sh")
    assert re.search(r"USER\s+10001:10001", dockerfile)
    assert "HEALTHCHECK" in dockerfile
    assert "PROJECTB_PROFILE=demo" in dockerfile and "PROJECTB_PROFILE" in entrypoint
    assert "deterministic.mock" in dockerfile and "deterministic.mock" in entrypoint
    assert "PROJECTB_EGRESS_POLICY=deny" in dockerfile and "PROJECTB_EGRESS_POLICY" in entrypoint
    assert "PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring" in dockerfile
    assert "tmpfs" in dockerfile.lower() or "projectb-demo" in dockerfile
    assert "audit" in dockerfile.lower()
    assert "socket.getaddrinfo" in dockerfile
    assert "socket.connect" in dockerfile
    assert "exec" in entrypoint
    assert "set -eu" in entrypoint or "set -euo pipefail" in entrypoint


def test_context_excludes_private_inputs() -> None:
    text = read_text(ROOT / ".dockerignore")
    for pattern in (".env", ".env.*", "**/*.sqlite*", "**/*.db", "**/private", "**/*.pem", "**/*.key"):
        assert pattern in text
    assert "frontend/node_modules" in text
    assert "backend/tests" in text
    assert "demo/fixtures/**" in text


def test_profile_is_demo_only_and_fixture_provenance_is_explicit() -> None:
    profile = json.loads(read_text(ROOT / "demo/profile.json"))
    assert profile["schemaVersion"] == 1
    assert profile["profileId"] == "demo"
    assert profile["session"]["idleTtlSeconds"] == 1800
    assert profile["session"]["absoluteTtlSeconds"] == 7200
    assert profile["limits"] == {
        "activeCourses": 1,
        "materials": 20,
        "concurrentJobs": 2,
        "stateBytes": 67108864,
        "requestsPerIpPerMinute": 60,
    }
    assert profile["provider"] == {
        "adapterId": "deterministic.mock",
        "network": "disabled",
        "credentials": "disabled",
        "production": False,
    }
    assert all(item["license"] == "CC0-1.0" for item in profile["fixtures"])
    assert profile["capabilities"] == {
        "allowUpload": False,
        "allowPathInput": False,
        "allowUrlInput": False,
        "allowCredentialInput": False,
        "allowExternalProvider": False,
    }


def test_evidence_states_are_truthful() -> None:
    evidence = read_text(ROOT / "docs/engineering/DIST-02_EVIDENCE.md")
    match = re.search(r"```json\s+(.*?)\s+```", evidence, flags=re.DOTALL)
    assert match is not None
    payload = json.loads(match.group(1))
    assert payload["image"]["status"] in {"not_executed", "pass"}
    assert payload["localSmoke"]["status"] == payload["image"]["status"]
    assert payload["publicUrl"]["status"] == "not_executed"
    assert payload["deployment"]["status"] == "not_executed"
    assert "api_key" not in evidence.lower()
    assert "password" not in evidence.lower()
```

The failing command and failure reason are recorded before D3. The test is deliberately strict about the forbidden Windows lock and unpinned install so a future maintainer cannot silently make Linux depend on a Windows wheel set.

### D3. Record the red result

```powershell
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "-m", "pytest", "backend/tests/integration/test_oci_distribution_contract.py", "-q"
) -TimeoutSeconds 300 -FailureCode "dist02_expected_red_missing_files"
```

The command must exit non-zero because the target files are absent or incomplete. Capture only a redacted command ID, exit code, and assertion summary; do not write raw output containing paths, environment variables, or host information to any tracked file.

### D4. Validate and freeze the handed-off demo profile

Compare the reviewed DEMO-01A `demo/profile.json` against the frozen profile above with a structural JSON comparison. If the predecessor already contains every field and exact value, leave it byte-for-byte unchanged but keep it in the eventual whole-index unit only when DIST-02 actually modifies it. If the reviewed handoff explicitly reserves the three additive objects, add exactly `distribution`, `persistence`, and `notice` using the JSON block above. If any existing field differs, stop with `oci_profile_handoff_mismatch`; do not overwrite the predecessor's decision.

After the permitted edit, run:

```powershell
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "-m", "pytest", "backend/tests/integration/test_oci_distribution_contract.py",
    "-q", "-k", "profile"
) -TimeoutSeconds 300 -FailureCode "dist02_profile_contract_failed" | Out-Null
```

Only the profile test should turn green here; the overall file still fails until D5-D7. The coordinator must ensure DEMO-01C2's API schema and fixture IDs use the same contract before this unit can pass review.

### D5. Implement the pinned multi-stage OCI image

Create `packaging/oci/Dockerfile` exactly as follows. The Node digest is a dispatch precondition: it remains blocked until `DEPENDENCY_BASELINE.md` owns the verified linux/amd64 digest. The Linux lock is copied read-only from its separately owned predecessor; this task does not generate or stage it.

````dockerfile
# syntax=docker/dockerfile:1.7
FROM --platform=linux/amd64 node:24.18.0-bookworm-slim@sha256:d45d78e7929b46875bbd4e29bea672d5bc48186c6c3588306521c815e78352d6 AS frontend-build
WORKDIR /build/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci --ignore-scripts --no-audit --no-fund
COPY frontend/ ./
RUN npm run build

FROM --platform=linux/amd64 python:3.14.6-slim-bookworm@sha256:f70215e5dbe2a47dee6d23f9c6d358bf3c148f59cce2fd165b61118e9d80f2bb AS python-deps
WORKDIR /build
COPY packaging/oci/requirements-linux-amd64.lock /tmp/requirements-linux-amd64.lock
RUN python -m pip install --require-hashes --no-deps --only-binary=:all: --no-cache-dir --target=/opt/projectb/site-packages -r /tmp/requirements-linux-amd64.lock

FROM --platform=linux/amd64 python:3.14.6-slim-bookworm@sha256:f70215e5dbe2a47dee6d23f9c6d358bf3c148f59cce2fd165b61118e9d80f2bb AS runtime
ARG PROJECTB_SOURCE_COMMIT
RUN case "$PROJECTB_SOURCE_COMMIT" in \
      ????????) ;; \
      ????????????????????????????????????????) ;; \
      *) exit 42 ;; \
    esac
LABEL org.opencontainers.image.title="ProjectB Demo" \
      org.opencontainers.image.version="0.1.0" \
      org.opencontainers.image.revision="$PROJECTB_SOURCE_COMMIT" \
      org.opencontainers.image.source="local-course-project" \
      org.opencontainers.image.licenses="NOASSERTION" \
      io.projectb.profile="demo" \
      io.projectb.network-policy="deny-egress"

ENV PYTHONPATH=/opt/projectb/site-packages:/opt/projectb/app \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HOME=/nonexistent \
    PROJECTB_PROFILE=demo \
    PROJECTB_PROVIDER_ADAPTER=deterministic.mock \
    PROJECTB_EGRESS_POLICY=deny \
    PROJECTB_DATA_ROOT=/tmp/projectb-demo \
    PROJECTB_STATIC_ROOT=/opt/projectb/static \
    PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring \
    PORT=7860

WORKDIR /opt/projectb
COPY --from=python-deps /opt/projectb/site-packages/ /opt/projectb/site-packages/
COPY backend/src/ /opt/projectb/app/
COPY --from=frontend-build /build/frontend/dist/ /opt/projectb/static/
COPY demo/profile.json /opt/projectb/demo/profile.json
COPY demo/fixtures/ /opt/projectb/demo/fixtures/
COPY packaging/oci/requirements-linux-amd64.lock /opt/projectb/licenses/requirements-linux-amd64.lock
COPY docs/engineering/DEPENDENCY_BASELINE.md /opt/projectb/licenses/DEPENDENCY_BASELINE.md
COPY --chmod=0555 packaging/oci/entrypoint.sh /usr/local/bin/projectb-entrypoint

RUN mkdir -p /opt/projectb/licenses/debian-notices /tmp/projectb-demo \
    && cp -a /usr/share/doc/. /opt/projectb/licenses/debian-notices/ \
    && chmod -R a-w /opt/projectb/app /opt/projectb/static /opt/projectb/demo /opt/projectb/licenses \
    && chmod 1770 /tmp/projectb-demo \
    && chown 10001:10001 /tmp/projectb-demo

RUN <<'PY'
from __future__ import annotations

import hashlib
import importlib.metadata
import json
import re
import subprocess
from pathlib import Path

root = Path("/opt/projectb")
lock = root / "licenses/requirements-linux-amd64.lock"
baseline = root / "licenses/DEPENDENCY_BASELINE.md"


def spdx_id(prefix: str, value: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9.-]", "-", value)
    return f"SPDXRef-{prefix}-{safe}"


packages: list[dict[str, object]] = []
for distribution in sorted(importlib.metadata.distributions(path=[str(root / "site-packages")]), key=lambda item: (item.metadata.get("Name", "").lower(), item.version)):
    name = distribution.metadata.get("Name", "unknown")
    license_value = distribution.metadata.get("License") or "NOASSERTION"
    packages.append({
        "SPDXID": spdx_id("Python", f"{name}-{distribution.version}"),
        "name": name,
        "versionInfo": distribution.version,
        "downloadLocation": "NOASSERTION",
        "filesAnalyzed": False,
        "licenseConcluded": "NOASSERTION",
        "licenseDeclared": license_value if re.fullmatch(r"[A-Za-z0-9.+-]+", license_value) else "NOASSERTION",
        "supplier": "NOASSERTION",
        "externalRefs": [{
            "referenceCategory": "PACKAGE-MANAGER",
            "referenceType": "purl",
            "referenceLocator": f"pkg:pypi/{name.lower()}@{distribution.version}",
        }],
    })

dpkg = subprocess.run(
    ["dpkg-query", "-W", "-f=${binary:Package}\t${Version}\n"],
    check=True,
    capture_output=True,
    text=True,
    timeout=30,
)
for line in sorted(item for item in dpkg.stdout.splitlines() if item):
    name, version = line.split("\t", 1)
    packages.append({
        "SPDXID": spdx_id("Debian", f"{name}-{version}"),
        "name": name,
        "versionInfo": version,
        "downloadLocation": "NOASSERTION",
        "filesAnalyzed": False,
        "licenseConcluded": "NOASSERTION",
        "licenseDeclared": "NOASSERTION",
        "supplier": "Organization: Debian",
        "externalRefs": [{
            "referenceCategory": "PACKAGE-MANAGER",
            "referenceType": "purl",
            "referenceLocator": f"pkg:deb/debian/{name}@{version}",
        }],
    })

lock_sha = hashlib.sha256(lock.read_bytes()).hexdigest()
baseline_sha = hashlib.sha256(baseline.read_bytes()).hexdigest()
document = {
    "spdxVersion": "SPDX-2.3",
    "dataLicense": "CC0-1.0",
    "SPDXID": "SPDXRef-DOCUMENT",
    "name": "ProjectB-demo-oci",
    "documentNamespace": f"https://local.invalid/projectb/sbom/{lock_sha}",
    "creationInfo": {
        "created": "1970-01-01T00:00:00Z",
        "creators": ["Tool: ProjectB deterministic OCI builder"],
        "licenseListVersion": "3.26",
    },
    "documentDescribes": [item["SPDXID"] for item in packages],
    "packages": packages,
    "annotations": [{
        "annotationDate": "1970-01-01T00:00:00Z",
        "annotationType": "OTHER",
        "annotator": "Tool: ProjectB deterministic OCI builder",
        "comment": f"linux_lock_sha256={lock_sha};dependency_baseline_sha256={baseline_sha}",
    }],
}
(root / "licenses/sbom.spdx.json").write_text(
    json.dumps(document, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)
PY

RUN <<'PY'
from pathlib import Path

launcher = r'''from __future__ import annotations

import ipaddress
import os
import socket
import sys


def _allow_loopback(host: object) -> bool:
    if isinstance(host, bytes):
        host = host.decode("ascii", errors="strict")
    if not isinstance(host, str):
        return False
    if host.lower() == "localhost":
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


def _deny_egress(event: str, args: tuple[object, ...]) -> None:
    host: object | None = None
    if event == "socket.getaddrinfo" and args:
        host = args[0]
    elif event in {"socket.connect", "socket.connect_ex"} and len(args) > 1:
        address = args[1]
        if isinstance(address, str):
            return
        if isinstance(address, tuple) and address:
            host = address[0]
    if host is not None and not _allow_loopback(host):
        raise PermissionError("demo_egress_denied")


if os.environ.get("PROJECTB_EGRESS_POLICY") != "deny":
    raise SystemExit("oci_contract_invalid")
sys.addaudithook(_deny_egress)

import uvicorn
from projectb.api.app import create_app

app = create_app(profile="demo")
uvicorn.run(app, host="0.0.0.0", port=int(os.environ["PORT"]), access_log=False)
'''
Path("/opt/projectb/oci_launcher.py").write_text(launcher, encoding="utf-8")
PY

RUN chmod 0444 /opt/projectb/oci_launcher.py /opt/projectb/licenses/sbom.spdx.json \
    && find /opt/projectb -xdev -type f -perm /022 -exec chmod go-w {} +

USER 10001:10001
EXPOSE 7860
HEALTHCHECK --interval=10s --timeout=3s --start-period=20s --retries=6 CMD ["python", "-c", "import json,urllib.request; d=json.load(urllib.request.urlopen('http://127.0.0.1:7860/api/health', timeout=2)); raise SystemExit(0 if d == {'status':'ok','profile':'demo'} else 1)"]
ENTRYPOINT ["/usr/local/bin/projectb-entrypoint"]
````

Do not add `apt-get`, `curl | sh`, remote `ADD`, a shell installer, `VOLUME`, secret build arguments, registry credentials, or production configuration. `npm ci --ignore-scripts` and wheel-only hashed Python installation make dependency installation explicit. If the separately owned Linux lock cannot be satisfied with wheels for linux/amd64/Python 3.14.6, the lock owner fixes and re-reviews it; DIST-02 does not remove `--only-binary`, `--require-hashes`, or `--no-deps` to force a build through.

### D6. Implement the entrypoint and allowlisted build context

Create `packaging/oci/entrypoint.sh`:

````sh
#!/bin/sh
set -eu

fail() {
    printf '%s\n' "$1" >&2
    exit "$2"
}

[ "$#" -eq 0 ] || fail "oci_invalid_argument" 64
[ "$(id -u)" = "10001" ] || fail "oci_contract_invalid" 65
[ "$(id -g)" = "10001" ] || fail "oci_contract_invalid" 65
[ "${PROJECTB_PROFILE:-}" = "demo" ] || fail "oci_contract_invalid" 65
[ "${PROJECTB_PROVIDER_ADAPTER:-}" = "deterministic.mock" ] || fail "oci_contract_invalid" 65
[ "${PROJECTB_EGRESS_POLICY:-}" = "deny" ] || fail "oci_contract_invalid" 65
[ "${PROJECTB_DATA_ROOT:-}" = "/tmp/projectb-demo" ] || fail "oci_contract_invalid" 65
[ "${PYTHON_KEYRING_BACKEND:-}" = "keyring.backends.null.Keyring" ] || fail "oci_contract_invalid" 65

case "${PORT:-}" in
    ''|*[!0-9]*) fail "oci_invalid_argument" 64 ;;
esac
[ "$PORT" -ge 1024 ] && [ "$PORT" -le 65535 ] || fail "oci_invalid_argument" 64

for name in $(env | sed 's/=.*//' | LC_ALL=C sort); do
    case "$name" in
        *API_KEY*|*TOKEN*|*PASSWORD*|*SECRET*|*CREDENTIAL*)
            fail "oci_contract_invalid" 65
            ;;
    esac
done

[ -d "/tmp/projectb-demo" ] || fail "oci_contract_invalid" 65
[ -w "/tmp/projectb-demo" ] || fail "oci_contract_invalid" 65
[ ! -L "/tmp/projectb-demo" ] || fail "oci_contract_invalid" 65
if find /tmp/projectb-demo -mindepth 1 -maxdepth 1 -print -quit | grep -q .; then
    fail "oci_contract_invalid" 65
fi

umask 077
exec /usr/local/bin/python /opt/projectb/oci_launcher.py
````

The script emits only stable codes and never prints the rejected environment name or value. It performs every check before importing application code. Do not add argument forwarding or a shell escape: the only process after validation is the fixed Python launcher.

Create the repository-root `.dockerignore` as an allowlist with explicit defense-in-depth exclusions:

```dockerignore
**
!frontend/
!frontend/**
!backend/
!backend/src/
!backend/src/**
!packaging/
!packaging/oci/
!packaging/oci/**
!demo/
!demo/profile.json
!demo/fixtures/
!demo/fixtures/**
!docs/
!docs/engineering/
!docs/engineering/DEPENDENCY_BASELINE.md

.git
.worktrees
.env
.env.*
**/.env
**/.env.*
**/*.sqlite*
**/*.db
**/private
**/private/**
**/*.pem
**/*.key
**/*.pfx
**/*.p12
**/*.pdf
**/*.doc
**/*.docx
**/*.ppt
**/*.pptx
**/*.xls
**/*.xlsx
**/node_modules
frontend/node_modules
frontend/dist
backend/tests
dist
artifacts
```

The later build runs only from the repository root and passes no additional context. This allowlist admits production frontend sources, production backend sources, the separately reviewed Linux lock, synthetic demo fixtures/profile, OCI scripts, and the dependency baseline. It excludes Git metadata, worktrees, test trees, generated artifacts, user documents, databases, private directories, credentials, and common key containers even if a future broad allowlist rule is added above them.

Run the deterministic structural subset after D5-D6:

```powershell
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "-m", "pytest", "backend/tests/integration/test_oci_distribution_contract.py",
    "-q", "-k", "dockerfile or runtime or context or profile"
) -TimeoutSeconds 300 -FailureCode "dist02_structural_contract_failed" | Out-Null
```

At this point the evidence-file test remains red by design.

### D7. Implement bounded local image smoke and evidence capture

Before creating the smoke script, the coordinator must bind one reviewed DEMO/T-04 handoff: a successful `GET /api/demo/profile` issues a caller/session-bound single-use CSRF proof in the `X-CSRF-Token` response header, and a state-changing request sends it in the same-named request header with exact `Origin`. The token is never placed in JSON, logs, evidence, URLs, or reviewer packets. If the upstream plans choose another safe transport, they must amend this step and its test before dispatch; the worker must not bypass middleware or reach into app memory.

Create `packaging/oci/smoke_test.ps1`:

````powershell
[CmdletBinding()]
param(
    [Parameter(Mandatory)][string]$ImageRef,
    [Parameter(Mandatory)][ValidatePattern('^[0-9a-f]{40}$')][string]$ExpectedSourceCommit,
    [Parameter(Mandatory)][string]$ExpectedLinuxLockSha256,
    [Parameter(Mandatory)][ValidatePattern('^[0-9a-f]{40}$')][string]$Demo01C2Commit,
    [Parameter(Mandatory)][ValidatePattern('^[0-9a-f]{40}$')][string]$Dist01Commit,
    [Parameter(Mandatory)][ValidatePattern('^[0-9a-f]{40}$')][string]$ApiReg01Commit,
    [Parameter(Mandatory)][ValidatePattern('^[0-9a-f]{40}$')][string]$Qa01C2Commit,
    [Parameter(Mandatory)][ValidatePattern('^[0-9a-f]{40}$')][string]$DemoReg01Commit,
    [Parameter(Mandatory)][ValidatePattern('^[0-9a-f]{40}$')][string]$G02C2Commit,
    [Parameter(Mandatory)][string]$EvidencePath,
    [Parameter(Mandatory)][string]$SbomOutputDirectory,
    [ValidateRange(30, 300)][int]$StartupTimeoutSeconds = 90
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Stop-Smoke {
    param([Parameter(Mandatory)][string]$Code)
    throw $Code
}

function Assert-AbsoluteLeaf {
    param([Parameter(Mandatory)][string]$Path, [Parameter(Mandatory)][string]$Code)
    if (-not [IO.Path]::IsPathFullyQualified($Path) -or
        -not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        Stop-Smoke $Code
    }
    $full = [IO.Path]::GetFullPath($Path)
    $current = [IO.Path]::GetPathRoot($full)
    foreach ($part in $full.Substring($current.Length).Split(
        @('\', '/'), [StringSplitOptions]::RemoveEmptyEntries
    )) {
        $current = Join-Path $current $part
        $item = Get-Item -LiteralPath $current -Force -ErrorAction Stop
        if (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
            Stop-Smoke $Code
        }
    }
    return $full
}

function Stop-ProcessTree {
    param([Parameter(Mandatory)][Diagnostics.Process]$Process)
    $rootId = $Process.Id
    $descendants = New-Object 'System.Collections.Generic.List[int]'
    $queue = New-Object 'System.Collections.Generic.Queue[int]'
    $queue.Enqueue($rootId)
    while ($queue.Count -gt 0) {
        $parentId = $queue.Dequeue()
        foreach ($child in @(Get-CimInstance Win32_Process -Filter "ParentProcessId=$parentId" `
            -ErrorAction SilentlyContinue)) {
            $childId = [int]$child.ProcessId
            if (-not $descendants.Contains($childId)) {
                $descendants.Add($childId)
                $queue.Enqueue($childId)
            }
        }
    }
    foreach ($childId in @($descendants.ToArray() | Sort-Object -Descending)) {
        Stop-Process -Id $childId -Force -ErrorAction SilentlyContinue
    }
    Stop-Process -Id $rootId -Force -ErrorAction SilentlyContinue
    $deadline = [Diagnostics.Stopwatch]::StartNew()
    do {
        $alive = @(Get-Process -Id (@($rootId) + $descendants.ToArray()) `
            -ErrorAction SilentlyContinue)
        if ($alive.Count -gt 0) { Start-Sleep -Milliseconds 25 }
    } while ($alive.Count -gt 0 -and $deadline.ElapsedMilliseconds -lt 5000)
    if ($alive.Count -gt 0) { Stop-Smoke "oci_cleanup_failed" }
}

function ConvertTo-Argument {
    param([Parameter(Mandatory)][string]$Value)
    if ($Value.IndexOf([char]0) -ge 0 -or $Value -match "[\r\n]") {
        Stop-Smoke "oci_invalid_argument"
    }
    if ($Value -notmatch '[\s"]') { return $Value }
    return '"' + ($Value -replace '(\\*)"', '$1$1\"' -replace '(\\+)$', '$1$1') + '"'
}

function Invoke-Docker {
    param(
        [Parameter(Mandatory)][string[]]$Arguments,
        [ValidateRange(1, 1800)][int]$TimeoutSeconds = 300,
        [Parameter(Mandatory)][string]$FailureCode
    )
    $start = [Diagnostics.ProcessStartInfo]::new()
    $start.FileName = $script:DockerExe
    $start.Arguments = (($Arguments | ForEach-Object { ConvertTo-Argument ([string]$_) }) -join " ")
    $start.WorkingDirectory = (Get-Location).Path
    $start.UseShellExecute = $false
    $start.CreateNoWindow = $true
    $start.RedirectStandardOutput = $true
    $start.RedirectStandardError = $true
    $process = [Diagnostics.Process]::new()
    $process.StartInfo = $start
    try {
        if (-not $process.Start()) { Stop-Smoke $FailureCode }
        $stdoutTask = $process.StandardOutput.ReadToEndAsync()
        $stderrTask = $process.StandardError.ReadToEndAsync()
        if (-not $process.WaitForExit($TimeoutSeconds * 1000)) {
            Stop-ProcessTree $process
            Stop-Smoke $FailureCode
        }
        $stdout = $stdoutTask.GetAwaiter().GetResult()
        $stderr = $stderrTask.GetAwaiter().GetResult()
        if ($stdout.Length -gt 1048576 -or $stderr.Length -gt 1048576 -or
            $process.ExitCode -ne 0) {
            Stop-Smoke $FailureCode
        }
        return [pscustomobject]@{ ExitCode=$process.ExitCode; Stdout=$stdout }
    } finally {
        $process.Dispose()
    }
}

function Get-FreeLoopbackPort {
    $listener = [Net.Sockets.TcpListener]::new([Net.IPAddress]::Loopback, 0)
    $listener.Start()
    try { return ([Net.IPEndPoint]$listener.LocalEndpoint).Port }
    finally { $listener.Stop() }
}

function New-DemoClient {
    $cookies = [Net.CookieContainer]::new()
    $handler = [Net.Http.HttpClientHandler]::new()
    $handler.CookieContainer = $cookies
    $handler.UseCookies = $true
    $handler.UseProxy = $false
    $client = [Net.Http.HttpClient]::new($handler)
    $client.Timeout = [TimeSpan]::FromSeconds(10)
    return [pscustomobject]@{ Client=$client; Handler=$handler; Cookies=$cookies }
}

function Invoke-DemoJson {
    param(
        [Parameter(Mandatory)][object]$ClientState,
        [Parameter(Mandatory)][Net.Http.HttpMethod]$Method,
        [Parameter(Mandatory)][Uri]$Uri,
        [AllowNull()][object]$Body,
        [AllowNull()][string]$CsrfToken
    )
    $request = [Net.Http.HttpRequestMessage]::new($Method, $Uri)
    try {
        if ($Method -ne [Net.Http.HttpMethod]::Get) {
            $request.Headers.Add("Origin", $script:Origin)
            if (-not [string]::IsNullOrWhiteSpace($CsrfToken)) {
                $request.Headers.Add("X-CSRF-Token", $CsrfToken)
            }
            $json = if ($null -eq $Body) { "{}" } else { $Body | ConvertTo-Json -Depth 10 -Compress }
            $request.Content = [Net.Http.StringContent]::new(
                $json, [Text.Encoding]::UTF8, "application/json"
            )
        }
        $response = $ClientState.Client.SendAsync($request).GetAwaiter().GetResult()
        try {
            $raw = $response.Content.ReadAsStringAsync().GetAwaiter().GetResult()
            if ($raw.Length -gt 262144) { Stop-Smoke "oci_profile_failed" }
            $payload = if ([string]::IsNullOrWhiteSpace($raw)) { $null } else { $raw | ConvertFrom-Json }
            $csrfValues = [Collections.Generic.IEnumerable[string]]$null
            $csrf = $null
            if ($response.Headers.TryGetValues("X-CSRF-Token", [ref]$csrfValues)) {
                $csrfItems = @($csrfValues)
                if ($csrfItems.Count -ne 1 -or $csrfItems[0].Length -lt 32 -or
                    $csrfItems[0] -match "[\r\n]") {
                    Stop-Smoke "oci_profile_failed"
                }
                $csrf = $csrfItems[0]
            }
            return [pscustomobject]@{
                Status = [int]$response.StatusCode
                Json = $payload
                Csrf = $csrf
            }
        } finally {
            $response.Dispose()
        }
    } finally {
        $request.Dispose()
    }
}

function Get-CookieFingerprint {
    param([Parameter(Mandatory)][object]$ClientState, [Parameter(Mandatory)][Uri]$Uri)
    $cookies = @($ClientState.Cookies.GetCookies($Uri) |
        Where-Object { $_.Name -eq $script:ExpectedSessionCookieName })
    if ($cookies.Count -ne 1 -or [string]::IsNullOrWhiteSpace($cookies[0].Value)) {
        Stop-Smoke "oci_isolation_failed"
    }
    $values = @($cookies | ForEach-Object { $_.Name + "=" + $_.Value } | Sort-Object)
    $bytes = [Text.Encoding]::UTF8.GetBytes(($values -join "`n"))
    $hash = [Security.Cryptography.SHA256]::Create()
    try {
        return ([BitConverter]::ToString($hash.ComputeHash($bytes))).Replace("-", "").ToLowerInvariant()
    } finally {
        $hash.Dispose()
    }
}

function Write-Evidence {
    param([Parameter(Mandatory)][hashtable]$Record)
    if (-not [IO.Path]::IsPathFullyQualified($EvidencePath)) { Stop-Smoke "oci_evidence_invalid" }
    $parent = Split-Path -Parent $EvidencePath
    if (-not (Test-Path -LiteralPath $parent -PathType Container)) { Stop-Smoke "oci_evidence_invalid" }
    $json = $Record | ConvertTo-Json -Depth 20
    if ($json -match '(?i)(api.?key|password|bearer|credential)[^\r\n]{0,64}[:=]') {
        Stop-Smoke "oci_evidence_invalid"
    }
    $markdown = @(
        "# DIST-02 Evidence"
        ""
        '```json'
        $json
        '```'
        ""
    ) -join [Environment]::NewLine
    [IO.File]::WriteAllText($EvidencePath, $markdown, [Text.UTF8Encoding]::new($false))
}

if ($ImageRef -notmatch '^projectb-demo:(local|dist02-[0-9a-f]{8,40})$' -or
    $ExpectedSourceCommit -notmatch '^[0-9a-f]{40}$' -or
    $ExpectedLinuxLockSha256 -notmatch '^[0-9a-f]{64}$') {
    Stop-Smoke "oci_invalid_argument"
}
$script:DockerExe = $env:PROJECTB_DOCKER_EXE
Assert-AbsoluteLeaf -Path $script:DockerExe -Code "oci_engine_failed"
if ([IO.Path]::GetFileName($script:DockerExe).ToLowerInvariant() -ne "docker.exe" -or
    $script:DockerExe -cne $env:PROJECTB_DOCKER_EXE) {
    Stop-Smoke "oci_engine_failed"
}
$script:ExpectedSessionCookieName = "projectb_session"
if ($env:PROJECTB_DEMO_T04_TRANSPORT -cne
    "session-cookie:projectb_session;csrf-response-header:X-CSRF-Token;csrf-request-header:X-CSRF-Token;origin:exact") {
    Stop-Smoke "oci_demo_t04_transport_unbound"
}
if (-not [IO.Path]::IsPathFullyQualified($EvidencePath) -or
    -not [IO.Path]::IsPathFullyQualified($SbomOutputDirectory) -or
    (Test-Path -LiteralPath $SbomOutputDirectory)) {
    Stop-Smoke "oci_invalid_argument"
}
[IO.Directory]::CreateDirectory($SbomOutputDirectory) | Out-Null

$suffix = [guid]::NewGuid().ToString("N")
$inspectContainer = "projectb-dist02-inspect-$suffix"
$runContainer = "projectb-dist02-run-$suffix"
$networkName = "projectb-dist02-net-$suffix"
$runStarted = $false
$networkCreated = $false
$clientA = $null
$clientB = $null

try {
    $inspectRaw = Invoke-Docker -Arguments @("image", "inspect", $ImageRef) -FailureCode "oci_image_invalid"
    $inspectItems = @($inspectRaw.Stdout | ConvertFrom-Json)
    if ($inspectItems.Count -ne 1) { Stop-Smoke "oci_image_invalid" }
    $inspect = $inspectItems[0]
    if ($inspect.Os -ne "linux" -or $inspect.Architecture -ne "amd64" -or
        $inspect.Config.User -ne "10001:10001" -or $null -ne $inspect.Config.Volumes) {
        Stop-Smoke "oci_image_invalid"
    }
    $requiredEnvironment = @(
        "PROJECTB_PROFILE=demo",
        "PROJECTB_PROVIDER_ADAPTER=deterministic.mock",
        "PROJECTB_EGRESS_POLICY=deny",
        "PROJECTB_DATA_ROOT=/tmp/projectb-demo",
        "PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring"
    )
    foreach ($item in $requiredEnvironment) {
        if ($item -notin @($inspect.Config.Env)) { Stop-Smoke "oci_image_invalid" }
    }
    if ($inspect.Config.Labels.'org.opencontainers.image.revision' -ne $ExpectedSourceCommit -or
        $inspect.Config.Labels.'io.projectb.profile' -ne "demo" -or
        $inspect.Config.Labels.'io.projectb.network-policy' -ne "deny-egress" -or
        $null -eq $inspect.Config.Healthcheck -or
        (@($inspect.Config.Healthcheck.Test) -join " ") -notmatch '/api/health') {
        Stop-Smoke "oci_image_invalid"
    }

    $history = Invoke-Docker -Arguments @(
        "history", "--no-trunc", "--format", "{{json .CreatedBy}}", $ImageRef
    ) -FailureCode "oci_history_rejected"
    if ($history.Stdout -match '(?i)(requirements-windows-x64|api.?key\s*=|token\s*=|password\s*=|credential\s*=|pip install -r)') {
        Stop-Smoke "oci_history_rejected"
    }

    Invoke-Docker -Arguments @("create", "--name", $inspectContainer, $ImageRef) `
        -FailureCode "oci_sbom_invalid" | Out-Null
    $sbomPath = Join-Path $SbomOutputDirectory "sbom.spdx.json"
    $profilePath = Join-Path $SbomOutputDirectory "profile.json"
    Invoke-Docker -Arguments @(
        "cp", "${inspectContainer}:/opt/projectb/licenses/sbom.spdx.json", $sbomPath
    ) -FailureCode "oci_sbom_invalid" | Out-Null
    Invoke-Docker -Arguments @(
        "cp", "${inspectContainer}:/opt/projectb/demo/profile.json", $profilePath
    ) -FailureCode "oci_sbom_invalid" | Out-Null
    Invoke-Docker -Arguments @("rm", $inspectContainer) -FailureCode "oci_cleanup_failed" | Out-Null
    $inspectContainer = $null

    $sbom = Get-Content -Raw -LiteralPath $sbomPath -Encoding UTF8 | ConvertFrom-Json
    $profile = Get-Content -Raw -LiteralPath $profilePath -Encoding UTF8 | ConvertFrom-Json
    if ($sbom.spdxVersion -ne "SPDX-2.3" -or $sbom.dataLicense -ne "CC0-1.0" -or
        @($sbom.packages).Count -lt 1 -or
        (@($sbom.annotations).comment -join " ") -notmatch [regex]::Escape($ExpectedLinuxLockSha256) -or
        @($profile.fixtures).Count -ne 2 -or
        @($profile.fixtures | Where-Object { $_.license -ne "CC0-1.0" }).Count -ne 0) {
        Stop-Smoke "oci_sbom_invalid"
    }
    $sbomSha = (Get-FileHash -LiteralPath $sbomPath -Algorithm SHA256).Hash.ToLowerInvariant()

    Invoke-Docker -Arguments @("network", "create", "--internal", $networkName) `
        -FailureCode "oci_engine_failed" | Out-Null
    $networkCreated = $true
    $port = Get-FreeLoopbackPort
    $script:Origin = "http://127.0.0.1:$port"
    $runArgs = @(
        "run", "--detach", "--name", $runContainer,
        "--network", $networkName,
        "--read-only",
        "--tmpfs", "/tmp/projectb-demo:rw,noexec,nosuid,nodev,size=67108864,uid=10001,gid=10001,mode=0770",
        "--cap-drop", "ALL",
        "--security-opt", "no-new-privileges:true",
        "--pids-limit", "256",
        "--memory", "512m",
        "--cpus", "1.0",
        "--publish", "127.0.0.1:${port}:7860",
        $ImageRef
    )
    Invoke-Docker -Arguments $runArgs -FailureCode "oci_start_failed" | Out-Null
    $runStarted = $true

    $baseUri = [Uri]$script:Origin
    $healthUri = [Uri]::new($baseUri, "/api/health")
    $profileUri = [Uri]::new($baseUri, "/api/demo/profile")
    $resetUri = [Uri]::new($baseUri, "/api/demo/session/reset")
    $clientA = New-DemoClient
    $clientB = New-DemoClient

    $deadline = [Diagnostics.Stopwatch]::StartNew()
    $health = $null
    while ($deadline.Elapsed.TotalSeconds -lt $StartupTimeoutSeconds) {
        try {
            $health = Invoke-DemoJson -ClientState $clientA -Method ([Net.Http.HttpMethod]::Get) `
                -Uri $healthUri -Body $null -CsrfToken $null
            if ($health.Status -eq 200 -and $health.Json.status -eq "ok" -and
                $health.Json.profile -eq "demo" -and
                @($health.Json.psobject.Properties).Count -eq 2) { break }
        } catch { }
        Start-Sleep -Milliseconds 250
    }
    if ($null -eq $health -or $health.Status -ne 200 -or $health.Json.profile -ne "demo") {
        Stop-Smoke "oci_ready_timeout"
    }

    $profileA = Invoke-DemoJson -ClientState $clientA -Method ([Net.Http.HttpMethod]::Get) `
        -Uri $profileUri -Body $null -CsrfToken $null
    $profileB = Invoke-DemoJson -ClientState $clientB -Method ([Net.Http.HttpMethod]::Get) `
        -Uri $profileUri -Body $null -CsrfToken $null
    if ($profileA.Status -ne 200 -or $profileB.Status -ne 200 -or
        [string]::IsNullOrWhiteSpace($profileA.Csrf) -or
        [string]::IsNullOrWhiteSpace($profileB.Csrf) -or
        $profileA.Json.profileId -ne "demo" -or
        $profileA.Json.session.idleTtlSeconds -ne 1800 -or
        $profileA.Json.session.absoluteTtlSeconds -ne 7200 -or
        $profileA.Json.limits.activeCourses -ne 1 -or
        $profileA.Json.limits.materials -ne 20 -or
        $profileA.Json.limits.concurrentJobs -ne 2 -or
        $profileA.Json.limits.stateBytes -ne 67108864 -or
        $profileA.Json.limits.requestsPerIpPerMinute -ne 60 -or
        $profileA.Json.provider.adapterId -ne "deterministic.mock") {
        Stop-Smoke "oci_profile_failed"
    }
    $fingerprintA = Get-CookieFingerprint -ClientState $clientA -Uri $baseUri
    $fingerprintB = Get-CookieFingerprint -ClientState $clientB -Uri $baseUri
    if ($fingerprintA -eq $fingerprintB) { Stop-Smoke "oci_isolation_failed" }

    $resetA = Invoke-DemoJson -ClientState $clientA -Method ([Net.Http.HttpMethod]::Post) `
        -Uri $resetUri -Body @{} -CsrfToken $profileA.Csrf
    if ($resetA.Status -lt 200 -or $resetA.Status -ge 300) { Stop-Smoke "oci_isolation_failed" }
    $profileBAfter = Invoke-DemoJson -ClientState $clientB -Method ([Net.Http.HttpMethod]::Get) `
        -Uri $profileUri -Body $null -CsrfToken $null
    if ($profileBAfter.Status -ne 200 -or
        (Get-CookieFingerprint -ClientState $clientB -Uri $baseUri) -ne $fingerprintB) {
        Stop-Smoke "oci_isolation_failed"
    }

    $profileAAfter = Invoke-DemoJson -ClientState $clientA -Method ([Net.Http.HttpMethod]::Get) `
        -Uri $profileUri -Body $null -CsrfToken $null
    $forbidden = Invoke-DemoJson -ClientState $clientA -Method ([Net.Http.HttpMethod]::Post) `
        -Uri $resetUri -Body @{
            upload="forbidden"; path="forbidden"; url="https://invalid.example";
            credential="forbidden"; provider="production"
        } -CsrfToken $profileAAfter.Csrf
    if ($forbidden.Status -notin @(400, 403, 404, 422)) { Stop-Smoke "oci_capability_leak" }

    $runningInspectRaw = Invoke-Docker -Arguments @("container", "inspect", $runContainer) `
        -FailureCode "oci_image_invalid"
    $runningInspect = @($runningInspectRaw.Stdout | ConvertFrom-Json)[0]
    if (-not $runningInspect.HostConfig.ReadonlyRootfs -or
        $runningInspect.Config.User -ne "10001:10001" -or
        $runningInspect.HostConfig.Privileged -or
        @($runningInspect.Mounts | Where-Object { $_.Type -eq "volume" }).Count -ne 0 -or
        $runningInspect.HostConfig.NetworkMode -ne $networkName) {
        Stop-Smoke "oci_image_invalid"
    }

    Invoke-Docker -Arguments @("stop", "--time", "10", $runContainer) `
        -TimeoutSeconds 30 -FailureCode "oci_shutdown_timeout" | Out-Null
    Invoke-Docker -Arguments @("rm", $runContainer) -FailureCode "oci_cleanup_failed" | Out-Null
    $runStarted = $false
    $runContainer = $null
    Invoke-Docker -Arguments @("network", "rm", $networkName) `
        -FailureCode "oci_cleanup_failed" | Out-Null
    $networkCreated = $false
    $networkName = $null

    $record = [ordered]@{
        schemaVersion = 1
        task = "DIST-02"
        sourceCommit = $ExpectedSourceCommit
        image = [ordered]@{
            status = "pass"
            reference = $ImageRef
            id = [string]$inspect.Id
            os = "linux"
            architecture = "amd64"
            user = "10001:10001"
        }
        provenance = [ordered]@{
            nodeBaseDigest = "sha256:d45d78e7929b46875bbd4e29bea672d5bc48186c6c3588306521c815e78352d6"
            pythonBaseDigest = "sha256:f70215e5dbe2a47dee6d23f9c6d358bf3c148f59cce2fd165b61118e9d80f2bb"
            linuxLockSha256 = $ExpectedLinuxLockSha256
            sbomSha256 = $sbomSha
            sbomPackageCount = @($sbom.packages).Count
        }
        localSmoke = [ordered]@{
            status = "pass"
            health = "pass"
            profile = "pass"
            twoSessionIsolation = "pass"
            callerScopedReset = "pass"
            quotaContract = "not_executed"
            forbiddenCapabilitySchema = "pass"
            network = "not_executed"
            persistence = "read_only_root_plus_tmpfs_no_volume"
        }
        predecessorEvidence = [ordered]@{
            demo01c2Commit = $Demo01C2Commit
            dist01Commit = $Dist01Commit
            apiReg01Commit = $ApiReg01Commit
            qa01c2Commit = $Qa01C2Commit
            demoReg01Commit = $DemoReg01Commit
            g02c2Commit = $G02C2Commit
        }
        publicUrl = [ordered]@{ status = "not_executed" }
        deployment = [ordered]@{ status = "not_executed" }
        externalBrowser = [ordered]@{ status = "not_executed" }
        publication = [ordered]@{ status = "not_executed" }
    }
    Write-Evidence -Record $record
} finally {
    if ($null -ne $clientA) { $clientA.Client.Dispose(); $clientA.Handler.Dispose() }
    if ($null -ne $clientB) { $clientB.Client.Dispose(); $clientB.Handler.Dispose() }
    if ($null -ne $runContainer) {
        try { Invoke-Docker -Arguments @("rm", "--force", $runContainer) -FailureCode "oci_cleanup_failed" | Out-Null } catch { }
    }
    if ($null -ne $inspectContainer) {
        try { Invoke-Docker -Arguments @("rm", "--force", $inspectContainer) -FailureCode "oci_cleanup_failed" | Out-Null } catch { }
    }
    if ($null -ne $networkName) {
        try { Invoke-Docker -Arguments @("network", "rm", $networkName) -FailureCode "oci_cleanup_failed" | Out-Null } catch { }
    }
}
````

The script never receives a credential, provider URL, registry, host account, or public URL. `PROJECTB_DOCKER_EXE` is the only accepted Docker executable and is validated as an absolute, non-reparse `docker.exe` leaf before every bounded call. The detached container's health polling, HTTP smoke, graceful stop, and forced cleanup each have finite deadlines; a timeout kills the complete Docker client process tree and fails closed. Cookie fingerprints and CSRF values exist only in process memory and never enter output/evidence. The internal Docker network and Python audit hook are checked as configuration inputs only; `network` and `quotaContract` remain `not_executed` until DEMO-01C2 supplies executable probes. DEMO-01C2 remains the authority for simulated clock expiry, exact request-rate/concurrent-job exhaustion, and the complete fixture workflow; the local container smoke validates only the reviewed profile/session/reset/capability and container-hardening subset.

### D8. Create the honest pre-execution evidence record

Create `docs/engineering/DIST-02_EVIDENCE.md` before any build. It must remain in `not_executed` state until the local command in D11 actually succeeds:

````markdown
# DIST-02 Evidence

```json
{
  "schemaVersion": 1,
  "task": "DIST-02",
  "sourceCommit": "not_executed",
  "image": {
    "status": "not_executed",
    "reference": "not_executed",
    "id": "not_executed",
    "os": "linux",
    "architecture": "amd64",
    "user": "10001:10001"
  },
  "provenance": {
    "nodeBaseDigest": "sha256:d45d78e7929b46875bbd4e29bea672d5bc48186c6c3588306521c815e78352d6",
    "pythonBaseDigest": "sha256:f70215e5dbe2a47dee6d23f9c6d358bf3c148f59cce2fd165b61118e9d80f2bb",
    "linuxLockSha256": "not_executed",
    "sbomSha256": "not_executed",
    "sbomPackageCount": 0
  },
  "localSmoke": {
    "status": "not_executed",
    "health": "not_executed",
    "profile": "not_executed",
    "twoSessionIsolation": "not_executed",
    "callerScopedReset": "not_executed",
    "quotaContract": "not_executed",
    "forbiddenCapabilitySchema": "not_executed",
    "network": "not_executed",
    "persistence": "not_executed"
  },
  "predecessorEvidence": {
    "demo01c2Commit": "not_executed",
    "dist01Commit": "not_executed",
    "apiReg01Commit": "not_executed",
    "qa01c2Commit": "not_executed",
    "demoReg01Commit": "not_executed",
    "g02c2Commit": "not_executed"
  },
  "publicUrl": {
    "status": "not_executed"
  },
  "deployment": {
    "status": "not_executed"
  },
  "externalBrowser": {
    "status": "not_executed"
  },
  "publication": {
    "status": "not_executed"
  }
}
```
````

This record is not a simulated result. If Docker or a predecessor gate is unavailable, leave the appropriate field `not_executed`, add no PASS statement, and return the blocker to the coordinator. D7 overwrites only this fenced JSON after all local checks and cleanup succeed.

### D9. Run the focused green contract test

```powershell
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "-m", "pytest", "backend/tests/integration/test_oci_distribution_contract.py", "-q"
) -TimeoutSeconds 300 -FailureCode "dist02_contract_green_failed" | Out-Null
```

All assertions must pass without Docker or network access. If a test passes because it searches for a comment rather than an operative instruction, strengthen it before continuing. In particular, the test must inspect every `FROM`, the operative pip line, final `USER`, healthcheck, profile JSON, context exclusions, and parsed evidence state.

### D10. Build one local linux/amd64 image with an empty Docker client config

```powershell
$DockerExe = $env:PROJECTB_DOCKER_EXE
Assert-AbsoluteLeaf -Path $DockerExe -Label "Docker"
$dockerVersion = Invoke-CheckedNative -FilePath $DockerExe -ArgumentList @(
    "version", "--format", "{{.Client.Version}}"
) -TimeoutSeconds 60 -FailureCode "oci_engine_failed"
$shortCommit = $BaseCommit.Substring(0, 12)
$imageRef = "projectb-demo:dist02-$shortCommit"
$dockerTempRoot = [IO.Path]::GetFullPath($env:TEMP).TrimEnd('\')
$dockerConfig = Join-Path $dockerTempRoot ("projectb-docker-config-" + [guid]::NewGuid().ToString("N"))
if (-not [IO.Path]::GetFullPath($dockerConfig).StartsWith(
    $dockerTempRoot + '\', [StringComparison]::OrdinalIgnoreCase)) {
    throw "oci_docker_config_containment_failed"
}
[IO.Directory]::CreateDirectory($dockerConfig) | Out-Null
Set-PrivateAcl -Path $dockerConfig
$priorDockerConfig = $env:DOCKER_CONFIG
try {
    $env:DOCKER_CONFIG = $dockerConfig
    Invoke-CheckedNative -FilePath $DockerExe -ArgumentList @(
        "build",
        "--platform", "linux/amd64",
        "--file", "packaging/oci/Dockerfile",
        "--build-arg", "PROJECTB_SOURCE_COMMIT=$BaseCommit",
        "--tag", $imageRef,
        "--tag", "projectb-demo:local",
        "."
    ) -TimeoutSeconds 1800 -FailureCode "oci_build_failed" | Out-Null
} finally {
    $env:DOCKER_CONFIG = $priorDockerConfig
    if (Test-Path -LiteralPath $dockerConfig) {
        $resolvedDockerConfig = (Resolve-Path -LiteralPath $dockerConfig).Path
        if (-not $resolvedDockerConfig.StartsWith(
            $dockerTempRoot + '\', [StringComparison]::OrdinalIgnoreCase)) {
            throw "oci_docker_config_containment_failed"
        }
        Remove-Item -LiteralPath $resolvedDockerConfig -Recurse -Force
    }
}
```

This is the only build command. It uses the repository root as context, no secret/build credential/SSH mount, no registry login, no push, no provenance claim from a remote service, and no external host mutation. The empty client config prevents accidental use of saved registry credentials. Public anonymous pulls and dependency downloads are allowed only for the pinned image digests and lockfiles already reviewed by G-02A/G-02C2. If the image already exists, remove only that exact local tag after recording its ID or choose a new commit-derived tag; never prune global Docker state.

### D11. Run the local container smoke and capture fresh evidence

```powershell
$sbomTempRoot = [IO.Path]::GetFullPath($env:TEMP).TrimEnd('\')
$sbomOutput = Join-Path $sbomTempRoot ("projectb-dist02-sbom-" + [guid]::NewGuid().ToString("N"))
if (-not [IO.Path]::GetFullPath($sbomOutput).StartsWith(
    $sbomTempRoot + '\', [StringComparison]::OrdinalIgnoreCase)) {
    throw "oci_sbm_output_containment_failed"
}
$smokeResult = Invoke-CheckedNative -FilePath $PowerShellExe -ArgumentList @(
    "-NoLogo", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass",
    "-File", (Join-Path $WorktreeRoot "packaging/oci/smoke_test.ps1"),
    "-ImageRef", $imageRef,
    "-ExpectedSourceCommit", $BaseCommit,
    "-ExpectedLinuxLockSha256", $linuxLockSha,
    "-Demo01C2Commit", $env:PROJECTB_DEMO_01C2_COMMIT,
    "-Dist01Commit", $env:PROJECTB_DIST_01_COMMIT,
    "-Qa01C2Commit", $env:PROJECTB_QA_01C2_COMMIT,
    "-DemoReg01Commit", $env:PROJECTB_DEMO_REG_01_COMMIT,
    "-G02C2Commit", $env:PROJECTB_G02C2_COMMIT,
    "-EvidencePath", (Join-Path $WorktreeRoot "docs/engineering/DIST-02_EVIDENCE.md"),
    "-SbomOutputDirectory", $sbomOutput
) -TimeoutSeconds 600 -FailureCode "dist02_local_smoke_failed"
```

After the script succeeds, independently parse the updated fenced JSON, compare its image ID with `docker image inspect`, compare its SBOM hash with the copied file, and assert every external/public field remains `not_executed`. Resolve `$sbomOutput` again, verify it remains a direct child of `$sbomTempRoot`, and remove only that verified path. Keep the local image for CI-01A handoff unless the coordinator explicitly says the immutable image ID has been consumed; do not push it.

```powershell
if (Test-Path -LiteralPath $sbomOutput) {
    $resolvedSbomOutput = (Resolve-Path -LiteralPath $sbomOutput).Path
    if (-not $resolvedSbomOutput.StartsWith(
        $sbomTempRoot + '\', [StringComparison]::OrdinalIgnoreCase)) {
        throw "oci_sbm_output_containment_failed"
    }
    Remove-Item -LiteralPath $resolvedSbomOutput -Recurse -Force
}
```

The documented local launch for a reviewed local tag is the hardened one-command form below. The `tmpfs` is mandatory: a bare `docker run --rm --publish ... projectb-demo:local` would leave mutable demo state in the container layer and is not an accepted distribution command.

```powershell
docker run --rm `
    --publish 127.0.0.1:7860:7860 `
    --read-only `
    --tmpfs "/tmp/projectb-demo:rw,noexec,nosuid,nodev,size=67108864,uid=10001,gid=10001,mode=0770" `
    --cap-drop ALL `
    --security-opt no-new-privileges:true `
    --pids-limit 256 `
    --memory 512m `
    --cpus 1.0 `
    projectb-demo:local
```

The application still binds the container listener to port `7860` and the host exposes it only on `127.0.0.1`. The Python audit hook rejects non-loopback provider/network calls even when a user omits an internal Docker network; the smoke test adds an internal network for an independent engine-level check. Stop with `Ctrl+C`; no host directory or volume is mounted.

### D12. Run regressions, policy checks, and the worktree credential scan

```powershell
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "-m", "pytest", "backend/tests/integration/test_oci_distribution_contract.py", "-q"
) -TimeoutSeconds 300 -FailureCode "dist02_contract_regression_failed" | Out-Null
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "-m", "ruff", "check", "--config", "backend/pyproject.toml",
    "backend/tests/integration/test_oci_distribution_contract.py"
) -TimeoutSeconds 300 -FailureCode "dist02_ruff_failed" | Out-Null
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "-m", "mypy", "--config-file", "backend/pyproject.toml", "backend/src"
) -TimeoutSeconds 600 -FailureCode "dist02_mypy_failed" | Out-Null
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "-m", "pytest",
    "backend/tests/integration/test_demo_profile.py",
    "backend/tests/integration/test_demo_isolation.py",
    "backend/tests/integration/test_demo_quotas.py",
    "backend/tests/integration/test_demo_workflow.py", "-q"
) -TimeoutSeconds 900 -FailureCode "dist02_demo_regression_failed" | Out-Null
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "scripts/test_all.py", "--profile", "demo"
) -TimeoutSeconds 1800 -FailureCode "dist02_full_suite_failed" | Out-Null
Invoke-CheckedNative -FilePath $PythonExe -ArgumentList @(
    "scripts/scan_secrets.py", "--worktree", "--git-exe", $GitExe
) -TimeoutSeconds 300 -FailureCode "dist02_worktree_scanner_failed" | Out-Null
```

Also run a no-network source audit over the seven owned files and fail if it finds a Windows lock reference, floating `FROM`, URL `ADD`, registry hostname, deployment command, secret-shaped build argument, credential value, real provider identifier, `VOLUME`, root user, or writable persistent path. The implementation worker records exact command IDs, fresh UTC timestamps, and exit statuses in the private transcript; the tracked evidence receives only the redacted structured results already defined.

### D13. Stage only the seven-path DIST-02 unit and capture the review packet

```powershell
$dist02Paths = @(
    "packaging/oci/Dockerfile",
    "packaging/oci/entrypoint.sh",
    ".dockerignore",
    "packaging/oci/smoke_test.ps1",
    "backend/tests/integration/test_oci_distribution_contract.py",
    "docs/engineering/DIST-02_EVIDENCE.md",
    "demo/profile.json"
)
$packet = Get-ReviewPacket -ExpectedPaths $dist02Paths
```

The whole-index assertion rejects the separately owned `packaging/oci/requirements-linux-amd64.lock` if the DIST-02 worker stages it, as well as fixtures, application source, generated SBOMs, image archives, Docker configuration, or any other path. The packet includes the full binary staged diff, tree ID, SHA-256, exact root/detailed plan hashes, DIST-01/DEMO-01C2/QA-01C2/G-02C2 dependency hashes, Linux-lock owner/hash evidence, base-image digest evidence, and fresh command summary. It remains in a current-user ACL directory and never contains cookies, CSRF values, Docker client configuration, courseware, credentials, or raw logs.

### D14. Obtain a fresh specification-compliance review

The fresh reviewer checks the immutable packet against `SPEC.md`, root DIST-02, AC-07, AC-10, AC-41, AC-47, confirmed SPEC section 4.5 demo limits, the frozen contracts here, and every named predecessor receipt. Its findings-first report explicitly checks:

- exact one-command local build/run interface and linux/amd64 provenance;
- deterministic mock, licensed synthetic fixtures, two isolated callers, caller-scoped reset, TTL/quota contract binding, and full fixture workflow binding;
- no upload/path/URL/credential/production-provider/public-data persistence capability;
- non-root, read-only root, 64 MiB tmpfs, no Docker volume, internal network, and audit-hook egress denial;
- exact Linux-only hash-locked dependency installation and zero Windows-lock use;
- honest local-only evidence with public URL, deployment, external-browser, and publication all `not_executed`.

The reviewer must return a blocking finding if DEMO-01C2 has not supplied a reviewed executable live-container workflow contract for expiry, job/material/request quotas, and the complete import-to-post-exam flow. The current structural/profile/session smoke is not evidence of that full flow. Resolve the gap in the predecessor owner, amend this plan/script to consume the reviewed interface, regenerate the packet, and repeat both reviews; never turn the predecessor label into an inferred PASS.

### D15. Obtain a distinct fresh quality/security/license review

The second fresh reviewer checks Dockerfile syntax/build-stage determinism, digest architecture, Linux-lock wheel compatibility, final filesystem, entrypoint ordering, numeric user, tmpfs permissions, healthcheck, Host/Origin/CSRF behavior, audit-hook coverage, internal-network cleanup, resource limits, two-client test strength, timeout/process-tree handling, Docker-output bounds, `.dockerignore` order, image-history scanning, SPDX 2.3 validity, Debian/Python notices, fixture CC0 provenance, absence of a false project-license claim, and exact cleanup scope. It also checks that no token/cookie/hash preimage or raw host path can reach evidence and that no local error triggers global image/container/network pruning. The reviewer identity must differ from the SPEC reviewer and worker.

Both private receipts use the exact schema consumed by `Read-ReviewReceipt`; any edit or evidence rerun changes the staged tree and invalidates both receipts.

### D16. Commit exactly the twice-reviewed DIST-02 tree

```powershell
$dist02Commit = Complete-ReviewedUnit -ExpectedPaths $dist02Paths `
    -Packet $packet -CommitMessage "build(DIST-02): add isolated OCI demo preflight"
if ((Invoke-CheckedGit -Arguments @("rev-parse", "HEAD^{tree}")).Stdout.Trim() -ne
    $packet.TreeId) {
    throw "dist02 committed tree mismatch"
}
```

The coordinator records the returned hash, review receipts, immutable image ID, and local evidence after consuming the reviewed commit. This worker does not edit root `PLAN.md`, `AGENT_LOG.md`, CI files, deployment evidence, or README; those remain separate owner tasks. It does not push a branch/image, create a PR, create a hosting account, deploy, publish, or open an external URL.

### DIST-02 Completion Standard

DIST-02 is complete only when D1-D16 are checked; the coordinator-owned Node digest and separate Linux lock owner/hash are reviewed; the DEMO/T-04 CSRF transport and DEMO-01C2 executable live-container workflow contract are reconciled; one fresh local build and smoke pass for the same image ID; SBOM/license/context/history checks pass; both fresh reviewers approve the identical staged tree; and the committed tree equals that tree. `publicUrl`, `deployment`, `externalBrowser`, and `publication` remain `not_executed`. G-02C2/D-025 and DEPLOY-01 remain later gates and cannot be represented as completed by this plan.

## Coordinator Handoff and Current Dispatchability

This detailed plan is bound to root `PLAN.md` SHA-256 `4BCFE8470DE57C0DD54004935285CAAD5CD9D1AFF0AA7370CC4E098887745F08` and the authoring contract SHA-256 `506A1E179B8B6BE8705BB9C5D7161452C16FD2F760AC4BCD1797CE58185E6CFC`. It is not dispatchable merely because the prose exists. Before cross-plan review can return PASS, the coordinator must:

1. Review and record terminal predecessor hashes/interfaces for both units.
2. Amend root/G-02A with a named owner and SHA-256 for `packaging/oci/requirements-linux-amd64.lock`; DIST-02 consumes it read-only and never stages it.
3. Promote the verified linux/amd64 Node builder digest into coordinator-owned dependency evidence.
4. Reconcile the final `create_app(profile="demo")` port/security configuration and the HTTP CSRF-proof transport without weakening Host/Origin/CSRF policy.
5. Bind DEMO-01C2's exact executable live-container workflow to the OCI smoke so expiry, quotas, isolation, reset, and the full fixture flow are observed rather than inferred.
6. Recompute the root-plan hash after every amendment, update this prelude/hash binding, and run fresh SPEC plus quality/security/license plan reviews over the resulting immutable plan set.

Until all six items are satisfied, DIST-01 may be evaluated independently once its own predecessors exist, but DIST-02 and the overall Windows/OCI distribution plan remain blocked for dispatch. This is an authoring-stage blocker only; no production file, container, external service, or release has been created by writing this plan.
