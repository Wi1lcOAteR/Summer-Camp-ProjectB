# AI4SE Project B Requirements Compliance Matrix

**Snapshot:** 2026-07-25T12:01:28+08:00
**Project stage:** Stage B scope reset; reduced `SPEC.md` awaits student confirmation.
**Status vocabulary:** `verified` = current evidence exists; `planned` = mapped to the active v1 contract but not implemented; `blocked` = named human/external gate; `not-started` = no implementation evidence.

This is the single current requirements matrix. Historical audits and superseded plans are evidence, not current completion claims.

| Course requirement | Current v1 mapping | Status / evidence | Blocking gate or next task |
| --- | --- | --- | --- |
| Real problem explainable in 30 seconds | `SPEC.md` 1.1--1.3 defines local-first source/evidence/review workbench | planned; SPEC draft complete | student confirms reduced SPEC |
| At least three clear modules | M1 material/source, M2 learning/check, M3 review plan | planned | implementation PLAN after SPEC signature |
| At least five INVEST stories | `SPEC.md` contains US-01--US-08 | planned; static count available | SPEC review |
| Module input/behavior/output/boundary/errors | `SPEC.md` section 3 fixes contracts and stable errors | planned | SPEC review |
| Non-functional security, performance, usability, observability | `SPEC.md` sections 4--5 and 8 | planned | PLAN mappings and implementation evidence |
| Architecture and data flow | `SPEC.md` section 6 | planned | PLAN interface review |
| Data model | `SPEC.md` section 7 | planned | migration/repository tasks after approval |
| Credential threat model | Credential Manager only; hidden input; no secret in DB/config/log/browser/Git | planned | security/credential implementation tasks |
| First-run view/update/clear credential flow | WebUI settings and X1 contract | planned | UI/API credential tasks |
| No real credentials in Git/history/log/snapshot | `.gitignore`, current evidence scans, fail-closed scanner requirement | partially verified; no known real key | run scanner before each commit |
| Distribution form | Windows x64 single-file plus OCI demo | planned; dependency/base evidence exists | DIST tasks; D-025 for public host |
| Clean build/run instructions | `SPEC.md` section 9 and future README | not-started | implementation and clean-environment evidence |
| Public accessible WebUI URL | Same-domain OCI mock demo; host remains unset | blocked | D-025 and authorized deployment |
| WebUI is mandatory and usable | Four-stage React workbench, responsive and keyboard/axe acceptance | planned | UI tasks after Open Design run |
| Open Design workflow | `frontend-design` + `default` / Neutral Modern selected; environment gate previously PASS | verified for installation/selection only | actual project/run/artifact in authorized UI task |
| Agent boundary | v1 has constrained single-request model ports, no autonomous loop/tool dispatch | planned and explicit | any future agent requires new SPEC decision |
| Superpowers installed and used | 14 skills callable; brainstorming and formal writing-plans evidence recorded | verified | continue stage-specific skills |
| `brainstorming -> writing-plans -> worktree -> execution -> TDD -> review -> finish` | Gate order fixed in `SPEC.md` 14 and current `PLAN.md` | planned; only first stages reached | SR-06/SR-07/G-03/G-04 |
| TDD red--green--refactor | `SPEC.md` AC-22 and future PLAN authoring contract | not-started | implementation approval |
| One fresh subagent per task | Future PLAN limits each dispatch unit to one session | not-started | reviewed implementation PLAN |
| Two-stage review per task | SPEC compliance then quality/security/license | not-started | reviewed implementation PLAN |
| Worktree/branch per independent feature | G-04 creates ownership map after cold start | blocked by stage gate | G-03 plus student implementation approval |
| `SPEC.md` required sections | Current draft includes problem, 8 stories, modules, NFR, architecture, model, credentials, distribution, tech, AC and risks | planned; document exists | student signature and independent review |
| `PLAN.md` with task/dependency/files/red test/verification | Current file is intentionally a non-dispatchable stage ledger | blocked by correct process | student confirms SPEC, then `writing-plans` |
| `SPEC_PROCESS.md` with at least three iterations and cold-start diff | Historical iterations exist; scope reset being appended; cold start absent | partial | G-03 |
| Different-type cold start using only SPEC/PLAN | Claude Code selected | blocked | final PLAN PASS and student-controlled clean session |
| `AGENT_LOG.md` timestamp/skill/context/subagent/commit/human change/lesson | Historical log exists; scope reset entry required | partial | synchronize current checkpoint |
| One-command automated tests | Canonical command specified as `python scripts/test_all.py` | not-started | foundation implementation task |
| Core automated tests | Domain/API/UI/mock/e2e/security acceptance in `SPEC.md` | not-started | implementation |
| GitLab CI with job exactly `unit-test` | Required by `SPEC.md` AC-20 | not-started | CI task and remote authorization |
| GitHub Actions on push | Required alongside GitLab by confirmed dual-platform strategy | not-started | CI task and remote authorization |
| Final course CI pass | No remote CI run exists | blocked | immutable candidate plus authorized push/observation |
| Incremental commit/PR history and subagent identity | Future task completion contract | not-started | implementation approval and remote authorization |
| README required sections | Exact section list fixed in `SPEC.md` section 9 | not-started | DOC task after verified behavior exists |
| Third-party source and license record | G-02A dependency/license evidence exists; final manifest/README absent | partial | manifest, license verifier, DOC task |
| Student `REFLECTION.md` 1500--2500 words | AI will not author it; student prompts recorded in `DECISIONS_NEEDED.md` | blocked on student | student draft before final submission |

## Active Scope Versus Archive

The active acceptance scope is only the reduced `SPEC.md`. Deferred OCR/image ingestion, remote whole-file F, durable remote jobs, exam-material automation and extended rubric libraries are indexed under `docs/superpowers/plans/archive/deferred-v2/` and marked `ARCHIVED / NOT DISPATCHABLE`.

No course hard requirement is satisfied solely by an archived task. Public WebUI, credentials, test command, CI, distribution, Open Design evidence, cold start, process documents, licenses and student reflection remain active requirements even when related implementation is not started.

## Current Evidence Boundary

- Standard evidence validator: expected `PASS rows=63 explicitly_blocked=2 python_pins=54 npm_packages=166`.
- Distribution-strict validator: expected failure only because D-025 leaves two hosting rows explicitly blocked.
- No product test, build, package, CI, provider request or deployment result exists yet.
- `.r5` reconstruction is archived local plan-review material and is not implementation evidence.
