# 学习辅导候选模块与领域模型

记录时间：2026-07-19T22:46:45+08:00

## 状态

本文依据已确认的产品方向整理候选模块、接口与数据约束，供后续 brainstorming 和 `SPEC.md` 使用。它不是已批准架构，不决定数据库、框架、模型供应商、部署方式或是否包含 agent。

## 已确认的输入

- 目标场景是大学学业中的“看懂”和“持续复习”。
- 首个真实课程是操作系统基础，材料为 15 份、932 页的混合文本/代码/公式/图表 PDF。
- 解释需要适配学生当前理解，且跨会话维护连续学习状态。
- 课件处理路径由用户选择，必须显示保真度、外发、凭据/费用和解析限制。
- 本地解析不能冒充原始页面；任何扩大外发范围的模式切换不能静默发生。
- 第一版只服务单个学生并采用本地优先 WebUI；私有课程数据默认在本机，不实现账号、多租户或分享。
- 首个纵向学习闭环选择互斥与竞态条件，使用合成线程轨迹的确定性 oracle、来源约束解释和后续变式复习。
- 课程材料按学期进度增量导入；每批材料先形成候选知识覆盖，经用户确认后才修订未来学习计划，不能清空既有证据。
- 学期中默认 `continuous` 持续模式；录入考试日期并由用户显式进入后才使用 `finals` 期末周模式。往年卷和老师重点是显式材料角色，不表示模型训练或原题预测。

## 候选职责模块

### M1 课程材料与保真工作区

**职责**：导入用户选择的课程材料，保留原始页与提取结果的对应关系，生成质量报告，执行课程级处理策略并向其他模块提供带来源的上下文。

**主要操作**：

- `inspect_material`：在处理前读取文件元数据、类型、页数和限制；
- `import_material_batch`：保存增量批次、材料角色、材料身份、内容哈希、原页引用、独立文件状态和解析版本；
- `set_processing_policy`：记录课程模式及用户同意；
- `propose_concept_coverage`：生成 `added/reinforced/changed/unmapped/duplicate` 候选覆盖；
- `confirm_concept_coverage`：追加用户确认/纠正，只有确认结果能进入计划；
- `retrieve_context`：按知识点返回页码、原始/归一化文本、页面图和质量标记；
- `delete_material`：级联清理本地派生数据并协调远端删除状态。

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
- `schedule_review`：在 `continuous` 中持续安排；仅在日期有效且用户显式进入 `finals` 后，才结合剩余时间、已确认老师重点和往年卷模式调整未来任务；
- `serve_review_task`：先要求主动提取，再按结果显示解释；
- `reschedule_from_result`：复习结果反向更新状态与后续解释深度。

**边界**：不删除历史证据来改写结果；不把概率/分数表述为客观真值；没有足够证据时保持“未知”。模型/provider 不直接决定权威覆盖、优先级、计划或掌握状态；“拟合往年卷”只表示结构、知识点、题型和难度分析及同类练习。

### X1 安全、凭据与审计（跨模块）

**职责**：凭据安全存储、数据外发预览、所有权检查、预算/超时、错误脱敏、同意与删除审计。

它是跨模块控制面，不应被包装成一个独立、可绕过的“安全页面”。M1-M3 的每个外发、存储和删除操作都要经过相同策略。

## 候选实体

