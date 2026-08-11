# AI4SE Project B Requirements Compliance Matrix

**Snapshot:** `2026-08-11`

**SPEC:** `312851CC77CA1E5E83CD87BEFF9A43539A87E656C85C9EF03541F53B6928F90A`

**PLAN pre-dispatch:** `910A3AEC9B4CEDCC119675C5D862879D178E3FE062CEE39C2AD62AF07219E923`

**PLAN current evidence-only state:** `A5824E3BA1E1941C81D2EE884FDC4E6E7750B9B64EA604CE149A037B0C1644D9`.
**Stage:** `LOCAL IMPLEMENTATION VERIFIED / SUBMISSION PACKAGE READYING`. Foundation, all three domain modules, local FastAPI, responsive WebUI, isolated mock demo, P-02, Windows/OCI recipes, and local CI contracts are implemented. DOC-01 files and the student reflection are committed at `9908799`; the startup/package repair is committed at `b3446d1`. D-025 classifies ProjectB as a local binary application whose FastAPI process serves only a loopback WebUI, so the conditional cloud-deployment clause is not applicable; current-artifact clean-VM/10-second evidence is waived by D-026; remote pipelines remain unexecuted.

`verified` means current local evidence exists; `planned` means a named active task owns it; `blocked` means a named human/external gate remains; `not-started` means no product evidence exists. This is the only active course matrix. Archived plans are recovery evidence, never PASS evidence.

