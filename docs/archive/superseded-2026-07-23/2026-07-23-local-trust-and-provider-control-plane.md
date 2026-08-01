# Local Trust and Provider Control Plane Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (- [ ]) syntax for tracking.

**Goal:** Build the fail-closed local request boundary, strict provider-profile and Windows Credential Manager lifecycle, immutable L/P/F consent policy, and one provider-neutral deterministic test/demo adapter contract for T-04A, T-04B, T-04C, T-05A, T-05B, T-05C, T-06, and T-07.

**Architecture:** T-04A/B establish one pure security module; T-04C installs it once in FastAPI and sends whitelist-only audit events. T-05A validates non-secret provider configuration before any adapter or store access; T-05B is the only production secret-store boundary; T-05C coordinates hidden credential lifecycle and forced-clear state without persisting values. T-06 binds every remote-capable operation to immutable consent/policy/capability snapshots and a canonical scope token. T-07 defines the one provider-neutral envelope and registry, with deterministic mock registration restricted to test/demo; no production adapter or network call is implemented here.

**Tech Stack:** CPython 3.14.6, FastAPI 0.139.2, Pydantic 2.13.4 where consumed through the reviewed foundation, pytest 9.1.1, Ruff 0.15.22, mypy 2.3.0, keyring 25.7.0 with WinVaultKeyring, and Python standard-library dataclasses, hashlib, hmac, secrets, json, decimal, and typing.

---

## Status And Dispatch Boundary

This is the formal detailed plan for exactly T-04A, T-04B, T-04C, T-05A, T-05B, T-05C, T-06, and T-07. It is planning input only: no implementation, test, scanner, review, commit, provider call, credential access, or human gate is claimed as executed.

Dispatch remains blocked until the root implementation gates are satisfied: G-01, G-02A, G-03 cold-start validation, explicit student implementation approval, and G-04 worktree creation. This file neither observes nor infers those gates, remote CI, deployment, account capability, or live provider behavior.

This revision supersedes the failed P02 snapshot SHA-256 2369DE2D92F0E4AB2B4A3C3BCBAC3F0F104D830787344B1CB224E72AF4095353. The root planning snapshot used for authoring is PLAN.md SHA-256 4BCFE8470DE57C0DD54004935285CAAD5CD9D1AFF0AA7370CC4E098887745F08. The exact reviewed domain-plan snapshot is 40C48BB62A87F17BFCFB635871F51C350EA2EC9F1AAFEE5ED2D9B7A7C7629C0B. Foundation and persistence are actively being repaired and have no reviewable terminal hashes for this handoff yet; final cross-plan PASS and every implementation dispatch remain blocked until the coordinator supplies their observed reviewed hashes. Any root, foundation, persistence, domain, or public-interface change requires this plan to rebind to the new hashes and repeat both independent reviews.

**G-04 schema-amendment blocker:** The current root G-04 contract describes a human-readable `WORKTREE_MAP.md` table but does not publish an immutable machine-readable dispatch row or a validator for it. This plan therefore remains `G04_SCHEMA_AMENDMENT_REQUIRED` and is not dispatchable. Root G-04 must first be amended, reviewed, and committed to publish `docs/engineering/WORKTREE_MAP.v2.json` with the exact v2 schema consumed below and to validate each row before worktree creation. The amendment must define the row's `base_commit` as the reviewed implementation-content ancestor while the commit containing the row is the unit's dispatch HEAD/BaseCommit; this two-commit meaning avoids an impossible self-referential Git hash. After that root change, this plan must be rebound to the new observed root/foundation/persistence/domain hashes and reviewed again. No worker may replace the absent row, plan hashes, dependency hashes, owner, or path with caller-supplied environment values.

## Dependency And Integration Order

~~~text
T-01F3 + T-03C
      |
     T-04A -> T-04B -> T-04C
                       |
             T-03C + T-04C + G-02A
                       |
                      T-05A -> T-05B -> T-05C
                                           |
                             T-02C + T-03C + T-05C
                                           |
                                          T-06 -> T-07
~~~

- T-04A creates application/security.py after reviewed T-01F3 and T-03C.
- T-04B modifies only the reviewed T-04A security module. T-04C follows T-04B and is this plan's only app.py owner.
- T-05A follows T-04C/T-03C/G-02A; T-05B follows T-05A; T-05C follows T-05B and consumes T-03C repository protocols.
- T-06 creates consent.py and consumes T-04 security. It does not stage security.py. A discovered security change returns to the T-04 owner for a separately reviewed serial commit.
- T-07 follows T-05C/T-06 and defines the shared adapter contract. X2 and M2 must consume it rather than invent another envelope.
- Workers never edit PLAN.md, SPEC.md, SPEC_PROCESS.md, AGENT_LOG.md, migrations, or predecessor files outside the exact unit set.

## Exact Path Ownership And Handoffs

| Unit | Exact owned paths | Count |
| --- | --- | ---: |
| T-04A | backend/src/projectb/application/security.py; backend/tests/integration/test_http_origin_policy.py | 2 |
| T-04B | backend/src/projectb/application/security.py; backend/tests/unit/test_csrf_tokens.py | 2 |
| T-04C | backend/src/projectb/api/middleware.py; backend/src/projectb/infrastructure/audit.py; backend/src/projectb/api/app.py; backend/tests/integration/test_http_security.py | 4 |
| T-05A | backend/src/projectb/domain/provider.py; backend/tests/unit/test_provider_profile.py | 2 |
| T-05B | backend/src/projectb/infrastructure/keyring_store.py; backend/tests/integration/test_win_vault_store.py | 2 |
| T-05C | backend/src/projectb/application/credentials.py; backend/tests/unit/test_credentials.py; backend/tests/integration/test_credential_boundary.py | 3 |
| T-06 | backend/src/projectb/application/consent.py; backend/tests/unit/test_consent_scope.py; backend/tests/integration/test_no_consent_egress.py | 3 |
| T-07 | backend/src/projectb/infrastructure/providers/base.py; backend/src/projectb/infrastructure/providers/mock.py; backend/src/projectb/application/provider.py; backend/tests/contract/test_provider_contract.py; backend/tests/contract/test_mock_scenarios.py | 5 |

The deliberate repeated handoff is application/security.py from T-04A to T-04B. app.py is handed from T-01B to T-04C and next to API-REG-01. T-06's root security reference is a consumed interface, not worker ownership. Each commit compares the whole index with its literal expected set.

## Frozen Public Contracts

### Request security and audit

- Worker/reviewer identities match `^[A-Za-z0-9][A-Za-z0-9._-]{1,63}$` and are pairwise distinct.
- `SecurityCode` includes `bind_non_loopback`, `bind_mismatch`, `server_metadata_missing`, `host_untrusted`, `origin_missing`, `origin_untrusted`, `csrf_missing`, `csrf_invalid`, `csrf_expired`, `csrf_replay`, `session_invalid`, `audit_field_forbidden`, `audit_value_forbidden`, and `request_failed`. `SecurityError` exposes only the stable code.
- `RequestMetadata(server_host, server_port, host_header, origin_header, method)` is the pure input to `TrustedRequestPolicy.check`. Missing ASGI `scope["server"]` metadata is rejected. The observed server host and port must equal the configured canonical bind exactly; another loopback address is not equivalent. Host and Origin must equal the configured canonical values. The policy never trusts forwarded headers, wildcard CORS, `null`, comma lists, user-info URLs, trailing-dot aliases, or alternate ports.
- `CsrfService.issue(session_id)` returns one 256-bit URL-safe token. `verify` consumes the token once, compares a digest in constant time, and rejects missing, mismatched, expired, replayed, malformed, or unknown sessions.
- `AuditWriter.record` accepts only fixed event kinds and deep-immutable, recursively bounded scalar/tuple metadata. It rejects paths, bodies, answers, prompts, credentials, arbitrary keys, secret-shaped values, oversized strings, oversized sequences, and unbounded counts before the sink. Successful mutating routes and explicitly marked provider actions are recorded; sanitized route exceptions become a generic `request_failed` response and never escape raw `call_next` text.

### Provider profiles and credentials

- `ProviderProfile` has exactly `profile_id`, `adapter_id`, `model_id`, `region`, `max_output_tokens`, `timeout_ms`, `daily_budget_usd`, `credential_ref`, and `schema_version`. `adapter_id` is `openai.reference`; `credential_ref` matches `cred_[A-Za-z0-9][A-Za-z0-9._-]{7,62}`.
- Strict parsing validates key names, Unicode/control characters, field types, lengths, integer/Decimal bounds, and scale before canonicalization. It rejects unknown fields; `api_key`/`token`/`password`/`secret`/`private_key`; `base_url`/`endpoint`/`plugin`/`module`/`callable`/dynamic adapter; wrong types; and coercion. Invalid data never reaches a store or adapter.
- Config fingerprint is lowercase SHA-256 over canonical bounded non-secret fields and excludes credential values and `credential_ref`.
- `SecretStore` has `set`, `status`, `clear`, and `resolve`. Only `resolve` returns a short-lived `SecretHandle`. Production construction verifies the actual `WinVaultKeyring` backend object identity and has no `.env` fallback. Backend causes are suppressed with `from None` and tests assert secret-bearing exceptions cannot appear in public errors.
- `CredentialService` persists lifecycle state through an injected authoritative repository. Forced clear records the exact profile plus reconciliation object/version in `delete_incomplete`, blocks new resolve after restart, and never auto-resumes when a new credential is configured. Recovery is one repository transaction/CAS that compares lifecycle generation and persisted evidence profile/object/object-version/evidence-version, then atomically marks the remote object resumable and writes lifecycle `ready`; failure commits neither side. There is no volatile resume callback or split ordering. Switching profile/mock or supplying cross-profile/stale-version evidence is rejected.

### Consent and provider-neutral ports

- A course has an explicit persisted `ProcessingPolicySelection` with mode `L`, `P`, or `F`. `None` is `UNSELECTED`; absence is never interpreted as `L`. An empty `L` consent is invalid and cannot authorize parsing. Local parsing requires an explicit current policy selection and exact material identity.
- `ConsentRecord` stores only opaque IDs, roles, hashes, mode, non-body payload scope, profile/config/capability/policy IDs, purpose, budget, timestamps, and revocation. Only `P`/`F` consent may be created, and both require non-empty exact payload scope.
- `scope_token` is lowercase SHA-256 of `course_id | material_id | content_hash | consent_record_id | config_fingerprint`. File/hash/mode/profile/config/capability/policy/purpose/budget changes invalidate old consent before adapter resolution.
- `PolicySnapshot` records Responses `store:false`, 30-day abuse monitoring, 24-hour prompt cache, file/image review exception, Files and Vector Stores retention until delete/expiry, training-use posture, processing region, deletion result semantics, expiry facts, and the disclosed provider removal window. Unknown policy facts fail closed for `P`/`F`.
- The five ports are `propose_concept_coverage`, `generate_explanation`, `generate_practice_candidate`, `analyze_exam_material`, and `generate_feedback`. Non-candidate states have empty authoritative content.
- `ProviderAdapterRegistry` is anchored to the coordinator-reviewed built-in manifest object and one reviewed factory identity. Duplicate manifest entries, duplicate registrations, caller-supplied adapter/profile claims, and local mock registration fail closed. Mock registration is explicit and limited to test/demo.
- `ProviderRequestEnvelope` carries a strict port-specific payload schema/version, immutable consent/scope proof, bounded task ID, input/output token limits, timeout, Decimal budget, idempotency key, cancellation token, profile/config/capability/policy snapshot IDs, and no caller-controlled adapter claim. `ProviderResponseEnvelope` carries a strict response schema/version, bounded usage/cost, cancellation/status, and candidate-only content; raw provider errors never cross the boundary.
- `DeterministicMock` covers success, low confidence, source_insufficient, bad_schema, timeout, rate_limit, cancelled, prompt_injection, duplicate_response, and wording_only. Same seed/idempotency key gives the same canonical domain fields.

## Fail-Closed Runtime Prelude

Every task executes this complete prelude in its own worktree before its first command. No task invokes a bare executable.

~~~powershell
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$PythonExe = $env:PROJECTB_PYTHON_EXE
$PowerShellExe = $env:PROJECTB_POWERSHELL_EXE
$GitExe = $env:PROJECTB_GIT_EXE
$WorktreeRoot = $env:PROJECTB_WORKTREE_ROOT
$UnitId = $env:PROJECTB_UNIT_ID
$BaseCommit = $env:PROJECTB_BASE_COMMIT
$AgentId = $env:PROJECTB_AGENT_ID
$RootPlanSha = $env:PROJECTB_ROOT_PLAN_SHA256
$DetailedPlanSha = $env:PROJECTB_DETAILED_PLAN_SHA256
$G04MapPath = "docs/engineering/WORKTREE_MAP.v2.json"
$DetailedPlanPath = "docs/superpowers/plans/2026-07-23-local-trust-and-provider-control-plane.md"
$DomainPlanPath = "docs/superpowers/plans/2026-07-22-domain-primitives-source.md"
$ExpectedRootPlanSha = "4BCFE8470DE57C0DD54004935285CAAD5CD9D1AFF0AA7370CC4E098887745F08"
$ExpectedDomainPlanSha = "40C48BB62A87F17BFCFB635871F51C350EA2EC9F1AAFEE5ED2D9B7A7C7629C0B"
if ([string]::IsNullOrWhiteSpace($WorktreeRoot) -or
    -not [IO.Path]::IsPathFullyQualified($WorktreeRoot) -or
    -not (Test-Path -LiteralPath $WorktreeRoot -PathType Container)) {
    throw "invalid worktree root"
}
if ($UnitId -notmatch "^(T-04A|T-04B|T-04C|T-05A|T-05B|T-05C|T-06|T-07)$") {
    throw "unexpected unit id"
}
if ($BaseCommit -notmatch "^[0-9a-f]{40}$" -or
    $RootPlanSha -notmatch "^[0-9A-F]{64}$" -or
    $DetailedPlanSha -notmatch "^[0-9A-F]{64}$") {
    throw "missing immutable snapshot binding"
}
function Assert-AbsoluteLeaf {
    param([Parameter(Mandatory)][string]$Path,[Parameter(Mandatory)][string]$Name)
    if (-not [IO.Path]::IsPathFullyQualified($Path) -or
        -not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        throw "$Name is not an absolute existing leaf"
    }
}
Assert-AbsoluteLeaf -Path $PythonExe -Name "python"
Assert-AbsoluteLeaf -Path $PowerShellExe -Name "powershell"
Assert-AbsoluteLeaf -Path $GitExe -Name "git"
if ([IO.Path]::GetFileName($GitExe).ToLowerInvariant() -ne "git.exe") {
    throw "git leaf is not approved"
}
if ($AgentId -notmatch "^[A-Za-z0-9][A-Za-z0-9._-]{1,63}$") {
    throw "invalid worker identity"
}
function Set-SafeChildEnvironment {
    param([Parameter(Mandatory)][Diagnostics.ProcessStartInfo]$StartInfo)
    $windows = [Environment]::GetFolderPath([Environment+SpecialFolder]::Windows)
    $temp = [IO.Path]::GetTempPath().TrimEnd([IO.Path]::DirectorySeparatorChar)
    if (-not [IO.Path]::IsPathFullyQualified($windows) -or
        -not (Test-Path -LiteralPath $windows -PathType Container) -or
        -not [IO.Path]::IsPathFullyQualified($temp) -or
        -not (Test-Path -LiteralPath $temp -PathType Container)) {
        throw "safe child environment roots unavailable"
    }
    $safe = [ordered]@{
        SYSTEMROOT=$windows
        WINDIR=$windows
        TEMP=$temp
        TMP=$temp
        PYTHONUTF8="1"
        PYTHONIOENCODING="utf-8"
        PYTHONDONTWRITEBYTECODE="1"
        NO_COLOR="1"
        GIT_TERMINAL_PROMPT="0"
        POWERSHELL_TELEMETRY_OPTOUT="1"
    }
    $StartInfo.EnvironmentVariables.Clear()
    foreach ($entry in $safe.GetEnumerator()) {
        $StartInfo.EnvironmentVariables.Add([string]$entry.Key,[string]$entry.Value)
    }
}
function Stop-NativeProcessTree {
    param([Parameter(Mandatory)][int]$ProcessId)
    $children = @(
        Get-CimInstance -ClassName Win32_Process -Filter "ParentProcessId=$ProcessId" -ErrorAction SilentlyContinue
    )
    foreach ($child in $children) {
        Stop-NativeProcessTree -ProcessId ([int]$child.ProcessId)
    }
    try {
        Stop-Process -Id $ProcessId -Force -ErrorAction Stop
    } catch {
        throw "bounded native process-tree cleanup failed"
    }
}
function ConvertTo-RedactedDiagnostic {
    param(
        [AllowEmptyString()][string]$Text,
        [ValidateRange(1,4194304)][int]$MaximumCharacters = 4096
    )
    $value = $Text.Replace($WorktreeRoot,"[WORKTREE]")
    $value = $value -replace "(?i)sk-(?:proj-)?[A-Za-z0-9_-]{12,}","[REDACTED]"
    $value = $value -replace "(?i)(api[_-]?key|token|password|secret|private[_-]?key)\s*[:=]\s*\S+","$1=[REDACTED]"
    $value = $value -replace "(?i)[A-Z]:\\Users\\[^\\\s]+","[USER_HOME]"
    $value = $value -replace "[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]","[CONTROL]"
    if ($value.Length -gt $MaximumCharacters) {
        $value = $value.Substring(0,$MaximumCharacters) + "[TRUNCATED]"
    }
    return $value
}
function Invoke-BoundedNative {
    param(
        [Parameter(Mandatory)][string]$FilePath,
        [string[]]$ArgumentList = @(),
        [ValidateRange(1,900)][int]$TimeoutSeconds = 300,
        [ValidateRange(1,4194304)][int]$MaximumOutputCharacters = 4096
    )
    Assert-AbsoluteLeaf -Path $FilePath -Name "native executable"
    $payload = @{ filePath=$FilePath; arguments=@($ArgumentList); root=$WorktreeRoot } |
        ConvertTo-Json -Compress -Depth 4
    $payload64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($payload))
    $child = @'
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$json = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String("__PAYLOAD__"))
$data = $json | ConvertFrom-Json
Set-Location -LiteralPath ([string]$data.root)
$arguments = @($data.arguments | ForEach-Object { [string]$_ })
& ([string]$data.filePath) @arguments
$code = $LASTEXITCODE
exit $code
'@.Replace("__PAYLOAD__",$payload64)
    $encoded = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($child))
    $start = New-Object Diagnostics.ProcessStartInfo
    $start.FileName = $PowerShellExe
    $start.Arguments = "-NoProfile -NonInteractive -EncodedCommand $encoded"
    $start.UseShellExecute = $false
    $start.CreateNoWindow = $true
    $start.RedirectStandardOutput = $true
    $start.RedirectStandardError = $true
    Set-SafeChildEnvironment -StartInfo $start
    $process = New-Object Diagnostics.Process
    $process.StartInfo = $start
    $stdout = ""
    $stderr = ""
    $exitCode = -1
    try {
        if (-not $process.Start()) { throw "native launch failed" }
        $stdoutTask = $process.StandardOutput.ReadToEndAsync()
        $stderrTask = $process.StandardError.ReadToEndAsync()
        if (-not $process.WaitForExit($TimeoutSeconds * 1000)) {
            Stop-NativeProcessTree -ProcessId $process.Id
            throw "native command timed out"
        }
        $stdout = ConvertTo-RedactedDiagnostic $stdoutTask.GetAwaiter().GetResult() $MaximumOutputCharacters
        $stderr = ConvertTo-RedactedDiagnostic $stderrTask.GetAwaiter().GetResult() $MaximumOutputCharacters
        $exitCode = $process.ExitCode
    } finally {
        $process.Dispose()
    }
    return [pscustomobject]@{ExitCode=$exitCode;Stdout=$stdout;Stderr=$stderr}
}
function Assert-SafeNativeProtocol {
    $secretName = "PROJECTB_SYNTHETIC_INHERITED_SECRET"
    $cloudName = "AWS_SECRET_ACCESS_KEY"
    $synthetic = "[REDACTED_FAKE_TEST_TOKEN]"
    $oldSecret = [Environment]::GetEnvironmentVariable($secretName,"Process")
    $oldCloud = [Environment]::GetEnvironmentVariable($cloudName,"Process")
    try {
        [Environment]::SetEnvironmentVariable($secretName,$synthetic,"Process")
        [Environment]::SetEnvironmentVariable($cloudName,$synthetic,"Process")
        $environmentProbe = @'
if ((Test-Path Env:PROJECTB_SYNTHETIC_INHERITED_SECRET) -or
    (Test-Path Env:AWS_SECRET_ACCESS_KEY)) { exit 91 }
[Console]::Out.Write("ENV_BLOCKED")
'@
        $environment = Invoke-BoundedNative $PowerShellExe @(
            "-NoProfile","-NonInteractive","-Command",$environmentProbe
        ) 10
        if ($environment.ExitCode -ne 0 -or $environment.Stdout -ne "ENV_BLOCKED") {
            throw "child inherited a non-allowlisted environment value"
        }
        $failureProbe = '[Console]::Error.Write("[REDACTED_FAKE_TEST_TOKEN]"); exit 23'
        $failure = Invoke-BoundedNative $PowerShellExe @(
            "-NoProfile","-NonInteractive","-Command",$failureProbe
        ) 10
        if ($failure.ExitCode -ne 23 -or
            $failure.Stderr -notmatch "\[REDACTED\]" -or
            $failure.Stderr -match "SYNTHETICONLY") {
            throw "nonzero diagnostics are not bounded and redacted"
        }
        $malformedProbe = '[Console]::Out.Write("left"+[char]0+"right")'
        $malformed = Invoke-BoundedNative $PowerShellExe @(
            "-NoProfile","-NonInteractive","-Command",$malformedProbe
        ) 10
        if ($malformed.ExitCode -ne 0 -or $malformed.Stdout -ne "left[CONTROL]right") {
            throw "malformed child output was not normalized"
        }
        $timedOut = $false
        try {
            Invoke-BoundedNative $PowerShellExe @(
                "-NoProfile","-NonInteractive","-Command","Start-Sleep -Seconds 30"
            ) 1 | Out-Null
        } catch {
            if ($_.Exception.Message -ne "native command timed out") { throw }
            $timedOut = $true
        }
        if (-not $timedOut) { throw "timeout protocol did not fail closed" }
    } finally {
        [Environment]::SetEnvironmentVariable($secretName,$oldSecret,"Process")
        [Environment]::SetEnvironmentVariable($cloudName,$oldCloud,"Process")
    }
}
function Invoke-CheckedNative {
    param(
        [Parameter(Mandatory)][string]$FilePath,
        [string[]]$ArgumentList = @(),
        [ValidateRange(1,900)][int]$TimeoutSeconds = 300,
        [string]$FailureMessage = "native command failed"
    )
    $result = Invoke-BoundedNative -FilePath $FilePath -ArgumentList $ArgumentList -TimeoutSeconds $TimeoutSeconds
    if ($result.ExitCode -ne 0) { throw "$FailureMessage exit=$($result.ExitCode)" }
    return $result
}
function Invoke-CheckedGit {
    param([Parameter(Mandatory)][string[]]$ArgumentList,[string]$FailureMessage="git command failed")
    return Invoke-CheckedNative -FilePath $GitExe -ArgumentList $ArgumentList -TimeoutSeconds 120 -FailureMessage $FailureMessage
}
function Invoke-CheckedPython {
    param([Parameter(Mandatory)][string[]]$ArgumentList,[int]$TimeoutSeconds=900)
    return Invoke-CheckedNative -FilePath $PythonExe -ArgumentList $ArgumentList -TimeoutSeconds $TimeoutSeconds -FailureMessage "python command failed"
}
function Get-GitBlobBytes {
    param(
        [Parameter(Mandatory)][string]$Commit,
        [Parameter(Mandatory)][string]$Path,
        [ValidateRange(1,4194304)][int]$MaximumBytes = 1048576
    )
    if ($Commit -notmatch "^[0-9a-f]{40}$" -or $Path -notmatch "^[A-Za-z0-9._/-]+$") {
        throw "invalid immutable blob selector"
    }
    $start = New-Object Diagnostics.ProcessStartInfo
    $start.FileName = $GitExe
    # This is the byte-preserving equivalent of `git show BaseCommit:<path>`.
    $start.Arguments = "show --format= --no-ext-diff --no-textconv $Commit`:$Path"
    $start.UseShellExecute = $false
    $start.CreateNoWindow = $true
    $start.RedirectStandardOutput = $true
    $start.RedirectStandardError = $true
    Set-SafeChildEnvironment -StartInfo $start
    $process = New-Object Diagnostics.Process
    $process.StartInfo = $start
    $bytes = New-Object IO.MemoryStream
    try {
        if (-not $process.Start()) { throw "immutable blob launch failed" }
        $copyTask = $process.StandardOutput.BaseStream.CopyToAsync($bytes)
        $errorTask = $process.StandardError.ReadToEndAsync()
        if (-not $process.WaitForExit(120000)) {
            Stop-NativeProcessTree -ProcessId $process.Id
            throw "immutable blob timed out"
        }
        $copyTask.GetAwaiter().GetResult()
        $errorText = ConvertTo-RedactedDiagnostic $errorTask.GetAwaiter().GetResult() 4096
        if ($process.ExitCode -ne 0) { throw "immutable blob read failed $errorText" }
        if ($bytes.Length -gt $MaximumBytes) { throw "immutable blob exceeds bound" }
        return ,$bytes.ToArray()
    } finally {
        $bytes.Dispose()
        $process.Dispose()
    }
}
function Get-GitBlobSha256 {
    param([Parameter(Mandatory)][string]$Commit,[Parameter(Mandatory)][string]$Path)
    $bytes = Get-GitBlobBytes -Commit $Commit -Path $Path
    return ([BitConverter]::ToString([Security.Cryptography.SHA256]::HashData($bytes))).Replace("-","").ToUpperInvariant()
}
function Get-GitBlobText {
    param([Parameter(Mandatory)][string]$Commit,[Parameter(Mandatory)][string]$Path)
    $bytes = Get-GitBlobBytes -Commit $Commit -Path $Path
    try {
        return [Text.UTF8Encoding]::new($false,$true).GetString($bytes)
    } catch {
        throw "immutable blob is not strict UTF-8"
    }
}
function Assert-ExactStagedPaths {
    param([Parameter(Mandatory)][string[]]$ExpectedPaths)
    $result = Invoke-CheckedGit -ArgumentList @("diff","--cached","--name-only")
    $actual = @($result.Stdout -split "\r?\n" | Where-Object { $_ } |
        ForEach-Object { $_ -replace "\\","/" } | Sort-Object)
    $expected = @($ExpectedPaths | ForEach-Object { $_ -replace "\\","/" } | Sort-Object)
    if ($actual.Count -ne $expected.Count -or
        (@(Compare-Object -ReferenceObject $expected -DifferenceObject $actual)).Count -ne 0) {
        throw "whole-index staged path mismatch"
    }
}
function Assert-UnitStart {
    param(
        [Parameter(Mandatory)][string]$ExpectedUnit,
        [Parameter(Mandatory)][string[]]$OwnedPaths,
        [Parameter(Mandatory)][string[]]$ExpectedDependencies
    )
    if ($UnitId -ne $ExpectedUnit) { throw "unit identity mismatch" }
    $top = (Invoke-CheckedGit -ArgumentList @("rev-parse","--show-toplevel")).Stdout.Trim()
    $resolvedRoot = (Resolve-Path -LiteralPath $WorktreeRoot).Path
    if ($top -ne $resolvedRoot) { throw "git top does not equal declared worktree" }
    $gitDir = (Invoke-CheckedGit -ArgumentList @("rev-parse","--git-dir")).Stdout.Trim()
    $commonDir = (Invoke-CheckedGit -ArgumentList @("rev-parse","--git-common-dir")).Stdout.Trim()
    if ([IO.Path]::GetFullPath($gitDir) -eq [IO.Path]::GetFullPath($commonDir)) {
        throw "unit is not an isolated worktree"
    }
    $head = (Invoke-CheckedGit -ArgumentList @("rev-parse","HEAD")).Stdout.Trim()
    if ($head -ne $BaseCommit) { throw "HEAD is not the reviewed base" }
    $branch = (Invoke-CheckedGit -ArgumentList @("symbolic-ref","--short","HEAD")).Stdout.Trim()
    if ($branch -notmatch "^codex/") { throw "unexpected branch" }
    try {
        $mapText = Get-GitBlobText -Commit $BaseCommit -Path $G04MapPath
    } catch {
        throw "G04_SCHEMA_AMENDMENT_REQUIRED"
    }
    try {
        $map = $mapText | ConvertFrom-Json
    } catch {
        throw "G04_SCHEMA_AMENDMENT_REQUIRED"
    }
    if ($map.schema_version -ne "worktree-map-v2" -or
        -not ($map.PSObject.Properties.Name -contains "rows")) {
        throw "G04_SCHEMA_AMENDMENT_REQUIRED"
    }
    $rows = @($map.rows | Where-Object { $_.unit_id -eq $ExpectedUnit })
    if ($rows.Count -ne 1) { throw "G04 row is missing or duplicated" }
    $row = $rows[0]
    $requiredRowFields = @(
        "unit_id","owner","branch","worktree_path","base_commit",
        "dependency_commits","merge_order","status","plan_hashes"
    )
    $actualRowFields = @($row.PSObject.Properties.Name | Sort-Object)
    if (@(Compare-Object ($requiredRowFields | Sort-Object) $actualRowFields).Count -ne 0) {
        throw "G04 row schema mismatch"
    }
    if ($row.unit_id -ne $ExpectedUnit -or $row.owner -ne $AgentId -or
        $row.branch -ne $branch -or $row.status -ne "dispatched" -or
        (($row.merge_order -isnot [int]) -and ($row.merge_order -isnot [long])) -or
        $row.merge_order -lt 1) {
        throw "G04 row worker/unit/branch/status mismatch"
    }
    if (-not [IO.Path]::IsPathFullyQualified([string]$row.worktree_path) -or
        [IO.Path]::GetFullPath([string]$row.worktree_path) -ne $resolvedRoot) {
        throw "G04 row worktree mismatch"
    }
    if ([string]$row.base_commit -notmatch "^[0-9a-f]{40}$") {
        throw "G04 row base commit malformed"
    }
    $baseAncestor = Invoke-BoundedNative -FilePath $GitExe -ArgumentList @(
        "merge-base","--is-ancestor",[string]$row.base_commit,$BaseCommit
    ) -TimeoutSeconds 120
    if ($baseAncestor.ExitCode -ne 0) { throw "G04 row base is not an ancestor" }
    $actualDependencies = @($row.dependency_commits.PSObject.Properties.Name | Sort-Object)
    $expectedDependenciesSorted = @($ExpectedDependencies | Sort-Object)
    if (@(Compare-Object $expectedDependenciesSorted $actualDependencies).Count -ne 0) {
        throw "G04 dependency set mismatch"
    }
    foreach ($dependency in $expectedDependenciesSorted) {
        $dependencyCommit = [string]$row.dependency_commits.$dependency
        if ($dependencyCommit -notmatch "^[0-9a-f]{40}$") {
            throw "G04 dependency commit malformed"
        }
        $dependencyAncestor = Invoke-BoundedNative -FilePath $GitExe -ArgumentList @(
            "merge-base","--is-ancestor",$dependencyCommit,$BaseCommit
        ) -TimeoutSeconds 120
        if ($dependencyAncestor.ExitCode -ne 0) {
            throw "G04 dependency is not an ancestor"
        }
    }
    $expectedPlanPaths = @("PLAN.md",$DomainPlanPath,$DetailedPlanPath)
    $actualPlanPaths = @($row.plan_hashes.PSObject.Properties.Name | Sort-Object)
    if (@(Compare-Object ($expectedPlanPaths | Sort-Object) $actualPlanPaths).Count -ne 0) {
        throw "G04 plan hash path set mismatch"
    }
    $actualRootSha = Get-GitBlobSha256 -Commit $BaseCommit -Path "PLAN.md"
    $actualDomainSha = Get-GitBlobSha256 -Commit $BaseCommit -Path $DomainPlanPath
    $actualDetailedSha = Get-GitBlobSha256 -Commit $BaseCommit -Path $DetailedPlanPath
    if ($RootPlanSha -ne $ExpectedRootPlanSha -or
        [string]$row.plan_hashes."PLAN.md" -ne $actualRootSha -or
        $actualRootSha -ne $ExpectedRootPlanSha -or
        [string]$row.plan_hashes.$DomainPlanPath -ne $actualDomainSha -or
        $actualDomainSha -ne $ExpectedDomainPlanSha -or
        $DetailedPlanSha -ne $actualDetailedSha -or
        [string]$row.plan_hashes.$DetailedPlanPath -ne $actualDetailedSha) {
        throw "G04 immutable plan bytes/hash mismatch"
    }
    $statusArgs = @("status","--porcelain=v1","--untracked-files=all","--") + $OwnedPaths
    $status = (Invoke-CheckedGit -ArgumentList $statusArgs).Stdout.Trim()
    if ($status) { throw "owned paths are not clean at unit start" }
    Assert-SafeNativeProtocol
}
function Get-CheckedTreeId {
    $tree = (Invoke-CheckedGit -ArgumentList @("write-tree")).Stdout.Trim()
    if ($tree -notmatch "^[0-9a-f]{40}$") { throw "invalid tree id" }
    return $tree
}
function Set-PrivateReviewAcl {
    param([Parameter(Mandatory)][string]$Path)
    $acl = Get-Acl -LiteralPath $Path
    $acl.SetAccessRuleProtection($true,$false)
    $identity = [Security.Principal.WindowsIdentity]::GetCurrent().Name
    $rule = New-Object Security.AccessControl.FileSystemAccessRule(
        $identity,"FullControl","ContainerInherit,ObjectInherit","None","Allow"
    )
    $acl.SetAccessRule($rule)
    Set-Acl -LiteralPath $Path -AclObject $acl
}
function Get-PrivateReviewPacket {
    $tree = Get-CheckedTreeId
    $reviewRoot = Join-Path ([IO.Path]::GetTempPath()) ("projectb-review-"+$UnitId+"-"+[guid]::NewGuid().ToString("N"))
    New-Item -ItemType Directory -Path $reviewRoot -Force | Out-Null
    Set-PrivateReviewAcl -Path $reviewRoot
    $payload = @{filePath=$GitExe;arguments=@("diff","--cached","--binary","--full-index");root=$WorktreeRoot} | ConvertTo-Json -Compress -Depth 4
    $payload64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($payload))
    $child = @'
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$data = ([Text.Encoding]::UTF8.GetString([Convert]::FromBase64String("__PAYLOAD__")) | ConvertFrom-Json)
Set-Location -LiteralPath ([string]$data.root)
& ([string]$data.filePath) @($data.arguments | ForEach-Object { [string]$_ })
exit $LASTEXITCODE
'@.Replace("__PAYLOAD__",$payload64)
    $encoded = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($child))
    $start = New-Object Diagnostics.ProcessStartInfo
    $start.FileName = $PowerShellExe
    $start.Arguments = "-NoProfile -NonInteractive -EncodedCommand $encoded"
    $start.UseShellExecute = $false
    $start.CreateNoWindow = $true
    $start.RedirectStandardOutput = $true
    $start.RedirectStandardError = $true
    Set-SafeChildEnvironment -StartInfo $start
    $process = New-Object Diagnostics.Process
    $process.StartInfo = $start
    try {
        if (-not $process.Start()) { throw "private review capture launch failed" }
        $outTask = $process.StandardOutput.ReadToEndAsync()
        $errTask = $process.StandardError.ReadToEndAsync()
        if (-not $process.WaitForExit(120000)) {
            Stop-NativeProcessTree -ProcessId $process.Id
            throw "private review capture timed out"
        }
        $rawDiff = $outTask.GetAwaiter().GetResult()
        $safeError = ConvertTo-RedactedDiagnostic $errTask.GetAwaiter().GetResult() 4096
        if ($process.ExitCode -ne 0) { throw "private review capture failed exit=$($process.ExitCode) $safeError" }
    } finally {
        $process.Dispose()
    }
    if ([string]::IsNullOrWhiteSpace($rawDiff) -or $rawDiff.Length -gt 4194304) {
        throw "private review packet is empty or outside the bound"
    }
    $packetPath = Join-Path $reviewRoot "staged.diff"
    [IO.File]::WriteAllText($packetPath,$rawDiff,[Text.UTF8Encoding]::new($false))
    $bytes = [IO.File]::ReadAllBytes($packetPath)
    if ($bytes.Length -gt 4194304) { throw "private review packet exceeds byte bound" }
    $digest = ([BitConverter]::ToString([Security.Cryptography.SHA256]::HashData($bytes))).Replace("-","").ToLowerInvariant()
    return [pscustomobject]@{Path=$packetPath;TreeId=$tree;PacketSha256=$digest}
}
function Assert-ReviewReceipt {
    param(
        [Parameter(Mandatory)][string]$Path,
        [Parameter(Mandatory)][string]$Role,
        [Parameter(Mandatory)][string]$TreeId,
        [Parameter(Mandatory)][string]$PacketSha256,
        [Parameter(Mandatory)][string]$ExpectedUnit
    )
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { throw "$Role review receipt missing" }
    $raw = Get-Content -Raw -LiteralPath $Path
    if ($raw.Length -gt 1048576) { throw "$Role review receipt too large" }
    $receipt = $raw | ConvertFrom-Json
    if ($receipt.result -ne "PASS" -or
        $receipt.unit_id -ne $ExpectedUnit -or
        $receipt.root_plan_sha256 -ne $RootPlanSha -or
        $receipt.detailed_plan_sha256 -ne $DetailedPlanSha -or
        $receipt.tree_id -ne $TreeId -or
        $receipt.packet_sha256 -ne $PacketSha256 -or
        $receipt.reviewer_id -notmatch "^[A-Za-z0-9][A-Za-z0-9._-]{1,63}$" -or
        $receipt.reviewer_id -eq $env:PROJECTB_AGENT_ID) {
        throw "$Role review receipt is not bound to this packet and tree"
    }
    return $receipt
}
function Start-UnitReview {
    param([Parameter(Mandatory)][string[]]$ExpectedPaths)
    $stageArgs = @("add","--") + $ExpectedPaths
    Invoke-CheckedGit -ArgumentList $stageArgs
    Assert-ExactStagedPaths -ExpectedPaths $ExpectedPaths
    Invoke-CheckedGit -ArgumentList @("diff","--cached","--check")
    Invoke-CheckedPython -ArgumentList @("scripts/scan_secrets.py","--staged","--git-exe",$GitExe) -TimeoutSeconds 300
    return Get-PrivateReviewPacket
}
function Assert-UnitReviewReceipts {
    param(
        [Parameter(Mandatory)][object]$Packet,
        [Parameter(Mandatory)][string]$ExpectedUnit
    )
    $spec = Assert-ReviewReceipt $env:PROJECTB_SPEC_REVIEW_RECEIPT "SPEC" $Packet.TreeId $Packet.PacketSha256 $ExpectedUnit
    $quality = Assert-ReviewReceipt $env:PROJECTB_QUALITY_REVIEW_RECEIPT "quality" $Packet.TreeId $Packet.PacketSha256 $ExpectedUnit
    if ($spec.reviewer_id -eq $quality.reviewer_id) { throw "reviewers must be distinct" }
    return [pscustomobject]@{Spec=$spec;Quality=$quality}
}
function Complete-ReviewedUnit {
    param(
        [Parameter(Mandatory)][string[]]$ExpectedPaths,
        [Parameter(Mandatory)][object]$Packet,
        [Parameter(Mandatory)][string]$CommitMessage
    )
    Assert-ExactStagedPaths -ExpectedPaths $ExpectedPaths
    Invoke-CheckedGit -ArgumentList @("diff","--cached","--check")
    Invoke-CheckedPython -ArgumentList @("scripts/scan_secrets.py","--staged","--git-exe",$GitExe) -TimeoutSeconds 300
    $recheck = Get-PrivateReviewPacket
    if ($recheck.TreeId -ne $Packet.TreeId -or $recheck.PacketSha256 -ne $Packet.PacketSha256) {
        throw "reviewed packet changed"
    }
    Invoke-CheckedGit -ArgumentList @("commit","-m",$CommitMessage)
    $head = (Invoke-CheckedGit -ArgumentList @("rev-parse","HEAD")).Stdout.Trim()
    $tree = (Invoke-CheckedGit -ArgumentList @("rev-parse","HEAD^{tree}")).Stdout.Trim()
    if ($head -notmatch "^[0-9a-f]{40}$" -or $tree -ne $Packet.TreeId) {
        throw "committed tree differs from reviewed tree"
    }
}
~~~