| 实体 | 核心字段（候选） | 关键约束 |
| --- | --- | --- |
| `UserProfile` | `id`, `timezone`, `learning_preferences` | 第一版为本地 actor；不存供应商密钥明文；偏好不能代替实际学习证据 |
| `Course` | `id`, `owner_id`, `title`, `processing_policy_id`, `active_plan_id` | 第一版绑定本地 actor；所有课程对象仍继承 owner scope；处理策略可查看/修改 |
| `MaterialBatch` | `id`, `course_id`, `role`, `state`, `created_at` | 批次内文件状态独立；失败不能覆盖成功；重复导入幂等 |
| `Material` | `id`, `course_id`, `original_name`, `content_hash`, `mime_type`, `size`, `page_count`, `state` | 原文件身份不可被提取文本替代；禁止重复/越界导入 |
| `MaterialPage` | `material_id`, `page_number`, `render_ref`, `raw_text`, `normalized_text`, `quality_flags`, `parser_version` | `(material_id, page_number)` 唯一；原始与归一化文本并存 |
| `ProcessingPolicy` | `id`, `course_id`, `mode`, `provider_scope`, `version`, `chosen_at` | 课程级有效；扩大外发需新的同意记录 |
| `ConsentRecord` | `id`, `course_id`, `from_mode`, `to_mode`, `payload_scope`, `provider`, `approved_at`, `revoked_at` | 追加式记录；不得覆盖旧授权历史；不保存正文 |
| `KnowledgeConcept` | `id`, `course_id`, `title`, `description`, `prerequisite_ids`, `status` | 必须至少有一个来源或标为学生自建；依赖不能形成非法循环 |
| `SourceReference` | `id`, `concept_id`, `material_id`, `page_number`, `region`, `kind` | 页码必须存在；区分课件、学生笔记和模型补充 |
| `ConceptCoverage` | `id`, `batch_id`, `concept_id`, `source_ids`, `relation`, `confidence`, `extractor_version` | 候选映射不等于权威知识；低置信与冲突需确认 |
| `CoverageDecision` | `id`, `coverage_id`, `decision`, `actor`, `reason`, `decided_at` | 追加式保留确认/纠正历史 |
| `StudyFocus` | `id`, `source_id`, `concept_id`, `kind`, `weight`, `confidence`, `status` | 老师明确重点、往年卷模式和系统推断分开；用户可纠正 |
| `ExplanationSession` | `id`, `course_id`, `concept_id`, `goal`, `baseline_evidence_ids`, `source_ids`, `processing_mode`, `created_at` | 输出与来源/模式绑定；不直接更新掌握状态 |
| `LearningEvidence` | `id`, `concept_id`, `type`, `prompt_ref`, `response_ref`, `outcome`, `source_ids`, `occurred_at` | 追加式；保留评分依据；删除正文时仍保持脱敏审计一致性 |
| `MasteryEstimate` | `id`, `concept_id`, `level`, `confidence`, `evidence_ids`, `algorithm_version`, `derived_at`, `corrected_by_user` | 每次估计可解释/重算；无证据不得标为已掌握 |
| `CourseReviewGoal` | `course_id`, `mode`, `target_local_date`, `timezone_id`, `version`, `finals_entered_at` | 默认 `continuous`；`finals` 同时需要有效日期与显式进入记录 |
| `LearningPlan` | `id`, `course_id`, `mode`, `goal_version`, `policy_version`, `created_at` | 输入可重放；活动版本唯一；旧版本保留 |
| `PlanRevision` | `from_version`, `to_version`, `reason_codes`, `input_ids`, `created_at` | 只替换允许变更的未来任务，不覆盖历史 |
| `ReviewTask` | `id`, `concept_id`, `due_at`, `reason`, `task_type`, `status`, `attempt_ids` | 到期原因可见；完成必须关联实际尝试 |
| `CredentialStatus` | `provider`, `storage_ref`, `configured`, `updated_at` | `storage_ref` 只指向安全存储；查看状态不回显值 |
| `AuditEvent` | `id`, `actor_id`, `event_type`, `data_category`, `provider`, `scope_ids`, `occurred_at`, `result` | 白名单元数据，不记录课件正文、作答或凭据 |

## 关键关系

```text
Course
  -> ProcessingPolicy -> ConsentRecord[]
  -> MaterialBatch[] -> Material[] -> MaterialPage[]
  -> ConceptCoverage[] -> CoverageDecision[]
  -> KnowledgeConcept[] -> SourceReference[] / StudyFocus[]
                         -> ExplanationSession[]
                         -> LearningEvidence[]
                         -> MasteryEstimate[]
                         -> ReviewTask[]
  -> CourseReviewGoal -> LearningPlan[] -> PlanRevision[]
```

