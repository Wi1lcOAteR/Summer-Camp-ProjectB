# AI4SE Project B Requirements Compliance Matrix

**Snapshot:** `2026-08-03`

**SPEC:** `AEA67BB5544AD22932DC4304964F7FD266FE8A5DE7AA396EA8974D30867E8381`

**PLAN pre-dispatch:** `910A3AEC9B4CEDCC119675C5D862879D178E3FE062CEE39C2AD62AF07219E923`

**PLAN current evidence-only state:** `E00979276FCDFB52FC88E5449B8E726BE9D00453B8FBD5A0B07D0005E4A0FCE1`
**Stage:** `G-03 COMPLETE / G-04 APPROVED / IMPLEMENTATION ACTIVE`. The student confirmed the revised SPEC; PLAN contains 39 dispatchable tasks plus the non-dispatch `QA-RELEASE` gate. Same-byte mechanical audit and both reviews are PASS. Two fresh Claude Code sessions completed the current-hash intake and disposable `F-01S1A` red/green exercise. On 2026-08-03 the student explicitly approved G-04. Formal `F-01S1A` is now implemented and reviewed at `b997fccae5c04cfa08547f5f9a99e8bbbd4f08d8`; later tasks remain incomplete until their own fresh TDD and review evidence exists.

`verified` means current local evidence exists; `planned` means a named active task owns it; `blocked` means a named human/external gate remains; `not-started` means no product evidence exists. This is the only active course matrix. Archived plans are recovery evidence, never PASS evidence.

