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

## 候选职责模块

### M1 课程材料与保真工作区

**职责**：导入用户选择的课程材料，保留原始页与提取结果的对应关系，生成质量报告，执行课程级处理策略并向其他模块提供带来源的上下文。

**主要操作**：

- `inspect_material`：在处理前读取文件元数据、类型、页数和限制；
- `import_material`：保存材料身份、内容哈希、原页引用和解析版本；
- `set_processing_policy`：记录课程模式及用户同意；
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
- `schedule_review`：结合目标日期、最近表现与知识依赖生成复习任务；
- `serve_review_task`：先要求主动提取，再按结果显示解释；
- `reschedule_from_result`：复习结果反向更新状态与后续解释深度。

**边界**：不删除历史证据来改写结果；不把概率/分数表述为客观真值；没有足够证据时保持“未知”。

### X1 安全、凭据与审计（跨模块）

**职责**：凭据安全存储、数据外发预览、所有权检查、预算/超时、错误脱敏、同意与删除审计。

它是跨模块控制面，不应被包装成一个独立、可绕过的“安全页面”。M1-M3 的每个外发、存储和删除操作都要经过相同策略。

## 候选实体

| 实体 | 核心字段（候选） | 关键约束 |
| --- | --- | --- |
| `UserProfile` | `id`, `timezone`, `learning_preferences` | 不存供应商密钥明文；偏好不能代替实际学习证据 |
| `Course` | `id`, `owner_id`, `title`, `target_date`, `processing_policy_id` | 所有课程对象继承 owner；处理策略可查看/修改 |
| `Material` | `id`, `course_id`, `original_name`, `content_hash`, `mime_type`, `size`, `page_count`, `state` | 原文件身份不可被提取文本替代；禁止重复/越界导入 |
| `MaterialPage` | `material_id`, `page_number`, `render_ref`, `raw_text`, `normalized_text`, `quality_flags`, `parser_version` | `(material_id, page_number)` 唯一；原始与归一化文本并存 |
| `ProcessingPolicy` | `id`, `course_id`, `mode`, `provider_scope`, `version`, `chosen_at` | 课程级有效；扩大外发需新的同意记录 |
| `ConsentRecord` | `id`, `course_id`, `from_mode`, `to_mode`, `payload_scope`, `provider`, `approved_at`, `revoked_at` | 追加式记录；不得覆盖旧授权历史；不保存正文 |
| `KnowledgeConcept` | `id`, `course_id`, `title`, `description`, `prerequisite_ids`, `status` | 必须至少有一个来源或标为学生自建；依赖不能形成非法循环 |
| `SourceReference` | `id`, `concept_id`, `material_id`, `page_number`, `region`, `kind` | 页码必须存在；区分课件、学生笔记和模型补充 |
| `ExplanationSession` | `id`, `course_id`, `concept_id`, `goal`, `baseline_evidence_ids`, `source_ids`, `processing_mode`, `created_at` | 输出与来源/模式绑定；不直接更新掌握状态 |
| `LearningEvidence` | `id`, `concept_id`, `type`, `prompt_ref`, `response_ref`, `outcome`, `source_ids`, `occurred_at` | 追加式；保留评分依据；删除正文时仍保持脱敏审计一致性 |
| `MasteryEstimate` | `id`, `concept_id`, `level`, `confidence`, `evidence_ids`, `algorithm_version`, `derived_at`, `corrected_by_user` | 每次估计可解释/重算；无证据不得标为已掌握 |
| `ReviewTask` | `id`, `concept_id`, `due_at`, `reason`, `task_type`, `status`, `attempt_ids` | 到期原因可见；完成必须关联实际尝试 |
| `CredentialStatus` | `provider`, `storage_ref`, `configured`, `updated_at` | `storage_ref` 只指向安全存储；查看状态不回显值 |
| `AuditEvent` | `id`, `actor_id`, `event_type`, `data_category`, `provider`, `scope_ids`, `occurred_at`, `result` | 白名单元数据，不记录课件正文、作答或凭据 |

## 关键关系

```text
Course
  -> ProcessingPolicy -> ConsentRecord[]
  -> Material[] -> MaterialPage[]
  -> KnowledgeConcept[] -> SourceReference[]
                         -> ExplanationSession[]
                         -> LearningEvidence[]
                         -> MasteryEstimate[]
                         -> ReviewTask[]
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

## 仍需 brainstorming 确认

- 正式支持的处理模式目录，尤其是否提供整份 PDF 云端处理；
- 目标用户是否只限单个学生，还是支持多用户/教师；
- 第一版必需材料类型与是否导入个人笔记/作业；
- “看懂”的具体知识点、诊断方法和成功标准；
- 复习目标日期与计划粒度；
- 是否包含课程定义中的 agent；
- 部署、供应商、凭据与分发方案。
