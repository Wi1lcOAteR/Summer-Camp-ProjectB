# AI4SE Project B 要求符合性审计

审计时间：2026-07-20；最近更新：2026-07-22T02:29:11+08:00（G-02A/B PASS、D-025 替代托管候选调查与门禁复核）
审计范围：当前 Git 工作区、提交历史与以下权威来源：

- [通用项目要求](requirements/项目要求.md)
- [Project B 应用类项目要求](requirements/AI4SE_Final_Project_B_应用类项目.md)
- [仓库执行约束](../AGENTS.md)
- [Skill 准备方案](../SKILLS_SETUP.md)

## 结论

项目仍符合 **Project B 非 harness 应用类项目**的选题边界：它有真实目标用户、可在 30 秒内说明的连续学习问题、M1/M2/M3 三个核心模块、WebUI 方向和明确的非 agent AI 边界。

当前只能判定为 **SPEC 已整体确认、G-02A/B 工程证据已 PASS、G-02C 等待 D-025、正式 `superpowers:writing-plans` 调用证据仍缺、最终交付尚不合规**。Open Design 环境门禁已满足：0.15.1、MCP、完整内置 `frontend-design`、学生选择的 `default`/Neutral Modern 和 fresh 只读发现均有证据；`projects=[]`、`active=false` 是实现前状态。剩余 Open Design 证据是获准 UI-01A 的真实 project/run/artifact 和浏览器验收，不是安装或环境阻塞。学生本人 brainstorming 反思也尚缺。`PLAN.md` 目前有 41 个 planning group、69 个可派发 dispatch unit；其中 G-01/G-02A/G-02B 已 PASS，G-02C 与其余 65 个 unit pending。冷启动验证、正式源码、产品测试、CI、分发、README、PR/MR、公开 WebUI URL 和学生本人撰写的 `REFLECTION.md` 仍未产生。

状态含义：

- **当前满足**：本次有可核验仓库证据；
- **文档覆盖，未验证**：规约已表达，但尚无实现/测试证据；
- **阶段门禁延后**：当前不应提前创建，后续阶段必须完成；
- **明确缺口**：当前阶段已经可以或必须修正，或进入下一阶段前必须解决。

## 逐项矩阵

