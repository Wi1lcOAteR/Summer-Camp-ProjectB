# DECISIONS_NEEDED

## 当前真正开放的人工事项

- **已解除的产品方向门禁**：学生于 2026-07-20 明确确认完整 `SPEC.md`；D-017 至 D-023 与 D-024 的“安装并使用 Open Design”方向已纳入 v1，不应重复提问。2026-07-21 学生又在 Open Design 界面实际选择 `frontend-design` + `default`（显示名 `Neutral Modern`），具体组合也已确认。`PLAN.md` 已按上游 `writing-plans` 规则通过透明 fallback 生成并审查，但当前会话仍缺少正式 `superpowers:writing-plans` 调用证据。
- **已确认但仍需工程验证的合同**：D-020 的精确 `ReviewPolicy v1`、Windows x64 单文件 `ProjectB.exe`、OCI demo、隔离限额与 Hugging Face Spaces Docker SDK 已随整体 SPEC 确认；它们仍须通过许可证、官方条款、构建/运行和安全验证，不能把“已确认方向”写成“已实现”。
- **新增部署决策 D-025**：2026-07-21 的当前官方文档已确认，新建 Gradio 或 Docker Space 需要付费方案；“CPU Basic 无小时费”不等于“可用免费账号创建”。2026-07-22 又完成替代路线的官方只读调查：已有 x64 Docker 主机可配现有 HTTPS 或 Tailscale Funnel，Azure for Students + Container Apps 是无需信用卡的托管候选；Cloudflare Quick Tunnel、Northflank Sandbox 与 Oracle Always Free 均有不适合作为当前最终路线的明确边界。调查不等于选择，G-02C 仍保持 pending。
- **学生本人过程证据**：课程审计要求学生用自己的话评价 brainstorming 的优点、不足与关键取舍；当前尚未提供，AI 不得代写或推断成学生观点。
- **当前阻断信号**：阶段 B 的内容已形成，但正式 `writing-plans` 流程证据尚未闭合；D-005 类型可并行选择，但执行阶段 C/G-03 前必须先恢复正式 skill 调用，或取得课程明确接受 fallback 的证据。冷启动修订和学生再次批准前不能进入实现。
- **外部环境门禁**：D-001 已复核为 Superpowers cache-only：当前 config 无 installed/enabled 状态、task 无 `superpowers:*`，正式 skill 证据仍缺；须在 Codex App 安装/启用并新建 task，或取得课程接受 fallback 的明确证据。D-024/D-003 的 MCP 注册、Open Design 0.15.1 daemon、内置完整 `frontend-design` 与学生选择的 `default`/Neutral Modern 均已验证；fresh task 的 `list_skills` 也成功，空项目列表和无活动上下文是实现前的真实状态。G-01 环境门禁已通过；实际 project/run/artifact 只在获准实现后的 UI-01A 中执行，Open Design 不需要无任务长期挂起。
- **执行时授权**：公开 demo 的 OCI、同构 WebUI、许可夹具/mock、隔离与 HTTPS 合同保持不变；实际托管平台须先解决 D-025。NJU Git/GitLab、GitHub 的建仓、push、PR/MR、镜像和远程 CI 配置也须当时授权。
- **工程核验而非学生决策**：OpenAI SDK/依赖许可证、动态数据政策、模型/容量/费用、材料权利、打包兼容性和干净机/浏览器/CI 证据。它们必须真实验证，但不应伪装成新的产品选择题。

## D-025 — 公开 OCI demo 的托管与费用冲突（待学生决定）

**状态：开放。2026-07-21 已从 Hugging Face 官方 `hub-docs` 当前提交核验：创建新的 Gradio 或 Docker Space 需要 PRO、Team 或 Enterprise 付费方案。2026-07-22 已完成替代路线的官方只读比较，详见 `docs/research/PUBLIC_HOSTING_ALTERNATIVES.md`。未选择替代平台，未创建账号资源、未添加付款方式、未消耗 student credit、未订阅、未部署。**

- **问题**：已确认的 Hugging Face Docker Space 首选方向无法在当前无付费授权下创建；必须确定课程所需公开 WebUI 的新托管路径。
- **为什么必须由你决定**：这会改变部署平台、账号/费用责任或已确认 SPEC，属于重大交付与成本决策，不能由智能体静默替换。
- **候选方案**：
  1. **推荐（若你已有资源）：使用现有学生/NJU 控制的 x64 Docker 主机**。已有域名/反向代理时沿用其 HTTPS；没有域名时可选择 Tailscale Funnel 提供 `ts.net` HTTPS URL。该方案保留同一 OCI/WebUI/mock/隔离合同且不新增云计算费用，但 Funnel 仍为 beta，主机、Docker 和隧道必须持续在线，并新增 tailnet policy 与公网暴露责任。
  2. **推荐的托管式备选：Azure for Students + Azure Container Apps Consumption**。官方当前学生方案无需信用卡并含 `US$100`/12 个月 credit；Container Apps 支持 `linux/amd64` OCI、默认 HTTPS FQDN、scale-to-zero 和月度免费 grant。你必须确认学生资格、允许创建 Azure 账号/资源并消耗 credit，同时禁止升级按量付费；registry、日志、网络、临时存储和冷启动仍须工程验证。
  3. **继续 Hugging Face Docker Spaces**，由你明确授权并承担符合条件的付费方案及周期性费用上限。该选择超出当前 Goal 的无付费授权，未确认前不会执行。
- **已筛除的当前最终路线**：Cloudflare Quick Tunnel 仅供测试/开发且有 200 在途请求与无 SSE 限制；Northflank Sandbox 创建资源前强制付款方式且官方称免费层不应用于 production；Oracle Always Free 多数注册需信用卡、存在 idle 回收，A1 又与当前 `linux/amd64` 镜像架构不符。Render/Koyeb 域名此前被浏览器安全策略禁止，本轮未绕过。
- **推荐方案及影响**：已有可持续在线主机时优先方案 1，改动最小；没有现成资源且符合学生资格时，方案 2 比无预算上限地订阅 HF 更保守，但仍会创建云账号/资源、消耗 student credit 并需要相应 SPEC diff。两者都必须由你选择，调查本身没有解除门禁。
- **不决定会阻塞哪些 task**：G-02C、G-03、T-01、DIST-02、公开 WebUI URL 与最终部署验收。G-02A、G-02B、冷启动提示词准备和不依赖托管商的文档工作不受影响。

以下 D-002 至 D-024 的已确认条目保留为 brainstorming 过程证据；其中候选/推荐均是**决策前历史比较**，不能覆盖后续确认结果。

## 2026-07-20 批量回答结果（已确认）

学生回复“感觉可以全A，你继续执行吧”，明确采用：

```text
D017=A, D018=A, D019=A, D020=A, D021=A, D022=A, D023=A, D024=A
补充：无
```

结果：OpenAI 参考 adapter；仅内置 adapter；基础期末材料范围；保守确定性调度；Windows x64/Python+React/SQLite/Credential Manager；合成或许可演示数据 + provider mock；NJU Git/GitLab 主仓 + GitHub 镜像和双 CI；安装并使用 Open Design。具体远程 push/PR/部署仍须执行时授权；Open Design 桌面端与 MCP 已安装/注册，2026-07-21 又实际选择完整内置 `frontend-design` + `default`（Neutral Modern），fresh MCP 只读发现成功，G-01 环境/选择门禁已 PASS；正式 project/run/artifact 后置 UI-01A。

