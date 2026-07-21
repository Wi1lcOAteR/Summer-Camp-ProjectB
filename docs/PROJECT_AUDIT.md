# 项目启动审计与课程差距

初次审计时间：2026-07-17T18:14:41+08:00
最近历史复查时间：2026-07-19T21:57:09+08:00
最近外部门禁复查：2026-07-21T21:08:02+08:00（G-01 scope correction）
最近文档一致性复查：2026-07-22T02:55:19+08:00（Superpowers cache-only 状态纠正）

> 当前要求符合性请以 [`REQUIREMENTS_COMPLIANCE_AUDIT.md`](REQUIREMENTS_COMPLIANCE_AUDIT.md) 为准。本文件前半部分保留启动阶段的历史快照，不能用其中“SPEC 不存在”“Open Design 未安装”等旧状态判断当前工作区。

## 当前权威状态（2026-07-22）

- 项目处于阶段 B 的工程证据与计划门禁收口期，尚未进入正式实现。
- `SPEC.md` 已由学生整体确认；`PLAN.md` 已形成，但正式 `superpowers:writing-plans` 调用证据仍缺，现有计划明确标记为 fallback。Superpowers 6.1.1 只是完整 cache payload，当前 config 无安装/启用项、task 无相应 skill；D-001 已重新开放。
- Open Design 0.15.1、Codex MCP、完整内置 `frontend-design` 和学生选择的 `default`（Neutral Modern）均已验证，G-01 已 PASS。该 bundled skill 不需要另行下载到 Codex；Open Design 也不需要无任务时长期保持开启。
- `list_projects=[]` 与 `get_active_context.active=false` 是实现前的正常状态。真实 project/run/artifact 只在冷启动完成且学生批准实现后的 UI-01A 中按需创建，不能提前生成 UI 来冒充环境验证。
- G-02A 工具链/依赖/许可证与 G-02B provider 政策/费用证据已分别 PASS；G-02C 已验证 freezer、OCI base 与 HF runtime 条件，但当前官方付费方案要求触发 D-025，仍为 pending。2026-07-22 已补充现有主机/Tailscale 和 Azure Students/Container Apps 的官方候选比较；没有选择或创建托管资源。
- 当前硬门禁是 D-025/G-02C、正式 `writing-plans` 证据或课程明确接受 fallback、不同类型全新 session 的 G-03 冷启动，以及冷启动修订后的学生实现批准。

## 启动时结论（历史）

项目当时处于阶段 A 的需求澄清，不是实现阶段。仓库没有源码或项目规约；当时仅凭 Superpowers v6.1.1 cache 与核心 skill 文件存在而记为“已安装”，但本次会话未将其注册到可调用清单。该安装判断已由 2026-07-22 的四层证据复核纠正为 cache-only。Open Design v0.15.0 安装器当时已下载并通过本地校验文件核对，尚未安装或接入。

## 启动时仓库现状（历史）

| 项目 | 状态 | 证据 / 影响 |
| --- | --- | --- |
| 课程原文 | 已读取 | 通用要求与 B 类要求均存在于 `docs/requirements/` |
| 约束与 skill 准备 | 已读取 | 根目录 `AGENTS.md`、`SKILLS_SETUP.md` |
| 既有源码 | 不存在 | 启动盘点仅发现文档和 `.codex/config.toml` |
| Git | 已初始化，操作受限 | `git init` 成功；沙箱账号触发 `dubious ownership`，未写全局例外 |
| SPEC | 不存在（正确） | mandatory brainstorming 未调用，禁止伪造 |
| PLAN | 不存在（正确） | SPEC 未确认，阶段 B 未开放 |
| 冷启动验证 | 尚未执行 | SPEC/PLAN 均未完成 |
| 实现 / 测试 / CI | 尚未执行 | 实现门禁未满足 |

## 启动时 Skill 与工具状态（历史）

### Superpowers

