# Superpowers Writing-Plans Validation

**Status:** ACTIVE REMEDIATION / NOT PASS

**Gate:** `PLAN.md` has not passed the formal `superpowers:writing-plans` gate. G-03 cold-start execution and all formal implementation tasks remain prohibited.

> **2026-07-25 scope-reset note:** All review records below apply to superseded plan bytes now indexed under `docs/archive/`. The current root `PLAN.md` is intentionally a non-dispatchable stage ledger while the reduced `SPEC.md` awaits student confirmation. No old subsystem PASS carries into the reduced scope. After signature, a new formal `writing-plans` invocation and same-snapshot reviews must create the only active implementation-plan evidence.

## Invocation and audit baseline

The `superpowers:writing-plans` skill was formally invoked for this self-review: its complete current `SKILL.md` was read and its required header, plan-location override, file map, task granularity, complete-code, exact-command, no-placeholder, scope-check, and self-review rules were applied to the plan.

This invocation proves that the audit occurred. It does **not** prove that the audited plan was originally generated in compliance with the skill, does not retroactively repair the plan, and is not a revalidation of any PLAN edits currently in progress.

Audit inputs:

- Specification: `E:\Personal_Documentary\ResearchProjects\ProjectB\SPEC.md`
- Audited plan: `E:\Personal_Documentary\ResearchProjects\ProjectB\PLAN.md`
- Writing-plans skill: `C:\Users\22078\.codex\plugins\cache\openai-api-curated\superpowers\11c74d6b\skills\writing-plans\SKILL.md`
- Project rules: `E:\Personal_Documentary\ResearchProjects\ProjectB\AGENTS.md`
- Course requirements: `E:\Personal_Documentary\ResearchProjects\ProjectB\docs\requirements\项目要求.md` and `E:\Personal_Documentary\ResearchProjects\ProjectB\docs\requirements\AI4SE_Final_Project_B_应用类项目.md`
- Audited PLAN SHA-256: `7524AE6352733A4EE96B9BA5DED453CEE2A635348664C4AE6127F446B3CAD0BD`

All counts and line references below apply only to that PLAN hash. A different hash is an unreviewed revision until the full revalidation section is executed and recorded.

## Reproducible baseline counts

| Measure | Audited result | Method / interpretation |
| --- | ---: | --- |
| Dispatch units | 69 | `### Task ...` headings excluding `Task Group` |
| Non-dispatch Task Group headings | 17 | Planning containers only |
| Total task headings | 86 | 69 dispatch units + 17 containers |
| Checkbox steps | 343 | Mechanical `- [ ]` / `- [x]` count |
| Dispatch units with no fenced code block | 45 | Mechanical per-unit fence scan |
| Dispatch units with at least one fenced block | 24 | 69 minus 45 |
| Dispatch units with complete code for every code-changing step | 0 | Manual line-by-line review of all 69 units |
| Angle-bracket scan matches | 83 | Mechanical `<[^>]+>` scan surface |
| Actual placeholder-token matches within those 83 | 80 | Manual classification; excludes one literal `<input type="password">` and two comparison-expression false positives |
| Non-placeholder angle matches | 3 | One HTML element plus two inequality-related matches |
| Literal case-insensitive word `placeholder` | 9 | Lexical count; not every use is itself a replaceable token |

The 83-result scan is intentionally reported as a mechanical scan, not as 83 independently classified placeholder defects. The classified placeholder-token result is 80.

## Required checklist and current result

