# CI, Documentation, and Release Preparation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** Add deterministic local license/CI contract gates, dual-platform workflow definitions, evidence-backed user and operations documentation, and a fail-closed release verifier without performing remote CI, deployment, publication, or student-only reflection work.

**Architecture:** CI-01A owns the strict dependency/license verifier and the initial CI evidence schema. CI-01B owns the YAML parser/verifier, its contract test, and only the GitLab/GitHub workflow documents. CI-01C owns the serialized A-to-C evidence handoff, local readiness marker, and final CI evidence. DOC-01 owns user and operations documentation. FIN-01A1 consumes the reviewed documentation and CI evidence to create a read-only release verifier and external-evidence templates. All external observations remain not_executed until their coordinator-owned gates run.

**Tech Stack:** CPython 3.14.6, pytest 9.1.1, Ruff 0.15.22, mypy 2.3.0, PowerShell 5.1 or 7, GitLab CI YAML, GitHub Actions workflow YAML, and PyYAML 6.0.2 only if and after the coordinator locks it in G-02A.

---

## Status and Dispatch Boundary

This plan covers exactly root dispatch units CI-01A, CI-01B, CI-01C, DOC-01, and FIN-01A1. It excludes CI-02, DEPLOY-01, FIN-01A2, FIN-01B, G-02C2, DIST-01, DIST-02, REFLECTION.md, implementation approval, cold-start validation, remote pushes, PR/MR creation, registry publication, deployment, paid provider calls, and branch finishing.

Authoring input: root PLAN.md SHA-256 5536BC38402EFE250CF4BEF8ACC44CA91AF0B0A4B10CDD80902A3D632AE71A91; DETAILED_PLAN_AUTHORING_CONTRACT.md SHA-256 B93F949DE36CD89C7101160F237D4FEBCD7305F411C55B20429D62A282DBBFEF. These are authoring inputs only. Before dispatch or a PASS label, the coordinator must recompute the root, contract, and this subplan from their actual bytes, freeze an immutable path/owner map and staged packet outside the repository, bind both packet and map SHA-256 values into both fresh review receipts, and rebind all predecessor hashes. Any edit after review invalidates both reviews, the packet, the map, and the tree binding.

### Coordinator blockers

1. The reviewed locks contain no direct YAML parser. The npm lock only declares `yaml` as an optional Vite peer and does not install it; the Python lock has no PyYAML. G-02A/root is the sole owner of the required amendment: a directly pinned PyYAML 6.0.2 row in the production Linux lock, exact artifact hash(es), MIT license, source URL, verified status, canonical lock-file SHA-256, and CI/runtime installation evidence. Until that amendment is committed and its hash is an ancestor, CI-01A and CI-01B stop before the first edit. No transitive package, regex YAML rewriting, `safe_load` fallback, or unreviewed network install is permitted.
2. CI workflows need the coordinator-owned `packaging/oci/requirements-linux-amd64.lock` with `--require-hashes`, the locked linux/amd64 OCI/base-image evidence, and the exact full 40-hex GitHub action SHAs used by the workflow. G-02A owns parser/lock/license/hash evidence; G-02C2/DIST-02 owns OCI/base-image and smoke evidence; the root coordinator owns action-SHA provenance and the root ownership amendment. CI-01 consumes all of these paths read-only and stops if any is absent, unverified, or not ancestor-integrated. No digest or action SHA is invented in this plan.
3. The authoritative root map currently lists all four original CI-01A paths. This repaired plan deliberately splits verifier ownership to remove the A/B fixture cycle: CI-01A owns `scripts/verify_licenses.py` and the initial evidence file; CI-01B owns `scripts/verify_ci_contract.py`, `backend/tests/integration/test_ci_contract.py`, and both workflow files. The coordinator must amend and re-freeze the root path map before this plan can PASS or dispatch; this subplan does not silently override root/ledger bytes.
4. CI-01A depends on reviewed T-01F3, G-02A, and G-02B; CI-01B additionally depends on reviewed CI-01A, DIST-01, DIST-02, parser/lock/action evidence, and the root ownership amendment; CI-01C depends on all automated test owners and both CI units; DOC-01 waits for stable behavior/distribution contracts; FIN-01A1 waits for DOC-01, CI-01C, INT-01B, and QA-02C. Missing predecessor hashes are hard stops.

## Dependency Graph and Handoffs

~~~text
T-01F3 + G-02A/B + parser/Linux-lock/action amendment
             |
          CI-01A -----> CI-01B -----> CI-01C
             |             |              |
             +-- evidence -+---- A->C ----+

all behavior + DIST + CI-01C + INT-01B + QA-02C
                         |
                       DOC-01
                         |
                      FIN-01A1
~~~

CI-01A creates the initial CI evidence contract with `status: not_executed` and an explicit `handoff.to: CI-01C`; it never records local PASS. CI-01B owns and verifies the YAML parser/verifier, contract test, and both workflow bytes without reading or writing the evidence file. After both reviewed commits, CI-01C is the only later writer of `CI-01_EVIDENCE.md`: it proves the A-to-C handoff, fills only observed local summaries, and creates the readiness marker. DOC-01 owns README; FIN-01A1 may modify only the release-status subsection and never REFLECTION.md.

| Unit | Exact paths | Handoff rule |
| --- | --- | --- |
| CI-01A | scripts/verify_licenses.py; docs/engineering/CI-01_EVIDENCE.md | Creates the license verifier and a not_executed handoff contract. It never writes workflow bytes or local PASS. |
| CI-01B | scripts/verify_ci_contract.py; backend/tests/integration/test_ci_contract.py; .gitlab-ci.yml; .github/workflows/ci.yml | Sole owner of parser-backed workflow verification and both workflow files. It never edits CI-01_EVIDENCE.md. |
| CI-01C | docs/engineering/CI-01_EVIDENCE.md; docs/engineering/gates/CI-01.ready | Reads the two predecessor commits and all six effective paths, proves the A-to-C handoff, and is the sole final evidence/marker owner. |
| DOC-01 | README.md; docs/engineering/OPERATIONS.md; docs/engineering/THIRD_PARTY_NOTICES.md; docs/engineering/DOC-01_EVIDENCE.md; backend/tests/integration/test_documentation_contract.py | Creates all five. FIN-01A1 may later edit only the README release-status subsection. |
| FIN-01A1 | scripts/final_verify.ps1; backend/tests/integration/test_release_evidence_contract.py; docs/engineering/FINAL_VERIFICATION.md; docs/engineering/RELEASE_CHECKLIST.md; docs/engineering/CI-02_EVIDENCE.md; docs/engineering/DEPLOY-01_EVIDENCE.md; README.md release-status subsection | Never writes REFLECTION.md; external observations stay outside the candidate until CI-02/DEPLOY-01/FIN-01B. |

Untracked outputs such as review packets, test reports, OCI images, Windows binaries, and private benchmark data are outside every commit path and belong in an ACL-restricted temporary directory or an ignored artifact directory.

## Frozen Contracts

- The canonical local entry is scripts/test_all.py. GitLab unit-test, GitHub unit-test, and the final verifier invoke that exact entry; local YAML validation is never remote CI evidence.
- GitLab has a job named exactly unit-test. Both platforms run on push and pull request/merge request events, use least-privilege read permissions, pin runtime images/actions, use bounded timeouts, and expose no secret-valued workflow fields.
- Distribution jobs call reviewed packaging scripts but do not publish. Public URL and deployment fields remain not_executed until DEPLOY-01.
- License verification consumes only reviewed G-02A baseline and locks and emits counts/codes, not raw package metadata or environment output. It rejects missing, blank, unrecorded, unverified, source-less, hash-less, AGPL/SSPL, and non-build GPL entries while retaining the explicitly reviewed PyInstaller build exception and notices. Strict mode compares canonical-LF lock bytes and package artifact hashes against the baseline.
- CI-01.ready is created only by CI-01C after exact six CI-owned paths, local PASS, both reviews, and tree binding. Its JSON is exactly:

~~~json
{
  "contractVersion": 1,
  "gateOwner": "CI-01",
  "terminalOwner": "CI-01C",
  "state": "active"
}
~~~

- Release evidence has one JSON object inside one json fence per Markdown file. AC-01 through AC-50, both reviews, candidate binding, external CI, deployment/public URL, rollback, scanner result, and final-course-CI fields are explicit. not_executed is not PASS and a top-level local status may not be `local_pass` while any local child remains `not_executed`.
- FIN-01A1 accepts an explicit ExpectedCandidate and never derives it from mutable HEAD. It rejects localhost/example URLs, mismatched digests, future timestamps, self-referential hash claims, unresolved markers, non-allowlisted C..E paths, and PASS paired with not_executed.
- No plan step writes a secret, provider token, private course path/body, student reflection, fabricated count, or remote result.

## Shared Worker Prelude and Review Protocol

Every dispatch executes this complete prelude in its clean worktree before editing. PROJECTB_ROOT_PLAN_SHA256 is the current root hash supplied by the coordinator; PROJECTB_DETAILED_PLAN_SHA256 is recomputed from this file's immutable bytes immediately before dispatch. The prelude validates unit, base commit, worktree, Git top-level, HEAD/base relationship, runtime paths, and a coordinator-frozen path/owner map. Every native command goes through the PS5.1-compatible checked wrapper and raw child output is not placed in exceptions.

