# 受约束 AI 模型端口合同

记录时间：2026-07-20T00:43:07+08:00

## 状态与范围

D-013 已确认第一版使用受约束 AI 功能，不包含课程定义的 agent。本文件把“模型可以做什么”与“应用权威状态由谁决定”分开，供后续 `SPEC.md`、技术选型和 PLAN 使用。它不选择 provider、具体模型、SDK、部署平台或提示词模板。

## 总体边界

```text
domain state + approved source scope
  -> ModelPort request
  -> provider adapter
  -> schema/size/source validation
  -> candidate result
  -> deterministic policy + user confirmation
  -> authoritative domain update
```

模型端口是有界的请求/响应函数，不是自主循环。每次调用必须具备：

- 明确的 `port_name` 和版本；
- 当前课程/任务/知识点 ID，而非任意文件路径；
- 允许读取的来源 ID、页码或已脱敏证据 ID；
- 输入内容的大小、图像数量、token/时间预算和取消信号；
- 可重试的幂等键、provider 追踪 ID 和最小化审计元数据；
- 结构化响应 schema、schema 版本和拒绝原因。

模型输出默认是 `candidate`，不能直接成为课件事实、知识覆盖、计划、优先级、掌握状态、授权或删除结果。

在模式 F 中，端口仍只使用应用内部 `source_id`；provider 文件/索引 ID 由适配器通过 `RemoteMaterialObject` 解析，不暴露为任意工具参数。模型引用必须映射回本地材料与页码，不能以“整份文件已上传”代替来源定位。

## 端口目录

| 端口 | 用途 | 必需输入 | 输出 | 权威写入 |
| --- | --- | --- | --- | --- |
| `propose_concept_coverage` | 从新材料提出知识覆盖候选 | `batch_id`、允许来源 ID、现有概念摘要、处理质量标记 | 概念 ID/候选标题、关系、来源 ID、置信度、理由、冲突标记 | 无；需 `CoverageDecision` |
| `generate_explanation` | 生成适配解释 | 已确认概念、来源页、学习目标、脱敏证据摘要、输出级别 | 分段解释、来源引用、未知/模型补充标记、下一步检查候选 | 无；不更新掌握 |
| `generate_practice_candidate` | 生成主动提取或迁移练习候选 | 已确认概念、rubric/oracle 类型、来源范围、难度边界、种子 | 题面、结构化答案检查点、来源、难度、变式参数 | 无；需 deterministic evaluator |
| `analyze_exam_material` | 分析往年卷/老师重点 | 材料角色、题目/重点来源、已确认概念、考试目标 | 题型/覆盖/难度/频度候选、`StudyFocus` 候选、证据引用 | 无；需用户确认 |
| `generate_feedback` | 将确定性结果转成可理解反馈 | evaluator 结果、rubric、来源、学生可见上下文 | 反馈、错误类别解释、下一步候选 | 无；不得自行评分 |

端口之间不能互相隐式调用；例如 `generate_explanation` 不得自行触发导入、检索任意页面、改期或激活计划。需要多个端口时，由应用状态机明确编排并记录每次调用。

## 通用请求合同

```json
{
  "port_name": "generate_explanation",
  "port_version": "v1",
  "request_id": "opaque-id",
  "course_id": "opaque-id",
  "task_id": "opaque-id-or-null",
  "source_scope": ["source-id"],
  "evidence_scope": ["evidence-id"],
  "input_digest": "non-secret-digest",
  "limits": {
    "max_output_tokens": 1200,
    "max_source_pages": 4,
    "timeout_ms": 20000
  },
  "idempotency_key": "opaque-key"
}
```

示例中的预算数值仅用于展示字段，不是已确认默认值。真实实现可以采用其他序列化格式，但必须保留同等字段语义。请求不能携带任意本地路径、凭据、未批准的原文范围或可执行工具参数；`source_scope` 为空时，端口只能返回“来源不足”，不能自行搜索。

## 通用响应合同

```json
{
  "request_id": "opaque-id",
  "port_name": "generate_explanation",
  "port_version": "v1",
  "status": "candidate",
  "content": {},
  "citations": [{"source_id": "opaque-id", "page": 25}],
  "uncertainties": ["source-insufficient"],
  "usage": {"input_units": 0, "output_units": 0},
  "provider_ref": "redacted-or-null"
}
```

允许的顶层状态至少包括 `candidate`、`source_insufficient`、`schema_rejected`、`provider_failed`、`cancelled` 和 `budget_exceeded`。除 `candidate` 外，状态不能进入权威写入路径；`content` 在错误状态下必须为空或仅含脱敏恢复信息。