- 当时会话暴露的 skills 中没有 `superpowers:*`，但官方插件缓存存在 Superpowers v6.1.1（MIT）及完整核心 skill 目录。
- 已检测：`brainstorming`、`writing-plans`、`using-git-worktrees`、`subagent-driven-development`、`executing-plans`、`test-driven-development`、`requesting-code-review`、`receiving-code-review`、`systematic-debugging`、`verification-before-completion`、`finishing-a-development-branch`，以及 `using-superpowers`、`dispatching-parallel-agents`、`writing-skills`。
- 官方仓库在 2026-07-19 复核显示最新版本为 v6.1.1；本地插件 manifest 同样为 v6.1.1。
- 官方 Codex 安装：App 侧栏 Plugins → Coding → Superpowers → `+`，或 CLI `/plugins` 搜索安装。
- 应检测的核心 skills：`brainstorming`、`writing-plans`、`using-git-worktrees`、`subagent-driven-development` / `executing-plans`、`test-driven-development`、`requesting-code-review`、`receiving-code-review`、`systematic-debugging`、`verification-before-completion`、`finishing-a-development-branch`。

### Open Design

- 当时未找到 `od` 命令、Open Design skill 或 MCP；MCP resources/templates 均为空。该历史缺口已由上方“当前权威状态”取代。
- D-024 已确认采用“安装并使用 Open Design”，因此该缺口不再是产品选择问题，而是正式 UI 前必须满足的外部环境门禁。
- 官方 release：v0.15.0（2026-07-14，commit `79e257d`），Apache-2.0，提供 Windows x64 安装器。
- 本地安装器大小 309,298,247 bytes；SHA-256 与同名 `.sha256` 一致，值为 `63fc2e609489474e99187cdf94d01d063c1dbee733aaf2464d835cdc1e96f6b5`；Authenticode 状态为 `NotSigned`，与上游 Windows 未签名发布说明一致。
- 官方说明支持 Codex，接入命令为 `od mcp install codex`，也支持 `--print` 预览配置。
- 安装器当时已下载但未运行。当时环境只允许写项目目录，无法合规完成会写入用户/系统目录且可能触发 SmartScreen 的安装；该历史缺口现已解除。

### 本地开发工具

| 工具 | 状态 |
| --- | --- |
| Git | 2.55.0.windows.3 |
| Node.js | 24.14.0 |
| npm | 已安装；`npm.ps1` 被执行策略阻止，后续应使用 `npm.cmd` |
| pnpm | 11.9.0 |
| Python | 3.13.5 |
| uv | 0.11.14 |
| Docker | CLI 29.1.2；沙箱无法读取用户 Docker config，daemon 尚未验证 |
| GitHub CLI (`gh`) | 未找到 |
| Gitleaks | 未找到 |
| Claude Code | 未找到 |
| Open Design (`od`) | 未找到 |

## 启动时课程差距（历史）

| 课程要求 | 当前状态 | 下一合规动作 |
| --- | --- | --- |
| Superpowers 全流程 | **当时误判**为插件已安装；实际只有 cache，本会话未注册 | 该历史判断已由 `SUPERPOWERS_VALIDATION.md` 纠正；须 App 安装/启用并新建 task |
| 真实、有用、至少 3 模块 | 未定义 | brainstorming 先确定真实用户与痛点，再验证模块边界 |
| 5+ INVEST 用户故事 | 缺失 | 在用户确认问题方向后逐项形成 |
| WebUI + Open Design | 安装器已验证，工具尚未安装 | 用户运行安装器后执行 `od mcp install codex`；在 SPEC 确认 design system/skill |
| 凭据威胁模型 | 缺失 | 根据是否使用鉴权 API 在 SPEC 定稿 |
| 分发与公网部署 | 缺失 | 在 SPEC 选择容器/二进制/包及部署平台 |
| TDD、一键测试 | 未到阶段 | PLAN 为每项指定失败测试与验证命令后实施 |
| GitLab CI `unit-test` | 缺失 | 技术栈确认后按 TDD 实现，不提前生成空壳证据 |
| 冷启动验证 | 缺失 | PLAN 后用不同类型智能体，仅传 SPEC/PLAN |
| README / REFLECTION | 缺失 | README 随实现维护；REFLECTION 仅由学生撰写 |
| PR/MR 与最终 CI pass | 缺失 | 实现阶段按 worktree/task 推进，远程动作需用户批准 |

