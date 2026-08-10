# ProjectB 精简 v1 规约

<!-- AGENT_CAPSULE:SPEC:BEGIN -->
# Agent Execution Capsule (generated; do not edit)

Version: 1. This ASCII capsule is a normative execution projection of the cited sections in the Chinese specification. The Chinese body remains authoritative for the complete product. Any conflict between this capsule and the body invalidates the document and must be reported as an ambiguity; do not choose a silent precedence.

## Product and users
ProjectB is a local-first study workbench for a student who needs traceable ingestion, deterministic practice, and repeatable review planning. It must remain explainable as three useful modules, not a single-turn chat wrapper.

M1 imports incremental digital PDF and UTF-8 TXT/Markdown. Preserve original-byte SHA-256, immutable material versions, PDF page or text-line source locators, and explicit user confirmation or rejection of knowledge-concept mappings. OCR, images, scanned documents, bulk ingestion, past-exam intelligence, and automatic mapping are deferred.

M2 uses a general knowledge-concept model. V1 acceptance covers mutex, race condition, and deadlock. Explanations and exercises bind to confirmed sources. Deterministic local evaluators produce append-only learning evidence; explanation-only concepts must not create mastery evidence. A real LLM may improve explanation text but must not own scoring, evidence, mastery, or plan state.

M3 derives deterministic mastery state and continuous/finals review plan revisions from the full append-only evidence history. Repeated identical inputs produce identical task order and plan hash. Completed tasks are not rewritten; new evidence or settings produce an auditable revision diff.

## Data and provider boundary
The default L profile is local and offline. Optional P mode has one built-in OpenAI adapter plus mock. Each remote request requires user preview and one-time consent bound to exact locator, material hash/version, provider port/profile, and budget. Send only the confirmed page or text fragment; never upload a whole file, use hosted file/tool behavior, or set store true. Provider failure must not mutate coverage, evidence, mastery, or plan state. The temporary Claude-compatible G-03 gateway is a process tool and is not a product provider.

## Security and credentials
Treat uploaded bytes, filenames, URLs, model output, and tool arguments as untrusted. Enforce magic/type and size/page/line limits, strict decoding, path containment, timeouts, output schema validation, safe Markdown rendering, loopback Host/Origin/CSRF controls, stable redacted errors, and an audit-field allowlist. Never log student answers, material text, consent previews, credentials, decoded secret payloads, or blob OIDs.

Credentials use Windows Credential Manager in local profile. First run provides hidden entry and status/update/clear operations; status never echoes a value. No real secret may be stored in SQLite, config, browser storage, Git, logs, fixtures, snapshots, process arguments, or committed environment files. Runtime test fixtures assemble secret-shaped positives from non-matching fragments. Every implementation/evidence commit is scanned. Third-party code and assets require source and license records.

## Agent and delivery boundary
V1 contains no autonomous multi-round agent. If later added, its loop, tool dispatch, guards, and deterministic mock tests require a new student-approved specification. The shipped application must provide a React WebUI, Windows x64 single-file distribution, an OCI mock demo, GitLab CI with a job named unit-test, GitHub CI evidence, and one-command tests. Delivery is local-only for this project: a local WebUI URL and architecture are required, while public HTTPS hosting and public URL evidence are waived by the student's D-025 decision. Remote push, PR, deployment, paid resource creation, G-04 implementation approval, and student reflection remain human gates. REFLECTION.md must be written by the student; AI may only polish a supplied draft and declare assistance.

## Baseline acceptance used by G-03
Before product implementation, a fresh non-Codex intake session and a separate execution session receive only final SPEC.md and PLAN.md. Intake must report both full-file SHA-256 hashes, the complete two-file listing, effective language, target F-01S1A, acceptance ID F01S1A_SINGLE_RULE_SCANNER_V2, and ambiguities. Execution starts only when ambiguities are empty. It creates only scripts/tests/bootstrap_scanner_contract.ps1 and scripts/bootstrap_scan_credentials.ps1, implements the locked single-path protocol plus provider_api_key rule, demonstrates the exact missing-scanner red and unchanged-command green, stays within the artifact and final-summary budgets, and never commits or integrates output. Formal implementation repeats F-01S1A after G-04; F-01S1B serially adds the remaining direct rules.
<!-- AGENT_CAPSULE:SPEC:END -->