## D-001 — Superpowers 安装与会话注册

**状态：开放。2026-07-22 只读复核纠正了旧结论：Superpowers v6.1.1 完整 bundle 只存在于 cache；`config.toml` 没有 Superpowers enabled plugin 或对应 marketplace，Codex CLI 的 marketplace/plugin 列表为空，当前 task 也没有 `superpowers:*`。此前 brainstorming 过程与 fallback PLAN 证据保留，但不能证明当前已安装或正式调用。详见 `docs/engineering/SUPERPOWERS_VALIDATION.md`。**

- **问题**：缓存 payload 存在，但 Superpowers 没有安装/启用到当前 Codex 环境，因此无法正式调用 `writing-plans`。
- **为什么必须由你处理**：Codex 的插件启用与会话注册发生在应用层；当前项目工作区不能修改该状态。
- **候选方案**：
  1. **推荐：在 Codex App 的 Plugins 中安装/重新启用 Superpowers，并新建 ProjectB task 验证实际 skill 清单**。
  2. 在已认证的 Codex CLI 中用 `/plugins` 安装，然后退出并开启新 CLI session；当前未认证 CLI 的空列表不能替代 App 安装。
  3. 取得课程明确书面接受：现有完整 fallback `PLAN.md` 可替代本次正式 `writing-plans` 调用。
- **推荐方案及影响**：方案 1 与官方插件加载规则和 Superpowers 自带 README 一致，不改写现有 brainstorming/PLAN 过程；新 task 只需正式运行 `writing-plans` 审核现有 SPEC/PLAN，并记录真实 diff。
- **阻塞范围**：不阻塞已有 `PLAN.md` fallback 草案的审查或 D-005 选择；但它阻塞阶段 B 正式闭合与 G-03 冷启动执行。恢复正式调用或取得课程明确接受 fallback 的证据前，不能把阶段 B 标为完成。

## D-002 — AI 辅助场景的产品主线（已选择，SPEC 已整体确认）

**状态：2026-07-19 学生回复“主线走 2 试试看”，选择学习辅导；后续 D-006 至 D-024 已把首版设计收敛为当前 `SPEC.md`。2026-07-20 学生明确确认完整 `SPEC.md`，本项不再开放重问。**

- **已知输入**：学生会反复使用模型帮助完成作业/项目、辅导学习和查找资料。
- **问题**：三类需求目前过宽；需要选定一个首要场景，才能继续识别真实痛点、目标用户和可验收结果。
- **为什么必须由你决定**：主场景会决定核心工作流、数据边界、是否需要 agent 以及至少三个模块如何围绕同一问题协作，课程禁止智能体代替学生决定。
- **候选方案**：
  1. **推荐：作业/项目协作** — 聚焦从理解要求、拆解任务、执行检查到形成可追溯交付物，最容易形成工程深度和客观验收标准。
  2. **学习辅导** — 聚焦诊断知识缺口、引导练习和追踪掌握度，用户价值明确，但必须避免退化为普通聊天问答。
  3. **资料检索与证据整理** — 聚焦多来源检索、可信度判断、引用与结论管理，验证性强，但需明确与通用搜索/研究工具的差异。
- **推荐方案及影响**：方案 1 与课程项目开发本身高度相关，学生能持续自用并产生真实过程数据；同时要设置学术诚信边界，避免产品目标变成“代写作业”。
- **课程适配比较（用于决策，不代表已选定）**：

  | 维度 | 作业/项目协作 | 学习辅导 | 资料检索与证据整理 |
  | --- | --- | --- | --- |
  | 可形成的三个核心模块 | 要求/约束提取；任务与进度；按 rubric 检查交付证据 | 知识诊断；引导练习；掌握度追踪 | 查询规划/检索；来源可信度与引用；证据笔记与综合 |
  | 相对普通聊天的差异 | 工作流状态、门禁和可追溯证据 | 自适应练习状态和长期学习记录 | 多来源证据链和可核验引用 |
  | 确定性自动测试空间 | 高：状态机、规则检查、rubric 评估可 mock | 高：题目状态、评分和复习调度可测试 | 中：数据模型可测试，但真实网页检索更易受外部变化影响 |
  | 主要风险 | 学术诚信、错误要求解析、范围过大 | 退化为问答、教学正确性难评估 | 来源质量、网页不稳定、版权与引用准确性 |
  | WebUI 展示力 | 高：任务板、证据链、验收视图 | 高：诊断、练习、进度视图 | 高：来源表、证据卡片、引用关系 |

- **分析边界**：以上比较仅依据课程工程约束和学生已描述的使用场景；尚无用户访谈、竞品调研或实际使用数据，不应当作产品价值已被验证。
- **阻塞范围**：已解除，可继续澄清学习辅导的具体问题；不解除后续设计与 SPEC 人工确认门禁。

## D-006 — 学习辅导的首要失败模式（已选择组合）

**状态：2026-07-19 学生选择方案 2 和 3，目标是大学学业中的“看懂”和“持续复习”。方案 1（避免直接给答案）仍作为学术诚信与教学交互边界，而不是当前首要价值主张。**

- **问题**：现有模型“辅导学习”仍可能只是聊天；需要确认学生最希望首先解决的真实失败模式。
- **为什么必须由你决定**：首要失败模式决定产品价值、模块行为和验收指标，不能只按工程实现便利性选择。
- **候选方案**：
  1. **推荐：被动得到答案却没有真正掌握** — 模型过早给出结论，用户缺少思考、练习、纠错和迁移检验。
  2. **解释不匹配当前水平** — 模型不知道用户已经会什么、卡在哪里，回答可能过难、过浅或跳步。
  3. **对话彼此孤立，学习没有连续性** — 模型不追踪目标、进度、遗忘和复习计划，每次都从头开始。
- **推荐方案及影响**：方案 1 最直接区别于“帮我答题”的普通聊天，也能自然引出诊断、引导练习和掌握度验证三个协作模块；但仍须由学生确认它是否真是最常遇到的问题。
- **选择影响**：产品暂定围绕两个连续环节设计：先根据学生已有理解提供适配解释，再把知识点掌握状态转化为后续复习安排。必须避免把二者做成两个互不关联的聊天功能。
- **阻塞范围**：已解除；课程、模块、行为、验收与整体规约均已确认，后续只受 Superpowers/Open Design 工具接入和实现顺序门禁约束。

## D-007 — 首个真实课程验证场景（已选择）

**状态：学生选择“操作系统基础”，并提供 15 份本地 PDF 课件作为真实材料；审计结果见 `docs/research/OPERATING_SYSTEMS_MATERIAL_AUDIT.md`。**

- **问题**：大学课程跨度很大；需要一个真实课程作为首个验证场景，才能定义输入材料、解释质量和复习效果的客观标准。
- **为什么必须由你决定**：课程内容决定是否需要公式、代码、图表、习题与引用支持，也决定学生能否亲自判断产品是否有效。
- **候选方案**：
  1. **推荐：选一门正在学习、资料可提供的具体课程** — 产品架构可保持通用，但 MVP 和验收先以该课程为基准。
  2. 先覆盖一类以文本/概念为主的大学课程 — 范围较宽，材料处理较简单，但验收容易模糊。
  3. 一开始覆盖文本、数学和编程混合课程 — 通用性最高，但输入解析、评测与 UI 范围明显扩大。
