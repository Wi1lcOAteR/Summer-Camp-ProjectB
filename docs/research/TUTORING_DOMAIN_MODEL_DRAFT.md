# 学习辅导候选模块与领域模型

记录时间：2026-07-19T22:46:45+08:00

## 状态

本文依据已确认的产品方向整理候选模块、接口与数据约束；最新 `SPEC.md` 是上位权威。D-013 已确认第一版使用受约束 AI 功能而不包含课程定义的 agent；D-017/D-018 已确认首版 local production 只注册平台内置 OpenAI adapter，不接受任意 endpoint 或第三方 plugin，deterministic mock 只注册于 test/demo；D-019 确认材料白名单，D-020 确认确定性调度方向，精确 `ReviewPolicy v1` 已随整体 SPEC 确认；D-021/D-022 已确认 Windows x64 本地 WebUI、Credential Manager 与公开 demo 的合成/许可夹具 + mock 数据边界；隔离 session、限额和具体分发/托管也已纳入 v1 方向，仍待实现验证。

## 已确认的输入

- 目标场景是大学学业中的“看懂”和“持续复习”。
- 首个真实课程是操作系统基础，材料为 15 份、932 页的混合文本/代码/公式/图表 PDF。
- 解释需要适配学生当前理解，且跨会话维护连续学习状态。
- 第一版正式提供 L（本地）、P（经确认页面/片段远端）和 F（整份 PDF/课程远端）三种路径；由用户选择，并显示保真度、外发、凭据/费用和解析限制。
- 本地解析不能冒充原始页面；任何扩大外发范围的模式切换不能静默发生。
- 第一版只服务单个学生并采用本地优先 WebUI；私有课程数据默认在本机，不实现账号、多租户或分享。
- 首个纵向学习闭环选择互斥与竞态条件，使用合成线程轨迹的确定性 oracle、来源约束解释和后续变式复习。
- 课程材料按学期进度增量导入；每批材料先形成候选知识覆盖，经用户确认后才修订未来学习计划，不能清空既有证据。
- 学期中默认 `continuous` 持续模式；录入考试日期并由用户显式进入后才使用 `finals` 期末周模式。往年卷和老师重点是显式材料角色，不表示模型训练或原题预测。
- 第一版材料角色仅为 `lecture`、无答案 `past_paper`、`teacher_focus`；三者支持 PDF/图片/文本，老师重点还可手工录入。答案、个人笔记、作业提交、教材和其他角色延期。
- D-020 已确认确定性调度方向；`SPEC.md` 的 `ReviewPolicy v1` 数值/纯函数/fixtures 已随整体签字确认。新证据自动修订/撤销与考后暂停语义已确认。
- Provider 差异仍由领域外 adapter port 隔离，但第一版不是开放插件平台：local production 只有内置 OpenAI adapter，用户只配置平台 schema 允许的模型、受控参数、预算和 `credential_ref`；`base_url`、任意 endpoint、动态 adapter/plugin 和未知字段在联网前拒绝。deterministic mock 只用于 test/demo。
- 第一版目标为 Windows x64；Python/FastAPI 后端、React/Vite/TypeScript WebUI 与 SQLite 组成 localhost 应用，secret 通过成熟 keyring 写入 Windows Credential Manager。公开 demo 使用同一领域合同，但只加载合成/明确许可夹具和 deterministic mock。

## 候选职责模块

### M1 课程材料与保真工作区

**职责**：导入用户选择的课程材料，保留原始页与提取结果的对应关系，生成质量报告，执行课程级处理策略并向其他模块提供带来源的上下文。

**主要操作**：

