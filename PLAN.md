# ProjectB v1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Every task is assigned to a fresh context, follows red-green-refactor, receives a two-stage review, and uses checkbox syntax for tracking.

**Goal:** Build the confirmed ProjectB single-user, local-first course learning workbench for Windows x64, with source-traceable material import, constrained AI assistance, deterministic understanding checks and review planning, a responsive WebUI, a safe public mock demo, and reproducible Windows/OCI distribution evidence.

**Architecture:** A Python/FastAPI application owns all authoritative domain state in SQLite and exposes one loopback/WebUI contract. React/Vite/TypeScript renders the browser experience. Material parsing, deterministic learning rules, credential handling, audit, and the provider-neutral adapter boundary are separate application services; the only local production adapter is the built-in OpenAI reference adapter, while deterministic mock is limited to tests/demo. The Windows deliverable is a single ProjectB.exe; the public deployment uses the same domain contracts in an OCI demo profile with synthetic/licensed fixtures and expiring isolated sessions.

**Tech Stack:** Python + FastAPI, React + Vite + TypeScript, SQLite, Windows Credential Manager through a verified keyring adapter, a verified parser/render stack, a verified OpenAI HTTP/SDK client behind a provider-neutral protocol, pytest/Vitest/Playwright (or the exact verified equivalents), and a verified Windows freezer. These are architecture placeholders only: exact package names, versions, licenses, provider capabilities, and hosting terms are evidence-gated in Task G-02. G-02 must replace every placeholder with a cited, locked value before T-01 or any implementation task is dispatched; no fresh agent may invent or run an unspecified equivalent.

## Global Constraints

- The student confirmed SPEC.md as the v1 contract on 2026-07-20. This plan implements that contract and cannot silently change its numeric limits, ReviewPolicy v1, source semantics, or scope.
- First release is one local actor on Windows x64. No registration, login, multi-tenancy, sharing, LAN listener, or private-course public persistence.
- The WebUI is mandatory. The local server binds loopback only; Host/Origin and CSRF checks protect state-changing requests.
- Material modes are L (local), P (consented page/fragment remote), and F (consented whole-file/course remote). No body parsing or remote call occurs before the exact policy and file/batch ConsentRecord exist.
- M1 accepts only lecture, answer-free past_paper, and teacher_focus roles. Answer keys, personal notes, assignments/submissions, textbooks, unknown roles, and suspected leaked answers fail closed.
- SourceLocator is the only material-fact reference. A missing, stale, ambiguous, or hash-mismatched locator cannot become coverage, exam analysis, plan input, or source evidence.
- The first vertical learning slice is the mutex/race-condition chain. Its oracle, rubric, and evidence transitions are deterministic; provider wording cannot alter correctness or mastery.
- ReviewPolicy v1 is fixed: budget 10–480 minutes in steps of 5, defaults 30/90, task durations 5/10/15/20/30, intervals [1,3,7,14,30], stable ordering, versioned tzdata, and the exact continuous/finals/post-exam semantics in SPEC.md.
- The first release has named constrained ports only: propose_concept_coverage, generate_explanation, generate_practice_candidate, analyze_exam_material, and generate_feedback. There is no autonomous agent loop, arbitrary tool dispatch, or model authority over coverage, plan, priority, mastery, consent, or deletion.
- Local production registers only the built-in OpenAI adapter. Deterministic mock is registered only in test/demo profiles. No arbitrary base_url, endpoint, dynamic adapter, plugin, or unknown profile field is accepted.
- Secrets are entered invisibly and stored only through the verified Windows Credential Manager backend. Config, SQLite, browser state, logs, snapshots, tests, .env, and Git never contain secret values. Status exposes configured/unconfigured and timestamp only.
- All model requests carry port/version, scope, limits, idempotency key, profile/config/capability/policy fingerprints, and a response schema. Responses use store:false and disable non-essential hosted state/tools; policy snapshots must separately describe retention and deletion facts.
- Public demo accepts only built-in synthetic or explicitly licensed fixtures, uses deterministic mock, forbids upload/credentials/provider egress/private persistence, and enforces the confirmed session, size, concurrency, and rate limits.
- Before formal implementation, Open Design MCP and an actual design system/skill must be verified and recorded; the existing HTML mockup is brainstorming evidence only.
- Before formal implementation, a different-type fresh agent must perform the required cold-start attempt using only SPEC.md and PLAN.md. D-005 (the agent type) remains a student decision and is not selected by this plan.
- Every task uses a short-lived dedicated worktree/branch as mapped in Task G-04, records red and green evidence, runs the relevant and full test entry points, passes a SPEC-compliance review and a quality/security/license review, then records its commit hash in PLAN.md and AGENT_LOG.md. The module worktrees listed by G-04 are merge destinations, not permission to implement several PLAN tasks in one context. Remote pushes, PR/MR creation, and deployment require execution-time user authorization.

## Fresh-context dispatch-unit rule

Rows labelled **Task Group** are planning containers only. They are never dispatched, never receive a worker commit, and never count as completed on their own. Every `### Task <unit-id>` row is one fresh-agent unit with one coherent contract, one short-lived worktree/branch, one red-to-green gate, two reviews, and one commit. A group is complete only when every child unit has its own evidence and hash. If a unit still contains independent contracts, split it before dispatch rather than hiding the split in a prompt.

| Planning group | Dispatch units (each independently executable) |
| --- | --- |
| G-02 | G-02A toolchain/dependency/license baseline; G-02B provider policy/cost evidence; G-02C distribution/hosting evidence |
| T-03 | T-03A schema/migration; T-03B course/material repositories; T-03C learning/remote repositories and tombstones |
| X2-03 | X2-03A F enqueue/state/scope; X2-03B polling/restart/idempotency recovery; X2-03C deletion/expiry/reconciliation |
| M3-02 | M3-02A mastery/evidence; M3-02B revisions/undo; M3-02C finals/post-exam |
| M2-02 | M2-02A explanation/practice candidates; M2-02B evaluator evidence/feedback |
| API-01 | API-01A course/material inspection; API-01B policy/consent; API-01C coverage/version conflicts |
| API-02 | API-02A explanation/practice sessions; API-02B attempts/checks/evidence |
| API-03 | API-03A plan/tasks/revisions; API-03B review-goal/finals; API-03C study-focus confirmation |
| API-04 | API-04A profile/credential lifecycle; API-04B audit/security status |
| UI-01 | UI-01A shell/tokens/accessibility; UI-01B timeline/navigation; UI-01C responsive/loading/error/empty states |
| UI-02 | UI-02A metadata/import state; UI-02B policy/consent/start/recovery |
| UI-03 | UI-03A source/coverage; UI-03B privacy; UI-03C credentials |
| UI-04 | UI-04A explanation/citations; UI-04B deterministic checks/evidence |
| UI-05 | UI-05A dashboard/revision diff; UI-05B finals/post-exam |
| DEMO-01 | DEMO-01A sessions/quotas/fixtures; DEMO-01B mock-only API/provider isolation; DEMO-01C UI notice/full demo workflow |
| QA-01 | QA-01A browser workflow/responsive; QA-01B accessibility/security; QA-01C backend fixture/artifact matrix |
| QA-02 | QA-02A performance; QA-02B cancellation/restart recovery; QA-02C private benchmark boundary |

The coordinator updates the parent group summary only after all child commits and reviews are recorded. G-03 cold-start choices must name one or two dispatch-unit IDs; a Task Group heading is not a valid choice.

## File and Ownership Map

The following paths are the intended responsibility boundaries. A task may add a narrowly scoped file inside its owned directory, but may not refactor another task's directory without a review note.

