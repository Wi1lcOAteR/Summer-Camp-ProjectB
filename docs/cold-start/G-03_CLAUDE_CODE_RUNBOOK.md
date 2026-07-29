# G-03 异类智能体冷启动操作手册与 G-03P 收据

> **状态：** 当前 `SR-08 PASS / G-03P 修订完成 / 正式 G-03 两次模型尝试均不完整`
> **用途：** 仅供学生操作。此文件属于过程证据，不能作为第三份上下文交给冷启动智能体。
> **语言约定：** 学生需要阅读或操作的后续文档默认使用中文；命令、文件名、哈希、任务编号和工具原始输出保持原样。

## 你现在需要做什么

目前不需要重新安装 Claude Code。项目内已经安装并验证：

- Claude Code：`2.1.220`
- Node.js：`v24.14.0`
- 本地启动器：`tmp/toolchains/claude-code/node_modules/.bin/claude.cmd`
- Git for Windows Bash：`C:\Program Files\Git\bin\bash.exe`

2026-07-29 的旧端点尝试 `a7671467-4cdb-4473-a9ab-587c336ef68d` 因 `401 authentication_failed` 停止。正确端点会话 `71a50d25-4cd7-48b1-9472-8107e82779ed` 成功调用 `claude-sonnet-5`，但模型只创建空目录便以空 `end_turn` 结束。第二次正确端点会话 `32b62490-7817-4d3d-8452-7a29a4de94ea` 使用 `claude-sonnet-4-6`，在哈希验证后收到 `504 Gateway Time-out`。两次都没有 F-01S 文件或测试收据。执行器已经增加产物后置条件，避免再把 CLI exit 0 误报为任务完成。不要向聊天或仓库提供账号密码、会话令牌或真实项目 API Key。

## 冻结输入

- `SPEC.md` SHA-256：`6A0DB7CAD19533FE9A31EA81A6B30ED493C01BE59D4C98DEB6EC04A89BD11E56`
- `PLAN.md` SHA-256：`E96C415AD716B002AD9B1EB3C2AFD7C78F693486CB83A795110B99B6755972C1`
- 尝试任务：完整执行无依赖任务 `F-01S`
- 工作目录：一次性空目录，不是真实仓库，也不是实现 worktree

如果任一哈希不同，立即停止。必须先针对同一份新哈希重新完成机械审计和两阶段 Stage B 评审，才能冷启动。

## 第一步：准备隔离目录

在 PowerShell 中逐行执行：

```powershell
$ProjectBRoot = "E:\Personal_Documentary\ResearchProjects\ProjectB"
$ClaudeCli = Join-Path $ProjectBRoot "tmp\toolchains\claude-code\node_modules\.bin\claude.cmd"
$ColdStartRoot = Join-Path $env:TEMP ("projectb-g03-" + [guid]::NewGuid().ToString())

New-Item -ItemType Directory -Path $ColdStartRoot | Out-Null
Copy-Item (Join-Path $ProjectBRoot "SPEC.md") $ColdStartRoot
Copy-Item (Join-Path $ProjectBRoot "PLAN.md") $ColdStartRoot
Set-Location $ColdStartRoot

Get-ChildItem -Force
Get-FileHash .\SPEC.md -Algorithm SHA256
Get-FileHash .\PLAN.md -Algorithm SHA256
& $ClaudeCli --version
```

目录中必须只有 `SPEC.md` 和 `PLAN.md`。两个哈希必须与“冻结输入”一致。

## 第二步：启动全新 Claude Code 会话

当前机器已准备本地、Git 忽略的隔离执行器。它会生成新会话编号、隐藏读取凭据、限制费用、清除子进程凭据并保存脱敏证据：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File 'E:\Personal_Documentary\ResearchProjects\ProjectB\tmp\run-g03-claude.ps1'
```

当前执行器固定端点为 `https://ai2.1343263.xyz`，使用该端点公开声明支持的 Bearer 认证。输入隐藏凭据后，它先请求 `/v1/models`，只列出名称中包含 `claude` 的模型；若有多个模型，由学生在终端选择。`claude-sonnet-5` 与 `claude-sonnet-4-6` 已分别暴露空结果和 504；继续尝试前应明确接受可能产生的额外费用，并优先确认网关稳定性。没有 Claude 模型或模型查询失败时会立即停止，不猜模型名。