## 已验证与未验证边界

- **已验证**：文件存在性与内容、工具命令可发现性、列出的本地版本、官方 release/安装/许可证信息、`git init` 的实际结果。
- **未验证**：任何业务行为、测试、构建、Docker daemon、CI、正式 Gitleaks 扫描、WebUI、云部署、远程仓库与冷启动智能体。

## 持续 Goal 完成审计（2026-07-17T18:19:47+08:00）

| 明确要求 | 权威证据 | 当前判定 |
| --- | --- | --- |
| 完整读取四类启动材料 | `AGENT_LOG.md` PRE-001 与已提交原文 | 已完成 |
| 检查开发环境 | PRE-001 工具版本输出与本审计 | 已完成；Docker daemon 等实现期能力未验证 |
| 检查 Superpowers 并列出相关 skills | PRE-001、PRE-004；插件和 skill 目录复查均为 `none` | 已完成检查；安装/可用性未达成 |
| 进入正确 Superpowers 阶段 | 必须实际调用 `superpowers:brainstorming` | 未达成；skill 不可用 |
| 检查 Open Design | PRE-001、PRE-004；`Get-Command od` 为 `none` | 已完成检查；安装未达成 |
| 梳理课程差距 | 本文件“主要差距”矩阵 | 已完成当前状态梳理 |
| 完成当前阶段所有无需决策工作 | 日志、审计、决策清单、Git 基线、凭据启发式扫描 | 已完成已识别的安全工作；等待门禁外部状态变化 |
| 持续沉淀 SPEC | 合规证据必须来自 brainstorming 与用户确认 | 尚不能开始；不得用模板冒充 |
| 生成 PLAN | 用户确认 SPEC + `writing-plans` | 门禁未开放 |
| 冷启动验证 | 不同类型新 session，仅提供 SPEC/PLAN | 门禁未开放 |
| 实现与 TDD | 实现门禁全部满足 + 用户批准 | 门禁未开放 |
| 最终课程交付全部完成 | 文件、测试、构建、CI、部署 URL、学生反思等逐项证据 | 远未完成，持续 Goal 必须保持活动状态 |

### 本轮结论

当前没有可以在不调用 mandatory brainstorming、不给产品方向做重大猜测、且不制造空壳交付物的进一步规约工作。下一有效动作仍是用户在 Codex App/CLI 安装 Superpowers 并新建会话；Open Design 可随后按 `DECISIONS_NEEDED.md` 安装。

### 第三次阻塞复查（2026-07-17T18:21:22+08:00）

Superpowers 插件、核心 skills 与 Open Design 仍均为 `none`。这是连续第三次相同结果，且没有新的用户决策或外部状态变化；当前完成审计仍显示 mandatory brainstorming 是所有后续工作的最早未满足前置条件。因此持续 Goal 应暂停为 blocked，恢复条件是安装 Superpowers、开启能暴露其 skills 的新会话并重新读取本仓库约束。

### 外部状态恢复（2026-07-17T22:05:24+08:00）

- 当时把“Superpowers v6.1.1 已进入官方 Codex 插件缓存且核心 skills 完整”记录为安装/前置恢复；2026-07-22 复核证明 cache 不等于 installed/enabled，该历史结论已被纠正。
- 已完整读取 `using-superpowers` 与 `brainstorming` skill，并保持“用户批准设计前不得实现”的硬门禁。
- Open Design 仍未安装。自动下载受 GitHub 网络连接与内置浏览器超时阻塞，用户改为手动下载官方 v0.15.0 安装器；安装后继续 MCP 接入验证。