| Writing-plans requirement | Result | Reproducible evidence |
| --- | --- | --- |
| Required plan header | **FAIL** | `PLAN.md:1`, `:3`, `:5`, `:7`, and `:9` contain the title, worker note, Goal, Architecture, and Tech Stack, but the required `---` does not immediately follow the header. `PLAN.md:9` also explicitly calls the stack “architecture placeholders”. |
| Required plan location | **PASS** | The skill default is `docs/superpowers/plans/...`, but the explicit course/project override requires root `PLAN.md`; the user override has priority. This PASS applies only to location, not content. |
| File structure and responsibility map before tasks | **FAIL** | A map exists at `PLAN.md:56`, but it is not exact or internally consistent. `PLAN.md:64` names `application/materials.py`, while tasks create `consent.py`, `material_inspection.py`, `material_import.py`, and `source_context.py` (`:766`, `:888`, `:959`, `:1037`). `PLAN.md:72` offers `ProjectB.spec` or a manifest while `DIST-01` selects `freezer-manifest.json` at `:1855`. |
| Each dispatch unit has goal/files/dependencies/completion metadata | **PASS** | Structural scan found all 69 dispatch units contain Goal, Files, dependencies/parallelism, and Completion standard fields. This is a skeleton PASS only. |
| Each step is one 2-5 minute action | **FAIL** | The 343 checkboxes repeatedly combine implementation, focused tests, regression, and refactor, or combine scan/add/diff/commit. Representative units: `T-03A` at `PLAN.md:608`, `M3-02A` at `:1744`, `API-01A` at `:2267`, and `QA-02C` at `:3442`. |
| Complete code in every code-changing step | **FAIL** | 45/69 dispatch units have no fenced code block. The remaining 24 contain only partial tests/commands; none supplies complete content for every created/modified code file. `T-01` at `PLAN.md:463` omits imports and most listed files; `T-02` at `:549`, `T-03A` at `:608`, `API-01A` at `:2267`, and `UI-01A` at `:2680` substitute prose for code. |
| Exact file paths, commands, and expected results | **FAIL** | Many paths are exact, but parent/child paths conflict. QA uses both `frontend/tests/e2e` (`PLAN.md:3239`) and `frontend/e2e` (`:3294`), and both `backend/tests/perf` (`:3348`) and `backend/tests/performance` (`:3402`). Vague commands remain at `:2268`, `:2699`, and `:3426`. The G-04 commands at `:393` do not implement the nonzero fail-closed result claimed at `:398`. |
| TDD red-green-refactor and frequent commit discipline | **FAIL** | The global protocol at `PLAN.md:76` and per-unit commit intent are present, but unit checkboxes collapse Green and refactor, frequently omit complete runnable red-test code, and combine multiple verification/commit actions. Intent is not executable compliance. |
| No placeholders or unspecified equivalents | **FAIL** | `PLAN.md:9` retains “or the exact verified equivalents”; `:72` retains an alternative freezer form; runtime placeholders appear at `:86`, `:402`, `:1864`, and `:2148`; `:3267` retains “axe or the verified accessibility equivalent”. The mechanical/classified counts are recorded above. Truthful `not executed` evidence states are not placeholders and must remain truthful until executed. |
| Scope check / separate plans for independent subsystems | **FAIL** | One 3,447-line plan contains 69 dispatch units and 17 independent planning groups spanning gates, foundation, materials, provider lifecycle, learning, review, API, UI, demo, QA, distribution, CI, documentation, and release. The skill requires separate plans when independent subsystems are present. |
| Self-review: SPEC coverage | **PASS, lexical only** | AC-01 through AC-50 all occur in the audited plan. This proves identifier coverage, not implementable behavioral coverage; incomplete code steps prevent a substantive PASS. |
| Self-review: placeholder scan | **FAIL** | The audited plan retains the placeholder/alternative findings above. |
| Self-review: type/path consistency | **FAIL** | The file-map, parent/child task, E2E, performance-test, and freezer path conflicts above remain unresolved. |
| Overall writing-plans gate | **NOT PASS** | Any required FAIL keeps the gate closed. |

## Active remediation target

The remediation must produce a plan set that a fresh worker can execute without inventing code, paths, commands, expected outcomes, dependencies, or tool choices. At minimum it must:

1. Preserve root `PLAN.md` as the course-required status/dependency entry point and split independent subsystems into linked, independently testable implementation plans when necessary.
2. Give every implementation plan the exact required header followed by `---`.
3. Replace every selected-stack alternative and replaceable token with a locked choice or an exact executable runtime mechanism; keep genuinely unresolved external decisions as explicit blockers, not implementation placeholders.
4. Establish one canonical `path | owner dispatch unit | create/modify | responsibility` manifest and make group/child task paths agree with it.
5. Expand every dispatch unit into separate 2-5 minute checkboxes for complete failing-test code, exact red command and expected failure, complete minimal implementation code, exact green command and expected result, refactor, focused regression, full regression, both reviews, credential scan, staged-diff check, commit, and evidence/hash recording.
6. Run the skill's final self-review for SPEC coverage, placeholder removal, and type/signature/path consistency over root `PLAN.md` and every linked subplan.

No in-progress PLAN edit is treated as satisfying any item above. The final review must bind its evidence to the new final PLAN/subplan hashes.

## Current remediation snapshot

The first remediation pass has corrected the required header, locked dependency versions, G-03 gate wording, G-04 on-demand worktree semantics, and several SPEC/PLAN coverage gaps. This is progress evidence only, not a replacement for the audited baseline above and not a formal revalidation.

Snapshot after the prelude repair:

- PLAN SHA-256: `C0C4B4C8FEA158AA4758C8A055F9266E243DE69FF4CC5DF97FE44AE7F5176C55`
- Dispatch units: 72
- Non-dispatch Task Group headings: 17
- Dispatch units with no fenced block: 48
- Dispatch units with fewer than five checkbox actions: 70
- Classified angle-bracket placeholders before T-01: 0
- Overall result: **NOT PASS**