- `inspect_material`：在处理前执行 v1 MIME/魔数、编码、大小、页数/像素/长度和批次限制；PDF 仅 `.pdf` + `application/pdf`/PDF 魔数，256 MiB/2,000 页；图片仅 `.png`/`image/png`、`.jpg`/`.jpeg`/`image/jpeg`、`.webp`/`image/webp`，20 MiB/50 megapixels；文本仅 UTF-8/UTF-8 BOM 的 `.txt`/`text/plain` 或 `.md`/`text/markdown`，2 MiB；手工重点 1-10,000 code points；单批 50 文件/1 GiB/5,000 PDF 页；
- `import_material_batch`：保存增量批次、材料角色、材料身份、内容哈希、原页引用、独立文件状态和解析版本；首版只接受已确认的三种角色和允许格式。声明的答案/个人笔记/作业等未知角色在正文处理前返回 `unsupported_role`；本地解析发现疑似答案/泄露时进入 `needs_user_review`，远端调用和权威写入为 0；
- `set_processing_policy`：记录课程模式及用户同意；
- `propose_concept_coverage`：生成 `added/reinforced/changed/unmapped/duplicate` 候选覆盖；
- `confirm_concept_coverage`：追加用户确认/纠正，只有确认结果能进入计划；
- `retrieve_context`：按知识点返回页码、原始/归一化文本、页面图和质量标记；
- `delete_material`：级联清理原文、页面、抽取和可重建索引，协调远端删除；历史只保留不能重建内容、路径或 provider ID 的 tombstone/失效 locator。

**边界**：不判断学生是否掌握；不把模型生成内容写成课件事实；不在没有同意记录时扩大数据外发。

### M2 适配解释与理解检查

**职责**：根据学生目标、已有学习证据和课件来源生成解释，要求学生复述、比较或应用，并记录可验证的理解证据。

**主要操作**：

- `diagnose_prior_knowledge`：用少量问题或学生自述定位起点；
- `explain_concept`：按目标深度和证据选择例子/步骤，引用具体课件页；
- `check_understanding`：用复述、概念比较或迁移题验证理解；
- `record_correction`：允许学生纠正来源、知识点或系统对困难的归因。

**边界**：生成解释不等于掌握；模型不能直接写入最终掌握状态；无来源的补充必须与课件内容分开标记。

### M3 掌握状态与持续复习

**职责**：把诊断、理解检查和提取练习转化为可解释的知识状态，生成复习任务并用后续表现更新计划。

**主要操作**：

- `record_learning_evidence`：追加一次可追溯的学习事件；
- `derive_mastery_estimate`：根据证据与版本化规则计算候选掌握状态；
- `revise_learning_plan`：结合已确认覆盖、最近表现、知识依赖和当前模式生成版本化计划；
- `schedule_review`：在 `continuous` 中持续安排；仅在日期有效且用户显式进入 `finals` 后，才用版本化简单规则结合剩余时间、可选每日预算、已确认老师重点和无答案往年卷模式调整未来任务；
- `serve_review_task`：先要求主动提取，再按结果显示解释；
- `reschedule_from_result`：复习结果反向更新状态与后续解释深度，自动生成只影响未开始任务的 `PlanRevision`，并提供可撤销修订；
- `handle_exam_date_passed`：仅在 `today_local > target_local_date` 时归档 `finals` 计划、暂停未来自动生成并询问新目标；考试当天仍可学习。

**边界**：不删除历史证据来改写结果；不把概率/分数表述为客观真值；没有足够证据时保持“未知”。模型/provider 不直接决定权威覆盖、优先级、计划或掌握状态；“拟合往年卷”只表示结构、知识点、题型和难度分析及同类练习。

### X1 安全、凭据与审计（跨模块）

**职责**：内置 OpenAI adapter 与共享 contract 的能力校验、非敏感 profile 配置、Windows Credential Manager 凭据存储、数据外发预览、所有权检查、预算/超时、错误脱敏、同意与删除审计。

它是跨模块控制面，不应被包装成一个独立、可绕过的“安全页面”。M1-M3 的每个外发、存储和删除操作都要经过相同策略。

