# ProjectB v1 Implementation Plan

<!-- AGENT_CAPSULE:PLAN:BEGIN -->
# Cold-Start Execution Capsule (generated; do not edit)

Version: 1. This ASCII capsule is a normative execution projection of the cited PLAN sections. The full PLAN remains required. Any conflict with the body invalidates the document and must be returned as an ambiguity; do not guess or choose precedence.

## Gates
The plan is NOT DISPATCHABLE. Product implementation is forbidden until same-byte mechanical and dual reviews pass, formal non-Codex G-03 completes, repairs are reviewed, and the student explicitly grants G-04. G-03 is the sole disposable pre-dispatch exception. Its artifacts are evidence only: do not commit, merge, update the task ledger, edit the real repository, contact a product provider, or treat its output as formal F-01S1A implementation.

## TDD and review protocol
For every behavior, first add the smallest requirement-shaped assertion, run the exact target command, and observe the expected failure for the missing behavior. Add only the smallest named implementation that makes the unchanged command pass. Then refactor under green tests, run targeted and regression gates, scan owned paths, obtain SPEC compliance review before quality/security/license review, and commit only after both reviews have no Critical issue. Preserve original candidate contract/scanner SHA-256 before and after every replay and direct scan, and persist the normalized ordered TDD receipt. Never weaken, skip, delete, or rewrite an assertion to manufacture green. Stop and report any ambiguity, missing dependency, unexpected failure, or step that cannot fit the task card.

## Formal G-03 protocol
Use two fresh non-Codex sessions with only final SPEC.md and PLAN.md in the initial directory. Both files must pass strict UTF-8 validation with no BOM, invalid bytes, or U+FFFD. Auto and English use this generated English capsule. Chinese mode is diagnostic only. Native Read is unavailable; use only the runner-provided strict UTF-8 extraction command.

Intake is read-only, Bash-only, has a USD 0.20 and five-minute limit, and must return structured data containing exact hashes of both files, the complete file listing, requested/effective language, target task F-01S1A, acceptance ID F01S1A_SINGLE_RULE_SCANNER_V2, and an ambiguity list. Execution must not start unless hashes, listing, task ID, acceptance ID, and empty ambiguity list are independently validated.

Execution is a second fresh session, has a USD 0.80 and twenty-minute limit, permits only sandboxed Bash, and may not use native Read/Edit, network, commit, or a third project context file. Before any key is requested, a live bubblewrap preflight must prove fail-closed startup, credential-environment scrubbing, host-mount exclusion, network isolation, bounded process-tree termination, and writes confined to the disposable root. Both sessions request claude-sonnet-4-6 with zero API retries and no fallback model. Empty end_turn, 504, timeout, budget breach, protocol mismatch, missing artifact, or extra artifact fails closed. CLI exit 0 alone never means completion.

## Target task F-01S1A
Initial files are exactly SPEC.md and PLAN.md. Create exactly two non-empty files: scripts/tests/bootstrap_scanner_contract.ps1 and scripts/bootstrap_scan_credentials.ps1. Do not modify either input document. The contract is at most 180 lines and the scanner is at most 140 lines. Implement only Write-ScanRecord, Convert-SourceText, Find-DirectSecret, and minimal single-path wiring. Positive fixtures are assembled at runtime from two fragments that do not match independently.

The only rule is provider_api_key: literal sk- plus 20--200 characters from [A-Za-z0-9_-], bounded at both ends by start/end or a character outside [A-Za-z0-9_-]. Source is always the literal path. Stable output path is the caller's -Path text with backslashes changed to forward slashes and one leading ./ removed; an absolute path used for reading never replaces this receipt path. Missing scope, read failure, and strict-UTF-8 failure use usage_missing_scope, read_failed, and decode_failed respectively.

The unchanged contract command is pwsh -NoProfile -File scripts/tests/bootstrap_scanner_contract.ps1. Before the scanner exists, require exit 1 with exactly CONTRACT_RED scanner_missing. After minimum implementation, require usage_and_output, provider_rule, then BOOTSTRAP_SCANNER_PATH_PASS. The direct artifact command is pwsh -NoProfile -File scripts/bootstrap_scan_credentials.ps1 -Path FILE. Clean is exit 0 with exactly CREDENTIAL_SCAN_PASS files=1; findings are exit 2 with exact key order source,path,rule; operational failure is exit 3 with stable code and optional source then path. Output never contains values, content, line data, decoded payloads, exceptions, or blob OIDs.

## Completion evidence
A candidate execution has exactly the two input documents and two allowed artifacts, unchanged input hashes, recorded and ordered Bash tool-use/tool-result evidence for the exact red and green commands, artifact SHA-256 and line counts, an added-files diff, questions/ambiguities, actual cost, and a final English summary of at most 300 words. After removing authentication variables, the coordinator independently replays the red and green conditions inside a new credential-free, network-unshared, mount-limited bubblewrap with a process-tree timeout. Its own oracle checks the provider rule lower/max/overmax lengths, punctuation and blocked-neighbor boundaries, strict UTF-8, path/source/error semantics, redaction, exact artifact bytes, and both line limits. No tool write, truncation, timeout, budget breach, or missing terminal result is incomplete, never PASS. Candidate-authored PASS text is not an oracle. Test-only paths cannot emit formal readiness. G-03 passes only after replay and process documentation; disposable files are never integrated.
<!-- AGENT_CAPSULE:PLAN:END -->

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` or `superpowers:executing-plans` to execute one task at a time. Every behavior task uses `superpowers:test-driven-development`; unexpected failures use `superpowers:systematic-debugging`; reviews use `superpowers:requesting-code-review` and `superpowers:receiving-code-review`; completion claims use `superpowers:verification-before-completion`; each worktree group closes with `superpowers:finishing-a-development-branch`.

**Status:** `G-03 COMPLETE / G-04 APPROVED / IMPLEMENTATION ACTIVE`

**SPEC binding:** the student confirmed the complete G-03 atomic SPEC on 2026-08-03 and later confirmed local-only delivery on 2026-08-09. Current SPEC SHA-256 is `483EF900BF9F5ED90FDA6117607D8F2436F3BDA633033FE2A0CB64AD6CAFC72E`; prior reviews and intake do not transfer to these bytes.

**Goal:** Build the reduced v1 local study workbench: source-grounded material import and mapping, deterministic learning evidence for mutex/race/deadlock, and continuous/finals review planning, with an optional consent-bound OpenAI P adapter and a local-only mock demo.

**Architecture:** React/Vite calls a profile-aware FastAPI application. Domain services own authority; SQLite stores metadata and append-only evidence; a content-addressed current-user store keeps material bytes; Windows Credential Manager keeps secrets. Provider output is non-authoritative and replaceable by a deterministic mock. The local profile is loopback-only; the public demo exposes only synthetic licensed fixtures, ephemeral state, and the mock.

**Pinned stack:** CPython 3.14.6; FastAPI 0.139.2; Pydantic 2.13.4; SQLite; pypdf 6.14.2; pypdfium2 5.12.1; keyring 25.7.0; OpenAI SDK 2.46.0; pytest 9.1.1; Ruff 0.15.22; mypy 2.3.0; Node 24.18.0/npm 11.16.0; React 19.2.7; Vite 8.1.5; TypeScript 7.0.2; Vitest 4.1.10; Playwright 1.61.1; axe 4.12.1; PyInstaller 6.21.0. Windows, Linux-CI, Linux-demo, npm, OCI-base, and license evidence are frozen under `docs/engineering/`.

## 1. Dispatch Gates

No formal task dispatch, task-status change, implementation commit, or integration may start until all of these are true on the same final SPEC/PLAN bytes. G-03 is the only pre-dispatch exception: two fresh sessions of one different-type coding agent work in a disposable copy containing only `SPEC.md` and `PLAN.md`. The read-only intake validates hashes, English capsules, target `F-01S1A`, acceptance ID `F01S1A_SINGLE_RULE_SCANNER_V2`, and ambiguity status. Only a clean intake may start execution. Neither session may commit, integrate, edit the real repository, or change the ledger. The disposable attempt leaves formal F-01S1A `not started`; only questions, misunderstandings, output gaps, receipts, and resulting documentation diffs become evidence. `G-03P` is remediation input but never closes G-03 or authorizes implementation.

1. `SR-08`: mechanical audit, SPEC-compliance review, and quality/security/license review all report no Critical or Major issue and record both hashes externally.
2. `G-03`: fresh non-Codex intake and execution sessions, with only final `SPEC.md` and `PLAN.md`, validate the English capsules and attempt complete `F-01S1A`. Record every question, misunderstanding, output gap, red/green output, independent replay, cost, and repair in `SPEC_PROCESS.md`. A Codex `G-03P` receipt cannot satisfy this item.
3. The repaired SPEC/PLAN snapshot is re-reviewed if either file changes.
4. `G-04`: after reading the cold-start record and repairs, the student explicitly approves implementation. The earlier SPEC confirmation is not G-04.

The student has confirmed local-only delivery for this project; D-025 public hosting and public URL evidence are waived and do not block local implementation or local release. `EXT-REMOTE-PREP`/`EXT-REMOTE-FINAL` remain unexecuted remote-mutation gates and cannot be represented as local evidence.

## 2. Worktrees, Ownership, and Order

After G-04, the coordinator creates these worktrees in order. `codex/foundation-v1` starts at the reviewed Stage-B tip; every later worktree starts at the reviewed terminal commit of the immediately preceding row, so the nine branches form one ancestry chain. No implementation tasks are parallel: API/UI registries, migrations, and evidence ledgers have serialized ownership, and the reduced plan favors recoverable commits over merge concurrency.

| Worktree branch | Tasks, strictly in order | Closure |
| --- | --- | --- |
| `codex/foundation-v1` | F-01S1A -> F-01S1B -> F-01S2 -> F-01S3 -> F-01S4 -> F-01A -> F-01B -> F-01C -> F-01D -> F-01E -> F-02 -> F-03 -> F-04 -> F-05 | next branch starts only at its reviewed terminal tip |
| `codex/m1-materials-v1` | M1-01 -> M1-02 -> M1-03 | next branch starts only at its reviewed terminal tip |
| `codex/m2-learning-v1` | M2-01 -> M2-02 -> M2-03 -> M2-04 | next branch starts only at its reviewed terminal tip |
| `codex/m3-api-v1` | P-01 -> M3-01 -> M3-02 -> API-01 -> API-02 -> API-03 | next branch starts only at its reviewed terminal tip |
| `codex/webui-v1` | UI-01 -> UI-02 -> UI-03 -> UI-04 -> UI-05 -> UI-06 | next branch starts only at its reviewed terminal tip |
| `codex/demo-v1` | DEMO-01 | next branch starts only at its reviewed terminal tip |
| `codex/provider-openai-v1` | P-02 | next branch starts only at its reviewed terminal tip |
| `codex/distribution-v1` | DIST-01 -> DIST-02 | next branch starts only at its reviewed terminal tip |
| `codex/release-v1` | CI-01 -> PREP/HOST/VM closures -> DOC-01 -> compliance -> REFLECTION-CLOSE -> EXT-REMOTE-FINAL | no push, MR, PR, deployment, publication, reflection commit, retarget, or merge without its named gate |

Only the root coordinator edits `PLAN.md`, `AGENT_LOG.md`, `SPEC_PROCESS.md`, or the compliance audit. Workers never stage those paths. Shared evidence updates happen after a terminal reviewed implementation hash exists. DOC-01 therefore does not own the compliance audit; the coordinator updates it in the scanned evidence commit after DOC-01 review.

## 3. Per-Task Protocol

Each task is one fresh subagent session with only its task card, confirmed SPEC, predecessor interfaces, exact commands, and owned paths. The following ordered checklist is already part of every card; it is not deferred to the dispatch prompt: `S0` run preflight; then, for each comma/slash-separated failure named in that card's Red field from left to right, `R1` add exactly one assertion and its smallest fixture to the first applicable owned test path, `R2` run the card's exact Red command and record the requirement-shaped failure, `G1` add or change exactly one named production function/schema object/configuration stanza in the listed Goal path that owns that assertion, and `G2` rerun the same targeted command. Each `R1`, `R2`, `G1`, and `G2` is a separate 2--5 minute checkbox; the next named failure cannot start before the current one is green. After the last assertion, `X1` refactor one symbol, `X2` rerun targeted green, `X3` run each listed regression/gate command separately, `X4` stage only owned paths and scan, `X5` request SPEC review, `X6` request quality/security/license review, `X7` commit, and `X8` record coordinator evidence. If any one step exceeds five minutes, stop as a plan defect. F-01S1A through F-01S4 are a serialized contract-first exception because they share two files: each task adds only its named groups and helpers, must leave the accumulated contract green, and may not weaken predecessor assertions.

Path aliases are exact: `domain/`, `services/`, `repositories/`, `storage/`, `security/`, `observability/`, `api/`, `providers/`, and `profiles/` mean the corresponding path below `backend/projectb/`; `evaluators/` means `backend/projectb/domain/learning/evaluators/`; `views/` and `styles/` mean the corresponding path below `frontend/src/`. No other abbreviation is allowed. A directory path ending `/` grants ownership only of the explicitly named descendants in that card, never an open glob.

`F-01S1A` through `F-01S4` use only Git and PowerShell because no committed project runtime exists yet. Their cross-platform contract and direct commands use PowerShell 7 as exact `pwsh -NoProfile -File ...` commands; later Windows-only bootstrap commands retain their explicitly written Windows PowerShell form. G-03/G-03P attempts only F-01S1A in a disposable directory and must run a real red then green without dependency downloads, commits, or original-repository edits. Formal F-01S1A after G-04 repeats that task; F-01S1B/S2/S3/S4 extend the same two files serially. F-01A creates the project-local toolchain only after F-01S4. Before F-01S4 exists, each scanner task scans its owned artifacts using all rules implemented so far and records the scoped clean receipt; after F-01S4, every implementation, review-fix, and coordinator evidence commit runs `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/bootstrap_scan_credentials.ps1 -Tracked -Staged`. Any Git/index/read/decode/scan error fails closed and no matching value is printed.

1. Run the worktree preflight and bind `$TaskId`, `$AgentId`, `$HumanChanges`, base commit, clean index, and predecessor hashes. Run the committed `scripts/bootstrap.ps1`, which provisions checksum-verified uv 0.11.14, CPython 3.14.6, and Node 24.18.0 under ignored project-local paths; it must never alter system PATH. Use its resolved `$Uv`, `$Py`, `$Node`, and `$Npm` paths. UI tasks additionally run `& $Npm --prefix frontend exec -- playwright install chromium`.
2. Write the named minimum failing test first. Run the exact red command and record its exit code plus the requirement-shaped failure. A missing test, import typo, or environment failure is not a valid red.
3. Implement the minimum behavior, run the exact green command, refactor under tests, then run `& $Py -m ruff check backend scripts`, `& $Py -m mypy backend/projectb`, `& $Py scripts/test_all.py`, `git diff --check`, `& $Py scripts/scan_credentials.py --tracked --staged`, and `& $Py scripts/verify_licenses.py` whenever those paths exist.
4. On any unexpected result, invoke `systematic-debugging` and log cause/evidence. Do not weaken, delete, skip, or mark a test expected-failure to obtain green.
5. Stage only owned paths, run the scanner again against both index and working-tree sources, and commit with the task card subject plus trailers `Task-ID: $TaskId`, `Agent: $AgentId`, and `Human-Changes: $HumanChanges`. No real key, model response, private material, generated database, build output, or browser profile may be staged. If `Human-Changes` names student-written code, each affected file or function must also contain a top comment `Student-authored: SCOPE`; generated files and formats that forbid comments are listed only in the trailer/log.
6. Request a SPEC/acceptance review first. If it passes, request correctness, maintainability, security, test, and license review. Apply valid feedback through `receiving-code-review`, add a regression red when behavior changes, recommit, and repeat both reviews against the terminal commit. Critical issues stop the sequence.
7. Run `verification-before-completion` on the terminal commit. The coordinator then records timestamp, task ID, skill chain, exact prompt/context, canonical worker ID, red/green/regression receipts, both reviews, terminal commit, human edits/reason, lesson, and license/scan result in `AGENT_LOG.md`; it stages only the owned ledger/log/audit paths, runs the same index-and-working-tree scanner, and marks the PLAN ledger in a separate `docs(task): record evidence [agent: coordinator]` commit.
8. At the end of each worktree group, invoke `finishing-a-development-branch`. Local integration is allowed after G-04; remote push/PR/MR is forbidden until `EXT-REMOTE-PREP`, and final merge/CI evidence is forbidden until `EXT-REMOTE-FINAL`.

### 3.1 Normative plan freeze versus mutable evidence

SR-08, G-03, and G-04 bind the full SPEC hash and the full pre-dispatch PLAN hash. After G-04, the coordinator may change only a ledger row's `status` from `not started` to `in progress`/`complete`, its `terminal commit` from `none` to one exact 40-hex hash, and the top execution-status label; each such evidence-only diff must be scanner-clean and committed separately. Those narrow changes do not alter the normative plan and do not invalidate SR-08/G-03/G-04. Any other PLAN or SPEC byte change is normative, immediately stops dispatch, and requires new hashes, mechanical audit, both reviews, G-03 repair if execution semantics changed, and fresh G-04 approval.

Common Windows bootstrap after F-01A:

```powershell
$RepoRoot = (git rev-parse --show-toplevel).Trim()
$UvRoot = Join-Path $RepoRoot 'tmp\toolchains\uv-0.11.14-x86_64-pc-windows-msvc'
$PythonRoot = Join-Path $RepoRoot 'tmp\toolchains\python-3.14.6-embed-amd64'
$NodeRoot = Join-Path $RepoRoot 'tmp\toolchains\node-v24.18.0-win-x64'
$Uv = Join-Path $UvRoot 'uv.exe'
$Py = Join-Path $PythonRoot 'python.exe'
$Node = Join-Path $NodeRoot 'node.exe'
$Npm = Join-Path $NodeRoot 'npm.cmd'
& (Join-Path $RepoRoot 'scripts\bootstrap.ps1')
& $Uv --version
& $Py --version
& $Node --version
& $Npm --version
$env:PATH = "$PythonRoot;$NodeRoot;$env:PATH" # current process only; never persisted
& $Npm --prefix frontend ci --ignore-scripts
```

Exact shared command blocks used by task cards:

```powershell
# BE-REGRESSION
& $Py -m ruff check backend scripts
& $Py -m mypy backend/projectb
& $Py scripts/test_all.py