The remaining plan work is tracked by responsibility rather than by raw line count:

| Plan responsibility | Dispatch units | Current state |
| --- | --- | --- |
| Process gates | G-01, G-02A, G-02B, G-02C, G-03, G-04 | Prelude repaired; G-02C and G-03 remain truthfully blocked |
| Foundation and security | T-01, T-02, T-03A, T-03B, T-03C, T-04, T-05, T-06, T-07, T-08 | T-01/T-02 detailed replacement fragments in progress; remainder incomplete |
| Materials and provider lifecycle | M1-01, M1-02, M1-03, M1-04, X2-01, X2-02, X2-03A, X2-03B, X2-03C | Skeleton only; incomplete |
| Learning loop | M2-01, M2-02A, M2-02B | Skeleton/partial examples only; incomplete |
| Review planning | M3-01, M3-02A, M3-02B, M3-02C, M3-02D, M3-03 | Skeleton/partial examples only; incomplete |
| HTTP API | API-01A, API-01B, API-01C, API-01D, API-02A, API-02B, API-03A, API-03B, API-03C, API-04A, API-04B | Skeleton only; incomplete |
| WebUI | UI-01A, UI-01B, UI-01C, UI-02A, UI-02B, UI-03A, UI-03B, UI-03C, UI-04A, UI-04B, UI-05A, UI-05B | Skeleton only; incomplete; no Open Design run is authorized yet |
| Demo and delivery | DEMO-01A, DEMO-01B, DEMO-01C, DIST-01, DIST-02 | Skeleton/partial examples only; host-specific work remains gated by D-025 |
| Verification and release | QA-01A, QA-01B, QA-01C, QA-02A, QA-02B, QA-02C, CI-01, DOC-01, INT-01, FIN-01 | Skeleton/partial examples only; incomplete |

The scope check will be closed by keeping root `PLAN.md` as the course-required dependency/status entry point and moving complete executable task bodies into linked subsystem plans under `docs/plans/`. A linked plan is not normative until its own required header, complete-code review, placeholder scan, path/type consistency review, and hash are recorded here. Temporary drafting fragments are archived under `docs/archive/` and must not be dispatched.

### Stable-snapshot dispatch audit

An independent read-only audit reran against the same `C0C4B4...F5176C55` snapshot after the prelude editor stopped. It found `72` ledger rows, `0` unknown dependencies, `0` ledger self-references, and `0` ledger cycles. The dependency graph is mechanically coherent, but the task bodies and release ownership are not yet executable:

- 66 implementation units fail the complete-code and atomic-step requirements; 65 have no implementation code block and 56 have no explicit Green PASS expectation.
- All four G-03 candidate units have known, non-semantic plan defects. T-02 used an invalid short hash fixture; M2-01 and M3-01 referenced undefined test helpers/imports; API-01A had no code block. These known defects must be fixed before a cold-start agent is asked to find higher-level ambiguity.
- No dispatch unit owns a real remote dual-CI observation or a real public deployment. `CI-02` and `DEPLOY-01` (or equivalently explicit, separately owned authorization-gated units with those exact responsibilities) must exist before FIN can depend on same-commit external evidence.
- FIN currently verifies one HEAD and then changes the files/ledger, invalidating the verified SHA. It must be split into verifier preparation, an immutable release-candidate commit, external evidence bound to that commit, and a final read-only attestation that does not mutate the candidate.
- Shared API route registration lacks a unique worker owner. Feature units must stop editing the registry concurrently; a serialized registry/integration unit must own that file.
- The status ledger needs distinct Red, Green, SPEC-review, quality-review, commit, and AGENT_LOG evidence fields. A combined prose review checkbox is not auditable evidence.
- The T-01-and-later surface still contains 69 classified runtime tokens, including agent identity, task ID, temporary directory, and SHA forms. Exact validated variable assignment must replace those tokens.

These are remediation findings, not completed edits. Semantic questions that remain after these mechanical defects are fixed are appropriate inputs to G-03; missing code, invalid fixtures, missing owners, and SHA cycles are not.

### Ownership and evidence-graph repair snapshot

The coordinator then applied the stable-snapshot ownership findings. The revised root plan is bound to SHA-256 `323B5B97472FD6AB03F7119DA663EF74D7B5B8CB0067ECC04CE45553CFDBDBE9` and contains 77 dispatch units plus 18 non-dispatch planning containers.

Fresh mechanical results for that hash:

