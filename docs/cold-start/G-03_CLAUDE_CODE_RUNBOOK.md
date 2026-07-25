# G-03 Claude Code Cold-Start Runbook

> **Status:** PREPARED / NOT EXECUTED
> **Purpose:** Operator-only procedure. This file is evidence and must not be supplied to the cold-start agent as a third context file.

## Frozen Inputs

- `SPEC.md` SHA-256: `795791627579BFEBE24717981168A54E2D546F613FEA84CCDF0AC0ECBA387862`
- `PLAN.md` SHA-256: `6FDD69F2FD309841CC46DB1C75C142E4E1E8474E1575A2E765F49EF67002A05D`
- Attempted task: `F-01A`
- Workspace: a disposable empty directory, not the real repository and not an implementation worktree

If either hash differs, stop. Re-run the same-hash mechanical and two-reviewer Stage B gate before cold start.

## Student-Controlled Setup

1. Install or open Claude Code and personally handle login, terms and any account choice. Do not enter a real project API key.
2. Record the exact Claude Code version, local time, fresh-session identifier and the initial visible file list.
3. Start a new session with memory/history disabled or absent. Do not expose the repository, Git history, `AGENTS.md`, prior chat, research notes, review receipts or this runbook.
4. Copy only the frozen `SPEC.md` and `PLAN.md` into the disposable directory and verify their SHA-256 values there.

## Prompt To Send

```text
You are a cold-start implementation agent. You have exactly two authoritative context files: SPEC.md and PLAN.md. Do not search for, infer, or request access to any repository history or other project documents.

First report the SHA-256 of both files and the complete file list you can see. Then attempt only PLAN task F-01A in this disposable workspace, following its red/green, validation, security, license, and completion requirements. Stop and ask a precise question whenever either file is ambiguous or a referenced input is unavailable; do not guess. Do not use real credentials, paid APIs, remote repositories, cloud resources, commits, pushes, PRs, or deployment. Keep the failing-test output, passing-test output, commands, produced diff, assumptions, questions, and any task requirement you could not satisfy.
```

## Evidence To Capture

- version, timestamp, session identifier and initial file list;
- the exact initial prompt and both reported hashes;
- every question and the answer actually supplied by the student;
- misunderstandings, unstated assumptions and missing referenced inputs;
- produced file diff plus red/green/verification command outputs;
- a requirement-by-requirement gap list for F-01A;
- whether the agent stopped instead of guessing.

Do not rewrite or summarize the transcript as if it were contemporaneous evidence. Save the raw export or screenshots first, then add a factual summary and key revision diff to `SPEC_PROCESS.md`.

## Exit Gate

1. Compare the output against F-01A without integrating it into the real repository.
2. Repair every exposed SPEC/PLAN ambiguity. If either file changes, compute new hashes and repeat both Stage B reviews on the exact new pair.
3. Record the cold-start questions, misunderstandings, output gaps and revision diff in `SPEC_PROCESS.md` and the run receipt in `AGENT_LOG.md`.
4. Ask the student for a fresh, explicit G-04 implementation approval. The earlier SPEC confirmation does not satisfy G-04.

## Current Blocker

On 2026-07-26, `Get-Command claude` did not find a local command. No Claude Code version, login, session, attempt, transcript or implementation output has been claimed.