- **推荐方案及影响**：方案 1 能用真实讲义、作业和考试范围做端到端验证，也不妨碍以后扩展；需要学生给出具体课程名称。
- **已有研究约束**：`docs/research/LEARNING_SCIENCE_BASELINE.md` 表明后续应以自我解释、主动提取、分散复习和可解释的知识状态作为候选机制；但不同课程对概念、程序、计算与代码的要求不同，研究不能替代本项选择。
- **选择影响**：首版以操作系统课件中的概念、代码、图表和中英术语为真实验证材料；产品架构可保持课程通用，但不得在尚未验证时宣称支持所有课程。
- **阻塞范围**：已解除；材料外发、provider、凭据与演示边界已由 D-008/D-014/D-017/D-021/D-022 收敛。

## D-008 — 课程材料的云端数据边界（能力范围已确认）

**状态：学生指出本地解析可能造成课件内容失真，要求把处理方式留给用户选择。D-009 确认首次导入必须显式选择、按课程记住且不得静默扩大外发；D-014 又确认平台实现 L/P/F 三种能力；D-017 选择内置 OpenAI 参考 adapter，D-021 选择 Windows Credential Manager。动态政策/区域/费用仍须在调用前快照核验，但不再是本项产品决策。**

- **问题**：操作系统课件的再分发许可证未知，且内容可能包含课程内部材料；需要确认应用能把哪些内容发送给云端模型。
- **为什么必须由你决定**：这直接决定隐私、版权风险、模型/部署路线、凭据需求、成本和多模态能力，智能体不能默认扩大数据外发范围。
- **候选方案**：
  1. **推荐：本地解析与索引，仅按需发送最小必要片段** — 云端模型只看到当前解释/练习所需的少量文本或页面图像，并向用户展示本次发送范围。
  2. 允许发送整份相关 PDF 或整门课程文本 — 实现简单、上下文完整，但隐私、版权、成本与供应商留存风险显著增加。
  3. 课件完全不离开本机，仅使用本地模型/规则 — 数据边界最强，但模型质量、硬件要求、安装与分发复杂度更高。
- **推荐方案及影响**：方案 1 在学习质量和风险之间更平衡，也能明确测试“没有用户动作就不外发”和“只发送被引用片段”；仍需学生明确接受云端最小片段外发。
- **威胁模型基线**：`docs/research/COURSEWARE_THREAT_MODEL_BASELINE.md` 已列出方案无关的资产、信任边界、12 类威胁、候选控制与测试证据；它不替代本项人工选择。
- **已确认的产品原则**：用户可按课程或学习任务选择处理路径；界面必须同时说明预期保真度、外发范围、凭据/费用和已知解析限制；模式切换不得静默扩大数据外发。
- **确认结果**：三种模式 L/P/F 都进入第一版；课程没有隐式默认外发，用户显式选择。新增文件、从 L/P 扩大到 F 或更换 provider 均创建新的、绑定实际文件范围的 `ConsentRecord`。
- **确认后的边界**：第一版只支持内置 OpenAI reference adapter；凭据进入 Windows Credential Manager；调用前展示版本化政策/能力/费用快照。具体模型目录、区域资格、容量与费用是运行时/工程核验，不代表允许静默外发。
- **阻塞范围**：产品方向已解除；模式 F 的页码映射、政策快照、对象对账和删除/过期仍须实现与测试。

## D-009 — 首次导入与模式默认策略（已确认）

**状态：学生确认首次导入时直接询问用户，并通过多个引导步骤/对话框完成说明与选择。课程级设置会被记住，任何扩大外发范围的切换仍需重新确认。学生已认可首版 mockup，并确认双端横向时间线、二级信息展示、图标引导与完成页配置入口强调。可交互 mockup：`docs/mockups/course-import-onboarding.html`。**

- **问题**：既然处理路径由用户选择，首次导入课程时仍需定义如何做出选择，以及后续是否按课程记住设置。
- **为什么必须由你决定**：默认行为会在保真度与隐私之间产生实际偏向；错误默认可能导致课件失真或未经充分理解的数据外发。
- **候选方案**：
  1. **推荐：首次导入必须显式选择，并按课程记住** — 没有选择就不开始解析/上传；每次远端请求仍显示实际页面与片段，用户可临时覆盖。
  2. 默认本地解析并标示低置信度页面，用户按需升级到云端页面/文件处理 — 最安全但可能让首次体验显得不完整。
  3. 在首次课程同意后默认使用高保真云端处理，用户可切回本地 — 体验顺畅但外发和成本风险更高。
- **推荐方案及影响**：方案 1 最符合“留给用户选择”，避免产品设计者替用户隐式决定；会增加一次导入步骤，需要清晰的模式比较和后续可修改入口。
- **真实材料证据**：全量 932 页抽取没有空文本页或页面异常，但 95 页少于 100 个非空白字符、全部页面需要 Unicode 归一化且均含图像对象。本地解析可作为能力，但不能宣称等价于原始幻灯片；三种模式比较见 `docs/research/COURSEWARE_PROCESSING_MODES.md`。
- **模型影响**：领域模型把材料状态设为 `awaiting_policy`，并把课程级 `ProcessingPolicy` 与每次扩大外发的追加式 `ConsentRecord` 分离；详见 `docs/research/TUTORING_DOMAIN_MODEL_DRAFT.md`。D-009 已确认这一步强制交互并按课程记住。
- **选择结果**：采用方案 1。首次导入依次检查课程、选择处理方式、确认权限、进入课程；无选择时不开始正文解析或上传。设置按课程保存，低保真检测只提示，不静默升级模式。
- **视觉方向**：桌面端与移动端均使用顶部 X 轴四阶段时间线；主要结论通过字号、颜色、字重与字体区分，次要信息降级；熟悉图标配合短句替代冗长说明；完成页高强调展示“课程设置 › 材料与隐私”。
- **阻塞范围**：首次导入交互与视觉层级、Open Design 环境/选择门禁均已解除。正式 UI 仍等待正式 `writing-plans`、冷启动修订和实现批准；获准后 UI-01A 还必须执行真实 Open Design project/run/artifact 和浏览器视觉验收。

## D-010 — 第一版用户与运行边界（已确认）

**状态：学生确认第一版采用单用户、本地优先路线。本机 WebUI 或桌面窗口都可接受；由于课程硬性要求可访问 WebUI，交付基线采用本地 WebUI，桌面壳只作为可选增强。多用户服务、课件分享和资料协作暂不进入第一版。**

- **问题**：第一版是只服务学生本人并在本机保存私有课程数据，还是从一开始做带登录和数据隔离的云端/多用户 Web 服务？
- **为什么必须由你决定**：这会直接改变认证、所有权模型、凭据存储、课件保存位置、WebUI 部署、删除语义、测试范围与课程分发方案，属于重大产品和架构路线，不能由智能体代选。
- **候选方案**：
  1. **推荐：单用户、本地优先 WebUI** — 私有课件与学习状态保存在学生本机；浏览器访问本地服务，按确认范围调用云端模型；课程要求的公网 URL 使用合成/授权样例提供可体验演示。隐私边界最清楚，但需要同时维护本地运行与公开演示配置。
  2. **单用户、云端个人实例** — 只有一个所有者账号，应用和数据部署到服务器；跨设备方便且公网 URL 自然，但所有课件、状态与凭据治理都进入服务端范围。
  3. **多用户 Web 服务** — 支持注册/登录、多个学生和完整租户隔离；展示力更强，但认证、授权、配额、滥用防护、删除和运维会显著挤压学习闭环的实现深度。
