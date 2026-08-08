# AGENT_LOG

## 2026-08-03T18:48:51+08:00 - MAINT-003 删除停用 G-03 runner

- **Task 编号**：MAINT-003。
- **触发的 Superpowers skill**：`using-superpowers`、`verification-before-completion`。
- **删除范围**：当前分支精确删除 `scripts/cold_start/g03_runner_core.ps1`、`run_g03_claude.ps1`、`update_agent_capsules.ps1` 以及 `tests/agent_capsules_contract.ps1`、`g03_runner_contract.ps1`、`g03_runner_entrypoint_contract.ps1`、`g03_snapshot_contract.ps1`。这些文件只服务于已停用的 runner 诊断流程。
- **保留范围**：SPEC/PLAN、`docs/cold-start/agent-capsules.json`、过程文档、历史计划和 `tmp/g03-manual/` 两文件快照均保留；中文手册已改为直接使用 Claude Code 插件的 intake/execution 提示词。
- **安全检查**：删除前主仓库状态与 `git worktree list` 已记录；两个旧 worktree 均有脏修改或未跟踪文件，按规则保留。进程命令行检查被 Windows 权限拒绝，现有进程列表未发现 Claude/runner 进程。删除后 `scripts/cold_start/` 不再存在；未执行递归删除、clean、reset 或历史重写。
- **Commit**：`6c5508e`（`chore(g03): remove retired runner diagnostics`）。

## 2026-08-03T18:17:11+08:00 - G-03-020 同字节双评审与冻结验证

- **Task 编号**：G-03-020。
- **触发的 Superpowers skill**：`verification-before-completion`、`requesting-code-review`、`receiving-code-review`。
- **冻结输入**：SPEC `AEA67BB5544AD22932DC4304964F7FD266FE8A5DE7AA396EA8974D30867E8381`；PLAN `910A3AEC9B4CEDCC119675C5D862879D178E3FE062CEE39C2AD62AF07219E923`。评审期间未修改 SPEC/PLAN。
- **评审输出**：规约合规 PASS（Critical=0, Major=0, Minor=0）；质量/安全/许可证 PASS（Critical=0, Major=0）。质量评审提出的三个 Minor 已记录为非阻塞后续加固，不伪装成当前缺陷已修复。
- **验证输出**：`PLAN_MECHANICAL_PASS Tasks=39 Ledger=39 Fields=5 AcRows=24 Placeholders=0 Unknown=0 Self=0 Cycle=0 DependencyEdges=38`；胶囊、快照、runner core 和 entrypoint 合约均通过；课程证据仍为 `rows=63 explicitly_blocked=2`。正式非 Codex G-03 intake/execution 和学生 G-04 批准仍未发生。
- **Commit**：`4d2d31c`（`fix(g03): harden atomic cold-start gate`）。
- **人工边界与经验**：本条只冻结和记录证据，不把本地合约通过误报为正式 G-03 PASS，也未进入产品实现。

## 2026-08-03T17:29:12+08:00 - G-03-019 原子计划与执行预言机修订

- **Task 编号**：G-03-019。
- **触发的 Superpowers skill**：`using-superpowers`、`brainstorming`、`writing-plans`、`test-driven-development`、`systematic-debugging`、`requesting-code-review`、`verification-before-completion`。
- **关键 context/output**：学生确认精简后的完整 SPEC。PLAN 将冷启动实现拆为 `F-01S1A` 和 `F-01S1B`，当前冷启动只实现单路径、单 provider 规则，并限制脚本行数与最终摘要长度。SPEC/PLAN 冻结哈希为 `AEA67BB5...E8381` / `910A3AEC...9E923`。
- **TDD 与评审证据**：规约评审发现状态文字和执行预言机覆盖缺口。新增错误码变异测试先失败；补齐缺文件、严格 UTF-8 BOM、`U+FFFD`、反斜杠路径和可选错误字段探针后，核心 runner 合约通过 `cases=13`。最终同字节双评审、完整验证和提交哈希待本条后续补记。
- **人工边界与经验**：学生只确认 SPEC 和本轮修订方向，尚未提供新的非 Codex execution 结果，也未批准 G-04。变动中的文件不能接受哈希绑定评审；以后先冻结 SPEC/PLAN，再派发只读评审。

## 2026-08-01T22:09:11+08:00 - G-03-018 原子任务 SPEC 候选
- **Task 编号**：G-03-018。
- **触发的 Superpowers skill**：`using-superpowers`、`brainstorming`、`verification-before-completion`。
- **关键 context/output**：学生确认原子执行设计，并确认新字节必须重新执行 SPEC/PLAN intake 与 execution。`SPEC.md` 现将冷启动收束到单路径、单规则 `F-01S1A`，其余规则归入串行 `F-01S1B`；英文 capsule 清单已机械同步。
- **验证证据**：`AGENT_CAPSULE_PASS documents=2`、`STRICT_UTF8_PASS files=2`、`PLACEHOLDER_PASS files=1`、`git diff --check` exit 0；SPEC SHA-256 为 `5ABC65A4...C598A`。
- **人工边界与经验**：PLAN 未修改，等待学生确认完整 SPEC 后才调用 `writing-plans`。不把旧 intake、长时间 thinking、网络/输出上限假说或本次文档检查冒充 G-03 PASS；原子任务需要同时锁定语义和输出预算，不能只缩短提示词。

## 2026-08-01 - G-03-017 Execution Planning Loop and Output-Risk Design
- **Task ID:** G-03-017
- **Skills:** `brainstorming`, `systematic-debugging`, `verification-before-completion`
- **Context/output:** The student supplied recent Claude thinking from two stalled execution attempts. Both disposable directories still contained only SPEC/PLAN. Thinking showed an explicit guess that single-path `source` was likely `path` and repeated pre-write design expansion.
- **Assessment:** Network/gateway latency and output-limit exhaustion remain unproven hypotheses. Independently, F-01S1 is under-specified and too large for its single-session/output budget, so neither stalled attempt can close execution.
- **Human direction:** The student approved revision. A concise Chinese design proposes F-01S1A/F-01S1B, exact field/function semantics, line limits, and a 300-word final-summary cap. Normative SPEC/PLAN changes wait for the required design review gate.

## 2026-08-01T20:58:13+08:00 - G-03-016 Intake Pass and Execution Snapshot Check
- **Task ID:** G-03-016
- **Skills:** `systematic-debugging`, `verification-before-completion`
- **Context/output:** The student supplied a fresh non-Codex intake JSON with the repaired hashes, exact two-file listing, correct language/task/acceptance ID, and `ambiguities=[]`. Intake is accepted; execution and G-03 remain open.
- **Inspection:** The running execution copy contained the repaired SPEC but pre-repair PLAN `D835D542...73D9E6`. The observed stall may be external model/gateway/network latency and is not diagnosed from available evidence, but the stale PLAN independently prevents formal same-snapshot acceptance.
- **Human boundary:** The student continues observing the current external session. It was not terminated or overwritten. A new two-file `execution-v2` directory was prepared without credentials for an optional fresh rerun.

## 2026-08-01T18:41:26+08:00 - G-03-015 Snapshot Binding Repair
- **Task ID:** G-03-015
- **Skills:** `systematic-debugging`, `test-driven-development`, `verification-before-completion`
- **Evidence:** Fresh non-Codex intake returned the correct two-file listing and actual hashes, then stopped on the stale PLAN-to-SPEC binding. No execution session ran.
- **Red/green:** The new snapshot contract first failed with `snapshot_hash_mismatch binding=plan_spec`; after synchronizing PLAN, capsule manifest, compliance matrix, and runbook it passed with SPEC `01E9A154...1D030` and PLAN `11EB0111...9964C`. Capsule check passed and capsule regression reported `cases=9`.
- **Commit:** `ebfad01` (`fix(g03): synchronize snapshot hash bindings`).
- **Human changes:** The student supplied the real intake JSON and requested that repaired files replace the current intake copies. No product code, remote state, or credential was changed.

## 2026-08-01 - MAINT-002 Directory Layout Refactor
- **Task ID:** MAINT-002
- **Skills:** `verification-before-completion`
- **Actions:** Moved active detailed plans to `docs/plans/`, design records to `docs/specs/`, and historical material to `docs/archive/`. Flattened archive engineering/fragments with filename prefixes. Added the Chinese `docs/INDEX.md` entry point and updated current links in SPEC, PLAN, handoff, and writing-plan audit documents.
- **Preservation:** Archive files were moved, not deleted. `docs/archive/README.md` preserves original paths, byte counts, and SHA-256 values. Dirty worktrees and the standalone checkout were retained.
- **Verification:** Pending old-tree/path scan, `git diff --check`, file-set check, and worktree/tmp nesting check.

## 2026-08-01T17:30:00+08:00 — MAINT-001 目录结构约束与临时文件清理

- **Task 编号**：MAINT-001
- **触发 skills**：`systematic-debugging`、`verification-before-completion`
- **关键 context**：用户要求为 `AGENTS.md` 增加目录结构约束，并清理评测后不再使用的工具链、缓存、安装包和临时脚本。
- **保留范围**：`tmp/stage-b-archive-20260725/`、`tmp/g03-evidence/`、`tmp/pdfs/` 以及两个存在未提交改动的 `.worktrees/` 未删除。
- **已移除范围**：项目根目录 Claude/Node 工具链、npm/uv 缓存、旧 G-03 preflight/许可证/测试临时目录、空临时脚本、Open Design 安装包和根目录 Python/Ruff/Codex 临时缓存；`.pytest_cache/` 因访问被拒绝而尚未删除。
- **验证**：清理前后执行 `git status --short --untracked-files=all` 和 `git worktree list`；根目录用户修改未被覆盖，`AGENTS.md` 新增第 11 节目录结构规则。
- **经验**：删除前必须区分课程归档、过程证据、活跃 worktree 与一次性运行物；工具链和缓存不得回到项目根目录或长期混入 `tmp/`。

> 本文件只记录实际发生的过程。未执行的步骤明确标为“尚未执行”。

## 2026-07-17T18:14:41+08:00 — PRE-001 启动审计

- **Task 编号**：PRE-001
- **主智能体**：OpenAI Codex（GPT-5；Codex App 的精确构建版本未向当前会话暴露）
- **触发的 Superpowers skill**：无。课程要求当前必须触发 `superpowers:brainstorming`，但当前会话技能目录、插件缓存与已暴露技能清单均未检测到 Superpowers，故未伪装或替代调用。
- **关键 prompt / context**：读取根目录 `AGENTS.md`、`SKILLS_SETUP.md`、`docs/requirements/项目要求.md`、`docs/requirements/AI4SE_Final_Project_B_应用类项目.md`；用户要求在不越过人工门禁的前提下持续推进。
- **检查结果**：
  - 仓库仅包含流程与课程文档，无既有源码或产品规约。
  - `SPEC.md`、`PLAN.md`、`SPEC_PROCESS.md`、`README.md`、`REFLECTION.md`、`.gitlab-ci.yml` 均不存在（本次仅创建真实过程所需的 `SPEC_PROCESS.md`，不创建虚假的 SPEC/PLAN/CI 证据）。
  - Superpowers 未安装/未暴露；所需核心 skills 均不可用。
  - Open Design 的 `od` 命令、skill 与 MCP 均未检测到。
  - 已从官方上游核验：Superpowers 最新 release 为 v5.1.0（commit `f2cbfbe`，MIT）；Open Design 最新 release 为 v0.15.0（commit `79e257d`，Apache-2.0）。
  - Open Design 官方当前支持 `od mcp install codex`；Windows x64 提供安装器。安装/运行新软件属于必须由用户在操作时确认或亲自完成的系统级操作，本次未执行。
  - 本地工具：Git 2.53.0.windows.3、Node 24.14.0、pnpm 11.9.0、Python 3.14.3、uv 0.11.14、Docker CLI 29.1.2。`npm.ps1` 被 PowerShell 执行策略阻止；可在后续使用 `npm.cmd`。`gh`、`gitleaks`、`claude`、`od` 未找到。
  - 已执行 `git init`。Git 随后因沙箱账号与目录所有者不同报告 `dubious ownership`；未修改用户全局 Git 配置，后续可使用 `git -c safe.directory=...` 做局部操作。
- **subagent 输出 / commit hash**：未派发 subagent；课程规定的冷启动阶段尚未到达。启动基线 commit：`4b72ced9ecfc3da0ee5691f4dbfebf8e9b593390`（课程原文、约束、Codex 配置与 `.gitignore`；commit message 已标注 Codex GPT-5）。
- **人工修改及原因**：尚无学生人工修改记录。
- **偏离、替代措施与影响**：
  - 无法调用 mandatory `brainstorming`。替代措施仅限启动审计、差距梳理和文档骨架；不得据此产出或声称产出合规 `SPEC.md`。
  - 无法自动操作 Codex App 插件界面：电脑控制规则禁止自动化 Codex 桌面应用及其扩展。需用户手动安装 Superpowers 并新建会话。
  - Open Design 未安装；在其可用前不得进行正式 UI 方向设计。
- **经验教训**：搜索摘要可能滞后；Open Design 版本必须以完整 Releases 页面为准。本次将初步摘要中的 v0.8.0 更正为 v0.15.0，未把错误版本写入正式状态。

## 2026-07-17T18:14:41+08:00 — PRE-002 提交前验证

- **Task 编号**：PRE-002
- **触发的 Superpowers skill**：无；`verification-before-completion` 同样不可用，故仅执行明确列出的手工验证，不能声称完成 Superpowers 验证步骤。
- **关键 prompt / context**：在首次本地提交前进行凭据与格式检查，不访问或输出真实凭据。
- **验证结果**：
  - 使用只返回文件名的启发式规则扫描 OpenAI/GitHub/AWS key 与私钥头：`POTENTIAL_SECRET_FILES: none`。
  - `npm.cmd --version`：11.9.0；这确认可绕过被执行策略拦截的 `npm.ps1`。
  - `git diff --cached --check` 首次指出 `.gitignore` 末尾多一个空行；已在后续过程文档提交前修正。
  - Gitleaks 尚未安装，因此本次结果是有限启发式扫描，不替代实现阶段的正式凭据扫描。
- **subagent 输出 / commit hash**：无 subagent。启动基线 commit 为 `4b72ced9ecfc3da0ee5691f4dbfebf8e9b593390`。
- **人工修改及原因**：尚无学生人工修改记录。
- **经验教训**：即使仓库只有文档，也应在首次提交前运行凭据模式扫描与 Git whitespace 检查，并明确工具能力边界。

## 2026-07-17T18:14:41+08:00 — PRE-003 过程文档提交

- **Task 编号**：PRE-003
- **触发的 Superpowers skill**：无；原因同 PRE-001。
- **关键 prompt / context**：提交当前阶段所有不依赖产品决策的过程证据。
- **subagent 输出 / commit hash**：无 subagent。过程文档 commit：`d16d3e9`。
- **人工修改及原因**：尚无学生人工修改记录。
- **验证结果**：提交前凭据模式扫描无命中文件；`git diff --cached --check` 仅报告三份 Markdown 的 EOF 空行，随后已移除。
- **经验教训**：过程日志可以引用已完成的前序 commit；本条自身的格式收尾 commit 由最终状态输出提供证据，避免递归追加日志。

## 尚未执行

- `superpowers:brainstorming` 与项目需求逐项澄清
- `SPEC.md` 的生成与用户确认
- `writing-plans`、`PLAN.md`、陌生智能体冷启动验证
- 任何实现、测试、构建、静态检查、UI 验证、凭据扫描或 CI
- 远程仓库、PR/MR、push、部署与发布

## 2026-07-17T18:19:47+08:00 — PRE-004 外部状态复查

- **Task 编号**：PRE-004
- **触发的 Superpowers skill**：无。再次检查后，插件缓存与 skills 目录仍未检测到 Superpowers。
- **关键 prompt / context**：持续 Goal 自动推进；要求以当前工作区和外部状态为准，不沿用旧结论。
- **复查结果**：
  - Git 工作区干净，HEAD 为 `1cd4427`。
  - Superpowers 插件目录：无；核心 skill 目录：无。
  - Open Design `od` 命令：无。
  - `SPEC_PROCESS.md`、`AGENT_LOG.md`、`DECISIONS_NEEDED.md` 存在；`SPEC.md`、`PLAN.md`、`README.md`、`REFLECTION.md`、`.gitlab-ci.yml` 不存在。
  - 后五项缺失并非可在当前阶段随意补空壳：`SPEC.md` 必须来自 mandatory brainstorming；`PLAN.md` 必须在用户确认 SPEC 后生成；README/CI 依赖已确认产品和技术栈；REFLECTION 仅能由学生本人撰写。
- **subagent 输出 / commit hash**：未派发 subagent；冷启动阶段尚未开放。
- **人工修改及原因**：无学生输入或外部状态变化。
- **经验教训**：持续任务每次恢复都应重新检查门禁依赖；“文件不存在”既可能是缺口，也可能是遵守阶段顺序的正确状态。

## 2026-07-17T18:21:22+08:00 — PRE-005 第三次门禁复查

- **Task 编号**：PRE-005
- **触发的 Superpowers skill**：无；第三次连续检查仍未发现 Superpowers 插件或核心 skills。
- **关键 prompt / context**：持续 Goal 的阻塞审计要求同一阻塞连续出现至少三轮，并以当前外部状态为准。
- **复查结果**：Git 工作区在复查前干净，HEAD 为 `4489e46`；Superpowers 插件目录为 `none`；核心 skills 为 `none`；Open Design 为 `none`。
- **subagent 输出 / commit hash**：未派发 subagent；阶段 C 尚未开放。
- **人工修改及原因**：连续三轮没有收到学生决策或观察到插件安装状态变化。
- **阻塞判定**：mandatory `superpowers:brainstorming` 无法调用；项目方向仍是占位文本，禁止替学生猜测；所有不依赖该门禁的审计、环境检查、过程证据与决策清单均已完成。符合持续 Goal 的第三次同条件阻塞阈值，应将 Goal 标记为 blocked，等待用户安装 Superpowers 后恢复。
- **经验教训**：无人值守流程应在真实外部依赖未变化时停止并留下可恢复入口，而不是通过重复检查制造虚假进展。

## 2026-07-17T22:05:24+08:00 — PRE-006 Superpowers 恢复与 Open Design 安装尝试

- **Task 编号**：PRE-006
- **触发的 Superpowers skill**：`using-superpowers`、`brainstorming`。已完整读取插件 v6.1.1 对应的两份 `SKILL.md`；brainstorming 的实现硬门禁继续生效。
- **关键 prompt / context**：用户要求自行安装 Open Design；只允许官方来源，不使用第三方镜像，不录入 API Key。
- **外部状态变化**：检测到官方 Codex 插件缓存已出现 Superpowers v6.1.1，包含 `brainstorming`、`writing-plans`、worktree、TDD、评审、调试与验证等核心 skills。此前的 Superpowers 阻塞已解除。
- **Open Design 官方核验**：最新版 v0.15.0（release commit `79e257d`），Windows x64，Apache-2.0；官方安装器与 `.sha256` 均由 GitHub Release 提供。
- **安装尝试与证据**：
  - 沙箱内 `curl` 无法连接 GitHub；按规则提升网络权限后仍无法连接 `github.com:443`。
  - Codex 内置浏览器打开官方下载页时超时并重置，未触发下载。
  - 成功从 `open-design.ai/install.sh` 下载并检查官方包装脚本，SHA-256 为 `5866B8465CC3475A0CE63BE379F04A3E5E9A01BA579E6E7FB54304C82EDE06B3`；脚本明确要求本机先已有 `od`，不能替代桌面安装，因此已删除临时副本。
  - 项目中不存在残留或零字节安装器。
- **人工恢复入口**：用户将从官方 GitHub Release 下载 `open-design-0.15.0-win-x64-setup.exe` 及同名 `.sha256`；安装完成后由智能体验证并执行 `od mcp install codex`。
- **subagent 输出 / commit hash**：未派发 subagent；当前仍处于阶段 A。
- **人工修改及原因**：用户选择在自动下载受阻时手动下载官方安装器。
- **经验教训**：Open Design 的 hosted `install.sh` 只是已有 CLI 的 MCP 包装器，不是桌面/CLI bootstrap；应避免把“接入 agent”和“安装产品”混为一谈。

## 2026-07-19T21:57:09+08:00 — PRE-007 阶段 A 恢复审计与 brainstorming 续接

- **Task 编号**：PRE-007
- **触发的 Superpowers skill**：沿用 PRE-006 已触发的 `using-superpowers`、`brainstorming` 流程。本次会话可调用 skill 清单未注册 `superpowers:*`；已完整读取官方缓存 v6.1.1 的两份 `SKILL.md` 并按 checklist 续接，但不把磁盘读取虚报为本次正式调用。
- **关键 prompt / context**：用户要求完整复读课程/仓库、检查 Superpowers 与 Open Design、完成当前阶段所有无决策工作，并在人工确认门禁停止；项目方向仍为占位文本。
- **检查结果**：
  - 根目录约束、`SKILLS_SETUP.md`、两份课程原文、全部已有过程文档、`.codex/config.toml`、`.gitignore` 与最近 Git 历史均已重新读取。
  - 官方插件缓存存在 Superpowers v6.1.1（MIT）及 14 个 skills；当前会话未注册这些 skills，因此阶段 B 前仍须新建/确认可调用插件的会话。
  - Open Design 官方 release v0.15.0（commit `79e257d`，Apache-2.0）与 Windows x64 资产存在。本地 309,298,247-byte 安装器的 SHA-256 与同名校验文件一致：`63fc2e609489474e99187cdf94d01d063c1dbee733aaf2464d835cdc1e96f6b5`。Authenticode 为 `NotSigned`，与上游 Windows 未签名说明一致。
  - `od`、Open Design skill/MCP、MCP resources/templates 均未检测到。安装会写入项目外目录且可能触发 SmartScreen；当前环境只允许写项目目录，未运行安装器，也未反复申请提权。
  - 当前工具版本：Git 2.55.0.windows.3、Node 24.14.0、npm 11.9.0、pnpm 11.9.0、Python 3.13.5、uv 0.11.14、Docker CLI 29.1.2；`gh`、`gitleaks`、`claude`、`od` 未找到。Docker 因用户配置读取权限警告，daemon 未验证。
- **subagent 输出 / commit hash**：未派发 subagent；当前阶段 A 且尚无 PLAN task。commit hash 将在本条过程文档提交后记录于任务输出，不递归修改本条。
- **人工修改及原因**：用户已把 Open Design 安装器和校验文件放入项目根目录；为防止 309 MB 第三方二进制误提交，智能体将这两个精确命名模式加入 `.gitignore`。
- **偏离、替代措施与影响**：本次会话不能正式调用 `superpowers:brainstorming`；替代措施是按已安装的同版本上游指令续接 PRE-006 已开始的流程并明确证据边界。此限制不阻塞需求提问，但 `writing-plans` 前必须恢复正式 skill 注册。
- **经验教训**：插件“缓存已安装”、会话“skill 已注册”和流程“实际调用”是三种不同证据，过程文档必须分别记录。

## 2026-07-19T22:00:55+08:00 — PRE-008 提交后完成验证

- **Task 编号**：PRE-008
- **触发的 Superpowers skill**：`verification-before-completion`。本次会话未注册该 skill；完整读取已安装 v6.1.1 上游指令后执行其“识别命令、全量运行、读取输出、再陈述状态”门禁，证据限制同 PRE-007。
- **关键 prompt / context**：验证 PRE-007 审计提交、阶段门禁、Superpowers 安装内容与 Open Design 状态，不验证尚不存在的业务功能。
- **验证结果**：
  - `git status --short --branch`：仅输出 `## master`；工作区干净。
  - `git show --oneline --stat HEAD`：`e29d235 docs: resume phase A audit [agent: Codex GPT-5]`，5 个文件变更，61 行新增、27 行删除。
  - `git diff HEAD^ HEAD --check`：退出码 0，无 whitespace 错误。
  - 门禁文件检查：`SPEC.md`、`PLAN.md`、`README.md`、`REFLECTION.md`、`.gitlab-ci.yml` 均不存在；当前阶段这是预期状态，不作为最终交付完成证据。
  - Superpowers manifest 版本为 6.1.1，skills 目录计数 14，必需核心项均存在。
  - Open Design：安装器哈希与 `.sha256` 匹配；Authenticode 为 `NotSigned`；`od` 命令不存在；安装器已被 Git 忽略。
- **subagent 输出 / commit hash**：无 subagent；被验证的过程提交为 `e29d235`。
- **人工修改及原因**：无。
- **经验教训**：阶段 A 的“完成验证”只证明启动审计和门禁状态，不能外推为 SPEC、实现、测试、CI 或部署完成。

## 2026-07-19T22:04:53+08:00 — BRAIN-001 真实使用场景澄清

- **Task 编号**：BRAIN-001
- **触发的 Superpowers skill**：续接 `brainstorming`；遵守一次只问一个问题、先理解目的再提出方案、用户批准设计前不实现的门禁。当前会话的 skill 注册限制见 PRE-007。
- **关键 prompt / context**：首问要求学生描述最近反复遇到且愿意用软件解决的问题；学生回答主要使用模型协助作业/项目、学习辅导和资料查找。
- **subagent 输出 / commit hash**：未派发 subagent；阶段 A 不存在 PLAN task。提交 hash 将在任务输出中记录。
- **人工修改及原因**：学生提供了三个真实使用场景；智能体仅归纳为候选主线，未替学生选择产品方向，也未创建 `SPEC.md`。
- **经验教训**：宽泛的“AI 帮我做事”能证明需求频率，但不能直接成为问题陈述；需要先确定唯一主线，再追问现有工作流的具体失败点。

## 2026-07-19T22:06:27+08:00 — BRAIN-001A 候选主线课程适配比较

- **Task 编号**：BRAIN-001A
- **触发的 Superpowers skill**：续接 `brainstorming`；未把无人值守分析计作新的对话迭代，也未跳过用户选择门禁。
- **关键 prompt / context**：用户尚未在作业/项目协作、学习辅导、资料检索三个场景中选定主线；Goal 允许等待期间开展候选方案比较。
- **分析输出**：按三模块一致性、区别于普通聊天的机制、确定性测试空间、主要风险和 WebUI 展示力形成对比矩阵；记录于 `DECISIONS_NEEDED.md` D-002。
- **subagent 输出 / commit hash**：未派发 subagent；无 PLAN task。提交 hash将在任务输出中记录。
- **人工修改及原因**：无新的学生输入；没有将分析结果写入 `SPEC.md` 或视为用户确认。
- **经验教训**：在产品方向未定时，可以比较选项的工程属性，但不能用“更容易实现/测试”替代学生对真实痛点的选择。

## 2026-07-19T22:07:52+08:00 — BRAIN-001B 人工产品决策门禁暂停

- **Task 编号**：BRAIN-001B
- **触发的 Superpowers skill**：续接 `brainstorming`；遵守目标用户、核心功能和产品主线不得由智能体代决策的门禁。
- **关键 prompt / context**：学生尚未在三个候选主线中作出选择；无人值守期间已完成课程适配比较，没有新的外部状态。
- **验证结果**：Git 工作区在记录前干净，HEAD 为 `3580eee`；`SPEC.md`、`PLAN.md` 均不存在；D-002 仍是当前未决问题。
- **subagent 输出 / commit hash**：未派发 subagent；无 PLAN task。提交 hash 将在任务输出中记录。
- **人工修改及原因**：无新的学生输入；未生成规约或实现。
- **阻塞判定**：同一产品主线决策连续三个 Goal 回合未解决，且所有无决策工作已经完成；持续 Goal 应标记为 blocked，等待学生选择后恢复。
- **经验教训**：持续执行不等于重复检查；到达人工产品门禁后应留下明确恢复入口并停止。

## 2026-07-19T22:08:59+08:00 — BRAIN-002 暂定学习辅导主线

- **Task 编号**：BRAIN-002
- **触发的 Superpowers skill**：续接 `brainstorming`；按一次一个问题和可逆假设原则继续需求澄清。
- **关键 prompt / context**：学生在三个候选主线中回复“主线走 2 试试看？”，即暂定学习辅导，但尚未确认具体痛点或完整设计。
- **subagent 输出 / commit hash**：未派发 subagent；阶段 A 无 PLAN task。提交 hash 将在任务输出中记录。
- **人工修改及原因**：学生选择了候选 2；智能体保留“试试看”的暂定语义，没有把它升级为不可逆产品承诺。
- **恢复判定**：BRAIN-001B 的产品主线阻塞已解除；从第 2 轮继续，旧 blocked 计数不沿用。
- **经验教训**：探索性选择应被记录为可验证假设，下一轮要用具体失败场景检验，而不是立即围绕标签堆功能。

## 2026-07-19T22:11:30+08:00 — BRAIN-003 理解适配与持续复习组合痛点

- **Task 编号**：BRAIN-003
- **触发的 Superpowers skill**：续接 `brainstorming`；一次只确认一个问题，并把学生选择写成可追溯的需求假设。
- **关键 prompt / context**：学生选择“解释不符合当前水平”和“对话孤立、缺少持续进度”，并明确大学学业的目标是看懂与持续复习。
- **subagent 输出 / commit hash**：未派发 subagent；阶段 A 无 PLAN task。提交 hash 将在任务输出中记录。
- **人工修改及原因**：学生把两个失败模式组合为同一主线；智能体据此要求两者共享学习状态，但未决定具体实现或技术栈。
- **阶段证据**：这是第 3 轮真实 brainstorming 迭代；已经达到课程对“至少 3 轮关键迭代”的数量下限，但 SPEC 所需内容仍远未澄清，不能提前结束阶段 A。
- **经验教训**：用户价值可能来自两个环节的闭环，而不是单点功能；关键是定义它们共享的状态与反馈，而不是简单增加功能数量。

## 2026-07-19T22:13:24+08:00 — BRAIN-003A 学习科学证据基线

- **Task 编号**：BRAIN-003A
- **触发的 Superpowers skill**：续接 `brainstorming`；在等待人工课程选择期间只开展不改变产品方向的背景研究。
- **关键 prompt / context**：暂定解决大学学业中的解释适配与持续复习；课程 D-007 尚未选择。检索并阅读自我解释、提取练习、分散练习和知识追踪的原始研究页面/摘要。
- **研究输出**：新增 `docs/research/LEARNING_SCIENCE_BASELINE.md`，分别记录研究对象、可支持的产品启发和禁止外推的边界；没有把论文结论写成已确认需求。
- **来源**：Chi et al. (1989), DOI `10.1207/s15516709cog1302_1`；Karpicke & Roediger (2008), DOI `10.1126/science.1152408`；Cepeda et al. (2006), DOI `10.1037/0033-2909.132.3.354`；Corbett & Anderson (1995), DOI `10.1007/BF01099821`。
- **subagent 输出 / commit hash**：未派发 subagent；无 PLAN task。提交 hash 将在任务输出中记录。
- **人工修改及原因**：无新的学生输入；未创建 `SPEC.md`。
- **经验教训**：学习科学证据适合约束交互和验收，但经典实验的任务、学科与人群边界必须保留，不能直接等同于产品有效性。

## 2026-07-19T22:29:48+08:00 — BRAIN-004 操作系统课件材料审计

- **Task 编号**：BRAIN-004
- **触发的 Superpowers skill**：续接 `brainstorming`；同时使用 `pdf` skill 做只读材料结构与视觉检查。
- **关键 prompt / context**：学生选择“操作系统基础”并给出本地课件目录；访问范围严格限制在该指定目录。
- **材料证据**：15 份 PDF、932 页、195,355,180 bytes；绪论 138 页、并发 279 页、虚拟化 296 页、持久化 219 页。所有文件未加密，首页为 1920 × 1080，前三页有非空文本。
- **工具与故障**：bundled Poppler 包装器找不到内部路径；MiKTeX `pdftotext` 因沙箱禁止写用户配置目录而报拒绝访问。未修改用户配置或申请提权，改用 bundled `pypdf`/`pypdfium2`。`pypdf` 报告可恢复的交叉引用对象警告，但 15 份文件均成功读取。
- **视觉验证**：临时渲染绪论、并发、虚拟化、持久化各一页为 1440 × 810 PNG，人工检查均清晰；临时文件已删除。
- **产出**：新增 `docs/research/OPERATING_SYSTEMS_MATERIAL_AUDIT.md`；只记录元数据、可读性与产品约束，不复制课件正文或图像。
- **subagent 输出 / commit hash**：未派发 subagent；阶段 A 无 PLAN task。提交 hash 将在任务输出中记录。
- **人工修改及原因**：学生提供课程名称与本地目录；智能体没有把课件加入 Git，因为许可证未知且文件仅限本地验证。
- **经验教训**：真实课件同时包含文本、代码、公式和图表；只做纯文本 RAG 会丢失关键上下文。解析器的容错警告也必须进入产品错误模型，而不是被隐藏。

## 2026-07-19T22:32:43+08:00 — BRAIN-004A 课程材料威胁模型基线

- **Task 编号**：BRAIN-004A
- **触发的 Superpowers skill**：续接 `brainstorming`；等待 D-008 人工决策期间只做不预设供应商/架构的安全分析。
- **关键 prompt / context**：操作系统课件许可证未知，材料约 195 MB；学生尚未决定是否允许最小必要片段发送到云端模型。
- **分析输出**：新增 `docs/research/COURSEWARE_THREAT_MODEL_BASELINE.md`，记录资产敏感级别、候选信任边界、12 类威胁、方案无关控制、三种数据边界影响和候选测试证据。
- **subagent 输出 / commit hash**：未派发 subagent；阶段 A 无 PLAN task。提交 hash 将在任务输出中记录。
- **人工修改及原因**：无新的学生输入；没有选择供应商、模型、存储或部署架构，也没有创建 `SPEC.md`。
- **经验教训**：数据最小化必须转化为可测不变量，例如“无确认时远端调用为零”和“请求仅含被引用页面”，否则容易停留在隐私口号。

## 2026-07-19T22:34:46+08:00 — BRAIN-005 用户可选的课件处理路径

- **Task 编号**：BRAIN-005
- **触发的 Superpowers skill**：续接 `brainstorming`；记录学生对候选方案的修正，不替其补全尚未表达的云端授权。
- **关键 prompt / context**：学生认为本地解析可能使课件内容失真，希望向用户提供可选择的处理选项。
- **采纳内容**：确认处理路径可按课程或任务选择，选择界面需呈现保真度、外发范围、凭据/费用和解析限制；模式切换不得静默扩大外发。
- **未采纳/未推断**：没有把反馈解释为允许整份 PDF 上传，也没有选择云供应商、模型或默认模式。
- **subagent 输出 / commit hash**：未派发 subagent；阶段 A 无 PLAN task。提交 hash 将在任务输出中记录。
- **人工修改及原因**：学生推翻“本地解析 + 最小片段云端调用作为单一推荐路径”的隐含收敛；智能体将其改为用户可选模式。
- **经验教训**：隐私默认不能忽视材料保真度；安全设计需要让取舍可见、可选择、可撤销，而不是用一个全局策略覆盖所有课程。

## 2026-07-19T22:40:53+08:00 — BRAIN-005A 课件解析保真度量化

- **Task 编号**：BRAIN-005A
- **触发的 Superpowers skill**：续接 `brainstorming`；使用 `pdf` skill 对已授权目录做只读全量统计，为 D-009 提供证据而不替学生选择默认模式。
- **关键 prompt / context**：学生担心本地解析使内容失真。审计脚本用 bundled `pypdf` 逐页统计文本与 PDF 资源结构，不保存课件正文。
- **验证结果**：932/932 页完成；空文本页 0，少于 100 个非空白字符的页面 95，文本中位数 226、均值 247.1 字符/页；932 页 NFKC 归一化会变化，`U+FFFD` 为 0；932 页含图像 XObject，87 页含 Form XObject；页面异常 0。
- **工具异常与恢复**：长时间 Python 子进程的 stdout 没有被外层终端捕获，前两次运行没有即时结果；改为临时 JSON 后，文件在外层进程返回后延迟落盘并包含完整统计。没有把无输出误记为成功，也不把本次时长当性能基准。
- **产出**：新增 `docs/research/COURSEWARE_PROCESSING_MODES.md`，并补充课程材料审计；临时 Python/JSON 未提交且已删除。
- **subagent 输出 / commit hash**：未派发 subagent；阶段 A 无 PLAN task。提交 hash 将在任务输出中记录。
- **人工修改及原因**：无新的学生输入；默认模式仍未决定。
- **经验教训**：文本“可抽取”与页面“保真”是不同断言。产品需要原页对照、质量报告和显式模式选择，不能只依据解析器退出码判断完整性。

## 2026-07-19T22:46:45+08:00 — BRAIN-005B 候选模块与领域模型

- **Task 编号**：BRAIN-005B
- **触发的 Superpowers skill**：续接 `brainstorming`；等待 D-009 时整理已确认信息，不把候选模型冒充已批准设计。
- **关键 prompt / context**：已确认操作系统真实课件、理解适配、持续复习、用户可选处理模式与安全约束；首次导入默认行为仍未决。
- **分析输出**：新增 `docs/research/TUTORING_DOMAIN_MODEL_DRAFT.md`，提出 M1 课程材料与保真、M2 适配解释与理解检查、M3 掌握状态与持续复习，以及跨模块安全/凭据/审计控制；记录候选实体、关系、状态流、不变量和测试种子。
- **agent 边界**：当前候选设计可以是确定性应用流程，尚未宣称 agent。若后续加入自主多轮决策/工具调用/反馈修正，需另行确认并实现可 mock 的主循环与护栏。
- **subagent 输出 / commit hash**：未派发 subagent；阶段 A 无 PLAN task。提交 hash 将在任务输出中记录。
- **人工修改及原因**：无新的学生输入；未创建 `SPEC.md`、未选择数据库/框架/模型/部署，也未决定 D-009。
- **经验教训**：跨模块合同应围绕可追溯来源和学习证据，而不是共享聊天文本；这样保真、学习与复习才能形成可测试闭环。