| Area | Files and responsibility |
| --- | --- |
| Backend packaging | backend/pyproject.toml, backend/src/projectb/__init__.py |
| Domain contracts | backend/src/projectb/domain/types.py, source.py, materials.py, provider.py, learning.py, review.py, errors.py |
| Application services | backend/src/projectb/application/materials.py, coverage.py, security.py, credentials.py, provider.py, remote.py, learning.py, review.py, demo.py |
| Persistence | backend/src/projectb/infrastructure/sqlite.py, migrations/*.sql, repositories/*.py, audit.py |
| Parsers and secrets | backend/src/projectb/infrastructure/parsers.py, keyring_store.py |
| Providers | backend/src/projectb/infrastructure/providers/base.py, mock.py, openai.py, openai_http.py |
| HTTP boundary | backend/src/projectb/api/app.py, dependencies.py, middleware.py, errors.py, routes/*.py |
| Backend tests | backend/tests/unit, backend/tests/contract, backend/tests/integration, backend/tests/fixtures |
| Frontend | frontend/package.json, vite.config.ts, tsconfig*.json, frontend/src/app, api, state, components, features, styles |
| Shared test/build entry | scripts/test_all.py, scripts/scan_secrets.ps1, scripts/verify_licenses.py |
| Windows distribution | packaging/windows/build.ps1, ProjectB.spec (or verified freezer manifest), smoke_test.ps1 |
| OCI/demo | packaging/oci/Dockerfile, entrypoint.sh, .dockerignore, demo/fixtures, demo/profile.json |
| Process/evidence docs | docs/engineering/*.md, README.md, .gitlab-ci.yml, .github/workflows/ci.yml |

## Execution and Review Protocol

Each implementation task must execute these concrete stages in its own worktree:

1. Add the smallest failing test named in the task and run its exact focused command. Preserve the failure output in the task's AGENT_LOG entry.
2. Add the smallest implementation satisfying that test and rerun the focused command.
3. Run the task's listed regression command and then python scripts/test_all.py.
4. Run the SPEC review: check every AC identifier listed by the task and inspect boundary/error paths.
5. Run the quality review: inspect ownership, security, dependency/license evidence, logging, migration compatibility, and test determinism. A Critical issue blocks the next task.
6. Run scripts/scan_secrets.ps1 (or the platform-equivalent scanner) before commit. A suspected real credential stops the task and is reported without echoing the value.
7. Stage only the exact files listed for the current checkpoint, inspect the staged diff, and commit with a message containing the parent task/checkpoint ID, fresh subagent identity, and any human changes. The executable command form is `git add -- <exact-file-1> <exact-file-2> ...; git diff --cached --check; git commit -m "<type>(<task-id>): <short purpose> [agent: <id>]"`; no `<exact-file>` or `<id>` placeholder may remain in the recorded evidence. The coordinator then updates this plan's status/commit and AGENT_LOG.md; no task may claim completion without those records.

## Status Ledger

There are 41 planning groups and 69 dispatch units (the 17 groups marked `Task Group` expand into the unit IDs in the dispatch table). All dispatch units start pending. The coordinator changes a unit checkbox, commit hash, and two review results only after real evidence exists; “尚未执行” is the truthful initial state.

| ID | Deliverable | Dependencies | Parallel group | Status / commit |
| --- | --- | --- | --- | --- |
| G-01 | Open Design MCP/design-system gate | SPEC confirmed | G | [ ] 尚未执行 |
| G-02A | Toolchain/dependency/license baseline | SPEC confirmed | G | [ ] 尚未执行 |
| G-02B | Provider policy/capability/cost evidence | G-02A | G | [ ] 尚未执行 |
| G-02C | Distribution/hosting evidence | G-02A | G | [ ] 尚未执行 |
| G-03 | Fresh-agent cold start and implementation approval | formal writing-plans evidence, G-01 PASS, G-02A/B/C PASS | G | [ ] 尚未执行 |
| G-04 | Worktree/branch ownership map | G-03 approved | G | [ ] 尚未执行 |
| T-01 | Reproducible project/test scaffold | G-01 PASS/G-02A PASS/G-03 approved/G-04 | F | [ ] 尚未执行 |
| T-02 | Domain primitives and SourceLocator | T-01 | D | [ ] 尚未执行 |
| T-03A | Idempotent SQLite schema and migration boundary | T-02 | D | [ ] 尚未执行 |
| T-03B | Course/material versioned repositories | T-03A | D | [ ] 尚未执行 |
| T-03C | Learning/remote repositories and tombstones | T-03B | D | [ ] 尚未执行 |
| T-04 | Loopback, Host/Origin, CSRF, and audit controls | T-01/T-03C | S | [ ] 尚未执行 |
| T-05 | Credential service and provider profile schema | T-03C/T-04 | S | [ ] 尚未执行 |
| T-06 | Consent/policy/scope service | T-02/T-03C/T-05 | S | [ ] 尚未执行 |
| T-07 | Provider-neutral registry and deterministic mock contract | T-05/T-06 | X | [ ] 尚未执行 |
| M1-01 | Input inspection and role validation | T-02/T-03C/T-06 | M1 | [ ] 尚未执行 |
| M1-02 | Local import, parser, raw/normalized page storage | M1-01/T-03C | M1 | [ ] 尚未执行 |
| M1-03 | Source retrieval, locator proof, and coverage diff/confirmation | M1-02/T-02/T-07 | M1 | [ ] 尚未执行 |
| X2-01 | Constrained port dispatcher and candidate validator | T-07/M1-03 | X2 | [ ] 尚未执行 |
| X2-02 | OpenAI P/reference Responses adapter | X2-01/G-02A/G-02B | X2 | [ ] 尚未执行 |
| X2-03A | F enqueue/state/scope contract | X2-02/T-03C/T-06 | X2 | [ ] 尚未执行 |
| X2-03B | Remote polling/restart/idempotency recovery | X2-03A | X2 | [ ] 尚未执行 |
| X2-03C | Remote deletion/expiry/reconciliation | X2-03B/G-02B | X2 | [ ] 尚未执行 |
| M1-04 | Material deletion, tombstones, and remote coordination | M1-03/X2-03C | M1 | [ ] 尚未执行 |
| M2-01 | Mutex/race parameterized oracle and probes | T-02/T-03C | M2 | [ ] 尚未执行 |
| M2-02A | Explanation/practice candidate flow | M2-01/X2-01/M1-03 | M2 | [ ] 尚未执行 |
| M2-02B | Evaluator evidence/feedback flow | M2-02A/T-03C | M2 | [ ] 尚未执行 |
| M3-01 | ReviewPolicy v1 pure planner and golden fixtures | T-02/T-03C/M1-03 | M3 | [ ] 尚未执行 |
| M3-02A | Mastery/evidence derivation | M2-02B/M3-01/M1-03/T-03C | M3 | [ ] 尚未执行 |
| M3-02B | Append-only plan revisions and undo | M3-02A | M3 | [ ] 尚未执行 |
| M3-02C | Finals entry/exit and post-exam state | M3-02B | M3 | [ ] 尚未执行 |
| M3-03 | Past-paper/teacher-focus candidate mapping and confirmation | M1-03/X2-01/M3-02C | M3 | [ ] 尚未执行 |
| API-01A | Course/material inspection routes | M1-03/T-04/T-06 | API | [ ] 尚未执行 |
| API-01B | Policy/consent routes | API-01A | API | [ ] 尚未执行 |
| API-01C | Coverage/version-conflict routes | API-01B/M1-03 | API | [ ] 尚未执行 |
| API-02A | Explanation/practice session routes | M2-02A/API-01C | API | [ ] 尚未执行 |
| API-02B | Attempt/check/evidence routes | M2-02B/API-02A | API | [ ] 尚未执行 |
| API-03A | Plan/task/revision routes | M3-02B/API-01C | API | [ ] 尚未执行 |
| API-03B | Review-goal/finals routes | M3-02C/API-03A | API | [ ] 尚未执行 |
| API-03C | Study-focus confirmation routes | M3-03/API-03B | API | [ ] 尚未执行 |
| API-04A | Profile/credential lifecycle routes | T-04/T-05/T-06/API-01C | API | [ ] 尚未执行 |
| API-04B | Audit/security status routes | API-04A/T-03C | API | [ ] 尚未执行 |
| UI-01A | Shell/tokens/accessibility base | G-01/API-01C | UI | [ ] 尚未执行 |
| UI-01B | Four-stage timeline/navigation | UI-01A | UI | [ ] 尚未执行 |
| UI-01C | Responsive/loading/error/empty shell states | UI-01B/API-01C | UI | [ ] 尚未执行 |
| UI-02A | Metadata/import state | UI-01C/API-01C | UI | [ ] 尚未执行 |
| UI-02B | Policy/consent/start/recovery | UI-02A/API-01B | UI | [ ] 尚未执行 |
| UI-03A | Source/coverage screens | UI-01C/API-01C | UI | [ ] 尚未执行 |
| UI-03B | Material privacy/deletion settings | UI-03A/API-01B | UI | [ ] 尚未执行 |
| UI-03C | Hidden credential settings | UI-01C/API-04A | UI | [ ] 尚未执行 |
| UI-04A | Source-bound explanation/citations | UI-01C/UI-03A/API-02A/M2-02A | UI | [ ] 尚未执行 |
| UI-04B | Deterministic checks/evidence UI | UI-04A/API-02B/M2-02B | UI | [ ] 尚未执行 |
| UI-05A | Review dashboard/revision diff | UI-01C/API-03A/M3-02C | UI | [ ] 尚未执行 |
| UI-05B | Finals/post-exam UI | UI-05A/API-03B/API-03C/M3-02C/M3-03 | UI | [ ] 尚未执行 |
| DEMO-01A | Ephemeral sessions/quotas/fixtures | API-01C/T-07/UI-01C | DEMO | [ ] 尚未执行 |
| DEMO-01B | Mock-only API/provider isolation | DEMO-01A/API-02B/API-03C/T-07 | DEMO | [ ] 尚未执行 |
| DEMO-01C | Demo notice/full workflow integration | DEMO-01B/UI-01C | DEMO | [ ] 尚未执行 |
| QA-01A | Browser workflow/responsive evidence | UI-02B/UI-03B/UI-03C/UI-04B/UI-05B/DEMO-01C | QA | [ ] 尚未执行 |
| QA-01B | Accessibility/security browser evidence | QA-01A/T-04/API-04B | QA | [ ] 尚未执行 |
| QA-01C | Backend fixture/artifact matrix | QA-01B/M1-01/M1-02 | QA | [ ] 尚未执行 |
| QA-02A | Performance evidence | M1-02/M3-02C/API-01C | QA | [ ] 尚未执行 |
| QA-02B | Cancellation/restart recovery evidence | QA-02A/X2-03B | QA | [ ] 尚未执行 |
| QA-02C | Private benchmark boundary | QA-02B | QA | [ ] 尚未执行 |
| DIST-01 | Windows x64 single-file build and clean-machine smoke | QA-01C/QA-02C/API-04B/G-02C | DIST | [ ] 尚未执行 |
| DIST-02 | OCI image and public demo deployment preflight | DEMO-01C/DIST-01/QA-01C/G-02C | DIST | [ ] 尚未执行 |
| CI-01 | One-command test, GitLab unit-test, GitHub Actions, scans | T-01/DIST-01/DIST-02 | CI | [ ] 尚未执行 |
| DOC-01 | README, dependency/license notices, operations and limits | CI-01/INT-01/QA-02C/G-01 | DOC | [ ] 尚未执行 |
| INT-01 | User-authorized live P/F evidence suite | X2-02/X2-03C/G-02B | INT | [ ] 尚未执行 |
| FIN-01 | Final verification, remote evidence, and branch finishing | DOC-01/CI-01/INT-01/QA-02C | FIN | [ ] 尚未执行 |

---

### Task G-01: Verify Open Design MCP, Skill, and Actual Design System

**Goal:** Satisfy the mandatory UI prerequisite without inventing a design system or skill choice.

**Files:**
- Create: docs/engineering/OPEN_DESIGN_VALIDATION.md
- Modify after the external verification: SPEC.md, SPEC_PROCESS.md, AGENT_LOG.md
- Do not modify: frontend source or production code

**Interfaces:**
- Consumes: the confirmed WebUI requirements in SPEC.md §4 and the installed Open Design 0.15.1 desktop application.
- Produces: a recorded Open Design version, MCP endpoint/tool evidence, actual skill identifier, actual design-system identifier, selected rationale, rejected alternatives, and a verification date. UI tasks consume these exact identifiers through docs/engineering/OPEN_DESIGN_VALIDATION.md.

**Dependencies / parallelism:** No code dependency. It may run beside G-02, but UI implementation is blocked until it passes. The student must execute external MCP/client-restart actions; the plan does not choose D-005 and must preserve the student's selected `frontend-design` + `default`/Neutral Modern combination.

- [ ] **Step 1: Capture the current failing gate**

Run:

~~~powershell
codex mcp list
od --version
rg -n "skillId|designSystemId|Open Design|MCP" SPEC.md docs/engineering 2>$null
~~~

Expected current state: FAIL because this Codex task's MCP process cached the old `http://127.0.0.1:7456` fallback before the healthy ephemeral daemon started. The student-selected `frontend-design` + `default`/`Neutral Modern` combination and direct daemon catalog evidence are recorded, but live MCP tool/context evidence is still absent. This failure is evidence, not permission to bypass the gate.

- [ ] **Step 2: Perform the user-authorized external setup and verification**

The student has opened Open Design 0.15.1 and selected `frontend-design` + `default`/`Neutral Modern`; keep the desktop app running and do not send a broad generation prompt. The MCP registration is already present in the current user config; do not add a duplicate entry or persist an ephemeral port. Start a fresh Codex task so the MCP client process re-runs dynamic daemon discovery, then call `list_skills`, `list_projects`, and `get_active_context`. If they still report the fallback `127.0.0.1:7456` connection error, preserve that exact error and the desktop daemon log rather than changing registration or bypassing the gate.

In the fresh task, use Open Design MCP only for read-only discovery: call `list_skills`, `list_projects`, and `get_active_context` when a real context exists. Do not call `start_run`, create a project merely to manufacture evidence, send a prompt, ask Open Design to generate a WebUI direction, or produce an artifact/source in this step. If the project list is empty or no active context exists, record that truthful result and keep G-01 partial; a controlled Open Design run belongs to a later explicitly scoped gate step.

- [ ] **Step 3: Record only observed facts**

Complete docs/engineering/OPEN_DESIGN_VALIDATION.md with the fresh MCP tool output, selected IDs/names, version, date, rejected alternatives and reasons, and the statement that the HTML mockup is not formal evidence. The file currently contains partial selection/daemon evidence only. Update SPEC.md and SPEC_PROCESS.md only with observed facts; if the fresh MCP result differs, stop and request a SPEC decision.

- [ ] **Step 4: Verify the gate**

Run:

~~~powershell
rg -n "actual|skill|design system|MCP|version|selected|rejected" docs/engineering/OPEN_DESIGN_VALIDATION.md
codex mcp list
~~~

Expected: the file contains an observed selected result, the tool is callable in a fresh session, and the selected IDs match the recorded evidence.

- [ ] **Step 5: Review and commit**

Spec review checks AC-44. Quality review checks that no UI code, unverified license, or invented design choice was added. Commit with process(G-01): record Open Design gate evidence; the coordinator records the hash in this plan and AGENT_LOG.md.
**Commit command:** `git add -- docs/engineering/OPEN_DESIGN_VALIDATION.md SPEC.md SPEC_PROCESS.md AGENT_LOG.md; git diff --cached --check; git commit -m "process(G-01): record Open Design gate evidence [agent: <fresh-agent-id>]"; git rev-parse HEAD`

**Completion standard:** Actual MCP/tool, skill, and design-system evidence is reproducible; UI tasks remain blocked if any part is unavailable or unrecorded.

### Task Group G-02 (not dispatchable): Toolchain, Provider, License, Cost, and Hosting Evidence

**Goal:** Turn all unverified implementation choices into explicit evidence before a dependency, provider, freezer, or public-host claim is made.

**Files:**
- Create: docs/engineering/DEPENDENCY_BASELINE.md
- Create: docs/engineering/PROVIDER_POLICY_EVIDENCE.md
- Create: docs/engineering/DISTRIBUTION_EVIDENCE.md
- Create: scripts/verify_evidence.ps1
- Modify: AGENT_LOG.md only through the coordinator

**Interfaces:**
- Consumes: SPEC.md §§8–10, docs/research/TECH_STACK_DISTRIBUTION_BASELINE.md, CONSTRAINED_AI_PORT_CONTRACT.md, and REMOTE_FILE_LIFECYCLE_CONTRACT.md.
- Produces: machine-checkable rows for exact Python/Node/package versions, parser/render choice, HTTP/SDK choice, keyring backend, test tools, freezer, Docker base image, and all direct/transitive licenses; provider capability/policy/retention/deletion/region/cost evidence with source URL and retrieval date; and an explicit decision record whenever a candidate cannot be verified. Downstream manifests and adapter tasks consume these records.

**Dependencies / parallelism:** May run beside G-01. It must finish before T-01, X2-02, DIST-01, DIST-02, or any statement about provider fees/licenses. Never write “supported”, “free”, “licensed”, or “exactly once” without a cited current source and test evidence.

- [ ] **Step 1: Add a failing evidence validator**

Create scripts/verify_evidence.ps1 that exits nonzero unless every required row has an exact version, source URL, license, verification date, and status verified or explicitly-blocked; it must reject rows containing a real secret or a blank source.

Run:

~~~powershell
powershell -ExecutionPolicy Bypass -File scripts/verify_evidence.ps1
~~~

Expected: FAIL because the evidence files and required rows do not yet exist.

- [ ] **Step 2: Fill the evidence rows from authoritative sources**

Record the selected compatible versions only after checking official release/compatibility pages and license texts. Record OpenAI policy snapshots for Responses, abuse monitoring, prompt cache, file safety review, Files, Vector Stores, deletion/expiry, region and pricing; distinguish “unknown/not verified” from a positive claim. Record Hugging Face Docker SDK terms, HTTPS/idle storage/quotas/cost, and the fallback SPEC-change procedure if the no-paid-resource boundary fails. Record the freezer's license and clean-machine constraints. Do not include private course PDFs.

- [ ] **Step 3: Run the validator to green**

Run:

~~~powershell
powershell -ExecutionPolicy Bypass -File scripts/verify_evidence.ps1
~~~

Expected: PASS with a row count and no secret findings. If any provider, license, fee, or hosting fact remains unavailable, it stays explicitly blocked and the dependent task cannot claim completion.

- [ ] **Step 4: Review and commit**

Group review checks AC-20, AC-39, AC-48, AC-49 and AC-50 after G-02A/B/C. Quality review checks source authority, dates, license compatibility, cost language, and absence of credentials. No worker commit is assigned to this heading; use the three unit commit commands below.

**Completion standard:** Every selected v1 dependency has a cited, compatible, usable evidence row and no required row is blocked. A blocked row is valid diagnostic evidence but leaves G-02 pending and prevents G-03/T-01; no unverified provider/license/fee claim appears in PLAN.md, code, README, or CI.

### Task G-02A: Establish the Toolchain, Dependency, and License Baseline

**Goal:** Lock exact compatible Python/Node packages, parser/render stack, keyring backend, test tools, freezer candidates, and direct/transitive license evidence.

**Files:** Create `docs/engineering/DEPENDENCY_BASELINE.md` and `scripts/verify_evidence.ps1`.

**Interfaces:** the validator rejects missing version/source/license/date/status rows and real-secret patterns; later manifests consume only `verified` compatible rows.

**Dependencies / parallelism:** Requires confirmed SPEC. It owns the shared validator and completes before G-02B/G-02C or T-01.

- [ ] **Red:** create the validator first and run `powershell -ExecutionPolicy Bypass -File scripts/verify_evidence.ps1`; expected FAIL because the dependency baseline rows are absent.
- [ ] **Green/refactor:** verify exact versions/licenses from authoritative sources, populate dependency rows, then rerun the validator. A required incompatible/unverified item leaves the unit pending.
- [ ] **Reviews:** SPEC review AC-07, AC-10, AC-40, AC-43; quality review source authority, compatibility, transitive licenses, retrieval dates, and no credentials. Critical findings block T-01/G-02B/C.
- [ ] **Commit:** `git add -- docs/engineering/DEPENDENCY_BASELINE.md scripts/verify_evidence.ps1`; run `git diff --cached --check`; commit with `git commit -m "docs(G-02A): lock toolchain and license baseline [agent: <fresh-agent-id>]"`.

**Completion standard:** Every implementation/build dependency has one compatible locked row and verified license, and the validator passes without an unresolved required row.

### Task G-02B: Establish Provider Capability, Policy, and Cost Evidence

**Goal:** Verify current OpenAI P/F capabilities, retention/deletion/region facts, endpoint limitations, and bounded cost assumptions without making a live paid call.

**Files:** Create `docs/engineering/PROVIDER_POLICY_EVIDENCE.md`; modify `scripts/verify_evidence.ps1` only through G-02A ownership.

**Interfaces:** dated evidence rows cover Responses, abuse monitoring, prompt cache, file review, Files/Vector Stores, deletion/expiry, region, pricing, and explicit unsupported/unknown facts.

**Dependencies / parallelism:** Requires G-02A. It may run beside G-02C with serialized validator edits. X2-02/X2-03C/INT-01 depend on this unit.

- [ ] **Red:** add provider-required-row assertions and run the validator; expected FAIL because provider rows are absent.
- [ ] **Green/refactor:** populate rows only from current official sources, distinguish unknown from support, then rerun the validator. Any v1-required capability/policy/cost row blocked leaves G-02B pending.
- [ ] **Reviews:** SPEC review AC-20, AC-21, AC-27, AC-39, AC-48, AC-49, AC-50; quality review dated source authority, `store:false`/ZDR wording, retention/deletion distinctions, cost arithmetic, and no key/request body. Critical findings block provider implementation.
- [ ] **Commit:** `git add -- docs/engineering/PROVIDER_POLICY_EVIDENCE.md scripts/verify_evidence.ps1`; run `git diff --cached --check`; commit with `git commit -m "docs(G-02B): verify provider policy and cost [agent: <fresh-agent-id>]"`.

**Completion standard:** All provider facts needed by the selected P/F contract are current, compatible, and usable; an unresolved required fact keeps the unit pending.

### Task G-02C: Establish Distribution and Hosting Evidence

**Goal:** Verify the Windows freezer, OCI base image, selected public host terms, HTTPS/storage/sleep/quota/cost limits, and fallback boundaries.

**Files:** Create `docs/engineering/DISTRIBUTION_EVIDENCE.md`; modify `scripts/verify_evidence.ps1` only through G-02A ownership.

**Interfaces:** dated rows cover freezer license/clean-machine constraints, Docker image digest/license, hosting runtime/HTTPS/storage/idle/quota/account/cost, and no-paid-resource fallback.

**Dependencies / parallelism:** Requires G-02A. It may run beside G-02B with serialized validator edits. DIST-01/DIST-02 depend on this unit.

- [ ] **Red:** add distribution/hosting required-row assertions and run the validator; expected FAIL because those rows are absent.
- [ ] **Green/refactor:** verify authoritative sources, record exact usable terms, then rerun the validator. A blocked selected freezer/base/host leaves G-02C pending and requires a SPEC change rather than substitution.
- [ ] **Reviews:** SPEC review AC-10, AC-41, AC-43, AC-47; quality review source dates, license compatibility, architecture support, cost language, and clean-host reproducibility. Critical findings block packaging/deployment.
- [ ] **Commit:** `git add -- docs/engineering/DISTRIBUTION_EVIDENCE.md scripts/verify_evidence.ps1`; run `git diff --cached --check`; commit with `git commit -m "docs(G-02C): verify distribution and hosting [agent: <fresh-agent-id>]"`.

**Completion standard:** The selected freezer, OCI base, and host each have a compatible verified row; no required distribution/hosting fact remains blocked.

### Task G-03: Run the Required Fresh-Agent Cold Start and Obtain Implementation Approval

**Goal:** Use a different agent type in a brand-new session to expose specification/plan ambiguity before formal implementation.

**Files:**
- Modify: SPEC.md only when the cold-start finding proves a specification defect
- Modify: PLAN.md only when the cold-start finding proves a plan defect
- Modify: SPEC_PROCESS.md
- Modify: DECISIONS_NEEDED.md if the student records a new decision
- Create: a disposable cold-start workspace whose initial visible inputs are only SPEC.md and PLAN.md
- Do not merge: any cold-start source changes

**Interfaces:**
- Consumes: only SPEC.md and PLAN.md supplied to the fresh agent; the task prompt must not include this conversation history.
- Produces: the student-selected D-005 agent type/version, session boundary, exact dispatch-unit IDs attempted (one or two), questions/pauses, misunderstood contract points, output gap, and before/after SPEC/PLAN diff. Task Group headings are forbidden cold-start choices. The implementation gate is a signed student decision after those revisions.

**Dependencies / parallelism:** Requires this plan, a reproducible G-01 PASS, a G-02 baseline with no blocked row needed by any selected v1 dependency, and a real `superpowers:writing-plans` invocation record (or explicit course acceptance of the documented fallback). A documented but unresolved G-01/G-02 block is not a pass. This is a hard gate before T-01. D-005 is deliberately left to the student; this task must not select one.

- [ ] **Step 1: Prepare the cold-start prompt**

Use a fresh session of the student-selected different agent, provide only SPEC.md and PLAN.md, and state: “Choose one or two implementation units from this eligible set: T-02, M2-01, M3-01, API-01A, or UI-01A. Do not choose a Task Group or G/DOC/FIN unit. This is a pre-implementation cold-start experiment: upstream task implementations are intentionally absent, so treat the interfaces declared in SPEC.md/PLAN.md as contracts and create only the minimum disposable scaffold/test doubles needed to attempt the selected unit. Do not mark a dependency complete, inspect any other repository file, or merge the attempt. If any requirement, interface, dependency, or acceptance criterion is uncertain, pause and ask instead of guessing.”

The normal dispatch dependency rule is deliberately suspended only inside this disposable G-03 experiment; it remains mandatory for every formal implementation dispatch after approval. Initialize the workspace with copies of exactly SPEC.md and PLAN.md, record an initial file listing, and keep every generated attempt file outside the implementation branches.

- [ ] **Step 2: Preserve the first failure/question**

Run the chosen task's first red-test command in the disposable workspace after the fresh agent creates its minimum temporary scaffold. Expected: FAIL on the selected behavior's absent implementation, or pause before the command when the fresh agent finds a specification gap; preserve the exact question, initial file listing, temporary scaffold, and command/output. A failure caused only by an intentionally absent upstream implementation is recorded as an implementation prerequisite, not misclassified as a SPEC defect. Do not fabricate a pass and do not merge its implementation.

- [ ] **Step 3: Analyze and revise**

Compare the agent's interpretation to SPEC.md. For each gap, record whether the document or agent was wrong, the expected-vs-actual output difference, and a focused diff to SPEC.md/PLAN.md. If a revision changes a confirmed contract, stop for student confirmation.

- [ ] **Step 4: Verify the gate**

Run:

~~~powershell
git diff -- SPEC.md PLAN.md SPEC_PROCESS.md
rg -n "冷启动|D-005|问题|误解|修订前|修订后|implementation approval" SPEC_PROCESS.md
~~~

Expected: evidence contains a different agent type, a new session, 1–2 attempted task IDs, all pauses and diffs, and an explicit student approval to enter implementation. Without that approval, all T-* and feature tasks remain blocked.

- [ ] **Step 5: Review and commit process evidence**

Spec review checks the course cold-start requirements and that no hidden context was supplied. Quality review checks truthful timestamps, no invented output, and no source merge. Commit with process(G-03): record cold-start findings; coordinator records the hash.
**Commit command:** `git add -- SPEC.md PLAN.md SPEC_PROCESS.md DECISIONS_NEEDED.md; git diff --cached --check; git commit -m "process(G-03): record cold-start findings [agent: <fresh-agent-id>]"; git rev-parse HEAD`

**Completion standard:** Every SPEC/PLAN defect exposed by the fresh agent is corrected and, when it changes a confirmed contract, explicitly confirmed by the student. Any unresolved defect leaves G-03 incomplete and blocks implementation even if it is documented; implementation approval is valid only after the corrected documents are reviewed.

### Task G-04: Create Worktree, Branch, and Shared-Document Ownership Map

**Goal:** Apply using-git-worktrees before implementation and prevent parallel agents from overwriting shared process evidence.

**Files:**
- Create: docs/engineering/WORKTREE_MAP.md
- Modify: .gitignore only if the map identifies disposable paths
- Do not alter: user changes in existing worktrees

**Interfaces:**
- Consumes: the implementation approval from G-03.
- Produces: one short-lived branch/worktree per dispatch unit, module merge-destination branches, owner unit IDs, merge order, base commit, shared-file owner (PLAN.md/AGENT_LOG.md/SPEC_PROCESS.md), and the rule that only the coordinator updates shared ledgers after a unit commit.

**Dependencies / parallelism:** Must precede T-01. Worktree creation itself is sequential; later feature worktrees may run in parallel only when their listed files and database migrations do not overlap.

- [ ] **Step 1: Verify the intended worktrees fail closed**

Run:

~~~powershell
git worktree list
git branch --list "codex/*"
~~~

Expected: FAIL closed if any worktree or branch is unrecorded; otherwise the pre-implementation inventory is the red-gate baseline. Any existing user worktree is preserved and listed rather than removed.

- [ ] **Step 2: Create the mapped worktrees**

Use the installed using-git-worktrees workflow to create coordinator-only module merge destinations such as codex/foundation, codex/materials, codex/provider, codex/learning, codex/review, codex/ui, and codex/distribution under a user-approved sibling directory. Before dispatch, create `../ProjectB-wt/<unit-id-lower>` on `codex/<unit-id-lower>-<short-name>` from the dependency commit; module destinations are never worker worktrees. Merge a unit only after both reviews. The worker does not edit shared ledgers; the coordinator records them after the child commit. Do not run destructive cleanup commands.

- [ ] **Step 3: Verify ownership**

Run:

~~~powershell
git worktree list
git status --short
~~~

Expected: every active worktree and branch appears in WORKTREE_MAP.md, no user edits disappear, and shared process files have one coordinator owner.

- [ ] **Step 4: Review and commit**

Spec review checks one-worktree-per-PR intent and merge dependencies. Quality review checks path containment, branch naming, and no forced push/reset. Commit with process(G-04): record worktree ownership; coordinator records the hash.
**Commit command:** `git add -- docs/engineering/WORKTREE_MAP.md .gitignore; git diff --cached --check; git commit -m "process(G-04): record worktree ownership [agent: <fresh-agent-id>]"; git rev-parse HEAD`

**Completion standard:** Fresh subagents can be dispatched task-by-task without shared-file races or untracked worktrees.

### Task T-01: Create the Reproducible Project and Test Scaffold

**Goal:** Make a minimal, bootable backend/frontend repository with one deterministic test command, using only versions/licenses verified in G-02.

**Files:**
- Create: backend/pyproject.toml
- Create: backend/src/projectb/__init__.py
- Create: backend/src/projectb/api/app.py
- Create: backend/tests/unit/test_health.py
- Create: frontend/package.json, frontend/package-lock.json, frontend/tsconfig.json, frontend/vite.config.ts
- Create: frontend/src/main.tsx, frontend/src/app/App.tsx
- Create: scripts/test_all.py
- Create: scripts/scan_secrets.ps1
- Modify: .gitignore

**Interfaces:**
- Consumes: docs/engineering/DEPENDENCY_BASELINE.md.
- Produces: create_app(profile: str = "local") -> FastAPI, GET /api/health -> {"status":"ok","profile":...}, python scripts/test_all.py as the single backend/unit/frontend-build entry point, and the first real project secret scanner. The initial entry point has an explicit scaffold phase and cannot pretend that later G-02 evidence or CI-01 license checks already exist.

**Dependencies / parallelism:** Reproducible G-01 PASS, usable G-02 PASS, G-03 approval, and G-04 are hard prerequisites. This is the shared foundation worktree; later tasks may branch from it but must not edit its manifests without a dependency review.

- [ ] **Step 1: Write the failing test**

~~~python
def test_health_reports_selected_profile():
    from projectb.api.app import create_app
    from fastapi.testclient import TestClient
    response = TestClient(create_app("test")).get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "profile": "test"}
~~~

Run the red test without installing the not-yet-created package:

~~~powershell
$env:PYTHONPATH = (Resolve-Path backend/src -ErrorAction SilentlyContinue)
python -m pytest backend/tests/unit/test_health.py -q
~~~

Expected: FAIL with the module/app not found.

- [ ] **Step 2: Implement the smallest scaffold**

~~~python
def create_app(profile: str = "local") -> FastAPI:
    app = FastAPI()
    @app.get("/api/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "profile": profile}
    return app
~~~

Wire only the exact G-02-verified package versions and create the committed npm lockfile before using `npm ci`. Make scripts/test_all.py invoke backend tests, frontend tests/build, and scripts/scan_secrets.ps1 after their locked installs. The scanner must include tracked/untracked project files, redact findings, and have a synthetic marker fixture proving a nonzero exit without containing a real secret. In scaffold phase, later G-02 evidence and CI-01 license/distribution gates are reported as `not_available_until:<task-id>`, never PASS; once their owner tasks land, absence is a hard failure.

- [ ] **Step 3: Verify**

Run:

~~~powershell
python -m pip install -e backend
npm --prefix frontend ci
python -m pytest backend/tests/unit/test_health.py -q
powershell -ExecutionPolicy Bypass -File scripts/scan_secrets.ps1
python scripts/test_all.py
~~~

Expected: focused test PASS; the secret scanner runs and passes on the clean scaffold; the entry runs backend tests and a frontend production build, and explicitly reports later evidence/license/distribution gates as not yet available rather than passing them. After G-02/CI-01 merge, the same command must run those gates and fail on a missing check or finding.

- [ ] **Step 4: Review and commit**

Spec review checks AC-10's one-command requirement and the local/demo profile boundary. Quality review checks lockfiles, reproducible install, no network calls in tests, and license evidence. Commit with build(T-01): add reproducible app and test scaffold; record hash and review results.
**Commit command:** `git add -- backend/pyproject.toml backend/src/projectb/__init__.py backend/src/projectb/api/app.py backend/tests/unit/test_health.py frontend/package.json frontend/package-lock.json frontend/tsconfig.json frontend/vite.config.ts frontend/src/main.tsx frontend/src/app/App.tsx scripts/test_all.py scripts/scan_secrets.ps1 .gitignore; git diff --cached --check; git commit -m "build(T-01): add reproducible app and test scaffold [agent: <fresh-agent-id>]"; git rev-parse HEAD`

**Completion standard:** A clean checkout can install the verified dependencies, run the one-command test entry, and start a profile-labelled health endpoint.

### Task T-02: Define Domain Primitives and SourceLocator Proof

**Goal:** Establish immutable IDs, material roles/modes/states, the four-way SourceLocator union, normalization, and unique-page proof used by every module.

**Files:**
- Create: backend/src/projectb/domain/types.py
- Create: backend/src/projectb/domain/source.py
- Create: backend/src/projectb/domain/materials.py
- Create: backend/src/projectb/domain/errors.py
- Create: backend/tests/unit/test_source_locator.py
- Create: backend/tests/fixtures/source_pages.json

**Interfaces:**
- Consumes: no provider or parser implementation.
- Produces:
  - normalize_source_text(value: str) -> str using NFKC, CRLF-to-LF, soft-hyphen removal, whitespace collapse, and trim.
  - prove_unique_pdf_page(chunk: str, pages: Sequence[PageText], content_hash: str) -> SourceLocator | SourceInsufficient.
  - validate_source_locator(locator: SourceLocator, catalog: SourceCatalog) -> None.
  - Mode = Literal["L","P","F"], MaterialRole = Literal["lecture","past_paper","teacher_focus"], plus immutable MaterialLimits/SelectedFile/MaterialUnit primitives consumed by M1. T-02 is the sole owner of domain/materials.py; downstream tasks extend behavior in application modules without editing this contract.

**Dependencies / parallelism:** T-01 required. This file is shared by M1/M2/M3/X2; all downstream branches consume the immutable interface. No parallel edits to source.py.

- [ ] **Step 1: Write the failing tests**

~~~python
from projectb.domain.source import PageText, prove_unique_pdf_page

pages = [
    PageText(page=24, text="unrelated preface"),
    PageText(page=25, text="A 32-character source span that occurs exactly once in the fixture."),
]
duplicate_pages = [
    PageText(page=1, text="same repeated source text"),
    PageText(page=2, text="same repeated source text"),
]

def test_unique_normalized_span_maps_to_one_page():
    result = prove_unique_pdf_page(
        "A 32-character source span that occurs exactly once in the fixture.",
        pages,
        "sha",
    )
    assert result.kind == "pdf_page" and result.page == 25

def test_duplicate_or_short_span_is_source_insufficient():
    assert prove_unique_pdf_page("same", duplicate_pages, "sha").reason in {"ambiguous", "too_short"}
~~~

Run: python -m pytest backend/tests/unit/test_source_locator.py -q

Expected: FAIL because the union and proof functions do not exist.

- [ ] **Step 2: Implement the minimal typed contract**

Use frozen dataclasses or the verified schema library for the four mutually exclusive locators: pdf_page(material_id, content_hash, page, region), image(material_id, content_hash, image_id, region), text_lines(material_id, content_hash, line_start, line_end), and manual_entry(entry_id, version). Reject unknown kinds, mixed fields, pages outside the catalog, and chunks below 32 normalized code points.

- [ ] **Step 3: Verify**

Run focused tests plus the locator matrix:

~~~powershell
python -m pytest backend/tests/unit/test_source_locator.py -q
python -m pytest backend/tests/unit -q
~~~

Expected: PASS for unique, duplicate, cross-page, visual-only, short, stale-hash, and missing-page fixtures.

- [ ] **Step 4: Review and commit**

Spec review checks AC-03, AC-12–14, AC-37, and the exact locator rules. Quality review checks immutability, Unicode corner cases, error normalization, and no course body text in logs. Commit with feat(T-02): add domain and source locator contracts.
**Commit command:** `git add -- backend/src/projectb/domain/types.py backend/src/projectb/domain/source.py backend/src/projectb/domain/materials.py backend/src/projectb/domain/errors.py backend/tests/unit/test_source_locator.py backend/tests/fixtures/source_pages.json; git diff --cached --check; git commit -m "feat(T-02): add domain and source locator contracts [agent: <fresh-agent-id>]"; git rev-parse HEAD`

**Completion standard:** Every later source-bearing interface can accept only a validated locator or an explicit source-insufficient result.

### Task Group T-03 (not dispatchable): SQLite Migrations, Versioned Repositories, and Tombstones

**Goal:** Persist authoritative state append-only enough to preserve materials, evidence, plans, consent, remote objects, and deletion history.

**Files:**
- Create: backend/src/projectb/infrastructure/sqlite.py
- Create: backend/src/projectb/infrastructure/migrations/001_initial.sql
- Create: backend/src/projectb/infrastructure/repositories/course_repo.py
- Create: backend/src/projectb/infrastructure/repositories/material_repo.py
- Create: backend/src/projectb/infrastructure/repositories/learning_repo.py
- Create: backend/src/projectb/infrastructure/repositories/remote_repo.py

**Interfaces:**
- Consumes: domain types from T-02.
- Produces:
  - Database.open(path: Path) -> Database, Database.migrate() -> None, Database.transaction().
  - Repository methods put_versioned(entity), get_active(id), list_history(owner_id), tombstone(id, reason).
  - RepositoryError("state_inconsistent" | "owner_forbidden" | "not_found").

**Dependencies / parallelism:** T-02 required. This owns all migration files; M1/M3/X2 worktrees must add migrations through this owner or a reviewed migration commit, never concurrently.

**Group execution:** Dispatch only T-03A, then T-03B, then T-03C. Their focused tests are `test_sqlite_schema.py`, `test_course_material_repositories.py`, and `test_learning_remote_repositories.py`; no combined worker test or commit exists for this heading.

**Group review:** After all three child reviews, check AC-06, AC-07, AC-17, AC-30, AC-35, and AC-40 across transaction boundaries, rollback, indexes, migration repeatability, and path/secret minimization. No worker commit is assigned to this group.

**Completion standard:** A restarted process can reopen the schema without rewriting history, and deletion leaves only non-reconstructive tombstones/invalid locators.

### Task T-03A: Add the Idempotent SQLite Schema and Migration Boundary

**Goal:** Create only the database bootstrap, owner-scoped schema, constraints, indexes, and repeatable migration contract.

**Files:** Create `backend/src/projectb/infrastructure/sqlite.py`, `backend/src/projectb/infrastructure/migrations/001_initial.sql`, and `backend/tests/integration/test_sqlite_schema.py`.

**Interfaces:** `Database.open(path)`, `Database.migrate()`, and `Database.transaction()`; schema tables and columns follow the T-03 group contract and contain no secret or audit-body fields.

**Dependencies / parallelism:** Requires T-02. It exclusively owns migration files and must complete before T-03B.

- [ ] **Red:** add idempotency, foreign-key, owner-column, rollback, and forbidden-column assertions; run `python -m pytest backend/tests/integration/test_sqlite_schema.py -q`. Expected: FAIL because the database bootstrap/schema is absent.
- [ ] **Green/refactor:** implement only schema bootstrap and migration invariants, then rerun the focused test and `python -m pytest backend/tests -q`.
- [ ] **Reviews:** SPEC review AC-06, AC-07, AC-30, AC-40; quality review transaction rollback, indexes, repeatability, path handling, and forbidden columns. Critical findings block T-03B.
- [ ] **Commit:** run the scanner, then `git add -- backend/src/projectb/infrastructure/sqlite.py backend/src/projectb/infrastructure/migrations/001_initial.sql backend/tests/integration/test_sqlite_schema.py`; run `git diff --cached --check`; commit with `git commit -m "feat(T-03A): add idempotent SQLite schema [agent: <fresh-agent-id>]"`; record `git rev-parse HEAD` through the coordinator.

**Completion standard:** A fresh and an already-migrated database reach the same schema with enforced ownership/foreign keys and no forbidden secret/body columns.

### Task T-03B: Add Course and Material Versioned Repositories

**Goal:** Implement owner-scoped course/material persistence, immutable versions, content-hash idempotency, and active/history reads without adding learning or remote behavior.

**Files:** Create `backend/src/projectb/infrastructure/repositories/course_repo.py`, `backend/src/projectb/infrastructure/repositories/material_repo.py`, and `backend/tests/integration/test_course_material_repositories.py`.

**Interfaces:** the T-03 group repository methods for courses/materials plus unique `(course_id, content_hash, role)` handling and owner-forbidden/not-found errors.

**Dependencies / parallelism:** Requires T-03A and consumes T-02 types. It completes before T-03C; no concurrent migration edits.

- [ ] **Red:** add version-history, duplicate-content, cross-owner, and rollback tests; run `python -m pytest backend/tests/integration/test_course_material_repositories.py -q`. Expected: FAIL because the repositories are absent.
- [ ] **Green/refactor:** implement only course/material repository behavior, rerun the focused test, then `python -m pytest backend/tests -q`.
- [ ] **Reviews:** SPEC review AC-06, AC-17, AC-30; quality review optimistic concurrency, stable ordering, indexes, rollback, and no body/path leakage. Critical findings block T-03C.
- [ ] **Commit:** run the scanner, then `git add -- backend/src/projectb/infrastructure/repositories/course_repo.py backend/src/projectb/infrastructure/repositories/material_repo.py backend/tests/integration/test_course_material_repositories.py`; run `git diff --cached --check`; commit with `git commit -m "feat(T-03B): add course and material repositories [agent: <fresh-agent-id>]"`; record the hash through the coordinator.

**Completion standard:** Course/material versions and duplicate imports are deterministic, owner-scoped, restart-safe, and append-only.

### Task T-03C: Add Learning, Remote, and Tombstone Repositories

**Goal:** Complete persistence for evidence/plans, consent/remote jobs, audit metadata, and non-reconstructive tombstones without changing the schema contract informally.

**Files:** Create `backend/src/projectb/infrastructure/repositories/learning_repo.py`, `backend/src/projectb/infrastructure/repositories/remote_repo.py`, and `backend/tests/integration/test_learning_remote_repositories.py`. Consume the complete schema committed by T-03A; this unit does not modify migrations.

**Interfaces:** append/list immutable evidence and plan revisions, persist remote job/object states and consent references, and tombstone an object while `get_active(id)` returns none and history remains non-reconstructive.

**Dependencies / parallelism:** Requires T-03B. A schema defect stops this unit and returns to the coordinator for a separately reviewed migration repair; it is never folded into this commit. T-04/T-05/T-06/M1/M2/M3/X2 depend on this terminal unit where they require persistence.

- [ ] **Red:** add append-only history, tombstone, restart, cross-owner, and state-inconsistent tests; run `python -m pytest backend/tests/integration/test_learning_remote_repositories.py -q`. Expected: FAIL because these repositories are absent.
- [ ] **Green/refactor:** implement the smallest repositories/tombstones, rerun the focused test, `python -m pytest backend/tests/integration -q`, and `python scripts/test_all.py`.
- [ ] **Reviews:** SPEC review AC-06, AC-07, AC-17, AC-30, AC-35, AC-40; quality review transaction ordering, migration compatibility, indexes, redaction, and tombstone non-reconstructiveness. Critical findings block downstream persistence consumers.
- [ ] **Commit:** run the scanner, then `git add -- backend/src/projectb/infrastructure/repositories/learning_repo.py backend/src/projectb/infrastructure/repositories/remote_repo.py backend/tests/integration/test_learning_remote_repositories.py`; run `git diff --cached --check`; commit with `git commit -m "feat(T-03C): add learning and remote repositories [agent: <fresh-agent-id>]"`; record the hash through the coordinator. Any migration change blocks this exact commit and requires a new owned unit.

**Completion standard:** All non-course/material authoritative histories reopen after restart, preserve immutable versions, and expose only non-reconstructive deletion history.

### Task T-04: Enforce Loopback, Host/Origin, CSRF, and Minimal Audit

**Goal:** Make every state-changing HTTP request pass the local trust-boundary checks and produce a redacted audit event.

**Files:**
- Create: backend/src/projectb/api/middleware.py
- Modify: backend/src/projectb/api/app.py
- Create: backend/src/projectb/application/security.py
- Create: backend/src/projectb/infrastructure/audit.py
- Create: backend/tests/integration/test_http_security.py

**Interfaces:**
- Consumes: app scaffold T-01 and database/audit repository T-03C.
- Produces:
  - TrustedRequestPolicy.check(request) -> None | SecurityError.
  - CsrfService.issue(session_id) -> str and CsrfService.verify(session_id, token) -> None.
  - AuditWriter.record(event_type, object_ids, result, metadata) -> None, with a whitelist-only payload.
  - create_app(profile) rejects untrusted Host/Origin and state changes without the CSRF proof.

**Dependencies / parallelism:** T-03C required. Security middleware is shared by all API routes and cannot be bypassed by a feature-specific router.

- [ ] **Step 1: Write the failing tests**

~~~python
def test_untrusted_origin_and_missing_csrf_are_rejected(client):
    assert client.get("/api/health", headers={"Host": "evil.invalid"}).status_code == 403
    assert client.post("/api/_security_probe", headers={"Origin": "https://evil.invalid"}).status_code == 403
    assert client.post("/api/_security_probe", headers={"Origin": "http://127.0.0.1"}).status_code == 403
~~~

Run: python -m pytest backend/tests/integration/test_http_security.py -q

Expected: FAIL because the middleware is not installed.

- [ ] **Step 2: Implement the minimal controls**

Install the shared middleware in `create_app`, bind the server configuration to 127.0.0.1, allow only the generated localhost origins, issue a random per-session CSRF token, require it on POST/PATCH/DELETE, and reject wildcard CORS. The test-only `_security_probe` route is defined inside the test fixture, never production routing. Audit only event type, opaque IDs, result, duration, and approved metadata keys; add a test logger that fails if a path, body, answer, or credential-shaped value is emitted.

- [ ] **Step 3: Verify**

~~~powershell
python -m pytest backend/tests/integration/test_http_security.py -q
python -m pytest backend/tests -q
~~~

Expected: trusted requests pass only with a valid token; hostile Host/Origin, replayed/empty token, and exception paths are rejected/redacted.

- [ ] **Step 4: Review and commit**

Spec review checks AC-07, AC-11, AC-21, AC-22, AC-30 and threat controls T-09/T-13. Quality review checks constant-time token comparison, session expiry, error headers, and no accidental permissive CORS. Commit with feat(T-04): enforce local request trust boundary.
**Commit command:** `git add -- backend/src/projectb/api/middleware.py backend/src/projectb/api/app.py backend/src/projectb/application/security.py backend/src/projectb/infrastructure/audit.py backend/tests/integration/test_http_security.py; git diff --cached --check; git commit -m "feat(T-04): enforce local request trust boundary [agent: <fresh-agent-id>]"; git rev-parse HEAD`

**Completion standard:** No feature route can mutate state or invoke a provider without passing the shared middleware and producing a redacted audit event.

### Task T-05: Implement Credential Storage and Provider Profile Validation

**Goal:** Provide hidden entry, status, update, clear, and fail-closed profile validation without exposing a secret to ordinary state.

**Files:**
- Create: backend/src/projectb/domain/provider.py
- Create: backend/src/projectb/application/credentials.py
- Create: backend/src/projectb/infrastructure/keyring_store.py
- Create: backend/tests/unit/test_credentials.py
- Create: backend/tests/integration/test_credential_boundary.py

**Interfaces:**
- Consumes: T-03C persistence and T-04 security.
- Produces:
  - SecretStore.set(credential_ref: str, value: SecretValue), status(ref) -> CredentialStatus, clear(ref), resolve(ref) -> SecretHandle.
  - CredentialService.configure(profile_id, hidden_value) -> CredentialStatus, status(profile_id) -> CredentialStatus, clear(profile_id, force=False) -> ClearResult.
  - validate_provider_profile(payload) -> ProviderProfile | ProfileError; allowed fields are adapter ID, model ID, controlled parameters, budget policy, credential_ref, and version.

**Dependencies / parallelism:** T-03C/T-04 and G-02A required. The real Windows backend selection comes from G-02A; tests use an in-memory fake and never parse .env.

- [ ] **Step 1: Write the failing tests**

~~~python
def test_status_never_returns_secret(fake_store):
    service = CredentialService(fake_store)
    status = service.configure("profile-1", "test-secret")
    assert status.configured is True
    assert "test-secret" not in repr(status)
    assert service.status("profile-1").configured is True

def test_base_url_and_unknown_fields_fail_before_resolve():
    assert validate_provider_profile({"adapter_id":"openai","base_url":"https://x"}).is_error
~~~

Run: python -m pytest backend/tests/unit/test_credentials.py backend/tests/integration/test_credential_boundary.py -q

Expected: FAIL because the service/store/schema do not exist.

- [ ] **Step 2: Implement the boundary**

Store the value only through the verified keyring adapter selected in G-02A; persist only credential_ref, configured flag, timestamp, and redacted failure code. Reject .env, key/token/password fields, base_url, endpoint, plugin/module path, unknown fields, and missing adapter/profile before calling resolve. clear(force=True) marks unfinished remote work as credential_unavailable/delete_incomplete and never silently switches profile or mock.

- [ ] **Step 3: Verify**

~~~powershell
python -m pytest backend/tests/unit/test_credentials.py backend/tests/integration/test_credential_boundary.py -q
python -m pytest backend/tests -q
~~~

Expected: hidden entry/status/update/clear pass; SQLite, browser response, logs, snapshots, and test reports contain no secret; forced clear fails future remote calls closed.

- [ ] **Step 4: Review and commit**

Spec review checks AC-07, AC-30, AC-40 and threat controls T-06/T-19. Quality review checks Windows backend behavior, process-memory lifetime, error redaction, and dependency/license evidence. Commit with feat(T-05): add fail-closed credential service.
**Commit command:** `git add -- backend/src/projectb/application/credentials.py backend/src/projectb/infrastructure/keyring_store.py backend/src/projectb/domain/provider.py backend/tests/unit/test_credentials.py backend/tests/integration/test_credential_boundary.py; git diff --cached --check; git commit -m "feat(T-05): add fail-closed credential service [agent: <fresh-agent-id>]"; git rev-parse HEAD`

**Completion standard:** The only code path that resolves a credential is the adapter invocation boundary, and all ordinary interfaces expose status/ref only.

### Task T-06: Implement Processing Policy, Consent, and Scope Tokens

**Goal:** Prevent silent data egress and bind every P/F request to an exact immutable consent and policy snapshot.

**Files:**
- Create: backend/src/projectb/application/consent.py
- Modify: backend/src/projectb/application/security.py only through the T-04 owner
- Create: backend/tests/unit/test_consent_scope.py
- Create: backend/tests/integration/test_no_consent_egress.py

**Interfaces:**
- Consumes: T-02 locator/types, T-03C repositories, T-05 profiles/credential status.
- Produces:
  - create_consent(course_id, mode, payload_scope, profile, capability_snapshot, policy_snapshot) -> ConsentRecord.
  - require_consent(consent_id, exact_payload) -> ConsentRecord.
  - scope_token(course_id, material_id, content_hash, consent_id, config_fingerprint) -> str using SHA-256.
  - processing_policy_for(course_id) -> ProcessingPolicy.

**Dependencies / parallelism:** T-02/T-03C/T-05 required; no parallel edits to shared security.py. Provider and M1 tasks consume this immutable contract.

- [ ] **Step 1: Write the failing tests**

~~~python
def test_remote_spy_is_not_called_without_exact_consent(remote_spy, service):
    result = service.request_remote("course-1", ["material-1"], mode="F")
    assert result.status == "awaiting_consent"
    assert remote_spy.calls == 0

def test_scope_token_changes_when_consent_or_config_changes():
    assert scope_token("c","m","h","consent-a","cfg") != scope_token("c","m","h","consent-b","cfg")
~~~

Run: python -m pytest backend/tests/unit/test_consent_scope.py backend/tests/integration/test_no_consent_egress.py -q

Expected: FAIL because consent validation and scope token generation are absent.

- [ ] **Step 2: Implement the minimal policy service**

Require exact file IDs/content hashes, mode, adapter/profile/config fingerprint, capability snapshot, policy snapshot, budget, and purpose in the append-only payload scope. A changed file, added batch, changed profile/config/policy, L/P-to-F transition, or re-enable after revoke creates a new record. Empty/unknown scope returns source_insufficient/awaiting_consent before adapter resolution.

- [ ] **Step 3: Verify**

~~~powershell
python -m pytest backend/tests/unit/test_consent_scope.py backend/tests/integration/test_no_consent_egress.py -q
python -m pytest backend/tests -q
~~~

Expected: no-consent, stale-consent, changed-hash, revoked-token, and profile-fingerprint tests all show zero provider calls; consent history remains readable.

- [ ] **Step 4: Review and commit**

Spec review checks AC-01, AC-02, AC-25, AC-28, AC-31 and AC-48. Quality review checks canonical payload hashing, replay protection, append-only history, and no body text in consent/audit. Commit with feat(T-06): enforce consent and source scope.
**Commit command:** `git add -- backend/src/projectb/application/consent.py backend/src/projectb/application/security.py backend/tests/unit/test_consent_scope.py backend/tests/integration/test_no_consent_egress.py; git diff --cached --check; git commit -m "feat(T-06): enforce consent and source scope [agent: <fresh-agent-id>]"; git rev-parse HEAD`

**Completion standard:** Every remote-capable service requires an exact, current consent record and can prove the scope token it is allowed to use.

### Task T-07: Build the Provider-Neutral Registry and Deterministic Mock Contract

**Goal:** Make constrained ports deterministic and testable without a network/LLM, while ensuring local production cannot fall back to mock.

**Files:**
- Create: backend/src/projectb/infrastructure/providers/base.py
- Create: backend/src/projectb/infrastructure/providers/mock.py
- Create: backend/src/projectb/application/provider.py
- Create: backend/tests/contract/test_provider_contract.py
- Create: backend/tests/contract/test_mock_scenarios.py

**Interfaces:**
- Consumes: T-05 profile validation and T-06 consent.
- Produces:
  - ProviderRequestEnvelope, ProviderResponseEnvelope, PortName, PortVersion.
  - ProviderAdapter.describe() -> CapabilityDescriptor; ProviderAdapter.invoke(request, secret_handle) -> ProviderResponseEnvelope.
  - ProviderAdapterRegistry.for_profile(profile, runtime_profile) -> ProviderAdapter | ConfigError.
  - DeterministicMock(scenario, seed).invoke(request), calls, and repeatable output by idempotency_key.

**Dependencies / parallelism:** T-05/T-06 required. This owns the shared adapter protocol; X2 and M2 must not invent alternate envelopes.

- [ ] **Step 1: Write the failing contract tests**

~~~python
def test_mock_wording_change_cannot_change_authoritative_inputs(mock_factory):
    request = {
        "port": "generate_explanation",
        "port_version": "1",
        "source_scope": ["source-1#page=1"],
        "idempotency_key": "test-request-1",
        "input": {"concept_id": "mutex"},
    }
    a = mock_factory("success", seed=7).invoke(request)
    b = mock_factory("same_structure_different_wording", seed=7).invoke(request)
    assert validate_candidate(a).canonical_domain_fields == validate_candidate(b).canonical_domain_fields

def test_local_registry_never_registers_mock():
    registry = ProviderAdapterRegistry()
    assert registry.for_profile({"adapter_id": "mock"}, "local").code == "adapter_unavailable"
    assert registry.for_profile({"adapter_id": "openai.reference"}, "local").code == "adapter_unavailable"
~~~

Run: python -m pytest backend/tests/contract/test_provider_contract.py backend/tests/contract/test_mock_scenarios.py -q

Expected: FAIL because registry/envelopes/mock scenarios do not exist.

- [ ] **Step 2: Implement the deterministic boundary**

Define the five named ports and the common request fields from CONSTRAINED_AI_PORT_CONTRACT.md. Mock scenarios must cover success, low confidence, source_insufficient, bad schema, timeout, rate limit, cancellation, prompt-injection text, duplicate response, and wording-only changes. All non-candidate states have empty authoritative content. The base registry starts with no production adapter; X2-02 registers `openai.reference` only after its implementation exists, while test/demo profiles explicitly register mock. Do not expose an arbitrary callable/tool list.

- [ ] **Step 3: Verify**

~~~powershell
python -m pytest backend/tests/contract -q
python -m pytest backend/tests -q
~~~

Expected: all scenario invariants pass, an empty local registry fails closed for both mock and not-yet-installed OpenAI, test/demo registration is explicit, and no test opens a network socket or resolves a real credential.

- [ ] **Step 4: Review and commit**

Spec review checks AC-21–24, AC-30, AC-32, AC-38, AC-49. Quality review checks schema strictness, idempotency, timeout/cancellation interfaces, and injection-as-data handling. Commit with feat(T-07): add provider-neutral contract and deterministic mock.
**Commit command:** `git add -- backend/src/projectb/infrastructure/providers/base.py backend/src/projectb/infrastructure/providers/mock.py backend/src/projectb/application/provider.py backend/tests/contract/test_provider_contract.py backend/tests/contract/test_mock_scenarios.py; git diff --cached --check; git commit -m "feat(T-07): add provider-neutral contract and deterministic mock [agent: <fresh-agent-id>]"; git rev-parse HEAD`

**Completion standard:** All later model calls compile against one contract and can be replayed deterministically without an LLM.

### Task M1-01: Inspect Material Metadata and Validate Roles Before Parsing

**Goal:** Enforce the complete v1 input-safety contract before body parsing, provider calls, coverage writes, or plan writes.

**Files:**
- Create: backend/src/projectb/application/material_inspection.py
- Create: backend/src/projectb/infrastructure/file_inspection.py
- Create: backend/tests/unit/test_material_inspection.py
- Create: backend/tests/fixtures/invalid_inputs/README.md

**Interfaces:**
- Consumes: MaterialRole and Mode from T-02, repositories from T-03C, and ProcessingPolicy from T-06.
- Produces: inspect_selected_material(selection: SelectedFile, declared_role: str, limits: MaterialLimits, sniffer: FileSniffer) -> InspectionResult.
- Produces: inspect_batch(course_id: str, selections: Sequence[SelectedFile]) -> BatchInspection.
- InspectionResult uses accepted, unsupported_role, needs_user_review, or rejected plus a white-listed failure code and affected file/page. FileSniffer may read structural metadata but cannot call the body parser or provider.

**Dependencies / parallelism:** Requires T-02, T-03C, and T-06. It owns application/infrastructure input inspection in the materials worktree; the immutable domain/materials.py contract belongs to T-02 and is read-only here. It may run in parallel with T-07 after those dependencies merge. It must not edit provider or UI files.

- [ ] **Step 1: Write and run the failing tests**

~~~python
def test_mime_conflict_is_rejected_without_body_or_network(parser_spy, provider_spy):
    result = inspect_selected_material(
        fake_selected_file("slides.pdf", mime="image/png"),
        "lecture",
        MaterialLimits.v1(),
        fake_sniffer(),
    )
    assert result.code == "mime_extension_conflict"
    assert parser_spy.calls == 0
    assert provider_spy.calls == 0

def test_answer_role_is_rejected_before_body_processing(parser_spy):
    result = inspect_selected_material(
        fake_selected_file("answers.pdf", mime="application/pdf"),
        "answer_key",
        MaterialLimits.v1(),
        fake_sniffer(),
    )
    assert result.code == "unsupported_role"
    assert parser_spy.calls == 0
~~~

Run: python -m pytest backend/tests/unit/test_material_inspection.py -q

Expected: FAIL because MaterialLimits.v1, FileSniffer, and inspect_selected_material do not exist.

- [ ] **Step 2: Implement the minimum behavior**

Implement the exact SPEC v1 limits: PDF extension/MIME/magic, 256 MiB and 2,000 pages; PNG/JPEG/WebP extension/MIME, 20 MiB and 50 megapixels; UTF-8 or UTF-8 BOM TXT/Markdown, 2 MiB; manual teacher_focus from 1 to 10,000 Unicode code points; at most 50 files, 1 GiB, and 5,000 PDF pages per batch. Reject empty, encrypted, corrupt, undecodable, disguised, outside-selection, and over-limit inputs. Explicit answer/personal-note/assignment/unknown roles return unsupported_role. Suspected answer/leak findings return needs_user_review with remote and authoritative write counts fixed at zero.

- [ ] **Step 3: Run green tests and regression**

Run:

~~~powershell
python -m pytest backend/tests/unit/test_material_inspection.py -q
python -m pytest backend/tests/unit -q
python scripts/test_all.py
~~~

Expected: PASS for every limit boundary, allowed MIME/extension pair, invalid encoding, encrypted/corrupt input, path escape, role rejection, and batch aggregate; rejected cases call neither parser nor provider.

- [ ] **Step 4: Review and commit**

SPEC review checks AC-01, AC-15, AC-33, AC-45 and threat controls T-01/T-05/T-20. Quality review checks symlink/path normalization, integer overflow, decompression/resource abuse, deterministic error codes, fixture licensing, and absence of private courseware. A Critical finding blocks M1-02. After both reviews pass, run the credential scan and commit with feat(M1-01): enforce material inspection contract; record the commit hash, red/green evidence, subagent identity, and human changes in PLAN.md and AGENT_LOG.md.
**Commit command:** `git add -- backend/src/projectb/application/material_inspection.py backend/src/projectb/infrastructure/file_inspection.py backend/tests/unit/test_material_inspection.py backend/tests/fixtures/invalid_inputs/README.md; git diff --cached --check; git commit -m "feat(M1-01): enforce material inspection contract [agent: <fresh-agent-id>]"; git rev-parse HEAD`

**Completion standard:** Every selected file and batch has a stable metadata-only result, and no rejected or undecided input can reach body parsing, remote work, coverage, or plan mutation.

### Task M1-02: Import Local Materials and Preserve Raw/Normalized Units

**Goal:** Persist incremental batches with content-hash idempotency, original units, parser versions, quality flags, cancellation hooks, and independent file-level failure.

**Files:**
- Create: backend/src/projectb/infrastructure/parsers.py
- Create: backend/src/projectb/application/material_import.py
- Modify: backend/src/projectb/infrastructure/repositories/material_repo.py
- Create: backend/tests/integration/test_material_import.py
- Create: backend/tests/fixtures/synthetic_materials/README.md
- Create: backend/tests/fixtures/synthetic_materials/good.pdf
- Create: backend/tests/fixtures/synthetic_materials/broken.pdf
- Create: backend/tests/fixtures/synthetic_materials/soft_hyphen.txt

**Interfaces:**
- Consumes: accepted InspectionResult values from M1-01 and database/repository contracts from T-03C.
- Produces: ParserAdapter.inspect_structure(file) -> StructuralMetadata and ParserAdapter.parse(file, cancel_token) -> ParsedMaterial.
- Produces: import_material_batch(course_id, batch_id, inspected_files, mode="L") -> ImportBatchResult.
- MaterialUnit stores raw_text, normalized_text, render_ref, quality_flags, parser_version, material_id, unit identity, and content_hash separately. Repeating course/content_hash/role resolves to the existing material and creates no duplicate local or remote job.

**Dependencies / parallelism:** Requires M1-01 and T-03C. Parser and repository edits are serialized in the materials worktree. It may run in parallel with X2-01 only after T-07 merges.

- [ ] **Step 1: Write and run the failing tests**

~~~python
from pathlib import Path
from types import SimpleNamespace

from projectb.application.material_import import import_material_batch, import_one

good_pdf = Path("backend/tests/fixtures/synthetic_materials/good.pdf")
broken_pdf = Path("backend/tests/fixtures/synthetic_materials/broken.pdf")
text_fixture_with_soft_hyphen = SimpleNamespace(
    path=Path("backend/tests/fixtures/synthetic_materials/soft_hyphen.txt"),
    original_text="mutex\u00ad race condition",
)

def test_partial_failure_and_duplicate_import_are_independent(tmp_path):
    first = import_material_batch("course", "batch-1", [good_pdf, broken_pdf], mode="L")
    second = import_material_batch("course", "batch-2", [good_pdf], mode="L")
    assert first.files["good_pdf"].state == "ready"
    assert first.files["broken_pdf"].state == "failed"
    assert second.files["good_pdf"].material_id == first.files["good_pdf"].material_id
    assert second.created_material_ids == []
    assert second.remote_jobs == []

def test_normalization_never_overwrites_raw_text():
    page = import_one(text_fixture_with_soft_hyphen)
    assert page.raw_text != page.normalized_text
    assert page.raw_text == text_fixture_with_soft_hyphen.original_text
~~~

Run: python -m pytest backend/tests/integration/test_material_import.py -q

Expected: FAIL because ParserAdapter, import_material_batch, and raw/normalized unit persistence are absent.

- [ ] **Step 2: Implement the minimum behavior**

Generate the three tiny fixture files deterministically in the test-fixture commit and document their origin/license in the fixture README; `broken.pdf` must have a valid PDF extension/MIME declaration but intentionally malformed bytes. Hash accepted files before parsing, persist one batch-file state per input, and keep original page/image/text/manual identity separate from extraction. Use only synthetic or explicitly licensed fixtures. Store parser/version and quality flags for low-text, visual-only, animation-first-frame, and warning states. Roll back only the failed file, keep successful files, expose an independent retry, and honor cancellation without launching new units. Manual teacher_focus uses manual_entry SourceLocator and never receives a fake page number.

- [ ] **Step 3: Run green tests and regression**

Run:

~~~powershell
python -m pytest backend/tests/integration/test_material_import.py -q
python -m pytest backend/tests/unit backend/tests/integration -q
python scripts/test_all.py
~~~

Expected: PASS for PDF/image/text/manual fixtures, duplicate submissions, partial failure, cancellation, restart, and parser warnings; source identity and raw text remain intact.

- [ ] **Step 4: Review and commit**

SPEC review checks AC-03, AC-15, AC-16, AC-17, AC-45 and AC-46 prerequisites. Quality review checks parser isolation, file-handle cleanup, bounded memory, cancellation, transactional recovery, idempotency, and parser/license evidence. A Critical finding blocks M1-03. After both reviews pass, scan credentials and commit with feat(M1-02): add incremental local material import; update PLAN.md and AGENT_LOG.md with the real hash and evidence.
**Commit command:** `git add -- backend/src/projectb/infrastructure/parsers.py backend/src/projectb/application/material_import.py backend/src/projectb/infrastructure/repositories/material_repo.py backend/tests/integration/test_material_import.py backend/tests/fixtures/synthetic_materials/README.md backend/tests/fixtures/synthetic_materials/good.pdf backend/tests/fixtures/synthetic_materials/broken.pdf backend/tests/fixtures/synthetic_materials/soft_hyphen.txt; git diff --cached --check; git commit -m "feat(M1-02): add incremental local material import [agent: <fresh-agent-id>]"; git rev-parse HEAD`

**Completion standard:** Local mode imports a safe mixed synthetic batch into traceable raw/normalized units, survives a partial failure/restart, and never creates duplicate authoritative material.

### Task M1-03: Retrieve Source Context and Confirm Coverage Diffs

**Goal:** Make source retrieval and added/reinforced/changed/unmapped/duplicate coverage candidates explicit, reviewable, and unable to mutate authoritative course knowledge before confirmation.

**Files:**
- Create: backend/src/projectb/application/source_context.py
- Create: backend/src/projectb/application/coverage.py
- Create: backend/tests/unit/test_coverage_confirmation.py
- Create: backend/tests/integration/test_source_context.py

**Interfaces:**
- Consumes: material units from M1-02, SourceLocator proof from T-02, processing policy from T-06, and provider candidate envelopes from T-07.
- Produces: retrieve_context(course_id, source_scope, locator) -> ContextBundle containing raw/normalized unit data and quality flags.
- Produces: propose_coverage(batch_id, candidate_source_scope) -> Sequence[ConceptCoverage].
- Produces: confirm_coverage(coverage_id, decision, reason, actor="local_user") -> CoverageDecision and authoritative_concepts(course_id) -> Sequence[KnowledgeConcept].
- Only accepted CoverageDecision history is authoritative; candidate confidence is a review signal, not a fact.

**Dependencies / parallelism:** Requires M1-02, T-02, T-06, and T-07. It owns application/source_context.py and application/coverage.py in the materials worktree; domain/materials.py remains a T-02-owned immutable contract and is not modified here. M2/M3 may start only after these interfaces merge.

- [ ] **Step 1: Write and run the failing tests**

~~~python
def test_unconfirmed_coverage_cannot_enter_authoritative_course(service):
    candidate = service.propose_coverage("batch-1", ["source-25"])[0]
    assert service.authoritative_concepts("course-1") == []
    service.confirm_coverage(candidate.id, "accepted", "matches source", actor="local_user")
    assert service.authoritative_concepts("course-1") == [candidate.concept_id]

def test_stale_hash_locator_is_rejected():
    with pytest.raises(SourceInvalid):
        retrieve_context(
            "course-1",
            ["source-25"],
            PdfPageLocator(material_id="m", content_hash="old", page=25),
        )
~~~

Run: python -m pytest backend/tests/unit/test_coverage_confirmation.py backend/tests/integration/test_source_context.py -q

Expected: FAIL because ContextBundle, coverage candidate/decision services, and authority filtering do not exist.

- [ ] **Step 2: Implement the minimum behavior**

Validate owner, source scope, content hash/version, and page/image/line/manual bounds on every retrieval. Preserve original units. Generate stable coverage relations and explicit conflict/low-confidence states. Append every accept/reject/correction; do not overwrite old decisions. Missing, deleted, ambiguous, or stale locators return source_insufficient and zero coverage/plan writes. Provider candidates enter only this candidate path.

- [ ] **Step 3: Run green tests and regression**

Run:

~~~powershell
python -m pytest backend/tests/unit/test_coverage_confirmation.py backend/tests/integration/test_source_context.py -q
python -m pytest backend/tests -q
python scripts/test_all.py
~~~

Expected: PASS for all five diff relations, conflicts, corrections, owner mismatch, deleted/stale/ambiguous locators, and repeated decisions; only confirmed coverage is scheduler-visible.

- [ ] **Step 4: Review and commit**

SPEC review checks AC-03, AC-16, AC-17, AC-19, AC-25, AC-37. Quality review checks optimistic concurrency, stable ordering, owner scope, append-only decisions, and redacted conflict errors. A Critical finding blocks X2-01, M2-02A, and M3-01. After both reviews pass, scan credentials and commit with feat(M1-03): add source-bound coverage confirmation; update the shared ledgers with the actual hash.
**Commit command:** `git add -- backend/src/projectb/application/source_context.py backend/src/projectb/application/coverage.py backend/tests/unit/test_coverage_confirmation.py backend/tests/integration/test_source_context.py; git diff --cached --check; git commit -m "feat(M1-03): add source-bound coverage confirmation [agent: <fresh-agent-id>]"; git rev-parse HEAD`

**Completion standard:** The material workspace returns validated source context and a complete candidate diff, while only an explicit append-only user decision can change authoritative course knowledge.

### Task X2-01: Dispatch Constrained Ports and Validate Candidate Responses

**Goal:** Centralize request-envelope, consent/source, schema, budget, timeout, cancellation, and authority checks for all five named model ports.

**Files:**
- Create: backend/src/projectb/application/port_dispatcher.py
- Create: backend/src/projectb/domain/provider_candidates.py
- Create: backend/tests/contract/test_port_dispatcher.py
- Create: backend/tests/contract/test_candidate_authority.py

**Interfaces:**
- Consumes: consent/scope from T-06, registry/mock from T-07, and source/coverage from M1-03.
- Produces: PortDispatcher.call(port_name, request_context, adapter) -> ValidatedPortResult.
- Produces: validate_port_request(request) -> NormalizedRequest | RequestError.
- Produces: validate_port_response(response, source_catalog, authority_matrix) -> ValidatedCandidate.
- ValidatedPortResult statuses are candidate, source_insufficient, schema_rejected, provider_scope_violation, provider_config_invalid, credential_unavailable, capability_unsupported, policy_unknown, provider_failed, cancelled, or budget_exceeded.

**Dependencies / parallelism:** Requires T-06, T-07, and M1-03. It owns the only application-level model dispatcher. OpenAI, M2, and M3 code cannot call adapters directly. It may run in parallel with M2-01.

- [ ] **Step 1: Write and run the failing tests**

~~~python
from projectb.application.port_dispatcher import PortDispatcher, validate_port_response


class AdapterSpy:
    def __init__(self):
        self.calls = 0

    def invoke(self, request, secret_handle=None):
        self.calls += 1
        return {"status": "candidate", "candidate": {}}


def make_request(source_scope):
    return {
        "port": "generate_explanation",
        "port_version": "1",
        "source_scope": source_scope,
        "idempotency_key": "x2-test-1",
        "input": {"concept_id": "mutex"},
    }


def test_empty_source_scope_never_reaches_adapter():
    adapter_spy = AdapterSpy()
    dispatcher = PortDispatcher()
    result = dispatcher.call("generate_explanation", make_request([]), adapter_spy)
    assert result.status == "source_insufficient"
    assert adapter_spy.calls == 0

def test_bad_schema_cannot_emit_authoritative_updates():
    bad_schema_response = {"status": "candidate", "candidate": {"unexpected": True}}
    catalog = {"source-1": {"material_id": "material-1", "content_hash": "hash-1"}}
    authority_matrix = {"generate_explanation": []}
    result = validate_port_response(bad_schema_response, catalog, authority_matrix)
    assert result.status == "schema_rejected"
    assert result.authoritative_updates == []
~~~

Run: python -m pytest backend/tests/contract/test_port_dispatcher.py backend/tests/contract/test_candidate_authority.py -q

Expected: FAIL because dispatcher, request normalization, candidate validation, and the authority matrix are absent.

- [ ] **Step 2: Implement the minimum behavior**

Require the port/version, course/task IDs, source/evidence scope, input digest, limits, idempotency key, profile/config/capability/policy fingerprints, and response-schema version. Reject arbitrary paths, credentials, executable tool parameters, unknown ports, missing consent, and mismatched snapshots before adapter resolution. Coverage/exam candidates require validated locators; explanation/practice/feedback without one are model_supplement only. Do not allow implicit port chaining or retries beyond the bounded policy.

- [ ] **Step 3: Run green tests and regression**

Run:

~~~powershell
python -m pytest backend/tests/contract/test_port_dispatcher.py backend/tests/contract/test_candidate_authority.py -q
python -m pytest backend/tests/contract -q
python scripts/test_all.py
~~~

Expected: PASS for empty/out-of-scope sources, stale consent, bad schema, injection text, timeout, cancellation, rate limit, and budget exhaustion; authoritative coverage, plan, due_at, mastery, consent, and deletion remain unchanged.

- [ ] **Step 4: Review and commit**

SPEC review checks AC-21–24, AC-30–32, AC-37–39. Quality review checks strict schema parsing, cancellation propagation, bounded retries, idempotency, provider-reference redaction, and the absence of an agent loop/tool dispatcher. A Critical finding blocks X2-02 and M2-02A. After both reviews pass, scan credentials and commit with feat(X2-01): add constrained port dispatcher; record hash/evidence/reviews in PLAN.md and AGENT_LOG.md.
**Commit command:** `git add -- backend/src/projectb/application/port_dispatcher.py backend/src/projectb/domain/provider_candidates.py backend/tests/contract/test_port_dispatcher.py backend/tests/contract/test_candidate_authority.py; git diff --cached --check; git commit -m "feat(X2-01): add constrained port dispatcher [agent: <fresh-agent-id>]"; git rev-parse HEAD`

**Completion standard:** Every model interaction has one auditable path from an exact consented source scope to candidate-only output, and all failure statuses preserve authoritative state.

### Task X2-02: Implement the OpenAI Reference Adapter for P Requests

**Goal:** Add the single built-in local-production adapter for consented page/fragment Responses calls without leaking provider details into domain state.

**Files:**
- Create: backend/src/projectb/infrastructure/providers/openai.py
- Create: backend/src/projectb/infrastructure/providers/openai_http.py
- Create: backend/tests/contract/test_openai_request_policy.py
- Create: backend/tests/integration/test_openai_adapter_fake_transport.py

**Interfaces:**
- Consumes: X2-01 dispatcher, T-05 SecretStore, T-06 consent, G-02A's verified client/license, and G-02B's policy/capability/cost evidence.
- Produces: build_responses_payload(request: ProviderRequestEnvelope) -> dict.
- Produces: OpenAIReferenceAdapter.describe() -> CapabilityDescriptor and invoke(request, secret_handle, transport) -> ProviderResponseEnvelope.
- Produces: OpenAITransport.post(payload, headers, timeout_ms) -> RawResponse; tests always inject a fake transport.

**Dependencies / parallelism:** Requires X2-01, G-02A, and G-02B. It owns the built-in OpenAI adapter files and may run in parallel with M2-01/M3-01. No real key/network is used outside INT-01.

- [ ] **Step 1: Write and run the failing tests**

~~~python
import json

from projectb.infrastructure.providers.openai import OpenAIReferenceAdapter, build_responses_payload


PAGE_REQUEST = {
    "port": "generate_explanation",
    "port_version": "1",
    "source_scope": ["source-1#page=1"],
    "store": False,
    "input": {"concept_id": "mutex"},
}
STALE_CONSENT_REQUEST = {**PAGE_REQUEST, "consent_record_id": "stale-consent"}


class FakeSecretHandle:
    pass


class FakeTransport:
    def __init__(self):
        self.calls = 0

    def post(self, *args, **kwargs):
        self.calls += 1
        raise AssertionError("stale policy must fail before transport")


def test_payload_uses_store_false_and_no_unapproved_hosted_tools():
    payload = build_responses_payload(PAGE_REQUEST)
    assert payload["store"] is False
    assert payload.get("background", False) is False
    assert payload.get("tools", []) == []
    assert "credential_ref" not in json.dumps(payload)

def test_policy_mismatch_blocks_transport():
    fake_transport = FakeTransport()
    adapter = OpenAIReferenceAdapter()
    result = adapter.invoke(STALE_CONSENT_REQUEST, FakeSecretHandle(), fake_transport)
    assert result.status == "provider_config_invalid"
    assert fake_transport.calls == 0
~~~

Run: python -m pytest backend/tests/contract/test_openai_request_policy.py backend/tests/integration/test_openai_adapter_fake_transport.py -q

Expected: FAIL because request construction, transport, and the reference adapter are absent.

- [ ] **Step 2: Implement the minimum behavior**

Use only the G-02A verified client and G-02B policy/capability contract. Build foreground Responses requests with store:false, no background, Conversations, remote MCP, Hosted Shell, or Code Interpreter; P sends only consented pages/images within limits and a strict response schema. Resolve the secret only inside the transport call. Normalize refusal, timeout, rate limit, cancellation, malformed response/schema, and provider IDs to provider-neutral statuses. Reject base_url, custom endpoint, plugin/module path, unknown profile fields, stale snapshots, and absent credentials before network access. Never present store:false as ZDR.

- [ ] **Step 3: Run green tests and regression**

Run:

~~~powershell
python -m pytest backend/tests/contract/test_openai_request_policy.py backend/tests/integration/test_openai_adapter_fake_transport.py -q
python -m pytest backend/tests/contract backend/tests/integration -q
python scripts/test_all.py
~~~

Expected: PASS for captured compliant payload, structured success/refusal, malformed schema, timeout/rate limit, stale policy/config, unsupported endpoint fields, missing secret, and prompt-injection output; fake transport sees only approved scope.

- [ ] **Step 4: Review and commit**

SPEC review checks AC-21, AC-22, AC-30–32, AC-37–39, AC-49. Quality review checks secret lifetime, payload/log redaction, timeout/cancellation, dependency/license evidence, endpoint immutability, and policy-snapshot wording. A Critical finding blocks X2-03A and INT-01. After both reviews pass, scan credentials and commit with feat(X2-02): add OpenAI reference adapter for P; update the shared ledgers with the real hash.
**Commit command:** `git add -- backend/src/projectb/infrastructure/providers/openai.py backend/src/projectb/infrastructure/providers/openai_http.py backend/tests/contract/test_openai_request_policy.py backend/tests/integration/test_openai_adapter_fake_transport.py; git diff --cached --check; git commit -m "feat(X2-02): add OpenAI reference adapter for P [agent: <fresh-agent-id>]"; git rev-parse HEAD`

**Completion standard:** Fake-transport tests prove a compliant P request and every failure path; local production exposes no other real adapter and no unverified provider assertion.

### Task Group X2-03 (not dispatchable): F Remote Lifecycle, Scope Filtering, Recovery, and Deletion

**Goal:** Track whole-file upload/index/search/delete with exact consent, per-course stores, at-least-once recovery, request filtering, File-ID allowlisting, locator proof, and truthful incomplete states.

**Files:**
- Create: backend/src/projectb/domain/remote.py
- Create: backend/src/projectb/application/remote.py
- Create: backend/src/projectb/infrastructure/providers/openai_files.py
- Modify: backend/src/projectb/infrastructure/repositories/remote_repo.py
- Create: backend/tests/contract/test_remote_lifecycle.py
- Create: backend/tests/integration/test_remote_recovery.py

**Interfaces:**
- Consumes: X2-02 adapter, T-03C persistence, T-06 consent/scope tokens, and T-02 locator proof.
- Produces: RemoteMaterialService.enqueue_upload(consent_id, material_id) -> RemoteJob.
- Produces: reconcile_job(job_id) -> RemoteMaterialObject, build_file_search_request(scope_tokens, allowed_file_ids) -> dict, validate_file_search_results(results, allowed_file_ids) -> ValidatedResults | ScopeViolation, and request_delete(object_id, reason) -> RemoteJob.
- RemoteMaterialObject separates provider File, association, and course/profile/config-exclusive Vector Store references and states.

**Dependencies / parallelism:** Group summary only. X2-03A requires X2-02/T-03C/T-06; X2-03B requires X2-03A; X2-03C requires X2-03B/G-02B. Migration/repository changes are serialized with the persistence owner. X2-03C must finish before M1-04 and INT-01.

- [ ] **Step 1: Write and run the failing tests**

~~~python
def test_f_without_consent_stays_awaiting_and_calls_nothing(remote_adapter):
    state = service.enqueue_upload("missing-consent", "material-1")
    assert state.state == "awaiting_consent"
    assert remote_adapter.calls == []

def test_any_out_of_allowlist_file_discards_the_full_response():
    with pytest.raises(ScopeViolation):
        validate_file_search_results(
            [result(file_id="allowed"), result(file_id="revoked")],
            ["allowed"],
        )
~~~

Run: python -m pytest backend/tests/contract/test_remote_lifecycle.py backend/tests/integration/test_remote_recovery.py -q

Expected: FAIL because the remote state machine, search filter, and recovery service are absent.

- [ ] **Step 2: Implement the minimum behavior in three fresh checkpoints**

1. **X2-03A lifecycle/scope:** persist the consent-to-upload/index state machine, exact adapter/profile/config/policy/material/hash/consent idempotency tuple, per-course/profile/config store ownership, association scope-token attributes, and post-result File-ID allowlisting.
2. **X2-03B recovery:** persist references before transitions, reconcile after timeout/restart, quarantine duplicates, bound polling/retry, and expose truthful `reconcile_required`/`credential_unavailable` states. Do not promise provider exactly-once.
3. **X2-03C deletion/expiry:** map only unique normalized spans of at least 32 code points to locators, then delete association, File, and an empty exclusive store in order; unknown cleanup remains incomplete and unusable.

Each checkpoint adds and runs its own focused red test before implementation, then runs the shared regression and exact commit command from the protocol. No subagent may implement two checkpoints in one session.

- [ ] **Step 3: Run green tests and regression**

Run:

~~~powershell
python -m pytest backend/tests/contract/test_remote_lifecycle.py backend/tests/integration/test_remote_recovery.py -q
python -m pytest backend/tests -q
python scripts/test_all.py
~~~

Expected: PASS for partial failure, lost response, restart, cancellation, offline recovery, duplicate objects, config/profile change, revoked scope, cross-file result, ambiguous/short/visual-only locator, single-file deletion, course deletion, and unsupported capability. No unusable or out-of-scope object reaches a port.

- [ ] **Step 4: Review and commit**

Group review checks AC-26, AC-27, AC-28, AC-29, AC-37, AC-48, AC-50 and the remote lifecycle matrix after X2-03A/B/C. Quality review checks transaction ordering, bounded polling/retry, provider-ref redaction, duplicate isolation/cost language, store ownership, and deletion evidence. A Critical finding blocks M1-04. No worker commit is assigned to this group heading; use the three unit commit commands below.

**Completion standard:** F remains disabled unless tracking/filter/result/deletion capabilities are proven; every object is recoverable and source-isolated, and every unknown cleanup state is visible and unusable.

### Task X2-03A: Add F Enqueue, State, and Scope Contracts

**Goal:** Establish exact-consent F enqueue, remote state/domain objects, idempotency keys, store ownership, and allowlisted search scope without polling or deletion behavior.

**Files:** Create `backend/src/projectb/domain/remote.py`, `backend/src/projectb/application/remote.py`, and `backend/tests/contract/test_remote_enqueue.py`; modify `backend/src/projectb/infrastructure/repositories/remote_repo.py` only through the T-03C interface.

**Interfaces:** `enqueue_upload(consent_id, material_id)`, remote object/job states through indexing/ready, one store per course/profile/config, scope-token metadata filtering, and post-result File-ID allowlisting.

**Dependencies / parallelism:** Requires X2-02, T-03C, T-06, and T-02. It owns the remote domain/application interface and completes before X2-03B.

- [ ] **Red:** assert missing/stale consent performs zero calls, the idempotency tuple is stable, and one out-of-allowlist result discards the whole response; run `python -m pytest backend/tests/contract/test_remote_enqueue.py -q`. Expected: FAIL because F enqueue/scope contracts are absent.
- [ ] **Green/refactor:** implement only enqueue/state/scope validation; run the focused test, `python -m pytest backend/tests/contract -q`, and `python scripts/test_all.py`.
- [ ] **Reviews:** SPEC review AC-26, AC-28, AC-29, AC-37, AC-48; quality review exact consent, canonical tokens, File-ID filtering, provider-ref redaction, and no out-of-scope candidate. Critical findings block X2-03B.
- [ ] **Commit:** scan secrets; `git add -- backend/src/projectb/domain/remote.py backend/src/projectb/application/remote.py backend/src/projectb/infrastructure/repositories/remote_repo.py backend/tests/contract/test_remote_enqueue.py`; run `git diff --cached --check`; commit with `git commit -m "feat(X2-03A): add F job and scope contract [agent: <fresh-agent-id>]"`.

**Completion standard:** An exact current consent can create one scoped F job, while stale/missing consent or any cross-file result produces no authoritative candidate.

### Task X2-03B: Add Remote Polling, Restart, and Idempotency Recovery

**Goal:** Reconcile at-least-once provider operations after timeout, cancellation, duplicate response, process restart, or credential loss without claiming exactly-once behavior.

**Files:** Modify `backend/src/projectb/application/remote.py` and `backend/src/projectb/infrastructure/repositories/remote_repo.py`; create `backend/tests/integration/test_remote_recovery.py`.

**Interfaces:** `reconcile_job(job_id)`, bounded status polling/retry, persisted provider references before transitions, duplicate quarantine, and truthful recovery states.

**Dependencies / parallelism:** Requires X2-03A. Shared remote files are serially owned; completes before X2-03C.

- [ ] **Red:** add lost-response, restart, duplicate, cancellation, offline, stale-config, and credential-unavailable cases; run `python -m pytest backend/tests/integration/test_remote_recovery.py -q`. Expected: FAIL because reconciliation/recovery is absent.
- [ ] **Green/refactor:** implement bounded recovery and quarantine only; run the focused test, `python -m pytest backend/tests/integration -q`, and `python scripts/test_all.py`.
- [ ] **Reviews:** SPEC review AC-26, AC-27, AC-28, AC-48, AC-50; quality review transaction ordering, timeouts, retry/idempotency, restart determinism, cost language, and no exactly-once claim. Critical findings block X2-03C.
- [ ] **Commit:** scan secrets; `git add -- backend/src/projectb/application/remote.py backend/src/projectb/infrastructure/repositories/remote_repo.py backend/tests/integration/test_remote_recovery.py`; run `git diff --cached --check`; commit with `git commit -m "feat(X2-03B): add remote recovery [agent: <fresh-agent-id>]"`.

**Completion standard:** Every interrupted job resumes, quarantines, or remains visibly incomplete from persisted state, without duplicating usable provider objects silently.

### Task X2-03C: Add Remote Deletion and Provider-object Reconciliation

**Goal:** Delete associations, Files, and empty exclusive stores in a verified order and keep ambiguous cleanup unusable and visible.

**Files:** Create `backend/src/projectb/infrastructure/providers/openai_files.py` and `backend/tests/integration/test_remote_deletion.py`; modify `backend/src/projectb/application/remote.py` and `backend/src/projectb/infrastructure/repositories/remote_repo.py`.

**Interfaces:** `request_delete(object_id, reason)`, ordered association/File/store cleanup, expiry reconciliation, locator invalidation, and `deleted | delete_incomplete | credential_unavailable` reports.

**Dependencies / parallelism:** Requires X2-03B and G-02B capability evidence. Shared remote files remain serial. M1-04 and INT-01 depend on this terminal unit.

- [ ] **Red:** add single-file, shared/non-empty store, course deletion, expiry, missing credential, unknown provider state, and locator invalidation tests; run `python -m pytest backend/tests/integration/test_remote_deletion.py -q`. Expected: FAIL because deletion reconciliation is absent.
- [ ] **Green/refactor:** implement the minimum ordered cleanup and fail-closed incomplete states; run the focused test, all remote tests, and `python scripts/test_all.py`.
- [ ] **Reviews:** SPEC review AC-27, AC-28, AC-29, AC-37, AC-48, AC-50; quality review deletion order/evidence, store ownership, bounded retry, provider-reference redaction, capability gating, and non-reconstructive history. Critical findings block M1-04.
- [ ] **Commit:** scan secrets; `git add -- backend/src/projectb/infrastructure/providers/openai_files.py backend/src/projectb/application/remote.py backend/src/projectb/infrastructure/repositories/remote_repo.py backend/tests/integration/test_remote_deletion.py`; run `git diff --cached --check`; commit with `git commit -m "feat(X2-03C): add remote deletion reconciliation [agent: <fresh-agent-id>]"`.

**Completion standard:** Cleanup reports only observed provider/local states, and every unproved or incomplete object is excluded from search, learning, and plan inputs.

### Task M1-04: Delete Materials, Invalidate Sources, and Coordinate Remote Cleanup

**Goal:** Make material deletion a verifiable cascade that removes reconstructive content, preserves minimal history, and never reports incomplete remote cleanup as success.

**Files:**
- Create: backend/src/projectb/application/material_deletion.py
- Modify: backend/src/projectb/infrastructure/repositories/material_repo.py
- Modify: backend/src/projectb/infrastructure/repositories/remote_repo.py
- Create: backend/tests/integration/test_material_deletion.py

**Interfaces:**
- Consumes: source/coverage from M1-03, remote lifecycle from X2-03C, tombstones from T-03C, and credential status from T-05.
- Produces: delete_material(material_id, actor="local_user") -> DeletionReport.
- DeletionReport contains local_state, invalid_locator_ids, remote_states, pending_job_ids, and a white-listed recovery_code.
- Retrieval, candidate validation, and new provider requests reject deleted/invalid locators immediately.

**Dependencies / parallelism:** Requires M1-03 and X2-03C. It owns the cross-layer deletion transaction in the materials worktree and cannot run in parallel with repository migration edits.

- [ ] **Step 1: Write and run the failing test**

~~~python
def test_delete_removes_reconstructive_content_but_preserves_history():
    report = delete_material("material-1")
    assert retrieve_body("material-1") is None
    assert retrieve_history("material-1").tombstone is True
    assert report.local_state == "deleted"
    assert report.remote_states in ({"deleted"}, {"delete_incomplete"})
~~~

Run: python -m pytest backend/tests/integration/test_material_deletion.py -q

Expected: FAIL because the local/remote cascade and locator invalidation are not wired.

- [ ] **Step 2: Implement the minimum behavior**

Stop queued work, invalidate locators/references, remove original copies, page renders, extracted/normalized text, and reconstructive indexes, then preserve attempts/evidence/old plans with non-reconstructive tombstones and source-invalid markers. Immediately remove revoked material from provider scope. Delete its association and File; delete a Vector Store only when course/F removal and reconciliation prove it empty. Missing credentials or any unproved layer returns credential_unavailable/delete_incomplete with bounded recovery instructions.

- [ ] **Step 3: Run green tests and regression**

Run:

~~~powershell
python -m pytest backend/tests/integration/test_material_deletion.py -q
python -m pytest backend/tests -q
python scripts/test_all.py
~~~

Expected: PASS for local-only, F-ready, partial remote failure, repeated deletion, forced credential clear, and shared-course-store scenarios; deleted content is not retrievable while other materials and old non-reconstructive history remain.

- [ ] **Step 4: Review and commit**

SPEC review checks AC-06, AC-17, AC-28–30, AC-40 and threat controls T-08/T-18. Quality review checks transaction rollback, background-job cancellation, tombstone minimization, idempotent retries, and provider-reference redaction. A Critical finding blocks API/UI material-deletion work. After both reviews pass, scan credentials and commit with feat(M1-04): add verifiable material deletion; update PLAN.md and AGENT_LOG.md with hash/evidence/reviews.
**Commit command:** `git add -- backend/src/projectb/application/material_deletion.py backend/src/projectb/infrastructure/repositories/material_repo.py backend/src/projectb/infrastructure/repositories/remote_repo.py backend/tests/integration/test_material_deletion.py; git diff --cached --check; git commit -m "feat(M1-04): add verifiable material deletion [agent: <fresh-agent-id>]"; git rev-parse HEAD`

**Completion standard:** A deletion report reflects actual local and remote state, and deleted content cannot re-enter retrieval, coverage, plans, learning evidence, or provider scope.

### Task M2-01: Implement the Mutex/Race Parameterized Oracle and Starting Probes

**Goal:** Provide the first vertical learning slice's deterministic diagnosis, legal-interleaving oracle, and rubric without model authority.

**Files:**
- Create: backend/src/projectb/domain/learning.py
- Create: backend/src/projectb/application/mutex_race.py
- Create: backend/tests/unit/test_mutex_race_oracle.py
- Create: backend/tests/fixtures/mutex_race_traces.json

**Interfaces:**
- Consumes: T-02 source types and T-03C evidence persistence interfaces.
- Produces: TraceSpec(seed, thread_events, shared_state, expected_final_state), enumerate_legal_interleavings(trace) -> Sequence[Interleaving], and evaluate_interleaving(answer, trace) -> OracleResult.
- Produces: run_starting_probes(trace, max_probes=3) -> Sequence[ProbeResult] with prerequisite, read_modify_write, or bad_interleaving failure categories.
- ProbeResult has no permanent mastery update. OracleResult exposes thread_order_ok, events_complete, final_value_ok, and stable error codes.

**Dependencies / parallelism:** Requires T-02 and T-03C. It may run in parallel with X2-01 and M3-01 because it owns learning/oracle files and emits no plan state.

- [ ] **Step 1: Write and run the failing tests**

~~~python
def test_seeded_trace_replays_legal_order_and_final_value():
    result = evaluate_interleaving(answer_for_seed(11), trace_for_seed(11))
    assert result.thread_order_ok is True
    assert result.events_complete is True
    assert result.final_value_ok is True

def test_probe_budget_is_three_and_diagnosis_is_not_mastery():
    results = run_starting_probes(trace_for_seed(3), max_probes=3)
    assert len(results) <= 3
    assert all(result.permanent_mastery_update is None for result in results)
~~~

Run: python -m pytest backend/tests/unit/test_mutex_race_oracle.py -q

Expected: FAIL because TraceSpec, the oracle, and probe runner do not exist.

- [ ] **Step 2: Implement the minimum behavior**

Represent the confirmed dependency chain from concurrent execution through shared state, non-atomic read-modify-write, interleaving, race, critical section, and one mutual-exclusion safety reason. Validate per-thread event order, event completeness, legal interleaving, and terminal shared value. Keep probe diagnosis separate from later evidence and mastery. Fixed seeds must produce the same trace and expected outcomes regardless of provider output.

- [ ] **Step 3: Run green tests and regression**

Run:

~~~powershell
python -m pytest backend/tests/unit/test_mutex_race_oracle.py -q
python -m pytest backend/tests/unit -q
python scripts/test_all.py
~~~

Expected: PASS for legal and illegal order, omitted/duplicate events, wrong final value, deterministic seed replay, all three diagnosis categories, and the three-probe cap; no model/mock text affects correctness.

- [ ] **Step 4: Review and commit**

SPEC review checks AC-12–14 and the five required vertical-slice stages. Quality review checks seeded reproducibility, exhaustive event validation, bounded complexity, stable error codes, and absence of hidden scoring weights. A Critical finding blocks M2-02A. After both reviews pass, scan credentials and commit with feat(M2-01): add mutex race oracle and probes; record hash and evidence in shared ledgers.
**Commit command:** `git add -- backend/src/projectb/domain/learning.py backend/src/projectb/application/mutex_race.py backend/tests/unit/test_mutex_race_oracle.py backend/tests/fixtures/mutex_race_traces.json; git diff --cached --check; git commit -m "feat(M2-01): add mutex race oracle and probes [agent: <fresh-agent-id>]"; git rev-parse HEAD`

**Completion standard:** The first learning slice has a replayable local correctness oracle and bounded probe diagnosis that remain fully testable with the real model removed.

### Task Group M2-02 (not dispatchable): Source-Bound Explanation, Practice, Feedback, and Evidence Flow

**Goal:** Connect source-bound explanations and practice candidates to deterministic evaluation and append-only LearningEvidence without directly changing mastery.

**Files:**
- Create: backend/src/projectb/application/learning.py
- Create: backend/src/projectb/application/evidence.py
- Modify: backend/src/projectb/domain/learning.py
- Create: backend/tests/integration/test_learning_flow.py
- Create: backend/tests/contract/test_learning_provider_boundary.py

**Interfaces:**
- Consumes: M2-01 oracle, M1-03 source/coverage, X2-01 dispatcher, and T-03C learning repository.
- Produces: start_explanation(course_id, concept_id, goal, baseline_evidence_ids, source_ids) -> ExplanationSession.
- Produces: create_practice_candidate(concept_id, trace_seed, source_scope) -> PracticeCandidate, evaluate_attempt(attempt, oracle) -> EvaluatorResult, record_learning_evidence(session_id, evaluator_result, occurred_at) -> LearningEvidence, and generate_feedback(evaluator_result, source_ids) -> FeedbackCandidate.
- FeedbackCandidate has no scoring authority; ExplanationSession cannot update mastery.

**Dependencies / parallelism:** Requires M2-01, M1-03, and X2-01. It may run in parallel with M3-01 after M2-01 merges, but M3-02A waits for this evidence contract.

- [ ] **Step 1: Write and run the failing tests**

~~~python
from datetime import datetime, timezone

def test_explanation_without_locator_is_supplement_only():
    session = start_explanation("c", "concept", "goal", [], [])
    assert session.material_fact_status == "model_supplement"
    assert session.mastery_updates == []

def test_successful_check_appends_oracle_evidence():
    trace = trace_for_seed(11)
    answer = answer_for_seed(11)
    result = evaluate_attempt(answer, lambda value: evaluate_interleaving(value, trace))
    occurred_at = datetime(2026, 7, 20, 12, 0, tzinfo=timezone.utc)
    evidence = record_learning_evidence("session", result, occurred_at)
    assert evidence.outcome == "demonstrated_now"
    assert evidence.evaluator == "mutex_race_oracle"
~~~

Run: python -m pytest backend/tests/integration/test_learning_flow.py backend/tests/contract/test_learning_provider_boundary.py -q

Expected: FAIL because explanation/practice/evidence orchestration and the evaluator/provider boundary are absent.

- [ ] **Step 2: Implement the minimum behavior**

Run at most three probes, select explanation shape from the deterministic failure category, and require validated locators for material facts. Practice candidates carry a replayable trace seed, source scope, and rubric. Evaluate locally, append evidence transactionally, and store only redacted response references in ordinary logs. Provider feedback may explain a deterministic result but cannot change pass/fail, evidence outcome, mastery, plan, consent, source, or deletion. Provider failure preserves the session and existing state.

- [ ] **Step 3: Run green tests and regression**

Run:

~~~powershell
python -m pytest backend/tests/integration/test_learning_flow.py backend/tests/contract/test_learning_provider_boundary.py -q
python -m pytest backend/tests -q
python scripts/test_all.py
~~~

Expected: PASS for source-bound success, model_supplement, malformed/injected/provider-failed feedback, wrong-source candidate, same-seed replay, isomorphic check, transfer check, and append-only evidence; no explanation alone changes mastery.

- [ ] **Step 4: Review and commit**

Group review checks AC-03, AC-04, AC-12–14, AC-21–24, AC-32 after M2-02A/B. Quality review checks evaluator/provider separation, answer/log redaction, transactionality, retry/cancellation, and evidence provenance. A Critical finding blocks M3-02A and API-02A. No worker commit is assigned to this heading; use the two unit commit commands below.

**Completion standard:** A student can complete the deterministic explanation/check cycle, inspect source/rubric, and append learning evidence without a false mastery or plan update.

### Task M2-02A: Build Source-bound Explanation and Practice Candidates

**Goal:** Orchestrate source-bound explanations, bounded probes, and replayable practice candidates while keeping all outputs candidate-only.

**Files:** Create `backend/src/projectb/application/learning.py` and `backend/tests/contract/test_learning_provider_boundary.py`; modify `backend/src/projectb/domain/learning.py`.

**Interfaces:** `start_explanation`, `create_practice_candidate`, at-most-three probes, validated locator requirements, supplement status, replayable trace seed/rubric, and unchanged state on provider failure.

**Dependencies / parallelism:** Requires M2-01, M1-03, and X2-01. It owns session/candidate orchestration and completes before M2-02B/API-02A.

- [ ] **Red:** assert no-locator supplement status, three-probe cap, source-bound candidate schema, deterministic seed, timeout/cancel unchanged state, and no mastery write; run `python -m pytest backend/tests/contract/test_learning_provider_boundary.py -q`. Expected: FAIL because learning orchestration is absent.
- [ ] **Green/refactor:** implement only explanation/practice candidate flow; run focused/contract tests and `python scripts/test_all.py`.
- [ ] **Reviews:** SPEC review AC-03, AC-12, AC-13, AC-21, AC-22, AC-23, AC-32; quality review provider/evaluator separation, source validation, cancellation/idempotency, and no answer/body logging. Critical findings block M2-02B/API-02A.
- [ ] **Commit:** scan secrets; `git add -- backend/src/projectb/application/learning.py backend/src/projectb/domain/learning.py backend/tests/contract/test_learning_provider_boundary.py`; run `git diff --cached --check`; commit with `git commit -m "feat(M2-02A): add explanation and practice candidates [agent: <fresh-agent-id>]"`.

**Completion standard:** Explanation/practice sessions are deterministic candidate flows with bounded probes and no authority over evidence, mastery, or plans.

### Task M2-02B: Add Deterministic Evaluation, Feedback, and Learning Evidence

**Goal:** Evaluate attempts through M2-01, append evidence transactionally, and allow provider feedback to explain but never change the oracle result.

**Files:** Create `backend/src/projectb/application/evidence.py` and `backend/tests/integration/test_learning_flow.py`; modify `backend/src/projectb/application/learning.py` through M2-02A ownership.

**Interfaces:** `evaluate_attempt`, `record_learning_evidence`, `generate_feedback`, evaluator provenance, immutable evidence IDs/outcomes, and provider failure preserving session/evidence state.

**Dependencies / parallelism:** Requires M2-02A and T-03C. M3-02A/API-02B/UI-04B depend on this terminal unit.

- [ ] **Red:** assert local oracle result, transactional append, duplicate attempt idempotency, malformed/timeout feedback unchanged evidence, and redacted answer references; run `python -m pytest backend/tests/integration/test_learning_flow.py -q`. Expected: FAIL because evidence/feedback orchestration is absent.
- [ ] **Green/refactor:** implement evaluation/evidence/feedback only; run focused/backend tests and `python scripts/test_all.py`.
- [ ] **Reviews:** SPEC review AC-04, AC-14, AC-17, AC-23, AC-24, AC-34; quality review transactionality, evaluator provenance, answer redaction, retry/cancellation, and provider non-authority. Critical findings block M3/API/UI consumers.
- [ ] **Commit:** scan secrets; `git add -- backend/src/projectb/application/evidence.py backend/src/projectb/application/learning.py backend/tests/integration/test_learning_flow.py`; run `git diff --cached --check`; commit with `git commit -m "feat(M2-02B): add evaluator evidence and feedback [agent: <fresh-agent-id>]"`.

**Completion standard:** Only deterministic evaluator results create append-only evidence, and feedback/model failures cannot alter correctness, mastery, or plans.

### Task M3-01: Implement ReviewPolicy v1 as a Pure Deterministic Planner

**Goal:** Implement the exact signed ReviewPolicy v1, canonical input hashing, deterministic IDs, capacity packing, prerequisites, time-zone semantics, and golden fixtures without provider involvement.

**Files:**
- Create: backend/src/projectb/domain/review.py
- Create: backend/src/projectb/application/review_planner.py
- Create: backend/tests/unit/test_review_policy_v1.py
- Create: backend/tests/fixtures/review_policy_v1_golden.json

**Interfaces:**
- Consumes: confirmed coverage/source contracts from M1-03, evidence types from M2-02B only through the declared LearningEvidence shape, and immutable clock/tzdata inputs.
- Produces: plan_reviews_v1(input: PlanReviewsInput) -> PlanReviewsOutput as a pure function.
- PlanReviewsInput includes sorted course/concept/coverage/dependencies, complete relevant LearningEvidence history, ConceptReviewState, current MasteryEstimate, current unstarted tasks, CourseReviewGoal, ReviewPolicy, today_local, timezone_id, and tzdata_version.
- PlanReviewsOutput includes candidate tasks, blocked concepts, capacity_exceeded, archive/pause result, plan_input_hash, and optional PlanRevision. IDs use the fixed UUIDv5 namespace and name plan_input_hash|concept_id|due_local_date|task_type.

**Dependencies / parallelism:** Requires T-02/T-03C and the confirmed M1-03 contract; it may begin before M2-02B implementation by using the declared evidence schema, but final integration waits for M2-02B. It owns review.py/review_planner.py and may run in parallel with M2-01/X2-02.

- [ ] **Step 1: Write and run the failing golden tests**

~~~python
@pytest.mark.parametrize("fixture_id", ["G-01", "G-02", "G-03", "G-04", "G-05"])
def test_review_policy_v1_golden_fixtures(fixture_id):
    fixture = load_review_fixture(fixture_id)
    assert plan_reviews_v1(fixture.input) == fixture.expected

def test_repeated_canonical_input_has_same_hash_ids_and_order():
    first = plan_reviews_v1(canonical_input)
    second = plan_reviews_v1(reordered_equivalent_input)
    assert first.plan_input_hash == second.plan_input_hash
    assert first.tasks == second.tasks
~~~

Run: python -m pytest backend/tests/unit/test_review_policy_v1.py -q

Expected: FAIL because PlanReviewsInput, canonical hashing, and plan_reviews_v1 do not exist.

- [ ] **Step 2: Implement the minimum exact policy**

Validate budget 10–480 step 5, defaults continuous 30/finals 90, durations 5/10/15/20/30 default 10, intervals [1,3,7,14,30], evidence transitions, and state/history consistency. Filter blocked prerequisites and prioritize learnable prerequisites. Use the signed stable tuple: overdue descending, confirmed teacher focus in finals, past-paper repeats descending capped 5, evidence weakness, requested/due date ascending, concept_id ascending. Build continuous 30-day and finals through-target windows, pack without split/overage, expose capacity_exceeded, derive due_at from the earliest valid local instant, and pause only when today_local is after target_local_date. Canonicalize complete input as UTF-8 JSON with sorted keys/IDs and SHA-256. No model, FSRS, BKT, hidden weight, wall clock, or network access.

- [ ] **Step 3: Run green tests and regression**

Run:

~~~powershell
python -m pytest backend/tests/unit/test_review_policy_v1.py -q
python -m pytest backend/tests/unit -q
python scripts/test_all.py
~~~

Expected: all five SPEC golden fixtures pass exactly; invalid budget/timezone/state returns the white-listed failure, DST fixtures avoid duplicate/nonexistent times, equivalent ordering yields identical hash/IDs/tasks, and provider mock changes have no effect.

- [ ] **Step 4: Review and commit**

SPEC review checks AC-05, AC-18, AC-34–36 and every ReviewPolicy v1 clause/fixture. Quality review checks purity, full-history hashing, stable sort, UUIDv5 namespace, tzdata injection, overflow/capacity behavior, and property tests for determinism. A Critical finding blocks M3-02A. After both reviews pass, scan credentials and commit with feat(M3-01): implement deterministic ReviewPolicy v1; record exact red/green output and hash in shared ledgers.
**Commit command:** `git add -- backend/src/projectb/domain/review.py backend/src/projectb/application/review_planner.py backend/tests/unit/test_review_policy_v1.py backend/tests/fixtures/review_policy_v1_golden.json; git diff --cached --check; git commit -m "feat(M3-01): implement deterministic ReviewPolicy v1 [agent: <fresh-agent-id>]"; git rev-parse HEAD`

**Completion standard:** Fixed normalized inputs, clock, timezone data, and policy version always produce the exact same tasks, reasons, dates, hashes, and IDs with no provider call.

### Task Group M3-02 (not dispatchable): Mastery, Plan Revisions, Undo, Finals, and Post-Exam State

**Goal:** Turn append-only evidence and confirmed inputs into explainable mastery estimates and versioned plan revisions that modify only unstarted future tasks.

**Files:**
- Create: backend/src/projectb/application/mastery.py
- Create: backend/src/projectb/application/review.py
- Modify: backend/src/projectb/infrastructure/repositories/learning_repo.py
- Create: backend/tests/integration/test_mastery_and_revisions.py
- Create: backend/tests/integration/test_finals_state.py

**Interfaces:**
- Consumes: M2-02B LearningEvidence, M3-01 planner, M1-03 confirmed coverage, and T-03C versioned repositories.
- Produces: derive_mastery(history, prior_state, policy_version, now) -> MasteryEstimate | StateInconsistent.
- Produces: revise_plan(course_id, trigger, planner_input) -> PlanRevision | NoChange, revert_revision(revision_id, actor) -> PlanRevision, update_review_goal(course_id, change, actor) -> CourseReviewGoal, and record_review_attempt(task_id, evaluator_result) -> LearningEvidence.
- MasteryEstimate includes level, algorithm_version, complete evidence IDs, derived_at, and user-correction state. Revert creates a new revision with reverts_revision_id.

**Dependencies / parallelism:** Group summary only. M3-02A requires M2-02B/M3-01/M1-03/T-03C; M3-02B requires M3-02A; M3-02C requires M3-02B. Repository edits are serialized. M3-03 and API-03A wait for the terminal M3-02C contract.

- [ ] **Step 1: Write and run the failing tests**

~~~python
def test_revision_replaces_only_unstarted_future_tasks_and_undo_is_append_only():
    revision = revise_plan("course", "budget_changed", planner_input)
    assert started_task.id in revision.unchanged_task_ids
    assert completed_task.id in revision.unchanged_task_ids
    undo = revert_revision(revision.id, actor="local_user")
    assert undo.reverts_revision_id == revision.id
    assert load_revision(revision.id) is not None

def test_exam_date_does_not_enter_finals_and_exam_day_does_not_pause():
    goal = update_review_goal("course", set_date(target_date), actor="local_user")
    assert goal.mode == "continuous"
    entered = update_review_goal("course", enter_finals(), actor="local_user")
    assert entered.mode == "finals"
    assert plan_for(today_local=target_date).post_exam_state != "post_exam_paused"
~~~

Run: python -m pytest backend/tests/integration/test_mastery_and_revisions.py backend/tests/integration/test_finals_state.py -q

Expected: FAIL because mastery derivation, revision persistence, undo, and finals state transitions are absent.

- [ ] **Step 2: Implement the minimum behavior in three fresh checkpoints**

1. **M3-02A mastery/evidence:** derive unknown/demonstrated_now/retained from complete evidence and signed rules; require an active-retrieval variant at least one local day later; preserve source-insufficient repair semantics; validate full history before returning state_inconsistent.
2. **M3-02B revision/undo:** route new evidence, budget/date/confirmed-coverage changes through M3-01; create no revision when candidate/current unstarted sets match; preserve started/completed tasks and old evidence; implement append-only revert revisions.
3. **M3-02C finals/post-exam:** require valid date/timezone plus explicit finals entry; make exit/clear/date changes affect future tasks only; pause/archive only after the local target date has completely passed and require a new explicit goal.

Each checkpoint has a separate red/green run, SPEC review, quality review, and exact task-file commit. The parent task remains pending until all three hashes are recorded.

- [ ] **Step 3: Run green tests and regression**

Run:

~~~powershell
python -m pytest backend/tests/integration/test_mastery_and_revisions.py backend/tests/integration/test_finals_state.py -q
python -m pytest backend/tests -q
python scripts/test_all.py
~~~

Expected: PASS for no evidence, incorrect/partial/pass/skip/source-insufficient, delayed variant retained, inconsistent state, no-change planning, budget/date/coverage revisions, undo, explicit finals entry/exit, exam-day learning, post-exam pause, and history preservation.

- [ ] **Step 4: Review and commit**

Group review checks AC-04, AC-05, AC-14, AC-17, AC-18, AC-34–36 after M3-02A/B/C. Quality review checks append-only transactions, concurrency/version conflicts, full-evidence validation, clock/timezone injection, no provider authority, and readable reason codes/diffs. A Critical finding blocks API-03/UI-05. No worker commit is assigned to this group heading; use the three unit commit commands below.

**Completion standard:** Every mastery/plan change is deterministic, evidence-linked, versioned, explainable, undoable through a new revision, and incapable of rewriting completed history.

### Task M3-02A: Derive Mastery from Complete Learning Evidence

**Goal:** Implement the deterministic mastery state derivation independently of plan revision and finals transitions.

**Files:** Create `backend/src/projectb/application/mastery.py` and `backend/tests/integration/test_mastery_derivation.py`.

**Interfaces:** `derive_mastery(history, prior_state, policy_version, now) -> MasteryEstimate | StateInconsistent`, including complete evidence IDs, algorithm version, derived timestamp, correction state, and source-insufficient repair semantics.

**Dependencies / parallelism:** Requires M2-02B, M3-01, M1-03, and T-03C. It is read-only against plan/review persistence and completes before M3-02B.

- [ ] **Red:** cover no evidence, incorrect/partial/pass/skip, delayed retained evidence, source-insufficient, inconsistent history, and provider wording variants; run `python -m pytest backend/tests/integration/test_mastery_derivation.py -q`. Expected: FAIL because mastery derivation is absent.
- [ ] **Green/refactor:** implement the signed evidence/state rules only; run the focused test, `python -m pytest backend/tests -q`, and `python scripts/test_all.py`.
- [ ] **Reviews:** SPEC review AC-04, AC-14, AC-17, AC-34; quality review full-history validation, clock injection, deterministic algorithm version, no provider authority, and readable reason codes. Critical findings block M3-02B.
- [ ] **Commit:** scan secrets; `git add -- backend/src/projectb/application/mastery.py backend/tests/integration/test_mastery_derivation.py`; run `git diff --cached --check`; commit with `git commit -m "feat(M3-02A): derive mastery from evidence [agent: <fresh-agent-id>]"`.

**Completion standard:** Identical evidence/history inputs produce identical mastery or a deterministic `state_inconsistent` result, and reading an explanation alone never changes state.

### Task M3-02B: Add Append-only Plan Revisions and Undo

**Goal:** Recalculate only unstarted future tasks, preserve history, and implement undo as a new revision.

**Files:** Create `backend/src/projectb/application/review.py`, modify `backend/src/projectb/infrastructure/repositories/learning_repo.py`, and create `backend/tests/integration/test_plan_revisions.py`.

**Interfaces:** `revise_plan`, `revert_revision`, no-change detection, immutable old plans/evidence, and started/completed task preservation.

**Dependencies / parallelism:** Requires M3-02A and consumes M3-01/M2-02B contracts. It completes before M3-02C; repository edits are serialized with T-03C.

- [ ] **Red:** assert budget/date/coverage/evidence triggers, no-change cases, started/completed preservation, optimistic conflict, and append-only undo; run `python -m pytest backend/tests/integration/test_plan_revisions.py -q`. Expected: FAIL because revision persistence is absent.
- [ ] **Green/refactor:** implement revision/undo transactions only; run the focused test, all backend tests, and `python scripts/test_all.py`.
- [ ] **Reviews:** SPEC review AC-05, AC-18, AC-34, AC-35, AC-36; quality review concurrency, append-only history, full input hashes, no hidden priority math, and rollback. Critical findings block M3-02C.
- [ ] **Commit:** scan secrets; `git add -- backend/src/projectb/application/review.py backend/src/projectb/infrastructure/repositories/learning_repo.py backend/tests/integration/test_plan_revisions.py`; run `git diff --cached --check`; commit with `git commit -m "feat(M3-02B): add append-only plan revisions [agent: <fresh-agent-id>]"`.

**Completion standard:** Revision and undo operations are deterministic, explainable, conflict-safe, and cannot rewrite started/completed tasks or old evidence.

### Task M3-02C: Add Finals Entry, Exit, and Post-exam State

**Goal:** Implement explicit finals mode and truthful exam-day/post-exam transitions without changing historical tasks.

**Files:** Modify `backend/src/projectb/application/review.py`; create `backend/tests/integration/test_finals_state.py`.

**Interfaces:** `update_review_goal`, explicit `enter_finals`/exit, valid local date/timezone/budget validation, exam-day learning, and `post_exam_paused` only after the target date.

**Dependencies / parallelism:** Requires M3-02B and M3-01. API-03A, M3-03, UI-05B, and QA-02A depend on this terminal unit.

- [ ] **Red:** assert date entry remains continuous, explicit entry changes to finals, exam day is not paused, exit/date edits affect future tasks only, and after-target state has zero future tasks; run `python -m pytest backend/tests/integration/test_finals_state.py -q`. Expected: FAIL because finals transitions are absent.
- [ ] **Green/refactor:** implement only finals/post-exam state transitions; run the focused test, all backend tests, and `python scripts/test_all.py`.
- [ ] **Reviews:** SPEC review AC-05, AC-08, AC-18, AC-34, AC-35, AC-36; quality review timezone/DST injection, explicit actions, history preservation, and no automatic re-entry. Critical findings block API-03/UI-05B.
- [ ] **Commit:** scan secrets; `git add -- backend/src/projectb/application/review.py backend/tests/integration/test_finals_state.py`; run `git diff --cached --check`; commit with `git commit -m "feat(M3-02C): add finals and post-exam states [agent: <fresh-agent-id>]"`.

**Completion standard:** Finals mode is entered only by an explicit action, exam-day behavior is usable, and post-exam pause is date-correct, visible, and reversible only through a new goal.

### Task M3-03: Analyze and Confirm Past-Paper and Teacher-Focus Candidates

**Goal:** Convert answer-free past papers and teacher focus into source-bound StudyFocus candidates that affect finals priority only after explicit user confirmation.

**Files:**
- Create: backend/src/projectb/application/study_focus.py
- Modify: backend/src/projectb/domain/review.py
- Create: backend/tests/contract/test_exam_material_analysis.py
- Create: backend/tests/integration/test_study_focus_confirmation.py

**Interfaces:**
- Consumes: allowed roles/materials from M1-01/M1-03, analyze_exam_material through X2-01, confirmed concepts, and plan revision service from M3-02C.
- Produces: propose_study_focus(material_id, confirmed_concepts, source_scope) -> Sequence[StudyFocusCandidate].
- Produces: confirm_study_focus(candidate_id, decision, correction, actor="local_user") -> StudyFocusDecision and active_study_focus(course_id) -> Sequence[StudyFocus].
- StudyFocus separates teacher_explicit from past_paper_pattern/system_inference, preserves locator/type/difficulty/confidence, and never carries an answer key or “predicted exam question” claim.

**Dependencies / parallelism:** Requires M1-03, X2-01, and M3-02C. It may run in the review worktree after M3-02C interfaces merge. It must not add training/fine-tuning/automatic-upload endpoints.

- [ ] **Step 1: Write and run the failing tests**

~~~python
def test_unconfirmed_exam_candidate_does_not_change_priority_or_plan():
    confirmed_concepts = [{"id": "concept-mutex", "confirmed": True}]
    plan_before = current_plan("course")
    candidate = propose_study_focus("past-paper-1", confirmed_concepts, ["source-3"])[0]
    assert active_study_focus("course") == []
    assert current_plan("course") == plan_before
    confirm_study_focus(candidate.id, "accepted", None, actor="local_user")
    assert active_study_focus("course")[0].concept_id == candidate.concept_id

def test_analysis_has_no_training_prediction_or_auto_upload_path(provider_spy):
    answer_key_fixture = {"role": "answer_key", "content_hash": "synthetic-answer-key"}
    result = analyze_exam_material_without_consent(answer_key_fixture)
    assert result.status == "unsupported_role"
    assert provider_spy.calls == 0
    assert registered_operations().isdisjoint({"train", "fine_tune", "predict_exam", "auto_upload"})
~~~

Run: python -m pytest backend/tests/contract/test_exam_material_analysis.py backend/tests/integration/test_study_focus_confirmation.py -q

Expected: FAIL because StudyFocus candidate/decision services and forbidden-operation assertions are absent.

- [ ] **Step 2: Implement the minimum behavior**

Accept only answer-free past_paper and teacher_focus material already passing M1 policy/consent. Validate every locator and candidate schema. Keep teacher-declared focus distinct from repetition-derived candidates; cap past-paper repeat count at five for planning. Append user accept/reject/correction decisions and trigger the M3-02C revision service only after confirmation. Provider failure, low confidence, missing locator, suspected answer/leak, or unsupported role creates no focus/priority/plan change. Expose structure/topic/type/difficulty analysis and similar practice only; no training, fine-tuning, original-question prediction, or automatic upload path exists.

- [ ] **Step 3: Run green tests and regression**

Run:

~~~powershell
python -m pytest backend/tests/contract/test_exam_material_analysis.py backend/tests/integration/test_study_focus_confirmation.py -q
python -m pytest backend/tests -q
python scripts/test_all.py
~~~

Expected: PASS for confirmed/unconfirmed/corrected mapping, source failure, injected provider output, answer role, provider failure, no-consent zero-call, repeat cap, teacher-vs-inference separation, and absence of forbidden operations.

- [ ] **Step 4: Review and commit**

SPEC review checks AC-18–20, AC-22–24, AC-33–36. Quality review checks role enforcement, candidate authority, locator validity, academic-integrity copy, injection handling, append-only decisions, and stable priority inputs. A Critical finding blocks API-03/UI-05B. After both reviews pass, scan credentials and commit with feat(M3-03): add confirmed study-focus mapping; record actual hash and review evidence in PLAN.md/AGENT_LOG.md.
**Commit command:** `git add -- backend/src/projectb/application/study_focus.py backend/src/projectb/domain/review.py backend/tests/contract/test_exam_material_analysis.py backend/tests/integration/test_study_focus_confirmation.py; git diff --cached --check; git commit -m "feat(M3-03): add confirmed study-focus mapping [agent: <fresh-agent-id>]"; git rev-parse HEAD`

**Completion standard:** Finals planning can consume only source-bound, user-confirmed StudyFocus records, while provider/unsupported/answer material can never alter priority or create a training/prediction path.
### Task DIST-01: Build the Windows x64 Single-File Distribution

**Goal:** Produce a reproducible single `ProjectB.exe` that embeds the production WebUI and required runtime resources, starts only the loopback WebUI, and can be smoke-tested on a clean Windows x64 machine without Python, Node, or Docker.

**Files:**
- Create: `packaging/windows/build.ps1`
- Create: `packaging/windows/freezer-manifest.json`
- Create: `packaging/windows/smoke_test.ps1`
- Create: `backend/tests/integration/test_windows_distribution_contract.py`
- Create: `docs/engineering/DIST-01_EVIDENCE.md`

**Interfaces:**
- Consumes: QA-01C/QA-02C terminal evidence, API-04B, the production frontend build, the data-directory/loopback contracts, and the exact freezer/version/license selected and verified by G-02C.
- Produces:
  - `powershell -NoProfile -ExecutionPolicy Bypass -File packaging/windows/build.ps1 -Clean -OutputDirectory dist` -> `dist/ProjectB.exe`.
  - `powershell -NoProfile -ExecutionPolicy Bypass -File packaging/windows/smoke_test.ps1 -ExePath dist/ProjectB.exe -DataRoot <temporary-directory>` -> a nonzero exit on startup, bind, health, SQLite, credential-status, shutdown, or residue failure.
  - A redacted evidence record containing the source commit, exact commands, Windows build/architecture, artifact SHA-256/size, freezer version, signature/SmartScreen truth, test times, and clean-machine result. It contains no credential, course body, local course path, or private fixture.

**Dependencies / parallelism:** QA-01C, QA-02C, API-04B, and G-02C must be complete; their transitive graph covers backend/API/UI. DIST-01 owns the Windows packaging files and must not run in parallel with changes to the application launcher, frontend asset base path, or dependency locks. If G-02C has not verified a compatible freezer and its license, this task is blocked; it must not silently substitute a tool. Building is local. Publishing an executable, creating a release, pushing a branch, or opening a PR/MR requires execution-time user authorization.

- [ ] **Step 1: Write and run the failing distribution-contract test**

Add tests that require a toolchain-evidence-linked manifest, one-file output, embedded frontend assets, external user-data storage, loopback-only launch arguments, and a smoke script that never accepts a secret on its command line.

Run:

~~~powershell
python -m pytest backend/tests/integration/test_windows_distribution_contract.py -q
~~~

Expected: FAIL because the freezer manifest, build script, smoke script, and `dist/ProjectB.exe` do not yet exist. Preserve this failure as the red evidence; do not create a dummy executable to satisfy the test.

- [ ] **Step 2: Add the minimum package and evidence path**

Make `build.ps1` perform a clean locked frontend build, stage only required static/backend resources, invoke only the G-02C-verified freezer, and emit exactly one user-facing `ProjectB.exe`. Resolve packaged resources relative to the frozen application while placing SQLite, material data, and logs in the documented external user-data directory. Exclude tests, development tools, `.git`, evidence drafts, credentials, private courseware, and demo-only provider registration. Make `smoke_test.ps1` start the executable, discover the loopback URL without parsing sensitive logs, verify health/profile, initialize SQLite, exercise configured/unconfigured credential status without a key, confirm no LAN listener, stop the process, and report residual files. Run the same smoke script on a clean Windows 11 x64 environment with Python, Node, and Docker absent, and record an actual result or `not executed`; never infer the clean-machine result from the development host.

- [ ] **Step 3: Run focused and full regression verification**

Run on the build host, then repeat the smoke command on the clean host:

~~~powershell
python -m pytest backend/tests/integration/test_windows_distribution_contract.py -q
powershell -NoProfile -ExecutionPolicy Bypass -File packaging/windows/build.ps1 -Clean -OutputDirectory dist
powershell -NoProfile -ExecutionPolicy Bypass -File packaging/windows/smoke_test.ps1 -ExePath dist/ProjectB.exe -DataRoot "$env:TEMP\ProjectB-DIST01-Smoke"
python scripts/test_all.py
~~~

Expected: the focused test, build, smoke test, and full suite PASS; the artifact is a single Windows x64 executable, serves the production WebUI on loopback, initializes external data, exposes only redacted credential state, and contains no private course material or secret. A development-host-only smoke run is not a clean-machine PASS.

- [ ] **Step 4: Review and commit**

SPEC compliance review checks AC-07, AC-11, AC-40, AC-43, and the Windows distribution contract in SPEC sections 8-10. Quality/security/license review checks deterministic locked inputs, resource discovery, process cleanup, loopback binding, writable-directory separation, artifact inspection, secret/courseware scan, freezer and bundled dependency licenses, code-signing truth, and the reproducibility of the clean-machine evidence. Critical findings block the commit. Commit with `build(DIST-01): package Windows x64 single-file app`. The coordinator then records the hash and both review outcomes in `PLAN.md` and `AGENT_LOG.md`.
**Commit command:** `git add -- packaging/windows/build.ps1 packaging/windows/freezer-manifest.json packaging/windows/smoke_test.ps1 backend/tests/integration/test_windows_distribution_contract.py docs/engineering/DIST-01_EVIDENCE.md; git diff --cached --check; git commit -m "build(DIST-01): package Windows x64 single-file app [agent: <fresh-agent-id>]"; git rev-parse HEAD`

**Completion standard:** The exact commands above pass, an actual clean Windows x64 host without developer runtimes can start and use `ProjectB.exe`, the evidence records the real signature/SmartScreen status, and scans find neither a secret nor private course content. No release/push claim is made without separate user authorization.

### Task DIST-02: Build the OCI Demo Image and Deployment Preflight

**Goal:** Package the complete demo profile as a reproducible OCI image that starts with one `docker run`, preserves the confirmed session/quota behavior, and makes upload, credentials, real-provider egress, and private persistence unreachable before any public deployment is attempted.

**Files:**
- Create: `packaging/oci/Dockerfile`
- Create: `packaging/oci/entrypoint.sh`
- Create: `.dockerignore`
- Create: `packaging/oci/smoke_test.ps1`
- Create: `backend/tests/integration/test_oci_distribution_contract.py`
- Create: `docs/engineering/DIST-02_EVIDENCE.md`
- Modify: `demo/profile.json`

**Interfaces:**
- Consumes: DEMO-01C's synthetic/explicitly licensed fixture manifest and ephemeral-session service, QA-01C evidence, DIST-01's resource-layout contract, and the base-image/hosting/license/cost evidence verified by G-02C.
- Produces:
  - `docker build --file packaging/oci/Dockerfile --tag projectb-demo:local .` -> a locally tagged OCI image.
  - `docker run --rm --publish 127.0.0.1:7860:7860 projectb-demo:local` -> the demo WebUI on port 7860.
  - A local smoke result for two isolated sessions, expiry/reset, quotas, health, and the full import/confirmation/learning/revision flow, plus a deployment-preflight record whose public URL/status remains `not executed` until a real authorized deployment occurs.

**Dependencies / parallelism:** DEMO-01C, DIST-01, QA-01C, and G-02C are required. Do not proceed if the Docker base image/license or the selected host's current HTTPS, storage, sleep, quota, account, and fee terms are unverified. This task owns OCI files and must not run beside demo-profile or fixture-manifest edits. Image push, registry creation, Hugging Face Space creation/change, deployment, or any paid resource requires explicit execution-time user authorization; lack of authorization is recorded as `not executed`, not as a failed or successful deployment.

- [ ] **Step 1: Write and run the failing OCI contract test**

Add a test that parses the Dockerfile and `demo/profile.json` and requires the deterministic mock, built-in licensed fixture IDs, exact 30-minute idle/2-hour lifetime, one course, 20 materials, two jobs, 64 MiB session state, 60 requests/IP/minute, no upload route, no credential store, no local-production adapter, a non-root runtime, health check, and a `.dockerignore` excluding secrets/private data.

Run:

~~~powershell
python -m pytest backend/tests/integration/test_oci_distribution_contract.py -q
~~~

Expected: FAIL because the OCI packaging contract is absent or incomplete. The test must not pull an image, open a network connection, or use a real credential.

- [ ] **Step 2: Add the minimum image and local preflight**

Use only the G-02-verified base image and locked dependencies. Build frontend/backend artifacts in deterministic stages, copy only runtime files and licensed fixtures, run as a non-root user, set the demo profile explicitly in `entrypoint.sh`, and keep runtime state in an ephemeral bounded directory. Fail startup if a credential/provider profile, arbitrary upload/path/URL, local data mount, or production adapter is enabled. Make the smoke script build/run the image, wait for health, exercise two browser-session IDs, test cross-session denial and quota/expiry/reset behavior, scan outputs for secrets/private paths, and always remove its local test container. Do not put a registry token or deployment credential in build arguments, image layers, logs, or evidence.

- [ ] **Step 3: Run focused and full regression verification**

Run:

~~~powershell
python -m pytest backend/tests/integration/test_oci_distribution_contract.py -q
docker build --file packaging/oci/Dockerfile --tag projectb-demo:local .
powershell -NoProfile -ExecutionPolicy Bypass -File packaging/oci/smoke_test.ps1 -Image projectb-demo:local -Port 7860
python scripts/test_all.py
~~~

Expected: focused tests, the single build command, the smoke run, and the full suite PASS; the container completes the interactive demo using only licensed/synthetic fixtures and mock responses, session isolation/limits are reproducible, and provider/credential/upload calls remain zero. These local results do not prove a public HTTPS URL.

- [ ] **Step 4: Review and commit**

SPEC compliance review checks AC-07, AC-10, AC-41, AC-47, and the confirmed demo limits in SPEC section 4.5. Quality/security/license review checks image provenance/digest, non-root execution, dependency locks/SBOM or equivalent inventory, base-image and fixture licenses, build-context exclusions, layer/history secret scans, session cleanup, resource bounds, network/provider fail-closed behavior, and honest hosting/cost wording. Commit with `build(DIST-02): add isolated OCI demo preflight`. The coordinator records the hash and reviews; public deployment evidence remains pending unless the user separately authorizes and an actual external-browser check succeeds.
**Commit command:** `git add -- packaging/oci/Dockerfile packaging/oci/entrypoint.sh .dockerignore packaging/oci/smoke_test.ps1 backend/tests/integration/test_oci_distribution_contract.py docs/engineering/DIST-02_EVIDENCE.md demo/profile.json; git diff --cached --check; git commit -m "build(DIST-02): add isolated OCI demo preflight [agent: <fresh-agent-id>]"; git rev-parse HEAD`

**Completion standard:** The exact local build/run/smoke commands pass from a clean checkout and the image cannot reach credential, upload, private-persistence, or real-provider paths. A public URL is recorded only after an authorized real deployment and external clean-browser verification; otherwise the URL/deployment fields explicitly remain `not executed`.

### Task CI-01: Unify Tests, Scans, GitLab CI, and GitHub Actions

**Goal:** Make one deterministic local command drive the same test/build/security/license gates used by NJU GitLab and the GitHub mirror, including the exact GitLab `unit-test` job and the selected distribution builds.

**Files:**
- Modify: `scripts/test_all.py`
- Create: `scripts/scan_secrets.py`
- Create: `scripts/scan_secrets.ps1`
- Create: `scripts/verify_licenses.py`
- Create: `scripts/verify_ci_contract.py`
- Create: `backend/tests/integration/test_ci_contract.py`
- Create: `.gitlab-ci.yml`
- Create: `.github/workflows/ci.yml`
- Create: `docs/engineering/CI-01_EVIDENCE.md`

**Interfaces:**
- Consumes: locked backend/frontend dependencies, all automated tests, DIST-01/DIST-02 build commands, and G-02 dependency/license evidence.
- Produces:
  - `python scripts/test_all.py` as the canonical fail-fast, non-interactive, network-free core test entry.
  - Cross-platform secret and license checks with redacted diagnostics and nonzero failure codes.
  - A GitLab job named exactly `unit-test` and GitHub push/PR jobs that invoke the same command for the same commit; OCI build and Windows artifact jobs call the verified DIST scripts without embedding credentials.

**Dependencies / parallelism:** T-01, all automated test owners, DIST-01, and DIST-02 are required. CI-01 exclusively owns CI YAML and shared test/scan scripts while in progress. Local validation can proceed without a remote. Any push, mirror configuration, runner/registry mutation, PR/MR creation, or remote CI trigger requires execution-time user authorization. A local YAML check cannot substitute for a real remote pipeline.

- [ ] **Step 1: Write and run the failing CI-contract test**

Use a YAML parser, not regular-expression rewriting, to assert the exact GitLab job name, shared entry command, push triggers, least-privilege GitHub permissions, distribution build jobs, pinned/verified tool versions, artifact retention, and absence of secret-valued workflow fields. Also assert that `test_all.py` reaches backend tests, frontend tests/build, contract/E2E tests that are CI-safe, secret scan, license verification, and evidence validation.

Run:

~~~powershell
python -m pytest backend/tests/integration/test_ci_contract.py -q
~~~

Expected: FAIL because the CI files and final shared gates do not yet exist. No remote pipeline is triggered in this step.

- [ ] **Step 2: Add the minimum shared gates and CI definitions**

Make `test_all.py` propagate each child exit code and never require a credential, private courseware, public URL, or network. The Python secret scanner is canonical on all platforms; the PowerShell script is a thin argument-safe wrapper. Scan tracked content and relevant build artifacts without printing matched secret values. Verify every shipped direct/transitive dependency and asset against G-02 evidence, failing on an unrecorded or incompatible license. Configure GitLab `unit-test` and GitHub tests to call only the shared entry, add OCI image-build verification, and add a verified Windows runner job for `ProjectB.exe`; use minimal token permissions and no real secret variables in ordinary tests.

- [ ] **Step 3: Run focused and full regression verification**

Run:

~~~powershell
python -m pytest backend/tests/integration/test_ci_contract.py -q
python scripts/verify_ci_contract.py
python scripts/scan_secrets.py
python scripts/verify_licenses.py --strict
python scripts/test_all.py
~~~

Expected: every local command PASS, the canonical entry exercises the complete CI-safe suite and frontend production build, scanners report no secret and no unlicensed dependency, and both YAML files validate against the same entry. Remote GitLab/GitHub status remains `not executed` until an authorized push produces real pipeline URLs.

- [ ] **Step 4: Review and commit**

SPEC compliance review checks AC-07, AC-10, AC-42, AC-43, and AC-47. Quality/security/license review checks deterministic installs/caches, pinned third-party actions/images, least-privilege tokens, protected artifact handling, untrusted-PR behavior, scanner redaction/false-negative fixtures, license completeness, job timeouts, and exact command parity. Commit with `ci(CI-01): add shared test and distribution gates`. After authorized remote execution, record only actual pipeline URLs, commit SHAs, job names, and results; do not copy a local PASS into the remote evidence fields.
**Commit command:** `git add -- scripts/test_all.py scripts/scan_secrets.py scripts/scan_secrets.ps1 scripts/verify_licenses.py scripts/verify_ci_contract.py .gitlab-ci.yml .github/workflows/ci.yml backend/tests/integration/test_ci_contract.py docs/engineering/CI-01_EVIDENCE.md; git diff --cached --check; git commit -m "ci(CI-01): add shared test and distribution gates [agent: <fresh-agent-id>]"; git rev-parse HEAD`

**Completion standard:** All local gates pass and, after separate user authorization to push, NJU GitLab `unit-test` and GitHub Actions both pass for the same recorded commit while the selected distribution jobs succeed. Without those real remote records, CI-01 remains incomplete and says `not executed` for remote evidence.

### Task DOC-01: Publish Accurate User, Operations, Security, and License Documentation

**Goal:** Give a new user and reviewer accurate, executable instructions for obtaining, running, configuring, deleting, testing, distributing, and operating ProjectB while clearly separating verified facts, known limits, and unexecuted external evidence.

**Files:**
- Create: `README.md`
- Create: `docs/engineering/OPERATIONS.md`
- Create: `docs/engineering/THIRD_PARTY_NOTICES.md`
- Create: `docs/engineering/DOC-01_EVIDENCE.md`
- Create: `backend/tests/integration/test_documentation_contract.py`

**Interfaces:**
- Consumes: the actual CLI/UI behavior, DIST-01/DIST-02 commands and evidence, CI-01 entry points, G-02 dependency/provider/hosting evidence, and the final security/credential boundaries.
- Produces: README sections for overview/30-second value, installation/acquisition, local run, test, Windows and OCI distribution commands, directory structure, credential configure/status/update/clear, data locations/deletion, security boundaries, deployment architecture/CI-CD, known limits, third-party dependencies/assets/licenses, and troubleshooting. Operations and notices provide detail without contradicting README.

**Dependencies / parallelism:** All behavior and distribution tasks must be stable; DOC-01 may begin with the section contract but factual commands and claims wait for their owning tasks. It owns these documentation files. It must not create or write `REFLECTION.md`; only the student authors that file. Remote artifact links, pipeline results, and public URLs are inserted only after authorized execution and direct verification, otherwise marked `not executed` or unavailable.

- [ ] **Step 1: Write and run the failing documentation-contract test**

Add a parser-based test for every required README heading, literal one-command test/build/run examples, Windows x64/no-Python-Node-Docker limits, localhost-only behavior, no `.env` production path, hidden Credential Manager workflow, demo restrictions, data retention/uninstall, SmartScreen/signature truth, CI platform roles, deployment architecture, known limitations, and source/license rows for every shipped third-party dependency and asset.

Run:

~~~powershell
python -m pytest backend/tests/integration/test_documentation_contract.py -q
~~~

Expected: FAIL because README and the supporting operations/license documents are absent or incomplete. The test must reject placeholder success language, example keys, private course paths, and claims of an unverified CI run or URL.

- [ ] **Step 2: Write the minimum complete and evidence-backed documentation**

Derive commands from executable scripts rather than inventing them. Describe the single-file local path, external data directory, loopback trust boundary, safe credential UI operations, forced-clear/delete-incomplete recovery, OCI demo limits, acquisition/uninstall, support boundary, and exact platform/architecture prerequisites. Generate dependency and asset notices only from G-02/CI-01 verified inventories and record source/license; do not claim a dependency, host, provider feature, free quota, code signature, CI result, downloadable release, or HTTPS URL without evidence. Explain that private courseware is excluded from Git/CI/distributions and that `.env` is not a supported production credential path.

- [ ] **Step 3: Run focused and full regression verification**

Run:

~~~powershell
python -m pytest backend/tests/integration/test_documentation_contract.py -q
python scripts/verify_licenses.py --strict
python scripts/test_all.py
~~~

Expected: focused docs tests, license validation, and the full suite PASS; every documented local command/path matches the implementation, every shipped dependency/asset has verified license evidence, and absent external facts are visibly marked `not executed` rather than presented as complete.

- [ ] **Step 4: Review and commit**

SPEC compliance review checks AC-07, AC-10, AC-39-44, AC-47, and the README/distribution requirements in the course rules. Quality/security/license review checks command reproducibility, link targets, terminology consistency, no secret/course body/local private path, threat and deletion accuracy, accessible plain-language instructions, complete third-party notices, and the absence of AI-authored reflection content. Commit with `docs(DOC-01): add user operations security and license guide` and let the coordinator record the task hash/reviews.
**Commit command:** `git add -- README.md docs/engineering/OPERATIONS.md docs/engineering/THIRD_PARTY_NOTICES.md docs/engineering/DOC-01_EVIDENCE.md backend/tests/integration/test_documentation_contract.py; git diff --cached --check; git commit -m "docs(DOC-01): add user operations security and license guide [agent: <fresh-agent-id>]"; git rev-parse HEAD`

**Completion standard:** A clean reader can follow README to test and run the supported artifacts, safely configure credential status without exposing a key, understand storage/deletion/demo/security limits, and trace every third-party item to verified license evidence. `REFLECTION.md` remains student-authored, and no CI/URL/release statement is fabricated.

### Task INT-01: Add the Authorization-Gated P/F Evidence Suite

**Goal:** Build a bounded, reproducible P/F lifecycle evidence runner whose normal implementation and CI verification use only a synthetic/licensed fixture, an in-memory fake secret handle, and a scripted transport; make any later real paid invocation stop for explicit user authorization and keep the key outside arguments, files, logs, reports, and the agent context.

**Files:**
- Create: `scripts/run_pf_evidence.py`
- Create: `backend/tests/integration/test_pf_evidence_guard.py`
- Create: `backend/tests/fixtures/pf_evidence_synthetic.json`
- Create: `docs/engineering/INT-01_EVIDENCE.md`
- Modify: `.gitignore`
- Generate but do not commit: `artifacts/int-01/summary.json`

**Interfaces:**
- Consumes: X2-02/X2-03C through the provider-neutral application boundary, G-02B capability/policy/price evidence, a non-course synthetic or explicitly licensed fixture, an injected clock/transport, and opaque `credential_ref`/secret-handle abstractions only.
- Produces:
  - `python scripts/run_pf_evidence.py --mode dry-run --fixture backend/tests/fixtures/pf_evidence_synthetic.json --output artifacts/int-01/summary.json` -> a redacted P/F request/lifecycle summary with zero network calls.
  - Guards for at most 5 pages/20,000 input tokens, 20 HTTP requests, two Responses, 1,500 output tokens per Response, five status polls, no retry for non-idempotent create, one retry for GET/status, ten minutes, and a US$1.00 preflight ceiling.
  - An authorization gate for a future student-run live mode that accepts a profile ID, never an API-key/token value; it resolves a handle only inside the adapter boundary and refuses to start when current official pricing is unavailable or the estimate exceeds the ceiling.

**Dependencies / parallelism:** X2-02, X2-03C, T-05/T-06, and G-02B are required. INT-01 owns the runner, fixture, and its tests and must not race with adapter/lifecycle changes. During implementation and automated verification, use no real key, no private courseware, and no paid/provider network call. A future live invocation is outside the default Step 3 and requires a fresh, explicit execution-time user authorization; the student provides only an already configured Credential Manager profile, never the secret itself. If authorization is absent, the live evidence remains `not executed` and AC-48 is not claimed.

- [ ] **Step 1: Write and run the failing guard tests**

Test that dry-run is the default, sockets/provider transport are never reached, `--api-key`/`--token`/arbitrary input paths are rejected, only the allowlisted synthetic fixture is accepted, raw bodies/provider IDs are absent from output, all AC-48 counters stop before exceeding their caps, stale policy/consent or missing pricing yields zero calls, and a fake credential value cannot appear in logs/snapshots/reports.

Run:

~~~powershell
python -m pytest backend/tests/integration/test_pf_evidence_guard.py -q
~~~

Expected: FAIL because the guarded runner and fixture do not exist. No real credential, courseware, network, or paid call is used to obtain the red evidence.

- [ ] **Step 2: Add the minimum offline evidence runner and live stop gate**

Implement a scripted P flow and F upload/index/scope-filter/query/revoke/delete flow through the same application interfaces as production. Validate the fixture license marker and size/token estimates before resolving a profile. Capture only booleans, counts, duration buckets, request configuration proofs (`store:false`, non-background, disabled hosted tools), scope/allowlist outcomes, redacted lifecycle states, and cleanup results. Reject arbitrary fixture paths and credential-like CLI/config fields. The dry run injects a fake `SecretHandle` and transport and records zero external calls. The live branch must stop with `authorization_required` unless the student has just authorized that exact scope/budget; no subagent may self-authorize it or read a key.

- [ ] **Step 3: Run focused and full regression verification**

Run only the offline commands during this task unless the user separately authorizes a live call:

~~~powershell
python -m pytest backend/tests/integration/test_pf_evidence_guard.py -q
python scripts/run_pf_evidence.py --mode dry-run --fixture backend/tests/fixtures/pf_evidence_synthetic.json --output artifacts/int-01/summary.json
python scripts/test_all.py
~~~

Expected: focused tests, dry-run lifecycle, and the full suite PASS with deterministic P/F evidence, exact caps, complete cleanup transitions, and zero network/real-credential/private-courseware use. The committed evidence must say `live provider run: not executed`; this PASS is not evidence that AC-48's real-provider clause has run.

- [ ] **Step 4: Review and commit**

SPEC compliance review checks AC-07, AC-21-23, AC-27-32, AC-37-40, AC-48-50 and explicitly records AC-48 live status separately from offline contract coverage. Quality/security/license review checks fail-before-resolve ordering, budget arithmetic, retry/idempotency rules, clock/timeouts, redaction, artifact ignore rules, fixture origin/license, no request/response body capture, and inability to smuggle a secret or course path through CLI/config. Commit with `test(INT-01): add authorization-gated P/F evidence suite`. The coordinator records the hash and reviews without converting dry-run results into live evidence.
**Commit command:** `git add -- scripts/run_pf_evidence.py backend/tests/integration/test_pf_evidence_guard.py backend/tests/fixtures/pf_evidence_synthetic.json docs/engineering/INT-01_EVIDENCE.md .gitignore; git diff --cached --check; git commit -m "test(INT-01): add authorization-gated P/F evidence suite [agent: <fresh-agent-id>]"; git rev-parse HEAD`

**Completion standard:** The offline suite passes deterministically with no key, courseware, network, or paid call; its runner cannot exceed the confirmed limits or emit sensitive content. INT-01 may claim real P/F evidence only after a separately authorized student-run invocation using a Credential Manager reference and the licensed/synthetic fixture; otherwise that requirement truthfully remains `not executed` and the final gate stays open.

### Task FIN-01: Verify the Release Evidence and Finish the Development Branch

**Goal:** Apply one fail-closed final gate to all acceptance criteria, tests, builds, security/license checks, UI/distribution evidence, process records, remote CI records, and the public WebUI URL, then use the finishing-a-development-branch workflow without inventing missing evidence or taking an unauthorized remote action.

**Files:**
- Create: `scripts/final_verify.ps1`
- Create: `backend/tests/integration/test_release_evidence_contract.py`
- Create: `docs/engineering/FINAL_VERIFICATION.md`
- Create: `docs/engineering/RELEASE_CHECKLIST.md`
- Modify: `README.md` only to insert directly verified artifact, CI, and public-URL facts
- Modify through the coordinator only: `PLAN.md`
- Modify through the coordinator only: `AGENT_LOG.md`

**Interfaces:**
- Consumes: every task commit/review, AC-01 through AC-50 evidence, `python scripts/test_all.py`, DIST smoke results, UI screenshots/interactions, secret/license scans, the course-submission commit, and actual GitLab/GitHub/public-deployment records when authorized and available.
- Produces:
  - `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/final_verify.ps1 -ExpectedCommit <sha>` -> PASS only when every required local and remote evidence item belongs to the expected commit and no Critical issue/open placeholder remains.
  - A final matrix mapping each AC to a command/result/evidence path, review result, timestamp, and commit; missing external facts remain `not executed` and cause the release gate to fail.

**Dependencies / parallelism:** DOC-01, CI-01, INT-01, and QA-02C are direct prerequisites; their acyclic transitive graph covers every G/T/M/X/API/UI/DEMO/QA/DIST unit and both reviews. FIN-01 does not run in parallel with product changes. D-005 is not selected here: the cold-start agent decision/evidence belongs only to G-03. Push, PR/MR creation/merge, release publication, registry push, deployment, or real paid invocation requires explicit execution-time user authorization. `REFLECTION.md` is checked only for student ownership/presence required by submission; the agent never writes it.

- [ ] **Step 1: Write and run the failing final-evidence contract**

Add tests requiring a unique source commit, all task hashes/statuses, red/green commands, both review results, local test/build/static/UI/distribution evidence, zero unresolved Critical issues, secret/license PASS, real GitLab `unit-test` and GitHub run URLs for the same commit, the final course CI PASS, and an externally accessible HTTPS WebUI URL. Reject localhost as the public URL, screenshots/local logs as CI proof, placeholder/example domains, mismatched commits, future timestamps, unsigned assertions, or `PASS` paired with `not executed`.

Run:

~~~powershell
python -m pytest backend/tests/integration/test_release_evidence_contract.py -q
~~~

Expected: FAIL while the verifier/matrix or any real remote evidence is absent. This failure is correct and must not be bypassed with dummy CI URLs or a fabricated deployment status.

- [ ] **Step 2: Add the minimum fail-closed verifier and evidence matrix**

Make `final_verify.ps1` run the canonical tests, focused release-contract test, secret/license/evidence validators, Windows and OCI artifact contract checks, and validate evidence metadata against `git rev-parse HEAD`. Require explicit rows for all ACs and both reviews. Query or inspect remote CI/deployment only after the user authorizes the necessary access; record the exact URL, commit, job, observed status, and observation time. If a remote is unavailable or authorization is withheld, leave `not executed` and return nonzero. Update README only with facts just verified. Do not rewrite student reflection, backfill conversations/timestamps, or infer a public result from local tests.

- [ ] **Step 3: Run focused and full regression verification**

After all authorized external evidence exists, run:

~~~powershell
$commit = git rev-parse HEAD
python -m pytest backend/tests/integration/test_release_evidence_contract.py -q
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/final_verify.ps1 -ExpectedCommit $commit
python scripts/test_all.py
~~~

Expected: the focused test, final verifier, and full suite PASS for the same commit; the verifier confirms real passing GitLab/GitHub records, the course-final CI, a reachable public HTTPS WebUI, reproducible Windows/OCI results, UI evidence, complete licenses, and no secret/private courseware. Before those facts exist, the expected result is nonzero and FIN-01 remains pending.

- [ ] **Step 4: Perform both reviews, commit, and invoke branch finishing**

SPEC compliance review walks AC-01 through AC-50 one by one and rejects missing, stale, or wrong-commit evidence. Quality/security/license review checks deterministic reproduction, scanner scope/redaction, artifact provenance, dependency/asset notices, data/credential boundaries, private-course exclusion, remote evidence authenticity, and release documentation. Commit local gate files with `chore(FIN-01): add fail-closed release verification`. The coordinator records the real commit/reviews in `PLAN.md` and `AGENT_LOG.md`, then invokes `finishing-a-development-branch` to present the actual merge/PR/keep options. Perform no push, PR/MR, merge, release, deployment, or paid call until the user explicitly authorizes that exact action.
**Commit command:** `git add -- scripts/final_verify.ps1 backend/tests/integration/test_release_evidence_contract.py docs/engineering/FINAL_VERIFICATION.md docs/engineering/RELEASE_CHECKLIST.md README.md; git diff --cached --check; git commit -m "chore(FIN-01): add fail-closed release verification [agent: <fresh-agent-id>]"; git rev-parse HEAD`

**Completion standard:** Every acceptance criterion has current evidence, all focused/full/build/static/UI/distribution checks pass, both reviews have no unresolved Critical issue, task/process records contain real hashes, secret/license checks pass, artifacts reproduce on their target environments, both remote CI systems and the final course pipeline pass for the recorded commit, and the public WebUI URL is actually reachable. Missing authorization or external evidence leaves FIN-01 pending with `not executed`; it can never be completed by fabricating CI or URL evidence.

### Task Group API-01 (not dispatchable): Course, Material, Policy, and Coverage Routes

Planning group ID: API-01 (not dispatchable; use API-01A/API-01B/API-01C)

**Goal:** Expose the M1 course/material workflow through a strict, owner-scoped HTTP contract. The route layer must stop at metadata inspection until the user selects L/P/F and creates an exact consent record; candidate coverage must remain separate from confirmed coverage and must use optimistic version checks.

**Files:**
- Modify: `backend/src/projectb/api/app.py` (register the route registry and keep the loopback/security middleware from T-04 in the request path)
- Create: `backend/src/projectb/api/routes/__init__.py`
- Create: `backend/src/projectb/api/routes/courses.py`
- Create: `backend/src/projectb/api/routes/materials.py`
- Create: `backend/src/projectb/api/routes/policy.py`
- Create: `backend/src/projectb/api/routes/coverage.py`
- Create: `backend/src/projectb/api/schemas/materials.py`
- Create: `backend/tests/integration/test_api_course_materials.py`
- Create: `backend/tests/integration/test_api_policy_coverage.py`

**Interfaces:**
- `GET /api/courses` -> `CourseSummary[]`; `POST /api/courses` accepts `{name, timezone_id}` and returns `CourseSummary` with status 201; `GET /api/courses/{course_id}` is owner-scoped.
- `POST /api/courses/{course_id}/batches/inspect` accepts a validated local staging/metadata envelope and returns `BatchInspection` with `awaiting_policy`, per-file limits, hashes, role candidates, and quality flags. It may stream enough bytes to validate magic, size, and hash, but must not parsebody text, persist extractable text, or call a provider before policy/consent.
- `GET /api/courses/{course_id}/batches/{batch_id}` returns independent per-file states, including `unsupported_role` and `needs_user_review`; `POST /api/courses/{course_id}/batches/{batch_id}/policy` accepts `{mode: L|P|F, file_ids, scope, profile_fingerprint}` and returns a policy preview without silently widening scope.
- `POST /api/courses/{course_id}/batches/{batch_id}/consent` accepts the exact file/hash/mode/profile/capability/policy payload and creates an immutable `ConsentRecord`; `GET` returns redacted status only. `GET/PATCH /api/courses/{course_id}/policy` reads or changes the course policy and requires a new confirmation when the outbound scope grows.
- `GET /api/courses/{course_id}/coverage?batch_id=...` returns candidate coverage, source locator/quality/confidence, and confirmation state. `POST /api/courses/{course_id}/coverage/decisions` accepts `{expected_version, decisions[]}` and writes an append-only `CoverageDecision`; stale versions return 409 and unconfirmed/ambiguous items never enter authoritative state.
- Route errors use the stable codes `validation_error`, `owner_forbidden`, `not_found`, `awaiting_policy`, `awaiting_consent`, `unsupported_role`, `needs_user_review`, `state_inconsistent`, and `conflict`; responses contain opaque IDs and recovery actions, never local paths, body text, or credentials.
- `routes/__init__.py` owns a single explicit router list. API-02, API-03, API-04, and DEMO-01 add routers through a coordinator-serialized registration change rather than importing arbitrary modules at runtime. API-01A/B/C are the only dispatchable units for this group.

**Dependencies / parallelism:** Group summary only. API-01A requires M1-03/T-04/T-06; API-01B requires API-01A; API-01C requires API-01B/M1-03. The route registry and `app.py` registration are shared API-boundary files; implementation and merges are serialized by the API owner. API-01C establishes the response/error envelope consumed by later API/UI tasks.

- [ ] **Step 1: Write the minimum failing test**

  Add a test that creates a course, inspects a staged PDF descriptor, and asserts `201`, `awaiting_policy`, per-file hash/limit metadata, zero parser calls, and zero provider calls. Add a second test that posts a coverage decision with a stale `expected_version` and expects 409 without a write.

  Run:

  ```powershell
  python -m pytest backend/tests/integration/test_api_course_materials.py backend/tests/integration/test_api_policy_coverage.py -q
  ```

  Expected: FAIL because the routers, schemas, and route registry do not yet exist.

- [ ] **Step 2: Implement the smallest route layer in three fresh checkpoints**

  1. **API-01A course/material inspection:** add strict course and batch schemas/routes, metadata/hash-only inspection, owner scope, and stable errors.
  2. **API-01B policy/consent:** add exact L/P/F policy preview and immutable consent snapshots, with CSRF/Host/Origin enforcement and no silent widening.
  3. **API-01C coverage/version conflict:** add candidate/confirmed coverage routes, expected-version checks, append-only decisions, and authoritative-service-only writes.

  Each checkpoint has its own focused red test and commit; shared `routes/__init__.py` and `app.py` registration is merged serially by the API owner. Do not duplicate domain validation or create a second persistence path.

- [ ] **Step 3: Focused and full regression**

  Run:

  ```powershell
  python -m pytest backend/tests/integration/test_api_course_materials.py backend/tests/integration/test_api_policy_coverage.py -q
  python -m pytest backend/tests -q
  python scripts/test_all.py
  ```

  Expected: focused route tests pass; the full backend suite and the one-command entry pass; no unauthorized parser/provider call, cross-owner read, body/path log, or silent policy expansion is observed.

- [ ] **Step 4: SPEC compliance review and quality/security/license review**

  SPEC review must check AC-01, AC-02, AC-03, AC-15, AC-16, AC-17, AC-25, AC-28, AC-30, AC-33, and AC-45 against each route and error path. Quality/security/license review must check strict schema bounds, multipart/hash handling, owner isolation, optimistic concurrency, CSRF/Host/Origin enforcement, redacted errors/audit, no secret/body persistence, dependency evidence from G-02, and no unverified third-party asset or parser license. Critical findings block the next API task.

  **Group record:** no worker commit is assigned to the group heading. The coordinator records API-01A/B/C hashes and reviews separately.

**Completion standard:** A clean test profile can create and inspect a course batch, require an explicit L/P/F policy and exact consent before processing, expose source-bound candidate coverage, reject stale or unauthorized decisions deterministically, and register the routes without bypassing shared security controls.

### Task API-01A: Add Course and Material Inspection Routes

**Goal:** Expose owner-scoped course creation/read and metadata-only batch inspection without policy, consent, or coverage writes.

**Files:** Modify `backend/src/projectb/api/app.py`; create `backend/src/projectb/api/routes/__init__.py`, `backend/src/projectb/api/routes/courses.py`, `backend/src/projectb/api/routes/materials.py`, `backend/src/projectb/api/schemas/materials.py`, and `backend/tests/integration/test_api_course_materials.py`.

**Interfaces:** course list/create/get; batch metadata/hash inspection and per-file states; stable redacted errors; shared security middleware remains in path.

**Dependencies / parallelism:** Requires M1-03, T-04, and T-06. It owns the initial route registry and completes before API-01B.

- [ ] **Red:** assert course 201, owner isolation, `awaiting_policy`, hash/limit metadata, and zero parser/provider calls; run `python -m pytest backend/tests/integration/test_api_course_materials.py -q`. Expected: FAIL because routes/schemas are absent.
- [ ] **Green/refactor:** implement only course/material inspection routes, run the focused test, backend regression, and `python scripts/test_all.py`.
- [ ] **Reviews:** SPEC review AC-01, AC-03, AC-15, AC-30, AC-33, AC-45; quality review strict bounds, streaming/hash handling, owner/CSRF enforcement, redacted errors, and no parser/body/provider access. Critical findings block API-01B.
- [ ] **Commit:** scan secrets; `git add -- backend/src/projectb/api/app.py backend/src/projectb/api/routes/__init__.py backend/src/projectb/api/routes/courses.py backend/src/projectb/api/routes/materials.py backend/src/projectb/api/schemas/materials.py backend/tests/integration/test_api_course_materials.py`; run `git diff --cached --check`; commit with `git commit -m "feat(API-01A): add course material inspection routes [agent: <fresh-agent-id>]"`.

**Completion standard:** Course and batch metadata inspection is owner-scoped, bounded, parser/provider-free, and consistently registered through shared security controls.

### Task API-01B: Add Policy and Exact-consent Routes

**Goal:** Expose L/P/F policy preview/change and immutable exact consent without widening scope or adding a second policy engine.

**Files:** Create `backend/src/projectb/api/routes/policy.py` and `backend/tests/integration/test_api_policy_consent.py`; modify `backend/src/projectb/api/routes/__init__.py` through the API route owner.

**Interfaces:** batch policy preview, exact consent create/redacted get, course policy get/patch, new-confirmation requirement on scope expansion, and stable awaiting-policy/consent errors.

**Dependencies / parallelism:** Requires API-01A and T-06. Registry edit is serialized; completes before API-01C.

- [ ] **Red:** assert no consent before policy, exact file/hash/profile snapshot, mode/scope changes invalidate old consent, widening needs confirmation, and no provider call; run `python -m pytest backend/tests/integration/test_api_policy_consent.py -q`. Expected: FAIL because policy/consent routes are absent.
- [ ] **Green/refactor:** implement strict route schemas over T-06 only; run the focused test, backend regression, and `python scripts/test_all.py`.
- [ ] **Reviews:** SPEC review AC-01, AC-02, AC-25, AC-28, AC-30; quality review canonical scope, CSRF/owner checks, redacted status, optimistic versioning, and no silent fallback. Critical findings block API-01C.
- [ ] **Commit:** scan secrets; `git add -- backend/src/projectb/api/routes/policy.py backend/src/projectb/api/routes/__init__.py backend/tests/integration/test_api_policy_consent.py`; run `git diff --cached --check`; commit with `git commit -m "feat(API-01B): add policy and consent routes [agent: <fresh-agent-id>]"`.

**Completion standard:** Every processing route can require a current exact policy/consent snapshot, and any widening or configuration change returns to explicit confirmation.

### Task API-01C: Add Coverage Decision and Version-conflict Routes

**Goal:** Expose source-bound coverage candidates and append-only user decisions with deterministic optimistic concurrency.

**Files:** Create `backend/src/projectb/api/routes/coverage.py` and `backend/tests/integration/test_api_coverage.py`; modify `backend/src/projectb/api/routes/__init__.py` through the API route owner.

**Interfaces:** candidate coverage list with locators/quality/confidence and decision post with `expected_version`; stale versions return 409 and unconfirmed/ambiguous candidates remain non-authoritative.

**Dependencies / parallelism:** Requires API-01B and M1-03. API-02/API-03/UI-01C/DEMO depend on this terminal unit.

- [ ] **Red:** assert candidate/confirmed separation, stale version 409/no write, owner mismatch, ambiguous locator rejection, and redacted error recovery; run `python -m pytest backend/tests/integration/test_api_coverage.py -q`. Expected: FAIL because coverage routes are absent.
- [ ] **Green/refactor:** implement the smallest coverage route layer, run the focused test, all API tests, and `python scripts/test_all.py`.
- [ ] **Reviews:** SPEC review AC-03, AC-16, AC-17, AC-19, AC-25, AC-37; quality review locator validation, optimistic concurrency, stable ordering, owner scope, append-only decisions, and no duplicate persistence path. Critical findings block downstream API/UI work.
- [ ] **Commit:** scan secrets; `git add -- backend/src/projectb/api/routes/coverage.py backend/src/projectb/api/routes/__init__.py backend/tests/integration/test_api_coverage.py`; run `git diff --cached --check`; commit with `git commit -m "feat(API-01C): add coverage decision routes [agent: <fresh-agent-id>]"`.

**Completion standard:** API consumers can distinguish and confirm source-bound candidates, while stale, unauthorized, ambiguous, or unconfirmed inputs cannot affect authoritative course state.

### Task Group API-02 (not dispatchable): Learning, Evidence, Explanation, and Practice Routes

Planning group ID: API-02 (not dispatchable; use API-02A/API-02B)

**Goal:** Provide the M2 HTTP contract for source-bound explanations, deterministic understanding checks, practice candidates, and append-only learning evidence. An explanation response is never itself mastery, and provider output can enter only a validated candidate or a labelled `model_supplement` display path.

**Files:**
- Create: `backend/src/projectb/api/routes/learning.py`
- Create: `backend/src/projectb/api/routes/explanations.py`
- Create: `backend/src/projectb/api/routes/practice.py`
- Create: `backend/src/projectb/api/schemas/learning.py`
- Create: `backend/tests/integration/test_api_learning.py`
- Create: `backend/tests/integration/test_api_evidence_boundaries.py`
- Modify: `backend/src/projectb/api/routes/__init__.py` only through the API route owner to register the new routers

**Interfaces:**
- `GET /api/courses/{course_id}/learning/state` returns the current source-backed concept/evidence summary with unknown states preserved; it never treats a viewed explanation as evidence.
- `POST /api/courses/{course_id}/explanations` accepts `{concept_id, goal, evidence_ids, source_locators, mode, consent_id, port_version, idempotency_key}` and returns an `ExplanationSession` plus candidate blocks. Missing/stale locators yield `source_insufficient`; general text is explicitly marked `model_supplement`.
- `GET /api/courses/{course_id}/explanations/{session_id}` returns the immutable session/candidate status. `POST .../explanations/{session_id}/attempts` accepts a student response and attempt key; `POST .../explanations/{session_id}/checks` invokes the deterministic mutex/race oracle and rubric, returning criterion-level feedback without directly writing mastery.
- `POST /api/courses/{course_id}/evidence` appends a validated `LearningEvidence` record only when it references an evaluator result/attempt; `GET .../evidence` is paginated and redacted. `POST /api/courses/{course_id}/practice/candidates/{candidate_id}/accept` records user acceptance but cannot promote an unverified provider candidate to authoritative coverage.
- Every provider-facing request is assembled by X2-01 with named port/version, allowed source/evidence IDs, budget/timeout, schema, and idempotency key. Route handlers reject arbitrary paths, unknown ports, stale consent, and malformed candidate payloads before dispatch and map failures to recoverable codes without changing authoritative state.

**Dependencies / parallelism:** Requires M2-02 and the stable API-01C envelope. Learning/explanation modules may be implemented in parallel with API-03/04 in separate worktrees, but the route registry registration is serialized. No route may call a provider or planner directly; it consumes application services and the shared provider contract.

- [ ] **Step 1: Write the minimum failing test**

  Add a test that starts an explanation with a valid source locator and asserts the response has an `ExplanationSession` but no `mastery`/`demonstrated_now` transition. Add a no-locator test that returns `source_insufficient` and records zero provider calls, then submit a parameterized trajectory attempt and assert only the deterministic evaluator can append evidence.

  Run:

  ```powershell
  python -m pytest backend/tests/integration/test_api_learning.py backend/tests/integration/test_api_evidence_boundaries.py -q
  ```

  Expected: FAIL because the learning routes and schemas are absent.

- [ ] **Step 2: Implement the smallest route layer**

  Define strict request models for source locators, port envelopes, attempts, and rubric results; inject M2/X2 services; enforce idempotency and consent; return candidate/status envelopes with stable error codes. Store only opaque IDs and approved evidence metadata in audit events. Keep student answer text out of ordinary logs and do not expose evaluator internals as a model-authored score.

- [ ] **Step 3: Focused and full regression**

  Run:

  ```powershell
  python -m pytest backend/tests/integration/test_api_learning.py backend/tests/integration/test_api_evidence_boundaries.py -q
  python -m pytest backend/tests -q
  python scripts/test_all.py
  ```

  Expected: focused tests pass; full regression passes with provider mock scenarios, locator validation, and security middleware; provider wording, timeout, bad schema, or injection fixtures leave coverage, plan, due dates, and mastery unchanged.

- [ ] **Step 4: SPEC compliance review and quality/security/license review**

  SPEC review must check AC-03, AC-04, AC-12, AC-13, AC-14, AC-21, AC-22, AC-23, AC-24, AC-32, and AC-34. Quality/security/license review must check source-locator freshness, evaluator determinism, idempotency/replay, answer-text redaction, provider boundary isolation, timeout/cancellation behavior, dependency/license evidence, and absence of arbitrary tool dispatch. Resolve Critical findings before API-03 or UI-04B consumes the contract.

  **Group record:** no worker commit is assigned to this heading. The coordinator records API-02A/B hashes and reviews separately.

**Completion standard:** The browser can start a source-bound explanation, run the bounded understanding/practice checks, and append evidence through the API while a missing source, provider failure, or wording change provably cannot create authoritative mastery or plan state.

### Task API-02A: Add Explanation and Practice Session Routes

**Goal:** Expose source-bound explanation creation/status and practice candidate acceptance without attempt/evidence writes.

**Files:** Create `backend/src/projectb/api/routes/learning.py`, `backend/src/projectb/api/schemas/learning.py`, and `backend/tests/integration/test_api_explanations.py`; modify `backend/src/projectb/api/routes/__init__.py` through the API owner.

**Interfaces:** learning state read, explanation create/get, practice candidate acceptance, strict source/evidence/consent/idempotency envelope, and recoverable provider/source failures.

**Dependencies / parallelism:** Requires M2-02A and API-01C. It completes before API-02B; route registration is serialized.

- [ ] **Red:** assert source-bound explanation create/get, missing locator supplement/failure semantics, deterministic practice candidate, owner/CSRF, timeout unchanged state, and no evidence/mastery write; run `python -m pytest backend/tests/integration/test_api_explanations.py -q`. Expected: FAIL because session routes are absent.
- [ ] **Green/refactor:** implement session/practice routes only; run focused/API/backend tests and `python scripts/test_all.py`.
- [ ] **Reviews:** SPEC review AC-03, AC-12, AC-13, AC-21, AC-22, AC-23, AC-32; quality review schema bounds, locator freshness, idempotency/cancel, redaction, and no direct adapter call. Critical findings block API-02B/UI-04A.
- [ ] **Commit:** scan secrets; `git add -- backend/src/projectb/api/routes/learning.py backend/src/projectb/api/schemas/learning.py backend/src/projectb/api/routes/__init__.py backend/tests/integration/test_api_explanations.py`; run `git diff --cached --check`; commit with `git commit -m "feat(API-02A): add explanation and practice routes [agent: <fresh-agent-id>]"`.

**Completion standard:** API clients can create/read source-bound candidate sessions with deterministic recovery and zero evidence/mastery authority.

### Task API-02B: Add Attempt, Check, Feedback, and Evidence Routes

**Goal:** Expose structured attempts/checks and append/list evidence only after the deterministic evaluator result.

**Files:** Create `backend/src/projectb/api/routes/evidence.py` and `backend/tests/integration/test_api_evidence_boundaries.py`; modify `backend/src/projectb/api/routes/learning.py`, `backend/src/projectb/api/schemas/learning.py`, and `backend/src/projectb/api/routes/__init__.py` through API-02A ownership.

**Interfaces:** attempt append, deterministic check, feedback status, evidence append/list, duplicate key handling, and no candidate-to-authority promotion.

**Dependencies / parallelism:** Requires API-02A and M2-02B. UI-04B/DEMO-01B depend on this terminal unit.

- [ ] **Red:** assert evidence only after valid oracle result, duplicate idempotency, malformed/provider failure unchanged evidence, paginated/redacted list, and owner/CSRF boundaries; run `python -m pytest backend/tests/integration/test_api_evidence_boundaries.py -q`. Expected: FAIL because check/evidence routes are absent.
- [ ] **Green/refactor:** implement only attempt/check/evidence routes; run focused/API/backend tests and `python scripts/test_all.py`.
- [ ] **Reviews:** SPEC review AC-04, AC-14, AC-17, AC-23, AC-24, AC-34; quality review evaluator determinism, answer redaction, transactionality, replay, cancellation, and no provider authority. Critical findings block UI/demo consumers.
- [ ] **Commit:** scan secrets; `git add -- backend/src/projectb/api/routes/evidence.py backend/src/projectb/api/routes/learning.py backend/src/projectb/api/schemas/learning.py backend/src/projectb/api/routes/__init__.py backend/tests/integration/test_api_evidence_boundaries.py`; run `git diff --cached --check`; commit with `git commit -m "feat(API-02B): add attempt check and evidence routes [agent: <fresh-agent-id>]"`.

**Completion standard:** HTTP evidence is append-only, oracle-proven, redacted, and unchanged by model wording/failure.

### Task Group API-03 (not dispatchable): Review, Finals, Plan Revision, and Task Routes

Planning group ID: API-03 (not dispatchable; use API-03A/API-03B/API-03C)

**Goal:** Expose deterministic M3 planning and review state through versioned, optimistic-concurrency-safe routes. The API must preserve history, require explicit finals entry, display policy/default provenance, and make every revision/reversal and post-exam pause observable.

**Files:**
- Create: `backend/src/projectb/api/routes/review.py`
- Create: `backend/src/projectb/api/routes/finals.py`
- Create: `backend/src/projectb/api/routes/revisions.py`
- Create: `backend/src/projectb/api/schemas/review.py`
- Create: `backend/tests/integration/test_api_review.py`
- Create: `backend/tests/integration/test_api_finals_revision.py`
- Modify: `backend/src/projectb/api/routes/__init__.py` only through the API route owner to register the new routers

**Interfaces:**
- `GET /api/courses/{course_id}/plan` returns the active plan, policy version, budget value/source, task reason codes, and current plan input hash. `POST /api/courses/{course_id}/plan/recalculate` accepts an expected plan version and a deterministic clock/tzdata context supplied by the application service; it returns the existing plan or a new `PlanRevision` without mutating started/completed tasks.
- `GET /api/courses/{course_id}/plan/revisions` and `GET .../plan/revisions/{revision_id}/diff` expose append-only history. `POST .../plan/revisions/{revision_id}/revert` creates a new revision with `reverts_revision_id`; it never deletes or edits the reverted revision.
- `PATCH /api/courses/{course_id}/review-goal` accepts `mode`, optional local exam date, IANA timezone, and 10–480 minute budget in five-minute steps. Date entry alone remains `continuous`. `POST /api/courses/{course_id}/finals/enter` is the explicit transition; `POST .../finals/exit` only affects future tasks.
- `GET /api/courses/{course_id}/review-tasks` lists tasks with concept, due local date, estimated minutes, evidence, and reason codes. `POST .../review-tasks/{task_id}/attempts` appends the actual attempt and delegates evidence/mastery changes to M3-02C. Past-paper/teacher-focus mappings are returned as unconfirmed candidates until the M3-03 confirmation route is called.
- `POST /api/courses/{course_id}/finals/mappings/{mapping_id}/confirm` accepts a user correction/confirmation and returns a revision candidate; provider output or a failed mapping cannot alter priority. When `today_local > target_local_date`, `POST .../plan/recalculate` returns `post_exam_paused` with zero future tasks and an archived finals plan.

**Dependencies / parallelism:** Requires M3-02C, M3-03, and API-01C's course/owner contract. Route tests may be written in parallel with API-02/04, but app/registry changes are coordinator-serialized. The routes must call the pure planner and repositories, never compute hidden weights or use provider output for authoritative ordering.

- [ ] **Step 1: Write the minimum failing test**

  Add a test that patches an exam date and asserts the goal remains `continuous`, then explicitly enters finals and asserts a `finals` plan. Add golden cases for a stale revision revert (new `reverts_revision_id`, old history intact) and `today_local > target_local_date` (zero tasks and `post_exam_paused`).

  Run:

  ```powershell
  python -m pytest backend/tests/integration/test_api_review.py backend/tests/integration/test_api_finals_revision.py -q
  ```

  Expected: FAIL because the review/finals/revision routers and schemas are absent.

- [ ] **Step 2: Implement the smallest route layer**

  Add strict date/timezone/budget validation, expected-version preconditions, route-level idempotency, and stable error mappings. Return policy version/default source and deterministic reason codes in every plan response. Ensure all writes are append-only and that failed/uncertain mappings stay candidates; route-level errors cannot partially promote coverage or delete historical evidence.

- [ ] **Step 3: Focused and full regression**

  Run:

  ```powershell
  python -m pytest backend/tests/integration/test_api_review.py backend/tests/integration/test_api_finals_revision.py -q
  python -m pytest backend/tests -q
  python scripts/test_all.py
  ```

  Expected: focused API tests pass; all M3 golden fixtures, evidence transitions, concurrency, security, and provider-mock regression pass; repeated fixed inputs return identical IDs/order/reasons and no task is silently dropped when capacity is exceeded.

- [ ] **Step 4: SPEC compliance review and quality/security/license review**

  SPEC review must check AC-04, AC-05, AC-16, AC-17, AC-18, AC-19, AC-22, AC-34, AC-35, and AC-36, including every ReviewPolicy v1 boundary. Quality/security/license review must check timezone/DST conversion, canonical hashes, optimistic concurrency, append-only history, authorization, audit redaction, no provider authority over scheduling, and verified test/dependency licenses. Critical issue resolution is required before UI-05B or DEMO-01 uses the route contract.

  **Group record:** no worker commit is assigned to this heading. The coordinator records API-03A/B/C hashes and reviews separately.

**Completion standard:** The API exposes a reproducible plan and review workflow with explicit finals entry, visible budget/policy/reasons, reversible future-task revisions, preserved history, and deterministic post-exam pause semantics.

### Task API-03A: Add Plan, Review-task, and Revision Routes

**Goal:** Expose deterministic plan/tasks, recalculation, revision history/diffs, and append-only revert without finals/focus transitions.

**Files:** Create `backend/src/projectb/api/routes/review.py`, `backend/src/projectb/api/schemas/review.py`, and `backend/tests/integration/test_api_review_plan.py`; modify `backend/src/projectb/api/routes/__init__.py` through the API owner.

**Interfaces:** plan get/recalculate, task list/attempt delegation, revision list/diff/revert, expected-version conflicts, and preserved started/completed history.

**Dependencies / parallelism:** Requires M3-02B and API-01C. It completes before API-03B; registration is serialized.

- [ ] **Red:** assert deterministic IDs/order/reasons, capacity visibility, stale revision conflict, append-only revert, and preserved started/completed tasks; run `python -m pytest backend/tests/integration/test_api_review_plan.py -q`. Expected: FAIL because plan/revision routes are absent.
- [ ] **Green/refactor:** implement only plan/task/revision routes; run focused/API/backend tests and `python scripts/test_all.py`.
- [ ] **Reviews:** SPEC review AC-05, AC-17, AC-18, AC-34, AC-35, AC-36; quality review canonical hashes, optimistic concurrency, append-only history, owner/audit, and no client/provider scheduling authority. Critical findings block API-03B/UI-05A.
- [ ] **Commit:** scan secrets; `git add -- backend/src/projectb/api/routes/review.py backend/src/projectb/api/schemas/review.py backend/src/projectb/api/routes/__init__.py backend/tests/integration/test_api_review_plan.py`; run `git diff --cached --check`; commit with `git commit -m "feat(API-03A): add plan task and revision routes [agent: <fresh-agent-id>]"`.

**Completion standard:** Plan/task/revision HTTP behavior is deterministic, conflict-safe, explainable, and history-preserving.

### Task API-03B: Add Review-goal, Finals, and Post-exam Routes

**Goal:** Expose date/timezone/budget goal changes, explicit finals entry/exit, and post-exam pause without study-focus confirmation.

**Files:** Create `backend/src/projectb/api/routes/finals.py` and `backend/tests/integration/test_api_finals_revision.py`; modify `backend/src/projectb/api/schemas/review.py` and `backend/src/projectb/api/routes/__init__.py` through API-03A ownership.

**Interfaces:** review-goal patch, explicit finals enter/exit, future-only effects, budget validation, exam-day active state, and after-date pause/zero future tasks.

**Dependencies / parallelism:** Requires API-03A and M3-02C. It completes before API-03C and UI-05B.

- [ ] **Red:** assert date-only remains continuous, explicit entry, 10/480 five-minute validation, exam-day not paused, exit future-only, and after-date pause; run `python -m pytest backend/tests/integration/test_api_finals_revision.py -q`. Expected: FAIL because finals routes are absent.
- [ ] **Green/refactor:** implement finals/goal routes only; run focused/API/backend tests and `python scripts/test_all.py`.
- [ ] **Reviews:** SPEC review AC-05, AC-08, AC-18, AC-34, AC-35, AC-36; quality review timezone/DST, explicit actions, history preservation, owner/CSRF/audit, and no automatic mode change. Critical findings block API-03C/UI-05B.
- [ ] **Commit:** scan secrets; `git add -- backend/src/projectb/api/routes/finals.py backend/src/projectb/api/schemas/review.py backend/src/projectb/api/routes/__init__.py backend/tests/integration/test_api_finals_revision.py`; run `git diff --cached --check`; commit with `git commit -m "feat(API-03B): add review goal and finals routes [agent: <fresh-agent-id>]"`.

**Completion standard:** Finals transitions are explicit, date-correct, owner-scoped, and modify only future planning state.

### Task API-03C: Add Study-focus Confirmation Routes

**Goal:** Expose source-bound teacher-focus/past-paper candidates and explicit confirmation without direct provider priority authority.

**Files:** Create `backend/src/projectb/api/routes/study_focus.py` and `backend/tests/integration/test_api_study_focus.py`; modify `backend/src/projectb/api/routes/__init__.py` through the API owner.

**Interfaces:** candidate list, confirm/reject/correct with expected version, source locator/role/confidence, and revision candidate only after confirmation.

**Dependencies / parallelism:** Requires API-03B and M3-03. UI-05B/DEMO-01B depend on this terminal unit.

- [ ] **Red:** assert unconfirmed/low-confidence/provider-failed candidate has no priority/plan effect, confirmed decision triggers a revision candidate, stale version conflicts, and unsupported role remains rejected; run `python -m pytest backend/tests/integration/test_api_study_focus.py -q`. Expected: FAIL because study-focus routes are absent.
- [ ] **Green/refactor:** implement only study-focus routes; run focused/API/backend tests and `python scripts/test_all.py`.
- [ ] **Reviews:** SPEC review AC-18, AC-19, AC-20, AC-22, AC-33, AC-34, AC-35, AC-36; quality review candidate authority, locator/role validation, optimistic concurrency, academic-integrity copy, and no provider direct plan write. Critical findings block UI/demo.
- [ ] **Commit:** scan secrets; `git add -- backend/src/projectb/api/routes/study_focus.py backend/src/projectb/api/routes/__init__.py backend/tests/integration/test_api_study_focus.py`; run `git diff --cached --check`; commit with `git commit -m "feat(API-03C): add study focus confirmation routes [agent: <fresh-agent-id>]"`.

**Completion standard:** Only source-bound user-confirmed focus decisions can feed plan revisions, with stale/provider-only inputs remaining non-authoritative.

### Task Group API-04 (not dispatchable): Credentials, Audit, Provider Settings, and Security Status Routes

Planning group ID: API-04 (not dispatchable; use API-04A/API-04B)

**Goal:** Provide the X1 settings surface for hidden credential entry, status/update/clear, validated provider profiles, and minimal audit/security status without returning or persisting secret values.

**Files:**
- Create: `backend/src/projectb/api/routes/settings.py`
- Create: `backend/src/projectb/api/routes/credentials.py`
- Create: `backend/src/projectb/api/routes/audit.py`
- Create: `backend/src/projectb/api/schemas/settings.py`
- Create: `backend/tests/integration/test_api_credentials.py`
- Create: `backend/tests/integration/test_api_audit_redaction.py`
- Modify: `backend/src/projectb/api/routes/__init__.py` only through the API route owner to register the new routers

**Interfaces:**
- `GET /api/settings/provider-profiles` returns only allowed adapter/model/controlled-parameter/profile fingerprints and `credential_ref`; it rejects unknown fields, `base_url`, custom endpoints, dynamic plugins, and key/token/password fields before credential resolution.
- `GET /api/settings/credentials/{profile_id}/status` returns `{configured, updated_at, error_code?}`. `PUT /api/settings/credentials/{profile_id}` accepts a hidden value over the protected local request and writes only through `SecretStore`; `DELETE .../credentials/{profile_id}` supports an explicit `force` flag and returns `delete_incomplete`/recovery information when remote cleanup cannot finish. The value must never be echoed, serialized, logged, or stored in browser state.
- `PUT /api/settings/provider-profiles/{profile_id}` validates the profile and capability/policy snapshot before it can authorize P/F; changing its fingerprint invalidates older consent records. `GET /api/settings/security` reports loopback binding, accepted origins, CSRF/session status, and demo/local profile, never a secret or file path.
- `GET /api/settings/audit?cursor=...` returns paginated whitelist-only events (type, opaque IDs, result, duration, approved metadata). It must not expose request bodies, answers, paths, course text, credential-shaped values, or provider payloads.
- All mutating settings routes use T-04 CSRF/Host/Origin checks and map `owner_forbidden`, `invalid_profile`, `credential_unavailable`, `delete_incomplete`, and `validation_error` without stack traces.

**Dependencies / parallelism:** Requires T-04, T-05, and T-06. It can be developed beside API-02/API-03 once API-01C's route envelope is available; registration remains serialized. The tests use an in-memory `SecretStore` fake and never parse `.env` or contact a provider.

- [ ] **Step 1: Write the minimum failing test**

  Add a test that configures a fake credential and asserts status is configured while the secret is absent from response, `repr`, SQLite, audit, and captured logs. Add profile tests rejecting `base_url`/unknown fields before `resolve`, and a forced-clear test that blocks subsequent P/F calls and returns `delete_incomplete` when a remote job remains.

  Run:

  ```powershell
  python -m pytest backend/tests/integration/test_api_credentials.py backend/tests/integration/test_api_audit_redaction.py -q
  ```

  Expected: FAIL because the settings/credential/audit routers are absent.

- [ ] **Step 2: Implement the smallest route layer**

  Use strict schemas and the T-05 credential service, inject the audit writer, set no-store/no-cache headers for credential responses, and accept the hidden value only in a bounded request body. Return status/ref/timestamp only; validate profile and policy snapshots before resolve; preserve deletion/recovery state on forced clear. Add a route test logger that fails on secret/path/body patterns.

- [ ] **Step 3: Focused and full regression**

  Run:

  ```powershell
  python -m pytest backend/tests/integration/test_api_credentials.py backend/tests/integration/test_api_audit_redaction.py -q
  python -m pytest backend/tests -q
  python scripts/test_all.py
  ```

  Expected: focused tests pass; full regression confirms hidden entry/status/update/clear, profile fail-closed behavior, CSRF and owner isolation, and zero secret findings in config, SQLite, browser responses, logs, snapshots, and test reports.

- [ ] **Step 4: SPEC compliance review and quality/security/license review**

  SPEC review must check AC-07, AC-11, AC-21, AC-28, AC-30, AC-31, AC-38, AC-39, and AC-40. Quality/security/license review must check constant-time/session-safe handling, process-memory lifetime, response caching, error redaction, forced-clear semantics, keyring backend evidence from G-02, and all direct/transitive license records. A suspected real credential stops the task and is reported without echoing it.

  **Group record:** no worker commit is assigned to this heading. The coordinator records API-04A/B hashes and reviews separately.

**Completion standard:** The local settings UI can safely configure, inspect, update, and clear a provider profile and read minimal audit/security status; no ordinary HTTP or persistence surface can reveal a credential or authorize an invalid profile.

### Task API-04A: Add Provider Profile and Credential Lifecycle Routes

**Goal:** Expose hidden configure/status/update/clear and strict provider-profile validation without audit listing/security status.

**Files:** Create `backend/src/projectb/api/routes/settings.py`, `backend/src/projectb/api/schemas/settings.py`, and `backend/tests/integration/test_api_credentials.py`; modify `backend/src/projectb/api/routes/__init__.py` through the API owner.

**Interfaces:** profile list/get/update, credential configure/status/clear, status/ref/timestamp only, no-store headers, force-clear recovery, and validation before secret resolution.

**Dependencies / parallelism:** Requires T-04, T-05, T-06, and API-01C. It completes before API-04B; UI-03C consumes this unit.

- [ ] **Red:** assert configured status without secret in response/repr/SQLite/logs, reject base_url/unknown fields before resolve, no-cache headers, CSRF/owner scope, and forced-clear incomplete recovery; run `python -m pytest backend/tests/integration/test_api_credentials.py -q`. Expected: FAIL because profile/credential routes are absent.
- [ ] **Green/refactor:** implement credential/profile routes only; run focused/API/backend tests and `python scripts/test_all.py`.
- [ ] **Reviews:** SPEC review AC-07, AC-11, AC-21, AC-30, AC-31, AC-38, AC-39, AC-40; quality review bounded secret lifetime, response caching, profile fail-closed order, redaction, keyring evidence, and licenses. A suspected credential stops the unit.
- [ ] **Commit:** scan secrets; `git add -- backend/src/projectb/api/routes/settings.py backend/src/projectb/api/schemas/settings.py backend/src/projectb/api/routes/__init__.py backend/tests/integration/test_api_credentials.py`; run `git diff --cached --check`; commit with `git commit -m "feat(API-04A): add profile and credential routes [agent: <fresh-agent-id>]"`.

**Completion standard:** HTTP clients can manage credential status safely, while no response, state, or invalid profile can expose or resolve the value improperly.

### Task API-04B: Add Redacted Audit and Security-status Routes

**Goal:** Expose minimal paginated audit/security state and prove route/request/error logs remain whitelist-only.

**Files:** Create `backend/src/projectb/api/routes/audit.py` and `backend/tests/integration/test_api_audit_redaction.py`; modify `backend/src/projectb/api/routes/__init__.py` through the API owner.

**Interfaces:** paginated audit events with type/opaque IDs/result/time/approved metadata, local security/credential capability status, redacted errors, and no path/body/answer/credential fields.

**Dependencies / parallelism:** Requires API-04A, T-04, and T-03C. QA-01B/DIST-01 consume this terminal unit.

- [ ] **Red:** inject secret/path/body-shaped values and assert they never appear in audit/status/response/logs; assert owner/CSRF/pagination bounds; run `python -m pytest backend/tests/integration/test_api_audit_redaction.py -q`. Expected: FAIL because audit/security routes are absent.
- [ ] **Green/refactor:** implement minimal whitelist-only audit/status routes; run focused/API/backend tests and `python scripts/test_all.py`.
- [ ] **Reviews:** SPEC review AC-07, AC-11, AC-30, AC-40; quality review whitelist schema, pagination, error/cache headers, cross-owner isolation, and scanner fixture redaction. Critical findings block QA/distribution.
- [ ] **Commit:** scan secrets; `git add -- backend/src/projectb/api/routes/audit.py backend/src/projectb/api/routes/__init__.py backend/tests/integration/test_api_audit_redaction.py`; run `git diff --cached --check`; commit with `git commit -m "feat(API-04B): add redacted audit and security status [agent: <fresh-agent-id>]"`.

**Completion standard:** Audit/security status is useful for recovery but cannot reconstruct a secret, answer, body, or private path.

### Task Group UI-01 (not dispatchable): Open Design-backed Shell, Timeline, Tokens, and Accessibility Base

Planning group ID: UI-01 (not dispatchable; use UI-01A/UI-01B/UI-01C)

**Goal:** Establish the formal responsive WebUI shell using the actual Open Design MCP/skill/design-system identifiers recorded by G-01. The shell must preserve the four-stage X-axis timeline at mobile and desktop widths, provide accessible landmarks/focus states, and expose a stable route/API boundary for later feature screens.

**Files:**
- Modify: `frontend/src/app/App.tsx`
- Create: `frontend/src/app/AppShell.tsx`
- Create: `frontend/src/app/routes.tsx`
- Create: `frontend/src/components/PhaseTimeline.tsx`
- Create: `frontend/src/components/StatusBanner.tsx`
- Create: `frontend/src/styles/tokens.css`
- Create: `frontend/src/styles/global.css`
- Create: `frontend/src/app/AppShell.test.tsx`
- Create: `frontend/src/components/PhaseTimeline.test.tsx`
- Create: `frontend/src/test/setup.ts`

**Interfaces:**
- `AppShell({profile, children})` renders semantic `header`, `nav`, `main`, and live status regions and consumes the selected Open Design tokens/components from `docs/engineering/OPEN_DESIGN_VALIDATION.md`; it must not invent a replacement system.
- `PhaseTimeline({activePhase, phases})` exposes exactly four phases (`import`, `understand`, `practice`, `review`) on one X axis at widths 320 px, 390 px, and 1440 px, with `aria-current`, visible labels/icon names, keyboard focus, and no page-level horizontal overflow.
- `routes.tsx` defines stable paths for import, materials/privacy, learning, review/finals, and settings and exposes a profile/health loading state; `StatusBanner` displays recoverable errors and demo/local profile without color-only meaning. The terminal shell unit is UI-01C.
- `tokens.css`/`global.css` contain the recorded design-system variables, responsive constraints, focus styles, typography/color contrast, and icon sizing. No feature state or secret is written to localStorage/sessionStorage.

**Dependencies / parallelism:** Group summary only. UI-01A requires G-01/API-01C; UI-01B requires UI-01A; UI-01C requires UI-01B/API-01C. No formal UI implementation may begin while Open Design evidence is missing. UI-02A through UI-05A may branch only after UI-01C; shared token/global files remain UI-01A-owned.

- [ ] **Step 1: Write the minimum failing test**

  Add Vitest/Testing Library tests that render the shell and assert four labelled timeline phases, `aria-current`, a main landmark, visible focusable navigation, and no `overflow-x` class at the supported viewport contract. Run:

  ```powershell
  npm --prefix frontend run test -- --run src/app/AppShell.test.tsx src/components/PhaseTimeline.test.tsx
  ```

  Expected: FAIL because the shell, timeline, and test setup do not exist.

- [ ] **Step 2: Implement the smallest shell**

  Wire the verified Open Design primitives/tokens, semantic layout, route outlet, profile health state, and keyboard/focus behavior. Keep the timeline horizontal at mobile by sizing its four stable tracks responsively; do not introduce a horizontal page scroller, decorative blobs, or an unverified icon/font library.

- [ ] **Step 3: Focused and full regression**

  Run:

  ```powershell
  npm --prefix frontend run test -- --run src/app/AppShell.test.tsx src/components/PhaseTimeline.test.tsx
  npm --prefix frontend run test -- --run
  npm --prefix frontend run build
  python scripts/test_all.py
  ```

  Expected: focused and full frontend tests, production build, and repository test entry pass; shell text fits at all required widths and no secret appears in client state.

- [ ] **Step 4: SPEC compliance review and quality/security/license review**

  SPEC review must check AC-08, AC-09, and AC-44 plus the §4.2 timeline/visual hierarchy requirements. Quality/security/license review must check actual Open Design evidence, keyboard/contrast/focus behavior, responsive overflow, bundle dependency licenses, CSP/API base URL handling, and absence of browser persistence for secrets. Critical UI findings block feature screens.

  **Group record:** no worker commit is assigned to the group heading. The coordinator records UI-01A/B/C hashes and reviews separately.

**Completion standard:** A production build renders the verified design system, four-phase horizontal timeline, accessible navigation, and profile/error status without page overflow or unrecorded design choices; later UI tasks have stable routes and tokens to consume.

### Task UI-01A: Build the Shell, Tokens, and Accessibility Base

**Goal:** Create the semantic application shell, verified design tokens, focus/contrast primitives, and route outlet using the G-01 evidence.

**Files:** Modify `frontend/src/app/App.tsx`; create `frontend/src/app/AppShell.tsx`, `frontend/src/app/routes.tsx`, `frontend/src/styles/tokens.css`, `frontend/src/styles/global.css`, `frontend/src/test/setup.ts`, and `frontend/src/app/AppShell.test.tsx`.

**Interfaces:** semantic header/nav/main/live status, profile/health state, stable route placeholders, no browser persistence of secrets, and only recorded Open Design tokens/components.

**Dependencies / parallelism:** Requires G-01 and API-01C. It owns global shell/token files and completes before UI-01B.

- [ ] **Red:** render landmark/focus/profile tests; run `npm --prefix frontend run test -- --run src/app/AppShell.test.tsx`. Expected: FAIL because the shell is absent.
- [ ] **Green/refactor:** implement shell/tokens/accessibility only; run the focused test, full frontend tests/build, and `python scripts/test_all.py`.
- [ ] **Reviews:** SPEC review AC-08, AC-09, AC-44; quality review actual G-01 evidence, contrast/focus, CSP/API base, dependency licenses, and no secret state. Critical findings block UI-01B.
- [ ] **Commit:** scan secrets; `git add -- frontend/src/app/App.tsx frontend/src/app/AppShell.tsx frontend/src/app/routes.tsx frontend/src/styles/tokens.css frontend/src/styles/global.css frontend/src/test/setup.ts frontend/src/app/AppShell.test.tsx`; run `git diff --cached --check`; commit with `git commit -m "feat(UI-01A): add shell tokens and accessibility base [agent: <fresh-agent-id>]"`.

**Completion standard:** A clean frontend build has accessible shell landmarks and recorded tokens with no unverified design choice.

### Task UI-01B: Add the Four-stage Timeline and Navigation

**Goal:** Add the stable X-axis `import -> understand -> practice -> review` timeline and keyboard navigation without changing global tokens.

**Files:** Create `frontend/src/components/PhaseTimeline.tsx` and `frontend/src/components/PhaseTimeline.test.tsx`; modify `frontend/src/app/routes.tsx` only through the UI-01A owner.

**Interfaces:** exactly four labelled phases, `aria-current`, keyboard focus, stable tracks at 320/390/1440 px, and no page-level horizontal overflow.

**Dependencies / parallelism:** Requires UI-01A. It owns the timeline component and completes before UI-01C.

- [ ] **Red:** assert four phases, labels/icons, active state, keyboard focus, and viewport layout; run `npm --prefix frontend run test -- --run src/components/PhaseTimeline.test.tsx`. Expected: FAIL because the timeline is absent.
- [ ] **Green/refactor:** implement the timeline/navigation only; run focused/full frontend tests, build, and `python scripts/test_all.py`.
- [ ] **Reviews:** SPEC review AC-08, AC-09, AC-44 and §4.2; quality review responsive track sizing, overflow, semantics, icon license, and no decorative/unverified assets. Critical findings block UI-01C.
- [ ] **Commit:** scan secrets; `git add -- frontend/src/components/PhaseTimeline.tsx frontend/src/components/PhaseTimeline.test.tsx frontend/src/app/routes.tsx`; run `git diff --cached --check`; commit with `git commit -m "feat(UI-01B): add four-stage timeline navigation [agent: <fresh-agent-id>]"`.

**Completion standard:** The four-stage timeline is deterministic, keyboard reachable, and visually stable at every required viewport.

### Task UI-01C: Add Responsive Loading, Error, and Empty States

**Goal:** Complete shell-level recoverable status, loading, empty, and error states without feature-specific logic.

**Files:** Create `frontend/src/components/StatusBanner.tsx`; modify `frontend/src/app/AppShell.tsx` and `frontend/src/app/routes.tsx`; add `frontend/src/components/StatusBanner.test.tsx`.

**Interfaces:** non-color-only profile/demo/error states, bounded text fitting, accessible live regions, and stable route placeholders consumed by UI-02B/UI-03C/UI-04B/UI-05B.

**Dependencies / parallelism:** Requires UI-01B and API-01C. Feature screens depend on this terminal shell unit.

- [ ] **Red:** assert loading/empty/error recovery, 320/390/1440 text fit, keyboard focus return, and no page overflow; run `npm --prefix frontend run test -- --run src/components/StatusBanner.test.tsx`. Expected: FAIL because status states are absent.
- [ ] **Green/refactor:** implement shell states only; run focused/full frontend tests, build, and `python scripts/test_all.py`.
- [ ] **Reviews:** SPEC review AC-08, AC-09, AC-44; quality review text overflow, aria-live/focus, untrusted error text, CSP, and bundle licenses. Critical findings block feature UI.
- [ ] **Commit:** scan secrets; `git add -- frontend/src/components/StatusBanner.tsx frontend/src/components/StatusBanner.test.tsx frontend/src/app/AppShell.tsx frontend/src/app/routes.tsx`; run `git diff --cached --check`; commit with `git commit -m "feat(UI-01C): add responsive shell states [agent: <fresh-agent-id>]"`.

**Completion standard:** All feature routes inherit accessible, responsive, recoverable shell states without duplicating global UI logic.

### Task Group UI-02 (not dispatchable): Import Onboarding and L/P/F Consent Flow

Planning group ID: UI-02 (not dispatchable; use UI-02A/UI-02B)

**Goal:** Implement the first-import workflow as an explicit metadata -> policy -> consent -> learning state machine. The UI must compare L/P/F fidelity, outbound scope, credentials/cost, and limits, never parse/upload silently, and end with the high-priority `开始学习` action and the visible `课程设置 › 材料与隐私` recovery path required by SPEC.

**Files:**
- Create: `frontend/src/features/import/ImportWizard.tsx`
- Create: `frontend/src/features/import/importApi.ts`
- Create: `frontend/src/features/import/importState.ts`
- Create: `frontend/src/features/import/PolicyComparison.tsx`
- Create: `frontend/src/features/import/ConsentSummary.tsx`
- Create: `frontend/src/features/import/ImportWizard.test.tsx`
- Create: `frontend/src/features/import/importState.test.ts`

**Interfaces:**
- `ImportState` is a discriminated union `metadata | policy | consent | ready | needs_user_review | failed`; transitions require the course/batch version and preserve per-file statuses.
- The wizard calls API-01A/API-01B `POST .../batches/inspect`, `POST .../policy`, `POST .../consent`, and `GET .../batches/{id}` through a typed client. File selection sends only bounded metadata/staging information to inspection; no parser or remote call is initiated by the browser before mode and exact file scope are confirmed.
- `PolicyComparison` renders L/P/F mode, fidelity, outbound files/pages, retention/policy snapshot summary, provider/credential/cost limits, and recovery for lower provider limits. `ConsentSummary` lists exact file IDs/hashes, mode, scope, profile fingerprint, and confirmation time; changing scope returns to a new consent step.
- The final action is labelled exactly `开始学习`; the settings link has higher visual weight than ordinary explanatory copy and leads to the materials/privacy settings route. Errors include a recovery action and never imply automatic mode switching.

**Dependencies / parallelism:** Group summary only. UI-02A requires UI-01C/API-01C; UI-02B requires UI-02A/API-01B. It may run beside UI-03 after the terminal shell contract, but shared import state is serially owned and must not duplicate API policy/consent logic. Use only design tokens/components selected by G-01.

- [ ] **Step 1: Write the minimum failing test**

  Add tests that select a bounded fixture, assert metadata inspection is called once with no parse/provider call, assert the Continue button is disabled before L/P/F selection, and assert changing the mode invalidates the old consent and returns to the consent step. Add a responsive render test for 320 px and 390 px.

  Run:

  ```powershell
  npm --prefix frontend run test -- --run src/features/import/ImportWizard.test.tsx src/features/import/importState.test.ts
  ```

  Expected: FAIL because the import feature and state machine are absent.

- [ ] **Step 2: Implement the smallest stateful wizard**

  Add typed API calls, guarded transitions, accessible mode controls, exact scope preview, loading/cancel/error states, and the final start-learning navigation. Keep selected file objects out of persistent browser storage; invalidate consent whenever file IDs, hashes, mode, profile, or policy fingerprint changes.

- [ ] **Step 3: Focused and full regression**

  Run:

  ```powershell
  npm --prefix frontend run test -- --run src/features/import/ImportWizard.test.tsx src/features/import/importState.test.ts
  npm --prefix frontend run test -- --run
  npm --prefix frontend run build
  python scripts/test_all.py
  ```

  Expected: focused tests and full build pass; no-body-before-policy, no-consent-egress, unsupported-role, needs-user-review, stale-consent, keyboard, and responsive cases remain green.

- [ ] **Step 4: SPEC compliance review and quality/security/license review**

  SPEC review must check AC-01, AC-02, AC-08, AC-09, AC-25, AC-28, AC-30, AC-33, AC-40, and AC-45. Quality/security/license review must check file-size/type/encoding display, no silent fallback, consent fingerprint invalidation, XSS-safe server text rendering, abort/timeout behavior, no secret persistence, and licenses for UI components/icons. Critical findings block demo onboarding.

  **Group record:** no worker commit is assigned to the group heading. The coordinator records UI-02A/B hashes and reviews separately.

**Completion standard:** At all required viewports a student can inspect metadata, compare L/P/F, explicitly authorize exact scope, recover from rejection, and begin learning; no parser/provider action or authoritative write occurs before the required policy and consent.

### Task UI-02A: Add Metadata Inspection and Import State Machine

**Goal:** Implement the metadata-first file selection state machine and bounded inspection client, stopping before policy/consent.

**Files:** Create `frontend/src/features/import/ImportWizard.tsx`, `frontend/src/features/import/importApi.ts`, `frontend/src/features/import/importState.ts`, and `frontend/src/features/import/importState.test.ts`.

**Interfaces:** discriminated `metadata | policy | consent | ready | needs_user_review | failed` state, per-file status preservation, typed API-01C client, no parser/provider call from browser, and no persistent selected-file bodies.

**Dependencies / parallelism:** Requires UI-01C and API-01C. It completes before UI-02B; shared import state files are serially owned.

- [ ] **Red:** assert bounded metadata selection, one inspection call, no parse/provider call, unsupported-role/needs-review states, and cancellation; run `npm --prefix frontend run test -- --run src/features/import/importState.test.ts`. Expected: FAIL because the state machine/client is absent.
- [ ] **Green/refactor:** implement metadata/state only; run focused/full frontend tests, build, and `python scripts/test_all.py`.
- [ ] **Reviews:** SPEC review AC-01, AC-03, AC-15, AC-33, AC-45; quality review file bounds, untrusted server text, abort behavior, and no browser persistence. Critical findings block UI-02B.
- [ ] **Commit:** scan secrets; `git add -- frontend/src/features/import/ImportWizard.tsx frontend/src/features/import/importApi.ts frontend/src/features/import/importState.ts frontend/src/features/import/importState.test.ts`; run `git diff --cached --check`; commit with `git commit -m "feat(UI-02A): add metadata import state [agent: <fresh-agent-id>]"`.

**Completion standard:** First import is visibly metadata-only and every file remains independently recoverable before a mode is chosen.

### Task UI-02B: Add L/P/F Policy, Consent, Start, and Recovery Screens

**Goal:** Complete explicit policy comparison, exact consent confirmation, recovery, and the emphasized `开始学习` action/settings path.

**Files:** Create `frontend/src/features/import/PolicyComparison.tsx`, `frontend/src/features/import/ConsentSummary.tsx`, and `frontend/src/features/import/ImportWizard.test.tsx`; modify `frontend/src/features/import/ImportWizard.tsx`, `frontend/src/features/import/importApi.ts`, and `frontend/src/features/import/importState.ts` through UI-02A ownership.

**Interfaces:** L/P/F fidelity/scope/retention/cost display, consent invalidation on file/hash/mode/profile/policy change, accessible recovery, exact `开始学习` label, and emphasized `课程设置 › 材料与隐私` link.

**Dependencies / parallelism:** Requires UI-02A and API-01B. UI-03 may consume the stable settings route after this unit.

- [ ] **Red:** assert Continue disabled before mode, old consent invalidated after scope change, policy/consent errors recover, final label/settings emphasis, and 320/390 responsive render; run `npm --prefix frontend run test -- --run src/features/import/ImportWizard.test.tsx`. Expected: FAIL because policy/consent screens are absent.
- [ ] **Green/refactor:** implement policy/consent/start/recovery only; run focused/full frontend tests, build, and `python scripts/test_all.py`.
- [ ] **Reviews:** SPEC review AC-01, AC-02, AC-08, AC-09, AC-25, AC-28, AC-30, AC-33, AC-40, AC-45; quality review no silent fallback, fingerprint invalidation, XSS-safe text, focus, and component licenses. Critical findings block demo onboarding.
- [ ] **Commit:** scan secrets; `git add -- frontend/src/features/import/PolicyComparison.tsx frontend/src/features/import/ConsentSummary.tsx frontend/src/features/import/ImportWizard.test.tsx frontend/src/features/import/ImportWizard.tsx frontend/src/features/import/importApi.ts frontend/src/features/import/importState.ts`; run `git diff --cached --check`; commit with `git commit -m "feat(UI-02B): add policy consent and start recovery [agent: <fresh-agent-id>]"`.

**Completion standard:** A student can compare and explicitly authorize exact scope, recover safely, and start learning while all pre-consent boundaries remain visible and enforced.

### Task Group UI-03 (not dispatchable): Source, Coverage, Privacy, and Credential Settings Screens

Planning group ID: UI-03 (not dispatchable; use UI-03A/UI-03B/UI-03C)

**Goal:** Make source traceability, candidate coverage confirmation, material/privacy controls, and credential lifecycle visible and safe. The screens must preserve the distinction between candidate and confirmed facts and make hidden credential entry/status/update/clear usable without exposing the value.

**Files:**
- Create: `frontend/src/features/materials/SourcePanel.tsx`
- Create: `frontend/src/features/materials/CoverageReview.tsx`
- Create: `frontend/src/features/materials/MaterialPrivacySettings.tsx`
- Create: `frontend/src/features/materials/materialsApi.ts`
- Create: `frontend/src/features/settings/CredentialSettings.tsx`
- Create: `frontend/src/features/settings/settingsApi.ts`
- Create: `frontend/src/features/materials/MaterialsSettings.test.tsx`
- Create: `frontend/src/features/settings/CredentialSettings.test.tsx`

**Interfaces:**
- `SourcePanel` renders only validated `SourceLocator` kinds (PDF page/region, image, text lines, manual entry), content-hash/version status, quality flags, and a stale/ambiguous `source_insufficient` state. It never guesses a page from a filename and never renders raw server HTML.
- `CoverageReview` consumes API-01C candidates/decisions, displays `added/reinforced/changed/unmapped/duplicate`, confidence, role, and source; it sends `expected_version` with decisions and disables plan-affecting actions until user confirmation.
- `MaterialPrivacySettings` reads/updates course policy, shows exact local/remote scope and provider policy snapshot, warns before widening, and surfaces deletion/`delete_incomplete` status without claiming success.
- `CredentialSettings` uses API-04A status/update/clear endpoints with `<input type="password">`, no value in React state beyond the submission boundary, no local/session storage, no clipboard/autofill copying, and explicit force-clear recovery text. Status exposes configured/unconfigured, timestamp, and redacted error code only.

**Dependencies / parallelism:** Group summary only. UI-03A requires UI-01C/API-01C; UI-03B requires UI-03A/API-01B; UI-03C requires UI-01C/API-04A and may run beside A/B. Shared tokens remain UI-01A-owned; no unit may implement a second credential store.

- [ ] **Step 1: Write the minimum failing test**

  Add tests asserting a stale locator renders `source_insufficient`, an unconfirmed coverage row cannot submit a plan-affecting decision, and a credential status/update/clear flow never renders the submitted value or stores it in `localStorage`/`sessionStorage`. Verify the privacy screen requires a new confirmation when outbound scope grows.

  Run:

  ```powershell
  npm --prefix frontend run test -- --run src/features/materials/MaterialsSettings.test.tsx src/features/settings/CredentialSettings.test.tsx
  ```

  Expected: FAIL because the source/settings features are absent.

- [ ] **Step 2: Implement the smallest screens**

  Add typed clients, optimistic version handling, safe locator links, candidate/confirmed affordances, privacy scope preview, hidden input/status/update/clear states, abort/error recovery, and accessible names/focus. Treat all server text as untrusted text and keep credentials out of analytics, query strings, state persistence, and logs.

- [ ] **Step 3: Focused and full regression**

  Run:

  ```powershell
  npm --prefix frontend run test -- --run src/features/materials/MaterialsSettings.test.tsx src/features/settings/CredentialSettings.test.tsx
  npm --prefix frontend run test -- --run
  npm --prefix frontend run build
  python scripts/test_all.py
  ```

  Expected: focused tests, full frontend regression/build, and the repository test command pass; source/coverage version conflicts, deletion-incomplete, invalid profile, and secret-scan fixtures remain redaction-safe.

- [ ] **Step 4: SPEC compliance review and quality/security/license review**

  SPEC review must check AC-03, AC-06, AC-07, AC-16, AC-17, AC-28, AC-30, AC-38, AC-39, AC-40, and AC-44. Quality/security/license review must check locator validation, optimistic concurrency, destructive-action confirmation, browser cache/autofill behavior, CSP/XSS, accessibility, redacted telemetry, and component/icon licenses. Critical findings block the learning loop UI.

  **Group record:** no worker commit is assigned to the group heading. The coordinator records UI-03A/B/C hashes and reviews separately.

**Completion standard:** A student can open a real source locator, review and confirm coverage, change privacy scope with explicit consent, and manage credentials through hidden/status/update/clear controls while stale sources, unconfirmed facts, and secrets remain safely bounded.

### Task UI-03A: Add Source and Coverage Review Screens

**Goal:** Render validated locators and candidate/confirmed coverage decisions without guessing or changing plan state.

**Files:** Create `frontend/src/features/materials/SourcePanel.tsx`, `frontend/src/features/materials/CoverageReview.tsx`, `frontend/src/features/materials/materialsApi.ts`, and the source/coverage portion of `frontend/src/features/materials/MaterialsSettings.test.tsx`.

**Interfaces:** PDF/image/text/manual locator display with hash/quality state, five coverage diff relations, expected-version decisions, and stale/ambiguous `source_insufficient` recovery.

**Dependencies / parallelism:** Requires UI-01C and API-01C. It completes before UI-03B; no credential or privacy implementation here.

- [ ] **Red:** assert stale locator, candidate/confirmed distinction, version conflict, and disabled plan-affecting action; run `npm --prefix frontend run test -- --run src/features/materials/MaterialsSettings.test.tsx`. Expected: FAIL because source/coverage screens are absent.
- [ ] **Green/refactor:** implement source/coverage only; run focused/full frontend tests, build, and `python scripts/test_all.py`.
- [ ] **Reviews:** SPEC review AC-03, AC-12, AC-13, AC-16, AC-17, AC-37; quality review locator trust, optimistic concurrency, XSS-safe text, accessibility, and component/icon licenses. Critical findings block UI-03B.
- [ ] **Commit:** scan secrets; `git add -- frontend/src/features/materials/SourcePanel.tsx frontend/src/features/materials/CoverageReview.tsx frontend/src/features/materials/materialsApi.ts frontend/src/features/materials/MaterialsSettings.test.tsx`; run `git diff --cached --check`; commit with `git commit -m "feat(UI-03A): add source and coverage review [agent: <fresh-agent-id>]"`.

**Completion standard:** Every displayed material fact is tied to a validated locator, and only explicit versioned user decisions can become authoritative.

### Task UI-03B: Add Material Privacy Scope and Deletion Settings

**Goal:** Make local/remote scope, policy snapshots, widening confirmation, and incomplete deletion recovery visible and safe.

**Files:** Create `frontend/src/features/materials/MaterialPrivacySettings.tsx`; extend `frontend/src/features/materials/MaterialsSettings.test.tsx`; modify `frontend/src/features/materials/materialsApi.ts` through UI-03A ownership.

**Interfaces:** exact L/P/F scope and provider policy display, re-confirmation on widening, deletion confirmation, and truthful `delete_incomplete`/recovery state.

**Dependencies / parallelism:** Requires UI-03A and API-01B/API-01C. Shared materials API files are serially owned; completes before QA-01.

- [ ] **Red:** assert widening requires new consent, deletion does not claim incomplete cleanup as success, and recovery action is accessible; run `npm --prefix frontend run test -- --run src/features/materials/MaterialsSettings.test.tsx`. Expected: FAIL because privacy screen is absent.
- [ ] **Green/refactor:** implement privacy/deletion only; run focused/full frontend tests, build, and `python scripts/test_all.py`.
- [ ] **Reviews:** SPEC review AC-25, AC-28, AC-30, AC-40; quality review destructive confirmation, redacted policy text, cache behavior, focus, and no local course-body persistence. Critical findings block QA-01.
- [ ] **Commit:** scan secrets; `git add -- frontend/src/features/materials/MaterialPrivacySettings.tsx frontend/src/features/materials/MaterialsSettings.test.tsx frontend/src/features/materials/materialsApi.ts`; run `git diff --cached --check`; commit with `git commit -m "feat(UI-03B): add material privacy settings [agent: <fresh-agent-id>]"`.

**Completion standard:** Users can see and change processing scope only through explicit confirmation, and deletion states remain truthful and recoverable.

### Task UI-03C: Add Hidden Credential Settings and Status

**Goal:** Provide hidden configure/status/update/clear controls with no credential value in browser state, storage, telemetry, or ordinary responses.

**Files:** Create `frontend/src/features/settings/CredentialSettings.tsx`, `frontend/src/features/settings/settingsApi.ts`, and `frontend/src/features/settings/CredentialSettings.test.tsx`.

**Interfaces:** password input bounded to submission, configured/unconfigured/timestamp/redacted error status, forced-clear recovery, and no clipboard/autofill/local/session storage.

**Dependencies / parallelism:** Requires UI-01C and API-04A. It may run beside UI-03A/B but owns settings files and must not add a credential store.

- [ ] **Red:** assert status/update/clear never render or persist the submitted value, no cache/storage/clipboard use, and forced clear exposes recovery; run `npm --prefix frontend run test -- --run src/features/settings/CredentialSettings.test.tsx`. Expected: FAIL because credential settings are absent.
- [ ] **Green/refactor:** implement hidden status/update/clear UI only; run focused/full frontend tests, build, and `python scripts/test_all.py`.
- [ ] **Reviews:** SPEC review AC-07, AC-11, AC-30, AC-31, AC-38, AC-39, AC-40; quality review password input behavior, cache/autofill, redaction, CSP, focus, and licenses. A suspected real credential stops the unit.
- [ ] **Commit:** scan secrets; `git add -- frontend/src/features/settings/CredentialSettings.tsx frontend/src/features/settings/settingsApi.ts frontend/src/features/settings/CredentialSettings.test.tsx`; run `git diff --cached --check`; commit with `git commit -m "feat(UI-03C): add hidden credential settings [agent: <fresh-agent-id>]"`.

**Completion standard:** Credential lifecycle is usable but the value is never retained or exposed outside the bounded submission boundary.

### Task Group UI-04 (not dispatchable): Learning Loop and Source-bound Explanation/Check UI

Planning group ID: UI-04 (not dispatchable; use UI-04A/UI-04B)

**Goal:** Render the first mutex/race-condition learning slice: source-bound explanation, at most three diagnostic probes, deterministic same-trajectory and transfer checks, feedback, and evidence status. The UI must make model supplements visibly distinct and never imply mastery from reading.

**Files:**
- Create: `frontend/src/features/learning/LearningLoop.tsx`
- Create: `frontend/src/features/learning/ExplanationPanel.tsx`
- Create: `frontend/src/features/learning/UnderstandingCheck.tsx`
- Create: `frontend/src/features/learning/learningApi.ts`
- Create: `frontend/src/features/learning/LearningLoop.test.tsx`
- Create: `frontend/src/features/learning/UnderstandingCheck.test.tsx`

**Interfaces:**
- `LearningLoop` loads API-02A learning state and starts an explanation with concept, goal, evidence IDs, validated locators, consent/mode, and idempotency key. It shows loading/cancel/failure states and keeps existing evidence/mastery unchanged on failure.
- `ExplanationPanel` renders source citations that open the SourcePanel, source quality/version, and a distinct `model_supplement` badge for general knowledge. It does not display a mastery claim or write a plan.
- `UnderstandingCheck` renders no more than three initial probes, accepts structured student responses, shows criterion-level oracle feedback (thread order, event completeness, terminal value, and safety invariant), and submits same-trajectory then transfer attempts through API-02B. Only a valid evaluator result creates evidence; later-session variation is required for `retained`.
- `learningApi.ts` uses the strict port/source/evidence envelope and maps `source_insufficient`, `provider_timeout`, `bad_schema`, `cancelled`, and `budget_exhausted` to recoverable UI states without interpolating untrusted HTML/Markdown.

**Dependencies / parallelism:** Group summary only. UI-04A requires UI-01C/UI-03A/API-02A/M2-02A; UI-04B requires UI-04A/API-02B/M2-02B. It can run beside UI-03/UI-05 after contracts stabilize, but must consume the shared SourceLocator/provider types and cannot add a second evaluator or mastery rule.

- [ ] **Step 1: Write the minimum failing test**

  Add tests asserting an explanation response displays citations/supplement labels but leaves mastery unknown, that a missing/stale locator shows `source_insufficient`, and that a successful deterministic check appends evidence only after the structured oracle result. Test provider wording variants and a failed/timeout response for unchanged state.

  Run:

  ```powershell
  npm --prefix frontend run test -- --run src/features/learning/LearningLoop.test.tsx src/features/learning/UnderstandingCheck.test.tsx
  ```

  Expected: FAIL because the learning feature and API client are absent.

- [ ] **Step 2: Implement the smallest learning flow**

  Add typed data loading, bounded probe/check forms, citation navigation, candidate/supplement badges, deterministic feedback rendering, cancellation, retry with the same idempotency key, and explicit evidence status. Keep answer text ephemeral and never send it to analytics or local storage.

- [ ] **Step 3: Focused and full regression**

  Run:

  ```powershell
  npm --prefix frontend run test -- --run src/features/learning/LearningLoop.test.tsx src/features/learning/UnderstandingCheck.test.tsx
  npm --prefix frontend run test -- --run
  npm --prefix frontend run build
  python scripts/test_all.py
  ```

  Expected: focused tests, full frontend/build, deterministic mock contract, locator, M2 oracle, and all repository tests pass; no UI path promotes a provider candidate or explanation view into authoritative mastery.

- [ ] **Step 4: SPEC compliance review and quality/security/license review**

  SPEC review must check AC-03, AC-04, AC-12, AC-13, AC-14, AC-21, AC-22, AC-23, AC-24, AC-32, and AC-34. Quality/security/license review must check answer/source text handling, XSS and markdown sanitization, cancellation/idempotency, keyboard interaction, visual distinction of supplements, evaluator ownership, and verified frontend dependency licenses.

  **Group record:** no worker commit is assigned to the group heading. The coordinator records UI-04A/B hashes and reviews separately.

**Completion standard:** The first learning slice is operable in the browser, shows where every material fact came from, limits probes, captures deterministic check evidence, and preserves unknown/mastery state across model failure or wording changes.

### Task UI-04A: Add Source-bound Explanation and Citation UI

**Goal:** Render explanation candidates with validated citations, visible supplement labels, cancellation, and failure recovery without claiming mastery.

**Files:** Create `frontend/src/features/learning/LearningLoop.tsx`, `frontend/src/features/learning/ExplanationPanel.tsx`, `frontend/src/features/learning/learningApi.ts`, and `frontend/src/features/learning/LearningLoop.test.tsx`.

**Interfaces:** source/evidence/consent/idempotency request envelope, citation navigation to SourcePanel, source quality/version, distinct `model_supplement`, and unchanged state on source/provider failure.

**Dependencies / parallelism:** Requires UI-01C, UI-03A, API-02A, and M2-02A. It completes before UI-04B.

- [ ] **Red:** assert citations/supplement labels, no mastery from viewing, stale-source recovery, timeout/cancel unchanged state, and wording invariance; run `npm --prefix frontend run test -- --run src/features/learning/LearningLoop.test.tsx`. Expected: FAIL because explanation UI is absent.
- [ ] **Green/refactor:** implement explanation/citation flow only; run focused/full frontend tests, build, and `python scripts/test_all.py`.
- [ ] **Reviews:** SPEC review AC-03, AC-12, AC-13, AC-21, AC-22, AC-32; quality review source text/XSS handling, cancellation/idempotency, supplement distinction, accessibility, and licenses. Critical findings block UI-04B.
- [ ] **Commit:** scan secrets; `git add -- frontend/src/features/learning/LearningLoop.tsx frontend/src/features/learning/ExplanationPanel.tsx frontend/src/features/learning/learningApi.ts frontend/src/features/learning/LearningLoop.test.tsx`; run `git diff --cached --check`; commit with `git commit -m "feat(UI-04A): add source-bound explanations [agent: <fresh-agent-id>]"`.

**Completion standard:** Explanations are source-traceable candidates with clear recovery/supplement status and zero authority over mastery.

### Task UI-04B: Add Deterministic Understanding Checks and Evidence UI

**Goal:** Complete bounded probes, same-trajectory/transfer checks, criterion feedback, and evidence display over the deterministic evaluator.

**Files:** Create `frontend/src/features/learning/UnderstandingCheck.tsx` and `frontend/src/features/learning/UnderstandingCheck.test.tsx`; modify `frontend/src/features/learning/LearningLoop.tsx` and `frontend/src/features/learning/learningApi.ts` through UI-04A ownership.

**Interfaces:** no more than three initial probes, structured answers, thread/event/value/invariant feedback, evidence only after valid evaluator result, and ephemeral answer text.

**Dependencies / parallelism:** Requires UI-04A and API-02B/M2-02B. QA-01A depends on this terminal learning unit.

- [ ] **Red:** assert probe limit, structured oracle feedback, no evidence on failed/malformed result, evidence after valid check, transfer ordering, and no answer persistence; run `npm --prefix frontend run test -- --run src/features/learning/UnderstandingCheck.test.tsx`. Expected: FAIL because check UI is absent.
- [ ] **Green/refactor:** implement checks/evidence only; run focused/full frontend tests, build, and `python scripts/test_all.py`.
- [ ] **Reviews:** SPEC review AC-04, AC-14, AC-23, AC-24, AC-34; quality review evaluator ownership, answer/log redaction, keyboard forms, retries/idempotency, and no client mastery rule. Critical findings block QA-01.
- [ ] **Commit:** scan secrets; `git add -- frontend/src/features/learning/UnderstandingCheck.tsx frontend/src/features/learning/UnderstandingCheck.test.tsx frontend/src/features/learning/LearningLoop.tsx frontend/src/features/learning/learningApi.ts`; run `git diff --cached --check`; commit with `git commit -m "feat(UI-04B): add deterministic learning checks [agent: <fresh-agent-id>]"`.

**Completion standard:** The browser records evidence only from the deterministic oracle and keeps student answers ephemeral across every failure/retry state.

### Task Group UI-05 (not dispatchable): Review Dashboard, Revisions, Finals, and Post-exam UI

Planning group ID: UI-05 (not dispatchable; use UI-05A/UI-05B)

**Goal:** Make deterministic review planning understandable and reversible. The dashboard must show task reasons, evidence, policy/default provenance, capacity, revisions/diffs/undo, explicit finals entry, and the exact post-exam pause behavior.

**Files:**
- Create: `frontend/src/features/review/ReviewDashboard.tsx`
- Create: `frontend/src/features/review/PlanRevisionDiff.tsx`
- Create: `frontend/src/features/review/FinalsModePanel.tsx`
- Create: `frontend/src/features/review/PostExamPaused.tsx`
- Create: `frontend/src/features/review/reviewApi.ts`
- Create: `frontend/src/features/review/ReviewDashboard.test.tsx`
- Create: `frontend/src/features/review/FinalsModePanel.test.tsx`

**Interfaces:**
- `ReviewDashboard` consumes API-03 plan/task data and displays concept, due local date, estimated minutes, evidence, reason codes, capacity overflow, policy version, and whether budget came from the user or the 30/90-minute default. It never reorders tasks client-side.
- `PlanRevisionDiff` shows added/reinforced/deferred/replaced future tasks, source/evidence reasons, revision IDs, and an accessible undo action that calls `POST .../revisions/{id}/revert`; started/completed tasks and old evidence remain visibly immutable.
- `FinalsModePanel` accepts a local exam date/timezone and budget, keeps the mode `continuous` until the user presses an explicit Enter finals action, shows confirmed teacher-focus/past-paper mappings and confidence, and explains every priority reason. It does not call provider endpoints directly.
- `PostExamPaused` renders only when `today_local > target_local_date`, shows archived finals state and zero future tasks, and asks for a new goal without automatically re-entering finals. Date edits/exit only affect future tasks.

**Dependencies / parallelism:** Group summary only. UI-05A requires UI-01C/API-03A/M3-02C; UI-05B requires UI-05A/API-03B/API-03C/M3-02C/M3-03. It may run beside UI-04, but consumes the M3 pure-planner response and cannot implement local priority math, hidden weights, or a second revision store. Shared timeline/tokens remain UI-01A-owned.

- [ ] **Step 1: Write the minimum failing test**

  Add tests for (a) date entry without explicit action remaining `continuous`, (b) explicit finals entry rendering policy/reason codes, (c) budget validation at 10/480 and five-minute steps, (d) undo creating a new revision rather than deleting history, and (e) an expired target rendering `post_exam_paused` with zero future tasks.

  Run:

  ```powershell
  npm --prefix frontend run test -- --run src/features/review/ReviewDashboard.test.tsx src/features/review/FinalsModePanel.test.tsx
  ```

  Expected: FAIL because review/finals components and the API client are absent.

- [ ] **Step 2: Implement the smallest review UI**

  Add typed API calls, deterministic server-order rendering, budget/date/timezone controls with accessible validation, revision diff/undo confirmation, explicit finals transition, candidate mapping confirmation, and post-exam pause/new-goal states. Keep all reasons and policy/default labels visible and do not hide capacity overflow.

- [ ] **Step 3: Focused and full regression**

  Run:

  ```powershell
  npm --prefix frontend run test -- --run src/features/review/ReviewDashboard.test.tsx src/features/review/FinalsModePanel.test.tsx
  npm --prefix frontend run test -- --run
  npm --prefix frontend run build
  python scripts/test_all.py
  ```

  Expected: focused tests, full frontend/build, M3 golden fixtures, API concurrency, and repository regression pass; repeated server inputs render identical order/reasons and no client mutation can alter authoritative due dates.

- [ ] **Step 4: SPEC compliance review and quality/security/license review**

  SPEC review must check AC-05, AC-08, AC-09, AC-16, AC-17, AC-18, AC-19, AC-34, AC-35, AC-36, and AC-44. Quality/security/license review must check date/DST display, numeric input bounds, undo semantics, candidate/confirmed distinction, accessible dialogs/focus, XSS-safe reason text, and frontend dependency licenses.

  **Group record:** no worker commit is assigned to the group heading. The coordinator records UI-05A/B hashes and reviews separately.

**Completion standard:** The browser presents a deterministic, source/evidence-linked review plan with visible policy and reasons, reversible future revisions, explicit finals mode, and truthful post-exam pause behavior at all required viewports.

### Task UI-05A: Add Review Dashboard and Revision Diff/Undo

**Goal:** Render server-ordered review tasks, visible policy/default/reasons/capacity, and append-only revision diff/undo without client priority math.

**Files:** Create `frontend/src/features/review/ReviewDashboard.tsx`, `frontend/src/features/review/PlanRevisionDiff.tsx`, `frontend/src/features/review/reviewApi.ts`, and `frontend/src/features/review/ReviewDashboard.test.tsx`.

**Interfaces:** plan/task listing, reason/evidence/policy/default provenance, capacity overflow, revision diff, and accessible undo that creates a new revision.

**Dependencies / parallelism:** Requires UI-01C and API-03A/M3-02C. It completes before UI-05B.

- [ ] **Red:** assert server order, visible reasons/default source/capacity, immutable started/completed tasks, and append-only undo; run `npm --prefix frontend run test -- --run src/features/review/ReviewDashboard.test.tsx`. Expected: FAIL because dashboard/revision UI is absent.
- [ ] **Green/refactor:** implement dashboard/revision UI only; run focused/full frontend tests, build, and `python scripts/test_all.py`.
- [ ] **Reviews:** SPEC review AC-05, AC-16, AC-17, AC-18, AC-34, AC-35; quality review no client sorting/weights, optimistic conflicts, XSS-safe reasons, dialog/focus, and licenses. Critical findings block UI-05B.
- [ ] **Commit:** scan secrets; `git add -- frontend/src/features/review/ReviewDashboard.tsx frontend/src/features/review/PlanRevisionDiff.tsx frontend/src/features/review/reviewApi.ts frontend/src/features/review/ReviewDashboard.test.tsx`; run `git diff --cached --check`; commit with `git commit -m "feat(UI-05A): add review dashboard and revision diff [agent: <fresh-agent-id>]"`.

**Completion standard:** Review tasks and revisions are explainable, server-deterministic, and undoable without erasing history.

### Task UI-05B: Add Finals and Post-exam UI

**Goal:** Render date/timezone/budget controls, explicit finals entry, confirmed focus mappings, exam-day state, and truthful post-exam pause/new-goal recovery.

**Files:** Create `frontend/src/features/review/FinalsModePanel.tsx`, `frontend/src/features/review/PostExamPaused.tsx`, and `frontend/src/features/review/FinalsModePanel.test.tsx`; modify `frontend/src/features/review/reviewApi.ts` through UI-05A ownership.

**Interfaces:** date entry remains continuous until explicit action, budget 10--480 in five-minute steps, future-only exit/change semantics, and pause only when today is after target.

**Dependencies / parallelism:** Requires UI-05A, API-03B/API-03C, M3-02C, and M3-03. QA-01A depends on this terminal review unit.

- [ ] **Red:** assert date-only continuous mode, explicit finals, boundary budget validation, confirmed mapping distinction, exam-day learning, and after-date pause/zero future tasks; run `npm --prefix frontend run test -- --run src/features/review/FinalsModePanel.test.tsx`. Expected: FAIL because finals/post-exam UI is absent.
- [ ] **Green/refactor:** implement finals/post-exam only; run focused/full frontend tests, build, and `python scripts/test_all.py`.
- [ ] **Reviews:** SPEC review AC-05, AC-08, AC-09, AC-18, AC-19, AC-34, AC-35, AC-36, AC-44; quality review date/DST display, numeric bounds, candidate/confirmed distinction, focus, and no provider/client priority authority. Critical findings block QA-01.
- [ ] **Commit:** scan secrets; `git add -- frontend/src/features/review/FinalsModePanel.tsx frontend/src/features/review/PostExamPaused.tsx frontend/src/features/review/FinalsModePanel.test.tsx frontend/src/features/review/reviewApi.ts`; run `git diff --cached --check`; commit with `git commit -m "feat(UI-05B): add finals and post-exam UI [agent: <fresh-agent-id>]"`.

**Completion standard:** Finals mode is explicit and explainable, exam-day behavior remains active, and post-exam pause never appears early or silently creates a new goal.

### Task Group DEMO-01 (not dispatchable): Isolated Ephemeral Demo Profile, Fixtures, Quotas, and Mock Enforcement

Planning group ID: DEMO-01 (not dispatchable; use DEMO-01A/DEMO-01B/DEMO-01C)

**Goal:** Deliver a runnable public-demo profile that exercises import, coverage confirmation, learning checks, plan revision/undo, and post-exam pause using only built-in synthetic or explicitly licensed fixtures and deterministic mock responses. It must fail closed for uploads, credentials, real provider egress, cross-session reads, and quota violations.

**Files:**
- Create: `backend/src/projectb/application/demo.py`
- Create: `backend/src/projectb/api/routes/demo.py`
- Create: `backend/tests/integration/test_demo_profile.py`
- Create: `backend/tests/integration/test_demo_isolation.py`
- Create: `backend/tests/integration/test_demo_quotas.py`
- Create: `demo/profile.json`
- Create: `demo/fixtures/course_os.json`
- Create: `demo/fixtures/materials.json`
- Create: `frontend/src/features/demo/DemoNotice.tsx`
- Create: `frontend/src/features/demo/DemoNotice.test.tsx`
- Modify: `backend/src/projectb/api/routes/__init__.py` only through the API route owner to register the demo router

**Interfaces:**
- `DemoSessionManager.create() -> DemoSession`, `get(session_id)`, `reset(session_id)`, and `sweep(now)` issue random opaque session IDs, bind one active course, and enforce 30-minute inactivity and two-hour absolute lifetime. State is in-memory/ephemeral and may be discarded on restart.
- `DemoQuotaPolicy` enforces at most one active course, 20 built-in materials, two concurrent jobs, 64 MiB temporary state, and 60 requests/minute/IP. It returns recoverable quota errors and never shares a writable fixed owner across browsers.
- `GET /api/demo/profile` returns a non-secret banner/profile contract; `POST /api/demo/session/reset` clears only the caller's session. Demo routes accept fixture IDs from `demo/profile.json`, reject arbitrary upload/path/URL/credential fields, and expose the same API-01C/02/03 domain contracts.
- The demo provider registry contains only the deterministic mock; attempts to resolve a credential, open a network socket, register OpenAI, or select an arbitrary adapter return `demo_forbidden`. `DemoNotice` continuously labels “demo data/simulated model” and never implies a real OpenAI call.
- Fixture files contain synthetic/licensed metadata and source locators only; the task must record source/license evidence for every non-original asset and must not copy the private OS PDFs.

**Dependencies / parallelism:** Group summary only. DEMO-01A requires API-01C/T-07/UI-01C; DEMO-01B requires DEMO-01A/API-02B/API-03C/T-07; DEMO-01C requires DEMO-01B/UI-01C. Route registration and shared provider registry changes are serialized. DIST-02 consumes DEMO-01C and may not add a second demo implementation.

- [ ] **Step 1: Write the minimum failing test**

  Add tests creating two sessions and asserting session A cannot read/reset session B, an arbitrary upload/credential/provider request is rejected, the fourth concurrent job is rejected, and expiry removes state. Add a mock-call assertion proving demo processing never opens a network socket.

  Run:

  ```powershell
  python -m pytest backend/tests/integration/test_demo_profile.py backend/tests/integration/test_demo_isolation.py backend/tests/integration/test_demo_quotas.py -q
  ```

  Expected: FAIL because the demo profile, session manager, fixtures, and route are absent.

- [ ] **Step 2: Implement the smallest isolated profile**

  Load and validate an allowlisted fixture manifest, generate opaque expiring sessions, enforce quotas/rate limits before application work, route all AI calls to the deterministic mock, and return profile markers. Keep state in a bounded ephemeral store, scrub it on reset/expiry, and reject sensitive fields with generic recoverable errors. Add the browser notice without persisting session contents.

- [ ] **Step 3: Focused and full regression**

  Run:

  ```powershell
  python -m pytest backend/tests/integration/test_demo_profile.py backend/tests/integration/test_demo_isolation.py backend/tests/integration/test_demo_quotas.py -q
  npm --prefix frontend run test -- --run src/features/demo/DemoNotice.test.tsx
  python -m pytest backend/tests -q
  python scripts/test_all.py
  ```

  Expected: focused demo/browser-notice tests and full regression pass; fixture license scan, cross-session access, TTL, quota, reset, no-egress, no-credential, and deterministic mock checks all pass.

- [ ] **Step 4: SPEC compliance review and quality/security/license review**

  SPEC review must check AC-23, AC-24, AC-25, AC-41, and AC-47 plus every confirmed session/fixture/quota rule in §4.5. Quality/security/license review must check cryptographic session opacity, timing/rate-limit behavior, memory bounds, reset races, no network/credential capability, fixture provenance/license records, and container-safe configuration. Critical findings block DIST-02 and public deployment.

  **Group record:** no worker commit is assigned to this heading. The coordinator records DEMO-01A/B/C hashes and reviews separately.

**Completion standard:** A clean demo profile can run the complete core workflow with allowlisted fixtures and mock-only AI, while upload, credential, provider egress, cross-session reads, persistence, and quota bypasses are demonstrably impossible.

### Task DEMO-01A: Add Ephemeral Sessions, Quotas, and Licensed Fixtures

**Goal:** Implement bounded in-memory sessions, isolation, expiry/reset, quotas, and an allowlisted synthetic/licensed fixture manifest without routes/provider wiring.

**Files:** Create `backend/src/projectb/application/demo.py`, `backend/tests/integration/test_demo_isolation.py`, `backend/tests/integration/test_demo_quotas.py`, `demo/profile.json`, `demo/fixtures/course_os.json`, and `demo/fixtures/materials.json`.

**Interfaces:** opaque session create/get/reset/sweep, one-course/twenty-material/two-job/64-MiB/60-rpm limits, 30-minute inactivity/two-hour absolute expiry, and fixture provenance/license records.

**Dependencies / parallelism:** Requires API-01C, T-07, and UI-01C contracts. It completes before DEMO-01B.

- [ ] **Red:** assert cross-session denial, reset isolation, inactivity/absolute expiry, quota/rate limits, and arbitrary fixture/path rejection; run `python -m pytest backend/tests/integration/test_demo_isolation.py backend/tests/integration/test_demo_quotas.py -q`. Expected: FAIL because session/quota/fixtures are absent.
- [ ] **Green/refactor:** implement session/quota/fixture loading only; run focused/backend tests and `python scripts/test_all.py`.
- [ ] **Reviews:** SPEC review AC-10, AC-41, AC-47; quality review cryptographic opacity, clock/rate-limit races, memory bounds, fixture provenance/licenses, and no private PDF content. Critical findings block DEMO-01B.
- [ ] **Commit:** scan secrets; `git add -- backend/src/projectb/application/demo.py backend/tests/integration/test_demo_isolation.py backend/tests/integration/test_demo_quotas.py demo/profile.json demo/fixtures/course_os.json demo/fixtures/materials.json`; run `git diff --cached --check`; commit with `git commit -m "feat(DEMO-01A): add ephemeral sessions quotas and fixtures [agent: <fresh-agent-id>]"`.

**Completion standard:** Two browsers cannot share demo state, limits fail closed, expiry/reset clears state, and every fixture is synthetic or explicitly licensed.

### Task DEMO-01B: Add Mock-only Demo API and Provider Isolation

**Goal:** Expose the core API contracts to demo sessions while making uploads, credentials, arbitrary adapters, network egress, and persistence impossible.

**Files:** Create `backend/src/projectb/api/routes/demo.py` and `backend/tests/integration/test_demo_profile.py`; modify `backend/src/projectb/api/routes/__init__.py` and `backend/src/projectb/application/demo.py` through the API/demo owners. Use the public T-07 registration interface without modifying its production registry files.

**Interfaces:** demo profile/reset routes, fixture-ID-only inputs, same API-01C/API-02B/API-03C contracts, deterministic mock-only registry, and `demo_forbidden` for sensitive capabilities.

**Dependencies / parallelism:** Requires DEMO-01A, API-02B, API-03C, and T-07. It completes before DEMO-01C; registry/route edits are serialized.

- [ ] **Red:** assert arbitrary upload/URL/path/credential/provider rejected, mock-only calls deterministic, socket open denied, sessions owner-scoped, and quotas enforced before work; run `python -m pytest backend/tests/integration/test_demo_profile.py -q`. Expected: FAIL because demo routes/provider profile are absent.
- [ ] **Green/refactor:** implement mock-only routes/profile; run focused/API/backend tests and `python scripts/test_all.py`.
- [ ] **Reviews:** SPEC review AC-23, AC-24, AC-25, AC-41, AC-47; quality review no network/credential capability, route isolation, registry fail-closed behavior, redaction, and fixture-only inputs. Critical findings block DEMO-01C.
- [ ] **Commit:** scan secrets; `git add -- backend/src/projectb/api/routes/demo.py backend/src/projectb/api/routes/__init__.py backend/tests/integration/test_demo_profile.py backend/src/projectb/application/demo.py`; run `git diff --cached --check`; commit with `git commit -m "feat(DEMO-01B): add mock-only demo API [agent: <fresh-agent-id>]"`. A required production-registry edit blocks this unit and returns to the T-07 owner.

**Completion standard:** Demo API runs the real domain contracts with deterministic mock data and has no upload, credential, egress, arbitrary-adapter, or private-persistence capability.

### Task DEMO-01C: Add Demo Notice and Full Workflow Integration

**Goal:** Add the persistent demo marker and verify the fixture-driven import-to-review workflow through the UI/API without mixing local/private semantics.

**Files:** Create `frontend/src/features/demo/DemoNotice.tsx`, `frontend/src/features/demo/DemoNotice.test.tsx`, and `backend/tests/integration/test_demo_workflow.py`; modify `frontend/src/app/AppShell.tsx` through UI-01C ownership.

**Interfaces:** continuously visible demo-data/simulated-model notice, session reset/recovery, and one fixture-driven core workflow using the same typed contracts.

**Dependencies / parallelism:** Requires DEMO-01B and UI-01C. QA-01A/DIST-02 consume this terminal unit.

- [ ] **Red:** assert marker visible on all demo routes, no real-provider implication, reset clears only caller state, and fixture workflow reaches coverage/learning/revision; run `npm --prefix frontend run test -- --run src/features/demo/DemoNotice.test.tsx` and `python -m pytest backend/tests/integration/test_demo_workflow.py -q`. Expected: FAIL because notice/integration are absent.
- [ ] **Green/refactor:** implement notice/integration only; run focused frontend/backend, full build, and `python scripts/test_all.py`.
- [ ] **Reviews:** SPEC review AC-08, AC-09, AC-23, AC-41, AC-44, AC-47; quality review clear simulation copy, session reset races, frontend state, XSS/accessibility, and no sensitive fields. Critical findings block QA/distribution.
- [ ] **Commit:** scan secrets; `git add -- frontend/src/features/demo/DemoNotice.tsx frontend/src/features/demo/DemoNotice.test.tsx frontend/src/app/AppShell.tsx backend/tests/integration/test_demo_workflow.py`; run `git diff --cached --check`; commit with `git commit -m "feat(DEMO-01C): add demo notice and workflow [agent: <fresh-agent-id>]"`.

**Completion standard:** The complete mock demo is clearly labelled, isolated, resettable, and exercises the core workflow without any private/real-provider capability.

### Task Group QA-01 (not dispatchable): Browser E2E, Responsive/Accessibility, Security, and Fixture-Matrix Evidence

Planning group ID: QA-01 (not dispatchable; use QA-01A/QA-01B/QA-01C)

**Goal:** Verify the user-visible workflows and security boundaries in a real browser across the AC-08 viewports, with deterministic local/demo fixtures and no private course material or real credentials. The suite must cover import through post-exam pause, accessibility, no-egress/no-secret behavior, and the full M1 input contract matrix.

**Files:**
- Create: `frontend/playwright.config.ts`
- Create: `frontend/tests/e2e/import_learning.spec.ts`
- Create: `frontend/tests/e2e/review_finals.spec.ts`
- Create: `frontend/tests/e2e/accessibility.spec.ts`
- Create: `frontend/tests/e2e/security_demo.spec.ts`
- Create: `backend/tests/integration/test_input_fixture_matrix.py`
- Create: `frontend/tests/e2e/fixtures/synthetic-materials.json`
- Create: `artifacts/qa/.gitkeep` (reports/screenshots are generated and ignored; no real course files)

**Interfaces:**
- Playwright starts the local test profile or demo profile through a documented web-server command, uses accessible roles/labels rather than implementation selectors, and records console/network events for assertions. Tests cover 320 px, 390 x 844, and 1440 x 900, all four horizontal timeline phases, keyboard/focus, import policy/consent, source/coverage, learning checks, review revisions, finals entry, and post-exam pause.
- `security_demo.spec.ts` asserts hostile Host/Origin/CSRF responses, no request contains a credential/body/path where forbidden, demo upload and provider egress are rejected, sessions are isolated, and the demo marker is visible. It never configures a real key or calls an external provider.
- `test_input_fixture_matrix.py` parameterizes PDF/image/text/manual fixtures for extension/MIME/magic, encoding, size/pages/pixels/text length, empty/corrupt/encrypted/disguised files, role allowlist, duplicate hashes, and suspected-leak `needs_user_review`; it asserts unauthorized body parsing/network calls/authoritative writes are zero.
- Playwright output is stored under `artifacts/qa` with redacted traces and screenshots; reports must not contain user answer text, coursebody text, absolute private paths, or credentials.

**Dependencies / parallelism:** Group summary only. QA-01A requires UI-02B/UI-03B/UI-03C/UI-04B/UI-05B/DEMO-01C; QA-01B requires QA-01A/T-04/API-04B; QA-01C requires QA-01B/M1-01/M1-02. E2E specs can be written in parallel by scenario, but the Playwright config, fixture manifest, and artifact policy have one QA owner. This group is verification-only unless a failing test identifies a separately reviewed product defect.

- [ ] **Step 1: Write the minimum failing test**

  Add the import smoke spec and run it against the test profile:

  ```powershell
  npm --prefix frontend exec playwright test frontend/tests/e2e/import_learning.spec.ts --project=chromium
  ```

  Expected: FAIL because the Playwright config/spec and browser route are not present; preserve the first failure output as QA evidence rather than weakening the assertion.

- [ ] **Step 2: Implement the smallest evidence suite**

  Add deterministic server startup/teardown, viewport projects, accessible selectors, network/console redaction hooks, fixture seeding, axe or the verified accessibility equivalent, and the M1 parameter matrix. Use stable test IDs only where an accessible role cannot express the contract. Keep generated artifacts outside source control and scrub them before commit.

- [ ] **Step 3: Focused and full regression**

  Run:

  ```powershell
  npm --prefix frontend exec playwright test frontend/tests/e2e/import_learning.spec.ts --project=chromium
  npm --prefix frontend exec playwright test frontend/tests/e2e --project=chromium
  python -m pytest backend/tests/integration/test_input_fixture_matrix.py -q
  python scripts/test_all.py
  ```

  Expected: focused and full browser suites, fixture matrix, and repository test entry pass at all three viewports; accessibility violations, page overflow, unsafe network calls, cross-session reads, and secret/body findings are zero. Record browser/OS/version, command, timestamps, and artifact paths.

- [ ] **Step 4: SPEC compliance review and quality/security/license review**

  SPEC review must check AC-01, AC-02, AC-03, AC-08, AC-09, AC-11, AC-18, AC-19, AC-20, AC-25, AC-33, AC-37, AC-40, AC-41, AC-44, AC-45, and AC-47. Quality/security/license review must check test isolation, selector robustness, trace/screenshot redaction, browser permission/network policy, accessibility evidence, fixture provenance, and Playwright/axe licenses. Any flaky or skipped scenario is a Critical gap until resolved or explicitly documented as unexecuted.

  **Group record:** no worker commit is assigned to this heading. The coordinator records QA-01A/B/C hashes and reviews separately.

**Completion standard:** Reproducible browser and fixture evidence covers the complete local/demo workflow, required responsive/accessibility states, hostile request boundaries, and every M1 input limit without private material, real credentials, or fabricated pass evidence.

### Task QA-01A: Add Core Browser Workflow and Responsive Evidence

**Goal:** Verify the complete local/mock-demo workflow and layout at 320 px, 390 x 844, and 1440 x 900 using accessible selectors.

**Files:** Create `frontend/playwright.config.ts`, `frontend/e2e/core_workflow.spec.ts`, `frontend/e2e/responsive.spec.ts`, and `docs/engineering/QA-01A_EVIDENCE.md`.

**Interfaces:** documented web-server startup, import/policy/consent, source/coverage, learning checks, review/revision/finals/post-exam, four-phase timeline, console/network capture, and redacted artifacts.

**Dependencies / parallelism:** Requires UI-02B/UI-03B/UI-03C/UI-04B/UI-05B and DEMO-01C. It completes before QA-01B.

- [ ] **Red:** add the first workflow/responsive specs and run `npm --prefix frontend run e2e -- core_workflow.spec.ts responsive.spec.ts`; expected FAIL before the configured server/spec support exists.
- [ ] **Green/refactor:** make only test harness/fixture adjustments, run focused E2E at all viewports, frontend tests/build, and `python scripts/test_all.py`; product defects go to their owner task.
- [ ] **Reviews:** SPEC review AC-01 through AC-19 plus AC-34--36/44 as exercised; quality review selectors, deterministic waits, artifact redaction, viewport overflow/text fit, and no external network. Critical findings block QA-01B.
- [ ] **Commit:** scan secrets; `git add -- frontend/playwright.config.ts frontend/e2e/core_workflow.spec.ts frontend/e2e/responsive.spec.ts docs/engineering/QA-01A_EVIDENCE.md`; run `git diff --cached --check`; commit with `git commit -m "test(QA-01A): add browser workflow and responsive evidence [agent: <fresh-agent-id>]"`.

**Completion standard:** The full supported workflow passes reproducibly at all required viewports with redacted artifacts and no private/provider dependency.

### Task QA-01B: Add Accessibility and Security Browser Evidence

**Goal:** Verify keyboard/focus/landmarks/contrast states and hostile Host/Origin/CSRF/demo-isolation boundaries in the browser.

**Files:** Create `frontend/e2e/accessibility.spec.ts`, `frontend/e2e/security_demo.spec.ts`, and `docs/engineering/QA-01B_EVIDENCE.md`.

**Interfaces:** keyboard-only flow, focus restoration, non-color status, accessible dialogs/forms, hostile request assertions, demo no-upload/no-egress/no-credential, and cross-session isolation.

**Dependencies / parallelism:** Requires QA-01A, T-04, and API-04B. It completes before QA-01C.

- [ ] **Red:** run `npm --prefix frontend run e2e -- accessibility.spec.ts security_demo.spec.ts`; expected FAIL until the new assertions/specs exist or expose a real product defect.
- [ ] **Green/refactor:** add verification harness only, route product failures to owning units, then run focused E2E, frontend tests/build, and `python scripts/test_all.py`.
- [ ] **Reviews:** SPEC review AC-07--11, AC-30, AC-40, AC-41, AC-44, AC-47; quality review keyboard/focus/contrast tooling, hostile-request fidelity, session isolation, trace redaction, and no scanner weakening. Critical findings block QA-01C.
- [ ] **Commit:** scan secrets; `git add -- frontend/e2e/accessibility.spec.ts frontend/e2e/security_demo.spec.ts docs/engineering/QA-01B_EVIDENCE.md`; run `git diff --cached --check`; commit with `git commit -m "test(QA-01B): add accessibility and security evidence [agent: <fresh-agent-id>]"`.

**Completion standard:** Browser evidence proves accessible operation and fail-closed local/demo security boundaries without suppressing real defects.

### Task QA-01C: Add Input Fixture and Artifact-redaction Matrix

**Goal:** Exhaust every M1 input/role/size/encoding/corruption boundary and prove QA artifacts contain no secret, answer, private path, or course body.

**Files:** Create `backend/tests/integration/test_input_fixture_matrix.py`, `backend/tests/fixtures/input_matrix/README.md`, `backend/tests/fixtures/input_matrix/manifest.json`, `backend/tests/fixtures/input_matrix/build_fixtures.py`, `scripts/check_artifact_redaction.py`, and `docs/engineering/QA-01C_EVIDENCE.md`. Generated binary/text cases live only in each test's temporary directory and are not committed.

**Interfaces:** synthetic/licensed fixture matrix for PDF/image/text/manual types, limits, MIME/magic/encoding, empty/corrupt/encrypted/disguised/duplicate/role cases, and redaction scan over QA artifacts.

**Dependencies / parallelism:** Requires QA-01B, M1-01, and M1-02. DIST-01/CI-01 consume this terminal QA unit.

- [ ] **Red:** run `python -m pytest backend/tests/integration/test_input_fixture_matrix.py -q` and `python scripts/check_artifact_redaction.py artifacts/qa`; expected FAIL because fixture matrix/scanner are absent.
- [ ] **Green/refactor:** add a deterministic manifest/generator for synthetic fixtures and verifier logic, generate cases only under the test temporary directory, then run focused matrix/redaction, backend tests, and `python scripts/test_all.py`.
- [ ] **Reviews:** SPEC review AC-01, AC-03, AC-15, AC-16, AC-33, AC-45, AC-46; quality review fixture provenance, resource bounds, parser/provider spy counts, scanner false-positive/negative fixtures, and output redaction. Critical findings block distribution.
- [ ] **Commit:** scan secrets; `git add -- backend/tests/integration/test_input_fixture_matrix.py backend/tests/fixtures/input_matrix/README.md backend/tests/fixtures/input_matrix/manifest.json backend/tests/fixtures/input_matrix/build_fixtures.py scripts/check_artifact_redaction.py docs/engineering/QA-01C_EVIDENCE.md`; run `git diff --cached --check`; commit with `git commit -m "test(QA-01C): add input and artifact matrix [agent: <fresh-agent-id>]"`. Generated fixture outputs are never staged.

**Completion standard:** Every accepted/rejected M1 boundary is deterministic with zero unauthorized parse/provider/write calls, and all QA artifacts pass redaction.

### Task Group QA-02 (not dispatchable): Performance, Cancellation, Restart Recovery, and Private Benchmark Boundaries

Planning group ID: QA-02 (not dispatchable; use QA-02A/QA-02B/QA-02C)

**Goal:** Produce reproducible evidence for local SLOs, long-job progress/cancellation, process restart recovery, idempotency, and the private real-sample benchmark contract. Synthetic tests must run in CI; any private course benchmark must remain local, redacted, and outside the repository and public demo.

**Files:**
- Create: `backend/tests/perf/test_local_slo.py`
- Create: `backend/tests/integration/test_job_cancellation_recovery.py`
- Create: `backend/tests/fixtures/perf_dataset.json`
- Create: `scripts/run_private_benchmark.ps1`
- Create: `docs/engineering/PRIVATE_BENCHMARK_TEMPLATE.md`
- Create: `artifacts/perf/.gitkeep` (generated reports only; real samples are never copied)

**Interfaces:**
- `test_local_slo.py` generates 1,000 concepts and 10,000 evidence rows and measures local read p95 < 500 ms and state-change p95 < 1 s on the documented reference environment. It also checks bounded memory/progress instrumentation and deterministic repeated planner results. Use only standard timing plus the memory/process library verified in G-02; do not add an unlicensed benchmark dependency.
- `test_job_cancellation_recovery.py` starts a synthetic import/remote job, asserts progress updates at least once per second, cancellation reaches `cancelling`/`cancelled` within 2 seconds and starts no new page after 5 seconds, restarts the process, and asserts observable state recovery within 10 seconds with no duplicate authoritative material/job/plan rows.
- `scripts/run_private_benchmark.ps1` accepts an explicit local sample path, verifies it is outside the repository and never copies it, runs metadata-first/parse/RSS/cancel/restart measurements, writes only redacted metrics (file counts, sizes, hashes, durations, peak RSS, timestamps, environment) to a user-selected evidence directory, and exits nonzero on threshold failure. It must not print document names, paths,body text, answers, or secrets.
- `PRIVATE_BENCHMARK_TEMPLATE.md` documents the reference Windows 11 x64/4 logical CPU/16 GiB/SSD environment, commands, start/end times, raw metric file location, and “not executed” placeholders; it is a template, not fabricated evidence.

**Dependencies / parallelism:** Group summary only. QA-02A requires M1-02/M3-02C/API-01C; QA-02B requires QA-02A/M1-02/T-03C/X2-03B; QA-02C requires QA-02B. Synthetic checks can run in parallel with UI/DEMO tasks, but benchmark scripts own only QA evidence paths and may not alter production thresholds or ReviewPolicy. Real private execution requires explicit student authorization and remains separate from CI, Docker, and public demo.

- [ ] **Step 1: Write the minimum failing test**

  Add a cancellation/restart test with a deterministic fake clock/worker and a p95 SLO test over the synthetic dataset. Run:

  ```powershell
  python -m pytest backend/tests/integration/test_job_cancellation_recovery.py backend/tests/perf/test_local_slo.py -q
  ```

  Expected: FAIL because job progress/recovery telemetry and the QA harness are absent or do not yet satisfy the thresholds; preserve the measured failure rather than relaxing limits.

- [ ] **Step 2: Implement the smallest evidence harness**

  Build deterministic fixtures, isolated temporary databases, bounded worker fakes, threshold assertions, redacted metric writers, repository/path containment checks, and restart/cancel orchestration. Make the private script refuse repository paths, missing explicit consent, or output destinations inside source control; keep actual sample content out of logs and artifacts.

- [ ] **Step 3: Focused and full regression**

  Run:

  ```powershell
  python -m pytest backend/tests/integration/test_job_cancellation_recovery.py backend/tests/perf/test_local_slo.py -q
  python -m pytest backend/tests -q
  python scripts/test_all.py
  powershell -ExecutionPolicy Bypass -File scripts/run_private_benchmark.ps1 -Help
  ```

  Expected: focused synthetic tests, full regression, and script help/path-safety checks pass. If the private benchmark is authorized and run, record raw redacted metrics and threshold outcome; otherwise record `尚未执行` rather than inventing results. No CI or public artifact contains the private sample.

- [ ] **Step 4: SPEC compliance review and quality/security/license review**

  SPEC review must check AC-15, AC-17, AC-26, AC-27, AC-34, AC-35, AC-36, and AC-46 plus every §5.3 timing/cancellation/restart threshold. Quality/security/license review must check clock/timezone determinism, worker shutdown races, duplicate prevention, process/path containment, memory measurement validity, redaction, artifact retention, and benchmark/tool licenses. A threshold failure is reported with raw evidence and cannot be relabelled as a pass.

  **Group record:** no worker commit is assigned to this heading. The coordinator records QA-02A/B/C hashes and reviews separately.

**Completion standard:** CI can reproduce synthetic SLO/cancellation/restart checks, and an explicitly authorized private benchmark can produce redacted, thresholded evidence without copying or exposing real course material; unexecuted external evidence remains truthfully marked.

### Task QA-02A: Add Synthetic Performance and SLO Evidence

**Goal:** Measure confirmed synthetic import, retrieval, planner, and API latency/memory thresholds under the reference test profile.

**Files:** Create `backend/tests/performance/test_synthetic_slo.py`, `scripts/run_performance.py`, and `docs/engineering/PERFORMANCE_EVIDENCE.md`.

**Interfaces:** injected/reference hardware metadata, warmup/sample counts, median/p95/peak-memory metrics, explicit thresholds from SPEC, nonzero exit on breach, and no private/provider data.

**Dependencies / parallelism:** Requires M1-02, M3-02C, and API-01C. It completes before QA-02B.

- [ ] **Red:** run `python -m pytest backend/tests/performance/test_synthetic_slo.py -q`; expected FAIL because benchmark harness/evidence is absent.
- [ ] **Green/refactor:** implement deterministic synthetic measurements only, run focused performance, backend regression, and `python scripts/test_all.py`.
- [ ] **Reviews:** SPEC review AC-45, AC-46 and NFR SLOs; quality review clock/timing methodology, flaky-threshold controls, memory sampling, environment metadata, and no private material. Critical findings block QA-02B.
- [ ] **Commit:** scan secrets; `git add -- backend/tests/performance/test_synthetic_slo.py scripts/run_performance.py docs/engineering/PERFORMANCE_EVIDENCE.md`; run `git diff --cached --check`; commit with `git commit -m "test(QA-02A): add synthetic performance evidence [agent: <fresh-agent-id>]"`.

**Completion standard:** Synthetic SLO checks are reproducible, thresholded, environment-labelled, and fail without hiding regressions.

### Task QA-02B: Add Cancellation and Restart-recovery Evidence

**Goal:** Verify bounded cancellation, process restart, remote-job reconciliation, and no duplicate authoritative writes across local/import/provider workflows.

**Files:** Create `backend/tests/integration/test_cancellation_restart.py`, `scripts/run_restart_recovery.py`, and `docs/engineering/RECOVERY_EVIDENCE.md`.

**Interfaces:** cancellation tokens, process kill/reopen checkpoints, SQLite recovery, X2-03B job reconciliation, duplicate quarantine, cleanup, and deterministic timeouts.

**Dependencies / parallelism:** Requires QA-02A, M1-02, T-03C, and X2-03B. It completes before QA-02C.

- [ ] **Red:** run `python -m pytest backend/tests/integration/test_cancellation_restart.py -q`; expected FAIL because the recovery harness/assertions are absent.
- [ ] **Green/refactor:** implement test harness/evidence only, route product defects to owners, then run focused recovery/backend/full tests.
- [ ] **Reviews:** SPEC review AC-17, AC-26, AC-27, AC-46, AC-50; quality review bounded waits/process cleanup, restart determinism, idempotency, provider-fake isolation, and no exactly-once overclaim. Critical findings block QA-02C.
- [ ] **Commit:** scan secrets; `git add -- backend/tests/integration/test_cancellation_restart.py scripts/run_restart_recovery.py docs/engineering/RECOVERY_EVIDENCE.md`; run `git diff --cached --check`; commit with `git commit -m "test(QA-02B): add cancellation and restart recovery [agent: <fresh-agent-id>]"`.

**Completion standard:** Interrupted operations resume, cancel, quarantine, or remain truthfully incomplete without duplicate authoritative state.

### Task QA-02C: Add the Authorization-gated Private Benchmark Boundary

**Goal:** Provide a safe template/runner for optional real-course performance evidence without committing or exposing the courseware.

**Files:** Create `scripts/run_private_benchmark.ps1`, `backend/tests/contract/test_private_benchmark_boundary.py`, `docs/engineering/PRIVATE_BENCHMARK_TEMPLATE.md`, and `docs/engineering/PRIVATE_BENCHMARK_EVIDENCE.md`.

**Interfaces:** explicit local-path/authorization preflight, output allowlist, course hash/count/aggregate metrics only, no body/render/answer/path copy, and `not executed` until separately authorized.

**Dependencies / parallelism:** Requires QA-02B. DIST/DOC/FIN consume this terminal QA unit; running against private courseware requires separate execution-time user authorization.

- [ ] **Red:** run `python -m pytest backend/tests/contract/test_private_benchmark_boundary.py -q`; expected FAIL because the runner/template safeguards are absent.
- [ ] **Green/refactor:** implement dry-run/preflight/redaction only and run contract/full tests. Do not point it at the user's course directory without new authorization; leave live evidence `not executed`.
- [ ] **Reviews:** SPEC review AC-07, AC-45, AC-46; quality review path containment, output schema/redaction, authorization guard, timestamps, artifact ignore rules, and no body/hash reversal risk. Critical findings block distribution/docs.
- [ ] **Commit:** scan secrets; `git add -- scripts/run_private_benchmark.ps1 backend/tests/contract/test_private_benchmark_boundary.py docs/engineering/PRIVATE_BENCHMARK_TEMPLATE.md docs/engineering/PRIVATE_BENCHMARK_EVIDENCE.md`; run `git diff --cached --check`; commit with `git commit -m "test(QA-02C): add private benchmark boundary [agent: <fresh-agent-id>]"`.

**Completion standard:** The offline guard tests pass, the runner cannot emit private content, and live private evidence remains `not executed` unless separately authorized and actually run.