隔离参数含义：

- `--bare` 与 `--safe-mode`：关闭自动记忆、`CLAUDE.md`、skills、plugins、hooks、MCP 和其他自定义上下文；
- `--setting-sources project`：排除用户设置中的旧认证值；
- `--strict-mcp-config`：不加载其他 MCP；
- `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB=1`：主进程可认证，但 Bash 等子进程看不到凭据；
- 新 `--session-id`：避免恢复旧对话；
- 不使用 `--continue`、`--resume`、`--add-dir` 或 `--dangerously-skip-permissions`。

首次运行可能要求登录或确认工作目录。账号选择、登录和条款确认必须由你本人完成。如果服务仍拒绝访问，保存完整错误信息并停止；不要反复尝试登录、修改系统安全策略或输入项目 API Key。

## 第三步：发送下面这段提示词

```text
你是一个没有项目历史上下文的冷启动实现智能体。你只有两份权威上下文文件：SPEC.md 和 PLAN.md。不得搜索、推断或请求访问任何仓库历史或其他项目文档。

先报告两份文件各自的 SHA-256，以及你能看到的完整文件列表。然后只尝试完整执行 PLAN 任务 F-01S。只能创建 scripts/tests/bootstrap_scanner_contract.ps1 和 scripts/bootstrap_scan_credentials.ps1，先运行任务规定的精确红测命令，再以完全相同的命令运行绿测，然后停止。不得修改测试合同来制造通过。

未修改的合同必须覆盖八个具名测试组、十一个 helper、所有稳定错误证明、index blob 与 worktree 分离、双来源报告、边界/引号/编码/index 模式和脱敏。行为绿测后，把这两个脚本的精确副本放入一个全新的一次性 Git 仓库并暂存两者；所有正向 fixture 必须在运行时由不匹配的片段拼接生成；使用 -Tracked -Staged 自扫描时必须精确得到 CREDENTIAL_SCAN_PASS files=4。

如果任一文件存在歧义，立即停止并提出一个精确问题，不得猜测。不得使用真实凭据、付费 API、远程仓库、云资源、commit、push、PR 或部署。保留全部输出、diff、假设、问题和任何未能满足的要求。
```

## 第四步：保存证据

必须保存：

- 工具版本、本地时间、会话编号和初始文件列表；
- 完整初始提示词和智能体报告的两个哈希；
- 智能体提出的每个问题，以及学生实际给出的回答；
- 误解、未声明假设和缺失引用输入；
- 产出文件 diff，以及红测、绿测和自扫描的完整输出；
- 对照 F-01S 的逐项差距清单；
- 智能体遇到歧义时是否确实停止，而不是自行猜测。

执行器还会检查隔离目录最终是否恰好包含两份冻结输入和两份非空 F-01S 脚本。缺少脚本或出现额外文件时，即使 Claude CLI exit 0，也会记录 `COLD_START_INCOMPLETE`，不能按完成处理。该检查不能替代后续对红测、绿测和自扫描输出的独立复验。

不要事后把转述或整理后的内容冒充同期原始证据。先保存原始导出或截图，再把事实摘要和关键修订 diff 写入 `SPEC_PROCESS.md`。

## 第五步：退出门禁

1. 不把冷启动产出合入真实仓库，只对照完整 F-01S 检查。
2. 修复暴露出的每一处 SPEC/PLAN 歧义。如果任一文件改变，重新计算哈希，并对完全相同的新文件重新执行 Stage B 两阶段评审。
3. 把问题、误解、产出差距和修订 diff 写入 `SPEC_PROCESS.md`，把运行收据写入 `AGENT_LOG.md`。
4. 完成后由学生重新明确批准 G-04 进入实现阶段。此前的 SPEC 确认或“继续”不等于 G-04 批准。

## G-03P 占位收据

