# ProjectB v1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` or `superpowers:executing-plans` to execute one task at a time. Every behavior task uses `superpowers:test-driven-development`; unexpected failures use `superpowers:systematic-debugging`; reviews use `superpowers:requesting-code-review` and `superpowers:receiving-code-review`; completion claims use `superpowers:verification-before-completion`; each worktree group closes with `superpowers:finishing-a-development-branch`.

**Status:** `COLD-START REMEDIATION / NOT DISPATCHABLE`

**Confirmed SPEC:** review-remediated SHA-256 `69A534D9E5145BF86B3A5CDAE94C7C8679C100A277C4638ED6DE51904555855E`; confirmed product-content SHA-256 `C6231816A62C807D205FC7A3E6142C5636DE18FD8A2C580B48E63B106F959AD6`.

**Goal:** Build the reduced v1 local study workbench: source-grounded material import and mapping, deterministic learning evidence for mutex/race/deadlock, and continuous/finals review planning, with an optional consent-bound OpenAI P adapter and a mock-only public demo.

**Architecture:** React/Vite calls a profile-aware FastAPI application. Domain services own authority; SQLite stores metadata and append-only evidence; a content-addressed current-user store keeps material bytes; Windows Credential Manager keeps secrets. Provider output is non-authoritative and replaceable by a deterministic mock. The local profile is loopback-only; the public demo exposes only synthetic licensed fixtures, ephemeral state, and the mock.

**Pinned stack:** CPython 3.14.6; FastAPI 0.139.2; Pydantic 2.13.4; SQLite; pypdf 6.14.2; pypdfium2 5.12.1; keyring 25.7.0; OpenAI SDK 2.46.0; pytest 9.1.1; Ruff 0.15.22; mypy 2.3.0; Node 24.18.0/npm 11.16.0; React 19.2.7; Vite 8.1.5; TypeScript 7.0.2; Vitest 4.1.10; Playwright 1.61.1; axe 4.12.1; PyInstaller 6.21.0. Windows, Linux-CI, Linux-demo, npm, OCI-base, and license evidence are frozen under `docs/engineering/`.

## 1. Dispatch Gates

No formal task dispatch, task-status change, implementation commit, or integration may start until all of these are true on the same final SPEC/PLAN bytes. G-03 is the only pre-dispatch exception: a fresh different-type coding agent works in a disposable copy containing only `SPEC.md` and `PLAN.md`, may attempt the complete dependency-free task `F-01S`, and may not commit, integrate, edit the real repository, or change the ledger. Its disposable attempt leaves formal F-01S `not started`; only its questions, misunderstandings, output gap, and resulting documentation diff become evidence. `G-03P` is the same procedure run by a fresh Codex task when no different-type service is accessible; it is useful remediation input but never closes G-03 or authorizes implementation.

1. `SR-08`: mechanical audit, SPEC-compliance review, and quality/security/license review all report no Critical or Major issue and record both hashes externally.
2. `G-03`: a fresh non-Codex coding-agent session, with only final `SPEC.md` and `PLAN.md`, attempts the complete `F-01S` task and records every question, misunderstanding, output gap, red/green output, and repair in `SPEC_PROCESS.md`. A Codex `G-03P` receipt cannot satisfy this item.
3. The repaired SPEC/PLAN snapshot is re-reviewed if either file changes.
4. `G-04`: after reading the cold-start record and repairs, the student explicitly approves implementation. The earlier SPEC confirmation is not G-04.

`D-025` hosting and `EXT-REMOTE-PREP`/`EXT-REMOTE-FINAL` authorizations do not block local implementation. They block remote mutation, final CI receipts, deployment, public URL, and release completion.

## 2. Worktrees, Ownership, and Order

After G-04, the coordinator creates `codex/implementation-v1` and these worktrees in order. A later worktree starts only from the locally integrated, reviewed predecessor. No implementation tasks are parallel: API/UI registries, migrations, and evidence ledgers have serialized ownership, and the reduced plan favors recoverable commits over merge concurrency.

| Worktree branch | Tasks, strictly in order | Closure |
| --- | --- | --- |
| `codex/foundation-v1` | F-01S -> F-01A -> F-01B -> F-02 -> F-03 -> F-04 -> F-05 | finish and locally integrate before M1 |
| `codex/m1-materials-v1` | M1-01 -> M1-02 -> M1-03 | finish and locally integrate before M2 |
| `codex/m2-learning-v1` | M2-01 -> M2-02 -> M2-03 -> M2-04 | finish and locally integrate before P-01 |
| `codex/m3-api-v1` | P-01 -> M3-01 -> M3-02 -> API-01 -> API-02 -> API-03 | finish and locally integrate before UI |
| `codex/webui-v1` | UI-01 -> UI-02 -> UI-03 -> UI-04 -> UI-05 -> UI-06 | finish and locally integrate before demo |
| `codex/demo-v1` | DEMO-01 | finish and locally integrate before provider adapter |
| `codex/provider-openai-v1` | P-02 | finish and locally integrate before distribution |
| `codex/distribution-v1` | DIST-01 -> DIST-02 | finish and locally integrate before CI |
| `codex/release-v1` | CI-01 -> external closures -> DOC-01 | no push, MR, PR, deployment, or publication without its named gate |