- Ledger IDs and task-body IDs: 77 / 77, exact set equality, no duplicate.
- Declared dependencies: zero unknown IDs, zero self-reference, zero cycle.
- Shared core/demo registry commit owners: `API-REG-01` and `DEMO-REG-01` only; zero feature-unit registry commit violation.
- Remote evidence owners: `CI-02` for same-candidate GitLab/GitHub observation and `DEPLOY-01` for publication/deployment/external-browser/rollback evidence.
- Release chain: `FIN-01A` prepares verifier/templates before immutable candidate `C`; `CI-02` and `DEPLOY-01` observe `C`; `FIN-01B` is read-only; coordinator evidence commit `E` is allowlisted and the course-final NJU CI observes `E`. No commit is required to contain its own object ID.
- Ledger evidence fields: Red, Green, SPEC review, quality review, worker commit, coordinator log, and detailed-plan/hash are separate columns. Unknown execution evidence remains `尚未执行`; absent formal detailed-plan approval remains `尚未通过`.
- Root-plan fenced-block result: 53 units with no fence; 75 units with fewer than five checkbox actions. The increase from the earlier snapshot reflects newly explicit owner/evidence units, not a regression in already detailed task bodies.
- Overall result: **NOT PASS** because the linked detailed plans are not complete or approved.

T-01 and T-02 currently point only to draft/unreviewed fragments with hashes `96615368978764AC166D614372DE9C4388404BFD999C8FC28EF5E15ADA82923F` and `F37B3F72926FB0B52C65EADC346894BD017CFB7D952E397907A8B03DCF1D25EB`. Those links are discovery metadata, not formal plan PASS. All other detailed-plan cells remain `尚未通过`.

### First detailed-fragment review

An independent fresh reviewer read the complete writing-plans skill, both fragments, their SPEC/PLAN contracts, and the G-02A baseline. The review is bound to the two hashes above and returned **FAIL** for both drafts. Syntax parsing passed for the Python, PowerShell, JSON, TOML, and JavaScript blocks, but syntax was not mistaken for behavioral compliance.

Critical/Major findings requiring a new review hash:

- T-01 has no tested later-gate registry, can trust weakened npm scripts/test discovery, omits `.test.ts`, and uses `git diff` on untracked generated locks, which can return a false clean result.
- T-01's secret scanner treats NUL-containing UTF-16 text as binary and skips it instead of decoding or failing closed.
- T-02 permits unversioned/invalid `MaterialLimits` values and does not enforce enum-typed authority fields at runtime.
- T-02 uses worker self-review rather than two different fresh reviewers, retains a replaceable worker identity, and maps unrelated AC identifiers.
- T-02's package layout and proof signature conflict with the root plan and therefore require a coordinator-owned root-plan update before dispatch.
- T-02's declared Ruff/mypy commands and code do not match the selected B/UP rules or explicit backend config.
- Both drafts contain code-changing steps far larger than the required 2--5 minute action size.

Drafting of M2-01/M3-01 was stopped when these Critical issues arrived. The partial `docs/engineering/plan_fragments/M2-01.md` is explicitly marked `INCOMPLETE DRAFT - DO NOT DISPATCH`, is not linked from the ledger, and is not evidence of progress toward a detailed-plan PASS.

### Second detailed-fragment review and decomposition decision

The repair drafts were frozen before review at these SHA-256 values:

- T-01: `33D67D3BE30528B0174BC43C5593D003228A980164A44379191790681C8468BB`
- T-02: `889AA9C9FDF24C6B376A15529D8C7510BEA7C674DA0744E9908CDC6D0D3C6D94`

Two independent findings-first reviewers and one mechanical reconstruction audit rechecked those exact bytes. The result remains **FAIL**. Positive evidence is limited to required headers, balanced fences, parseable displayed code, raw-lock hashes, and closure of several first-review findings; it is not implementation or product-test evidence.

Blocking findings on the frozen hashes:

- Both fragments are too large for one fresh worker: T-01 combines 42 paths and 82 checkbox steps; T-02 combines 13 paths and 63 steps. Each contains multiple independently testable/committable contracts, violating the course dispatch-unit rule and root PLAN's own split-before-dispatch rule.
- Root `PLAN.md` still owns the old T-01/T-02 file sets, signatures, commit scopes, ledger links, and hashes. T-02 correctly labels itself not dispatchable; T-01 did not provide an equivalent pre-dispatch atomic-sync gate.
- T-01's scanner excludes project text formats such as `.lock`, `.sql`, and `.sh`, has only lexical containment rather than a reparse/symlink boundary, and does not fail closed on unmarked NUL-bearing text. Its Ruff/mypy commands can miss `backend/pyproject.toml`, and its Vite check can be satisfied by comments/dead text.
- On the Windows target, the displayed Python subprocess registry passes bare `npm`; the mechanical reviewer reproduced `FileNotFoundError` where `npm.cmd` resolution is required. The deferred browser gate also calls an absent `e2e` package script, and G-02C does not own its declared ready marker.
- T-02 does not strictly validate catalog container/member types, can split a string into image IDs or leak `AttributeError`, and reports 21/72 expected tests where mechanical reconstruction actually produces 23/74.

