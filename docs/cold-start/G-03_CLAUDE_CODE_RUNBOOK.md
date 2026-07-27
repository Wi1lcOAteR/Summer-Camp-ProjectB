# G-03 Different-Agent Runbook and G-03P Receipt

> **Status:** CURRENT SR-08 PASS / G-03P REMEDIATION COMPLETE / FORMAL G-03 OPEN
> **Purpose:** Operator-only procedure. This file is evidence and must not be supplied to the cold-start agent as a third context file.

## Frozen Inputs

- `SPEC.md` SHA-256: `6A0DB7CAD19533FE9A31EA81A6B30ED493C01BE59D4C98DEB6EC04A89BD11E56`
- `PLAN.md` SHA-256: `E96C415AD716B002AD9B1EB3C2AFD7C78F693486CB83A795110B99B6755972C1`
- Attempted task: complete dependency-free `F-01S`
- Workspace: a disposable empty directory, not the real repository and not an implementation worktree

If either hash differs, stop. Re-run the same-hash mechanical and two-reviewer Stage B gate before cold start.

## Student-Controlled Setup

1. Install or open an accessible non-Codex coding agent such as Claude Code, Gemini CLI or GitHub Copilot CLI, and personally handle login, terms and any account choice. Do not enter a real project API key.
2. Record the exact tool and version, local time, fresh-session identifier and the initial visible file list.
3. Start a new session with memory/history disabled or absent. Do not expose the repository, Git history, `AGENTS.md`, prior chat, research notes, review receipts or this runbook.
4. Copy only the frozen `SPEC.md` and `PLAN.md` into the disposable directory and verify their SHA-256 values there.

## Prompt To Send

```text
You are a cold-start implementation agent. You have exactly two authoritative context files: SPEC.md and PLAN.md. Do not search for, infer, or request access to any repository history or other project documents.

First report the SHA-256 of both files and the complete file list you can see. Then attempt only complete PLAN task F-01S. Create only scripts/tests/bootstrap_scanner_contract.ps1 and scripts/bootstrap_scan_credentials.ps1, run its exact red then green command, and stop. The unchanged contract must cover all eight named groups, eleven helpers, every stable error proof, index-blob/worktree separation, both-source reporting, boundaries/quotes/encoding/index modes, and redaction. After behavioral green, put exact copies of only those two scripts in a fresh disposable Git repository, stage both, and require exactly CREDENTIAL_SCAN_PASS files=4 from -Tracked -Staged; construct every positive fixture from non-matching fragments at runtime. Stop and ask a precise question whenever either file is ambiguous; do not guess. Do not use real credentials, paid APIs, remote repositories, cloud resources, commits, pushes, PRs, or deployment. Keep outputs, diff, assumptions, questions, and any requirement you could not satisfy.
```

## Evidence To Capture

- version, timestamp, session identifier and initial file list;
- the exact initial prompt and both reported hashes;
- every question and the answer actually supplied by the student;
- misunderstandings, unstated assumptions and missing referenced inputs;
- produced file diff plus red/green/verification command outputs;
- a requirement-by-requirement gap list for F-01S;
- whether the agent stopped instead of guessing.

Do not rewrite or summarize the transcript as if it were contemporaneous evidence. Save the raw export or screenshots first, then add a factual summary and key revision diff to `SPEC_PROCESS.md`.

## Exit Gate

1. Compare the output against complete F-01S without integrating it into the real repository.
2. Repair every exposed SPEC/PLAN ambiguity. If either file changes, compute new hashes and repeat both Stage B reviews on the exact new pair.
3. Record the cold-start questions, misunderstandings, output gaps and revision diff in `SPEC_PROCESS.md` and the run receipt in `AGENT_LOG.md`.
4. Ask the student for a fresh, explicit G-04 implementation approval. The earlier SPEC confirmation does not satisfy G-04.

## G-03P Placeholder Receipt

- On 2026-07-27, local `codex-cli 0.144.4` was attempted first in an ephemeral disposable directory. It produced no output or scaffold for about four minutes and was terminated; this failed transport attempt is not cold-start evidence.
- Fresh projectless Codex desktop task `019fa1f5-8031-7450-883c-2462fc623703` received only the older SPEC/PLAN. Its first pass stopped before red and exposed unavailable F-01A inputs. After narrowing, it reported all seven questions answered.
- Exact red command exited 1 with `CONTRACT_RED scanner_missing`. The unchanged command then exited 0 with 12 named contract groups and `BOOTSTRAP_SCANNER_CONTRACT_PASS cases=12`.
- That receipt used obsolete hashes `600395...ED71` / `8A4BE...AFD`. Generated scanner/contract hashes `37CC6252...2D60` / `F0CA58FA...C516` remain outside the repository and are not F-01S implementation. Later review found its staged-source coverage insufficient, so it is historical evidence only.

## Current G-03P Recheck

- Fresh projectless task `019fa331-3da1-7f80-a37c-ac7abb135a46` received only SPEC `6A0DB7...11E56` and predecessor PLAN `D574B8...1D742`.
- It produced the exact missing-scanner red and unchanged eight-group green with all eleven helpers. Projectless contract/scanner SHA-256 values were `E970C52C...3A79B` / `097F5683...9F64`.
- Its added self-scan found assignment fixtures in contract index/worktree bytes and exited 2. This was not hidden or called PASS.
- Final PLAN `E96C415A...972C1` makes runtime-fragment fixtures and exact `files=4` self-scan mandatory. Focused current-hash course/SPEC and quality/security/license reviews both passed with no Critical/Major issue.
- This repair evidence remains same-family G-03P and does not replace the formal run described above.

## Current Blocker

Claude is rejected by the currently available service path, Gemini requires a special relay, and Copilot is not provisioned. G-03 remains open until any non-Codex coding agent can repeat the final-hash procedure. G-03P does not satisfy the different-type requirement, authorize implementation, or close G-04.