Only the root coordinator edits `PLAN.md`, `AGENT_LOG.md`, `SPEC_PROCESS.md`, or the compliance audit. Workers never stage those paths. Shared evidence updates happen after a terminal reviewed implementation hash exists. DOC-01 therefore does not own the compliance audit; the coordinator updates it in the scanned evidence commit after DOC-01 review.

## 3. Per-Task Protocol

Each task is one fresh subagent session with only its task card, confirmed SPEC, predecessor interfaces, exact commands, and owned paths. A task card is a single-session packet; its implementation is decomposed into the following explicit 2--5 minute steps required by course section 4.1: for each named Red assertion in written order, (a) add exactly one assertion/fixture in one owned test file, (b) run the card's exact targeted command and record the requirement-shaped red, (c) add or change at most one named production function, schema object, or configuration stanza in one owned path, and (d) rerun that same targeted test to green. After all assertion loops, separately (e) refactor one symbol, (f) run targeted green, (g) run each listed regression/gate command one at a time, (h) stage and scan, and (i) perform each review/commit/log action. Any step estimated above five minutes must be split again before dispatch and the expanded checklist copied into the task prompt and `AGENT_LOG.md`; combining two files or two behaviors in one step is forbidden. This shared expansion is normative and avoids repeating the same microstep boilerplate in every card.

Path aliases are exact: `domain/`, `services/`, `repositories/`, `storage/`, `security/`, `observability/`, `api/`, `providers/`, and `profiles/` mean the corresponding path below `backend/projectb/`; `evaluators/` means `backend/projectb/domain/learning/evaluators/`; `views/` and `styles/` mean the corresponding path below `frontend/src/`. No other abbreviation is allowed. A directory path ending `/` grants ownership only of the explicitly named descendants in that card, never an open glob.

`F-01S` alone uses only Git and Windows PowerShell because no committed project runtime exists yet. G-03/G-03P attempts the complete F-01S task in a disposable directory and must run a real red then green without any dependency ledger, package download, Git commit, or original-repository edit. Formal F-01S after G-04 repeats the task in the implementation worktree. F-01A then creates the project-local toolchain. Only the not-yet-created Python/Node commands are exempt before F-01A: red/green, staging only owned paths, both reviews, trailers, verification, logging, and commits still apply. Before every implementation, review-fix, and coordinator evidence commit, stage only owned evidence paths and run `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/bootstrap_scan_credentials.ps1 -Tracked -Staged`; `-Staged` must scan index blob bytes, not working-tree substitutes. Any Git/index/read/decode/scan error fails closed and no matching value is printed. The full protocol applies from F-01A onward.

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
| 1 | F-01S | G-04 | no: first fail-closed scanner | foundation | not started | none |
| 2 | F-01A | F-01S + BOOTSTRAP-LICENSE-EVIDENCE | no: creates project-local toolchain | foundation | not started | none |
| 3 | F-01B | F-01A | no: creates shared quality gates | foundation | not started | none |
| 4 | F-02 | F-01B | no: migration order | foundation | not started | none |
| 5 | F-03 | F-02 | no: migration order | foundation | not started | none |
| 6 | F-04 | F-03 | no: security base | foundation | not started | none |
| 7 | F-05 | F-04 | no: security base | foundation | not started | none |
| 8 | M1-01 | F-05 | no: material contracts | m1-materials | not started | none |
| 9 | M1-02 | M1-01 | no: consumes extraction | m1-materials | not started | none |
| 10 | M1-03 | M1-02 | no: consumes material repo | m1-materials | not started | none |
| 11 | M2-01 | M1-03 | no: evaluator base | m2-learning | not started | none |
| 12 | M2-02 | M2-01 | no: registry assembly | m2-learning | not started | none |
| 13 | M2-03 | M2-02 | no: evidence authority | m2-learning | not started | none |
| 14 | M2-04 | M2-03 | no: mastery consumes evidence | m2-learning | not started | none |
| 15 | P-01 | M2-04 | no: provider port and mock | m3-api | not started | none |
| 16 | M3-01 | P-01 | no: planner contract | m3-api | not started | none |
| 17 | M3-02 | M3-01 | no: revision persistence | m3-api | not started | none |
| 18 | API-01 | M3-02 | no: creates app registry | m3-api | not started | none |
| 19 | API-02 | API-01 | no: modifies app registry | m3-api | not started | none |
| 20 | API-03 | API-02 | no: closes local API | m3-api | not started | none |
| 21 | UI-01 | API-03 | no: creates route registry | webui | not started | none |
| 22 | UI-02 | UI-01 | no: modifies route registry | webui | not started | none |
| 23 | UI-03 | UI-02 | no: modifies route registry | webui | not started | none |
| 24 | UI-04 | UI-03 | no: modifies route registry | webui | not started | none |
| 25 | UI-05 | UI-04 | no: modifies route registry | webui | not started | none |
| 26 | UI-06 | UI-05 | no: modifies route registry | webui | not started | none |
| 27 | DEMO-01 | UI-06 | no: profile assembly | demo | not started | none |
| 28 | P-02 | DEMO-01 + P-EVIDENCE | no: real adapter is isolated last | provider-openai | not started | none |
| 29 | DIST-01 | P-02 + QA-RELEASE | no: Windows release | distribution | not started | none |
| 30 | DIST-02 | DIST-01 | no: consumes frozen frontend/runtime | distribution | not started | none |
| 31 | CI-01 | DIST-02 | no: consumes all commands | release | not started | none |
| 32 | DOC-01 | CI-01 + EXT-REMOTE-PREP + D-025-HOST-CLOSE + DIST-01-VM-CLOSE | no: final verified guide | release | not started | none |