The coordinator therefore rejected further in-place patching. The old fragments remain immutable failure evidence and are never dispatch inputs. The active repair is to create formal subsystem plans under `docs/plans/` and atomically split root tasks as follows:

- T-01A through T-01F: toolchain/raw lock, backend health, frontend/lock materialization, scanner, runner contracts, and gate registry/canonical entry.
- T-02A through T-02C: common errors/IDs/material primitives, source hashing/locator/catalog, and proof/public facade.

Root `PLAN.md`, the two new subsystem plans, their ledger hashes, and all downstream terminal dependencies must be reviewed as one snapshot. Until that review passes, neither the old fragments nor the new paths satisfy Stage B.

## Read-only revalidation commands

Run from `E:\Personal_Documentary\ResearchProjects\ProjectB`. These commands read files and print or throw; they do not modify the workspace.

### 1. Hash and required header

~~~powershell
$plan = 'PLAN.md'
(Get-FileHash -Algorithm SHA256 -LiteralPath $plan).Hash
$raw = Get-Content -Raw -Encoding utf8 -LiteralPath $plan
$headerPattern = '(?ms)\A# .+ Implementation Plan\r?\n\r?\n> \*\*For agentic workers:\*\*.+?\r?\n\r?\n\*\*Goal:\*\*.+?\r?\n\r?\n\*\*Architecture:\*\*.+?\r?\n\r?\n\*\*Tech Stack:\*\*.+?\r?\n\r?\n---\r?\n'
if ($raw -notmatch $headerPattern) { throw 'WRITING_PLANS_HEADER_FAIL' }
'WRITING_PLANS_HEADER_PASS'
~~~

### 2. Dispatch, group, checkbox, and fence counts

~~~powershell
$raw = Get-Content -Raw -Encoding utf8 -LiteralPath 'PLAN.md'
$units = [regex]::Matches($raw, '(?ms)^### Task (?!Group )(?<id>[^:]+):(?<body>.*?)(?=^### Task |\z)')
$groups = [regex]::Matches($raw, '(?m)^### Task Group ')
$noFence = @($units | Where-Object {
    [regex]::Matches($_.Groups['body'].Value, '(?m)^\s*(?:~~~|```)').Count -eq 0
})
$checkboxes = [regex]::Matches($raw, '(?m)^\s*- \[[ xX]\]').Count
[pscustomobject]@{
    DispatchUnits = $units.Count
    TaskGroups = $groups.Count
    Checkboxes = $checkboxes
    UnitsWithoutFence = $noFence.Count
    UnitsWithFence = $units.Count - $noFence.Count
}
$units | ForEach-Object {
    $fences = [regex]::Matches($_.Groups['body'].Value, '(?m)^\s*(?:~~~|```)').Count
    [pscustomobject]@{ Unit = $_.Groups['id'].Value.Trim(); FenceLines = $fences }
}
~~~

Fence counts cannot prove code completeness. A reviewer must still inspect every code-changing checkbox and record that the displayed code is complete for every listed file; the final acceptable incomplete-unit count is zero.

### 3. Placeholder scan and classification surface

~~~powershell
$raw = Get-Content -Raw -Encoding utf8 -LiteralPath 'PLAN.md'
$angleMatches = @([regex]::Matches($raw, '<[^>]+>'))
$placeholderTokens = @($angleMatches | Where-Object {
    $_.Value -ne '<input type="password">' -and $_.Value -notmatch '^<\s*(?:=|\d)'
})
[pscustomobject]@{
    AngleScanMatches = $angleMatches.Count
    ClassifiedPlaceholderTokens = $placeholderTokens.Count
    LiteralPlaceholderWord = [regex]::Matches($raw, '(?i)\bplaceholder\b').Count
}
$placeholderTokens | ForEach-Object Value | Group-Object | Sort-Object Count -Descending
rg -ni 'TBD|TODO|implement later|fill in details|Similar to Task|architecture placeholders|exact verified equivalents|or verified freezer manifest|or the verified accessibility equivalent' PLAN.md
if ($placeholderTokens.Count -ne 0) { throw "WRITING_PLANS_PLACEHOLDER_FAIL count=$($placeholderTokens.Count)" }
~~~

If plans are split, repeat the same scan for every linked implementation-plan file. Legitimate HTML and mathematical comparisons must be classified explicitly rather than silently ignored.

### 4. Representative path-consistency scan

~~~powershell
rg -n --pcre2 'frontend/(?:tests/e2e|e2e)|backend/tests/(?:perf|performance)|ProjectB\.spec|freezer-manifest\.json|application/(?:materials|consent|material_inspection|material_import|source_context)\.py' PLAN.md
~~~