| Hard requirement | Active mapping | Status / current evidence | Closure |
| --- | --- | --- | --- |
| Real useful problem explainable in 30 seconds | SPEC 1.1--1.3 | verified document | implementation evidence after G-04 |
| At least three clear modules | M1 materials, M2 learning, M3 review | verified specification; not implemented | M1-01--03, M2-01--04, M3-01--02 |
| At least five INVEST stories | US-01--US-08 | verified document; current-hash SR-08 revalidation pending | implementation evidence after G-04 |
| Module contracts and objective acceptance | SPEC 3 and AC-01--24 | planned; each AC mapped in PLAN 12 | named task/gate per AC |
| Architecture/data flow/data model | SPEC 6--7 | planned | F-02/03, feature repositories, API-01--03 |
| Performance/reliability/errors/observability | SPEC 5 | planned | F-04, API-03, QA-RELEASE, DIST-01 |
| Input validation and safe deletion | SPEC 3.1 and 8 | planned | M1-01--03, API-01, UI-03/06 |
| Host/Origin/CSRF/session boundary | local plus explicit public profile | planned | F-04 and DEMO-01 positive/negative tests |
| Secret never enters DB/config/log/browser/Git | WinVault plus fail-closed scanner | F-01S1A single-path provider rule verified; full scanner and credential lifecycle remain incomplete | F-01S1B--S4, F-01E/F-05 and every-task protocol |
| First-run hidden credential status/update/clear | value-free settings contract | planned | F-05, API-03, UI-06, DIST-01 real lifecycle |
| Optional model is consent-bound and non-authoritative | L+P; mock default; exact text fragments only | P-only evidence verified; adapter not started | P-01/P-02/API-02/UI-04 |
| No autonomous-agent overclaim | v1 has constrained request ports, no autonomous loop | verified specification boundary | P-01/P-02 contract tests |
| Usable WebUI | import, mapping, learning, review, settings | planned | UI-01--06 |
| Open Design workflow | `frontend-design`, `default`/Neutral Modern selected; environment PASS | partially verified | actual run/artifact/evidence in UI-01 |
| Responsive/keyboard/accessibility | 360/768/1440, visible focus, axe | planned | each UI task red/green plus QA-RELEASE |
| At least one reproducible distribution | Windows x64 single file and OCI mock demo | exact inputs verified; products not started | DIST-01/02; registry/pull closes at EXT-REMOTE-PREP |
| Windows cold start <=10 seconds | clean reference VM contract | not-started; named environment gate | DIST-01-VM-CLOSE measured receipt |
| Linux/amd64 dependency/base evidence | separate CI/demo hashed locks and OCI digests | verified planning input: 41 CI, 14 demo | F-01A exact-lock sync; DIST-02 build/SBOM/smoke |
| Public HTTPS WebUI URL | immutable mock OCI image | blocked on student D-025 | D-025-HOST-CLOSE then DOC-01 |
| One-command tests | `python scripts/test_all.py` | not-started | F-01E; QA-RELEASE observes full pass |
| Core automated tests | domain/storage/API/UI/E2E/security/performance | not-started | F-02 through DEMO-01/P-02 |
| Every push runs CI | F-01D seeds pinned scanner/backend/frontend current-suite workflows; CI-01 adds distribution | not-started | EXT-REMOTE-PREP branch-tip current-suite receipts |
| GitLab job exactly `unit-test` | `.gitlab-ci.yml` | not-started | CI-01, final NJU pipeline receipt |
| GitHub repository visibility/access | public repo or private with TA collaborator | blocked on remote authorization | EXT-REMOTE-PREP visibility/collaborator receipt |
| GitHub Actions and PR evidence | workflow plus full-SHA actions | not-started | CI-01, EXT-REMOTE-PREP, EXT-REMOTE-FINAL |
| Final course CI PASS | authoritative NJU GitLab plus mirror evidence on final docs commit | blocked on remote authorization | EXT-REMOTE-FINAL |
| Incremental commits and PR/MR history | 39 task commits, scanned coordinator evidence commits, 9 stacked worktree branches | planned | per-task protocol and EXT-REMOTE-PREP/FINAL sequential retarget-and-merge closure |
| Fresh subagent per PLAN task | one clean session/task | verified for F-01S1A; remaining tasks pending | continue per task |
| TDD red-green-refactor | exact red/green command in all 39 cards; shared assertion-level 2--5 minute step expansion | verified for F-01S1A, including reviewer-driven red/mutation evidence | continue every behavior task |
| SPEC review then quality/security/license review | terminal hash-bound review loop | verified for F-01S1A after initial Major 3 repair; remaining tasks pending | every task protocol; Critical stops sequence |
| Required Superpowers order | brainstorming -> plan -> worktree -> TDD -> reviews -> finish | brainstorming/writing-plans/G-03 evidenced; implementation stages gated | explicit G-04, then task protocol |
| `SPEC.md` required sections | 14 sections, 8 stories, 24 AC, risks/deferred scope | current bytes confirmed by student; same-byte SR-08 PASS | implementation evidence after G-04 |
| `PLAN.md` exact task fields | exactly 39 tasks; dependency/parallel/files/red/green/done in each | mechanical audit and dual review PASS | explicit G-04, then ledger execution |
| Stranger cold start with only SPEC/PLAN | two fresh non-Codex sessions intake then F-01S1A | verified: current hashes, empty ambiguities, exact red, two artifacts, PowerShell 7 green exit 0 | complete; disposable artifacts are not product implementation |
| Cold-start repair then implementation approval | separate post-repair student gate | verified: G-03 complete; student explicitly approved G-04 on 2026-08-03 | local implementation active; remote/release gates remain separate |
| `SPEC_PROCESS.md` process and cold-start diff | sections 1--2 contain >3 real question/answer/revision rounds; later sections retain G-03P/failures/final run | verified: final intake, segmented execution, red/green, hashes, line counts and limitations recorded | continue per-task evidence after G-04 |
| `AGENT_LOG.md` timestamp/task/skill/context/output/hash/human edits/lesson | historical and current entries exist | partial | coordinator evidence commit after every task |
| Student-written code declaration | conditional top-of-file/function comment plus trailer/log | F-01S1A records `Human-Changes: none`; no student-authored code claimed | per-task protocol step 5 |
| README required sections | intro/install/run/distribution/tree/security/credentials/limits/deployment/licenses | not-started | DOC-01 after remote/host receipts |
| Third-party sources/licenses | 63-row ledger, 54 Python/166 npm closure, Linux subset, five immutable bootstrap license rows | verifier now hash/shape-binds bootstrap evidence; products not started | F-01B/F-01E notices, DIST SBOM, DOC-01 final index |
| Student reflection 1500--2500 Chinese characters | AI may review only a supplied student draft | blocked on student | REFLECTION-CLOSE before EXT-REMOTE-FINAL exact final commit/CI |

## Evidence Receipts