## 5. Foundation Tasks

### F-01S: Dependency-free index and worktree credential scanner

- **Dependencies / parallelism:** G-04 for formal repository implementation; G-03/G-03P may attempt this complete task pre-dispatch in an isolated two-file workspace. No parallel work because every commit gate depends on it.
- **Goal / files:** Create only `scripts/tests/bootstrap_scanner_contract.ps1` and `scripts/bootstrap_scan_credentials.ps1`. `-Tracked` enumerates `git ls-files -z` and scans current working-tree bytes. `-Staged` enumerates `git diff --cached --name-only -z --diff-filter=ACMR`, resolves each stage-0 entry with `git ls-files --stage -z -- PATH`, rejects non-regular mode, and obtains exact index blob bytes through a binary-safe `System.Diagnostics.Process` `git cat-file blob OID` stdout stream; it never substitutes filesystem bytes. With both switches, scan both `(worktree,path)` and `(index,path)` source pairs even when the path is identical. No switch is `usage_missing_scope`.
- **Scope/encoding:** For worktree sources, resolve the Git top level and require every root-to-leaf component to stay below root, be regular, and lack `ReparsePoint`; for index sources require normalized non-absolute non-escaping Git paths and mode `100644` or `100755`. Stable errors are `git_root_failed`, `git_list_failed`, `index_entry_failed`, `index_mode_unsupported`, `path_escape`, `reparse_point`, `not_regular_file`, `read_failed`, `decode_failed`, `nul_unmarked`, `unsupported_file_type`, and `scan_failed`. Text allowlist is `.md,.txt,.json,.jsonl,.toml,.yaml,.yml,.ini,.cfg,.conf,.env,.example,.py,.pyi,.js,.mjs,.cjs,.ts,.tsx,.jsx,.html,.css,.scss,.sql,.ps1,.psm1,.psd1,.sh,.bash,.cmd,.bat,.lock,.in` plus extensionless `.gitignore,.gitattributes,.dockerignore,Dockerfile,Makefile,LICENSE,NOTICE`; binary skip list is `.png,.jpg,.jpeg,.gif,.webp,.pdf,.ico,.zip,.gz,.7z,.exe,.dll,.pyd,.so,.woff,.woff2,.ttf,.mp3,.mp4,.sqlite,.db`; everything else fails. Decode strict UTF-8 with/without BOM or BOM-declared UTF-16LE/BE; unmarked NUL fails.
- **Rules:** Tests assemble positive prefixes from fragments. The six token/private-key rules and lengths remain: provider `s+k-` + 20--200 `[A-Za-z0-9_-]`; GitHub `gh` + one of `p_,o_,u_,s_,r_` + 20--255 alphanumerics; AWS `AK+IA|AS+IA` + exactly 16 uppercase alphanumerics; Google `AI+za` + exactly 35 `[A-Za-z0-9_-]`; Slack `xo` + one of `xb,xp,xa,xr,xs` + `-` + 10--200 alphanumeric/hyphen; PEM `BEGIN ... PRIVATE KEY`. Token matches require start/end or a neighbor outside `[A-Za-z0-9_-]`. Assignment names are case-insensitive `api_key|api-key|apikey|access_token|auth_token|client_secret|password|passwd|secret|token`, bounded on the left by start or a non-`[A-Za-z0-9_-]`, followed by optional horizontal whitespace, `:`/`=`, and optional whitespace. A quoted value uses matching single/double quotes, forbids newline, permits backslash only before the matching quote or backslash, and contains 8--512 decoded characters; an unquoted value is the maximal 8--512 run of `[A-Za-z0-9_./+=:@-]`. Normalize only for safe values `example,placeholder,changeme,not-set,none,null,redacted`, a whole value enclosed by one angle-bracket pair, a whole shell-variable form, or a whole square-bracket form containing `redacted`. Encoded detection decodes exactly one strict UTF-8 Base64/Base64URL layer (16--4096, 0--2 terminal `=`) or even hex layer (32--8192) and reports only decoded matches of the first six rules.
- **Output:** Scan every source/path pair and emit unique findings sorted by `source,path,rule`. Clean exit 0 is exactly `CREDENTIAL_SCAN_PASS files=N`, where N is the decimal source-pair count. Finding exit 2 prints one line each using the exact object key order `CREDENTIAL_SCAN_FINDING {"source":SOURCE_JSON_STRING,"path":PATH_JSON_STRING,"rule":RULE_JSON_STRING}`. Operational exit 3 prints only `CREDENTIAL_SCAN_ERROR {"code":CODE_JSON_STRING}` with optional `,"source":SOURCE_JSON_STRING` then `,"path":PATH_JSON_STRING` in that property order. JSON strings use standard escaping. Values, content, line data, decoded payloads, and blob OIDs are forbidden.
- **Red:** create the contract first and run exactly `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/tests/bootstrap_scanner_contract.ps1`; expect exit 1 and `CONTRACT_RED scanner_missing`. The contract covers every rule, boundaries/quotes/placeholders, encodings, path/reparse/mode failures, rename, staged-secret+clean-worktree, clean-index+dirty-worktree, both-source findings, binary-safe index blobs, exact exits, and redaction.
- **Green/refactor:** create the minimum scanner and rerun the exact Red command; expect exit 0, all named groups, and `BOOTSTRAP_SCANNER_CONTRACT_PASS` without changing assertions.
- **Done / commit:** G-03/G-03P records diff and red/green then stops without integration. Formal post-G-04 execution stages only the two files, scans index and worktree, obtains both reviews, and commits `build(F-01S): add fail-closed bootstrap scanner [agent: worker]`.