- **推荐方案及影响**：方案 1 与当前“学生本人 + 本地操作系统课件 + 用户控制外发”的证据最一致，也更适合把工程深度投入材料保真、适配解释和持续复习；需要在部署设计中明确公开演示不含私人课件、不使用真实 key。
- **工程对比证据**：`docs/research/USER_DEPLOYMENT_BOUNDARY_OPTIONS.md` 逐项比较三种路线的拓扑、数据位置、凭据、公开 WebUI、测试、迁移和返工风险，并列出不随选择变化的核心合同。
- **选择结果**：采用方案 1。第一版只有本地 actor，不实现注册、登录、账号找回或多租户隔离；核心实体仍保留明确 owner/actor scope 以便测试归属和未来迁移。私有课件、学习状态和索引默认保存在本机，只有按课程策略确认的页面/片段可调用远端 provider。
- **延期范围**：多用户账号、课件分享、资料协作、教师视角和跨设备同步均不进入第一版；它们是未来方向，不应提前增加数据库或 UI 范围。
- **阻塞范围**：D-010 已解除目标用户、认证和数据位置方向的阻塞；D-021/D-022 已确认 Windows x64、本地 WebUI、Windows Credential Manager、公开 mock 数据、单文件分发和 OCI/Hugging Face 方向。具体打包器、平台官方条件与部署动作仍按工程证据及执行授权处理。

## D-011 — “看懂 + 复习”的首个知识点（已确认）

**状态：学生表示没有具体偏好并授权智能体从既有候选中选择。智能体按已记录的推荐与理由采用“并发中的互斥与竞态条件”作为第一版首个纵向学习闭环；复习、agent、provider 与部署已由后续 D-013、D-017、D-020 至 D-023 分别确认。**

- **问题**：从操作系统课件中选择一个具体知识点，作为 M1 来源定位 → M2 起点诊断/适配解释/理解检查 → M3 延迟复习的首个端到端验收样例。
- **为什么必须由你决定**：真正“卡住”的知识点和你能否判断自己已经理解属于学生体验，不能只按实现方便选；该选择会固定首批题型、知识依赖和成功标准。
- **候选方案**：
  1. **推荐：并发中的互斥与竞态条件** — 对应“多处理器编程、互斥、同步、并发 bugs”等真实课件；可用线程交错、临界区识别、错误执行轨迹和修复比较做确定性理解检查，概念与代码兼具。
  2. **进程与调度** — 可验证进程状态、上下文切换、策略选择和等待/周转等指标；计算结果客观，适合可解释反馈，但对课件视觉保真难点覆盖较少。
  3. **地址空间与地址转换** — 可验证虚拟/物理地址、映射、保护与异常；公式和结构图能检验多模态保真，但第一轮诊断与解释设计更复杂。
- **推荐方案及影响**：先用互斥/竞态建立最小学习闭环：学生能用自己的话解释竞态与临界区，能从两线程执行轨迹定位错误，能比较一种修复的正确性，并在延迟后的变式题中再次完成，而不是仅复述答案。
- **闭环设计证据**：`docs/research/FIRST_LEARNING_LOOP_CANDIDATES.md` 分别给出三种知识点的候选知识图、起点诊断、适配解释、理解检查、延迟复习、确定性测试种子和共同评分边界；不包含课件正文或正式题库。
- **选择结果**：采用方案 1。第一轮范围只包括共享状态、非原子读-改-写、线程交错、竞态条件、临界区和一种互斥修复的安全性理由；同步原语大全、内存模型、死锁证明与公平性算法不进入首个切片。
- **阻塞范围**：D-011 已解除 M2 首批探针/解释分支、M3 变式复习类型和确定性轨迹 oracle 的方向阻塞；来源页已形成可纠正映射，具体版本化间隔数值与正式题目属于 PLAN/实现证据，不是新的产品方向门禁。

## D-012 — 复习计划的目标时间语义（已确认）

**状态：2026-07-20 学生先确认“持续安排”，随后补充考试日期通常在学期末才给定；用户设置考试日期后，可以显式进入期末周学习模式，用往年卷和老师给定重点进行针对性突击。两次回答共同形成“学期中持续模式 + 可选期末周模式”，不是互相排斥的选择。**

- **问题**：复习计划主要围绕课程考试/截止日期倒排，还是以没有固定截止日期的长期掌握为主？
- **为什么必须由学生决定**：目标日期会改变 `CourseReviewGoal`、任务优先级、到期解释、最后冲刺行为和“成功”的时间窗口；这属于学习体验而不是实现参数。
- **选择结果**：默认采用 `continuous` 持续模式，不要求开学时已有考试日期。新课件分批到达后，系统先让用户确认新增/变化的可学习知识，再版本化调整计划。用户录入考试日期后，仅获得进入 `finals` 模式的条件；必须由用户显式进入，不能因为检测到日期就静默切换。
- **期末周输入角色**：用户可把往年卷和老师给定重点作为新的材料批次导入。系统将题型、知识点和难度分布映射到已经确认的课程知识，并结合薄弱证据形成可解释的优先级；来源、映射置信度和用户修正必须可见。
- **语义边界**：“拟合往年卷”在第一版仅指分析结构、知识点覆盖、题型和难度，并据此选择或生成同类练习；不表示微调/训练模型，不承诺预测原题，不处理泄露试题，也不自动上传任何资料。模型/provider 不能单独决定权威优先级、掌握状态或计划版本。
- **调度设计证据**：`docs/research/REVIEW_SCHEDULING_OPTIONS.md` 固定双模式状态流、任务原因合同、UTC/local date/IANA 时区语义和虚拟时钟测试；`docs/research/INCREMENTAL_COURSE_WORKFLOW.md` 固定增量导入、知识覆盖确认、计划修订和期末资料映射流程。
- **后续 D-019/D-020 结果**：`finals` 不设自动提前窗口，始终由用户在有效日期后显式进入；每日预算可选，未填时显示版本化默认；使用简单确定性间隔/证据规则，不采用 FSRS/BKT；新证据只重排未开始任务并可撤销；考试后归档/暂停并询问新目标。第一版材料只含 `lecture`、无答案 `past_paper`、`teacher_focus`，答案/个人笔记/作业延期。
- **阻塞范围**：产品方向已解除；具体工程数值、材料权利核验和学术诚信测试在 PLAN/实现中固化。

## D-013 — 第一版是否包含课程定义的 agent（已确认）

**状态：2026-07-20 学生回答“就用受约束AI功能吧”，选择方案 1。**

