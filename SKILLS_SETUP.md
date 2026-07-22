# AI4SE 期末项目 B：Skill 准备方案

本方案只采用课程指定或其上游公开维护的成熟项目，不为作业自造方法论 skill。具体业务技术栈确定后，再添加框架专用 skill，避免无关 skill 污染上下文。

## 一、必须安装：Superpowers

- 上游：<https://github.com/obra/superpowers>
- 许可证：MIT
- 用途：课程要求的规约、计划、worktree、subagent、TDD、评审、调试与完成验证。
- 选择理由：它不是“类似方案”，而是作业文档明确指定的框架；上游已经提供 Codex App、Codex CLI、Claude Code 等适配，不应手工复制或改写其中的 skill。

### ProjectB 当前状态（2026-07-22）

当前状态已变为 **已安装并启用，但本任务未重新加载**：`config.toml` 已有 `[plugins."superpowers@openai-api-curated"]` 与 `enabled = true`；所选安装快照 `11c74d6b` 的 manifest 版本为 `5.1.3`，14 个 skill 目录及其 `SKILL.md` 均完整。此前 `openai-curated-remote` 下的 6.1.1 仅作为旧 cache 保留，不再用于判断当前安装状态。当前 task 仍未暴露任何 `superpowers:*` skill；Codex CLI 0.144.4 的空 marketplace/plugin 列表属于独立 CLI 环境，不能推翻桌面端 config/cache 直接证据。精确证据见 [`docs/engineering/SUPERPOWERS_VALIDATION.md`](docs/engineering/SUPERPOWERS_VALIDATION.md)。

因此现在不需要重新下载 skill 或重复安装；只需在安装完成后**新建 ProjectB task** 验证。不要把本任务的旧 skill 快照、手工读取 `SKILL.md` 或现有 fallback `PLAN.md` 当作正式 skill 调用。

安装方式按你实际使用的编码智能体选择一种：

### Codex App（推荐作为主开发智能体）

1. 打开 Codex App 左侧的 **Plugins**。
2. 在 Coding 分类中找到 **Superpowers**。
3. 点击 `+` 并完成安装。
4. 在 **Installed** 行确认 Superpowers 已启用。
5. 新建会话，要求 Codex 列出可用的 Superpowers skills，确认下列核心项存在。

### Codex CLI

1. 在 Codex CLI 输入 `/plugins`。
2. 搜索 `superpowers`。
3. 选择 **Install Plugin**。
4. 退出并重新进入项目会话后验证 skill 列表。

### Claude Code（适合作为冷启动验证的第二种智能体）

在 Claude Code 中执行：

```text
/plugin install superpowers@claude-plugins-official
```

Claude Code 与 Codex 属于不同类型的智能体，可用于课程要求的陌生智能体冷启动验证；必须新开 session，且只提供 `SPEC.md` 与 `PLAN.md`。

## 二、Superpowers 必用 skill

| 阶段 | 上游 skill | 本作业用途 |
| --- | --- | --- |
| 需求澄清 | `brainstorming` | 共同设计并沉淀 `SPEC.md` |
| 计划 | `writing-plans` | 生成带文件路径、失败测试与验证步骤的 `PLAN.md` |
| 隔离开发 | `using-git-worktrees` | 独立功能使用独立 worktree/分支 |
| 实现 | `subagent-driven-development` | 每个 task 交给新鲜 subagent |
| 计划执行备选 | `executing-plans` | 不适合会话内逐 task 派发时使用 |
| 测试 | `test-driven-development` | 强制红—绿—重构 |
| 评审 | `requesting-code-review` | 先规约合规、再代码质量 |
| 接收评审 | `receiving-code-review` | 核验并处理评审意见 |
| 调试 | `systematic-debugging` | 先定位根因再修复 |
| 完成验证 | `verification-before-completion` | 用当次证据支持“完成”声明 |
| 收尾 | `finishing-a-development-branch` | 决定合并、PR/MR、保留或丢弃 |

`dispatching-parallel-agents` 仅在任务真正独立、没有共享写入和前置依赖时启用，不作为默认流程。

## 三、有 UI 时启用：Open Design

- 上游：<https://github.com/nexu-io/open-design>
- 许可证：Apache-2.0
- 用途：按设计系统生成/迭代 UI 原型和真实前端资产，并在 `SPEC.md` 中留下 design system 与 skill 选择证据。
- 启用条件：项目含 Web 页面、移动界面、桌面 UI、控制台、营销页或文档站。纯后端/纯 CLI 才可不装；但本作业最终要求 WebUI，因此通常应安装。

