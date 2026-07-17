# 项目启动审计与课程差距

审计时间：2026-07-17T18:14:41+08:00

## 结论

项目目前处于“阶段 A 前置环境门禁”，不是实现阶段。仓库没有源码或项目规约；Superpowers 与 Open Design 均不可用。最先需要人工完成的是安装 Superpowers 并新建会话，随后才可由 `brainstorming` 逐项明确项目方向。

## 仓库现状

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

- 当前会话暴露的 skills 中没有 `superpowers:*`。
- 用户 Codex 插件缓存和 skills 目录中未找到 Superpowers 或其核心 skill 目录。
- 官方最新 release：v5.1.0，commit `f2cbfbe`，MIT。
- 官方 Codex 安装：App 侧栏 Plugins → Coding → Superpowers → `+`，或 CLI `/plugins` 搜索安装。
- 应检测的核心 skills：`brainstorming`、`writing-plans`、`using-git-worktrees`、`subagent-driven-development` / `executing-plans`、`test-driven-development`、`requesting-code-review`、`receiving-code-review`、`systematic-debugging`、`verification-before-completion`、`finishing-a-development-branch`。

### Open Design

- 当前未找到 `od` 命令、Open Design skill 或 MCP。
- 官方最新 release：v0.15.0，commit `79e257d`，Apache-2.0，提供 Windows x64 安装器。
- 官方说明支持 Codex，接入命令为 `od mcp install codex`，也支持 `--print` 预览配置。
- 本次未下载安装或运行系统级软件；待用户按 `DECISIONS_NEEDED.md` 处理。

### 本地开发工具

| 工具 | 状态 |
| --- | --- |
| Git | 2.53.0.windows.3 |
| Node.js | 24.14.0 |
| npm | 已安装；`npm.ps1` 被执行策略阻止，后续应使用 `npm.cmd` |
| pnpm | 11.9.0 |
| Python | 3.14.3 |
| uv | 0.11.14 |
| Docker | CLI 29.1.2；沙箱无法读取用户 Docker config，daemon 尚未验证 |
| GitHub CLI (`gh`) | 未找到 |
| Gitleaks | 未找到 |
| Claude Code | 未找到 |
| Open Design (`od`) | 未找到 |

## 对课程要求的主要差距

| 课程要求 | 当前状态 | 下一合规动作 |
| --- | --- | --- |
| Superpowers 全流程 | 缺失 | 用户手动安装，重启会话，从 `brainstorming` 开始 |
| 真实、有用、至少 3 模块 | 未定义 | brainstorming 先确定真实用户与痛点，再验证模块边界 |
| 5+ INVEST 用户故事 | 缺失 | 在用户确认问题方向后逐项形成 |
| WebUI + Open Design | 工具缺失 | 安装 Open Design；在 SPEC 确认 design system/skill |
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