This command lists the known conflict surface. Final PASS requires one canonical path per owned responsibility and a manual parent/child/file-map comparison, not merely a zero exit code from `rg`.

### 5. Acceptance-criterion coverage

~~~powershell
$specAc = @(rg -o 'AC-[0-9]{2}' SPEC.md | Sort-Object -Unique)
$planAc = @(rg -o 'AC-[0-9]{2}' PLAN.md | Sort-Object -Unique)
$delta = @(Compare-Object -ReferenceObject $specAc -DifferenceObject $planAc)
if ($delta.Count -ne 0) {
    $delta
    throw 'WRITING_PLANS_AC_COVERAGE_FAIL'
}
"WRITING_PLANS_AC_COVERAGE_PASS count=$($specAc.Count)"
~~~

Lexical AC equality is necessary but not sufficient. The final reviewer must map each AC to complete executable task steps and tests.

### 6. Evidence-file integrity check

~~~powershell
git diff --check -- docs/engineering/WRITING_PLANS_VALIDATION.md
git diff -- docs/engineering/WRITING_PLANS_VALIDATION.md
~~~

## Final PASS conditions

The status may change from `ACTIVE REMEDIATION / NOT PASS` only after all of the following have fresh evidence bound to the final hashes:

- Every root/subplan required header validator passes.
- Every selected file path, interface/type name, command, and expected outcome is exact and consistent.
- Every dispatch unit uses separate 2-5 minute actions and includes complete runnable failing-test and implementation code for every changed file.
- Red, green, refactor, focused regression, full regression, both reviews, secret scan, commit, and hash-recording actions are individually executable.
- Classified replaceable placeholder tokens and unspecified implementation alternatives are zero; truthful `not executed` external evidence remains explicit where applicable.
- AC-01 through AC-50 have substantive task/test mappings, not just lexical references.
- The SPEC coverage, placeholder, and type/path consistency self-review has been rerun across every plan file with no unresolved finding.
- The validation record contains the final plan hashes and does not reuse the audited baseline counts as proof of the repaired version.

Until those conditions are recorded, the formal plan gate remains **NOT PASS**, G-03 remains blocked, and no implementation authorization can be inferred from this skill invocation.

## Replacement snapshot validation (2026-07-23T02:40:20+08:00)

The pre-repair snapshot remains immutable failure evidence:

- Root `PLAN.md`: `5BFE0EA545180AB0CC55FF9217FE7899039992F5DAA2144B20C9E5C95E86065D`
- Foundation draft: `39CA455BCAB42EB36AA9EFEC9A5724BFF0795F3881E6C700B4FABFEDD5574C55`
- Domain draft: `75DA026E6FA72EC55596131B0B2CC57403A9C25E57B6B968D268C55563C61C88`
- Independent frozen reviews: `/root/snapshot_plan_quality` = FAIL and `/root/snapshot_spec_review` = FAIL

The replacement snapshot frozen for this validation is:

- Root `PLAN.md`: `83B9A69272CBF7E831BB386E69AE5376968C931F4188DD23DC2988D8782D6787`
- `docs/archive/superseded-2026-07-23/2026-07-22-foundation-scaffold.md`: `D00496FAAC456AA4CB0E69DE9104BF085C54621D76A199AC456A06601D73E87E`
- `docs/archive/superseded-2026-07-23/2026-07-22-domain-primitives-source.md`: `E01303C74E2EA22C26CCF3C43D6E118C00C3311850D3E321EA781A92DB61BEA5`

Fresh mechanical evidence on those exact hashes:

| Check | Result |
| --- | --- |
| Required header / balanced fences | PASS for all three files |
| Root dispatch units / unique | 113 / 113 |
| Root Task Groups / unique | 37 / 37 |
| Root ledger/body symmetric difference | 0 (the Markdown header row is excluded) |
| Root dependency graph | 113/113 visited; unknown 0; self 0; cycle 0 |
| SPEC/root AC lexical coverage | 50/50; delta 0 |
| Root replaceable placeholder tokens | 0 |
| Detailed-plan angle-token classification | HTML/JSX, regex lookbehind, and mathematical comparisons only; replaceable tokens 0 |
| Foundation displayed PowerShell/Python syntax | 35/35 and 31/31 parsed; errors 0 |
| Domain displayed PowerShell/Python syntax | 77/77 and 45/45 parsed; errors 0 |
| `git diff --check` | exit 0; only Git LF-to-CRLF notices |

These results establish internal mechanical consistency and displayed-code syntax only. They do not execute the proposed product, dependencies, tests, build, scanner, CI, or distribution flow.