| 要求 | 当前证据 | 判定 | 后续动作 |
| --- | --- | --- | --- |
| B 类真实应用，不是 harness | [SPEC](../SPEC.md) 的问题陈述、用户边界与受约束 AI 端口 | 当前满足 | 保持第一版无自主 agent loop；若未来改变须重新触发 agent 门禁 |
| 30 秒说明真实价值 | `SPEC.md` 1.2 已有整体确认的说明 | 文档覆盖，未验证 | 实现后用真实流程而非演示页证明价值 |
| 至少 3 个职责清晰模块 | M1 材料保真、M2 适配解释、M3 持续复习；X1/X2 为跨模块控制面 | 文档覆盖，未验证 | PLAN 按模块依赖拆分，核心路径需自动化测试 |
| 至少 5 个 INVEST 用户故事 | `SPEC.md` 有 US-01 至 US-10，且已整体确认 | 文档覆盖，未验证 | 实现后逐项映射自动化验收与真实流程 |
| SPEC 必需章节 | 问题、10 个用户故事、模块规约、NFR、架构/数据流、数据模型、凭据、分发、技术选型、50 项 AC、风险均已存在；D-017 至 D-024、Open Design 实际组合和工程候选已同步 | 文档覆盖，未验证 | 补学生本人 brainstorming 反思，并在实现阶段提供真实证据 |
| 无 agent 时不要求 harness 内核 | `SPEC.md` 明确模型只有具名受约束端口，无自主循环/工具分发 | 当前满足 | provider mock 是项目可靠性设计，不冒充 harness 交付物 |
| API key 安全存储与生命周期 | `SPEC.md` 安全/凭据章节、provider profile/`credential_ref`、[威胁模型](research/COURSEWARE_THREAT_MODEL_BASELINE.md)；D-021 已选成熟 keyring 适配 Windows Credential Manager | 文档覆盖，未验证 | TDD 验证隐藏录入、状态、更新、清除、错误脱敏和失败关闭；普通 config、SQLite、日志和前端状态禁止 secret |
| OpenAI Responses 政策快照 | `SPEC.md` 8.2、AC-39/49 已约束 `store:false`、application state、abuse monitoring、cache、文件审查例外与 Files/Vector Stores 生命周期 | 文档覆盖，未验证 | 实现时从官方政策刷新并绑定 consent/profile 指纹；测试不得把 `store:false` 或“默认不训练”误报为 ZDR |
| WebUI | localhost WebUI、首次导入流程和响应式 AC 已写；已有需求 mockup | 文档覆盖，未验证 | mockup 不算正式源码；最终必须提供可访问 URL 并做真实双端 UI 验证 |
| Open Design | 0.15.1 daemon、MCP、完整内置 `frontend-design`、学生选择的 `default`/Neutral Modern 和 fresh `list_skills/list_projects/get_active_context` 结果均有记录；空项目/无活动上下文是实现前状态 | 当前满足（环境门禁）；正式工作流阶段门禁延后 | UI-01A 在冷启动和实现批准后按需开启 Open Design，创建真实 project/run/artifact、做截图与 review；生成源代码不得绕过 TDD 红测进入生产目录 |
| Superpowers | v6.1.1 缓存与核心 skills 已核验；`brainstorming` 过程有日志；阶段 B 完整读取上游 `writing-plans` 规则并透明记录 fallback | 明确缺口 | 当前会话未注册 `superpowers:*`；不得把 fallback 冒充正式调用，后续新会话需修复注册并继续全流程留证 |
| SPEC_PROCESS 至少 3 轮迭代与反思 | [SPEC_PROCESS](../SPEC_PROCESS.md) 已记录多轮原始回答、采纳、修正与未执行边界，但尚无独立的 brainstorming 优点/不足反思段 | 明确缺口 | 学生本人补充优点、不满和关键取舍；不得由 AI 代替个人判断或隐瞒代写 |
| PLAN 细粒度任务 | `PLAN.md` 有 41 个 planning group、69 个 dispatch unit；宽 group 明确不可派发，unit ID 无重复；每个 unit 含目标、文件、接口、依赖/并行、预期红测或失败门禁、命令、双评审、literal commit 和完成标准 | 当前满足（生成方式证据受限） | G-01/G-02A/G-02B 已 PASS；G-02C 与其余 65 个 unit pending。正式 `writing-plans` 未注册的限制继续披露，冷启动发现的问题须反向修订计划 |
| 陌生智能体冷启动 | 尚未执行 | 阶段门禁延后 | SPEC+PLAN 后由不同类型全新 session，仅提供两文件并记录提问、误解、差距与修订 diff |
| worktree/subagent/TDD/两阶段评审 | 尚无正式实现 | 阶段门禁延后 | 获准实现后每 task 新鲜 subagent、先红后绿再重构、先规约合规评审再质量评审 |
| 一键测试 | 无测试命令、测试代码或本次运行证据 | 阶段门禁延后 | PLAN 选择统一命令并覆盖 M1/M2/M3、安全策略、adapter contract 和端到端关键流 |
| GitHub Actions | D-023 已确认 GitHub 镜像保留 Actions；`.github/workflows/ci.yml` 不存在 | 阶段门禁延后 | 实现每次 push 调用与 GitLab 相同的一键测试入口并实际运行；镜像/push/PR 需执行当时授权 |
| GitLab `unit-test` job | D-023 已确认 NJU Git/GitLab 主仓；`.gitlab-ci.yml` 不存在 | 阶段门禁延后 | 最终硬交付；job 名必须严格为 `unit-test`，最后一次课程 CI 必须通过 |
| GitHub/NJU Git 与 PR/MR 历史 | D-023 已确认 NJU Git/GitLab 主仓 + GitHub 镜像；当前只有本地小步文档提交，无远程/PR/MR | 文档覆盖，未验证 | 未经执行当时授权不 push、建 PR/MR 或启用镜像；实现阶段每 worktree 对应可审查 PR/MR |
| 分发形态 | 整体 SPEC 已确认 Windows x64 单文件 `ProjectB.exe` 方向 | 文档覆盖，未验证 | 按[技术栈与分发基线](research/TECH_STACK_DISTRIBUTION_BASELINE.md)选冻结工具；验证单文件/干净机/SmartScreen/数据保留 |
| README | 不存在 | 阶段门禁延后 | 随实现维护项目简介、安装、运行、分发、目录、安全、凭据、限制、第三方依赖与许可证 |
| 第三方许可证 | G-02A 已锁定 54 个 Python、166 个 npm 条目及审查许可证集合；OpenAI SDK Apache-2.0、PyInstaller exception、Open Design Apache-2.0 等已有证据。课件许可证未知且未入仓 | 当前阶段满足；最终分发未验证 | T-01 从证据锁生成生产 manifest，CI-01 重新扫描，README/分发包保留完整 notices；公开夹具仍只用合成或明确许可材料 |
| 公开 WebUI URL / CI/CD | OCI/mock/隔离合同已确认；G-02C 证实 HF Docker Space 创建需要付费方案；2026-07-22 已完成现有主机/Tailscale 与 Azure Students/Container Apps 的候选调查，但 D-025 未选择、未部署 | 明确缺口 | 学生选择已有 x64 Docker 主机（既有 HTTPS 或 Tailscale Funnel）、Azure for Students + Container Apps，或明确承担 HF 费用；确认 SPEC diff 后实测 build/run/HTTPS/隔离/CI |
| AGENT_LOG | 历史条目包含时间、task、skill、上下文、人工修改与教训；D-017 至 D-024 批量确认和当前审计均已记录 | 当前满足 | 后续每次真实决策/task 后即时追加，不回写或伪造历史证据 |
| REFLECTION 1500–2500 字 | 文件不存在 | 阶段门禁延后 | 必须由学生本人撰写；AI 只能在有学生初稿后按声明范围润色或指出论证缺口 |