- Current mechanical: `PLAN_MECHANICAL_PASS Tasks=39 Ledger=39 Fields=5 AcRows=24 Placeholders=0 Unknown=0 Self=0 Cycle=0 DependencyEdges=38` against SPEC `AEA67BB5...E8381` / PLAN `910A3AEC...9E923`.
- Current SR-08 revalidation: same-byte SPEC review and quality/security/license review both returned `Critical=0, Major=0`. Current evidence includes fixed acceptance ID, Bash-only execution, exact ordered tool-use/tool-result evidence, pre-key live bubblewrap checks, cleared child environment, bounded output, contract mutation replay, and a coordinator behavior oracle. Minor follow-ups (CR-only line counting, unknown tool event negatives, and direct runtime over-limit test) are recorded as non-blocking hardening items; no product PASS is inherited.
- Historical Stage B reviews: `/root/plan_spec_review` and `/root/plan_quality_review` both returned `PASS; Critical=0, Major=0, Minor=0` against SPEC `79579162...7862` and PLAN `6FDD69...A05D`; these verdicts do not transfer to current bytes.
- Failed reviews: the first pair returned `Critical=0, Major=3, Minor=2` and `Critical=1, Major=10, Minor=1` against SPEC `600395...ED71` / PLAN `8A4BE...AFD`. The second pair returned `Critical=0, Major=3, Minor=0` and `Critical=0, Major=6, Minor=2` against SPEC `69A534...855E` / PLAN `47624A...225A`. Findings were repaired but verdicts are not reused.
- Current G-03P remediation: fresh projectless task `019fa331-3da1-7f80-a37c-ac7abb135a46` used SPEC `6A0DB7...11E56` / predecessor PLAN `D574B8...1D742`, produced exact missing-scanner red and eight-group green with eleven helpers, then its optional self-scan found `credential_assignment` in both contract sources. Final PLAN `E96C...` makes exact `files=4` self-scan cleanliness mandatory; focused dual review passed. This remains same-family evidence and does not close G-03.
- Formal G-03 incomplete attempt: Claude Code session `71a50d25-4cd7-48b1-9472-8107e82779ed` used `claude-sonnet-5`, final SPEC/PLAN hashes, and an initial two-file directory. It reported those hashes, then created only an empty `scripts/tests` directory and returned an empty `end_turn`; CLI exit 0, no permission denials, about `$0.4712`, no scripts/diff/red/green/self-scan. Runner postconditions now reject this as `required_artifact_missing`; G-03 remains open.
- Formal G-03 gateway timeout: Claude Code session `32b62490-7817-4d3d-8452-7a29a4de94ea` used `claude-sonnet-4-6`, final hashes, and an initial two-file directory. It verified the hashes, then the gateway returned `504 Gateway Time-out`; CLI exit 1, about `$0.1818`, no scripts/diff/red/green/self-scan. G-03 remains open.
- Bootstrap licenses: official GitHub Contents/Refs API resolved five immutable texts; task ownership correction changed evidence SHA-256 to `FD65C5D2F8421F7B99AE4D540B80A8BBED1C28C78EF45851F7C6E5051034F310`. The standard verifier binds this raw hash and all five immutable row identities; the stale-hash red and corrected green were both observed while the standard receipt stayed at 63 rows.
- Standard: `EVIDENCE_VALIDATION_PASS rows=63 explicitly_blocked=2 python_pins=54 npm_packages=166`.
- Linux supplement: `LINUX_EVIDENCE_PASS ci_packages=41 demo_packages=14 license_rows=41`.
- P-only provider: `PROVIDER_V1_P_EVIDENCE_PASS rows=7 models=2 expires=2026-08-25`; evidence SHA-256 `35A3F46E036563E3FC681DF3190EB56336AB48B9D9817AD48F4D5DF42230F076`.
- Strict distribution remains expected to fail only on the two D-025 hosting rows. No product test/build/package/CI/provider-call/deployment evidence exists.

## Deferred Boundary

OCR/image/scanned-PDF/bulk ingestion, remote whole-file F and durable jobs, past-exam/teacher-focus intelligence, and rubrics beyond mutex/race/deadlock are only in `archive/deferred-v2`. They cannot satisfy current rows or enter v1 acceptance without a new brainstorming, SPEC confirmation, and plan.
