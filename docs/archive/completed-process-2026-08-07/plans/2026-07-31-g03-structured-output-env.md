# G-03 结构化输出与本地测试环境实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 让 G-03 从根目录受控读取本地测试变量，并使用 Claude CLI 原生 JSON Schema 获得可稳定验证的 intake/execution 结果。

**Architecture:** 新建一个不执行 shell 语义的通用 `.env` 解析器，各测试消费者只按名称取值；G-03 仅选择 API key，并保持端点、模型、预算和哈希由 runner 参数固定。两个 schema 只约束 Claude 的最终结果，现有 coordinator 继续二次检查哈希、文件、任务、命令、TDD 事件与候选产物。

**Tech Stack:** Windows PowerShell 5.1 合同测试、PowerShell 7/WSL2 正式 runner、Claude Code 2.1.220、JSON Schema、Pester-free contract scripts。

---

## 文件职责

- `.env.example`：可提交的空值模板和明文风险说明。
- `.env`：忽略且不提交的本机测试变量集合；本任务只创建空模板，不写真实值。
- `scripts/local_test_env.ps1`：严格解析、显式取值和 Git 忽略/未跟踪检查。
- `scripts/cold_start/tests/local_test_env_contract.ps1`：解析器、安全边界和无泄露合同。
- `scripts/cold_start/schemas/g03-intake.schema.json`：intake 最终结果结构。
- `scripts/cold_start/schemas/g03-execution.schema.json`：execution 最终结果结构。
- `scripts/cold_start/g03_runner_core.ps1`：结构化结果解析与有界诊断分类。
- `scripts/cold_start/run_g03_claude.ps1`：凭据来源选择、schema 参数和阶段控制。
- `scripts/cold_start/tests/g03_runner_contract.ps1`：核心行为合同。
- `scripts/cold_start/tests/g03_runner_entrypoint_contract.ps1`：入口参数、静态安全与测试场景合同。
- `docs/cold-start/G-03_CLAUDE_CODE_RUNBOOK.md`：学生可直接执行的中文操作手册。
- `AGENT_LOG.md`：实际红绿输出、评审与提交证据。

### Task 1: 建立可复用的本地测试 `.env` 合同

**依赖：** 已确认设计 `bbd7919`。

**可并行：** 否。后续 runner 接入依赖这里的函数名和失败语义。

**Files:**
- Create: `.env.example`
- Create locally, never stage: `.env`
- Create: `scripts/local_test_env.ps1`
- Create: `scripts/cold_start/tests/local_test_env_contract.ps1`
- Modify: `AGENT_LOG.md`

- [ ] **Step 1: 先写严格解析器的失败合同**

合同脚本先 dot-source 尚不存在的 `scripts/local_test_env.ps1`，然后要求以下公开接口：

```powershell
$values = Read-ProjectBTestEnv -Path $envPath
$key = Get-ProjectBTestEnvValue -Values $values -Name 'PROJECTB_G03_CLAUDE_API_KEY'
$safe = Test-ProjectBTestEnvGitSafety -ProjectRoot $projectRoot -Path $envPath
```

固定断言：无 BOM UTF-8、LF/CRLF、空行、注释和多个 `PROJECTB_[A-Z0-9_]+` 变量通过；BOM、NUL、非法名、重复名、非赋值行、超过 32 KiB 的文件、超过 4096 字符的行失败为固定枚举；取值函数只返回点名变量；异常文本和测试输出都不包含拼接得到的假 key。

- [ ] **Step 2: 运行红测并保存真实失败原因**