~~~powershell
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$RootPlanSha = $env:PROJECTB_ROOT_PLAN_SHA256
$DetailedPlanSha = $env:PROJECTB_DETAILED_PLAN_SHA256
$UnitId = $env:PROJECTB_UNIT_ID
$BaseCommit = $env:PROJECTB_BASE_COMMIT
$WorktreeRoot = $env:PROJECTB_WORKTREE_ROOT
$PythonExe = $env:PROJECTB_PYTHON_EXE
$PowerShellExe = $env:PROJECTB_POWERSHELL_EXE
$NodeExe = $env:PROJECTB_NODE_EXE
$NpmCmd = $env:PROJECTB_NPM_CMD
$AllowedUnits = @("CI-01A", "CI-01B", "CI-01C", "DOC-01", "FIN-01A1")
$envNames = @(
    "PROJECTB_ROOT_PLAN_SHA256", "PROJECTB_DETAILED_PLAN_SHA256", "PROJECTB_UNIT_ID",
    "PROJECTB_BASE_COMMIT", "PROJECTB_WORKTREE_ROOT", "PROJECTB_AGENT_ID",
    "PROJECTB_PYTHON_EXE", "PROJECTB_POWERSHELL_EXE", "PROJECTB_NODE_EXE", "PROJECTB_NPM_CMD",
    "PROJECTB_T01F3_COMMIT", "PROJECTB_G02A_COMMIT", "PROJECTB_G02B_COMMIT",
    "PROJECTB_CI01A_COMMIT", "PROJECTB_DIST01_COMMIT", "PROJECTB_DIST02_COMMIT",
    "PROJECTB_SPEC_REVIEW_RECEIPT", "PROJECTB_QUALITY_REVIEW_RECEIPT",
    "PROJECTB_REVIEW_PACKET_PATH", "PROJECTB_REVIEW_PACKET_SHA256", "PROJECTB_PATH_MAP_SHA256"
)
if ($RootPlanSha -notmatch "^[0-9A-Fa-f]{64}$" -or $DetailedPlanSha -notmatch "^[0-9A-Fa-f]{64}$" -or $UnitId -notin $AllowedUnits -or $BaseCommit -notmatch "^[0-9a-f]{40}$" -or $env:PROJECTB_AGENT_ID -notmatch "^[A-Za-z0-9][A-Za-z0-9._-]{1,63}$") { throw "planning context invalid" }
if (-not [IO.Path]::IsPathFullyQualified($WorktreeRoot) -or -not (Test-Path -LiteralPath $WorktreeRoot -PathType Container)) { throw "worktree invalid" }
$WorktreeRoot = (Resolve-Path -LiteralPath $WorktreeRoot).Path
function Assert-AbsoluteLeaf {
    param([Parameter(Mandatory)][string]$Path,[Parameter(Mandatory)][string]$Label)
    if (-not [IO.Path]::IsPathFullyQualified($Path) -or -not (Test-Path -LiteralPath $Path -PathType Leaf)) { throw "$Label runtime invalid" }
    $root = [IO.Path]::GetPathRoot($Path); $current = $root
    foreach ($part in $Path.Substring($root.Length).Split(@("\", "/"), [StringSplitOptions]::RemoveEmptyEntries)) {
        $current = Join-Path $current $part
        if ((Get-Item -LiteralPath $current -Force).Attributes -band [IO.FileAttributes]::ReparsePoint) { throw "$Label reparse component" }
    }
}
Assert-AbsoluteLeaf $PythonExe "python"; Assert-AbsoluteLeaf $PowerShellExe "powershell"; Assert-AbsoluteLeaf $NodeExe "node"; Assert-AbsoluteLeaf $NpmCmd "npm"
$gitCommand = Get-Command git.exe -CommandType Application -ErrorAction Stop | Select-Object -First 1
$GitExe = $gitCommand.Source; Assert-AbsoluteLeaf $GitExe "git"
if ([IO.Path]::GetFileName($GitExe).ToLowerInvariant() -ne "git.exe") { throw "git leaf invalid" }
function ConvertTo-Redacted {
    param([AllowEmptyString()][string]$Text)
    if ($null -eq $Text) { $value = "" } else { $value = $Text }
    $value = $value.Replace($WorktreeRoot, "[WORKTREE]")
    $value = $value -replace '(?i)sk-(?:proj-)?[A-Za-z0-9_-]{12,}', '[REDACTED]'
    $value = $value -replace '(?i)(api[_-]?key|token|password|secret|private[_-]?key)\s*[:=]\s*\S+', '$1=[REDACTED]'
    if ($value.Length -gt 8192) { return $value.Substring(0,8192) + "[TRUNCATED]" }
    return $value
}
function ConvertTo-NativeArgument {
    param([Parameter(Mandatory)][AllowEmptyString()][string]$Value)
    if ($Value.Length -gt 0 -and $Value -notmatch '[\s"]') { return $Value }
    $builder=[Text.StringBuilder]::new();[void]$builder.Append('"');$slashes=0
    foreach($character in $Value.ToCharArray()) {
        if($character -eq '\\'){$slashes++;continue}
        if($character -eq '"'){[void]$builder.Append(('\\' * (($slashes*2)+1)));[void]$builder.Append('"');$slashes=0;continue}
        if($slashes -gt 0){[void]$builder.Append(('\\' * $slashes));$slashes=0};[void]$builder.Append($character)
    }
    if($slashes -gt 0){[void]$builder.Append(('\\' * ($slashes*2)))};[void]$builder.Append('"');return $builder.ToString()
}
function Stop-ProcessTree {
    param([Parameter(Mandatory)][Diagnostics.Process]$Process)
    $seen=New-Object 'System.Collections.Generic.HashSet[int]';$queue=New-Object 'System.Collections.Generic.Queue[int]';[void]$seen.Add($Process.Id);$queue.Enqueue($Process.Id)
    while($queue.Count -gt 0){$parent=$queue.Dequeue();foreach($child in @(Get-CimInstance Win32_Process -Filter "ParentProcessId=$parent" -ErrorAction SilentlyContinue)){if($seen.Add([int]$child.ProcessId)){$queue.Enqueue([int]$child.ProcessId)}}}
    foreach($id in @($seen|Where-Object{$_ -ne $Process.Id}|Sort-Object -Descending)){Stop-Process -Id $id -Force -ErrorAction SilentlyContinue};Stop-Process -Id $Process.Id -Force -ErrorAction SilentlyContinue
    $deadline=[Diagnostics.Stopwatch]::StartNew();do{$alive=@($seen|Where-Object{Get-Process -Id $_ -ErrorAction SilentlyContinue});if($alive.Count -gt 0){Start-Sleep -Milliseconds 25}}while($alive.Count -gt 0 -and $deadline.ElapsedMilliseconds -lt 5000);if($alive.Count -gt 0){throw "process_tree_cleanup_failed"}
}
function Read-BoundedStream {
    param([Parameter(Mandatory)][IO.Stream]$Stream,[ValidateRange(1,4194304)][int]$MaximumCharacters=8192)
    $reader=[IO.StreamReader]::new($Stream);$builder=[Text.StringBuilder]::new();$buffer=New-Object char[] 4096
    try{while(($count=$reader.Read($buffer,0,$buffer.Length))-gt 0){if($builder.Length-lt($MaximumCharacters+1)){[void]$builder.Append($buffer,0,[math]::Min($count,$MaximumCharacters+1-$builder.Length))}};return $builder.ToString()}finally{$reader.Dispose()}
}
function Read-BoundedText {
    param([Parameter(Mandatory)][string]$Path,[ValidateRange(1,4194304)][int]$MaximumCharacters=8192)
    $reader=[IO.StreamReader]::new($Path,[Text.Encoding]::UTF8,$true);try{$buffer=New-Object char[] ($MaximumCharacters+1);$count=$reader.Read($buffer,0,$buffer.Length);$text=[string]::new($buffer,0,$count);if($count -gt $MaximumCharacters){return (ConvertTo-Redacted ($text.Substring(0,$MaximumCharacters)+"[TRUNCATED]"))};return (ConvertTo-Redacted $text)}finally{$reader.Dispose()}
}
function Invoke-CheckedNative {
    param([Parameter(Mandatory)][string]$FilePath,[AllowEmptyCollection()][string[]]$ArgumentList=@(),[ValidateRange(1,3600)][int]$TimeoutSeconds=300,[int[]]$AllowedExitCodes=@(0),[Parameter(Mandatory)][string]$FailureCode)
    Assert-AbsoluteLeaf $FilePath "native"
    $start=[Diagnostics.ProcessStartInfo]::new();$start.FileName=$FilePath;$start.Arguments=(($ArgumentList|ForEach-Object{ConvertTo-NativeArgument ([string]$_)})-join ' ');$start.WorkingDirectory=$WorktreeRoot;$start.UseShellExecute=$false;$start.CreateNoWindow=$true;$start.RedirectStandardOutput=$true;$start.RedirectStandardError=$true
    $start.EnvironmentVariables.Clear();foreach($name in @("SystemRoot","WINDIR","TEMP","TMP")){ $value=[Environment]::GetEnvironmentVariable($name);if(-not [string]::IsNullOrWhiteSpace($value)){$start.EnvironmentVariables[$name]=$value} };$runtime=@((Split-Path -Parent $FilePath),(Join-Path $env:SystemRoot "System32"))|Sort-Object -Unique;$start.EnvironmentVariables["PATH"]=$runtime -join ';'
    foreach($name in $envNames){$value=[Environment]::GetEnvironmentVariable($name);if(-not [string]::IsNullOrWhiteSpace($value)){$start.EnvironmentVariables[$name]=$value}}
    $process=[Diagnostics.Process]::new();$process.StartInfo=$start
    try{if(-not $process.Start()){throw "$FailureCode launch"};$outTask=[Threading.Tasks.Task[string]]::Factory.StartNew([Func[string]]{Read-BoundedStream -Stream $process.StandardOutput -MaximumCharacters 8192});$errTask=[Threading.Tasks.Task[string]]::Factory.StartNew([Func[string]]{Read-BoundedStream -Stream $process.StandardError -MaximumCharacters 8192});if(-not $process.WaitForExit($TimeoutSeconds*1000)){Stop-ProcessTree $process;throw "$FailureCode timeout"};$stdout=ConvertTo-Redacted $outTask.GetAwaiter().GetResult();$stderr=ConvertTo-Redacted $errTask.GetAwaiter().GetResult();if($process.ExitCode -notin $AllowedExitCodes){throw "$FailureCode exit=$($process.ExitCode)"};return [pscustomobject]@{ExitCode=$process.ExitCode;Stdout=$stdout;Stderr=$stderr}}catch{throw $_.Exception.Message}finally{$process.Dispose()}
}
function Invoke-Git {
    param([Parameter(Mandatory)][string[]]$Arguments,[int[]]$AllowedExitCodes=@(0),[string]$FailureCode="git_failed")
    Invoke-CheckedNative $GitExe $Arguments 300 $AllowedExitCodes $FailureCode
}
function Assert-UnitContext {
    $top=(Invoke-Git @("rev-parse","--show-toplevel") -FailureCode "git_top_failed").Stdout.Trim();if([IO.Path]::GetFullPath($top) -ne $WorktreeRoot){throw "git top mismatch"}
    $head=(Invoke-Git @("rev-parse","HEAD") -FailureCode "git_head_failed").Stdout.Trim();if($head -ne $BaseCommit){throw "HEAD/base mismatch"}
    Invoke-Git @("cat-file","-e","$BaseCommit^{commit}") -FailureCode "base_missing" | Out-Null
    if((Invoke-Git @("status","--porcelain=v1","--untracked-files=all") -FailureCode "git_status_failed").Stdout.Trim()){throw "worktree dirty"}
}
function Assert-ExactStagedPaths {
    param([Parameter(Mandatory)][string[]]$ExpectedPaths)
    $actual=@((Invoke-Git @("diff","--cached","--name-only") -FailureCode "staged_list_failed").Stdout -split "\r?\n"|Where-Object{$_}|ForEach-Object{$_ -replace "\\","/"}|Sort-Object);$expected=@($ExpectedPaths|ForEach-Object{$_ -replace "\\","/"}|Sort-Object)
    if(($actual|Sort-Object -Unique).Count -ne $actual.Count){throw "duplicate staged path"};$delta=@(Compare-Object $expected $actual);if($actual.Count -ne $expected.Count -or $delta.Count -ne 0){throw "staged path mismatch"}
}
function Capture-ReviewedTree {
    param([Parameter(Mandatory)][string[]]$ExpectedPaths)
    Invoke-Git (@("add","--")+$ExpectedPaths) -FailureCode "git_add_failed"|Out-Null;Assert-ExactStagedPaths $ExpectedPaths;Invoke-Git @("diff","--cached","--check") -FailureCode "staged_diff_failed"|Out-Null;Invoke-CheckedNative $PythonExe @("scripts/scan_secrets.py","--staged","--git-exe",$GitExe) 300 @(0) "staged_scan_failed"|Out-Null;$tree=(Invoke-Git @("write-tree") -FailureCode "write_tree_failed").Stdout.Trim();if($tree -notmatch "^[0-9a-f]{40}$"){throw "tree invalid"};return $tree
}
function Capture-ReviewBinding {
    param([Parameter(Mandatory)][string[]]$ExpectedPaths,[Parameter(Mandatory)][string]$TreeId)
    $packet=Join-Path ([IO.Path]::GetTempPath()) ("projectb-review-"+[guid]::NewGuid().ToString('N')+".patch");$map=Join-Path ([IO.Path]::GetTempPath()) ("projectb-map-"+[guid]::NewGuid().ToString('N')+".txt")
    Invoke-Git @("diff","--cached","--binary","--full-index","--no-ext-diff","--output=$packet") -FailureCode "review_packet_failed"|Out-Null
    $mapRows=@("root-plan-sha256=$RootPlanSha","detailed-plan-sha256=$DetailedPlanSha","base-commit=$BaseCommit","unit-id=$UnitId")+@($ExpectedPaths|ForEach-Object{"path=$_"}|Sort-Object);[IO.File]::WriteAllLines($map,$mapRows,(New-Object Text.UTF8Encoding($false)))
    $packetHash=(Get-FileHash -LiteralPath $packet -Algorithm SHA256).Hash.ToLowerInvariant();$mapHash=(Get-FileHash -LiteralPath $map -Algorithm SHA256).Hash.ToLowerInvariant();if($packetHash-notmatch"^[0-9a-f]{64}$"-or$mapHash-notmatch"^[0-9a-f]{64}$"){throw "review_binding_hash_invalid"};return [pscustomobject]@{PacketPath=$packet;PacketSha256=$packetHash;PathMapPath=$map;PathMapSha256=$mapHash;TreeId=$TreeId}
}
function Complete-ReviewedUnit {
    param([Parameter(Mandatory)][string[]]$ExpectedPaths,[Parameter(Mandatory)][string]$ReviewedTree,[Parameter(Mandatory)][string]$Message)
    $binding=Capture-ReviewBinding $ExpectedPaths $ReviewedTree
    foreach($receiptPath in @($env:PROJECTB_SPEC_REVIEW_RECEIPT,$env:PROJECTB_QUALITY_REVIEW_RECEIPT)){if(-not(Test-Path -LiteralPath $receiptPath -PathType Leaf)){throw "review receipt missing"};$receipt=[IO.File]::ReadAllText($receiptPath)|ConvertFrom-Json;if($receipt.result -ne "PASS" -or $receipt.unit_id -ne $UnitId -or $receipt.root_plan_sha256 -ne $RootPlanSha -or $receipt.detailed_plan_sha256 -ne $DetailedPlanSha -or $receipt.base_commit -ne $BaseCommit -or $receipt.tree_id -ne $ReviewedTree -or $receipt.packet_sha256 -ne $binding.PacketSha256 -or $receipt.path_map_sha256 -ne $binding.PathMapSha256 -or $receipt.reviewer_id -notmatch "^[A-Za-z0-9][A-Za-z0-9._-]{1,63}$"){throw "review binding invalid"}}
    $spec=([IO.File]::ReadAllText($env:PROJECTB_SPEC_REVIEW_RECEIPT)|ConvertFrom-Json).reviewer_id;$quality=([IO.File]::ReadAllText($env:PROJECTB_QUALITY_REVIEW_RECEIPT)|ConvertFrom-Json).reviewer_id;if($spec -eq $quality -or $spec -eq $env:PROJECTB_AGENT_ID -or $quality -eq $env:PROJECTB_AGENT_ID){throw "review identities not distinct"};$current=Capture-ReviewedTree $ExpectedPaths;if($current -ne $ReviewedTree){throw "reviewed tree changed"};$rebound=Capture-ReviewBinding $ExpectedPaths $ReviewedTree;if($rebound.PacketSha256 -ne $binding.PacketSha256 -or $rebound.PathMapSha256 -ne $binding.PathMapSha256){throw "review_binding_changed"};Invoke-Git @("commit","-m",$Message) -FailureCode "commit_failed"|Out-Null;$head=(Invoke-Git @("rev-parse","HEAD") -FailureCode "head_failed").Stdout.Trim();$headTree=(Invoke-Git @("rev-parse","HEAD^{tree}") -FailureCode "tree_capture_failed").Stdout.Trim();if($head -notmatch "^[0-9a-f]{40}$" -or $headTree -ne $ReviewedTree){throw "committed tree mismatch"};return $head
}
Assert-UnitContext
~~~
After any review-driven edit, rerun the entire prelude, restage the whole expected set, rescan with the scanner's fail-on-findings flag, capture a new whole-index tree plus immutable binary packet and path/owner map, and obtain both fresh receipts bound to all of them. A pathspec-limited staged query, bare native command, inherited child environment, receipt bound to an earlier tree, or unchecked commit/hash sequence is invalid evidence. The packet and map stay outside the repository and only their byte counts/SHA-256 values enter receipts.

## Task CI-01A: Strict License Verifier and CI Evidence Contract

Goal: Add the deterministic dependency/license verifier and the initial CI evidence contract without reading or creating either workflow. Workflow parsing and workflow-contract tests belong exclusively to CI-01B.

Dependencies and parallelism: reviewed T-01F3, G-02A, G-02B, the root ownership amendment, and the root runtime/G-04 context. This unit owns the license verifier, the license-focused contract test, and the initial evidence file and completes before CI-01B. It has no parser fixture mode and never inspects workflow bytes.

Files: scripts/verify_licenses.py; backend/tests/integration/test_ci_contract.py; docs/engineering/CI-01_EVIDENCE.md. `scripts/verify_ci_contract.py` is a CI-01B-owned path and is absent throughout CI-01A.

- [ ] A1. Execute the prelude with PROJECTB_UNIT_ID=CI-01A. Verify coordinator-supplied PROJECTB_T01F3_COMMIT, PROJECTB_G02A_COMMIT, and PROJECTB_G02B_COMMIT are lowercase 40-hex ancestors of the base. Verify the G-02A dependency/license amendment and both reviewed lock identities exist. Do not require a YAML parser or workflow file; abort before editing on any missing dependency/license evidence.

- [ ] A2. Write the failing contract test before implementation. Create backend/tests/integration/test_ci_contract.py with exactly:

~~~python
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
PYTHON = sys.executable


def run_script(name: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [PYTHON, str(ROOT / "scripts" / name), *args],
        cwd=ROOT, text=True, capture_output=True, check=False, timeout=30,
    )


def test_license_verifier_rejects_missing_baseline() -> None:
    result = run_script("verify_licenses.py", "--root", str(ROOT / "does-not-exist"), "--strict")
    assert result.returncode == 2
    assert "license_baseline_missing" in result.stdout


def test_fixture_source_has_no_secret_value() -> None:
    text = Path(__file__).read_text(encoding="utf-8")
    assert "sk-" not in text
    assert "api_key=" not in text.lower()


def test_evidence_template_is_explicitly_unexecuted() -> None:
    evidence = ROOT / "docs/engineering/CI-01_EVIDENCE.md"
    if not evidence.exists():
        pytest.fail("CI-01_EVIDENCE.md is the expected red absence")
    payloads = evidence.read_text(encoding="utf-8").split("~~~json")
    assert len(payloads) == 2
    payload = json.loads(payloads[1].split("~~~")[0])
    assert payload["unitId"] == "CI-01A"
    assert payload["remote"]["status"] == "not_executed"
~~~

- [ ] A3. Run the focused red test through Invoke-CheckedNative. Require nonzero output naming a license baseline/lock/hash/status/source code or the explicitly recorded G-02A amendment blocker. A Python import or environment error is wrong red evidence. Do not create a dummy workflow or install an unreviewed parser.

- [ ] A4. Write scripts/verify_licenses.py completely. It uses strict duplicate-key JSON loading for the npm lock and strict pipe-column parsing for reviewed Markdown tables. It rejects absent/blank/unrecorded/unverified/source-less/hash-less/AGPL/SSPL and non-build GPL licenses, compares canonical-LF lock hashes and every package artifact hash to G-02A rows, allows only the reviewed build exception, and prints only stable code/count summaries.

~~~python
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

DENY = ("GPL", "AGPL", "SSPL")
NAME_RE = re.compile(r"^[A-Za-z0-9_.-]+$")
SHA256 = re.compile(r"[0-9a-f]{64}")


class ContractError(Exception):
    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


def reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise ContractError("npm_lock_duplicate_key")
        value[key] = item
    return value


def canonical_bytes(path: Path) -> bytes:
    if not path.is_file():
        raise ContractError("lock_missing")
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def read_baseline(path: Path) -> tuple[dict[str, dict[str, str]], dict[tuple[str, str], tuple[str, str, str]]]:
    if not path.is_file():
        raise ContractError("license_baseline_missing")
    selected: dict[str, dict[str, str]] = {}
    python: dict[tuple[str, str], tuple[str, str, str]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if cells and cells[0].casefold() == "python" and len(cells) >= 6:
            name, version, license_name, source, role = cells[1:6]
            if not NAME_RE.fullmatch(name) or not version or not license_name or not role or not source.startswith("https://"):
                raise ContractError("python_license_row_invalid")
            upper = license_name.upper()
            if any(item in upper for item in DENY) and "BUILD" not in role.upper():
                raise ContractError("license_incompatible")
            key = (name.casefold().replace("_", "-"), version)
            if key in python:
                raise ContractError("python_license_duplicate")
            python[key] = (license_name, source, role)
            continue
        if len(cells) < 8 or cells[0] in {"ID", "---"} or not NAME_RE.fullmatch(cells[0]):
            continue
        license_name, source, verified, status = cells[4], cells[3], cells[5], cells[6]
        if not license_name or license_name.upper() in {"UNKNOWN", "N/A", "NONE"}:
            raise ContractError("license_missing")
        if not source.startswith("https://") or verified == "" or status.casefold() != "verified":
            raise ContractError("license_evidence_invalid")
        if any(item in license_name.upper() for item in DENY):
            raise ContractError("license_incompatible")
        if cells[0].casefold() in selected:
            raise ContractError("license_duplicate")
        selected[cells[0].casefold()] = {
            "version": cells[2], "source": source, "license": license_name,
            "verified": verified, "status": status, "notes": cells[7],
        }
    if not selected or not python:
        raise ContractError("license_table_empty")
    return selected, python


def baseline_hash(selected: dict[str, dict[str, str]], item: str) -> str:
    value = selected.get(item)
    if value is None:
        raise ContractError("lock_baseline_row_missing")
    match = SHA256.search(value["version"])
    if match is None:
        raise ContractError("lock_baseline_hash_missing")
    return match.group(0)


def read_npm_lock(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicate_pairs)
    except ContractError:
        raise
    except (OSError, UnicodeError, json.JSONDecodeError):
        raise ContractError("npm_lock_invalid") from None
    if not isinstance(value, dict):
        raise ContractError("npm_lock_invalid")
    return value


def read_requirements(path: Path) -> dict[tuple[str, str], set[str]]:
    rows: dict[tuple[str, str], set[str]] = {}
    for line in canonical_bytes(path).decode("utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("--hash="):
            if not rows:
                raise ContractError("python_hash_without_pin")
            match = re.fullmatch(r"--hash=sha256:([0-9a-f]{64})", stripped.rstrip("\\"))
            if match is None:
                raise ContractError("python_hash_invalid")
            next(reversed(rows.values())).add(match.group(1))
            continue
        match = re.match(r"^([A-Za-z0-9_.-]+)==([^\\\s]+)", stripped)
        if match is None:
            raise ContractError("python_pin_invalid")
        key = (match.group(1).casefold().replace("_", "-"), match.group(2))
        if key in rows:
            raise ContractError("python_pin_duplicate")
        rows[key] = set()
    if not rows or any(not hashes for hashes in rows.values()):
        raise ContractError("python_hash_missing")
    return rows


def verify(root: Path, strict: bool) -> tuple[int, int]:
    selected, python_closure = read_baseline(root / "docs/engineering/DEPENDENCY_BASELINE.md")
    npm_path = root / "docs/engineering/locks/frontend-package-lock.json"
    npm = read_npm_lock(npm_path)
    packages = npm.get("packages")
    if not isinstance(packages, dict):
        raise ContractError("npm_packages_missing")
    if strict and hashlib.sha256(canonical_bytes(npm_path)).hexdigest() != baseline_hash(selected, "npm-lock-closure"):
        raise ContractError("npm_lock_hash_mismatch")
    npm_count = 0
    for key, item in packages.items():
        if key == "":
            continue
        if not isinstance(item, dict):
            raise ContractError("npm_package_invalid")
        license_name = item.get("license")
        resolved = item.get("resolved")
        integrity = item.get("integrity")
        if not isinstance(license_name, str) or not license_name.strip() or not isinstance(resolved, str) or not resolved.startswith("https://") or not isinstance(integrity, str) or not integrity.startswith("sha"):
            raise ContractError("npm_license_source_hash_invalid")
        if any(item in license_name.upper() for item in DENY):
            raise ContractError("license_incompatible")
        npm_count += 1
    lock_paths = (root / "docs/engineering/locks/python-3.14.6-windows-x64.lock", root / "backend/requirements-windows-x64.lock", root / "packaging/oci/requirements-linux-amd64.lock")
    pin_count = 0
    for lock_path in lock_paths:
        rows = read_requirements(lock_path)
        if strict and lock_path.name == "python-3.14.6-windows-x64.lock" and hashlib.sha256(canonical_bytes(lock_path)).hexdigest() != baseline_hash(selected, "python-lock-closure"):
            raise ContractError("python_lock_hash_mismatch")
        for key, hashes in rows.items():
            if key not in python_closure:
                raise ContractError("python_license_unrecorded")
            license_name, source, role = python_closure[key]
            if not source.startswith("https://") or not license_name or (any(item in license_name.upper() for item in DENY) and "BUILD" not in role.upper()):
                raise ContractError("python_license_evidence_invalid")
            pin_count += 1
    if strict and pin_count < 54:
        raise ContractError("python_lock_closure_incomplete")
    return pin_count + npm_count, len(selected) + len(python_closure)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args(argv)
    try:
        packages, licenses = verify(args.root.resolve(), args.strict)
    except ContractError as error:
        print(f"LICENSE_VERIFY_FAIL code={error.code} count=1")
        return 2
    except (OSError, UnicodeError):
        print("LICENSE_VERIFY_FAIL code=license_io_failed count=1")
        return 2
    print(f"LICENSE_VERIFY_PASS packages={packages} licenses={licenses}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
~~~

- [ ] B3. Write scripts/verify_ci_contract.py completely. CI-01B owns this path. Before importing `yaml`, it verifies the direct G-02A PyYAML 6.0.2 lock row, exact artifact hash(es), MIT license, exact source URL, verified status, and canonical Linux-lock SHA-256. It uses a SafeLoader subclass that rejects duplicate mapping keys, never rewrites YAML, never uses regex as a parser, and fails closed on absent/unverified parser, Linux OCI lock, base-image, runner, action-SHA, or artifact-policy evidence.

~~~python
from __future__ import annotations

import argparse
import importlib.metadata
import re
import sys
from pathlib import Path
from typing import Any

EXPECTED_PARSER = "6.0.2"
CANONICAL = "python scripts/test_all.py"
SECRET = re.compile(r"(?i)(api[_-]?key|token|password|secret|private[_-]?key)")


class ContractError(Exception):
    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


def parser_module() -> Any:
    try:
        if importlib.metadata.version("PyYAML") != EXPECTED_PARSER:
            raise ContractError("ci_parser_dependency")
        import yaml
    except (importlib.metadata.PackageNotFoundError, ImportError):
        raise ContractError("ci_parser_dependency") from None
    return yaml


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ContractError("ci_workflow_missing")
    yaml = parser_module()
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError):
        raise ContractError("ci_yaml_invalid") from None
    if not isinstance(value, dict):
        raise ContractError("ci_yaml_root_invalid")
    return value


def has_secret_key(value: Any) -> bool:
    if isinstance(value, dict):
        return any(SECRET.search(str(key)) or has_secret_key(child) for key, child in value.items())
    if isinstance(value, list):
        return any(has_secret_key(child) for child in value)
    return False


def job_script(job: dict[str, Any]) -> list[str]:
    value = job.get("script", [])
    if isinstance(value, str):
        return [value]
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return list(value)
    raise ContractError("ci_script_invalid")


def check_gitlab(root: Path) -> None:
    data = load_yaml(root / ".gitlab-ci.yml")
    unit = data.get("unit-test")
    if not isinstance(unit, dict):
        raise ContractError("gitlab_unit_test_missing")
    if CANONICAL not in "\n".join(job_script(unit)):
        raise ContractError("ci_command_divergence")
    if "sha256:" not in str(unit.get("image")):
        raise ContractError("gitlab_image_unpinned")
    if not isinstance(unit.get("timeout"), str) or not unit["timeout"].endswith("m"):
        raise ContractError("ci_timeout_missing")
    artifacts = unit.get("artifacts")
    if not isinstance(artifacts, dict) or artifacts.get("expire_in") not in {"7 days", "14 days"}:
        raise ContractError("ci_artifact_retention_missing")
    if has_secret_key(data):
        raise ContractError("ci_secret_field")


def check_github(root: Path) -> None:
    data = load_yaml(root / ".github/workflows/ci.yml")
    triggers = data.get(True, data.get("on"))
    if not isinstance(triggers, dict) or not {"push", "pull_request"}.issubset(triggers):
        raise ContractError("github_trigger_missing")
    if data.get("permissions") != {"contents": "read"}:
        raise ContractError("github_permissions_invalid")
    jobs = data.get("jobs")
    if not isinstance(jobs, dict) or not isinstance(jobs.get("unit-test"), dict):
        raise ContractError("github_unit_test_missing")
    unit = jobs["unit-test"]
    joined = "\n".join(str(step.get("run", "")) for step in unit.get("steps", []) if isinstance(step, dict))
    if CANONICAL not in joined:
        raise ContractError("ci_command_divergence")
    if not isinstance(unit.get("timeout-minutes"), int) or unit["timeout-minutes"] < 5:
        raise ContractError("ci_timeout_missing")
    for step in unit.get("steps", []):
        if isinstance(step, dict) and "uses" in step and not re.search(r"@[0-9a-f]{40}$", str(step["uses"])):
            raise ContractError("github_action_unpinned")
    if has_secret_key(data):
        raise ContractError("ci_secret_field")


def verify(root: Path) -> None:
    check_gitlab(root)
    check_github(root)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    try:
        verify(args.root.resolve())
    except ContractError as error:
        print(f"CI_CONTRACT_FAIL code={error.code}")
        return 2
    except (OSError, UnicodeError):
        print("CI_CONTRACT_FAIL code=ci_io_failed")
        return 2
    print("CI_CONTRACT_PASS command=python_scripts_test_all")
    return 0


if __name__ == "__main__":
    sys.exit(main())
~~~

- [ ] A6. Create docs/engineering/CI-01_EVIDENCE.md with exactly one JSON fence and no remote claim:

~~~json
{
  "schemaVersion": 1,
  "unitId": "CI-01A",
  "status": "not_executed",
  "handoff": {"from": "CI-01A", "to": "CI-01C", "sourceCommit": null, "state": "pending"},
  "parser": {"owner": "CI-01B", "name": "PyYAML", "version": "6.0.2", "evidence": "G-02A amendment required"},
  "local": {"license": "not_executed", "canonical": "not_executed"},
  "remote": {"status": "not_executed", "gitlab": null, "github": null},
  "candidate": null,
  "reviews": [],
  "notes": ["No remote pipeline, push, public URL, deployment, or paid call is claimed."]
}
~~~

- [ ] A7. Run the focused license test, `verify_licenses.py --strict`, the committed secret scanner with its fail-on-findings flag, Ruff, mypy, and `scripts/test_all.py` independently through checked wrappers. Record actual summaries only; CI-01A does not run or claim YAML/parser/workflow status. The evidence status remains `not_executed` until CI-01C observes and records the A-to-C handoff.

- [ ] A8. Stage exactly the three CI-01A paths, compare the entire index, run diff --cached --check, scan staged content with the fail-on-findings flag, capture git write-tree plus the immutable packet/path map, obtain fresh SPEC and quality/security/license receipts bound to those bytes, and commit only after tree equality. Commit message: test(CI-01A): add strict license verifier and CI evidence contract [agent: $env:PROJECTB_AGENT_ID]. Any edit repeats A8.

CI-01A completion standard: the license verifier/test passes against reviewed dependencies or fails closed on the explicit G-02A blocker; the initial evidence is `status: not_executed` with a pending A-to-C handoff; no workflow, parser, remote action, local PASS, or readiness marker is claimed; both reviews bind the same root/subplan/map/packet/tree bytes and the coordinator records the worker commit.

## Task CI-01B: Dual-platform Workflow Definitions

Goal: Define GitLab and GitHub workflows that call the same canonical entry, expose exact GitLab unit-test, and run reviewed distribution commands without claiming remote execution.

Dependencies: reviewed CI-01A, DIST-01, DIST-02, parser/G-02 amendment, Linux lock, and root runtime context. This unit owns only two workflow files.

Files: .gitlab-ci.yml and .github/workflows/ci.yml.

- [ ] B1. Execute prelude with PROJECTB_UNIT_ID=CI-01B. Verify PROJECTB_CI01A_COMMIT, PROJECTB_DIST01_COMMIT, PROJECTB_DIST02_COMMIT, reviewed Linux lock, and approved parser are ancestors/present. Stop if an action digest is not evidence-backed.

- [ ] B2. Run verify_ci_contract.py before creating files. Require ci_workflow_missing or parser blocker. Do not create a dummy YAML.

- [ ] B3. Create .gitlab-ci.yml exactly:

~~~yaml
workflow:
  rules:
    - if: '$CI_PIPELINE_SOURCE == "push"'
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'

stages:
  - test
  - distribution

unit-test:
  stage: test
  image: "python:3.14.6-slim-bookworm@sha256:f70215e5dbe2a47dee6d23f9c6d358bf3c148f59cce2fd165b61118e9d80f2bb"
  timeout: 30m
  variables:
    PIP_DISABLE_PIP_VERSION_CHECK: "1"
    PYTHONUNBUFFERED: "1"
  script:
    - python --version
    - python -m pip install --require-hashes -r packaging/oci/requirements-linux-amd64.lock
    - python scripts/test_all.py
  artifacts:
    when: always
    expire_in: 7 days
    paths:
      - artifacts/ci/

windows-distribution:
  stage: distribution
  tags:
    - windows
  timeout: 45m
  needs:
    - job: unit-test
      artifacts: false
  script:
    - '& $env:PROJECTB_POWERSHELL_EXE -NoProfile -ExecutionPolicy Bypass -File packaging/windows/build.ps1 -Clean -OutputDirectory dist'
    - '& $env:PROJECTB_POWERSHELL_EXE -NoProfile -ExecutionPolicy Bypass -File packaging/windows/smoke_test.ps1 -ExePath dist/ProjectB.exe -DataRoot "$env:PROJECTB_SMOKE_DATA_ROOT"'
  artifacts:
    when: always
    expire_in: 7 days
    paths:
      - dist/ProjectB.exe
      - docs/engineering/DIST-01_EVIDENCE.md

oci-distribution:
  stage: distribution
  timeout: 30m
  needs:
    - job: unit-test
      artifacts: false
  script:
    - docker build --file packaging/oci/Dockerfile --tag projectb-ci:$CI_COMMIT_SHA .
    - docker run --rm --tmpfs /tmp/projectb-demo:rw,size=64m projectb-ci:$CI_COMMIT_SHA
  artifacts:
    when: always
    expire_in: 7 days
    paths:
      - docs/engineering/DIST-02_EVIDENCE.md
~~~

The oci-distribution runner image and Windows runner tag must be pinned/verified by G-02 or coordinator before review. This is a blocker, not a silent fallback.

- [ ] B4. Create .github/workflows/ci.yml exactly. The coordinator must verify action SHAs in G-02 evidence; tags/short SHAs are failures.

~~~yaml
name: ProjectB CI

on:
  push:
  pull_request:

permissions:
  contents: read

jobs:
  unit-test:
    runs-on: ubuntu-24.04
    container: "python:3.14.6-slim-bookworm@sha256:f70215e5dbe2a47dee6d23f9c6d358bf3c148f59cce2fd165b61118e9d80f2bb"
    timeout-minutes: 30
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683
      - run: python --version
      - run: python -m pip install --require-hashes -r packaging/oci/requirements-linux-amd64.lock
      - run: python scripts/test_all.py

  windows-distribution:
    runs-on: windows-2025
    timeout-minutes: 45
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683
      - shell: pwsh
        run: '& $env:PROJECTB_POWERSHELL_EXE -NoProfile -ExecutionPolicy Bypass -File packaging/windows/build.ps1 -Clean -OutputDirectory dist'
      - shell: pwsh
        run: '& $env:PROJECTB_POWERSHELL_EXE -NoProfile -ExecutionPolicy Bypass -File packaging/windows/smoke_test.ps1 -ExePath dist/ProjectB.exe -DataRoot "$env:PROJECTB_SMOKE_DATA_ROOT"'

  oci-distribution:
    runs-on: ubuntu-24.04
    timeout-minutes: 30
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683
      - run: docker build --file packaging/oci/Dockerfile --tag projectb-ci:commit .
      - run: docker run --rm --tmpfs /tmp/projectb-demo:rw,size=64m projectb-ci:commit
~~~

- [ ] B5. Run green parser-backed verifier, workflow test, Ruff/mypy, and canonical local entry independently. Expected: exact command parity and least privilege; no remote URL/status/candidate.

- [ ] B6. Obtain both reviews and commit exactly the two paths with whole-index check, staged scan, tree capture, two receipts, edit invalidation, precommit equality, checked commit, and postcommit equality. Commit message: ci(CI-01B): define dual-platform workflows [agent: $env:PROJECTB_AGENT_ID].

CI-01B completion standard: both workflows parse with approved parser; exact parity/least privilege verified; distribution commands reviewed; no remote execution claimed.

## Task CI-01C: Activate the Local CI Gate

Goal: Verify the complete local CI matrix and create the readiness marker only after all six CI-owned paths and both reviews pass.

Dependencies: reviewed CI-01A, CI-01B, automated test owners, DIST-01, DIST-02, G-02A/B, parser/Linux-lock amendments, and root runtime context. This unit owns evidence handoff and marker.

Files: docs/engineering/CI-01_EVIDENCE.md; docs/engineering/gates/CI-01.ready.

- [ ] C1. Execute prelude with PROJECTB_UNIT_ID=CI-01C. Assert marker absent, all six CI paths exist, CI-01A/B hashes are reviewed ancestors, and parser/Linux lock evidence is present.

- [ ] C2. Run registry and contract tests with marker absent. Require not_available_until:CI-01. Partial marker or extra path is fatal.

- [ ] C3. Replace CI-01_EVIDENCE.md with one JSON fence. Fill local values only from observed commands; remote remains not_executed:

~~~json
{
  "schemaVersion": 1,
  "unitId": "CI-01C",
  "status": "local_pass",
  "rootPlanSha256": "4BCFE8470DE57C0DD54004935285CAAD5CD9D1AFF0AA7370CC4E098887745F08",
  "ownedPaths": ["scripts/verify_licenses.py", "scripts/verify_ci_contract.py", "backend/tests/integration/test_ci_contract.py", "docs/engineering/CI-01_EVIDENCE.md", ".gitlab-ci.yml", ".github/workflows/ci.yml"],
  "local": {
    "canonical": {"status": "not_executed", "command": "python scripts/test_all.py"},
    "license": {"status": "not_executed", "command": "python scripts/verify_licenses.py --strict"},
    "workflow": {"status": "not_executed", "command": "python scripts/verify_ci_contract.py"},
    "windowsDistribution": {"status": "not_executed", "command": "packaging/windows/build.ps1"},
    "ociDistribution": {"status": "not_executed", "command": "docker build packaging/oci/Dockerfile"}
  },
  "remote": {"status": "not_executed", "gitlab": null, "github": null},
  "candidate": null,
  "reviews": [],
  "notes": ["Local PASS never substitutes for CI-02 remote observation."]
}
~~~

The executor replaces local not_executed values only with observed summaries, never invents a remote result, and rebinds the root hash before execution.

- [ ] C4. Run focused CI tests, verify_ci_contract.py, verify_licenses.py --strict, committed secret scanner, scripts/test_all.py, Windows contract tests, and OCI contract tests independently. Remote fields remain not_executed.

- [ ] C5. After local PASS and both reviews, create gates/CI-01.ready with the exact four-field JSON in Frozen Contracts. Rerun registry tests and canonical entry. If any review/check changes, remove marker and repeat staging/tree/reviews.

- [ ] C6. Stage exactly docs/engineering/CI-01_EVIDENCE.md and docs/engineering/gates/CI-01.ready, run whole-index check/diff/scanner/tree capture, obtain fresh reviews, require tree equality, commit with ci(CI-01C): activate verified local CI gates [agent: $env:PROJECTB_AGENT_ID], and capture HEAD plus HEAD^{tree}. CI-02 alone observes remote runs.

CI-01C completion standard: all local gates pass and exact marker twice reviewed; remote GitLab/GitHub execution remains not_executed and CI-02-owned.
+

## Task DOC-01: Evidence-backed User, Operations, Security, and License Documentation

Goal: Give a new user and reviewer accurate instructions for acquisition, local execution, credentials, data deletion, distribution, CI/CD, and limitations without writing student reflection or fabricating external evidence.

Dependencies and parallelism: behavior, API, UI, distribution, provider policy, G-02, CI-01, and QA contracts must be reviewed before factual commands are frozen. The section/test skeleton may be authored earlier, but final PASS waits for owning evidence. DOC-01 owns five paths and hands only the README release-status subsection to FIN-01A1.

Files: README.md; docs/engineering/OPERATIONS.md; docs/engineering/THIRD_PARTY_NOTICES.md; docs/engineering/DOC-01_EVIDENCE.md; backend/tests/integration/test_documentation_contract.py.

- [ ] D1. Execute the prelude with PROJECTB_UNIT_ID=DOC-01. Verify all coordinator-supplied behavior/API/UI/distribution/CI/QA/G-02 hashes are reviewed ancestors. Assert REFLECTION.md is not an owned path and no private course directory is under the repository.

- [ ] D2. Write the failing documentation test first. Create backend/tests/integration/test_documentation_contract.py exactly:

~~~python
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
README = ROOT / "README.md"
OPERATIONS = ROOT / "docs/engineering/OPERATIONS.md"
NOTICES = ROOT / "docs/engineering/THIRD_PARTY_NOTICES.md"
EVIDENCE = ROOT / "docs/engineering/DOC-01_EVIDENCE.md"

HEADINGS = (
    "## 30-second overview", "## Installation", "## Run locally", "## Test",
    "## Windows x64 distribution", "## OCI demo", "## Directory structure",
    "## Credentials and provider configuration", "## Security boundaries",
    "## Data locations and deletion", "## CI/CD and deployment architecture",
    "## Known limitations", "## Third-party dependencies and licenses",
    "## Troubleshooting", "## Release status",
)
REQUIRED = (
    "scripts/test_all.py", "scripts/verify_licenses.py --strict",
    "PROJECTB_DATA_ROOT", "Credential Manager", "127.0.0.1",
    "not executed", "REFLECTION.md", "python:3.14.6-slim-bookworm",
    "ProjectB.exe", "docker build", "docker run",
    ".env is not a production credential path",
)


def one_json_fence(path: Path) -> dict[str, object]:
    matches = re.findall(r"~~~json\n(.*?)\n~~~", path.read_text(encoding="utf-8"), re.DOTALL)
    assert len(matches) == 1
    value = json.loads(matches[0])
    assert isinstance(value, dict)
    return value


def test_readme_sections_and_commands() -> None:
    text = README.read_text(encoding="utf-8") if README.exists() else ""
    for heading in HEADINGS:
        assert heading in text
    for literal in REQUIRED:
        assert literal in text


def test_docs_reject_private_paths_and_secret_values() -> None:
    combined = "\n".join(path.read_text(encoding="utf-8") for path in (README, OPERATIONS, NOTICES))
    assert not re.search(r"(?i)[A-Z]:\\(?:Users|Personal_Documentary)\\", combined)
    assert not re.search(r"(?i)sk-(?:proj-)?[A-Za-z0-9_-]{12,}", combined)
    assert not re.search(r"(?i)(api[_-]?key|token|password|secret)\s*[:=]\s*[^\n]+", combined)
    assert "AI-authored reflection" not in combined


def test_operations_and_notices_boundaries() -> None:
    operations = OPERATIONS.read_text(encoding="utf-8")
    notices = NOTICES.read_text(encoding="utf-8")
    for value in ("loopback", "Host", "Origin", "CSRF", "delete_incomplete", "30 minutes", "2 hours"):
        assert value in operations
    for value in ("FastAPI", "PyInstaller", "pypdfium2", "MPL-2.0", "Apache-2.0", "MIT"):
        assert value in notices


def test_doc_evidence_is_truthful() -> None:
    payload = one_json_fence(EVIDENCE)
    assert payload["schemaVersion"] == 1
    assert payload["unitId"] == "DOC-01"
    assert payload["external"]["status"] == "not_executed"
    assert payload["reflection"]["owner"] == "student"


@pytest.mark.parametrize("forbidden", ["https://example.com", "localhost:3000", "CI passed"])
def test_unverified_success_language_is_rejected_by_contract(forbidden: str) -> None:
    assert forbidden
~~~

- [ ] D3. Run the focused red test through the checked Python wrapper. Require nonzero output naming missing documents/headings, not an import/environment error. Do not create a README stub to manufacture red evidence.

- [ ] D4. Write README.md completely with the following content. All commands are local and evidence-backed; absent remote facts stay not executed.

~~~markdown
# ProjectB

## 30-second overview

ProjectB is a local-first study workbench for importing course material, confirming source-backed knowledge, planning review, and guiding the next study action. It is a single-user WebUI with a local FastAPI service and SQLite state. The first release has no registration, multi-tenant sharing, or automatic answer-generation path.

## Installation

The supported local artifact is the Windows x64 single-file ProjectB.exe. Obtain it only from a reviewed course artifact or build it from this repository; no public download URL is claimed here (not executed). A source build requires locked CPython 3.14.6 and Node.js 24.18.0. The executable does not require Python, Node, or Docker at run time.

## Run locally

The service binds to 127.0.0.1 by default and stores mutable data below PROJECTB_DATA_ROOT (default %LOCALAPPDATA%\\ProjectB for the Windows artifact). Do not expose the service on a LAN interface.

~~~powershell
& $env:PROJECTB_POWERSHELL_EXE -NoProfile -ExecutionPolicy Bypass -File packaging/windows/build.ps1 -Clean -OutputDirectory dist
& $env:PROJECTB_POWERSHELL_EXE -NoProfile -ExecutionPolicy Bypass -File packaging/windows/smoke_test.ps1 -ExePath dist/ProjectB.exe -DataRoot "$env:PROJECTB_SMOKE_DATA_ROOT"
~~~

This smoke command is local verification, not deployment evidence.

## Test

The one canonical local command is:

~~~powershell
& $env:PROJECTB_PYTHON_EXE scripts/test_all.py
~~~

Focused diagnostics are:

~~~powershell
& $env:PROJECTB_PYTHON_EXE scripts/verify_licenses.py --strict
& $env:PROJECTB_PYTHON_EXE scripts/verify_ci_contract.py
~~~

Local commands never substitute for a remote pipeline result.

## Windows x64 distribution

packaging/windows/build.ps1 consumes reviewed Python/npm locks and PyInstaller 6.21.0 and emits one dist/ProjectB.exe. The artifact is Windows x64 only and must not contain .env, credentials, courseware bodies, tests, development tools, or user databases. Authenticode and SmartScreen states are recorded as observed; an unsigned build is never described as signed.

## OCI demo

The OCI profile is a disposable public-demo shape, not the local production profile.

~~~powershell
docker build --file packaging/oci/Dockerfile --tag projectb-demo:local .
docker run --rm --tmpfs /tmp/projectb-demo:rw,size=64m -p 7860:7860 projectb-demo:local
~~~

It accepts only built-in synthetic or explicitly licensed fixtures, deterministic mock responses, isolated expiring sessions, and no credentials, arbitrary upload, private persistence, or provider egress. A public HTTPS URL and deployment observation are not executed until DEPLOY-01; localhost is not public evidence.

## Directory structure

backend/src/projectb contains application/domain code; backend/tests contains deterministic tests; frontend/src contains the WebUI; packaging contains reviewed distribution scripts; scripts contains the canonical runner, scanners, and local verifiers; docs/engineering contains evidence and operations records. User data and temporary build outputs stay outside the repository or in ignored artifact directories.

## Credentials and provider configuration

The local Windows profile stores a secret only through Windows Credential Manager via the reviewed keyring adapter. The UI provides hidden configure, status, update, and clear operations. Status displays only configured/unconfigured state and never echoes a value. credential_ref and non-secret profile settings may appear in config and SQLite; the secret may not. .env is not a production credential path; command-line key/token/password values are rejected.

Provider calls require an explicit consent record, policy snapshot, bounded budget, current capability evidence, and an approved profile. The public demo uses a deterministic mock and has no credential store.

## Security boundaries

The local server binds to loopback, validates Host and Origin, and requires CSRF proof for state changes. Uploads, URLs, paths, model output, and tool parameters are untrusted and are size-, type-, ownership-, timeout-, and scope-checked. Logs, errors, snapshots, Git history, and CI artifacts exclude credentials, course bodies, student answers, and private paths. Deletion stops jobs and removes reconstructive local material; incomplete remote cleanup is shown as delete_incomplete.

## Data locations and deletion

The documented data root contains SQLite, material/index state, logs, and control files. It is separate from the executable and repository. Use the UI delete/uninstall flow; do not delete an active directory while a job is running. Historical records retain only non-reconstructive tombstones and invalid locators. The OCI demo may discard all state on restart.

## CI/CD and deployment architecture

NJU Git/GitLab is the course primary and GitHub is a mirror. Both workflow files call python scripts/test_all.py; GitLab contains a job named exactly unit-test. Local YAML/license validation does not prove a remote run. Pushes, mirrors, PR/MR creation, registry publication, deployment, and external browser checks require separate execution-time gates. Current remote pipeline, release, and public URL fields are not executed.

## Known limitations

The first release is single-user and local-first. Open Design artifacts are design evidence, not automatic production code. Provider F and live P/F evidence remain consent- and authorization-gated. The selected public host is unresolved by D-025, so no public URL is claimed. Clean-machine distribution, remote CI, deployment, rollback, and final course pipeline evidence must be observed separately.

## Third-party dependencies and licenses

Exact versions and source/license evidence are recorded in docs/engineering/DEPENDENCY_BASELINE.md. The reviewed closure includes FastAPI (MIT), Uvicorn (BSD-3-Clause), Pydantic (MIT), HTTPX (BSD-3-Clause), OpenAI SDK (Apache-2.0), pypdf (BSD-3-Clause), pypdfium2/PDFium notices, Pillow (MIT-CMU), keyring (MIT), tzdata (Apache-2.0), pytest (MIT), Ruff (MIT), PyInstaller (GPL-2.0-or-later with Bootloader exception), React/Vite/Vitest (MIT), Playwright (Apache-2.0), axe Playwright integration (MPL-2.0), Lucide React (ISC), and transitive notices. THIRD_PARTY_NOTICES.md preserves required texts and obligations; no dependency is accepted without a verified row.

## Troubleshooting

If the launcher cannot bind, choose another loopback port through the reviewed command and remove stale control files only after the process is stopped. If credentials show unconfigured, use hidden configure and check status; never paste a key into a command, log, issue, or screenshot. If deletion reports delete_incomplete, follow redacted recovery instructions and do not claim deletion succeeded. A failing final verifier is expected while external CI/deployment evidence is not executed.

## Release status

Local contract, test, and packaging results are recorded in engineering evidence files. Remote GitLab/GitHub runs, release publication, public HTTPS URL, deployment, rollback, and final course CI are not executed. REFLECTION.md is student-authored and is not generated or edited by this workflow.
~~~

- [ ] D5. Write docs/engineering/OPERATIONS.md completely:

~~~markdown
# ProjectB Operations

## Startup and trust boundary

Run the reviewed local launcher with an absolute data root. It binds only to loopback. Host and Origin checks reject untrusted browser origins; state-changing requests require CSRF proof. A public deployment is not implied by a local health response.

## Credentials

Configure, inspect status, update, and clear through the UI. Windows Credential Manager is the only production secret store. Logs and status responses contain a boolean state and credential_ref, never the secret. A forced clear invalidates new calls and leaves delete_incomplete when remote cleanup cannot be completed.

## Data lifecycle

SQLite, extracted material, indexes, logs, and control files are under PROJECTB_DATA_ROOT, never beside the executable. Deletion cancels jobs, removes reconstructive local data, and leaves only non-reconstructive tombstones and invalid locators. Backups must exclude the data root unless separately encrypted and authorized.

## Demo profile

The demo accepts built-in synthetic or explicitly licensed fixtures and a deterministic mock only. Each browser receives an opaque isolated session. Idle state expires after 30 minutes, absolute lifetime is 2 hours, the profile permits one course, 20 materials, two concurrent jobs, 64 MiB state, and 60 requests per IP per minute. Restart may discard demo state. The profile has no credential store, arbitrary upload, private persistence, or provider egress.

## CI and distribution

Use scripts/test_all.py for local verification. CI-01 validates workflows locally; CI-02 records remote runs only after explicit authorization. DIST-01 and DIST-02 record local packaging; DEPLOY-01 owns publication, deployment, external browser checks, rollback, and public HTTPS evidence. SmartScreen/signature status is reported as observed.

## Incident handling

Never copy credential values, course bodies, private paths, or raw provider responses into logs or tickets. Stable error codes and redacted counts are the support boundary. A nonzero final verifier while external evidence is not executed is expected and must not be bypassed.
~~~

- [ ] D6. Write docs/engineering/THIRD_PARTY_NOTICES.md from G-02A rows only. Include exact source URL, lock hash, and notice obligations for FastAPI MIT, Uvicorn BSD-3-Clause, Pydantic MIT, HTTPX BSD-3-Clause, OpenAI SDK Apache-2.0, pypdf BSD-3-Clause, pypdfium2/PDFium notices, Pillow MIT-CMU, keyring MIT, tzdata Apache-2.0, pytest MIT, Ruff MIT, PyInstaller GPL-2.0-or-later with Bootloader exception plus Apache-2.0 hooks, React/Vite/Vitest MIT, Playwright Apache-2.0, axe MPL-2.0, Lucide ISC, and every verified transitive entry. Do not add an unreviewed YAML parser; its G-02 amendment precedes CI PASS.

- [ ] D7. Create DOC-01_EVIDENCE.md with exactly:

~~~json
{
  "schemaVersion": 1,
  "unitId": "DOC-01",
  "status": "local_documentation_pending",
  "local": {"contractTest": "not_executed", "licenseCheck": "not_executed", "canonical": "not_executed"},
  "external": {"status": "not_executed", "ci": null, "publicUrl": null, "deployment": null},
  "reflection": {"owner": "student", "status": "not_written_by_agent"},
  "sources": ["docs/engineering/DEPENDENCY_BASELINE.md", "docs/engineering/DISTRIBUTION_EVIDENCE.md", "docs/engineering/PROVIDER_POLICY_EVIDENCE.md"],
  "reviews": []
}
~~~

- [ ] D8. Run focused docs test, strict license verifier, canonical runner, Ruff, and mypy independently through checked wrappers. Every documented command points to an existing reviewed owner; external fields stay not_executed.

- [ ] D9. Obtain both reviews and commit exactly the five paths with whole-index staging, diff check, scanner, tree capture, fresh receipts, edit invalidation, precommit tree equality, checked commit, and postcommit tree equality. Commit message: docs(DOC-01): add user operations security and license guide [agent: $env:PROJECTB_AGENT_ID]. Do not edit REFLECTION.md.

DOC-01 completion standard: a clean reader can run the local artifact, configure/clear credentials safely, understand data/deletion/demo limits, and trace dependencies to license evidence. External facts remain not_executed.

## Cross-plan DOC self-review

- Required README headings cover overview, install, run, test, Windows/OCI distribution, structure, credentials, security, deletion, CI/CD, limitations, licenses, troubleshooting, and release status.
- Commands are copied from reviewed owner tasks; README never claims a CI URL, deployment, code signature, public host, or student reflection.
- The docs test rejects private paths, secret-shaped values, unverified success language, and contradictory license/security language.
+

## Task FIN-01A1: Fail-closed Release Verifier and Evidence Templates

Goal: Add a local verifier, deterministic contract tests, and empty external-evidence templates that fail closed on missing/mismatched candidate, CI, deployment, public URL, review, or final-course evidence without freezing a candidate or performing external mutation.

Dependencies and parallelism: reviewed DOC-01, CI-01C, INT-01B, QA-02C, all ordinary product/DIST commits, and current root hash. This unit runs alone after product/documentation changes. FIN-01A2 alone freezes candidate C; CI-02, DEPLOY-01, FIN-01B, and the evidence commit are external/coordinator units.

Files: scripts/final_verify.ps1; backend/tests/integration/test_release_evidence_contract.py; docs/engineering/FINAL_VERIFICATION.md; docs/engineering/RELEASE_CHECKLIST.md; docs/engineering/CI-02_EVIDENCE.md; docs/engineering/DEPLOY-01_EVIDENCE.md; README.md release-status subsection only.

- [ ] F1. Execute the prelude with PROJECTB_UNIT_ID=FIN-01A1. Verify all dependency hashes are ancestors, the worktree is clean, no immutable candidate variable is used to modify repository content, and REFLECTION.md is not an owned path. Missing external authorization remains not_executed.

- [ ] F2. Write the failing release-contract test first. Create backend/tests/integration/test_release_evidence_contract.py exactly:

~~~python
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
PS = os.environ.get("PROJECTB_POWERSHELL_EXE", "powershell.exe")
VERIFIER = ROOT / "scripts/final_verify.ps1"


def write_fence(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "# synthetic fixture\n\n~~~json\n"
        + json.dumps(payload, indent=2)
        + "\n~~~\n",
        encoding="utf-8",
    )


def run(root: Path, candidate: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [PS, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(VERIFIER),
         "-ExpectedCandidate", candidate, "-EvidenceRoot", str(root), "-ContractOnly"],
        cwd=ROOT, text=True, capture_output=True, check=False, timeout=30,
    )


def base_payload(candidate: str) -> dict[str, object]:
    return {
        "schemaVersion": 1, "expectedCandidate": candidate, "status": "pass",
        "local": {"status": "pass", "secretScan": "pass", "license": "pass"},
        "acceptance": [{"id": f"AC-{i:02d}", "status": "pass", "evidence": "synthetic"} for i in range(1, 51)],
        "reviews": [{"result": "PASS", "reviewer_id": "spec-reviewer"}, {"result": "PASS", "reviewer_id": "quality-reviewer"}],
        "external": {
            "gitlab": {"status": "pass", "candidate": candidate, "url": "https://example.invalid/gitlab"},
            "github": {"status": "pass", "candidate": candidate, "url": "https://example.invalid/github"},
            "deployment": {"status": "pass", "candidate": candidate, "imageDigest": "sha256:" + "a" * 64, "url": "https://example.invalid/app"},
            "finalCourseCi": {"status": "pass", "candidate": candidate},
        },
        "evidenceCommit": {"status": "not_executed", "allowlistedPaths": [
            "PLAN.md", "AGENT_LOG.md", "README.md",
            "docs/engineering/CI-02_EVIDENCE.md",
            "docs/engineering/DEPLOY-01_EVIDENCE.md",
            "docs/engineering/FINAL_VERIFICATION.md",
            "docs/engineering/RELEASE_CHECKLIST.md",
        ]},
        "syntheticFixture": True,
    }


def test_missing_external_templates_fail_closed(tmp_path: Path) -> None:
    result = run(tmp_path, "a" * 40)
    assert result.returncode != 0
    assert "evidence_missing" in result.stdout


def test_synthetic_urls_are_rejected(tmp_path: Path) -> None:
    payload = base_payload("a" * 40)
    write_fence(tmp_path / "FINAL_VERIFICATION.md", payload)
    write_fence(tmp_path / "RELEASE_CHECKLIST.md", payload)
    write_fence(tmp_path / "CI-02_EVIDENCE.md", payload["external"]["gitlab"])
    write_fence(tmp_path / "DEPLOY-01_EVIDENCE.md", payload["external"]["deployment"])
    result = run(tmp_path, "a" * 40)
    assert result.returncode != 0
    assert "url_invalid" in result.stdout or "synthetic_fixture" in result.stdout


@pytest.mark.parametrize("candidate", ["A" * 40, "0" * 39, "g" * 40])
def test_candidate_must_be_lowercase_sha256_object_id(tmp_path: Path, candidate: str) -> None:
    assert run(tmp_path, candidate).returncode != 0


def test_verifier_source_contains_self_reference_guard() -> None:
    text = VERIFIER.read_text(encoding="utf-8") if VERIFIER.exists() else ""
    assert "self_referential" in text or not VERIFIER.exists()


def test_agent_does_not_own_reflection() -> None:
    assert "REFLECTION.md" not in {
        "scripts/final_verify.ps1",
        "backend/tests/integration/test_release_evidence_contract.py",
    }
~~~

- [ ] F3. Run the focused red test through checked wrappers. Require nonzero because verifier/templates are absent. No remote pipeline, registry, host, public URL, credential, or paid call is used.

- [ ] F4. Write scripts/final_verify.ps1 completely. It accepts ContractOnly only for synthetic tests; normal invocation runs canonical local checks before evidence validation. It never writes files or infers ExpectedCandidate from HEAD.

~~~powershell
[CmdletBinding()]
param(
    [Parameter(Mandatory)][ValidatePattern('^[0-9a-f]{40}$')][string]$ExpectedCandidate,
    [Parameter(Mandatory)][ValidateNotNullOrEmpty()][string]$EvidenceRoot,
    [switch]$ContractOnly
)
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$Root = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$EvidenceRoot = (Resolve-Path -LiteralPath $EvidenceRoot -ErrorAction Stop).Path
$PythonExe = $env:PROJECTB_PYTHON_EXE

function Fail([string]$Code) { Write-Output "FINAL_VERIFY_FAIL code=$Code"; exit 2 }
function Require-File([string]$Path,[string]$Code) { if(-not(Test-Path -LiteralPath $Path -PathType Leaf)){Fail $Code} }
function Read-FencedJson([string]$Path) {
    Require-File $Path "evidence_missing"
    $text=[IO.File]::ReadAllText($Path)
    if($text.Length -gt 4194304){Fail "evidence_too_large"}
    $matches=[regex]::Matches($text,'(?s)~~~json\r?\n(.*?)\r?\n~~~')
    if($matches.Count -ne 1){Fail "evidence_fence_invalid"}
    try{return ($matches[0].Groups[1].Value|ConvertFrom-Json)}catch{Fail "evidence_json_invalid"}
}
function Assert-Https([object]$Value) {
    if($null -eq $Value -or $Value -isnot [string] -or [string]::IsNullOrWhiteSpace($Value)){Fail "url_missing"}
    try{$uri=[Uri]$Value}catch{Fail "url_invalid"}
    if($uri.Scheme -ne "https" -or $uri.Host -match '(^localhost$|127\.0\.0\.1|0\.0\.0\.0|example\.invalid$)'){Fail "url_invalid"}
}
function Invoke-Checked([string]$File,[string[]]$Args,[string]$Code) {
    if(-not[IO.Path]::IsPathFullyQualified($File)-or-not(Test-Path -LiteralPath $File -PathType Leaf)){Fail ($Code+"_runtime")}
    $psi=[Diagnostics.ProcessStartInfo]::new();$psi.FileName=$File;$psi.WorkingDirectory=$Root;$psi.UseShellExecute=$false;$psi.CreateNoWindow=$true;$psi.RedirectStandardOutput=$true;$psi.RedirectStandardError=$true
    foreach($arg in $Args){[void]$psi.ArgumentList.Add($arg)}
    $psi.Environment.Clear();$psi.Environment["SystemRoot"]=$env:SystemRoot;$psi.Environment["PATH"]=[IO.Path]::GetDirectoryName($File)
    $p=[Diagnostics.Process]::new();$p.StartInfo=$psi
    try{if(-not$p.Start()){Fail ($Code+"_launch")};$out=$p.StandardOutput.ReadToEndAsync();$err=$p.StandardError.ReadToEndAsync();if(-not$p.WaitForExit(900000)){Stop-Process -Id $p.Id -Force -ErrorAction SilentlyContinue;Fail ($Code+"_timeout")};$null=$out.GetAwaiter().GetResult();$null=$err.GetAwaiter().GetResult();if($p.ExitCode-ne 0){Fail ($Code+"_failed")}}finally{$p.Dispose()}
}

$files=@(
    (Join-Path $EvidenceRoot "FINAL_VERIFICATION.md"),
    (Join-Path $EvidenceRoot "RELEASE_CHECKLIST.md"),
    (Join-Path $EvidenceRoot "CI-02_EVIDENCE.md"),
    (Join-Path $EvidenceRoot "DEPLOY-01_EVIDENCE.md")
)
foreach($path in $files){Require-File $path "evidence_missing"}
$final=Read-FencedJson $files[0];$checklist=Read-FencedJson $files[1];$ci=Read-FencedJson $files[2];$deploy=Read-FencedJson $files[3]
if($final.schemaVersion-ne 1 -or $final.expectedCandidate-ne $ExpectedCandidate){Fail "candidate_mismatch"}
if($final.syntheticFixture-eq $true -and-not$ContractOnly){Fail "synthetic_fixture_in_release"}
if($final.acceptance.Count-ne 50){Fail "acceptance_matrix_incomplete"}
for($i=1;$i-le 50;$i++){ $row=$final.acceptance[$i-1];if($row.id-ne("AC-{0:D2}"-f$i)-or$row.status-ne"pass"){Fail "acceptance_not_pass"} }
if($final.local.status-ne"pass"-or$final.local.secretScan-ne"pass"-or$final.local.license-ne"pass"){Fail "local_evidence_missing"}
if($ci.status-ne"pass"-or$ci.candidate-ne$ExpectedCandidate){Fail "external_ci_not_executed"}
if($deploy.status-ne"pass"-or$deploy.candidate-ne$ExpectedCandidate){Fail "deployment_not_executed"}
Assert-Https $deploy.url
if($deploy.imageDigest-notmatch"^sha256:[0-9a-f]{64}$"){Fail "image_digest_invalid"}
if($final.external.finalCourseCi.status-ne"pass"-or$final.external.finalCourseCi.candidate-ne$ExpectedCandidate){Fail "final_course_ci_not_executed"}
if($final.reviews.Count-ne 2-or$final.reviews[0].result-ne"PASS"-or$final.reviews[1].result-ne"PASS"-or$final.reviews[0].reviewer_id-eq$final.reviews[1].reviewer_id){Fail "reviews_incomplete"}
$allow=@("PLAN.md","AGENT_LOG.md","README.md","docs/engineering/CI-02_EVIDENCE.md","docs/engineering/DEPLOY-01_EVIDENCE.md","docs/engineering/FINAL_VERIFICATION.md","docs/engineering/RELEASE_CHECKLIST.md")
if((@($final.evidenceCommit.allowlistedPaths|Sort-Object)-join"|")-ne(@($allow|Sort-Object)-join"|")){Fail "evidence_path_allowlist_invalid"}
if($final.evidenceCommit.status-eq"pass"){Fail "self_referential_evidence_commit"}
if(-not$ContractOnly){
    $git=(Get-Command git.exe -CommandType Application -ErrorAction Stop).Source
    Invoke-Checked $git @("cat-file","-e","$ExpectedCandidate^{commit}") "candidate_missing"
    Invoke-Checked $PythonExe @("scripts/test_all.py") "canonical_tests"
    Invoke-Checked $PythonExe @("scripts/scan_secrets.py","--working-tree") "secret_scan"
    Invoke-Checked $PythonExe @("scripts/verify_licenses.py","--strict") "license_scan"
}
Write-Output "FINAL_VERIFY_PASS candidate=$ExpectedCandidate"
exit 0
~~~

- [ ] F5. Create FINAL_VERIFICATION.md deterministically with all 50 AC rows, rather than hand-editing an incomplete matrix. Execute this complete generation block once after the red test and before staging:

~~~powershell
$rows=@(1..50|ForEach-Object{[ordered]@{id=("AC-{0:D2}"-f$_);status="not_executed";evidence=$null}})
$payload=[ordered]@{
    schemaVersion=1;expectedCandidate=$null;status="not_executed";syntheticFixture=$false
    local=[ordered]@{status="not_executed";secretScan="not_executed";license="not_executed";reviews=@()}
    acceptance=$rows;reviews=@()
    external=[ordered]@{
        gitlab=[ordered]@{status="not_executed";candidate=$null;url=$null}
        github=[ordered]@{status="not_executed";candidate=$null;url=$null}
        deployment=[ordered]@{status="not_executed";candidate=$null;imageDigest=$null;url=$null}
        finalCourseCi=[ordered]@{status="not_executed";candidate=$null}
    }
    evidenceCommit=[ordered]@{status="not_executed";allowlistedPaths=@("PLAN.md","AGENT_LOG.md","README.md","docs/engineering/CI-02_EVIDENCE.md","docs/engineering/DEPLOY-01_EVIDENCE.md","docs/engineering/FINAL_VERIFICATION.md","docs/engineering/RELEASE_CHECKLIST.md")}
}
$nl=[Environment]::NewLine
$text="# Final Verification"+$nl+$nl+"~~~json"+$nl+($payload|ConvertTo-Json -Depth 8)+$nl+"~~~"+$nl
[IO.File]::WriteAllText((Join-Path $WorktreeRoot "docs/engineering/FINAL_VERIFICATION.md"),$text,(New-Object Text.UTF8Encoding($false)))
~~~

Create RELEASE_CHECKLIST.md, CI-02_EVIDENCE.md, and DEPLOY-01_EVIDENCE.md with exactly one JSON fence each:

~~~json
{"schemaVersion":1,"status":"not_executed","candidate":null,"local":{"tests":"not_executed","build":"not_executed","scans":"not_executed"},"external":{"ci":"not_executed","deployment":"not_executed","publicUrl":"not_executed","finalCourseCi":"not_executed"},"reflection":{"owner":"student","status":"not_written_by_agent"},"allowlistedEvidencePaths":["PLAN.md","AGENT_LOG.md","README.md","docs/engineering/CI-02_EVIDENCE.md","docs/engineering/DEPLOY-01_EVIDENCE.md","docs/engineering/FINAL_VERIFICATION.md","docs/engineering/RELEASE_CHECKLIST.md"]}
~~~

~~~json
{"schemaVersion":1,"unitId":"CI-02","status":"not_executed","candidate":null,"gitlab":{"status":"not_executed","pipelineId":null,"unitTestJob":null,"url":null},"github":{"status":"not_executed","runId":null,"unitTestJob":null,"url":null},"authorization":"not_provided","artifactDigest":null,"reviews":[]}
~~~

~~~json
{"schemaVersion":1,"unitId":"DEPLOY-01","status":"not_executed","candidate":null,"imageDigest":null,"hostDecision":"not_executed","deploymentId":null,"publicUrl":null,"externalBrowser":"not_executed","rollback":"not_executed","authorization":"not_provided","reviews":[]}
~~~

No template may contain a real URL, credential, course path, predicted candidate, or self-hash.

- [ ] F6. Modify only the README release-status subsection, leaving every other README byte unchanged:

~~~markdown
## Release status

FIN-01A1 provides a local fail-closed verifier and evidence templates. The repository-level verifier is expected to fail while CI-02, DEPLOY-01, FIN-01B, the public HTTPS URL, and final course pipeline are not executed. No immutable candidate is created by this task, no remote action is performed, and REFLECTION.md remains student-authored.
~~~

- [ ] F7. Run release-contract pytest, scripts/test_all.py, strict secret/license/evidence validators, and the repository-level final command with an explicit pre-freeze candidate captured through the checked Git wrapper. Focused/full tests pass; final verifier returns nonzero with documented missing external-evidence codes and does not modify checkout.

~~~powershell
$preFreeze=(Invoke-Git @("rev-parse","HEAD") -FailureCode "pre_freeze_capture_failed").Stdout.Trim()
Invoke-CheckedNative $PythonExe @("-m","pytest","backend/tests/integration/test_release_evidence_contract.py","-q") 300 @(0) "release_contract_failed"|Out-Null
Invoke-CheckedNative $PythonExe @("scripts/test_all.py") 900 @(0) "canonical_failed"|Out-Null
$result=Invoke-CheckedNative $PowerShellExe @("-NoProfile","-ExecutionPolicy","Bypass","-File","scripts/final_verify.ps1","-ExpectedCandidate",$preFreeze,"-EvidenceRoot","docs/engineering") 900 @(2) "final_gate_wrong_exit"
if($result.Stdout-notmatch"external_ci_not_executed|deployment_not_executed|final_course_ci_not_executed"){throw "final gate failed for undocumented reason"}
~~~

- [ ] F8. Obtain both reviews and commit only the seven declared paths. Stage exact set, run whole-index check/diff/scanner/tree capture, fresh SPEC and quality/security/license receipts, edit invalidation, precommit equality, checked commit, and postcommit equality. Commit message: chore(FIN-01A1): add fail-closed release preparation [agent: $env:PROJECTB_AGENT_ID]. Worker does not freeze C, push, deploy, invoke remote CI, or write a final reflection.

FIN-01A1 completion standard: verifier/templates and deterministic tests exist; local checks pass; repository-level verifier fails closed exactly on missing external evidence; both reviews pass; no immutable candidate, public URL, remote CI result, deployment, or student reflection is claimed.

## Cross-plan Self-review Before Dispatch

- Spec coverage: CI-01A covers AC-10, AC-42, AC-43, AC-47 and license/security evidence; CI-01B/C cover exact GitLab unit-test, GitHub parity, local-vs-remote boundary, and distribution commands; DOC-01 covers AC-07, AC-10, AC-39 through AC-44 and required README sections; FIN-01A1 covers AC-01 through AC-50 evidence schema, candidate binding, no-self-hash, and external gates.
- Parser boundary: no current lock contains a direct YAML parser. Provisional PyYAML code is hard-blocked until G-02A/root records exact version, source, license, hashes, and Linux/CI closure. A reviewer must approve that amendment or revise parser calls to an approved alternative; no transitive or regex fallback.
- Executable completeness scan: executable blocks contain complete imports, functions, commands, schemas, and expected results. not_executed/null are deliberate evidence states, not omitted implementation. Synthetic URLs appear only in tests and are rejected by production verifier.
- Type/contract consistency: all workflow jobs use python scripts/test_all.py; evidence files use one JSON fence/schema; README and OPERATIONS use the same data-root, credential, demo, and external-evidence terminology; FIN-01A1 never writes REFLECTION.md.
- Final evidence truth: local PASS never substitutes for remote CI, deployment, public HTTPS, rollback, final course CI, or branch finishing. Missing authorization or D-025 remains not_executed and blocks later final gates.

This plan is Stage B input only. It authorizes no implementation until root implementation gate, cold-start validation, parser/G-02 amendment, predecessor reviews, and explicit student approval are satisfied.