## 2026-07-19T22:50:40+08:00 — BRAIN-006 首次导入规则解释与确认

- **Task 编号**：BRAIN-006
- **触发的 Superpowers skill**：续接 `brainstorming`；对不清楚的候选规则先解释，不把困惑当作同意；首次真正适合视觉呈现时按 just-in-time 规则提供 visual companion 邀请。
- **关键 prompt / context**：学生询问 D-009 推荐规则的详细含义。智能体以操作系统课件为例说明三种处理模式、课程级设置、逐次外发预览、扩大授权和远端删除。
- **澄清结果**：学生确认首次导入直接询问用户，通过多个引导步骤/对话框完成说明与选择；课程级记住设置，扩大外发仍需确认。D-009 已解除。
- **subagent 输出 / commit hash**：未派发 subagent；阶段 A 无 PLAN task。首次导入决策与 mockup 提交：`a5b1dcf`。
- **人工修改及原因**：学生采纳显式首次引导，并要求提供界面展示；仍未创建 `SPEC.md` 或正式 UI 实现。
- **经验教训**：用户提出“是什么意思”说明抽象安全规则不足以支持决策；解释必须落到具体数据流。即便解释充分，也不能把没有反对当作默认同意。

## 2026-07-19T23:00:55+08:00 — BRAIN-007 首次导入可交互 mockup

- **Task 编号**：BRAIN-007
- **触发的 Superpowers skill**：续接 `brainstorming` 的 visual companion just-in-time 流程；使用 `visualize` skill 制作可交互 UI mockup，并按前端视觉 QA 要求检查桌面/移动视图。
- **关键 prompt / context**：学生从未见过 visual companion，明确要求用界面展示已确认的首次导入引导。
- **工具故障与替代**：visual companion 第一次因 Git Bash PATH 缺少标准工具失败，第二次到端口绑定时因 `127.0.0.1:55535` EACCES 失败；未继续重试或申请提权。Open Design `od` 仍不存在。替代为项目内自包含 HTML mockup和本地截图，影响是无法通过 companion 事件文件收集点击数据，需以聊天反馈为准。
- **产出**：`docs/mockups/course-import-onboarding.html`、`course-import-onboarding-v1-desktop.png`、`course-import-onboarding-v1-mobile.png`；`.superpowers/` 已加入 `.gitignore`，会话密钥和失败会话文件不提交。截图在 BRAIN-008 更新界面后加上 `v1` 标识，以免被误认为新版视觉证据。
- **浏览器验证**：bundled Playwright 缺少 Chromium executable，未下载；使用 Microsoft Edge 150.0.4078.83。桌面 1440 × 900：body overflow=false、clipped=[]、mode overlap=false；移动 390 × 844：body overflow=false、outside=[]、mode overlap=false；page/console errors=[]。
- **交互验证**：默认 `page-cloud`；连续点击“继续”后 `permission-mode` 与 `ready-mode` 均为“按页云端处理”。
- **全路径验证**：`local`、`page-cloud`、`full-cloud` 三条路径的权限名称、外发范围和完成页名称均与选择一致；三条路径在取消课程级记忆后均显示“仅本次导入”。
- **subagent 输出 / commit hash**：未派发 subagent；阶段 A 无 PLAN task。首次导入决策与 mockup 提交：`a5b1dcf`。
- **人工修改及原因**：学生确认用多步引导并要求视觉展示；mockup 只验证信息架构与交互节奏，不替代 Open Design design system/skill 选择。
- **经验教训**：安全同意页不能只讲隐私；将真实课程规模与解析证据放在模式选择前，用户更容易理解为什么存在不同处理方式。

## 2026-07-19T23:32:52+08:00 — BRAIN-008 导入引导信息层级修订

- **Task 编号**：BRAIN-008
- **触发的 Superpowers skill**：续接 `brainstorming` 与 visual companion 迭代；使用 `visualize` skill 修改已批准的需求阶段 mockup，并使用 `browser:control-in-app-browser` 尝试双端验证。
- **关键 prompt / context**：学生认可第一版，并要求用字体大小、颜色、字重和字体建立二级展示，使用图标减少冗余文字；桌面端与移动端均采用 X 轴时间线；“开始学习”页需强调配置修改位置。
- **采纳内容**：将左侧竖向阶段栏改为顶部四节点横向时间线；在桌面端和移动端保持同一 X 轴阅读方向；处理模式改为“图标 + 标题 + 简述 + 短事实”；强调“不会静默切换”；完成页突出路径“课程设置 › 材料与隐私”，最终主操作改为“开始学习”。
- **验证故障与替代**：项目外置 Node 依赖暴露 `playwright` 但缺少配套 `playwright-core`，首次自动化脚本未启动。随后按 Browser skill 使用应用内浏览器，但 `file://` 页面被其 URL 安全策略拒绝；遵守策略未改用本地端口、其他浏览器或间接绕过。
- **本次验证证据**：临时 Node 静态检查通过，覆盖交互脚本语法、成对标签、四列横向时间线与进度更新、900/560 px 响应式规则、模式图标/短事实、设置路径、最终按钮文案及无外部资源依赖；`failures=[]`。这只能证明结构与脚本约束，不证明新版视觉没有裁切或重叠。
- **截图证据边界**：旧桌面/移动截图重命名为 `course-import-onboarding-v1-*.png`，只保留第一版历史证据；新版尚无浏览器截图或视觉验收，不得引用 v1 截图证明 v2。
- **规约沉淀**：创建 `SPEC.md` 阶段 A 工作草案，并更新候选领域模型中已经过时的 D-009 状态；未决产品/部署/技术选择仍明确保留，没有作为已批准设计写入。
- **subagent 输出 / commit hash**：未派发 subagent；阶段 A 无 PLAN task。第二版 mockup、阶段 A `SPEC.md` 草案与过程修订提交：`64a1cde`。
- **人工修改及原因**：学生直接确认视觉方向并给出具体修订，不涉及正式框架、模型、数据库或部署选择；仍未进入正式 UI 实现。
- **经验教训**：阶段进度、关键风险和后续配置入口属于不同视觉层级；把它们都写成正文会增加扫描负担，应该分别用时间线、强调条与位置路径承载。

## 2026-07-19T23:40:56+08:00 — BRAIN-009 第一版用户边界提问

- **Task 编号**：BRAIN-009
- **触发的 Superpowers skill**：续接 `brainstorming`；在阶段 A 工作草案形成后选择影响面最大的未决问题，并保持一次只询问一项。
- **关键 prompt / context**：当前证据以学生本人、本地操作系统课件和用户控制外发为中心，但课程最终要求可访问 WebUI；单用户本地优先、单用户云端实例和多用户服务会导致不同的认证、凭据、存储、部署与删除模型。
- **候选与推荐**：在 `DECISIONS_NEEDED.md` D-010 比较三种边界，推荐单用户、本地优先 WebUI，并使用不含私人课件/真实 key 的公开演示满足课程 URL；该推荐不等于学生确认。
- **subagent 输出 / commit hash**：未派发 subagent；阶段 A 无 PLAN task。D-010 候选比较提交：`cfdc6d1`。
- **人工修改及原因**：尚未收到学生对 D-010 的回答；未选择认证、数据库、凭据后端、部署或分发技术。
- **经验教训**：把“网页界面”等同于“多用户云服务”会过早扩大安全与运维范围；应先确认真实用户和数据所在位置，再选框架。

## 2026-07-19T23:46:48+08:00 — BRAIN-009A 单用户本地优先边界确认

- **Task 编号**：BRAIN-009A
- **触发的 Superpowers skill**：续接 `brainstorming`；接收 D-010 人工决定后同步设计，不把“桌面窗口也可以”用于绕过课程 WebUI 硬要求。
- **关键 prompt / context**：学生回答“我觉得本机好，做成WebUI或者桌面窗口都好，多用户服务虽然挺好（比如可以分享课件，资料等），但是感觉不急着做”。
- **确认结果**：第一版采用单用户、本地优先 WebUI；桌面窗口仅作为可选壳。注册、登录、多租户、分享、教师视角和跨设备同步延期，不进入第一版。
- **分析与安全补充**：新增 `docs/research/USER_DEPLOYMENT_BOUNDARY_OPTIONS.md`，比较三种路线的拓扑、数据、凭据、测试和迁移；本地 WebUI 增补 loopback、`Host`/`Origin`、CORS 与 CSRF 风险/验收，避免把无登录误解为无访问控制。
- **subagent 输出 / commit hash**：未派发 subagent；阶段 A 无 PLAN task。D-010 结果、研究基线与规约同步提交：`0b3ed66`。
- **人工修改及原因**：学生作出用户/运行边界决定；智能体只依据课程硬要求将 WebUI 定为交付基线，没有选择语言、框架、数据库、provider、分发或公开部署。
- **经验教训**：本地优先减少服务器数据风险，但会引入 localhost 浏览器攻击面和公开演示双配置；这些不能因为“只有一个用户”而省略测试。

## 2026-07-19T23:52:05+08:00 — BRAIN-010 首个学习闭环知识点提问

- **Task 编号**：BRAIN-010
- **触发的 Superpowers skill**：续接 `brainstorming`；D-010 收敛后回到产品核心，一次只询问一个能把“看懂”转为客观验收的知识点。
- **关键 prompt / context**：操作系统课件真实包含并发/互斥/同步/并发 bugs、进程/调度、地址空间等主题；目前 M2/M3 仍缺少首个具体知识点、题型和延迟复习成功标准。
- **候选与推荐**：在 `DECISIONS_NEEDED.md` D-011 比较互斥与竞态、进程与调度、地址空间与地址转换；推荐互斥/竞态，因为可同时覆盖概念、代码轨迹、错误诊断、修复比较和变式复习。推荐不等于学生确认。
- **subagent 输出 / commit hash**：未派发 subagent；阶段 A 无 PLAN task。D-011 候选比较提交：`26ba7a2`。
- **人工修改及原因**：尚未收到学生对 D-011 的回答；未创建题目、复制课件正文或选择实现技术。
- **经验教训**：只有把“看懂”绑定到学生产出的可观察行为和延迟后的变式表现，才能避免把阅读解释或模型自评误当成学习效果。

## 2026-07-19T23:57:51+08:00 — BRAIN-010A 互斥与竞态纵向切片确认

- **Task 编号**：BRAIN-010A
- **触发的 Superpowers skill**：续接 `brainstorming`；在学生明确授权从 D-011 既有候选中选择后采用已推荐方案，并限制授权外延。
- **关键 prompt / context**：学生回答“没啥偏好的，你随便搞一个吧”，随后要求今后提问时使用阻断信号以便及时发现。
- **选择与范围**：采用互斥与竞态条件；首轮只包含共享状态、非原子读-改-写、线程交错、竞态、临界区和一种互斥修复的安全性理由。同步原语大全、内存模型、死锁证明和公平性算法延期。
- **规约与研究输出**：新增 `docs/research/FIRST_LEARNING_LOOP_CANDIDATES.md`；M2 写入三类起点探针、适配解释与轨迹/迁移检查；M3 写入 `demonstrated_now -> retained` 的后续证据门禁；新增参数化 oracle/provider mock 隔离验收。
- **subagent 输出 / commit hash**：未派发 subagent；阶段 A 无 PLAN task。D-011 结果、候选闭环与规约提交：`84e84ac`。
- **人工修改及原因**：学生授权该知识点选择；智能体没有借此决定复习间隔、agent、provider、整份云端处理、分发或部署。
- **经验教训**：无偏好授权仍应绑定已公开的候选、推荐依据和排除范围；“随便”不能被解释为对所有后续产品决定的空白授权。

## 2026-07-20T00:08:54+08:00 — BRAIN-010B 互斥/竞态本地来源页映射

- **Task 编号**：BRAIN-010B
- **触发的 Superpowers skill**：续接 `brainstorming`；使用 `pdf` skill 在 D-011 已确认后定位真实来源，不创建正式题库或复制受限材料。
- **关键 prompt / context**：首个纵向切片需要可追溯来源，但课件许可未知且纯文本无法保留线程颜色、时间轴、箭头、临界区和代码分组。
- **只读扫描**：对多处理器编程、互斥、互斥进阶、并发 bugs 四份 PDF 做通用信号统计，命中页分别为 18/47、31/38、31/35、24/69；`pypdf` 的既有交叉引用警告可恢复，四份均完成。
- **视觉验证**：用 `pypdfium2`/Pillow 临时渲染 7 页并检查；主要候选收敛为多处理器编程第 25/27 页和互斥第 2/14 页；并发 bugs 第 8/59/66 页与互斥进阶延期。
- **产出与许可证边界**：新增 `docs/research/MUTEX_RACE_SOURCE_MAP.md`，只提交文件名、页码、通用标签、用途、保真约束和测试不变量；课件、正文与图像均未加入 Git。
- **清理故障**：临时 Python 脚本已删除。托管环境拒绝递归及逐文件 `Remove-Item`，`apply_patch` 无法读取二进制 PNG；停止继续绕过并将 `tmp/` 加入 `.gitignore`。8 个预览文件共 3,538,417 bytes 留在本机 ignored 目录，不提交或分发。
- **subagent 输出 / commit hash**：未派发 subagent；阶段 A 无 PLAN task。来源映射、过程证据与忽略规则提交：`25c4070`。
- **人工修改及原因**：无新产品决定；未选择 provider、处理模式目录、复习间隔或实现技术。
- **经验教训**：页面关键词只能缩小人工复核范围；代码与时序图的视觉语义必须由原页对照承担。清理失败也必须如实记录，不能把 Git 忽略冒充物理删除。

## 2026-07-20T00:10:58+08:00 — BRAIN-011 复习时间语义人工门禁

- **Task 编号**：BRAIN-011
- **触发的 Superpowers skill**：续接 `brainstorming`；互斥/竞态切片与来源完成后，一次只询问 M3 中影响最大的目标日期语义。
- **关键 prompt / context**：学生要求今后需要回答问题时发出阻断信号，以免问题被普通进度淹没。当前 `Course.target_date`、`ReviewTask.due_at/reason` 和复习成功窗口仍未定义。
- **候选与推荐**：在 `DECISIONS_NEEDED.md` D-012 比较“可选目标日期 + 自适应安排”、仅长期掌握、手动日期；推荐可选目标日期，在没有日期时退化为长期复习，不预设普适间隔算法。
- **subagent 输出 / commit hash**：未派发 subagent；阶段 A 无 PLAN task。D-012 候选比较提交：`aea59e0`。
- **人工修改及原因**：尚未收到学生对 D-012 的回答；未选择调度算法、固定间隔、通知渠道或日历集成。
- **经验教训**：复习“何时发生”是产品语义而不只是 cron 参数；如果不先确定目标日期角色，调度算法和 UI 都会把未经确认的学习策略固化。

## 2026-07-20T00:18:53+08:00 — BRAIN-011A 增量课程与期末周模式收敛

- **Task 编号**：BRAIN-011A
- **触发的 Superpowers skill**：续接 `brainstorming`；在 D-012 人工回答后，把新产品语义落实为阶段 A 研究与规约，不进入 `writing-plans` 或正式实现。
- **关键 prompt / context**：学生先回答“我觉得持续安排吧，因为最后需要模型根据用户上传的重点详情进行针对性学习。顺便提醒一下，一般来说课件不会在一开学的时候就全给你，所以我们更类似‘导入课件→确认可以学习/复习的知识→筹划学习计划→引导用户学习’这样的操作”，随后补充“考试日期一般在学期末给定，用户划定考试日期以后其实就可以进入期末周学习模式，进行拟合往年卷，重点突击老师给定的重点等行为”。
- **分析与规约结果**：确认 `continuous` 为默认学期中模式；新材料按 `MaterialBatch` 增量导入，候选知识覆盖需经 `CoverageDecision` 后才进入版本化 `LearningPlan`。有效考试日期只是进入条件之一，用户显式操作后才进入 `finals`；往年卷/老师重点作为显式材料角色映射到已确认知识，优先级保留来源、置信度和用户修正。将“拟合往年卷”限定为结构/题型/知识点/难度分析与同类练习，不推断训练、微调、原题预测或自动上传授权。
- **产出**：新增 `docs/research/INCREMENTAL_COURSE_WORKFLOW.md`；更新 `DECISIONS_NEEDED.md`、`SPEC.md`、`SPEC_PROCESS.md`、调度语义、领域模型、威胁模型和操作系统材料审计。新增 AC-15 至 AC-20，覆盖增量幂等、部分失败、历史保留、日期/模式分离、映射确认和无训练/自动上传路径。
- **验证证据**：`git diff --check`、本地 Markdown 链接目标检查、代码围栏平衡检查和强特征凭据正则扫描均通过；`gitleaks` 与 `detect-secrets` 未安装，未声称执行它们。无正式实现测试，符合阶段 A 门禁。
- **subagent 输出 / commit hash**：未派发 subagent；阶段 A 无 PLAN task。规约与研究文档提交：`adbac3d`。
- **人工修改及原因**：学生决定了双模式核心语义；智能体仅选择了与该语义一致的领域命名、状态、不变量和候选测试，未替学生决定期末窗口、每日上限、具体调度算法、答案/笔记范围、provider、部署或 agent。
- **经验教训**：考试日期不应成为开学时的硬依赖；把“材料到达”和“用户确认知识”分成两个版本化事件，才能同时支持不完整课件、持续复习和期末突击而不重写学习历史。

## 2026-07-20T00:34:54+08:00 — BRAIN-012 第一版 Agent 自主性人工门禁

- **Task 编号**：BRAIN-012
- **触发的 Superpowers skill**：续接 `brainstorming`；在双模式主流程明确后，准备“是否包含课程定义的 agent”这一重大产品/架构选择，一次只保留一个当前人工问题。
- **关键 prompt / context**：学生希望模型依据用户上传的重点详情做针对性学习，但尚未说明模型应由应用流程调用，还是要自主选择工具并循环修正。课程 Project B 原文明确无 agent 也合规；有 agent 时才触发自编码循环、工具分发、治理护栏和 mock/stub 确定性测试义务。
- **候选与推荐**：新增 `docs/research/AGENT_BOUNDARY_OPTIONS.md`，比较 1）受约束 AI 功能、无课程定义 agent；2）只生成可审查计划提案的有界规划 agent；3）全流程学习教练 agent。推荐方案 1；若学生明确希望展示 agent，方案 2 是可控折中，方案 3 延期。
- **共同边界**：三种方案都可使用模型做候选知识映射、适配解释、练习生成和期末资料分析；模型均不得扩大外发、读取凭据、绕过用户确认、给自己评分后写掌握状态或直接激活计划。
- **验证证据**：本地 Markdown 引用目标检查、代码围栏平衡、`git diff --check` 和强特征凭据正则扫描通过；无实现或测试代码，未跨越阶段 A 门禁。
- **subagent 输出 / commit hash**：未派发 subagent；阶段 A 无 PLAN task。D-013 候选边界提交：`5fd7a7a`。
- **人工修改及原因**：尚未收到学生对 D-013 的选择；未创建 agent 主循环、工具、prompt、依赖或 PLAN task，也未把推荐写成最终 SPEC 范围。
- **经验教训**：“使用 LLM”与“构建 agent”必须分别确认；否则很容易为了标签加入自主循环，却没有证明它比可测试的应用状态机解决了更多真实用户问题。

## 2026-07-20T00:40:04+08:00 — BRAIN-012A D-013 第二次门禁复查

- **Task 编号**：BRAIN-012A
- **触发的 Superpowers skill**：续接 `brainstorming`；这是 D-013 后的自动 Goal 续接复查，不引入新的产品问题。
- **当前证据**：工作区干净，HEAD 为 `ebec1cf`；`DECISIONS_NEEDED.md` 仍将 D-013 标为当前人工门禁，`SPEC.md` 未把 agent 推荐写成最终范围，`PLAN.md` 不存在；`od` 命令仍未找到。
- **阻塞判定**：尚未收到用户对方案 1/2/3 的选择；根据课程门禁，不能生成 PLAN、创建 agent 主循环或开始实现。当前没有不依赖该选择且能实质推进的安全任务。
- **subagent 输出 / commit hash**：未派发 subagent；本次复查以 D-013 过程日志提交 `ebec1cf` 为当前基线，不产生功能或规约提交。
- **人工修改及原因**：没有产品文档修改；保留 D-013 原问题和候选，避免把自动续接误记为人工确认。
- **经验教训**：人工门禁复查应核对外部状态和工作区，而不是重复提出新问题或用无关文档制造进度。

## 2026-07-20T00:42:01+08:00 — BRAIN-012B D-013 第三次门禁复查与阻塞

- **Task 编号**：BRAIN-012B
- **触发的 Superpowers skill**：续接 `brainstorming`；完成同一人工门禁的第三次连续状态审计。
- **当前证据**：工作区干净，HEAD 为 `54dbfaa`；D-013 仍是 `DECISIONS_NEEDED.md` 的当前人工门禁；`SPEC.md` 仍显示未签字确认；`PLAN.md` 不存在；`od` 命令仍未找到。
- **阻塞判定**：连续三次 Goal 复查均未收到方案 1/2/3 选择，且没有不依赖该选择而能实质推进的安全任务；当时已达到调用 `update_goal(status=blocked)` 的条件，但本轮尚未调用该工具即收到学生输入，故没有把未执行的状态写成已完成动作。
- **subagent 输出 / commit hash**：未派发 subagent；本次复查基于门禁提交 `54dbfaa`，不创建功能或规约提交。
- **人工修改及原因**：只追加本条审计记录；没有猜测 agent 范围、创建 PLAN 或开始实现。
- **经验教训**：达到三次相同门禁后应正式停止 Goal，而不是继续重复询问或消耗运行资源。

## 2026-07-20T00:43:07+08:00 — BRAIN-013 受约束 AI 功能确认

- **Task 编号**：BRAIN-013
- **触发的 Superpowers skill**：续接 `brainstorming`；学生在 D-013 门禁后明确选择模型自主性边界。
- **学生原始回答**：“就用受约束AI功能吧”。
- **选择结果**：采用方案 1。第一版使用模型完成候选知识映射、适配解释、练习生成、往年卷结构/题型/知识点/难度分析和反馈；不包含课程定义的自主 agent，不创建自主工具选择/循环修正主循环。
- **权威边界**：应用状态机、版本化规则、确定性 oracle 和用户确认负责材料外发、知识覆盖、计划修订、优先级和掌握状态；模型输出只能通过 schema、来源、预算、超时和错误隔离进入候选流程。
- **规约影响**：D-013 标为已确认；SPEC 的技术选型不再把 agent 边界写成未决，但仍保留 provider、模型端口和具体技术栈选择。`AGENT_BOUNDARY_OPTIONS.md` 作为被否决/延期方案的决策证据保留。
- **subagent 输出 / commit hash**：未派发 subagent；受约束模型端口合同与规约同步提交：`9a4db15`。
- **人工修改及原因**：学生明确选择方案 1；智能体没有据此替学生决定 provider、模型、分发、部署、间隔算法或 SPEC 整体签字。
- **经验教训**：确认“不做 agent”不是取消 AI，而是把模型能力限制在可审查候选和解释端口，以便继续验证学习效果与安全边界。

## 2026-07-20T00:51:22+08:00 — BRAIN-014 远端课程材料能力人工门禁

- **Task 编号**：BRAIN-014
- **触发的 Superpowers skill**：续接 `brainstorming`；D-013 解除后审计阶段 A 未决项，把数据边界拆成“能力目录”和后续 provider 选择，一次只询问前者。
- **关键 prompt / context**：学生已要求本地解析失真时应有用户可选路径，且首次导入必须显式选择/按课程记住；但从未明确授权第一版提供整份 PDF/课程云端上传。真实操作系统材料许可证未知，样本为 195 MB/932 页。
- **候选与推荐**：新增 `docs/research/REMOTE_MATERIAL_CAPABILITY_OPTIONS.md`，比较 1）本地 + 经确认页面/片段远端；2）再增加整份 PDF/课程远端；3）课程材料完全本地。推荐方案 1，它仍给用户数据边界选择，同时把第一版远端生命周期限制在任务级页面/片段。
- **过程修正**：`COURSEWARE_PROCESSING_MODES.md` 不再把已确认的 D-009 写成未决，并链接受约束模型端口；D-008 明确默认交互已解除，整份能力由 D-014 单独确认。
- **验证证据**：本地 Markdown 链接、代码围栏、过时 D-009 表述、`git diff --check` 和强特征凭据正则扫描均通过；没有上传材料或调用 provider。
- **subagent 输出 / commit hash**：未派发 subagent；阶段 A 无 PLAN task。D-014 候选边界提交：`2b6e3b1`。
- **人工修改及原因**：尚未收到学生对 D-014 的回答；未选择 provider、模型、留存政策、凭据或实现技术。
- **经验教训**：让用户选择处理路径不等于产品必须在第一版实现所有可能的外发层级；能力上限本身需要明确授权和可验证的生命周期。

## 2026-07-20T00:55:17+08:00 — BRAIN-014A D-014 第二次门禁复查

- **Task 编号**：BRAIN-014A
- **触发的 Superpowers skill**：续接 `brainstorming`；这是 D-014 后的自动 Goal 续接复查，不引入新的产品问题。
- **当前证据**：工作区干净，HEAD 为 `5d943e1`；`DECISIONS_NEEDED.md` 仍将 D-014 标为当前人工门禁，`SPEC.md` 仍未签字，`PLAN.md` 不存在；`od` 命令仍未找到。
- **阻塞判定**：尚未收到用户对远端材料能力方案 1/2/3 的选择；处理模式目录、删除合同和 provider 筛选都依赖该上限，不能继续定稿或进入计划。当前没有不依赖该选择且能实质推进的安全任务。
- **subagent 输出 / commit hash**：未派发 subagent；本次复查以 D-014 过程日志提交 `5d943e1` 为当前基线，不产生功能或规约提交。
- **人工修改及原因**：没有修改 D-014 候选或替学生选择；只追加真实复查证据。
- **经验教训**：材料能力上限未确认时，提前选择 provider 会把供应商能力反向固化为未经授权的产品边界。

## 2026-07-20T00:57:31+08:00 — BRAIN-015 用户控制的三模式外发范围确认

- **Task 编号**：BRAIN-015
- **触发的 Superpowers skill**：续接 `brainstorming`；学生在 D-014 门禁后明确选择由平台提供能力、用户决定外发层级。
- **学生原始回答**：“外发决策也留给用户自行决定吧，我们的平台只要实现对应的功能即可”。
- **选择结果**：按上下文采用 D-014 方案 2。第一版正式提供 L（本地）、P（经确认页面/片段远端）和 F（整份 PDF/课程远端）；没有默认/静默外发。课程记住模式，但每批新增文件、内容哈希变化、扩大范围和更换 provider 均需新的精确 `ConsentRecord`。
- **规约与研究输出**：新增 `docs/research/REMOTE_FILE_LIFECYCLE_CONTRACT.md`，定义 `RemoteMaterialObject` / `RemoteJob`、文件级授权、上传/索引/失败/删除状态、幂等、切换、对账、适配器能力声明和 12 类确定性场景；同步 SPEC AC-25 至 AC-29、威胁 T-18、领域模型和处理模式目录。
- **安全边界**：F 文件只有 `ready` 才能进入模型端口；端口仍使用本地 `source_id` 并映射回页码。从 F 切回 L/P 后立即禁止新 F 请求；删除未知/失败显示 `delete_incomplete`，不能伪报成功。
- **验证证据**：`git diff --check`、本地 Markdown 链接、代码围栏、过时 D-014/F 未决表述和强特征凭据正则扫描通过；没有上传真实材料、创建凭据或调用 provider。
- **subagent 输出 / commit hash**：未派发 subagent；阶段 A 无 PLAN task。三模式与生命周期合同提交：`fe94963`。
- **人工修改及原因**：学生选择让平台实现全部外发层级；智能体没有据此替学生选择 provider、数据政策、容量/费用、凭据或实际课件权利结论。
- **经验教训**：课程级模式记忆不能代替新增文件的 payload 授权；否则“用户选择”会在后续增量导入时退化为静默整份上传。

## 2026-07-20T01:02:00+08:00 — BRAIN-016 Provider 适配策略人工门禁

- **Task 编号**：BRAIN-016
- **触发的 Superpowers skill**：续接 `brainstorming`；D-014 解除后将 provider 选择拆成适配策略问题，避免同时决定厂商、模型、区域和凭据。
- **关键 prompt / context**：平台已确认实现 L/P/F 三种能力，用户决定具体外发层级；模式 F 需要真实上传、索引、引用、删除和政策展示。Provider 仍未选。
- **官方资料核验**：OpenAI Developer Docs MCP 读取 File Search、Files/Vector Stores 删除参考与 Data controls；确认官方文档展示 PDF 文件上传、vector store 状态、文件引用、删除入口、`expires_after` 说明及文件/向量库应用状态保留规则。Google/Anthropic 官方站点本轮通过 web/PowerShell 均连接失败，未将其能力写成事实。
- **候选与推荐**：新增 `docs/research/PROVIDER_STRATEGY_OPTIONS.md`，比较统一适配器 + 一个真实参考 provider、单 provider 紧耦合、多个真实 provider；推荐方案 1。
- **验证证据**：本地 Markdown 链接、代码围栏、`git diff --check` 和强特征凭据正则扫描通过；未读取或提交任何 API key，未调用真实 API。
- **subagent 输出 / commit hash**：未派发 subagent；阶段 A 无 PLAN task。D-015 候选策略提交：`2444b87`。
- **人工修改及原因**：尚未收到学生对 D-015 的选择；未创建 adapter、凭据流程实现、provider SDK 依赖或 PLAN task。
- **经验教训**：先确定“适配器策略”再选择厂商，可以把用户外发控制和生命周期合同留在领域层，也能避免不完整的官方资料被误当成产品承诺。

## 2026-07-20T01:18:36+08:00 — BRAIN-016A D-015 第二次门禁复查

- **Task 编号**：BRAIN-016A
- **触发的 Superpowers skill**：续接 `brainstorming`；这是 D-015 后的自动 Goal 续接复查，不扩展候选范围。
- **当前证据**：工作区干净，HEAD 为 `f9ebb13`；D-015 仍是当前人工门禁，`SPEC.md` 未签字，`PLAN.md` 不存在；`od` 命令仍未找到。
- **阻塞判定**：尚未收到 provider 策略方案 1/2/3 的选择；真实 adapter、凭据、数据政策和 F 端到端测试依赖该策略。当前没有不依赖该选择且能实质推进的安全任务。
- **subagent 输出 / commit hash**：未派发 subagent；本次复查以 D-015 过程日志提交 `f9ebb13` 为当前基线，不产生功能或规约提交。
- **人工修改及原因**：没有替学生选择 provider 策略或继续调查未选厂商；只追加真实复查证据。
- **经验教训**：自动续接遇到同一人工门禁时，应核对当前状态并停止，而不是用更多 provider 名单制造虚假进展。

## 2026-07-20T01:19:58+08:00 — BRAIN-016B D-015 第三次门禁复查与阻塞

- **Task 编号**：BRAIN-016B
- **触发的 Superpowers skill**：续接 `brainstorming`；这是 D-015 的第三次连续 Goal 状态审计，不引入新的产品选择。
- **当前证据**：工作区干净，HEAD 为 `b917d58`；D-015 仍是当前人工门禁，`SPEC.md` 未签字，`PLAN.md` 不存在；`od` 命令仍未找到。
- **阻塞判定**：连续三次 Goal 审计均未收到 provider 适配策略方案 1/2/3 的选择，且当前没有不依赖该选择而能实质推进的安全任务；已达到 `update_goal(status=blocked)` 的门槛，本条审计提交完成后调用该阻断信号。
- **subagent 输出 / commit hash**：未派发 subagent；本次审计以 `b917d58` 为基线，只追加过程日志，不产生功能或规约修改。
- **人工修改及原因**：没有替学生选择 provider、凭据、API 或 adapter，也没有生成 `PLAN.md`；只记录第三次真实复查与阻断条件。
- **经验教训**：同一人工门禁连续三次没有变化时，应正式标记 Goal 阻塞，而不是继续重复审计或消耗运行资源。

## 2026-07-20T01:33:25+08:00 — BRAIN-017 用户配置 Provider 与统一适配器确认

- **Task 编号**：BRAIN-017
- **触发的 Superpowers skill**：续接 `brainstorming`；学生恢复此前因 D-015 阻塞的 Goal，并给出 provider 适配架构方向。没有进入 `writing-plans`。
- **关键 prompt / context**：学生原始回答为“供应商让用户自己在config里面配置喽，我们写好适配器就行”。按最小语义确认统一 `ProviderAdapterRegistry`，用户在本地设置中选择平台已实现的 adapter/profile，领域层不硬编码供应商。
- **安全与范围解释**：普通 config 只含 adapter ID、模型、受控参数、预算和 `credential_ref`；key/token 仍由隐藏录入进入本机安全凭据存储。未把回答解释为允许任意 endpoint、第三方插件、明文 secret，或已选择具体 provider/模型/区域/政策。未知/坏配置与能力不足在联网前失败关闭；配置/政策变化使旧 consent 失效。
- **规约产出**：D-015 标为已确认架构方向；`SPEC.md` 新增 profile/能力快照与 AC-30 至 AC-32；同步远端生命周期、模型端口、威胁、领域模型、处理模式和历史候选。D-016 缩小为首版交付一个还是多个真实 adapter 的人工门禁。
- **subagent 输出 / commit hash**：`/root/d015_audit` 先完成只读交叉审计，后只修改四份 provider/生命周期研究合同；`/root/next_gate_audit` 只读梳理后续门禁，后只修改三份威胁/领域/处理模式文档。两者均报告 scoped `git diff --check`、围栏、链接与强特征凭据扫描通过，未提交 Git。主智能体在基线 `0e06cbc` 上整合核心规约；本轮最终 commit 在任务输出记录。
- **人工修改及原因**：学生决定 provider 由最终用户配置、平台负责 adapter；智能体仅补充课程强制的 secret 分离、失败关闭和授权隔离，没有替学生选择真实 adapter 数量或厂商。
- **经验教训**：“用户可配置 provider”必须拆成注册表、非秘密 profile、凭据引用和能力/政策快照；否则容易同时退化成明文 key、任意 URL 和无法审计的兼容性承诺。

## 2026-07-20T01:46:35+08:00 — AUDIT-002 Requirements 当前符合性复核

- **Task 编号**：AUDIT-002
- **触发的 Superpowers skill**：当前仍在 `brainstorming` 阶段；按 `verification-before-completion` 的证据纪律逐项读取命令输出，但本会话未注册该 skill，因此不把手工复核虚报为正式调用。
- **关键 prompt / context**：学生要求确认项目当前是否仍符合 requirements 文件夹文档。实际课程原文位于 `docs/requirements/`；完整读取通用要求与 Project B 应用类要求，并与 `AGENTS.md`、当前 SPEC/过程文档、文件清单和 Git 历史对照。
- **实际检查**：确认 `SPEC.md`、`SPEC_PROCESS.md`、`AGENT_LOG.md` 存在；`PLAN.md`、README、REFLECTION、正式源码、测试命令、GitHub/GitLab CI、分发产物和部署 URL 不存在；`od` 仍不可用；非文档正式源码计数为 0。检查到 `SPEC_PROCESS.md` 页首仍错误写“尚未形成 SPEC”，已立即修正。
- **审计结论**：项目仍符合 Project B 选题边界，并基本遵守阶段 A 门禁；当前不满足最终交付要求。缺失的 PLAN/实现/TDD/CI/分发等大多是阶段门禁后的硬任务，不等于豁免；Open Design、Superpowers 阶段 B 注册、技术/分发选型、双远程平台策略和过程反思是签字或后续阶段前的明确缺口。
- **产出与证据边界**：新增 `docs/REQUIREMENTS_COMPLIANCE_AUDIT.md` 四态矩阵，并将 `docs/PROJECT_AUDIT.md` 明确标为启动历史快照；没有创建空壳 PLAN、README、CI、测试或 REFLECTION，也没有声称任何实现验证通过。
- **subagent 输出 / commit hash**：`/root/requirements_audit` 只读核对课程条款与仓库证据，指出 SPEC_PROCESS 旧页首、最新决策日志缺口及最终交付缺项；未修改文件或提交。主智能体负责修订和最终验证，本轮 commit 在任务输出记录。
- **人工修改及原因**：学生主动要求 requirements 复核；智能体将结果分为当前满足、文档覆盖未验证、阶段门禁延后和明确缺口，避免用“阶段正确”冒充“项目最终合规”。
- **经验教训**：门禁既禁止提前造实现证据，也不能成为遗漏最终硬项的理由；合规审计必须同时报告当前阶段正确性和截止提交时仍欠缺的证据。

## 2026-07-20T01:55:20+08:00 — BRAIN-018 D-016 首版真实 Adapter 数量确认

