# ProjectB v1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` or `superpowers:executing-plans` to execute one task at a time. Every behavior task uses `superpowers:test-driven-development`; unexpected failures use `superpowers:systematic-debugging`; reviews use `superpowers:requesting-code-review` and `superpowers:receiving-code-review`; completion claims use `superpowers:verification-before-completion`; each worktree group closes with `superpowers:finishing-a-development-branch`.

**Status:** `SAME-HASH REVIEW CANDIDATE / NOT DISPATCHABLE`

**Confirmed SPEC:** annotated SHA-256 `795791627579BFEBE24717981168A54E2D546F613FEA84CCDF0AC0ECBA387862`; confirmed product-content SHA-256 `C6231816A62C807D205FC7A3E6142C5636DE18FD8A2C580B48E63B106F959AD6`.

**Goal:** Build the reduced v1 local study workbench: source-grounded material import and mapping, deterministic learning evidence for mutex/race/deadlock, and continuous/finals review planning, with an optional consent-bound OpenAI P adapter and a mock-only public demo.

**Architecture:** React/Vite calls a profile-aware FastAPI application. Domain services own authority; SQLite stores metadata and append-only evidence; a content-addressed current-user store keeps material bytes; Windows Credential Manager keeps secrets. Provider output is non-authoritative and replaceable by a deterministic mock. The local profile is loopback-only; the public demo exposes only synthetic licensed fixtures, ephemeral state, and the mock.

**Pinned stack:** CPython 3.14.6; FastAPI 0.139.2; Pydantic 2.13.4; SQLite; pypdf 6.14.2; pypdfium2 5.12.1; keyring 25.7.0; OpenAI SDK 2.46.0; pytest 9.1.1; Ruff 0.15.22; mypy 2.3.0; Node 24.18.0/npm 11.16.0; React 19.2.7; Vite 8.1.5; TypeScript 7.0.2; Vitest 4.1.10; Playwright 1.61.1; axe 4.12.1; PyInstaller 6.21.0. Windows, Linux-CI, Linux-demo, npm, OCI-base, and license evidence are frozen under `docs/engineering/`.

## 1. Dispatch Gates

No formal task dispatch, task-status change, implementation commit, or integration may start until all of these are true on the same final SPEC/PLAN bytes. G-03 is the only pre-dispatch exception: Claude Code works in a disposable copy containing only `SPEC.md` and `PLAN.md`, may create temporary scaffold solely to expose ambiguity, and may not commit, integrate, edit the real repository, or change the ledger. Its F-01A attempt leaves formal F-01A `not started`; only its questions, misunderstandings, output gap, and resulting documentation diff become evidence.

1. `SR-08`: mechanical audit, SPEC-compliance review, and quality/security/license review all report no Critical or Major issue and record both hashes externally.
2. `G-03`: a fresh Claude Code session, with only final `SPEC.md` and `PLAN.md`, attempts `F-01A` and records every question, misunderstanding, output gap, and repair in `SPEC_PROCESS.md`.
3. The repaired SPEC/PLAN snapshot is re-reviewed if either file changes.
4. `G-04`: after reading the cold-start record and repairs, the student explicitly approves implementation. The earlier SPEC confirmation is not G-04.

`D-025` hosting and `EXT-REMOTE-CLOSE` remote authorization do not block local implementation. They block remote mutation, final CI receipts, deployment, public URL, and `DOC-01` completion.

## 2. Worktrees, Ownership, and Order

After G-04, the coordinator creates `codex/implementation-v1` and these worktrees in order. A later worktree starts only from the locally integrated, reviewed predecessor. No implementation tasks are parallel: API/UI registries, migrations, and evidence ledgers have serialized ownership, and the reduced plan favors recoverable commits over merge concurrency.

| Worktree branch | Tasks, strictly in order | Closure |
| --- | --- | --- |
| `codex/foundation-v1` | F-01A -> F-01B -> F-02 -> F-03 -> F-04 -> F-05 | finish and locally integrate before M1 |
| `codex/m1-materials-v1` | M1-01 -> M1-02 -> M1-03 | finish and locally integrate before M2 |
| `codex/m2-learning-v1` | M2-01 -> M2-02 -> M2-03 -> M2-04 | finish and locally integrate before P-01 |
| `codex/m3-api-v1` | P-01 -> M3-01 -> M3-02 -> API-01 -> API-02 -> API-03 | finish and locally integrate before UI |
| `codex/webui-v1` | UI-01 -> UI-02 -> UI-03 -> UI-04 -> UI-05 -> UI-06 | finish and locally integrate before demo |
| `codex/demo-v1` | DEMO-01 | finish and locally integrate before provider adapter |
| `codex/provider-openai-v1` | P-02 | finish and locally integrate before distribution |
| `codex/distribution-v1` | DIST-01 -> DIST-02 | finish and locally integrate before CI |
| `codex/release-v1` | CI-01 -> external closures -> DOC-01 | no push, MR, PR, deployment, or publication without its named gate |

Only the root coordinator edits `PLAN.md`, `AGENT_LOG.md`, `SPEC_PROCESS.md`, or the compliance audit. Workers never stage those paths. Shared evidence updates happen after a terminal reviewed implementation hash exists.

## 3. Per-Task Protocol

Each task is one fresh subagent session with only its task card, confirmed SPEC, predecessor interfaces, exact commands, and owned paths.

`F-01A` alone uses its dependency-free PowerShell preflight and task-local bootstrap sequence because no committed project runtime exists yet. Only the not-yet-created Python/Node commands are exempt: red/green, staging only owned paths, both reviews, trailers, verification, logging, and commits still apply. Before every F-01A implementation/review-fix commit and the coordinator evidence commit, stage the intended files and run `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/bootstrap_scan_credentials.ps1 -Tracked -Staged`; any Git/read/decode/scan error fails closed and no matching value is printed. The protocol below applies literally from `F-01B` onward.