- **问题**：第一版只使用受应用状态机约束的模型功能，还是加入能自主多轮选择工具并根据验证反馈修正的学习规划/教练 agent？
- **为什么必须由你决定**：这不是模型或框架的小选择，而是产品自主性与工程范围。若包含 agent，课程要求自行编码主循环、工具分发和治理护栏，并用 mock/stub 做确定性测试；它会改变 M1-M3 权威边界、PLAN task、风险和验收。Project B 原文允许无 agent，因此不能以“课程可能更喜欢 AI”替你默认加入。
- **候选方案**：
  1. **推荐：受约束 AI 功能，不含课程定义的 agent** — 模型生成候选知识映射、解释、练习和期末资料分析；应用规则/用户确认负责流程、计划和掌握状态。范围最匹配已确认价值，也最容易证明可靠性。
  2. **有界学习规划 agent** — 用户发起重新规划后，agent 自主调用只读课程状态工具，提交候选计划，并根据确定性验证器反馈修正；用户确认后才激活。能展示真实 agent 主循环，但需要额外循环、工具、预算和安全测试。
  3. **全流程学习教练 agent** — 自主决定诊断、解释、练习和重排。交互最灵活，状态空间和安全面最大，会显著扩大第一版并可能削弱当前三个模块的完成度。
- **推荐方案及影响**：推荐方案 1。当前瓶颈是课件保真、知识确认、有效学习证据和可解释计划，而不是工具选择；普通 AI 功能已足以提供针对性学习。若你明确想展示 agent，方案 2 是可控折中，方案 3 应延期。
- **边界证据**：`docs/research/AGENT_BOUNDARY_OPTIONS.md` 列出每种方案的模型端口/工具、状态机、权威写入、治理护栏、mock 测试和 SPEC/PLAN 影响。
- **原阻塞范围**：M2/M3 模型接口、是否新增 agent 主循环与工具分发、威胁模型、技术选型、验收标准和后续 PLAN 拆分。
- **确认后的范围**：第一版不包含课程定义的 agent；M2/M3 可以继续定义受 schema、来源、预算和用户确认约束的模型端口，但不创建自主 agent 主循环或工具分发。

## D-014 — 第一版远端课程材料能力范围（已确认）

**状态：2026-07-20 学生回答“外发决策也留给用户自行决定吧，我们的平台只要实现对应的功能即可”。按上下文采用方案 2：平台实现 L/P/F 三种能力，由用户自行选择；该回答不授权默认或静默外发。**

- **问题**：第一版在本地解析/原页对照之外，提供到“经确认页面/片段远端处理”，还是还要提供整份 PDF/课程上传，或完全禁止课程材料外发？
- **为什么必须由你决定**：这会确定用户实际能选择的处理目录、课程材料外发上限、版权与供应商留存风险、远端文件生命周期、删除语义、凭据/成本和测试范围。不能因为 mockup 展示过三个候选就把整份外发当作已授权功能。
- **候选方案**：
  1. **推荐：本地解析 + 经确认页面/片段远端处理** — 用户可选择课程内容不外发，或在每次任务中预览并确认少量页面/片段；不提供整份 PDF 上传。能补救视觉失真，同时保持可审计范围。
  2. **再提供整份 PDF/课程云端处理** — 保留前三种模式；上下文可能更完整，但需实现文件上传、索引、留存、删除、成本和许可证治理。
  3. **课程材料完全不外发** — 只使用本地解析/规则或本地模型；数据边界最强，但本地多模态、硬件和分发负担更高，也可能无法充分解决保真问题。
- **推荐方案及影响**：推荐方案 1。它仍把数据边界选择留给用户，只是将第一版能力上限控制在页面/片段；整份上传可以在确认 provider、材料权利和真实必要性后扩展。
- **边界证据**：`docs/research/REMOTE_MATERIAL_CAPABILITY_OPTIONS.md` 比较三种目录的数据流、UX、风险、删除状态、测试义务和选择后的 SPEC/PLAN 影响；`docs/research/COURSEWARE_PROCESSING_MODES.md` 提供 932 页真实材料的保真证据。
- **原阻塞范围**：M1 正式处理模式目录、X1 同意/删除合同、provider 能力筛选、凭据/成本设计、相关验收和首次导入 mockup 的最终文案。
- **确认后的范围**：第一版正式提供 L（本地）、P（经确认页面/片段远端）和 F（整份 PDF/课程远端）三种模式；首次选择、每批新增文件和扩大范围均显式确认。D-017 后续选择 OpenAI 为唯一真实参考 provider。

## D-015 — 第一版 Provider 适配策略（已确认架构方向）

**状态：2026-07-20 学生回答“供应商让用户自己在config里面配置喽，我们写好适配器就行”。采用 provider-neutral 统一适配器/注册表：产品不硬编码或静默指定供应商，用户在本地设置中选择平台已实现的 adapter 并配置 provider profile。该回答不代表允许任意 endpoint、加载第三方插件或把 API key 写入明文 config。**

以下问题、候选和原推荐保留为 D-015 决策前的历史比较；当前架构方向以“确认后的范围”为准。

- **问题**：L/P/F 三种能力由一个 provider 紧耦合实现、由统一适配器连接一个真实参考 provider，还是第一版同时交付多个真实 provider？
- **为什么必须由你决定**：provider 策略会改变 F 的上传/索引/引用/删除生命周期、凭据与费用 UI、数据政策展示、测试矩阵和替换成本；不能在未核验政策时默认为某家服务，也不能把 provider 差异泄漏到领域层。
- **候选方案**：
  1. **推荐：统一适配器 + 一个真实参考 provider** — 先实现 provider-neutral 合同、完整 mock 和一家真实适配器；其他 provider 后续按能力声明接入。能真实验证 L/P/F，同时控制第一版范围。
  2. **单 provider 紧耦合** — 直接围绕一家 SDK 实现全部功能，初期代码少，但供应商政策/API 变化会直接影响领域层，迁移成本高。
  3. **第一版多个真实 provider** — 让用户选择两家或更多服务，但会显著增加凭据、政策、生命周期、成本和端到端测试；当前部分官方资料尚未核验。
- **当时推荐及后续结果**：当时推荐方案 1；D-016 采纳一个真实 adapter + mock，D-017 随后选择 OpenAI。这里的历史比较不再表示 provider 未决。
- **证据**：`docs/research/PROVIDER_STRATEGY_OPTIONS.md` 记录了本轮已核验的 OpenAI 官方资料、未核验的其他候选、统一适配器最低能力和各方案影响。
- **原阻塞范围**：provider adapter、凭据配置、模式 F 的真实端到端测试、费用/留存展示和后续 PLAN 拆分；不阻塞继续完善 provider-neutral 研究合同。
- **确认后的范围**：领域层只依赖统一能力、状态和错误码；无有效配置时 L 仍可用，P/F 失败关闭。非秘密 config 只含内置 adapter ID、受支持模型/参数、预算和 `credential_ref`；固定 endpoint 由内置 adapter 管理，用户不得提供任意 `base_url`。secret 隐藏录入并进入 Windows Credential Manager。更换 adapter/profile、模型/config 或政策快照必须产生新授权，旧远端对象单独追踪。D-016/D-017/D-018 已把首版限制为一个内置 OpenAI adapter + mock、无第三方 plugin。

## D-016 — 第一版真实 Provider Adapter 交付范围（已确认）

**状态：2026-07-20 学生回复“1”，选择一个真实参考 adapter + 统一接口/完整 mock；D-017 至 D-021 后续选择 OpenAI、仅内置 adapter、Windows x64 技术/凭据基线。具体受支持模型、动态区域/政策/费用仍须技术核验。**

以下候选保留为决策前比较证据；当前范围以“确认后的范围”为准。

