# G-03 Progress Logging Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make every G-03 runner invocation immediately discoverable and continuously observable without persisting credentials, prompts, document content, or raw model output.

**Architecture:** Keep logging inside the existing runner process. Append one allowlisted JSON object per line to `status.log`, mirror a concise progress line to the terminal, emit 15-second heartbeats while Claude child processes run, and bind the final status log path into `completion.json`. Preserve the existing formal Linux/WSL2 sandbox gate; native Windows receives a controlled platform event before any credential prompt.

**Tech Stack:** Windows PowerShell 5.1-compatible script syntax for local contracts, PowerShell 7 on Linux/WSL2 for formal execution, Pester-free contract scripts.

---

### Task 1: Add fail-closed progress logging and heartbeat evidence

**Files:**
- Modify: `.gitattributes`
- Modify: `scripts/cold_start/tests/g03_runner_entrypoint_contract.ps1`
- Modify: `scripts/cold_start/tests/g03_runner_contract.ps1`
- Modify: `scripts/cold_start/g03_runner_core.ps1`
- Modify: `scripts/cold_start/run_g03_claude.ps1`
- Modify: `docs/cold-start/G-03_CLAUDE_CODE_RUNBOOK.md`
- Modify: `AGENT_LOG.md`

- [x] **Step 1: Write the failing entrypoint contract**

Extend every test scenario to require a UTF-8 `status.log`. Parse each non-empty line as JSON and reject any key outside `timestamp`, `stage`, `event`, and `elapsed_seconds`. Require ordered `runner/started`, scenario-stage activity, and `runner/finished` events; require `completion.json.status_log` to identify the same file. Add static assertions for a 15-second heartbeat interval and the controlled `unsupported_platform` event.

- [x] **Step 2: Run the contract and observe the expected red**

Run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cold_start/tests/g03_runner_entrypoint_contract.ps1
```

Expected: exit 1 because `status.log` and `completion.json.status_log` do not exist.

- [x] **Step 3: Implement the minimum logger and heartbeats**

Add `Write-G03Progress` using UTF-8 without BOM and fixed fields only. Print `G03_EVIDENCE_ROOT <path>` at startup. Record controlled stage transitions around capsule, input, platform, preflight, hidden credential wait, intake, execution, replay, and completion. Change `Invoke-G03Claude` to wait in bounded intervals and emit `heartbeat` every 15 seconds without writing child output. Add `status_log` to completion receipts. Do not log exception text, process arguments, prompt text, paths other than the initial evidence-root terminal line, or secret-bearing values.

- [x] **Step 4: Run focused and regression contracts**

Run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cold_start/tests/g03_runner_entrypoint_contract.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cold_start/tests/g03_runner_contract.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cold_start/tests/agent_capsules_contract.ps1
```

Expected: `G03_RUNNER_ENTRYPOINT_PASS cases=5`, `G03_RUNNER_CONTRACT_PASS cases=11`, and `AGENT_CAPSULE_CONTRACT_PASS cases=9`.

- [x] **Step 5: Verify safety and record the process change**

Run PowerShell AST parsing, strict UTF-8 checks, scoped credential-shape scanning, and `git diff --check`. Record the actual red/green outputs and the native-Windows limitation in `AGENT_LOG.md`. Request a quality/security review before committing.

- [x] **Step 6: Commit only the owned files**

```powershell
git add -- .gitattributes scripts/cold_start/g03_runner_core.ps1 scripts/cold_start/run_g03_claude.ps1 scripts/cold_start/tests/g03_runner_contract.ps1 scripts/cold_start/tests/g03_runner_entrypoint_contract.ps1 docs/cold-start/G-03_CLAUDE_CODE_RUNBOOK.md docs/superpowers/plans/2026-07-30-g03-progress-logging.md AGENT_LOG.md
git commit -m "fix(g03): add observable runner progress"
```

Implementation checkpoint: `39f323d3791d78b6de0d0adb4d47bf3b5263ba5e`.

Do not stage the student's existing `docs/research/*` or `docs/engineering/SUPERPOWERS_VALIDATION.md` changes.