### 2026-07-19 复查（历史）

- 完整复读根目录约束、课程通用要求、B 类要求、全部已有项目文档与 Git 历史；仓库仍无源码、`SPEC.md` 或 `PLAN.md`。
- Superpowers v6.1.1 缓存和 14 个 skills 均存在；本次任务的可调用 skill 清单没有注册它们。已完整读取 `using-superpowers` 与 `brainstorming`，按其清单续接阶段 A，并在日志保留证据限制。
- Open Design v0.15.0 官方 release、Windows x64 资产、本地哈希一致性与未签名状态已核对；`od`/MCP 均不存在。安装因工作区外写入限制交由用户处理，不重复尝试提权。
- Git 工作区原本只有两份 Open Design 下载文件未跟踪；已精确加入 `.gitignore`，防止大文件误提交。

### 阶段 A 交付边界更新（2026-07-20；历史快照）

学生对 D-017 至 D-024 全部选择方案 A，最新 `SPEC.md` 已把这些选择收敛为规约。下表区分“文档已覆盖”与“已有实现/运行证据”；后者当前仍为空。

| 决策 | 已确认方向 | 截至当时的证据边界 |
| --- | --- | --- |
| D-017/D-018 OpenAI 边界 | 首版唯一真实实现为内置 OpenAI adapter，并保留 deterministic mock/contract；不接受任意 endpoint/plugin | **截至 2026-07-20 的历史快照**：只有合同与官方政策研究；OpenAI Python SDK 许可证/精确版本尚未核验，P/F 真实集成测试尚未执行。当前 G-02A 已核验精确包/许可证；P/F 集成仍未执行 |
| D-021 + 分发方向 | D-021 确认 Windows x64、Python/FastAPI + React/Vite、SQLite、Credential Manager；整体 SPEC 已确认单文件 `ProjectB.exe` 方向 | 无依赖/源码/凭据测试/冻结构建/干净机/SmartScreen 证据；不得把方向确认冒充实现完成 |
| D-022 + 部署方向 | D-022 确认许可夹具 + mock/无真实 key；整体 SPEC 已确认 OCI、HF Spaces、无上传/egress、隔离 session/限额方向 | **截至 2026-07-20 的历史快照**：无镜像/build/run/URL/隔离证据；官方页面 502/curl 超时。该网络阻塞后来关闭，当前 HF 付费方案冲突与 D-025/G-02C 状态以当前证据为准 |
| D-023 远程仓库/CI | NJU Git/GitLab 主仓 + GitHub 镜像；GitLab `unit-test` + GitHub Actions 双 CI | 当前没有远程 push、PR/MR、镜像或 CI 运行；这些动作仍需执行当时的用户授权 |
| D-024 Open Design | 0.15.1 桌面端与 MCP 已注册；学生已选择完整内置 `frontend-design` + `default`（Neutral Modern） | fresh MCP `list_skills` 成功；`projects=[]`、`active=false` 是实现前正常状态。G-01 环境门禁已 PASS；真实 project/run/artifact 和正式 UI 证据后置 UI-01A |

OpenAI 的 Responses 能力/政策快照还须在每次 P/F 同意前刷新并记录，覆盖 application state、abuse monitoring、prompt cache、文件审查例外和 Files/Vector Stores 生命周期；`store:false` 不得表述为 ZDR。

详细拓扑、分发完成标准、公开 demo 隔离/限额、依赖许可证门禁与远程操作边界见 [`research/TECH_STACK_DISTRIBUTION_BASELINE.md`](research/TECH_STACK_DISTRIBUTION_BASELINE.md)。这些选择解决了产品/交付方向问题，但不能充当实现或最终课程交付证据。

### 阶段 B 更新（2026-07-20T18:45:26+08:00）

