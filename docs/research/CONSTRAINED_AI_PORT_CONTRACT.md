# 受约束 AI 模型端口合同

记录时间：2026-07-20T00:43:07+08:00

## 状态与范围

D-013 已确认第一版使用受约束 AI 功能，不包含课程定义的 agent。D-015 又确认平台采用统一 `ProviderAdapterRegistry`，由用户配置平台已支持的 provider profile；D-016 确认首版一个真实 adapter + 完整 mock；D-017 选择 OpenAI 作为唯一真实参考 adapter；D-018 确认只允许平台内置 adapter，不开放任意自定义 endpoint 或第三方 plugin。本文件把“模型可以做什么”与“应用权威状态由谁决定”分开，供后续 `SPEC.md`、技术选型和 PLAN 使用。具体 OpenAI 模型版本、SDK/HTTP 客户端、部署平台和提示词模板仍未选择。

## 总体边界

```text
domain state + approved source scope
  -> ModelPort request
  -> configured provider profile
  -> ProviderAdapterRegistry
  -> registered provider adapter
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
- 非秘密 `provider_profile_id`、`config_fingerprint`、能力与政策快照 ID；
- 结构化响应 schema、schema 版本和拒绝原因。

模型输出默认是 `candidate`，不能直接成为课件事实、知识覆盖、计划、优先级、掌握状态、授权或删除结果。

provider profile 只保存 adapter 允许的非秘密配置和指向本机安全存储的 `credential_ref`。模型端口请求、响应、普通配置文件、浏览器持久化、日志与快照均不得包含凭据值；只有 X1 凭据边界可在调用 adapter 时解析 `credential_ref`。

首版 OpenAI profile 只能包含平台 schema 明确允许的模型/预算等非秘密字段和 `credential_ref`，不得包含任意 `base_url`、自定义 endpoint、动态 adapter 路径或第三方 plugin。平台内置 adapter 的 endpoint 与能力映射由代码/版本化注册表决定，用户 config 不能把兼容 OpenAI 协议的其他服务升级为受支持 provider。

未知 adapter/profile、无效配置、缺失凭据、无法验证的能力/政策快照或当前端口能力不足时，必须在读取或发送远端 payload 前失败关闭；不得猜测配置、自动选择另一 provider 或静默扩大来源范围。模式 L 不依赖远端 profile，仍可继续使用。

在模式 F 中，端口只使用应用内部 `SourceLocator`/source-scope token；provider File/association/store ID 由适配器通过同一 profile/config/policy 指纹的 `RemoteMaterialObject` 解析，不暴露为任意工具参数。模型引用必须映射回本地 locator，不能以“整份文件已上传”代替来源定位。

## OpenAI reference adapter 的端口能力边界

- 首版所有 `/v1/responses` 调用都是前台调用并显式发送 `store:false`。禁用 background、Conversations、远程 MCP，以及 Hosted Shell/Code Interpreter 等执行型 hosted tools；模式 F 所需的 File Search 只能由 adapter 绑定已授权、课程独占的 Vector Store，不向模型开放任意工具选择或参数分发。
- [File inputs](https://developers.openai.com/api/docs/guides/file-inputs#how-it-works) 证明：具备视觉能力的模型通过 Responses 接收 PDF `input_file` 时，会同时获得抽取文本与逐页图像。模式 P 可利用该路径，但调用仍只发送已授权来源。
- [File Search](https://developers.openai.com/api/docs/guides/tools-file-search) 证明 Responses 可检索 vector store 中已上传并达到 `completed` 的文件，并支持按 vector-store-file attributes 做 [metadata filtering](https://developers.openai.com/api/docs/guides/tools-file-search#metadata-filtering)；其示例 citation 仍只有文件级信息，未证明原 PDF 页码/页面视觉。
- [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs) 可约束 Responses 输出 schema，并提供独立 refusal 路径；结构化输出仍可能有内容错误，因此 adapter 解析成功后仍必须通过来源、页码和领域规则验证。
- [Data controls](https://developers.openai.com/api/docs/guides/your-data#storage-requirements-and-retention-controls-per-endpoint) 的 2026-07-20 快照显示：`store:false` 只关闭 Responses application-state 存储，不能消除默认最长 30 天、可能含 prompt/response 的 abuse-monitoring 日志，也不能消除非 ZDR 组织支持模型最长 24 小时的 prompt cache；图像/文件存在特殊安全审查例外。`/v1/files`、`/v1/vector_stores` 仍非 ZDR 且应用状态直到删除。每个 `policy_snapshot_id` 必须同时覆盖 Responses、abuse monitoring、prompt cache、图像/文件审查例外、Files 和 Vector Stores；“默认不用于训练”不能被解释为请求后不留存。

因此 OpenAI 返回的 file citation 只是 provider 候选证据。只有本地映射成功、得到版本匹配的 `SourceLocator` 并通过 `source_scope` 存在性校验后，响应合同才可产生 `source_locator`。缺少该 locator 时，`propose_concept_coverage`/`analyze_exam_material` 必须返回空内容的 `source_insufficient`；`generate_explanation`/`generate_practice_candidate`/`generate_feedback` 最多返回明确标为 `model_supplement` 的一般知识，不能产生“基于材料”的事实、进入 `ConceptCoverage`/`StudyFocus`/计划或作为来源证据。不得要求模型猜 locator，也不得把文件名当 locator。OpenAI Python SDK 的许可证尚未现场核验，正式选择 SDK 前必须另行检查并记录。

每次 F request 还必须从有效 consent 生成 association `scope_token` allowlist，在 File Search tool 上使用 `in` metadata filter，并包含/验证每个 result/citation File ID。撤销 token 立即移出 allowlist；出现越界 File ID 时整次响应为 `provider_scope_violation`，所有 content 丢弃。若 attributes/filter/results 能力或 allowlist 上限无法证明，则该 store `source_disabled`，不得仅靠 prompt 隔离来源。locator 文本证明采用与 `SPEC.md` 相同的 NFKC/空白规范化和唯一 >=32 code-point 页内 span；歧义或视觉-only 必须失败。

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
  "provider_profile_id": "opaque-profile-id",
  "config_fingerprint": "non-secret-config-digest",
  "capability_snapshot_id": "opaque-capability-snapshot",
  "policy_snapshot_id": "opaque-policy-snapshot",
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

示例中的预算数值仅用于展示字段，不是已确认默认值。真实实现可以采用其他序列化格式，但必须保留同等字段语义。请求不能携带任意本地路径、`credential_ref` 或凭据值、未批准的原文范围或可执行工具参数；`source_scope` 为空时，端口只能返回“来源不足”，不能自行搜索。profile/config/policy 指纹与当前 consent 不一致时，调用必须在 adapter 前被拒绝。

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

允许的顶层状态至少包括 `candidate`、`source_insufficient`、`schema_rejected`、`provider_scope_violation`、`provider_config_invalid`、`credential_unavailable`、`capability_unsupported`、`policy_unknown`、`provider_failed`、`cancelled` 和 `budget_exceeded`。除 `candidate` 外，状态不能进入权威写入路径；`content` 在错误状态下必须为空或仅含脱敏恢复信息。

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
| `LearningPlan` / `PlanRevision` | 否，最多提供候选输入 | 是（ReviewPolicy v1） | 自动修订无需二次确认；覆盖决定、进入 finals、手动覆盖等输入动作本身需确认 |
| `ReviewTask.due_at` / priority | 否 | 是 | 手动覆盖时 |
| `MasteryEstimate` | 否 | 是（证据/rubric） | 纠正/撤销时 |
| `ConsentRecord`、凭据、删除结果 | 否 | 是 | 是 |

## 失败与恢复语义

```text
requested -> provider_pending
provider_pending -> candidate -> validated -> awaiting_confirmation
provider_pending -> provider_failed/cancelled/budget_exceeded
requested -> provider_config_invalid/credential_unavailable/capability_unsupported/policy_unknown
candidate -> schema_rejected/source_insufficient
```

- provider 超时、限流、格式错误或预算耗尽：保留当前权威状态，候选标为可重试失败。
- schema 失败：不尝试从自由文本猜字段；记录脱敏错误和端口版本。
- Structured Outputs refusal、解析失败或字段虽合法但引用无法映射：分别归一化为白名单状态，不从自由文本补字段、猜页码或绕过本地来源校验。
- 来源不存在或权限改变：拒绝候选并要求重新检索/覆盖确认。
- 同一幂等键重复请求：本地只合并为同一逻辑 job/候选写入，但真实 provider 按 at-least-once 语义处理；超时或响应丢失后先用请求引用对账，不能承诺返回同一 provider 响应、绝不产生重复对象或绝不重复计费。发现重复对象时先隔离，再选择 canonical 对象并排队清理；mock 可按键确定性返回同一结果。
- provider 返回提示注入、工具指令或越权请求：把它当普通输出数据拒绝，不执行其中动作。
- profile/config/policy 指纹变化：旧 consent 不再匹配；已有候选可保留为历史但不能用于新权威写入，新请求等待配置校验与用户确认。
- 凭据被强制清除：所有新 provider 调用失败关闭；尚未完成的删除/对账对象保持隔离和 `credential_unavailable`/`delete_incomplete`。只有同 profile 凭据重新录入且用户显式恢复时才执行一次有界对账，不能自动换 profile、回退 mock 或把未知远端状态标为 `deleted`。

## Provider mock 与确定性测试合同

核心测试必须能在没有真实 LLM、网络和凭据时运行。deterministic mock 只注册在 test/demo profile；local production registry 只注册平台内置 OpenAI adapter，不能在配置失败时回退到 mock。registry/mock 至少支持未知 adapter、坏配置、缺失凭据、能力不足、政策未知，以及按 `request_id`/测试种子返回成功候选、低置信候选、无来源、坏 schema、超时、限流、注入文本、重复响应和不同措辞但相同结构的反馈。

必测不变量：

1. 无有效 `ConsentRecord` 或来源范围为空时，远端调用为 0 或端口立即返回 `source_insufficient`。
2. provider 输出措辞变化不改变 evaluator 结果、掌握状态、计划版本或 `due_at`。
3. 低置信/冲突候选在用户确认前不进入课程知识、`StudyFocus` 或计划。
4. provider 失败、取消和预算耗尽不删除已有证据、不创建重复任务、不升级外发范围。
5. 相同请求、规则、来源和时钟下，候选校验与应用状态机结果可重放。
6. 任何模型输出都不能调用文件、凭据、网络或删除工具；工具分发层不存在 agent loop。
7. 日志、错误和审计只含端口、对象 ID、状态、耗时和计量，不含原文、回答或 key。
8. profile/config/policy 指纹变化后旧 consent 不匹配，provider mock 调用为 0；旧远端引用不能被新 profile 使用。
9. 未知 adapter、坏配置、缺失凭据或能力不足时失败关闭，不自动切换 provider；本地模式仍可运行。
10. OpenAI File Search 只返回 file citation 或无法证明页面视觉时，不产生伪造 locator；本地映射失败时 coverage/exam-analysis 返回空 `source_insufficient`，解释/练习/反馈最多返回 `model_supplement`，且不进入 `ConceptCoverage`/`StudyFocus`/计划或来源证据。
11. profile 出现 `base_url`、未知 endpoint、动态 adapter/plugin 字段时 schema 拒绝，provider mock/真实调用均为 0。
12. policy snapshot 同时覆盖 Responses `store:false` 的边界、最长 30 天 abuse monitoring、最长 24 小时 prompt cache、图像/文件审查例外，以及 Files/Vector Stores 的“非 ZDR、应用状态直到删除”；不能被“默认不训练”字段覆盖。
13. 真实 adapter 的超时/响应丢失按 at-least-once 对账，测试不声称 provider exactly-once/绝不重复计费；deterministic mock 才能按相同请求键返回可重放结果。
14. local production registry 不注册 mock；test/demo profile 不解析真实凭据或调用真实 provider。

## 尚未选择的技术项

- OpenAI reference adapter 的模型版本、SDK/HTTP 客户端、区域、成本上限与用户组织数据控制资格；SDK 许可证尚未现场核验；
- 平台内置 OpenAI adapter 的稳定 endpoint 清单和版本化非秘密配置 schema；任意自定义 endpoint/plugin 已由 D-018 排除；
- 本地模型、远端最小片段或混合路由的具体实现；
- token/图像/页数预算的最终数值；
- schema 序列化库、重试策略和凭据存储适配器；
- 是否把某些端口完全实现为规则/模板而不调用模型。