本地正式版、开发/测试默认路径和公开 demo 都不从 `.env` 读取 API key；开发/测试使用 mock，真实集成只允许学生明确启动的独立人工 profile。凭据状态只返回已配置/未配置和更新时间；更新/清除不回显明文。存在远端清理任务时先警告并尝试清理；用户强制清除后所有新远端调用立即失败关闭，遗留对象保持 `delete_incomplete` 与脱敏恢复入口。公开 demo 的每个访客使用随机隔离 session，跨 session 读取为 0；30 分钟无活动/2 小时总寿命后清除，单 session 上限为 1 个课程、20 个材料夹具、2 个并发任务和 64 MiB 临时状态，每 IP 每分钟 60 请求。OpenAI 的动态能力、留存和 Responses/Files/Vector Stores 政策快照见 `REFERENCE_PROVIDER_OPTIONS.md` 与 `REMOTE_FILE_LIFECYCLE_CONTRACT.md`，本文不复制易过期细节。

## 候选实体

| 实体 | 核心字段（候选） | 关键约束 |
| --- | --- | --- |
| `UserProfile` | `id`, `timezone`, `learning_preferences` | 第一版为本地 actor；不存供应商密钥明文；偏好不能代替实际学习证据 |
| `Course` | `id`, `owner_id`, `title`, `processing_policy_id`, `active_plan_id` | 第一版绑定本地 actor；所有课程对象仍继承 owner scope；处理策略可查看/修改 |
| `MaterialBatch` | `id`, `course_id`, `role`, `state`, `created_at` | 首版 `role` 仅为 `lecture`/无答案 `past_paper`/`teacher_focus`；批次内文件状态独立；`needs_user_review` 无远端/权威写入；失败不能覆盖成功；重复导入幂等 |
| `Material` | `id`, `course_id`, `original_name`, `content_hash`, `mime_type`, `size`, `page_count`, `state` | 原文件身份不可被提取文本替代；禁止重复/越界导入 |
| `MaterialPage` | `material_id`, `page_number`, `render_ref`, `raw_text`, `normalized_text`, `quality_flags`, `parser_version` | `(material_id, page_number)` 唯一；原始与归一化文本并存 |
| `SourceLocator` | 见下方四分支判别联合 | 材料事实必须指向仍存在、哈希/版本匹配的 locator；删除后只能失效并留下脱敏 tombstone |
| `ProviderProfile` | `id`, `adapter_id`, `model_id`, `controlled_parameters`, `budget_policy`, `credential_ref`, `config_version` | local production 的 `adapter_id` 只允许内置 OpenAI；config 不含 secret、`base_url`、任意 endpoint 或 plugin；任一变更创建新版本 |
| `ProviderPolicySnapshot` | `id`, `profile_id`, `config_version`, `capabilities`, `retention`, `training_use`, `deletion_semantics`, `verified_at`, `source_refs` | 未知字段保持未知；能力不足时失败关闭；政策变化不能改写旧快照 |
| `ProcessingPolicy` | `id`, `course_id`, `mode`, `provider_profile_id`, `config_version`, `policy_snapshot_id`, `version`, `chosen_at` | 课程级有效；扩大外发或切换 profile/config/policy snapshot 需新的同意记录 |
| `ConsentRecord` | `id`, `course_id`, `from_mode`, `to_mode`, `payload_scope`, `provider_profile_id`, `config_version`, `policy_snapshot_id`, `approved_at`, `revoked_at` | 追加式记录；与实际 profile/config/policy snapshot 精确绑定；不得覆盖旧授权历史；不保存正文或 secret |
| `RemoteMaterialObject` / `RemoteJob` / `CourseVectorStore` | `course_id`, `material_id`, `scope_token`, profile/config/policy 指纹, `provider_refs`, `state`, `job_type` | 每课程/profile/config 独占 store；association token 过滤 + File ID 后验 allowlist；File/association/store 分层删除；能力不足 `source_disabled` |
| `KnowledgeConcept` | `id`, `course_id`, `title`, `description`, `prerequisite_ids`, `status` | 必须至少有一个来源或标为学生自建；依赖不能形成非法循环 |
| `SourceReference` | `id`, `concept_id`, `locator`, `source_kind`, `state` | `locator` 使用统一 `SourceLocator`；区分课件、期末材料、学生当次作答和无权威引用模型补充；首版不接收个人笔记材料 |
| `ConceptCoverage` | `id`, `batch_id`, `concept_id`, `source_ids`, `relation`, `confidence`, `extractor_version` | 候选映射不等于权威知识；低置信与冲突需确认 |
| `CoverageDecision` | `id`, `coverage_id`, `decision`, `actor`, `reason`, `decided_at` | 追加式保留确认/纠正历史 |
| `StudyFocus` | `id`, `source_id`, `concept_id`, `kind`, `weight`, `confidence`, `status` | 老师明确重点、往年卷模式和系统推断分开；用户可纠正 |
| `ExplanationSession` | `id`, `course_id`, `concept_id`, `goal`, `baseline_evidence_ids`, `source_ids`, `processing_mode`, `created_at` | 输出与来源/模式绑定；不直接更新掌握状态 |
| `LearningEvidence` | `id`, `concept_id`, `type`, `prompt_ref`, `response_ref`, `outcome`, `source_ids`, `occurred_at` | 追加式；保留评分依据；删除正文时仍保持脱敏审计一致性 |
| `ConceptReviewState` | `concept_id`, `interval_index`, `last_outcome`, `last_evidence_at`, `state_version` | 每个知识点保留上一轮调度状态；由完整相关 `LearningEvidence` 历史重算并校验，不能由新计划静默覆盖 |
| `MasteryEstimate` | `id`, `concept_id`, `level`, `confidence`, `evidence_ids`, `algorithm_version`, `derived_at`, `corrected_by_user` | 每次估计可解释/重算；无证据不得标为已掌握 |
| `CourseReviewGoal` | `course_id`, `mode`, `target_local_date`, `timezone_id`, `daily_budget_minutes`, `post_exam_state`, `version`, `finals_entered_at` | 默认 `continuous`；`finals` 同时需要有效日期与显式进入记录；预算可空；仅 `today_local > target_local_date` 后暂停 |
| `ReviewPolicy` | `policy_id`, `version`, `budget_rules`, `task_duration_rules`, `interval_rules`, `evidence_rules`, `stable_order`, `tzdata_version`, `effective_from` | v1 精确合同见下方；不能藏在 prompt，历史计划引用原版本 |
| `LearningPlan` | `id`, `course_id`, `mode`, `goal_version`, `policy_version`, `created_at` | 输入可重放；活动版本唯一；旧版本保留 |
| `PlanRevision` | `from_version`, `to_version`, `reason_codes`, `input_ids`, `reverts_revision_id`, `created_at` | 只替换允许变更的未来任务；撤销通过新修订完成，不覆盖历史 |
| `ReviewTask` | `id`, `concept_id`, `due_at`, `estimated_minutes`, `interval_index`, `reason_codes`, `status`, `attempt_ids`, `plan_revision_id` | 时长取 v1 白名单，索引为 0-4；到期原因可见；完成必须关联实际尝试 |
| `CredentialStatus` | `provider_profile_id`, `storage_ref`, `configured`, `updated_at` | `storage_ref` 只指向安全存储；profile config 不含 secret；查看状态不回显值 |
| `AuditEvent` | `id`, `actor_id`, `event_type`, `data_category`, `provider_profile_id`, `config_version`, `scope_ids`, `occurred_at`, `result` | 白名单元数据，不记录课件正文、作答或凭据 |