> **状态：2026-08-03 G-03 原子执行规约已由学生确认。** 学生于 2026-07-25 确认的产品方向和 2026-08-01 确认的原子执行设计是本次修订基础，并于 2026-08-03 明确确认本次完整 SPEC。两次 execution 长时间 thinking、无候选文件及一次 `source` 猜测作为真实失败证据保留；网关延迟、内部规划循环和输出上限均未被冒充为已确认根因。旧 SPEC/PLAN 哈希、评审和 intake 不转移到当前字节。

> **2026-07-27 过程修订：** Claude Code、Gemini CLI 与 GitHub Copilot CLI 当前均因访问或账号条件不可用。学生明确授权先用全新 Codex 任务做同类型占位预审 `G-03P`，待可访问非 Codex 类型后补做正式 `G-03`。这项修订不改变产品功能范围；`G-03P` 不满足“不同类型智能体”要求，也不解除实现门禁。
>
> **实现门禁：** 本次完整 SPEC 已确认，`superpowers:writing-plans` 已用于重写 `PLAN.md`。完整计划双评审、不同类型智能体冷启动、缺陷修订和学生再次明确批准实现完成前，禁止创建正式实现源码。

## 1. 问题陈述

### 1.1 要解决的问题

大学课程材料分散在 PDF、文本讲义和临时笔记中。学生往往能读完材料，却难以回答三个持续问题：某个知识点依据哪一页材料、自己是否真正理解、今天应该复习什么。通用聊天工具会把材料事实、模型补充和掌握判断混在一起，也缺少可重复的检查与复习状态。

ProjectB 是面向单个学生的本地优先课程学习工作台。它把材料来源、知识点、确定性理解检查和复习计划连接成一条可审计闭环；AI 只能生成来源绑定的解释、练习候选和措辞反馈，不能决定正确性、掌握状态或复习优先级。

### 1.2 目标用户与 30 秒说明

首版用户是使用 Windows x64、需要整理计算机课程材料并准备平时复习或期末考试的单个学生。第一条验收课程是操作系统并发基础。

> 导入课件后，ProjectB 让你确认“哪些页支持哪个知识点”，用确定性题目检查是否真正理解，再按每天可用时间生成可追溯的复习计划。课件默认留在本机；只有你逐次确认的片段才会发给模型。

### 1.3 第一版成功标准

- 至少提供 M1 材料与来源、M2 学习检查、M3 复习计划三个职责清晰的模块。
- 用户可以从新安装的 Windows x64 应用完成“导入 -> 映射 -> 学习 -> 复习”全流程。
- 核心规则在移除真实模型后仍可用 deterministic mock 和自动化测试验证。
- 提供一键测试、GitLab/GitHub CI、Windows 单文件分发、OCI demo 和可本地访问的 WebUI URL。

## 2. 用户故事

1. **US-01 导入材料：** 作为学生，我希望增量导入数字 PDF、TXT 或 Markdown，以便在同一课程中积累可检索材料，而不上传到第三方。
2. **US-02 核对来源：** 作为学生，我希望把具体页或文本行确认到一个知识点，以便任何后续解释和复习任务都能回到原文。
3. **US-03 获取解释：** 作为学生，我希望选择已确认来源后获得适合当前水平的解释，并在外发前看到精确片段和风险，以便控制材料边界。
4. **US-04 检查理解：** 作为学生，我希望完成结构化练习并得到确定性评分，以便模型措辞不会改变正确性或掌握状态。
5. **US-05 持续复习：** 作为学生，我希望按每天可用时间得到稳定的复习计划，以便课程推进时持续安排旧知识。
6. **US-06 期末模式：** 作为学生，我希望设置考试日期并压缩未掌握内容的复习间隔，以便计划不会排到考试之后。
7. **US-07 管理凭据与隐私：** 作为学生，我希望隐藏录入、更新和清除 API key，并删除本地材料，以便秘密和私人材料不会出现在配置、日志或演示环境中。
8. **US-08 体验公开演示：** 作为访客，我希望无需上传文件或配置 key 就能体验完整流程，以便了解产品而不会产生真实 provider 调用或持久化私人数据。

这些故事均有单一用户价值、可独立验收；具体边界固定在下列模块合同中，避免实现时重新解释。

## 3. 功能规约

### M1 课程材料与来源工作区