1. Run the worktree preflight and bind `$TaskId`, `$AgentId`, `$HumanChanges`, base commit, clean index, and predecessor hashes. Run the committed `scripts/bootstrap.ps1`, which provisions checksum-verified uv 0.11.14, CPython 3.14.6, and Node 24.18.0 under ignored project-local paths; it must never alter system PATH. Use its resolved `$Uv`, `$Py`, `$Node`, and `$Npm` paths. UI tasks additionally run `& $Npm --prefix frontend exec -- playwright install chromium`.
2. Write the named minimum failing test first. Run the exact red command and record its exit code plus the requirement-shaped failure. A missing test, import typo, or environment failure is not a valid red.
3. Implement the minimum behavior, run the exact green command, refactor under tests, then run `& $Py -m ruff check backend scripts`, `& $Py -m mypy backend/projectb`, `& $Py scripts/test_all.py`, `git diff --check`, `& $Py scripts/scan_credentials.py --tracked --staged`, and `& $Py scripts/verify_licenses.py` whenever those paths exist.
4. On any unexpected result, invoke `systematic-debugging` and log cause/evidence. Do not weaken, delete, skip, or mark a test expected-failure to obtain green.
5. Stage only owned paths, run the scanner again, and commit with the task card subject plus trailers `Task-ID: $TaskId`, `Agent: $AgentId`, and `Human-Changes: $HumanChanges`. No real key, model response, private material, generated database, build output, or browser profile may be staged.
6. Request a SPEC/acceptance review first. If it passes, request correctness, maintainability, security, test, and license review. Apply valid feedback through `receiving-code-review`, add a regression red when behavior changes, recommit, and repeat both reviews against the terminal commit. Critical issues stop the sequence.
7. Run `verification-before-completion` on the terminal commit. The coordinator then records timestamp, task ID, skill chain, exact prompt/context, canonical worker ID, red/green/regression receipts, both reviews, terminal commit, human edits/reason, lesson, and license/scan result in `AGENT_LOG.md`; it marks the PLAN ledger in a separate `docs(task): record evidence [agent: coordinator]` commit.
8. At the end of each worktree group, invoke `finishing-a-development-branch`. Local integration is allowed after G-04; remote push/PR/MR is forbidden until `EXT-REMOTE-CLOSE`.

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
| 1 | F-01A | G-04 | no: creates project-local toolchain | foundation | not started | none |
| 2 | F-01B | F-01A | no: creates shared quality gates | foundation | not started | none |
| 3 | F-02 | F-01B | no: migration order | foundation | not started | none |
| 4 | F-03 | F-02 | no: migration order | foundation | not started | none |
| 5 | F-04 | F-03 | no: security base | foundation | not started | none |
| 6 | F-05 | F-04 | no: security base | foundation | not started | none |
| 7 | M1-01 | F-05 | no: material contracts | m1-materials | not started | none |
| 8 | M1-02 | M1-01 | no: consumes extraction | m1-materials | not started | none |
| 9 | M1-03 | M1-02 | no: consumes material repo | m1-materials | not started | none |
| 10 | M2-01 | M1-03 | no: evaluator base | m2-learning | not started | none |
| 11 | M2-02 | M2-01 | no: registry assembly | m2-learning | not started | none |
| 12 | M2-03 | M2-02 | no: evidence authority | m2-learning | not started | none |
| 13 | M2-04 | M2-03 | no: mastery consumes evidence | m2-learning | not started | none |
| 14 | P-01 | M2-04 | no: provider port and mock | m3-api | not started | none |
| 15 | M3-01 | P-01 | no: planner contract | m3-api | not started | none |
| 16 | M3-02 | M3-01 | no: revision persistence | m3-api | not started | none |
| 17 | API-01 | M3-02 | no: creates app registry | m3-api | not started | none |
| 18 | API-02 | API-01 | no: modifies app registry | m3-api | not started | none |
| 19 | API-03 | API-02 | no: closes local API | m3-api | not started | none |
| 20 | UI-01 | API-03 | no: creates route registry | webui | not started | none |
| 21 | UI-02 | UI-01 | no: modifies route registry | webui | not started | none |
| 22 | UI-03 | UI-02 | no: modifies route registry | webui | not started | none |
| 23 | UI-04 | UI-03 | no: modifies route registry | webui | not started | none |
| 24 | UI-05 | UI-04 | no: modifies route registry | webui | not started | none |
| 25 | UI-06 | UI-05 | no: modifies route registry | webui | not started | none |
| 26 | DEMO-01 | UI-06 | no: profile assembly | demo | not started | none |
| 27 | P-02 | DEMO-01 + P-EVIDENCE | no: real adapter is isolated last | provider-openai | not started | none |
| 28 | DIST-01 | P-02 + QA-RELEASE | no: Windows release | distribution | not started | none |
| 29 | DIST-02 | DIST-01 | no: consumes frozen frontend/runtime | distribution | not started | none |
| 30 | CI-01 | DIST-02 | no: consumes all commands | release | not started | none |
| 31 | DOC-01 | CI-01 + EXT-REMOTE-CLOSE + D-025-HOST-CLOSE | no: final evidence only | release | not started | none |

## 5. Foundation Tasks

### F-01A: Reproducible project-local toolchain and frontend test harness

