# AI4SE Project B Requirements Compliance Matrix

**Snapshot:** `2026-07-26T00:49:31+08:00`

**SPEC:** `795791627579BFEBE24717981168A54E2D546F613FEA84CCDF0AC0ECBA387862`

**PLAN frozen:** `6FDD69F2FD309841CC46DB1C75C142E4E1E8474E1575A2E765F49EF67002A05D`
**Stage:** Stage B same-hash dual review PASS. G-03 cold start and G-04 implementation approval remain open; no implementation dispatch is authorized.

`verified` means current local evidence exists; `planned` means a named active task owns it; `blocked` means a named human/external gate remains; `not-started` means no product evidence exists. This is the only active course matrix. Archived plans are recovery evidence, never PASS evidence.

| Hard requirement | Active mapping | Status / current evidence | Closure |
| --- | --- | --- | --- |
| Real useful problem explainable in 30 seconds | SPEC 1.1--1.3 | verified document | implementation evidence after G-04 |
| At least three clear modules | M1 materials, M2 learning, M3 review | verified specification; not implemented | M1-01--03, M2-01--04, M3-01--02 |
| At least five INVEST stories | US-01--US-08 | verified document; same-hash review PASS | implementation evidence after G-04 |
| Module contracts and objective acceptance | SPEC 3 and AC-01--24 | planned; each AC mapped in PLAN 12 | named task/gate per AC |
| Architecture/data flow/data model | SPEC 6--7 | planned | F-02/03, feature repositories, API-01--03 |
| Performance/reliability/errors/observability | SPEC 5 | planned | F-04, API-03, QA-RELEASE, DIST-01 |
| Input validation and safe deletion | SPEC 3.1 and 8 | planned | M1-01--03, API-01, UI-03/06 |
| Host/Origin/CSRF/session boundary | local plus explicit public profile | planned | F-04 and DEMO-01 positive/negative tests |
| Secret never enters DB/config/log/browser/Git | WinVault plus fail-closed scanner | baseline partially verified; product not started | F-01B/F-05 and every-task protocol |
| First-run hidden credential status/update/clear | value-free settings contract | planned | F-05, API-03, UI-06, DIST-01 real lifecycle |
| Optional model is consent-bound and non-authoritative | L+P; mock default; exact text fragments only | P-only evidence verified; adapter not started | P-01/P-02/API-02/UI-04 |
| No autonomous-agent overclaim | v1 has constrained request ports, no autonomous loop | verified specification boundary | P-01/P-02 contract tests |
| Usable WebUI | import, mapping, learning, review, settings | planned | UI-01--06 |
| Open Design workflow | `frontend-design`, `default`/Neutral Modern selected; environment PASS | partially verified | actual run/artifact/evidence in UI-01 |
| Responsive/keyboard/accessibility | 360/768/1440, visible focus, axe | planned | each UI task red/green plus QA-RELEASE |
| At least one reproducible distribution | Windows x64 single file and OCI mock demo | exact inputs verified; products not started | DIST-01/02; public OCI registry/pull-by-digest closes at EXT-REMOTE-CLOSE |
| Windows cold start <=10 seconds | clean reference VM contract | not-started | DIST-01 measured receipt |
| Linux/amd64 dependency/base evidence | separate CI/demo hashed locks and OCI digests | verified planning input: 41 CI, 14 demo | F-01A exact-base sync; DIST-02 build/SBOM/smoke |
| Public HTTPS WebUI URL | immutable mock OCI image | blocked on student D-025 | D-025-HOST-CLOSE then DOC-01 |
| One-command tests | `python scripts/test_all.py` | not-started | F-01B; QA-RELEASE observes full pass |
| Core automated tests | domain/storage/API/UI/E2E/security/performance | not-started | F-02 through DEMO-01/P-02 |
| Every push runs CI | dual platform definitions | not-started | CI-01 then EXT-REMOTE-CLOSE |
| GitLab job exactly `unit-test` | `.gitlab-ci.yml` | not-started | CI-01, final NJU pipeline receipt |
| GitHub Actions and PR evidence | workflow plus full-SHA actions | not-started | CI-01, EXT-REMOTE-CLOSE |
| Final course CI PASS | authoritative NJU GitLab plus mirror evidence | blocked on remote authorization | EXT-REMOTE-CLOSE |
| Incremental commits and PR/MR history | 31 task commits, coordinator evidence commits, 9 worktree branches | planned | per-task protocol and EXT-REMOTE-CLOSE |
| Fresh subagent per PLAN task | one clean session/task | planned | after G-04 |
| TDD red-green-refactor | exact red/green command in all 31 task cards | not-started | every behavior task after G-04 |
| SPEC review then quality/security/license review | terminal hash-bound review loop | planned | every task protocol; Critical stops sequence |
| Required Superpowers order | brainstorming -> plan -> worktree -> TDD -> reviews -> finish | brainstorming/writing-plans evidenced; later stages gated | G-03/G-04 then task protocol |
| `SPEC.md` required sections | 14 sections, 8 stories, 24 AC, risks/deferred scope | verified student-confirmed document | SR-08 same-hash review |
| `PLAN.md` exact task fields | exactly 31 tasks after reviewer-required F-01 split; dependency/parallel/files/red/green/done in each | verified: mechanical audit plus two same-hash SR-08 reviews PASS | preserve frozen hashes through G-03 |
| Stranger cold start with only SPEC/PLAN | Claude Code, task F-01A; operator runbook prepared | blocked: `CLAUDE_CODE_NOT_ON_PATH`; no attempt claimed | G-03 student-accessible clean session |
| Cold-start repair then implementation approval | separate post-repair student gate | blocked | G-04; current SPEC confirmation does not substitute |
| `SPEC_PROCESS.md` process and cold-start diff | scope/signoff history exists | partial | record G-03 transcript/gaps/diff truthfully |
| `AGENT_LOG.md` timestamp/task/skill/context/output/hash/human edits/lesson | historical and current entries exist | partial | coordinator evidence commit after every task |
| README required sections | intro/install/run/distribution/tree/security/credentials/limits/deployment/licenses | not-started | DOC-01 after remote/host receipts |
| Third-party sources/licenses | 63-row ledger plus verifier-bound bootstrap artifacts, 54 Python/166 npm closure, Linux subset, notices planned | partially verified | F-01A/F-01B notices, DIST SBOM, DOC-01 final index |
| Student reflection 1500--2500 Chinese characters | AI may review only a supplied student draft | blocked on student | REFLECTION-CLOSE |

