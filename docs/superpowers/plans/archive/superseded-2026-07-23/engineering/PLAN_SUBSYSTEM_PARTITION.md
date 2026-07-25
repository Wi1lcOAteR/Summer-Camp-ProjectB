# Detailed Plan Partition Record

**Recorded:** 2026-07-23T11:03:46.7766942+08:00

**Status:** Stage B planning input only. This record is not a `writing-plans` PASS, implementation approval, cold-start result, review PASS, or execution evidence.

## Count Reconciliation

The current root `PLAN.md` contains 113 dispatch units and 37 non-dispatchable Task Groups. The formal detailed-plan set is partitioned as follows:

- 15 dispatch units in the existing foundation and domain plans.
- 86 dispatch units in 12 additional subsystem plans.
- 12 coordinator, human, or external-evidence dispatch units that remain in root `PLAN.md` and are not converted into implementation-worker plans.
- Reconciliation: `15 + 86 + 12 = 113`, with no intended duplicate or omitted dispatch ID.

No detailed plan becomes normative until its exact hash is linked from the root ledger and an independent SPEC review plus an independent quality/security/license review both pass on the same root/subplan snapshot.

## Detailed Plan Set

| Plan | Dispatch units | Current state |
| --- | --- | --- |
| `2026-07-22-foundation-scaffold.md` | T-01A, T-01B, T-01C1, T-01C2, T-01D, T-01E1, T-01E2, T-01F1, T-01F2, T-01F3 | Existing; independent review returned NOT PASS; repair and new-hash review required |
| `2026-07-22-domain-primitives-source.md` | T-02A, T-02B1, T-02B2A, T-02B2B, T-02C | Existing; independent review returned NOT PASS; repair and new-hash review required |
| `2026-07-23-persistence-repositories.md` | T-03A, T-03B, T-03C | Authoring in progress; unreviewed |
| `2026-07-23-local-trust-and-provider-control-plane.md` | T-04A, T-04B, T-04C, T-05A, T-05B, T-05C, T-06, T-07 | Not yet generated |
| `2026-07-23-durable-jobs-material-workspace.md` | T-08A, T-08B, T-08C, M1-01, M1-02A, M1-02B, M1-02C, M1-03A, M1-03B, M1-04 | Not yet generated |
| `2026-07-23-constrained-ai-and-remote-lifecycle.md` | X2-01, X2-02, X2-03A, X2-03B, X2-03C, INT-01A | Not yet generated |
| `2026-07-23-mutex-learning-loop.md` | M2-01, M2-02A, M2-02B | Not yet generated |
| `2026-07-23-review-planning-and-finals.md` | M3-01A, M3-01B, M3-01C, M3-02A, M3-02B, M3-02C, M3-02D, M3-03 | Not yet generated |
| `2026-07-23-http-api.md` | API-01A, API-01B, API-01C, API-01D1, API-01D2, API-01D3, API-02A, API-02B, API-03A, API-03B, API-03C, API-04A, API-04B, API-REG-01 | Not yet generated |
| `2026-07-23-webui.md` | UI-01A1, UI-01A2, UI-01B, UI-01C, UI-02A, UI-02B, UI-03A, UI-03B, UI-03C, UI-04A, UI-04B, UI-05A, UI-05B | Not yet generated; Open Design run remains deferred to authorized UI execution |
| `2026-07-23-public-demo-profile.md` | DEMO-01A, DEMO-01B, DEMO-REG-01, DEMO-01C1, DEMO-01C2 | Not yet generated |
| `2026-07-23-system-verification.md` | QA-01A1, QA-01A2, QA-01B1, QA-01B2, QA-01C1, QA-01C2, QA-02A, QA-02B, QA-02C | Not yet generated |
| `2026-07-23-windows-oci-distribution.md` | DIST-01, DIST-02 | Not yet generated; D-025 affects only host-specific continuation, not offline plan authoring |
| `2026-07-23-ci-docs-and-release-preparation.md` | CI-01A, CI-01B, CI-01C, DOC-01, FIN-01A1 | Not yet generated |

## Encapsulated Human and External Units

The following 12 root dispatch units are deliberately excluded from implementation-worker detailed plans:

`G-01`, `G-02A`, `G-02B`, `G-02C1`, `G-02C2`, `G-03`, `G-04`, `INT-01B`, `FIN-01A2`, `CI-02`, `DEPLOY-01`, and `FIN-01B`.

Their evidence must come from their named coordinator, student, remote platform, deployment target, or fresh cold-start session. Unattended agents may prepare validation procedures and templates but must not infer decisions, create remote resources, manufacture observations, or mark these rows complete.

- D-005 blocks only the later G-03 cold-start choice and execution.
- D-025 blocks G-02C2 and the host-specific DIST-02/DEPLOY chain, but not offline plan authoring.
- Remote push, PR/MR creation, CI observation, deployment, and release attestation remain execution-time authorization/evidence gates.

## Serialized Shared-Path Handoffs

These paths are intentionally owned by more than one dispatch unit over time and therefore cannot be edited in parallel:

| Path | Required owner order |
| --- | --- |
| `backend/src/projectb/infrastructure/repositories/material_repo.py` | T-03B -> M1-02B -> M1-02C -> M1-04 |
| `backend/src/projectb/infrastructure/repositories/remote_repo.py` | T-03C -> X2-03A -> X2-03B -> X2-03C -> M1-04 |
| `backend/src/projectb/infrastructure/repositories/learning_repo.py` | T-03C -> M3-02B |
| `backend/src/projectb/application/security.py` | T-04A -> T-04B -> T-06 |
| `backend/src/projectb/api/app.py` | T-01B -> T-04C -> API-REG-01 -> DEMO-REG-01 |
| `.gitignore` | G-04 -> T-01A -> INT-01A |
| `frontend/src/app/AppShell.tsx` | UI-01A2 -> UI-01C -> DEMO-01C1 |
| `demo/profile.json` | DEMO-01A -> DIST-02 |
| `README.md` | DOC-01 -> FIN-01A1 -> allowlisted evidence-only commit E |

Every detailed plan must identify the predecessor hash and must stop rather than silently changing an earlier owner's contract. Plans that can be authored concurrently still require a same-snapshot interface review before their hashes are linked.

## Planned Authoring Batches

1. Repair and re-review foundation/domain while authoring persistence.
2. Author local trust/provider control plane and durable jobs/material workspace in parallel, then perform an interface review.
3. Author constrained AI/remote lifecycle, learning loop, and review planning after their shared contracts are fixed.
4. Author HTTP API and WebUI against the reviewed service/domain interfaces.
5. Author demo, system verification, distribution, and CI/docs/release preparation.
6. Run one full-set mechanical audit and independent cross-plan review before any root ledger cell is marked PASS.

The batches describe safe planning order only. They do not authorize worktrees, implementation, Open Design generation, product tests, commits, remote actions, or human gate execution.