### F-01A: Reproducible toolchain, bootstrap licenses, frontend harness, and push CI seed

- **Dependencies / parallelism:** F-01S and `BOOTSTRAP-LICENSE-EVIDENCE`; no, because all later tasks consume the project-local runtime and every branch tip must contain push CI.
- **Goal / files:** Create `.python-version`, `pyproject.toml`, `backend/requirements-windows-x64.lock`, `requirements.linux-ci.lock`, `packaging/oci/requirements.linux-demo.lock`, `frontend/package.json`, `frontend/package-lock.json`, `frontend/.npmrc`, `frontend/tsconfig.json`, `frontend/vite.config.ts`, `frontend/src/foundation/RuntimeProbe.tsx`, `frontend/src/foundation/RuntimeProbe.test.tsx`, `scripts/bootstrap.ps1`, `scripts/tests/foundation_contract.ps1`, `licenses/bootstrap/uv-LICENSE-APACHE`, `licenses/bootstrap/uv-LICENSE-MIT`, `licenses/bootstrap/cpython-LICENSE`, `licenses/bootstrap/node-LICENSE`, `licenses/bootstrap/npm-LICENSE`, `.gitlab-ci.yml`, and `.github/workflows/ci.yml`. Initial CI triggers on every push; GitLab already has job `unit-test`; both run F-01S and the foundation contract. CI-01 later expands the same files, so every eventual branch tip contains a workflow before first remote push.
- **Pinned inputs:** Python targets are raw-byte copies of the three reviewed lock files with hashes `246083f8...0fc6`, `d24ddf37...fc35`, and `09ce5772...34f7`. The npm target preserves closure `071826d5...3c2f` and exact root map: dependencies `react@19.2.7`, `react-dom@19.2.7`, `lucide-react@1.25.0`; devDependencies `vite@8.1.5`, `@vitejs/plugin-react@6.0.3`, `typescript@7.0.2`, `vitest@4.1.10`, `@testing-library/dom@10.4.1`, `@testing-library/react@16.3.2`, `@testing-library/user-event@14.6.1`, `jsdom@29.1.1`, `@playwright/test@1.61.1`, `@axe-core/playwright@4.12.1`, `@types/react@19.2.17`, `@types/react-dom@19.2.3`, `@types/node@24.13.3`. `.npmrc` enables `engine-strict`, `ignore-scripts`, `audit`, `fund=false`, `save-exact`, and `package-lock`; TypeScript is strict with `noUncheckedIndexedAccess`; Vite/Vitest use JSDOM, `*.test.ts(x)`, React, and strict loopback ports 5173/4173.
- **Red:** create `scripts/tests/foundation_contract.ps1`; run exactly `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/tests/foundation_contract.ps1`; expect missing artifact/hash/license-evidence, raw-lock parity, manifest/config, push-trigger/`unit-test`, blocked-`npm.ps1`, corrupt-download/version-drift, and runtime-probe failures. It may use only Git/PowerShell until bootstrap resolves local tools.
- **Green/refactor:** consume the artifact rows and exact license URL/tag-or-commit/SHA-256 rows from `docs/engineering/BOOTSTRAP_LICENSE_EVIDENCE.md`; bootstrap verifies bytes before extraction, never changes system PATH/registry, and copies only verified license bytes. Rerun the exact Red command, scan index and worktree, then run `& $Npm --prefix frontend exec -- vitest run src/foundation/RuntimeProbe.test.tsx`; the test must operate an accessible React counter through JSDOM/Testing Library/user-event.
- **Done / commit:** exact local toolchains, locks/manifests, byte-pinned licenses, minimal push CI, negative contracts, and React interaction pass. Commit `build(F-01A): materialize reviewed toolchain [agent: worker]`.