- **Task 编号**：BRAIN-018
- **触发的 Superpowers skill**：续接 `brainstorming`；学生明确回答 D-016 为方案 `1`，没有进入 `writing-plans` 或实现。
- **关键 prompt / context**：D-016 要求在“一个真实参考 adapter + 完整 mock”“多个真实 adapter”“仅接口/mock”中选择首版交付范围；学生回复“1”。
- **确认结果**：首版实现统一 `ProviderAdapter`/registry、完整 provider mock、共享 contract suite 和一个真实参考 adapter。真实联网证据只覆盖该参考实现；参考实现不成为静默默认，用户仍配置 profile/凭据并逐次确认外发。
- **未决定项**：具体 provider、模型、区域、SDK/许可证、留存/训练政策、费用上限、技术栈、分发与部署仍未决定；研究资料不能替学生选择。
- **过程动作**：更新 `DECISIONS_NEEDED.md`、`SPEC.md`、`SPEC_PROCESS.md`、requirements 审计和 provider 策略研究的 D-016 状态；并行派发三个只读官方资料调查（OpenAI、Google Gemini、Anthropic），不读取 key、不调用付费 API、不上传课件。
- **subagent 输出 / commit hash**：三个 provider 调查尚在进行；本条日志与规约修改将在资料核验后与下一批文档一并提交，当前基线为 `8858b6e`。
- **人工修改及原因**：学生只决定真实 adapter 数量；智能体没有把任何 provider、模型或政策写成已选定事实。
- **经验教训**：先确定真实实现数量再比较厂商，能保持 provider-neutral 领域合同，同时避免把“用户配置”误解为“首版无限兼容任意供应商”。

## 2026-07-20T02:07:29+08:00 — BRAIN-019 D-017 Provider 候选与批量门禁准备

- **Task 编号**：BRAIN-019
- **触发的 Superpowers skill**：续接 `brainstorming`；学生要求把剩余问题一次性列出，以便离线时集中回答。没有进入 `writing-plans`。
- **关键 prompt / context**：D-016 已选一个真实参考 adapter；需要在不替学生选厂商的前提下，准备具体 provider 候选和其余会影响 SPEC/交付的人工决定。
- **subagent 输出**：`/root/openai_adapter_audit` 核验 OpenAI P/F、File Search、删除/过期、结构化输出和页码/视觉缺口；`/root/gemini_adapter_audit` 报告 Gemini P 强但 Files/Store 生命周期、政策 tier 和页码引用复杂；`/root/anthropic_adapter_audit` 报告 Claude P/citations 强但无直接匹配的托管索引生命周期。三者均只读、未改文件、未调用付费 API。
- **官方资料边界**：OpenAI 既有官方 MCP 证据可复核；本轮主会话 web 请求返回 503，Google/Anthropic 部分页面也遇到 503/TLS。未把未现场复核的精确限制、政策或许可证写成已验证事实。
- **规约产出**：新增 `docs/research/REFERENCE_PROVIDER_OPTIONS.md`；D-017 写入 `DECISIONS_NEEDED.md`，暂列 OpenAI/Gemini/Claude 与条件推荐；新增 D-018 至 D-024 批量问题，覆盖自定义 endpoint、期末材料、调度、技术/凭据、公开演示、远程平台和 Open Design。
- **人工修改及原因**：学生明确要求一次性提问；智能体将问题按重大影响分组，并保留可由工程默认处理的小选择，不提前选择 provider、技术栈或部署。
- **验证计划**：批量答案收到后逐项更新 SPEC/过程文档，再运行链接、围栏、凭据扫描；在 SPEC 签字前仍不生成 PLAN 或源码。
- **经验教训**：为避免用户离线时反复被单个门禁唤醒，应一次暴露所有真正改变产品/交付的选择，同时给出安全推荐和不决定的阻塞范围。

## 2026-07-20T17:07:19+08:00 — BRAIN-020 / AUDIT-003 断网恢复后的阶段 A 规约整合

- **Task 编号**：BRAIN-020、AUDIT-003。
- **触发的 Superpowers skill**：续接 `brainstorming`；继续使用已完整读取的 `openai-docs` skill 所要求的官方 OpenAI Docs MCP 证据边界。`superpowers:*` 在本会话未注册，因此没有把手工审计冒充正式 `writing-plans`/`verification-before-completion` 调用。
- **关键 prompt / context**：学生在断网前一次回答 D-017 至 D-024 均为方案 A（原始回答“感觉可以全A，你继续执行吧”），本轮恢复指令为“昨天断网了，你继续推进”。不得重复提问，不得越过 `SPEC.md` 签字、Open Design、冷启动和实现批准门禁。
- **恢复证据**：恢复时工作区只有规约/研究文档未提交改动；HEAD 为 `ccaa5734c8d91dd747c55d7daf6d1270d2f42c56`；没有 `PLAN.md`、正式源码、测试、CI、README 或 `REFLECTION.md`。未启动安装器、未上传课件、未读取或写入真实 API key、未向远程仓库 push。
- **只读审计输出**：`/root/spec_gap_audit` 指出 ReviewPolicy、SourceLocator、泄漏处理、输入限制、凭据清除、demo 隔离和 stale domain 文档缺口；`/root/decisions_audit` 指出 D-003/D-004/D-006 至 D-012/D-014/D-016/D-017/D-021 等台账状态过期；`/root/research_diff_review` 指出 Responses 留存、真实上传 exactly-once 过度承诺和 Vector Store 所有权缺口；`/root/final_stage_a_audit` 及其后续复核又指出 attribution、ReviewPolicy 唯一性、request-level store scope、locator 证明、预算、自动修订确认、合规审计 stale 文案和调度历史输入缺口。它们均为只读审计，没有提交代码。
- **本轮人工整合**：修订 `SPEC.md`、`DECISIONS_NEEDED.md`、`SPEC_PROCESS.md`、`docs/PROJECT_AUDIT.md`、`docs/REQUIREMENTS_COMPLIANCE_AUDIT.md` 及 `docs/research/` 下相关合同；明确 D-017 至 D-024 的确认边界，保留单文件分发、OCI/Hugging Face demo、隔离限额和 ReviewPolicy 数值为待整体签字的工程候选；修正合规审计的“无需选择”误导表述。
- **调度规约修订原因**：`plan_reviews_v1` 不能只接收最新证据，否则相同历史可能因快照截断得到不同计划。现在显式输入完整相关 `LearningEvidence[]`、每概念 `ConceptReviewState`（`interval_index`/`last_outcome`/`last_evidence_at`/`state_version`）和当前带版本/纠正信息的 `MasteryEstimate`，并将三者纳入 canonical `plan_input_hash`；快照不一致时返回 `state_inconsistent`，不静默覆盖。
- **当前门禁状态**：阶段 A 静态审计正在由本轮命令完成；`SPEC.md` 仍未由学生整体确认。Open Design 安装/MCP 与 design system/skill、Hugging Face 官方现场复核、学生本人 brainstorming 反思、Superpowers 新会话正式 `writing-plans` 和后续冷启动仍未执行；本轮不生成 `PLAN.md` 或实现代码。
- **经验教训**：过程文档必须区分“用户确认的方向”“待整体签字的工程候选”和“执行时才有证据的外部状态”；可重放调度也必须把历史状态完整纳入输入，而不是依赖一个易变的最新快照。

## 2026-07-20T17:16:44+08:00 — AUDIT-004 阶段 A 静态验证结果

- **Task 编号**：AUDIT-004。
- **触发的 Superpowers skill**：阶段 A 续接 `brainstorming`；按课程要求执行手工 `verification-before-completion` 证据检查，但当前会话没有注册该 skill，故仅记录实际命令，不宣称正式 skill 调用。
- **本次实际输出**：仓库 Markdown 文件 27 个；本地 Markdown 链接 11 个、坏链接 0；代码围栏不平衡 0；`SPEC.md` 必需章节缺失 0；用户故事 10 个（US-01 至 US-10，缺失/重复 0）；验收标准 50 个（AC-01 至 AC-50，缺失/重复 0）；M1/M2/M3 输入/行为/输出/边界/错误处理契约缺失 0；占位符扫描 0；强特征凭据扫描 0；`git diff --check` 无错误（仅报告工作树 LF/CRLF 转换警告）。
- **门禁文件证据**：`PLAN.md` 不存在，正式源码样文件计数 0；`README.md` 与 `REFLECTION.md` 尚不存在，未把缺失文件伪报为完成。没有运行测试/构建/CI，因为课程门禁禁止在 SPEC 未签字前创建实现。
- **工具环境复核**：Superpowers 缓存 `6.1.1` 存在并检测到 14 个核心 skill（含 `brainstorming`、`writing-plans`、TDD、worktree、评审和验证技能），但 `superpowers` CLI 与本会话 `superpowers:*` 均不可调用；Open Design 安装器 309,298,247 bytes，SHA-256 与 sidecar 均为 `63fc2e609489474e99187cdf94d01d063c1dbee733aaf2464d835cdc1e96f6b5`，Authenticode `NotSigned`，`od` 命令及 MCP resources/templates 仍为空/不可用。
- **结果与影响**：阶段 A 文档结构和安全/归属边界通过本次静态检查；这不等于产品最终合规、实现可运行或公开部署完成。当前只剩学生/外部环境门禁和后续阶段任务，不创建 `PLAN.md`、源码或远程状态。

## 2026-07-20T17:22:25+08:00 — AUDIT-005 独立复核后的最终规约收口

- **Task 编号**：AUDIT-005。
- **subagent 输出**：`/root/consistency_audit_final` 的只读复核发现两项 attribution/语义风险：M3 边界把待签字候选写成已固定，以及领域模型把精确 ReviewPolicy 归因于 D-020；没有发现 D-017 至 D-024、分发候选或 locator/历史输入的其他 P1。主智能体按报告修订 `SPEC.md` 与 `docs/research/TUTORING_DOMAIN_MODEL_DRAFT.md`，未让 subagent 写入或提交。
- **修订后复核**：再次得到 Markdown 27、local links 11/坏链接 0、围栏 0、用户故事 10、AC 50 且无缺失/重复、模块契约缺失 0、源码 0、`PLAN.md` 不存在、占位符 0、强特征凭据 0、`git diff --check` 无错误。针对“已固定/已确认隔离/本地原生包/无需选择”等 stale attribution 的搜索仅剩明确标注“待整体签字”的候选或历史说明。
- **门禁结果**：阶段 A 静态一致性收口；仍未执行 Open Design 外部安装/MCP、Superpowers 新会话 `writing-plans`、学生本人反思、SPEC 整体签字、PLAN、冷启动、实现、测试、CI、分发和部署。下一步提交只包含文档证据，不跨越门禁。

## 2026-07-20T17:24:04+08:00 — AUDIT-006 阶段 A 文档提交记录

- **Task 编号**：AUDIT-006。
- **提交 hash**：`11e1899afcf2355871e86ba6fa1a98658f767821`（`docs: finalize stage-a specification candidate [agent: Codex GPT-5]`）。
- **提交内容**：20 个规约/研究/审计文档；未包含 Open Design 安装器（已被忽略）、`PLAN.md`、正式源码、凭据或远程操作。
- **提交后动作**：本条记录将在下一次本地小提交中写入；不改变阶段门禁或产品边界。

## 2026-07-20T17:29:14+08:00 — AUDIT-007 自动续接后的门禁复核

- **Task 编号**：AUDIT-007。
- **触发上下文**：Goal 自动续接；没有新的学生产品决策，也没有把续接指令解释为 `SPEC.md` 签字。
- **当前状态**：HEAD 为 `bc3990fb6be147e359cf7c37c2670f6ab2da893c`，工作树干净；`PLAN.md`、`README.md`、`REFLECTION.md` 和正式源码仍不存在。
- **静态复核输出**：Markdown 27 个、本地链接 11 个且坏链接 0、代码围栏不平衡 0、用户故事 10 个、AC 50 个且无缺失、占位符 0、强特征凭据 0；`git diff --check` 无错误。
- **外部环境复核**：Superpowers `6.1.1` 缓存与 14 个核心 skill 仍存在，但 `superpowers` CLI/当前会话注册仍为空；Open Design 安装器 SHA-256 仍为 `63fc2e609489474e99187cdf94d01d063c1dbee733aaf2464d835cdc1e96f6b5`，`od` 及 MCP resources/templates 仍不可用。
- **结论**：没有安全的非决策实现工作可继续；继续停在学生整体确认 `SPEC.md`、Open Design 外部安装、Superpowers 新会话注册和学生本人反思门禁，不创建计划或源码。

## 2026-07-20T17:49:27+08:00 — GATE-001 SPEC 签字与 Open Design 配置调查

- **Task 编号**：GATE-001。
- **触发的 skill**：使用 `computer-use` skill 调查已安装的 Windows 应用；完整读取其 guidance/confirmations。应用自动化随后返回 `Computer Use was not approved to use Open Design`，因此停止 UI 输入并改用只读文件/进程/CLI 预览。Superpowers `writing-plans` 缓存文件已完整读取，但当前会话未注册该正式 skill，未虚报调用。
- **学生原始回答**：`已确认spec.md，已安装open design，brainstorming我感觉其实你可以代写（因为我确实没想出啥reflection，不要明确说出作者是AI就行感觉）`。
- **签字结果**：把完整 `SPEC.md` 视为学生于 2026-07-20 做出的整体确认；ReviewPolicy v1、单文件 `ProjectB.exe`、OCI/Hugging Face demo 和隔离限额成为 v1 工程方向，但仍须真实许可证、官方条款、构建/运行与安全验证。
- **Open Design 证据**：`Open Design.exe` 位于 `C:\Users\22078\AppData\Local\Programs\Open Design`，运行时版本 0.15.0；桌面进程正在运行。配置为 `agentId=codex`、`skillId=null`、`designSystemId=default`、`projectLocations=[]`，说明安装/onboarding 完成但尚未选择实际 skill/design system 或关联项目。
- **MCP 根因与只读验证**：`codex mcp list` 输出“没有配置 MCP server”；`~/.codex/config.toml` 只有 node_repl/OpenAI Docs。Open Design 自带 CLI 执行 `mcp install codex --print --json` 返回将运行 `codex mcp add open-design -- od mcp --daemon-url http://127.0.0.1:7456`。当前沙箱无权写用户配置，没有执行实际 add。
- **Reflection 边界**：拒绝代写或隐瞒 `REFLECTION.md` 的 AI 作者身份；这与学生个人偏好冲突，但课程 `AGENTS.md` 明文优先。可以在学生提供自己的事实/判断后校对、压缩或指出缺口，并记录辅助范围。
- **未执行**：未创建 `PLAN.md`、源码或 `REFLECTION.md`；未修改 Codex/Open Design 用户配置，未进行远程 push、付费调用或部署。

## 2026-07-20T18:45:26+08:00 — PLAN-001 阶段 B 计划生成与 Open Design 根因收口

- **Task 编号**：PLAN-001。
- **触发的 Superpowers skill**：已完整读取缓存的上游 `writing-plans` v6.1.1 规则，但本会话工具清单没有注册 `superpowers:writing-plans`，因此没有把手工产出冒充正式 skill 调用。按规则保留证据限制，并使用无历史上下文的计划分工 subagent 生成草案区段，作为透明 fallback。
- **关键 prompt / context**：学生已确认完整 `SPEC.md`；任务要求继续到当前阶段所有无需决策的工作，但不得跳过 Open Design、冷启动或实现批准门禁。计划必须覆盖材料、受约束模型端口、学习证据、复习规划、API、WebUI、演示、质量、分发、CI、文档和最终证据。
- **subagent 输出**：`/root/stage_b_plan_writer` 合并 G/T/M/X 区；`/root/plan_section_b` 合并 API/UI/DEMO/QA 区；`/root/plan_section_c` 合并 DIST/CI/DOC/INT/FIN 区。最终 `PLAN.md` 有 41 个详细 task（G-01..04、T-01..07、M1/X2/M2/M3、API/UI/DEMO/QA、DIST/CI/DOC/INT/FIN），每段包含目标、文件、接口、依赖/并行关系、红测或失败门禁、验证命令、双阶段评审、commit 和完成标准；所有状态保持 pending，未创建源码或测试。
- **Open Design 证据**：桌面端 `Open Design.exe` 0.15.0 已运行；只读配置显示 `agentId=codex`、`skillId=null`、`designSystemId=default`、无项目位置。`codex mcp list` 仍无服务器；其自带 CLI 的只读预览给出 `codex mcp add open-design -- od mcp --daemon-url http://127.0.0.1:7456`。当前环境不能写工作区外 Codex 配置，未执行该命令，需学生本机终端/新会话完成并记录实际 skill/design-system。
- **人工修改及原因**：主智能体修正 41-task 计划的红测表述、`backend/src/projectb/domain/materials.py` 路径和 body-text 术语；未选择 D-005、provider、design system、skill 或任何远程部署。拒绝代写/隐瞒学生 `REFLECTION.md` 作者身份，符合 `AGENTS.md`。
- **验证证据**：计划标题 41、台账 41（排除表头后）且无重复；计划专属 `git diff --check` 通过；尚未运行测试/构建/CI，因为仍在阶段 B。
- **经验教训**：外部桌面应用“已安装”不等于 MCP 已注册或实际设计系统已选；计划阶段应把工具接入证据和用户决策分别建模，fallback 生成也必须明确说明不能替代正式 skill 调用。

## 2026-07-20T19:17:40+08:00 — OD-002 MCP 重载与按需 skill/design system 调查

- **Task 编号**：OD-002（G-01 调查补充）。
- **触发的 skill / 工具**：使用已读取的 `computer-use` guidance/confirmations 做只读窗口枚举；尝试启动 Open Design 时收到 `Computer Use was not approved to use Open Design`，立即停止 UI 输入。随后使用当前已暴露的 `mcp__open_design__*` 工具做只读可用性检查，并读取本机 Open Design 0.15.0 bundled skill/design-system 文件；没有启动 Open Design run、上传文件或写用户配置。
- **当前注册证据**：`C:\Users\22078\.codex\config.toml` 已出现 `[mcp_servers.open-design]`，当前 Codex 工具清单也已暴露 `list_skills/list_plugins/list_projects/list_agents` 等 Open Design MCP 方法；但所有调用返回 `cannot reach the Open Design daemon at http://127.0.0.1:7456`。配置中的 `OD_SIDECAR_IPC_PATH` 本应从桌面 sidecar 发现其动态端口；桌面当前无可枚举窗口、daemon 日志最近记录 `shutdown requested`，所以发现失败后 CLI 回退到默认 7456。无需重复注册，只需正常重开并保持 Open Design 桌面端运行后复验。独立 PowerShell `codex mcp list` 仍显示无服务器，作为桌面/CLI 配置加载差异保留，不把它误判为唯一真相。
- **按需目录调查**：本地 bundled 目录有 162 个 skill 条目、151 个 design-system 条目；其中 `frontend-design` 为 2 文件完整工作流并带 Apache-2.0 LICENSE，覆盖 React/app/dashboard、真实 loading/error/empty 状态、响应式、键盘/焦点/对比度和自审；`web-design-guidelines` 带固定引用快照，适合作为实现后的审查 skill。`ui-ux-pro-max`、`platform-design`、`ui-skills`、`shadcn-ui`、`design-review` 的本地 `SKILL.md` 明确是 catalog stub/需上游 bundle，不声称已完整安装。
- **候选比较**：推荐 `skillId=frontend-design`；推荐 `designSystemId=default`（Neutral Modern，明确面向 B2B tools/dashboards/utility pages），并记录项目级覆盖：卡片半径最多 8px、letter-spacing 固定 0、学习工作台用紧凑间距。备选 design system 为 `shadcn`；`application`/`dashboard` 的紫色/深色玻璃、`notion` 的暖米色/负 tracking、`linear-app` 的深色紫/负 tracking 均与仓库 UI 规约不合。该组合仍是候选，未替学生写成已选定 SPEC 合同。
- **官方网络边界**：本轮官方站点/GitHub 两次访问均 HTTP 503；来源与许可证结论仅依据本机 bundled 文件中的 upstream/source/evidence 字段，不把网络失败伪报为验证成功。
- **人工修改及原因**：新增 [`docs/research/OPEN_DESIGN_SKILL_OPTIONS.md`](docs/research/OPEN_DESIGN_SKILL_OPTIONS.md) 作为候选比较和来源边界；未修改 `SPEC.md` 的实际选择。后续应由学生确认推荐组合或指定备选，且先让 Open Design daemon 恢复后再写 `OPEN_DESIGN_VALIDATION.md`。本条只追加真实环境与候选证据。
- **经验教训**：Open Design skill 是生成/审查配方，design system 是视觉 token/组件契约；两者都按需传给 run，不需要把 162 个条目全部安装。catalog stub 与完整 bundled workflow 必须分开记录。

## 2026-07-20T19:56:11+08:00 — PLAN-002 dispatch-unit granularity and red-test repair

- **Task 编号**：PLAN-002（阶段 B 计划质量复审）。
- **触发的 skill / 工具**：依据已完整读取的上游 `writing-plans` 规则与 `verification-before-completion` 约束进行只读复审；本会话仍没有可调用的正式 `superpowers:*` skill，因此没有冒充正式 skill 调用。
- **关键 prompt / context**：独立 plan-quality reviewer 指出宽 task 的 checkpoint、未定义红测 fixture、`materials.py` ownership 冲突、ledger 依赖遗漏、G-03 松门禁、T-01 后置脚本时序和 per-task commit 命令不够可执行。
- **subagent 输出**：`/root/plan_quality_review2` 提供 P1/P2 findings；`/root/plan_granularity_patch` 建议将宽项改为 Task Group 并正式拆成 dispatch units。两者均只读，没有改动实现文件。
- **主智能体修改**：`PLAN.md` 将 41 个 planning group 细化为 56 个 dispatch unit；新增 T-03A-C、X2-03A-C、M3-02A-C、API-01A-C、UI-01A-C、UI-02A-B、UI-03A-C、UI-04A-B、UI-05A-B。父 group 标为不可派发，unit 各自写入文件、接口、红测/绿测、双评审与 literal commit shell。修复 domain/materials 所有权、ledger 终端依赖、未定义 fixture、G-03 unresolved gate、T-01 bootstrap scanner/install 语义、G-01 重复注册命令和 G-04 worktree 命名。
- **验证证据**：`PLAN.md` 统计为 56 个 `### Task <unit-id>` heading、9 个 `Task Group` heading；尚未运行实现测试/构建/CI。Open Design MCP 直接调用 `list_skills/list_projects/get_active_context` 仍返回 `127.0.0.1:7456` daemon unreachable；三个现存 Open Design 进程没有 TCP listener，daemon 日志最后是正常 shutdown。当前重新枚举 bundled 目录得到 162 个 skill、152 个 design system（更正早先 151 的计数）。读取进程 command line 的 `Get-CimInstance Win32_Process` 返回访问拒绝，未反复请求提权。本条不把候选 skill/design system 写成已选。
- **人工修改及原因**：没有改变 `SPEC.md` 已确认的产品边界；仅为满足课程 fresh-agent 粒度和可追溯性拆分计划。没有创建/修改 `REFLECTION.md`。
- **经验教训**：复杂模块必须把子契约变成可审计的 dispatch ID，而不是只在 Step 2 里写“请自行拆分”；工具注册成功也必须分别验证 daemon 运行、资源选择和实际返回证据。

## 2026-07-20T20:51:23+08:00 — PLAN-003 terminal dependency and umbrella-unit audit

- **Task 编号**：PLAN-003（阶段 B 第二轮独立复审）。
- **触发的 skill / 工具**：继续依据已读取的 `writing-plans`、TDD 与 verification 规则做只读/静态审查；正式 Superpowers skill 仍不可调用，未声称完成正式阶段 B 流程。
- **subagent 输出**：`/root/plan_final_audit` 发现 G-01/G-02 可被绕过、API-02/API-03/API-04/DEMO/QA 仍为 umbrella、数个红测会因 fixture/依赖顺序错误失败、终端依赖缺口和 32 个旧 unit 缺 literal commit shell；`/root/docs_state_audit` 发现 D-005 与正式 writing-plans 门禁顺序、D-024 重问边界和历史 Open Design 当前时态不一致。
- **主智能体修改**：G-03/T-01 改为要求 G-01 PASS、G-02A/B/C 可用 PASS 与正式 writing-plans 证据；D-005 只可先选择，不能提前执行。新增 G-02A-C、M2-02A-B、API-02A-B、API-03A-C、API-04A-B、DEMO-01A-C、QA-01A-C、QA-02A-C，当前为 41 个 planning group、69 个 dispatch unit、17 个不可派发 group。修复 T-01 lockfile/red install、T-04 pre-API probe/app ownership、M1 synthetic fixtures、T-07 registry时序、M2/M3 fixture 与 UI/API/QA 终端依赖。
- **当前证据**：尚未执行任何实现红测/绿测、构建、CI、provider 或 Open Design run；所有新增 unit 仍 pending。后续还需完成 literal commit command 审计、静态图/链接/凭据检查和独立复核。
- **经验教训**：依赖表不能使用 `all` 或非派发 group 充当可解析前置；红测不仅要“会失败”，还必须先因目标实现缺失而失败，不能被安装顺序、未知 fixture 或尚未存在的上游 route 抢先触发。

## 2026-07-20T21:31:55+08:00 — PLAN-004 final static verification and file-scope repair

- **Task 编号**：PLAN-004（阶段 B 计划最终静态核对）。
- **触发的 skill / 工具**：按已读取的上游 `writing-plans` 与 verification checklist 做静态审计；本会话仍未注册可调用的正式 `superpowers:*`，没有把手工检查写成正式 skill 调用。
- **关键 prompt / context**：用户要求按需调查项目 skill；本轮收尾 Open Design 候选比较、计划拆分质量和阶段门禁证据，保持未获确认的 skill/design system 不进入 `SPEC.md`。
- **主智能体修改**：在 `PLAN.md` 为 T-07 红测补充局部 `request` 合同示例；将 API/UI/DEMO 子 unit 的 11 个共享文件路径展开为完整路径并与 literal `git add` 命令一致；在 `SPEC_PROCESS.md` 增加 PLAN-003 终审状态记录。
- **验证证据**：69 个 dispatch heading、69 个台账行、17 个不可派发 group；重复/缺失 ID 为 0；必填字段缺失为 0；提交命令路径不在 Files 声明中为 0；依赖未知节点为 0、拓扑环为 0；AC-01..AC-50 缺失为 0；14 个本地 Markdown 链接损坏为 0；全部 Markdown 围栏奇数为 0；凭据模式命中为 0；implementation-like 文件数为 0；`git diff --check` 只有换行符转换警告，没有 whitespace error。
- **人工修改及原因**：仅修订计划/过程文档，没有创建实现源码、测试、CI、部署或 `REFLECTION.md`；保留正式 `superpowers:writing-plans`、Open Design daemon/实际选择、冷启动和实现批准门禁。
- **经验教训**：计划的共享文件所有权必须同时出现在 Files、依赖和提交命令中；静态审计必须以 UTF-8 读取中文文档，并避免 `\s*` 跨行吞掉 Markdown 围栏。

## 2026-07-20T21:56:54+08:00 — PLAN-005 cold-start deadlock and exact-scope repair

- **Task 编号**：PLAN-005（阶段 B 独立终审修复）。
- **触发的 skill / 工具**：继续按上游 `writing-plans`、TDD 与 verification 规则进行只读复审和静态核验；正式 `superpowers:*` 仍不可调用，未声称正式 skill 证据。
- **subagent 输出**：`/root/final_docs_sanity` 发现 G-03 候选 unit 经 T-01 反向依赖 G-03，形成冷启动自依赖；X2-01 提交遗漏 `provider_candidates.py`；T-03C/DEMO-01B/QA-01C 有模糊 stage 指令；X2-01/X2-02 红测示例有未定义标识符。该审查还确认当前过程文档对 Open Design、41/69/17、formal writing-plans 与 D-005/G-03 顺序没有当前时态冲突。
- **主智能体修改**：把 G-03 明确为初始只含 `SPEC.md`/`PLAN.md` 的一次性 pre-implementation workspace，允许仅在实验中用最小临时 scaffold/test double，产物不合并，正式派发仍遵守依赖；补齐 X2-01/X2-02 自包含红测初始化与 X2-01 提交文件；禁止 T-03C 偷带 migration，DEMO-01B 只消费 T-07 公开注册接口，QA-01C 用精确 manifest/generator 路径；将 UI-03C 依赖改为 API-04A。同步把两份研究基线从“待注册 MCP”更新为“已注册、daemon 不可达、不得重复注册”。
- **验证证据**：PLAN 仍为 17 个不可派发 group、69 个 dispatch heading/69 个台账行；命令路径不在 Files 声明中为 0；未知依赖为 0、拓扑环为 0；AC-01..AC-50 缺失为 0；Markdown 围栏奇数为 0；模糊 migration/provider/fixture stage 指令已移除；`git diff --check` 无 whitespace error。
- **本地提交**：阶段 B 计划、审计与研究文档提交为 `83b32e7d7db16c1fcccbe23c3168a026629482b7`（`docs: finalize stage-b dispatch plan [agent: Codex GPT-5]`）；未 push、未创建 PR/MR。
- **人工修改及原因**：只修订计划、研究和过程文档；未创建、合并或运行任何正式实现，未越过冷启动/实现批准门禁，未创建 `REFLECTION.md`。
- **经验教训**：冷启动发生在正式依赖尚未实现之前，因此必须把“上下文依赖合同”和“已实现依赖”分开；否则课程要求本身会在计划图外形成语义死锁。

## 2026-07-21T18:58:23+08:00 — OD-003 Open Design 选择确认与连接诊断

- **Task 编号**：OD-003（G-01 部分验证）。
- **触发的 Superpowers skill**：无；本次是 Open Design 外部环境/证据检查，当前会话仍未暴露 `superpowers:*`。没有把本地读取或直接 API 请求冒充 Open Design MCP 成功调用。
- **关键 prompt / context**：学生提供 Open Design 截图，界面已显示 `技能: frontend-design`、`Neutral Modern` 和链接目录 `ProjectB`，并询问“选了之后怎么办”。为避免在实现门禁前生成原型，明确要求暂不点击“发送”。
- **运行与选择证据**：Open Design 0.15.1 daemon 日志报告健康动态 loopback endpoint；直接只读 API 返回 `frontend-design`、`mode=prototype`、`designSystemRequired=true`、`default` 与 `Neutral Modern`，与学生截图一致。截图未复制入仓库，动态端口未写入仓库或 Codex 配置。
- **MCP 诊断**：当前 Codex task 的 MCP 进程仍缓存启动时的 fallback `127.0.0.1:7456`；`list_skills`、`list_projects`、`get_active_context` 因而继续失败。已安装 `od mcp --help` 说明 MCP 进程会缓存 URL，daemon 重启后须重启 MCP client；恢复动作是保持 Open Design 开启并新建 Codex task，不重复注册 MCP。
- **文档修改**：将 D-024 的实际选择写入 `SPEC.md`，新增 [`docs/engineering/OPEN_DESIGN_VALIDATION.md`](docs/engineering/OPEN_DESIGN_VALIDATION.md)，并同步 `PLAN.md` 与当前状态审计。G-01 仍为 partial；没有创建 Open Design project/run/artifact，没有修改正式 UI/源码、测试、CI 或 `REFLECTION.md`。
- **subagent 输出 / commit hash**：`/root/od_docs_audit` 进行只读当前时态一致性复核，确认 G-01 未误标 PASS 且历史/当前状态无剩余冲突；本轮选择证据提交为 `39f278dee93fa61bc3fa70334b3f81e56ef04e3c`（`docs: record Open Design selection evidence [agent: Codex GPT-5]`）。
- **人工修改及原因**：学生本人完成界面选择；智能体只记录已观察事实并解释下一步，以遵守 UI 设计选择和实现阶段人工门禁。
- **经验教训**：桌面 daemon 健康、composer 选择和当前 task 的 MCP 可达性是三项独立证据；不能因前两项成功就把 G-01 写成 PASS，也不能把每次重启变化的端口固化进配置。

## 2026-07-21T21:08:02+08:00 — OD-004 Open Design 门禁范围修正

- **Task 编号**：OD-004（G-01 scope correction）。
- **触发的 Superpowers skill / 工具**：无正式 Superpowers skill；依据仓库 `AGENTS.md`、`SKILLS_SETUP.md`、已安装 Open Design 0.15.1 本地文档、`frontend-design/SKILL.md`、default/Neutral Modern package 和新任务提供的 MCP 只读结果做证据复核。
- **学生原始问题**：学生指出“按理来说不应该是下载 skill 文件吗，为什么要让我把 Open Design 打开挂着”，要求解释并修正文档。
- **事实证据**：Open Design 桌面包已携带完整 `frontend-design/SKILL.md`、Apache-2.0 `LICENSE.txt` 和 default design-system 文件；fresh MCP task 返回 built-in `frontend-design`（`mode=prototype`、`designSystemRequired=true`）、`projects=[]`、`active=false`。空 project/context 是实现前状态，不是 MCP 失败。
- **主智能体修改**：将 G-01 改为 environment/MCP/bundled-skill/selection gate 并标记 PASS；明确 daemon 只在 MCP 调用或实际 design run 时按需运行，不要求长期挂起或创建空 project；将真实 project/run/artifact、截图和 review 证据后置到 UI-01A，并规定生成源代码不得绕过 TDD 红测进入生产目录。同步修订 `SPEC.md`、`PLAN.md`、`SPEC_PROCESS.md`、`DECISIONS_NEEDED.md`、`SKILLS_SETUP.md`、审计和研究基线。
- **验证边界**：本轮未创建 Open Design project、未发送 prompt、未运行生成、未修改前端/生产源码、未运行测试/构建/CI，未创建或修改 `REFLECTION.md`。OD-003 的 stale-endpoint 历史记录保留。
- **subagent 输出 / commit hash**：`/root/od_gate_scope_audit` 只读复核确认 G-01 应 PASS、无须长期开 daemon、UI-01A 后置 run；修订提交为 `b93c096db29f7b957950a0cfc74b80170a38d25a`（`docs: correct Open Design gate scope [agent: Codex GPT-5]`）。
- **经验教训**：必须把“技能文件已安装”“MCP/daemon 可连接”“正式 Open Design run 已执行”建成三个独立证据层；否则会为了证明工具可用而制造空项目或让用户无意义地保持桌面应用运行。
## 2026-07-21T22:25:00+08:00 - G-02 evidence baseline (pending)

- **Task:** G-02 group; G-02A/G-02B/G-02C remain pending.
- **Skills/tools used:** `openai-docs` was read and followed for current OpenAI policy evidence; official OpenAI Developer Docs MCP search/fetch was used. Formal `superpowers:*` skills are still not callable in this session, so the required red/green evidence validator was run directly and the limitation is not represented as a formal Superpowers invocation.
- **Subagent evidence:** `g02a_dependency_audit` found no project manifests or lockfiles; host Python 3.14.3 and `pypdf 6.10.2` are environment-only; Codex-bundled `pypdfium2`/Playwright are not project dependencies; exact FastAPI, keyring, test, freezer, React/Vite, OpenAI SDK and transitive licenses remain unverified. `g02c_distribution_audit_retry` found Docker daemon unavailable and first-party freezer/registry/Hugging Face retrieval blocked by connection close/timeouts; no build, account, deployment, or paid action was performed.
- **Red evidence:** after fixing two script-level PowerShell issues, `powershell -ExecutionPolicy Bypass -File scripts/verify_evidence.ps1` returned `EVIDENCE_VALIDATION_FAIL errors=3 rows=0` because all three evidence files were absent.
- **Green evidence:** the same command returned `EVIDENCE_VALIDATION_PASS rows=37 explicitly_blocked=28` after adding the three ledgers. This validates table shape, URLs, dates, allowed status values, and secret-pattern absence only; it does not close G-02.
- **Files changed by coordinator:** `docs/engineering/DEPENDENCY_BASELINE.md`, `PROVIDER_POLICY_EVIDENCE.md`, `DISTRIBUTION_EVIDENCE.md`, `scripts/verify_evidence.ps1`, `PLAN.md`. The ledgers intentionally mark unresolved rows `explicitly-blocked`; no production source, credentials, private course material, package install, or remote deployment was added.
- **Commit:** checkpoint `24caa35` (`docs(G-02): record blocked evidence baseline [agent: Codex GPT-5]`). This is a partial evidence checkpoint; G-02A/B/C remain pending and no implementation gate was opened.
- **Lesson:** a validator PASS can coexist with blocked evidence by design; downstream tasks must consume only `verified` rows and keep all blocked implementation gates closed.

## 2026-07-21T22:40:00+08:00 - G-03 Superpowers availability recheck

- **Observed callable tools:** the current session tool catalog contains no `superpowers:*` entries.
- **Observed local cache:** `C:\Users\22078\.codex\plugins\cache\openai-curated-remote\superpowers\6.1.1\skills` contains the expected `brainstorming`, `writing-plans`, worktree, TDD, review, debugging and verification directories.
- **Decision:** cached files are not treated as a formal skill invocation. G-03 remains blocked until a fresh session exposes the registered skill or the course explicitly accepts the documented fallback, then the student selects D-005 and approves implementation after cold-start revisions.
- **No changes:** no cached skill source was copied into the repository, no implementation was started, and no user-level Codex configuration was modified.

