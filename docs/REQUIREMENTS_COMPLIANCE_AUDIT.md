# AI4SE Project B 要求符合性审计

审计时间：2026-07-20（本轮执行）
审计范围：当前 Git 工作区、提交历史与以下权威来源：

- [通用项目要求](requirements/项目要求.md)
- [Project B 应用类项目要求](requirements/AI4SE_Final_Project_B_应用类项目.md)
- [仓库执行约束](../AGENTS.md)
- [Skill 准备方案](../SKILLS_SETUP.md)

## 结论

项目仍符合 **Project B 非 harness 应用类项目**的选题边界：它有真实目标用户、可在 30 秒内说明的连续学习问题、M1/M2/M3 三个核心模块、WebUI 方向和明确的非 agent AI 边界。

当前只能判定为 **阶段 A 流程基本合规、最终交付尚不合规**。`SPEC.md` 是未签字工作草案；`PLAN.md`、冷启动验证、正式源码、测试、CI、分发、README、PR/MR、公开 WebUI URL 和学生本人撰写的 `REFLECTION.md` 均尚未产生。它们在当前门禁下多数属于合法延后，但仍是最终提交前的硬缺口，不能写成“已满足”。

状态含义：

- **当前满足**：本次有可核验仓库证据；
- **文档覆盖，未验证**：规约已表达，但尚无实现/测试证据；
- **阶段门禁延后**：当前不应提前创建，后续阶段必须完成；
- **明确缺口**：当前阶段已经可以或必须修正，或进入下一阶段前必须解决。

## 逐项矩阵