### F-01B: One-command runner, credential scanner, and license gates

- **Dependencies / parallelism:** F-01A; no, because every later task depends on these fail-closed quality commands.
- **Goal / files:** Create `scripts/test_all.py`, `scripts/scan_credentials.py`, `scripts/verify_licenses.py`, `scripts/tests/test_quality_gates.py`, `scripts/tests/fixtures/scanner/clean.txt`, `scripts/tests/fixtures/scanner/placeholder.env.example`, `scripts/tests/fixtures/scanner/binary.png`, and `licenses/THIRD_PARTY_NOTICES.md`; positive shapes are assembled only in test runtime. Retain F-01S as the runtime-free fallback and prove the Python scanner is a strict superset, including exact index blobs and separate index/worktree source reporting. The runner invokes backend tests, foundation Vitest, frontend build when its entry exists, contracts, credential scan, and license verification with bounded child processes and propagated nonzero exits. License verification binds reviewed Python/npm/bootstrap/OCI authorities and notices.
- **Red:** create `scripts/tests/test_quality_gates.py`; run `& $Py -m pytest scripts/tests/test_quality_gates.py -q`; expect missing runner/scanner/license-verifier, failure-propagation, redaction, notice, and exact-command assertions.
- **Green/refactor:** rerun the exact Red command, `& $Py scripts/scan_credentials.py --tracked --staged`, `& $Py scripts/verify_licenses.py`, the literal `python scripts/test_all.py` under the common bootstrap's process-local PATH, `& $Py scripts/test_all.py`, `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/verify_evidence.ps1`, and `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/verify_linux_dependency_evidence.ps1`.
- **Done / commit:** one-command orchestration, timeout/child failure propagation, credential redaction, full reviewed license/notices closure, and both literal/explicit Python invocations pass; no empty-suite or `passWithNoTests` path can yield green. Commit `build(F-01B): add fail-closed quality gates [agent: worker]`.

### F-02: Core metadata schema and unit of work

- **Dependencies / parallelism:** F-01B; no, because it creates migration 001 and the transaction base consumed by F-03.
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
- **Goal / files:** Use the real Open Design project/run with `frontend-design` and `default`/Neutral Modern; record it in `docs/engineering/OPEN_DESIGN_RUN.md`. Create `frontend/src/styles/tokens.css`, `frontend/src/styles/global.css`, `frontend/src/app/App.tsx`, `frontend/src/app/routes.tsx`, `frontend/src/app/Shell.test.tsx`, `frontend/src/api/client.ts`, `frontend/src/api/capabilities.ts`, `frontend/playwright.config.ts`, `frontend/e2e/support/testServer.ts`, and `frontend/e2e/shell.spec.ts`. Generated design is evidence only until the red test runs.
- **Red:** `& $Npm --prefix frontend exec -- vitest run src/app/Shell.test.tsx` and `& $Npm --prefix frontend exec -- playwright test e2e/shell.spec.ts`; expect missing four-stage navigation, 360/768/1440 layout, keyboard, and axe assertions.
- **Green/refactor:** run `& $Npm --prefix frontend exec -- playwright install chromium`, rerun both exact Red commands, then run `FE-REGRESSION` and `LICENSE-SECURITY-GATE`.
- **Done / commit:** real Open Design evidence exists; compact workbench shell has no hero/nested cards/overflow, radius <=8 px and letter spacing 0. Commit `feat(UI-01): build opendesign workbench shell [agent: worker]`.

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
- **Goal / files:** Create `backend/projectb/profiles/demo.py`, `backend/projectb/demo/fixtures.manifest.json`, `backend/projectb/demo/course.json`, `backend/projectb/demo/materials.md`, `backend/tests/demo/test_demo_profile.py`, `backend/tests/demo/test_demo_security.py`, and `frontend/e2e/demo.spec.ts`; serially update `backend/projectb/profiles/registry.py`. Fixtures are synthetic CC0 and <=20; SQLite is ephemeral; sessions expire at 30-minute idle/two-hour absolute; upload/credential/OpenAI/cross-session state are absent and outbound calls are denied process-wide.
- **Trust contract:** local Docker smoke requires `PROJECTB_DEMO_LOCAL_SMOKE=1` and permits only `http://127.0.0.1:7860`; public mode refuses startup without one exact HTTPS `PROJECTB_PUBLIC_ORIGIN`, derives Host/Origin allowlists without wildcards, uses HttpOnly/SameSite=Lax/Secure cookies, session-bound CSRF, and rejects forwarded headers unless D-025 supplies an exact trusted-proxy boundary.
- **Red:** `& $Py -m pytest backend/tests/demo -q` and `& $Npm --prefix frontend exec -- playwright test e2e/demo.spec.ts`; expect forbidden-route, egress, TTL, cross-session, public-origin, and fixture-license failures.
- **Green/refactor:** rerun both exact Red commands, then run `BE-REGRESSION`, `FE-REGRESSION`, and `LICENSE-SECURITY-GATE`.
- **Done / commit:** same UI/domain contracts run on licensed synthetic data; forbidden capabilities are absent, not merely hidden. Commit `feat(DEMO-01): add isolated mock demo [agent: worker]`.