| 项目 | v1 合同 |
| --- | --- |
| 输入 | 可提取文本的数字 PDF、扩展名 `.txt` 的 UTF-8 文本、扩展名 `.md` 的 UTF-8 Markdown |
| 行为 | 校验类型和限制，计算原始文件字节 SHA-256，将原文件保存在当前用户应用数据目录，将材料元数据和抽取文本写入 SQLite；重复哈希在同一课程内返回同一 `Material`，相同原件由不同 parser contract 处理时追加 `MaterialVersion`；每个文件独立事务，批次返回逐文件结果 |
| 输出 | `Material`、`MaterialVersion`、抽取状态、PDF 页目录或文本行目录 |
| 边界 | 每次最多 5 个文件、单文件最多 20 MiB、单次总计最多 50 MiB、PDF 每文件最多 200 页、文本最多 1,000,000 个 Unicode code points |
| 错误 | 类型伪装、超限、无可提取文本、非法 UTF-8、解析超时或损坏文件均在权威写入前失败；不得留下半完成材料版本 |

`content_hash` 是原始文件字节的 SHA-256，格式为 64 个小写十六进制字符，不带前缀。PDF 中允许空白页，但整份 PDF 没有任何可提取文本时返回 `unsupported_scanned_pdf`。OCR、图片输入和扫描件属于延期能力。批次先校验总文件数/总字节限制，再按文件提交；一个文件失败不回滚其他成功文件，但失败文件不得留下 Material、原件或抽取内容。

TXT/Markdown 解码必须拒绝非法 UTF-8，并在抽取视图中把 CRLF/CR 规范化为 LF 后编号；原始文件和 `content_hash` 不做规范化。PDF 抽取结果记录 parser ID/version，升级 parser 只能在同一逻辑 `Material` 下创建新的 `MaterialVersion`，不能静默改写旧 locator。`MaterialVersion` 的唯一键为 `(material_id, parser_id, parser_version, extraction_contract_version)`；locator 必须绑定 `material_version_id` 和原始 `content_hash`。

原始字节存储以全局 `content_hash` 为内容地址，但每个课程拥有独立的 `Material` 和 `MaterialBlobRef`。两个课程导入同一字节时可共享一个 blob，删除一个课程中的材料只删除该课程的逻辑材料、版本和引用；只有事务提交后已不存在任何 `MaterialBlobRef` 时才可删除 blob 字节。删除失败必须保留可重试 tombstone，不得先删共享字节。相同课程+相同 hash+相同 parser contract 完全幂等；相同 hash+新 parser contract 只新增版本。

来源只允许两种判别联合：

- PDF：`{kind:"pdf_page", material_id, material_version_id, content_hash, page}`，`page` 从 1 开始且存在于该 `material_version_id` 的已验证页目录。
- 文本：`{kind:"text_lines", material_id, material_version_id, content_hash, line_start, line_end}`，行号从 1 开始且形成该版本中的非空闭区间。

用户创建或编辑 `KnowledgeConcept`，再从有效 locator 中确认 `CoverageDecision`。系统不在 v1 自动分析往年卷、老师重点或整门课程。材料删除会移除本地原件和抽取内容，使相关 locator、coverage 和未开始复习任务失效；历史证据只保留不含正文的 tombstone 与 opaque ID。

### M2 来源绑定学习与确定性检查

`KnowledgeConcept` 是通用实体，至少包含 `concept_id`、`course_id`、名称、可空 `evaluator_id`、版本和状态。v1 自带三个 evaluator：

- `os.mutex.v1`：判断给定事件序列是否保持临界区互斥不变量。
- `os.race.v1`：展开 read/modify/write 事件，校验线程内顺序、事件完整性和最终共享状态。
- `os.deadlock.v1`：根据资源分配或 wait-for 图确定是否存在环，并校验给出的环路径。

没有受支持 evaluator 的知识点仍可绑定来源和获取解释，但 UI 必须标记为 `explanation_only`，不得产生掌握结论。

模型只通过三个具名端口工作：`generate_explanation`、`generate_practice_candidate`、`generate_feedback_wording`。端口返回候选文本或结构化练习，不拥有课程事实、评分、掌握状态或计划写入权。首版不包含自主多轮决策、工具自主调用或反馈自修正，因此不属于课程定义的 agent。

模式固定为：

