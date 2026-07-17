# DECISIONS_NEEDED

## D-001 — 手动安装 Superpowers（当前硬阻塞）

- **问题**：当前 Codex 会话未检测到 Superpowers，无法按课程要求触发 `superpowers:brainstorming`。
- **为什么必须由你处理**：官方 Codex App 安装流程需要在侧栏 Plugins 中点击安装；当前电脑控制规则禁止智能体自动化 Codex 桌面应用及其扩展。
- **候选方案**：
  1. **推荐：Codex App** — Plugins → Coding → Superpowers → `+`，安装后新建项目会话。
  2. **Codex CLI** — 输入 `/plugins`，搜索 Superpowers，选择 Install Plugin，然后重新进入项目会话。
  3. 暂停本项目；不安装则无法形成课程认可的 brainstorming 证据。
- **推荐方案及影响**：选择方案 1，与当前主智能体环境一致；安装后应能看到 `superpowers:brainstorming`、`writing-plans`、`using-git-worktrees`、`subagent-driven-development`、`test-driven-development`、评审、调试与完成验证等 skills。
- **阻塞范围**：阶段 A、`SPEC.md`，以及全部后续阶段。

## D-002 — 项目方向（安装后首个 brainstorming 问题）

- **问题**：项目目标仍为模板占位符，没有具体想法。
- **为什么必须由你决定**：目标用户、真实问题、是否含 agent、核心数据边界会显著改变最终产品，课程禁止智能体代替学生决定。
- **候选方案**：
  1. **推荐：从你的真实痛点出发** — 你先给出一个最近反复遇到、愿意实际使用软件解决的问题，brainstorming 再逐项澄清。
  2. 你给出 2–3 个感兴趣领域，由 brainstorming 比较真实用户价值与工程深度。
  3. 完全没有方向时，由 brainstorming 每次只问一个关于日常工作/学习痛点的问题，逐步收敛，不直接替你选题。
- **推荐方案及影响**：方案 1 最容易证明“真实、有人会用”，也更容易形成可验收的三模块应用。
- **阻塞范围**：问题陈述、用户故事、模块边界与全部 SPEC 内容。

## D-003 — 安装 Open Design（WebUI 必需流程）

- **问题**：课程最终要求 WebUI，而本项目约束规定含 UI 时使用 Open Design；当前 `od`、skill 与 MCP 均不可用。
- **为什么必须由你处理**：Windows 安装器属于系统级新软件安装/首次运行，智能体不能在没有操作时人工确认的情况下替你执行；当前自动化规则也要求安装动作由用户确认或接管。
- **候选方案**：
  1. **推荐：安装官方 Windows x64 v0.15.0**，之后运行 `od mcp install codex`，再新建 Codex 会话验证 MCP/skills。
  2. 从源码运行（Node 24、pnpm 10.33.x），隔离性更强但维护成本显著更高，不适合作为课程项目默认路径。
  3. 明确决定不用 Open Design；这需要你确认，并在 `AGENT_LOG.md` 记录理由与影响。
- **推荐方案及影响**：方案 1 与官方 Quick Start 一致，后续可在 SPEC 中留下 design system 与 skill 选择证据。
- **阻塞范围**：正式 UI 方向选择与 UI 实现；不阻塞安装 Superpowers 后先开始问题/用户层面的 brainstorming。

## D-004 — 远程平台策略（暂不阻塞阶段 A）

- **问题**：课程原文同时要求 GitHub PR/Actions 和 NJU Git/GitLab CI，最终清单又强制 `.gitlab-ci.yml` 与 `unit-test` job。
- **为什么必须由你决定**：远程仓库归属、镜像策略和 PR/MR 证据属于学生账号与提交策略，且用户未授权远程 push/建 PR。
- **候选方案**：
  1. **推荐：NJU Git/GitLab 为主，GitHub 作公开镜像**；GitLab CI 满足硬提交，GitHub Actions/PR 保留通用要求证据。
  2. 只用 NJU Git/GitLab，并在 SPEC/日志中解释课程文本冲突及取舍。
  3. 只用 GitHub（风险最高：可能缺失 NJU Git 与 GitLab CI 硬项）。
- **推荐方案及影响**：方案 1 最保守但维护两套 CI；具体远程操作仍需你在执行时批准。
- **阻塞范围**：不阻塞阶段 A；在 SPEC 的分发/CI 策略定稿前必须决定。

## D-005 — 冷启动智能体类型（后续门禁）

- **问题**：当前未检测到 `claude`，而冷启动必须使用不同类型智能体的新 session。
- **为什么必须由你决定**：可能涉及安装并登录另一种智能体，且只能由学生控制账号与授权。
- **候选方案**：
  1. **推荐：Claude Code + Superpowers**，与主开发 Codex 类型不同，课程材料也明确举例支持。
  2. 使用另一种课程允许的智能体（Cursor Agent、Gemini CLI、OpenCode 等），确保全新 session 且仅提供 SPEC/PLAN。
- **推荐方案及影响**：方案 1 与现有准备文档一致；可在 PLAN 完成前再安装。
- **阻塞范围**：不阻塞阶段 A/B；阻塞阶段 C 冷启动验证。