Windows 上优先从上游 Releases 安装 Open Design 桌面版；它会自动发现本机编码智能体，并附带维护好的 skills 与 design systems。安装后为 Codex 接入 MCP：

```powershell
od mcp install codex
```

ProjectB 当前无需重复执行上述安装：Open Design 0.15.1、Codex MCP、完整 bundled `frontend-design` 和 `default`/Neutral Modern 选择均已验证，G-01 已 PASS。以下说明用于区分已完成的环境接入和后续获准的真实 UI run。

这里要区分三个层次：

1. **Bundled skill/design system**：桌面版已经携带完整条目时（例如 `frontend-design` 与 `default`/Neutral Modern），界面选择只是把现有工作流附加到一次 Open Design run，不需要再把 `SKILL.md` 下载到 Codex。只有明确标为 catalog stub、正文要求另装 upstream 的条目才需要额外获取。
2. **MCP/daemon**：MCP 把编码智能体连接到一个正在运行的本地 Open Design 实例，用于读取项目、上下文和 artifact；它不是 skill 安装器。Open Design 只需在 MCP 调用或实际 project/run 期间开启，不要求无任务时长期挂起。
3. **实际 Open Design run**：环境验证只证明工具可用和选择已记录；课程所需的真实 UI 工作流证据必须在获准的 UI task 中创建 project/run/artifact，并与 TDD 顺序、评审和截图证据一起保存。不得为制造环境门禁 PASS 而创建空项目。

若使用 WSL2，注意系统自带 `/usr/bin/od` 可能与 Open Design 命令重名，应按 Open Design 的 WSL2 指南配置，或从桌面应用 **Settings → MCP server** 复制使用绝对路径的配置。

新项目尚未选择 UI 方向时的提示示例（ProjectB 已完成此步，不要重复运行）：

```text
Use open-design to produce a WebUI direction for this project. Read SPEC.md first,
propose a design system and skill, and do not implement it until I confirm the direction.
```

确认后，把最终选择（例如 design system 名称、所用 skill、拒绝的备选及理由）写入 `SPEC.md` 与 `SPEC_PROCESS.md`，不要只留在聊天记录里。

## 四、暂不预装的 skill

在项目题目和技术栈尚未确定前，不建议预装 React、Python、Docker、安全扫描或云部署类的零散社区 skill：

- 它们不是当前课程的硬性 skill；
- 质量、许可证和维护状态差异较大；
- 可能与 Superpowers 的 TDD、计划和评审触发规则冲突；
- 技术栈确定后才能判断是否真正需要。

这里并不表示不使用成熟工具。实现阶段应按技术栈选择官方工具，例如 Playwright/Vitest/Pytest、Gitleaks、Docker、GitLab CI 等；“工具”不需要为了使用而包装成 skill。

## 五、安装后自检

新建一个空白测试会话，输入：

```text
Read AGENTS.md. We are at the idea stage of an AI4SE final project.
Tell me which skill must be used now and what gate prevents implementation.
Do not write code.
```

合格表现应为：

1. 触发 `brainstorming`；
2. 开始逐步澄清项目；
3. 明确 `SPEC.md`、`PLAN.md` 和冷启动验证完成前不得实现；
4. 不直接创建业务代码。

若 Codex 直接开始搭框架，先检查 Superpowers 是否在当前 Codex 环境安装成功、是否重新开启了会话，以及项目根目录是否存在 `AGENTS.md`。

仅看到 `~/.codex/plugins/cache/.../superpowers/<version>` 不代表安装成功。还应确认 `config.toml` 存在对应 enabled plugin 状态，并以新任务实际暴露/调用 skill 为最终证据。

## 六、版本与来源记录

正式开工当天，在 `AGENT_LOG.md` 第一条记录以下信息：

- 主智能体类型与版本；
- 第二种冷启动智能体类型与版本；
- Superpowers 安装来源与当时版本/commit；
- Open Design 是否启用、版本、所选 design system/skill；
- 任何偏离上游默认流程的原因。

不要把上游 skill 源码复制进作业仓库冒充自制成果；使用插件安装并在 README 中按许可证注明第三方依赖即可。