- `L`：默认。本地解析、来源选择、deterministic evaluator、证据和计划均不调用 provider。
- `P`：请求级外发。每次调用前展示将外发的精确 locator、抽取片段、端口、模型 profile、token/费用上限和政策摘要；只有用户确认后才创建不可变 `ConsentRecord` 并发送请求。

P 请求只能包含已确认、哈希仍匹配的来源片段和最少必要指令。学生答案正文只在本地保存；反馈端口最多接收确定性 rubric 结果和已确认来源，不接收原始答案。OpenAI adapter 使用 Responses API、`store:false`、无 hosted tool/File/Vector Store、受控超时和输出 schema。任何能力、定价或政策证据过期时失败关闭，不静默换模型、endpoint 或 adapter。

`LearningEvidence` 是不可变追加记录，至少包含 evidence/attempt/course/concept ID、evaluator 及版本、`check_kind`、`outcome`、按 ID 排序的 rubric 结果、source locator ID、发生时间和 evidence version。`check_kind` 只允许 `starting_probe`、`isomorphic`、`transfer`、`delayed_variant`；`outcome` 只允许 `incorrect`、`partial`、`passed`、`refused`、`source_insufficient`、`skipped`。重复 `attempt_key` 不得追加第二条证据。起点探针不写永久负面标签；只有通过的结构化检查可以提高掌握估计。

掌握状态只允许 `unknown`、`demonstrated_now`、`retained`。同一知识点至少有一条通过的 `isomorphic` 和一条通过的 `transfer` evidence 后为 `demonstrated_now`；至少跨一个本地日再通过不同 `variant_id` 的 `delayed_variant` 后为 `retained`。来源不足、provider 失败、跳过或拒绝不降低也不提高掌握状态。

### M3 确定性复习计划

`ReviewPolicy v1` 是纯函数合同：

- 模式只允许 `continuous` 或 `finals`；IANA 时区必填。
- `daily_budget_minutes` 为 10--120、步长 5、默认 30；任务时长固定为 10 分钟，不拆分、不超预算。
- 基础复习间隔为 `[1, 3, 7, 14, 30]` 天。
- `continuous` 直接使用基础间隔。`finals` 按生成时的 mastery 使用固定倍率压缩每个基础间隔：`unknown=1/2`、`demonstrated_now=3/4`、`retained=1`，采用整数向上取整且最少 1 天；因此三种状态的间隔分别为 `[1,2,4,7,15]`、`[1,3,6,11,23]`、`[1,3,7,14,30]`。同日重复 due date 只保留最弱 evidence 对应的一个任务。
- 稳定优先级依次为 evidence weakness、请求日期、concept ID；系统/来源错误不伪装成学习失败。
- `continuous` 生成未来 30 个本地日；`finals` 必须提供考试本地日期，压缩后仍晚于考试日期的任务被截断，所有任务不得晚于该日期，日期已过去时生成零任务并进入归档状态。
- 相同规范化输入必须得到相同任务顺序和 `plan_input_hash`；输入未变化时不创建新 revision。

计划 revision 追加保存。重新导入、coverage 变化、新 evidence、预算/考试日期变化会生成可比较的新 revision；已完成任务不被改写，未开始任务可以按上一 revision 恢复。v1 不提供通知、日历同步或跨设备同步。

### X1 凭据、安全与审计

- 本地服务只绑定 loopback；校验 Host、Origin 和 session-bound CSRF，禁止 LAN/public 监听。
- API key 只通过隐藏输入进入 Windows Credential Manager。SQLite、配置、浏览器存储、日志、测试、快照、`.env` 和 Git 不保存秘密。
- 凭据状态只返回 configured/unconfigured 和更新时间；支持更新与清除，不回显明文。
- 上传文件、抽取文本、URL、provider 输出和工具参数均视为不可信输入；执行类型、大小、schema、权限、超时和输出限制。
- 审计事件使用字段白名单，只记录 opaque ID、动作、结果、政策/配置指纹和脱敏错误码，不记录路径、正文、答案或 secret。
- 提交前运行 fail-closed 凭据扫描；发现疑似真实凭据立即停止且不得复述完整值。

### X2 Provider 与 demo profile