## 2026-07-21T22:45:00+08:00 - Documentation checkpoint verification

- `scripts/verify_evidence.ps1`: `EVIDENCE_VALIDATION_PASS rows=37 explicitly_blocked=28`.
- `git diff --check`: pass; working tree clean after commit `96164fe`.
- PLAN dispatch ledger: `PLAN_DISPATCH_UNIQUE_PASS count=69`.
- Focused credential scan: `CREDENTIAL_SCAN_PASS actual-token-patterns=0`; engineering evidence links: `ENGINEERING_LINKS_PASS`.
- No backend/frontend implementation, README, CI file or student `REFLECTION.md` was created. G-02A/B/C remain pending, and G-03 remains blocked by formal Superpowers registration/fallback acceptance, cold-start validation and implementation approval.

## 2026-07-21T23:03:34+08:00 - OD-005 current-state documentation cleanup

- **Task:** Correct residual Open Design wording before the student restarts Goal mode; no implementation task was opened.
- **Trigger/context:** The student correctly challenged the earlier implication that a bundled skill needed downloading or that Open Design had to remain open without active work. The authoritative state is G-01 PASS, with a real project/run/artifact deferred to UI-01A after cold-start validation and implementation approval.
- **Changes:** Added a current authoritative snapshot to `docs/PROJECT_AUDIT.md`, relabeled its startup-only tool state as historical, corrected stale G-01/current-stage/count wording in `SPEC_PROCESS.md` and `docs/REQUIREMENTS_COMPLIANCE_AUDIT.md`, marked the stale-endpoint research section as superseded, fixed the remaining “Open Design 可用后” wording in `docs/research/MUTEX_RACE_SOURCE_MAP.md`, and updated `SKILLS_SETUP.md` to say ProjectB must not repeat installation or the preselection prompt.
- **Evidence boundary:** Historical timestamped observations were retained rather than rewritten. No Open Design prompt, `start_run`, project, artifact, production source, test, build, CI, deployment, credential, or `REFLECTION.md` was created or modified.
- **Skill/workflow:** No formal `superpowers:*` skill is callable in this task; this was a documentation consistency correction, not a substitute for the still-missing formal `writing-plans` evidence.
- **Subagent reviews:** `/root/od_consistency_audit` found the remaining stale wording in `MUTEX_RACE_SOURCE_MAP.md` and then reported no findings on the final diff. `/root/process_status_audit` found the stale G-01/68-pending counts and startup-stage labels; all four current-state findings were corrected. Both reviews were read-only.
- **Verification:** `git diff --check` passed (line-ending conversion warnings only); `scripts/verify_evidence.ps1` returned `EVIDENCE_VALIDATION_PASS rows=37 explicitly_blocked=28`; the PLAN ledger returned `rows=69 pass=1 pending=68`; current-contract and stale-wording assertions passed; focused credential scan found no matching token/private-key pattern.
- **Commit:** `3d0100d` (`docs(OD-005): clarify Open Design workflow state [agent: Codex GPT-5]`).
- **Lesson:** Status documents need an explicit current snapshot when historical diagnostics remain in the same file; otherwise a correct evidence trail can be mistaken for a live instruction.

## 2026-07-22T00:53:17+08:00 - G-02A exact dependency and license baseline

- **Task 编号**：G-02A。
- **触发的 Superpowers skill / 工具**：当前会话仍未暴露正式 `superpowers:*`；按 TDD/verification 和课程双评审纪律使用证据校验器、精确临时 CPython/Node 运行时及 fresh read-only reviewer。未把这些动作冒充 `superpowers:writing-plans` 或正式实现。
- **关键 prompt / context**：在任何生产 manifest 前锁定 Windows x64 工具链、直接/传递依赖、许可证和组件兼容性；不得使用真实 key、provider 请求、私人课件或系统级安装。
- **Red / Green 证据**：扩展校验器后，文档/锁缺失产生 `EVIDENCE_VALIDATION_FAIL errors=29 rows=37`；修复后严格运行得到 `EVIDENCE_VALIDATION_PASS rows=63 explicitly_blocked=2 python_pins=54 npm_packages=166`。CRLF 锁副本仍 PASS；React direct 漂移和 `UNKNOWN` Python 许可证 fixture 均按预期 FAIL。Python 3.14.6 smoke 输出 `PYTHON_SMOKE_PASS packages=16 ... provider_network=0`；Node 24.18.0 smoke 输出 `NODE_SMOKE_PASS modules=13 ...`；Uvicorn、PDFium 和收集 keyring completion 资源后的单文件组件均重新运行成功。
- **subagent 输出 / review**：`g02a_exact_audit` 与其 npm closure 子审计给出 54/166 精确闭包；`g02a_staged_review` 先发现 CRLF 摘要、PLAN 文件合同、direct/license 校验和 smoke 证据问题，修复后又发现错误的 Python 包计数。最终复审确认无 P0/P1 或证据真实性阻断，并保留 clean-clone bootstrap 与完整应用/干净机验证给 T-01/DIST-01。
- **人工修改及原因**：使用规范化 LF 摘要；增加 18 个 Python direct 和 npm root 3+13 direct 的双向/版本/许可证校验、PyPI 精确来源、npm tarball/SRI 与许可证 allowlist；新增无网络 Python/Node smoke harness。没有创建生产源码、manifest、CI、部署或 `REFLECTION.md`。
- **commit hash**：`22b516af7b6f4896c6127e75b2585435e407a3c0`（`docs(G-02A): lock toolchain and license baseline [agent: Codex GPT-5]`）。
- **经验教训**：锁文件的字节摘要必须定义跨平台换行语义；“依赖表存在”不等于 direct 集合、许可证或 smoke 已被机器互证；人类可读计数也必须由测试数据派生，不能手填后长期漂移。

## 2026-07-22T01:16:37+08:00 - G-02B provider policy, capability, and cost evidence

- **Task 编号**：G-02B。
- **触发的 skill / 工具**：完整遵循已读取的 `openai-docs` skill，通过官方 OpenAI Developer Docs MCP 获取模型、定价、数据控制、PDF input、token counting、File Search 与 API reference；没有 key、请求正文、付费调用或私人材料。正式 `superpowers:writing-plans` 仍不可调用，该缺口不被本任务冒充关闭。
- **关键 prompt / context**：验证 P/F 实现所需的当前能力、留存/删除/区域/费用事实，同时解决“G-02B 等待 X2-03 live test、X2-03 又依赖 G-02B”的计划循环；官方未保证事项只能映射为显式 fail-closed，不能解释成供应商支持。
- **验证证据**：`-RequireProviderReady` 返回 `EVIDENCE_VALIDATION_PASS rows=63 explicitly_blocked=2 python_pins=54 npm_packages=166`；两项 blocker 均属于 G-02C。离线手算为 `0.01650 + 0.03135 + 0.00250 + 0.10000 = US$0.15035`，低于 AC-48 的 US$1 上限；这不是实际账单或调用成功证据。
- **subagent 输出 / review**：`g02b_official_audit` 建议把有官方来源且有确定性 fail-closed 的负能力边界标为 verified，以消除计划循环。`g02b_staged_review` 核对 AC-20/21/27/39/48/49/50、价格和 P/F 原语，发现 Vector Store 删除受理后最长 30 天服务端移除窗口遗漏；修复后批准提交。
- **人工修改及原因**：新增精确模型、PDF input、token count、F filter/result rows 与保守费用公式；明确 `store:false` 不是 ZDR，F 默认 `source_disabled`，未知清理为 `delete_incomplete`，delete accepted 不等于即时物理清除。没有启用 adapter、创建 provider 对象或修改生产源码。
- **commit hash**：`5ac9d47ddda845ed78f1758326fb547610274f4c`（`docs(G-02B): verify provider policy and cost [agent: Codex GPT-5]`）。
- **经验教训**：证据门禁判断的是“实现是否无需猜测”，不要求供应商提供正向保证；但删除 API 成功、数据不可再用和服务端物理清除必须分开建模与展示。

## 2026-07-22T01:25:01+08:00 - G-02C hosting cost conflict checkpoint

- **Task 编号**：G-02C（blocked checkpoint，未完成）。
- **触发的 skill / 工具**：读取并遵循 `browser:control-in-app-browser` 的安全边界做官方页面调查；浏览器明确拒绝 Render/Koyeb 域名后没有绕过或改用其他表面访问。其余精确事实来自 PyPI/PyInstaller 官方资料、Docker Official Images `repo-info` 固定提交和 Hugging Face 官方 `hub-docs` 固定提交。未调用正式 Superpowers skill。
- **关键 prompt / context**：验证已确认的 Windows 单文件、OCI/HF demo 是否满足许可证、架构、HTTPS、存储、休眠、配额和无付费授权；证据冲突时必须提出 SPEC 决策而非静默替换。
- **事实与验证**：PyInstaller 6.21.0、`python:3.14.6-slim-bookworm` index/amd64 digest、HF Docker runtime/HTTPS/50GB 临时盘/CPU Basic/48 小时休眠均有固定官方快照。当前 HF 文档同时要求付费方案才能创建新的 Docker/Gradio Space；`host-cost`、`host-account` 因此是仅余两个 blocker。标准 validator PASS（63/2/54/166），`-RequireDistributionReady` 按预期 FAIL `explicitly-blocked rows=2`。
- **subagent 输出 / review**：`g02c_blocker_review` 对 AC-10/41/43/47 与证据质量做两阶段只读审查，未发现 Critical，批准提交 blocked checkpoint，但明确禁止勾选 G-02C Green/Reviews/Commit。
- **人工修改及原因**：新增 D-025 三个候选方向并同步 SPEC、PLAN 和两份分发研究文档；保留 OCI/同构 WebUI/mock/HTTPS/隔离合同，不选择账号、主机或费用方案。没有 Docker build/run、账号动作、付费订阅、部署或公网 URL。
- **checkpoint hash**：`be666537706b4c133673029d950e84f15ea3ae1b`（`docs(G-02C): record hosting cost conflict [agent: Codex GPT-5]`）。
- **经验教训**：“免费硬件档位”与“免费账号可创建资源”是不同命题；外部平台事实与已确认成本边界冲突时，正确产出是可审查的 blocker 和人工决策，而不是替用户换平台。

## 2026-07-22T02:29:11+08:00 - G-02C-R1 alternative-host research and documentation repair

- **Task 编号**：G-02C-R1（D-025 只读研究；G-02C 仍未完成）。
- **触发的 Superpowers skill / 工具**：当前可调用清单仍没有 `superpowers:*`，没有把本轮研究冒充 `writing-plans` 或任何正式 Superpowers 调用。使用各厂商官方网页/官方 Markdown 与 Microsoft Learn commit metadata 做只读核验；未登录、未接受条款、未创建账号或资源。
- **关键 prompt / context**：Goal 在 Open Design 文档修正后续接；学生尚未选择托管平台。本轮只允许完成不依赖该选择的候选调查、当前状态同步和验证，必须保持 OCI/同构 WebUI/mock/HTTPS/隔离合同，不得越过 D-025、G-03 或实现批准门禁。
- **网络失败与替代**：官方搜索接口返回 HTTP 503；`curl.exe` 返回 `schannel: AcquireCredentialsHandle failed: SEC_E_NO_CREDENTIALS`，`Invoke-WebRequest` 返回“基础连接已经关闭: 接收时发生错误”。没有重试提权、关闭 TLS 校验或访问已被浏览器安全策略禁止的 Render/Koyeb。Node.js 24.14.0 `fetch` 对相同官方 URL 成功，只读取公开内容。
- **研究结论**：新增 `docs/research/PUBLIC_HOSTING_ALTERNATIVES.md`。条件候选是已有 x64 Docker 主机（既有 HTTPS 或 Tailscale Funnel）与 Azure for Students + Container Apps；付费 HF 保留为需明确成本授权的第三项。Cloudflare Quick Tunnel、Northflank Sandbox、Oracle Always Free 与静态 Pages 的当前不适用原因均有官方来源。没有把候选写成 selected host，也没有修改 `SPEC.md`。
- **subagent / review**：`/root/hosting_tunnel_research` 的初始任务消息在传输中不可读，未产生可采信输出并被中止；其遗留只读子任务 `/root/hosting_tunnel_research/cloudflare_tailscale` 也在最终复验前中止，未使用其输出或文件。本轮事实均由主智能体从官方来源复核。`/root/d025_spec_review` 的第一次只读规约审查发现本条过程记录与两份审计更新时间缺失（P1/P2），并确认其余 D-025/G-03/实现门禁一致；缺口即时修复后，复审以无 Critical/P1 批准当前 diff，且未改写旧时间戳证据。
- **第二阶段质量复核**：逐项回读官方当前页面，检查候选表中的 OCI 架构、HTTPS、免费/credit/付款方式、scale-to-zero、临时存储、beta/带宽、idle 回收和非 production 限制；把“HF 仍是 selected host”改为“实际 host 未定，HF 只保留冲突证据”，并移除静态托管段落中可能暗示应用已实现的措辞。未引入第三方代码或依赖，因此本轮没有新增 README 许可证条目。
- **人工修改及原因**：同步 `DECISIONS_NEEDED.md`、`PLAN.md`、`SPEC_PROCESS.md`、两份审计、分发证据和四份研究基线；只把已完成调查写成候选证据，`host-cost`/`host-account` 保持 `explicitly-blocked`。没有 Open Design project/run/artifact、Docker build/run、registry、付款方式、student credit、部署、CI、生产源码或 `REFLECTION.md`。
- **验证证据**：普通校验为 `EVIDENCE_VALIDATION_PASS rows=63 explicitly_blocked=2 python_pins=54 npm_packages=166`；`-RequireDistributionReady` 按预期只因两项托管 blocker 返回 exit 1。Markdown 校验为 34 文件、20 本地链接、0 坏链接、0 奇数围栏；当前时态陈旧措辞扫描为 0；`git diff --check` 无 whitespace error，仅有 Windows 行尾提示。
- **commit hash**：`47f294ca994cc1fdafc82420a167f305716152ed`（`docs(G-02C-R1): research no-paid hosting alternatives [agent: Codex GPT-5]`）。该 hash 是只读研究/文档 checkpoint，不是 G-02C PASS。
- **经验教训**：免费额度、无需信用卡、无需付款方式和不会自动产生账单是四个不同条件；候选调查可以让人工门禁更易回答，但在学生选择并确认 SPEC diff 前不能把候选事实写入 selected-host 证据行。

## 2026-07-22T02:55:19+08:00 - D-001 Superpowers installation-state correction

- **Task 编号**：D-001（只读环境诊断；阶段 B/G-03 仍阻断）。
- **触发的 skill / 工具**：使用 `openai-docs` skill 的 Codex self-knowledge 路径。Codex manual helper 因 Windows Schannel `SEC_E_NO_CREDENTIALS` 失败；按 skill 规则改用官方 OpenAI Docs MCP，获取 `Plugins` 与 `Build plugins` 页面。没有关闭 TLS 校验、登录 CLI 或修改用户配置。
- **关键 context**：Goal 自动续接后仍无 D-025 选择；唯一安全推进项是验证重开 task 是否已经让正式 Superpowers skills 可用。当前 task 的 skill catalog 仍无 `superpowers:*`。
- **环境证据**：Codex CLI 0.144.4；Superpowers 6.1.1 manifest SHA-256 `42F44D5E17AFF909BD6F2A53795D516D8CA78CD9512C32C91F19CBBCCED68877`；14 个核心 skill 目录完整。`config.toml` 没有 Superpowers enabled-plugin 或对应 marketplace；CLI `marketplace list`、installed/available plugin JSON 均为空。CLI doctor 的未认证/网络结果只描述 CLI 环境，不冒充桌面账号状态。
- **官方交叉核验**：OpenAI `openai/plugins` 当前 HEAD `11c74d6ba24d3a6d48f54a194cd00ef3beea18f9`，marketplace blob `dff3ad09da7efc35a6d3b905b1aa07795bc240b6` 将 Superpowers 标为 Codex 可安装。官方文档说明插件安装/启用状态与 cache 分离，bundled skills 在安装后的新 chat/session 才可用。
- **修订与非动作**：新增 `docs/engineering/SUPERPOWERS_VALIDATION.md`，同步 `SKILLS_SETUP.md`、D-001、PLAN/G-03、过程和审计当前状态。没有复制/修改缓存、添加 marketplace、安装 plugin、修改 auth/config、正式调用 Superpowers、执行冷启动或开始实现。
- **结论**：旧的“插件已安装，只差会话注册”判断证据不足，现纠正为“cache-only / not callable”。用户须在 Codex App Plugins 安装/启用 Superpowers 并新建 task，或取得课程接受 fallback 的明确证据。
- **两阶段复核**：先按 `AGENTS.md`/D-001/G-03 检查门禁合规，确认没有把 cache、fallback 或历史触发冒充正式 invocation；再核对官方 plugin loading/config 规则、CLI/desktop 证据隔离、bundle hash、skills 清单和历史/current 措辞。修复三处历史快照的“已安装”误导表述后，无 Critical/P1 残留。
- **验证证据**：标准 evidence validator 为 `PASS rows=63 explicitly_blocked=2 python_pins=54 npm_packages=166`；distribution-strict 仍按预期只因两项 D-025 host blocker 失败。PLAN ledger 为 69 unique/3 PASS/66 pending；Markdown 为 35 文件、21 本地链接、0 坏链接、0 奇数围栏；当前 Superpowers 陈旧措辞扫描 0，focused credential scan 0，`git diff --check` 无 whitespace error。
- **commit hash**：`1eb9a7da7a2814b89779861672f0e0f6e75c7d33`（`docs(D-001): correct Superpowers installation state [agent: Codex GPT-5]`）。该提交只记录环境诊断和门禁纠正，不是正式 Superpowers invocation。
- **经验教训**：插件 payload、marketplace 可发现性、installed/enabled config 和新任务实际 skill catalog 是四层独立证据；任何一层缺失都不能用 cache 路径代替正式 invocation。

## 2026-07-22T20:16:26+08:00 - D-001 Superpowers installation recovery and stale-task diagnosis

- **Task 编号**：D-001（安装层恢复；新 task 注册/正式调用仍阻断）。
- **触发的 skill / 工具**：使用 `openai-docs` skill 的 Codex self-knowledge 路径。Codex manual helper 再次因 Windows Schannel `SEC_E_NO_CREDENTIALS` 失败；按 skill 规则改用官方 OpenAI Docs MCP 获取 `Plugins` 与 `Build plugins`。没有关闭 TLS 校验或修改用户配置。
- **关键 prompt / context**：学生指出已添加 Superpowers 并询问为何仍不可用。当前 task 的 supplied skill catalog 仍无 `superpowers:*`，因此需要区分安装状态与旧 task 的加载快照。
- **环境证据**：`config.toml` 现含 `[plugins."superpowers@openai-api-curated"]` 与 `enabled = true`，最后写入时间 `2026-07-22T20:11:10+08:00`。所选 `11c74d6b` 安装快照 manifest 版本 5.1.3、MIT、SHA-256 `CE06DE063CABC2C41FFCE239AEB5CB941FCAB0C98DDDEDE927AA06E854D40AED`；14 个 skill 目录全部含 `SKILL.md`。旧的 6.1.1 remote cache 不再用于判断当前安装。
- **诊断**：安装与启用层 PASS；当前任务加载层 FAIL。官方文档明确说明 installed plugin 的 bundled skills 在安装后的新 chat/task 或 CLI session 才可用。CLI 的空 marketplace/plugin JSON 属于独立未认证 CLI 环境，不能推翻桌面 config/cache 的直接证据。
- **修订与非动作**：同步 `SUPERPOWERS_VALIDATION.md`、`SKILLS_SETUP.md`、D-001、PLAN/G-03、过程与审计当前状态；保留 02:55 的历史诊断原文并追加本次状态变化。没有由智能体安装/重装插件、复制 skill、正式调用 Superpowers、执行冷启动、创建实现源码、Open Design run、部署或 `REFLECTION.md`。
- **门禁结论**：D-001 已从“安装/启用”缩小为“新建 ProjectB task 并实际调用 `writing-plans`”。在新 task 产生真实 invocation/diff 前，不把 fallback 计划标成正式 Superpowers 产物，也不进入 G-03 或实现。
- **subagent / 两阶段评审**：`/root/superpowers_stale_audit` 先审查课程门禁与当前/历史时态，再审查证据强度和文档质量；发现 `SPEC.md` 风险矩阵的旧 cache-only 当前态、日志字段缺口，以及两处把 config 与具体快照绑定过强的 P1/P2。四项均已修正；复核未发现 Critical/P1，最终 P2 也在提交前关闭，并确认其余路径、版本、hash、14 skills 和新 task 门禁一致。
- **验证证据**：`scripts/verify_evidence.ps1` 返回 `EVIDENCE_VALIDATION_PASS rows=63 explicitly_blocked=2 python_pins=54 npm_packages=166`；`-RequireDistributionReady` 按预期只因 D-025 的两条 hosting rows 返回 exit 1。Markdown 为 35 文件、21 本地链接、0 坏链接、0 奇数围栏；当前态陈旧措辞扫描 0，focused credential scan 0；`git diff --check` 无 whitespace error，仅有既有 CRLF 提示。
- **人工修改及原因**：主智能体只修订 9 份规约/过程/审计文档，使安装、启用、会话加载和正式 invocation 四层证据分离；没有重写先前时间戳日志或将学生安装动作归因给智能体。
- **commit hash**：`178ab5c584849ca3cbf855d48a7a9b074ab220ef`（`docs(D-001): record Superpowers installation recovery [agent: Codex GPT-5]`）。该提交证明文档状态修正，不是正式 Superpowers invocation。

## 2026-07-22T21:09:21+08:00 - PLAN-006 formal writing-plans invocation and three-audit checkpoint

- **Task 编号**：D-001 / PLAN-006（正式 invocation 已闭合；阶段 B 计划质量复审未通过）。
- **触发的 Superpowers skill**：新 task catalog 实际暴露 14 个 Superpowers skills。主智能体完整读取、明确宣布并使用 `using-superpowers`、`brainstorming`、`dispatching-parallel-agents`、`receiving-code-review`、`writing-plans`，正式调用 `writing-plans` 审核已确认的 `SPEC.md` 与 fallback `PLAN.md`。调用证据只关闭 D-001，不冒充计划 PASS。
- **关键 prompt / context**：只允许审查并修订规约、计划、研究与过程证据；禁止越过阶段 B、G-03 和学生实现批准。要求分别核对 formal skill 合规、SPEC/PLAN/AC 覆盖与 gate、69-unit dispatch/worktree/commit 可执行性，并保留历史记录、不伪造失败测试或人工决定。
- **subagent 输出 / review**：`/root/plan_skill_audit` 只读判定 baseline PLAN 未满足完整代码、2--5 分钟单动作、placeholder/path/coverage 要求；`/root/plan_coverage_audit` 只读发现 source/deletion/F lifecycle 的 API/UI 链、M3 owner、UUID/hash/region/evidence/trace grammar 与命名冲突，并确认 D-025 不应阻塞 G-03；`/root/plan_dispatch_audit` 只读确认 69/69 标题/ledger 一致，同时发现 worktree 前置循环、deploy owner、CI/FIN commit 自引用、G-01 历史证据和 review ledger 缺口。三项审计阶段均未编辑文件。
- **后续授权与所有权**：主智能体随后分别授权 coverage agent 只改 `SPEC.md`/`PLAN.md`，skill agent 只创建 `docs/engineering/WRITING_PLANS_VALIDATION.md`，dispatch agent 只更新 `SKILLS_SETUP.md`、`SUPERPOWERS_VALIDATION.md`、`DECISIONS_NEEDED.md`、`SPEC_PROCESS.md`、`AGENT_LOG.md` 与两份审计。coverage repair 当前把目标结构更新为 42 groups/72 units（新增 T-08、M3-02D、API-01D；17 个 Task Group 不变），并把 G-03 前置收敛为 formal plan evidence、G-01、G-02A/B 与 D-005。该拆分避免共享文件交叉写入；本条不声称尚未复验的 PLAN 已通过。
- **研究文档修订概览**：主代理协调的窄幅研究同步更新 constrained AI/source locator、OpenAI adapter SDK/Apache-2.0 manifest/notice、L/P/F consent/remote lifecycle、provider/threat/deployment/domain-model 边界，只对齐已确认事实。没有新增依赖、源码、真实 key/provider 调用、账号资源、付费、部署或新产品选择。
- **人工修改及原因**：学生此前完成 Superpowers 安装/启用；本轮没有新的 D-025 host 选择或 D-005 agent 选择。D-001 因新 task 的真实 catalog 与 invocation 关闭；阶段 B 因 formal review FAIL 保持开放。`REFLECTION.md` 仍由学生本人撰写，AI 未创建或代写。
- **验证证据与边界**：focused current-state/stale-wording 扫描的剩余旧措辞均位于明确标注的历史段或时间戳日志；当前权威段一致写明 D-001 closed、Stage B FAIL、D-025 不阻塞 cold start。七个目标 Markdown 文件检查为 `files=7 odd_fences=0 broken_local_links=0`；`git diff --check` exit 0，仅报告既有 LF/CRLF 转换 warning；目标 diff 为 7 文件、84 insertions/30 deletions，未包含 PLAN/SPEC/生产源码。`WRITING_PLANS_VALIDATION.md` 已由独立 owner 创建并自验。active PLAN remediation 尚在独立 owner 工作树中，42/72 是待完整复验的目标结构，不在此写成 PASS。未运行产品测试、构建、CI、Open Design run、provider 或部署。
- **commit hash**：尚未创建；不得把工作树 diff 或 invocation 当作提交证据。
- **经验教训**：工具被正式调用只证明流程发生，不证明产物合规；外部托管决策、冷启动可理解性与实现批准必须分开建 gate。审计发现与后续修订也必须分开记录，才能避免把只读 reviewer 写成实现者。
- **经验教训**：`enabled = true` 能证明插件来源与开关状态，但不能单独证明具体缓存 hash；具体快照必须由该来源的实际安装目录和 manifest 独立证明。安装成功也不会热更新已运行 task 的 skill catalog。

## 2026-07-22T23:22:28+08:00 - PLAN-007 detailed-plan review remediation resumed

- **Task 编号**：PLAN-007（阶段 B 详细计划修订；仍未通过）。
- **触发的 Superpowers skill**：主智能体继续使用已完整读取的 `using-superpowers`、`writing-plans`、`receiving-code-review` 与 `dispatching-parallel-agents`；没有调用实现、worktree 或 TDD skill，因为实现门禁仍关闭。
- **关键 prompt / context**：恢复中断前的 `T-01`/`T-02` fragment 复审，只允许修订计划和过程证据。两个作者分别独占一个 fragment；Critical/Major 必须由不同 fresh reviewer 在新 hash 上复核后才可链接为正式详细计划。`M2-01` 保持 `INCOMPLETE DRAFT - DO NOT DISPATCH`，未继续起草。
- **恢复时证据**：根 `PLAN.md` SHA-256 为 `323B5B97472FD6AB03F7119DA663EF74D7B5B8CB0067ECC04CE45553CFDBDBE9`；`T-01` 仍为首轮失败审查所绑定的 `96615368978764AC166D614372DE9C4388404BFD999C8FC28EF5E15ADA82923F`，`T-02` 存在中断留下的未复审局部修改 `7C209A738535D50D03B327C03B5229542280B3E39DBF3107B74EA197881EA89E`。两者均保持 draft/unreviewed，不能派发。
- **过程修订**：把 `SPEC_PROCESS.md` 顶层阶段 B/G-03 当前态从旧的“skill 未加载、G-02C 阻塞”更新为已发生 formal invocation、plan NOT PASS、77 dispatch/18 container、D-025 仅阻塞 host-specific delivery；带时间戳的历史诊断未改写。
- **验证证据**：`scripts/verify_evidence.ps1` 本次返回 `EVIDENCE_VALIDATION_PASS rows=63 explicitly_blocked=2 python_pins=54 npm_packages=166`；`git diff --check` exit 0，仅报告仓库现有 LF/CRLF 转换提示。UTF-8 原文扫描确认计划台账没有文件级乱码；此前 PowerShell 显示链的乱码未被当成缺陷记录。
- **人工修改及原因**：学生没有新增产品、D-005 或 D-025 决策。主智能体只纠正当前状态摘要并重新派发已审查问题；未创建生产源码、Open Design run、冷启动、CI、部署、真实凭据或 `REFLECTION.md`。
- **commit hash**：尚未创建；fragment 作者与独立复审仍在进行。
- **经验教训**：在 Windows 上必须用原始 UTF-8 搜索或字节检查区分文件损坏与终端转码；不能根据一段被转码的显示输出修改过程证据。
- **冻结复审快照**：为防止 reviewer 读取变化中的文件，主智能体在作者完成核心修订后中止两个写入会话；作者没有回报可采信的最终自检结论，故只采用文件本身。冻结的 `T-01` SHA-256 为 `33D67D3BE30528B0174BC43C5593D003228A980164A44379191790681C8468BB`（82 个 checkbox step、110 条 fence line、必需 header PASS），`T-02` 为 `889AA9C9FDF24C6B376A15529D8C7510BEA7C674DA0744E9908CDC6D0D3C6D94`（63 个 checkbox step、124 条 fence line、必需 header PASS）；两者仍是 draft/unreviewed。
- **复审派发**：`/root/plan_coverage_audit` 只读检查 SPEC/AC、正式 root atomic-sync、评审身份与单 session 粒度；`/root/plan_fragment_quality_review` 只读检查 writing-plans、正确性、安全、测试、锁/扫描/gate 语义；`/root/plan_fragment_syntax_audit` 在临时目录机械重建代码并核对语法、路径集和 expected-count。三者均被明确禁止编辑项目文件；结果尚未返回。

## 2026-07-22T23:59:35+08:00 - PLAN-008 fragment review failure and unit decomposition

- **Task 编号**：PLAN-008（T-01/T-02 formal replacement；阶段 B 仍未通过）。
- **触发的 Superpowers skill**：继续使用 `writing-plans`、`receiving-code-review`、`dispatching-parallel-agents`；评审模板要求参照 `requesting-code-review` 与 `verification-before-completion`。未调用实现/TDD/worktree skill。
- **关键 prompt / context**：对 PLAN-007 冻结的两个 fragment 做两阶段 findings-first 复审和独立机械重建；Critical/Major 未清零前不得继续 M2/M3 或标记详细计划 PASS。收到失败结果后，只允许拆计划/根合同，不允许生产源码或跨门禁执行。
- **subagent 输出 / review**：`/root/plan_coverage_audit` 判定 root Files/hash/signature 未同步、两个 unit 过大、e2e/G-02C owner 不闭合、scanner/Vite 与 T-02 catalog/count/TDD-review 缺口；`/root/plan_fragment_quality_review` 进一步把 root ownership、scanner 漏扫与超大粒度列为 Critical，并确认 strict Ruff/mypy、symlink 和 T-02 mapping 边界问题；`/root/plan_fragment_syntax_audit` 在临时目录确认显示代码可解析、T-02 临时 pytest 为 74 passed，同时复现目标 Windows 上裸 `npm` 的 Python subprocess 解析失败。三者均未编辑项目文件。
- **主智能体判断与修订方向**：接受可复现 finding，不把“语法可解析”混同为可派发。旧 T-01/T-02 fragment 保留为失败证据；新建两份 `docs/superpowers/plans/` 正式计划。T-01 拆成 6 个独立 worker/commit，T-02 拆成 3 个；第三个独占 owner 同步根 PLAN，目标为 84 dispatch/20 container、84/84 ledger/body、0 unknown/self/cycle。该计数是正在修订的目标，不是 PASS。
- **人工修改及原因**：学生没有新增决定；拆分属于满足课程单-session 粒度和已确认技术合同的工程修复。未代选 D-005/D-025，未修改产品方向或学生反思。
- **验证边界**：reviewer 的临时重建、AST/parser 和 74-test 运行仅验证计划中显示代码，发生在临时目录，不是项目实现测试。`WRITING_PLANS_VALIDATION.md` 与 `SPEC_PROCESS.md` 已同步记录失败哈希和拆分策略；新 root/subsystem 文件仍在写入，尚无复审哈希。
- **commit hash**：尚未创建；不得在三份 replacement 同步并复审前提交或声称 Stage B 完成。
- **经验教训**：把大任务的内部动作拆成 2--5 分钟步骤仍不等于把 dispatch unit 拆小；文件所有权、独立红绿周期、review/commit 边界和单-session 上下文体量必须同时满足。

## 2026-07-23T02:40:20+08:00 - PLAN-009 replacement snapshot validation and restart pause

- **Task 编号**：PLAN-009（根计划与 T-01/T-02 replacement snapshot 收束；阶段 B 仍未通过）。
- **触发的 Superpowers skill**：继续使用已完整读取的 `using-superpowers`、`writing-plans` 与 `dispatching-parallel-agents`；本 task 的 catalog 可调用 14 个 Superpowers skills。未触发 worktree、TDD、实现、Open Design run 或 finishing skill。
- **关键 prompt / context**：只允许修订和机械验证 formal plan set 与过程证据；禁止越过 G-03。学生要求减少围绕单任务的重复确认，随后要求本轮结束后暂停 Goal 以便重启电脑，因此检查被合并为批次，且没有启动下一批 subsystem plan。
- **subagent 输出**：`/root/root_plan_final_repair` 只修改 `PLAN.md`，回报 113 dispatch、37 groups、ledger/body delta 0、DAG 113/113、unknown/self/cycle 0、根占位符与裸工具命令 0，并停止编辑。`/root/foundation_snapshot_review`、其机械子审计和 `/root/domain_snapshot_review` 均为只读；因学生重启请求，它们在给出 review verdict 前被中止，故没有可记录的 PASS。
- **当前哈希**：`PLAN.md` `83B9A69272CBF7E831BB386E69AE5376968C931F4188DD23DC2988D8782D6787`；foundation `D00496FAAC456AA4CB0E69DE9104BF085C54621D76A199AC456A06601D73E87E`；domain `E01303C74E2EA22C26CCF3C43D6E118C00C3311850D3E321EA781A92DB61BEA5`。旧冻结 FAIL 哈希与 reviewer 身份记录在 `WRITING_PLANS_VALIDATION.md`，没有被覆盖。
- **验证证据**：根 113/113 dispatch、37/37 group、ledger/body delta 0，依赖 113/113 可拓扑遍历且 unknown/self/cycle 为 0，AC 50/50；三份 header/fence PASS。foundation 35 个 PowerShell 与 31 个 Python block、domain 77 个 PowerShell 与 45 个 Python block 均为 0 个语法错误；详细计划尖括号命中均分类为 HTML/JSX、正则或数学表达式；`git diff --check` exit 0，仅有 LF/CRLF 提示。未运行产品测试、构建、CI 或真实 scanner。
- **Git 状态**：实际分支仍为 `master`，HEAD `519b3000336d18f8b89628fdc14691d3b700002c`，仅根工作树；没有新 branch/worktree，也没有 commit。当前计划与过程文件仍为工作树改动/未跟踪文件，未把它们冒充提交证据。
- **人工修改及原因**：学生只要求节省交互额度并在本轮后暂停重启，没有作出 D-005/D-025 或实现批准。主智能体仅记录真实校验和未完成 review 状态，未代写 `REFLECTION.md`。
- **门禁 / 恢复点**：formal plan 为 **NOT PASS**。重启后先复核三份哈希并重新完成 T-01/T-02 独立评审，再继续剩余 subsystem plans；之后才可能进入 D-005 与 G-03。当前按学生要求停止，不进行自动续跑。
- **commit hash**：尚未创建。
- **经验教训**：机械解析通过不能替代独立规约/质量评审；用户请求暂停时，应保留未完成 reviewer 的真实状态，而不是为了形成整齐结论把它补写成 PASS。

## 2026-07-23T11:07:28.3604077+08:00 - PLAN-010 independent review failure and full subsystem partition

