# 项目启动审计与课程差距

初次审计时间：2026-07-17T18:14:41+08:00
最近历史复查时间：2026-07-19T21:57:09+08:00

> 当前（2026-07-20）要求符合性请以 [`REQUIREMENTS_COMPLIANCE_AUDIT.md`](REQUIREMENTS_COMPLIANCE_AUDIT.md) 为准。本文件前半部分保留启动阶段的历史快照，不能用其中“SPEC 不存在”等旧状态判断当前工作区。

## 启动时结论（历史）

项目目前处于阶段 A 的需求澄清，不是实现阶段。仓库没有源码或项目规约；Superpowers v6.1.1 已安装且核心 skills 完整，但本次会话未将其注册到可调用清单。Open Design v0.15.0 安装器已下载并通过本地校验文件核对，尚未安装或接入。当前可继续 brainstorming 的逐项提问，但不得创建 `PLAN.md` 或编写实现。

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

## Skill 与工具状态

### Superpowers

- 当前会话暴露的 skills 中没有 `superpowers:*`，但官方插件缓存存在 Superpowers v6.1.1（MIT）及完整核心 skill 目录。
- 已检测：`brainstorming`、`writing-plans`、`using-git-worktrees`、`subagent-driven-development`、`executing-plans`、`test-driven-development`、`requesting-code-review`、`receiving-code-review`、`systematic-debugging`、`verification-before-completion`、`finishing-a-development-branch`，以及 `using-superpowers`、`dispatching-parallel-agents`、`writing-skills`。
- 官方仓库在 2026-07-19 复核显示最新版本为 v6.1.1；本地插件 manifest 同样为 v6.1.1。
- 官方 Codex 安装：App 侧栏 Plugins → Coding → Superpowers → `+`，或 CLI `/plugins` 搜索安装。
- 应检测的核心 skills：`brainstorming`、`writing-plans`、`using-git-worktrees`、`subagent-driven-development` / `executing-plans`、`test-driven-development`、`requesting-code-review`、`receiving-code-review`、`systematic-debugging`、`verification-before-completion`、`finishing-a-development-branch`。

### Open Design

- 当前未找到 `od` 命令、Open Design skill 或 MCP；MCP resources/templates 均为空。
- 官方 release：v0.15.0（2026-07-14，commit `79e257d`），Apache-2.0，提供 Windows x64 安装器。
- 本地安装器大小 309,298,247 bytes；SHA-256 与同名 `.sha256` 一致，值为 `63fc2e609489474e99187cdf94d01d063c1dbee733aaf2464d835cdc1e96f6b5`；Authenticode 状态为 `NotSigned`，与上游 Windows 未签名发布说明一致。
- 官方说明支持 Codex，接入命令为 `od mcp install codex`，也支持 `--print` 预览配置。
- 安装器已下载但未运行。当前环境只允许写项目目录，无法合规完成会写入用户/系统目录且可能触发 SmartScreen 的安装；待用户按 `DECISIONS_NEEDED.md` 处理。

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
| Superpowers 全流程 | 插件已安装；本会话未注册 | 当前继续逐项澄清；阶段 B 前新建能正式调用 `writing-plans` 的会话 |
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

- Superpowers v6.1.1 已安装到官方 Codex 插件缓存；核心 skills 完整，mandatory brainstorming 前置环境已恢复。
- 已完整读取 `using-superpowers` 与 `brainstorming` skill，并保持“用户批准设计前不得实现”的硬门禁。
- Open Design 仍未安装。自动下载受 GitHub 网络连接与内置浏览器超时阻塞，用户改为手动下载官方 v0.15.0 安装器；安装后继续 MCP 接入验证。

### 当前复查（2026-07-19T21:57:09+08:00）

- 完整复读根目录约束、课程通用要求、B 类要求、全部已有项目文档与 Git 历史；仓库仍无源码、`SPEC.md` 或 `PLAN.md`。
- Superpowers v6.1.1 缓存和 14 个 skills 均存在；本次任务的可调用 skill 清单没有注册它们。已完整读取 `using-superpowers` 与 `brainstorming`，按其清单续接阶段 A，并在日志保留证据限制。
- Open Design v0.15.0 官方 release、Windows x64 资产、本地哈希一致性与未签名状态已核对；`od`/MCP 均不存在。安装因工作区外写入限制交由用户处理，不重复尝试提权。
- Git 工作区原本只有两份 Open Design 下载文件未跟踪；已精确加入 `.gitignore`，防止大文件误提交。