## 端口专属约束

### 知识覆盖候选

- `source_ids` 必须属于当前批次且已通过处理策略；页码必须存在。
- `concept_id` 只能引用已有概念；新概念使用候选标题，不能伪造已确认 ID。
- 置信度是候选排序信号，不是事实概率；`changed`、`unmapped` 或来源冲突必须显式标记。
- 应用只在用户创建 `CoverageDecision` 后把候选加入课程知识和计划。

### 解释与反馈

- 所有“基于课件”的陈述必须引用来源；没有引用的内容标记为模型补充或未知。
- 反馈输入来自确定性 rubric/oracle；模型不能改变通过/失败、掌握等级或证据类型。
- 学生回答正文不进入普通日志；模型上下文使用最小必要脱敏摘要。

### 练习候选

- 题面必须绑定已确认概念和来源；参数化轨迹题必须携带可重放种子。
- 结构化检查点交给本地 evaluator；无法确定性判定的题目只能标为候选，不能提高掌握估计。
- 练习生成不读取考试未知资料，不承诺“原题预测”。

### 期末资料分析

- 输入必须带 `MaterialRole`：`past_paper` 或 `teacher_focus`；角色由用户确认，不由模型猜测。
- 输出是 `StudyFocus` 候选，必须包含来源、题号/页码（如有）、映射概念、证据类型和置信度。
- `teacher_focus` 的明确陈述与模型从频度推断的重点分开保存；二者不能合并成无来源的权威标签。
- 分析不调用训练/微调接口，不自动上传，不生成泄露试题或“必考”承诺。

## 权威性矩阵

| 状态/动作 | 模型可提议 | 应用规则可计算 | 必须用户确认 |
| --- | --- | --- | --- |
| 来源片段与候选引用 | 是 | 是（存在性校验） | 低置信/冲突时 |
| `ConceptCoverage` | 是 | 是（去重/冲突分类） | 是 |
| `StudyFocus` | 是 | 是（频度/权重候选） | 是 |
| `LearningPlan` / `PlanRevision` | 否，最多提供候选输入 | 是 | 激活重大修订时 |
| `ReviewTask.due_at` / priority | 否 | 是 | 手动覆盖时 |
| `MasteryEstimate` | 否 | 是（证据/rubric） | 纠正/撤销时 |
| `ConsentRecord`、凭据、删除结果 | 否 | 是 | 是 |

## 失败与恢复语义

```text
requested -> provider_pending
provider_pending -> candidate -> validated -> awaiting_confirmation
provider_pending -> provider_failed/cancelled/budget_exceeded
candidate -> schema_rejected/source_insufficient
```

- provider 超时、限流、格式错误或预算耗尽：保留当前权威状态，候选标为可重试失败。
- schema 失败：不尝试从自由文本猜字段；记录脱敏错误和端口版本。
- 来源不存在或权限改变：拒绝候选并要求重新检索/覆盖确认。
- 同一幂等键重复请求：返回同一候选或明确的已取消状态，不重复计费或写入。
- provider 返回提示注入、工具指令或越权请求：把它当普通输出数据拒绝，不执行其中动作。

## Provider mock 与确定性测试合同

核心测试必须能在没有真实 LLM、网络和凭据时运行。mock 至少支持按 `request_id`/测试种子返回：成功候选、低置信候选、无来源、坏 schema、超时、限流、注入文本、重复响应和不同措辞但相同结构的反馈。

必测不变量：

1. 无有效 `ConsentRecord` 或来源范围为空时，远端调用为 0 或端口立即返回 `source_insufficient`。
2. provider 输出措辞变化不改变 evaluator 结果、掌握状态、计划版本或 `due_at`。
3. 低置信/冲突候选在用户确认前不进入课程知识、`StudyFocus` 或计划。
4. provider 失败、取消和预算耗尽不删除已有证据、不创建重复任务、不升级外发范围。
5. 相同请求、规则、来源和时钟下，候选校验与应用状态机结果可重放。
6. 任何模型输出都不能调用文件、凭据、网络或删除工具；工具分发层不存在 agent loop。
7. 日志、错误和审计只含端口、对象 ID、状态、耗时和计量，不含原文、回答或 key。

## 尚未选择的技术项

- provider、模型版本、区域、留存/训练政策和成本上限；
- 本地模型、远端最小片段或混合路由的具体实现；
- token/图像/页数预算的最终数值；
- schema 序列化库、重试策略和凭据存储适配器；
- 是否把某些端口完全实现为规则/模板而不调用模型。