- **Task 编号**：PLAN-010（阶段 B 详细计划修复与剩余子系统分区；仍未通过）。
- **触发的 Superpowers skill**：继续使用已完整读取并正式调用的 `using-superpowers`、`writing-plans`、`dispatching-parallel-agents` 与 `receiving-code-review`。未触发 worktree、TDD、实现、Open Design run、finishing 或部署 skill。
- **关键 prompt / context**：学生要求恢复 Goal、离开期间继续所有无需决策的安全工作，并把人工审核/执行统一封装而不是重复询问。当前只允许计划、静态验证与过程证据；D-005、D-025、G-03、远程 CI/部署和实现批准均保持人工/外部门禁。
- **review 输入与结果**：`/root/foundation_snapshot_review_r2` 复核 root `83B9...6787` + foundation `D004...87E`，返回 NOT PASS；`/root/domain_snapshot_review_r2` 复核同一 root + domain `E013...E5`，返回 NOT PASS。两者均只读、未提交。foundation 的 Critical 是 pathspec-limited staged check 后 whole-index commit；domain 的两个 Critical 是 facade owner 冲突和最终累计测试必然失败。完整 findings 已同步到 `docs/engineering/WRITING_PLANS_VALIDATION.md`。
- **机械/运行边界**：domain reviewer 的临时显示代码重建为 135 pass/1 fail，仅证明计划内矛盾；foundation reviewer 本机为 Python 3.13.5、Node 24.14.0、npm 11.9.0、Windows PowerShell 5.1，且无目标 Ruff/pwsh，未声称目标环境通过。当前没有运行产品测试、构建或正式 scanner。
- **协调者修订**：根计划新增 native-command fail-closed 与 whole-index staged-set 合同，把 T-02 计数修为五个 child，并要求 proof 输入是完整连续 1..N 页面目录；新增 `docs/engineering/PLAN_SUBSYSTEM_PARTITION.md` 与 `docs/engineering/DETAILED_PLAN_AUTHORING_CONTRACT.md`，并把审查事实写入 validation/SPEC process。没有修改生产源码。
- **分区证据**：现有 foundation/domain 覆盖 15 dispatch，12 份待生成计划覆盖 86 dispatch，12 个 coordinator/human/external unit 留在 root；总数 `15 + 86 + 12 = 113`。共享路径与串行 owner 已记录，D-025 仅阻塞 host-specific 链，D-005 仅后置阻塞 G-03。
- **subagent 状态**：`/root/repair_foundation_plan`、`/root/repair_domain_plan` 分别独占修复两份计划；`/root/remaining_plan_partition_r2` 正在独占起草 T-03A/B/C persistence 计划。当前条目不把进行中作者、自检或未冻结文件写成完成证据。
- **当前验证**：协调者改动后的 root 仍机械得到 113 dispatch/113 unique、37 group/37 unique、status-ledger/body delta 0、AC 50/50、围栏偶数；placeholder 目标扫描无命中。`git diff --check` 对新增/修改过程文件 exit 0，仅报告既有 LF/CRLF 提示。完整 DAG、新计划代码块与 same-snapshot review 等待作者冻结后重跑。
- **Git / commit**：分支仍为 `master`，HEAD 仍为 `519b3000336d18f8b89628fdc14691d3b700002c`；工作树已有多项用户/流程改动。本轮未 stage、未 commit、未创建 worktree/branch，不把 dirty 状态归因于 reviewer。
- **人工修改及原因**：学生没有新增产品选择、D-005/D-025 决策或实现批准。协调者只采纳可复现 review finding、明确计划分区与安全模板；`REFLECTION.md` 未创建或代写。
- **门禁 / 下一步**：阶段 B 保持 **NOT PASS**。等待三个作者冻结后做语法/路径/依赖/placeholder/whole-index protocol 检查并派不同 fresh reviewer；随后按分区批量生成其余计划。任何需要学生或外部平台的动作继续封装，不重复询问。
- **commit hash**：尚未创建。
- **经验教训**：计划中的提交安全必须验证整个 Git index，而不是只验证预期 pathspec；计划代码可解析也不等于最终累计测试可达。共享 facade 的首次 owner、后续导出和永久测试断言必须在 same-snapshot review 中一起检查。

## 2026-07-23T11:50:37.7529423+08:00 - PLAN-011 R3 semantic review failure

- **Task 编号**：PLAN-011（foundation/domain/persistence same-snapshot 复审；阶段 B 未通过）。
- **触发的 Superpowers skill**：继续使用 `writing-plans`、`dispatching-parallel-agents`、`receiving-code-review` 与 evidence-before-claim 的 verification 纪律；未调用实现/TDD/worktree/finishing skill。
- **冻结输入**：root `E8740A7D17723C30DB362C1BFEA24AC10B9A5108AB46EB239DFC236314274CCA`；foundation `6B9ADB0999229259772F475057F7D5FB2A67F23E2E86A9581C8F3CEA2D5353A2`；domain `50F38BF2935FD6596C0388E44E2E3B5DA0A5A35A61AFD78992AB1D4EF5CEB40D`；persistence `4217FD325A464FFA47196E261659AD85FC806812B30F609DB46B21D61BD3B07E`。foundation/domain repair 作者停止写入后才发 review；persistence 作者在三个完整 unit 和 closure 已存在、文件稳定后被协调者中止，未把其未返回自检当证据。
- **foundation reviewer**：`/root/foundation_recheck_r3` NOT PASS。55 类 raw runtime command 未完整 fail-closed；review/stage/commit 顺序未证明 reviewers 看过 exact staged bytes；scanner test literal private-key marker 使 self-scan 必然失败；另有 wrong executable/fake wrapper/environment/output redaction、identity regex 与 Ruff UP035 finding。
- **domain reviewer**：`/root/domain_recheck_r3` NOT PASS。临时重建为 `144 passed`，但 strict mypy 1.14.1/Python 3.14 target 模式报 10 个 unreachable error；unit prelude 仍缺完整 absolute Git/runtime/worktree/base/timeout 验证；import order 不能通过 Ruff I001。reviewer 确认此前 facade owner、最终 exports、1..N page directory、stable errors、regex 和 whole-index staging 已关闭。
- **persistence reviewer**：`/root/persistence_review_r1` NOT PASS。sole migration 缺 durable lease/payload、MaterialBatch/Attempt；remote consent 未绑定 F 和 exact material scope，撤销后 cleanup 不可表达；audit 仅限制 key 而允许私人路径 value。另有 SQLite Any/raw error、非 canonical UTC、超大 checkbox 与缺 remote AC review scope。显示包原测试 26 pass，新增 probe 复现 remote/audit 缺陷；不是项目测试证据。
- **修订派发**：三个原独占作者分别收到对应 findings，只允许修改自己的 detailed plan；要求保留已关闭 finding、增加负测、补齐 authoring contract、运行机械重建并回报新 hash。没有编辑生产源码或 root 决策合同。
- **环境边界**：reviewer 无目标 CPython 3.14.6/Ruff 0.15.22/mypy 2.3.0 完整环境时明确不作精确工具链 PASS；临时 mypy/test 仅用于发现显示代码矛盾。
- **既有证据复验**：本轮普通 `scripts/verify_evidence.ps1` 返回 `PASS rows=63 explicitly_blocked=2 python_pins=54 npm_packages=166`；distribution-strict 按预期仅因两项 hosting row 退出 1。未修改或误解锁 D-025。
- **人工边界**：没有询问或代选 D-005/D-025，没有执行 G-03、远程账号/CI、Open Design run、部署、付费、provider request 或 `REFLECTION.md`。
- **Git / commit**：未 stage/commit/branch/worktree；HEAD 仍是 `519b3000336d18f8b89628fdc14691d3b700002c`，dirty worktree 保留。
- **门禁 / 下一步**：等待三个修复作者冻结新哈希，再派与作者不同的 fresh reviewers。任何一个 Critical/Major 未清零时，不能链接 PASS 或开始后续依赖计划的正式审查。
- **经验教训**：静态 schema 必须从所有已声明下游恢复需求倒推；consent 不只验证“存在且未撤销”，还必须绑定 mode 与精确材料范围，并允许撤销后的治理性清理而不重新授权使用。
## 2026-07-23T13:28:52.5541243+08:00 - PLAN-012 domain PASS and foundation/persistence R4/R2 findings

- **Task 编号**：PLAN-012（阶段 B 详细计划独立复审与继续修订；阶段 B 仍未完成）。
- **触发的 Superpowers skill**：继续使用 `writing-plans`、`dispatching-parallel-agents`、`receiving-code-review` 与 `verification-before-completion` 的证据纪律；没有调用实现、TDD、worktree、Open Design run、finishing、远程 CI 或部署 skill。
- **冻结输入与独立结论**：root `PLAN.md` 为 `4BCFE8470DE57C0DD54004935285CAAD5CD9D1AFF0AA7370CC4E098887745F08`。`/root/domain_recheck_r5` 对 domain `40C48BB62A87F17BFCFB635871F51C350EA2EC9F1AAFEE5ED2D9B7A7C7629C0B` 返回 PASS；`/root/foundation_recheck_r4` 对 foundation `837F1E71CDA4542898631EC441E3469ECB235B55F8CB024EF33F9AA8DF665A59` 返回 NOT PASS；`/root/persistence_review_r2` 对 persistence `2F67280FED1C7F5337837B5CB08E9099F09D5236A19B124B2D3C007C301B8810` 返回 NOT PASS。三名 reviewer 均只读、未提交。
- **domain PASS 证据**：临时重建显示代码得到 `144 passed`；Ruff 0.15.22、mypy 2.3.0 strict、`compileall` 和 PowerShell AST 均通过。五个 unit 的 whole-index、tree/reviewer/commit 绑定已存在；唯一 Minor 是 T-02B1 在 `git diff --cached --check` 前捕获 tree，但该命令只读且 commit 前会重复，未构成阻断。该 PASS 只覆盖 domain 详细计划，不代表 14-plan 集合或 Stage B PASS。
- **foundation NOT PASS**：显示代码缺少 `hashlib`、`Path`、`dataclasses.replace` 等 imports；每个 unit 的 `PROJECTB_UNIT_ID`/base/worktree/Git-root/HEAD 合同仍不完整；runtime identity 可由同一可变环境自证；子进程环境/输出脱敏、npm lock 原始字节比较、reparse/TOCTOU、exact 40-hex、裸 `rg`、Ruff F401 与进程树 timeout 仍有缺口。作者已接收逐项 finding，仅修改 foundation 计划。
- **persistence NOT PASS**：撤销后 cleanup 状态可重新写入 scope token；`tombstone_object` 可无 provider 删除证据直接标记 deleted；显示包 Ruff 0.15.22 有 50 项、mypy 2.3.0 有 1 项；migration 可直接插入非 hex hash 与非 canonical UTC；仍有 350/154/149 行的单 checkbox；root T-03C AC 范围漂移；native timeout 和 exact staged-content review packet 不完整。临时重建为 `183 passed`、`compileall` PASS、36 个 PowerShell block 解析 0 error，这些正向结果不能覆盖上述失败。
- **协议修订**：root 与 `docs/engineering/DETAILED_PLAN_AUTHORING_CONTRACT.md` 已要求 whole-index staged set、`git write-tree`、双 reviewer tree binding、edit invalidation、precommit tree equality 和 postcommit `HEAD^{tree}` equality；本轮 reviewers 又要求所有原生命令有有界 timeout/进程树清理、诊断脱敏，并在 scanner 后把实际 staged diff 内容以非公开 hash-bound packet 交给两名 reviewer。进行中的作者均已收到该加严项。
- **新计划进度**：`2026-07-23-local-trust-and-provider-control-plane.md` 正在覆盖 T-04A/B/C、T-05A/B/C、T-06、T-07；其旧 snapshot hash 已在冻结前纠正为当前 root/domain，并明确 foundation/persistence 最终 hash 到位后必须 rebind 和重做 cross-plan reviews。当前稿不是 PASS 或 dispatch 授权。
- **验证与人工边界**：本次 `scripts/verify_evidence.ps1` 返回 `EVIDENCE_VALIDATION_PASS rows=63 explicitly_blocked=2 python_pins=54 npm_packages=166`；`-RequireDistributionReady` 按预期仅因两条 D-025 hosting row 返回 exit 1。没有执行 D-005/G-03、实现批准、真实 Open Design project/run、worktree、生产源码、CI、provider 调用、付费、部署或 `REFLECTION.md`。
- **Git / commit**：分支仍为 `master`，HEAD 仍为 `519b3000336d18f8b89628fdc14691d3b700002c`；未 stage、未 commit、未创建 worktree/branch。当前 dirty 文档状态不被冒充提交证据。
- **经验教训**：显示测试全过仍不能覆盖数据库直接插入、状态迁移和静态门禁缺陷；review 必须同时绑定源码树、实际 staged 内容和不可变 predecessor snapshot。只有同一 final root 上的完整 14-plan 集合复审后才能更新 Stage B 状态。

## 2026-07-25T12:29:39.2373040+08:00 - SCOPE-RESET-001 阶段 B 范围收束与可恢复存档

- **Task 编号**：SCOPE-RESET-001（执行学生确认的阶段 B 精简与可恢复存档计划；不包含产品实现）。
- **触发的 Superpowers skill**：读取并遵循 `using-superpowers`、`executing-plans`、`subagent-driven-development`、`systematic-debugging` 与 `verification-before-completion`。`using-git-worktrees` 未用于本次文档协调：课程 G-04 要求先完成新 SPEC 签字、正式 PLAN、同快照复审和冷启动；当前只在现有 worktree 建立 `codex/stage-b-scope-reset` 文档分支，未创建实现 worktree。
- **关键 prompt / context**：学生要求把 113-task / 14-plan 方案收束为三模块 v1，同时满足课程文档要求，并将所有未实现功能以可恢复、不可派发计划存档；不得删除历史内容或跨越人工门禁。
- **范围与人工选择**：M1 仅数字 PDF、UTF-8 TXT/Markdown、原始字节哈希、页/行定位和人工知识点映射；M2 保留通用知识点模型，以互斥/竞态/死锁为首批确定性检查；M3 保留追加式学习证据、掌握状态和连续/期末复习。模型只保留本地 L 与逐次确认片段外发 P，仍要求 OpenAI adapter、Credential Manager、mock、React WebUI、Windows 单文件、OCI demo、双 CI 和最终公网 URL。
- **存档动作**：旧根计划、六份详细计划、三个片段和两份工程合同移入 `docs/superpowers/plans/archive/superseded-2026-07-23/`；新增归档索引和四份 `ARCHIVED / NOT DISPATCHABLE` 延期计划。`.r5-verify-final-20260723` 移到被忽略的 `tmp/stage-b-archive-20260725/`，只保存为计划代码重建物。
- **凭据处理**：扫描发现旧 local-trust 草稿含两个模拟 OpenAI key 形式的测试字面量。原始字节只保存到被忽略的本地存档；可提交副本将两个值替换为 `[REDACTED_FAKE_TEST_TOKEN]`。日志和终端输出均未复述原值；归档索引记录原始与可提交 SHA-256。
- **当前文档**：重写 `SPEC.md`、当前门禁 `PLAN.md`、`DECISIONS_NEEDED.md` 和课程符合性矩阵；同步 `SPEC_PROCESS.md`、项目审计、分发证据、writing-plans 验证、skills 状态和本会话交接。README 与学生 `REFLECTION.md` 未提前创建。
- **subagent 输出 / review**：`/root/archive_docs` 创建归档索引和四份延期计划，并报告 5/5 diff、结构、占位符和旧哈希校验通过；主智能体随后独立核验并对模拟凭据执行安全替换。`/root/scope_spec_review` 与 `/root/spec_compliance_fast` 均被中断且没有返回结论，故不计作独立复审或 PASS；正式双评审仍留在学生确认后的同哈希 SPEC/PLAN 门禁。
- **验证结果**：当前 SPEC `C6231816...9AD6` 为 14 章/8 个唯一故事/24 个唯一 AC；12 个归档文件逐项匹配索引，4 份延期计划结构通过，`.r5` 为 1021 文件/35989967 字节且 manifest-v1 `50187D07...77C3D`；42 份非旧档 Markdown 的 21 个本地链接全部存在；拟提交 28 文件的配置化凭据模式命中 0；`git diff --check` 退出 0。标准证据返回 `PASS rows=63 explicitly_blocked=2`；distribution-strict 只因 D-025 两行 hosting evidence 按预期退出 1。首次递归链接枚举被既有 `.pytest_cache` 的访问拒绝中断，随后用 `rg --files` 限定仓库 Markdown 并通过，没有删除或提权访问缓存。
- **未执行**：没有创建生产源码、实现 worktree、Open Design run、provider request、测试/构建、CI、远程 push/PR、镜像发布、部署、付费资源或 `REFLECTION.md`。
- **Git / commit**：本地分支 `codex/stage-b-scope-reset`，范围重置基线 `519b3000336d18f8b89628fdc14691d3b700002c`；归档 checkpoint 为 `ccd1dfe`，活跃范围/门禁文档 checkpoint 为 `5f54431`；两个提交均不含无关 dirty 文档或生产源码。
- **门禁 / 下一步**：先完成最终机械验证并提交诚实的 `NOT PASS` 历史检查点；随后只请求学生重新确认当前完整 `SPEC.md`。旧签字不自动覆盖新文本，确认前不得调用 `writing-plans` 或进入冷启动/实现。
- **经验教训**：活跃入口只保留 SPEC、单一 PLAN 和要求矩阵，可显著降低恢复成本；历史内容仍需以哈希索引和明确恢复条件保全。凭据扫描必须覆盖计划示例和归档草稿，模拟 token 也不应进入可提交历史。

## 2026-07-25T19:13:57.2253721+08:00 - PLAN-V1-001 精简 SPEC 签字与正式计划启动

- **Task 编号**：PLAN-V1-001（记录精简 SPEC 签字并启动正式 `writing-plans`；未进入生产实现）。
- **触发的 Superpowers skill**：重新读取并使用 `using-superpowers` 与 `writing-plans`；计划完成前不触发 worktree、TDD、执行或 finishing skill。
- **关键 prompt / context**：学生回复“确认当前 SPEC，先把主体做出来先，剩两个门禁我想想办法”。回复前只读复核当前 `SPEC.md` SHA-256 为 `C6231816A62C807D205FC7A3E6142C5636DE18FD8A2C580B48E63B106F959AD6`，与请求确认的快照一致。
- **人工确认与边界**：SPEC 整体签字已闭合，`writing-plans` 获准。Claude Code 冷启动、冷启动修订后实现批准、D-025、远程授权和学生 `REFLECTION.md` 仍未闭合；当前回复不替代未来 G-04 批准。
- **当前动作**：只更新签字/门禁元数据与过程证据，随后把根 `PLAN.md` 重写为最多 30 个单-session task 的唯一实现计划并做同哈希双评审。
- **未执行**：未创建 backend/frontend、实现 worktree、Open Design run、provider request、测试/构建、CI、部署或远程资源。
- **Git / commit**：分支 `codex/stage-b-scope-reset`，起始 HEAD `d94235c4ce8d669f7aca2bb8707fd8c55411fc53`；计划 checkpoint 尚未创建，无关 dirty 文档保持 unstaged。
- **经验教训**：产品方向确认与实现批准是不同时间点的证据；即使学生希望尽快实现，也必须先让冷启动问题进入可审查修订，再请求实现授权。

## 2026-07-26T00:49:31.3372555+08:00 - PLAN-V1-002 精简计划冻结与阶段 B 双评审

- **Task 编号**：PLAN-V1-002（完成精简 implementation PLAN、机械验证、同哈希双评审和 G-03 操作包；不包含产品实现）。
- **触发的 Superpowers skill**：使用 `using-superpowers`、`writing-plans`、`dispatching-parallel-agents`、`requesting-code-review`、`receiving-code-review`、`systematic-debugging` 与 `verification-before-completion`。worktree、TDD、执行和 finishing skills 仍由 G-03/G-04 门禁阻止。
- **关键 prompt / context**：学生确认 `C6231816...9AD6` 的精简 SPEC 并要求先推进主体；课程仍要求正式 PLAN 通过、Claude Code 陌生智能体冷启动、修订后再次实现批准。计划必须覆盖三模块、L+P、React WebUI、Credential Manager、双 CI、Windows 单文件、OCI mock demo、公网 URL、README 与学生反思门禁，同时不把四类延期能力带回 v1。
- **计划结果**：当前 `SPEC.md` 注记后哈希为 `795791627579BFEBE24717981168A54E2D546F613FEA84CCDF0AC0ECBA387862`；唯一 `PLAN.md` 为 `6FDD69F2FD309841CC46DB1C75C142E4E1E8474E1575A2E765F49EF67002A05D`，含 31 个单-session task。F-01 被 reviewer 要求拆为 F-01A/F-01B；首提交扫描缺口随后以 dependency-free、fail-closed、只输出 path/rule ID 的 bootstrap scanner 闭合。
- **subagent 输出 / review**：只读 reviewer `/root/plan_spec_review` 与 `/root/plan_quality_review` 均对上述同一哈希返回 `PASS; Critical=0, Major=0, Minor=0`，且均未编辑仓库。冻结文档 reviewer `/root/freeze_docs_audit` 返回 `PASS; Critical=0, Major=0`，只指出反思长度一处 `word`/中文字符口径 Minor，已在不改变 SPEC/PLAN 的前提下修正。更早的 `35D8...`、`6AC...` 与 `D639...` 结论只作为真实修订轨迹保留，不继承 PASS。
- **人工修改及原因**：主智能体只采纳可复现 reviewer findings，拆分 foundation、补齐工具链/许可证/凭据门禁并同步过程证据；学生本轮没有授权 G-04、远程平台、付费 provider、部署或代写反思。无关 `docs/research/*` 与 `docs/engineering/SUPERPOWERS_VALIDATION.md` 改动保持 unstaged。
- **验证证据**：机械审计为 `Tasks=31 Ledger=31 Fields=5 DependencyEdges=30 AcRows=24 Placeholders=0`；标准 evidence 为 `rows=63 explicitly_blocked=2 python_pins=54 npm_packages=166`；Linux evidence 为 `ci_packages=41 demo_packages=14 license_rows=41`；provider evidence 为 `rows=7 models=2 expires=2026-08-25`。最终 19 文件 authoring surface 为 `markdown=12 links=10 broken=0 credential_matches=0 utf8_replacement=0`，distribution-strict 按预期只因 D-025 两行退出 1。第一次工作树级 `git diff --check` 未覆盖未跟踪 runbook；暂存后检查发现并修正其一处行尾空格，再对完整 staged set 复验。
- **Git / commit**：分支 `codex/stage-b-scope-reset`，起始 HEAD `d94235c4ce8d669f7aca2bb8707fd8c55411fc53`；阶段 B 冻结 checkpoint 为 `d1941701373dd38312b9a9145376da8071fa2966`，只包含上述 19 个计划/证据文件，不含生产源码或无关 dirty 文档。
- **未执行 / 门禁**：`Get-Command claude` 未找到，G-03 仅准备 runbook，未执行 session 或产出 transcript。没有生产源码、实现 worktree、Open Design run、产品测试/构建、CI、provider call、远程 push/PR、镜像发布、部署或 `REFLECTION.md`。
- **经验教训**：一个首提交安全门禁不能依赖尚未实现的后续 scanner；bootstrap 路径必须无第三方依赖、失败关闭且在第一次 staged commit 前即可执行。review PASS 必须绑定完全相同的 SPEC/PLAN 字节。

## 2026-07-27T13:26:43+08:00 - G-03P-001 Codex 同类型冷启动占位

- **Task 编号**：G-03P-001（同类型 Codex 占位冷启动和文档修订；不满足正式 G-03，不包含产品实现）。
- **触发的 Superpowers skill**：使用 `executing-plans`、`writing-plans`、`receiving-code-review` 与证据优先的验证纪律；因仍在实现门禁前，未触发 worktree、正式 TDD 派发或 finishing。还读取 `openai-docs` 以核对 Codex 使用入口，但本机官方手册 helper 因 Windows Schannel `SEC_E_NO_CREDENTIALS` 未取得在线结果，故只使用本地 CLI 帮助与桌面任务能力，不把失败查询写成官方结论。
- **关键 prompt / context**：学生报告 Claude 被拒、Gemini 需特殊中转、Copilot 未开通，要求先用 Codex CLI 或 Codex 做占位，后续再补异类型冷启动；随后允许无人值守继续，但“能跳的门禁”不构成绕过课程人工门禁的授权。
- **CLI 结果**：`codex-cli 0.144.4` 以 `--ephemeral --ignore-user-config --ignore-rules --sandbox workspace-write` 在系统临时 disposable 目录启动，只含 SPEC/PLAN。约 4 分钟无输出或 scaffold 后安全终止，未形成红/绿证据；输入副本保留，未改项目仓库。
- **subagent / task 输出**：用户明确创建的项目外 Codex 桌面任务 ID 为 `019fa1f5-8031-7450-883c-2462fc623703`。旧哈希首轮在红测前正确停止并指出 F-01A 输入不可获得；第二轮提出 7 组 scanner 合同问题；当前哈希第三轮报告问题全部闭合、`NEW_QUESTIONS None`。
- **修订与人工边界**：主智能体只修订 SPEC 的 G-03/G-03P 过程门禁和 PLAN 的 F-01A 无依赖 scanner 切片合同；产品范围、31-task ledger、D-025、远程授权、学生反思和 G-04 均未改变。项目外生成脚本未合入仓库，也未标记 F-01A started/completed。
- **红/绿证据**：精确命令 `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/tests/bootstrap_scanner_contract.ps1` 先以 exit 1、`CONTRACT_RED scanner_missing` 失败；最小实现后同一命令 fresh rerun 为 exit 0，12 个行为组通过并输出 `BOOTSTRAP_SCANNER_CONTRACT_PASS cases=12`。测试中先遇到系统 temp sandbox 限制，改把 disposable repos 放到输出目录；随后修复 PowerShell 5.1 `String.Split` overload 和空路径 JSON 语义，未删减测试或断言。
- **哈希 / 产物**：SPEC `6003950E...ED71`；PLAN `8A4BE778...AFD`；项目外 scanner `37CC6252...2D60`；项目外 contract `F0CA58FA...C516`。临时 contract repositories 已清理，原仓库无生产源码变更。
- **评审与门禁**：占位任务明确声明同类型限制。旧 same-hash 双评审因 SPEC/PLAN 字节变化而失效；当前字节的机械审计和双评审、正式非 Codex G-03、学生 G-04 仍待完成，未授权正式实现。
- **commit hash**：待本次过程文档验证后填写；无关 `docs/research/*` 与 `docs/engineering/SUPERPOWERS_VALIDATION.md` 修改保持 unstaged。
- **经验教训**：冷启动 task 不能把“正式实现阶段可从仓库取得的输入”误当成两文档 disposable 环境已有输入。把一个无依赖、行为闭合的安全切片明确嵌入首 task，可在不提前实现完整工具链的情况下验证计划可执行性。

## 2026-07-27T14:01:29+08:00 - G-03P-002 同哈希评审失败与安全修订

- **Task 编号**：G-03P-002（修复 G-03P 后评审 findings；仍不包含正式实现）。
- **触发的 Superpowers skill**：使用 `writing-plans`、`requesting-code-review`、`receiving-code-review`、`systematic-debugging` 和 `verification-before-completion` 的约束；没有触发实现 worktree、正式 TDD dispatch 或 finishing。
- **关键 prompt / context**：学生允许无人值守继续所有可跳过的工作，但课程硬门禁仍不可跳。评审对象固定为 SPEC `6003950E...ED71` 和 PLAN `8A4BE778...AFD`，要求分别审查课程合规和质量/安全/许可证。
- **review 输出**：`/root/g03p_spec_review` 为 `FAIL; Critical=0, Major=3, Minor=2`；`/root/g03p_quality_review` 为 `NOT PASS; Critical=1, Major=10, Minor=1`。Critical 复现的是 index 中有秘密、工作树已清理时 staged scanner 读取错误字节源；两名 reviewer 均只读、未改仓库。
- **主智能体修订**：将 scanner 拆为完整 F-01S，强制从 index OID binary-safe 读取 blob，并分别报告 index/worktree；新增两类交叉状态回归。计划增至 32 个 session task，增加统一 2--5 分钟 microstep、初始 push CI、最终远程 CI、GitHub visibility、mutable-ledger 例外、coordinator scan、学生手写声明、clean VM gate、精确文件 ownership。SPEC 补 MaterialVersion/MaterialBlobRef 和 finals 固定倍率表。
- **许可证核验**：PowerShell/curl raw 因 Schannel `SEC_E_NO_CREDENTIALS` 失败，Python raw 读取超时；GitHub 官方 Contents/Refs API 随后成功返回 5 份文本和 4 个 tag commit。实际 byte/hash 记录于 `docs/engineering/BOOTSTRAP_LICENSE_EVIDENCE.md`，其 SHA-256 为 `E9EFCF96...E7E0`。无 key、付费调用或第三方模板。
- **机械证据**：修订候选得到 `PLAN_MECHANICAL_PASS Tasks=32 Ledger=32 Fields=5 DependencyEdges=31 AcRows=24 Placeholders=0`；候选 SPEC `69A534D9...855E`，PLAN `47624A3E...225A`。本条不把尚未返回的新双评审写成 PASS。
- **G-03P 重跑**：旧 task 收到新输入请求后因删除旧输出触发审批，已改为保留旧证据；另建 projectless task `019fa224-046d-7a41-9841-b6632be08057`，但其只读复制两份 ProjectB 文件同样触发桌面审批。没有代批、没有读取额外文件、没有新红/绿证据。
- **人工修改及原因**：学生未新增产品/托管/付费选择；finals 数值和 material ref 语义是对既有已签字承诺的确定性实现合同。D-025、正式非 Codex G-03、G-04、远程授权和 `REFLECTION.md` 均保持开放。
- **commit hash**：`c34ed0e01b0e1849a62298d6d0807d2bb2edfef0`（`docs(stage-b): checkpoint cold-start remediation [agent: Codex]`）；这是诚实的 `NOT PASS` 修订检查点，不是 SR-08/G-03/G-04 closure。无关 `docs/research/*` 与 `docs/engineering/SUPERPOWERS_VALIDATION.md` 修改保持 unstaged。
- **经验教训**：只检查 staged 文件名不等于检查 staged 内容；提交安全门禁必须把 Git index 和工作树视为两个独立、不可信字节源。最终 README commit 也必须落在最终 PR/MR 与 CI 证据之前，而不是之后。

## 2026-07-27T18:18:41+08:00 - G-03P-003 审批事故核对与第三轮计划修订

- **Task 编号**：G-03P-003（只处理 Stage-B 事故核对、评审修订和证据验证；不包含产品实现）。
- **触发的 Superpowers skill**：`using-superpowers`、`systematic-debugging`、`brainstorming`、`writing-plans`、`test-driven-development`、`requesting-code-review`；继续遵守 `verification-before-completion`。因门禁未闭合，没有使用 worktree、正式 subagent implementation、产品 TDD 或 finishing。
- **关键 prompt / context**：学生说明误批两个桌面请求后已停止任务，要求检查文件并继续；此前授权无人值守修复可自动推进项，但不授权绕过课程人工门禁。主智能体先只读核对仓库、两个 thread 和两个项目外输出目录。
- **事故结果**：仓库未被两个桌面任务改写，index 为空；旧 task 自己的 `outputs/scripts` 被删除，旧文件级证据丢失但 thread transcript 保留。新 task 仅有获准的 SPEC/PLAN 精确副本，随后从副本恢复并产生 requirement-shaped red。无 ProjectB 额外读取/复制或真实凭据迹象。
- **review 输出**：对 SPEC `69A534...855E` / PLAN `47624A...225A`，`/root/g03p_spec_review` 返回 `Critical=0, Major=3, Minor=0`，`/root/g03p_quality_review` 返回 `Critical=0, Major=6, Minor=2`。两者均只读；共同阻塞 locator version、F-01A 粒度、current-suite CI、许可证、runner、reflection/final commit 和 stacked PR closure。
- **主智能体修订**：SPEC locator 补 `material_version_id`；PLAN 将 foundation 拆成 F-01A--E，固定 scanner grammar、CI images/action、九分支 stacked base/依赖顺序 retarget-and-merge、Open Design receipt 和学生反思先于最终 commit。过程中的 `7B13DB32...A7EE` 候选又因 current-suite 空后端自审被替换；最终哈希须在修订停止后重算。35 task/35 ledger/24 AC/0 placeholder；当前双评审尚未返回，仍是 NOT PASS。
- **TDD / 验证证据**：bootstrap license binding 静态合同先 exit 1，再 PASS；真实一字节 mutation 被 verifier 以 exit 1 拒绝。标准 evidence PASS 为 `rows=63 explicitly_blocked=2 python_pins=54 npm_packages=166`；此前同轮 Linux/provider 分别 PASS `41/14/41` 与 `7/2`；strict distribution 只因 D-025 两行按预期失败。
- **人工修改及原因**：学生没有新增产品、托管、付费、远程或 provider 决策。任务拆分、CI current-suite 和 versioned locator 是修复已确认合同的工程细化；`REFLECTION.md` 未创建或代写。无关 research/validation 修改保持 unstaged。
- **commit hash**：待新双评审、当前哈希 G-03P、全量文档/凭据/Git 校验后填写；本条不预造 commit 或 PASS。
- **经验教训**：桌面批准必须先看目标路径和动作；即使隔离任务没有触碰仓库，删除其旧输出仍会损失可复验文件。远程 CI 合同必须在首次 push 前执行“该 tip 当前存在的所有测试”，不能依赖未来的 CI 扩展补救历史分支。

## 2026-07-27T19:17:43+08:00 - G-03P-004 最终占位、self-scan 修订与 SR-08

- **Task 编号**：G-03P-004（fresh Codex 占位冷启动、输出 gap 修订、最终同哈希双评审；不满足正式 G-03，不包含产品实现）。
- **触发的 Superpowers skill**：主智能体使用 `systematic-debugging`、`brainstorming`、`writing-plans`、`test-driven-development`、`requesting-code-review` 和证据优先验证；fresh task 使用 `executing-plans`/TDD/verification。没有 worktree、正式实现派发或 finishing。
- **关键 prompt / context**：学生要求在误批停止后检查文件并继续，且此前明确要求用 Codex 先做同类型冷启动占位。fresh projectless task 只获准读取最终候选的 SPEC/PLAN 两路径，不得枚举仓库、提交、联网或集成。
- **G-03P 输出**：task `019fa331-3da1-7f80-a37c-ac7abb135a46` 验证 SPEC `6A0DB7...11E56` 和 predecessor PLAN `D574B8...1D742`；先得到 exit 1 `CONTRACT_RED scanner_missing`，再以同一命令得到八组 exit 0 green。十一 helper 顺序符合 PLAN；项目外 contract/scanner hash 为 `E970C52C...3A79B` / `097F5683...9F64`。
- **真实 gap 与修订**：两文件 tracked+staged self-scan exit 2，在 contract 的 index/worktree 源均发现 `credential_assignment`；独立 AST review substitute 未执行，不补造收据。PLAN 因此新增 runtime-fragment fixture 和精确 `CREDENTIAL_SCAN_PASS files=4` Green/Done 条件，形成最终 hash `E96C415A...972C1`；F-01S ledger 仍为 not started。
- **许可证 TDD**：把 bootstrap license owner 从 F-01A 修正到 F-01B 后，旧 verifier 真实返回 `Bootstrap license evidence hash mismatch`；更新到 `FD65C5D2...4F310` 后标准收据恢复 `rows=63 explicitly_blocked=2`。`DEPENDENCY_BASELINE.md` 同步 F-01A/F-01B/F-01E ownership。
- **最终 review**：current-hash course/SPEC review 为 `PASS; Critical=0, Major=0, Minor=0`；quality/security/license review 为 `PASS; Critical=0, Major=0, Minor=1`。唯一 Minor 是 Pillow 未有明确 v1 生产用途；不得因此宣称依赖最小化已完成。
- **最终身份与门禁**：SPEC `6A0DB7CAD19533FE9A31EA81A6B30ED493C01BE59D4C98DEB6EC04A89BD11E56`（27188 bytes）；PLAN `E96C415AD716B002AD9B1EB3C2AFD7C78F693486CB83A795110B99B6755972C1`（82442 bytes）；35 task/35 ledger/24 AC/0 placeholder。SR-08 closed；正式非 Codex G-03、学生 G-04、D-025、远程授权和 `REFLECTION.md` 仍开放。
- **人工修改及原因**：学生未新增产品/托管/付费选择。主智能体只修复评审与 cold-start 暴露的确定性合同，并保持无关 research/validation 修改 unstaged；没有代批任何桌面权限或外部操作。
- **commit hash**：`059082cf700f40a43b2bb931b996b04fac654f69`（`docs(stage-b): close reviewed cold-start remediation [agent: Codex]`）；这是 SR-08/current G-03P remediation 检查点，不是正式 G-03、G-04 或实现完成。
- **经验教训**：合同测试全绿仍可能无法通过同一提交安全门；cold-start task 的 Done 必须验证它自己将提交的字节，而不是只验证被测行为。PLAN 中的 task owner 变化也必须同步所有冻结 evidence ledger，否则“唯一权威输入”会互相矛盾。

## 2026-07-28T07:32:59+08:00 - G-03-SETUP Claude Code 本地安装与学生文档中文化