## Mandatory Finalization For Every Unit

Each unit repeats separate executable 2-5 minute checkboxes for red, green, regressions, stage, scanner, private review packet, receipt validation, tree recheck, commit, and post-commit tree equality. None of those commands is claimed as executed here.

1. Add the literal owned paths through Invoke-CheckedGit and enumerate the entire index with Assert-ExactStagedPaths.
2. Run checked git diff --cached --check and checked scripts/scan_secrets.py --staged --git-exe $GitExe. Diagnostics are bounded, path-redacted, credential-redacted, and never include raw child output beyond 4096 characters.
3. Capture `Get-PrivateReviewPacket` only after the scanner passes. Its exact staged `--binary --full-index` diff is stored beneath a current-user-only temporary directory and is never printed. Dispatch a fresh SPEC reviewer and a different fresh quality/security/license reviewer with that private packet path, packet SHA-256, and tree ID. Both receipts name root hash, detailed-plan hash, unit ID, worker ID, reviewer ID, packet hash, and the same tree.
4. Any edit invalidates both reviews. Restage, rescan, recapture, and repeat both reviews.
5. Immediately before commit, repeat exact path, diff, scanner, and tree checks. Require equality with the reviewed tree.
6. Commit through Invoke-CheckedGit. Separately capture/validate HEAD and HEAD^{tree}; require committed tree equality. Worker reports evidence to the coordinator and never edits shared ledgers.

Every native invocation, including tests, Ruff, mypy, Git, scanner, and private review-packet capture, is bounded. Timeout invokes recursive Windows process-tree cleanup; failure to clean the tree is itself blocking. Reviewers receive only the scanner-approved private packet; ordinary diagnostics are bounded and sanitized.

### Required G-04 v2 row contract before dispatch

The pending root amendment must make `docs/engineering/WORKTREE_MAP.v2.json` a UTF-8 JSON object whose only top-level keys are `schema_version` (literal `worktree-map-v2`) and `rows` (an array). Each row has exactly `unit_id`, `owner`, `branch`, `worktree_path`, `base_commit`, `dependency_commits`, `merge_order`, `status`, and `plan_hashes`. `unit_id` is one of the dispatched IDs; `owner` is the reviewed worker identity grammar; `branch` is the exact `codex/` ref; `worktree_path` is an absolute canonical path; `base_commit` is a 40-lowercase-hex implementation-content ancestor; `dependency_commits` has exactly the declared dependency IDs and 40-lowercase-hex commits; `merge_order` is a positive integer; `status` is exactly `dispatched`; and `plan_hashes` has exactly `PLAN.md`, the reviewed domain-plan path, and this detailed-plan path mapped to uppercase SHA-256 values. The row must be committed before the unit worktree is created, so the commit containing the row is the immutable dispatch `BaseCommit`/HEAD while its `base_commit` points to the earlier implementation-content ancestor. The G-04 validator must reject duplicate rows, unknown keys, malformed paths/hashes, missing dependencies, non-ancestor commits, and rows whose worktree/owner/branch no longer match the actual worktree. Until that amended validator and schema are present in the BaseCommit snapshot, `Assert-UnitStart` must stop with `G04_SCHEMA_AMENDMENT_REQUIRED`.

## Task T-04A: Enforce Loopback, Host, And Origin Policy

**Goal:** Reject non-loopback binding and untrusted Host/Origin before route execution.

**Files:**
- Create: backend/src/projectb/application/security.py
- Test: backend/tests/integration/test_http_origin_policy.py

**Interfaces:** `RequestMetadata`, `TrustedRequestPolicy.local(port, bind_host)`, `TrustedRequestPolicy.check(request)`, `SecurityCode`, and `SecurityError`.

**Dependencies / parallelism:** Requires reviewed T-01F3 and T-03C commits. It serially precedes T-04B; no parallel editor may touch security.py.

**Expected first failure:** the focused test cannot import projectb.application.security.

- [ ] **Step 1: Execute the prelude and verify exact predecessor hashes**

Run the complete prelude. Compare the coordinator-recorded T-01F3/T-03C hashes with PROJECTB_BASE_COMMIT ancestry through checked Git. Stop if either is absent or unreviewed.

~~~powershell
$owned=@("backend/src/projectb/application/security.py","backend/tests/integration/test_http_origin_policy.py")
Assert-UnitStart -ExpectedUnit "T-04A" -OwnedPaths $owned -ExpectedDependencies @("T-01F3","T-03C")
if ($RootPlanSha -ne "4BCFE8470DE57C0DD54004935285CAAD5CD9D1AFF0AA7370CC4E098887745F08") { throw "root plan snapshot mismatch" }
~~~

- [ ] **Step 2: Write the failing request-policy test**

Create backend/tests/integration/test_http_origin_policy.py:

~~~python
import pytest
from projectb.application.security import (
    RequestMetadata,
    SecurityCode,
    SecurityError,
    TrustedRequestPolicy,
)


def metadata(
    server_host: str | None = "127.0.0.1",
    server_port: int | None = 8765,
    host: str | None = "127.0.0.1:8765",
    origin: str | None = "http://127.0.0.1:8765",
    method: str = "GET",
) -> RequestMetadata:
    return RequestMetadata(server_host, server_port, host, origin, method)


def test_explicit_loopback_host_and_origin_pass() -> None:
    TrustedRequestPolicy.local(8765).check(metadata())


@pytest.mark.parametrize("value", ["0.0.0.0", "::", "192.168.1.8"])
def test_non_loopback_configuration_fails(value: str) -> None:
    with pytest.raises(SecurityError) as error:
        TrustedRequestPolicy.local(8765, value)
    assert error.value.code is SecurityCode.BIND_NON_LOOPBACK


def test_missing_asgi_server_metadata_fails() -> None:
    with pytest.raises(SecurityError) as error:
        TrustedRequestPolicy.local(8765).check(metadata(server_host=None, server_port=None))
    assert error.value.code is SecurityCode.SERVER_METADATA_MISSING


@pytest.mark.parametrize(
    ("server_host", "server_port"),
    [("::1", 8765), ("localhost", 8765), ("127.0.0.1", 8766)],
)
def test_other_loopback_or_port_does_not_equal_configured_bind(
    server_host: str,
    server_port: int,
) -> None:
    with pytest.raises(SecurityError) as error:
        TrustedRequestPolicy.local(8765, "127.0.0.1").check(
            metadata(server_host=server_host, server_port=server_port)
        )
    assert error.value.code is SecurityCode.BIND_MISMATCH


@pytest.mark.parametrize(
    "value",
    ["evil.invalid:8765", "127.0.0.1:80", "127.0.0.1:8765,evil.invalid", "127.0.0.1.:8765"],
)
def test_untrusted_host_fails(value: str) -> None:
    with pytest.raises(SecurityError) as error:
        TrustedRequestPolicy.local(8765).check(metadata(host=value))
    assert error.value.code is SecurityCode.HOST_UNTRUSTED


@pytest.mark.parametrize(
    "value", ["https://evil.invalid", "null", "http://127.0.0.1:8765@evil.invalid"]
)
def test_untrusted_origin_fails(value: str) -> None:
    with pytest.raises(SecurityError) as error:
        TrustedRequestPolicy.local(8765).check(metadata(origin=value, method="POST"))
    assert error.value.code is SecurityCode.ORIGIN_UNTRUSTED


def test_state_change_requires_origin() -> None:
    with pytest.raises(SecurityError) as error:
        TrustedRequestPolicy.local(8765).check(metadata(origin=None, method="DELETE"))
    assert error.value.code is SecurityCode.ORIGIN_MISSING
~~~

- [ ] **Step 3: Run red and preserve the expected import failure**

~~~powershell
$red = Invoke-BoundedNative -FilePath $PythonExe -ArgumentList @("-m","pytest","backend/tests/integration/test_http_origin_policy.py","-q") -TimeoutSeconds 120
if ($red.ExitCode -eq 0) { throw "T-04A red unexpectedly passed" }
if (($red.Stdout + $red.Stderr) -notmatch "security") { throw "T-04A failed for the wrong reason" }
~~~

Expected: nonzero with missing security module/type, not timeout or interpreter failure.

- [ ] **Step 4: Add the minimal pure policy**

Create backend/src/projectb/application/security.py:

~~~python
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class SecurityCode(StrEnum):
    BIND_NON_LOOPBACK = "bind_non_loopback"
    BIND_MISMATCH = "bind_mismatch"
    SERVER_METADATA_MISSING = "server_metadata_missing"
    HOST_UNTRUSTED = "host_untrusted"
    ORIGIN_MISSING = "origin_missing"
    ORIGIN_UNTRUSTED = "origin_untrusted"
    CSRF_MISSING = "csrf_missing"
    CSRF_INVALID = "csrf_invalid"
    CSRF_EXPIRED = "csrf_expired"
    CSRF_REPLAY = "csrf_replay"
    SESSION_INVALID = "session_invalid"
    AUDIT_FIELD_FORBIDDEN = "audit_field_forbidden"
    AUDIT_VALUE_FORBIDDEN = "audit_value_forbidden"


class SecurityError(Exception):
    def __init__(self, code: SecurityCode) -> None:
        self.code = code
        super().__init__(code.value)


@dataclass(frozen=True)
class RequestMetadata:
    server_host: str | None
    server_port: int | None
    host_header: str | None
    origin_header: str | None
    method: str = "GET"


~~~

- [ ] **Step 5: Append the exact request policy**

Append to backend/src/projectb/application/security.py:

~~~python
@dataclass(frozen=True)
class TrustedRequestPolicy:
    bind_host: str
    port: int
    allowed_host: str
    allowed_origin: str

    def __post_init__(self) -> None:
        if self.bind_host not in {"127.0.0.1", "::1"}:
            raise SecurityError(SecurityCode.BIND_NON_LOOPBACK)
        if type(self.port) is not int or not 1 <= self.port <= 65535:
            raise SecurityError(SecurityCode.BIND_NON_LOOPBACK)

    @classmethod
    def local(cls, port: int, bind_host: str = "127.0.0.1") -> TrustedRequestPolicy:
        if type(port) is not int or not 1 <= port <= 65535:
            raise SecurityError(SecurityCode.BIND_NON_LOOPBACK)
        if bind_host not in {"127.0.0.1", "::1"}:
            raise SecurityError(SecurityCode.BIND_NON_LOOPBACK)
        canonical_host = f"[{bind_host}]:{port}" if bind_host == "::1" else f"{bind_host}:{port}"
        return cls(bind_host, port, canonical_host, f"http://{canonical_host}")

    def check(self, request: RequestMetadata) -> None:
        if request.server_host is None or request.server_port is None:
            raise SecurityError(SecurityCode.SERVER_METADATA_MISSING)
        if request.server_host != self.bind_host or request.server_port != self.port:
            raise SecurityError(SecurityCode.BIND_MISMATCH)
        if request.host_header is None:
            raise SecurityError(SecurityCode.HOST_UNTRUSTED)
        host = request.host_header.strip().lower()
        if (
            not host
            or host != self.allowed_host
            or any(value in host for value in (",", "\r", "\n", "/", "\\", "@"))
            or host.endswith(".")
        ):
            raise SecurityError(SecurityCode.HOST_UNTRUSTED)
        origin = request.origin_header
        if origin is None:
            if request.method.upper() in {"POST", "PUT", "PATCH", "DELETE"}:
                raise SecurityError(SecurityCode.ORIGIN_MISSING)
            return
        normalized = origin.strip().lower()
        if (
            normalized == "null"
            or normalized != self.allowed_origin
            or any(value in normalized for value in (",", "\r", "\n", "\\", "@"))
        ):
            raise SecurityError(SecurityCode.ORIGIN_UNTRUSTED)
~~~

- [ ] **Step 6: Run focused green**

~~~powershell
Invoke-CheckedPython -ArgumentList @("-m","pytest","backend/tests/integration/test_http_origin_policy.py","-q") -TimeoutSeconds 120
~~~

Expected: all loopback/Host/Origin cases pass and no route, filesystem, keyring, or network operation occurs.

- [ ] **Step 7: Run refactor checks and regressions**

~~~powershell
Invoke-CheckedPython @("-m","ruff","check","--config","backend/pyproject.toml","backend/src/projectb/application/security.py","backend/tests/integration/test_http_origin_policy.py") 120
Invoke-CheckedPython @("-m","mypy","--config-file","backend/pyproject.toml","backend/src/projectb/application/security.py","backend/tests/integration/test_http_origin_policy.py") 120
Invoke-CheckedPython @("-m","pytest","backend/tests/integration/test_http_origin_policy.py","backend/tests","-q") 300
Invoke-CheckedPython @("scripts/test_all.py") 900
~~~

Expected: each checked command exits 0 independently. No CORS/proxy setting is added.

- [ ] **Step 8: Run both reviews**

SPEC review checks AC-07/AC-11 and threat T-13: loopback-only binding, exact Host/Origin, missing/null/foreign origins, malformed aliases, proxy/CORS bypass, redaction, and no registration route. Quality/security/license review checks IPv6 brackets, Unicode/control characters, header normalization, deterministic tests, dependency scope, and pre-route enforcement. Critical/Important findings require a new red test and invalidate prior reviews.

- [ ] **Step 9: Stage, scan, and capture the private T-04A packet**

~~~powershell
$expected=@("backend/src/projectb/application/security.py","backend/tests/integration/test_http_origin_policy.py")
$reviewPacket=Start-UnitReview $expected
~~~