- **Dependencies / parallelism:** G-04; no, because this is the only task allowed to bootstrap without a committed project runtime.
- **Goal / files:** Materialize `.python-version`, `pyproject.toml`, the three reviewed Python locks, the reviewed `frontend/package.json`/`package-lock.json` and base configs, `frontend/src/foundation/RuntimeProbe.tsx`, `frontend/src/foundation/RuntimeProbe.test.tsx`, `scripts/bootstrap.ps1`, dependency-free `scripts/bootstrap_scan_credentials.ps1`, `scripts/tests/foundation_contract.ps1`, and `licenses/bootstrap/`. Bootstrap consumes the verifier-bound evidence in `docs/engineering/DEPENDENCY_BASELINE.md`: uv 0.11.14 from `https://github.com/astral-sh/uv/releases/download/0.11.14/uv-x86_64-pc-windows-msvc.zip` (SHA-256 `52ba5d19409aaa688a8a1a6ec8dfb6a4817230d20186e75f4006105c3e39a846`, Apache-2.0 OR MIT), CPython from `https://www.python.org/ftp/python/3.14.6/python-3.14.6-embed-amd64.zip` (SHA-256 `df901e84a896ff1ee720ad03377e0c8d8c2244fda79808aeeaff6316df1cb75c`, PSF-2.0), and Node/npm from `https://nodejs.org/dist/v24.18.0/node-v24.18.0-win-x64.zip` (SHA-256 `0ae68406b42d7725661da979b1403ec9926da205c6770827f33aac9d8f26e821`; Node MIT/bundled notices; npm 11.16.0 Artistic-2.0 notice). It validates bytes/versions before extraction, enables only the reviewed CPython site-packages path, uses project-local `uv.exe` to sync the Windows lock, resolves `node.exe`/`npm.cmd`, and never changes system PATH or registry. The bootstrap scanner uses Git's exact tracked/staged path sets, scans secret/private-key/plain-and-encoded shapes assembled safely by tests, reports paths and rule IDs only, and treats Git/read/decode errors as failures.
- **Red:** create dependency-free `scripts/tests/foundation_contract.ps1`; run `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/tests/foundation_contract.ps1`; expect missing bootstrap scanner, scanner positive/negative/fail-closed/redaction, artifact URL+hash+license, manifests/config, and runtime-probe assertions. This red requires only Windows PowerShell and may not use global Python, Node, npm, or uv.
- **Green/refactor:** implement the minimum toolchain/harness, run the task-local form of the common bootstrap, rerun the exact Red command, run `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/bootstrap_scan_credentials.ps1 -Tracked -Staged`, then run `& $Npm --prefix frontend exec -- vitest run src/foundation/RuntimeProbe.test.tsx`. The Vitest test must render a real React counter through JSDOM and Testing Library, reach it by accessible role/name, drive it with `user-event`, observe state change, and fail when the configured Node engine or DOM setup drifts; `expect(true)` and existence-only assertions are forbidden.
- **Done / commit:** exact project-local uv/CPython/Node/npm hashes and versions, canonical locks/manifests, retained bootstrap license texts, the fail-closed value-redacting staged/tracked bootstrap scanner, blocked-`npm.ps1`, corrupt-download/version-drift negatives, and the React/JSDOM interaction contract pass. Stage only owned paths, rerun the bootstrap scanner, then commit `build(F-01A): materialize reviewed toolchain [agent: worker]` with required trailers.

### F-01B: One-command runner, credential scanner, and license gates

- **Dependencies / parallelism:** F-01A; no, because every later task depends on these fail-closed quality commands.
- **Goal / files:** Create `scripts/test_all.py`, full `scripts/scan_credentials.py`, `scripts/verify_licenses.py`, `scripts/tests/test_quality_gates.py`, scanner fixtures that contain no credential-shaped literal, and `licenses/THIRD_PARTY_NOTICES.md`; retain the F-01A bootstrap scanner as the runtime-free fallback and prove the Python scanner is a strict superset. The runner invokes backend tests, the real foundation Vitest test, frontend build when its entry exists, contract checks, credential scan, and license verification with bounded child processes and propagated nonzero exits. Scanner covers plain/encoded secret shapes, private keys, false positives, staged/tracked scope, and child failure without echoing matches. License verification binds the reviewed Python/npm/bootstrap/OCI authorities and notices.
- **Red:** create `scripts/tests/test_quality_gates.py`; run `& $Py -m pytest scripts/tests/test_quality_gates.py -q`; expect missing runner/scanner/license-verifier, failure-propagation, redaction, notice, and exact-command assertions.
- **Green/refactor:** rerun the exact Red command, `& $Py scripts/scan_credentials.py --tracked --staged`, `& $Py scripts/verify_licenses.py`, the literal `python scripts/test_all.py` under the common bootstrap's process-local PATH, `& $Py scripts/test_all.py`, `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/verify_evidence.ps1`, and `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/verify_linux_dependency_evidence.ps1`.
- **Done / commit:** one-command orchestration, timeout/child failure propagation, credential redaction, full reviewed license/notices closure, and both literal/explicit Python invocations pass; no empty-suite or `passWithNoTests` path can yield green. Commit `build(F-01B): add fail-closed quality gates [agent: worker]`.

### F-02: Core metadata schema and unit of work

- **Dependencies / parallelism:** F-01B; no, because it creates migration 001 and the transaction base consumed by F-03.
- **Goal / files:** Create `backend/projectb/storage/db.py`, `storage/migrations/001_core.sql`, `repositories/uow.py`, and `backend/tests/storage/test_core_schema.py`. Own only Course, Material, SourceLocator, KnowledgeConcept, CoverageDecision, ProviderProfile, ConsentRecord, and AuditEvent schema, foreign keys, uniqueness, migration idempotency, and transaction boundaries.
- **Red:** `& $Py -m pytest backend/tests/storage/test_core_schema.py -q`; expect absent schema/migration and rollback behavior.
- **Green/refactor:** rerun the exact Red command, then run `BE-REGRESSION` and `LICENSE-SECURITY-GATE`.
- **Done / commit:** a fresh and an already-migrated database are deterministic; rollback leaves no partial row; schema fields match SPEC section 7. Commit `feat(F-02): add core sqlite schema [agent: worker]`.

### F-03: Learning and review schema constraints

- **Dependencies / parallelism:** F-02; no, because migration 002 is ordered after the reviewed core schema.
- **Goal / files:** Create `storage/migrations/002_learning.sql` and `backend/tests/storage/test_learning_schema.py` for Attempt, LearningEvidence, MasteryEstimate, ReviewPlanRevision, and ReviewTask. Enforce append-only evidence, idempotency keys, parent revisions, completed-task protection, and cascade/restrict rules.
- **Red:** `& $Py -m pytest backend/tests/storage/test_learning_schema.py -q`; expect missing tables/triggers and mutable-evidence rejection failure.
- **Green/refactor:** rerun the exact Red command, then run `BE-REGRESSION` and `LICENSE-SECURITY-GATE`.
- **Done / commit:** all 13 entities and deletion rules are mechanically tested without feature repositories. Commit `feat(F-03): add learning sqlite constraints [agent: worker]`.