| Hard requirement | Active mapping | Status / current evidence | Closure |
| --- | --- | --- | --- |
| Real useful problem explainable in 30 seconds | SPEC 1.1--1.3 | verified document | implementation evidence after G-04 |
| At least three clear modules | M1 materials, M2 learning, M3 review | M1, M2 and M3 domain/repository flows complete through `3a93f27` | API-01--03 and UI integration |
| At least five INVEST stories | US-01--US-08 | verified document; eight stories retained in current SPEC | local implementation evidence complete; remote acceptance remains external |
| Module contracts and objective acceptance | SPEC 3 and AC-01--24 | all 39 local PLAN tasks complete; D-025/D-026 are explicit waivers | remote CI receipt only |
| Architecture/data flow/data model | SPEC 6--7 | core and learning schema plus M1/M2/M3 repositories and complete local API implemented through `e41df6a` | UI-01--06 integration |
| Performance/reliability/errors/observability | SPEC 5 | cached non-import API p95 contract verified at `e41df6a`; release measurements remain planned | QA-RELEASE, DIST-01 |
| Input validation and safe deletion | SPEC 3.1 and 8 | parser/type/timeout/limits plus shared/last-ref deletion, source invalidation and retryable tombstone verified through `aa2a6da` | API-01, UI-03/06 integration |
| Host/Origin/CSRF/session boundary | local plus explicit public profile | local loopback policy, session-bound CSRF, safe errors and audit allowlist committed at `736292a`; public profile remains planned | DEMO-01 positive/negative tests |
| Secret never enters DB/config/log/browser/Git | WinVault plus fail-closed scanner | Scanner verified at `1d6dcab`; value-free WinVault lifecycle, redacted failures, safe audit references and value-free API responses verified through `e41df6a` | UI-06 browser integration plus every-task scan |
| First-run hidden credential status/update/clear | value-free settings contract | backend lifecycle and local API status/update/clear verified through `e41df6a`; first run remains unconfigured | UI-06, DIST-01 application lifecycle |
| Optional model is consent-bound and non-authoritative | L+P; mock default; exact text fragments only | P-only evidence and governed adapter verified at `8e6b23f`; no real key/call | P-01/P-02/API-02/UI-04 |
| No autonomous-agent overclaim | v1 has constrained request ports, no autonomous loop | verified specification boundary | P-01/P-02 contract tests |
| Usable WebUI | import, mapping, learning, review, settings | all five views and the responsive shell are implemented; frontend suite `60 passed` and Vite build passed in the current full local gate | remote/manual course acceptance remains external |
| Open Design workflow | `frontend-design`, `default`/Neutral Modern selected; environment PASS | verified: real project/run/artifact, immutable hashes and reviewed production screenshots in `docs/engineering/OPEN_DESIGN_RUN.md` | reuse reviewed tokens/components in UI-02--06 |
| Responsive/keyboard/accessibility | 360/768/1440, visible focus, axe | UI-01 Playwright `12 passed`; UI-02 focused E2E `3 passed` across 360/768/1440 with keyboard focus, no overflow and no serious/critical axe findings | UI-03--06 plus QA-RELEASE |
| At least one reproducible distribution | Windows x64 single file and OCI mock demo | Windows build/development smoke and local OCI build/run/smoke are verified; no registry publication is required for local delivery | complete locally |
| Windows clean-host / former <=10-second target | D-026 student decision | waived, not passed: the prior 36.64 MB artifact measured `23.554`, `14.664`, and `11.487` seconds plus strict timeouts; the current 29.22 MB artifact (`12C6131...6201`) passes local smoke but was not clean-VM timed | not required for local submission package; retain limitation |
| Linux/amd64 dependency/base evidence | separate CI/demo hashed locks and OCI digests | verified planning input: 41 CI, 14 demo | F-01A exact-lock sync; DIST-02 build/SBOM/smoke |
| WebUI access / conditional cloud deployment | D-025 local-binary classification and course section 4.11 | verified local loopback WebUI at `http://127.0.0.1:4173/`; no remotely hosted service, so public cloud deployment is not applicable | local browser receipt in submission handoff |
| One-command tests | `python scripts/test_all.py` | current release bytes: backend `284 passed`, frontend `60 passed`, Ruff/mypy/Vite, credential and license gates passed | final commit reruns the same command |
| Core automated tests | domain/storage/API/UI/E2E/security/performance | current full local gate is backend `284 passed`, frontend `60 passed`; prior system Chrome Learning/Settings E2E `9 passed` across 360/768/1440 | remote CI remains external |
| Every push runs CI | F-01D seeds pinned scanner/backend/frontend current-suite workflows; CI-01 adds distribution | implemented locally at `069acb8541b8d59a7977a484f06d8f9abbefe780`; YAML and seed contract verified, remote push not executed | EXT-REMOTE-PREP branch-tip current-suite receipts |
| GitLab job exactly `unit-test` | `.gitlab-ci.yml` | implemented locally and mechanically verified; remote pipeline not executed | CI-01, final NJU pipeline receipt |
| GitHub repository visibility/access | public repo or private with TA collaborator | blocked on remote authorization | EXT-REMOTE-PREP visibility/collaborator receipt |
| GitHub Actions and PR evidence | workflow plus full-SHA actions | workflow implemented locally with exact checkout SHA and least permissions; PR/remote run not executed | CI-01, EXT-REMOTE-PREP, EXT-REMOTE-FINAL |
| Final course CI PASS | authoritative NJU GitLab plus mirror evidence on final docs commit | blocked on remote authorization | EXT-REMOTE-FINAL |
| Incremental commits and PR/MR history | 39 task rows, scanned coordinator evidence commits, 9 stacked worktree branches | local branch/commit history preserved; remote PR/MR creation and merge are unexecuted | EXT-REMOTE-PREP/FINAL sequential retarget-and-merge closure |
| Fresh subagent per PLAN task | one clean session/task | fresh worker `/root/m1_01_impl` completed M1-01; earlier deviations and reviewer identities remain recorded | continue every behavior task |
| TDD red-green-refactor | exact red/green command in all 39 cards; shared assertion-level 2--5 minute step expansion | local implementation tasks retain RED/GREEN receipts; current full gate is green | remote CI replay remains external |
| SPEC review then quality/security/license review | terminal hash-bound review loop | local tasks received staged spec and quality review; resolved Critical/Major findings are recorded in AGENT_LOG | final release-doc review and remote CI receipt |
| Required Superpowers order | brainstorming -> plan -> worktree -> TDD -> reviews -> finish | local workflow and deviations are recorded; release branch is at local finishing stage | remote integration remains external |
| `SPEC.md` required sections | 14 sections, 8 stories, 24 AC, risks/deferred scope | current bytes confirmed by student; final release-doc two-stage revalidation PASS with Critical=0, Major=0 | complete locally |
| `PLAN.md` exact task fields | exactly 39 tasks; dependency/parallel/files/red/green/done in each | 39/39 local task rows are marked complete with commit evidence | remote release gates remain separate |
| Stranger cold start with only SPEC/PLAN | two fresh non-Codex sessions intake then F-01S1A | verified: current hashes, empty ambiguities, exact red, two artifacts, PowerShell 7 green exit 0 | complete; disposable artifacts are not product implementation |
| Cold-start repair then implementation approval | separate post-repair student gate | verified: G-03 complete; student explicitly approved G-04 on 2026-08-03 | local implementation active; remote/release gates remain separate |
| `SPEC_PROCESS.md` process and cold-start diff | sections 1--2 contain >3 real question/answer/revision rounds; later sections retain G-03P/failures/final run | verified: final intake, segmented execution, red/green, hashes, line counts and limitations recorded | continue per-task evidence after G-04 |
| `AGENT_LOG.md` timestamp/task/skill/context/output/hash/human edits/lesson | historical and current entries exist | current through startup repair `b3446d1` and local docs `9908799` | final evidence sync, then external gates |
| Student-written code declaration | conditional top-of-file/function comment plus trailer/log | F-01C records `Human-Changes: none`; no student-authored code claimed | per-task protocol step 5 |
| README required sections | intro/install/run/distribution/tree/security/credentials/limits/local architecture/licenses | committed at `9908799`; README contract `1 passed`; link verifier `LINK_VERIFICATION_PASS files=2 links=5`; D-025/D-026 waivers and remote gaps are stated | remote final gate |
| Third-party sources/licenses | 63-row ledger, 54 Python/166 npm closure, Linux subset, five immutable bootstrap license rows | F-01A manifests/locks and F-01B exact license bytes implemented; F-01E notice inventory and baseline-license hash verifier pass (`python=54 npm=166`) | F-01E terminal commit, DIST SBOM, DOC-01 final index |
| Student reflection 1500--2500 Chinese characters | AI may review only a supplied student draft | supplied student draft lightly polished; `1938` CJK characters, explicit AI-assistance declaration, committed at `9908799` | remote final gate |