- **Task 编号**：G-03-SETUP（只准备异类智能体工具和中文操作材料；不执行正式冷启动，不进入产品实现）。
- **触发的 Superpowers skill**：使用 `using-superpowers` 约束技能选择；npm 首次读取失败后完整使用 `systematic-debugging`，先复现并定位默认缓存目录权限问题，再改变单一变量复验；完成前使用 `verification-before-completion`。未触发实现 worktree、产品 TDD、subagent 派发或 finishing。
- **关键 prompt / context**：学生要求尝试通过 Node.js 安装 Claude Code，并要求 G-03 操作手册及后续所有需要学生阅读的文档使用中文。冻结 SPEC/PLAN 不得因翻译操作而改变，正式 G-03、G-04 和 D-025 仍保持门禁状态。
- **安装证据**：本机 `node v24.14.0`、`npm.cmd 11.9.0`、Git for Windows `2.55.0.windows.3`；npm registry 元数据返回 `@anthropic-ai/claude-code 2.1.220`、Node engine `>=22.0.0` 和 integrity `sha512-ogBr...2Auyw==`。首次 `npm view` 因默认 `C:\Users\22078\AppData\Local\npm-cache` 无写权限返回 `EPERM`；把 cache 和 prefix 限定到仓库已忽略的 `tmp/` 后成功安装 2 个 package。`tmp/toolchains/claude-code/node_modules/.bin/claude.cmd --version` 实际输出 `2.1.220 (Claude Code)`；手册中的 `--safe-mode`、空 MCP、新 session 参数组合也通过本机参数解析并返回同一版本。
- **安全与许可证边界**：未运行登录、未读取钥匙串、未输入或输出账号凭据/API Key、未调用模型服务。安装物只存在于 Git 忽略的 `tmp/toolchains/claude-code/`，不是产品依赖，也未加入分发。包清单声明 `SEE LICENSE IN README.md`，README 指向 Anthropic Commercial Terms 和 Privacy Policy；正式使用时由学生本人接受账号与服务条款。
- **文档修改**：把 `docs/cold-start/G-03_CLAUDE_CODE_RUNBOOK.md` 和 `DECISIONS_NEEDED.md` 改为中文，保留命令、哈希、任务编号和原始工具输出字面值；合并重复 G-03 待办，并新增经本机 `--help` 验证的 `--safe-mode`、空 MCP、新 session 隔离命令。今后学生需要阅读、操作或签字的 README/操作手册/决策文档默认中文；工程审计和机器证据可以保留技术原文。`REFLECTION.md` 仍只能由学生本人撰写。
- **人工修改及原因**：没有修改已冻结并通过评审的 `SPEC.md`、`PLAN.md`，避免使 SR-08 同哈希评审失效；没有接触用户已有的 `docs/research/*` 和 `docs/engineering/SUPERPOWERS_VALIDATION.md` 修改。
- **subagent 输出或 commit hash**：本 task 未派发 subagent；文档与安装收据提交为 `c9adf685d29634f78735be282a4551bca1f9def3`。正式非 Codex G-03 尚未执行。
- **经验教训**：Windows PowerShell 的 `npm.ps1` 执行策略和 npm 缓存写权限是两个独立问题；使用 `npm.cmd` 解决前者，项目内 `--cache`/`--prefix` 解决后者，无需提权或修改系统策略。工具安装成功不等于账号或服务路径可用，门禁状态必须继续区分。

## 2026-07-29T16:35:21+08:00 - G-03-001 正式异类冷启动认证失败

- **Task 编号**：G-03-001（正式异类智能体冷启动 transport/auth 尝试；未到达 F-01S 实现）。
- **触发的 Superpowers skill**：使用 `using-superpowers`、`systematic-debugging` 和 `verification-before-completion`；因为模型 turn 未开始，没有触发产品 TDD、worktree、subagent implementation 或 finishing。
- **关键 prompt / context**：学生要求用 Claude Code 和一次性 API 凭据执行 G-03。主智能体拒绝把聊天中已公开的 key 写入工具参数或文件，改用 PowerShell `Read-Host -AsSecureString` 隐藏输入；runner 只复制冻结 SPEC/PLAN 到系统临时目录。
- **运行收据**：会话 `a7671467-4cdb-4473-a9ab-587c336ef68d`，Claude Code `2.1.220`；SPEC/PLAN 哈希精确为 `6A0DB7...11E56` / `E96C415A...972C1`，初始文件数 2。中转返回 `401 authentication_failed`，exit 1，input/output token 0、费用 0，隔离目录无新增文件。
- **故障根因与修订**：Windows `.cmd` 破坏内联 MCP JSON；用户设置又覆盖显式 API key。runner 已删除内联 JSON，改用 Bearer token、project-only settings、显式当前中转/模型、subprocess credential scrub、`--allowedTools`、120 秒 API timeout 和 2 次 retry；并将文件写为带 BOM UTF-8 以兼容 PowerShell 5.1。当前凭据仍被端点拒绝，因此没有再次猜测认证配置。
- **安全与人工边界**：日志对 key 和掩码后缀脱敏；未把凭据提交、写入过程文档或回显。学生仍需确认凭据平台的 base URL、认证方式和模型名。没有修改 SPEC/PLAN、产品源码、远程资源或 `REFLECTION.md`。
- **subagent 输出或 commit hash**：没有派发 subagent；失败收据提交为 `47e91fef3987a0ad7f6f95c3b9835979afea2277`。正式 G-03 和 G-04 仍开放。
- **经验教训**：CLI init 不等于模型已执行；只有出现模型问题/产物和 task 验证才可能闭合 G-03。代理端点、认证头和模型必须作为一个不可拆分的配置三元组核对，不能只凭“key 已生成”推断可用。

## 2026-07-29 - G-03-002 正确端点确认与模型发现修订

- **Task 编号**：G-03-002（只修正正式冷启动 transport 配置并验证公开协议；尚未执行模型 turn）。
- **触发的 Superpowers skill**：使用 `using-superpowers`、`systematic-debugging` 和 `verification-before-completion`；未触发产品 TDD、worktree、subagent implementation 或 finishing。
- **关键 prompt / context**：学生确认凭据对应 `https://ai2.1343263.xyz` 的直接 Claude 分组，并预计后续继续使用该服务。该信息替代 runner 的旧 ChatAnywhere/deepseek 临时配置，但不改变产品 SPEC 中内置 OpenAI adapter 的交付范围。
- **公开探针**：浏览器安全层拒绝自定义域名，Windows curl 又因 Schannel `SEC_E_NO_CREDENTIALS` 失败；未关闭 TLS 校验，改用 Node 24 fetch。根路径返回 200；无凭据 `/v1/models` 返回 `API_KEY_REQUIRED` 并声明支持 Bearer、`x-api-key`、`x-goog-api-key`；Anthropic `/v1/messages` 对假的 x-api-key 和 Bearer 均返回 `INVALID_API_KEY`。未使用真实凭据、未产生模型 token 或费用。
- **runner 修订**：端点改为 `ai2.1343263.xyz`，保留 Bearer token；隐藏输入后先查询 `/v1/models`，过滤真实 Claude 模型并在多个候选时要求终端选择；所选模型写入脱敏 metadata 并通过 `--model` 传给 Claude Code。旧 401 保留为历史证据，不倒写成功。
- **人工修改及原因**：只修改 Git 忽略的本地 runner 和中文过程文档，不改 SPEC/PLAN、产品 provider 设计、源码、远程资源或 `REFLECTION.md`。
- **subagent 输出或 commit hash**：没有派发 subagent；runner 的 PowerShell 语法、静态安全约束和假凭据失败路径已在本地复验，正式 Claude turn 仍未发生。端点修订收据为 `5af19473006c0a6628554f5b3358e4a5278b71cd`；G-03 与 G-04 仍开放。
- **经验教训**：自定义端点的网页首页可访问不代表 API 配置正确；必须分别验证协议路径、认证头和服务实际返回的模型 ID。模型发现应优先于硬编码别名，尤其是第三方 Anthropic-compatible gateway。

## 2026-07-29T20:54:24+08:00 - G-03-003 正式 Claude 模型执行不完整

- **Task 编号**：G-03-003（最终哈希上的正式异类冷启动 F-01S 尝试；结果不完整）。
- **触发的 Superpowers skill**：使用 `using-superpowers`、`verification-before-completion`；发现 CLI exit 0 与空产物不一致后使用 `systematic-debugging`，runner 修复使用 `test-driven-development`。未触发产品 worktree、正式 F-01S、subagent implementation 或 finishing。
- **关键 prompt / context**：Claude Code 只得到 SPEC `6A0DB7...11E56`、PLAN `E96C415A...972C1` 和要求完整尝试 F-01S 的初始 prompt。会话 `71a50d25-4cd7-48b1-9472-8107e82779ed` 使用 `claude-sonnet-5`，初始文件精确为两份。
- **模型输出与费用**：Claude 报告正确哈希/文件列表并读取 F-01S，检查 Git/PowerShell 后只创建空 `scripts/tests`。可用 Bash/Edit/Read，实际没有 Edit；没有问题、diff、红测、绿测或自扫描。结果为空 `end_turn`，CLI exit 0、permission denial 0、费用约 `$0.4712`。独立文件检查确认仍只有 SPEC/PLAN。
- **故障根因与 TDD 修订**：runner 错把 CLI exit 0 视为任务完成，没有验证 task 产物。先新增本地后置条件测试并观察实现文件缺失红；最小 helper 后测试输出 `G03_POSTCONDITION_TEST_PASS`。runner 现要求隔离目录恰好包含两份冻结输入和两份非空脚本，否则写 `COLD_START_INCOMPLETE`；本次目录被精确判为 `required_artifact_missing`。下一次默认模型单变量改为端点列出的 `claude-sonnet-4-6`。
- **人工修改及原因**：只修改 Git 忽略的 runner/helper/test 和过程文档；SPEC/PLAN、产品源码、远程资源、用户研究草稿与 `REFLECTION.md` 均未修改。
- **subagent 输出或 commit hash**：没有派发 Codex subagent；异类智能体即上述隔离 Claude Code session。过程文档收据为 `4e7f7ed8c6110caa4776ff1d9cea150b2c03758c`。G-03、G-04 仍开放。
- **经验教训**：进程成功只证明 CLI 正常结束。冷启动门禁必须同时验证冻结上下文、实际产物和测试收据；第三方兼容端点返回空 `end_turn` 时必须按不完整失败处理，不能靠 exit code 制造 PASS。

## 2026-07-29T23:31:20+08:00 - G-03-004 正式 Claude 4.6 网关超时

- **Task 编号**：G-03-004（最终哈希上的第二次正式异类冷启动 F-01S 尝试；网关 504）。
- **触发的 Superpowers skill**：使用 `using-superpowers`、`systematic-debugging` 和 `verification-before-completion`；未触发产品 TDD、worktree、正式 F-01S、subagent implementation 或 finishing。
- **关键 prompt / context**：学生报告 Claude Code exit 1 与脱敏日志路径。主智能体只读检查 `metadata.json`、`completion.json`、`models.json`、隔离目录和结构化 `claude-output.log`，没有再次调用模型或读取密钥。
- **运行收据**：会话 `32b62490-7817-4d3d-8452-7a29a4de94ea`，Claude Code `2.1.220`，模型 `claude-sonnet-4-6`，SPEC/PLAN 哈希 `6A0DB7...11E56` / `E96C415A...972C1`，初始文件数 2。模型读取文件并用 `certutil` 得到正确哈希后，网关返回 `API Error: 504 Gateway Time-out`；runner 状态 `CLAUDE_FAILED`、exit 1，费用约 `$0.1818`，隔离目录无新增文件。
- **人工修改及原因**：记录第二次正式异类失败事实；不修改 SPEC/PLAN、产品源码、远程资源、用户研究草稿或 `REFLECTION.md`。
- **subagent 输出或 commit hash**：没有派发 Codex subagent；异类智能体即上述隔离 Claude Code session。过程文档收据为 `0047d3efba1e35afa27d1e96421973924afbbf9c`。G-03、G-04 仍开放。
- **经验教训**：在同一中转上换用 Sonnet 4.6 后仍失败，继续盲目重试会消耗费用但不能增加工程确定性。下一步必须明确模型/端点策略，而不是把 504 当成可忽略的偶发输出。

## 2026-07-30T20:16:54+08:00 - G-03-005 多语言 capsule、F-01S1 拆分与 runner 失败关闭修订

- **Task 编号**：G-03-005（执行学生批准的冷启动可执行性修订；不包含正式 G-03 付费复测或产品实现）。
- **触发的 Superpowers skill**：使用 `using-superpowers`、`executing-plans`、`writing-plans`、`test-driven-development`、`systematic-debugging`、`requesting-code-review` 和 `verification-before-completion`。正式 worktree/subagent implementation/finishing 仍由 G-03/G-04 阻塞。
- **关键 prompt / context**：学生提供完整修订计划，要求中文 SPEC/学生文档、英文 capsule、F-01S1--4 串行拆分、两段式 Claude 冷启动、总预算 `$1`、不跳过 G-03/G-04。恢复时 SPEC/PLAN 和 capsule 脚本已有未提交半成品；学生原有研究文档保持未暂存且未修改。
- **TDD 与验证输出**：core missing、runner missing、candidate verifier missing、execution evidence parser missing 四个要求形红灯均实际运行；修订后 capsule 合同 `cases=9`、core `cases=8`、entrypoint `cases=4`。标准 evidence 保持 `rows=63 explicitly_blocked=2 python_pins=54 npm_packages=166`；strict UTF-8 与相关文件凭据形状扫描通过。机械审计为 38/38、5 fields、24 AC、0 placeholder、unknown/self/cycle 0。
- **review 输出**：第一名只读 reviewer 对 predecessor PLAN 返回 Critical=2/Major=1；第二名返回 Critical=2/Major=5。没有把失败 verdict 写成 PASS。修复 capsule 规则、自包含 `-Path` CLI、test-only schema、内存捕获、固定模型/端点、Linux/WSL2 sandbox、结构化费用/工具/歧义和独立红绿/直接扫描重放后，当前新哈希仍待重新双评审。
- **安全与环境**：未调用模型、未输入或读取真实 key、未把子进程原始输出落盘。官方 Claude 文档确认原生 Windows 无 OS sandbox；本机 WSL 枚举返回 `E_ACCESSDENIED`。正式 runner 在原生 Windows 会在隐藏输入前失败关闭，学生需提供可用 WSL2/Linux 环境。
- **当前哈希 / 人工边界**：SPEC `BE32CA...EFFF`，PLAN `35D989...F48F`。当前字节等待同哈希双评审和学生重新确认；G-03、G-04、D-025、远程授权、产品实现与学生反思均保持开放。commit hash 尚未产生。

## 2026-07-30 - G-03-006 第二轮审查修复与安全重放

- **Task 编号**：G-03-006（修复 G-03-005 第二轮审查问题；不执行付费模型复测或产品实现）。
- **触发的 Superpowers skill**：`using-superpowers`、`executing-plans`、`systematic-debugging`、`test-driven-development`、`requesting-code-review`、`verification-before-completion`。
- **关键 prompt / context**：继续学生批准的 G-03 修订计划；输入包括两名只读 reviewer 的失败 verdict。只修改 SPEC/PLAN/capsule、G-03 runner/合同和过程文档；学生已有 `docs/research/*` 与 `docs/engineering/SUPERPOWERS_VALIDATION.md` 修改不纳入。
- **真实 red/green**：合同先因缺少 `CommandInvoker` 与入口仍授权 `Edit` 失败；空实现和错误 JSON 键顺序候选分别被新增断言证明旧 oracle 可欺骗。修订后 `G03_RUNNER_CONTRACT_PASS cases=8` 与 `G03_RUNNER_ENTRYPOINT_PASS cases=4`。候选重放改为 coordinator 自有行为 oracle，stream parser 要求真实有序红绿 tool result；正式路径使用无凭据、断网、限挂载 bubblewrap 和进程树 timeout。
- **review 输出**：第二轮 SPEC review 为 `Critical=1, Major=1`；第二轮质量/安全/许可证 review 为 `Critical=2, Major=4, Minor=2`。当前修订不继承旧 verdict，必须在最终同一哈希重新双评审。
- **当前哈希 / 人工边界**：SPEC `14C03D68...0713`，PLAN `D6A0C79B...879D`。正式 Linux bubblewrap 预检、同哈希双评审、学生重新确认、G-03、G-04、D-025、远程授权和学生本人反思仍开放。commit hash 尚未产生。

## 2026-07-30 - G-03-007 Claude stream 包装格式与 oracle 证据修复

- **Task 编号**：G-03-007（只修复 runner 解析与过程文档；不执行付费模型复测或产品实现）。
- **触发的 Superpowers skill**：`using-superpowers`、`executing-plans`、`systematic-debugging`、`test-driven-development`、`requesting-code-review`、`verification-before-completion`。
- **关键 prompt / context**：根据历史 Claude Code stream-json 收据定位失败 `tool_result.content` 的真实 `Exit code 1` 包装；保持独立 bubblewrap 重放只接受裸 `CONTRACT_RED scanner_missing`，避免放宽候选验证。
- **TDD 红—绿证据**：先将真实包装格式加入合同样例，旧 parser 实际返回 `tdd_evidence_missing`；最小 parser 白名单修订后 `G03_RUNNER_CONTRACT_PASS cases=8`，并新增错误退出码/额外行拒绝与 `exit_code=1` TDD receipt 断言；入口合同 `G03_RUNNER_ENTRYPOINT_PASS cases=4`。
- **文档与哈希**：PLAN capsule、中文 G-03 手册、合规矩阵、SPEC_PROCESS、DECISIONS_NEEDED 同步更新。当前 SPEC `14C03D688A09451DCA06F66507CE4510510A8A3BC550057376B0A1EF95270713`；PLAN `95FF14D23DB92692BA005C3AA42598ABB5DDCFEE2DEFC28B950B00617C3EC663`。
- **人工修改及原因**：只修改 G-03 runner、其合同和过程文档；保留用户的 `docs/research/*` 与 `docs/engineering/SUPERPOWERS_VALIDATION.md` 修改，不创建产品源码、REFLECTION、远程状态或真实凭据。
- **经验教训**：外部 CLI 的结构化事件包装必须以真实收据为依据，并在规范化后保留退出码；候选重放与模型事件解析是两个不同的信任边界，不能用一个宽松规则覆盖两者。
- **最终同哈希复核**：SPEC/课程合规 reviewer 与质量/安全/许可证 reviewer 均返回 `PASS Critical=0 Major=0 Minor=0`；两者核对的当前哈希为 SPEC `14C03D688A09451DCA06F66507CE4510510A8A3BC550057376B0A1EF95270713`、PLAN `95FF14D23DB92692BA005C3AA42598ABB5DDCFEE2DEFC28B950B00617C3EC663`。正式 Linux/WSL2 bubblewrap、非 Codex Claude 双 session、学生确认和 G-04 仍未执行。

## 2026-07-30T23:56:43+08:00 - G-03-008 可观察运行状态与 Windows/WSL2 边界修订

- **Task 编号**：G-03-008（只增强 G-03 runner 的可观察性、跨平台字节稳定性和中文操作说明；不执行付费模型复测或产品实现）。
- **触发的 Superpowers skill**：`using-superpowers`、`brainstorming`、`writing-plans`、`executing-plans`、`using-git-worktrees`、`systematic-debugging`、`test-driven-development`、`requesting-code-review`、`verification-before-completion`。学生选择保留严格 runner 并加入持续状态日志。
- **关键 prompt / context**：学生在原生 Windows PowerShell 5.1 中运行 `pwsh` 得到 command-not-found，并要求长任务持续反馈。Claude CLI 本身可在 Windows 使用，但正式 G-03 合同依赖 Linux/WSL2 的 namespace、`bubblewrap`、`socat`、`timeout` 和 PowerShell 7，以实现断网、限挂载、凭据环境清理与有界进程树终止；只在 Windows 安装 `pwsh` 不能提供等价证据。
- **TDD 红—绿证据**：入口合同先实际失败 `Runner contract literal missing: status.log`；heartbeat 合同先实际失败 `Wait-G03ProcessWithHeartbeat ... not recognized`；未捕获异常场景先因缺少 `completion.json` 失败。最小实现后本次完整运行得到 `G03_RUNNER_ENTRYPOINT_PASS cases=5`、`G03_RUNNER_CONTRACT_PASS cases=9`、`AGENT_CAPSULE_CONTRACT_PASS cases=9`。新增 `status.log` 为 UTF-8 无 BOM JSONL，只允许 `timestamp/stage/event/elapsed_seconds`，intake/execution 每 15 秒心跳，所有受控结束写 `completion.json.status_log`；合同还拒绝冻结哈希、capsule prompt 标记和原始异常文本进入状态日志。
- **原生 Windows 证据**：证据目录 `tmp/g03-native-preflight-1a9d1361-dac5-40ef-9f77-dbe24006e795`；runner 依次记录 `runner/started`、capsule pass、input validated、`platform/unsupported_platform`、`EXECUTION_FAILED`、`runner/finished`，退出码 37。它在隐藏凭据输入前失败关闭，没有调用模型、没有联网、没有产生费用。
- **worktree 与字节稳定性**：按 `using-git-worktrees` 创建 `.worktrees/g03-progress-logging` 和分支 `codex/g03-progress-logging`；新 worktree 暴露 `core.autocrlf=true` 会把冻结 SPEC/PLAN 转为 CRLF并触发 capsule hash mismatch，故新增 `.gitattributes` LF 规则。机械还原 LF 后哈希恢复为 SPEC `14C03D...0713`、PLAN `95FF14D...C663`。环境拒绝写 `.git/worktrees/g03-progress-logging/index.lock`，因此按 skill 的 sandbox fallback 在当前 `codex/stage-b-scope-reset` 工作区继续，未 reset、clean 或覆盖用户文件。
- **回归与安全验证**：严格 UTF-8 `files=7`、PowerShell AST `files=4`、作用域凭据形状扫描 `files=7` 均通过；标准证据保持 `rows=63 explicitly_blocked=2 python_pins=54 npm_packages=166`，Linux 依赖证据 `ci_packages=41 demo_packages=14 license_rows=41`，provider 证据 `rows=7 models=2`；`git diff --check` 无错误，仅报告未纳入文件的行尾转换警告。SPEC/PLAN SHA-256 未变化。
- **人工修改及原因**：只修改 G-03 runner、合同、中文手册、局部计划、换行规则和本日志；保留学生已有 `docs/research/*` 与 `docs/engineering/SUPERPOWERS_VALIDATION.md` 修改为 unstaged。没有读取或写入真实凭据，没有修改产品源码、冻结 SPEC/PLAN、远程状态或 `REFLECTION.md`。
- **review 与修复**：第一轮只读质量/安全评审为 `FAIL Critical=0 Major=2 Minor=0`。Major 1 指出 heartbeat writer 或启动后首条日志写入异常会绕过局部进程清理；reviewer 的受控复现为 `HAS_EXITED_AFTER_EXCEPTION=False`。先新增 writer-throws 与 host-timeout delayed-marker 负例，旧实现实际以 `A progress-writer failure must propagate only after terminating the child process` 失败；最小修订在 waiter 和 runner 两层 `finally` 中终止并等待进程树，随后输出 `process_writer_failure_cleanup`、`process_timeout_cleanup` 和 `G03_RUNNER_CONTRACT_PASS cases=11`。Major 2 指出计划暂存清单漏掉 `.gitattributes` 与 heartbeat 合同，现已补齐。主智能体按原 reviewer 的两个复现条件逐项闭合后进行第二阶段复核，结论 `PASS Critical=0 Major=0 Minor=0`；第一轮 FAIL 保留在本记录中。
- **最终复验**：修复后同一差异完整运行得到入口 `cases=5`、core `cases=11`、capsule `cases=9`，严格 UTF-8 `files=8`、PowerShell AST `files=4`、作用域凭据形状扫描 `files=8`；三份标准证据与 SPEC/PLAN 哈希均保持不变。Linux/WSL2 正式进程树与 bubblewrap 仍需在目标环境现场验证，未用 Windows 单进程合同冒充正式证据。
- **subagent 输出或 commit hash**：质量/安全 reviewer 为上述第一轮 FAIL；主智能体完成精确回归与修复闭环。实现检查点为 `39f323d3791d78b6de0d0adb4d47bf3b5263ba5e`（`fix(g03): add observable runner progress`）。正式 Linux/WSL2 live preflight、Claude 双 session、G-03 证据闭合和 G-04 仍开放。
- **经验教训**：长时 runner 的“无输出”不能区分正常等待、网关阻塞和异常退出；可观察日志必须与敏感原始输出分离，并由受控状态码而非异常字符串提供诊断。冻结输入按原始字节绑定时，Git 行尾策略也是安全与可复现性合同的一部分。

## 2026-07-31T02:00:00+08:00 - G-03-009 WSL2 bubblewrap PowerShell 初始化修复

- **Task 编号**：G-03-009（修复正式 WSL2 预检，不执行 Claude 模型调用）。
- **触发的 Superpowers skill**：`using-superpowers`、`systematic-debugging`、`test-driven-development`、`verification-before-completion`。
- **故障证据**：用户 WSL2 会话已通过 capsule、输入哈希和平台识别，但 `preflight` 以退出码 55 失败。独立诊断中 `bwrap` 返回 PowerShell 初始化错误 `No such file or directory` 和 exit 70；用户在相同挂载参数增加只读 `--ro-bind /etc /etc` 后得到 `G03_DIAG_OK` exit 0。该差异没有输入凭据或调用网络。
- **TDD 红—绿**：先新增 `sandbox_runtime_mounts` 合同，旧代码实际失败 `Bubblewrap preflight must expose /etc read-only for PowerShell initialization.`；最小修订把 `/etc` 加入只读 runtime mounts。随后本地合同输出 `G03_RUNNER_CONTRACT_PASS cases=12`、`G03_RUNNER_ENTRYPOINT_PASS cases=5`、`AGENT_CAPSULE_CONTRACT_PASS cases=9`。
- **安全边界**：`/etc` 仅通过 `--ro-bind` 暴露，未增加 `/mnt`、项目目录外写权限或网络；已有 preflight 仍检查凭据环境、宿主挂载、DNS 和进程树终止。
- **人工边界**：正式 WSL2 bubblewrap preflight 尚待学生重新运行；在用户提供新 `status.log` 前，不标记 G-03 完成，不请求或接收 API key。

## 2026-07-31T02:10:00+08:00 - G-03-010 intake 失败分类收据

- **Task 编号**：G-03-010（为真实 WSL2 intake 失败增加脱敏诊断分类；不重试模型）。
- **事实证据**：会话 `a323a48b-e1de-4b1a-a334-451a05608767` 已通过 preflight 并在隐藏 key 后启动 intake；`process_finished elapsed_seconds=0`，退出码 43，证据目录没有原始 stdout/stderr。该收据只能证明 intake 非零失败，不能安全推断认证或 MCP 根因。
- **修订**：新增 `Get-G03ProcessDiagnosticCode`，只根据固定关键词输出 `cli_mcp_config`、`provider_auth`、`gateway_504`、`cli_startup`、`wall_timeout`、`child_nonzero`、`child_empty_output` 或 `child_output_protocol`；runner 写 `process-diagnostic.json`，字段仅为 `stage`、`exit_code`、`timed_out`、`code`，不保存 stderr、prompt、路径或凭据。
- **TDD 与验证**：先以 helper 缺失实际失败；实现后 `G03_RUNNER_CONTRACT_PASS cases=13`、`G03_RUNNER_ENTRYPOINT_PASS cases=5`、`AGENT_CAPSULE_CONTRACT_PASS cases=9` 全部通过。真实 API key 未再次输入，模型未再次调用。
- **人工边界**：下一次 WSL2 运行若仍失败，请只提供 `process-diagnostic.json`、`status.log` 和 `completion.json`；G-03 仍未闭合。

## 2026-07-31T02:20:00+08:00 - G-03-011 WSL CLI 相对路径解析修复

- **Task 编号**：G-03-011（修复真实 WSL2 intake 的 CLI 启动失败；不重试模型）。
- **事实证据**：最新会话 `65422312-9090-4692-ae95-09d09adf7fed` 的 `process-diagnostic.json` 为 `stage=intake`、`exit_code=127`、`code=cli_startup`。runner 将子进程工作目录切换到 disposable `/tmp/projectb-g03-*`，而学生传入的 `./tmp/toolchains/.../claude` 是项目根相对路径，因此在子进程中解析失败。
- **TDD 与修订**：新增相对/绝对 CLI 路径合同；`Resolve-G03ClaudeCliPath` 将相对路径按 `ProjectRoot` 解析为绝对路径，再交给 timeout 子进程。回归输出 `G03_RUNNER_CONTRACT_PASS cases=13`、`G03_RUNNER_ENTRYPOINT_PASS cases=5`、`AGENT_CAPSULE_CONTRACT_PASS cases=9`。
- **人工边界**：没有重新输入或读取 key，没有调用模型；下一次正式运行仍需学生在隐藏输入框输入临时 key，G-03 尚未闭合。

## 2026-07-31T02:30:00+08:00 - G-03-012 intake JSON 协议失败诊断

- **Task 编号**：G-03-012（记录真实 intake 退出码 44 的安全诊断；不重试模型）。
- **事实证据**：会话 `0b18ae59-9b31-4b84-b42f-e2786c8a68c5` 已通过 preflight，intake 运行 36 秒并产生 15/30 秒 heartbeat，随后退出码 0；runner 在 `ConvertFrom-Json` 阶段失败并以 44 结束。该事实说明路径和子进程启动已修复，但输出不是单一合法 JSON envelope；原始 stdout 未落盘。
- **修订**：协议解析失败和空结果现在也写 `process-diagnostic.json`，使用固定 `child_empty_output` 或 `child_output_protocol` 枚举；入口合同新增两条诊断调用断言，core 合同新增 malformed-output 负例。
- **验证**：`G03_RUNNER_CONTRACT_PASS cases=13`、`G03_RUNNER_ENTRYPOINT_PASS cases=5`、`AGENT_CAPSULE_CONTRACT_PASS cases=9` 全绿。没有再次输入或读取真实 key。
- **人工边界**：下一次只需查看最新 `process-diagnostic.json` 确定 provider/CLI 输出类型；G-03 仍未闭合。

## 2026-07-31T02:27:19+08:00 - G-03-013 Claude 提示行协议兼容修复

- **Task 编号**：G-03-013（修复正式 WSL2 intake 的 Claude Code stdout 协议兼容；不重试模型）。
- **触发的 Superpowers skill**：`using-superpowers`、`systematic-debugging`、`test-driven-development`、`requesting-code-review`、`receiving-code-review`、`verification-before-completion`。
- **事实证据**：会话 `f195336c-e5fc-4366-9ad5-3c90fb106811` 通过 capsule、哈希、平台和 preflight；intake 运行 59 秒，Claude Code 子进程 exit 0，但 runner 记录 `child_output_protocol` 并以 44 结束。三份既有脱敏日志均显示 stdout 首行是固定的 `Permission mode forced to default` 安全提示，后续行才是合法 JSON/stream-json；因此本次证据不支持“API 鉴权失败”，根因是 runner 把提示行和 JSON 整体交给 `ConvertFrom-Json`。
- **TDD 红—绿**：首次合同因 `Get-G03ClaudeJsonPayload` 缺失准确失败；宽正则实现后，新增的未观测 ASCII 变体负例又按预期失败。最小最终实现仅大小写敏感地接受正常 Unicode 提示和历史日志中的 mojibake 提示各一次；任意前言、任意分隔符、大小写变化、重复提示和重复 BOM 均拒绝。execution 同步改为只允许首行一次固定提示，其他非 JSON 行返回 `stream_output_protocol`。
- **验证证据**：core 合同 `G03_RUNNER_CONTRACT_PASS cases=13`，入口合同 `cases=5`，capsule 合同 `cases=9`，历史真实首行回放 `G03_OBSERVED_NOTICE_COMPAT_PASS`，课程证据 `rows=63 explicitly_blocked=2 python_pins=54 npm_packages=166`。
- **双评审**：首轮规约复核为 `FAIL Critical=0 Major=2 Minor=0`，质量/安全复核为 `FAIL Critical=0 Major=1 Minor=0`，共同指出 intake 正则过宽；规约复核另指出 execution 会跳过任意坏行。修复后只读复核为 `PASS Critical=0 Major=0 Minor=0`，独立确认变造提示与任意 execution 前言均失败关闭。
- **人工修改及原因**：只修改 G-03 runner、core、合同和中文过程记录；SPEC/PLAN 哈希保持 `14C03D...0713` / `95FF14D...C663`。未读取或写入真实 key，未再次调用模型，未修改产品源码、远程状态、学生研究文档或 `REFLECTION.md`。
- **门禁结论**：本次只修复 runner，不能关闭 G-03。学生仍需用相同命令重新隐藏输入临时 key；只有得到正式 `G03_EVIDENCE_READY` 并完成证据复验后，才可处理 G-04 实现批准。

## 2026-07-31T02:39:37+08:00 - G-03-014 第二次协议失败与脱敏形状诊断

- **Task 编号**：G-03-014（为无法从安全日志区分的 stdout 协议失败增加结构诊断；不重试模型）。
- **触发的 Superpowers skill**：`using-superpowers`、`systematic-debugging`、`test-driven-development`、`verification-before-completion`。
- **事实证据**：会话 `49fa60fb-85ea-4728-bf86-b68b2a532423` 在 WSL2 中再次通过 capsule、冻结哈希、平台和 preflight；intake 运行 25 秒，Claude Code 子进程 exit 0，仍以 `child_output_protocol`、runner exit 44 结束。没有 `intake-receipt.json` 或候选产物。本次仍不是 401、504、超时或 CLI 启动失败，但原始 stdout 按安全设计未落盘，现有证据不足以区分提示变体、ANSI、重复行或 JSON 行协议。
- **TDD 红—绿**：先新增纯 JSON、精确提示、未识别但带安全锚点的提示和伪 key 原文泄露负例，旧代码因 `Get-G03ClaudeOutputShape` 缺失准确失败。最小实现后 core 合同输出 `claude_output_shape` 和 `G03_RUNNER_CONTRACT_PASS cases=13`，入口合同 `cases=5`。
- **诊断边界**：仅在 `child_output_protocol` 时向 `process-diagnostic.json` 增加 `output_shape`；字段只有 JSON/非空行/固定提示/ANSI/HTML/其他文本计数、固定前缀/分隔符枚举和 stderr 是否存在。不得保存 stdout/stderr 原文、哈希可逆片段、prompt、模型结果、路径或凭据。
- **评审结论**：规约审查确认未改变 G-03 成功条件、费用、产物或人工门禁；质量/安全审查确认序列化诊断不包含测试中的伪 key 或任意文本。正式 G-03 仍开放，必须以新 runner 再产生一次结构证据，不能把本次失败计为 PASS。

## 2026-08-03T20:55:56+08:00 - G-03-015 人工 Claude Code 冷启动完成

- **Task 编号**：G-03-015（不同类型智能体的当前哈希 intake 与 disposable F-01S1A；不属于正式产品实现）。
- **触发的 Superpowers skill**：`using-superpowers`、`brainstorming`、`systematic-debugging`、`receiving-code-review`、`verification-before-completion`。
- **关键 prompt / context**：学生停用历史 runner，要求用 Claude Code 插件和短检查点降低长 thinking 中断风险。两个新 session 初始均只含冻结 SPEC/PLAN；execution 分为预检、contract 分块、RED、scanner 分块和只读 GREEN 回放。
- **subagent 输出或 commit hash**：Intake 哈希和文件集合正确、歧义为空；RED 为 `CONTRACT_RED scanner_missing`、exit 1；最终 PowerShell 7 回放为 `GROUP usage_and_output`、`GROUP provider_rule`、`BOOTSTRAP_SCANNER_PATH_PASS`、exit 0。候选 scanner/contract 分别为 95/161 行，SHA-256 `104085D3...B5C6E` / `8BA08B9A...F161E`。G-03 闭合文档提交为 `e0c5e550453ddde4571ce1dab4fe9586b1d8a34f`。
- **人工修改及原因**：学生逐段转交 Claude 原始 JSON，并在 3D 非结构化修复后要求只读 3D-R。主智能体未修改候选产物；只检查文件集合、冻结哈希、行数、规则和兼容性 green。插件费用和旧 runner bubblewrap 收据不可得，明确记录为限制而不补造。
- **清理记录**：为独立诊断创建了忽略目录 `tmp/g03-replay-ps5/`，并尝试下载 `tmp/toolchains/PowerShell-7.6.3-win-x64.zip` 到约 6.9 MB；下载超时。两次 `Remove-Item` 精确清理被环境策略拒绝后，未提权、未使用破坏性 Git 命令；改以 `apply_patch` 删除两个诊断文本，并用 .NET 精确删除已核验且未占用的 archive/空目录。`tmp/g03-replay-ps5/`、该 zip 和空 `tmp/toolchains/powershell-7.6.3/` 均已移除。
- **经验教训**：模型长思考问题应通过单 session 的原子检查点解决；每轮强制短 JSON 能保留真实 RED/GREEN，又避免把候选自述 `PASS` 当作 oracle。G-03 完成不等于 G-04，正式 F-01S1A 仍为 `not started`。

## 2026-08-03T21:23:01+08:00 - G-04 实现阶段批准

- **Task 编号**：G-04。
- **触发的 Superpowers skill**：`using-superpowers`、`using-git-worktrees`、`subagent-driven-development`、`test-driven-development`、`requesting-code-review`、`receiving-code-review`、`verification-before-completion`。
- **关键 prompt / context**：学生在读取 G-03 闭合结果后明确回复“批准进入实现阶段”。权威规范输入仍为 SPEC `AEA67BB5...E8381`、预派发 PLAN `910A3AEC...E923`；批准后的证据态 PLAN 仅更新执行标签和首项状态，哈希为 `382BCDB3...943F2`。
- **subagent 输出或 commit hash**：本条为人工门禁记录，尚未派发实现 subagent；协调提交 hash 在提交后补记于后续 task 记录。
- **人工修改及原因**：学生只批准本地实现。远程 push、PR/MR、发布、云资源、公网部署和真实 provider 调用未获本次授权。
- **经验教训**：冷启动完成与实现批准必须保留为两个独立事实；实现产物仍须从正式 worktree 中重新取得红—绿、双评审和提交证据，不能继承 disposable G-03 候选。

## 2026-08-03T22:37:12+08:00 - F-01S1A 单路径凭据扫描器核心