### P-02: P-only OpenAI adapter from the reviewed policy snapshot

- **Dependencies / parallelism:** DEMO-01, P-01, and P-EVIDENCE; no, because it is isolated after the mock-complete core and is the only production-adapter registry modifier.
- **Goal / files:** Consume read-only `docs/engineering/PROVIDER_POLICY_V1_P_EVIDENCE.md` and `scripts/verify_provider_policy_v1.ps1`; create `backend/projectb/providers/openai_adapter.py`, `backend/projectb/providers/policy.v1.json`, and `backend/tests/providers/test_openai_adapter.py`; serially update `backend/projectb/providers/registry.py`. Evidence hash is `35a3f46e...f076`, P-only and time-bounded. Mock HTTP transport tests, not real keys or paid calls, prove request/response behavior.
- **Contract:** local production remains in L with no selected provider until the user explicitly enables P; its registry permits only the built-in OpenAI adapter with a fresh policy, configured credential status, allowlisted model, and explicit input/output caps. Deterministic provider mock remains absent from local and registered only by test/demo profiles. Consent displays the computed maximum cost. Adapter sends only confirmed extracted fragments through Responses API with `store:false`, 60-second timeout, zero automatic retries, strict output schema, no student answer, and no network when snapshot is absent/stale or consent mismatches.
- **Red:** first require `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/verify_provider_policy_v1.ps1` to pass; then run `& $Py -m pytest backend/tests/providers/test_openai_adapter.py -q`; expect missing adapter/derived policy/registry update plus local-rejects-mock, unconfigured-L, stale-fixture, forbidden-field, schema, timeout, and zero-network failures.
- **Green/refactor:** if and only if evidence expired, return to the coordinator for an official-source refresh; otherwise rerun the verifier and exact Red test, then run `BE-REGRESSION` and `LICENSE-SECURITY-GATE`.
- **Done / commit:** P-only evidence and adapter are hash-bound; no F/direct-file behavior leaks into v1. Commit `feat(P-02): add governed openai p adapter [agent: worker]`.

### QA-RELEASE: Verification-only gate

This is not a dispatch task and owns no file. From a clean worktree, run the common bootstrap, `& $Npm --prefix frontend exec -- playwright install chromium`, `BE-REGRESSION`, `FE-REGRESSION`, `& $Npm --prefix frontend exec -- playwright test`, `LICENSE-SECURITY-GATE`, `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/verify_evidence.ps1`, `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/verify_linux_dependency_evidence.ps1`, and `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/verify_provider_policy_v1.ps1`. Playwright config runs 360/768/1440 projects. Any failure returns to the owning task with a defect-specific red test. QA-RELEASE may not repair feature behavior itself.

### DIST-01: Windows x64 single-file distribution

- **Dependencies / parallelism:** P-02 and QA-RELEASE; no, because it freezes the complete local application resources.
- **Goal / files:** Create `packaging/windows/build.ps1`, `packaging/windows/ProjectB.spec`, `packaging/windows/hooks/hook-keyring.py`, `packaging/windows/hooks/hook-pypdfium2.py`, `packaging/windows/smoke_test.ps1`, `backend/tests/distribution/test_windows_contract.py`, and `docs/engineering/DIST-01_EVIDENCE.md`. Build one `ProjectB.exe`; mutable data stays under `%LOCALAPPDATA%\ProjectB` or explicit data root; bind loopback only; embed WebUI and notices.
- **Red:** `& $Py -m pytest backend/tests/distribution/test_windows_contract.py -q`; expect missing single-file/resource/data-root/bind/startup/WinVault assertions.
- **Green/refactor:** rerun the exact Red command; run `powershell -NoProfile -ExecutionPolicy Bypass -File packaging/windows/build.ps1 -Python $Py -Output dist/ProjectB.exe`, scan index/worktree, and run `powershell -NoProfile -ExecutionPolicy Bypass -File packaging/windows/smoke_test.ps1 -Artifact dist/ProjectB.exe -DataRoot tmp/dist01-smoke` on the development host.
- **Done / commit:** local artifact hash, resource/data-root/bind behavior, no-secret scan, and development-host smoke are recorded. Commit `build(DIST-01): package windows single file [agent: worker]`. Clean-host startup/WinVault evidence is owned separately by `DIST-01-VM-CLOSE`.