| 要求 | 当前证据 | 判定 | 后续动作 |
| --- | --- | --- | --- |
| B 类真实应用，不是 harness | [SPEC](../SPEC.md) 的问题陈述、用户边界与受约束 AI 端口 | 当前满足 | 保持第一版无自主 agent loop；若未来改变须重新触发 agent 门禁 |
| 30 秒说明真实价值 | `SPEC.md` 1.2 已有候选说明 | 文档覆盖，未验证 | SPEC 签字时确认措辞；实现后用真实流程而非演示页证明价值 |
| 至少 3 个职责清晰模块 | M1 材料保真、M2 适配解释、M3 持续复习；X1/X2 为跨模块控制面 | 文档覆盖，未验证 | PLAN 按模块依赖拆分，核心路径需自动化测试 |
| 至少 5 个 INVEST 用户故事 | `SPEC.md` 有 US-01 至 US-09 | 文档覆盖，未验证 | 当前仍标为候选，签字前逐项确认可独立价值与验收映射 |
| SPEC 必需章节 | 问题、模块规约、NFR、架构/数据流、数据模型、凭据、AC、风险均已存在 | 明确缺口 | 技术栈、具体 adapter、分发/目标平台、公开部署、Open Design design system/skill 尚未收敛，不能签字 |
| 无 agent 时不要求 harness 内核 | `SPEC.md` 明确模型只有具名受约束端口，无自主循环/工具分发 | 当前满足 | provider mock 是项目可靠性设计，不冒充 harness 交付物 |
| API key 安全存储与生命周期 | `SPEC.md` 安全/凭据章节、provider profile/`credential_ref`、[威胁模型](research/COURSEWARE_THREAT_MODEL_BASELINE.md) | 文档覆盖，未验证 | 选择本机安全存储实现；TDD 验证隐藏录入、状态、更新、清除和失败关闭；普通 config 禁止 secret |
| WebUI | localhost WebUI、首次导入流程和响应式 AC 已写；已有需求 mockup | 文档覆盖，未验证 | mockup 不算正式源码；最终必须提供可访问 URL 并做真实双端 UI 验证 |
| Open Design | v0.15.0 安装器/校验已核验；`od`、MCP、skill 当前不可用 | 明确缺口 | 依仓库更严格约束，正式 UI 前必须接入并在 SPEC 记录 design system/skill，或由学生明确批准偏离 |
| Superpowers | v6.1.1 缓存与核心 skills 已核验；`brainstorming` 过程有日志 | 明确缺口 | 当前会话未注册 `superpowers:*`；进入阶段 B 前必须在新会话正式调用 `writing-plans` 并继续全流程留证 |
| SPEC_PROCESS 至少 3 轮迭代与反思 | [SPEC_PROCESS](../SPEC_PROCESS.md) 已记录 14 轮原始回答、采纳、修正与未执行边界，但尚无独立的 brainstorming 优点/不足反思段 | 明确缺口 | 签字前补学生本人对 brainstorming 优点、不满和关键取舍的反思；不得由 AI 代替个人判断 |
| PLAN 细粒度任务 | `PLAN.md` 不存在 | 阶段门禁延后 | 仅在 SPEC 明确签字后用 `writing-plans` 生成；每项含依赖、文件、预期红测、命令和完成标准 |
| 陌生智能体冷启动 | 尚未执行 | 阶段门禁延后 | SPEC+PLAN 后由不同类型全新 session，仅提供两文件并记录提问、误解、差距与修订 diff |
| worktree/subagent/TDD/两阶段评审 | 尚无正式实现 | 阶段门禁延后 | 获准实现后每 task 新鲜 subagent、先红后绿再重构、先规约合规评审再质量评审 |
| 一键测试 | 无测试命令、测试代码或本次运行证据 | 阶段门禁延后 | PLAN 选择统一命令并覆盖 M1/M2/M3、安全策略、adapter contract 和端到端关键流 |
| GitHub Actions | `.github/workflows/ci.yml` 不存在 | 阶段门禁延后 | 课程通用要求写明每次 push 自动测试；技术栈确定后实现并实际运行 |
| GitLab `unit-test` job | `.gitlab-ci.yml` 不存在 | 阶段门禁延后 | 最终硬交付；job 名必须严格为 `unit-test`，最后一次课程 CI 必须通过 |
| GitHub/NJU Git 与 PR/MR 历史 | 当前只有本地小步文档提交，无远程/PR/MR | 明确缺口 | D-004 必须确认双平台策略；未经授权不 push/建 PR，实现阶段每 worktree 对应可审查 PR/MR |
| 分发形态 | 容器/原生二进制/包、目标平台均未选 | 明确缺口 | SPEC 签字前确认；实现后在干净环境复现获取、运行和安全配置 key |
| README | 不存在 | 阶段门禁延后 | 随实现维护项目简介、安装、运行、分发、目录、安全、凭据、限制、第三方依赖与许可证 |
| 第三方许可证 | Superpowers MIT、Open Design Apache-2.0 已记录；课件许可证未知且未入仓 | 文档覆盖，未验证 | 每个 SDK/资产接入前核验；最终汇总到 README；公开夹具必须使用合成或明确许可材料 |
| 公开 WebUI URL / CI/CD | 未部署，无 URL 或执行记录 | 阶段门禁延后 | 选择不含私人课件/真实 key 的演示架构；最终提供可访问 URL 和最后一次通过的 CI 证据 |
| AGENT_LOG | 历史条目包含时间、task、skill、上下文、人工修改与教训 | 当前满足 | 每次真实决策/task 后即时更新；本轮 D-015 和本次审计需与提交同步记录 |
| REFLECTION 1500–2500 字 | 文件不存在 | 阶段门禁延后 | 必须由学生本人撰写；AI 只能在有学生初稿后按声明范围润色或指出论证缺口 |

## 严格解释

1. 课程原文把 Open Design 写为“强烈推荐”，但本仓库 `AGENTS.md` 对含 UI 项目将其提升为必须遵循的工作流；当前按更严格规则执行。
2. 通用要求同时写明 GitHub 仓库/PR/Actions，最终清单又强制 NJU Git 与 `.gitlab-ci.yml`。在课程方没有进一步澄清前，最保守的交付是保留 GitHub PR/Actions 证据，同时以 NJU Git/GitLab CI 满足最终提交；D-004 仍需学生确认。
3. Project B 已明确不含课程定义的 agent，因此不需要 Project A 的 harness 内核、harness mock-LLM 单元测试或机制演示；但本项目仍应使用 provider mock 对受约束 AI 端口和权威状态隔离做确定性测试。
4. 阶段门禁解释“为什么现在没有实现”，不免除最终要求。没有实际命令输出、CI 记录或可访问 URL 时，不得声称测试、分发或部署已经完成。

## 当前最近门禁

当前 `SPEC.md` 未签字，D-016 仍需确认第一版真实 adapter 的交付数量。此后还必须在签字前收敛技术栈、安全凭据后端、分发/目标平台、公开演示架构、GitHub/NJU Git 策略与 Open Design design system/skill。以上完成前不生成 `PLAN.md`，更不开始正式实现。