- [ ] **Step 10: Validate both T-04A review receipts**

~~~powershell
$receipts=Assert-UnitReviewReceipts $reviewPacket "T-04A"
~~~

- [ ] **Step 11: Recheck and commit the reviewed T-04A tree**

~~~powershell
Complete-ReviewedUnit $expected $reviewPacket "feat(T-04A): enforce local request origins [agent: $env:PROJECTB_AGENT_ID]"
~~~

**Completion standard:** Only an explicit loopback Host/Origin reaches the application boundary.

## Task T-04B: Add Session-Bound CSRF Tokens

**Goal:** Issue, expire, bind, and consume unpredictable CSRF tokens for state-changing requests.

**Files:**
- Modify: backend/src/projectb/application/security.py
- Test: backend/tests/unit/test_csrf_tokens.py

**Interfaces:** CsrfService(clock, ttl), issue(session_id), and verify(session_id, token).

**Dependencies / parallelism:** Requires reviewed T-04A and serial ownership of security.py. It precedes T-04C.

**Expected first failure:** CsrfService is absent from the reviewed T-04A module.

- [ ] **Step 1: Run the prelude and verify T-04A base**

Stop if the base is not the reviewed T-04A commit or another unit has modified security.py.

~~~powershell
$owned=@("backend/src/projectb/application/security.py","backend/tests/unit/test_csrf_tokens.py")
Assert-UnitStart -ExpectedUnit "T-04B" -OwnedPaths $owned -ExpectedDependencies @("T-04A")
~~~

- [ ] **Step 2: Write failing CSRF tests**

Create backend/tests/unit/test_csrf_tokens.py:

~~~python
from datetime import UTC, datetime, timedelta

import pytest
from projectb.application.security import CsrfService, SecurityCode, SecurityError


class Clock:
    def __init__(self) -> None:
        self.value = datetime(2026, 7, 23, tzinfo=UTC)

    def __call__(self) -> datetime:
        return self.value


def test_token_is_unpredictable_replaced_and_single_use() -> None:
    clock = Clock()
    service = CsrfService(clock=clock, ttl=timedelta(minutes=15))
    first = service.issue("session-a1")
    second = service.issue("session-a1")
    assert len(first) >= 43
    assert first != second
    with pytest.raises(SecurityError) as error:
        service.verify("session-a1", first)
    assert error.value.code is SecurityCode.CSRF_REPLAY
    service.verify("session-a1", second)
    with pytest.raises(SecurityError) as error:
        service.verify("session-a1", second)
    assert error.value.code is SecurityCode.CSRF_REPLAY


def test_cross_session_malformed_and_expired_tokens_fail() -> None:
    clock = Clock()
    service = CsrfService(clock=clock, ttl=timedelta(minutes=15))
    token = service.issue("session-a1")
    with pytest.raises(SecurityError) as error:
        service.verify("session-b1", token)
    assert error.value.code is SecurityCode.SESSION_INVALID
    with pytest.raises(SecurityError) as error:
        service.verify("session-a1", "short")
    assert error.value.code is SecurityCode.CSRF_INVALID
    clock.value += timedelta(minutes=16)
    with pytest.raises(SecurityError) as error:
        service.verify("session-a1", token)
    assert error.value.code is SecurityCode.CSRF_EXPIRED
~~~

- [ ] **Step 3: Run red**

~~~powershell
$red=Invoke-BoundedNative $PythonExe @("-m","pytest","backend/tests/unit/test_csrf_tokens.py","-q") 120
if ($red.ExitCode -eq 0 -or ($red.Stdout+$red.Stderr) -notmatch "CsrfService") { throw "T-04B red evidence invalid" }
~~~

- [ ] **Step 4: Replace security.py with the complete post-T-04B file**

Write the complete post-T-04B file below; it preserves the reviewed T-04A APIs and adds CSRF support:

~~~python
from __future__ import annotations

import hashlib
import hmac
import re
import secrets
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from enum import StrEnum


class SecurityCode(StrEnum):
    BIND_NON_LOOPBACK = "bind_non_loopback"
    BIND_MISMATCH = "bind_mismatch"
    SERVER_METADATA_MISSING = "server_metadata_missing"
    HOST_UNTRUSTED = "host_untrusted"
    ORIGIN_MISSING = "origin_missing"
    ORIGIN_UNTRUSTED = "origin_untrusted"
    CSRF_MISSING = "csrf_missing"
    CSRF_INVALID = "csrf_invalid"
    CSRF_EXPIRED = "csrf_expired"
    CSRF_REPLAY = "csrf_replay"
    SESSION_INVALID = "session_invalid"
    AUDIT_FIELD_FORBIDDEN = "audit_field_forbidden"
    AUDIT_VALUE_FORBIDDEN = "audit_value_forbidden"


class SecurityError(Exception):
    def __init__(self, code: SecurityCode) -> None:
        self.code = code
        super().__init__(code.value)


@dataclass(frozen=True)
class RequestMetadata:
    server_host: str | None
    server_port: int | None
    host_header: str | None
    origin_header: str | None
    method: str = "GET"


@dataclass(frozen=True)
class TrustedRequestPolicy:
    bind_host: str
    port: int
    allowed_host: str
    allowed_origin: str

    def __post_init__(self) -> None:
        if self.bind_host not in {"127.0.0.1", "::1"}:
            raise SecurityError(SecurityCode.BIND_NON_LOOPBACK)
        if type(self.port) is not int or not 1 <= self.port <= 65535:
            raise SecurityError(SecurityCode.BIND_NON_LOOPBACK)

    @classmethod
    def local(cls, port: int, bind_host: str = "127.0.0.1") -> TrustedRequestPolicy:
        if type(port) is not int or not 1 <= port <= 65535:
            raise SecurityError(SecurityCode.BIND_NON_LOOPBACK)
        if bind_host not in {"127.0.0.1", "::1"}:
            raise SecurityError(SecurityCode.BIND_NON_LOOPBACK)
        canonical_host = f"[{bind_host}]:{port}" if bind_host == "::1" else f"{bind_host}:{port}"
        return cls(bind_host, port, canonical_host, f"http://{canonical_host}")

    def check(self, request: RequestMetadata) -> None:
        if request.server_host is None or request.server_port is None:
            raise SecurityError(SecurityCode.SERVER_METADATA_MISSING)
        if request.server_host != self.bind_host or request.server_port != self.port:
            raise SecurityError(SecurityCode.BIND_MISMATCH)
        if request.host_header is None:
            raise SecurityError(SecurityCode.HOST_UNTRUSTED)
        host = request.host_header.strip().lower()
        if (
            not host
            or host != self.allowed_host
            or any(value in host for value in (",", "\r", "\n", "/", "\\", "@"))
            or host.endswith(".")
        ):
            raise SecurityError(SecurityCode.HOST_UNTRUSTED)
        origin = request.origin_header
        if origin is None:
            if request.method.upper() in {"POST", "PUT", "PATCH", "DELETE"}:
                raise SecurityError(SecurityCode.ORIGIN_MISSING)
            return
        normalized = origin.strip().lower()
        if (
            normalized == "null"
            or normalized != self.allowed_origin
            or any(value in normalized for value in (",", "\r", "\n", "\\", "@"))
        ):
            raise SecurityError(SecurityCode.ORIGIN_UNTRUSTED)
~~~

- [ ] **Step 5: Append the CSRF entry and service**

Append to backend/src/projectb/application/security.py:

~~~python
_SESSION = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{7,127}$")


@dataclass
class _CsrfEntry:
    digest: bytes
    expires_at: datetime
    used: bool = False


class CsrfService:
    def __init__(
        self,
        *,
        clock: Callable[[], datetime] = lambda: datetime.now(UTC),
        ttl: timedelta = timedelta(minutes=15),
    ) -> None:
        if ttl <= timedelta(0) or ttl > timedelta(hours=1):
            raise ValueError("csrf ttl outside bound")
        self._clock = clock
        self._ttl = ttl
        self._entries: dict[str, _CsrfEntry] = {}
        self._retired: dict[str, set[bytes]] = {}

    def issue(self, session_id: str) -> str:
        self._validate_session(session_id)
        previous = self._entries.get(session_id)
        if previous is not None:
            previous.used = True
            self._retired.setdefault(session_id, set()).add(previous.digest)
        token = secrets.token_urlsafe(32)
        self._entries[session_id] = _CsrfEntry(
            hashlib.sha256(token.encode("ascii")).digest(),
            self._clock() + self._ttl,
        )
        return token

    def verify(self, session_id: str, token: str | None) -> None:
        self._validate_session(session_id)
        if token is None:
            raise SecurityError(SecurityCode.CSRF_MISSING)
        if not isinstance(token, str) or not 43 <= len(token) <= 128:
            raise SecurityError(SecurityCode.CSRF_INVALID)
        try:
            presented = hashlib.sha256(token.encode("ascii")).digest()
        except UnicodeEncodeError:
            raise SecurityError(SecurityCode.CSRF_INVALID) from None
        if presented in self._retired.get(session_id, set()):
            raise SecurityError(SecurityCode.CSRF_REPLAY)
        entry = self._entries.get(session_id)
        if entry is None:
            raise SecurityError(SecurityCode.SESSION_INVALID)
        if entry.used:
            raise SecurityError(SecurityCode.CSRF_REPLAY)
        if self._clock() >= entry.expires_at:
            entry.used = True
            self._retired.setdefault(session_id, set()).add(entry.digest)
            raise SecurityError(SecurityCode.CSRF_EXPIRED)
        if not hmac.compare_digest(entry.digest, presented):
            raise SecurityError(SecurityCode.CSRF_INVALID)
        entry.used = True
        self._retired.setdefault(session_id, set()).add(entry.digest)

    @staticmethod
    def _validate_session(session_id: str) -> None:
        if not isinstance(session_id, str) or _SESSION.fullmatch(session_id) is None:
            raise SecurityError(SecurityCode.SESSION_INVALID)
~~~

- [ ] **Step 6: Run green and cumulative security tests**

~~~powershell
Invoke-CheckedPython @("-m","pytest","backend/tests/unit/test_csrf_tokens.py","backend/tests/integration/test_http_origin_policy.py","-q") 120
~~~

- [ ] **Step 7: Run Ruff, mypy, backend, and canonical regression**

~~~powershell
Invoke-CheckedPython @("-m","ruff","check","--config","backend/pyproject.toml","backend/src/projectb/application/security.py","backend/tests/unit/test_csrf_tokens.py","backend/tests/integration/test_http_origin_policy.py") 120
Invoke-CheckedPython @("-m","mypy","--config-file","backend/pyproject.toml","backend/src/projectb/application/security.py","backend/tests/unit/test_csrf_tokens.py","backend/tests/integration/test_http_origin_policy.py") 120
Invoke-CheckedPython @("-m","pytest","backend/tests/unit/test_csrf_tokens.py","backend/tests/integration/test_http_origin_policy.py","backend/tests","-q") 300
Invoke-CheckedPython @("scripts/test_all.py") 900
~~~

- [ ] **Step 8: Run both reviews**

SPEC review checks AC-11/T-13 for 256-bit entropy, session binding, expiry, replay, constant-time comparison, and no Origin-only mutation. Quality/security/license review checks clock handling, process-memory lifetime, Unicode, error/token leakage, timing behavior, and T-04C compatibility.

- [ ] **Step 9: Stage, scan, and capture the private T-04B packet**

~~~powershell
$expected=@("backend/src/projectb/application/security.py","backend/tests/unit/test_csrf_tokens.py")
$reviewPacket=Start-UnitReview $expected
~~~

- [ ] **Step 10: Validate both T-04B review receipts**

~~~powershell
$receipts=Assert-UnitReviewReceipts $reviewPacket "T-04B"
~~~

- [ ] **Step 11: Recheck and commit the reviewed T-04B tree**

~~~powershell
Complete-ReviewedUnit $expected $reviewPacket "feat(T-04B): add session CSRF tokens [agent: $env:PROJECTB_AGENT_ID]"
~~~

**Completion standard:** No state change is authorized by a token from another, expired, replayed, missing, or malformed session.

## Task T-04C: Wire Shared Middleware And Whitelist-Only Audit

**Goal:** Install T-04A/B exactly once in create_app and emit only allowlisted audit metadata.

**Files:**
- Create: backend/src/projectb/api/middleware.py
- Create: backend/src/projectb/infrastructure/audit.py
- Modify: backend/src/projectb/api/app.py
- Test: backend/tests/integration/test_http_security.py

**Interfaces:** `SecurityMiddleware`, `AuditAction`, `mark_provider_action`, `AuditWriter`, `AuditEvent`, `AppSecurityProfile(bind_host, port)`, and `create_app(profile, audit_writer)`. No feature router is registered.

**Dependencies / parallelism:** Requires reviewed T-04B, T-01B/T-01F3, and T-03C. This is the serialized app.py owner before API-REG-01.

**Expected first failure:** middleware/audit types and create_app security arguments are absent.

- [ ] **Step 1: Validate predecessor hashes**

~~~powershell
$owned=@("backend/src/projectb/api/middleware.py","backend/src/projectb/infrastructure/audit.py","backend/src/projectb/api/app.py","backend/tests/integration/test_http_security.py")
Assert-UnitStart -ExpectedUnit "T-04C" -OwnedPaths $owned -ExpectedDependencies @("T-01B","T-01F3","T-03C","T-04B")
~~~

Stop unless the authoritative G-04 row names the reviewed T-04B, T-01B/T-01F3, and T-03C dependency commits. The common prelude performs the exact row and ancestry checks.

- [ ] **Step 2: Create the security integration-test fixtures**

Create backend/tests/integration/test_http_security.py with the imports, private-value matrix, and secured app fixture:

~~~python
import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from projectb.api.app import AppSecurityProfile, create_app
from projectb.api.middleware import mark_provider_action
from projectb.infrastructure.audit import AuditWriter

PRIVATE_VALUES = (
    r"C:\Users\student\lecture.pdf",
    r"\\server\share\lecture.pdf",
    "/home/student/lecture.pdf",
    "~/lecture.pdf",
    "https://example.invalid/private",
    "private lecture body with spaces",
)

_AUDIT_BASELINES: dict[str, dict[str, object]] = {
    "request_rejected": {"error_code": "host_untrusted", "status_code": 403},
    "request_failed": {"method": "POST", "status_code": 500},
    "state_change_succeeded": {"duration_ms": 4, "status_code": 204},
    "provider_action_succeeded": {"duration_ms": 4, "status_code": 200},
}


def _audit_case(
    event_type: str, result: str, key: str, value: object
) -> tuple[str, str, str, dict[str, object]]:
    metadata = dict(_AUDIT_BASELINES[event_type])
    metadata[key] = value
    return event_type, result, key, metadata


ALLOWED_KEY_CASES: tuple[tuple[str, str, str, dict[str, object]], ...] = (
    _audit_case("request_rejected", "rejected", "error_code", "host_untrusted"),
    _audit_case("request_rejected", "rejected", "status_code", 403),
    _audit_case("request_failed", "failed", "method", "POST"),
    _audit_case("request_failed", "failed", "status_code", 500),
    _audit_case("state_change_succeeded", "accepted", "duration_ms", 4),
    _audit_case("state_change_succeeded", "accepted", "status_code", 204),
    _audit_case("state_change_succeeded", "accepted", "count", 1),
    _audit_case("state_change_succeeded", "accepted", "states", ("ready",)),
    _audit_case("state_change_succeeded", "accepted", "course_id", "course-1"),
    _audit_case("state_change_succeeded", "accepted", "material_id", "material-1"),
    _audit_case("provider_action_succeeded", "accepted", "duration_ms", 4),
    _audit_case("provider_action_succeeded", "accepted", "status_code", 200),
    _audit_case("provider_action_succeeded", "accepted", "mode", "P"),
    _audit_case("provider_action_succeeded", "accepted", "profile_id", "profile-1"),
    _audit_case("provider_action_succeeded", "accepted", "request_id", "request-1"),
)


@pytest.fixture()
def secured() -> tuple[TestClient, AuditWriter, FastAPI]:
    audit = AuditWriter.memory()
    app = create_app(AppSecurityProfile(bind_host="127.0.0.1", port=8765), audit_writer=audit)

    @app.post("/api/_security_probe")
    def probe() -> dict[str, bool]:
        return {"changed": True}

    @app.post("/api/_provider_probe")
    def provider_probe(request: Request) -> dict[str, bool]:
        mark_provider_action(request, ("course-1", "request-1"))
        return {"called": True}

    @app.post("/api/_failure_probe")
    def failure_probe() -> None:
        raise RuntimeError("synthetic-sensitive-body")

    return TestClient(app, base_url="http://127.0.0.1:8765"), audit, app
~~~

- [ ] **Step 3: Append the request-boundary tests**

Append to backend/tests/integration/test_http_security.py:

~~~python


def test_untrusted_host_origin_and_missing_csrf_fail(
    secured: tuple[TestClient, AuditWriter, FastAPI],
) -> None:
    client, _, _ = secured
    assert client.get("/api/health", headers={"Host": "evil.invalid:8765"}).status_code == 403
    assert (
        client.post(
            "/api/_security_probe",
            headers={"Host": "127.0.0.1:8765", "Origin": "https://evil.invalid"},
        ).status_code
        == 403
    )
    assert (
        client.post(
            "/api/_security_probe",
            headers={"Host": "127.0.0.1:8765", "Origin": "http://127.0.0.1:8765"},
        ).status_code
        == 403
    )


def test_fresh_token_allows_once_and_replay_fails(
    secured: tuple[TestClient, AuditWriter, FastAPI],
) -> None:
    client, _, app = secured
    session_id = "session-a1"
    token = app.state.csrf_service.issue(session_id)
    client.cookies.set("projectb_session", session_id)
    headers = {
        "Host": "127.0.0.1:8765",
        "Origin": "http://127.0.0.1:8765",
        "X-CSRF-Token": token,
    }
    assert client.post("/api/_security_probe", headers=headers).status_code == 200
    assert client.post("/api/_security_probe", headers=headers).status_code == 403
    assert [event.event_type for event in app.state.audit_writer.events].count(
        "state_change_succeeded"
    ) == 1
~~~

- [ ] **Step 4: Append the exception and audit-schema tests**

Append to backend/tests/integration/test_http_security.py:

~~~python


def test_provider_success_and_route_exception_are_sanitized_and_audited(
    secured: tuple[TestClient, AuditWriter, FastAPI],
) -> None:
    client, audit, app = secured
    session_id = "session-a1"
    client.cookies.set("projectb_session", session_id)

    def headers() -> dict[str, str]:
        return {
            "Host": "127.0.0.1:8765",
            "Origin": "http://127.0.0.1:8765",
            "X-CSRF-Token": app.state.csrf_service.issue(session_id),
        }

    assert client.post("/api/_provider_probe", headers=headers()).status_code == 200
    failed = client.post("/api/_failure_probe", headers=headers())
    assert failed.status_code == 500
    assert failed.json() == {"error": "request_failed"}
    assert "synthetic-sensitive-body" not in failed.text
    assert {event.event_type for event in audit.events} >= {
        "provider_action_succeeded",
        "request_failed",
    }
    assert all("synthetic-sensitive-body" not in repr(event) for event in audit.events)
~~~

- [ ] **Step 5: Append immutable and per-key private-value audit tests**

Append to backend/tests/integration/test_http_security.py:

~~~python


def test_audit_accepts_deep_immutable_event_specific_metadata(
    secured: tuple[TestClient, AuditWriter, FastAPI],
) -> None:
    _, audit, _ = secured
    source: dict[str, object] = {
        "duration_ms": 4,
        "status_code": 204,
        "count": 1,
        "states": ("ready",),
        "course_id": "course-1",
        "material_id": "material-1",
    }
    audit.record("state_change_succeeded", ("course-1",), "accepted", source)
    source["count"] = 99
    assert audit.events[0].metadata == {
        "duration_ms": 4,
        "status_code": 204,
        "count": 1,
        "states": ("ready",),
        "course_id": "course-1",
        "material_id": "material-1",
    }
    with pytest.raises(TypeError):
        audit.events[0].metadata["count"] = 2  # type: ignore[index]


@pytest.mark.parametrize("private_value", PRIVATE_VALUES)
@pytest.mark.parametrize("event_type,result,key,baseline", ALLOWED_KEY_CASES)
def test_audit_rejects_private_values_under_every_allowed_key(
    secured: tuple[TestClient, AuditWriter, FastAPI],
    private_value: str,
    event_type: str,
    result: str,
    key: str,
    baseline: dict[str, object],
) -> None:
    _, audit, _ = secured
    metadata = dict(baseline)
    metadata[key] = private_value
    with pytest.raises(ValueError):
        audit.record(event_type, ("course-1",), result, metadata)
~~~

- [ ] **Step 6: Append unknown-field and sequence-bound tests**

Append to backend/tests/integration/test_http_security.py:

~~~python


def test_audit_rejects_unknown_fields_and_oversized_sequences(
    secured: tuple[TestClient, AuditWriter, FastAPI],
) -> None:
    _, audit, _ = secured
    with pytest.raises(ValueError):
        audit.record(
            "state_change_succeeded",
            ("course-1",),
            "accepted",
            {"duration_ms": 4, "status_code": 204, "body": "synthetic body"},
        )
    with pytest.raises(ValueError):
        audit.record(
            "state_change_succeeded",
            ("course-1",),
            "accepted",
            {
                "duration_ms": 4,
                "status_code": 204,
                "states": tuple("ready" for _ in range(17)),
            },
        )
    assert all("synthetic body" not in repr(event) for event in audit.events)
~~~

- [ ] **Step 7: Run red**

~~~powershell
$red=Invoke-BoundedNative $PythonExe @("-m","pytest","backend/tests/integration/test_http_security.py","-q") 120
if ($red.ExitCode -eq 0) { throw "T-04C red unexpectedly passed" }
~~~

- [ ] **Step 8: Define the event-specific immutable audit schema**

Create backend/src/projectb/infrastructure/audit.py with only the immutable event types and exact per-event key grammar:

~~~python
from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from types import MappingProxyType

from projectb.application.security import SecurityCode

_OPAQUE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
_SECRET = re.compile(
    r"(?i)(sk-(?:proj-)?[A-Za-z0-9_-]{12,}|"
    r"api[_-]?key|password|secret|private[_-]?key)"
)
_PATH_OR_URL = re.compile(
    r"(?i)(?:^|[\s\"'(])(?:[a-z]:[\\/]|\\\\[^\\/\s]+[\\/]|//[^/\s]+/|/[^/\s]|~(?:[\\/]|$)|[a-z][a-z0-9+.-]*://)"
)
_CONTROL = re.compile(r"[\x00-\x1f\x7f]")
_EVENT_RESULTS = {
    "request_rejected": "rejected",
    "request_failed": "failed",
    "state_change_succeeded": "accepted",
    "provider_action_succeeded": "accepted",
}
_EVENT_ALLOWED = {
    "request_rejected": frozenset({"error_code", "status_code"}),
    "request_failed": frozenset({"method", "status_code"}),
    "state_change_succeeded": frozenset(
        {"duration_ms", "status_code", "count", "states", "course_id", "material_id"}
    ),
    "provider_action_succeeded": frozenset(
        {"duration_ms", "status_code", "mode", "profile_id", "request_id"}
    ),
}
_EVENT_REQUIRED = {
    "request_rejected": frozenset({"error_code", "status_code"}),
    "request_failed": frozenset({"method", "status_code"}),
    "state_change_succeeded": frozenset({"duration_ms", "status_code"}),
    "provider_action_succeeded": frozenset({"duration_ms", "status_code"}),
}
_ID_KEYS = frozenset({"profile_id", "course_id", "material_id", "request_id"})
_METHODS = frozenset({"GET", "HEAD", "OPTIONS", "POST", "PUT", "PATCH", "DELETE", "OTHER"})
_MODES = frozenset({"L", "P", "F"})
_STATES = frozenset({"ready", "not_applicable", "delete_incomplete", "credential_reentered"})
_SECURITY_CODES = frozenset(code.value for code in SecurityCode)
type AuditScalar = str | int
type AuditValue = AuditScalar | tuple[str, ...]


@dataclass(frozen=True)
class AuditEvent:
    event_type: str
    object_ids: tuple[str, ...]
    result: str
    metadata: Mapping[str, AuditValue]
~~~

- [ ] **Step 9: Append audit value validation and the writer**

Append to backend/src/projectb/infrastructure/audit.py:

~~~python
def _reject_private_value(value: object) -> None:
    values = value if isinstance(value, tuple) else (value,)
    for item in values:
        if type(item) is str and (
            _CONTROL.search(item) is not None
            or _SECRET.search(item) is not None
            or _PATH_OR_URL.search(item) is not None
        ):
            raise ValueError(SecurityCode.AUDIT_VALUE_FORBIDDEN.value)


def _freeze_field(event_type: str, key: str, value: object) -> AuditValue:
    _reject_private_value(value)
    if key in {"duration_ms", "count"}:
        if type(value) is int and 0 <= value <= 1_000_000_000:
            return value
    elif key == "status_code":
        if type(value) is int and (
            (event_type == "request_rejected" and value == 403)
            or (event_type == "request_failed" and value == 500)
            or (event_type.endswith("_succeeded") and 200 <= value <= 299)
        ):
            return value
    elif key in _ID_KEYS:
        if type(value) is str and _OPAQUE_ID.fullmatch(value) is not None:
            return value
    elif key == "error_code":
        if type(value) is str and value in _SECURITY_CODES:
            return value
    elif key == "method":
        if type(value) is str and value in _METHODS:
            return value
    elif key == "mode":
        if type(value) is str and value in _MODES:
            return value
    elif key == "states" and isinstance(value, tuple):
        if (
            1 <= len(value) <= 16
            and all(type(item) is str and item in _STATES for item in value)
            and value == tuple(sorted(set(value)))
        ):
            return value
    raise ValueError(SecurityCode.AUDIT_VALUE_FORBIDDEN.value)


class AuditWriter:
    def __init__(self, sink: list[AuditEvent]) -> None:
        self._sink = sink

    @classmethod
    def memory(cls) -> AuditWriter:
        return cls([])

    @property
    def events(self) -> tuple[AuditEvent, ...]:
        return tuple(self._sink)

    def record(
        self,
        event_type: str,
        object_ids: Iterable[str],
        result: str,
        metadata: Mapping[str, object],
    ) -> None:
        if event_type not in _EVENT_RESULTS or result != _EVENT_RESULTS[event_type]:
            raise ValueError(SecurityCode.AUDIT_VALUE_FORBIDDEN.value)
        supplied_ids = tuple(object_ids)
        if len(supplied_ids) > 16 or len(supplied_ids) != len(set(supplied_ids)):
            raise ValueError(SecurityCode.AUDIT_VALUE_FORBIDDEN.value)
        for value in supplied_ids:
            _reject_private_value(value)
            if type(value) is not str or _OPAQUE_ID.fullmatch(value) is None:
                raise ValueError(SecurityCode.AUDIT_VALUE_FORBIDDEN.value)
        frozen_ids = tuple(sorted(supplied_ids))
        keys = frozenset(metadata)
        allowed = _EVENT_ALLOWED[event_type]
        required = _EVENT_REQUIRED[event_type]
        if (
            len(metadata) > 16
            or any(type(key) is not str for key in metadata)
            or not required.issubset(keys)
            or not keys.issubset(allowed)
        ):
            raise ValueError(SecurityCode.AUDIT_FIELD_FORBIDDEN.value)
        frozen = {
            key: _freeze_field(event_type, key, value)
            for key, value in sorted(metadata.items())
        }
        self._sink.append(
            AuditEvent(event_type, frozen_ids, result, MappingProxyType(frozen))
        )