### F-04: HTTP trust, session-bound CSRF, safe errors, and audit whitelist

- **Dependencies / parallelism:** F-03; no, because later credentials and APIs consume this single trust/audit contract.
- **Goal / files:** Create `backend/projectb/security/http.py`, `observability/audit.py`, `backend/tests/security/test_http_boundary.py`, and `test_audit_redaction.py`. Local policy permits loopback Host/Origin only; unsafe methods require a session-bound CSRF token; valid tokens replayed in another session fail; errors/logs expose no bodies, paths, answers, fragments, or secrets.
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
- **Goal / files:** Create `domain/materials/models.py`, `services/materials/extract_text.py`, and parser tests/fixtures with recorded licenses. Hash original bytes before decoding. UTF-8 TXT/MD yields stable one-based line locators. For digital PDF, pypdfium2 validates readability/page count and pypdf extracts per-page text; disagreement, encryption, zero usable text, and scanned PDFs fail before persistence. Parsing runs in a terminable worker with a 30-second per-file deadline; timeout kills the process tree, deletes temporary output, and returns a stable retryable error. Parser ID/version is immutable material-version metadata; a parser change creates a new version and cannot rewrite an old locator.
- **Red:** `& $Py -m pytest backend/tests/materials/test_text_extraction.py backend/tests/materials/test_pdf_extraction.py -q`; expect hash/locator/golden/scanned-PDF failures plus deterministic timeout, process termination, temporary cleanup, and parser-upgrade immutability failures.
- **Green/refactor:** rerun the exact Red command, then run `BE-REGRESSION` and `LICENSE-SECURITY-GATE`.
- **Done / commit:** raw hash, immutable parser/version fingerprint, new-version-on-upgrade, page/line bounds, magic/type checks, 30-second retryable timeout cleanup, and deterministic golden fixtures pass. Commit `feat(M1-01): extract source-located materials [agent: worker]`.

### M1-02: Atomic incremental import and content store

- **Dependencies / parallelism:** M1-01; no, because import consumes the reviewed byte hash and locator output.
- **Goal / files:** Create `services/materials/importer.py`, `repositories/materials.py`, `storage/content_store.py`, and `backend/tests/materials/test_importer.py`. Preflight at most 5 files and 50 MiB total before any authoritative write; each file is at most 20 MiB, each PDF at most 200 pages, and decoded TXT/Markdown at most 1,000,000 Unicode code points. Preserve successful sibling files, report per-file outcomes, roll back a failed/timed-out file and its temporary bytes, and deduplicate same-course raw hashes.
- **Red:** `& $Py -m pytest backend/tests/materials/test_importer.py -q`; expect atomicity, idempotency, content-address, mixed-batch timeout, and `limit-1 / limit / limit+1` failures for file count, batch bytes, file bytes, PDF pages, and Unicode code points.
- **Green/refactor:** rerun the exact Red command, then run `BE-REGRESSION` and `LICENSE-SECURITY-GATE`.
- **Done / commit:** exact SPEC limits and preflight ordering pass; no half-written Material/content/temp bytes survive failure or timeout; same input is idempotent; mixed batch outcomes are recoverable. Commit `feat(M1-02): import materials atomically [agent: worker]`.

### M1-03: Concepts, confirmed coverage, and deletion

- **Dependencies / parallelism:** M1-02; no, because coverage and deletion consume the reviewed material repository.
- **Goal / files:** Create `repositories/coverage.py`, `services/materials/coverage.py`, `services/materials/delete.py`, and `backend/tests/materials/test_coverage.py`. Mapping is append-only confirmed/rejected history; only confirmed current-hash locators authorize learning. Delete removes local bytes and invalidates future use without deleting historical evidence.
- **Red:** `& $Py -m pytest backend/tests/materials/test_coverage.py -q`; expect unconfirmed/stale locator authorization and deletion failures.
- **Green/refactor:** rerun the exact Red command, then run `BE-REGRESSION` and `LICENSE-SECURITY-GATE`.
- **Done / commit:** multiple concepts, explicit confirmation, stale-source fail-close, and deletion semantics satisfy AC-03/04. Commit `feat(M1-03): bind concepts to confirmed sources [agent: worker]`.

## 7. M2 Learning Tasks

### M2-01: Evaluator contract and mutex rubric

- **Dependencies / parallelism:** M1-03; no, because evaluator authority requires current confirmed coverage.
- **Goal / files:** Create `domain/learning/evaluators/base.py`, `mutex.py`, `registry.py`, schemas, and `backend/tests/learning/test_mutex_evaluator.py`. Rubrics are versioned, deterministic, source-bound, and return structured outcomes; concepts without an evaluator are explanation-only and cannot create mastery evidence.
- **Red:** `& $Py -m pytest backend/tests/learning/test_mutex_evaluator.py -q`; expect missing golden/negative determinism and explanation-only guard.
- **Green/refactor:** rerun the exact Red command, then run `BE-REGRESSION` and `LICENSE-SECURITY-GATE`.
- **Done / commit:** mutex evaluator and registry base pass repeated/shuffled fixture tests. Commit `feat(M2-01): add deterministic mutex evaluator [agent: worker]`.

### M2-02: Race and deadlock rubrics plus registry assembly