### `SourceLocator` 判别联合

| `kind` | 必需字段 | 语义 |
| --- | --- | --- |
| `pdf_page` | `material_id`, `content_hash`, `page`, `region?` | PDF 的 1-based 页及可选页内区域 |
| `image` | `material_id`, `content_hash`, `image_id`, `region?` | 独立图片或材料内图像及可选区域 |
| `text_lines` | `material_id`, `content_hash`, `line_start`, `line_end` | UTF-8 文本的闭区间行范围 |
| `manual_entry` | `entry_id`, `version` | 用户手工录入的 `teacher_focus`，不伪造材料页码 |

四个分支互斥，未知 `kind` 或多分支字段混用时 schema 失败。任何“基于材料”的事实都必须打开有效 locator；OpenAI File Search citation 不能直接替代本地映射。`propose_concept_coverage` / `analyze_exam_material` 无法校验 locator 时返回空候选与 `source_insufficient`；`generate_explanation` / `generate_practice_candidate` / `generate_feedback` 此时只能返回标为 `model_supplement` 的非权威补充，不能进入课程事实、计划或掌握证据。

### `ReviewPolicy v1` 精确默认

- `daily_budget_minutes` 为 10-480 的整数、步长 5；空值时 `continuous` 30 分钟/日、`finals` 90 分钟/日。
- `estimated_minutes` 只取 5/10/15/20/30，默认 10；按稳定顺序装入预算，不自动超额。
- 间隔阶梯为 `[1, 3, 7, 14, 30]` 个本地日，`interval_index` 为 0-4。新知识、错误、拒答或来源不足置 0；部分正确降一级；rubric 主动提取通过升一级；跳过不产生证据。`retained` 还需相隔至少一个本地日的变式主动提取通过。
- 先过滤未满足前置依赖的任务并优先可学习前置；其余按逾期天数降序、`finals` 已确认老师重点、往年卷重复覆盖降序（封顶 5）、证据弱度降序、到期时间升序、`concept_id` 升序稳定比较，不使用隐藏权重或模型排序。

