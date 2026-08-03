# G-03 Claude Code 手工冷启动手册

## 当前状态

旧版 PowerShell runner 已停用并删除。G-03 已于 2026-08-03 使用 Claude Code 插件的两个独立新 session 完成：先 intake，再以短检查点执行。产品实现仍受 G-04 门禁约束。

- SPEC SHA-256：`AEA67BB5544AD22932DC4304964F7FD266FE8A5DE7AA396EA8974D30867E8381`
- PLAN SHA-256：`910A3AEC9B4CEDCC119675C5D862879D178E3FE062CEE39C2AD62AF07219E923`
- 任务：`F-01S1A`
- 验收 ID：`F01S1A_SINGLE_RULE_SCANNER_V2`

同字节机械审计、规约评审和质量/安全/许可证评审均已通过。Intake 无歧义；execution 得到规定红测和绿测，生成的 contract/scanner 分别为 161/95 行。候选产物仅保存在 disposable 目录，不作为正式实现合入。

成功执行采用 `1 -> 2A -> 2B -> 2C -> 2D -> 3A -> 3B -> 3C -> 3D-R` 的短检查点。每轮只执行一个动作、禁止解释推理，并返回紧凑 JSON；`3D-R` 的最终输出为 `GROUP usage_and_output`、`GROUP provider_rule`、`BOOTSTRAP_SCANNER_PATH_PASS`，exit 0。

## 输入目录

使用以下两个 disposable 目录。每个目录必须只包含 `SPEC.md` 和 `PLAN.md`：

- `tmp/g03-manual/20260803-atomic/intake`
- `tmp/g03-manual/20260803-atomic/execution`

Intake 和 execution 必须使用两个全新、互相独立的 Claude Code session。不要把本手册、AGENTS.md、历史计划或源码加入智能体上下文。

## Intake 提示词

```text
You are a fresh non-Codex intake session for ProjectB G-03.

The current directory must contain exactly two files: SPEC.md and PLAN.md.
Do not edit files. Do not create files or directories. Do not use network, git, or external tools.

Read both documents and return exactly one JSON object, with no Markdown:
{
  "spec_sha256": "...",
  "plan_sha256": "...",
  "files": ["PLAN.md", "SPEC.md"],
  "language": "English",
  "task": "F-01S1A",
  "acceptance_id": "F01S1A_SINGLE_RULE_SCANNER_V2",
  "ambiguities": []
}

Compute both SHA-256 values independently. The complete sorted file list must be exactly ["PLAN.md", "SPEC.md"].
If anything is unclear or inconsistent, stop and list it in ambiguities instead of guessing.
```

只有 intake 返回 `ambiguities=[]` 才能继续 execution。

## Execution 提示词

```text
You are a separate fresh non-Codex implementation session for ProjectB G-03.

You have only SPEC.md and PLAN.md. Do not modify either document.
Implement only F-01S1A.

Create only scripts/tests/bootstrap_scanner_contract.ps1 first. Run:
pwsh -NoProfile -File scripts/tests/bootstrap_scanner_contract.ps1
Preserve exit code 1 with the sole output CONTRACT_RED scanner_missing.

Then create only scripts/bootstrap_scan_credentials.ps1 and rerun the same command. Require:
usage_and_output
provider_rule
BOOTSTRAP_SCANNER_PATH_PASS

Implement only Write-ScanRecord, Convert-SourceText, Find-DirectSecret, and minimal -Path wiring for provider_api_key.
The rule is sk- plus 20--200 [A-Za-z0-9_-] characters, bounded on both sides by start/end or a character outside that set.
Use source=path, normalize backslashes to slashes, remove one leading ./, reject missing scope/read/BOM/invalid UTF-8/U+FFFD, and never print secret values or file content.

The contract must be <=180 lines, the scanner <=140 lines, and positive fixtures must join independently non-matching fragments.
Do not create other files, use network, modify SPEC.md/PLAN.md, or commit.

Return exactly one JSON object with no Markdown:
{
  "task": "F-01S1A",
  "acceptance_id": "F01S1A_SINGLE_RULE_SCANNER_V2",
  "ambiguities": [],
  "questions": [],
  "red_command": "pwsh -NoProfile -File scripts/tests/bootstrap_scanner_contract.ps1",
  "green_command": "pwsh -NoProfile -File scripts/tests/bootstrap_scanner_contract.ps1",
  "summary": "A concise English summary of at most 300 words."
}
```

## 结果判定

- Intake 有歧义：停止，不运行 execution。
- Execution 未创建两个文件、未保留 red、green 不完整或创建额外文件：G-03 未通过。
- 两个 session 都完成后，把原始 JSON、文件列表和命令输出保存到 `tmp/g03-manual/`，再在 `SPEC_PROCESS.md` 和 `AGENT_LOG.md` 记录事实。
- G-03 通过不等于允许实现。实现前仍需学生明确批准 G-04，并重新按 PLAN 使用 worktree、TDD 和双评审。