- **Dependencies / parallelism:** M2-01; no, because this task is the only serialized modifier of the evaluator registry.
- **Goal / files:** Create `evaluators/race.py`, `evaluators/deadlock.py`, their two test files, and serially update `registry.py`. Race checks shared access/concurrency/order; deadlock checks resources/hold-wait/cycle/progress. Each has golden, near-miss, invalid, and stable-order fixtures.
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
- **Goal / files:** Create `providers/port.py`, `providers/mock.py`, `providers/registry.py`, `repositories/provider_profiles.py`, `services/providers/consent.py`, and provider tests. Define exactly `generate_explanation`, `generate_practice_candidate`, and `generate_feedback_wording`; every candidate is non-authoritative. Feedback input accepts only deterministic rubric output plus confirmed current-hash sources and rejects the original answer. The production local registry defaults to L with no adapter; it reserves only the built-in OpenAI adapter slot for explicit P. Deterministic mock is dependency-injected only in tests and demo, and local profile must reject it. Immutable consent binds port, exact locator/hash/fragment preview, profile, policy fingerprint, configured token/cost caps, and request nonce; no match means zero network calls.
- **Red:** `& $Py -m pytest backend/tests/providers/test_consent.py backend/tests/providers/test_mock.py -q`; expect three-port schema, feedback-answer exclusion, consent mismatch/reuse/stale-source/network-count, local-no-provider, and local-rejects-mock failures.
- **Green/refactor:** rerun the exact Red command, then run `BE-REGRESSION` and `LICENSE-SECURITY-GATE`.
- **Done / commit:** all three ports and their least-data input contracts pass; L performs zero calls, local rejects mock, test/demo injection covers success/schema/timeout/error deterministically, and provider candidates cannot write coverage/evidence/mastery/plan. Commit `feat(P-01): add consent-bound provider port [agent: worker]`.

### M3-01: Pure continuous and finals planner

- **Dependencies / parallelism:** P-01; no, because the serial worktree freezes authority/provider ports before planning.
- **Goal / files:** Create `domain/review/planner.py` and `backend/tests/review/test_planner.py`. Implement ReviewPolicy v1 as a pure function: mode is `continuous` or `finals`; IANA timezone is required; daily budget is 10--120 minutes in steps of 5 with default 30; tasks are fixed 10 minutes and never split/overrun the budget; base intervals are exactly `[1,3,7,14,30]` local days; stable priority is evidence weakness, requested date, then concept ID; system/source errors never become learning failures. Continuous covers 30 local days. Finals requires a local exam date, schedules nothing after it, and an already-past date yields zero tasks plus archived state. Stale sources are excluded.
- **Red:** `& $Py -m pytest backend/tests/review/test_planner.py -q`; expect table-driven mode/timezone/default/step/range, fixed-duration/budget, exact-interval, weakness/date/concept tie-break, error-neutrality, 30-day horizon, finals cutoff/past-date archive, stale-source, and repeat-hash failures.
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
- **Goal / files:** Create `api/routes/review.py`, `credentials.py`, `settings.py`, `profiles/local.py`, `profiles/registry.py`, serially update `api/app.py`, and add API plus `backend/tests/system/test_performance.py`. Credential responses are value-free; first run is explicitly unconfigured; local bind is `127.0.0.1`; cached non-import API p95 is under 500 ms on the recorded fixture/reference host.
- **Red:** `& $Py -m pytest backend/tests/api/test_review_settings_routes.py backend/tests/system/test_performance.py -q`; expect 404, secret-shape, first-run, revision, and p95 failures.
- **Green/refactor:** rerun the exact Red command, then run `BE-REGRESSION` and `LICENSE-SECURITY-GATE`.
- **Done / commit:** complete local API assembly, settings validation, credential lifecycle, planner revisions, and measured performance pass. Commit `feat(API-03): close local api profile [agent: worker]`.

## 9. WebUI Tasks

UI tasks own one view and its CSS module/test/E2E file. `frontend/src/app/routes.tsx` is a serialized handoff UI-01 -> UI-06. Every task introduces its own responsive/keyboard/axe red; there is no later fabricated visual failure.

### UI-01: Open Design run, tokens, shell, client, and browser harness

- **Dependencies / parallelism:** API-03; no, because it creates the only frontend route registry and browser harness.
- **Goal / files:** Use the real Open Design project/run with `frontend-design` and `default`/Neutral Modern; record project/run/artifact/screenshots/license in `docs/engineering/OPEN_DESIGN_RUN.md`. Create tokens, global CSS, `App.tsx`, `routes.tsx`, API client, capability model, Playwright config, test-server launcher, and shell tests. Generated design is evidence only until the red test runs.
- **Red:** `& $Npm --prefix frontend exec -- vitest run src/app/Shell.test.tsx` and `& $Npm --prefix frontend exec -- playwright test e2e/shell.spec.ts`; expect missing four-stage navigation, 360/768/1440 layout, keyboard, and axe assertions.
- **Green/refactor:** run `& $Npm --prefix frontend exec -- playwright install chromium`, rerun both exact Red commands, then run `FE-REGRESSION` and `LICENSE-SECURITY-GATE`.
- **Done / commit:** real Open Design evidence exists; compact workbench shell has no hero/nested cards/overflow, radius <=8 px and letter spacing 0. Commit `feat(UI-01): build opendesign workbench shell [agent: worker]`.

### UI-02: Import view

- **Dependencies / parallelism:** UI-01; no, because it serially registers `/import` in `routes.tsx`.
- **Goal / files:** Create `views/import/ImportView.tsx`, CSS module, unit/E2E tests, and serially register `/import`. Show limits, selected files, per-file progress/result, recoverable errors, and existing material list; use icons with tooltips for icon-only actions.
- **Red:** run `& $Npm --prefix frontend exec -- vitest run src/views/import/ImportView.test.tsx` and `& $Npm --prefix frontend exec -- playwright test e2e/import.spec.ts`; expect upload/results/responsive/keyboard/axe failures.
- **Green/refactor:** rerun both exact Red commands, then run `FE-REGRESSION` and `LICENSE-SECURITY-GATE`.
- **Done / commit:** AC-01 import flow works at all three viewports without hiding failures. Commit `feat(UI-02): add material import view [agent: worker]`.

### UI-03: Mapping and source inspection view