Fresh read-only reviews `/root/foundation_snapshot_review` and `/root/domain_snapshot_review` were started on these hashes. The student then requested an immediate computer-restart pause. Both reviewers (and the foundation mechanical child) were stopped before returning a verdict, so no review PASS exists and no finding is silently classified as resolved.

Only the foundation and domain subsystem plans exist in the replacement plan set. The remaining subsystem plans are not yet generated, hash-linked, or independently reviewed. Therefore the formal writing-plans gate remains **NOT PASS**; G-03 and implementation remain prohibited. Resume by rechecking the three hashes and rerunning the two independent reviews, then continue the remaining subsystem plans.

## Post-restart independent review checkpoint (2026-07-23T11:07:28.3604077+08:00)

The stopped reviews were replaced with two fresh read-only reviews against the exact replacement hashes recorded above. Both returned **NOT PASS**; neither reviewer edited the repository.

Foundation review `/root/foundation_snapshot_review_r2` found:

- Critical: every close step queried staged names with a pathspec and then used a whole-index commit, so unrelated staged files or credentials could be committed invisibly.
- Major: the title retained `[Feature Name]`; T-01E2 lacked bounded timeout and malformed/nonzero/fake-wrapper negative tests; package-script validation allowed extra lifecycle scripts; T-01E1 did not reject parent-directory reparse aliases; T-01F1 interface names/output redaction disagreed with root; displayed snippets could not satisfy selected Ruff rules; and the root heading reference was stale.
- Environment boundary: the reviewer observed CPython 3.13.5, Node 24.14.0, npm 11.9.0, Windows PowerShell 5.1, and no target Ruff/pwsh environment, so it made no target-toolchain execution claim.

Domain review `/root/domain_snapshot_review_r2` found:

- Critical: root and child plans disagreed over which unit first creates `source/__init__.py`, and T-02B1 permanently asserted that a symbol later required by T-02C was absent. Mechanical reconstruction of the displayed final code produced 135 passes and that one unavoidable failure.
- Major: unique-page proof could return a page outside a verified catalog count; native commands could mask earlier nonzero exits; identity regexes differed; public error/insufficient constructors could leak unstable exceptions; and root/subplan review scopes drifted.

The coordinator accepted the reproducible findings and did not reinterpret syntax parsing as behavioral PASS. Repair is in progress on new hashes. Root `PLAN.md` now additionally requires fail-closed native commands, whole-index exact staged-set comparison, five T-02 child units, and a complete contiguous 1..N page directory before proof can return a locator. The exact reusable rules are recorded in `docs/engineering/DETAILED_PLAN_AUTHORING_CONTRACT.md`.

An independent partition audit reconciled the final set as 15 dispatch units in the two existing plans, 86 units in 12 additional subsystem plans, and 12 coordinator/human/external units kept in root: `15 + 86 + 12 = 113`. The mapping and serialized shared-file handoffs are recorded in `docs/engineering/PLAN_SUBSYSTEM_PARTITION.md`. Persistence-plan authoring has started; this is drafting evidence only.

The formal gate remains **ACTIVE REMEDIATION / NOT PASS**. No repaired file, new subsystem plan, root change, or process record is linked as PASS until its new hash and same-snapshot independent reviews are recorded.

## R3 same-snapshot review checkpoint (2026-07-23T11:50:37.7529423+08:00)

The coordinator froze root `PLAN.md` at `E8740A7D17723C30DB362C1BFEA24AC10B9A5108AB46EB239DFC236314274CCA` and dispatched three fresh read-only reviewers. All three returned **NOT PASS**; no reviewer edited the repository.

### Foundation R3

Reviewed plan hash: `6B9ADB0999229259772F475057F7D5FB2A67F23E2E86A9581C8F3CEA2D5353A2`.

- Critical: many Python/Node/npm/Git commands still bypassed the checked wrapper; review happened before final staging; commit did not reassert the reviewed whole index; and the scanner's committed test source contained a literal private-key marker that made its own required clean scan fail.
- Major: runtime identity could still be spoofed by output/wrapper behavior and inherited environment, identity values were not regex-validated, and displayed imports violated selected Ruff `UP` rules.
- Closed findings remained closed: concrete title, exact package scripts, full E1 component walk, and the F1 gate names/captured bounded child process.

### Domain R3

Reviewed plan hash: `50F38BF2935FD6596C0388E44E2E3B5DA0A5A35A61AFD78992AB1D4EF5CEB40D`.

- Mechanical reconstruction produced `144 passed`, but strict mypy reported ten unreachable-code errors because runtime foreign-type checks operated directly on already-narrow public annotations.
- The five unit preludes still lacked the full absolute Git/runtime, checked timeout, unit/base/worktree/HEAD contract; displayed import ordering also violated configured Ruff `I001`.
- Earlier ownership, final-export, five-child, page-directory, stable-error, identity-regex, whole-index staging, and separate commit/hash findings were confirmed closed.