## Evidence Receipts

- Stage B mechanical: `PLAN_MECHANICAL_PASS Tasks=31 Ledger=31 Fields=5 DependencyEdges=30 AcRows=24 Placeholders=0`.
- Stage B reviews: `/root/plan_spec_review` and `/root/plan_quality_review` both returned `PASS; Critical=0, Major=0, Minor=0` against SPEC `79579162...7862` and PLAN `6FDD69F2...A05D`; both were read-only.
- Standard: `EVIDENCE_VALIDATION_PASS rows=63 explicitly_blocked=2 python_pins=54 npm_packages=166`.
- Linux supplement: `LINUX_EVIDENCE_PASS ci_packages=41 demo_packages=14 license_rows=41`.
- P-only provider: `PROVIDER_V1_P_EVIDENCE_PASS rows=7 models=2 expires=2026-08-25`; evidence SHA-256 `35A3F46E036563E3FC681DF3190EB56336AB48B9D9817AD48F4D5DF42230F076`.
- Strict distribution remains expected to fail only on the two D-025 hosting rows. No product test/build/package/CI/provider-call/deployment evidence exists.

## Deferred Boundary

OCR/image/scanned-PDF/bulk ingestion, remote whole-file F and durable jobs, past-exam/teacher-focus intelligence, and rubrics beyond mutex/race/deadlock are only in `archive/deferred-v2`. They cannot satisfy current rows or enter v1 acceptance without a new brainstorming, SPEC confirmation, and plan.