# LICENSE-SECURITY-GATE, after staging only owned paths
& $Py scripts/scan_credentials.py --tracked --staged
& $Py scripts/verify_licenses.py
git diff --check

# FE-REGRESSION
& $Npm --prefix frontend exec -- vitest run
& $Npm --prefix frontend run build
& $Py scripts/test_all.py
```

## 4. Task Ledger

| # | Task | Depends on | Parallel | Worktree | Status | Terminal commit |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 | F-01S1A | G-04 | no: atomic scanner starts the chain | foundation | complete | b997fccae5c04cfa08547f5f9a99e8bbbd4f08d8 |
| 2 | F-01S1B | F-01S1A | no: extends shared direct-rule files | foundation | complete | c07b90823448600950ba59e7ea4522a190918e92 |
| 3 | F-01S2 | F-01S1B | no: extends shared scanner files | foundation | complete | 3a75411e210f99bc7098a2dfb3a1197ce8b96640 |
| 4 | F-01S3 | F-01S2 | no: extends shared scanner files | foundation | complete | b7d929771657c02ff40150a8f81768a31ec0dfed |
| 5 | F-01S4 | F-01S3 | no: closes full scanner gate | foundation | complete | 1d6dcab15adf1649cda7309360f3cdeff0423e27 |
| 6 | F-01A | F-01S4 | no: materializes runtimes and locks | foundation | complete | `8b725db53d044af41e9d6352802eecbe0c2e5d6d` |
| 7 | F-01B | F-01A + BOOTSTRAP-LICENSE-EVIDENCE | no: closes bootstrap licenses | foundation | complete | `8b725db53d044af41e9d6352802eecbe0c2e5d6d` |
| 8 | F-01C | F-01B | no: creates frontend harness | foundation | complete | `39d79c2e6d423883a0614cc8d9bb947dd02a7dba` |
| 9 | F-01D | F-01C | no: seeds push CI before feature branches | foundation | complete | `069acb8541b8d59a7977a484f06d8f9abbefe780` |
| 10 | F-01E | F-01D | no: creates shared quality gates | foundation | complete | ae152e3 |
| 11 | F-02 | F-01E | no: migration order | foundation | complete | 62022db |
| 12 | F-03 | F-02 | no: migration order | foundation | complete | `1aaeb6f1912c7f1e5323ea6ab843b689937adbd1` |
| 13 | F-04 | F-03 | no: security base | foundation | complete | `736292a14b41083122791a7182f554e354943a5f` |
| 14 | F-05 | F-04 | no: security base | foundation | complete | `e11a150e1f0233206803a4763a53f237fced097c` |
| 15 | M1-01 | F-05 | no: material contracts | m1-materials | complete | `07ebf95f0ac3c4c9436619bf74be4c78a7612913` |
| 16 | M1-02 | M1-01 | no: consumes extraction | m1-materials | complete | `bdc893ef99e0ac7cac4d1481052fc30e5d5333b9` |
| 17 | M1-03 | M1-02 | no: consumes material repo | m1-materials | complete | `aa2a6da62cc0d185510c2b17e33ab168f33a74d6` |
| 18 | M2-01 | M1-03 | no: evaluator base | m2-learning | complete | `9b49e07b6e5a237005c1d267f84b902cc48fff7c` |
| 19 | M2-02 | M2-01 | no: registry assembly | m2-learning | complete | `4c384f7e7d6360a96a81480d22309645356f9fe0` |
| 20 | M2-03 | M2-02 | no: evidence authority | m2-learning | complete | `2da06362bbd11d3d8da2a8b8b3e49c63f57cae82` |
| 21 | M2-04 | M2-03 | no: mastery consumes evidence | m2-learning | complete | `7d72b02e46f0a05d456e031d6e1720923570f8f5` |
| 22 | P-01 | M2-04 | no: provider port and mock | m3-api | complete | `f2563ac87cf61665dae98d404a02dff41f9fab37` |
| 23 | M3-01 | P-01 | no: planner contract | m3-api | complete | `36e7ee8992fc8b15df7ee3360e9f5ca517c7e52c` |
| 24 | M3-02 | M3-01 | no: revision persistence | m3-api | complete | `3a93f27a48f3e027380135a2b65f4b28f3f4a624` |
| 25 | API-01 | M3-02 | no: creates app registry | m3-api | complete | `6d44eacfbde94d36042e9037c8d4cacfe208b4fc` |
| 26 | API-02 | API-01 | no: modifies app registry | m3-api | complete | `7da00e3cb5dc371291d2d164a1ebd677049cdabc` |
| 27 | API-03 | API-02 | no: closes local API | m3-api | complete | `e41df6a93eb999746c1b6314c2e2a2d9c4dda8bb` |
| 28 | UI-01 | API-03 | no: creates route registry | webui | complete | `c6a63d7ddd887384170ccfee70fa3f54b3b00102` |
| 29 | UI-02 | UI-01 | no: modifies route registry | webui | complete | `4c14231ad3511109929779d88a49f05969413eaa` |
| 30 | UI-03 | UI-02 | no: modifies route registry | webui | complete | `891c057a5b0faa1ce390a1534efd87be65bce62e` |
| 31 | UI-04 | UI-03 | no: modifies route registry | webui | complete | `6f057f25a0ca1ccd7909e6b247e3359bfcd0e3f4` |
| 32 | UI-05 | UI-04 | no: modifies route registry | webui | complete | `0f644dd5cf9d865d5c70fad0ce52d96ac3aad47b` |
| 33 | UI-06 | UI-05 | no: modifies route registry | webui | complete | `b67d6529fad1193177732513aba106198f13a2e6` |
| 34 | DEMO-01 | UI-06 | no: profile assembly | demo | complete | `a160f72ad9cd60021e6d34b2f4438978a2c2ce5e` |
| 35 | P-02 | DEMO-01 + P-EVIDENCE | no: real adapter is isolated last | provider-openai | complete | `8e6b23f` |
| 36 | DIST-01 | P-02 + QA-RELEASE | no: Windows release | distribution | complete | `662a381` |
| 37 | DIST-02 | DIST-01 | no: consumes frozen frontend/runtime | distribution | complete | `5145fea` |
| 38 | CI-01 | DIST-02 | no: consumes all commands | release | complete | `3a51c7b` |
| 39 | DOC-01 | CI-01 + DIST-01-VM-CLOSE | no: final verified guide | release | in progress: local guide/tests green; VM performance and Git commit pending | none |

## 5. Foundation Tasks

### F-01S1A: Single-path scanner protocol and provider rule

- **Dependencies / parallelism:** G-04 for formal implementation; G-03/G-03P may attempt this complete task before dispatch. No parallel work because F-01S1A through F-01S4 share exactly two files.
- **Goal / files:** Create only `scripts/tests/bootstrap_scanner_contract.ps1` and `scripts/bootstrap_scan_credentials.ps1`. Implement `Write-ScanRecord`, `Convert-SourceText`, `Find-DirectSecret`, and minimal `-Path` wiring. The only rule is `provider_api_key`: literal `sk-` plus 20--200 `[A-Za-z0-9_-]`, bounded at each end by start/end or a character outside `[A-Za-z0-9_-]`. `source` is always literal `path`; receipt `path` is the caller's argument with `\` changed to `/` and one leading `./` removed. Reading may resolve an absolute path but must not replace receipt text. Decode strict UTF-8 without BOM or `U+FFFD`. Missing scope, non-file/read failure, and decode failure are `usage_missing_scope`, `read_failed`, and `decode_failed`. Runtime positive fixtures join two independently non-matching fragments.
- **Red:** create only the contract file with groups `usage_and_output` and `provider_rule`; run exactly `pwsh -NoProfile -File scripts/tests/bootstrap_scanner_contract.ps1`; expect exit 1 and the sole output `CONTRACT_RED scanner_missing`.
- **Green/refactor:** create the scanner and rerun the unchanged command; require both group names followed by `BOOTSTRAP_SCANNER_PATH_PASS`. Clean is exit 0 with exactly `CREDENTIAL_SCAN_PASS files=1`. Findings are exit 2, one per unique result, with exact JSON key order `source,path,rule`; operational failure is exit 3 with exact `code` and optional `source,path`. Never print values/content/line data/decoded payloads/exceptions/OIDs. The contract is at most 180 lines and scanner at most 140 lines; exceeding either is a plan defect, not completion.
- **Done / commit:** G-03 records exact hashes, line counts, red/green tool results, direct provider-rule oracle, stable source/path/error checks, <=300-word final English summary, questions, and cost, then stops without integration. Formal post-G-04 execution repeats the task, obtains both reviews, and commits `build(F-01S1A): add single-path scanner core [agent: worker]`.

### F-01S1B: Remaining direct rules and artifact safety

- **Dependencies / parallelism:** F-01S1A; no, because this task extends the same contract and scanner and may not weaken its two predecessor groups.
- **Goal / files:** Modify only the two F-01S1A files. Add exact rules: `github_token` uses `ghp_,gho_,ghu_,ghs_,ghr_` plus 20--255 `[A-Za-z0-9]`; `aws_access_key` uses `AKIA|ASIA` plus exactly 16 `[A-Z0-9]`; `google_api_key` uses `AIza` plus exactly 35 `[A-Za-z0-9_-]`; `slack_token` uses `xoxb-,xoxp-,xoxa-,xoxr-,xoxs-` plus 10--200 `[A-Za-z0-9-]`; `private_key` is `-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----`. The first four use the same neighbor boundary as F-01S1A. Add stable dedupe/sort by `source,path,rule` and artifact byte safety.
- **Red:** add `direct_rules_and_order` and `artifact_direct_safety`, run the unchanged contract, and observe the first missing rule/order/safety behavior while the two F-01S1A groups remain green.
- **Green/refactor:** implement only the five rules, dedupe/sort, and self-safety needed by those groups. Require `usage_and_output`, `provider_rule`, `direct_rules_and_order`, `artifact_direct_safety`, then `BOOTSTRAP_SCANNER_CORE_PASS`; directly scan both owned files and require exit 0 with exactly `CREDENTIAL_SCAN_PASS files=1` each.
- **Done / commit:** all six direct shapes, boundaries, stable order, redaction, and both artifact scans pass; both reviews pass. Commit `build(F-01S1B): complete direct scanner rules [agent: worker]`.

### F-01S2: Assignment and encoded-secret rules

- **Dependencies / parallelism:** F-01S1B; no, because this task extends the same contract and scanner and may not weaken the four predecessor groups.
- **Goal / files:** Modify only the two F-01S1A files. Add `Find-AssignmentSecret` and `Find-EncodedSecret`. Assignment names are case-insensitive `api_key|api-key|apikey|access_token|auth_token|client_secret|password|passwd|secret|token`, bounded on the left by start or non-`[A-Za-z0-9_-]`, then optional horizontal whitespace, `:` or `=`, and optional horizontal whitespace. A quoted value uses the same opening/closing single or double quote, forbids CR/LF, permits backslash only before that matching quote or backslash, and contains 8--512 decoded characters; an unquoted value is the maximal 8--512 run of `[A-Za-z0-9_./+=:@-]`. Safe whole values after ASCII trim and case-fold are exactly `example,placeholder,changeme,not-set,none,null,redacted`, one nonempty angle-bracket pair, `\$(?:[A-Za-z_][A-Za-z0-9_]*|\{[A-Za-z_][A-Za-z0-9_]*\})`, or `\[[^\]\r\n]*redacted[^\]\r\n]*\]`.
- **Encoded contract:** `encoded_secret` decodes exactly one layer and then applies only the six direct rules, never assignment matching. Standard Base64 candidate `[A-Za-z0-9+/]{16,4096}={0,2}` is bounded by start/end or non-`[A-Za-z0-9+/=]`; Base64URL candidate `[A-Za-z0-9_-]{16,4096}={0,2}` is bounded by start/end or non-`[A-Za-z0-9_=-]`. Both require legal padding, total length divisible by four, strict byte decoding, and strict decoded UTF-8. Hex candidate `[0-9A-Fa-f]{32,8192}` is even-length and bounded by start/end or non-hex. Tests name every rule ID and assert boundary negatives for every candidate family.
- **Red:** add `assignment_quotes_boundaries` and the encoded cases within `encodings_and_types`, run the unchanged contract, and observe the first missing named rule without changing predecessor assertions.
- **Green/refactor:** implement only the two named helpers; run the unchanged contract and require predecessor groups plus the two new groups and `BOOTSTRAP_SCANNER_RULES_PASS`. Re-run direct artifact safety against exact bytes of both files.
- **Done / commit:** all direct, assignment, placeholder, quote, boundary, and one-layer encoded cases pass with no content leak. Both reviews pass; commit `build(F-01S2): add assignment and encoded rules [agent: worker]`.

### F-01S3: Exact worktree and staged-index sources

- **Dependencies / parallelism:** F-01S2; no, because this task extends the same files and consumes the stable rule helpers.
- **Goal / files:** Modify only the two scanner files. Add `Invoke-GitProcess`, `Get-WorktreeSources`, `Get-IndexSources`, `Read-WorktreeBytes`, and `Read-IndexBlobBytes`. `-Tracked` scans current worktree bytes from `git ls-files -z`; `-Staged` resolves one regular stage-0 entry and reads exact blob bytes through binary-safe `git cat-file blob OID`. Both switches scan both source/path pairs. Worktree components must remain below the Git root, be regular, and lack `ReparsePoint`; index paths must be normalized, non-absolute, non-escaping, and mode `100644` or `100755`.
- **Red:** add `staged_vs_worktree`, `index_modes_and_rename`, and source portions of `path_safety_and_errors`. PATH-first fake Git proves nonzero list/cat-file, zero/two stage-0 rows, escaping paths, unsupported modes, rename, staged-secret/clean-worktree, clean-index/dirty-worktree, and binary-safe blob separation.
- **Green/refactor:** implement the five helpers and connect them to the existing rules; run the unchanged contract and require all accumulated groups plus `BOOTSTRAP_SCANNER_SOURCES_PASS`. Stable errors are `git_root_failed`, `git_list_failed`, `index_entry_failed`, `index_mode_unsupported`, `path_escape`, `reparse_point`, `not_regular_file`, and `read_failed`.
- **Done / commit:** exact index/worktree source reporting, mode/path safety, rename handling, error redaction, and all predecessor groups pass. Both reviews pass; commit `build(F-01S3): add exact Git source scanning [agent: worker]`.

### F-01S4: Full orchestration, formats, and bootstrap gate

- **Dependencies / parallelism:** F-01S3; no, because this task closes the scanner used by every later task.
- **Goal / files:** Modify only the two scanner files. Add `Invoke-BootstrapScan`, UTF-8 with/without BOM, BOM-declared UTF-16LE/BE, unmarked-NUL rejection, dedupe/sort by source/path/rule, and constant top-level `scan_failed`. The text allowlist is `.md,.txt,.json,.jsonl,.toml,.yaml,.yml,.ini,.cfg,.conf,.env,.example,.py,.pyi,.js,.mjs,.cjs,.ts,.tsx,.jsx,.html,.css,.scss,.sql,.ps1,.psm1,.psd1,.sh,.bash,.cmd,.bat,.lock,.in` plus extensionless `.gitignore,.gitattributes,.dockerignore,Dockerfile,Makefile,LICENSE,NOTICE`. The binary skip list is `.png,.jpg,.jpeg,.gif,.webp,.pdf,.ico,.zip,.gz,.7z,.exe,.dll,.pyd,.so,.woff,.woff2,.ttf,.mp3,.mp4,.sqlite,.db`; everything else fails. Stable remaining errors are `decode_failed`, `nul_unmarked`, `unsupported_file_type`, and `scan_failed`. Finding and error JSON property order remains source/path/rule or code/source/path and never includes value/content/OID.
- **Red:** complete `encodings_and_types`, `path_safety_and_errors`, and `redaction`; use the PowerShell AST parser to prove the top-level catch is constant and contains no exception/value/content interpolation. Run the unchanged contract and observe the first missing F-01S4 behavior.
- **Green/refactor:** implement only `Invoke-BootstrapScan` and final wiring. Require exactly `usage_and_output`, `provider_rule`, `direct_rules_and_order`, `artifact_direct_safety`, `assignment_quotes_boundaries`, `encodings_and_types`, `staged_vs_worktree`, `index_modes_and_rename`, `path_safety_and_errors`, `redaction`, then `BOOTSTRAP_SCANNER_CONTRACT_PASS`. In a fresh Git repository containing exact copies of only the two files, stage both and require exactly `CREDENTIAL_SCAN_PASS files=4`.
- **Done / commit:** the complete fail-closed scanner, exact ten-group contract, AST redaction proof, and tracked+staged self-scan pass with both reviews. Commit `build(F-01S4): close bootstrap scanner gate [agent: worker]`.

### F-01A: Reproducible runtimes, manifests, and reviewed locks

- **Dependencies / parallelism:** F-01S4; no, because every later task consumes the closed bootstrap scanner and these project-local runtime inputs.
- **Goal / files:** Create `.python-version`, `pyproject.toml`, `backend/requirements-windows-x64.lock`, `requirements.linux-ci.lock`, `packaging/oci/requirements.linux-demo.lock`, `frontend/package.json`, `frontend/package-lock.json`, `frontend/.npmrc`, `scripts/bootstrap.ps1`, and `scripts/tests/foundation_runtime_contract.ps1`. `docs/engineering/DEPENDENCY_BASELINE.md` is the sole artifact authority; the three files under `docs/engineering/locks/` are the sole lock authorities. Bootstrap downloads into ignored project-local storage, verifies bytes before extraction, blocks `npm.ps1`, and changes neither system PATH nor registry.
- **Pinned inputs:** Canonical-LF lock SHA-256 values are Windows `246083f8b210c3e33904f3057dfd48e7d8db548804d11fa5b087ecb291ad0fc6`, Linux CI `d24ddf3789ea9f276ee6ba4062634fef3c85c4572a7eb62096cbd570bfb0fc35`, Linux demo `09ce57726c02a090f134d4f2c25f2681dce58ebf2d8425502129d42ac2be34f7`, and npm `8b793ee9ca823ca1079efe12c4962a8786059b4aaf08bcb715264ad7b4718354`. The production npm identity is private `projectb@0.1.0`. The npm root map is dependencies `react@19.2.7`, `react-dom@19.2.7`, `lucide-react@1.25.0`; devDependencies `vite@8.1.5`, `@vitejs/plugin-react@6.0.3`, `typescript@7.0.2`, `vitest@4.1.10`, `@testing-library/dom@10.4.1`, `@testing-library/react@16.3.2`, `@testing-library/user-event@14.6.1`, `jsdom@29.1.1`, `@playwright/test@1.61.1`, `@axe-core/playwright@4.12.1`, `@types/react@19.2.17`, `@types/react-dom@19.2.3`, `@types/node@24.13.3`. The 2026-08-05 security refresh preserves this root dependency map and 166-package/license closure while updating transitive `postcss` to `8.5.25` and `undici` to `7.29.0`.
- **Red:** create the runtime contract and run `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/tests/foundation_runtime_contract.ps1`; expect missing artifact/hash, raw-lock parity, manifest, blocked-`npm.ps1`, corrupt-download, version-drift, and system-mutation failures.
- **Green/refactor:** implement only the listed runtime/manifest files, rerun the exact Red command, then use the returned `$Py` and `$Npm` to print exact versions and install only the hashed locks with scripts disabled.
- **Done / commit:** exact local Windows runtimes, manifests, four lock closures, corrupt-download negatives, and no system mutation pass. Commit `build(F-01A): materialize reviewed runtimes [agent: worker]`.

### F-01B: Byte-pinned bootstrap license closure

- **Dependencies / parallelism:** F-01A and `BOOTSTRAP-LICENSE-EVIDENCE`; no, because notices and later distribution consume these exact bytes.
- **Goal / files:** Create `scripts/tests/bootstrap_license_contract.ps1`, `licenses/bootstrap/uv-LICENSE-APACHE`, `licenses/bootstrap/uv-LICENSE-MIT`, `licenses/bootstrap/cpython-LICENSE`, `licenses/bootstrap/node-LICENSE`, and `licenses/bootstrap/npm-LICENSE`; serially modify `scripts/bootstrap.ps1`. `docs/engineering/BOOTSTRAP_LICENSE_EVIDENCE.md` at SHA-256 `FD65C5D2F8421F7B99AE4D540B80A8BBED1C28C78EF45851F7C6E5051034F310` is the sole license-byte authority; runtime artifact URLs/hashes remain solely in `DEPENDENCY_BASELINE.md`.
- **Red:** run `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/tests/bootstrap_license_contract.ps1`; expect missing five targets, wrong-byte/count/hash, mutable-ref, transport-fallback, and evidence-ledger-binding failures.
- **Green/refactor:** for each evidence row, fetch `https://api.github.com/repos/OWNER/REPO/contents/PATH?ref=40_HEX_COMMIT` with GitHub JSON accept headers, decode exactly the returned base64 once, and verify commit, byte count, blob ID, and SHA-256 before copying. The immutable raw commit URL recorded in the same row is allowed only as a fallback whose bytes pass the same checks; tag URLs and unverified transport output fail closed. Rerun the exact Red command and `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/verify_evidence.ps1`.
- **Done / commit:** five exact license files and all negative transport/byte checks pass without treating raw-download failure as evidence. Commit `build(F-01B): close bootstrap licenses [agent: worker]`.

