# AI4SE Project B 要求符合性审计

审计时间：2026-07-20（本轮执行）
审计范围：当前 Git 工作区、提交历史与以下权威来源：

- [通用项目要求](requirements/项目要求.md)
- [Project B 应用类项目要求](requirements/AI4SE_Final_Project_B_应用类项目.md)
- [仓库执行约束](../AGENTS.md)
- [Skill 准备方案](../SKILLS_SETUP.md)

## 结论

项目仍符合 **Project B 非 harness 应用类项目**的选题边界：它有真实目标用户、可在 30 秒内说明的连续学习问题、M1/M2/M3 三个核心模块、WebUI 方向和明确的非 agent AI 边界。

当前只能判定为 **阶段 A 核心产品与交付规约已有文档覆盖、阶段门禁尚未全部满足、最终交付尚不合规**。`SPEC.md` 是未签字工作草案；Open Design/Superpowers 的正式工具接入证据与学生本人对 brainstorming 的过程反思尚缺。`PLAN.md`、冷启动验证、正式源码、测试、CI、分发、README、PR/MR、公开 WebUI URL 和学生本人撰写的 `REFLECTION.md` 均尚未产生。它们在当前门禁下多数属于合法延后，但仍是最终提交前的硬缺口，不能写成“已满足”。

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
| 至少 5 个 INVEST 用户故事 | `SPEC.md` 有 US-01 至 US-10 | 文档覆盖，未验证 | 当前仍待整体签字，签字前逐项确认可独立价值与验收映射 |
| SPEC 必需章节 | 问题、10 个用户故事、模块规约、NFR、架构/数据流、数据模型、凭据、分发、技术选型、50 项 AC、风险均已存在；D-017 至 D-024 已同步 | 文档覆盖，未验证 | 完成 placeholder/矛盾/范围自审，补学生本人 brainstorming 反思和 Open Design 实际 design system/skill 后，由学生明确整体签字 |
| 无 agent 时不要求 harness 内核 | `SPEC.md` 明确模型只有具名受约束端口，无自主循环/工具分发 | 当前满足 | provider mock 是项目可靠性设计，不冒充 harness 交付物 |
| API key 安全存储与生命周期 | `SPEC.md` 安全/凭据章节、provider profile/`credential_ref`、[威胁模型](research/COURSEWARE_THREAT_MODEL_BASELINE.md)；D-021 已选成熟 keyring 适配 Windows Credential Manager | 文档覆盖，未验证 | TDD 验证隐藏录入、状态、更新、清除、错误脱敏和失败关闭；普通 config、SQLite、日志和前端状态禁止 secret |
| OpenAI Responses 政策快照 | `SPEC.md` 8.2、AC-39/49 已约束 `store:false`、application state、abuse monitoring、cache、文件审查例外与 Files/Vector Stores 生命周期 | 文档覆盖，未验证 | 实现时从官方政策刷新并绑定 consent/profile 指纹；测试不得把 `store:false` 或“默认不训练”误报为 ZDR |
| WebUI | localhost WebUI、首次导入流程和响应式 AC 已写；已有需求 mockup | 文档覆盖，未验证 | mockup 不算正式源码；最终必须提供可访问 URL 并做真实双端 UI 验证 |
| Open Design | D-024 已确认安装并使用；v0.15.0 安装器/校验已核验，但 `od`、MCP、skill 当前不可用 | 明确缺口 | 当前环境禁止向工作区外安装；须由用户环境完成安装/MCP 接入并在新会话验证，随后在 SPEC 记录 design system/skill；不得静默偏离 |
| Superpowers | v6.1.1 缓存与核心 skills 已核验；`brainstorming` 过程有日志 | 明确缺口 | 当前会话未注册 `superpowers:*`；进入阶段 B 前必须在新会话正式调用 `writing-plans` 并继续全流程留证 |
| SPEC_PROCESS 至少 3 轮迭代与反思 | [SPEC_PROCESS](../SPEC_PROCESS.md) 已记录 14 轮原始回答、采纳、修正与未执行边界，但尚无独立的 brainstorming 优点/不足反思段 | 明确缺口 | 签字前补学生本人对 brainstorming 优点、不满和关键取舍的反思；不得由 AI 代替个人判断 |
| PLAN 细粒度任务 | `PLAN.md` 不存在 | 阶段门禁延后 | 仅在 SPEC 明确签字后用 `writing-plans` 生成；每项含依赖、文件、预期红测、命令和完成标准 |
| 陌生智能体冷启动 | 尚未执行 | 阶段门禁延后 | SPEC+PLAN 后由不同类型全新 session，仅提供两文件并记录提问、误解、差距与修订 diff |
| worktree/subagent/TDD/两阶段评审 | 尚无正式实现 | 阶段门禁延后 | 获准实现后每 task 新鲜 subagent、先红后绿再重构、先规约合规评审再质量评审 |
| 一键测试 | 无测试命令、测试代码或本次运行证据 | 阶段门禁延后 | PLAN 选择统一命令并覆盖 M1/M2/M3、安全策略、adapter contract 和端到端关键流 |
| GitHub Actions | D-023 已确认 GitHub 镜像保留 Actions；`.github/workflows/ci.yml` 不存在 | 阶段门禁延后 | 实现每次 push 调用与 GitLab 相同的一键测试入口并实际运行；镜像/push/PR 需执行当时授权 |
| GitLab `unit-test` job | D-023 已确认 NJU Git/GitLab 主仓；`.gitlab-ci.yml` 不存在 | 阶段门禁延后 | 最终硬交付；job 名必须严格为 `unit-test`，最后一次课程 CI 必须通过 |
| GitHub/NJU Git 与 PR/MR 历史 | D-023 已确认 NJU Git/GitLab 主仓 + GitHub 镜像；当前只有本地小步文档提交，无远程/PR/MR | 文档覆盖，未验证 | 未经执行当时授权不 push、建 PR/MR 或启用镜像；实现阶段每 worktree 对应可审查 PR/MR |
| 分发形态 | 课程原文要求明确类别；SPEC 提议 Windows x64 单文件 `ProjectB.exe`，但该细节不是 D-021 原答案，须由整体签字确认 | 明确缺口 | 学生整体确认后按[技术栈与分发基线](research/TECH_STACK_DISTRIBUTION_BASELINE.md)选冻结工具；验证单文件/干净机/SmartScreen/数据保留 |
| README | 不存在 | 阶段门禁延后 | 随实现维护项目简介、安装、运行、分发、目录、安全、凭据、限制、第三方依赖与许可证 |
| 第三方许可证 | Superpowers MIT、Open Design Apache-2.0 已记录；课件许可证未知且未入仓；公开夹具仅可使用合成或明确许可材料；OpenAI Python SDK 许可证尚未现场核验 | 文档覆盖，未验证 | SDK、冻结/安装工具、传递依赖与资产接入前逐项核验，最终汇总到 README 并生成分发内容许可证清单 |
| 公开 WebUI URL / CI/CD | D-022 只确认许可夹具 + mock/无真实 key；OCI/HF Spaces/隔离限额是待整体签字的工程候选。官方页面复核受 502/超时且未部署 | 明确缺口 | 整体签字并重核官方 Docker/HTTPS/费用/临时存储后，再实测 build/run/隔离/CI；账号/部署需执行时授权，不得付费 |
| AGENT_LOG | 历史条目包含时间、task、skill、上下文、人工修改与教训 | 当前满足 | 每次真实决策/task 后即时更新；D-017 至 D-024 批量确认与本轮审计需在提交前同步记录 |
| REFLECTION 1500–2500 字 | 文件不存在 | 阶段门禁延后 | 必须由学生本人撰写；AI 只能在有学生初稿后按声明范围润色或指出论证缺口 |