Run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cold_start/tests/local_test_env_contract.ps1
```

Expected: exit 1，输出 `LOCAL_TEST_ENV_RED parser_missing`。

- [ ] **Step 3: 写最小解析实现**

实现应采用严格 UTF-8 解码，不调用 `source`、`Invoke-Expression` 或环境整体导入：

```powershell
function Read-ProjectBTestEnv {
    param([Parameter(Mandatory=$true)][string]$Path,[int]$MaxBytes=32768,[int]$MaxLineChars=4096)
    $bytes = [IO.File]::ReadAllBytes($Path)
    if ($bytes.Length -gt $MaxBytes) { throw 'DOTENV_FILE_TOO_LARGE' }
    if ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) { throw 'DOTENV_UTF8_INVALID' }
    try { $text = (New-Object Text.UTF8Encoding($false,$true)).GetString($bytes) } catch { throw 'DOTENV_UTF8_INVALID' }
    if ($text.Contains([char]0) -or $text.Contains([char]0xFFFD)) { throw 'DOTENV_UTF8_INVALID' }
    $result = [ordered]@{}
    foreach ($line in @($text -split "`r?`n")) {
        if ($line.Length -gt $MaxLineChars) { throw 'DOTENV_LINE_TOO_LONG' }
        if ([string]::IsNullOrWhiteSpace($line) -or $line.StartsWith('#')) { continue }
        if ($line -cnotmatch '^(PROJECTB_[A-Z0-9_]+)=(.*)$') { throw 'DOTENV_SYNTAX_INVALID' }
        if ($result.Contains($Matches[1])) { throw 'DOTENV_DUPLICATE_NAME' }
        $result[$Matches[1]] = $Matches[2]
    }
    return $result
}
```

`Test-ProjectBTestEnvGitSafety` 使用 `git -C <root> check-ignore -q -- .env` 与 `git -C <root> ls-files --error-unmatch -- .env`，只返回 `Ignored`、`Tracked` 和固定 `Code`，不记录文件内容。

- [ ] **Step 4: 提交空模板并创建本地文件**

`.env.example` 的有效内容为：

```dotenv
# 本文件仅供本地测试。复制为 .env 后填值；.env 是明文文件，禁止提交或粘贴到日志。
PROJECTB_G03_CLAUDE_API_KEY=
```

若根目录 `.env` 不存在，复制该模板为 `.env`；随后必须证明 `.env` 被忽略且未被追踪，且 `git diff --cached` 不含它。

- [ ] **Step 5: 运行绿测并提交**

Run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cold_start/tests/local_test_env_contract.ps1
git check-ignore -q .env
git ls-files --error-unmatch .env
```

Expected: `LOCAL_TEST_ENV_CONTRACT_PASS`；`check-ignore` exit 0；`ls-files` exit 1。

Commit only:

```powershell
git add -- .env.example scripts/local_test_env.ps1 scripts/cold_start/tests/local_test_env_contract.ps1 AGENT_LOG.md
git commit -m "feat(test): add strict local env contract"
```

**完成标准：** 可保存多个本地测试变量，G-03 以外的变量不会被隐式注入任何子进程，真实 `.env` 不进入 Git 或证据。

### Task 2: 用 JSON Schema 固定 intake 结果

**依赖：** Task 1。

**可并行：** 否。会修改 runner/core 共享文件。

**Files:**
- Create: `scripts/cold_start/schemas/g03-intake.schema.json`
- Modify: `scripts/cold_start/tests/g03_runner_contract.ps1`
- Modify: `scripts/cold_start/tests/g03_runner_entrypoint_contract.ps1`
- Modify: `scripts/cold_start/g03_runner_core.ps1`
- Modify: `scripts/cold_start/run_g03_claude.ps1`
- Modify: `AGENT_LOG.md`

- [ ] **Step 1: 先写 schema 与凭据来源失败合同**

入口合同新增精确接口 `CredentialSource=Auto|Prompt|DotEnv`；静态要求 intake 参数同时含 `--output-format json` 与 `--json-schema`。核心合同要求合法外层 envelope + prose result 分类为 `structured_result_protocol`，外层非 JSON 分类为 `outer_output_protocol`，envelope 字段错误分类为 `envelope_protocol`，合法结构但哈希/文件/任务不匹配分类为 `intake_contract_mismatch`。

- [ ] **Step 2: 运行红测**

