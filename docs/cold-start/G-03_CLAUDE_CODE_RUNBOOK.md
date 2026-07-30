# G-03 Claude Code 冷启动操作手册

## 当前状态

G-03 尚未完成，产品实现仍被 G-04 门禁阻塞。当前候选输入为：

- SPEC SHA-256：`14C03D688A09451DCA06F66507CE4510510A8A3BC550057376B0A1EF95270713`
- PLAN SHA-256：`95FF14D23DB92692BA005C3AA42598ABB5DDCFEE2DEFC28B950B00617C3EC663`
- 目标任务：`F-01S1`
- 固定模型：`claude-sonnet-4-6`
- 固定过程端点：`https://ai2.1343263.xyz`
- 总预算上限：`$1.00`，其中 intake `$0.20`、execution `$0.80`

这两个哈希必须在同哈希机械审计和双评审通过、学生重新确认后才可用于正式复测。任何 SPEC/PLAN 字节变化都必须更新本手册中的哈希并重走评审。

## 为什么不能直接在当前 Windows 终端正式运行

Claude Code 的 `--safe-mode` 只关闭自定义配置，不提供网络隔离。Claude 官方 sandbox 在 macOS、Linux 和 WSL2 上使用操作系统机制；原生 Windows 不支持该强制隔离。本次 execution 必须允许 Bash，又明确禁止网络，所以跟踪版 runner 在原生 Windows 会在询问 API key 前以 `EXECUTION_FAILED` 停止。

这里的限制来自正式 G-03 的隔离合同，而不是 Claude CLI 本身：Claude CLI 可以在 Windows 运行，但当前 runner 使用 Linux namespace 和 `bubblewrap` 实现只暴露一次性目录、断网、清空凭据环境以及有界终止整个候选进程树。原生 Windows 没有可直接等价替换的 `bwrap`/namespace 机制；仅安装 PowerShell 7 的 `pwsh` 仍不能把原生 Windows 运行算作该合同的正式证据。

正式运行环境必须是 Linux 或 WSL2，并同时提供：

```bash
command -v pwsh
command -v timeout
command -v bwrap
command -v socat
node --version
```

runner 会传入以下失败关闭策略：sandbox 必须可用、网络域名全部拒绝、禁止 unsandboxed escape、权限模式 `dontAsk`、禁用 WebFetch/WebSearch。缺少 `bwrap`、`socat`、`pwsh` 或 `timeout` 时不会询问 key，也不会调用模型。sandbox 只读挂载 `/etc`、`/usr`、`/bin`、`/lib`、`/lib64` 和 PowerShell 运行时；其中 `/etc` 只为 PowerShell/.NET 初始化提供系统配置，不开放写入。询问 key 前还会真实启动一次 bubblewrap 预检，验证凭据环境变量不可见、宿主 `/mnt` 不可见、外网不可达、写入只落在一次性目录内，并用超时样例验证进程树能够终止；任何一项失败都不会调用模型。

## 运行时反馈日志合同

runner 必须在创建本次证据目录后立即向终端输出该目录，并在其中创建 UTF-8 无 BOM 的 `status.log`。该文件采用每行一个固定字段 JSON 对象，字段仅允许 `timestamp`、`stage`、`event` 和可选的非负 `elapsed_seconds`；不得记录 API key、认证头、prompt、模型原始输出、材料正文、文件内容或任意异常文本。

至少记录以下阶段：runner 启动、capsule 校验、输入哈希校验、平台检查、bubblewrap 预检、等待隐藏凭据、intake、execution、独立 replay 和最终状态。intake 与 execution 运行期间每 15 秒追加一次 `heartbeat`，包含累计秒数；阶段完成记录受控结果码，不复制子进程 stdout/stderr。所有受控退出都必须同时写最终状态到 `status.log` 和 `completion.json`。原生 Windows、缺少命令或预检失败必须给出明确的受控事件，不得只留下静默非零退出。

观察运行状态：

```powershell
# Windows 侧查看映射目录时
Get-Content -Wait <evidence-root>\status.log
```

```bash
# WSL2/Linux 内
tail -f <evidence-root>/status.log
```

## 运行前必须完成

1. 撤销此前在聊天中暴露过的 API key，只创建一次新的临时 key。
2. 确认上面的 SPEC/PLAN 哈希仍与仓库一致：

```powershell
Get-FileHash SPEC.md,PLAN.md -Algorithm SHA256
```

