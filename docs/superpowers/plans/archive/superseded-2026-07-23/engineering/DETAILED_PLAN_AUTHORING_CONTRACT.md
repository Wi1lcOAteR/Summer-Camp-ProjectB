# Detailed Plan Authoring Contract

**Status:** Stage B planning rule. It constrains every formal file under `docs/superpowers/plans/`; it is not implementation, test output, review PASS, or permission to execute a task.

## Required Plan Shape

Every detailed subsystem plan must:

1. Use the exact Superpowers `writing-plans` title/worker-note/Goal/Architecture/Tech Stack header followed by `---`.
2. Name the exact root dispatch IDs it covers and exclude all others.
3. Provide a pairwise-disjoint path ownership table, plus every intentional later shared-path handoff.
4. Lock public types, function signatures, stable error codes, security invariants, and dependency versions before task bodies.
5. Give each dispatch unit exact dependencies, files, expected failing test, complete failing-test code, exact red command/result, complete minimal implementation code for every changed production file, exact green command/result, refactor, focused/full regression, Ruff/mypy where applicable, scanner, two reviews, exact staging, commit, hash capture, and completion standard.
6. Keep each checkbox to one 2--5 minute action. A command block may contain several commands only when each command is independently checked and the step remains one verification concern.
7. Use only synthetic or explicitly licensed fixtures. Never embed private courseware, real credentials, external account data, or fabricated execution output.
8. Keep human/external units blocked. A plan may define their validation procedure but cannot claim an account, remote CI run, deployment, cold-start response, student decision, or implementation approval occurred.

Signature-only overview blocks may use `...` when explicitly labelled non-executable. Executable test and implementation blocks may not use ellipses, `pass`, TODOs, placeholders, undefined helpers, or omitted imports.

## Runtime and Native-command Prelude

Every executable dispatch section must establish and validate the absolute runtime variables required by root `PLAN.md` and the immutable `docs/engineering/WORKTREE_MAP.v2.json` row: `PROJECTB_PYTHON_EXE`, `PROJECTB_NODE_EXE`, `PROJECTB_NPM_CMD`, and `PROJECTB_POWERSHELL_EXE`, plus unit ID, agent ID, base commit, worktree root, and the absolute Git application leaf. The prelude must read the v2 map blob at the declared base commit and compare the row's owner, branch, worktree, dependency hashes, plan blob hashes, and all four path/lowercase-sha256/exact-version/provenance attestations before any red test. Environment variables corroborate the immutable row; they never replace it.

PowerShell 5.1 is supported by the project. Therefore `[Diagnostics.ProcessStartInfo].ArgumentList` is prohibited. A bounded native wrapper must use a PS5.1-compatible argument transport (for example `Start-Process -ArgumentList` with an explicit Windows quoting function or `ProcessStartInfo.Arguments`), redirect stdout/stderr to bounded temporary files outside the repository, use a finite timeout, and recursively clean the full process tree with a PS5.1-compatible mechanism. The wrapper must test launch failure, nonzero exit, timeout, empty/malformed/multiline output, wrong executable, and fake-wrapper behavior when those failures affect authority. It must construct a sanitized child environment from an explicit allowlist of required non-secret `PROJECTB_*` paths/IDs, `SystemRoot`, and `PATH`; it may not inherit the caller environment wholesale or echo secrets. If a plan intentionally requires a PowerShell-7-only API, it must pin and validate that runtime instead of claiming PS5.1 support.

Use this minimum checked Git resolution in every prelude:

~~~powershell
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$GitExe = (Get-Command git -CommandType Application -ErrorAction Stop).Source
if (-not [IO.Path]::IsPathFullyQualified($GitExe) -or
    -not (Test-Path -LiteralPath $GitExe -PathType Leaf)) {
    throw "git executable must be an absolute existing leaf"
}
$Root = (Resolve-Path -LiteralPath $env:PROJECTB_WORKTREE_ROOT -ErrorAction Stop).Path
$Top = (& $GitExe -c "safe.directory=$($Root.Replace('\','/'))" -C $Root rev-parse --show-toplevel)
$GitExit = $LASTEXITCODE
if ($GitExit -ne 0 -or [IO.Path]::GetFullPath($Top.Trim()) -ne $Root) {
    throw "declared worktree is not the Git top-level"
}
~~~

Native output must be captured as status/code/count or redacted evidence. Never include complete child output, secret values, private paths, course bodies, or raw provider data in a thrown error or process log.
## Exact Staged-set and Private-review Packet Contract

