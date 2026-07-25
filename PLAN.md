# ProjectB Stage B Scope-Reset Plan

> **Status: ACTIVE REMEDIATION / NOT DISPATCHABLE.** This file is the current stage-gate ledger while the reduced `SPEC.md` awaits student confirmation. It is not an implementation plan and authorizes no production code, worktree, Open Design run, CI, provider call, or deployment.

**Goal:** Replace the superseded 113-unit planning set with a course-compliant, reviewable plan for the reduced v1 without losing deferred work or historical evidence.

**Current specification:** [`SPEC.md`](SPEC.md), reduced v1 draft, not yet signed.

**Superseded planning evidence:** [`docs/superpowers/plans/archive/README.md`](docs/superpowers/plans/archive/README.md).

**Deferred feature plans:** [`docs/superpowers/plans/archive/deferred-v2/`](docs/superpowers/plans/archive/deferred-v2/).

## Gate Ledger

| ID | Gate | Dependency | Status | Completion evidence |
| --- | --- | --- | --- | --- |
| SR-01 | Freeze hashes and preserve the old root/detailed plans | approved scope-reset design | complete | archive index records paths, bytes and SHA-256; checkpoint `ccd1dfe` |
| SR-02 | Move `.r5` plan reconstruction out of the active source tree | SR-01 | complete | ignored local archive tree digest; no production-source claim; checkpoint `ccd1dfe` |
| SR-03 | Draft reduced v1 SPEC and deferred-plan set | SR-01 | complete | current `SPEC.md` plus four `ARCHIVED / NOT DISPATCHABLE` plans; archive checkpoint `ccd1dfe` |
| SR-04 | Synchronize requirements, process and decision documents | SR-03 | complete | reduced SPEC, current matrix, decisions, process log and handoff agree on the confirmation gate; checkpoint `5f54431` |
| SR-05 | Run document, credential, link and evidence validation | SR-04 | complete | SPEC `C6231816...9AD6`; archive/deferred/link/credential/diff checks pass; standard evidence is 63/2 and strict fails only at D-025; checkpoint `5f54431` |
| SR-06 | Student confirms the complete reduced SPEC | SR-05 | blocked on student | explicit student response naming the current SPEC snapshot |
| SR-07 | Invoke `superpowers:writing-plans` and replace this ledger with the implementation PLAN | SR-06 | blocked | one active plan, at most about 30 fresh-agent units, exact red/green/review commands |
| SR-08 | Review the same SPEC/PLAN hashes for compliance and quality | SR-07 | blocked | independent SPEC and quality/security/license PASS receipts |
| G-03 | Claude Code cold start using only final SPEC/PLAN | SR-08 + D-005 | blocked | questions, misunderstandings, output gap and repair diff in `SPEC_PROCESS.md` |
| G-04 | Student approves implementation and worktree map | G-03 | blocked | explicit approval, branch/worktree ownership record |

## Current v1 Boundary

- M1: extractable-text PDF, UTF-8 TXT/Markdown, raw hash, page/line locators and user-confirmed concept mapping.
- M2: generic concepts, bundled mutex/race/deadlock deterministic evaluators, source-bound explanation/practice/feedback candidates and append-only evidence.
- M3: deterministic mastery plus continuous/finals review planning.
- Provider modes: local `L` and request-scoped fragment `P`; built-in OpenAI adapter plus deterministic test/demo mock.
- Required delivery remains WebUI, Credential Manager, one-command tests, GitLab `unit-test`, GitHub CI, Windows single-file, OCI demo and a final public HTTPS URL.

The following are not v1 implementation tasks: OCR/images/scanned material, remote whole-file mode F, durable remote jobs, exam-material automation and additional deterministic rubric libraries. They remain recoverable in the deferred archive and require a new brainstorming/spec/plan cycle before dispatch.

## Implementation-Plan Authoring Contract After SR-06

The future replacement `PLAN.md` must:

1. map every current SPEC acceptance criterion and every course hard requirement to an executable task or named human/external gate;
2. keep each dispatch unit small enough for one fresh subagent session and list exact dependencies, files, failing test, red/green/refactor commands, two reviews, credential scan and completion standard;
3. use one authoritative active task DAG rather than duplicating root and 14 subsystem plans;
4. preserve archived feature links without treating archived tasks as current acceptance scope;
5. stop at external authorization gates for live provider calls, remote repositories, CI observation, image publication and deployment.

## Required Validation Before SR-06

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\verify_evidence.ps1
git diff --check
```

The standard evidence validator must remain `PASS` with exactly two explicitly blocked hosting rows. Distribution-strict validation must fail only because D-025 is unresolved. Local Markdown links, required SPEC sections, at least five user stories, active/deferred scope separation and credential-pattern scans must also pass.

Current pre-confirmation verification snapshot:

- SPEC: 14 required sections, 8 unique user stories, 24 unique acceptance criteria, SHA-256 `C6231816A62C807D205FC7A3E6142C5636DE18FD8A2C580B48E63B106F959AD6`.
- Archive: 12 superseded files match indexed byte lengths and SHA-256; four deferred plans have all eight recovery sections and the required non-dispatchable status.
- Recovery tree: 1,021 files / 35,989,967 bytes, manifest-v1 SHA-256 `50187D07B1BC03226B26AD3DD8873C01C6EDD2E244D069116CC60FD728277C3D`; local path is ignored by Git.
- Documents/security: 42 non-superseded Markdown files contain 21 valid local links and zero broken links; the 28-file intended checkpoint surface has zero configured credential-pattern matches; `git diff --check` exits 0.
- Evidence: normal validator returns `rows=63 explicitly_blocked=2`; distribution-strict exits 1 only because the two D-025 hosting rows remain explicitly blocked.

## Human Gates

- **Immediate:** student reviews and confirms the complete reduced `SPEC.md`.
- **Before G-03:** student controls Claude Code installation, login, exact version and a clean session.
- **Before implementation:** student approves cold-start repairs.
- **Before public delivery:** student resolves D-025 and separately authorizes remote push/PR/CI/image/deployment actions.
- **Before final submission:** student writes `REFLECTION.md`; AI may only review a student draft with disclosed assistance.