- `PLAN.md` 已按缓存的上游 `writing-plans` v6.1.1 规则通过透明 fallback 生成：41 个 planning group 展开为 69 个 dispatch unit；宽 group 明确不可派发，unit 包含文件、依赖/并行关系、红测或失败门禁、验证命令、双评审、literal commit 和完成标准。当前会话未注册正式 `superpowers:writing-plans`，所以该调用证据仍明确缺失。
- Open Design 桌面端已更新至 0.15.1，MCP 配置已写入；学生已在 composer 选择完整内置 `frontend-design` + `default`（Neutral Modern）并链接 `ProjectB`。新任务的 `list_skills` 已成功，`list_projects=[]`、`active=false` 如实表示尚未进入实现。G-01 环境门禁已 PASS；daemon 不要求长期运行，真实 project/run/artifact 后置 UI-01A。候选与选择审计见 [`research/OPEN_DESIGN_SKILL_OPTIONS.md`](research/OPEN_DESIGN_SKILL_OPTIONS.md)。
- D-005 的不同类型冷启动智能体/账号可以先由学生选择，但阶段 B 的正式 `superpowers:writing-plans` 证据仍未闭合；恢复正式调用或取得课程明确接受 fallback 的证据前，不执行 G-03。之后全新 session 只能获得 `SPEC.md` 与 `PLAN.md`，且冷启动修订和再次批准前禁止正式实现。
- Hugging Face 当前官方条款、依赖/SDK/冻结工具许可证等已放入 G-02 工程证据门禁；学生本人 brainstorming 反思仍是课程交付缺口且不得由 AI 代写。

### Open Design 门禁更新（2026-07-21T21:08:02+08:00）

- 学生已在 Open Design 界面选择 `frontend-design` + `default`（Neutral Modern）并链接 `ProjectB`；该组合不再是待确认候选。
- Open Design 0.15.1 daemon、完整 bundled skill、学生选择和 fresh MCP 只读结果均已记录；`projects=[]`、`active=false` 不构成环境缺口，G-01 已 PASS。
- 正确后续动作不是保持窗口或创建空项目，而是在冷启动和实现批准后的 UI-01A 按需开启 Open Design，执行真实 project/run/artifact，记录截图与 review，并在 TDD 红测后再写生产 UI。本轮没有发送 prompt、生成 artifact 或修改正式 UI/源码。
## 2026-07-21 G-02 evidence checkpoint（历史）

- G-01 is now correctly scoped as an Open Design environment/selection gate and is recorded as PASS. A real project/run/artifact remains deferred to UI-01A after cold-start and implementation approval.
- G-02 evidence ledgers and `scripts/verify_evidence.ps1` now exist. The validator has both observed red and green runs; green means 37 rows are structurally valid and no secret pattern was found, while 28 rows remain explicitly blocked.
- No project dependency manifest/lockfile, production source, build, provider call, deployment, or public URL exists. G-02A/B/C, G-03 and all implementation units remain pending.

## 2026-07-22 G-02 current evidence state

- G-02A PASS：exact evidence commit `22b516af7b6f4896c6127e75b2585435e407a3c0`；54 个 Python pins、166 个 npm entries、direct/license 双向校验和无网络 smoke 已复审。生产 manifest 与 clean-clone/full-app 仍属于 T-01/DIST-01。
- G-02B PASS：exact evidence commit `5ac9d47ddda845ed78f1758326fb547610274f4c`；官方模型/价格/PDF/token count/File Search/留存与负能力边界已复审。F 仍为 `source_disabled`，未调用 provider。
- G-02C PENDING：reviewed blocker checkpoint `be666537706b4c133673029d950e84f15ea3ae1b`。HF Docker Space 需要付费方案，`host-cost`/`host-account` 是仅余两个 blocker；D-025 的候选证据见 `docs/research/PUBLIC_HOSTING_ALTERNATIVES.md`，仍由学生决定，未静默换平台或创建资源。
- 当前 validator 为 `PASS rows=63 explicitly_blocked=2 python_pins=54 npm_packages=166`；distribution-strict 模式按预期失败。G-03 与所有正式实现继续关闭。