3. 在 Windows 侧先运行所有无网络合同：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cold_start/update_agent_capsules.ps1 -Mode Check
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cold_start/tests/agent_capsules_contract.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cold_start/tests/g03_runner_contract.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cold_start/tests/g03_runner_entrypoint_contract.ps1
```

4. 在 Linux/WSL2 内安装项目局部 Claude Code，不写系统级 Node 目录：

```bash
mkdir -p tmp/toolchains/claude-code
npm install --prefix tmp/toolchains/claude-code @anthropic-ai/claude-code@2.1.220
```

5. 核对该过程工具的使用条款。固定版本 `@anthropic-ai/claude-code@2.1.220` 的 `package.json` 声明 `SEE LICENSE IN README.md`；README 指向 Anthropic Commercial Terms 和 Privacy Policy，而不是普通开源许可证。正式运行前由学生确认接受这些条款。它只用于 G-03 过程验证，不进入产品源码或分发物。

## 正式命令

不要在提示符为 `(base) PS E:\...>` 的原生 Windows PowerShell 中直接执行下一段 `pwsh` 命令。先从 Windows 进入 WSL2，再切到 WSL 映射后的项目目录：

```powershell
wsl
```

```bash
cd /mnt/e/Personal_Documentary/ResearchProjects/ProjectB
command -v pwsh timeout bwrap socat node
```

只有上一条同时列出五个可执行文件后，才在同一个 WSL2 终端运行：

```powershell
pwsh -NoProfile -File ./scripts/cold_start/run_g03_claude.ps1 `
  -AgentLanguage Auto `
  -Model claude-sonnet-4-6 `
  -MaxTotalBudgetUsd 1.00 `
  -ExpectedSpecSha256 14C03D688A09451DCA06F66507CE4510510A8A3BC550057376B0A1EF95270713 `
  -ExpectedPlanSha256 95FF14D23DB92692BA005C3AA42598ABB5DDCFEE2DEFC28B950B00617C3EC663 `
  -ClaudeCli ./tmp/toolchains/claude-code/node_modules/@anthropic-ai/claude-code/bin/claude
```

API key 只在隐藏输入框输入。runner 不把子进程原始 stdout/stderr 写入磁盘；只保存白名单结构化字段、费用、工具调用计数、问题、产物哈希、独立重放结果和必要的脱敏 `process-diagnostic.json`。诊断文件只包含阶段、退出码、超时标志和固定枚举码，不包含原始错误、prompt、路径或凭据。认证环境变量在 `finally` 中清除，Claude 子进程凭据继承 scrub 保持启用。

## 两段执行

1. Intake：全新 session，5 分钟、`$0.20`，只允许 runner 提供的严格 UTF-8 capsule 提取命令。它必须返回两份哈希、完整两文件列表、English、`F-01S1`、固定 acceptance ID 和空歧义数组。任何写入或额外目录都会失败。
2. Execution：第二个全新 session，20 分钟、`$0.80`，只允许强制 sandbox 内的 Bash。原生 Read 和 Edit 均不授权；它也不能使用网络、commit 或第三份项目上下文。
3. Coordinator replay：runner 不相信 Claude 自报。它先验证 stream-json 中真实发生过、顺序正确且有对应 tool result 的精确红测和绿测；Claude 失败工具结果允许且只允许规范化的 `Exit code 1` 加 `CONTRACT_RED scanner_missing`，其他退出码或额外行均失败。随后清除认证环境变量，在新的无凭据、断网、限挂载 bubblewrap 中重放；每次重放和直接扫描前后都核对候选 contract/scanner 原始 SHA-256，防止可写重放根替换验证器。coordinator 自有行为 oracle 还会独立检查所有列出的直接规则及前缀变体、下限/上限/超限长度、标点与阻断邻接边界、严格 UTF-8、稳定排序和 JSON 键序、脱敏、缺参错误和两个产物的精确字节，候选脚本自报 PASS 不能替代这些检查。最终证据会持久化规范化且有序的 TDD receipt。

只有全部满足才写正式 schema `projectb.g03.formal.v1` 和状态 `G03_EVIDENCE_READY`。`TestScenario` 只能写到系统临时目录，schema 固定为 `projectb.g03.test.v1`，状态以 `TEST_ONLY_` 开头，不能作为正式收据。

## 状态含义

- `CAPSULE_INVALID`：capsule 漂移、正文哈希或标记错误。
- `UTF8_INVALID`：BOM、非法 UTF-8 或 `U+FFFD`。
- `INTAKE_FAILED`：哈希、文件、费用或结构化协议不匹配。
- `INTAKE_AMBIGUOUS`：智能体明确报告歧义，execution 不启动。
- `EXECUTION_FAILED`：网关、模型、超时、预算、sandbox 或 execution 协议失败。
- `COLD_START_INCOMPLETE`：产物集合、函数、输入哈希、红绿重放或直接扫描失败。
- `G03_EVIDENCE_READY`：仅表示候选证据已通过 runner 独立复验；仍需把事实写入 `SPEC_PROCESS.md` 并完成课程门禁结论。

## 历史失败证据

- `71a50d25-4cd7-48b1-9472-8107e82779ed`：Sonnet 5，约 `$0.4712`，空 `end_turn`，仅创建空目录。
- `32b62490-7817-4d3d-8452-7a29a4de94ea`：Sonnet 4.6，约 `$0.1818`，哈希验证后网关 504。

两次都没有 F-01S1 产物或红绿收据，只能作为失败历史，不能关闭 G-03。