Run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cold_start/tests/g03_runner_contract.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cold_start/tests/g03_runner_entrypoint_contract.ps1
```

Expected: 两者 exit 1，分别指出结构化诊断接口和 `CredentialSource`/`--json-schema` 缺失。

- [ ] **Step 3: 提交 intake schema**

Schema 使用 `type: object`、完整 `required`、`additionalProperties: false`；hash 为 `^[A-F0-9]{64}$`，`files` 精确为 `PLAN.md`、`SPEC.md`，`language/task/acceptance_id` 使用固定 enum/const，`ambiguities` 为字符串数组。runner 通过严格 UTF-8 读取后压缩为单行参数：

```powershell
$intakeSchemaJson = (Read-G03StrictUtf8 $intakeSchemaPath | ConvertFrom-Json | ConvertTo-Json -Depth 12 -Compress)
$intakeArgs = @(
    '--print', '--output-format', 'json', '--json-schema', $intakeSchemaJson,
    '--no-session-persistence', '--bare', '--safe-mode',
    '--setting-sources', 'project', '--settings', $sandboxSettingsPath,
    '--no-chrome', '--strict-mcp-config',
    '--session-id', ([guid]::NewGuid().ToString()), '--name', 'ProjectB-G03-Intake',
    '--model', $Model, '--permission-mode', 'dontAsk',
    '--tools', 'Bash', '--allowedTools', ("Bash(" + $extractorCommand + ")"),
    '--max-budget-usd', $intakeBudgetUsd.ToString([Globalization.CultureInfo]::InvariantCulture),
    $intakePrompt
)
```

- [ ] **Step 4: 接入 `.env` 凭据选择与精确诊断**

runner dot-source `scripts/local_test_env.ps1`，在任何 Claude 调用前解析 `CredentialSource`：`Prompt` 保留隐藏输入；`DotEnv` 要求 Git 安全检查通过且 key 非空、单行、无首尾空白；`Auto` 在存在有效变量时使用它，否则隐藏输入。只把该值赋给 `ANTHROPIC_AUTH_TOKEN`，现有 `finally` 清理保持不变。

将结构解析结果改成固定对象：

```powershell
[pscustomobject]@{ Valid=$false; Code='structured_result_protocol'; Value=$null }
[pscustomobject]@{ Valid=$true; Code='ok'; Value=$value }
```

`process-diagnostic.json` 只写阶段、退出码、超时和上述固定码，不写 result、stderr 或 `.env` 路径。

- [ ] **Step 5: 运行绿测并提交**

Run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cold_start/tests/local_test_env_contract.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cold_start/tests/g03_runner_contract.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cold_start/tests/g03_runner_entrypoint_contract.ps1
```

Expected: 三个 `*_PASS`，且测试拼接的假 key 不出现在测试输出或临时证据中。

Commit only owned files with `git commit -m "fix(g03): enforce structured intake output"`。

**完成标准：** intake 不再依赖提示词保证 JSON，任何协议层失败能从脱敏诊断码区分。

### Task 3: 固定 execution 结果并保持真实 TDD 证据

**依赖：** Task 2。

**可并行：** 否。与 Task 2 修改相同 runner/core/test 文件。

**Files:**
- Create: `scripts/cold_start/schemas/g03-execution.schema.json`
- Modify: `scripts/cold_start/tests/g03_runner_contract.ps1`
- Modify: `scripts/cold_start/tests/g03_runner_entrypoint_contract.ps1`
- Modify: `scripts/cold_start/g03_runner_core.ps1`
- Modify: `scripts/cold_start/run_g03_claude.ps1`
- Modify: `AGENT_LOG.md`

- [ ] **Step 1: 先写 execution 失败合同**

要求 execution 参数含 `--output-format stream-json --json-schema <schema>`；result 缺失、非 JSON、额外字段和错误命令分别得到 `envelope_protocol`、`structured_result_protocol` 或 `execution_contract_mismatch`。保留两次真实 Bash contract tool_use/tool_result 的顺序、红测 exit 1、绿测四行输出和独立 replay 校验。

- [ ] **Step 2: 运行红测**