- 2026-07-27 首先在一次性目录尝试本地 `codex-cli 0.144.4`。约四分钟没有输出或脚手架后终止；这是传输失败，不属于冷启动证据。
- 全新、无项目历史的 Codex 桌面任务 `019fa1f5-8031-7450-883c-2462fc623703` 只收到旧版 SPEC/PLAN。首轮在红测前停止并指出 F-01A 输入不可用；缩小任务后，它报告七组问题均已回答。
- 精确红测以 exit 1 和 `CONTRACT_RED scanner_missing` 失败；完全相同的命令随后以 exit 0 通过 12 个具名合同组，并输出 `BOOTSTRAP_SCANNER_CONTRACT_PASS cases=12`。
- 该收据使用已废弃哈希 `600395...ED71` / `8A4BE...AFD`。仓库外 scanner/contract 哈希 `37CC6252...2D60` / `F0CA58FA...C516` 不是 F-01S 正式实现。后续评审发现其 staged-source 覆盖不足，因此只保留为历史证据。

## 当前 G-03P 复核

- 全新、无项目历史的任务 `019fa331-3da1-7f80-a37c-ac7abb135a46` 只收到 SPEC `6A0DB7...11E56` 和前一版 PLAN `D574B8...1D742`。
- 它得到精确的缺少 scanner 红测，并以未修改的合同完成八组绿测和全部十一个 helper。仓库外 contract/scanner SHA-256 为 `E970C52C...3A79B` / `097F5683...9F64`。
- 附加自扫描在合同的 index/worktree 字节中发现赋值 fixture，并以 exit 2 失败；该失败没有被隐藏或冒充 PASS。
- 最终 PLAN `E96C415A...972C1` 已强制要求运行时片段 fixture 和精确 `files=4` 自扫描。针对当前哈希的课程/SPEC 评审与质量/安全/许可证评审均无 Critical/Major 问题。
- 这仍是同类型 G-03P 修订证据，不能替代本手册规定的正式异类智能体运行。

## 正式 G-03 首次模型尝试

- 会话 `71a50d25-4cd7-48b1-9472-8107e82779ed` 使用 Claude Code `2.1.220`、端点 `ai2.1343263.xyz` 和模型 `claude-sonnet-5`；冻结哈希正确，初始目录精确只有 `SPEC.md`、`PLAN.md`。
- 智能体报告了两个哈希和完整文件列表，并读取 F-01S 卡片。它调用 Bash/Read 检查 Git 与 Windows PowerShell，创建了空的 `scripts/tests` 目录，但没有调用 Edit、没有写入两份脚本。
- 会话未提出问题，未报告 SPEC/PLAN 歧义，未执行精确红测、绿测或 tracked+staged 自扫描，也没有 diff。最终结果是空 `end_turn`、CLI exit 0；记录费用约 `$0.4712`。
- 主智能体独立检查隔离目录，实际文件仍只有两份冻结输入。新后置条件测试先因实现缺失而失败，最小实现后通过，并能把该目录判为 `required_artifact_missing`。本次是有效的正式异类失败收据，但不满足 PLAN 的 G-03 完成标准。

## 正式 G-03 第二次模型尝试

- 会话 `32b62490-7817-4d3d-8452-7a29a4de94ea` 使用 Claude Code `2.1.220`、端点 `ai2.1343263.xyz` 和模型 `claude-sonnet-4-6`；冻结哈希正确，初始目录精确只有 `SPEC.md`、`PLAN.md`。
- 智能体先尝试一个不存在的 Linux 路径，随后确认 Windows 临时目录中只有两份文件，读取 SPEC/PLAN 并使用 `certutil` 得到正确 SHA-256。由于 Read 工具按错误编码显示中文，日志中出现 mojibake，但 PLAN 的英文任务协议仍可读。
- 第 6 turn 后网关返回 `API Error: 504 Gateway Time-out`。Claude Code 记录 `subtype=success`、`is_error=true`、`stop_reason=stop_sequence`，runner 因此写 `CLAUDE_FAILED`、exit 1。费用约 `$0.1818`；隔离目录没有新增文件。
- 这是第二份正式异类失败收据。它把问题从单个 Sonnet 5 alias 扩展为当前网关对长 Claude Code agent run 的稳定性/兼容性风险，仍不能关闭 G-03。

## 当前阻塞

Claude Code `2.1.220`、正确端点认证和模型发现均已实际运行，但 `claude-sonnet-5` 与 `claude-sonnet-4-6` 都没有产出 F-01S。正式 G-03 只有在 Claude Code 或其他非 Codex 编码智能体按最终哈希产出问题、diff、红/绿和自扫描证据后才关闭；两次不完整收据、G-03P 或旧端点 401 收据都不能批准实现，也不能关闭 G-04。