### DIST-02: Reproducible linux/amd64 mock OCI image

- **Dependencies / parallelism:** DIST-01; no, because it consumes the frozen frontend/resource layout and shared notice bundle.
- **Goal / files:** Create `packaging/oci/Dockerfile`, `packaging/oci/entrypoint.sh`, `packaging/oci/.dockerignore`, `packaging/oci/smoke_test.ps1`, `backend/tests/distribution/test_oci_contract.py`, `packaging/oci/sbom.spdx.json`, `packaging/oci/THIRD_PARTY_NOTICES.md`, and `docs/engineering/DIST-02_EVIDENCE.md`. Pin Node builder and Python runtime by reviewed linux/amd64 manifest digest; install only the hashed demo lock; run non-root with tmpfs, healthcheck, egress deny, and demo profile.
- **Red:** `& $Py -m pytest backend/tests/distribution/test_oci_contract.py -q`; expect floating-image, Windows-lock, root, persistence, egress, notice/SBOM, public-origin, and forbidden-capability failures.
- **Green/refactor:** rerun the exact Red command and `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/verify_linux_dependency_evidence.ps1`; run `docker build --platform linux/amd64 --file packaging/oci/Dockerfile --tag projectb-demo:local .`, then `docker run -d --rm --name projectb-demo-smoke --read-only --tmpfs /tmp/projectb-demo:rw,size=64m -e PROJECTB_DEMO_LOCAL_SMOKE=1 -p 127.0.0.1:7860:7860 projectb-demo:local`. In `try/finally`, run `powershell -NoProfile -ExecutionPolicy Bypass -File packaging/oci/smoke_test.ps1 -Container projectb-demo-smoke -Image projectb-demo:local -BaseUrl http://127.0.0.1:7860`, `docker image inspect projectb-demo:local`, and finally `docker rm -f projectb-demo-smoke`. The smoke script must fail on wrong architecture/user/history/filesystem, missing SBOM/notices, persistence, forbidden routes, provider egress, or nonzero network count.
- **Done / commit:** clean build, exact local run command, automated inspect/SBOM/license checks, and local-browser demo pass; record the local image ID/digest without a registry push or deployment claim. Commit `build(DIST-02): package mock demo image [agent: worker]`.

### CI-01: Dual CI definitions and local contract

- **Dependencies / parallelism:** DIST-02; no, because CI consumes every final local test and distribution command.
- **Goal / files:** Expand F-01A's `.gitlab-ci.yml` and `.github/workflows/ci.yml`; create `scripts/verify_ci_contract.py`, `backend/tests/contracts/test_ci_files.py`, and `docs/engineering/CI-01_EVIDENCE.md`. Preserve push triggers and GitLab `unit-test`; add Python, frontend, and distribution jobs using pinned images/locks. GitHub actions use full reviewed commit SHAs and least permissions.
- **Red:** `& $Py -m pytest backend/tests/contracts/test_ci_files.py -q`; expect absent `unit-test`, push triggers, lock parity, action pin, and distribution commands.
- **Green/refactor:** rerun the exact Red command, run `& $Py scripts/verify_ci_contract.py`, `BE-REGRESSION`, `FE-REGRESSION`, and `LICENSE-SECURITY-GATE`, then locally execute every command named by both CI files. Remote status remains `not_executed` until authorization.
- **Done / commit:** both definitions are locally validated and map to the same test/build contracts; no CI PASS is claimed yet. Commit `ci(CI-01): define gitlab and github pipelines [agent: worker]`.

### DOC-01: Final README, compliance, notices, and release evidence

- **Dependencies / parallelism:** CI-01, EXT-REMOTE-PREP, D-025-HOST-CLOSE, and DIST-01-VM-CLOSE; no, because it records observed remote/deployment facts and must not predict them.
- **Goal / files:** Create/finalize `README.md`, serially finalize `licenses/THIRD_PARTY_NOTICES.md`, create `scripts/verify_links.py` and `backend/tests/contracts/test_readme.py`. The root coordinator, not this worker, owns `docs/REQUIREMENTS_COMPLIANCE_AUDIT.md`. `REFLECTION.md` remains student-authored and is never created or filled by this task.
- **Red:** `& $Py -m pytest backend/tests/contracts/test_readme.py -q`; expect missing project/install/run/distribution/tree/security/credential/limits/deployment/CI/license sections or unverified URL/status claims.
- **Green/refactor:** after the prerequisite receipts, rerun the exact Red command, `& $Py scripts/verify_links.py`, `BE-REGRESSION`, `FE-REGRESSION`, `LICENSE-SECURITY-GATE`, strict evidence checks, and external-browser HTTPS acceptance against the exact deployed image digest.
- **Done / commit:** README contains only observed commands/results, final public URL, architecture, CI/CD, credential guidance, third-party sources/licenses, and limitations; compliance rows are implemented/verified or honestly gated. Commit `docs(DOC-01): publish verified project guide [agent: worker]`.