`LearningEvidence` 是 M2 与 M3 的主要合同；`SourceReference` 是 M1 与 M2/M3 的主要合同；`ProcessingPolicy`/`ConsentRecord` 约束所有可能跨越本地边界的操作。

## 候选状态流

### 材料导入

```text
selected -> inspected -> awaiting_policy -> processing
         -> rejected
processing -> ready | ready_with_warnings | failed
ready/ready_with_warnings -> deleting -> deleted | delete_incomplete
```

D-009 已确认：`awaiting_policy` 必须由用户在首次导入引导中显式完成；选择按课程记住，任何扩大外发范围的切换仍需新的 `ConsentRecord`。

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
```

录入考试日期本身不切换模式。模式、日期、覆盖或规则变更都创建版本记录，只重排未开始的未来任务。

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
2. 所有“课件事实”必须能回到存在的 `MaterialPage`；无来源内容标为模型补充或学生笔记。
3. `MasteryEstimate` 必须引用一个或多个 `LearningEvidence`，并保留算法版本与推导时间。
4. 解释会话不能直接把知识点标为“已掌握”；至少需要学生产出的理解检查或复习表现。
5. 处理模式保存在课程级，但每次扩大外发范围都需要独立 `ConsentRecord`。
6. 删除课程材料时，所有派生页面、索引、来源引用和远端对象进入可观察的级联状态，不能只隐藏 UI。
7. 凭据实体只暴露配置状态，不暴露值；日志与审计事件不保存课程正文或学生作答。
8. 未经用户确认的 `ConceptCoverage` / `StudyFocus` 不能进入权威计划；provider 输出只能作为候选。
9. 新材料、材料删除、日期或模式变化都不删除 `Attempt`、`LearningEvidence`、用户修正和旧计划；失效来源必须可见。
10. `finals` 必须同时存在有效考试日期和显式进入记录；材料角色和考试日期均不构成外发授权。

## 是否构成 agent：尚未决定

上述三个模块可以先由确定性应用流程编排，不要求自主多轮决策或自主工具调用，因此目前不能把产品宣称为 agent。

如果后续要求系统自主决定诊断轮次、选择工具、反思失败并反复调整学习计划，则该部分将构成课程定义中的 agent；届时必须另行确认，并自行实现可用 mock/stub 测试的主循环、工具分发和治理护栏。不能仅依赖现成 agent 框架提示词。

## 可直接转为测试的候选要求

- 同一课程的页面、概念和证据不能被另一用户读取；
- `MaterialPage` 的原始文本不会因重新归一化而丢失；
- 无 `ConsentRecord` 时远端供应商 mock 调用为 0；
- `ExplanationSession` 没有来源时不能标记为“基于课件”；
- 没有 `LearningEvidence` 时不能产生“已掌握”状态；
- 完成一次复习必须追加尝试证据，并能解释下一次到期时间的原因；
- 删除材料后检索不能返回其页面，远端删除失败必须显示 `delete_incomplete`。
- 重复文件导入幂等，批次部分失败保留文件级成功/失败状态；
- 新覆盖确认前计划不变，确认后产生带原因的新计划版本；
- 仅设置考试日期不改变 `continuous`，显式进入/退出 `finals` 只重排未来任务；
- provider 失败、提示注入或候选映射变化不能改变权威覆盖、计划和掌握状态；
- 往年卷流程没有模型训练、微调、自动上传或预测原题路径。

## 仍需 brainstorming 确认

- 正式支持的处理模式目录，尤其是否提供整份 PDF 云端处理；
- 公开演示 WebUI 与授权样例策略；
- `past_paper` / `teacher_focus` 的文件格式，以及是否导入答案、个人笔记/作业；
- 互斥/竞态正式题目内容；
- 期末模式启用窗口、考试后状态、每日投入、计划粒度与具体调度算法；
- 是否包含课程定义中的 agent；
- 部署、供应商、凭据与分发方案。