### F-01C: Strict frontend foundation harness

- **Dependencies / parallelism:** F-01B; no, because CI seed consumes its deterministic commands.
- **Goal / files:** Create `frontend/tsconfig.json`, `frontend/vite.config.ts`, `frontend/src/foundation/RuntimeProbe.tsx`, `frontend/src/foundation/RuntimeProbe.test.tsx`, and `scripts/tests/frontend_foundation_contract.ps1`. `.npmrc` already requires `engine-strict`, `ignore-scripts`, `audit`, `fund=false`, `save-exact`, and lockfiles; TypeScript is strict with `noUncheckedIndexedAccess`; Vite/Vitest use JSDOM, `*.test.ts(x)`, React, and loopback ports 5173/4173.
- **Red:** run `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/tests/frontend_foundation_contract.ps1`; expect config, empty-suite, non-loopback, inaccessible-control, and missing interaction failures.
- **Green/refactor:** create only the listed frontend files, rerun the exact Red command, then `& $Npm --prefix frontend exec -- vitest run src/foundation/RuntimeProbe.test.tsx`; Testing Library/user-event must operate an accessible counter and an empty suite must fail.
- **Done / commit:** strict config and the real React interaction pass without `passWithNoTests`. Commit `test(F-01C): add frontend foundation harness [agent: worker]`.