- **问题**：统一适配器架构已确认后，第一版是交付一个真实参考 adapter、交付两个或更多真实 adapter，还是只交付 mock/接口并让用户自行扩展？
- **为什么必须由你决定**：真实 adapter 数量会直接改变首版可用供应商范围、SDK/许可证、凭据与政策 UI、F 的上传/索引/引用/删除测试矩阵，以及课程交付进度；“运行时由用户配置”不能替代项目对已支持 adapter 的明确承诺。
- **候选方案**：
  1. **推荐：一个真实参考 adapter + 统一接口/完整 mock** — 用户可配置该 adapter 的非秘密参数，核心状态机保持可替换；其他真实 adapter 后续加入。能提供真实 AI/F 链路证据，同时控制第一版范围。
  2. **第一版交付两个真实 adapter** — 用户能实际切换供应商，更能展示适配层价值，但每家都需独立核验政策、能力、凭据、删除与端到端测试。
  3. **只交付接口/mock，不内置真实 adapter** — 最容易保持 provider-neutral，但无法证明真实 AI 与模式 F 可用，不符合当前产品目标，风险最高。
- **当时推荐及后续结果**：推荐方案 1，且学生已采纳；D-017 后续把具体参考厂商收敛为 OpenAI。模型目录、动态区域/政策/费用是运行时能力/政策快照，不再是参考厂商选择题。
- **当前安全边界**：首版 config 只选择平台内置并经过 contract test 的 adapter；任意自定义 endpoint 或第三方 adapter/plugin 不在已确认范围，若未来加入需单独评估 SSRF、本地网络访问、供应链和能力伪报风险。
- **原阻塞范围**：真实 adapter 目录、SDK/许可证、凭据配置字段、政策快照、P/F 联网验证和 PLAN task 拆分；不阻塞继续完善 provider-neutral 合同。
- **确认后的范围**：第一版实现统一 `ProviderAdapter`/registry、完整 provider mock、共享 contract suite 和一个真实参考 adapter。只有该参考 adapter 承担真实 P/F 联网验证；其余 provider 只保留扩展点，不作为首版可用能力。参考实现不能成为静默默认，用户仍须显式配置 profile 与凭据并对每次外发授权。

## D-017 — 第一版真实参考 Provider（已确认：OpenAI）

**状态：2026-07-20 学生批量回复“全A”，选择 OpenAI API 作为首版唯一真实参考 adapter。**

- **问题**：D-016 已确认只交付一个真实参考 adapter；需要从具备官方 API、可核验数据政策并能覆盖 P/F 生命周期的候选中选择具体 provider。
- **为什么必须由你决定**：具体 provider 会决定 SDK/许可证、PDF/图像与文件接口、结构化输出、引用定位、上传/索引/删除语义、凭据字段、区域/留存/训练政策、费用和真实端到端测试。即使 adapter-neutral，也不能由智能体把一家服务悄悄写成首版唯一真实实现。
- **候选方向**：OpenAI API、Google Gemini API、Anthropic Claude API。逐项比较见 `docs/research/REFERENCE_PROVIDER_OPTIONS.md`：OpenAI 与当前 F 生命周期最接近但原生页码/视觉引用有缺口；Gemini 的 P 很强但文件政策层级和 F 引用/过期组合更复杂；Claude 的 P/页码 citations 较强但没有与当前合同直接对应的托管索引生命周期。若某家不能满足模式 F 的对象追踪和删除合同，将从候选中降级或排除。
- **决策前推荐与结果**：OpenAI 当时因 Files/Vector Stores 生命周期最接近现有 F 合同而被推荐，学生已明确选择。页码/视觉保真缺口仍必须通过本地映射或失败关闭，不能把选择写成无条件兼容。
- **当前安全边界**：不读取真实 key、不调用付费 API、不上传真实课件；研究只使用官方开发文档。G-02A 已核验 OpenAI Python SDK 2.46.0 为 Apache-2.0 并写入精确闭包；生产 manifest、CI 许可证重扫和最终分发 notices 仍由 T-01/CI-01 复核。
- **原阻塞范围**：真实 adapter 名称、SDK/许可证、模型/文件端点、凭据配置、政策快照、费用上限和 P/F 联网验收；不阻塞继续完善 provider-neutral 规约。
- **确认后的范围**：真实 adapter 使用 OpenAI Responses、Files、Vector Stores/File Search 与 Structured Outputs 的已核验能力；不默认固定模型版本，模型由受支持 profile 配置。原生 File Search 页码/视觉引用不足必须本地映射或失败关闭；文件/向量库对象与政策快照、删除/过期对账不可省略。SDK 许可证的证据基线已由 G-02A 核验；生产 manifest、CI notices 和最终兼容性仍由 T-01/CI-01/INT-01 复核。

## D-018 — Provider 配置是否允许自定义 endpoint（已确认：仅内置 adapter）

**状态：2026-07-20 学生批量回复“全A”，选择首版只允许平台内置并通过合同测试的 adapter/profile。**

- **问题**：用户在 config 中选择 provider 时，首版只允许平台已经实现并通过合同测试的 adapter，还是允许填写任意兼容 endpoint？
- **为什么必须由你决定**：自定义 endpoint 会引入 SSRF/本地网络访问、TLS/认证、兼容性伪报、供应链和无法核验的留存/删除政策；它会改变安全模型和 F 的可用性。
- **候选方案**：
  1. **推荐：仅平台内置 adapter** — config 只选择已实现的 adapter/profile；无任意 URL/plugin，未知能力失败关闭。
  2. **内置 adapter + 受限自定义 endpoint** — 仅对声明兼容性的 P 开放，allowlist/网络策略/能力探测通过后才可用，F 默认关闭。
  3. **任意 endpoint/plugin** — 灵活度最高，但首版无法验证生命周期、政策和供应链，不建议用于课程交付。
- **原阻塞范围**：config schema、SSRF 防护、能力快照、参考 adapter 的真实端到端范围。
- **确认后的范围**：第一版不接受用户填写任意 base URL，不加载第三方 adapter/plugin，不做自动兼容探测。OpenAI endpoint 由内置 adapter 控制；config 只选择受支持模型/非秘密参数和 `credential_ref`。未来增加 endpoint/plugin 必须重新触发安全与供应链评审。

## D-019 — 首版期末资料输入范围（已确认：基础范围）

**状态：2026-07-20 学生批量回复“全A”，选择 `lecture`、无答案 `past_paper` 与 `teacher_focus`；答案、个人笔记和作业提交延期。**

- **问题**：`past_paper`、`teacher_focus` 已确定为材料角色，但答案、个人笔记和作业提交是否进入第一版？
- **为什么必须由你决定**：这会改变材料模型、学术诚信、敏感数据、外发授权和公开演示夹具范围。
- **候选方案**：
  1. **推荐：lecture + 无答案往年卷 + teacher_focus** — 支持 PDF/图片/文本/手工重点；答案、个人笔记和作业提交延期。
  2. 增加独立 `answer_key` 与 `personal_note` 角色 — 不接收作业提交；每个文件单独授权并明确“参考资料/个人材料”而非权威课件。
  3. 全部支持 — 追加答案、个人笔记、作业/提交和其他考试材料，并为每类建立独立治理。