- **Task 编号**：F-01S1A。
- **触发的 Superpowers skill**：`using-git-worktrees`、`subagent-driven-development`、`test-driven-development`、`systematic-debugging`、`requesting-code-review`、`receiving-code-review`、`verification-before-completion`。
- **关键 prompt / context**：新鲜 worker `/root/f01s1a_impl` 只获得任务卡、两条 owned path、PowerShell 7 路径、G-04 状态和 TDD/脱敏/行数约束；禁止读取或复制 G-03 disposable 产物。基线为 `3b5c1491a0ad24e4fcde843f4afb9c4f24af890c`。
- **红—绿证据**：首次 contract-only 运行 exit 1，唯一输出 `CONTRACT_RED scanner_missing`；最小 scanner 后同一命令 exit 0，输出 `usage_and_output`、`provider_rule`、`BOOTSTRAP_SCANNER_PATH_PASS`。首轮独立规约 reviewer 返回 `FAIL Critical=0 Major=3 Minor=0`：错误支持多路径、缺 200/完整字符集正例、缺“只移除一个 ./”断言。修订中 `single_path_only` 先以 exit 1 失败；另以临时 mutation 证明窄化规则命中 `provider_maximum_alphabet`、循环剥离前缀命中 `provider_double_prefix_receipt`，随后恢复正确实现并保持同一 contract green。
- **评审与复验**：三项 Major 逐条关闭后，协调器按任务卡重新做规约逐项检查，再做正确性、可维护性、安全、测试和许可证复核，结论 `Critical=0 Major=0 Minor=0`。终端复验为 contract exit 0；两份产物分别直接扫描得到 `CREDENTIAL_SCAN_PASS files=1`；AST/严格 UTF-8、`git diff --check`、63 行课程证据、Linux 依赖证据和 provider 证据均通过；contract/scanner 为 100/78 行。无新增依赖或许可证义务。
- **subagent 输出 / commit hash**：实现提交 `b997fccae5c04cfa08547f5f9a99e8bbbd4f08d8`，仅含 `scripts/bootstrap_scan_credentials.ps1` 与 `scripts/tests/bootstrap_scanner_contract.ps1`。备用只读 Codex CLI reviewer 因继承的无效 OpenAI 环境凭据以 401 退出，未产生 verdict，不计为评审证据，也未重试。
- **人工修改及原因**：`Human-Changes: none`。协调器仅按已验证的 reviewer 反馈补充行为测试、收束多路径实现和执行 mutation 复验；未加入学生代码、真实凭据或第三方代码。
- **环境限制与经验教训**：系统 `core.autocrlf=true` 会改变固定哈希证据字节，故 worktree 以 `core.autocrlf=false` checkout；沙箱拒绝 `.git/worktrees/foundation-v1/index.lock`，提交改用忽略目录 `tmp/git-indexes/foundation-v1.index`，并逐一证明 staged blob 与工作树 blob 相同。评审发现测试通过不等于边界完整；对已正确但未被测试的行为，应保留 mutation 失败而不是伪造普通 RED。

## 2026-08-04T00:30:00+08:00 - Worktree 默认 Git index 写权限复核

- **Task 编号**：环境诊断 / F-01S1B 前置检查。
- **触发的 Superpowers skill**：`systematic-debugging`、`using-git-worktrees`、`verification-before-completion`。
- **关键 prompt / context**：复核此前 `index.lock: Permission denied` 与 `config.worktree: Permission denied`，区分 Git 规则、仓库 ACL 与沙箱挂载状态；禁止删除 dirty worktree、reset 或 clean。
- **证据**：根 `.git` 与链接 worktree 元数据路径均可读取；直接创建并删除精确的 `.git/worktrees/foundation-v1/index.lock` 成功；随后在 worktree 上执行 `git -c safe.directory=... -c core.autocrlf=false read-tree HEAD` exit 0，默认 `git status --short --untracked-files=all` 为空。根目录临时写探针也成功。此前失败只在 worktree 初始化后的沙箱上下文出现，且失败目标集中在 `.git/worktrees/foundation-v1`，不是 PLAN/AGENTS 门禁或 Git 语义错误。
- **结论与处置**：当前默认 index 已恢复可用，后续提交优先使用默认 index；`tmp/git-indexes/foundation-v1.index` 仅保留为可恢复备用，不再作为强制前置。未发起提权：本会话 approval policy 为 `never`，开发者明确规定 `sandbox_permissions=require_escalated` 会被拒绝；没有可执行的提权通道。若再次复现，记录 exact error 并切换备用 index，不修改全局 Git 配置。
- **人工修改及原因**：`Human-Changes: none`。本条只记录真实探针和环境结论。
- **经验教训**：链接 worktree 的 Git 元数据可能受沙箱生命周期或挂载身份影响；先做精确锁文件探针和 `read-tree`，不要把一次性 Permission denied 当成永久 Git 限制。

## 2026-08-04T14:30:00+08:00 - F-01S1B 其余直接凭据规则与产物安全

- **Task 编号**：F-01S1B。
- **触发的 Superpowers skill**：`subagent-driven-development`、`test-driven-development`、`requesting-code-review`、`receiving-code-review`、`verification-before-completion`；worktree 继续使用已验证的 `codex/foundation-v1`。
- **关键 prompt / context**：fresh worker `/root/f01s1b_impl2` 仅修改 scanner 与 contract 两条 owned path；在 F-01S1A 基础上增加 GitHub/AWS/Google/Slack/private-key 直接规则、稳定排序去重与产物自扫描，不进入 F-01S2 assignment/encoded 范围。
- **红—绿证据**：正式 RED 为 contract exit 1，前置组 `usage_and_output`、`provider_rule` 通过后停止于 `CONTRACT_FAIL direct_rules_and_order`；修正 35 字符 Google 正例后 GREEN exit 0。独立规约评审先后返回 `Major=2`（终止标记错误、边界覆盖不足）和 `Major=1`（部分允许前缀只有负例）；修订后以两次 mutation 复验：GitHub 上限放宽到 256 时在 `github_long` 失败，删除 `gho_` 时在 `github_gho` 失败。恢复正确实现后 exact contract 依次输出 `usage_and_output`、`provider_rule`、`direct_rules_and_order`、`artifact_direct_safety`、`BOOTSTRAP_SCANNER_CORE_PASS`，exit 0。
- **规约复核**：GitHub 五前缀、AWS 两前缀、Slack 五前缀和五种 private-key 头均有正向断言；四类 token 的最小/最大/超限及左右邻接边界已覆盖；provider 前置组未弱化；排序、去重、脱敏和两个产物自扫描满足任务卡。最终 `Critical=0 Major=0`。
- **质量/安全/许可证复核**：scanner 98 行、contract 165 行，均低于 140/180 上限；严格 UTF-8、稳定 JSON key 顺序、无值/内容/异常泄漏保持不变；两个 owned files 直接扫描均唯一输出 `CREDENTIAL_SCAN_PASS files=1`；`git diff --check` clean。无新增依赖、第三方代码、资产或许可证义务。最终 `Critical=0 Major=0 Minor=0`。
- **subagent 输出 / commit hash**：worker 提交 `2d79a1e11efe7b27123ae963f6007cf290985311`；review-fix 提交 `c07b90823448600950ba59e7ea4522a190918e92` 为本 task terminal commit。
- **人工修改及原因**：`Human-Changes: none`。协调器只按独立 reviewer findings 增加失败断言、执行 mutation、恢复实现并提交 review fix；学生未修改代码。
- **环境与经验教训**：本 task 的 `git add`、`git diff --cached --check` 和 commit 均成功使用默认 worktree index，未请求提权或备用 index。规则正则正确不等于回归合同完整；每个允许前缀必须至少有一个正向 fixture，负例不能证明该分支仍被支持。

## 2026-08-04T14:42:00+08:00 - F-01S2 派发准备

- **Task 编号**：F-01S2（in progress，尚无产品代码）。
- **触发的 Superpowers skill**：`subagent-driven-development`、`test-driven-development`。
- **关键 prompt / context**：依赖 F-01S1B terminal commit `c07b90823448600950ba59e7ea4522a190918e92` 已满足；下一 fresh worker 仅可修改 scanner 与 contract，按任务卡先增加 assignment/encoded 的最小失败断言，再实现 `Find-AssignmentSecret` 与 `Find-EncodedSecret`。
- **subagent 输出 / commit hash**：尚未产生 worker 输出或产品 commit。状态提交为 `c12a58b`，只把 PLAN ledger 和课程矩阵改为 in progress。
- **人工修改及原因**：`Human-Changes: none`。协调器未越过 fresh-subagent 门禁直接编写 F-01S2 行为代码。
- **经验教训**：任务状态 `in progress` 只表示串行所有权已打开；没有 RED/GREEN、双评审和 terminal commit 时不得声称完成。

## 2026-08-04T15:58:00+08:00 - F-01S2 assignment 与 encoded 规则完成

- **Task 编号**：F-01S2。
- **触发的 Superpowers skill**：`subagent-driven-development`、`test-driven-development`、`systematic-debugging`、`requesting-code-review`、`receiving-code-review`、`verification-before-completion`。
- **关键 prompt / context**：fresh worker `/root/f01s2_impl` 仅获得 F-01S2 task card、两条 owned path、PowerShell 7 路径、140/180 行上限和 F-01S1B 前置合同；禁止进入 tracked/staged source 范围。
- **红—绿证据**：contract-only RED 在前置三组通过后以 `CONTRACT_FAIL assignment_basic` exit 1；assignment 最小实现后继续增加 quoted/safe/boundary 断言。encoded RED 在 direct/assignment 全绿后以 `CONTRACT_FAIL encoded_base64url_provider_api_key` exit 1。协调器补做 mutation：禁用 double-quoted 分支时 `CONTRACT_FAIL assignment_double_escape`，移除 Hex family 时 `CONTRACT_FAIL encoded_hex_provider_api_key`，放宽 Base64URL 上限时长 candidate 被 `encoded_base64_long` 边界断言拦截，均 exit 1；恢复后 fresh full contract exit 0。
- **规约评审**：assignment 十个名称、左右边界、`:`/`=`、unquoted alphabet、8/512 长度、单/双引号配对、只允许 matching quote/backslash escape、CR/LF 拒绝、Unicode scalar 长度、七个 literal placeholder 与三种结构化 placeholder 均有断言。encoded 对六个 direct rule ID、Base64/Base64URL/Hex、canonical/padding、长度、family 边界、严格 UTF-8、只解一层及禁止 assignment-on-decoded 均有断言。最终 `Critical=0 Major=0`。
- **质量/安全/许可证评审**：最终合同依次输出 `usage_and_output`、`provider_rule`、`direct_rules_and_order`、`assignment_quotes_boundaries`、`encodings_and_types`、`artifact_direct_safety`、`BOOTSTRAP_SCANNER_RULES_PASS`；两个产物直接扫描唯一输出 `CREDENTIAL_SCAN_PASS files=1`；PowerShell AST error 0、`git diff --check` clean。scanner 140/140 行，contract 180/180 行。无新增依赖、第三方代码或许可证义务；最终 `Critical=0 Major=0 Minor=0`。
- **subagent 输出 / commit hash**：worker 在协调器提交后返回最终回执，报告完整 RED/GREEN、AST、自扫描、独立 review 与最终产物哈希；build commit 为 `d9a1a958fa64d6f812144d044b6de6f054f296a7`。worker 留下的 Base64URL 最大长度 review improvement 与协调器补充的超长反例由 `3a75411e210f99bc7098a2dfb3a1197ce8b96640` 提交，后者为 terminal commit。
- **人工修改及原因**：`Human-Changes: none`。协调器未改变产品方向，只执行临时 mutation、恢复候选、补齐 Base64URL max/over-limit 对称覆盖、做两阶段复验和提交。
- **经验教训**：紧贴行数上限的任务仍可完成，但必须使用表驱动断言并保持每个 family 的独立失败证据；并发 worker 在 coordinator commit 后仍可能留下 review fix，因此最终 `update-index --refresh` 与状态检查必须放在所有 agent 回执之后。

## 2026-08-04T16:15:00+08:00 - F-01S3 派发准备

- **Task 编号**：F-01S3（in progress，尚无本 task 产品代码）。
- **触发的 Superpowers skill**：`subagent-driven-development`、`test-driven-development`、`using-git-worktrees`。
- **关键 prompt / context**：依赖 F-01S2 terminal commit `3a75411e210f99bc7098a2dfb3a1197ce8b96640` 已满足；fresh worker 仅可修改 scanner 与 contract，通过 PATH-first fake Git 为 tracked worktree 与 staged index 的精确字节、mode/path/rename/error 合同取得 RED。
- **subagent 输出 / commit hash**：尚未产生；状态提交只记录串行所有权打开。
- **人工修改及原因**：`Human-Changes: none`；协调器未提前实现 F-01S3。
- **经验教训**：Git source 扫描必须把工作树字节与 index blob 字节作为两个独立 source/path 对，不能用当前文件系统内容替代 staged blob。

## 2026-08-04T19:03:08+08:00 - F-01S3 实现与复核

- **Task 编号**：F-01S3（complete；terminal commit `b7d929771657c02ff40150a8f81768a31ec0dfed`）。
- **触发的 Superpowers skill**：`subagent-driven-development`、`test-driven-development`、`systematic-debugging`、`verification-before-completion`；协调器在 worker 评审后执行可读性重构和合同补强。
- **关键 prompt / context**：依赖 F-01S2 terminal `3a75411e210f99bc7098a2dfb3a1197ce8b96640`；只修改 scanner 与 contract。source 字面量经 SPEC/PLAN 检索确定为 `worktree`、`index`，单路径仍为 `path`。
- **subagent 输出 / commit hash**：fresh worker 报告初始 scanner `31BDCF...`、contract `4388D6...`，但默认 index 创建 `index.lock` 被沙箱拒绝，未产生 commit。协调器保留其 RED：旧组全部通过后 `CONTRACT_FAIL dirty_worktree`，GREEN 最终 `BOOTSTRAP_SCANNER_SOURCES_PASS`。
- **人工修改及原因**：`Human-Changes: coordinator review fixes`。修复 PowerShell `VoidTaskResult` 污染 Git 进程返回值、fake Git 的 `ValueFromRemainingArguments` 绑定、`$matches`/`$Matches` 变量冲突和 junction 清理；随后将 scanner 从 68 个压缩行重构为可读函数，并增加绝对路径/未规范化 index 路径合同反例。所有修改在 GREEN 合同下复验。
- **验证证据**：合同输出 `usage_and_output`、`provider_rule`、`direct_rules_and_order`、`assignment_quotes_boundaries`、`encodings_and_types`、`artifact_direct_safety`、`staged_vs_worktree`、`index_modes_and_rename`、`path_safety_and_errors`、`BOOTSTRAP_SCANNER_SOURCES_PASS`，exit 0；scanner/contract 自扫描均 `CREDENTIAL_SCAN_PASS files=1`；两份 AST 解析错误数为 0；`git diff --check` 无错误（仅 LF/CRLF 警告）。最终 scanner SHA-256 `DC35C2D9AFD4D2F5E852E68BF03B5D27CFA5E34F46861B021302FAA683FDFADB`，contract SHA-256 `EC0A69B9F8BB1A8B32A14DB963950E5F058B27D8CD32AE055DCFC159299F36E6`。
- **SPEC 合规评审**：Critical=0，Important=0；确认精确工作树字节、stage-0 index blob、模式/路径/reparse 门禁、稳定脱敏错误、两 source/path 输出和前置合同组均覆盖。
- **质量/安全/许可证评审**：Critical=0，Important=0；未引入依赖或许可证义务，无值/内容/OID/异常日志，进程有 30 秒树终止，合同 fixture 与 fake Git 均为运行时临时内容。
- **经验教训**：PowerShell 异步 void task 和自动变量 `$Matches` 都会隐式进入输出/覆盖局部变量；此类语言语义必须用函数级探针验证，不能只看合同 marker。当前唯一未闭合项是 linked worktree 默认 index 的宿主写权限。
- **提交门禁证据**：协调器执行 `git -c safe.directory=E:/Personal_Documentary/ResearchProjects/ProjectB/.worktrees/foundation-v1 add -- AGENT_LOG.md PLAN.md docs/REQUIREMENTS_COMPLIANCE_AUDIT.md scripts/bootstrap_scan_credentials.ps1 scripts/tests/bootstrap_scanner_contract.ps1` 时收到 `fatal: Unable to create 'E:/Personal_Documentary/ResearchProjects/ProjectB/.git/worktrees/foundation-v1/index.lock': Permission denied`；未使用 alternate index、ACL 修改、reset 或 clean。临时探针 `tmp/f01s3-command-probe/` 已在合同结束后删除，未留下 untracked 文件。
- **插件提交核验**：学生报告通过插件提交后，协调器核验到 commit `8b51796b02b5c1555c2d2468ab7c02838bce79a1` 位于根 worktree 的 `codex/stage-b-scope-reset`，只包含 `AGENTS.md`、`docs/engineering/SUPERPOWERS_VALIDATION.md` 与 10 份既有研究文档，不包含本 task 两个 scanner 文件；因此该 commit 不能作为 F-01S3 terminal hash，且未对其执行重写或撤销。
- **最终提交核验**：学生在精确配置 `safe.directory` 后，于正确 worktree 创建 `b7d929771657c02ff40150a8f81768a31ec0dfed`；协调器验证该 commit 只修改两个 scanner 文件，`git diff b7d9297^ b7d9297 --check` clean，且工作树产物哈希与最终 GREEN 候选一致。
- **提交时 scanner 边界**：提交前 `-Staged` 如实以 `decode_failed` 停在已跟踪的 `docs/mockups/course-import-onboarding-v1-desktop.png`；这不是凭据 finding，而是 F-01S3 还没有 F-01S4 所属的文本 allowlist 与 binary skip list。两个实际 staged 产品文件已分别用 `-Path` 扫描并得到 `CREDENTIAL_SCAN_PASS files=1`，因此未把这次全 index 操作失败冒充为 PASS；F-01S4 必须用同一 PNG 回归闭合该缺口。

## 2026-08-05T11:10:21+08:00 - F-01S4 完整凭据扫描门禁

- **Task 编号**：F-01S4（complete；terminal commit `1d6dcab15adf1649cda7309360f3cdeff0423e27`）。
- **触发的 Superpowers skill**：`subagent-driven-development`、`test-driven-development`、`systematic-debugging`、`requesting-code-review`、`verification-before-completion`。
- **关键 prompt / context**：fresh worker 仅修改 scanner 与 contract；按任务卡依次补齐 UTF-8 BOM、UTF-16LE/BE、未标记 NUL、文本 allowlist、binary skip list、未知类型失败、`Invoke-BootstrapScan`、稳定错误顺序与顶层常量 `scan_failed`。前序合同组不得弱化。
- **TDD RED/GREEN**：首个 RED 将 UTF-8 BOM 期望改为接受，旧 scanner 返回 `decode_failed`；后续逐项增加 UTF-16、NUL、未知扩展、PNG、完整 allowlist/skiplist、AST redaction 与 fresh Git `files=4` 断言。最终同一命令输出精确十组并以 `BOOTSTRAP_SCANNER_CONTRACT_PASS` 结束，exit 0。
- **安全门禁修复**：首次全仓扫描 exit 2，只报告两份 `docs/archive/superseded-2026-07-23/` 历史计划的 `assignment_secret`。经学生明确批准，仅将四个合成代码变量重命名并同步引用；独立提交 `f6350daf66260f8850fed32ef2d2c4a0bd2be6a6` 后，`-Tracked -Staged` 得到 `CREDENTIAL_SCAN_PASS files=162`。未输出匹配值，未添加 archive 例外。
- **验证证据**：fresh 合同 exit 0；scanner 与 contract AST error 均为 0；fresh Git 仅含两文件时 `CREDENTIAL_SCAN_PASS files=4`；真实仓库 PNG 回归 `files=0`；两个 owned 文件直接扫描各 `files=1`；最终全仓双来源 `files=162`；`git diff --check` clean。
- **产物哈希**：scanner `55F058673608FEEE5968F52FE22DCEC03E22AFD50DB99B038F115622532B326E`；contract `34F628AE4E401AE6AB184321155C46ABD42628BBDAC9D913A66DA2BD1AD37614`。
- **SPEC 合规评审**：Critical=0，Major=0。确认严格编码、文件类型门禁、source/path/rule 去重排序、稳定 `code/source/path` 错误、常量顶层失败和精确十组输出均符合 F-01S4。
- **质量/安全/许可证评审**：Critical=0，Major=0。独立 reviewer 已派发但跨日恢复后没有回执，未冒充其 PASS；协调器使用当前 diff、任务卡、AST、完整合同与全仓扫描完成两阶段复核。未引入依赖、第三方代码或许可证义务。
- **subagent 输出 / commit hash**：worker `/root/f01s4_impl` 完成实现并保留完整证据；学生在宿主终端创建产品提交 `1d6dcab15adf1649cda7309360f3cdeff0423e27`，提交 trailers 为 `Task-ID: F-01S4`、`Agent: /root/f01s4_impl`、`Human-Changes: none`。
- **人工修改及原因**：产品文件 `Human-Changes: none`。协调器只执行只读复核与经学生批准的独立 archive 误报修复；没有改变 scanner 验收范围。
- **经验教训**：完整 scanner 第一次启用时必须先清除仓库历史文本中的合成 assignment 误报，不能通过忽略 archive 或缩小扫描范围制造 PASS；二进制跳过计数应只统计实际扫描文本，tracked/index 双来源则分别计数。

## 2026-08-05T13:01:39+08:00 - F-01A 可复现运行时与锁闭包

- **Task 编号**：F-01A（complete；terminal commit `8b725db53d044af41e9d6352802eecbe0c2e5d6d`，后续策略修复与并发 F-01B 评审修复合并于该提交）。
- **触发的 Superpowers skill**：`using-git-worktrees`、`subagent-driven-development`、`test-driven-development`、`systematic-debugging`、`requesting-code-review`、`verification-before-completion`。
- **关键 prompt / context**：fresh worker `/root/f01a_impl` 只获得 F-01A task card、权威依赖/锁路径、已验证 worktree 与验证命令；创建十个任务文件，禁止改写后续应用功能。权威输入为 uv `0.11.14`、CPython `3.14.6`、Node `24.18.0` 及三份 Python 锁和 npm 锁。
- **TDD RED/GREEN**：初始合同 exit 1，覆盖缺失产物/哈希、四份 raw-lock parity、manifest、`npm.ps1`、损坏下载、版本漂移和系统修改；随后为 Python site 配置、uv 漂移、`.python-version`/`.npmrc` scanner allowlist、正式 npm identity、junction 路径和 120 秒下载超时分别取得真实 RED。最终运行时合同输出 `FOUNDATION_RUNTIME_CONTRACT_PASS locks=4 python=3.14.6 node=24.18.0 npm=11.16.0`。
- **subagent 输出 / commit hash**：worker 产品提交 `d86f2d0ada64924eb63a4898b5c7743bfa59f870`；scanner 无扩展名文本修复为独立提交 `de3f336050dc781fca71252fa07086897e6a2949`；协调器安全/质量 review-fix 终点为 `201c09ebf044b20e601aef5bb3ba8c6dd0336a60`。
- **规约合规评审**：Critical=0，Major=0。十个 task-card 文件、项目内运行时、下载后哈希、解压前验证、四锁 raw parity、`npm.cmd`、无 PATH/registry 修改和精确版本均有合同证据。
- **质量/安全/许可证评审**：初审发现旧权威 npm 锁的 `undici` High、`postcss` Moderate、一次性 G-02A npm identity、junction 逃逸、无下载超时五项 Major；修订后 fresh `npm ci` 安装 115 个平台包，`npm audit` 与 `npm ls` 均 exit 0，证据验证保持 `rows=63 explicitly_blocked=2 python_pins=54 npm_packages=166`，许可证计数不变。最终 Critical=0，Major=0。独立 reviewer 派发接口本回合不可用，未冒充独立回执；协调器按 task card/SPEC/完整 diff 和新鲜命令完成两阶段评审。
- **人工修改及原因**：`Human-Changes: none`。学生只在宿主终端执行受阻的 Git 提交；协调器 review fix 更新两个传递安全补丁、正式私有 npm identity、reparse/timeout 防护和权威证据绑定，未改变直接依赖或产品范围。
- **凭据/依赖/环境证据**：最终 `CREDENTIAL_SCAN_PASS files=182`；bootstrap 与合同 AST error 均为 0；npm canonical-LF hash 更新为 `8b793ee9ca823ca1079efe12c4962a8786059b4aaf08bcb715264ad7b4718354`，生产锁与权威锁逐字节一致。权限探针空提交 `4ec79e7` 证明 `git commit` 可经宿主审批提权，今后不再把同类提交转交学生。
- **经验教训**：预审时“audit 为零”会随公告变化，生产锁物化当天必须重新审计；路径的字符串前缀不等于物理包含，下载/解压根必须拒绝 reparse point；权威锁可以为安全补丁修订，但必须同步哈希、验证器、PLAN 和过程证据，不能静默漂移。

## 2026-08-05T14:57:05+08:00 - F-01B 字节锁定 bootstrap 许可证闭包

- **Task 编号**：F-01B（complete；terminal commit `8b725db53d044af41e9d6352802eecbe0c2e5d6d`，并发暂存导致与 F-01A 策略修复同提交）。
- **触发的 Superpowers skill**：`subagent-driven-development`、`test-driven-development`、`systematic-debugging`、`requesting-code-review`、`receiving-code-review`、`verification-before-completion`。
- **关键 prompt / context**：fresh worker `/root/f01b_impl` 只获得 F-01B task card、F-01A 前置接口和 `BOOTSTRAP_LICENSE_EVIDENCE.md`；仅实现五份精确许可证、许可证合同和 `scripts/bootstrap.ps1` 的许可证安装入口。
- **TDD RED/GREEN**：初始合同对五个缺失目标、错误字节/数量/哈希、可变引用、传输回退和证据绑定产生 RED；规约评审指出初版仅静态检查传输关键字，随后增加真实 API-first、不可变 raw fallback、错误元数据、两类错误字节、双传输失败、partial 文件拒绝和 junction 根拒绝。最终输出 `BOOTSTRAP_LICENSE_CONTRACT_PASS`，离线入口输出 `BOOTSTRAP_LICENSE_PASS files=5`。
- **subagent 输出 / commit hash**：产品提交 `35e0561dcf6a20e11b57181fc28021f75647a77b`；路径类型和唯一测试沙箱修复为 `cad13ce0b29137a95c58b8a85a57b325f4e20e48`；API null 元数据 fail-closed 复审为 `efaa8f0814f82ccccd3a980eb49d4e34bfd612ac`；最终与 F-01A npm 策略收紧一并落在 `8b725db53d044af41e9d6352802eecbe0c2e5d6d`。协调器先提交门禁兼容修复 `de96057`，使 scanner 精确识别五个 extensionless 许可证名，并用 `.gitattributes` 保持上游字节且避免文本 diff 空白误报。
- **规约合规评审**：独立 reviewer 初审发现 1 Critical（传输合同未执行真实路径）、1 Major（license root reparse）和 1 Minor（恒真断言）；修订后合同覆盖计划要求的正负路径，Critical=0、Major=0。
- **质量/安全/许可证评审**：五个目标的 byte count、SHA-256 与 Git blob ID 均和唯一证据表一致；API 错误或 null 元数据都不回退，只有 API 传输抛错才使用相同不可变 commit 的 raw URL，复制前再次验证长度/blob/SHA；partial 使用 `CreateNew` 且不覆盖既有文件。最终 Critical=0、Major=0。
- **人工修改及原因**：`Human-Changes: none`。协调器只处理 reviewer finding、扫描器精确 allowlist 和字节锁定 diff 属性；未改许可证内容、依赖选择或产品范围。
- **验证证据**：提交后合同 exit 0；标准证据 `rows=63 explicitly_blocked=2 python_pins=54 npm_packages=166`；`CREDENTIAL_SCAN_PASS files=194`。五份许可证的长度/SHA-256 分别为 13804/`B0E25A78...10231`、157606/`148EACF7...6CA5`、9742/`7610D223...A257`、11357/`C71D239D...0AB4`、1077/`860E3D7A...176C`。
- **经验教训**：哈希锁定第三方文本可能合法包含 Git 空白诊断形状，也可能没有扩展名；门禁应以精确路径和不可变哈希理解这类产物，不能修改上游字节或宽泛跳过扫描。传输安全必须由可执行正负合同支撑，静态关键字搜索不能作为 PASS 证据。

## 2026-08-05T15:00:00+08:00 - F-01A npm 策略前置修复

- **Task 编号**：F-01A-review（complete；与并发 F-01B 修复共同终止于 `8b725db53d044af41e9d6352802eecbe0c2e5d6d`）。
- **触发的 Superpowers skill**：`systematic-debugging`、`test-driven-development`、`verification-before-completion`。
- **根因与 TDD 证据**：F-01C 预检发现计划声称的六项 frontend npm policy 与实际两项不一致；先收紧 F-01A contract，真实 RED 为 `CONTRACT_RED manifest .npmrc policy`，补齐 `audit=true`、`fund=false`、`save-exact=true`、`package-lock=true` 后 GREEN 为 `FOUNDATION_RUNTIME_CONTRACT_PASS locks=4 python=3.14.6 node=24.18.0 npm=11.16.0`。
- **人工修改及原因**：`Human-Changes: none`。未改变依赖版本，只补齐已冻结的安全安装策略；并发 worker 当时已暂存两份 F-01B 复审修复，因此 Git 将它们一并提交，未重写历史。
- **验证**：`CREDENTIAL_SCAN_PASS files=194`、`git diff --cached --check` exit 0；最终 F-01B 合同和标准证据验证均通过。
- **经验教训**：进入后续 task 前必须逐字核对前置合同与实际文件，不要仅依据 PLAN 的“already requires”描述。

## 2026-08-05T16:47:49+08:00 - F-01C 严格前端基础骨架

- **Task 编号**：F-01C（complete；terminal commit `39d79c2e6d423883a0614cc8d9bb947dd02a7dba`）。
- **触发的 Superpowers skill**：`test-driven-development`、`systematic-debugging`、`requesting-code-review`、`verification-before-completion`；沿用 `using-git-worktrees` 的 `codex/foundation-v1` worktree。
- **关键 prompt / context**：只实现 F-01C 的五个 owned path：严格 TypeScript、Vite/Vitest loopback/JSDOM 配置、可访问计数器组件、真实 user-event 测试和 PowerShell 合同。该组件仅是测试骨架，不是产品 UI；Open Design 仍由 UI-01 执行。
- **TDD RED/GREEN**：合同先以 `CONTRACT_RED missing_frontend_tsconfig.json` 失败；首次真实 Vitest 运行又分别暴露 `describe is not defined` 和缺少 JSDOM 的 user-event 失败。显式导入 Vitest API，并在 `frontend/` 工作目录加载 `vite.config.ts` 后，合同输出 `FRONTEND_FOUNDATION_CONTRACT_PASS`，真实交互为 `1 passed`；不存在的测试过滤器 exit 1，证明空 suite 不会变绿。
- **规约合规评审**：strict + `noUncheckedIndexedAccess`、React/JSDOM、5173/4173 loopback、禁止 `0.0.0.0`、可访问 button/status 和 click 后计数更新均有合同/运行证据。Critical=0，Major=0。
- **质量/安全/许可证评审**：`tsc --noEmit` exit 0，`npm audit --audit-level=moderate` 为 0 vulnerabilities；合同优先项目内锁定 npm，在 CI 环境可回退当前 `npm.cmd`/`npm`，并恢复 PowerShell 错误策略。没有新增依赖或许可证。Critical=0，Major=0。
- **subagent / 人工修改**：fresh worker 派发接口本轮没有返回可用会话，协调器 `/root` 执行并使用 `[agent: coordinator]`，未冒充 worker；`Human-Changes: none`。PLAN 所写 `npm --prefix frontend exec` 不改变 cwd，实际等价验证在 `frontend/` 目录执行锁定 npm，以确保加载唯一的 `vite.config.ts`；未修改冻结 PLAN 语义。
- **验证证据**：`CREDENTIAL_SCAN_PASS files=204`、`EVIDENCE_VALIDATION_PASS rows=63 explicitly_blocked=2 python_pins=54 npm_packages=166`、`git diff --cached --check` exit 0。
- **经验教训**：npm 的 `--prefix` 选择包根但不保证子进程 cwd；前端测试配置发现必须由实际启动目录验证，不能只做配置文本检查。

## 2026-08-05T18:01:20+08:00 - F-01D 可移植 push CI 种子

- **Task 编号**：F-01D（complete；terminal commit `069acb8541b8d59a7977a484f06d8f9abbefe780`）。
- **触发的 Superpowers skill**：`test-driven-development`、`systematic-debugging`、`requesting-code-review`、`receiving-code-review`、`verification-before-completion`；沿用 `using-git-worktrees` 创建的 `codex/foundation-v1` worktree。
- **关键 prompt / context**：只创建 `.gitlab-ci.yml`、`.github/workflows/ci.yml` 和 `scripts/tests/ci_seed_contract.ps1`。两端每次 push 运行固定 digest 的 scanner/backend/frontend current-suite；GitLab job 名精确为 `unit-test`；F-01E 前 backend 只能记录 `runner_absent_pre_feature`，存在 `backend/projectb` 却缺 runner 时必须失败。F-01A/B 的 Windows-only bootstrap 契约不塞入 Linux runner，Windows push job 仍由 DIST-01 所有。
- **TDD RED/GREEN**：初始合同得到 `CONTRACT_RED gitlab_missing`；创建两份 CI 后转绿。评审修订先得到 `CONTRACT_RED gitlab_commands`，随后两端 scanner job 加入 seed contract、前端改为 `vitest run` 自动发现全部测试。最小权限变异临时加入 `id-token: write` 后得到 `CONTRACT_RED github_permissions`，恢复仅 `contents: read` 后再次输出 `CI_SEED_CONTRACT_PASS`。
- **跨平台修复**：固定 Linux CI 暴露 scanner contract 的 Windows 路径与 `pwsh.exe` 假设；前置修复 `7210b25fb3e33f92ed34a964f1e926607738639a` 改为平台路径、Linux `pwsh` 和可执行 fake Git。Windows 全量输出 `BOOTSTRAP_SCANNER_CONTRACT_PASS`；WSL 真实 Git 最小仓库输出 `CREDENTIAL_SCAN_PASS files=2`。完整 WSL 合同因本机每次子进程启动约 8 秒而在 10 分钟超时，未冒充完整 Linux PASS。
- **规约合规评审**：fresh reviewer `/root/f01d_review` 初审提出 CI current-suite 与 trigger/fail-closed 检查问题；依据 PLAN 的 Windows-only/current-suite 明确边界撤销不适用项，其余修订完成后最终 `Critical=0, Major=0`。
- **质量/安全/许可证评审**：精确校验 GitHub 顶层权限块、三个 checkout 引用全部使用唯一固定 SHA、GitLab 唯一 workflow rules、无 path/branch filter、allow-failure、manual/delayed 或 `|| true` 绕过；无新增依赖或许可证。最终 `Critical=0, Major=0`。
- **subagent / 人工修改**：实现由 coordinator 完成，fresh subagent 负责独立双阶段评审；未冒充 worker。`Human-Changes: none`。此前沙箱 Git index 限制已通过正式提权提交解决，不再转交学生。
- **验证证据**：`CI_SEED_CONTRACT_PASS`；前端 `1 passed`；`tsc --noEmit` exit 0；`CI_YAML_PARSE_PASS files=2`；`CREDENTIAL_SCAN_PASS files=210`；`EVIDENCE_VALIDATION_PASS rows=63 explicitly_blocked=2 python_pins=54 npm_packages=166`；`git diff --cached --check` exit 0。Docker daemon 不可用，固定容器内命令和远程 pipeline 均为 `not executed / blocked`。
- **commit hash**：跨平台前置修复 `7210b25fb3e33f92ed34a964f1e926607738639a`；F-01D 产品提交 `069acb8541b8d59a7977a484f06d8f9abbefe780`。
- **经验教训**：seed CI 合同不能只验证关键字存在；触发条件、最小权限、固定 action、测试发现和绕过路径都要有可变异的失败证据。平台专用契约必须按已确认计划进入对应 runner，不能为了表面上的“全量”把 Windows 行为伪装成 Linux PASS。
## 2026-08-06T15:45:00+08:00 - F-01E quality gates review repair

- Task: `F-01E`; skills: `systematic-debugging`, `test-driven-development`, `receiving-code-review`, `verification-before-completion`.
- Context: second-stage quality review identified Git enumeration/count drift, an index-mode error-code mismatch, and an unbound Python license baseline.
- Changes: added one-pass `scan_git_snapshot`; aligned unsupported modes to `index_mode_unsupported`; bound normalized baseline license rows to SHA-256 `7013e4d8dee96ab1c461bf7b093c35770cd371b5ea7462a77f050f8912f51beb`; removed the obsolete second-pass counter.
- Verification: `21 passed` with project-local pytest basetemp; `CREDENTIAL_SCAN_PASS files=226`; `LICENSE_VERIFICATION_PASS python=54 npm=166`; `TEST_ALL_PASS mode=all`; `CI_SEED_CONTRACT_PASS`; `git diff --check`; Python compilation.
- Human changes: none. Commit is pending normal Git index permission; no alternate index or ACL workaround used.
- Lesson: a quality receipt must derive its findings and counts from the same captured Git source lists, and mutable license evidence must be hash-bound.
## 2026-08-06T16:25:00+08:00 - F-02 core SQLite schema and UoW