### F-01D: Portable push-CI seed

- **Dependencies / parallelism:** F-01C; no, because every later branch must inherit working push CI before its first remote push.
- **Goal / files:** Create `.gitlab-ci.yml`, `.github/workflows/ci.yml`, and `scripts/tests/ci_seed_contract.ps1`. Both trigger on every push and reject an empty suite. GitLab job `unit-test` and the matching GitHub scanner job run `pwsh` in `mcr.microsoft.com/powershell:7.5-ubuntu-24.04@sha256:042240d57ec9e47e511033b92625a8d95875ee5860af3015992c248b58a8be81`, install Git before invoking the complete F-01S4 scanner contract, and record versions. Backend jobs use `python:3.14.6-slim-bookworm@sha256:f70215e5dbe2a47dee6d23f9c6d358bf3c148f59cce2fd165b61118e9d80f2bb`; frontend jobs use `node:24.18.0-bookworm-slim@sha256:d45d78e7929b46875bbd4e29bea672d5bc48186c6c3588306521c815e78352d6`. GitHub uses `ubuntu-24.04`, top-level `permissions: {contents: read}`, and `actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683` only.
- **Current-suite rule:** scanner and frontend foundation always run. Before F-01E, both `scripts/test_all.py` and `backend/projectb` are absent and the backend job records `runner_absent_pre_feature`, not a backend PASS; `backend/projectb` without the runner is fatal. From F-01E onward, absence or failure of `scripts/test_all.py --backend` is always fatal and its `scripts/tests` suite is nonempty even before feature modules exist. If later test paths exist, each ecosystem job must discover and execute them through the shared runner/direct locked command; no `rules:exists`, path filter, allow-failure, skipped required job, or empty suite may turn existing core tests green.
- **Red:** run `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/tests/ci_seed_contract.ps1`; expect missing push trigger, exact GitLab job, image digest, checkout SHA, least-permission, current-suite, locked install, and empty-suite failures.
- **Green/refactor:** create only the two CI files, rerun the exact Red command, then locally execute every CI seed command in the corresponding pinned image contract where Docker is available; otherwise keep container execution explicitly blocked and do not claim remote PASS.
- **Done / commit:** both configs are mechanically portable, execute all tests present at that branch tip, and contain no early-branch bypass. Commit `ci(F-01D): seed push test pipelines [agent: worker]`.

### F-01E: One-command runner, credential scanner, and license gates

- **Dependencies / parallelism:** F-01D; no, because every later task and seeded CI current-suite rule depend on these fail-closed quality commands.
- **Goal / files:** Create `scripts/test_all.py`, `scripts/scan_credentials.py`, `scripts/verify_licenses.py`, `scripts/tests/test_quality_gates.py`, `scripts/tests/fixtures/scanner/clean.txt`, `scripts/tests/fixtures/scanner/placeholder.env.example`, `scripts/tests/fixtures/scanner/binary.png`, and `licenses/THIRD_PARTY_NOTICES.md`; positive shapes are assembled only in test runtime. Retain the completed F-01S4 scanner as the runtime-free fallback and prove the Python scanner is a strict superset, including exact index blobs and separate index/worktree source reporting. The runner supports only `--all` (default), `--backend`, and `--frontend`; backend mode always includes the nonempty `scripts/tests` suite and adds every discovered `backend/tests` file, while frontend mode includes all Vitest tests plus the build. All modes run their applicable contracts, credential scan, and license verification with bounded children and propagated nonzero exits.
- **Red:** create `scripts/tests/test_quality_gates.py`; run `& $Py -m pytest scripts/tests/test_quality_gates.py -q`; expect missing runner/scanner/license-verifier, unsupported mode, empty-suite, CI current-suite, failure-propagation, redaction, notice, and exact-command assertions.
- **Green/refactor:** rerun the exact Red command, `& $Py scripts/scan_credentials.py --tracked --staged`, `& $Py scripts/verify_licenses.py`, the literal `python scripts/test_all.py` under the common bootstrap's process-local PATH, `& $Py scripts/test_all.py --backend`, `& $Py scripts/test_all.py --frontend`, both evidence verifiers, and the F-01D seed contract.
- **Done / commit:** one-command/mode orchestration, child failure propagation, credential redaction, full notices, evidence binding, and CI current-suite enforcement pass; no empty suite yields green. Commit `build(F-01E): add fail-closed quality gates [agent: worker]`.

**Coordinator verification update (2026-08-06):** Review regressions were repaired before closure. The Python scanner now captures tracked and staged Git enumerations once and derives findings/count from that snapshot; unsupported index modes emit `index_mode_unsupported`; the license verifier binds normalized Python license rows to baseline SHA-256 `7013e4d8dee96ab1c461bf7b093c35770cd371b5ea7462a77f050f8912f51beb`. Evidence: quality gates `21 passed`; scanner `CREDENTIAL_SCAN_PASS files=226`; license verifier `LICENSE_VERIFICATION_PASS python=54 npm=166`; `test_all.py --all` and `CI_SEED_CONTRACT_PASS` passed; `git diff --check` and Python compilation passed. Docker and remote CI remain unexecuted environment gates. The implementation terminal commit is `ae152e3`.

### F-02: Core metadata schema and unit of work

- **Dependencies / parallelism:** F-01E; no, because it creates migration 001 and the transaction base consumed by F-03.
- **Goal / files:** Create `backend/projectb/storage/db.py`, `backend/projectb/storage/migrations/001_core.sql`, `backend/projectb/repositories/uow.py`, and `backend/tests/storage/test_core_schema.py`. Own only Course, Material, MaterialVersion, MaterialBlobRef, SourceLocator, KnowledgeConcept, CoverageDecision, ProviderProfile, ConsentRecord, and AuditEvent schema, foreign keys, uniqueness, migration idempotency, reference-safe blob deletion, and transaction boundaries.
- **Red:** `& $Py -m pytest backend/tests/storage/test_core_schema.py -q`; expect absent schema/migration and rollback behavior.
- **Green/refactor:** rerun the exact Red command, then run `BE-REGRESSION` and `LICENSE-SECURITY-GATE`.
- **Done / commit:** a fresh and an already-migrated database are deterministic; rollback leaves no partial row; schema fields match SPEC section 7. Commit `feat(F-02): add core sqlite schema [agent: worker]`.

### F-03: Learning and review schema constraints

- **Dependencies / parallelism:** F-02; no, because migration 002 is ordered after the reviewed core schema.
- **Goal / files:** Create `storage/migrations/002_learning.sql` and `backend/tests/storage/test_learning_schema.py` for Attempt, LearningEvidence, MasteryEstimate, ReviewPlanRevision, and ReviewTask. Enforce append-only evidence, idempotency keys, parent revisions, completed-task protection, and cascade/restrict rules.
- **Red:** `& $Py -m pytest backend/tests/storage/test_learning_schema.py -q`; expect missing tables/triggers and mutable-evidence rejection failure.
- **Green/refactor:** rerun the exact Red command, then run `BE-REGRESSION` and `LICENSE-SECURITY-GATE`.
- **Done / commit:** all SPEC entities and deletion rules are mechanically tested without feature repositories. Commit `feat(F-03): add learning sqlite constraints [agent: worker]`.