- local profile 只注册内置 OpenAI adapter；不接受任意 `base_url`、plugin、动态 adapter 或未知字段。
- deterministic mock 只在测试和 demo profile 注册，禁止在 local production 被静默选中。
- demo 只加载仓库内合成或许可 fixture，禁止上传、凭据输入、provider 出网和跨 session 持久化；每个 session 使用隔离临时状态并在过期后删除。
- demo 与本地应用共享领域合同和 WebUI，不维护另一套功能逻辑。

## 4. WebUI 交互规约

WebUI 使用 Open Design 的 `frontend-design` skill 与 `default` / Neutral Modern 设计系统，面向工作台而非营销页。真实 Open Design project/run/artifact 在获准实现后的 UI task 中产生，环境验证本身不能代替实际 run。

主导航固定为“导入 -> 映射 -> 学习 -> 复习”四阶段，并提供独立设置入口：

- 导入页显示文件限制、逐文件结果和可恢复错误。
- 映射页并排显示来源片段与知识点，只有显式确认才产生 coverage。
- 学习页显示来源、解释、结构化练习、确定性 rubric 和 evidence 状态；模型补充必须可辨识。
- 复习页显示今日预算、任务来源、掌握状态、计划 revision diff、连续/期末模式。
- 设置页提供 provider profile、隐藏凭据操作、隐私范围、安全状态和材料删除。

桌面和 360 px 宽移动视口不得出现横向溢出或文字遮挡。所有交互可键盘完成，焦点可见，状态不只依赖颜色，表单错误与控件具有关联标签。卡片圆角不超过 8 px，`letter-spacing: 0`，不使用营销 hero、嵌套卡片或装饰性渐变球。

## 5. 非功能需求

### 5.1 性能与可靠性

- 已缓存的本地非导入 API 在合成数据下 p95 小于 500 ms。
- 单文件导入最长 30 秒；超时返回可重试错误且不提交半完成版本。
- provider 请求默认 60 秒超时、一次显式重试上限为 0；用户可重新发起并生成新的 consent。
- Windows 应用在参考环境冷启动后 10 秒内提供可访问 WebUI。
- SQLite 写入使用事务；重复导入、attempt 和 plan generation 有确定性幂等键。

### 5.2 可观测性与错误处理

- 日志使用结构化事件和 request ID，不包含正文、路径、答案或凭据。
- 稳定错误码至少包含 `unsupported_type`、`file_too_large`、`content_unreadable`、`unsupported_scanned_pdf`、`source_stale`、`consent_required`、`provider_unconfigured`、`provider_unavailable`、`invalid_attempt`、`state_conflict`。
- 错误必须说明是否可重试以及用户可采取的下一步，不把内部异常或 provider 响应原文直接展示给用户。

### 5.3 测试与质量

- 提供一条项目级命令 `python scripts/test_all.py`，运行 backend unit/integration、frontend unit/build、凭据扫描和必要 contract tests。
- 核心规则使用 pytest/Vitest 和 deterministic fixtures；浏览器流程使用 Playwright，自动检查 360/768/1440 px、键盘流程和 axe 无严重违规。
- 每个行为 task 严格红--绿--重构，并在提交前做 SPEC 合规评审、质量/安全/许可证评审和全量回归。

## 6. 架构与数据流

```text
React/Vite WebUI
  -> FastAPI loopback API + Host/Origin/CSRF boundary
  -> Application services
       M1 import/source/coverage
       M2 explanation/practice/evaluator/evidence
       M3 mastery/review planner
       X1 credential/consent/audit
  -> SQLite metadata and current-user content-addressed material store
  -> Windows Credential Manager
  -> Local parser
  -> Provider-neutral port -> OpenAI adapter OR deterministic mock
```

权威数据流是：校验并导入原始文件 -> 生成页/行目录 -> 用户确认 concept/source coverage -> 本地检查来源有效性 -> 可选 P consent/provider 候选 -> deterministic evaluator -> 追加 evidence -> 推导 mastery -> 生成 review revision。provider 返回不能绕过任何本地验证或直接写权威状态。

公开 demo 使用同一前后端镜像和 `demo` profile，数据源替换为合成/许可 fixture、mock 和临时 SQLite；它不是第二套产品。

## 7. 数据模型