## 关键关系

```text
Course
  -> ProcessingPolicy -> ProviderProfile -> ProviderPolicySnapshot[]
                      -> ConsentRecord[]
                      -> RemoteMaterialObject[] -> RemoteJob[]
  -> MaterialBatch[] -> Material[] -> MaterialPage[]
  -> ConceptCoverage[] -> CoverageDecision[]
  -> KnowledgeConcept[] -> SourceReference[] / StudyFocus[]
                         -> ExplanationSession[]
                         -> LearningEvidence[] / ConceptReviewState[]
                         -> MasteryEstimate[]
                         -> ReviewTask[]
  -> CourseReviewGoal -> LearningPlan[] -> PlanRevision[]
```

`LearningEvidence` 是 M2 与 M3 的主要合同；`SourceReference` 是 M1 与 M2/M3 的主要合同；adapter registry、`ProviderProfile`、`ProviderPolicySnapshot`、`ProcessingPolicy` 和 `ConsentRecord` 共同约束所有可能跨越本地边界的操作。

## 候选状态流

### 材料导入

```text
selected -> inspected -> awaiting_policy -> processing
         -> rejected
processing -> ready | ready_with_warnings | failed
ready/ready_with_warnings -> deleting -> deleted | delete_incomplete
```

D-009 已确认：`awaiting_policy` 必须由用户在首次导入引导中显式完成；选择按课程记住，任何扩大外发范围的切换仍需新的 `ConsentRecord`。

D-014 已确认 L/P/F 都进入第一版；F 的文件级 consent、远端对象、任务、切换和删除状态见 `docs/research/REMOTE_FILE_LIFECYCLE_CONTRACT.md`。

D-017/D-018 已确认首版不是开放 provider 平台：local production registry 只注册内置 OpenAI adapter，用户只选择平台支持的模型与受控 profile 参数；mock 只注册于 test/demo。模型、受控参数或政策指纹变化都创建新的 config/policy 版本，并在远端处理前获取新的 `ConsentRecord`。旧 `provider_refs` 只保留给创建它们的 OpenAI profile 做对账或删除，不得复用到新配置；`base_url`、任意 endpoint、动态 adapter/plugin 和未知字段在联网前拒绝。

材料在 `ready` / `ready_with_warnings` 后只产生候选覆盖；`CoverageDecision` 确认后才触发新计划版本。后续增量批次沿用同一流程，不假设整门课资料已经到齐。