### F-04: HTTP trust, session-bound CSRF, safe errors, and audit whitelist

- **Dependencies / parallelism:** F-03; no, because later credentials and APIs consume this single trust/audit contract.
- **Goal / files:** Create `backend/projectb/security/http.py`, `backend/projectb/observability/audit.py`, `backend/tests/security/test_http_boundary.py`, and `backend/tests/security/test_audit_redaction.py`. Local policy permits loopback Host/Origin only; unsafe methods require a session-bound CSRF token; valid tokens replayed in another session fail; errors/logs expose no bodies, paths, answers, fragments, or secrets.
- **Red:** `& $Py -m pytest backend/tests/security/test_http_boundary.py backend/tests/security/test_audit_redaction.py -q`; expect Host/Origin/CSRF/replay and redaction failures.
- **Green/refactor:** rerun the exact Red command, then run `BE-REGRESSION` and `LICENSE-SECURITY-GATE`.
- **Done / commit:** positive and negative trust tests, cross-session replay, request IDs, error codes, and audit field whitelist pass. Commit `feat(F-04): enforce local http trust boundary [agent: worker]`.

### F-05: Windows Credential Manager lifecycle

- **Dependencies / parallelism:** F-04; no, because the credential service must use the reviewed audit/redaction boundary.
- **Goal / files:** Create `backend/projectb/security/credentials.py` and `backend/tests/security/test_credentials.py`. Provide status/update/clear without plaintext reads; use WinVault for local profile; expose an unconfigured first-run state. A Windows integration test uses a random disposable target and always deletes it in `finally`; non-Windows CI uses a deterministic fake and never claims WinVault verification.
- **Red:** `& $Py -m pytest backend/tests/security/test_credentials.py -q`; expect missing value-free lifecycle and cleanup behavior.
- **Green/refactor:** rerun the exact Red command, run `BE-REGRESSION` and `LICENSE-SECURITY-GATE`, then on Windows run `& $Py -m pytest backend/tests/security/test_credentials.py -q -m windows`.
- **Done / commit:** set/status/update/clear and guaranteed cleanup pass; SQLite/config/log/browser responses contain no secret. Commit `feat(F-05): add winvault credential lifecycle [agent: worker]`.

## 6. M1 Material Tasks

### M1-01: Material primitives and deterministic extraction

- **Dependencies / parallelism:** F-05; no, because it establishes the sole Material/SourceLocator extraction contract.
- **Goal / files:** Create `backend/projectb/domain/materials/models.py`, `backend/projectb/services/materials/extract_text.py`, `backend/tests/materials/test_text_extraction.py`, `backend/tests/materials/test_pdf_extraction.py`, `backend/tests/fixtures/materials/digital.pdf`, `backend/tests/fixtures/materials/scanned.pdf`, `backend/tests/fixtures/materials/notes.txt`, `backend/tests/fixtures/materials/notes.md`, and `backend/tests/fixtures/materials/LICENSES.md`. Hash original bytes before decoding. UTF-8 TXT/MD yields stable one-based line locators. For digital PDF, pypdfium2 validates readability/page count and pypdf extracts per-page text; disagreement, encryption, zero usable text, and scanned PDFs fail before persistence. Parsing runs in a terminable worker with a 30-second per-file deadline; timeout kills the process tree, deletes temporary output, and returns a stable retryable error. Parser ID/version/extraction-contract is immutable `MaterialVersion` metadata; a parser change creates a new version and cannot rewrite an old locator.
- **Red:** `& $Py -m pytest backend/tests/materials/test_text_extraction.py backend/tests/materials/test_pdf_extraction.py -q`; expect hash/locator/golden/scanned-PDF failures plus deterministic timeout, process termination, temporary cleanup, and parser-upgrade immutability failures.
- **Green/refactor:** rerun the exact Red command, then run `BE-REGRESSION` and `LICENSE-SECURITY-GATE`.
- **Done / commit:** raw hash, immutable parser/version fingerprint, new-version-on-upgrade, page/line bounds, magic/type checks, 30-second retryable timeout cleanup, and deterministic golden fixtures pass. Commit `feat(M1-01): extract source-located materials [agent: worker]`.

### M1-02: Atomic incremental import and content store

- **Dependencies / parallelism:** M1-01; no, because import consumes the reviewed byte hash and locator output.
- **Goal / files:** Create `backend/projectb/services/materials/importer.py`, `backend/projectb/repositories/materials.py`, `backend/projectb/storage/content_store.py`, and `backend/tests/materials/test_importer.py`. Preflight at most 5 files and 50 MiB total before any authoritative write; each file is at most 20 MiB, each PDF at most 200 pages, and decoded TXT/Markdown at most 1,000,000 Unicode code points. Preserve successful siblings, roll back a failed/timed-out file and temporary bytes, deduplicate same-course hashes, create a new version for same-hash/new-parser, and share cross-course blobs through transactional refs.
- **Red:** `& $Py -m pytest backend/tests/materials/test_importer.py -q`; expect atomicity, same-hash/same-parser idempotency, same-hash/new-parser versioning, same-hash/two-course blob sharing, mixed-batch timeout, and `limit-1 / limit / limit+1` failures for all limits.
- **Green/refactor:** rerun the exact Red command, then run `BE-REGRESSION` and `LICENSE-SECURITY-GATE`.
- **Done / commit:** exact SPEC limits and preflight ordering pass; no half-written Material/content/temp bytes survive failure or timeout; same input is idempotent; mixed batch outcomes are recoverable. Commit `feat(M1-02): import materials atomically [agent: worker]`.

### M1-03: Concepts, confirmed coverage, and deletion

- **Dependencies / parallelism:** M1-02; no, because coverage and deletion consume the reviewed material repository.
- **Goal / files:** Create `backend/projectb/repositories/coverage.py`, `backend/projectb/services/materials/coverage.py`, `backend/projectb/services/materials/delete.py`, and `backend/tests/materials/test_coverage.py`. Mapping is append-only confirmed/rejected history; only confirmed current-version locators authorize learning. Delete removes the course ref and invalidates future use without deleting historical evidence; shared blob bytes remain until the last cross-course ref is gone, and failed final-byte deletion leaves a retryable tombstone.
- **Red:** `& $Py -m pytest backend/tests/materials/test_coverage.py -q`; expect unconfirmed/stale-version locator authorization, one-of-two-course deletion preservation, last-ref deletion, and retryable tombstone failures.
- **Green/refactor:** rerun the exact Red command, then run `BE-REGRESSION` and `LICENSE-SECURITY-GATE`.
- **Done / commit:** multiple concepts, explicit confirmation, stale-source fail-close, and deletion semantics satisfy AC-03/04. Commit `feat(M1-03): bind concepts to confirmed sources [agent: worker]`.

## 7. M2 Learning Tasks

### M2-01: Evaluator contract and mutex rubric

- **Dependencies / parallelism:** M1-03; no, because evaluator authority requires current confirmed coverage.
- **Goal / files:** Create `backend/projectb/domain/learning/evaluators/base.py`, `backend/projectb/domain/learning/evaluators/mutex.py`, `backend/projectb/domain/learning/evaluators/registry.py`, `backend/projectb/domain/learning/evaluators/schemas.py`, and `backend/tests/learning/test_mutex_evaluator.py`. Rubrics are versioned, deterministic, source-bound, and return structured outcomes; concepts without an evaluator are explanation-only and cannot create mastery evidence.
- **Red:** `& $Py -m pytest backend/tests/learning/test_mutex_evaluator.py -q`; expect missing golden/negative determinism and explanation-only guard.
- **Green/refactor:** rerun the exact Red command, then run `BE-REGRESSION` and `LICENSE-SECURITY-GATE`.
- **Done / commit:** mutex evaluator and registry base pass repeated/shuffled fixture tests. Commit `feat(M2-01): add deterministic mutex evaluator [agent: worker]`.

### M2-02: Race and deadlock rubrics plus registry assembly

- **Dependencies / parallelism:** M2-01; no, because this task is the only serialized modifier of the evaluator registry.
- **Goal / files:** Create `backend/projectb/domain/learning/evaluators/race.py`, `backend/projectb/domain/learning/evaluators/deadlock.py`, `backend/tests/learning/test_race_evaluator.py`, and `backend/tests/learning/test_deadlock_evaluator.py`; serially update `backend/projectb/domain/learning/evaluators/registry.py`. Race checks shared access/concurrency/order; deadlock checks resources/hold-wait/cycle/progress. Each test constructs golden, near-miss, invalid, and stable-order cases in code.
- **Red:** `& $Py -m pytest backend/tests/learning/test_race_evaluator.py backend/tests/learning/test_deadlock_evaluator.py -q`; expect both evaluator and three-ID registry assertions to fail.
- **Green/refactor:** rerun the exact Red command, then run `BE-REGRESSION` and `LICENSE-SECURITY-GATE`.
- **Done / commit:** mutex/race/deadlock are mutually registered, deterministic, and versioned; no LLM participates in grading. Commit `feat(M2-02): add concurrency evaluator set [agent: worker]`.

### M2-03: Attempts and append-only learning evidence

- **Dependencies / parallelism:** M2-02; no, because evidence records the terminal evaluator ID/version registry.
- **Goal / files:** Create `services/learning/attempts.py`, `repositories/evidence.py`, and `backend/tests/learning/test_evidence.py`. Validate structured local answers, current source coverage, evaluator ID/version, and idempotency key before appending one immutable LearningEvidence row; student answer text never enters provider/audit logs.
- **Red:** `& $Py -m pytest backend/tests/learning/test_evidence.py -q`; expect duplicate, mutation, stale-source, and answer-leak failures.
- **Green/refactor:** rerun the exact Red command, then run `BE-REGRESSION` and `LICENSE-SECURITY-GATE`.
- **Done / commit:** duplicate attempt keys yield one evidence row and stable response; provider failure cannot alter evidence. Commit `feat(M2-03): append immutable learning evidence [agent: worker]`.

### M2-04: Deterministic mastery derivation

- **Dependencies / parallelism:** M2-03; no, because mastery consumes the complete append-only evidence history.
- **Goal / files:** Create `services/learning/mastery.py`, `repositories/mastery.py`, and `backend/tests/learning/test_mastery.py`. Derive only from complete evidence history with stable input hash, UTC storage, course-local day boundaries, demonstrated/retained timing rules, and no manual/provider override.
- **Red:** `& $Py -m pytest backend/tests/learning/test_mastery.py -q`; expect ordering, timezone, incomplete-history, and override failures.
- **Green/refactor:** rerun the exact Red command, then run `BE-REGRESSION` and `LICENSE-SECURITY-GATE`.
- **Done / commit:** repeated/shuffled complete inputs produce the same state/hash; omitted history fails closed. Commit `feat(M2-04): derive mastery from evidence [agent: worker]`.

## 8. Provider, M3, and API Tasks

### P-01: Provider-neutral port, exact consent, profiles, and mock

- **Dependencies / parallelism:** M2-04; no, because the provider candidate boundary must be unable to mutate reviewed authority state.
- **Goal / files:** Create `backend/projectb/providers/port.py`, `backend/projectb/providers/mock.py`, `backend/projectb/providers/registry.py`, `backend/projectb/repositories/provider_profiles.py`, `backend/projectb/services/providers/consent.py`, `backend/tests/providers/test_consent.py`, and `backend/tests/providers/test_mock.py`. Define exactly `generate_explanation`, `generate_practice_candidate`, and `generate_feedback_wording`; every candidate is non-authoritative. Feedback input accepts only deterministic rubric output plus confirmed current-version sources and rejects the original answer. The local registry defaults to L with no adapter; mock is injected only in tests/demo. Immutable consent binds port, exact locator/version/hash/fragment preview, profile, policy fingerprint, token/cost caps, and nonce; no match means zero network calls.
- **Red:** `& $Py -m pytest backend/tests/providers/test_consent.py backend/tests/providers/test_mock.py -q`; expect three-port schema, feedback-answer exclusion, consent mismatch/reuse/stale-source/network-count, local-no-provider, and local-rejects-mock failures.
- **Green/refactor:** rerun the exact Red command, then run `BE-REGRESSION` and `LICENSE-SECURITY-GATE`.
- **Done / commit:** all three ports and their least-data input contracts pass; L performs zero calls, local rejects mock, test/demo injection covers success/schema/timeout/error deterministically, and provider candidates cannot write coverage/evidence/mastery/plan. Commit `feat(P-01): add consent-bound provider port [agent: worker]`.