| 实体 | 核心字段与约束 |
| --- | --- |
| `Course` | opaque ID、名称、时区、创建时间；首版单本地 actor |
| `Material` | course、文件名、媒体类型、原始 content hash、状态；`(course_id, content_hash)` 唯一且幂等 |
| `MaterialVersion` | material、parser ID/version、extraction contract version、抽取状态/目录；四元唯一键，旧版本不可改写 |
| `MaterialBlobRef` | material、content hash；跨课程 blob 引用，最后一个引用删除后才允许删除内容地址字节 |
| `SourceLocator` | PDF page 或 text lines 判别联合；必须绑定 material version 和原始 hash |
| `KnowledgeConcept` | course、名称、可空 evaluator ID、版本、active/explanation_only 状态 |
| `CoverageDecision` | concept、locator IDs、confirmed/rejected、版本和确认时间；追加历史 |
| `ProviderProfile` | 内置 adapter ID、受支持模型、预算、credential ref、config/policy fingerprint；无 secret |
| `ConsentRecord` | P 端口、精确 locator/hash、外发预览摘要、profile/policy/预算指纹、时间；不可变 |
| `Attempt` | concept、check kind、variant ID、结构化本地答案、状态；正文不进入日志或 provider feedback |
| `LearningEvidence` | attempt、evaluator/version、rubric、outcome、source IDs、幂等键、UTC 时间；不可变 |
| `MasteryEstimate` | concept、derived state、完整 evidence input hash；只能派生，不手工覆盖 |
| `ReviewPlanRevision` | mode、时区、预算、考试日期、input hash、父 revision、创建时间 |
| `ReviewTask` | revision、concept、due local date、时长、状态、source/evidence refs |
| `AuditEvent` | actor/action/result、opaque refs、指纹和脱敏错误；字段白名单 |

关系删除规则必须在 migration 和 repository tests 中验证。材料正文与学生答案不进入审计、普通日志、demo fixture 或 CI artifact。

## 8. 凭据威胁模型

| 威胁 | 对策与验收 |
| --- | --- |
| key 被提交或写入配置 | Credential Manager 单一存储；secret scanner 覆盖 staged diff、常见编码和私钥模式 |
| UI/日志回显 key | password input、不返回 secret、日志白名单；浏览器与 API 测试断言 key 不出现 |
| 恶意文件或类型伪装 | magic/type/大小/页数/UTF-8 校验、解析超时、事务回滚 |
| prompt injection 或模型越权 | 来源片段视为不可信数据；provider 只产候选；schema 校验；权威规则完全本地 |
| 未经同意外发材料 | 每次 P 请求绑定精确 locator/hash/port/profile；无匹配 consent 时网络调用为 0 |
| 过期来源污染学习状态 | 每次使用前校验材料存在和 hash；失效来源不能生成新 explanation/evidence/plan task |
| demo 泄露私人数据或产生费用 | 无上传/credential/provider 出网；仅许可 fixture + mock + 过期 session |

## 9. 分发、部署与 CI

- 本地分发：Windows x64 单文件 `ProjectB.exe`，首次启动创建当前用户数据目录并打开 loopback WebUI；README 说明 SmartScreen、架构、数据目录、凭据录入和清除。
- 本地演示：`linux/amd64` OCI 镜像，单条 `docker build` 与单条 `docker run` 启动 demo profile。公网托管由 D-025 明确 waived；不得静默付费或创建云资源。
- GitLab：`.gitlab-ci.yml` 必须含名称严格为 `unit-test` 的 job，并在 push 运行测试；最终课程提交对应 pipeline 必须 PASS。
- GitHub：镜像仓库保留 PR 历史和 Actions；每次 push 测试并构建相应分发产物。
- README 最终必须包含项目简介、安装、运行、分发命令、目录结构、安全边界、凭据配置、已知限制、部署架构、第三方依赖与许可证。

## 10. 技术选型

| 选择 | 理由 |
| --- | --- |
| Python 3.14 + FastAPI/Pydantic/SQLite | 本地应用、确定性领域规则、事务持久化和 PDF 生态成熟 |
| React + Vite + TypeScript | 适合响应式工作台、组件测试和静态资源打包 |
| pypdf/pypdfium2 | 数字 PDF 文本与页目录；v1 不承担 OCR |
| keyring WinVault | 复用 Windows Credential Manager，不自造加密格式 |
| OpenAI Python SDK behind a port | 唯一真实 adapter，与领域规则隔离；可由 mock 完整替换 |
| PyInstaller | Windows x64 单文件分发，并保留 bootloader 许可证例外说明 |
| Docker/OCI | 复用同一应用合同提供无凭据 mock demo |
| pytest/Vitest/Playwright/axe | 覆盖领域、API、UI、响应式和无障碍 |
| Open Design `frontend-design` + Neutral Modern | 已由学生选择，适合紧凑工具型 WebUI |