- **Dependencies / parallelism:** UI-02; no, because it serially registers `/mapping` in `routes.tsx`.
- **Goal / files:** Create `views/mapping/MappingView.tsx`, CSS module, tests, and register `/mapping`. Present source fragments with page/line locators, multiple concepts, explicit confirm/reject, stale markers, and delete confirmation.
- **Red:** run `& $Npm --prefix frontend exec -- vitest run src/views/mapping/MappingView.test.tsx` and `& $Npm --prefix frontend exec -- playwright test e2e/mapping.spec.ts`; expect source/confirmation/stale/delete/responsive/keyboard/axe failures.
- **Green/refactor:** rerun both exact Red commands, then run `FE-REGRESSION` and `LICENSE-SECURITY-GATE`.
- **Done / commit:** unconfirmed mappings are visibly non-authoritative; source and destructive actions remain inspectable. Commit `feat(UI-03): add source mapping view [agent: worker]`.

### UI-04: Source-bound learning and consent view

- **Dependencies / parallelism:** UI-03; no, because it serially registers `/learning` in `routes.tsx`.
- **Goal / files:** Create `views/learning/LearningView.tsx`, CSS module, tests, and register `/learning`. Show sources, explanation, structured practice, deterministic rubric/evidence state, explanation-only state, optional feedback wording, provider candidate labeling, exact P preview, caps, and confirmation. The consent preview shows that feedback sends rubric/current source but not the student's original answer.
- **Red:** run `& $Npm --prefix frontend exec -- vitest run src/views/learning/LearningView.test.tsx` and `& $Npm --prefix frontend exec -- playwright test e2e/learning.spec.ts`; expect source/rubric/feedback-answer-exclusion/consent/no-authority/responsive/keyboard/axe failures.
- **Green/refactor:** rerun both exact Red commands, then run `FE-REGRESSION` and `LICENSE-SECURITY-GATE`.
- **Done / commit:** model content is identifiable and cannot appear as grading/mastery; no consent means no call. Commit `feat(UI-04): add grounded learning view [agent: worker]`.

### UI-05: Review planner and revision diff view

- **Dependencies / parallelism:** UI-04; no, because it serially registers `/review` in `routes.tsx`.
- **Goal / files:** Create `views/review/ReviewView.tsx`, CSS module, tests, and register `/review`. Show today's budget, task sources, mastery, continuous/finals controls, exam cutoff, revision diff, completion, and recovery.
- **Red:** run `& $Npm --prefix frontend exec -- vitest run src/views/review/ReviewView.test.tsx` and `& $Npm --prefix frontend exec -- playwright test e2e/review.spec.ts`; expect budget/mode/diff/recovery/responsive/keyboard/axe failures.
- **Green/refactor:** rerun both exact Red commands, then run `FE-REGRESSION` and `LICENSE-SECURITY-GATE`.
- **Done / commit:** deterministic plan/revision behavior is visible without rewriting completed tasks. Commit `feat(UI-05): add review planning view [agent: worker]`.

### UI-06: Settings, first-run credential guidance, privacy, and deletion

- **Dependencies / parallelism:** UI-05; no, because it serially registers `/settings` and freezes the route registry.
- **Goal / files:** Create `views/settings/SettingsView.tsx`, CSS module, tests, and register `/settings`. First-run guidance uses a hidden password control; status/update/clear never echo values; show local/P privacy boundary, provider profile/caps, data location, security state, material deletion, and demo capability restrictions.
- **Red:** run `& $Npm --prefix frontend exec -- vitest run src/views/settings/SettingsView.test.tsx` and `& $Npm --prefix frontend exec -- playwright test e2e/settings.spec.ts`; expect hidden-input/no-echo/status/delete/responsive/keyboard/axe failures.
- **Green/refactor:** rerun both exact Red commands, then run `FE-REGRESSION` and `LICENSE-SECURITY-GATE`.
- **Done / commit:** first-run credential path and privacy/security controls satisfy AC-14/16 without visible instructional feature copy. Commit `feat(UI-06): add secure settings view [agent: worker]`.

## 10. Demo, Provider Adapter, Distribution, CI, and Docs

### DEMO-01: Mock-only public demo profile

- **Dependencies / parallelism:** UI-06; no, because it is the only profile-registry modifier after local assembly.
- **Goal / files:** Create `profiles/demo.py`, synthetic CC0 fixture manifests/content, `backend/tests/demo/`, `frontend/e2e/demo.spec.ts`, and serially update the profile registry. Demo has one course, <=20 fixtures, ephemeral SQLite, 30-minute idle/two-hour absolute sessions, no upload/credential/OpenAI routes, no cross-session state, and a process-wide outbound deny guard.
- **Trust contract:** local Docker smoke requires `PROJECTB_DEMO_LOCAL_SMOKE=1` and permits only `http://127.0.0.1:7860`; public mode refuses startup without one exact HTTPS `PROJECTB_PUBLIC_ORIGIN`, derives Host/Origin allowlists without wildcards, uses HttpOnly/SameSite=Lax/Secure cookies, session-bound CSRF, and rejects forwarded headers unless D-025 supplies an exact trusted-proxy boundary.
- **Red:** `& $Py -m pytest backend/tests/demo -q` and `& $Npm --prefix frontend exec -- playwright test e2e/demo.spec.ts`; expect forbidden-route, egress, TTL, cross-session, public-origin, and fixture-license failures.
- **Green/refactor:** rerun both exact Red commands, then run `BE-REGRESSION`, `FE-REGRESSION`, and `LICENSE-SECURITY-GATE`.
- **Done / commit:** same UI/domain contracts run on licensed synthetic data; forbidden capabilities are absent, not merely hidden. Commit `feat(DEMO-01): add isolated mock demo [agent: worker]`.

### P-02: P-only OpenAI adapter from the reviewed policy snapshot