### M3-01: Pure continuous and finals planner

- **Dependencies / parallelism:** P-01; no, because the serial worktree freezes authority/provider ports before planning.
- **Goal / files:** Create `backend/projectb/domain/review/planner.py` and `backend/tests/review/test_planner.py`. Implement ReviewPolicy v1 as a pure function: IANA timezone; budget 10--120 by 5, default 30; fixed 10-minute tasks; base intervals `[1,3,7,14,30]`; stable priority weakness/date/concept ID. Continuous uses base intervals for 30 local days. Finals requires an exam date and applies mastery multipliers with integer ceiling: unknown `1/2 -> [1,2,4,7,15]`, demonstrated_now `3/4 -> [1,3,6,11,23]`, retained `1 -> base`; duplicate same-day concept tasks collapse to the weakest evidence, post-exam tasks drop, and past exam yields archived zero tasks. Stale sources and system errors are excluded, not treated as learning failures.
- **Red:** `& $Py -m pytest backend/tests/review/test_planner.py -q`; expect table-driven mode/timezone/default/step/range, budget, all three exact interval tables, duplicate collapse, tie-break, error-neutrality, horizon, cutoff/past-date archive, stale-source, and repeat-hash failures.
- **Green/refactor:** rerun the exact Red command, then run `BE-REGRESSION` and `LICENSE-SECURITY-GATE`.
- **Done / commit:** every ReviewPolicy v1 rule passes boundary tables; identical normalized inputs yield the same input hash, task order, and archive state in both modes. Commit `feat(M3-01): plan deterministic reviews [agent: worker]`.

### M3-02: Review revisions, diff, and recovery

- **Dependencies / parallelism:** M3-01; no, because revision persistence consumes the reviewed pure planner output.
- **Goal / files:** Create `services/review/revisions.py`, `repositories/review_plans.py`, and `backend/tests/review/test_revisions.py`. Append revisions only when normalized `plan_input_hash` changes for evidence/coverage/budget/exam inputs; equal hashes return the existing revision. Produce stable diffs, preserve completed tasks, permit unstarted-task recovery, and remove stale-source future tasks.
- **Red:** `& $Py -m pytest backend/tests/review/test_revisions.py -q`; expect equal-hash duplicate-revision, mutation, diff, completed-task, recovery, and stale-source failures.
- **Green/refactor:** rerun the exact Red command, then run `BE-REGRESSION` and `LICENSE-SECURITY-GATE`.
- **Done / commit:** equal input hash creates no revision; changed hashes produce deterministic parent links/diffs; recovery never rewrites completed history. Commit `feat(M3-02): persist review revisions [agent: worker]`.

### API-01: App factory, course/material APIs, and static assembly contract

- **Dependencies / parallelism:** M3-02; no, because it creates the sole app and API route registries.
- **Goal / files:** Create `api/app.py`, `api/routes/courses.py`, `api/routes/materials.py`, `api/static.py`, `repositories/courses.py`, and `backend/tests/api/test_material_routes.py`. Integrate F-04 middleware; implement course/import/result/source/mapping/delete APIs; static serving is confined to a configured build directory and never serves user data.
- **Red:** `& $Py -m pytest backend/tests/api/test_material_routes.py -q`; expect 404s, missing trust middleware, and path-traversal rejection.
- **Green/refactor:** rerun the exact Red command, then run `BE-REGRESSION` and `LICENSE-SECURITY-GATE`.
- **Done / commit:** M1 routes, error codes, request IDs, multipart limits, and static boundary pass. Commit `feat(API-01): assemble material api [agent: worker]`.

### API-02: Learning, evidence, mastery, consent, and mock-provider APIs

- **Dependencies / parallelism:** API-01; no, because it serially modifies `api/app.py` and its route registry.
- **Goal / files:** Create `api/routes/learning.py`, `api/routes/providers.py`, serially update `api/app.py`, and add `backend/tests/api/test_learning_routes.py`. Expose source-bound explanation/practice/feedback-wording candidates, deterministic evaluate/evidence/mastery, and preview/consent/provider calls. Local production defaults to L and has no mock route/registration; tests may inject mock through the P-01 test seam. Feedback forwards rubric plus confirmed source only, never the original answer; no provider candidate may write authority state.
- **Red:** `& $Py -m pytest backend/tests/api/test_learning_routes.py -q`; expect 404, three-port contract, raw-answer outbound rejection, local-mock rejection, stale-source, consent, idempotency, and authority failures.
- **Green/refactor:** rerun the exact Red command, then run `BE-REGRESSION` and `LICENSE-SECURITY-GATE`.
- **Done / commit:** M2 and all three P-01 ports are reachable through the app factory; L has no adapter and zero network, local rejects mock, and test injection remains non-authoritative. Commit `feat(API-02): assemble learning api [agent: worker]`.

### API-03: Review, credential, settings, and final local profile

- **Dependencies / parallelism:** API-02; no, because it closes the same app registry and publishes the local profile interface.
- **Goal / files:** Create `backend/projectb/api/routes/review.py`, `backend/projectb/api/routes/credentials.py`, `backend/projectb/api/routes/settings.py`, `backend/projectb/profiles/local.py`, `backend/projectb/profiles/registry.py`, `backend/tests/api/test_review_settings_routes.py`, and `backend/tests/system/test_performance.py`; serially update `backend/projectb/api/app.py`. Credential responses are value-free; first run is unconfigured; local bind is `127.0.0.1`; cached non-import API p95 is under 500 ms on the recorded fixture/reference host.
- **Red:** `& $Py -m pytest backend/tests/api/test_review_settings_routes.py backend/tests/system/test_performance.py -q`; expect 404, secret-shape, first-run, revision, and p95 failures.
- **Green/refactor:** rerun the exact Red command, then run `BE-REGRESSION` and `LICENSE-SECURITY-GATE`.
- **Done / commit:** complete local API assembly, settings validation, credential lifecycle, planner revisions, and measured performance pass. Commit `feat(API-03): close local api profile [agent: worker]`.

## 9. WebUI Tasks

UI tasks own one view and its CSS module/test/E2E file. `frontend/src/app/routes.tsx` is a serialized handoff UI-01 -> UI-06. Every task introduces its own responsive/keyboard/axe red; there is no later fabricated visual failure.

### UI-01: Open Design run, tokens, shell, client, and browser harness

- **Dependencies / parallelism:** API-03; no, because it creates the only frontend route registry and browser harness.
- **Goal / files:** Use the real Open Design project/run with `frontend-design` and `default`/Neutral Modern; record in `docs/engineering/OPEN_DESIGN_RUN.md` the project ID, run ID, Open Design agent/version, skill ID, design-system ID, artifact path and SHA-256, 360/768/1440 screenshot paths and SHA-256 values, every asset/source/license, review findings, and remediation. Create `frontend/src/styles/tokens.css`, `frontend/src/styles/global.css`, `frontend/src/app/App.tsx`, `frontend/src/app/routes.tsx`, `frontend/src/app/Shell.test.tsx`, `frontend/src/api/client.ts`, `frontend/src/api/capabilities.ts`, `frontend/playwright.config.ts`, `frontend/e2e/support/testServer.ts`, and `frontend/e2e/shell.spec.ts`. Generated design is evidence only until the red test runs.
- **Red:** `& $Npm --prefix frontend exec -- vitest run src/app/Shell.test.tsx` and `& $Npm --prefix frontend exec -- playwright test e2e/shell.spec.ts`; expect missing four-stage navigation, 360/768/1440 layout, keyboard, and axe assertions.
- **Green/refactor:** run `& $Npm --prefix frontend exec -- playwright install chromium`, rerun both exact Red commands, then run `FE-REGRESSION` and `LICENSE-SECURITY-GATE`.
- **Done / commit:** the complete Open Design receipt above is hash-bound, all Critical/Major design findings are closed, and the compact workbench shell has no hero/nested cards/overflow, radius <=8 px and letter spacing 0. Commit `feat(UI-01): build opendesign workbench shell [agent: worker]`.

### UI-02: Import view

- **Dependencies / parallelism:** UI-01; no, because it serially registers `/import` in `routes.tsx`.
- **Goal / files:** Create `frontend/src/views/import/ImportView.tsx`, `frontend/src/views/import/ImportView.module.css`, `frontend/src/views/import/ImportView.test.tsx`, and `frontend/e2e/import.spec.ts`; serially update `frontend/src/app/routes.tsx` for `/import`. Show limits, selected files, progress/result, errors, and material list; use icon tooltips.
- **Red:** run `& $Npm --prefix frontend exec -- vitest run src/views/import/ImportView.test.tsx` and `& $Npm --prefix frontend exec -- playwright test e2e/import.spec.ts`; expect upload/results/responsive/keyboard/axe failures.
- **Green/refactor:** rerun both exact Red commands, then run `FE-REGRESSION` and `LICENSE-SECURITY-GATE`.
- **Done / commit:** AC-01 import flow works at all three viewports without hiding failures. Commit `feat(UI-02): add material import view [agent: worker]`.

### UI-03: Mapping and source inspection view

- **Dependencies / parallelism:** UI-02; no, because it serially registers `/mapping` in `routes.tsx`.
- **Goal / files:** Create `frontend/src/views/mapping/MappingView.tsx`, `frontend/src/views/mapping/MappingView.module.css`, `frontend/src/views/mapping/MappingView.test.tsx`, and `frontend/e2e/mapping.spec.ts`; serially update `frontend/src/app/routes.tsx` for `/mapping`. Present source fragments, locators, concepts, confirm/reject, stale markers, and delete confirmation.
- **Red:** run `& $Npm --prefix frontend exec -- vitest run src/views/mapping/MappingView.test.tsx` and `& $Npm --prefix frontend exec -- playwright test e2e/mapping.spec.ts`; expect source/confirmation/stale/delete/responsive/keyboard/axe failures.
- **Green/refactor:** rerun both exact Red commands, then run `FE-REGRESSION` and `LICENSE-SECURITY-GATE`.
- **Done / commit:** unconfirmed mappings are visibly non-authoritative; source and destructive actions remain inspectable. Commit `feat(UI-03): add source mapping view [agent: worker]`.

### UI-04: Source-bound learning and consent view

- **Dependencies / parallelism:** UI-03; no, because it serially registers `/learning` in `routes.tsx`.
- **Goal / files:** Create `frontend/src/views/learning/LearningView.tsx`, `frontend/src/views/learning/LearningView.module.css`, `frontend/src/views/learning/LearningView.test.tsx`, and `frontend/e2e/learning.spec.ts`; serially update `frontend/src/app/routes.tsx` for `/learning`. Show sources, explanation, practice, deterministic rubric/evidence, explanation-only state, feedback wording, provider labels, exact P preview/caps/confirmation, and original-answer exclusion.
- **Red:** run `& $Npm --prefix frontend exec -- vitest run src/views/learning/LearningView.test.tsx` and `& $Npm --prefix frontend exec -- playwright test e2e/learning.spec.ts`; expect source/rubric/feedback-answer-exclusion/consent/no-authority/responsive/keyboard/axe failures.
- **Green/refactor:** rerun both exact Red commands, then run `FE-REGRESSION` and `LICENSE-SECURITY-GATE`.
- **Done / commit:** model content is identifiable and cannot appear as grading/mastery; no consent means no call. Commit `feat(UI-04): add grounded learning view [agent: worker]`.

### UI-05: Review planner and revision diff view