### 模式与计划修订

```text
continuous
  -> import batch -> coverage confirmation -> plan revision -> guided learning
  -> exam date set -> finals available
  -> explicit enter -> finals

finals
  -> confirmed past-paper/teacher-focus mapping -> plan revision
  -> explicit exit/date cleared -> continuous
  -> today_local > target_local_date -> post_exam_paused -> archive finals plan/ask new goal
```

录入考试日期本身不切换模式。模式、日期、覆盖、预算或规则变更都创建版本记录，只重排未开始的未来任务。自动重排不要求逐次确认，但用户可以撤销；撤销会追加新修订并保留全部中间版本。考试当天仍可学习；仅 `today_local > target_local_date` 后不再生成未来任务，先暂停并询问新目标。

### 学习闭环

```text
choose goal
  -> gather prior evidence
  -> explain with sources
  -> learner self-explains/applies
  -> append evidence
  -> derive mastery estimate
  -> create/reschedule review task
  -> later retrieval attempt
  -> append new evidence and repeat
```

## 候选不变量

1. 原始材料、原页渲染、原始抽取和归一化抽取均有独立身份与版本，任何派生值不能覆盖来源。
2. 所有“材料事实”必须能回到存在且版本匹配的 `SourceLocator`；无有效 locator 的内容只能标为无权威材料引用补充，不能进入权威课程事实或计划。
3. `MasteryEstimate` 必须引用一个或多个 `LearningEvidence`，并保留算法版本与推导时间。
4. 解释会话不能直接把知识点标为“已掌握”；至少需要学生产出的理解检查或复习表现。
5. 处理模式保存在课程级，但每次扩大外发范围都需要独立 `ConsentRecord`。
6. 删除课程材料时，原文、派生页面、可重建索引和远端对象进入可观察的级联状态；历史只留不能重建正文、路径或 provider ID 的 tombstone 与失效 locator，不能只隐藏 UI。
7. 凭据实体只暴露配置状态，不暴露值；secret 只进入 Windows Credential Manager，不进入 config、SQLite、浏览器、日志、快照或 `.env`。
8. 未经用户确认的 `ConceptCoverage` / `StudyFocus` 不能进入权威计划；provider 输出只能作为候选。
9. 新材料、材料删除、日期或模式变化都不删除 `Attempt`、`LearningEvidence`、用户修正和旧计划；失效来源必须可见。
10. `finals` 必须同时存在有效考试日期和显式进入记录；材料角色和考试日期均不构成外发授权。
11. Provider config 不保存 key/token 等 secret，只保存平台支持的 OpenAI 模型、受控参数、预算和安全凭据引用；`base_url`、任意 endpoint、动态 adapter/plugin、未知字段或能力不足时不能进入远端调用。
12. `ConsentRecord`、`RemoteMaterialObject` 和 `RemoteJob` 必须引用同一不可变 profile/config/policy snapshot；配置切换不得迁移或复用旧 consent、幂等键或 `provider_refs`。
13. 第一版只接受允许格式的 `lecture`、无答案 `past_paper` 和 `teacher_focus`；答案、个人笔记、作业提交和其他角色保持 `unsupported_role`，不能静默降级。
14. 调度严格使用上面的 `ReviewPolicy v1`；自动修订可撤销，仅 `today_local > target_local_date` 后进入 `post_exam_paused`。
15. deterministic mock 只在 test/demo profile 注册；local production 不得暴露 mock 作为可伪装的真实 provider。公开 demo 只使用内置合成/许可夹具、隔离限时 session，不接受上传、真实凭据、真实 provider 出站或私人材料持久化。

## Agent 边界：已确认第一版不包含

上述三个模块由确定性应用流程编排。模型通过具名端口生成候选知识映射、解释、练习、反馈和期末资料分析，不自主选择工具、循环修正或直接写入权威状态，因此第一版不能宣称为 agent。