- **Dependencies / parallelism:** DEMO-01, P-01, and P-EVIDENCE; no, because it is isolated after the mock-complete core and is the only production-adapter registry modifier.
- **Goal / files:** Consume read-only `docs/engineering/PROVIDER_POLICY_V1_P_EVIDENCE.md` and `scripts/verify_provider_policy_v1.ps1`; create `providers/openai_adapter.py`, mechanically derived `providers/policy.v1.json`, adapter tests, and serially update P-01's `providers/registry.py`. The reviewed evidence SHA-256 is `35a3f46e036563e3fc681df3190eb56336ab48b9d9817ad48f4d5df42230f076`; it is P-only, expires after 30 days, allowlists exact model IDs/pricing, and excludes direct PDF/File/Vector Store/hosted tools/F mode. Mock HTTP transport tests, not the deterministic provider adapter and not a real key/paid call, prove request/response behavior.
- **Contract:** local production remains in L with no selected provider until the user explicitly enables P; its registry permits only the built-in OpenAI adapter with a fresh policy, configured credential status, allowlisted model, and explicit input/output caps. Deterministic provider mock remains absent from local and registered only by test/demo profiles. Consent displays the computed maximum cost. Adapter sends only confirmed extracted fragments through Responses API with `store:false`, 60-second timeout, zero automatic retries, strict output schema, no student answer, and no network when snapshot is absent/stale or consent mismatches.
- **Red:** first require `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/verify_provider_policy_v1.ps1` to pass; then run `& $Py -m pytest backend/tests/providers/test_openai_adapter.py -q`; expect missing adapter/derived policy/registry update plus local-rejects-mock, unconfigured-L, stale-fixture, forbidden-field, schema, timeout, and zero-network failures.
- **Green/refactor:** if and only if evidence expired, return to the coordinator for an official-source refresh; otherwise rerun the verifier and exact Red test, then run `BE-REGRESSION` and `LICENSE-SECURITY-GATE`.
- **Done / commit:** P-only evidence and adapter are hash-bound; no F/direct-file behavior leaks into v1. Commit `feat(P-02): add governed openai p adapter [agent: worker]`.

### QA-RELEASE: Verification-only gate

This is not a dispatch task and owns no file. From a clean worktree, run the common bootstrap, `& $Npm --prefix frontend exec -- playwright install chromium`, `BE-REGRESSION`, `FE-REGRESSION`, `& $Npm --prefix frontend exec -- playwright test`, `LICENSE-SECURITY-GATE`, `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/verify_evidence.ps1`, `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/verify_linux_dependency_evidence.ps1`, and `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/verify_provider_policy_v1.ps1`. Playwright config runs 360/768/1440 projects. Any failure returns to the owning task with a defect-specific red test. QA-RELEASE may not repair feature behavior itself.

### DIST-01: Windows x64 single-file distribution

- **Dependencies / parallelism:** P-02 and QA-RELEASE; no, because it freezes the complete local application resources.
- **Goal / files:** Create `packaging/windows/build.ps1`, PyInstaller spec/hooks, `smoke_test.ps1`, distribution contract tests, and `docs/engineering/DIST-01_EVIDENCE.md`. Build one `ProjectB.exe`; mutable data stays under `%LOCALAPPDATA%\ProjectB` or explicit data root; bind loopback only; embed WebUI and notices.
- **Red:** `& $Py -m pytest backend/tests/distribution/test_windows_contract.py -q`; expect missing single-file/resource/data-root/bind/startup/WinVault assertions.
- **Green/refactor:** rerun the exact Red command; run `powershell -NoProfile -ExecutionPolicy Bypass -File packaging/windows/build.ps1 -Python $Py -Output dist/ProjectB.exe`, `& $Py scripts/scan_credentials.py --tracked --staged`, and `powershell -NoProfile -ExecutionPolicy Bypass -File packaging/windows/smoke_test.ps1 -Artifact dist/ProjectB.exe -DataRoot tmp/dist01-smoke`. Repeat the smoke script against the exact artifact hash on a clean Windows 11 x64 reference VM with 2 vCPU, 8 GiB RAM, SSD, and no Python/Node/Docker; measure process start through health and WebUI readiness <=10.0 seconds, and run a disposable real WinVault set/status/update/clear with guaranteed `finally` cleanup.
- **Done / commit:** artifact hash, OS build/CPU/RAM/storage, startup duration, SmartScreen observation, clean-host prerequisites, no-secret scan, and smoke receipts are recorded. Commit `build(DIST-01): package windows single file [agent: worker]`.

### DIST-02: Reproducible linux/amd64 mock OCI image

- **Dependencies / parallelism:** DIST-01; no, because it consumes the frozen frontend/resource layout and shared notice bundle.
- **Goal / files:** Create `packaging/oci/Dockerfile`, entrypoint, `.dockerignore`, smoke script, OCI contract tests, SBOM/notices, and `docs/engineering/DIST-02_EVIDENCE.md`. Pin Node builder and Python runtime by reviewed linux/amd64 manifest digest; install only the hashed demo lock; run non-root with tmpfs, healthcheck, egress deny, and demo profile.
- **Red:** `& $Py -m pytest backend/tests/distribution/test_oci_contract.py -q`; expect floating-image, Windows-lock, root, persistence, egress, notice/SBOM, public-origin, and forbidden-capability failures.
- **Green/refactor:** rerun the exact Red command and `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/verify_linux_dependency_evidence.ps1`; run `docker build --platform linux/amd64 --file packaging/oci/Dockerfile --tag projectb-demo:local .`, then `docker run -d --rm --name projectb-demo-smoke --read-only --tmpfs /tmp/projectb-demo:rw,size=64m -e PROJECTB_DEMO_LOCAL_SMOKE=1 -p 127.0.0.1:7860:7860 projectb-demo:local`. In `try/finally`, run `powershell -NoProfile -ExecutionPolicy Bypass -File packaging/oci/smoke_test.ps1 -Container projectb-demo-smoke -Image projectb-demo:local -BaseUrl http://127.0.0.1:7860`, `docker image inspect projectb-demo:local`, and finally `docker rm -f projectb-demo-smoke`. The smoke script must fail on wrong architecture/user/history/filesystem, missing SBOM/notices, persistence, forbidden routes, provider egress, or nonzero network count.
- **Done / commit:** clean build, exact local run command, automated inspect/SBOM/license checks, and local-browser demo pass; record the local image ID/digest without a registry push or deployment claim. Commit `build(DIST-02): package mock demo image [agent: worker]`.