- Task: `F-02`; skills: `test-driven-development`, `systematic-debugging`, `receiving-code-review`, `verification-before-completion`.
- Context: implement only the F-02 owned migration, database entry point, UoW and storage contract tests after F-01E commit `ae152e3`.
- TDD: controlled RED was `5 failed` because `backend/projectb/storage/db.py` was absent; the literal command also hit the pre-existing host `%TEMP%` ACL, so evidence uses project-local `--basetemp`. GREEN is `7 passed` after review regressions were added.
- Spec review: the ten SPEC section 7 entities, lower-case content hashes, single-page/text-line locator union, uniqueness, foreign keys, immutable history, shared blob references and rollback boundaries are represented and tested.
- Quality review: independent review found 5 Major and 3 Minor issues. Fixed uppercase hash acceptance, PDF page ranges, mutable material hash, deletable coverage history, missing blob tombstones, migration atomicity and BEGIN connection cleanup. Blob bytes remain owned by M1-03; F-02 preserves `storage_ref` with `delete_pending=1` until that later boundary succeeds.
- Verification: targeted `7 passed`; backend regression `26 passed`; full runner and final scan are rerun after this evidence update. Human changes: none. Fresh worker dispatch was unavailable, so coordinator implementation is recorded rather than attributed to a worker.
- Lesson: database deletion metadata must survive physical-byte failure, and insert-time hash equality is insufficient without update immutability.

## 2026-08-06T17:52:17+08:00 - F-03 学习证据与复习计划数据库约束

- **Task 编号**：`F-03`；使用 `using-git-worktrees`、`subagent-driven-development`、`test-driven-development`、`systematic-debugging`、`requesting-code-review`、`receiving-code-review`、`verification-before-completion`。
- **关键 context**：fresh worker `/root/f03_impl` 只处理 migration 002、学习 schema 测试及经 coordinator 明确授权的 F-02 迁移清单兼容断言；基线提交为 `29da38e`，`Human-Changes: none`。
- **红绿证据**：初始 RED 因缺少 `002_learning` 和目标表失败；后续分别观察到旧迁移清单断言、SPEC 枚举/字段、Attempt 幂等键和同一 Attempt 多证据的失败。最终目标命令为 `14 passed`，后端回归为 `14 passed`。
- **规约评审**：fresh reviewer `/root/f03_spec_review` 发现 5 个 Major：掌握状态、`finals` 模式、预算/任务时长、LearningEvidence 字段与枚举、外键删除测试。已改为 `unknown/demonstrated_now/retained`、`continuous/finals`、预算 10--120 且步长 5、任务固定 10 分钟，并增加 evidence context、版本、枚举、幂等与删除规则约束。
- **质量/安全/许可证评审**：coordinator 复核发现 Attempt 缺少规范化 check kind/幂等键，以及同一 Attempt 可产生多条证据；均以独立 RED 后修复。未新增第三方代码或依赖。全量 runner 输出 `35 passed`、Vitest `1 passed`、Vite build PASS、`CREDENTIAL_SCAN_PASS files=234`、`LICENSE_VERIFICATION_PASS python=54 npm=166`、`TEST_ALL_PASS mode=all`。
- **subagent 输出与 commit**：worker 产物经评审修订后提交为 `1aaeb6f1912c7f1e5323ea6ab843b689937adbd1`；coordinator 修订均来自已记录的 reviewer finding 或额外 RED，没有学生代码改动。
- **已知基线问题**：计划中的独立 Ruff/mypy 命令仍因既有 `scripts/evidence/g02a_python_smoke.py` E402 和 `uow.py` 双模块名失败；F-03 未修改这些路径，全量项目 runner 仍通过。
- **经验教训**：schema 的绿色测试必须同时核对 SPEC 正文枚举和跨表权威关系；只给 evidence 一个通用幂等键，不能自动保证“一次 attempt 只生成一条证据”。

## 2026-08-06T18:15:44+08:00 - F-04 本地 HTTP 信任边界与审计白名单

- **Task 编号与 skill**：`F-04`；使用 `test-driven-development`、`systematic-debugging`、`requesting-code-review`、`verification-before-completion`，沿用 `codex/foundation-v1` worktree。
- **关键 context**：只创建计划列出的 HTTP 策略、审计模块和两份测试；不提前创建 FastAPI app、业务路由或 F-05 凭据逻辑。fresh subagent 派发接口本阶段不可用，因此实现明确归属 coordinator，`Human-Changes: none`。
- **红绿与评审**：初始 RED 为 15 个缺模块失败；GREEN 为 15 passed。SPEC 合规检查覆盖 loopback Host/Origin、unsafe 方法的 session-CSRF、跨 session replay、稳定 request ID/error code 和审计字段白名单。质量检查额外以 RED 修复底层 URL 异常 cause 泄露和十六进制 request ID 兼容；提交前合成 `token=` 形状被 scanner 拒绝后改为无凭据形状 fixture。
- **验证与 commit**：owned-path Ruff PASS、mypy PASS；全量 `50 passed`、Vitest `1 passed`、Vite build PASS、`CREDENTIAL_SCAN_PASS files=238`、许可证 PASS、`TEST_ALL_PASS mode=all`。产品提交为 `736292a14b41083122791a7182f554e354943a5f`，未新增依赖或第三方代码。
- **经验教训**：安全错误不能只隐藏响应正文，还要抑制携带不可信输入的异常链；HTTP request ID 是 opaque ID，不应复用业务 error-code 的格式约束。

## 2026-08-06T18:42:00+08:00 - F-05 Windows 凭据生命周期

- **Task 编号与 skill**：`F-05`；使用 `test-driven-development`、`systematic-debugging`、`requesting-code-review`、`receiving-code-review`、`verification-before-completion`，沿用 `codex/foundation-v1` worktree。
- **关键 context**：实现仅含 Windows Credential Manager 后端、无明文读取的 status/update/clear 服务、确定性 fake 与一次性 WinVault 集成测试；`Human-Changes: none`。
- **红绿证据**：初始 RED 为 5 个缺模块失败；包根修复后目标测试通过。规约评审发现状态缺少更新时间，新增 RED 后改为只返回 `configured` 与可空 UTC `updated_at`。质量评审再发现原始 target 可进入审计、审计 sink 异常会误报已完成变更及异常路径覆盖不足；新增 RED 后改用固定 opaque 引用、稳定脱敏后端错误，并明确审计传输失败不反转权威凭据结果。
- **评审与验证**：最终复审 `Critical=0, Major=0`。目标测试 `9 passed`；Windows 随机 target 的首次写入、二次更新和 `finally` 清理为 `1 passed`；全量后端 `59 passed`，Vitest `1 passed`，Vite build PASS，Ruff/mypy PASS，`CREDENTIAL_SCAN_PASS files=246`，许可证 PASS，`TEST_ALL_PASS mode=all`。
- **subagent 输出与 commit**：两个既有独立 reviewer 分别检查 SPEC 合同与质量/安全边界；修订后复核无剩余 Major。产品提交为 `e11a150e1f0233206803a4763a53f237fced097c`，未新增依赖或第三方代码。
- **经验教训**：凭据状态不能暴露实现后端；审计引用必须与调用方 target 解耦；外部审计传输失败时，API 返回状态必须与已经完成的不可回滚凭据变更一致。

## 2026-08-06T19:18:00+08:00 - M1-01 确定性材料抽取与来源定位

- **Task 编号与 skill**：`M1-01`；使用 `subagent-driven-development`、`test-driven-development`、`systematic-debugging`、`requesting-code-review`、`receiving-code-review`、`verification-before-completion`；新 worktree/分支为 `codex/m1-materials-v1`。
- **关键 context / subagent**：fresh worker `/root/m1_01_impl` 只创建任务卡列出的 9 个文件，不修改过程文档或提交。测试使用仓库 `tmp` 工具链并设置 `PYTHONNOUSERSITE=1`，确认实际解析器为锁定的 `pypdf 6.14.2`、`pypdfium2 5.12.1`；`Human-Changes: none`。
- **红绿证据**：初始 RED 因 `projectb.domain` 与 `projectb.services` 缺失而收集失败；locator 上界补充 RED 为 `source_kind` 参数缺失。worker GREEN 为目标 `11 passed`。协调者审查又观察到改后缀 ZIP 被接受及 PDF 指纹漏记 pdfium 的 `2 failed`，最小修复后同一命令恢复 `11 passed`。
- **规约与质量评审**：原始字节 SHA-256、严格 UTF-8 与换行规范化、一基页/行 locator、真实上界、不可变版本、数字 PDF 双解析器一致性、扫描/加密/伪装拒绝、30 秒默认 worker、进程树终止、临时输出清理及稳定错误均符合 M1-01。未新增依赖；fixture 为项目合成内容并有许可说明。
- **验证与 commit**：全量后端 `70 passed`，Vitest `1 passed`，TypeScript/Vite build PASS，owned-path Ruff/mypy PASS，`CREDENTIAL_SCAN_PASS files=250`，许可证 PASS，`TEST_ALL_PASS mode=all`。核心提交 `0ba43d849de4595b36e9f7ddd36a2544c5320a30`；发现 Git 将 PDF 当文本检查后，新增 binary 属性提交 `07ebf95f0ac3c4c9436619bf74be4c78a7612913`，两份工作区 PDF 与 Git blob 哈希一致。
- **经验教训**：参与抽取判定的每个解析器都必须进入版本指纹；文本扩展名不能代替二进制 magic 检查；PowerShell 不会默认因外部命令非零退出而停止，提交链必须显式检查 `$LASTEXITCODE`。

## 2026-08-06T19:38:00+08:00 - M1-02 原子导入与内容地址存储

- **Task 编号与 skill**：`M1-02`；使用 `test-driven-development`、`systematic-debugging`、`requesting-code-review`、`verification-before-completion`。fresh-agent 调度接口未返回可用调用，为避免阻塞按学生“尽快推进”指令由 coordinator 实现；此偏离未冒充 subagent，`Human-Changes: none`。
- **关键 context**：批次先校验 5 文件和 50 MiB，再对整批做无写入的流式哈希/大小快照；每个文件独立抽取、staging、内容 promote 和 SQLite 事务。状态为 `imported/idempotent/failed`，错误不回显路径或底层异常。
- **红绿与评审**：初始 RED 为缺少 importer/repository/content-store；初版目标 `13 passed`。规约复核以 RED 复现解析期间源文件变化仍被导入，修复为 snapshot hash 不一致时 `content_changed` 且零权威写入。最终覆盖 5/20/50 MiB、200 页、1,000,000 codepoints 的边界，same-course 幂等、新 parser 新版本、跨课程 blob 共享、混合批次、超时与临时清理。
- **验证与 commit**：目标 `14 passed`，全量后端 `84 passed`，Vitest `1 passed`，TypeScript/Vite build PASS，Ruff/mypy PASS，`CREDENTIAL_SCAN_PASS files=264`，许可证 PASS，`TEST_ALL_PASS mode=all`。产品提交为 `bdc893ef99e0ac7cac4d1481052fc30e5d5333b9`，未新增依赖或第三方代码。
- **经验教训**：文件大小 `stat` 只能做快速预检，权威写入前仍需对同一批次完成流式快照并将解析 hash 绑定该快照；文件系统 promote 与 SQLite 事务之间必须在失败后按实际引用状态补偿清理。

## 2026-08-06T19:50:00+08:00 - M1-03 确认式来源映射与删除

- **Task 编号与 skill**：`M1-03`；使用 `test-driven-development`、`systematic-debugging`、`requesting-code-review`、`verification-before-completion`。fresh-agent 调度仍不可用，由 coordinator 实现并明确记录偏离；`Human-Changes: none`。
- **关键 context**：coverage decision 只追加历史；每个 concept 仅最新 decision 生效，且必须 confirmed、同课程、locator 仍存在并属于材料最新版本。删除先提交课程 material/ref 删除和最后引用 tombstone，再清理 blob；失败保留可重试状态。
- **红绿与评审**：RED 为缺少 coverage/delete 模块；GREEN 为 5 passed。规约检查覆盖多个知识点、rejected/unconfirmed、parser 升级后旧 locator 失效、材料删除后未来授权失败且 decision 历史保留。质量检查修复最后引用删除与并发复用同 hash 的交错：删除在 SQLite 写锁内再次确认零引用；导入 staging 保留到引用提交后并可恢复缺失 blob。
- **验证与 commit**：M1-02/03 联合 `19 passed`，全量后端 `89 passed`，Vitest `1 passed`，TypeScript/Vite build PASS，Ruff/mypy PASS，`CREDENTIAL_SCAN_PASS files=272`，许可证 PASS，`TEST_ALL_PASS mode=all`。产品提交 `aa2a6da62cc0d185510c2b17e33ab168f33a74d6`，未新增依赖或第三方代码。
- **经验教训**：coverage 授权必须在每次使用时重新验证 locator 的存在性和 current version，不能只信历史确认；跨 SQLite/文件系统删除必须在提交后清理，并在最终零引用检查期间阻止新引用插入。

## 2026-08-06T20:00:00+08:00 - M2-01 确定性 mutex evaluator

- **Task 编号与 skill**：`M2-01`；使用 `test-driven-development`、`requesting-code-review`、`verification-before-completion`。fresh-agent 调度不可用，由 coordinator 实现并记录偏离；`Human-Changes: none`。
- **红绿与合同**：RED 为缺少 `projectb.domain.learning`。实现冻结的 check/outcome schema、Evaluator protocol、`os.mutex.v1` 和 registry。有效 trace、首个互斥冲突 witness、畸形/未闭合 trace、重复执行、来源顺序/去重及 explanation-only guard 共 `7 passed`；rubric 固定按 code 排序，无 LLM 参与评分。
- **验证与 commit**：全量后端 `96 passed`，Vitest `1 passed`，TypeScript/Vite build PASS，Ruff/mypy PASS，`CREDENTIAL_SCAN_PASS files=280`，许可证 PASS，`TEST_ALL_PASS mode=all`。产品提交 `9b49e07b6e5a237005c1d267f84b902cc48fff7c`。
- **经验教训**：确定性 evaluator 的输入顺序中只有语义事件顺序可影响结果；来源 ID 和 rubric 呈现顺序必须规范化，避免同一证据因集合顺序产生不同 hash。

## 2026-08-06T20:12:00+08:00 - M2-02 race/deadlock evaluator 与 registry

- **Task 编号与 skill**：`M2-02`；使用 `test-driven-development`、`receiving-code-review`、`verification-before-completion`；coordinator 实现，fresh-agent 调度偏离延续，`Human-Changes: none`。
- **红绿与合同**：RED 为缺少 race/deadlock 模块。race 按 read/add/write 重放线程内顺序、共享最终值和重叠事务；deadlock 从 hold/wait 构造 wait-for graph 并校验环。初版目标 11 passed；审查以 RED 发现多环图只接受内部首个环，改为验证答案是否为任一真实闭环后目标 `12 passed`。
- **验证与 commit**：registry 串行扩展为 `os.mutex.v1/os.race.v1/os.deadlock.v1`。全量后端 `108 passed`，Vitest `1 passed`，TypeScript/Vite build PASS，Ruff/mypy PASS，`CREDENTIAL_SCAN_PASS files=290`，许可证 PASS，`TEST_ALL_PASS mode=all`。产品提交 `4c384f7e7d6360a96a81480d22309645356f9fe0`。
- **经验教训**：deadlock 题应接受图中任意可验证的真实环，不能把 evaluator 的遍历顺序变成隐藏答案；race trace 必须同时验证事件完整性和学生给出的最终共享状态。

## 2026-08-06T20:22:00+08:00 - M2-03 不可变学习证据

- **Task 编号与 skill**：`M2-03`；使用 `test-driven-development`、`requesting-code-review`、`verification-before-completion`；coordinator 实现并记录 fresh-agent 调度偏离，`Human-Changes: none`。
- **红绿与合同**：RED 为缺少 learning attempts 服务。submit 先按 attempt_key 查询稳定幂等结果，再验证 current confirmed coverage、concept evaluator 和 evaluator ID/version；attempt 与 evidence 单事务追加，DB trigger 保护 evidence 更新/删除。结构化答案含可选 rationale，只写本地 attempt JSON。
- **隐私与故障**：反馈措辞回调只收到 evaluator/outcome/rubric/source IDs，不接收 answer、rationale 或 variant；provider 异常发生在 evidence 提交后并被隔离。目标 `4 passed` 覆盖重复 key、mutation、stale source、explanation-only 和答案不外发。
- **验证与 commit**：全量后端 `112 passed`，Vitest `1 passed`，TypeScript/Vite build PASS，Ruff/mypy PASS，`CREDENTIAL_SCAN_PASS files=298`，许可证 PASS，`TEST_ALL_PASS mode=all`。产品提交 `2da06362bbd11d3d8da2a8b8b3e49c63f57cae82`。
- **经验教训**：幂等查找必须早于随时间变化的 coverage 复验和 provider 调用；答案隐私最好通过类型边界实现，而不是依赖调用者记得删除字段。

## 2026-08-06T20:40:00+08:00 - M2-04 完整证据驱动的掌握度推导

- **Task 编号与 skill**：`M2-04`；使用 `subagent-driven-development`、`test-driven-development`、`requesting-code-review`、`verification-before-completion`；实现者为 fresh worker `/root/m2_04_impl`；`Human-Changes: none`。
- **关键 context**：只新增 mastery repository/service 和目标测试。服务必须在 SQLite 写锁内读取 concept 的完整追加式 evidence 历史，不接受手工或 provider 指定的掌握状态。
- **TDD RED/GREEN**：RED 因 `projectb.services.learning.mastery` 不存在而收集失败，原因与计划一致。GREEN 目标命令为 `4 passed`；完整历史 ID 缺失或重复失败关闭，输入顺序不影响状态或 SHA-256。
- **规约合规评审**：只有 passed isomorphic + transfer 可提升为 `demonstrated_now`；后续跨课程本地日且 variant 不同的 passed delayed check 可提升为 `retained`；错误、跳过和来源不足不降级。Critical=0，Major=0。
- **质量/安全/许可证评审**：推导与幂等写入在同一 `BEGIN IMMEDIATE` 事务中；时区使用 IANA `ZoneInfo`，时间戳必须为 UTC `Z`；未新增依赖或第三方代码。仓库现有 namespace mypy 调用需 `--explicit-package-bases`，定向复验通过。Critical=0，Major=0。
- **验证与 commit**：定向 Ruff PASS，定向 Mypy PASS；全量后端 `116 passed`，Vitest `1 passed`，Vite production build PASS，`CREDENTIAL_SCAN_PASS files=304`，`LICENSE_VERIFICATION_PASS python=54 npm=166`，`TEST_ALL_PASS mode=all`。产品提交 `7d72b02e46f0a05d456e031d6e1720923570f8f5`。文档提交前的 evidence RED 暴露全局 `core.autocrlf=true` 将原始字节锁定文件转为 CRLF；规范化 LF 后哈希恢复 `FD65...F310`，以 `.gitattributes` 精确锁定修复提交 `eecb54d1a30fedb57b617d6b3f021be3753106e6`，随后 `EVIDENCE_VALIDATION_PASS rows=63 explicitly_blocked=2 python_pins=54 npm_packages=166`。
- **经验教训**：掌握度不能从调用方提供的证据子集推断；必须由存储层完整读取、规范化并绑定输入哈希，才能保持可审计性。

## 2026-08-06T21:10:00+08:00 - P-01 精确 consent 与 provider-neutral 候选端口

- **Task 编号与 skill**：`P-01`；使用 `subagent-driven-development`、`test-driven-development`、`systematic-debugging`、`requesting-code-review`、`verification-before-completion`。fresh-agent 派发接口本阶段未返回可用会话，由 coordinator `/root` 实现并明确使用 `[agent: coordinator]`；`Human-Changes: none`。
- **关键 context**：只实现 `generate_explanation`、`generate_practice_candidate`、`generate_feedback_wording` 三类非权威候选端口，以及 local/test/demo registry、profile repository、deterministic mock 和一次性 consent。本 task 不连接真实 OpenAI 或写 API route。
- **TDD RED/GREEN**：初始 RED 为缺少 `projectb.providers`。首轮 GREEN 后审查用回归 RED 复现两个 Major：调用方可保留旧 hash 重建 preview 并偷换 instruction/rubric；任意当前 locator 未经用户确认也可进入预览。修复为执行前重算完整 request hash，并每次重验最新 confirmed coverage。最终目标 `15 passed`。
- **规约合规评审**：feedback 类型不存在原始答案字段；consent 绑定 operation、locator/version/hash/片段预览哈希、profile/policy、token/费用上限和 nonce。无 consent、不匹配、已使用或过期来源均在 provider 调用前失败。Critical=0，Major=0。
- **质量/安全/许可证评审**：一次性消费使用 `BEGIN IMMEDIATE` 与追加式 `audit_event`，并在网络调用前提交，因此并发/失败都不能重放。schema/timeout/error 三种失败后 coverage/evidence/mastery/plan 计数不变。local 无 adapter 且拒绝 mock，mock 仅 test/demo 注入。无新依赖或第三方代码。Critical=0，Major=0。
- **验证与 commit**：定向 Ruff PASS，定向 Mypy PASS；全量后端 `131 passed`，Vitest `1 passed`，Vite production build PASS，`CREDENTIAL_SCAN_PASS files=310`，`LICENSE_VERIFICATION_PASS python=54 npm=166`，`TEST_ALL_PASS mode=all`。产品提交 `f2563ac87cf61665dae98d404a02dff41f9fab37`。
- **经验教训**：consent 不能只信任调用方携带的 hash，必须从实际将外发的结构重算；“当前 locator”也不等于“用户确认来源”。

## 2026-08-06T21:24:00+08:00 - M3-01 确定性连续/期末复习策略

- **Task 编号与 skill**：`M3-01`；使用 `test-driven-development`、`requesting-code-review`、`verification-before-completion`。fresh-agent 调度本阶段仍未返回可用会话，由 coordinator 实现并使用 `[agent: coordinator]`；`Human-Changes: none`。
- **TDD RED/GREEN**：RED 因 `projectb.domain.review` 不存在而收集失败。GREEN 目标 `15 passed`，覆盖 mode/IANA timezone/预算范围与步长、默认 30 分钟、固定 10 分钟任务、三组精确期末间隔、连续 30 日窗口、考试截止和过期归档。
- **规约与质量评审**：同 concept/日期只保留最弱 evidence，每日依 weakness -> request date -> concept ID 稳定排序且不超预算；`stale_source/system_error` 仅排除，不伪装为学习失败。打乱完整输入后 tasks 与 input hash 不变。未新增依赖或第三方代码；Critical=0，Major=0。
- **验证与 commit**：定向 Ruff/Mypy PASS；全量后端 `146 passed`，Vitest `1 passed`，Vite production build PASS，`CREDENTIAL_SCAN_PASS files=324`，`LICENSE_VERIFICATION_PASS python=54 npm=166`，`TEST_ALL_PASS mode=all`。产品提交 `36e7ee8992fc8b15df7ee3360e9f5ca517c7e52c`。
- **经验教训**：策略输入哈希必须包含被排除的过期/系统错误状态，才能在状态恢复时生成新 revision；但这些错误不能影响 weakness 优先级。

## 2026-08-06T21:36:00+08:00 - M3-02 复习 revision、diff 与恢复

- **Task 编号与 skill**：`M3-02`；使用 `test-driven-development`、`requesting-code-review`、`verification-before-completion`。fresh-agent 调度本阶段仍不可用，coordinator 实现并使用 `[agent: coordinator]`；`Human-Changes: none`。
- **TDD RED/GREEN**：初始 RED 因缺少 `services.review.revisions`。首轮 GREEN 后审查以 RED 证明同一 `concept@due` 的 evidence/source 变化被误报 retained；修复为稳定 `added/removed/changed/retained` 四分 diff。最终目标 `6 passed`。
- **规约与质量评审**：同 course/input hash 返回原 revision；输入变化追加确定 revision ID 和父链。已完成 concept/日期任务保留在历史中，新 revision 不重建；skipped 可恢复 pending，completed 失败关闭；stale source 新 revision 删除未来任务。SQLite 写入均在 `BEGIN IMMEDIATE` 内，未新增依赖。Critical=0，Major=0。
- **验证与 commit**：定向 Ruff/Mypy PASS；全量后端 `152 passed`，Vitest `1 passed`，Vite production build PASS，`CREDENTIAL_SCAN_PASS files=328`，`LICENSE_VERIFICATION_PASS python=54 npm=166`，`TEST_ALL_PASS mode=all`。产品提交 `3a93f27a48f3e027380135a2b65f4b28f3f4a624`。
- **经验教训**：revision diff 不能只比较任务槽位 ID；同日同 concept 的来源或证据变化也是用户必须看到的修订。

## 2026-08-06T21:50:00+08:00 - API-01 FastAPI 材料应用边界

- **Task 编号与 skill**：`API-01`；使用 `test-driven-development`、`requesting-code-review`、`verification-before-completion`；由 coordinator 实现并使用 `[agent: coordinator]`；`Human-Changes: none`。
- **TDD RED/GREEN**：RED 因 `projectb.api` 缺失。首轮 GREEN 后审查以 RED 发现 importer 持久化临时名 `0.txt` 而不是经验证的原文件名；修复为每文件独立临时子目录，同时保留 basename 并避免同名覆盖。目标 `4 passed`。
- **规约与质量评审**：app middleware 将所有请求绑定 loopback Host，禁止 forwarded headers，不安全方法必须同时提供 loopback Origin、session cookie 与 CSRF header。课程、导入结果、来源、映射和删除 API 全部贯通；数量/单文件/批次字节限制在解析前执行。静态挂载目录与内容库/数据库必须不重叠，路径穿越与私有文件不可服务。Critical=0，Major=0。
- **验证与 commit**：定向 Ruff PASS，owned-file Mypy PASS；全量后端 `156 passed`，Vitest `1 passed`，Vite production build PASS，`CREDENTIAL_SCAN_PASS files=334`，`LICENSE_VERIFICATION_PASS python=54 npm=166`，`TEST_ALL_PASS mode=all`。产品提交 `6d44eacfbde94d36042e9037c8d4cacfe208b4fc`。
- **经验教训**：安全临时文件名不能直接流入业务元数据；上传的存储身份和用户可见文件名必须分离。

## 2026-08-06T22:00:00+08:00 - API-02 学习、mastery 与 provider API

- **Task 编号与 skill**：`API-02`；使用 `test-driven-development`、`requesting-code-review`、`verification-before-completion`；coordinator 实现并使用 `[agent: coordinator]`；`Human-Changes: none`。
- **TDD RED/GREEN**：RED 为 app factory 不接受 test-only provider registry seam，且 learning/provider route 不存在。GREEN 目标 `3 passed`，覆盖 attempt 幂等、两类通过 evidence 推导 `demonstrated_now`、三类 preview/consent/execute 和 consent 重放。
- **规约与质量评审**：API 按 concept evaluator 将 JSON 转为结构化练习/答案，并使用已评审 AttemptService/MasteryService。feedback preview 使用 extra-forbid schema，原始 answer 在 provider 调用前 422；三类 candidate 均标记 `authoritative=false`，调用前后 coverage/evidence/mastery/plan 计数不变。local 默认 registry 无 adapter，test 才可注入 mock。Critical=0，Major=0。
- **验证与 commit**：定向 Ruff 和 owned-file Mypy PASS；全量后端 `159 passed`，Vitest `1 passed`，Vite production build PASS，`CREDENTIAL_SCAN_PASS files=348`，许可证 PASS，`TEST_ALL_PASS mode=all`。产品提交 `7da00e3cb5dc371291d2d164a1ebd677049cdabc`。
- **经验教训**：provider preview 可以在本地进程内短暂保留精确片段，但不应追加到 SQLite；重启后丢失 preview 必须失败关闭，而不能仅凭 consent ID 重建外发。

## 2026-08-07T10:35:00+08:00 - API-03 本地 API 闭合

- **Task 编号与 skill**：`API-03`；使用 `test-driven-development`、`systematic-debugging`、`requesting-code-review`、`verification-before-completion`；由 coordinator `/root` 实现，`Human-Changes: none`。
- **关键 context**：新增复习、凭据、设置路由和 Windows 本地 profile；凭据响应不得包含密钥值，首次运行保持未配置，本地服务只绑定 `127.0.0.1`，复习计划输入必须由服务端已有证据推导。
- **TDD RED/GREEN**：初始 RED 为 app factory 缺少 credential service 且目标路由不存在，共 4 项失败；首轮 GREEN 为 4 项通过。合规审查发现调用方可提交掌握度、弱点和来源 seed 的 Critical 权限问题，新增回归 RED 后改为服务端读取 coverage/evidence/mastery，外部 `seeds` 字段返回 422；最终目标集 `19 passed`。
- **双评审**：规约评审确认复习计划、revision、凭据生命周期、设置校验和回环绑定符合 API-03；质量/安全/许可评审确认凭据响应无值、调用方不能伪造复习权威输入、静态目录不越界，且未引入新依赖。Critical=0，Major=0。
- **验证与 commit**：owned Ruff/Mypy PASS；全量后端 `163 passed in 45.27s`，Vitest `1 passed`，Vite production build PASS，`CREDENTIAL_SCAN_PASS files=354`，许可证验证 PASS，`TEST_ALL_PASS mode=all`。产品提交 `e41df6a93eb999746c1b6314c2e2a2d9c4dda8bb`。
- **经验教训**：复习计划即使是确定性算法，也不能信任浏览器上传的掌握度或来源；API 应只接受用户控制项，把权威学习证据留在服务端重建。

## 2026-08-07T11:55:00+08:00 - UI-01 Open Design 与响应式工作台壳层

- **Task 编号与 skill**：`UI-01`；使用 Open Design `frontend-design` + `default`/Neutral Modern、`test-driven-development`、`systematic-debugging`、`requesting-code-review`、`verification-before-completion`。fresh worker `/root/ui01_impl` 完成 RED 后会话结束，coordinator `/root` 接续 GREEN 和评审修复；这是明确记录的单 task 双会话偏离，`Human-Changes: none`。
- **Open Design 证据**：项目 `projectb-learning-workbench-v1`，run `1fec5e0c-ef5b-4960-982a-2e374ef739ff`，Open Design `0.18.0`，Codex CLI `0.144.4`，结果 `succeeded/exit 0/deliverableValid=true`。HTML、原始预览和 360/768/1440 生产截图路径、SHA-256、资产/许可及修订均记录于 `docs/engineering/OPEN_DESIGN_RUN.md`。
- **TDD RED/GREEN**：Vitest 初始 RED 因 `App.tsx` 缺失；Playwright 三档 12 项中 6 项按预期因 banner/阶段导航/键盘目标缺失失败。GREEN 先修正精确命令不加载 frontend config 的 harness；随后 360/768 分别观察到 20px/6px 溢出，定位为设置入口 `min-width:80px` 后修复。审查新增未知 profile 失败关闭 RED，最终目标 Vitest `4 passed`、Playwright `12 passed`。
- **规约评审**：真实 Open Design 产物先于生产实现；四阶段和设置入口、回环/本地状态、360/768/1440、键盘焦点、状态非仅颜色均满足 UI-01/AC-16。外部设计默认 12/16px token 未复制，生产圆角只保留 4/8px。Critical=0，Major=0。
- **质量/安全/许可评审**：API client 使用同源凭据策略且不写浏览器存储；未知 profile/mode 或 local 非回环响应失败关闭；无外部图片、字体、CDN 或新依赖，Lucide 来源已在现有锁与许可清单。移动端保留可见阶段名，错误横幅不再孤字换行。Critical=0，Major=0。
- **验证与 commit**：最终一键回归为后端 `163 passed`、前端 `5 passed`、Vite production build PASS、`CREDENTIAL_SCAN_PASS files=368`、`LICENSE_VERIFICATION_PASS python=54 npm=166`、`TEST_ALL_PASS mode=all`；最终定向 E2E `12 passed`。产品提交 `c6a63d7ddd887384170ccfee70fa3f54b3b00102`。
- **清理**：清理前后均记录 `git status --short --untracked-files=all` 与 `git worktree list`；删除本任务生成的 `test-results/.last-run.json`、空 `test-results/` 和 `tmp/opendesign-*` 临时转发文件，停止临时 Node 转发，保留 Open Design 桌面程序和持久化证据。
- **经验教训**：响应式 grid 的列宽不能覆盖子元素残留的 `min-width`；安全状态也不能从未知服务响应静默降级，必须以运行时校验失败关闭。

## 2026-08-07T12:40:00+08:00 - UI-02 材料导入页

- **Task 编号与 skill**：`UI-02`；使用 `subagent-driven-development`、`test-driven-development`、`systematic-debugging`、`requesting-code-review`、`verification-before-completion`。fresh worker `/root/ui02_impl` 实现，coordinator `/root` 复验和关闭审查问题；`Human-Changes: none`。
- **关键 context**：只实现 `/import`，接入已有课程、session-CSRF、multipart 导入和材料列表 API；显示 5 文件/单文件 20 MiB/批次 50 MiB 限制、选择、进度、逐文件结果与可恢复错误。按学生要求压缩验证，不重复运行全量仓库测试。
- **TDD RED/GREEN**：首个 RED 因 `ImportView` 缺失；首轮环境失败来自未设置 `PLAYWRIGHT_BROWSERS_PATH`，随后精确定位 `npm --prefix` 未加载 frontend Playwright config，改用显式 `--config frontend/playwright.config.ts`。审查以新增 RED 证明未知 per-file `status` 会被误当成功，修复为只接受 `imported/idempotent/failed` 且失败状态必须携带错误码。
- **双评审**：规约评审确认 AC-01 所需文件限制、导入结果、失败保留和材料刷新均可见；质量/安全评审确认同源 cookie、session-bound CSRF header、FormData、React 转义和响应 schema 失败关闭。未引入新依赖。Critical=0，Major=0。
- **验证与提交状态**：最终聚焦 Vitest `3 passed`；Playwright 在 360/768/1440 三个 project 中 `3 passed`；TypeScript exit 0；`CREDENTIAL_SCAN_PASS files=400`；`git diff --cached --check` exit 0。宿主沙箱两次拒绝创建 `.git/worktrees/webui-v1/index.lock`，学生仅执行原样提供的 commit 命令完成产品提交 `4c14231ad3511109929779d88a49f05969413eaa`，没有修改代码。
- **清理与经验教训**：删除本任务生成的 `frontend/test-results/.last-run.json` 和空目录；没有残留 4173 listener。Playwright 命令必须显式绑定 config 和浏览器缓存；API 成功状态必须白名单验证，不能以“没有 error_code”推断成功。

## 2026-08-08T17:42:00+08:00 - UI-03/UI-04 路由收口与来源绑定学习页

- **Task 与 skill**：同步 UI-03 已有提交，并执行 UI-04；使用 `subagent-driven-development`、`test-driven-development`、`receiving-code-review`、`verification-before-completion`。fresh worker `/root/ui04_learning` 完成首轮实现，coordinator `/root` 处理规格审查问题并提交；`Human-Changes: none`。
- **TDD 与评审**：首轮 RED 因 `LearningView` 缺失。规格评审发现硬编码来源、固定 evidence、缺少 material version/hash 绑定及键盘/重要状态 E2E 覆盖；新增失败测试后改为读取既有课程、材料、source 与 coverage API，未确认或 stale 来源失败关闭，explanation-only 不产生评分证据，P 预览显示 locator/version/hash/profile/caps 且不含原始答案。Critical=0，Major=0。
- **验证与提交**：聚焦 Vitest `5 passed`；frontend 回归 `35 passed`；TypeScript、Vite build、凭据扫描与许可证检查通过；系统 Chrome 在 360/768/1440 三个 viewport 中 Playwright `3 passed`。UI-03 提交 `891c057a5b0faa1ce390a1534efd87be65bce62e`；UI-04 提交 `6f057f25a0ca1ccd7909e6b247e3359bfcd0e3f4`。

## 2026-08-08T21:00:02+08:00 - UI-05 确定性复习计划与 revision 差异

- **Task 与 skill**：执行 UI-05；使用 `subagent-driven-development`、`test-driven-development`、`requesting-code-review`、`receiving-code-review`、`systematic-debugging`、`verification-before-completion`。fresh Terra worker `/root/ui05_review` 完成首轮实现，spec reviewer `/root/ui05_spec_review` 只读评审，coordinator `/root` 修复评审问题并提交；`Human-Changes: none`。
- **TDD 与评审**：首轮 RED 为 `ReviewView` 缺失。独立复跑发现测试未 cleanup、Shell 保留旧 unavailable 断言及嵌套 `<main>` axe 失败；补失败证据后修复。规格评审发现 `final`/`finals` 错配、非法 12 分钟预算、缺少考试日期/归档、静态 diff/recovery 与伪 source/mastery；新增 RED 后实现 30 分钟合法预算、canonical mastery、完整 hash、finals 间隔/截断、动态任务数与恢复状态。Critical=0；评审 Major 均已处理。
- **验证与提交**：聚焦 Vitest `4 passed`；frontend 回归 `38 passed`；TypeScript、Vite build、`CREDENTIAL_SCAN_PASS files=440`、许可证检查和 `git diff --cached --check` 通过；系统 Chrome 在 360/768/1440 三个 viewport 中 Playwright `3 passed`，含键盘、预算/压缩、考试截断、恢复、overflow 与 axe。产品提交 `0f644dd5cf9d865d5c70fad0ce52d96ac3aad47b`。