### Persistence P01 R1

Reviewed plan hash: `4217FD325A464FFA47196E261659AD85FC806812B30F609DB46B21D61BD3B07E`.

- Critical: the sole migration lacked durable-job lease/payload fields, MaterialBatch state, and protected Attempt persistence required by declared downstream tasks.
- Critical: remote authorization did not require F mode or exact material/hash/role consent scope; awaiting-consent state and revoke-driven cleanup were not representable together; audit values could persist a private path under an allowed key.
- Major: strict mypy exposed an uncast `sqlite3` Any; malformed databases leaked raw SQLite errors; timestamp validation accepted non-canonical forms used in lexical ordering; several code-writing checkboxes covered hundreds of lines rather than 2--5 minutes; and T-03C review omitted remote lifecycle ACs.
- The reviewer reconstructed the displayed package and obtained 26 passes, then added negative probes that reproduced the remote-scope, lifecycle, and audit defects. This is plan-review evidence, not project implementation testing.

All three plans returned to their exclusive authors with the exact findings and no scope expansion. Their next hashes remain unreviewed until the repairs finish and new fresh reviewers bind a verdict to the same root hash. Stage B, G-03, Open Design execution, worktrees, implementation, CI, and deployment remain closed.
## R4/R5 independent review checkpoint (2026-07-23T13:28:52.5541243+08:00)

Reviewed root snapshot: `4BCFE8470DE57C0DD54004935285CAAD5CD9D1AFF0AA7370CC4E098887745F08`.

### Domain R5: PASS

Reviewed plan hash: `40C48BB62A87F17BFCFB635871F51C350EA2EC9F1AAFEE5ED2D9B7A7C7629C0B`.

- Fresh reconstruction produced 144 passing displayed tests; Ruff 0.15.22, mypy 2.3.0 strict, compileall, and PowerShell AST checks passed.
- All five units include complete context validation, checked native commands, exact whole-index staging, reviewer tree binding, re-review on edits, precommit equality, and postcommit `HEAD^{tree}` equality.
- One non-blocking ordering observation remains: T-02B1 captures its tree before the read-only cached diff check and repeats the check before commit. No Critical or Major finding remained on the reviewed hash.
- This is a subsystem-plan PASS only. It does not close Stage B or permit dispatch while the final root/14-plan set and G-03 remain incomplete.

### Foundation R4: NOT PASS

Reviewed plan hash: `837F1E71CDA4542898631EC441E3469ECB235B55F8CB024EF33F9AA8DF665A59`.

- Critical: displayed E1/E2 blocks omitted required imports; the final package would fail collection/execution.
- Critical: unit/base/worktree/Git-root/HEAD metadata was not validated for each dispatch.
- Major: executable identity could still be self-authorized from mutable environment values; subprocess environment/output were insufficiently sanitized; npm raw-lock byte identity, reparse/TOCTOU containment, exact 40-hex IDs, bare-tool removal, Ruff cleanliness, and descendant process cleanup were incomplete.
- The previous scanner, exact-index, tree-binding, E1 component-walk, E2 script-map, and F1 name/capture findings remained closed. The exclusive author is repairing the new findings; no review result carries forward to the changed bytes.

### Persistence P01 R2: NOT PASS

Reviewed plan hash: `2F67280FED1C7F5337837B5CB08E9099F09D5236A19B124B2D3C007C301B8810`.

- Critical: a revoked object could regain a scope token after `delete_requested -> delete_incomplete`; the reproduced probe returned `revoked_scope_reintroduced=True`.
- Critical: reason-only `tombstone_object` could mark an object deleted without validated provider deletion evidence.
- Major: reconstructed code failed Ruff 0.15.22 with 50 diagnostics and mypy 2.3.0 with one redundant cast; the migration accepted a non-hex 64-character hash and `not-utc`; representative code-writing checkboxes remained 350, 154, and 149 lines; root T-03C AC scope omitted AC-25--31/50; native timeouts and exact staged-content review packet binding were incomplete.
- Closed R1 findings stayed closed: durable job leases/payloads, material batch/file state, protected Attempts, exact F/material/hash/role consent matching, safe initial awaiting-consent, bounded audit values, redacted migration errors, and canonical repository-layer UTC validation.
- Reconstruction evidence was 183 passing displayed tests, compileall PASS, and 36 PowerShell blocks with zero parse errors. These results do not override the lifecycle, schema, static, and granularity failures.

All subsequent authors must add bounded process-tree native execution, sanitized diagnostics, and a private hash-bound staged diff packet after the staged scanner. Both reviews must bind that packet and the checked tree ID; any edit invalidates both. Stage B remains **ACTIVE REMEDIATION / NOT PASS**.