### CI-01: Dual CI definitions and local contract

- **Dependencies / parallelism:** DIST-02; no, because CI consumes every final local test and distribution command.
- **Goal / files:** Create `.gitlab-ci.yml`, `.github/workflows/ci.yml`, `scripts/verify_ci_contract.py`, CI contract tests, and `docs/engineering/CI-01_EVIDENCE.md`. GitLab has a job named exactly `unit-test`; Python, frontend, and distribution jobs consume pinned images/locks and run on push. GitHub actions use full reviewed commit SHAs and least permissions.
- **Red:** `& $Py -m pytest backend/tests/contracts/test_ci_files.py -q`; expect absent `unit-test`, push triggers, lock parity, action pin, and distribution commands.
- **Green/refactor:** rerun the exact Red command, run `& $Py scripts/verify_ci_contract.py`, `BE-REGRESSION`, `FE-REGRESSION`, and `LICENSE-SECURITY-GATE`, then locally execute every command named by both CI files. Remote status remains `not_executed` until authorization.
- **Done / commit:** both definitions are locally validated and map to the same test/build contracts; no CI PASS is claimed yet. Commit `ci(CI-01): define gitlab and github pipelines [agent: worker]`.

### DOC-01: Final README, compliance, notices, and release evidence

- **Dependencies / parallelism:** CI-01, EXT-REMOTE-CLOSE, and D-025-HOST-CLOSE; no, because it records terminal remote/deployment facts and must not predict them.
- **Goal / files:** Finalize `README.md`, notices/license index, compliance audit, distribution/CI/deployment evidence links, known limitations, `scripts/verify_links.py`, and its tests. `REFLECTION.md` remains student-authored and is never created or filled by this task.
- **Red:** `& $Py -m pytest backend/tests/contracts/test_readme.py -q`; expect missing project/install/run/distribution/tree/security/credential/limits/deployment/CI/license sections or unverified URL/status claims.
- **Green/refactor:** after both external closure receipts, rerun the exact Red command, `& $Py scripts/verify_links.py`, `BE-REGRESSION`, `FE-REGRESSION`, `LICENSE-SECURITY-GATE`, strict evidence checks, and an external-browser HTTPS acceptance against the exact deployed image digest.
- **Done / commit:** README contains only observed commands/results, final public URL, architecture, CI/CD, credential guidance, third-party sources/licenses, and limitations; compliance rows are implemented/verified or honestly gated. Commit `docs(DOC-01): publish verified project guide [agent: worker]`.

## 11. External Closure Gates

| Gate | Required actor/action | Exact closure evidence | Blocks |
| --- | --- | --- | --- |
| `P-EVIDENCE` | closed locally on 2026-07-25; coordinator refreshes only after expiry or official drift, with no account/key/call | evidence SHA-256 `35a3f46e036563e3fc681df3190eb56336ab48b9d9817ad48f4d5df42230f076`; `PROVIDER_V1_P_EVIDENCE_PASS rows=7 models=2 expires=2026-08-25`; no F/File/tool behavior | P-02 only if the snapshot expires |
| `EXT-REMOTE-CLOSE` | student selects the authoritative NJU Git/GitLab remote, GitHub mirror, and public OCI registry, then explicitly authorizes each remote mutation. Coordinator pushes the nine reviewed branches in order, creates/merges an NJU GitLab MR and a GitHub PR for every worktree branch, publishes the reviewed DIST-02 image without rebuilding it, pulls it back from the public registry by digest on a clean host, runs the exact DIST-02 smoke, and never force-pushes | both remote URLs; nine branch/commit -> GitLab MR -> GitHub PR mappings with worker/human attribution; final NJU pipeline exact `unit-test` PASS; GitHub Actions PASS; public `registry/repository@sha256:...` reference equal to reviewed local image; SBOM/signature-or-unsigned note; pull-by-digest and clean-host run receipts; timestamps | any push/MR/PR, image publication, final remote CI, deployment prerequisite, and DOC-01 |
| `D-025-HOST-CLOSE` | student selects host/cost/account/region and exact proxy/origin boundary; coordinator deploys only the public-registry digest closed by EXT-REMOTE-CLOSE and only after separate authorization | deployment command/config diff, the same public image digest, HTTPS URL, Host/Origin/cookie/CSRF positive-negative tests, external 360/1440 browser screenshots, mock/no-upload/no-key/no-egress proof | deployment, public URL, DOC-01 |
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
| AC-19 | DIST-01 and DOC-01 |
| AC-20 | DIST-02, CI-01, EXT-REMOTE-CLOSE |
| AC-21 | D-025-HOST-CLOSE and DOC-01 |
| AC-22 | per-task protocol and coordinator evidence commits |
| AC-23 | F-01A/F-01B, all scans/reviews, DIST-01/02, DOC-01 |
| AC-24 | G-03 and `SPEC_PROCESS.md` |

The authoritative course matrix is `docs/REQUIREMENTS_COMPLIANCE_AUDIT.md`; before G-03 it must bind the final SPEC/PLAN hashes and map every hard row to these task IDs or named gates.

## 13. Deferred Scope and Recovery

The active tasks do not implement OCR/image/scanned PDF/bulk ingestion, whole-file F or durable remote jobs, past-exam/teacher-focus intelligence, or rubrics beyond mutex/race/deadlock. Their only plans are:

- `docs/superpowers/plans/archive/deferred-v2/advanced-material-ingestion.md`
- `docs/superpowers/plans/archive/deferred-v2/remote-f-and-durable-jobs.md`
- `docs/superpowers/plans/archive/deferred-v2/exam-material-intelligence.md`
- `docs/superpowers/plans/archive/deferred-v2/extended-concept-rubrics.md`

They remain `ARCHIVED / NOT DISPATCHABLE`. Recovery requires `brainstorming -> SPEC confirmation -> writing-plans`; no active task may silently absorb them.