精确版本和许可证以已验证 evidence ledger 为计划输入；正式 manifest 由获准后的首个 foundation task 物化，不采用当前 PATH 环境作为证据。

## 11. 验收标准

### 11.1 G-03 原子冷启动合同

G-03 intake 的目标固定为 `F-01S1A`，acceptance ID 固定为 `F01S1A_SINGLE_RULE_SCANNER_V2`。Execution 只实现单文件 `-Path` 入口、严格 UTF-8、`Write-ScanRecord`、`Convert-SourceText`、`Find-DirectSecret` 和 `provider_api_key` 规则；`source` 固定为 `path`，输出 path 使用调用参数将 `\` 替换为 `/` 并去掉一个开头的 `./`。缺 scope、读取失败和解码失败分别使用 `usage_missing_scope`、`read_failed`、`decode_failed`，不得输出内容或秘密值。

合同文件最多 180 行、scanner 最多 140 行、最终英文摘要最多 300 词；超过任一上限必须报告 plan defect。红灯必须为 exit 1 且唯一输出 `CONTRACT_RED scanner_missing`；绿灯必须覆盖 `usage_and_output`、`provider_rule` 并以 `BOOTSTRAP_SCANNER_PATH_PASS` 结束。20 分钟、预算超限、输出截断、无工具写入或无终止结果均为 execution incomplete。`F-01S1B` 串行增加其余五类直接规则、去重排序和 `artifact_direct_safety`，不属于本轮冷启动。

| ID | 客观判定 |
| --- | --- |
| AC-01 | 可创建课程并增量导入合法 PDF/TXT/MD；超限、伪装和无文本 PDF 在写入前失败 |
| AC-02 | 原始字节 hash、PDF 页和文本行 locator 可重复生成且越界被拒绝；同 hash 新 parser 只新增版本 |
| AC-03 | 用户可创建多个知识点并确认/拒绝来源映射；未确认映射不能进入学习或计划 |
| AC-04 | 删除材料会移除该课程引用并阻止失效 locator 产生新权威记录；跨课程仍引用同 hash 时不得删除共享 blob |
| AC-05 | 三个内置并发 evaluator 对 golden/negative fixtures 给出确定性相同结果 |
| AC-06 | explanation-only 概念可解释但不能产生掌握证据 |
| AC-07 | 无 consent 时 P 网络调用为 0；consent 精确绑定 locator/hash/port/profile/预算 |
| AC-08 | OpenAI adapter 只发送已预览片段，使用 `store:false`、无 hosted file/tool，并校验 schema |
| AC-09 | provider 失败不改变 coverage、evidence、mastery 或 plan；本地流程仍可使用 |
| AC-10 | LearningEvidence 幂等追加，重复 attempt key 不产生第二条记录，学生答案不进入日志/provider |
| AC-11 | mastery 只由完整 evidence 历史确定性推导并满足 demonstrated/retained 时序规则 |
| AC-12 | continuous/finals 计划遵守预算、固定 mastery 压缩表、稳定顺序和考试截止，重复输入产生相同 hash/任务 |
| AC-13 | 新 evidence 或设置变化产生 revision diff；已完成任务不被重写，未开始任务可恢复 |
| AC-14 | key 可隐藏录入、更新、清除；状态不回显明文；SQLite/config/log/browser/Git 无 secret |
| AC-15 | loopback、Host、Origin、CSRF 和审计字段白名单均有自动化正反测试 |
| AC-16 | 四阶段 WebUI 在 360/768/1440 px 无溢出，键盘可用且 axe 无 serious/critical 违规 |
| AC-17 | demo 使用许可 fixture + mock，禁止上传、凭据、provider 出网和跨 session 持久化 |
| AC-18 | `python scripts/test_all.py` 在干净项目环境运行全部核心测试并以非零退出表示任一失败 |
| AC-19 | Windows 单文件在目标 Windows x64 干净环境启动并完成 smoke；README 说明安全配置和限制 |
| AC-20 | OCI 镜像可由单条 build/run 启动；GitLab `unit-test` 与 GitHub CI 均通过 |
| AC-21 | 提供可本地访问的 WebUI URL，README 记录本地架构和 CI/CD；公网 HTTPS URL 由 D-025 明确 waived |
| AC-22 | 每个实现 task 有红/绿/回归、两阶段评审、凭据扫描、commit hash 和 AGENT_LOG 记录 |
| AC-23 | 不含真实凭据或未记录许可证；第三方来源与许可证在 README/清单中可追溯 |
| AC-24 | 不同类型的新鲜编码智能体只凭最终 SPEC/PLAN 完成只读 intake，并在无歧义时由第二个全新 session 尝试原子任务 F-01S1A；字段语义、产物/摘要预算、问题、误解、diff、费用和独立红绿复验写入 SPEC_PROCESS；同类型 Codex 只能记为 G-03P 占位预审 |

## 12. 延期功能与恢复规则

以下能力不属于精简 v1 验收，但以 `ARCHIVED / NOT DISPATCHABLE` 计划保存：

- [`advanced-material-ingestion.md`](docs/archive/deferred-v2/advanced-material-ingestion.md)：OCR、图片、扫描件和大批量导入。
- [`remote-f-and-durable-jobs.md`](docs/archive/deferred-v2/remote-f-and-durable-jobs.md)：整文件模式 F、远端对象、durable job 和清理恢复。
- [`exam-material-intelligence.md`](docs/archive/deferred-v2/exam-material-intelligence.md)：往年卷、老师重点和自动知识点映射。
- [`extended-concept-rubrics.md`](docs/archive/deferred-v2/extended-concept-rubrics.md)：更多知识点的确定性 rubric。

恢复任何延期能力前必须重新执行 `brainstorming`、形成明确 SPEC diff、由学生确认、再调用 `writing-plans`。归档草稿和旧实现片段不能直接派发。自主 agent、多用户、共享和任意 provider plugin 不只是延期项；它们需要新的产品提案和学生决策。

## 13. 风险与开放事项

| 风险/决策 | 当前处理 |
| --- | --- |
| 已确认 SPEC 后发生范围漂移 | 任何产品条款变化必须形成明确 diff 并重新由学生确认；状态/证据元数据不得静默改变验收合同 |
| D-025 公网托管 | 学生已确认本项目本地交付，公网托管与公网 URL waived；不阻塞本地实现、分发或文档 |
| Claude 冷启动曾空结束、504 及长时间 thinking | 保留真实失败；不猜测传输根因。用英文 capsule、原子 F-01S1A、锁定字段、产物/摘要预算、超时和产物后置条件失败关闭，再做一次受控复测 |
| 真实课件许可未知 | 只允许本地私人使用；仓库、CI、分发和 demo 只能使用合成或明确许可 fixture |
| Provider 能力/政策/价格会变化 | 每次实现/运行前刷新 allowlisted snapshot；无法证明时失败关闭 |
| Windows/OCI 打包兼容性未证明 | 保留为 DIST task，必须用当次干净环境证据闭合 |
| 学生过程反思缺失 | 由学生本人提供观点和最终 `REFLECTION.md`；AI 不代写 |
| 远程仓库、PR、CI、部署未授权执行 | 到对应 gate 再请求授权；本地文档和测试不能冒充外部证据 |

## 14. 阶段门禁

1. 学生确认产品方向和 G-03 原子执行设计。**已分别于 2026-07-25 和 2026-08-01 完成。**
2. 学生确认本次完整 SPEC 候选。**已于 2026-08-03 完成。**
3. 用 `writing-plans` 修订单一 PLAN，生成两份文档内的英文 capsule，并在同一最终哈希上完成机械审计和双评审。
4. 学生确认修订后的完整 SPEC/PLAN，然后使用不同类型的两个全新 session、仅凭最终 SPEC/PLAN 完成 G-03 intake 与 F-01S1A execution，并记录修订和独立复验。
5. 学生阅读冷启动结果并明确批准 G-04 实现门禁。
6. 才可使用 worktree、subagent、TDD 和两阶段评审编写正式代码。

当前处于第 3 步；旧签字和旧 intake 不覆盖当前字节，也不得推断第 5 步的实现授权。