~~~

- [ ] **Step 10: Define middleware actions and request extraction**

Create backend/src/projectb/api/middleware.py:

~~~python
from __future__ import annotations

from collections.abc import Awaitable, Callable
from enum import StrEnum
from time import perf_counter

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.types import ASGIApp

from projectb.application.security import (
    CsrfService,
    RequestMetadata,
    SecurityCode,
    SecurityError,
    TrustedRequestPolicy,
)
from projectb.infrastructure.audit import AuditWriter


class AuditAction(StrEnum):
    STATE_CHANGE = "state_change"
    PROVIDER_ACTION = "provider_action"


def mark_provider_action(request: Request, object_ids: tuple[str, ...]) -> None:
    if len(object_ids) > 16 or any(
        type(value) is not str or not 1 <= len(value) <= 128 for value in object_ids
    ):
        raise ValueError("invalid audit object ids")
    request.scope["projectb.audit_action"] = AuditAction.PROVIDER_ACTION
    request.scope["projectb.audit_object_ids"] = object_ids


def _server_metadata(request: Request) -> tuple[str | None, int | None]:
    server = request.scope.get("server")
    if (
        not isinstance(server, (tuple, list))
        or len(server) != 2
        or type(server[0]) is not str
        or type(server[1]) is not int
    ):
        return None, None
    return server[0], server[1]
~~~

- [ ] **Step 11: Append middleware authorization, auditing, and sanitization**

Append to backend/src/projectb/api/middleware.py:

~~~python


class SecurityMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        *,
        policy: TrustedRequestPolicy,
        csrf: CsrfService,
        audit: AuditWriter,
    ) -> None:
        super().__init__(app)
        self._policy = policy
        self._csrf = csrf
        self._audit = audit

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        server_host, server_port = _server_metadata(request)
        safe_method = (
            request.method.upper()
            if request.method.upper()
            in {"GET", "HEAD", "OPTIONS", "POST", "PUT", "PATCH", "DELETE"}
            else "OTHER"
        )
        started = perf_counter()
        try:
            self._policy.check(
                RequestMetadata(
                    server_host,
                    server_port,
                    request.headers.get("host"),
                    request.headers.get("origin"),
                    request.method,
                )
            )
            if request.method.upper() in {"POST", "PUT", "PATCH", "DELETE"}:
                session_id = request.cookies.get("projectb_session")
                if session_id is None:
                    raise SecurityError(SecurityCode.CSRF_MISSING)
                self._csrf.verify(session_id, request.headers.get("x-csrf-token"))
        except SecurityError as error:
            self._audit.record(
                "request_rejected",
                set(),
                "rejected",
                {"error_code": error.code.value, "status_code": 403},
            )
            return JSONResponse({"error": error.code.value}, status_code=403)
        try:
            response = await call_next(request)
        except Exception:
            self._audit.record(
                "request_failed",
                tuple(),
                "failed",
                {"method": safe_method, "status_code": 500},
            )
            return JSONResponse({"error": "request_failed"}, status_code=500)
        if 200 <= response.status_code < 300 and request.method.upper() in {
            "POST",
            "PUT",
            "PATCH",
            "DELETE",
        }:
            action = request.scope.get("projectb.audit_action", AuditAction.STATE_CHANGE)
            object_ids = request.scope.get("projectb.audit_object_ids", tuple())
            event_type = (
                "provider_action_succeeded"
                if action is AuditAction.PROVIDER_ACTION
                else "state_change_succeeded"
            )
            self._audit.record(
                event_type,
                object_ids if isinstance(object_ids, tuple) else tuple(),
                "accepted",
                {
                    "duration_ms": min(int((perf_counter() - started) * 1000), 1_000_000_000),
                    "status_code": response.status_code,
                },
            )
        return response
~~~

- [ ] **Step 12: Replace the app handoff with the secured factory**

Modify backend/src/projectb/api/app.py to this complete post-T-04C content:

~~~python
from __future__ import annotations

from dataclasses import dataclass

from fastapi import FastAPI

from projectb.api.middleware import SecurityMiddleware
from projectb.application.security import CsrfService, TrustedRequestPolicy
from projectb.infrastructure.audit import AuditWriter


@dataclass(frozen=True)
class AppSecurityProfile:
    bind_host: str = "127.0.0.1"
    port: int = 8765


def create_app(
    profile: AppSecurityProfile | None = None,
    *,
    audit_writer: AuditWriter | None = None,
) -> FastAPI:
    selected = profile or AppSecurityProfile()
    audit = audit_writer or AuditWriter.memory()
    app = FastAPI()
    app.state.csrf_service = CsrfService()
    app.state.security_policy = TrustedRequestPolicy.local(selected.port, selected.bind_host)
    app.state.audit_writer = audit
    app.add_middleware(
        SecurityMiddleware,
        policy=app.state.security_policy,
        csrf=app.state.csrf_service,
        audit=audit,
    )

    @app.get("/api/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app
~~~

- [ ] **Step 13: Run focused green, Ruff, mypy, backend, and canonical tests**

~~~powershell
Invoke-CheckedPython @("-m","pytest","backend/tests/integration/test_http_security.py","-q") 120
Invoke-CheckedPython @("-m","ruff","check","--config","backend/pyproject.toml","backend/src/projectb/api/middleware.py","backend/src/projectb/infrastructure/audit.py","backend/src/projectb/api/app.py","backend/tests/integration/test_http_security.py") 120
Invoke-CheckedPython @("-m","mypy","--config-file","backend/pyproject.toml","backend/src/projectb/api/middleware.py","backend/src/projectb/infrastructure/audit.py","backend/src/projectb/api/app.py","backend/tests/integration/test_http_security.py") 120
Invoke-CheckedPython @("-m","pytest","backend/tests","-q") 300
Invoke-CheckedPython @("scripts/test_all.py") 900
~~~

Expected: each exits 0; hostile requests never enter the probe, successful mutations/provider actions are audited, route exceptions return only `request_failed`, and audit values remain bounded and immutable.

- [ ] **Step 14: Run both reviews**

SPEC review checks AC-07/AC-11/AC-21/AC-22/AC-30 and threats T-09/T-13: single middleware, no route bypass, Host/Origin/CSRF ordering, audit allowlist, error headers, and no feature registration. Quality/security/license review checks middleware order, exception handling, test-only probe scope, CORS absence, sink redaction, and licenses.

- [ ] **Step 15: Stage and scan exact T-04C paths**

~~~powershell
$expected=@("backend/src/projectb/api/middleware.py","backend/src/projectb/infrastructure/audit.py","backend/src/projectb/api/app.py","backend/tests/integration/test_http_security.py")
$stageArgs=@("add","--")+$expected
Invoke-CheckedGit $stageArgs
Assert-ExactStagedPaths $expected
Invoke-CheckedGit @("diff","--cached","--check")
Invoke-CheckedPython @("scripts/scan_secrets.py","--staged","--git-exe",$GitExe) 300
$reviewPacket=Get-PrivateReviewPacket
~~~

- [ ] **Step 16: Validate both private packet/tree-bound review receipts**

~~~powershell
$specReceipt=Assert-ReviewReceipt $env:PROJECTB_SPEC_REVIEW_RECEIPT "SPEC" $reviewPacket.TreeId $reviewPacket.PacketSha256 "T-04C"
$qualityReceipt=Assert-ReviewReceipt $env:PROJECTB_QUALITY_REVIEW_RECEIPT "quality" $reviewPacket.TreeId $reviewPacket.PacketSha256 "T-04C"
if ($specReceipt.reviewer_id -eq $qualityReceipt.reviewer_id) { throw "reviewers must be distinct" }
~~~

- [ ] **Step 17: Recheck the reviewed tree and commit T-04C**

~~~powershell
Assert-ExactStagedPaths $expected
Invoke-CheckedGit @("diff","--cached","--check")
Invoke-CheckedPython @("scripts/scan_secrets.py","--staged","--git-exe",$GitExe) 300
$recheck=Get-PrivateReviewPacket
if ($recheck.TreeId -ne $reviewPacket.TreeId -or $recheck.PacketSha256 -ne $reviewPacket.PacketSha256) { throw "reviewed packet changed" }
Invoke-CheckedGit @("commit","-m","feat(T-04C): wire trust boundary and audit [agent: $env:PROJECTB_AGENT_ID]")
$committedHead=(Invoke-CheckedGit @("rev-parse","HEAD")).Stdout.Trim()
$committedTree=(Invoke-CheckedGit @("rev-parse","HEAD^{tree}")).Stdout.Trim()
if ($committedHead -notmatch "^[0-9a-f]{40}$" -or $committedTree -ne $reviewPacket.TreeId) { throw "committed tree differs from reviewed tree" }
~~~

**Completion standard:** No feature route can mutate state or invoke a provider without the shared request checks and a redacted audit event.

## Task T-05A: Define The Strict ProviderProfile Schema

**Goal:** Reject arbitrary endpoints/plugins/unknown fields and secret-shaped configuration before store or adapter access.

**Files:**
- Create: backend/src/projectb/domain/provider.py
- Test: backend/tests/unit/test_provider_profile.py

**Interfaces:** `ProviderProfile`, `ProfileError`, `validate_provider_profile(payload)`, and the validated profile's `canonical_non_secret_json`, `config_fingerprint`, and `safe_dict` surfaces.

**Dependencies / parallelism:** Requires reviewed T-03C/T-04C and coordinator-recorded G-02A evidence. It precedes T-05B.

**Expected first failure:** projectb.domain.provider is absent.

- [ ] **Step 1: Run the prelude and verify T-03C/T-04C/G-02A evidence**

Stop without reading credentials or installing packages if any required reviewed hash/evidence is absent.

~~~powershell
$owned=@("backend/src/projectb/domain/provider.py","backend/tests/unit/test_provider_profile.py")
Assert-UnitStart -ExpectedUnit "T-05A" -OwnedPaths $owned -ExpectedDependencies @("G-02A","T-03C","T-04C")
~~~

- [ ] **Step 2: Write the failing strict-schema test**

Create backend/tests/unit/test_provider_profile.py:

~~~python
import hashlib

from projectb.domain.provider import ProfileError, ProviderProfile, validate_provider_profile

BASE: dict[str, object] = {
    "profile_id": "profile-1",
    "adapter_id": "openai.reference",
    "model_id": "gpt-5.4-mini-2026-03-17",
    "region": "us",
    "max_output_tokens": 1200,
    "timeout_ms": 20000,
    "daily_budget_usd": "1.00",
    "credential_ref": "cred_openai_1",
    "schema_version": "v1",
}


def test_valid_profile_fingerprints_only_non_secret_fields() -> None:
    result = validate_provider_profile(BASE)
    assert isinstance(result, ProviderProfile)
    assert result.is_error is False
    assert (
        result.config_fingerprint
        == hashlib.sha256(result.canonical_non_secret_json.encode("utf-8")).hexdigest()
    )
    assert "cred_openai_1" not in result.canonical_non_secret_json


def test_endpoint_plugin_secret_and_unknown_fields_are_rejected() -> None:
    cases = (
        ("base_url", "https://example.invalid", "custom_endpoint_forbidden"),
        ("endpoint", "https://example.invalid", "custom_endpoint_forbidden"),
        ("plugin", "synthetic.module", "custom_endpoint_forbidden"),
        ("api_key", "synthetic-value", "secret_field"),
        ("token", "synthetic-value", "secret_field"),
        ("unknown", "value", "unknown_field"),
    )
    for field, value, code in cases:
        payload = dict(BASE)
        payload[field] = value
        result = validate_provider_profile(payload)
        assert isinstance(result, ProfileError)
        assert result.code == code
        assert value not in repr(result)


def test_wrong_types_bad_adapter_and_bad_reference_fail_without_coercion() -> None:
    for field, value, code in (
        ("timeout_ms", "20000", "invalid_value"),
        ("max_output_tokens", True, "invalid_value"),
        ("daily_budget_usd", 1.0, "invalid_value"),
        ("adapter_id", "mock", "unsupported_adapter"),
        ("credential_ref", "key-value", "invalid_credential_ref"),
    ):
        payload = dict(BASE)
        payload[field] = value
        result = validate_provider_profile(payload)
        assert isinstance(result, ProfileError)
        assert result.code == code


def test_lengths_controls_decimal_scale_and_numeric_bounds_fail_before_hashing() -> None:
    cases: tuple[tuple[str, object], ...] = (
        ("profile_id", "p" * 65),
        ("model_id", "m" * 97),
        ("model_id", "model\nname"),
        ("region", "u\x00s"),
        ("daily_budget_usd", "1.001"),
        ("daily_budget_usd", "1e2"),
        ("daily_budget_usd", "NaN"),
        ("daily_budget_usd", "1000.01"),
        ("max_output_tokens", 128001),
        ("timeout_ms", 120001),
    )
    for field, value in cases:
        payload = dict(BASE)
        payload[field] = value
        result = validate_provider_profile(payload)
        assert isinstance(result, ProfileError)
        assert result.code == "invalid_value"


def test_malformed_field_names_are_rejected_without_echo() -> None:
    for key in ("x" * 65, "bad\nfield", "密钥"):
        payload = dict(BASE)
        payload[key] = "synthetic"
        result = validate_provider_profile(payload)
        assert isinstance(result, ProfileError)
        assert result.code == "invalid_field_name"
        assert key not in repr(result)
~~~

- [ ] **Step 3: Run red**

~~~powershell
$red=Invoke-BoundedNative $PythonExe @("-m","pytest","backend/tests/unit/test_provider_profile.py","-q") 120
if ($red.ExitCode -eq 0 -or ($red.Stdout+$red.Stderr) -notmatch "provider") { throw "T-05A red evidence invalid" }
~~~

- [ ] **Step 4: Implement the strict parser**

Create backend/src/projectb/domain/provider.py:

~~~python
from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Mapping
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Final

_IDENTITY: Final[re.Pattern[str]] = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{1,63}$")
_CREDENTIAL: Final[re.Pattern[str]] = re.compile(r"^cred_[A-Za-z0-9][A-Za-z0-9._-]{7,62}$")
_MODEL: Final[re.Pattern[str]] = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,95}$")
_BUDGET: Final[re.Pattern[str]] = re.compile(r"^(?:0|[1-9][0-9]{0,3})(?:\.[0-9]{1,2})?$")
_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "profile_id",
        "adapter_id",
        "model_id",
        "region",
        "max_output_tokens",
        "timeout_ms",
        "daily_budget_usd",
        "credential_ref",
        "schema_version",
    }
)
_SECRET_FIELDS: Final[frozenset[str]] = frozenset(
    {"api_key", "token", "password", "secret", "private_key", "access_key", "client_secret"}
)
_ENDPOINT_FIELDS: Final[frozenset[str]] = frozenset(
    {"base_url", "endpoint", "url", "plugin", "module", "callable", "adapter_path", "tool"}
)
~~~

- [ ] **Step 5: Append immutable profile and safe serialization types**

Append to backend/src/projectb/domain/provider.py:

~~~python


@dataclass(frozen=True)
class ProfileError:
    code: str
    field: str | None = None
    is_error: bool = True

    def __repr__(self) -> str:
        return f"ProfileError(code={self.code!r}, field={self.field!r})"


@dataclass(frozen=True)
class ProviderProfile:
    profile_id: str
    adapter_id: str
    model_id: str
    region: str
    max_output_tokens: int
    timeout_ms: int
    daily_budget_usd: Decimal
    credential_ref: str
    schema_version: str
    is_error: bool = False

    @property
    def canonical_non_secret_json(self) -> str:
        return json.dumps(
            {
                "adapter_id": self.adapter_id,
                "daily_budget_usd": format(self.daily_budget_usd, "f"),
                "max_output_tokens": self.max_output_tokens,
                "model_id": self.model_id,
                "profile_id": self.profile_id,
                "region": self.region,
                "schema_version": self.schema_version,
                "timeout_ms": self.timeout_ms,
            },
            ensure_ascii=True,
            separators=(",", ":"),
            sort_keys=True,
            allow_nan=False,
        )

    @property
    def config_fingerprint(self) -> str:
        return hashlib.sha256(self.canonical_non_secret_json.encode("utf-8")).hexdigest()

    def safe_dict(self) -> dict[str, object]:
        return {
            "profile_id": self.profile_id,
            "adapter_id": self.adapter_id,
            "model_id": self.model_id,
            "region": self.region,
            "max_output_tokens": self.max_output_tokens,
            "timeout_ms": self.timeout_ms,
            "daily_budget_usd": format(self.daily_budget_usd, "f"),
            "credential_ref": self.credential_ref,
            "schema_version": self.schema_version,
            "config_fingerprint": self.config_fingerprint,
        }

    def __repr__(self) -> str:
        return (
            f"ProviderProfile(profile_id={self.profile_id!r}, "
            f"adapter_id={self.adapter_id!r}, credential_ref=<ref>)"
        )


def _error(code: str, field: str | None = None) -> ProfileError:
    return ProfileError(code, field)
~~~

- [ ] **Step 6: Append strict validation and canonical construction**

Append to backend/src/projectb/domain/provider.py:

~~~python


def validate_provider_profile(payload: Mapping[str, object]) -> ProviderProfile | ProfileError:
    if not isinstance(payload, Mapping) or len(payload) > 16:
        return _error("invalid_value")
    for key in payload:
        if (
            type(key) is not str
            or not 1 <= len(key) <= 64
            or not key.isascii()
            or any(ord(character) < 33 or ord(character) > 126 for character in key)
        ):
            return _error("invalid_field_name")
    keys = set(payload)
    unknown = keys - _FIELDS
    if unknown:
        field = sorted(unknown)[0]
        if field in _SECRET_FIELDS:
            return _error("secret_field", field)
        if field in _ENDPOINT_FIELDS:
            return _error("custom_endpoint_forbidden", field)
        return _error("unknown_field", field)
    missing = _FIELDS - keys
    if missing:
        return _error("missing_field", sorted(missing)[0])
    text_fields = (
        "profile_id",
        "adapter_id",
        "model_id",
        "region",
        "credential_ref",
        "schema_version",
    )
    if any(type(payload[field]) is not str for field in text_fields):
        return _error("invalid_value")
    text_values = tuple(str(payload[field]) for field in text_fields)
    if any(
        not value.isascii()
        or any(ord(character) < 32 or ord(character) > 126 for character in value)
        for value in text_values
    ):
        return _error("invalid_value")
    if _IDENTITY.fullmatch(str(payload["profile_id"])) is None:
        return _error("invalid_value", "profile_id")
    if payload["adapter_id"] != "openai.reference":
        return _error("unsupported_adapter", "adapter_id")
    if _MODEL.fullmatch(str(payload["model_id"])) is None:
        return _error("invalid_value", "model_id")
    if payload["region"] not in {"us", "global"} or payload["schema_version"] != "v1":
        return _error("invalid_value")
    if _CREDENTIAL.fullmatch(str(payload["credential_ref"])) is None:
        return _error("invalid_credential_ref", "credential_ref")
    if (
        type(payload["max_output_tokens"]) is not int
        or not 1 <= payload["max_output_tokens"] <= 128000
    ):
        return _error("invalid_value", "max_output_tokens")
    if type(payload["timeout_ms"]) is not int or not 1000 <= payload["timeout_ms"] <= 120000:
        return _error("invalid_value", "timeout_ms")
    if type(payload["daily_budget_usd"]) is not str:
        return _error("invalid_value", "daily_budget_usd")
    if _BUDGET.fullmatch(payload["daily_budget_usd"]) is None:
        return _error("invalid_value", "daily_budget_usd")
    try:
        budget = Decimal(payload["daily_budget_usd"])
    except (InvalidOperation, ValueError):
        return _error("invalid_value", "daily_budget_usd")
    if not budget.is_finite() or budget < Decimal("0") or budget > Decimal("1000"):
        return _error("invalid_value", "daily_budget_usd")
    budget = budget.quantize(Decimal("0.01"))
    return ProviderProfile(
        str(payload["profile_id"]),
        str(payload["adapter_id"]),
        str(payload["model_id"]),
        str(payload["region"]),
        payload["max_output_tokens"],
        payload["timeout_ms"],
        budget,
        str(payload["credential_ref"]),
        str(payload["schema_version"]),
    )
~~~

- [ ] **Step 7: Run green, Ruff, mypy, backend, and canonical tests**

~~~powershell
Invoke-CheckedPython @("-m","pytest","backend/tests/unit/test_provider_profile.py","-q") 120
Invoke-CheckedPython @("-m","ruff","check","--config","backend/pyproject.toml","backend/src/projectb/domain/provider.py","backend/tests/unit/test_provider_profile.py") 120
Invoke-CheckedPython @("-m","mypy","--config-file","backend/pyproject.toml","backend/src/projectb/domain/provider.py","backend/tests/unit/test_provider_profile.py") 120
Invoke-CheckedPython @("-m","pytest","backend/tests","-q") 300
Invoke-CheckedPython @("scripts/test_all.py") 900
~~~

- [ ] **Step 8: Run both reviews**

SPEC review checks AC-30/AC-38 and threats T-06/T-12: exact fields, unknown/secret/endpoint/plugin rejection before calls, non-secret fingerprint, schema version, and exact identity regex. Quality/security/license review checks strict types, Decimal bounds, Unicode/control characters, repr redaction, canonical JSON, and G-02A license evidence.

- [ ] **Step 9: Stage, scan, and capture the private T-05A packet**

~~~powershell
$expected=@("backend/src/projectb/domain/provider.py","backend/tests/unit/test_provider_profile.py")
$reviewPacket=Start-UnitReview $expected
~~~

- [ ] **Step 10: Validate both T-05A review receipts**

~~~powershell
$receipts=Assert-UnitReviewReceipts $reviewPacket "T-05A"
~~~

- [ ] **Step 11: Recheck and commit the reviewed T-05A tree**

~~~powershell
Complete-ReviewedUnit $expected $reviewPacket "feat(T-05A): define strict provider profile [agent: $env:PROJECTB_AGENT_ID]"
~~~

**Completion standard:** Ordinary config cannot select arbitrary code/network targets or carry a secret value.

## Task T-05B: Implement The WinVault SecretStore Adapter

**Goal:** Put secret values only behind the verified Windows Credential Manager adapter and expose status/ref-only ordinary outputs.

**Files:**
- Create: backend/src/projectb/infrastructure/keyring_store.py
- Test: backend/tests/integration/test_win_vault_store.py

**Interfaces:** `SecretStore`, `SecretValue`, `SecretHandle`, `CredentialStatus`, `SecretStoreError`, `WinVaultSecretStore.from_system`, and the private deterministic `_for_test_backend` seam. There is no public arbitrary production-backend constructor.

**Dependencies / parallelism:** Requires reviewed T-05A and keyring 25.7.0 evidence. It precedes T-05C.

**Expected first failure:** keyring_store types are absent.

- [ ] **Step 1: Verify predecessor and evidence bindings**

~~~powershell
$owned=@("backend/src/projectb/infrastructure/keyring_store.py","backend/tests/integration/test_win_vault_store.py")
Assert-UnitStart -ExpectedUnit "T-05B" -OwnedPaths $owned -ExpectedDependencies @("T-05A")
~~~

- [ ] **Step 2: Create the WinVault test backend and basic boundary tests**

Create backend/tests/integration/test_win_vault_store.py:

~~~python
from datetime import UTC, datetime, timedelta

import keyring
import pytest
from keyring.backends.Windows import WinVaultKeyring
from projectb.infrastructure.keyring_store import (
    CredentialStatus,
    SecretStoreError,
    SecretValue,
    WinVaultSecretStore,
)


class FakeWinVault:
    def __init__(self) -> None:
        self.values: dict[tuple[str, str], str] = {}

    def set_password(self, service: str, ref: str, value: str) -> None:
        self.values[(service, ref)] = value

    def get_password(self, service: str, ref: str) -> str | None:
        return self.values.get((service, ref))

    def delete_password(self, service: str, ref: str) -> None:
        self.values.pop((service, ref), None)


def test_test_backend_contract_never_returns_secret_in_status_or_repr() -> None:
    store = WinVaultSecretStore._for_test_backend(FakeWinVault())
    store.set("cred_openai_1", SecretValue.from_text("synthetic-secret"))
    status = store.status("cred_openai_1")
    assert isinstance(status, CredentialStatus)
    assert status.configured is True
    assert "synthetic-secret" not in repr(status)
    handle = store.resolve("cred_openai_1")
    assert handle.reveal() == "synthetic-secret"
    assert "synthetic-secret" not in repr(handle)
    handle.close()
    with pytest.raises(SecretStoreError) as closed:
        handle.reveal()
    assert closed.value.code == "credential_handle_closed"


def test_clear_and_missing_resolution_fail_closed() -> None:
    store = WinVaultSecretStore._for_test_backend(FakeWinVault())
    store.set("cred_openai_1", SecretValue.from_text("synthetic-secret"))
    store.clear("cred_openai_1")
    assert store.status("cred_openai_1").configured is False
    with pytest.raises(SecretStoreError) as error:
        store.resolve("cred_openai_1")
    assert error.value.code == "credential_unavailable"
~~~

- [ ] **Step 3: Append production-identity, expiry, and cause-redaction tests**

Append to backend/tests/integration/test_win_vault_store.py:

~~~python