## 严格解释

1. 课程原文把 Open Design 写为“强烈推荐”，但本仓库 `AGENTS.md` 对含 UI 项目将其提升为必须遵循的工作流；当前按更严格规则执行。
2. 通用要求同时写明 GitHub 仓库/PR/Actions，最终清单又强制 NJU Git 与 `.gitlab-ci.yml`。D-023 已确认采用 NJU Git/GitLab 主仓 + GitHub 镜像，并维护 GitLab `unit-test` 与 GitHub Actions 双 CI；该策略不等于授权当前会话执行远程 push、PR/MR、镜像或部署。
3. Project B 已明确不含课程定义的 agent，因此不需要 Project A 的 harness 内核、harness mock-LLM 单元测试或机制演示；但本项目仍应使用 provider mock 对受约束 AI 端口和权威状态隔离做确定性测试。
4. 阶段门禁解释“为什么现在没有实现”，不免除最终要求。没有实际命令输出、CI 记录或可访问 URL 时，不得声称测试、分发或部署已经完成。

## 当前最近门禁

当前 `SPEC.md` 未签字；D-017 至 D-024 的方向已同步，但单文件分发、OCI/Hugging Face demo、隔离限额和 `ReviewPolicy v1` 数值仍只是待整体签字的工程候选。Hugging Face Spaces Docker SDK 是首选候选，官方现场复核受网络阻塞，账号/部署只在执行时请求授权。阶段 A 仍有五项真实门禁：恢复联网后重核该平台；Open Design 安装/MCP 接入及实际 design system/skill 记录；Superpowers skill 在可调用会话中的正式使用；学生本人补充 brainstorming 优点/不足/关键取舍；学生明确整体确认 `SPEC.md`。在这些门禁及课程规定顺序满足前不生成 `PLAN.md`，更不开始正式实现。