## 11. External Closure Gates

| Gate | Required actor/action | Exact closure evidence | Blocks |
| --- | --- | --- | --- |
| `P-EVIDENCE` | closed locally on 2026-07-25; coordinator refreshes only after expiry or official drift, with no account/key/call | evidence SHA-256 `35a3f46e036563e3fc681df3190eb56336ab48b9d9817ad48f4d5df42230f076`; `PROVIDER_V1_P_EVIDENCE_PASS rows=7 models=2 expires=2026-08-25`; no F/File/tool behavior | P-02 only if the snapshot expires |
| `BOOTSTRAP-LICENSE-EVIDENCE` | closed locally 2026-07-27: coordinator resolved official GitHub tags to commits and hashed Contents-API bytes; F-01A re-verifies immutable commit URLs | `docs/engineering/BOOTSTRAP_LICENSE_EVIDENCE.md` SHA-256 `E9EFCF961D7C3309D30D8E4DBC5C465074E5E69BC2E9BED63FBF7B5EF29EE7E0`; five URL/commit/blob/byte/hash/license rows | F-01A if evidence drifts |
| `DIST-01-VM-CLOSE` | coordinator or student supplies a clean Windows 11 x64 VM with 2 vCPU, 8 GiB RAM, SSD, and no Python/Node/Docker; run the exact DIST-01 artifact hash, <=10.0-second readiness measurement, and disposable real WinVault lifecycle with `finally` cleanup | artifact hash, OS build/CPU/RAM/storage, startup duration, SmartScreen observation, WinVault value-free receipt, cleanup and no-secret scan | DOC-01 and final distribution claim |
| `EXT-REMOTE-PREP` | after explicit authorization, coordinator configures NJU GitLab, GitHub mirror, and public OCI registry; pushes reviewed branch tips (all contain F-01A push CI), opens one GitLab MR and GitHub PR per worktree, and publishes/pulls the reviewed DIST-02 digest without rebuilding | remote URLs; branch/commit/MR/PR mappings; visibility evidence showing GitHub public or named TA collaborator on private repo; push-trigger receipts for every branch tip; public image digest/SBOM; clean pull/run receipts | deployment prerequisite and DOC-01 |
| `D-025-HOST-CLOSE` | student selects host/cost/account/region and exact proxy/origin boundary; coordinator deploys only the public-registry digest closed by EXT-REMOTE-PREP and only after separate authorization | deployment command/config diff, same digest, HTTPS URL, Host/Origin/cookie/CSRF positive-negative tests, 360/1440 screenshots, mock/no-upload/no-key/no-egress proof | deployment, public URL, DOC-01 |
| `EXT-REMOTE-FINAL` | after DOC-01 and coordinator compliance update, coordinator scans/stages the final release branch, pushes the new tip to the existing GitLab MR/GitHub PR, merges without history rewrite, and observes the exact final course commit | final commit -> MR/PR mapping; authoritative NJU pipeline `unit-test` PASS; GitHub Actions PASS; immutable final commit IDs/timestamps | final course submission/completion claim |
| `REFLECTION-CLOSE` | student writes `REFLECTION.md` in 1500--2500 Chinese characters as required by the course text; AI may only review a supplied draft and record assistance | student-authored file and assistance declaration | final course completion |

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
| AC-18 | F-01B and QA-RELEASE |
| AC-19 | DIST-01, DIST-01-VM-CLOSE, and DOC-01 |
| AC-20 | DIST-02, CI-01, EXT-REMOTE-PREP, and EXT-REMOTE-FINAL |
| AC-21 | D-025-HOST-CLOSE and DOC-01 |
| AC-22 | per-task protocol and coordinator evidence commits |
| AC-23 | F-01S/F-01A/F-01B, all scans/reviews, DIST-01/02, DOC-01 |
| AC-24 | G-03 and `SPEC_PROCESS.md` |

The authoritative course matrix is `docs/REQUIREMENTS_COMPLIANCE_AUDIT.md`; before G-03 it must bind the final SPEC/PLAN hashes and map every hard row to these task IDs or named gates.

## 13. Deferred Scope and Recovery

The active tasks do not implement OCR/image/scanned PDF/bulk ingestion, whole-file F or durable remote jobs, past-exam/teacher-focus intelligence, or rubrics beyond mutex/race/deadlock. Their only plans are:

- `docs/superpowers/plans/archive/deferred-v2/advanced-material-ingestion.md`
- `docs/superpowers/plans/archive/deferred-v2/remote-f-and-durable-jobs.md`
- `docs/superpowers/plans/archive/deferred-v2/exam-material-intelligence.md`
- `docs/superpowers/plans/archive/deferred-v2/extended-concept-rubrics.md`

They remain `ARCHIVED / NOT DISPATCHABLE`. Recovery requires `brainstorming -> SPEC confirmation -> writing-plans`; no active task may silently absorb them.