def test_system_construction_requires_the_actual_winvault_type(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    actual = WinVaultKeyring()  # type: ignore[no-untyped-call]
    monkeypatch.setattr(keyring, "get_keyring", lambda: actual)
    store = WinVaultSecretStore.from_system()
    assert store.backend_identity == "keyring.backends.Windows.WinVaultKeyring"

    Spoof = type(
        "WinVaultKeyring",
        (FakeWinVault,),
        {"__module__": "keyring.backends.Windows"},
    )
    monkeypatch.setattr(keyring, "get_keyring", lambda: Spoof())
    with pytest.raises(SecretStoreError) as error:
        WinVaultSecretStore.from_system()
    assert error.value.code == "backend_unavailable"


def test_resolved_handle_expires_within_sixty_seconds() -> None:
    now = datetime(2026, 7, 23, tzinfo=UTC)
    store = WinVaultSecretStore._for_test_backend(FakeWinVault(), clock=lambda: now)
    store.set("cred_openai_1", SecretValue.from_text("synthetic-secret"))
    assert store.resolve("cred_openai_1").expires_at <= now + timedelta(seconds=60)


def test_backend_exception_cause_is_suppressed_and_secret_is_not_rendered() -> None:
    class ExplodingBackend(FakeWinVault):
        def get_password(self, service: str, ref: str) -> str | None:
            raise RuntimeError("synthetic-secret-in-backend-cause")

    store = WinVaultSecretStore._for_test_backend(ExplodingBackend())
    with pytest.raises(SecretStoreError) as error:
        store.resolve("cred_openai_1")
    assert error.value.code == "credential_unavailable"
    assert error.value.__cause__ is None
    assert error.value.__suppress_context__ is True
    assert "synthetic-secret-in-backend-cause" not in str(error.value)
    assert "synthetic-secret-in-backend-cause" not in repr(error.value)
~~~

- [ ] **Step 4: Run red**

~~~powershell
$red=Invoke-BoundedNative $PythonExe @("-m","pytest","backend/tests/integration/test_win_vault_store.py","-q") 120
if ($red.ExitCode -eq 0) { throw "T-05B red unexpectedly passed" }
~~~

- [ ] **Step 5: Define secret values, handles, status, and store protocol**

Create backend/src/projectb/infrastructure/keyring_store.py:

~~~python
from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Protocol

_REF = re.compile(r"^cred_[A-Za-z0-9][A-Za-z0-9._-]{7,62}$")
_SERVICE = "ProjectB"


class KeyringBackend(Protocol):
    def set_password(self, service: str, ref: str, value: str) -> None:
        raise NotImplementedError

    def get_password(self, service: str, ref: str) -> str | None:
        raise NotImplementedError

    def delete_password(self, service: str, ref: str) -> None:
        raise NotImplementedError


class SecretStoreError(Exception):
    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


@dataclass(frozen=True)
class SecretValue:
    _value: str

    @classmethod
    def from_text(cls, value: str) -> SecretValue:
        if type(value) is not str or not 1 <= len(value) <= 8192 or "\x00" in value:
            raise SecretStoreError("invalid_secret")
        return cls(value)

    def reveal(self) -> str:
        return self._value

    def __repr__(self) -> str:
        return "SecretValue(<redacted>)"


class SecretHandle:
    __slots__ = ("_value", "expires_at", "clock")

    def __init__(self, value: str, expires_at: datetime, clock: Callable[[], datetime]) -> None:
        self._value: str | None = value
        self.expires_at = expires_at
        self.clock = clock

    def reveal(self) -> str:
        if self._value is None:
            raise SecretStoreError("credential_handle_closed")
        if self.clock() >= self.expires_at:
            self.close()
            raise SecretStoreError("credential_handle_expired")
        return self._value

    def close(self) -> None:
        self._value = None

    def __repr__(self) -> str:
        return f"SecretHandle(expires_at={self.expires_at.isoformat()})"


@dataclass(frozen=True)
class CredentialStatus:
    configured: bool
    checked_at: datetime
    error_code: str | None = None


class SecretStore(Protocol):
    def set(self, credential_ref: str, value: SecretValue) -> None:
        raise NotImplementedError

    def status(self, credential_ref: str) -> CredentialStatus:
        raise NotImplementedError

    def clear(self, credential_ref: str) -> None:
        raise NotImplementedError

    def resolve(self, credential_ref: str) -> SecretHandle:
        raise NotImplementedError
~~~

- [ ] **Step 6: Append the sealed WinVault implementation**

Append to backend/src/projectb/infrastructure/keyring_store.py:

~~~python


class WinVaultSecretStore:
    def __init__(
        self,
        backend: KeyringBackend,
        *,
        clock: Callable[[], datetime],
    ) -> None:
        self._backend = backend
        self._clock = clock

    @property
    def backend_identity(self) -> str:
        return f"{type(self._backend).__module__}.{type(self._backend).__name__}"

    @classmethod
    def from_system(cls) -> WinVaultSecretStore:
        try:
            import keyring
            from keyring.backends.Windows import WinVaultKeyring

            backend = keyring.get_keyring()
        except Exception:
            raise SecretStoreError("backend_unavailable") from None
        if type(backend) is not WinVaultKeyring:
            raise SecretStoreError("backend_unavailable")
        return cls(backend, clock=lambda: datetime.now(UTC))

    @classmethod
    def _for_test_backend(
        cls,
        backend: KeyringBackend,
        *,
        clock: Callable[[], datetime] | None = None,
    ) -> WinVaultSecretStore:
        return cls(backend, clock=clock or (lambda: datetime.now(UTC)))

    @staticmethod
    def _validate_ref(credential_ref: str) -> None:
        if _REF.fullmatch(credential_ref) is None:
            raise SecretStoreError("invalid_credential_ref")

    def set(self, credential_ref: str, value: SecretValue) -> None:
        self._validate_ref(credential_ref)
        if not isinstance(value, SecretValue):
            raise SecretStoreError("invalid_secret")
        try:
            self._backend.set_password(_SERVICE, credential_ref, value.reveal())
        except Exception:
            raise SecretStoreError("store_unavailable") from None

    def status(self, credential_ref: str) -> CredentialStatus:
        self._validate_ref(credential_ref)
        try:
            configured = self._backend.get_password(_SERVICE, credential_ref) is not None
        except Exception:
            return CredentialStatus(False, self._clock(), "store_unavailable")
        return CredentialStatus(configured, self._clock())

    def clear(self, credential_ref: str) -> None:
        self._validate_ref(credential_ref)
        try:
            self._backend.delete_password(_SERVICE, credential_ref)
        except Exception:
            raise SecretStoreError("store_unavailable") from None

    def resolve(self, credential_ref: str) -> SecretHandle:
        self._validate_ref(credential_ref)
        try:
            value = self._backend.get_password(_SERVICE, credential_ref)
        except Exception:
            raise SecretStoreError("credential_unavailable") from None
        if value is None:
            raise SecretStoreError("credential_unavailable")
        now = self._clock()
        return SecretHandle(value, now + timedelta(seconds=60), self._clock)
~~~

- [ ] **Step 7: Run focused green and boundary regressions**

~~~powershell
Invoke-CheckedPython @("-m","pytest","backend/tests/integration/test_win_vault_store.py","-q") 120
Invoke-CheckedPython @("-m","ruff","check","--config","backend/pyproject.toml","backend/src/projectb/infrastructure/keyring_store.py","backend/tests/integration/test_win_vault_store.py") 120
Invoke-CheckedPython @("-m","mypy","--config-file","backend/pyproject.toml","backend/src/projectb/infrastructure/keyring_store.py","backend/tests/integration/test_win_vault_store.py") 120
Invoke-CheckedPython @("-m","pytest","backend/tests","-q") 300
Invoke-CheckedPython @("scripts/test_all.py") 900
~~~

- [ ] **Step 8: Run both reviews**

SPEC review checks AC-07/AC-40 and threats T-06/T-19: WinVault production identity, no .env fallback, status/ref-only output, short handle lifetime, clear behavior, and no browser/SQLite/log value. Quality/security/license review checks backend selection, exception redaction, memory lifetime, Windows packaging behavior, test-only injection isolation, keyring license, and test fixtures.

- [ ] **Step 9: Stage, scan, and capture the private T-05B packet**

~~~powershell
$expected=@("backend/src/projectb/infrastructure/keyring_store.py","backend/tests/integration/test_win_vault_store.py")
$reviewPacket=Start-UnitReview $expected
~~~

- [ ] **Step 10: Validate both T-05B review receipts**

~~~powershell
$receipts=Assert-UnitReviewReceipts $reviewPacket "T-05B"
~~~

- [ ] **Step 11: Recheck and commit the reviewed T-05B tree**

~~~powershell
Complete-ReviewedUnit $expected $reviewPacket "feat(T-05B): add WinVault secret store [agent: $env:PROJECTB_AGENT_ID]"
~~~

**Completion standard:** Secret values exist only inside WinVault and one bounded adapter handle.

## Task T-05C: Coordinate Credential Lifecycle And Forced Clear

**Goal:** Provide hidden configure/status/update/clear behavior and fail closed after forced credential removal.

**Files:**
- Create: backend/src/projectb/application/credentials.py
- Test: backend/tests/unit/test_credentials.py
- Test: backend/tests/integration/test_credential_boundary.py

**Interfaces:** `CredentialService.configure`, `status`, `clear`, `resume`, and `resolve_for_call`; `CredentialStatusView`; `ClearResult`; `CredentialLifecycleState`; `CredentialStateRepository`; `CredentialRepositoryError`; `ReconciliationTarget`; `ReconciliationEvidence`; and `RemoteWorkCoordinator`.

**Dependencies / parallelism:** Requires reviewed T-03C/T-04C/T-05A/T-05B. Before dispatch, T-03C must publish an owner-scoped authoritative adapter whose `CredentialStateRepository.recover` is one durable database transaction: compare lifecycle generation, load exact persisted reconciliation evidence, compare profile/object/object-version/evidence-version, mark the reconciliation object remotely resumable, and replace lifecycle state with `ready`, or commit none of those writes. This task may not add a migration, split recovery across repositories/callbacks, or silently substitute an in-memory production store. `StateRepository` below is a test-only transaction model. T-06/T-07 consume this interface.

**Expected first failure:** CredentialService is absent.

- [ ] **Step 1: Verify predecessor hashes**

~~~powershell
$owned=@("backend/src/projectb/application/credentials.py","backend/tests/unit/test_credentials.py","backend/tests/integration/test_credential_boundary.py")
Assert-UnitStart -ExpectedUnit "T-05C" -OwnedPaths $owned -ExpectedDependencies @("T-03C","T-04C","T-05A","T-05B")
~~~

Stop unless the authoritative G-04 row names reviewed T-03C/T-04C/T-05A/T-05B dependency commits and the reviewed T-03C contract exposes the atomic recovery transaction above.

- [ ] **Step 2: Create credential test doubles**

Create backend/tests/unit/test_credentials.py with imports, a fake secret store, and a coordinator that exposes only a reconciliation target and fail-closed unavailability marking:

~~~python
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest
from projectb.application.credentials import (
    CredentialLifecycleState,
    CredentialRepositoryError,
    CredentialService,
    ReconciliationEvidence,
    ReconciliationTarget,
)
from projectb.domain.provider import ProviderProfile
from projectb.infrastructure.keyring_store import (
    CredentialStatus,
    SecretHandle,
    SecretStoreError,
    SecretValue,
)


@dataclass
class FakeStore:
    values: dict[str, str]

    def set(self, ref: str, value: SecretValue) -> None:
        self.values[ref] = value.reveal()

    def status(self, ref: str) -> CredentialStatus:
        return CredentialStatus(ref in self.values, datetime.now(UTC))

    def clear(self, ref: str) -> None:
        self.values.pop(ref, None)

    def resolve(self, ref: str) -> SecretHandle:
        if ref not in self.values:
            raise SecretStoreError("credential_unavailable")
        now = datetime.now(UTC)
        return SecretHandle(self.values[ref], now + timedelta(seconds=30), lambda: now)


class Coordinator:
    def __init__(self, target: ReconciliationTarget | None) -> None:
        self.target = target
        self.marked: list[ReconciliationTarget] = []

    def reconciliation_target(self, profile_id: str) -> ReconciliationTarget | None:
        if self.target is None or self.target.profile_id != profile_id:
            return None
        return self.target

    def mark_credential_unavailable(self, target: ReconciliationTarget) -> None:
        self.marked.append(target)
~~~

- [ ] **Step 3: Append the transactional repository test model**

Append to backend/tests/unit/test_credentials.py:

~~~python


class StateRepository:
    def __init__(self) -> None:
        self.values: dict[str, CredentialLifecycleState] = {}
        self.evidence: dict[str, ReconciliationEvidence] = {}
        self.remote_resumable: dict[tuple[str, str], int] = {}
        self.fail_recovery = False

    def get(self, profile_id: str) -> CredentialLifecycleState | None:
        return self.values.get(profile_id)

    def put(
        self,
        state: CredentialLifecycleState,
        expected_generation: int | None,
    ) -> CredentialLifecycleState:
        current = self.values.get(state.profile_id)
        current_generation = None if current is None else current.generation
        if current_generation != expected_generation:
            raise CredentialRepositoryError("stale_credential_state")
        self.values[state.profile_id] = state
        return state

    def recover(
        self,
        profile_id: str,
        expected_generation: int,
        evidence_id: str,
        reconciliation_object_id: str,
        reconciliation_object_version: int,
        evidence_version: int,
    ) -> CredentialLifecycleState:
        current = self.values.get(profile_id)
        evidence = self.evidence.get(evidence_id)
        if (
            current is None
            or current.generation != expected_generation
            or not current.resume_required
            or current.reconciliation_object_id != reconciliation_object_id
            or current.reconciliation_object_version != reconciliation_object_version
            or evidence is None
            or evidence.profile_id != profile_id
            or evidence.reconciliation_object_id != reconciliation_object_id
            or evidence.reconciliation_object_version != reconciliation_object_version
            or evidence.evidence_version != evidence_version
        ):
            raise CredentialRepositoryError("reconciliation_required")
        next_state = CredentialLifecycleState(
            profile_id,
            current.generation + 1,
            "ready",
            False,
            evidence.evidence_id,
            reconciliation_object_id,
            reconciliation_object_version,
        )
        next_remote = dict(self.remote_resumable)
        next_remote[(profile_id, reconciliation_object_id)] = reconciliation_object_version
        if self.fail_recovery:
            raise CredentialRepositoryError("recovery_commit_failed")
        self.values[profile_id] = next_state
        self.remote_resumable = next_remote
        return next_state
~~~

- [ ] **Step 4: Append credential profiles and the blocked-recovery fixture**

Append to backend/tests/unit/test_credentials.py:

~~~python


PROFILE = ProviderProfile(
    "profile-1",
    "openai.reference",
    "gpt-5.4-mini-2026-03-17",
    "us",
    1200,
    20000,
    Decimal("1.00"),
    "cred_openai_1",
    "v1",
)

TARGET = ReconciliationTarget("profile-1", "response-object-1", 3)


def blocked_reentered_service() -> tuple[
    CredentialService,
    StateRepository,
    FakeStore,
    Coordinator,
]:
    repository = StateRepository()
    store = FakeStore({"cred_openai_1": "synthetic-secret"})
    coordinator = Coordinator(TARGET)
    first = CredentialService(store, {"profile-1": PROFILE}, coordinator, repository)
    assert first.clear("profile-1", force=True).status == "forced"
    restarted = CredentialService(store, {"profile-1": PROFILE}, coordinator, repository)
    restarted.configure("profile-1", "synthetic-new-secret")
    return restarted, repository, store, coordinator
~~~

- [ ] **Step 5: Append configure and clear boundary tests**

Append to backend/tests/unit/test_credentials.py:

~~~python


def test_status_never_returns_secret_and_resolve_is_only_handle_boundary() -> None:
    service = CredentialService(
        FakeStore({}), {"profile-1": PROFILE}, Coordinator(None), StateRepository()
    )
    status = service.configure("profile-1", "synthetic-secret")
    assert status.configured is True
    assert "synthetic-secret" not in repr(status)
    assert service.resolve_for_call("profile-1").reveal() == "synthetic-secret"


def test_nonforced_clear_blocks_active_remote_work() -> None:
    service = CredentialService(
        FakeStore({"cred_openai_1": "synthetic-secret"}),
        {"profile-1": PROFILE},
        Coordinator(TARGET),
        StateRepository(),
    )
    result = service.clear("profile-1")
    assert result.status == "blocked"
    assert service.status("profile-1").configured is True


def test_forced_clear_and_restart_preserve_exact_blocked_target() -> None:
    restarted, repository, _, coordinator = blocked_reentered_service()
    status = restarted.status("profile-1")
    assert status.configured is True
    assert status.resume_required is True
    assert status.remote_state == "credential_reentered"
    assert status.reconciliation_object_id == "response-object-1"
    assert status.reconciliation_object_version == 3
    assert coordinator.marked == [TARGET]
    with pytest.raises(SecretStoreError) as blocked:
        restarted.resolve_for_call("profile-1")
    assert blocked.value.code == "resume_required"
    assert repository.remote_resumable == {}
~~~

- [ ] **Step 6: Append evidence identity and atomic-failure tests**

Append to backend/tests/unit/test_credentials.py:

~~~python
def test_resume_rejects_cross_profile_and_wrong_object_version() -> None:
    service, repository, _, _ = blocked_reentered_service()
    repository.evidence["cross-profile"] = ReconciliationEvidence(
        "cross-profile", "profile-2", "response-object-1", 3, 1, "provider_deleted", True
    )
    repository.evidence["wrong-version"] = ReconciliationEvidence(
        "wrong-version", "profile-1", "response-object-1", 4, 1, "provider_deleted", True
    )
    for evidence_id in ("cross-profile", "wrong-version"):
        with pytest.raises(SecretStoreError) as rejected:
            service.resume("profile-1", evidence_id)
        assert rejected.value.code == "reconciliation_required"
    assert repository.remote_resumable == {}


def test_recovery_persistence_failure_is_atomic_and_restart_stays_blocked() -> None:
    service, repository, store, coordinator = blocked_reentered_service()
    repository.evidence["reconcile-1"] = ReconciliationEvidence(
        "reconcile-1", "profile-1", "response-object-1", 3, 1, "provider_deleted", True
    )
    repository.fail_recovery = True
    with pytest.raises(SecretStoreError) as failed:
        service.resume("profile-1", "reconcile-1")
    assert failed.value.code == "recovery_commit_failed"
    assert repository.remote_resumable == {}
    assert repository.get("profile-1").remote_state == "credential_reentered"  # type: ignore[union-attr]

    restarted = CredentialService(store, {"profile-1": PROFILE}, coordinator, repository)
    with pytest.raises(SecretStoreError) as blocked:
        restarted.resolve_for_call("profile-1")
    assert blocked.value.code == "resume_required"

    repository.fail_recovery = False
    resumed = restarted.resume("profile-1", "reconcile-1")
    assert resumed.resume_required is False
    assert resumed.remote_state == "ready"
    assert repository.remote_resumable == {("profile-1", "response-object-1"): 3}
    assert restarted.resolve_for_call("profile-1").reveal() == "synthetic-new-secret"
    assert all("synthetic-new-secret" not in repr(state) for state in repository.values.values())
~~~

- [ ] **Step 7: Create the validation-before-boundary integration test**

Create backend/tests/integration/test_credential_boundary.py:

~~~python
from projectb.domain.provider import ProfileError, validate_provider_profile


def test_bad_profile_fails_before_store_or_network_resolution() -> None:
    calls = 0

    def forbidden_resolve() -> None:
        nonlocal calls
        calls += 1

    payload: dict[str, object] = {
        "profile_id": "profile-1",
        "adapter_id": "openai.reference",
        "model_id": "gpt-5.4-mini-2026-03-17",
        "region": "us",
        "max_output_tokens": 1200,
        "timeout_ms": 20000,
        "daily_budget_usd": "1.00",
        "credential_ref": "cred_openai_1",
        "schema_version": "v1",
        "base_url": "https://example.invalid",
    }
    result = validate_provider_profile(payload)
    if not isinstance(result, ProfileError):
        forbidden_resolve()
    assert isinstance(result, ProfileError)
    assert result.code == "custom_endpoint_forbidden"
    assert calls == 0
~~~

- [ ] **Step 8: Run red**

~~~powershell
$red=Invoke-BoundedNative $PythonExe @("-m","pytest","backend/tests/unit/test_credentials.py","backend/tests/integration/test_credential_boundary.py","-q") 120
if ($red.ExitCode -eq 0) { throw "T-05C red unexpectedly passed" }
~~~

- [ ] **Step 9: Define reconciliation identity and repository errors**

Create backend/src/projectb/application/credentials.py with exact target/evidence identity and stable repository errors:

~~~python
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Protocol

from projectb.domain.provider import ProfileError, ProviderProfile, validate_provider_profile
from projectb.infrastructure.keyring_store import (
    SecretHandle,
    SecretStore,
    SecretStoreError,
    SecretValue,
)


class CredentialRepositoryError(Exception):
    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


@dataclass(frozen=True)
class ReconciliationTarget:
    profile_id: str
    reconciliation_object_id: str
    reconciliation_object_version: int

    def __post_init__(self) -> None:
        if (
            not 1 <= len(self.profile_id) <= 64
            or not 1 <= len(self.reconciliation_object_id) <= 128
            or not 1 <= self.reconciliation_object_version <= 2_147_483_647
        ):
            raise ValueError("invalid_reconciliation_target")


@dataclass(frozen=True)
class ReconciliationEvidence:
    evidence_id: str
    profile_id: str
    reconciliation_object_id: str
    reconciliation_object_version: int
    evidence_version: int
    result: str
    complete: bool

    def __post_init__(self) -> None:
        if (
            not 1 <= len(self.evidence_id) <= 128
            or not 1 <= len(self.profile_id) <= 64
            or not 1 <= len(self.reconciliation_object_id) <= 128
            or not 1 <= self.reconciliation_object_version <= 2_147_483_647
            or self.evidence_version != 1
            or self.result not in {"provider_deleted", "provider_expired"}
            or self.complete is not True
        ):
            raise ValueError("invalid_reconciliation_evidence")


class RemoteWorkCoordinator(Protocol):
    def reconciliation_target(self, profile_id: str) -> ReconciliationTarget | None:
        raise NotImplementedError

    def mark_credential_unavailable(self, target: ReconciliationTarget) -> None:
        raise NotImplementedError
~~~

- [ ] **Step 10: Append lifecycle state and the atomic repository contract**

Append to backend/src/projectb/application/credentials.py:

~~~python


@dataclass(frozen=True)
class CredentialLifecycleState:
    profile_id: str
    generation: int
    remote_state: str
    resume_required: bool
    reconciliation_id: str | None
    reconciliation_object_id: str | None
    reconciliation_object_version: int | None

    def __post_init__(self) -> None:
        if self.generation < 1 or self.remote_state not in {
            "ready",
            "not_applicable",
            "delete_incomplete",
            "credential_reentered",
        }:
            raise ValueError("invalid_credential_state")
        if self.resume_required != (
            self.remote_state in {"delete_incomplete", "credential_reentered"}
        ):
            raise ValueError("invalid_credential_state")
        has_target = (
            self.reconciliation_object_id is not None
            and self.reconciliation_object_version is not None
            and 1 <= len(self.reconciliation_object_id) <= 128
            and 1 <= self.reconciliation_object_version <= 2_147_483_647
        )
        if self.resume_required and (not has_target or self.reconciliation_id is not None):
            raise ValueError("invalid_credential_state")
        if not self.resume_required and has_target != (self.reconciliation_id is not None):
            raise ValueError("invalid_credential_state")
        if self.reconciliation_id is not None and self.remote_state != "ready":
            raise ValueError("invalid_credential_state")


class CredentialStateRepository(Protocol):
    def get(self, profile_id: str) -> CredentialLifecycleState | None:
        raise NotImplementedError

    def put(
        self,
        state: CredentialLifecycleState,
        expected_generation: int | None,
    ) -> CredentialLifecycleState:
        raise NotImplementedError

    def recover(
        self,
        profile_id: str,
        expected_generation: int,
        evidence_id: str,
        reconciliation_object_id: str,
        reconciliation_object_version: int,
        evidence_version: int,
    ) -> CredentialLifecycleState:
        """Atomically compare evidence/state, mark remote resumable, and write ready."""
        raise NotImplementedError


@dataclass(frozen=True)
class CredentialStatusView:
    configured: bool
    error_code: str | None
    remote_state: str
    resume_required: bool
    reconciliation_id: str | None
    reconciliation_object_id: str | None
    reconciliation_object_version: int | None


@dataclass(frozen=True)
class ClearResult:
    status: str
    remote_state: str
    recovery: str | None
~~~

- [ ] **Step 11: Append service construction and lifecycle writes**

Append to backend/src/projectb/application/credentials.py:

~~~python


class CredentialService:
    def __init__(
        self,
        store: SecretStore,
        profiles: Mapping[str, ProviderProfile],
        remote: RemoteWorkCoordinator,
        repository: CredentialStateRepository,
    ) -> None:
        self._store = store
        self._profiles = dict(profiles)
        self._remote = remote
        self._repository = repository

    def _state(self, profile_id: str) -> CredentialLifecycleState | None:
        return self._repository.get(profile_id)

    def _put_state(
        self,
        profile_id: str,
        remote_state: str,
        resume_required: bool,
        reconciliation_id: str | None = None,
        reconciliation_object_id: str | None = None,
        reconciliation_object_version: int | None = None,
    ) -> CredentialLifecycleState:
        current = self._state(profile_id)
        generation = 1 if current is None else current.generation + 1
        state = CredentialLifecycleState(
            profile_id,
            generation,
            remote_state,
            resume_required,
            reconciliation_id,
            reconciliation_object_id,
            reconciliation_object_version,
        )
        return self._repository.put(
            state,
            None if current is None else current.generation,
        )

    def configure(self, profile_id: str, hidden_value: str) -> CredentialStatusView:
        profile = self._profile(profile_id)
        self._store.set(profile.credential_ref, SecretValue.from_text(hidden_value))
        current = self._state(profile_id)
        if current is not None and current.resume_required:
            self._put_state(
                profile_id,
                "credential_reentered",
                True,
                reconciliation_object_id=current.reconciliation_object_id,
                reconciliation_object_version=current.reconciliation_object_version,
            )
        else:
            self._put_state(profile_id, "ready", False)
        return self.status(profile_id)

    def status(self, profile_id: str) -> CredentialStatusView:
        profile = self._profile(profile_id)
        lifecycle = self._state(profile_id)
        stored = self._store.status(profile.credential_ref)
        return CredentialStatusView(
            stored.configured,
            "resume_required"
            if lifecycle is not None and lifecycle.resume_required
            else stored.error_code,
            "not_applicable" if lifecycle is None else lifecycle.remote_state,
            False if lifecycle is None else lifecycle.resume_required,
            None if lifecycle is None else lifecycle.reconciliation_id,
            None if lifecycle is None else lifecycle.reconciliation_object_id,
            None if lifecycle is None else lifecycle.reconciliation_object_version,
        )
~~~

- [ ] **Step 12: Append fail-closed clear and resolve behavior**

Append to backend/src/projectb/application/credentials.py:

~~~python

    def clear(self, profile_id: str, *, force: bool = False) -> ClearResult:
        profile = self._profile(profile_id)
        target = self._remote.reconciliation_target(profile_id)
        if target is not None and target.profile_id != profile_id:
            raise SecretStoreError("reconciliation_target_invalid")
        if target is not None and not force:
            return ClearResult(
                "blocked",
                "delete_incomplete",
                "wait for reconciliation or use force clear",
            )
        if target is not None:
            self._put_state(
                profile_id,
                "delete_incomplete",
                True,
                reconciliation_object_id=target.reconciliation_object_id,
                reconciliation_object_version=target.reconciliation_object_version,
            )
            self._remote.mark_credential_unavailable(target)
            self._store.clear(profile.credential_ref)
            return ClearResult(
                "forced",
                "delete_incomplete",
                "re-enter the same profile credential or clean up in the provider console",
            )
        self._store.clear(profile.credential_ref)
        self._put_state(profile_id, "not_applicable", False)
        return ClearResult("cleared", "not_applicable", None)

    def resolve_for_call(self, profile_id: str) -> SecretHandle:
        lifecycle = self._state(profile_id)
        if lifecycle is not None and lifecycle.resume_required:
            code = (
                "resume_required"
                if lifecycle.remote_state == "credential_reentered"
                else "credential_unavailable"
            )
            raise SecretStoreError(code)
        return self._store.resolve(self._profile(profile_id).credential_ref)
~~~

- [ ] **Step 13: Append atomic resume and validated profile configuration**

Append to backend/src/projectb/application/credentials.py:

~~~python

    def resume(self, profile_id: str, evidence_id: str) -> CredentialStatusView:
        profile = self._profile(profile_id)
        lifecycle = self._state(profile_id)
        if lifecycle is None or not lifecycle.resume_required:
            raise SecretStoreError("resume_not_required")
        if not self._store.status(profile.credential_ref).configured:
            raise SecretStoreError("credential_unavailable")
        if (
            lifecycle.reconciliation_object_id is None
            or lifecycle.reconciliation_object_version is None
        ):
            raise SecretStoreError("reconciliation_required")
        try:
            self._repository.recover(
                profile_id,
                lifecycle.generation,
                evidence_id,
                lifecycle.reconciliation_object_id,
                lifecycle.reconciliation_object_version,
                1,
            )
        except CredentialRepositoryError as error:
            raise SecretStoreError(error.code) from None
        return self.status(profile_id)

    def configure_payload(
        self,
        profile_id: str,
        payload: Mapping[str, object],
        hidden_value: str,
    ) -> CredentialStatusView | ProfileError:
        profile = validate_provider_profile(payload)
        if isinstance(profile, ProfileError):
            return profile
        if profile.profile_id != profile_id:
            return ProfileError("profile_mismatch", "profile_id")
        existing = self._profiles.get(profile_id)
        lifecycle = self._state(profile_id)
        if (
            existing is not None
            and lifecycle is not None
            and lifecycle.resume_required
            and existing.config_fingerprint != profile.config_fingerprint
        ):
            return ProfileError("profile_change_forbidden", "profile_id")
        self._profiles[profile_id] = profile
        return self.configure(profile_id, hidden_value)

    def _profile(self, profile_id: str) -> ProviderProfile:
        profile = self._profiles.get(profile_id)
        if profile is None:
            raise SecretStoreError("profile_not_found")
        return profile
~~~

- [ ] **Step 14: Run focused green and all quality/regression commands**

~~~powershell
Invoke-CheckedPython @("-m","pytest","backend/tests/unit/test_credentials.py","backend/tests/integration/test_credential_boundary.py","-q") 120
Invoke-CheckedPython @("-m","ruff","check","--config","backend/pyproject.toml","backend/src/projectb/application/credentials.py","backend/tests/unit/test_credentials.py","backend/tests/integration/test_credential_boundary.py") 120
Invoke-CheckedPython @("-m","mypy","--config-file","backend/pyproject.toml","backend/src/projectb/application/credentials.py","backend/tests/unit/test_credentials.py","backend/tests/integration/test_credential_boundary.py") 120
Invoke-CheckedPython @("-m","pytest","backend/tests","-q") 300
Invoke-CheckedPython @("scripts/test_all.py") 900
~~~

- [ ] **Step 15: Run both reviews**

SPEC review checks AC-07/AC-30/AC-40 and threats T-06/T-19: hidden configure/status/update/clear, validation-before-resolve, forced clear, same-profile recovery, no profile/mock switch, no secret persistence. Quality/security/license review checks clear/resolve races, callback failures, memory lifetime, redaction, repository compatibility, and keyring licenses.

- [ ] **Step 16: Stage, scan, and capture the private T-05C packet**

~~~powershell
$expected=@("backend/src/projectb/application/credentials.py","backend/tests/unit/test_credentials.py","backend/tests/integration/test_credential_boundary.py")
$reviewPacket=Start-UnitReview $expected
~~~

- [ ] **Step 17: Validate both T-05C review receipts**

~~~powershell
$receipts=Assert-UnitReviewReceipts $reviewPacket "T-05C"
~~~

- [ ] **Step 18: Recheck and commit the reviewed T-05C tree**

~~~powershell
Complete-ReviewedUnit $expected $reviewPacket "feat(T-05C): coordinate credential lifecycle [agent: $env:PROJECTB_AGENT_ID]"
~~~

**Completion standard:** Only `resolve_for_call` obtains a short-lived handle. Forced clear writes authoritative repository state before clearing the store, blocks all new remote calls after a fresh service restart, and remains blocked after credential re-entry until the same profile has explicit persisted reconciliation evidence and an explicit resume action. Recovery is one durable repository transaction/CAS: an injected persistence failure leaves both lifecycle and remote-resumable state unchanged across restart, while success atomically commits the matched profile/object/version/evidence tuple and `ready` state.

## Task T-06: Implement Processing Policy, Consent, And Scope Tokens

**Goal:** Prevent silent egress and bind every P/F request to exact immutable payload/profile/config/capability/policy/purpose/budget consent.

**Files:**
- Create: backend/src/projectb/application/consent.py
- Test: backend/tests/unit/test_consent_scope.py
- Test: backend/tests/integration/test_no_consent_egress.py
- Consume only: backend/src/projectb/application/security.py

**Interfaces:** `PayloadScopeItem`, `CapabilitySnapshot`, `PolicySnapshot`, `ProcessingMode`, `ConsentExpectation`, `ConsentRecord`, `ConsentRepository`, `InMemoryConsentRepository`, `AuthorizationStateRepository`, `InMemoryAuthorizationStateRepository`, `ConsentService`, `ProcessingPolicy`, and `AuthorizationDecision`.

**Dependencies / parallelism:** Requires reviewed T-02C/T-03C/T-04C/T-05C. It does not edit or stage security.py. Any required security change returns to T-04 for a new serial review.

**Expected first failure:** projectb.application.consent is absent.

- [ ] **Step 1: Run the prelude and verify all predecessor hashes**

Import only published predecessor APIs. Stop if T-02C/T-03C/T-04C/T-05C is missing, unreviewed, or interface-incompatible.

~~~powershell
$owned=@("backend/src/projectb/application/consent.py","backend/tests/unit/test_consent_scope.py","backend/tests/integration/test_no_consent_egress.py")
Assert-UnitStart -ExpectedUnit "T-06" -OwnedPaths $owned -ExpectedDependencies @("T-02C","T-03C","T-04C","T-05C")
~~~

- [ ] **Step 2: Write failing unit tests for exact scope and policy**

Create backend/tests/unit/test_consent_scope.py:

~~~python
from dataclasses import replace
from decimal import Decimal
from typing import cast

import pytest
from projectb.application.consent import (
    AuthorizationState,
    CapabilitySnapshot,
    ConsentExpectation,
    ConsentService,
    InMemoryAuthorizationStateRepository,
    InMemoryConsentRepository,
    PayloadScopeItem,
    PolicySnapshot,
    ProcessingMode,
    ProcessingPolicy,
    ProviderProfileSnapshot,
)


def scope(content_hash: str = "a" * 64) -> tuple[PayloadScopeItem, ...]:
    return (PayloadScopeItem("material-1", content_hash, "lecture", ("source-1",)),)


def capability() -> CapabilitySnapshot:
    return CapabilitySnapshot("cap-1", ("file_search", "responses"))


def policy() -> PolicySnapshot:
    return PolicySnapshot(
        "policy-1",
        True,
        30,
        24,
        True,
        "until_delete_or_expiry",
        "until_delete_or_expiry",
        False,
        "not_used_unless_opt_in",
        "us",
        30,
        30,
        "provider_confirmation_required",
        30,
    )


def expectation(content_hash: str = "a" * 64) -> ConsentExpectation:
    return ConsentExpectation(
        ProcessingMode.P,
        scope(content_hash),
        "profile-1",
        "c" * 64,
        "cap-1",
        "policy-1",
        "explain",
        Decimal("1.00"),
    )


def authority(*, selected: bool = True) -> InMemoryAuthorizationStateRepository:
    repository = InMemoryAuthorizationStateRepository()
    if selected:
        repository.policy_by_course["course-1"] = ProcessingPolicy(
            "course-1", ProcessingMode.P, 1
        )
    repository.materials[("course-1", "material-1")] = scope()[0]
    repository.profiles["profile-1"] = ProviderProfileSnapshot(
        "profile-1", "c" * 64
    )
    repository.capabilities["cap-1"] = capability()
    repository.provider_policies["policy-1"] = policy()
    return repository
~~~

- [ ] **Step 3: Append scope, snapshot, and unselected-policy tests**

Append to backend/tests/unit/test_consent_scope.py:

~~~python


def test_scope_token_changes_with_consent_or_config() -> None:
    first = ConsentService.scope_token("course-1", "material-1", "a" * 64, "consent-a", "c" * 64)
    second = ConsentService.scope_token("course-1", "material-1", "a" * 64, "consent-b", "c" * 64)
    third = ConsentService.scope_token("course-1", "material-1", "a" * 64, "consent-a", "d" * 64)
    assert len(first) == 64
    assert first != second
    assert first != third


def test_changed_payload_and_revocation_invalidate_consent() -> None:
    service = ConsentService(
        InMemoryConsentRepository(), authority(), id_factory=lambda: "consent-a"
    )
    record = service.create_consent(
        "course-1",
        expectation(),
        capability(),
        policy(),
    )
    assert service.require_consent(record.consent_id, expectation()) == record
    assert service.require_consent(record.consent_id, expectation("b" * 64)) is None
    service.revoke(record.consent_id)
    assert service.require_consent(record.consent_id, expectation()) is None


def test_policy_snapshot_preserves_all_retention_facts() -> None:
    snapshot = policy()
    assert snapshot.responses_store_false is True
    assert snapshot.abuse_monitoring_max_days == 30
    assert snapshot.prompt_cache_max_hours == 24
    assert snapshot.file_review_exception is True
    assert snapshot.files_retention == "until_delete_or_expiry"
    assert snapshot.vector_stores_retention == "until_delete_or_expiry"
    assert snapshot.zero_data_retention is False
    assert snapshot.training_use == "not_used_unless_opt_in"
    assert snapshot.processing_region == "us"
    assert snapshot.file_expiry_days == 30
    assert snapshot.vector_store_expiry_days == 30
    assert snapshot.deletion_semantics == "provider_confirmation_required"
    assert snapshot.removal_window_days == 30


def test_absence_is_unselected_and_empty_l_consent_cannot_authorize_parse() -> None:
    states = authority(selected=False)
    service = ConsentService(InMemoryConsentRepository(), states, id_factory=lambda: "consent-a")
    current = service.processing_policy_for("course-1")
    assert current.mode is None
    assert current.status == "unselected"
    assert service.authorize_local_parse("course-1", scope()[0], 1).status == "policy_unselected"
    local = ConsentExpectation(
        ProcessingMode.L,
        tuple(),
        None,
        None,
        None,
        None,
        "parse",
        Decimal("0.00"),
    )
    with pytest.raises(ValueError, match="remote consent mode"):
        service.create_consent("course-1", local, None, None)
    states.policy_by_course["course-1"] = ProcessingPolicy("course-1", ProcessingMode.L, 1)
    assert service.authorize_local_parse("course-1", scope()[0], 1).status == "authorized_local"
~~~

- [ ] **Step 4: Append exact-authority mutation tests**

Append to backend/tests/unit/test_consent_scope.py:

~~~python


def test_authorization_reloads_exact_current_authority() -> None:
    states = authority()
    service = ConsentService(InMemoryConsentRepository(), states, id_factory=lambda: "consent-a")
    record = service.create_consent("course-1", expectation(), capability(), policy())
    assert service.require_consent(record.consent_id, expectation()) == record

    mutations: tuple[tuple[str, AuthorizationState], ...] = (
        ("material", scope("b" * 64)[0]),
        ("profile", ProviderProfileSnapshot("profile-1", "d" * 64)),
        ("capability", CapabilitySnapshot("cap-1", ("responses",))),
        (
            "policy",
            PolicySnapshot(
                "policy-1",
                True,
                30,
                24,
                True,
                "until_delete_or_expiry",
                "until_delete_or_expiry",
                False,
                "not_used_unless_opt_in",
                "eu",
                30,
                30,
                "provider_confirmation_required",
                30,
            ),
        ),
    )
    for kind, changed in mutations:
        states.replace(kind, changed)
        assert service.require_consent(record.consent_id, expectation()) is None
        states.restore_defaults(
            scope()[0],
            ProviderProfileSnapshot("profile-1", "c" * 64),
            capability(),
            policy(),
        )
~~~

- [ ] **Step 5: Write the failing zero-egress integration test**

Create backend/tests/integration/test_no_consent_egress.py:

~~~python
from decimal import Decimal

from projectb.application.consent import (
    CapabilitySnapshot,
    ConsentExpectation,
    ConsentService,
    InMemoryAuthorizationStateRepository,
    InMemoryConsentRepository,
    PayloadScopeItem,
    PolicySnapshot,
    ProcessingMode,
    ProcessingPolicy,
    ProviderProfileSnapshot,
)


def test_remote_callback_is_not_called_without_exact_consent() -> None:
    calls = 0

    def remote_callback() -> None:
        nonlocal calls
        calls += 1

    states = InMemoryAuthorizationStateRepository()
    states.policy_by_course["course-1"] = ProcessingPolicy("course-1", ProcessingMode.F, 1)
    material = PayloadScopeItem("material-1", "a" * 64, "lecture", ("source-1",))
    states.materials[("course-1", "material-1")] = material
    states.profiles["profile-1"] = ProviderProfileSnapshot("profile-1", "c" * 64)
    states.capabilities["cap-1"] = CapabilitySnapshot("cap-1", ("file_search", "responses"))
    states.provider_policies["policy-1"] = PolicySnapshot(
        "policy-1",
        True,
        30,
        24,
        True,
        "until_delete_or_expiry",
        "until_delete_or_expiry",
        False,
        "not_used_unless_opt_in",
        "us",
        30,
        30,
        "provider_confirmation_required",
        30,
    )
    service = ConsentService(
        InMemoryConsentRepository(), states, id_factory=lambda: "consent-a"
    )
    expectation = ConsentExpectation(
        ProcessingMode.F,
        (material,),
        "profile-1",
        "c" * 64,
        "cap-1",
        "policy-1",
        "coverage",
        Decimal("1.00"),
    )
    decision = service.authorize_remote(
        "course-1",
        None,
        expectation,
        remote_callback,
    )
    assert decision.status == "awaiting_consent"
    assert calls == 0
~~~

- [ ] **Step 6: Run red**

~~~powershell
$red=Invoke-BoundedNative $PythonExe @("-m","pytest","backend/tests/unit/test_consent_scope.py","backend/tests/integration/test_no_consent_egress.py","-q") 120
if ($red.ExitCode -eq 0 -or ($red.Stdout+$red.Stderr) -notmatch "consent") { throw "T-06 red evidence invalid" }
~~~

- [ ] **Step 7: Define processing, payload, capability, and policy types**

Create backend/src/projectb/application/consent.py with this first complete section:

~~~python
from __future__ import annotations

import hashlib
import re
from collections.abc import Callable
from dataclasses import dataclass, replace
from datetime import UTC, datetime
from decimal import Decimal
from enum import StrEnum
from typing import Protocol

_HASH = re.compile(r"^[0-9a-f]{64}$")
_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")


class ProcessingMode(StrEnum):
    L = "L"
    P = "P"
    F = "F"


@dataclass(frozen=True)
class PayloadScopeItem:
    material_id: str
    content_hash: str
    role: str
    source_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        if _ID.fullmatch(self.material_id) is None or _HASH.fullmatch(self.content_hash) is None:
            raise ValueError("invalid payload scope")
        if self.role not in {"lecture", "past_paper", "teacher_focus"}:
            raise ValueError("unsupported_role")
        if (
            not self.source_ids
            or len(self.source_ids) > 64
            or tuple(sorted(set(self.source_ids))) != self.source_ids
            or any(_ID.fullmatch(value) is None for value in self.source_ids)
        ):
            raise ValueError("invalid source scope")


@dataclass(frozen=True)
class CapabilitySnapshot:
    snapshot_id: str
    capabilities: tuple[str, ...]

    def __post_init__(self) -> None:
        if (
            _ID.fullmatch(self.snapshot_id) is None
            or not self.capabilities
            or len(self.capabilities) > 32
            or tuple(sorted(set(self.capabilities))) != self.capabilities
            or any(_ID.fullmatch(value) is None for value in self.capabilities)
        ):
            raise ValueError("invalid capability snapshot")
~~~

- [ ] **Step 8: Append the provider policy and consent expectation types**

Append to backend/src/projectb/application/consent.py:

~~~python


@dataclass(frozen=True)
class PolicySnapshot:
    snapshot_id: str
    responses_store_false: bool
    abuse_monitoring_max_days: int
    prompt_cache_max_hours: int
    file_review_exception: bool
    files_retention: str
    vector_stores_retention: str
    zero_data_retention: bool
    training_use: str
    processing_region: str
    file_expiry_days: int
    vector_store_expiry_days: int
    deletion_semantics: str
    removal_window_days: int

    def __post_init__(self) -> None:
        if _ID.fullmatch(self.snapshot_id) is None:
            raise ValueError("invalid policy snapshot")
        required = (
            self.responses_store_false is True
            and self.abuse_monitoring_max_days == 30
            and self.prompt_cache_max_hours == 24
            and self.file_review_exception is True
            and self.files_retention == "until_delete_or_expiry"
            and self.vector_stores_retention == "until_delete_or_expiry"
            and self.zero_data_retention is False
            and self.training_use == "not_used_unless_opt_in"
            and _ID.fullmatch(self.processing_region) is not None
            and 1 <= self.file_expiry_days <= 3650
            and 1 <= self.vector_store_expiry_days <= 3650
            and self.deletion_semantics == "provider_confirmation_required"
            and 1 <= self.removal_window_days <= 365
        )
        if not required:
            raise ValueError("policy_unknown")


@dataclass(frozen=True)
class ConsentExpectation:
    mode: ProcessingMode
    payload_scope: tuple[PayloadScopeItem, ...]
    profile_id: str | None
    config_fingerprint: str | None
    capability_snapshot_id: str | None
    policy_snapshot_id: str | None
    purpose: str
    budget_limit_usd: Decimal


@dataclass(frozen=True)
class ConsentRecord:
    consent_id: str
    course_id: str
    expectation: ConsentExpectation
    capability_snapshot: CapabilitySnapshot
    policy_snapshot: PolicySnapshot
    created_at: datetime
    revoked_at: datetime | None


@dataclass(frozen=True)
class ProcessingPolicy:
    course_id: str
    mode: ProcessingMode | None
    version: int

    def __post_init__(self) -> None:
        if _ID.fullmatch(self.course_id) is None or self.version < 0:
            raise ValueError("invalid processing policy")
        if self.mode is None and self.version != 0:
            raise ValueError("invalid processing policy")
        if self.mode is not None and self.version < 1:
            raise ValueError("invalid processing policy")

    @property
    def status(self) -> str:
        return "unselected" if self.mode is None else "selected"

    @property
    def remote_allowed(self) -> bool:
        return self.mode in {ProcessingMode.P, ProcessingMode.F}
~~~

- [ ] **Step 9: Append authorization snapshots and the state repository protocol**

Append to backend/src/projectb/application/consent.py:

~~~python


@dataclass(frozen=True)
class AuthorizationDecision:
    status: str
    consent_id: str | None


@dataclass(frozen=True)
class ProviderProfileSnapshot:
    profile_id: str
    config_fingerprint: str

    def __post_init__(self) -> None:
        if (
            _ID.fullmatch(self.profile_id) is None
            or _HASH.fullmatch(self.config_fingerprint) is None
        ):
            raise ValueError("invalid profile snapshot")


type AuthorizationState = (
    PayloadScopeItem | ProviderProfileSnapshot | CapabilitySnapshot | PolicySnapshot
)


class AuthorizationStateRepository(Protocol):
    def current_policy(self, course_id: str) -> ProcessingPolicy | None:
        raise NotImplementedError

    def current_material(self, course_id: str, material_id: str) -> PayloadScopeItem | None:
        raise NotImplementedError

    def current_profile(self, profile_id: str) -> ProviderProfileSnapshot | None:
        raise NotImplementedError

    def current_capability(self, snapshot_id: str) -> CapabilitySnapshot | None:
        raise NotImplementedError

    def current_provider_policy(self, snapshot_id: str) -> PolicySnapshot | None:
        raise NotImplementedError
~~~

- [ ] **Step 10: Append the in-memory authority repository**

Append to backend/src/projectb/application/consent.py:

~~~python
class InMemoryAuthorizationStateRepository:
    def __init__(self) -> None:
        self.policy_by_course: dict[str, ProcessingPolicy] = {}
        self.materials: dict[tuple[str, str], PayloadScopeItem] = {}
        self.profiles: dict[str, ProviderProfileSnapshot] = {}
        self.capabilities: dict[str, CapabilitySnapshot] = {}
        self.provider_policies: dict[str, PolicySnapshot] = {}

    def current_policy(self, course_id: str) -> ProcessingPolicy | None:
        return self.policy_by_course.get(course_id)

    def current_material(self, course_id: str, material_id: str) -> PayloadScopeItem | None:
        return self.materials.get((course_id, material_id))

    def current_profile(self, profile_id: str) -> ProviderProfileSnapshot | None:
        return self.profiles.get(profile_id)

    def current_capability(self, snapshot_id: str) -> CapabilitySnapshot | None:
        return self.capabilities.get(snapshot_id)

    def current_provider_policy(self, snapshot_id: str) -> PolicySnapshot | None:
        return self.provider_policies.get(snapshot_id)

    def replace(self, kind: str, state: AuthorizationState) -> None:
        if kind == "material" and isinstance(state, PayloadScopeItem):
            self.materials[("course-1", state.material_id)] = state
        elif kind == "profile" and isinstance(state, ProviderProfileSnapshot):
            self.profiles[state.profile_id] = state
        elif kind == "capability" and isinstance(state, CapabilitySnapshot):
            self.capabilities[state.snapshot_id] = state
        elif kind == "policy" and isinstance(state, PolicySnapshot):
            self.provider_policies[state.snapshot_id] = state
        else:
            raise ValueError("invalid authority replacement")

    def restore_defaults(
        self,
        material: PayloadScopeItem,
        profile: ProviderProfileSnapshot,
        capability: CapabilitySnapshot,
        policy: PolicySnapshot,
    ) -> None:
        self.materials[("course-1", material.material_id)] = material
        self.profiles[profile.profile_id] = profile
        self.capabilities[capability.snapshot_id] = capability
        self.provider_policies[policy.snapshot_id] = policy
~~~

- [ ] **Step 11: Append the consent repository contract and test implementation**

Append to backend/src/projectb/application/consent.py:

~~~python


class ConsentRepository(Protocol):
    def append(self, record: ConsentRecord) -> None:
        raise NotImplementedError

    def get(self, consent_id: str) -> ConsentRecord | None:
        raise NotImplementedError

    def latest_for_course(self, course_id: str) -> ConsentRecord | None:
        raise NotImplementedError

    def revoke(self, consent_id: str, when: datetime) -> None:
        raise NotImplementedError


class InMemoryConsentRepository:
    def __init__(self) -> None:
        self._records: dict[str, ConsentRecord] = {}

    def append(self, record: ConsentRecord) -> None:
        if record.consent_id in self._records:
            raise ValueError("duplicate consent")
        self._records[record.consent_id] = record

    def get(self, consent_id: str) -> ConsentRecord | None:
        return self._records.get(consent_id)

    def latest_for_course(self, course_id: str) -> ConsentRecord | None:
        matches = [record for record in self._records.values() if record.course_id == course_id]
        return max(matches, key=lambda record: record.created_at, default=None)

    def revoke(self, consent_id: str, when: datetime) -> None:
        record = self._records.get(consent_id)
        if record is not None:
            self._records[consent_id] = replace(record, revoked_at=when)
~~~

- [ ] **Step 12: Define scope-token and expectation validation**

Append this exact section to consent.py:

~~~python
class ConsentService:
    def __init__(
        self,
        repository: ConsentRepository,
        state_repository: AuthorizationStateRepository,
        *,
        id_factory: Callable[[], str],
        clock: Callable[[], datetime] = lambda: datetime.now(UTC),
    ) -> None:
        self._repository = repository
        self._state_repository = state_repository
        self._id_factory = id_factory
        self._clock = clock

    @staticmethod
    def scope_token(
        course_id: str,
        material_id: str,
        content_hash: str,
        consent_record_id: str,
        config_fingerprint: str,
    ) -> str:
        if any(
            _ID.fullmatch(value) is None for value in (course_id, material_id, consent_record_id)
        ):
            raise ValueError("invalid scope identity")
        if _HASH.fullmatch(content_hash) is None or _HASH.fullmatch(config_fingerprint) is None:
            raise ValueError("invalid scope digest")
        value = "|".join(
            (course_id, material_id, content_hash, consent_record_id, config_fingerprint)
        )
        return hashlib.sha256(value.encode("ascii")).hexdigest()

    @staticmethod
    def _validate_expectation(expectation: ConsentExpectation) -> None:
        if type(expectation.mode) is not ProcessingMode or expectation.mode not in {
            ProcessingMode.P,
            ProcessingMode.F,
        }:
            raise ValueError("remote consent mode must be P or F")
        if not expectation.purpose or len(expectation.purpose) > 128:
            raise ValueError("invalid purpose")
        if (
            type(expectation.budget_limit_usd) is not Decimal
            or not expectation.budget_limit_usd.is_finite()
            or expectation.budget_limit_usd < 0
            or expectation.budget_limit_usd > Decimal("1000")
            or expectation.budget_limit_usd
            != expectation.budget_limit_usd.quantize(Decimal("0.01"))
        ):
            raise ValueError("invalid budget")
        if (
            not expectation.payload_scope
            or len(expectation.payload_scope) > 64
            or tuple(sorted(expectation.payload_scope, key=lambda item: item.material_id))
            != expectation.payload_scope
            or not expectation.profile_id
            or not expectation.config_fingerprint
            or not expectation.capability_snapshot_id
            or not expectation.policy_snapshot_id
        ):
            raise ValueError("remote consent incomplete")
        if _HASH.fullmatch(expectation.config_fingerprint) is None:
            raise ValueError("invalid config fingerprint")
~~~

- [ ] **Step 13: Append authority matching and consent creation**

Append to backend/src/projectb/application/consent.py:

~~~python

    def _authority_matches(
        self,
        course_id: str,
        exact: ConsentExpectation,
        capability_snapshot: CapabilitySnapshot,
        policy_snapshot: PolicySnapshot,
    ) -> bool:
        selected = self._state_repository.current_policy(course_id)
        if selected is None or selected.mode is not exact.mode:
            return False
        if any(
            self._state_repository.current_material(course_id, item.material_id) != item
            for item in exact.payload_scope
        ):
            return False
        if exact.profile_id is None or exact.config_fingerprint is None:
            return False
        if self._state_repository.current_profile(exact.profile_id) != ProviderProfileSnapshot(
            exact.profile_id, exact.config_fingerprint
        ):
            return False
        capability = self._state_repository.current_capability(
            exact.capability_snapshot_id or ""
        )
        policy = self._state_repository.current_provider_policy(
            exact.policy_snapshot_id or ""
        )
        return capability == capability_snapshot and policy == policy_snapshot

    def create_consent(
        self,
        course_id: str,
        expectation: ConsentExpectation,
        capability: CapabilitySnapshot | None,
        policy: PolicySnapshot | None,
    ) -> ConsentRecord:
        if _ID.fullmatch(course_id) is None:
            raise ValueError("invalid course")
        self._validate_expectation(expectation)
        if capability is None or policy is None:
            raise ValueError("remote consent incomplete")
        if (
            capability.snapshot_id != expectation.capability_snapshot_id
            or policy.snapshot_id != expectation.policy_snapshot_id
            or self._state_repository.current_capability(capability.snapshot_id) != capability
            or self._state_repository.current_provider_policy(policy.snapshot_id) != policy
            or not self._authority_matches(course_id, expectation, capability, policy)
        ):
            raise ValueError("snapshot mismatch")
        consent_id = self._id_factory()
        if _ID.fullmatch(consent_id) is None:
            raise ValueError("invalid consent id")
        record = ConsentRecord(
            consent_id,
            course_id,
            expectation,
            capability,
            policy,
            self._clock(),
            None,
        )
        self._repository.append(record)
        return record
~~~

- [ ] **Step 14: Append consent lookup and local/remote authorization**

Append to backend/src/projectb/application/consent.py:

~~~python

    def require_consent(
        self,
        consent_id: str,
        exact: ConsentExpectation,
    ) -> ConsentRecord | None:
        record = self._repository.get(consent_id)
        if (
            record is None
            or record.revoked_at is not None
            or record.expectation != exact
            or not self._authority_matches(
                record.course_id,
                exact,
                record.capability_snapshot,
                record.policy_snapshot,
            )
        ):
            return None
        return record

    def revoke(self, consent_id: str) -> None:
        self._repository.revoke(consent_id, self._clock())

    def processing_policy_for(self, course_id: str) -> ProcessingPolicy:
        selected = self._state_repository.current_policy(course_id)
        return selected if selected is not None else ProcessingPolicy(course_id, None, 0)

    def authorize_local_parse(
        self,
        course_id: str,
        material: PayloadScopeItem,
        policy_version: int,
    ) -> AuthorizationDecision:
        selected = self._state_repository.current_policy(course_id)
        if selected is None:
            return AuthorizationDecision("policy_unselected", None)
        if selected.version != policy_version:
            return AuthorizationDecision("policy_changed", None)
        if self._state_repository.current_material(course_id, material.material_id) != material:
            return AuthorizationDecision("scope_changed", None)
        return AuthorizationDecision("authorized_local", None)

    def authorize_remote(
        self,
        course_id: str,
        consent_id: str | None,
        exact: ConsentExpectation,
        callback: Callable[[], None],
    ) -> AuthorizationDecision:
        if exact.mode not in {ProcessingMode.P, ProcessingMode.F} or consent_id is None:
            return AuthorizationDecision("awaiting_consent", None)
        record = self.require_consent(consent_id, exact)
        if record is None or record.course_id != course_id:
            return AuthorizationDecision("awaiting_consent", None)
        callback()
        return AuthorizationDecision("authorized", consent_id)
~~~

- [ ] **Step 15: Run focused green**

~~~powershell
Invoke-CheckedPython @("-m","pytest","backend/tests/unit/test_consent_scope.py","backend/tests/integration/test_no_consent_egress.py","-q") 120
~~~

- [ ] **Step 16: Append the exact mutation and empty-scope matrix**

Append to backend/tests/unit/test_consent_scope.py:

~~~python
@pytest.mark.parametrize(
    ("field", "value"),
    (
        ("mode", ProcessingMode.F),
        (
            "payload_scope",
            (PayloadScopeItem("material-2", "a" * 64, "lecture", ("source-1",)),),
        ),
        ("payload_scope", scope("b" * 64)),
        ("profile_id", "profile-2"),
        ("config_fingerprint", "d" * 64),
        ("capability_snapshot_id", "cap-2"),
        ("policy_snapshot_id", "policy-2"),
        ("purpose", "different-purpose"),
        ("budget_limit_usd", Decimal("2.00")),
    ),
)
def test_every_authority_or_consent_mutation_invalidates(
    field: str,
    value: object,
) -> None:
    service = ConsentService(
        InMemoryConsentRepository(), authority(), id_factory=lambda: "consent-a"
    )
    original = expectation()
    record = service.create_consent("course-1", original, capability(), policy())
    if field == "mode":
        changed = replace(original, mode=cast(ProcessingMode, value))
    elif field == "payload_scope":
        changed = replace(original, payload_scope=cast(tuple[PayloadScopeItem, ...], value))
    elif field == "profile_id":
        changed = replace(original, profile_id=cast(str, value))
    elif field == "config_fingerprint":
        changed = replace(original, config_fingerprint=cast(str, value))
    elif field == "capability_snapshot_id":
        changed = replace(original, capability_snapshot_id=cast(str, value))
    elif field == "policy_snapshot_id":
        changed = replace(original, policy_snapshot_id=cast(str, value))
    elif field == "purpose":
        changed = replace(original, purpose=cast(str, value))
    else:
        changed = replace(original, budget_limit_usd=cast(Decimal, value))
    assert service.require_consent(record.consent_id, changed) is None


@pytest.mark.parametrize("mode", (ProcessingMode.P, ProcessingMode.F))
def test_empty_remote_scope_is_rejected_and_callback_count_stays_zero(
    mode: ProcessingMode,
) -> None:
    calls = 0

    def callback() -> None:
        nonlocal calls
        calls += 1

    service = ConsentService(
        InMemoryConsentRepository(), authority(), id_factory=lambda: "consent-a"
    )
    empty = replace(expectation(), mode=mode, payload_scope=tuple())
    with pytest.raises(ValueError, match="incomplete"):
        service.create_consent("course-1", empty, capability(), policy())
    assert service.authorize_remote("course-1", None, empty, callback).status == "awaiting_consent"
    assert calls == 0
~~~

- [ ] **Step 17: Run Ruff 0.15.22, mypy 2.3.0, affected suite, and canonical suite**

~~~powershell
Invoke-CheckedPython @("-m","ruff","check","--config","backend/pyproject.toml","backend/src/projectb/application/consent.py","backend/tests/unit/test_consent_scope.py","backend/tests/integration/test_no_consent_egress.py") 120
Invoke-CheckedPython @("-m","mypy","--config-file","backend/pyproject.toml","backend/src/projectb/application/consent.py","backend/tests/unit/test_consent_scope.py","backend/tests/integration/test_no_consent_egress.py") 120
Invoke-CheckedPython @("-m","pytest","backend/tests/unit/test_consent_scope.py","backend/tests/integration/test_no_consent_egress.py","-q") 180
Invoke-CheckedPython @("-m","pytest","backend/tests","-q") 300
Invoke-CheckedPython @("scripts/test_all.py") 900
~~~

- [ ] **Step 18: Run both reviews**

SPEC review checks AC-01/AC-02/AC-25/AC-28/AC-31/AC-39/AC-48 and threats T-02/T-12/T-19: exact consent, zero egress, token formula, retention facts, revocation, all fingerprint changes, no body/path/secret. Quality/security/license review checks canonical equality, time/id injection, append-only repository compatibility, callback ordering, budget Decimal, redaction, and no security.py edit.

- [ ] **Step 19: Stage, scan, and capture the private T-06 packet**

~~~powershell
$expected=@("backend/src/projectb/application/consent.py","backend/tests/unit/test_consent_scope.py","backend/tests/integration/test_no_consent_egress.py")
$reviewPacket=Start-UnitReview $expected
~~~

- [ ] **Step 20: Validate both T-06 review receipts**

~~~powershell
$receipts=Assert-UnitReviewReceipts $reviewPacket "T-06"
~~~

- [ ] **Step 21: Recheck and commit the reviewed T-06 tree**

~~~powershell
Complete-ReviewedUnit $expected $reviewPacket "feat(T-06): enforce consent and source scope [agent: $env:PROJECTB_AGENT_ID]"
~~~

**Completion standard:** Every remote-capable service proves exact current consent and scope token before adapter resolution; absent/stale consent yields zero calls.

## Task T-07: Build The Provider-Neutral Registry And Deterministic Mock Contract

**Goal:** Make constrained ports deterministic without network/LLM/credentials and prevent local production fallback to mock.

**Files:**
- Create: backend/src/projectb/infrastructure/providers/base.py
- Create: backend/src/projectb/infrastructure/providers/mock.py
- Create: backend/src/projectb/application/provider.py
- Test: backend/tests/contract/test_provider_contract.py
- Test: backend/tests/contract/test_mock_scenarios.py

**Interfaces:** `PortName`, `PortVersion`, `PayloadSchemaVersion`, `ResponseSchemaVersion`, `ResponseStatus`, `RequestLimits`, `ConsentScopeProof`, `ProviderRequestEnvelope.from_authorized_mapping`, `ProviderResponseEnvelope.create`, `Usage`, `CapabilityDescriptor`, `ProviderAdapter`, `DeterministicMock`, `AdapterError`, `BuiltinManifest`, `ReviewedBuiltinBinding`, `ProviderAdapterRegistry`, `ConfigError`, `CandidateValidation`, and `validate_candidate`.

**Dependencies / parallelism:** Requires reviewed T-05C/T-06. X2/M2/API/DEMO consume this exact contract.

**Expected first failure:** provider base/mock/registry modules are absent.

- [ ] **Step 1: Verify predecessor hashes and worktree authority**

~~~powershell
$owned=@("backend/src/projectb/infrastructure/providers/base.py","backend/src/projectb/infrastructure/providers/mock.py","backend/src/projectb/application/provider.py","backend/tests/contract/test_provider_contract.py","backend/tests/contract/test_mock_scenarios.py")
Assert-UnitStart -ExpectedUnit "T-07" -OwnedPaths $owned -ExpectedDependencies @("T-05C","T-06")
~~~

- [ ] **Step 2: Create the provider contract fixtures and reviewed-manifest helpers**

Create backend/tests/contract/test_provider_contract.py:

~~~python
from decimal import Decimal
from typing import cast

import pytest
from projectb.application.provider import (
    BuiltinManifest,
    BuiltinManifestEntry,
    ConfigError,
    ProviderAdapterRegistry,
    ReviewedBuiltinBinding,
)
from projectb.domain.provider import ProviderProfile
from projectb.infrastructure.providers.base import (
    CapabilityDescriptor,
    MutableCancellationToken,
    PortName,
    ProviderAdapter,
    ProviderRequestEnvelope,
    ProviderResponseEnvelope,
)
from projectb.infrastructure.providers.mock import DeterministicMock

PROFILE = ProviderProfile(
    "profile-1",
    "openai.reference",
    "gpt-5.4-mini-2026-03-17",
    "us",
    1200,
    20000,
    Decimal("1.00"),
    "cred_openai_1",
    "v1",
)
_PORT_PAYLOADS: dict[PortName, dict[str, object]] = {
    PortName.PROPOSE_CONCEPT_COVERAGE: {
        "goal_id": "goal-1",
        "source_scope": ["source-1"],
    },
    PortName.GENERATE_EXPLANATION: {
        "concept_id": "mutex",
        "source_scope": ["source-1"],
    },
    PortName.GENERATE_PRACTICE_CANDIDATE: {
        "concept_id": "mutex",
        "difficulty": 3,
        "source_scope": ["source-1"],
    },
    PortName.ANALYZE_EXAM_MATERIAL: {
        "exam_context_id": "exam-1",
        "source_scope": ["source-1"],
    },
    PortName.GENERATE_FEEDBACK: {
        "attempt_id": "attempt-1",
        "source_scope": ["source-1"],
    },
}
~~~

- [ ] **Step 3: Append request-envelope and reviewed-manifest fixtures**

Append to backend/tests/contract/test_provider_contract.py:

~~~python


def request_mapping(
    port: PortName = PortName.GENERATE_EXPLANATION,
) -> dict[str, object]:
    return {
        "port_name": port.value,
        "port_version": "v1",
        "payload_schema_version": "v1",
        "request_id": "request-1",
        "course_id": "course-1",
        "task_id": "task-1",
        "consent_proof": {
            "consent_id": "consent-1",
            "mode": "P",
            "scope_token": "a" * 64,
            "scope_digest": "b" * 64,
            "config_fingerprint": PROFILE.config_fingerprint,
            "capability_snapshot_id": "cap-1",
            "policy_snapshot_id": "policy-1",
        },
        "payload": _PORT_PAYLOADS[port],
        "input_digest": "c" * 64,
        "limits": {
            "max_input_tokens": 20000,
            "max_output_tokens": 1200,
            "timeout_ms": 20000,
            "budget_usd": "1.00",
        },
        "idempotency_key": "idem-1",
    }


def request(
    port: PortName = PortName.GENERATE_EXPLANATION,
    *,
    cancelled: bool = False,
) -> ProviderRequestEnvelope:
    return ProviderRequestEnvelope.from_authorized_mapping(
        request_mapping(port),
        profile=PROFILE,
        cancellation=MutableCancellationToken(cancelled),
    )


class BuiltinAdapter:
    adapter_id = "openai.reference"

    def describe(self) -> CapabilityDescriptor:
        return CapabilityDescriptor(self.adapter_id, tuple(PortName), True, True)

    def invoke(
        self,
        request: ProviderRequestEnvelope,
        secret_handle: object | None = None,
    ) -> ProviderResponseEnvelope:
        raise AssertionError("contract registry test must not invoke a provider")


def builtin_factory() -> ProviderAdapter:
    return BuiltinAdapter()


def manifest() -> BuiltinManifest:
    return BuiltinManifest(
        "projectb-builtins-v1",
        (
            BuiltinManifestEntry(
                "openai.reference",
                "v1",
                builtin_factory.__module__,
                builtin_factory.__qualname__,
                tuple(PortName),
            ),
        ),
    )
~~~

- [ ] **Step 4: Append exact-port and caller-claim rejection tests**

Append to backend/tests/contract/test_provider_contract.py:

~~~python


@pytest.mark.parametrize("port", tuple(PortName))
def test_each_port_requires_its_exact_payload_schema(port: PortName) -> None:
    envelope = request(port)
    assert envelope.port_name is port
    assert envelope.task_id == "task-1"
    assert envelope.provider_profile_id == PROFILE.profile_id
    assert envelope.config_fingerprint == PROFILE.config_fingerprint


def test_request_rejects_caller_profile_adapter_paths_credentials_and_tools() -> None:
    for field, value in (
        ("adapter_id", "openai.reference"),
        ("provider_profile_id", "profile-2"),
        ("config_fingerprint", "d" * 64),
        ("local_path", "C:\\private\\course.pdf"),
        ("credential_ref", "cred_openai_1"),
        ("tools", ["shell"]),
    ):
        payload = request_mapping()
        payload[field] = value
        with pytest.raises(ValueError):
            ProviderRequestEnvelope.from_authorized_mapping(
                payload,
                profile=PROFILE,
                cancellation=MutableCancellationToken(),
            )


def test_request_bounds_task_payload_budget_and_cancellation() -> None:
    payload = request_mapping()
    payload["task_id"] = None
    with pytest.raises(ValueError):
        ProviderRequestEnvelope.from_authorized_mapping(
            payload,
            profile=PROFILE,
            cancellation=MutableCancellationToken(),
        )
~~~

- [ ] **Step 5: Append reviewed-factory, duplicate, and mock-registration tests**

Append to backend/tests/contract/test_provider_contract.py:

~~~python

    payload = request_mapping()
    limits = dict(cast(dict[str, object], payload["limits"]))
    limits["budget_usd"] = "1.001"
    payload["limits"] = limits
    with pytest.raises(ValueError):
        ProviderRequestEnvelope.from_authorized_mapping(
            payload,
            profile=PROFILE,
            cancellation=MutableCancellationToken(),
        )

    payload = request_mapping(PortName.GENERATE_EXPLANATION)
    payload["payload"] = {"attempt_id": "attempt-1", "source_scope": ["source-1"]}
    with pytest.raises(ValueError):
        ProviderRequestEnvelope.from_authorized_mapping(
            payload,
            profile=PROFILE,
            cancellation=MutableCancellationToken(),
        )


def test_registry_is_bound_to_reviewed_manifest_and_factory_object_identity() -> None:
    reviewed_manifest = manifest()
    binding = ReviewedBuiltinBinding(reviewed_manifest, builtin_factory)
    registry = ProviderAdapterRegistry.from_reviewed_builtin(
        binding,
        coordinator_manifest=reviewed_manifest,
        coordinator_factory=builtin_factory,
    )
    assert isinstance(registry.for_profile(PROFILE), BuiltinAdapter)
    malformed = cast(ProviderProfile, {"adapter_id": "openai.reference"})
    assert isinstance(registry.for_profile(malformed), ConfigError)

    with pytest.raises(ConfigError) as wrong_factory:
        ProviderAdapterRegistry.from_reviewed_builtin(
            binding,
            coordinator_manifest=reviewed_manifest,
            coordinator_factory=lambda: BuiltinAdapter(),
        )
    assert wrong_factory.value.code == "builtin_authority_mismatch"


def test_duplicate_manifest_and_mock_registration_fail_closed() -> None:
    entry = manifest().entries[0]
    with pytest.raises(ConfigError) as duplicate_manifest:
        BuiltinManifest("projectb-builtins-v1", (entry, entry))
    assert duplicate_manifest.value.code == "builtin_manifest_invalid"

    mock = DeterministicMock("success", seed=7)
    with pytest.raises(ConfigError) as duplicate_mock:
        ProviderAdapterRegistry.for_test_demo("test", (mock, mock))
    assert duplicate_mock.value.code == "duplicate_or_forbidden_adapter"
    registry = ProviderAdapterRegistry.for_test_demo("demo", (mock,))
    assert registry.test_demo_adapter() is mock
~~~

- [ ] **Step 6: Create deterministic mock request fixtures**

Create backend/tests/contract/test_mock_scenarios.py:

~~~python
import socket
from decimal import Decimal

import pytest
from projectb.application.provider import ConfigError, validate_candidate
from projectb.domain.provider import ProviderProfile
from projectb.infrastructure.providers.base import (
    MutableCancellationToken,
    PortName,
    ProviderRequestEnvelope,
    ProviderResponseEnvelope,
    ResponseSchemaVersion,
    ResponseStatus,
    Usage,
)
from projectb.infrastructure.providers.mock import AdapterError, DeterministicMock

PROFILE = ProviderProfile(
    "profile-1",
    "openai.reference",
    "gpt-5.4-mini-2026-03-17",
    "us",
    1200,
    20000,
    Decimal("1.00"),
    "cred_openai_1",
    "v1",
)


def request(*, cancelled: bool = False) -> ProviderRequestEnvelope:
    return ProviderRequestEnvelope.from_authorized_mapping(
        {
            "port_name": PortName.GENERATE_EXPLANATION.value,
            "port_version": "v1",
            "payload_schema_version": "v1",
            "request_id": "request-1",
            "course_id": "course-1",
            "task_id": "task-1",
            "consent_proof": {
                "consent_id": "consent-1",
                "mode": "P",
                "scope_token": "a" * 64,
                "scope_digest": "b" * 64,
                "config_fingerprint": PROFILE.config_fingerprint,
                "capability_snapshot_id": "cap-1",
                "policy_snapshot_id": "policy-1",
            },
            "payload": {"concept_id": "mutex", "source_scope": ["source-1"]},
            "input_digest": "c" * 64,
            "limits": {
                "max_input_tokens": 20000,
                "max_output_tokens": 1200,
                "timeout_ms": 20000,
                "budget_usd": "1.00",
            },
            "idempotency_key": "idem-1",
        },
        profile=PROFILE,
        cancellation=MutableCancellationToken(cancelled),
    )
~~~

- [ ] **Step 7: Append deterministic scenario and response-boundary tests**

Append to backend/tests/contract/test_mock_scenarios.py:

~~~python


@pytest.mark.parametrize(
    ("scenario", "error_code"),
    (("timeout", "timeout"), ("rate_limit", "rate_limit"), ("cancelled", "cancelled")),
)
def test_operational_scenarios_are_explicit(scenario: str, error_code: str) -> None:
    with pytest.raises(AdapterError) as error:
        DeterministicMock(scenario, seed=7).invoke(request())
    assert error.value.code == error_code


@pytest.mark.parametrize(
    "scenario",
    (
        "success",
        "low_confidence",
        "source_insufficient",
        "bad_schema",
        "prompt_injection",
        "duplicate_response",
        "wording_only",
    ),
)
def test_scenarios_are_deterministic_and_network_free(
    scenario: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_socket(*args: object, **kwargs: object) -> None:
        raise AssertionError("mock attempted network")

    monkeypatch.setattr(socket, "socket", fail_socket)
    first = DeterministicMock(scenario, seed=7).invoke(request())
    second = DeterministicMock(scenario, seed=7).invoke(request())
    assert first == second
    assert first.response_schema_version is ResponseSchemaVersion.V1
    if first.status is not ResponseStatus.CANDIDATE:
        assert first.content == {}


def test_cancellation_is_checked_before_recording_a_call() -> None:
    mock = DeterministicMock("success", seed=7)
    with pytest.raises(AdapterError) as error:
        mock.invoke(request(cancelled=True))
    assert error.value.code == "cancelled"
    assert mock.calls == []


def test_duplicate_idempotency_replays_the_same_bounded_response() -> None:
    mock = DeterministicMock("duplicate_response", seed=7)
    first = mock.invoke(request())
    second = mock.invoke(request())
    assert first == second
    assert mock.calls == ["idem-1", "idem-1"]
    assert first.usage == Usage(0, 0, Decimal("0.0000"))


def test_wording_change_cannot_change_canonical_fields() -> None:
    first = validate_candidate(DeterministicMock("success", seed=7).invoke(request()))
    second = validate_candidate(DeterministicMock("wording_only", seed=7).invoke(request()))
    assert first.canonical_domain_fields == second.canonical_domain_fields


def test_non_candidate_cannot_validate_as_authoritative() -> None:
    response = DeterministicMock("source_insufficient", seed=7).invoke(request())
    with pytest.raises(ConfigError) as error:
        validate_candidate(response)
    assert error.value.code == "candidate_not_authoritative"


def test_non_candidate_content_and_bad_candidate_schema_fail_closed() -> None:
    with pytest.raises(ValueError, match="non-candidate"):
        ProviderResponseEnvelope.create(
            request(),
            ResponseStatus.SOURCE_INSUFFICIENT,
            {"unexpected": "candidate"},
            usage=Usage(0, 0, Decimal("0.0000")),
        )
    with pytest.raises(ValueError, match="schema"):
        ProviderResponseEnvelope.create(
            request(),
            ResponseStatus.CANDIDATE,
            {"canonical_domain_fields": {}, "wording": "synthetic"},
            usage=Usage(0, 0, Decimal("0.0000")),
        )
~~~

- [ ] **Step 8: Run red**

~~~powershell
$red=Invoke-BoundedNative $PythonExe @("-m","pytest","backend/tests/contract/test_provider_contract.py","backend/tests/contract/test_mock_scenarios.py","-q") 120
if ($red.ExitCode -eq 0 -or ($red.Stdout+$red.Stderr) -notmatch "provider") { throw "T-07 red evidence invalid" }
~~~

- [ ] **Step 9: Define provider names, cancellation, and request limits**

Create backend/src/projectb/infrastructure/providers/base.py:

~~~python
from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from enum import StrEnum
from types import MappingProxyType
from typing import Protocol, cast, runtime_checkable

from projectb.domain.provider import ProviderProfile

_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
_HASH = re.compile(r"^[0-9a-f]{64}$")
_BUDGET = re.compile(r"^(?:0|[1-9][0-9]{0,3})(?:\.[0-9]{1,2})?$")
_FORBIDDEN = frozenset(
    {
        "adapter_id",
        "provider_profile_id",
        "config_fingerprint",
        "path",
        "local_path",
        "url",
        "credential_ref",
        "secret",
        "api_key",
        "token",
        "tools",
        "tool",
        "body",
        "prompt",
    }
)
type PayloadValue = str | int | tuple[str, ...]


class PortName(StrEnum):
    PROPOSE_CONCEPT_COVERAGE = "propose_concept_coverage"
    GENERATE_EXPLANATION = "generate_explanation"
    GENERATE_PRACTICE_CANDIDATE = "generate_practice_candidate"
    ANALYZE_EXAM_MATERIAL = "analyze_exam_material"
    GENERATE_FEEDBACK = "generate_feedback"


class PortVersion(StrEnum):
    V1 = "v1"


class PayloadSchemaVersion(StrEnum):
    V1 = "v1"


class ResponseSchemaVersion(StrEnum):
    V1 = "v1"


class ResponseStatus(StrEnum):
    CANDIDATE = "candidate"
    SOURCE_INSUFFICIENT = "source_insufficient"
    SCHEMA_REJECTED = "schema_rejected"
    PROVIDER_SCOPE_VIOLATION = "provider_scope_violation"
    PROVIDER_CONFIG_INVALID = "provider_config_invalid"
    CREDENTIAL_UNAVAILABLE = "credential_unavailable"
    CAPABILITY_UNSUPPORTED = "capability_unsupported"
    POLICY_UNKNOWN = "policy_unknown"
    PROVIDER_FAILED = "provider_failed"
    CANCELLED = "cancelled"
    BUDGET_EXCEEDED = "budget_exceeded"
~~~

- [ ] **Step 10: Append cancellation, primitive validators, and consent proof**

Append to backend/src/projectb/infrastructure/providers/base.py:

~~~python


@runtime_checkable
class CancellationToken(Protocol):
    def is_cancelled(self) -> bool:
        raise NotImplementedError


@dataclass
class MutableCancellationToken:
    cancelled: bool = False

    def is_cancelled(self) -> bool:
        return self.cancelled


def _require_id(value: object, code: str) -> str:
    if type(value) is not str or _ID.fullmatch(value) is None:
        raise ValueError(code)
    return value


def _require_hash(value: object, code: str) -> str:
    if type(value) is not str or _HASH.fullmatch(value) is None:
        raise ValueError(code)
    return value


def _require_mode(value: object) -> str:
    if type(value) is not str or value not in {"P", "F"}:
        raise ValueError("provider consent proof")
    return value


def _require_scope(value: object) -> tuple[str, ...]:
    if not isinstance(value, (tuple, list)) or not 1 <= len(value) <= 64:
        raise ValueError("provider payload source scope")
    result = tuple(_require_id(item, "provider payload source scope") for item in value)
    if result != tuple(sorted(set(result))):
        raise ValueError("provider payload source scope")
    return result


@dataclass(frozen=True)
class ConsentScopeProof:
    consent_id: str
    mode: str
    scope_token: str
    scope_digest: str
    config_fingerprint: str
    capability_snapshot_id: str
    policy_snapshot_id: str

    @classmethod
    def from_mapping(cls, payload: object) -> ConsentScopeProof:
        if not isinstance(payload, Mapping) or set(payload) != {
            "consent_id",
            "mode",
            "scope_token",
            "scope_digest",
            "config_fingerprint",
            "capability_snapshot_id",
            "policy_snapshot_id",
        }:
            raise ValueError("provider consent proof")
        return cls(
            _require_id(payload["consent_id"], "provider consent proof"),
            _require_mode(payload["mode"]),
            _require_hash(payload["scope_token"], "provider consent proof"),
            _require_hash(payload["scope_digest"], "provider consent proof"),
            _require_hash(payload["config_fingerprint"], "provider consent proof"),
            _require_id(payload["capability_snapshot_id"], "provider consent proof"),
            _require_id(payload["policy_snapshot_id"], "provider consent proof"),
        )
~~~

- [ ] **Step 11: Append request limits and exact per-port payload validation**

Append to backend/src/projectb/infrastructure/providers/base.py:

~~~python


@dataclass(frozen=True)
class RequestLimits:
    max_input_tokens: int
    max_output_tokens: int
    timeout_ms: int
    budget_usd: Decimal

    @classmethod
    def from_mapping(cls, payload: object) -> RequestLimits:
        if not isinstance(payload, Mapping) or set(payload) != {
            "max_input_tokens",
            "max_output_tokens",
            "timeout_ms",
            "budget_usd",
        }:
            raise ValueError("provider request limits")
        input_tokens = payload["max_input_tokens"]
        output_tokens = payload["max_output_tokens"]
        timeout_ms = payload["timeout_ms"]
        raw_budget = payload["budget_usd"]
        if (
            type(input_tokens) is not int
            or not 1 <= input_tokens <= 200_000
            or type(output_tokens) is not int
            or not 1 <= output_tokens <= 32_768
            or type(timeout_ms) is not int
            or not 1_000 <= timeout_ms <= 120_000
            or type(raw_budget) is not str
            or _BUDGET.fullmatch(raw_budget) is None
        ):
            raise ValueError("provider request limits")
        try:
            budget = Decimal(raw_budget)
        except (InvalidOperation, ValueError):
            raise ValueError("provider request limits") from None
        if not budget.is_finite() or budget > Decimal("1000"):
            raise ValueError("provider request limits")
        return cls(input_tokens, output_tokens, timeout_ms, budget.quantize(Decimal("0.01")))


_PORT_FIELDS: dict[PortName, frozenset[str]] = {
    PortName.PROPOSE_CONCEPT_COVERAGE: frozenset({"goal_id", "source_scope"}),
    PortName.GENERATE_EXPLANATION: frozenset({"concept_id", "source_scope"}),
    PortName.GENERATE_PRACTICE_CANDIDATE: frozenset(
        {"concept_id", "difficulty", "source_scope"}
    ),
    PortName.ANALYZE_EXAM_MATERIAL: frozenset({"exam_context_id", "source_scope"}),
    PortName.GENERATE_FEEDBACK: frozenset({"attempt_id", "source_scope"}),
}


def _validated_port_payload(
    port_name: PortName,
    payload: object,
) -> Mapping[str, PayloadValue]:
    if not isinstance(payload, Mapping) or set(payload) != _PORT_FIELDS[port_name]:
        raise ValueError("provider payload shape")
    frozen: dict[str, PayloadValue] = {}
    for key, value in payload.items():
        if key == "source_scope":
            frozen[key] = _require_scope(value)
        elif key == "difficulty":
            if type(value) is not int or not 1 <= value <= 5:
                raise ValueError("provider payload difficulty")
            frozen[key] = value
        else:
            frozen[key] = _require_id(value, "provider payload identity")
    return MappingProxyType(frozen)
~~~

- [ ] **Step 12: Append authorized request construction**

Append to backend/src/projectb/infrastructure/providers/base.py:

~~~python


@dataclass(frozen=True)
class ProviderRequestEnvelope:
    port_name: PortName
    port_version: PortVersion
    payload_schema_version: PayloadSchemaVersion
    request_id: str
    course_id: str
    task_id: str
    provider_profile_id: str
    config_fingerprint: str
    consent_proof: ConsentScopeProof
    payload: Mapping[str, PayloadValue]
    input_digest: str
    limits: RequestLimits
    idempotency_key: str
    cancellation: CancellationToken = field(compare=False, repr=False)

    @classmethod
    def from_authorized_mapping(
        cls,
        payload: Mapping[str, object],
        *,
        profile: ProviderProfile,
        cancellation: CancellationToken,
    ) -> ProviderRequestEnvelope:
        if type(profile) is not ProviderProfile:
            raise ValueError("validated ProviderProfile required")
        if not isinstance(payload, Mapping) or any(
            type(key) is not str or key in _FORBIDDEN for key in payload
        ):
            raise ValueError("forbidden provider request field")
        required = {
            "port_name",
            "port_version",
            "payload_schema_version",
            "request_id",
            "course_id",
            "task_id",
            "consent_proof",
            "payload",
            "input_digest",
            "limits",
            "idempotency_key",
        }
        if set(payload) != required:
            raise ValueError("provider request shape")
        try:
            port_name = PortName(cast(str, payload["port_name"]))
            port_version = PortVersion(cast(str, payload["port_version"]))
            payload_version = PayloadSchemaVersion(
                cast(str, payload["payload_schema_version"])
            )
        except (TypeError, ValueError):
            raise ValueError("provider request version") from None
        proof = ConsentScopeProof.from_mapping(payload["consent_proof"])
        if proof.config_fingerprint != profile.config_fingerprint:
            raise ValueError("provider profile proof mismatch")
        if not isinstance(cancellation, CancellationToken):
            raise ValueError("cancellation token required")
        return cls(
            port_name,
            port_version,
            payload_version,
            _require_id(payload["request_id"], "provider request identity"),
            _require_id(payload["course_id"], "provider request identity"),
            _require_id(payload["task_id"], "provider task identity"),
            profile.profile_id,
            profile.config_fingerprint,
            proof,
            _validated_port_payload(port_name, payload["payload"]),
            _require_hash(payload["input_digest"], "provider input digest"),
            RequestLimits.from_mapping(payload["limits"]),
            _require_id(payload["idempotency_key"], "provider idempotency key"),
            cancellation,
        )

~~~

- [ ] **Step 13: Append immutable request serialization**

Append to backend/src/projectb/infrastructure/providers/base.py:

~~~python
    def to_mapping(self) -> dict[str, object]:
        return {
            "port_name": self.port_name.value,
            "port_version": self.port_version.value,
            "payload_schema_version": self.payload_schema_version.value,
            "request_id": self.request_id,
            "course_id": self.course_id,
            "task_id": self.task_id,
            "provider_profile_id": self.provider_profile_id,
            "config_fingerprint": self.config_fingerprint,
            "consent_proof": {
                "consent_id": self.consent_proof.consent_id,
                "mode": self.consent_proof.mode,
                "scope_token": self.consent_proof.scope_token,
                "scope_digest": self.consent_proof.scope_digest,
                "config_fingerprint": self.consent_proof.config_fingerprint,
                "capability_snapshot_id": self.consent_proof.capability_snapshot_id,
                "policy_snapshot_id": self.consent_proof.policy_snapshot_id,
            },
            "payload": dict(self.payload),
            "input_digest": self.input_digest,
            "limits": {
                "max_input_tokens": self.limits.max_input_tokens,
                "max_output_tokens": self.limits.max_output_tokens,
                "timeout_ms": self.limits.timeout_ms,
                "budget_usd": format(self.limits.budget_usd, "f"),
            },
            "idempotency_key": self.idempotency_key,
        }
~~~

- [ ] **Step 14: Append bounded usage accounting**

Append to backend/src/projectb/infrastructure/providers/base.py:

~~~python


@dataclass(frozen=True)
class Usage:
    input_tokens: int
    output_tokens: int
    cost_usd: Decimal

    def __post_init__(self) -> None:
        if (
            type(self.input_tokens) is not int
            or not 0 <= self.input_tokens <= 200_000
            or type(self.output_tokens) is not int
            or not 0 <= self.output_tokens <= 32_768
            or type(self.cost_usd) is not Decimal
            or not self.cost_usd.is_finite()
            or not Decimal("0") <= self.cost_usd <= Decimal("1000")
            or self.cost_usd != self.cost_usd.quantize(Decimal("0.0001"))
        ):
            raise ValueError("provider usage")
~~~

- [ ] **Step 15: Append strict response construction**

Append to backend/src/projectb/infrastructure/providers/base.py:

~~~python


@dataclass(frozen=True)
class ProviderResponseEnvelope:
    response_schema_version: ResponseSchemaVersion
    request_id: str
    task_id: str
    port_name: PortName
    port_version: PortVersion
    status: ResponseStatus
    content: Mapping[str, object]
    citations: tuple[str, ...]
    uncertainties: tuple[str, ...]
    usage: Usage
    provider_ref: str | None

    @classmethod
    def create(
        cls,
        request: ProviderRequestEnvelope,
        status: ResponseStatus,
        content: Mapping[str, object],
        *,
        usage: Usage,
        provider_ref: str | None = None,
    ) -> ProviderResponseEnvelope:
        if type(status) is not ResponseStatus:
            raise ValueError("provider response status")
        if provider_ref is not None:
            _require_id(provider_ref, "provider response reference")
        if status is ResponseStatus.CANDIDATE:
            if set(content) != {"canonical_domain_fields", "wording"}:
                raise ValueError("provider response schema")
            fields = content["canonical_domain_fields"]
            wording = content["wording"]
            if not isinstance(fields, Mapping) or set(fields) != {
                "concept_id",
                "candidate_kind",
                "confidence",
            }:
                raise ValueError("provider response schema")
            if (
                type(fields["concept_id"]) is not str
                or type(fields["candidate_kind"]) is not str
                or _ID.fullmatch(fields["concept_id"]) is None
                or _ID.fullmatch(fields["candidate_kind"]) is None
                or type(fields["confidence"]) is not float
                or not 0 <= fields["confidence"] <= 1
                or type(wording) is not str
                or not 1 <= len(wording) <= 4096
            ):
                raise ValueError("provider response schema")
            frozen_fields: Mapping[str, object] = MappingProxyType(dict(fields))
            frozen_content: Mapping[str, object] = MappingProxyType(
                {"canonical_domain_fields": frozen_fields, "wording": wording}
            )
        else:
            if content:
                raise ValueError("non-candidate content must be empty")
            frozen_content = MappingProxyType({})
        return cls(
            ResponseSchemaVersion.V1,
            request.request_id,
            request.task_id,
            request.port_name,
            request.port_version,
            status,
            frozen_content,
            tuple(),
            tuple(),
            usage,
            provider_ref,
        )
~~~

- [ ] **Step 16: Append adapter capabilities and protocol**

Append to backend/src/projectb/infrastructure/providers/base.py:

~~~python


@dataclass(frozen=True)
class CapabilityDescriptor:
    adapter_id: str
    ports: tuple[PortName, ...]
    supports_file_search: bool
    supports_page_locator: bool

    def __post_init__(self) -> None:
        if (
            _ID.fullmatch(self.adapter_id) is None
            or not self.ports
            or len(set(self.ports)) != len(self.ports)
            or type(self.supports_file_search) is not bool
            or type(self.supports_page_locator) is not bool
        ):
            raise ValueError("provider capability")


class ProviderAdapter(Protocol):
    adapter_id: str

    def describe(self) -> CapabilityDescriptor:
        raise NotImplementedError

    def invoke(
        self,
        request: ProviderRequestEnvelope,
        secret_handle: object | None = None,
    ) -> ProviderResponseEnvelope:
        raise NotImplementedError
~~~

- [ ] **Step 17: Create deterministic mock scenario dispatch**

Create backend/src/projectb/infrastructure/providers/mock.py:

~~~python
from __future__ import annotations

from decimal import Decimal
from hashlib import sha256

from projectb.infrastructure.providers.base import (
    CapabilityDescriptor,
    PortName,
    ProviderRequestEnvelope,
    ProviderResponseEnvelope,
    ResponseStatus,
    Usage,
)


class AdapterError(Exception):
    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


class DeterministicMock:
    adapter_id = "mock"

    def __init__(self, scenario: str, *, seed: int) -> None:
        self.scenario = scenario
        self.seed = seed
        self.calls: list[str] = []

    def describe(self) -> CapabilityDescriptor:
        return CapabilityDescriptor("mock", tuple(PortName), False, True)

    def invoke(
        self,
        request: ProviderRequestEnvelope,
        secret_handle: object | None = None,
    ) -> ProviderResponseEnvelope:
        if secret_handle is not None:
            raise AdapterError("mock_must_not_resolve_credentials")
        if request.cancellation.is_cancelled() or self.scenario == "cancelled":
            raise AdapterError("cancelled")
        self.calls.append(request.idempotency_key)
        digest = sha256(
            f"{self.seed}|{request.idempotency_key}".encode("ascii")
        ).hexdigest()
        if self.scenario in {"timeout", "rate_limit"}:
            raise AdapterError(self.scenario)
        if self.scenario == "source_insufficient":
            return self._response(request, ResponseStatus.SOURCE_INSUFFICIENT, {})
        if self.scenario in {"bad_schema", "prompt_injection"}:
            return self._response(request, ResponseStatus.SCHEMA_REJECTED, {})
        if self.scenario == "low_confidence":
            return self._candidate(request, digest, 0.2, "synthetic low confidence")
        if self.scenario not in {"success", "duplicate_response", "wording_only"}:
            raise AdapterError("unknown_mock_scenario")
        wording = (
            "different synthetic wording"
            if self.scenario == "wording_only"
            else "synthetic explanation"
        )
        return self._candidate(request, digest, 0.8, wording)

~~~

- [ ] **Step 18: Append deterministic candidate and response helpers**

Append to backend/src/projectb/infrastructure/providers/mock.py:

~~~python
    def _candidate(
        self,
        request: ProviderRequestEnvelope,
        digest: str,
        confidence: float,
        wording: str,
    ) -> ProviderResponseEnvelope:
        content: dict[str, object] = {
            "canonical_domain_fields": {
                "concept_id": "mutex",
                "candidate_kind": "explanation",
                "confidence": confidence,
            },
            "wording": wording,
        }
        return self._response(
            request,
            ResponseStatus.CANDIDATE,
            content,
            provider_ref=f"mock-{digest[:16]}",
        )

    @staticmethod
    def _response(
        request: ProviderRequestEnvelope,
        status: ResponseStatus,
        content: dict[str, object],
        *,
        provider_ref: str | None = None,
    ) -> ProviderResponseEnvelope:
        return ProviderResponseEnvelope.create(
            request,
            status,
            content,
            usage=Usage(0, 0, Decimal("0.0000")),
            provider_ref=provider_ref,
        )
~~~

- [ ] **Step 19: Define built-in manifest and candidate result types**

Create backend/src/projectb/application/provider.py:

~~~python
from __future__ import annotations

import re
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import Literal

from projectb.domain.provider import ProfileError, ProviderProfile, validate_provider_profile
from projectb.infrastructure.providers.base import (
    PortName,
    ProviderAdapter,
    ProviderResponseEnvelope,
    ResponseSchemaVersion,
    ResponseStatus,
)

RuntimeProfile = Literal["local", "test", "demo"]
AdapterFactory = Callable[[], ProviderAdapter]
_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
_FACTORY_NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_.:]{0,255}$")


class ConfigError(Exception):
    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


@dataclass(frozen=True)
class BuiltinManifestEntry:
    adapter_id: str
    profile_schema_version: str
    factory_module: str
    factory_qualname: str
    ports: tuple[PortName, ...]

    def __post_init__(self) -> None:
        if (
            _ID.fullmatch(self.adapter_id) is None
            or self.profile_schema_version != "v1"
            or _FACTORY_NAME.fullmatch(self.factory_module) is None
            or _FACTORY_NAME.fullmatch(self.factory_qualname) is None
            or not self.ports
            or len(set(self.ports)) != len(self.ports)
        ):
            raise ConfigError("builtin_manifest_invalid")


@dataclass(frozen=True)
class BuiltinManifest:
    manifest_id: str
    entries: tuple[BuiltinManifestEntry, ...]

    def __post_init__(self) -> None:
        adapter_ids = tuple(entry.adapter_id for entry in self.entries)
        if (
            _ID.fullmatch(self.manifest_id) is None
            or not self.entries
            or len(adapter_ids) != len(set(adapter_ids))
        ):
            raise ConfigError("builtin_manifest_invalid")


@dataclass(frozen=True)
class ReviewedBuiltinBinding:
    manifest: BuiltinManifest
    factory: AdapterFactory


@dataclass(frozen=True)
class CandidateValidation:
    canonical_domain_fields: Mapping[str, object]
    wording: str
~~~

- [ ] **Step 20: Append reviewed registry construction and lookup**

Append to backend/src/projectb/application/provider.py:

~~~python


class ProviderAdapterRegistry:
    def __init__(
        self,
        runtime_profile: RuntimeProfile,
        adapters: Mapping[str, ProviderAdapter],
        authority_manifest: BuiltinManifest | None,
    ) -> None:
        if runtime_profile not in {"local", "test", "demo"}:
            raise ConfigError("runtime_profile_invalid")
        if len(adapters) != len(set(adapters)):
            raise ConfigError("duplicate_adapter")
        self._runtime_profile = runtime_profile
        self._adapters = MappingProxyType(dict(adapters))
        self._authority_manifest = authority_manifest

    @classmethod
    def from_reviewed_builtin(
        cls,
        binding: ReviewedBuiltinBinding,
        *,
        coordinator_manifest: BuiltinManifest,
        coordinator_factory: AdapterFactory,
    ) -> ProviderAdapterRegistry:
        if (
            binding.manifest is not coordinator_manifest
            or binding.factory is not coordinator_factory
            or len(coordinator_manifest.entries) != 1
        ):
            raise ConfigError("builtin_authority_mismatch")
        entry = coordinator_manifest.entries[0]
        if (
            binding.factory.__module__ != entry.factory_module
            or binding.factory.__qualname__ != entry.factory_qualname
        ):
            raise ConfigError("builtin_factory_mismatch")
        adapter = binding.factory()
        descriptor = adapter.describe()
        if (
            adapter.adapter_id != entry.adapter_id
            or descriptor.adapter_id != entry.adapter_id
            or descriptor.ports != entry.ports
        ):
            raise ConfigError("builtin_factory_mismatch")
        return cls("local", {entry.adapter_id: adapter}, coordinator_manifest)

    @classmethod
    def for_test_demo(
        cls,
        runtime_profile: Literal["test", "demo"],
        adapters: tuple[ProviderAdapter, ...],
    ) -> ProviderAdapterRegistry:
        if runtime_profile not in {"test", "demo"}:
            raise ConfigError("runtime_profile_invalid")
        ids = tuple(adapter.adapter_id for adapter in adapters)
        if not ids or len(ids) != len(set(ids)) or any(value != "mock" for value in ids):
            raise ConfigError("duplicate_or_forbidden_adapter")
        return cls(runtime_profile, dict(zip(ids, adapters, strict=True)), None)
~~~

- [ ] **Step 21: Append validated profile and demo lookups**

Append to backend/src/projectb/application/provider.py:

~~~python

    def for_profile(self, profile: ProviderProfile) -> ProviderAdapter | ConfigError:
        if self._runtime_profile != "local":
            return ConfigError("provider_profile_not_used_in_demo")
        if type(profile) is not ProviderProfile:
            return ConfigError("provider_config_invalid")
        validated = validate_provider_profile(
            {
                "profile_id": profile.profile_id,
                "adapter_id": profile.adapter_id,
                "model_id": profile.model_id,
                "region": profile.region,
                "max_output_tokens": profile.max_output_tokens,
                "timeout_ms": profile.timeout_ms,
                "daily_budget_usd": format(profile.daily_budget_usd, "f"),
                "credential_ref": profile.credential_ref,
                "schema_version": profile.schema_version,
            }
        )
        if isinstance(validated, ProfileError) or validated != profile:
            return ConfigError("provider_config_invalid")
        if self._authority_manifest is None:
            return ConfigError("builtin_authority_missing")
        entry_ids = {entry.adapter_id for entry in self._authority_manifest.entries}
        if profile.adapter_id not in entry_ids:
            return ConfigError("adapter_unavailable")
        adapter = self._adapters.get(profile.adapter_id)
        return adapter if adapter is not None else ConfigError("adapter_unavailable")

    def test_demo_adapter(self) -> ProviderAdapter | ConfigError:
        if self._runtime_profile not in {"test", "demo"}:
            return ConfigError("adapter_unavailable")
        adapter = self._adapters.get("mock")
        return adapter if adapter is not None else ConfigError("adapter_unavailable")
~~~

- [ ] **Step 22: Append candidate-only validation**

Append to backend/src/projectb/application/provider.py:

~~~python


def validate_candidate(response: ProviderResponseEnvelope) -> CandidateValidation:
    if response.response_schema_version is not ResponseSchemaVersion.V1:
        raise ConfigError("schema_rejected")
    if response.status is not ResponseStatus.CANDIDATE:
        raise ConfigError("candidate_not_authoritative")
    fields = response.content.get("canonical_domain_fields")
    wording = response.content.get("wording")
    if not isinstance(fields, Mapping) or type(wording) is not str:
        raise ConfigError("schema_rejected")
    if set(fields) != {"concept_id", "candidate_kind", "confidence"}:
        raise ConfigError("schema_rejected")
    if (
        type(fields["concept_id"]) is not str
        or type(fields["candidate_kind"]) is not str
        or _ID.fullmatch(fields["concept_id"]) is None
        or _ID.fullmatch(fields["candidate_kind"]) is None
        or type(fields["confidence"]) is not float
        or not 0 <= fields["confidence"] <= 1
        or not 1 <= len(wording) <= 4096
    ):
        raise ConfigError("schema_rejected")
    return CandidateValidation(MappingProxyType(dict(fields)), wording)
~~~

- [ ] **Step 23: Run focused green**

~~~powershell
Invoke-CheckedPython @("-m","pytest","backend/tests/contract/test_provider_contract.py","backend/tests/contract/test_mock_scenarios.py","-q") 120
~~~

- [ ] **Step 24: Run the complete displayed port/schema/authority matrix**

~~~powershell
Invoke-CheckedPython @("-m","pytest","backend/tests/contract/test_provider_contract.py","backend/tests/contract/test_mock_scenarios.py","-q") 120
~~~

Expected: all five port payload schemas, caller-claim rejection, manifest/factory object identity, duplicate rejection, cancellation, idempotency replay, strict response version/schema, non-candidate emptiness, injection-as-data, and no-network scenarios pass.

- [ ] **Step 25: Run Ruff 0.15.22, mypy 2.3.0, contract/backend/canonical tests**

~~~powershell
Invoke-CheckedPython @("-m","ruff","check","--config","backend/pyproject.toml","backend/src/projectb/infrastructure/providers/base.py","backend/src/projectb/infrastructure/providers/mock.py","backend/src/projectb/application/provider.py","backend/tests/contract/test_provider_contract.py","backend/tests/contract/test_mock_scenarios.py") 120
Invoke-CheckedPython @("-m","mypy","--config-file","backend/pyproject.toml","backend/src/projectb/infrastructure/providers/base.py","backend/src/projectb/infrastructure/providers/mock.py","backend/src/projectb/application/provider.py","backend/tests/contract/test_provider_contract.py","backend/tests/contract/test_mock_scenarios.py") 120
Invoke-CheckedPython @("-m","pytest","backend/tests/contract","-q") 180
Invoke-CheckedPython @("-m","pytest","backend/tests","-q") 300
Invoke-CheckedPython @("scripts/test_all.py") 900
~~~

- [ ] **Step 26: Run both reviews**

SPEC review checks AC-21/AC-22/AC-23/AC-24/AC-30/AC-32/AC-38/AC-39/AC-49: one envelope, five ports, no paths/tools/credentials, candidate-only authority, explicit mock separation, deterministic wording invariance, no agent loop. Quality/security/license review checks strict mapping, idempotency, timeout/cancel status, injection-as-data, socket absence, registry fail-closed behavior, redaction, and licenses.

- [ ] **Step 27: Stage, scan, and capture the private T-07 packet**

~~~powershell
$expected=@("backend/src/projectb/infrastructure/providers/base.py","backend/src/projectb/infrastructure/providers/mock.py","backend/src/projectb/application/provider.py","backend/tests/contract/test_provider_contract.py","backend/tests/contract/test_mock_scenarios.py")
$reviewPacket=Start-UnitReview $expected
~~~

- [ ] **Step 28: Validate both T-07 review receipts**

~~~powershell
$receipts=Assert-UnitReviewReceipts $reviewPacket "T-07"
~~~

- [ ] **Step 29: Recheck and commit the reviewed T-07 tree**

~~~powershell
Complete-ReviewedUnit $expected $reviewPacket "feat(T-07): add provider-neutral contract and deterministic mock [agent: $env:PROJECTB_AGENT_ID]"
~~~

**Completion standard:** All later model calls compile against one deterministic contract without an LLM, and local production cannot silently fall back to mock.

## Mechanical Reconstruction And Self-Review

- [ ] **Reconstruct all Python code blocks**

Use a temporary directory outside the repository to materialize every Python fenced block at its named path in task order. Do not write implementation files in the project worktree. Run the approved CPython compileall over the reconstructed tree and record only sanitized diagnostics.

- [ ] **Run strict Ruff 0.15.22 reconstruction**

Run the pinned Ruff 0.15.22 executable through the bounded Python wrapper with --config backend/pyproject.toml against every reconstructed production/test file. Any diagnostic blocks this plan and must be repaired in the displayed block.

- [ ] **Run strict mypy 2.3.0 reconstruction**

Create only temporary package facades required to import the displayed modules, using exports already fixed by predecessor plans. Run pinned mypy 2.3.0 with --config-file backend/pyproject.toml. Undefined names, incompatible handoffs, untyped public contracts, or missing imports block review.

- [ ] **Parse PowerShell and Markdown**

Parse every PowerShell block with the approved PowerShell AST parser, require balanced fences, scan for disallowed implementation omissions, and verify all eight task IDs and 23 owned paths. No parse-only result is a review PASS.

- [ ] **Cross-plan review**

Compare this exact hash with root PLAN.md and direct predecessor/successor contracts. Check create/modify timing, SecurityError/CsrfService, ProviderProfile, SecretStore/SecretHandle, ConsentExpectation/scope token, ProviderRequest/Response envelopes, runtime profile serialization, security.py/app.py handoffs, whole-index safety, scanner/review packet, and cumulative tests.

Coverage is exact: T-04A/B/C, T-05A/B/C, T-06, and T-07 each have one dispatch body and one literal stage set. Shared security.py is serialized T-04A then T-04B; T-06 consumes it without staging. app.py remains T-04C after T-01B and before API-REG-01. No private courseware, real credential, external account data, live provider call, arbitrary endpoint, network fixture, remote action, or fabricated PASS appears.

G-02A, G-03, G-04, implementation approval, INT-01, remote CI, deployment, and student reflection remain externally owned and unexecuted. The coordinator links this plan's observed SHA-256 only after independent SPEC and quality/security/license reviewers both pass the same root/plan/tree snapshot.