Every commit step must compare the expected paths with the entire Git index. A pathspec-limited query cannot detect an unrelated or secret-bearing extra staged file.

~~~powershell
function Assert-ExactStagedPaths {
    param([Parameter(Mandatory)][string[]]$ExpectedPaths)
    $actual = @(
        & $GitExe -c "safe.directory=$($Root.Replace('\','/'))" -C $Root diff --cached --name-only
    )
    $exitCode = $LASTEXITCODE
    if ($exitCode -ne 0) { throw "staged-path query failed" }
    $actual = @($actual | Where-Object { $_ } | ForEach-Object { $_ -replace '\\','/' } | Sort-Object)
    $expected = @($ExpectedPaths | ForEach-Object { $_ -replace '\\','/' } | Sort-Object)
    if (($actual | Sort-Object -Unique).Count -ne $actual.Count) { throw "duplicate staged path detected" }
    if ($actual.Count -ne $expected.Count -or @(Compare-Object $expected $actual).Count -ne 0) {
        throw "whole-index staged path set mismatch"
    }
}
~~~

Each operation is checked independently: add only the literal owned paths; run the whole-index assertion; run `git diff --cached --check`; run the absolute committed scanner; and capture the exact staged bytes with `git diff --cached --binary --full-index --no-ext-diff` into a current-user-only temporary directory outside the repository. The packet must not be printed, committed, or copied into evidence. Hash the packet bytes with SHA-256, validate a lowercase 40-hex `git write-tree` ID, and record only packet path, byte count, packet hash, tree ID, expected path count, and a redacted status.

Both fresh reviewer receipts must name the same packet hash and tree ID, exact root/contract/subplan hashes, unit ID, worker identity, distinct reviewer identities, and observed test/static/scanner results. A reviewer that cannot access the private packet must return NOT PASS; a packet hash or tree mismatch invalidates both reviews. Any implementation, formatting, staging, or review-driven edit requires a new scanner run, packet hash, tree ID, and both reviews. Immediately before commit, repeat the complete proof and require the new tree ID to equal the reviewed tree; commit only through the checked native wrapper. After commit, capture and validate `git rev-parse HEAD` and `git rev-parse HEAD^{tree}` independently and require the committed tree to equal the reviewed tree. Never run a bare commit after a pathspec-limited query or let a later successful command mask a failure.

## TDD and Review Evidence

For every behavior change, the plan must preserve these separate observable checkpoints:

- Red test source written before production source.
- Focused red command exits nonzero for the named missing/incorrect behavior, not an environment accident.
- Minimal implementation source.
- Focused green command exits zero.
- Refactor under the passing focused test.
- Focused regression, affected-suite regression, configured Ruff, configured mypy, and canonical `scripts/test_all.py` each run and are checked independently.
- Staged credential scan, exact staged-set evidence, and a checked `git write-tree` ID bound to both reviews and the committed `HEAD^{tree}`.
- Fresh SPEC reviewer findings first, then PASS after Critical/Important issues are resolved.
- Different fresh quality/security/license reviewer findings first, then PASS after Critical/Important issues are resolved.
- Worker, SPEC reviewer, and quality reviewer identities match `^[A-Za-z0-9][A-Za-z0-9._-]{1,63}$`, are non-empty, and are pairwise distinct.
- The coordinator records the observed commit hash and evidence in root `PLAN.md` and `AGENT_LOG.md`; the worker does not edit shared ledgers.

Plans must not preclaim exact passing test counts unless the complete displayed final code has been mechanically reconstructed on the same plan hash. Prefer `all focused tests pass` and require the executor to record actual counts.

## Cross-plan Review

Before any detailed-plan hash is marked PASS, independent reviewers must compare it with the same root `PLAN.md` hash and its direct predecessor/successor plan contracts. Review at least:

- Path ownership and create/modify timing.
- Type names, enum values, signatures, error codes, serialization, and public exports.
- Dependency order and shared-file handoffs.
- Security, credential, consent, provider, audit, and untrusted-input boundaries.
- Final cumulative tests: no earlier test may permanently assert a condition a later unit is required to change.
- PowerShell fail-closed behavior and exact staged-index safety.
- License/provenance coverage and absence of private fixtures.

A balanced fence, parseable code block, lexical AC match, or file hash is necessary mechanical evidence but is not by itself a plan PASS.