- **原阻塞范围**：M1 材料角色、M3 期末映射、学术诚信提示、测试夹具和公开演示数据。
- **确认后的范围**：`lecture` 首轮以 PDF 为真实样本；`past_paper` 支持不含答案的 PDF/图片/文本；`teacher_focus` 支持 PDF/图片/文本和手工录入。系统不导入答案 key、个人笔记、作业题目/提交或疑似泄露试题；公开演示只使用合成或明确许可材料。

## D-020 — 期末调度参数预设（已确认：保守确定性）

**状态：2026-07-20 学生批量回复“全A”，选择保守、可解释、版本化的确定性调度。**

- **问题**：在已确认“持续模式默认、日期 + 显式操作进入 finals”后，首版采用哪种调度控制强度？
- **候选方案**：
  1. **推荐：保守确定性** — 用户可随时录入日期但必须显式进入 finals；每日投入为可选用户预算；使用版本化的简单间隔/证据规则；新证据自动重排未开始未来任务并提供撤销；考试日后归档/暂停并询问新目标。
  2. 自适应算法 — 使用 FSRS/BKT 类间隔和自动重排，用户设置每日上限；学习效果潜力更高，但解释、参数和验证成本更大。
  3. 手动优先 — 每次计划重排都要求用户确认，系统只给建议；风险最低，但持续安排价值明显减弱。
- **原阻塞范围**：M3 规则版本、任务粒度、虚拟时钟测试、期末 UI 和计划验收。
- **确认后的范围**：已确认每日预算可选、确定性简单规则、无 FSRS/BKT、未来任务自动修订/撤销和考后暂停。**整体 SPEC 已确认的 v1 合同**：预算 10–480、30/90 默认、`[1,3,7,14,30]` 间隔、纯函数/排序/fixtures 与严格 `today_local > target_local_date` 边界；实现仍需验证。

## D-021 — 本地运行与技术/凭据预设（已确认：Windows x64 优先）

**状态：2026-07-20 学生批量回复“全A”，选择 Windows x64 优先、本地 WebUI、Python/FastAPI + React/Vite/TypeScript + SQLite、Windows Credential Manager/keyring 技术基线。**

- **问题**：第一版本地 WebUI 的目标平台与安全存储/技术路线采用哪种组合？
- **候选方案**：
  1. **推荐：Windows x64 优先** — 本地 WebUI + SQLite；Python/FastAPI + React/Vite 作为默认候选；Windows Credential Manager（通过成熟 keyring 适配）保存 secret；macOS/Linux 作为后续目标。
  2. 跨平台优先 — 从第一版支持 Windows/macOS/Linux，使用跨平台 keyring；分发、UI 和凭据测试矩阵更大。
  3. 容器优先 — Docker 运行本地/远端服务，凭据用受控 secret 注入或加密文件；跨平台获取容易，但与本地 OS 凭据和私有课件边界冲突更大。
- **说明**：选择预设后，语言内的小型库、目录结构和 SQLite schema 仍由工程实现按许可证/测试证据选择；不会因此默认引入桌面壳或多用户服务。
- **原阻塞范围**：SPEC 技术选型、凭据后端、分发脚本、CI 构建矩阵和 localhost 安全实现。
- **确认后的范围**：后端使用 Python/FastAPI，前端使用 React/Vite/TypeScript，持久化 SQLite；secret 通过成熟 keyring 适配 Windows Credential Manager，普通 config 仅保存引用；macOS/Linux 延期。**整体 SPEC 已确认的 v1 分发方向**：单文件 Windows x64 `ProjectB.exe`，最终用户无需 Python/Node/Docker。Python 3.13 只是兼容性候选；精确依赖/解释器/冻结工具在 PLAN 前按许可证与矩阵证据锁定。

## D-022 — 公开 WebUI 演示数据与 provider（已确认：合成/许可数据 + mock）

**状态：2026-07-20 学生批量回复“全A”，选择公开实例只使用合成/明确许可材料和确定性 provider mock，不持有真实 key。**

- **问题**：课程要求最终提供可访问 WebUI URL，但项目不能把私人课件或真实 key 放入公开服务；公开实例展示到什么程度？
- **候选方案**：
  1. **推荐：合成/明确许可材料 + provider mock** — 公开实例完整展示导入、确认、学习和复习流程，不持有真实 key；本地安装版再支持用户自己的真实 adapter。
  2. 合成/许可材料 + 可选用户自带 key — key 只在浏览器会话中使用且不落服务器；实现和安全说明更复杂。
  3. 公开实例使用项目持有的真实 provider key — 费用、滥用和凭据风险不可接受，不建议也不作为默认实现。
- **原阻塞范围**：公开部署拓扑、README URL、演示夹具许可证、CI/CD 和凭据威胁模型。
- **确认后的范围**：公开实例展示与本地版相同的核心 WebUI/状态机，但只用许可夹具与 mock；关闭真实凭据/provider egress。**整体 SPEC 已确认的 v1 demo 合同**：OCI container、隔离到期 session/限额；Hugging Face Spaces Docker SDK 曾是首选，但当前官方证据已证明其付费账号冲突，实际托管商等待 D-025。替代路线证据见 `docs/research/PUBLIC_HOSTING_ALTERNATIVES.md`；账号、registry、镜像 push 和部署仍需执行时授权。

## D-023 — 远程仓库与 CI 证据策略（已确认：双平台）

**状态：2026-07-20 学生批量回复“全A”，选择 NJU Git/GitLab 主仓 + GitHub 镜像，同时维护 GitLab `unit-test` 与 GitHub Actions/PR 证据。**

- **问题**：课程同时出现 GitHub PR/Actions 与 NJU Git/GitLab CI 的要求，首版采用哪种主仓/镜像策略？
- **候选方案**：
  1. **推荐：NJU Git/GitLab 主仓 + GitHub 镜像** — `.gitlab-ci.yml` 严格包含 `unit-test`，同时保留 GitHub Actions/PR 证据；远程 push/建 PR 仍需你实际批准。
  2. 只用 NJU Git/GitLab — 在 README/日志解释课程文本冲突，不维护 GitHub 镜像。
  3. GitHub 主仓 + GitLab 镜像 — 操作简单但可能缺失最终 NJU Git 硬项，风险最高。
- **原阻塞范围**：CI 文件、worktree/PR 证据、最终提交链接与最后一次 pass 记录。
- **确认后的范围**：NJU Git/GitLab 是课程提交权威；GitHub 镜像保留通用要求的 PR/Actions 证据。两套 CI 共享同一一键测试命令，GitLab job 名严格为 `unit-test`。当前授权不包含远程 push、建 PR 或创建仓库，这些操作仍需执行时确认。

## D-024 — Open Design 环境门禁（环境/选择已通过，正式 run 后置）

**状态：2026-07-21 学生在 Open Design composer 实际选择 `frontend-design` + `default`（显示名 `Neutral Modern`）并链接 `ProjectB`。Open Design 0.15.1 daemon 健康，fresh Codex task 的 `list_skills` 成功返回 built-in `frontend-design`；`list_projects=[]`、`get_active_context.active=false` 如实表示尚未创建 project/run。G-01 的环境与选择门禁已 PASS，阶段 B 计划仍为 41 个 planning group、69 个 dispatch unit。**