- **Dependencies / parallelism:** UI-04; no, because it serially registers `/review` in `routes.tsx`.
- **Goal / files:** Create `frontend/src/views/review/ReviewView.tsx`, `frontend/src/views/review/ReviewView.module.css`, `frontend/src/views/review/ReviewView.test.tsx`, and `frontend/e2e/review.spec.ts`; serially update `frontend/src/app/routes.tsx` for `/review`. Show budget, sources, mastery, continuous/finals controls and compression, cutoff, revision diff, completion, and recovery.
- **Red:** run `& $Npm --prefix frontend exec -- vitest run src/views/review/ReviewView.test.tsx` and `& $Npm --prefix frontend exec -- playwright test e2e/review.spec.ts`; expect budget/mode/diff/recovery/responsive/keyboard/axe failures.
- **Green/refactor:** rerun both exact Red commands, then run `FE-REGRESSION` and `LICENSE-SECURITY-GATE`.
- **Done / commit:** deterministic plan/revision behavior is visible without rewriting completed tasks. Commit `feat(UI-05): add review planning view [agent: worker]`.

### UI-06: Settings, first-run credential guidance, privacy, and deletion

- **Dependencies / parallelism:** UI-05; no, because it serially registers `/settings` and freezes the route registry.
- **Goal / files:** Create `frontend/src/views/settings/SettingsView.tsx`, `frontend/src/views/settings/SettingsView.module.css`, `frontend/src/views/settings/SettingsView.test.tsx`, and `frontend/e2e/settings.spec.ts`; serially update `frontend/src/app/routes.tsx` for `/settings`. First-run guidance uses hidden password input; status/update/clear never echo; show privacy/profile/caps/data/security/deletion/demo restrictions.
- **Red:** run `& $Npm --prefix frontend exec -- vitest run src/views/settings/SettingsView.test.tsx` and `& $Npm --prefix frontend exec -- playwright test e2e/settings.spec.ts`; expect hidden-input/no-echo/status/delete/responsive/keyboard/axe failures.
- **Green/refactor:** rerun both exact Red commands, then run `FE-REGRESSION` and `LICENSE-SECURITY-GATE`.
- **Done / commit:** first-run credential path and privacy/security controls satisfy AC-14/16 without visible instructional feature copy. Commit `feat(UI-06): add secure settings view [agent: worker]`.

## 10. Demo, Provider Adapter, Distribution, CI, and Docs

### DEMO-01: Mock-only public demo profile

- **Dependencies / parallelism:** UI-06; no, because it is the only profile-registry modifier after local assembly.
- **Goal / files:** Create `backend/projectb/profiles/demo.py`, `backend/projectb/demo/fixtures.manifest.json`, `backend/projectb/demo/course.json`, `backend/projectb/demo/materials.md`, `backend/tests/demo/test_demo_profile.py`, `backend/tests/demo/test_demo_security.py`, and `frontend/e2e/demo.spec.ts`; serially update `backend/projectb/profiles/registry.py`, `backend/projectb/api/app.py`, `backend/projectb/api/routes/settings.py`, `frontend/src/app/App.tsx`, `frontend/src/app/Shell.test.tsx`, `frontend/src/views/import/ImportView.tsx`, `frontend/src/views/import/ImportView.test.tsx`, `frontend/src/views/learning/LearningView.tsx`, `frontend/src/views/learning/LearningView.test.tsx`, `frontend/src/views/settings/SettingsView.tsx`, and `frontend/src/views/settings/SettingsView.test.tsx`; update `frontend/playwright.config.ts` or a task-owned demo server helper only if required to boot the real assembly. `create_app` must keep local defaults unchanged while accepting a profile-owned HTTP policy, cookie contract, route-capability set, and validated published settings state. Host/Origin/forwarding preflight must run before any session allocation or fixture seed; rejected requests cannot create or refresh sessions. Demo assembly removes upload, credential, and provider routes and every frontend capability that could select/transmit files or solicit provider use. Session cleanup must run independently of later traffic, retain active leases, and retry deletion failures instead of forgetting state. The Python process guard must deny connection, address-resolution, datagram, and post-bootstrap subprocess paths; DIST-02 separately proves container-level egress denial. `demo.spec.ts` must boot and exercise the real `create_demo_app` assembly rather than replace its API with route stubs. Fixtures are synthetic CC0 and <=20; SQLite is ephemeral; sessions expire at 30-minute idle/two-hour absolute; upload/credential/OpenAI/cross-session state are absent.
- **Trust contract:** local Docker smoke requires `PROJECTB_DEMO_LOCAL_SMOKE=1` and permits only `http://127.0.0.1:7860`; public mode refuses startup without one exact HTTPS `PROJECTB_PUBLIC_ORIGIN`, derives Host/Origin allowlists without wildcards, uses HttpOnly/SameSite=Lax/Secure cookies, session-bound CSRF, and rejects forwarded headers unless D-025 supplies an exact trusted-proxy boundary.
- **Red:** `& $Py -m pytest backend/tests/demo -q` and `& $Npm --prefix frontend exec -- playwright test e2e/demo.spec.ts`; expect forbidden-route, egress, TTL, cross-session, public-origin, and fixture-license failures.
- **Green/refactor:** rerun both exact Red commands, then run `BE-REGRESSION`, `FE-REGRESSION`, and `LICENSE-SECURITY-GATE`.
- **Done / commit:** same UI/domain contracts run on licensed synthetic data; forbidden capabilities are absent, not merely hidden. Commit `feat(DEMO-01): add isolated mock demo [agent: worker]`.

### P-02: P-only OpenAI adapter from the reviewed policy snapshot

- **Dependencies / parallelism:** DEMO-01, P-01, and P-EVIDENCE; no, because it is isolated after the mock-complete core and is the only production-adapter registry modifier.
- **Goal / files:** Consume read-only `docs/engineering/PROVIDER_POLICY_V1_P_EVIDENCE.md` and `scripts/verify_provider_policy_v1.ps1`; create `backend/projectb/providers/openai_adapter.py`, `backend/projectb/providers/policy.v1.json`, and `backend/tests/providers/test_openai_adapter.py`; serially update `backend/projectb/providers/port.py`, `backend/projectb/providers/registry.py`, `backend/projectb/services/providers/consent.py`, `backend/projectb/security/credentials.py`, `backend/projectb/profiles/local.py`, `backend/projectb/api/app.py`, `backend/projectb/api/routes/credentials.py`, `backend/projectb/api/routes/providers.py`, `backend/projectb/api/routes/settings.py`, `backend/tests/providers/test_consent.py`, `backend/tests/api/test_learning_routes.py`, `backend/tests/api/test_review_settings_routes.py`, `frontend/src/api/client.ts`, `frontend/src/views/learning/LearningView.tsx`, `frontend/src/views/learning/LearningView.test.tsx`, `frontend/src/views/settings/SettingsView.tsx`, `frontend/src/views/settings/SettingsView.test.tsx`, `frontend/e2e/learning.spec.ts`, and `frontend/e2e/settings.spec.ts`. This expansion is required to make explicit local P enablement, immutable server-derived cost/cap/profile consent, credential-safe assembly, fail-closed policy drift, and the exact source-bound UI preview executable rather than adapter-only dead code. Evidence SHA-256 is `35a3f46e036563e3fc681df3190eb56336ab48b9d9817ad48f4d5df42230f076`, P-only and time-bounded. Mock HTTP transport tests, not real keys or paid calls, prove request/response behavior.
- **Contract:** local production remains in L with no selected provider until the user explicitly enables P; its registry permits only the built-in OpenAI adapter with a fresh policy, configured credential status, allowlisted model, and explicit input/output caps. Deterministic provider mock remains absent from local and registered only by test/demo profiles. Consent displays the computed maximum cost. Adapter sends only confirmed extracted fragments through Responses API with `store:false`, 60-second timeout, zero automatic retries, strict output schema, no student answer, and no network when snapshot is absent/stale or consent mismatches.
- **Red:** first require `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/verify_provider_policy_v1.ps1` to pass; then run `& $Py -m pytest backend/tests/providers/test_openai_adapter.py -q`; expect missing adapter/derived policy/registry update plus local-rejects-mock, unconfigured-L, stale-fixture, forbidden-field, schema, timeout, and zero-network failures.
- **Green/refactor:** if and only if evidence expired, return to the coordinator for an official-source refresh; otherwise rerun the verifier and exact Red test, then run `BE-REGRESSION` and `LICENSE-SECURITY-GATE`.
- **Done / commit:** P-only evidence and adapter are hash-bound; no F/direct-file behavior leaks into v1. Full local gates and system-Chrome E2E pass; coordinator quality review found and closed WinVault status-read and concurrent enable/disable consistency defects. Commit `feat(P-02): add governed openai p adapter [agent: worker]` at `8e6b23f`.

### QA-RELEASE: Verification-only gate

This is not a dispatch task and owns no file. From a clean worktree, run the common bootstrap, `& $Npm --prefix frontend exec -- playwright install chromium`, `BE-REGRESSION`, `FE-REGRESSION`, `& $Npm --prefix frontend exec -- playwright test`, `LICENSE-SECURITY-GATE`, `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/verify_evidence.ps1`, `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/verify_linux_dependency_evidence.ps1`, and `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/verify_provider_policy_v1.ps1`. Playwright config runs 360/768/1440 projects. Any failure returns to the owning task with a defect-specific red test. QA-RELEASE may not repair feature behavior itself.

### DIST-01: Windows x64 single-file distribution

- **Dependencies / parallelism:** P-02 and QA-RELEASE; no, because it freezes the complete local application resources.
- **Goal / files:** Create `packaging/windows/build.ps1`, `packaging/windows/ProjectB.spec`, `packaging/windows/launcher.py`, `packaging/windows/hooks/hook-keyring.py`, `packaging/windows/hooks/hook-pypdfium2.py`, `packaging/windows/smoke_test.ps1`, `backend/tests/distribution/test_windows_contract.py`, and `docs/engineering/DIST-01_EVIDENCE.md`; serially modify `.github/workflows/ci.yml`, `scripts/tests/ci_seed_contract.ps1`, and the worktree-aware npm resolver in `scripts/test_all.py`. Build one `ProjectB.exe`; mutable data stays under `%LOCALAPPDATA%\ProjectB` or explicit data root; bind loopback only; embed WebUI and notices. Add a required push-triggered `windows-package` job on `windows-2025` that runs the same reviewed build/contract, scans the runner-local artifact with the canonical binary-safe scanner, and prints its SHA-256; no upload action or remote publication occurs. The job exists in the distribution branch before its first push.
- **Red:** `& $Py -m pytest backend/tests/distribution/test_windows_contract.py -q`; expect missing single-file/resource/data-root/bind/startup/WinVault/push-CI Windows artifact assertions. Then rerun the F-01D seed contract and require its new `windows-package` assertion to fail before the workflow edit.
- **Green/refactor:** rerun the exact Red command; run `powershell -NoProfile -ExecutionPolicy Bypass -File packaging/windows/build.ps1 -Python $Py -Output dist/ProjectB.exe`, scan index/worktree, and run `powershell -NoProfile -ExecutionPolicy Bypass -File packaging/windows/smoke_test.ps1 -Artifact dist/ProjectB.exe -DataRoot tmp/dist01-smoke` on the development host.
- **Done / commit:** local artifact hash, resource/data-root/bind behavior, no-secret scan, development-host smoke (including a data root containing spaces), and push-triggered Windows build contract are recorded. Commit `662a381` (`build(DIST-01): package windows single file [agent: coordinator]`). Clean-host startup/WinVault evidence is owned separately by `DIST-01-VM-CLOSE`.

### DIST-02: Reproducible linux/amd64 mock OCI image