## Evidence Receipts

- Pre-dispatch mechanical baseline: `PLAN_MECHANICAL_PASS Tasks=39 Ledger=39 Fields=5 AcRows=24 Placeholders=0 Unknown=0 Self=0 Cycle=0 DependencyEdges=38` against the recorded pre-dispatch SPEC/PLAN bytes. Current evidence-only edits preserve the 39-row ledger while adding completion hashes and D-025/D-026 decisions.
- Current D-025/D-026 normative revalidation PASS: the first read-only review caught a stale README assertion and surfaced the course-text ambiguity; the student then explicitly classified ProjectB as a local app under the conditional server-project clause. After repairing the README contract and removing public-registry/HTTPS contradictions, final two-stage review returned Critical=0, Major=0 against SPEC `312851CC...8F90A` and PLAN `A5824E3B...1644D9`.
- Historical Stage B reviews: `/root/plan_spec_review` and `/root/plan_quality_review` both returned `PASS; Critical=0, Major=0, Minor=0` against SPEC `79579162...7862` and PLAN `6FDD69...A05D`; these verdicts do not transfer to current bytes.
- Failed reviews: the first pair returned `Critical=0, Major=3, Minor=2` and `Critical=1, Major=10, Minor=1` against SPEC `600395...ED71` / PLAN `8A4BE...AFD`. The second pair returned `Critical=0, Major=3, Minor=0` and `Critical=0, Major=6, Minor=2` against SPEC `69A534...855E` / PLAN `47624A...225A`. Findings were repaired but verdicts are not reused.
- Current G-03P remediation: fresh projectless task `019fa331-3da1-7f80-a37c-ac7abb135a46` used SPEC `6A0DB7...11E56` / predecessor PLAN `D574B8...1D742`, produced exact missing-scanner red and eight-group green with eleven helpers, then its optional self-scan found `credential_assignment` in both contract sources. Final PLAN `E96C...` makes exact `files=4` self-scan cleanliness mandatory; focused dual review passed. This remains same-family evidence and does not close G-03.
- Formal G-03 incomplete attempt: Claude Code session `71a50d25-4cd7-48b1-9472-8107e82779ed` used `claude-sonnet-5`, final SPEC/PLAN hashes, and an initial two-file directory. It reported those hashes, then created only an empty `scripts/tests` directory and returned an empty `end_turn`; CLI exit 0, no permission denials, about `$0.4712`, no scripts/diff/red/green/self-scan. Runner postconditions now reject this as `required_artifact_missing`; G-03 remains open.
- Formal G-03 gateway timeout: Claude Code session `32b62490-7817-4d3d-8452-7a29a4de94ea` used `claude-sonnet-4-6`, final hashes, and an initial two-file directory. It verified the hashes, then the gateway returned `504 Gateway Time-out`; CLI exit 1, about `$0.1818`, no scripts/diff/red/green/self-scan. G-03 remains open.
- Bootstrap licenses: official GitHub Contents/Refs API resolved five immutable texts; task ownership correction changed evidence SHA-256 to `FD65C5D2F8421F7B99AE4D540B80A8BBED1C28C78EF45851F7C6E5051034F310`. The standard verifier binds this raw hash and all five immutable row identities; the stale-hash red and corrected green were both observed while the standard receipt stayed at 63 rows.
- F-01D local CI seed: product commit `069acb8541b8d59a7977a484f06d8f9abbefe780`; `CI_SEED_CONTRACT_PASS`, `CI_YAML_PARSE_PASS files=2`, frontend `1 passed`, TypeScript exit 0, scanner `files=210`, and final fresh review `Critical=0, Major=0`. Docker daemon and both remote pipelines were not executed, so no remote CI PASS is claimed.
- Standard: `EVIDENCE_VALIDATION_PASS rows=63 explicitly_blocked=2 python_pins=54 npm_packages=166`.
- Linux supplement: `LINUX_EVIDENCE_PASS ci_packages=41 demo_packages=14 license_rows=41`.
- P-only provider: `PROVIDER_V1_P_EVIDENCE_PASS rows=7 models=2 expires=2026-08-25`; evidence SHA-256 `35A3F46E036563E3FC681DF3190EB56336AB48B9D9817AD48F4D5DF42230F076`.
- Strict course completion remains expected to fail only on unexecuted remote repository/CI rows. D-025 closes public hosting as not applicable to this local binary application, and D-026 waives current-artifact clean-VM timing. No public deployment or provider call is claimed.

## Deferred Boundary

OCR/image/scanned-PDF/bulk ingestion, remote whole-file F and durable jobs, past-exam/teacher-focus intelligence, and rubrics beyond mutex/race/deadlock are only in `archive/deferred-v2`. They cannot satisfy current rows or enter v1 acceptance without a new brainstorming, SPEC confirmation, and plan.