## 严格解释

1. 课程原文把 Open Design 写为“强烈推荐”，但本仓库 `AGENTS.md` 对含 UI 项目将其提升为必须遵循的工作流；当前按更严格规则执行。
2. 通用要求同时写明 GitHub 仓库/PR/Actions，最终清单又强制 NJU Git 与 `.gitlab-ci.yml`。D-023 已确认采用 NJU Git/GitLab 主仓 + GitHub 镜像，并维护 GitLab `unit-test` 与 GitHub Actions 双 CI；该策略不等于授权当前会话执行远程 push、PR/MR、镜像或部署。
3. Project B 已明确不含课程定义的 agent，因此不需要 Project A 的 harness 内核、harness mock-LLM 单元测试或机制演示；但本项目仍应使用 provider mock 对受约束 AI 端口和权威状态隔离做确定性测试。
4. 阶段门禁解释“为什么现在没有实现”，不免除最终要求。没有实际命令输出、CI 记录或可访问 URL 时，不得声称测试、分发或部署已经完成。

## 当前最近门禁

`SPEC.md` 已于 2026-07-20 整体确认；G-01、G-02A、G-02B 已 PASS。G-02C 的唯一当前证据阻断是 D-025：HF Docker Space 的付费账号门槛与无付费授权冲突。现有主机/Tailscale 与 Azure Students/Container Apps 已有官方候选证据，但调查不等于学生选择或 selected-host 验证。除此之外仍须恢复正式 Superpowers `writing-plans` 调用或取得课程明确接受 fallback 的证据，再由不同类型全新 session 执行 G-03 冷启动；D-005 可先选择。Open Design 真实 project/run/artifact 后置 UI-01A，学生本人 brainstorming 反思不得由 AI 代写。D-025、正式 planning 证据、冷启动修订和再次批准前不开始正式实现。
## 2026-07-21 evidence update

This timestamped section is historical. Its 37-row/28-blocker result was true for the first ledger checkpoint and is superseded by the current update below; it must not be used as the current G-02 status.

## 2026-07-22 evidence update

G-02A passed at `22b516af7b6f4896c6127e75b2585435e407a3c0`; G-02B passed at `5ac9d47ddda845ed78f1758326fb547610274f4c`. G-02C has reviewed blocker checkpoint `be666537706b4c133673029d950e84f15ea3ae1b` and remains pending D-025. Standard evidence validation reports `PASS rows=63 explicitly_blocked=2 python_pins=54 npm_packages=166`; distribution-strict validation fails exactly on `host-cost` and `host-account`. No production source, provider call, account resource, paid plan, build, deployment, CI, README or REFLECTION was created.