- **Dependencies / parallelism:** DIST-01; no, because it consumes the frozen frontend/resource layout and shared notice bundle.
- **Goal / files:** Create `packaging/oci/Dockerfile`, `packaging/oci/entrypoint.sh`, `packaging/oci/.dockerignore`, `packaging/oci/smoke_test.ps1`, `backend/tests/distribution/test_oci_contract.py`, `packaging/oci/sbom.spdx.json`, `packaging/oci/THIRD_PARTY_NOTICES.md`, and `docs/engineering/DIST-02_EVIDENCE.md`; serially modify `.gitlab-ci.yml`, `.github/workflows/ci.yml`, and `scripts/tests/ci_seed_contract.ps1`. Pin Node builder and Python runtime by reviewed linux/amd64 manifest digest; install only the hashed demo lock; run non-root with tmpfs, healthcheck, egress deny, and demo profile. Before the distribution branch's first push, both CI files have required push-triggered OCI jobs that run the same literal `docker build --platform linux/amd64` contract, inspect architecture/user/SBOM/notices, and never push an image. GitLab's job uses only runner tag `projectb-docker-linux-amd64` and fails unless preflight reports linux/amd64, Docker Engine `29.1.2`, BuildKit, at least 4 GiB memory, and no privileged host mount; GitHub uses its pinned `ubuntu-24.04` runner contract.
- **Red:** `& $Py -m pytest backend/tests/distribution/test_oci_contract.py -q`; expect floating-image, Windows-lock, root, persistence, egress, notice/SBOM, public-origin, forbidden-capability, and dual push-CI OCI-build failures. Rerun the F-01D seed contract and require both OCI-job assertions to fail before workflow edits.
- **Green/refactor:** rerun the exact Red command and `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/verify_linux_dependency_evidence.ps1`; run `docker build --platform linux/amd64 --file packaging/oci/Dockerfile --tag projectb-demo:local .`, then `docker run -d --rm --name projectb-demo-smoke --read-only --tmpfs /tmp/projectb-demo:rw,size=64m -e PROJECTB_DEMO_LOCAL_SMOKE=1 -p 127.0.0.1:7860:7860 projectb-demo:local`. In `try/finally`, run `powershell -NoProfile -ExecutionPolicy Bypass -File packaging/oci/smoke_test.ps1 -Container projectb-demo-smoke -Image projectb-demo:local -BaseUrl http://127.0.0.1:7860`, `docker image inspect projectb-demo:local`, and finally `docker rm -f projectb-demo-smoke`. The smoke script must fail on wrong architecture/user/history/filesystem, missing SBOM/notices, persistence, forbidden routes, provider egress, or nonzero network count.
- **Done / commit:** clean build, exact local run command, automated inspect/SBOM/license checks, local-browser demo, and both push-triggered OCI build contracts pass; record the local image ID/digest without a registry push or deployment claim. Commit `build(DIST-02): package mock demo image [agent: worker]`.

### CI-01: Dual CI definitions and local contract

- **Dependencies / parallelism:** DIST-02; no, because CI consumes every final local test and distribution command.
- **Goal / files:** Create `scripts/verify_ci_contract.py`, `backend/tests/contracts/test_ci_files.py`, and `docs/engineering/CI-01_EVIDENCE.md`; serially modify `.gitlab-ci.yml` or `.github/workflows/ci.yml` only if the new verifier exposes final-assembly drift. The verifier parses both CI documents structurally and proves that their already-existing F-01D/DIST jobs preserve push triggers, GitLab `unit-test`, exact runner/image/action pins, least permissions, current-suite execution, Windows packaging, OCI build/inspect, lock install commands, timeout/failure propagation, and no allow-failure/path-filter/empty-suite bypass. It emits a stable command/job/requirement mapping and refuses any unrecognized job.
- **Red:** first create `backend/tests/contracts/test_ci_files.py`; run `& $Py -m pytest backend/tests/contracts/test_ci_files.py -q`; expect only the genuinely new `verify_ci_contract` module/receipt/stable-mapping/final-parity failures. Do not assert that predecessor-owned push jobs or distribution commands are absent.
- **Green/refactor:** implement the missing verifier and evidence receipt, rerun the exact Red command, run `& $Py scripts/verify_ci_contract.py`, `BE-REGRESSION`, `FE-REGRESSION`, and `LICENSE-SECURITY-GATE`, then locally execute every command named by both CI files. Any configuration repair gets its own new failing parity assertion before the serial edit. Remote status remains `not_executed` until authorization.
- **Done / commit:** the new structural verifier and stable mapping pass, both existing definitions remain locally executable and equivalent at the requirement level, and no CI PASS is claimed yet. Commit `ci(CI-01): verify final dual pipelines [agent: worker]`.

### DOC-01: Final README, compliance, notices, and release evidence

- **Dependencies / parallelism:** CI-01 and DIST-01-VM-CLOSE; no, because it records observed local release facts and must not predict remote or public deployment facts.
- **Goal / files:** Create/finalize `README.md`, serially finalize `licenses/THIRD_PARTY_NOTICES.md`, create `scripts/verify_links.py` and `backend/tests/contracts/test_readme.py`. The root coordinator, not this worker, owns `docs/REQUIREMENTS_COMPLIANCE_AUDIT.md`. `REFLECTION.md` remains student-authored and is never created or filled by this task.
- **Red:** `& $Py -m pytest backend/tests/contracts/test_readme.py -q`; expect missing project/install/run/distribution/tree/security/credential/limits/local-architecture/CI/license sections or unverified status claims.
- **Green/refactor:** after the prerequisite receipts, rerun the exact Red command, `& $Py scripts/verify_links.py`, `BE-REGRESSION`, `FE-REGRESSION`, `LICENSE-SECURITY-GATE`, strict evidence checks, and external-browser HTTPS acceptance against the exact deployed image digest.
- **Done / commit:** README contains only observed local commands/results, local architecture, CI/CD, credential guidance, third-party sources/licenses, and limitations; public deployment is recorded as waived/not executed per D-025 and compliance rows are implemented/verified or honestly gated. Commit `docs(DOC-01): publish verified project guide [agent: worker]`.

## 11. External Closure Gates

| Gate | Required actor/action | Exact closure evidence | Blocks |
| --- | --- | --- | --- |
| `P-EVIDENCE` | closed locally on 2026-07-25; coordinator refreshes only after expiry or official drift, with no account/key/call | evidence SHA-256 `35a3f46e036563e3fc681df3190eb56336ab48b9d9817ad48f4d5df42230f076`; `PROVIDER_V1_P_EVIDENCE_PASS rows=7 models=2 expires=2026-08-25`; no F/File/tool behavior | P-02 only if the snapshot expires |
| `BOOTSTRAP-LICENSE-EVIDENCE` | closed locally 2026-07-27: coordinator resolved official GitHub tags to commits and hashed Contents-API bytes; F-01B re-verifies immutable commit URLs | `docs/engineering/BOOTSTRAP_LICENSE_EVIDENCE.md` SHA-256 `FD65C5D2F8421F7B99AE4D540B80A8BBED1C28C78EF45851F7C6E5051034F310`; five URL/commit/blob/byte/hash/license rows | F-01B if evidence drifts |
| `DIST-01-VM-CLOSE` | coordinator or student supplies a clean Windows 11 x64 VM with 2 vCPU, 8 GiB RAM, SSD, and no Python/Node/Docker; run the exact DIST-01 artifact hash, <=10.0-second readiness measurement, and disposable real WinVault lifecycle with `finally` cleanup | artifact hash, OS build/CPU/RAM/storage, startup duration, SmartScreen observation, WinVault value-free receipt, cleanup and no-secret scan | DOC-01 and final distribution claim |
| `EXT-REMOTE-PREP` | after explicit authorization, coordinator configures NJU GitLab, GitHub mirror, and public OCI registry; before any push it proves the NJU project has a protected runner tagged only `projectb-docker-linux-amd64` with the exact DIST-02 preflight capabilities. It then pushes the nine reviewed branch tips (all contain F-01D push CI) and opens the same stacked base chain on both hosts: `foundation -> default`, `m1 -> foundation`, `m2 -> m1`, `m3-api -> m2`, `webui -> m3-api`, `demo -> webui`, `provider -> demo`, `distribution -> provider`, `release -> distribution`. It publishes/pulls the reviewed DIST-02 digest without rebuilding and does not merge yet | remote URLs; value-free GitLab runner/tag/version/arch/memory/BuildKit receipt; nine branch/commit/base/MR/PR mappings per host; visibility evidence showing GitHub public or named TA collaborator on private repo; push-trigger/current-suite/artifact-build receipts for every branch tip; public image digest/SBOM; clean pull/run receipts | deployment prerequisite and DOC-01 |
| `D-025-HOST-CLOSE` | waived by the student for this local-only project; no host, public registry, paid resource, or public URL is required | `not applicable`/`not executed` record with the local-only decision | none |
| `REFLECTION-CLOSE` | after DOC-01, the student writes `REFLECTION.md` in 1500--2500 Chinese characters as required by the course text; AI may only review a supplied draft and record assistance. The coordinator stages that student-authored file only after the declaration is present | student-authored file, character count, assistance declaration, and scanner-clean staged receipt | EXT-REMOTE-FINAL |
| `EXT-REMOTE-FINAL` | after DOC-01, coordinator compliance update, and REFLECTION-CLOSE, coordinator commits those final docs on `codex/release-v1`, scans, pushes, and requires both hosts green. On each host, merge in dependency order: `foundation`, `m1`, `m2`, `m3-api`, `webui`, `demo`, `provider`, `distribution`, `release`. Before each merge after foundation, retarget that existing stacked MR/PR from its predecessor branch to the default branch and verify the diff contains only that worktree's reviewed commits. Use the host's ordinary merge-commit strategy; forbid squash/rebase/history rewrite and preserve every terminal task commit as an ancestor. Do not delete a source branch until its mapping and green receipt are recorded | final release source commit containing README/compliance/student reflection; nine terminal-task-to-source/base/MR/PR mappings and nine merged closures per host; each merged default-branch commit and ancestry proof; authoritative NJU `unit-test` PASS and GitHub Actions PASS for their respective exact final default-branch merge commits; immutable IDs/timestamps | final course submission/completion claim |

No gate permits paid resources, real-key disclosure, history rewrite, force-push, publication, or deployment beyond the student's exact authorization.

## 12. Acceptance and Requirement Mapping

| SPEC acceptance | Active owner/evidence |
| --- | --- |
| AC-01 | M1-01/M1-02, API-01, UI-02 |
| AC-02 | M1-01 and M1-02 |
| AC-03 | M1-03, API-01, UI-03 |
| AC-04 | M1-03, UI-03, UI-06 |
| AC-05 | M2-01 and M2-02 |
| AC-06 | M2-01, API-02, UI-04 |
| AC-07 | P-01, API-02, UI-04 |
| AC-08 | P-02 and P-EVIDENCE |
| AC-09 | P-01/P-02 authority-negative tests |
| AC-10 | M2-03 |
| AC-11 | M2-04 |
| AC-12 | M3-01 |
| AC-13 | M3-02, API-03, UI-05 |
| AC-14 | F-05, API-03, UI-06, DIST-01 |
| AC-15 | F-04 and DEMO-01 public trust tests |
| AC-16 | UI-01--UI-06 and QA-RELEASE |
| AC-17 | DEMO-01 and DIST-02 |
| AC-18 | F-01E, F-01D current-suite CI, and QA-RELEASE |
| AC-19 | DIST-01, DIST-01-VM-CLOSE, and DOC-01 |
| AC-20 | DIST-02, CI-01, EXT-REMOTE-PREP, and EXT-REMOTE-FINAL |
| AC-21 | Local WebUI URL and architecture in DOC-01; public HTTPS URL waived by D-025 |
| AC-22 | per-task protocol and coordinator evidence commits |
| AC-23 | F-01S1A--F-01S4/F-01A/F-01B/F-01E, all scans/reviews, DIST-01/02, DOC-01 |
| AC-24 | G-03 and `SPEC_PROCESS.md` |

The authoritative course matrix is `docs/REQUIREMENTS_COMPLIANCE_AUDIT.md`; before G-03 it must bind the final SPEC/PLAN hashes and map every hard row to these task IDs or named gates.

## 13. Deferred Scope and Recovery

The active tasks do not implement OCR/image/scanned PDF/bulk ingestion, whole-file F or durable remote jobs, past-exam/teacher-focus intelligence, or rubrics beyond mutex/race/deadlock. Their only plans are:

- `docs/archive/deferred-v2/advanced-material-ingestion.md`
- `docs/archive/deferred-v2/remote-f-and-durable-jobs.md`
- `docs/archive/deferred-v2/exam-material-intelligence.md`
- `docs/archive/deferred-v2/extended-concept-rubrics.md`

They remain `ARCHIVED / NOT DISPATCHABLE`. Recovery requires `brainstorming -> SPEC confirmation -> writing-plans`; no active task may silently absorb them.