Run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cold_start/tests/g03_runner_contract.ps1
```

Expected: exit 1，因为 execution schema/参数尚不存在。

- [ ] **Step 3: 提交 execution schema 和最小接线**

Schema 精确要求 `task`、`acceptance_id`、`ambiguities`、`questions`、`red_command`、`green_command`；禁止额外属性，两个命令使用固定 const。`Get-G03ExecutionEvidence` 继续从 stream-json 统计工具事件，但把最终 result 的解析失败与业务不匹配分开；Schema 不能替代 coordinator 的事件顺序和产物验证。

- [ ] **Step 4: 运行绿测和全部离线回归**

Run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cold_start/update_agent_capsules.ps1 -Mode Check
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cold_start/tests/agent_capsules_contract.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cold_start/tests/local_test_env_contract.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cold_start/tests/g03_runner_contract.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cold_start/tests/g03_runner_entrypoint_contract.ps1
```

Expected: capsule 检查不改文件，四个合同脚本全部输出各自 `PASS`。

- [ ] **Step 5: 提交**

Commit only owned files with `git commit -m "fix(g03): enforce structured execution output"`。

**完成标准：** execution 的最终结果结构稳定，同时原有红—绿工具证据和 coordinator replay 没有被削弱。

### Task 4: 中文手册、评审与一次受控正式复测

**依赖：** Task 3；正式复测还依赖学生在忽略的 `.env` 中填入新临时 key。

**可并行：** 代码评审可与手册校对并行；正式复测必须在所有离线验证通过后串行执行。

**Files:**
- Modify: `docs/cold-start/G-03_CLAUDE_CODE_RUNBOOK.md`
- Modify: `SPEC_PROCESS.md`（仅在产生正式新证据后）
- Modify: `AGENT_LOG.md`
- Modify: this plan status only

- [ ] **Step 1: 更新中文操作手册**

将正式命令改为 `-CredentialSource DotEnv`，说明 `.env` 是明文本地测试兼容源、不得提交；列出 `status.log` 观察方法和新诊断码。删除“每次隐藏输入 key”的过时描述，但保留 `Prompt` 兼容路径。

- [ ] **Step 2: 机械、安全和两阶段评审**

Run:

```powershell
git diff --check
git check-ignore -q .env
git ls-files --error-unmatch .env
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/bootstrap_scan_credentials.ps1
```

Expected: diff clean；`.env` ignored/untracked；凭据扫描无真实 secret。先做 SPEC/设计符合性评审，再做正确性、安全、测试质量和许可证评审；Critical/Major 清零后才能复测。

- [ ] **Step 3: 在 WSL2 发起最多一次正式运行**

```bash
export TEMP=/tmp TMP=/tmp
pwsh -NoProfile -File ./scripts/cold_start/run_g03_claude.ps1 \
  -CredentialSource DotEnv \
  -AgentLanguage Auto \
  -Model claude-sonnet-4-6 \
  -MaxTotalBudgetUsd 1.00 \
  -ExpectedSpecSha256 14C03D688A09451DCA06F66507CE4510510A8A3BC550057376B0A1EF95270713 \
  -ExpectedPlanSha256 95FF14D23DB92692BA005C3AA42598ABB5DDCFEE2DEFC28B950B00617C3EC663 \
  -ClaudeCli ./tmp/toolchains/claude-code/node_modules/@anthropic-ai/claude-code/bin/claude
```

Expected success: `G03_RUNNER_STATE G03_EVIDENCE_READY`。若失败，只记录本次新固定诊断码与脱敏证据目录，不自动重试或切换模型。

- [ ] **Step 4: 独立复验并诚实更新过程文档**

成功时独立验证 `completion.json`、`intake-receipt.json`、`execution-summary.json`、candidate hashes 和 replay receipt 后，才把事实写入 `SPEC_PROCESS.md`；失败时保持 G-03 未通过并写明阻塞。任何情况下都不把 `.env` 或原始模型输出纳入证据。

- [ ] **Step 5: 最终提交**

Commit only owned documentation/evidence references with `git commit -m "docs(g03): record structured cold-start result"`。

**完成标准：** 离线实现和文档可复现；只有正式证据确实为 `G03_EVIDENCE_READY` 时才关闭 G-03，随后仍等待学生 G-04 实现批准。