- **问题**：如何在不把 Open Design 运行时、skill 安装和正式 UI run 混成一个门禁的情况下，留下可复现证据？
- **为什么曾必须由你决定**：skill/design system 会约束整个 WebUI 的视觉与交互合同；智能体只能比较适配度，不能把候选静默写成学生确认。该决策已经通过学生的界面选择解除；后续真实 run 只消费已确认合同，不新增产品方向选择。
- **候选方案**：
  1. **推荐：`frontend-design` + `default`（Neutral Modern）**；生成真实 React/app 工作台，并加入项目覆盖：卡片半径最多 8px、letter-spacing=0、紧凑信息密度。实现后另用 `web-design-guidelines` 审查。
  2. `frontend-design` + `shadcn`；组件更紧凑、默认 8px radius，但视觉更单色，需要严格把 success/warn/error 只用于状态。
  3. 先运行 `design-brief` 生成自定义 design system；自由度高但会新增一次重大视觉确认，并可能与已确认 UI 约束冲突。
- **选择结果及影响**：学生采用方案 1。`frontend-design` 是完整 bundled Apache-2.0 工作流，`default`/Neutral Modern 明确用于 B2B tools/dashboard/utility；ProjectB 覆盖卡片半径、字距、密度与状态色。无需安装 catalog-only 的上游包，`web-design-guidelines` 留作实现后审查。完整比较见 [`docs/research/OPEN_DESIGN_SKILL_OPTIONS.md`](docs/research/OPEN_DESIGN_SKILL_OPTIONS.md)。
- **恢复动作**：无需保持 Open Design 长期开启或创建空项目。实际 UI-01A 获准后，临时开启 Open Design，创建/打开真实 ProjectB project，执行受控 run，记录 project/context/artifact 和审查证据；运行结束即可关闭。
- **原阻塞范围**：正式 WebUI 设计系统、UI 实现和视觉验收；环境验证后，前两项不再阻塞阶段 C 冷启动，实际设计 run 后置到 UI-01A。
- **阻塞范围**：G-01 已解除；正式 UI task 仍受正式 `writing-plans`、冷启动、实现批准和 UI-01A 的真实 Open Design run/TDD/浏览器证据约束。现有 HTML 仍只是 brainstorming mockup。

## D-003 — Open Design 接入（D-024 的历史别名；外部配置门禁）

**历史快照（已被 D-024 更新）：此前曾记录配置未注册或 daemon 不可达；当前应以 D-024 的“环境/选择门禁已通过、正式 project/run 后置”事实为准。**

**历史视觉 brainstorming 快照：当时 Superpowers visual companion 先因 Git Bash PATH 缺失失败，修正后又因本机拒绝绑定 `127.0.0.1:55535`（EACCES）失败；当时 Open Design MCP 尚未注册。当前已由 D-024 更新为“已注册、组合已确认、环境门禁通过、正式 project/run 后置”。已有自包含 HTML + Playwright/Edge 截图只用于需求澄清，不替代 Open Design 正式流程。**

- **历史问题**：课程最终要求 WebUI，而本项目约束规定含 UI 时使用 Open Design；当时桌面端已安装但 Codex MCP 尚未接入。
- **历史处理**：MCP 注册发生在项目工作区之外，已由用户随后完成；不要再次执行旧注册命令。
- **当前动作**：以 D-024 为准，环境门禁已经完成；实际 design system 与 skill 已由学生确认并记录进 `SPEC.md`。在获准实现后的 UI-01A 临时开启 daemon，执行真实 Open Design run 并记录 artifact/context，不提前生成或修改正式 UI。
- **阻塞范围**：不再阻塞 UI 方向选择或阶段 C 冷启动；仍约束正式 UI task 必须在 UI-01A 完成真实 Open Design run、TDD 和浏览器视觉证据。

## D-004 — 远程平台策略（D-023 的历史别名；已确认）

**状态：采用 NJU Git/GitLab 主仓 + GitHub 镜像，双 CI/PR 证据；远程写操作仍需执行时授权。**

- **问题**：课程原文同时要求 GitHub PR/Actions 和 NJU Git/GitLab CI，最终清单又强制 `.gitlab-ci.yml` 与 `unit-test` job。
- **为什么必须由你决定**：远程仓库归属、镜像策略和 PR/MR 证据属于学生账号与提交策略，且用户未授权远程 push/建 PR。
- **候选方案**：
  1. **推荐：NJU Git/GitLab 为主，GitHub 作公开镜像**；GitLab CI 满足硬提交，GitHub Actions/PR 保留通用要求证据。
  2. 只用 NJU Git/GitLab，并在 SPEC/日志中解释课程文本冲突及取舍。
  3. 只用 GitHub（风险最高：可能缺失 NJU Git 与 GitLab CI 硬项）。
- **推荐方案及影响**：方案 1 最保守但维护两套 CI；具体远程操作仍需你在执行时批准。
- **阻塞范围**：策略已解除；只剩建仓、push、PR/MR、镜像、远程 CI 与部署的执行时授权和真实证据。

## D-005 — 冷启动智能体类型（后续门禁）

**状态：`SPEC.md` 与 fallback `PLAN.md` 内容已具备，D-005 可先选择；但正式 `writing-plans` 过程证据未闭合，G-03 仍不得执行。**

- **问题**：当前未检测到 `claude`，而冷启动必须使用不同类型智能体的新 session。
- **为什么必须由你决定**：可能涉及安装并登录另一种智能体，且只能由学生控制账号与授权。
- **候选方案**：
  1. **推荐：Claude Code + Superpowers**，与主开发 Codex 类型不同，课程材料也明确举例支持。
  2. 使用另一种课程允许的智能体（Cursor Agent、Gemini CLI、OpenCode 等），确保全新 session 且仅提供 SPEC/PLAN。
- **推荐方案及影响**：方案 1 与现有准备文档一致；需要学生自行控制安装、登录和账号授权。若已有 Cursor/Gemini/OpenCode 等不同类型工具，方案 2 可减少安装工作，但仍必须全新 session 且只给 `SPEC.md` 与 `PLAN.md`。
- **执行边界**：G-03 是正式实现前的一次性可理解性实验，初始只能看 `SPEC.md` 与 `PLAN.md`。其候选 unit 的正式依赖此时故意尚未实现，冷启动只能创建不合并的最小临时 scaffold/test double；普通依赖规则在后续正式派发时重新生效。
- **阻塞范围**：阶段 A/B 已完成到可审查计划；本项阻塞阶段 C 冷启动验证，继而阻塞规约修订后的实现批准。
## G-02 historical external blockers (2026-07-21; superseded)

This section preserves the truthful pre-evidence checkpoint and is not the current status. It has been superseded by the 2026-07-22 G-02A/G-02B PASS records, the G-02C blocked checkpoint, and D-025 above. No new product decision was requested at the time. The confirmed choices then remained: Windows x64 local WebUI, one built-in OpenAI adapter plus deterministic mock, and an OCI/Hugging Face public demo direction.

- At that checkpoint the repository had no project dependency manifest or lockfile, so exact versions and transitive licenses were still pending.
- At that checkpoint OpenAI policy facts were recorded but the selected model/cost preflight and F scope/lifecycle proof were not verified; real P/F calls remained disabled.
- At that checkpoint freezer, OCI digest and Hugging Face terms could not be retrieved. No account, deployment, paid resource or host substitution was created.

The current safe action is no longer a generic recheck: G-02A and G-02B are closed with cited evidence, while D-025 is the remaining student decision for G-02C. Historical wording is retained to preserve process evidence and must not be used as the current blocker list.
