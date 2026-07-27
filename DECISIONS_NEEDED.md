# DECISIONS_NEEDED

> **Current snapshot:** 2026-07-27T14:01:29+08:00. This file lists only decisions or student-owned evidence that remain open. The reduced product direction remains confirmed. Current remediation candidate is SPEC `69A534D9...855E` and PLAN `47624A3E...225A`; previous review verdicts are historical or failed, and current bytes are not dispatchable until fresh dual review, formal G-03, and G-04.

## D-025: Public OCI Demo Host

**Status:** Open, but not a blocker for SPEC confirmation, plan authoring, cold start or host-neutral local implementation. It blocks host-specific release work and the required public HTTPS URL.

**Confirmed conflict:** The previously selected Hugging Face Docker Space route requires an eligible paid plan and is incompatible with the current no-paid-resource authorization.

**Options retained for later decision:**

1. Use an existing student/NJU-controlled x64 Docker host with existing HTTPS or an explicitly accepted Tailscale Funnel boundary.
2. Use Azure for Students plus Azure Container Apps Consumption, subject to eligibility, explicit resource authorization and no pay-as-you-go upgrade.
3. Explicitly authorize a paid Hugging Face plan and a recurring cost ceiling.

No account, payment method, cloud resource, image push or deployment may be created before the student selects a route and authorizes the corresponding external action.

## G-03: Different-Type Cold Start

**Status:** Open. Claude Code was rejected by the available service path, Gemini currently requires an unavailable special relay, and Copilot is not provisioned. Any newly accessible non-Codex coding agent may be used; the student controls its account, login and terms.

**G-03P receipt:** The first projectless Codex task completed the earlier scanner slice with real red/green and exposed plan ambiguity. Subsequent security review found that version did not prove index-blob scanning, so its 12-group green is historical only. F-01S now includes exact index/worktree regressions; two projectless reruns are waiting on the desktop's cross-directory read approval and no new pass is claimed.

**Remaining student-owned action:** When one non-Codex service becomes usable, follow [`docs/cold-start/G-03_CLAUDE_CODE_RUNBOOK.md`](docs/cold-start/G-03_CLAUDE_CODE_RUNBOOK.md) in a fresh session with no memory and provide only the final `SPEC.md` plus `PLAN.md`. Record the tool/version/session and return its exact questions, misunderstandings, diff and red/green receipt. Do not supply G-03P output as a third context file.

The current SPEC/PLAN bytes need fresh same-hash dual review. Neither old review, the failed review, nor G-03P authorizes implementation.

## Future Implementation Approval

**Status:** Not yet requestable. It becomes available only after:

1. the reduced SPEC is confirmed;
2. `writing-plans` produces a reviewed implementation PLAN;
3. a different-type coding-agent cold start is completed;
4. exposed SPEC/PLAN defects are repaired and reviewed.

The student must then explicitly approve entering implementation. No earlier `continue` statement is reused as this approval.

## External Execution Authorizations

These are deferred until their PLAN tasks are ready and remain separate approvals:

- create or configure NJU Git/GitLab and GitHub repositories;
- push branches, create PR/MR, or mirror commits;
- observe remote CI as final evidence;
- publish an OCI image or Windows release artifact;
- create cloud resources or deploy the public WebUI;
- perform an explicitly bounded live OpenAI integration observation.

Local implementation, mocks, tests and builds do not imply permission for these external actions.

## Student-Written Process Evidence

The student still needs to provide, in their own words:

- which brainstorming questions genuinely helped;
- which parts felt redundant or overly formal;
- the most important product or engineering trade-off;
- the final 1500--2500 Chinese-character `REFLECTION.md`.

AI must not draft or conceal authorship of `REFLECTION.md`. After a student draft exists, AI may proofread or identify argument gaps and must disclose the assistance scope.

## Resolved Decision Index

| IDs / topic | Resolved outcome |
| --- | --- |
| D-001 | Superpowers installed, enabled and callable; 14 skills detected; formal `writing-plans` invocation previously occurred |
| D-002, D-006, D-007 | Single-user course-learning workbench; first validation domain is operating-systems concurrency |
| D-008--D-010 | Local-first Windows x64 WebUI and explicit user-controlled material handling |
| D-011--D-012 | Understanding plus ongoing/finals review loop |
| D-013 | v1 has constrained model ports and no autonomous agent loop |
| D-015--D-018 | One provider-neutral boundary, built-in OpenAI adapter, no arbitrary endpoint/plugin |
| D-020--D-023 | Deterministic planning; Windows single-file plus OCI demo; synthetic/licensed public fixtures; GitLab primary plus GitHub mirror |
| D-024 | Open Design `frontend-design` plus `default` / Neutral Modern selected |
| 2026-07-25 scope reset | Reduced v1; input PDF/TXT/Markdown; modes L+P; generic concept model with mutex/race/deadlock acceptance; deferred capabilities archived |
| 2026-07-25 reduced SPEC signature | Student explicitly confirmed the complete `C6231816...9AD6` content snapshot; `writing-plans` is now authorized, but cold-start repair and implementation approval remain later gates |

## Engineering Checks That Are Not Student Decisions

Dependency licenses, exact toolchain materialization, provider capability/policy refresh, parser and package compatibility, secret scanning, clean-machine build, browser evidence, CI schema and performance measurements remain engineering verification tasks. A failed check may require a later SPEC change, but it must not be presented as a product choice unless it actually changes user-visible scope, cost or external authority.