如果未来要求系统自主决定诊断轮次、选择工具、反思失败并反复调整学习计划，则会改变 D-013 已确认范围；届时必须重新取得学生确认，并自行实现可用 mock/stub 测试的主循环、工具分发和治理护栏。不能仅依赖现成 agent 框架提示词。

第一版五个具名模型端口、统一请求/响应 envelope、权威性矩阵和 provider mock 合同见 `docs/research/CONSTRAINED_AI_PORT_CONTRACT.md`。

## 可直接转为测试的候选要求

- 同一课程的页面、概念和证据不能被另一用户读取；
- `MaterialPage` 的原始文本不会因重新归一化而丢失；
- 无 `ConsentRecord` 时捕获式 adapter/contract spy 的远端调用为 0；
- `ExplanationSession` 没有来源时不能标记为“基于课件”；
- 没有 `LearningEvidence` 时不能产生“已掌握”状态；
- 完成一次复习必须追加尝试证据，并能解释下一次到期时间的原因；
- 删除材料后检索不能返回正文/单元，历史只剩非重建 tombstone/失效 locator；远端删除失败必须显示 `delete_incomplete`。
- 重复文件导入幂等，批次部分失败保留文件级成功/失败状态；
- 新覆盖确认前计划不变，确认后产生带原因的新计划版本；
- 仅设置考试日期不改变 `continuous`，显式进入/退出 `finals` 只重排未来任务；
- 未填写/填写每日预算时计划均可由固定时钟和策略版本重放；预算修改只影响未开始任务；
- 自动重排撤销会产生新的 `PlanRevision`，不删除旧计划或学习证据；考试当天仍可学习，仅目标本地日期已过去后计划暂停并询问新目标；
- 含答案往年卷、个人笔记或作业提交在首版被拒绝或保持 `unsupported_role`，不能进入权威覆盖；
- provider 失败、提示注入或候选映射变化不能改变权威覆盖、计划和掌握状态；
- locator 缺失、失效或哈希/版本不匹配时，coverage/exam 端口返回空结果 + `source_insufficient`，解释/练习/反馈至多返回 `model_supplement`；
- 非内置 adapter、任意 endpoint/plugin 字段、缺少 P/F 所需能力或政策字段未知时，相应远端调用为 0，L 模式仍可用；
- provider profile/config/policy snapshot 与 consent 不一致时拒绝请求；切换配置后旧 `provider_refs` 不能出现在新 profile 的请求中；
- provider config schema 拒绝 key/token、`base_url`、任意 endpoint/plugin 等字段；凭据只存 Windows Credential Manager，状态只暴露是否配置；强制清除后新远端调用失败关闭；
- 往年卷流程没有模型训练、微调、自动上传或预测原题路径。

## 已固定边界与仍待工程验证

- L/P/F、OpenAI、mock-only test/demo、许可夹具演示和 Credential Manager 已确认；M1 数值限制、隔离限额与 `ReviewPolicy v1` 也已随整体 SPEC 确认，仍待实现验证。
- 操作系统真实课件的远端处理/衍生练习权利、原始/派生数据保存期限仍待核验；不影响本地私有测试，但阻塞公开分发真实材料。
- 互斥/竞态正式题目内容；
- 模拟练习组卷细则、通知/日历同步和不可用日期等延期功能；
- OpenAI 支持模型目录、动态能力/区域/费用/留存政策必须在实际调用前刷新并保存政策快照；OpenAI Python SDK 许可证和兼容性仍须在加入依赖前核验。
- 精确依赖版本和 Windows 单文件冻结工具基线已由 G-02A PASS 与 G-02C blocker 证据固化，但完整应用打包、干净机、最终公开 URL 与远程 CI 仍待验证。Hugging Face 当前付费冲突及替代托管候选见 [`PUBLIC_HOSTING_ALTERNATIVES.md`](PUBLIC_HOSTING_ALTERNATIVES.md)；D-025 前任何变化不得绕过 SPEC、创建账号资源或产生付费责任。
