# ProjectB 规约（v1 已确认）

> 状态：**已由学生整体确认（2026-07-20）**。学生明确回复“已确认spec.md”；本文现为阶段 B 计划的权威规约。该确认不触发冷启动或实现，后续仍须遵守 Superpowers、Open Design、冷启动复核和实现批准门禁。
>
> 标记：`已确认` 表示学生已明确选择；`候选` 表示为下一轮评审准备；`未决` 表示课程规定必须由学生决定。
>
> 签字影响：本文签字前标为“待整体签字”的 `ReviewPolicy v1`、单文件 `ProjectB.exe`、OCI demo、隔离限额与 Hugging Face Spaces 首选方向已随整体确认成为 v1 工程合同；它们仍须通过许可证、官方条款、构建、运行与安全验证，证据不满足时只能走显式 SPEC 变更。

## 1. 问题陈述

### 1.1 已确认的问题

大学课程学习中，通用模型的解释常常不知道学生已经会什么、具体卡在哪里，结果可能过难、过浅或跳步；不同会话又彼此孤立，无法把一次“看懂”延续成可追踪的复习计划。

首个真实验证课程是“操作系统基础”。现有材料为 15 份 PDF、932 页、约 195.4 MB，包含中文/英文术语、代码、公式和图表。纯文本抽取不能等价替代原始幻灯片，因此材料处理必须同时考虑保真度、隐私、费用和用户授权。

### 1.2 候选的 30 秒说明

ProjectB 是面向大学课程的连续学习工作台：它让学生分批导入自己的课件并确认当前可学习知识，依据课件页码和既有学习证据提供适配解释，再把理解检查转化为可解释、可随新材料修订的学习与复习计划；录入考试日期后，学生还可显式进入期末周模式。

### 1.3 目标用户边界

- `已确认`：首个验证用户是正在学习“操作系统基础”的大学生本人。
- `已确认`：第一版只服务学生本人，采用单用户、本地优先运行；不实现注册、登录、多租户或教师视角。
- `已确认`：产品目标是帮助“看懂”和“持续复习”，不是代写作业或替学生完成课程考核。
- `延期`：多用户服务、课件分享、资料协作和跨设备同步可以作为未来方向，但不进入第一版范围。

D-010 已选择单用户、本地优先路线。三种候选路线及选择依据见 `docs/research/USER_DEPLOYMENT_BOUNDARY_OPTIONS.md`。

## 2. 用户故事（已整体确认）

1. **US-01 课程导入**：作为学生，我希望在导入课程时先看到文件规模与可读性检查，再明确选择处理方式，以便知道系统将如何使用我的材料。
2. **US-02 原始来源核对**：作为学生，我希望任何基于材料的解释都能回到具体 PDF 页、图片、文本行或手工重点版本，以便发现解析失真或模型误读。
3. **US-03 适配解释**：作为学生，我希望系统先利用我的目标和已有学习证据判断起点，再调整解释深度，以便避免过难、过浅或跳步。
4. **US-04 理解检查**：作为学生，我希望在解释后通过复述、比较或应用题检验理解，以便“看过解释”不会被误记为“已经掌握”。
5. **US-05 连续复习**：作为学生，我希望系统依据可见的学习证据和可配置每日投入生成确定性复习任务，并说明安排原因，以便跨会话持续复习。
6. **US-06 授权控制**：作为学生，我希望按课程查看和修改材料处理方式，并在扩大外发范围前再次确认，以便控制隐私、版权和费用风险。
7. **US-07 数据清理**：作为学生，我希望删除课程材料时能够看到本地派生数据与远端对象的清理结果，以便确认删除不只是隐藏界面入口。
8. **US-08 增量更新**：作为学生，我希望每次收到新课件后只导入新增批次、确认新增或变化的知识覆盖，并查看/撤销未来计划修订，以便课程资料不齐时也能持续学习且不丢失历史。
9. **US-09 期末周模式**：作为学生，我希望录入考试日期后显式进入期末周模式，将往年卷和老师重点映射到已确认知识，并结合薄弱证据安排突击；考试日结束后系统暂停并询问新目标，以便有限时间优先处理高价值缺口又不无限生成任务。
10. **US-10 凭据管理**：作为学生，我希望在本地界面隐藏录入、查看配置状态、更新和清除 OpenAI 凭据，同时普通配置与浏览器永远看不到明文，以便使用受约束 AI 功能而不暴露 key。

这些故事分别围绕单一用户价值，可独立验收；首个纵向里程碑按 M1 来源定位 → M2 互斥/竞态解释与检查 → M3 确定性复习交付，X1/X2 从第一项远端能力开始贯穿。后续 task 顺序由 `PLAN.md` 依据依赖拆分，但不能删除或改写上述用户价值。

## 3. 功能规约

### M1 课程材料与保真工作区

| 项目 | 规约 |
| --- | --- |
| 输入 | 用户选择的课程、一个或多个 `MaterialBatch`、材料角色与课程级处理策略。第一版白名单为：`lecture`（PDF/图片/文本）、无答案 `past_paper`（PDF/图片/文本）、`teacher_focus`（PDF/图片/文本/手工录入）。首个真实样本为“操作系统基础”15 份 PDF。 |
| 行为 | 先检查文件名、类型、大小、页数、加密状态、哈希、重复和限制；在用户明确选择前不解析正文、不上传内容。第一版提供 L（本地）、P（经确认页面/片段远端）和 F（整份 PDF/课程远端）三种能力，由用户显式选择。处理后保留原始页面、抽取结果、解析版本和质量标记的对应关系，生成 `added/reinforced/changed/unmapped/duplicate` 候选知识覆盖，并等待用户确认。 |
| 输出 | 批次/文件状态、质量报告、可追溯页面上下文、候选 `ConceptCoverage`、追加式 `CoverageDecision`、课程级 `ProcessingPolicy`、`ConsentRecord`、`RemoteMaterialObject` 与可观察远端任务状态。 |
| 边界 | 当前真实可读性证据只覆盖 PDF；图片、文本和手工重点仍须用合成/许可夹具验证。新批次不代表完整教学范围；候选覆盖未经用户确认不得成为课程事实或进入计划。答案 key、个人笔记、作业题目/提交、教材、未知角色与疑似泄露试题不进入第一版。首版真实路径只注册平台内置 OpenAI adapter，另有 test/demo mock；不接受任意 `base_url`、自定义 endpoint 或第三方 plugin。模式 F 若不能完成本地 `SourceLocator` 映射、对象追踪、政策快照和删除/过期对账，必须失败关闭其来源型端口。 |
| 错误处理 | 加密、损坏、越界、解析失败、低文本页和远端删除失败必须指出受影响文件/页及恢复方式；不得静默丢页、替换原文或升级外发范围。 |

#### M1 输入安全合同（工程默认 v1）

- PDF：扩展名 `.pdf` 且 MIME/魔数为 `application/pdf`；单文件不超过 256 MiB、2,000 页。加密、空文件、损坏、MIME/扩展名冲突或页数无法确定时拒绝正文处理。
- 图片：`.png`/`image/png`、`.jpg`/`.jpeg`/`image/jpeg`、`.webp`/`image/webp`；单文件不超过 20 MiB、解码后不超过 50 megapixels；动画只取首帧并明确提示，解码失败拒绝。
- 文本：`.txt`/`text/plain` 或 `.md`/`text/markdown`，UTF-8/UTF-8 BOM，单文件不超过 2 MiB；其他编码先要求用户在本地转换，不猜测后继续。
- 手工 `teacher_focus`：每条 1–10,000 个 Unicode code points；只保存用户录入内容和版本，不伪造课件页码。
- 单批最多 50 个文件、总计 1 GiB、PDF 总计 5,000 页；任一限制变化必须形成新的输入合同版本。Provider 的当前限制若更低，在 consent 前显示并失败关闭，不静默拆分或改用其他 endpoint。
- 用户明确声明为答案、个人笔记、作业题目/提交或其他延期角色时，在正文处理/外发前返回 `unsupported_role`。本地解析后发现疑似答案或泄露迹象时进入 `needs_user_review`，远端调用与权威覆盖/计划写入为 0；系统不声称能可靠识别所有泄露内容。

### M2 适配解释与理解检查

| 项目 | 规约 |
| --- | --- |
| 输入 | 学习目标、经用户确认的知识点、已有 `LearningEvidence`、来源页面、可选 `StudyFocus` 与当前处理策略。 |
| 行为 | 先定位学生起点，再生成与课件来源绑定的解释；要求学生复述、比较或应用；允许学生纠正来源和系统对困难的归因。首个切片使用概念区分、合成线程轨迹和修复理由三个探针定位失败类型。 |
| 输出 | `ExplanationSession`、来源引用、学生作答与新增 `LearningEvidence`。 |
| 边界 | 一次模型回答或用户阅读行为不等于掌握；无来源补充必须标为模型补充，不能冒充课件事实。首个切片不扩展到同步原语大全、高级内存模型、死锁证明或公平性算法。 |
| 错误处理 | 来源不足、模型超时、预算耗尽或内容冲突时保留现有状态，向用户显示可恢复错误，不生成虚假掌握记录。 |

“来源”统一使用判别联合 `SourceLocator`：PDF 为 `{kind: pdf_page, material_id, content_hash, page, region?}`，图片为 `{kind: image, material_id, content_hash, image_id, region?}`，文本为 `{kind: text_lines, material_id, content_hash, line_start, line_end}`，手工重点为 `{kind: manual_entry, entry_id, version}`。任何“基于材料”的事实都必须指向仍存在且哈希/版本匹配的 locator；无 locator 时 coverage/exam-analysis 空内容失败关闭，解释/练习/反馈最多显示 `model_supplement`，不得进入权威课程事实、计划或来源证据。

### M3 掌握状态与持续复习

| 项目 | 规约 |
| --- | --- |
| 输入 | 完整的追加式 `LearningEvidence` 历史、每个知识点的上一轮 `ConceptReviewState`、当前 `MasteryEstimate`、经用户确认的知识覆盖、知识点依赖、`ReviewPolicy` 版本、当前计划版本、可选考试本地日期/IANA 时区、可选每日预算、`post_exam_state`、已确认 `StudyFocus`、往年卷映射和历次复习尝试。 |
| 行为 | 用版本化、确定性的简单间隔/证据规则推导可解释的掌握估计与 `LearningPlan`；在默认 `continuous` 模式中持续安排，不使用 FSRS/BKT，也不让模型计算权威到期时间。用户可选填每日投入预算；未填写时显示并使用版本化工程默认容量。新证据、目标日期、预算或确认覆盖变化会自动创建 `PlanRevision`，只替换未开始的未来任务，并展示 diff、原因和撤销入口。录入考试日期且用户显式进入 `finals` 后，才结合剩余时间、老师重点、往年卷模式、知识依赖与薄弱证据调整优先级。复习时优先主动提取，再依据结果显示解释并调整后续计划。考试本地日期完整结束后归档本次期末计划、暂停自动生成未来任务并询问新目标。 |
| 输出 | `MasteryEstimate`、版本化 `LearningPlan` / `PlanRevision`、revision diff/`reverts_revision_id`、`ReviewTask`、安排/变更原因、归档/暂停结果和新的尝试证据。 |
| 边界 | 无证据时保持“未知”；掌握度不是客观真值；不得删除历史证据或计划版本来改写结果。模型/provider 只能提出解释、练习或候选映射，不能直接写入权威知识覆盖、优先级、计划或掌握状态。下方的 v1 间隔、容量、证据转换、排序、预算单位/范围和任务时长已随整体签字成为 v1 工程合同；PLAN 只能实现并验证，后续调整必须产生新的 ReviewPolicy/SPEC 版本。 |
| 错误处理 | 证据不完整、日期/时区/预算非法、规则版本不兼容或撤销目标冲突时不提升掌握状态、不覆盖当前计划；保留可重算标记、白名单错误原因和用户纠正入口。 |

#### ReviewPolicy v1（已随整体 SPEC 确认，待实现验证）

1. `daily_budget_minutes` 为 10–480 的整数、步长 5；空值时 `continuous` 使用 30 分钟/日，`finals` 使用 90 分钟/日。界面始终显示实际值、来源（用户/默认）和 policy version。
2. 单个 `ReviewTask.estimated_minutes` 只取 5/10/15/20/30，默认 10；按稳定优先级依次装入每日预算，若当日第一项也超过剩余预算则不自动超额，提示用户修改预算或拆分任务。
3. 间隔阶梯为 `[1, 3, 7, 14, 30]` 个本地日，`interval_index` 为 0–4。新知识、错误、拒答或来源不足设为 0；部分正确降一级（不低于 0）；满足 rubric 的主动提取通过则升一级（不高于 4）。跳过不产生证据、不提升等级；`retained` 还要求至少一次相隔一个本地日的变式主动提取通过。
4. 先过滤未满足前置依赖的任务；有可学习前置时优先安排前置。其余使用稳定字典序：逾期天数降序 → `finals` 中已确认老师重点 → 往年卷重复覆盖次数（封顶 5）→ 证据弱度 → 到期时间升序 → `concept_id` 升序。每项输出 reason codes，不使用隐藏权重或模型排序。
5. `finals` 不设置自动提前窗口；`today_local <= target_local_date` 时仍可学习。只有 `today_local > target_local_date`（考试本地日期已经完整结束）才归档本次计划并进入 `post_exam_paused`。
6. 新证据、预算、目标日期或覆盖变化只生成替换未开始未来任务的 `PlanRevision`。撤销生成带 `reverts_revision_id` 的新修订；已开始/完成任务、证据和旧修订不可删除。固定输入、时钟、tzdata 与 policy version 必须得到相同结果。

`plan_reviews_v1` 是纯函数：输入为规范化且按 ID 排序的课程/概念/已确认覆盖、前置依赖、完整相关 `LearningEvidence` 历史、每个知识点上一轮 `ConceptReviewState`、当前 `MasteryEstimate`、当前未开始任务、`CourseReviewGoal`、`ReviewPolicy v1`、`today_local`、IANA `timezone_id` 和 `tzdata_version`；输出为候选任务、容量溢出与可选 `PlanRevision`，不调用 provider。`ConceptReviewState` 至少包含 `concept_id`、`interval_index`、`last_outcome`、`last_evidence_at` 和 `state_version`；`MasteryEstimate` 必须带算法版本、证据 ID 集合和用户纠正状态。函数先校验状态快照与完整证据历史的一致性；不一致时返回 `state_inconsistent`，不得静默覆盖状态。其唯一算法为：

1. UTC 证据时间先按固定 tzdata 转为 `evidence_local_date`。无证据概念的 `base_due_local_date = max(coverage_confirmed_local_date, today_local)`；有证据时先按第 3 条转换 `interval_index`，再取 `evidence_local_date + intervals[index]`。`source_insufficient` 只创建次日本地来源修复任务并把复习索引置 0，不降低现有 `MasteryEstimate`。
2. 只有已确认覆盖、非 `needs_user_review` 且所有直接前置概念处于 `demonstrated_now`/`retained` 的概念可生成学习任务；被阻塞概念不生成任务，其尚未满足且本身可学习的前置概念加入候选并带 `prerequisite` reason。
3. `continuous` 的生成窗口为 `[today_local, today_local + 29 days]`，请求日期为 `base_due_local_date`。`finals` 窗口为 `[today_local, target_local_date]`；无证据概念请求当天，有证据概念请求 `max(today_local, evidence_local_date + 1 day)`，从而最早隔日复习并把原本更晚的间隔压缩到考前。目标日期已过去时直接输出归档/暂停、零任务。
4. 每个窗口日收集 `requested_date <= day` 且尚未装箱的任务；证据弱度固定为 `incorrect=4, partial=3, unknown/no_evidence=2, demonstrated_now=1, retained=0`，系统/来源错误不改该值。按上方 ReviewPolicy 规则 4 的字典序装入当日分钟预算，不拆分、不超额；剩余任务留到下一日。窗口结束仍未放入的任务进入 `capacity_exceeded`，不得静默丢弃或突破预算。
5. `due_local_date` 是装箱日；`due_at` 仅是显示/通知派生值，取该 IANA 时区当天最早有效 instant（午夜不存在时取首个有效 instant，歧义时取较早 instant）。领域排序只使用 local date，避免 DST 改变计划。
6. 规范化输入使用 UTF-8 canonical JSON（对象 key 和实体 ID 升序）计算 SHA-256 `plan_input_hash`；canonical payload 必须包含完整相关 `LearningEvidence` 历史、`ConceptReviewState`、当前 `MasteryEstimate` 及其版本/纠正字段，而不是只包含最新一条证据。revision/task ID 使用固定 namespace UUIDv5，task name 为 `plan_input_hash|concept_id|due_local_date|task_type`。相同输入得到相同 ID/顺序；候选任务集合与当前未开始集合完全相同时不创建新 revision。

v1 golden fixtures（每项任务默认 10 分钟）：

| Fixture | 输入摘要 | 必须输出 |
| --- | --- | --- |
| G-01 continuous-new | `today=2026-07-20`，空预算（30），`c-a/c-b/c-c` 均已确认、无证据/依赖 | 三项均在 07-20，顺序 `c-a,c-b,c-c`，reason 含 `new_coverage` |
| G-02 evidence-step | 07-20：`c-a` index0 主动提取通过；`c-b` index2 部分正确；`c-c` index3 错误 | 新 index 分别 `1,1,0`；base/due 分别为 07-23、07-23、07-21 |
| G-03 prerequisite | `c-b` 依赖未知的 `c-a`，即使 `c-b` 是老师重点 | 只安排 `c-a`，`c-b` 标 `blocked_by_prerequisite`，老师重点不能越过依赖 |
| G-04 finals-capacity | `today=07-20,target=07-21,budget=20`；三个新概念中 `c-b` 老师重点、`c-c` 往年卷重复 2 次、`c-a` 无焦点 | 07-20 为 `c-b,c-c`，07-21 为 `c-a`；无超额，reason/顺序稳定 |
| G-05 post-exam | `today=07-21,target=07-20,mode=finals` | 零任务；归档当前 finals 并进入 `post_exam_paused` |

这些数值是透明、版本化、可经真实使用调整的工程默认，不宣称是普适教学规律。修改 v1 需要新的 SPEC/策略版本、迁移说明和回归测试；`PLAN.md` 只能实现该合同，不能自行重新选择数值。

### 首个纵向切片：互斥与竞态条件（已确认）

首个切片按以下知识依赖收敛：

```text
并发执行 -> 共享状态 -> 非原子读-改-写 -> 线程交错
         -> 竞态条件 -> 临界区 -> 一种互斥修复的安全性理由
```

学习流程必须包含：

1. **起点探针**：至多 3 个低成本探针，分别检查竞态必要条件、读-改-写事件展开和错误交错定位；探针只定位失败类型，不立即产生永久“未掌握”标签。
2. **适配解释**：根据失败类型选择概念边界、事件状态表、因果链或修复不变量的解释；每个被称为课件事实的结论都绑定存在的本地页。
3. **同构检查**：学生对新的合成两线程轨迹给出合法交错和结果，确定性 oracle 检查线程内顺序、事件完备性与终值。
4. **迁移检查**：学生对表面不同的共享状态场景定位竞态窗口，并说明候选互斥修复保护的安全不变量。
5. **延迟复习**：后续会话先要求主动提取，再提供反馈；只有后续变式证据才能把状态从 `demonstrated_now` 更新为 `retained`。具体间隔数值由版本化工程策略持有，测试使用可注入时钟，不能把任一默认值宣称为普适学习规律。

参数化轨迹 oracle 负责可判定结果；模型/provider 只能提供受来源与 rubric 约束的解释性反馈，不能为自己的输出评分后直接写入掌握状态。

首轮本地来源候选为 `[并发]多处理器编程` 第 25/27 页与 `[并发]互斥` 第 2/14 页；页码、用途、视觉保真限制和版本不变量见 `docs/research/MUTEX_RACE_SOURCE_MAP.md`。这些是可纠正的本地映射，不得随仓库或公开演示分发课件内容。

### X1 安全、凭据与审计（跨模块）

所有材料读取、外发、状态更新和删除都必须经过同一策略层；安全不能只是一个可绕过的设置页面。该控制面负责所有权检查、请求预览、文件级授权、凭据状态、预算/超时、错误脱敏、同意记录、远端对象生命周期、删除审计和最小化日志。第一版 secret 由成熟 keyring 适配 Windows Credential Manager；普通 config、SQLite、浏览器持久化、日志和快照只保存 `credential_ref` 或非秘密状态。若仍有 OpenAI 删除/对账任务，清除凭据前先警告并尝试清理；用户强制清除后所有新远端调用立即失败关闭，遗留对象保留 `delete_incomplete`、原 profile 引用和“重新录入凭据后重试/到 provider 控制台手工删除”的脱敏恢复说明。模式 F 的 provider 无关合同及 OpenAI Files/Vector Stores 映射见 `docs/research/REMOTE_FILE_LIFECYCLE_CONTRACT.md`。

### X2 受约束 AI 模型端口（已确认边界）

第一版提供五类具名端口：`propose_concept_coverage`、`generate_explanation`、`generate_practice_candidate`、`analyze_exam_material` 和 `generate_feedback`。每次调用必须携带端口/版本、课程或任务 ID、允许来源/证据 ID、预算/超时、幂等键和结构化响应 schema；不得携带任意本地路径、凭据或未批准来源。

模型输出一律先作为候选，经来源存在性、schema、大小、预算和领域规则校验后，才进入用户确认或确定性 evaluator。provider 失败、坏 schema、提示注入、取消或预算耗尽不得改变知识覆盖、计划、任务到期、掌握状态、授权或删除结果。详细端口与 mock 合同见 `docs/research/CONSTRAINED_AI_PORT_CONTRACT.md`。

首版唯一真实参考实现是平台内置 OpenAI adapter；deterministic mock 只在 test/demo profile 注册，其他 provider 不是第一版可配置能力。Responses 的 PDF file input 可用于已授权的直接视觉请求，Files + 每课程独占 Vector Store/File Search 可用于模式 F，Structured Outputs 只约束返回结构。OpenAI 原生 File Search citation 不足以证明本地 PDF 页码或页面视觉，因此必须先映射并验证本地 `SourceLocator`；无法定位时，`propose_concept_coverage`/`analyze_exam_material` 返回空内容的 `source_insufficient` 并失败关闭。`generate_explanation`/`generate_practice_candidate`/`generate_feedback` 只能另行显示标为 `model_supplement` 的一般知识，不能称为基于材料、进入覆盖/计划或作为来源证据。禁止猜页码或用文件名冒充 locator。

所有非后台 Responses 请求显式设置 `store:false`，首版禁用 background、Conversations、远程 MCP、Hosted Shell/Code Interpreter 等非必要托管状态/工具。该设置只减少 Responses application-state 存储，**不**消除默认最长 30 天、可能含 prompt/response 的 abuse-monitoring 日志，也不消除非 ZDR 组织支持模型最长 24 小时的 prompt cache；图像/文件还受官方特殊安全审查例外。每次 P/F consent 的 `policy_snapshot_id` 必须同时覆盖 Responses、abuse monitoring、prompt cache、Files 和 Vector Stores，不能只展示“默认不训练”。

#### 模式 F 请求级来源隔离与 locator 证明 v1

1. 每个 vector-store file association 写入不可由用户配置的 `scope_token = SHA256(course_id | material_id | content_hash | consent_record_id | config_fingerprint)` 属性。本地 `RemoteMaterialObject` 保存 token 与 provider File/association 引用；token 不含课程名/路径/正文。
2. 每次 File Search 从仍有效的 `ConsentRecord` 解析精确 allowed File IDs/tokens，在 tool request 中强制使用 `scope_token in [...]` metadata filter，并请求包含 `file_search_call.results`。返回后再次断言每个 result/citation File ID 属于本次 allowlist；任一越界时丢弃整次响应、记 `provider_scope_violation`，权威状态不变。
3. 撤销/切换后 token 立即从 allowlist 移除，即使远端删除未完成也不能再命中。若当前 OpenAI profile/model 不能证明 association attributes、metadata filter、结果包含或 allowlist 大小满足本次 scope，整个课程 store 进入 `source_disabled`，F 请求为 0；不得只依赖 prompt 要求模型忽略其他文件。
4. locator 只通过可重放的文本唯一匹配建立：本地逐页文本和 File Search result chunk 均执行 Unicode NFKC、CRLF→LF、移除 soft hyphen、连续空白折叠/trim；结果必须含至少 32 个 normalized code points，并作为连续子串只匹配同一 `content_hash` 的**唯一一页**。零匹配、多页重复、跨页 chunk、过短 chunk或视觉-only 结论均返回 `source_insufficient`。
5. F 不用模型猜页码，也不上传额外 page sidecar 冒充原生引用。视觉结论只有在已知本地 locator 后，通过另一次经 consent 的 P 直接页面/图像请求才能称为材料事实；否则最多是 `model_supplement`。
6. locator golden fixtures：唯一文本 span 必须映射到预期页；两页含相同 span 必须失败；纯图片页/少于 32 字符必须失败；返回任一非 allowlist File ID 必须使整次响应失败且不写覆盖/计划。

## 4. 关键交互与 WebUI

### 4.1 首次导入（已确认）

1. 检查课程：只读取元数据并显示材料规模与限制。
2. 处理方式：显式比较保真度、外发范围、凭据/费用和解析限制；无选择时不继续正文处理。
3. 确认权限：展示课程模式、本地保存范围、云端发送范围和升级规则。
4. 开始学习：汇总选择，并强调后续修改位置为“课程设置 › 材料与隐私”。

课程级设置会被记住；任何扩大外发范围的切换仍需再次展示实际范围并确认。低保真检测只提示，不自动上传。

### 4.2 视觉层级（已确认方向）

- 桌面端与移动端均使用顶部 X 轴四阶段时间线，不在移动端退化为竖向步骤栏或横向滚动。
- 主要结论通过字号、颜色、字重与字体建立一级强调；依据和限制作为二级信息，减少同时争夺注意力的正文。
- 使用熟悉图标配合短句引导视线；颜色不能成为唯一状态信号。
- “不会静默切换处理方式”和“课程设置 › 材料与隐私”必须高于普通说明文字的视觉权重。
- 当前需求稿见 `docs/mockups/course-import-onboarding.html`。学生已选择安装并使用 Open Design；MCP 注册已写入且当前会话已暴露 Open Design 工具，但 daemon 尚不可达，实际 skill/design system 仍未由学生确认。在恢复可调用性并记录实际选择前，该 HTML 只代表 brainstorming 需求稿，不是正式 UI 或 Open Design 证据。

### 4.3 增量导入与计划修订（已确认）

1. 每次新课件作为独立材料批次进入既有课程，不要求开学时资料完整。
2. 系统展示本批次相对既有知识的 `added/reinforced/changed/unmapped/duplicate` 差异；来源、质量和映射置信度可见。
3. 用户确认可学习/可复习范围后，系统才创建新计划版本；未确认、冲突和低置信项目保持待处理。
4. 计划修订展示新增/加强/延期项、引用材料和证据、被替换的未来任务及版本化原因。
5. 新批次、材料删除或计划修订均不清空历史尝试、学习证据、用户修正和旧计划。

详细状态、不变量与确定性场景见 `docs/research/INCREMENTAL_COURSE_WORKFLOW.md`。

### 4.4 期末周模式（已确认核心语义）

1. 学期中默认处于 `continuous`；没有考试日期也能持续安排。
2. 用户录入考试本地日期和时区后，界面提供“进入期末周模式”，但不得自动切换。
3. 往年卷和老师重点先按材料策略处理，再映射到已确认知识；用户可查看来源、题型/覆盖、难度、置信度并修正。
4. `finals` 模式结合老师明确重点、往年卷重复覆盖、薄弱证据、知识依赖和剩余时间修订未来计划，并解释每个优先级原因。
5. “拟合往年卷”仅表示结构、题型、知识点和难度分析及同类练习，不表示微调/训练模型、预测原题或自动上传资料。
6. 每日投入预算可选；未填写时界面显示正在使用的版本化默认容量。新证据、预算、日期或覆盖变化自动修订未开始任务，展示 diff/原因并可撤销；撤销创建新修订，不删除历史。
7. 修改/清除日期或退出期末模式只影响未来可变任务；历史证据不变。只有考试本地日期完整结束（`today_local > target_local_date`）后才归档本次 `finals` 计划、进入 `post_exam_paused`、停止自动生成未来任务并询问新目标；新目标不会自动再次进入 `finals`。

### 4.5 公开 demo profile（已确认）

- 公开 HTTPS WebUI 只允许从内置合成/明确许可夹具中选择材料，不接受任意上传、路径或 URL；所有 AI 路径固定使用 deterministic mock，构建与运行环境不包含真实 provider 网络权限或 credential store。
- 每个浏览器获得随机、不含身份信息的隔离临时 session；不同 session 不能读取彼此状态。30 分钟无活动或创建满 2 小时后自动清除，用户可随时重置；服务重启可丢弃全部 demo 状态。
- 单 session 最多 1 个活动课程、20 个材料夹具、2 个并发任务和 64 MiB 临时状态；每 IP 每分钟最多 60 个请求，超限返回可恢复提示。固定 demo owner 只作内部 scope，不允许所有访客共享同一可写状态。
- demo 必须完整演示导入、覆盖确认、学习检查、计划修订/撤销和考后暂停，而不是静态 mockup；界面持续标明“演示数据/模拟模型”，不能暗示真实 OpenAI 调用。

## 5. 非功能需求

### 5.1 安全与隐私

- 没有有效同意记录时，远端课件内容调用次数必须为零。
- 文件路径、课件正文、学生作答、掌握状态和凭据不得进入普通日志。
- 所有外部输入、模型输出和工具参数均视为不可信，执行类型/大小/页数/超时/所有权校验。
- 往年卷与老师重点和课件采用相同的不可信输入、最小外发与提示注入隔离；材料角色不构成新的授权。
- 凭据不得硬编码、提交、写入日志或回显；必须支持隐藏录入、配置状态查看、更新和清除。
- 首版凭据由成熟 keyring 适配 Windows Credential Manager；普通 config、SQLite、前端状态和浏览器存储不得包含 secret。OpenAI profile 只允许平台 schema 中的模型、预算等非秘密字段与 `credential_ref`，出现任意 `base_url`、自定义 endpoint 或动态 plugin 字段时在联网前拒绝。
- 删除必须覆盖原文缓存、抽取、可重建正文的索引和适用的远端对象，并停止后台任务；历史证据/计划只保留不含正文、路径或 provider ID 的 tombstone 与失效 locator，使历史仍可解释但不能重建已删内容。未完成清理必须显示真实状态。
- 本地 Web 服务默认只绑定 loopback；校验 `Host`/`Origin`，拒绝任意跨域访问，所有状态变更具备 CSRF 防护，避免恶意网页借浏览器访问 localhost 数据。
- 公开 demo profile 只加载合成或明确许可夹具与 deterministic provider mock，禁用任意上传、真实凭据录入、真实 provider 出站调用和私人课件持久化；不同访客使用有期限的隔离 session。

完整候选威胁模型见 `docs/research/COURSEWARE_THREAT_MODEL_BASELINE.md`。

### 5.2 可用性与无障碍

- WebUI 在 320 px 以上宽度不应产生页面级横向滚动；文字、时间线、模式控件和操作按钮不得重叠或裁切。
- 交互必须支持键盘和可见焦点；图标提供文本标签或可访问名称。
- 关键状态不能只靠颜色表示；错误需要给出恢复动作。
- 首次导入选择只对当前课程生效，不让用户误解为全局授权。

### 5.3 性能、可靠性与可观测性

- 参考环境为 Windows 11 x64、4 个逻辑 CPU、16 GiB RAM、SSD；环境差异必须随基准结果记录。15 份、932 页、约 195.4 MB 的真实样本仅在本地私有基准中使用，不进入仓库/CI/公开 demo。
- 该样本的元数据/哈希检查目标为 15 秒内给出首屏和逐文件状态；完整本地解析/来源索引在 20 分钟内完成，峰值进程 RSS 不超过 2 GiB。若正式解析器基准无法达到，必须在 SPEC 签字后通过显式变更记录调整，而不是删除测试。
- 长任务至少每秒更新一次进度；用户取消后 2 秒内界面进入 `cancelling/cancelled`，5 秒内不再启动新页处理。进程重启后 10 秒内恢复可观察任务状态，不重复权威材料或计划；远端上传只承诺本地幂等和重复对象对账，不承诺 provider exactly-once。
- 本地非模型 API 在 1,000 个概念、10,000 条证据的合成数据集上，读操作 p95 小于 500 ms、状态变更 p95 小于 1 s；真实 provider 延迟单独显示，不计入该本地 SLO。
- 导入和远端请求必须具备超时、取消、本地幂等和有界重试；失败不得产生重复本地权威材料/job。真实 provider 若产生重复对象或潜在额外费用，必须隔离、对账、清理并如实显示，不能承诺 exactly-once。
- 模型调用必须按端口、版本、来源范围和幂等键审计；schema 校验失败时不得从自由文本猜测字段或进入权威写入路径。
- 结构化日志只记录白名单元数据、内部对象 ID、耗时和结果，不记录敏感正文。

## 6. 架构与数据流

```text
Windows x64 browser
  -> React/Vite/TypeScript localhost WebUI
       -> Python/FastAPI application service
            -> M1 Material / Fidelity
            -> M2 Explanation / Understanding Check
            -> M3 Mastery / Review
            -> X1 Policy / Credential / Audit / Remote Lifecycle
            -> X2 Constrained Model Ports
            -> SQLite + local material/unit storage
            -> keyring -> Windows Credential Manager
            -> Local parser/render adapter
            -> ProviderAdapterRegistry
                 -> built-in OpenAI reference adapter (local profile only)
                      -> user-configured ProviderProfile
                      -> capability/policy snapshot

Public HTTPS browser
  -> same WebUI + FastAPI domain contracts in demo profile
       -> per-browser ephemeral session / automatic reset
       -> synthetic or explicitly licensed fixtures only
       -> deterministic provider mock only
       -> no credential store / no provider egress / no arbitrary upload
```

材料数据流必须经过以下门禁：

```text
用户选择文件 -> 元数据检查 -> awaiting_policy
  -> 用户选择处理模式 -> 记录策略/同意
  -> 本地解析或经确认的远端调用
  -> 原页/抽取/质量报告 -> 候选知识覆盖 -> 用户确认
  -> 计划新版本 -> 带来源的解释/复习上下文
```

模式 F 的额外数据流为：

```text
文件批次 -> 文件级 consent -> upload -> index -> ready
         -> 受约束端口按本地 SourceLocator 引用
         -> 切换/撤销 -> delete_requested -> deleted | delete_incomplete
```

新材料与期末模式的数据流为：

```text
新批次 -> 覆盖差异 -> 用户确认 -> PlanRevision -> 持续学习

考试日期 + 用户显式进入
  -> 往年卷/老师重点候选映射 -> 用户确认
  -> finals PlanRevision -> 同类练习/模拟 -> 新证据 -> 再规划
```

`已确认`：第一版私有课件、索引和学习状态默认留在 Windows x64 本机，由浏览器访问 localhost WebUI；不包含账号或多租户服务。后端采用 Python/FastAPI，前端采用 React/Vite/TypeScript，权威状态存入 SQLite，secret 进入 Windows Credential Manager。远端能力经过统一适配器注册表；首版唯一真实实现是平台内置 OpenAI adapter，另有 test/demo mock/contract suite，未配置 profile 时不会静默启用。单文件 `ProjectB.exe` 分发与 Hugging Face Spaces Docker SDK 上的 OCI demo 已随整体 SPEC 确认为 v1 工程方向，后者仍待官方连通性/费用复核。精确依赖/冻结/索引库不能改变上述已确认边界。

## 7. 候选数据模型

| 实体 | 目的 | 核心约束 |
| --- | --- | --- |
| `Course` | 聚合课程材料、策略和学习状态 | 第一版绑定本地 actor；所有对象仍继承明确 owner scope；处理策略可查看和修改 |
| `MaterialBatch` / `MaterialRole` / `RoleValidation` | 表示一次增量导入、用途与角色检查 | 第一版只允许 `lecture`、无答案 `past_paper`、`teacher_focus`；文件独立状态；内容哈希幂等；`needs_user_review` 时无远端/权威写入；角色不扩大外发授权 |
| `Material` / `MaterialUnit` / `SourceLocator` | 保存文件/手工条目身份、可引用单元、抽取与质量 | PDF 页、图片、文本行范围和手工 entry 使用判别联合类型；原始单元和抽取独立版本；locator 绑定内容哈希/版本且可失效 |
| `ProcessingPolicy` | 保存当前课程模式 | 扩大外发不能仅覆盖原值 |
| `ConsentRecord` | 追加记录授权和撤销 | 不保存课件正文；保留 from/to mode、payload scope 与 provider profile/config/policy 指纹 |
| `ProviderProfile` / `ProviderCapabilitySnapshot` / `ProviderPolicySnapshot` | 保存用户选择的非秘密 provider 配置及调用所依据的能力/政策 | 第一版 adapter ID 只允许内置 OpenAI；profile 只含受支持模型、受控参数、预算和 `credential_ref`，拒绝任意 endpoint/plugin；policy 覆盖 Responses/abuse monitoring/cache/Files/Vector Stores；快照不可被后续配置静默改写 |
| `RemoteMaterialObject` / `RemoteJob` / `CourseVectorStore` | 追踪模式 F 的远端对象、scope token 和任务 | 每课程/profile/config 独占 Vector Store；File/association/store 分层状态；association 带不可由用户配置的 `scope_token`，request 过滤并后验验证 File ID；能力不足为 `source_disabled`；重复对象对账/清理 |
| `KnowledgeConcept` / `SourceReference` | 将知识点绑定材料来源 | 材料事实必须指向存在且版本匹配的 `SourceLocator`；模型补充单独标记，失效 locator 只留脱敏 tombstone |
| `ConceptCoverage` / `CoverageDecision` | 表示材料到知识点的候选映射与用户确认 | 候选/确认分离；低置信、冲突项不能自动进入计划 |
| `StudyFocus` | 表示老师重点或往年卷模式到知识点的映射 | 来源、种类、置信度和确认状态可见；不得与模型推断混淆 |
| `ProbeTemplate` / `Attempt` | 生成可重放的参数化探针并记录一次尝试 | 模板与实例分离；参数种子可重放；普通日志不存作答正文 |
| `RubricCriterion` | 把概念、过程、结论和来源分开评分 | 必需条件失败不能被总分掩盖；记录 evaluator 类型 |
| `ExplanationSession` | 记录一次适配解释 | 绑定目标、基线证据、来源和处理模式；不直接更新掌握 |
| `LearningEvidence` | 连接理解检查与复习 | 追加式、保留评分依据和时间 |
| `ConceptReviewState` | 保存每个知识点上一轮调度状态 | 至少包含 `concept_id`、`interval_index`、`last_outcome`、`last_evidence_at`、`state_version`；由完整证据历史重算并与当前估计校验，不得被新计划静默覆盖 |
| `MasteryEstimate` | 可解释的候选掌握状态 | 引用证据、规则版本和推导时间；可纠正/重算 |
| `ReviewPolicy` | 固定可重放的调度合同 | 包含 v1 预算默认/范围、任务时长、间隔阶梯、证据转换、稳定排序和 tzdata version；历史计划引用原版本 |
| `CourseReviewGoal` | 保存持续/期末模式、可选考试日期、IANA 时区、每日预算分钟和考试后状态 | `finals` 必须同时有日期和显式进入记录；预算可空；仅 `today_local > target_local_date` 后暂停；版本化变更 |
| `LearningPlan` / `PlanRevision` | 保存可重放计划及每次修订 | 旧版本不可覆盖；自动修订只重排未开始未来任务；撤销以 `reverts_revision_id` 创建新修订 |
| `ReviewTask` | 表示后续复习 | `estimated_minutes` 取 v1 白名单；到期原因可见；完成必须关联实际尝试 |
| `CredentialStatus` / `AuditEvent` | 凭据状态与最小化审计 | 不暴露 key，不记录正文或作答 |

字段级候选设计见 `docs/research/TUTORING_DOMAIN_MODEL_DRAFT.md`。

## 8. 凭据威胁模型与配置流程

### 已确认约束

1. 首次需要云端能力时，以隐藏输入录入凭据。
2. 查看只返回“已配置/未配置”和更新时间，不回显明文。
3. 支持更新与清除；存在远端删除/对账任务时先警告并尝试清理。用户强制清除后新远端调用立即失败关闭，遗留对象保持 `delete_incomplete` 与脱敏恢复说明。
4. 第一版正式运行、本地二进制和公开 demo 均不从 `.env` 读取 API key；开发/测试也使用 mock 或独立人工集成 profile。若未来增加 `.env` 兼容，必须作为新的显式安全变更评审，不能由库默认行为偷偷启用。
5. 用户在本地 config/设置中选择平台已实现的 adapter，并配置模型、受控参数、预算和凭据引用；API key/token 不得进入普通 config、浏览器存储、日志或快照。
6. 未知 adapter、无效 profile、缺少凭据或能力声明不足时，在网络调用前失败关闭；L 模式仍可使用。切换 adapter/profile 或其政策指纹后，旧同意不得复用。

### 已确认实现边界与待验证项

- 第一版目标平台为 Windows x64，secret 通过成熟 keyring 适配 Windows Credential Manager；前端只能提交隐藏录入值给后端凭据服务，状态接口只返回“已配置/未配置”、更新时间和白名单错误码。keyring 包、版本、许可证、Windows 后端行为及打包兼容性在加入依赖前核验。
- Provider-neutral 架构保留；local production profile 只注册内置 OpenAI reference adapter，deterministic mock 只在 test/demo profile 注册。普通 config 不允许 `base_url`、任意 endpoint、模块路径或第三方 plugin；具体 OpenAI 模型由受支持 profile 显式配置，不设静默固定模型。
- 每次 P/F 外发前必须展示并绑定 OpenAI capability/policy snapshot。当前官方快照说明 API 数据默认不用于训练（除非组织显式选择分享）；Responses 默认 application state、最长 30 天 abuse monitoring、最长 24 小时 prompt cache、图像/文件安全审查例外，以及 Files/Vector Stores 非 ZDR且保留到删除必须分别呈现。首版 Responses 固定 `store:false` 并禁用非必要后台/托管工具，但不得把它解释为 ZDR。动态政策、区域资格、费用与容量在运行前刷新/展示并受预算限制。
- 模式 F 只有在 adapter 通过上传、异步 ready、本地 `SourceLocator` 映射、每课程独占 Vector Store 对账、删除/过期和恢复 contract test 后才能启用。OpenAI Python SDK 许可证本轮未现场核验；在选包/锁版本前必须验证并记录，不能把候选 SDK 当作已获许可依赖。

## 9. 分发、部署、CI 与设计系统

- `已确认`：最终必须提供可访问的 WebUI URL。
- `已确认`：第一版真实使用形态是单用户、本地 WebUI；桌面窗口只能作为可选壳，不能替代 WebUI。多用户与分享不进入第一版。
- `已随整体 SPEC 确认的 v1 工程方向`：课程分发类别采用 **Windows x64 单文件原生可执行二进制**。交付物 `ProjectB.exe` 内嵌前端与必要运行资源，用户不需安装 Python、Node 或 Docker；运行期数据写入文档化目录。具体冻结工具在 PLAN 中按许可证、冷启动、Credential Manager 和资源集成证据选择。若无代码签名，README/发布页如实说明 SmartScreen，不能伪称已签名。
- `已随整体 SPEC 确认的 v1 工程方向`：公开实例使用同一 WebUI/领域合同的 **OCI container demo**，首选 **Hugging Face Spaces（Docker SDK）**，固定为许可夹具 + deterministic mock；无真实 key、任意上传/provider egress 或私人课件持久化。镜像须支持单条 build/run。2026-07-20 官方复核因 web 502、`curl` 超时未完成；部署前须重核 Docker、HTTPS、休眠/临时存储、费用与账号条款。不满足无付费边界时须通过 SPEC 变更，不能静默产生费用。
- `已确认`：NJU Git/GitLab 为课程主仓，GitHub 为镜像；两套 CI 调用同一条一键测试命令。`.gitlab-ci.yml` 必须含名称严格为 `unit-test` 的 job，GitHub Actions 每次 push 运行测试；最终两边真实记录和课程提交对应 CI 必须通过。建仓、push、PR/MR、镜像和部署仍需执行时授权。
- `已确认路线/外部门禁`：Open Design 0.15.0 桌面端已安装，agent 已设为 Codex；学生已完成 MCP 注册，`~/.codex/config.toml` 出现 `open-design` 且当前会话暴露 MCP 方法。实际调用仍返回 daemon `127.0.0.1:7456` 不可达，配置仍为 `skillId=null`、`designSystemId=default`、项目位置为空。只读候选调查推荐 `frontend-design` + `default`（项目覆盖：卡片半径最多 8px、letter-spacing=0、紧凑工作台），`shadcn` 为 design-system 备选，`web-design-guidelines` 仅作实现后审查；这些尚未由学生确认。daemon 恢复且实际选择写入本文前不得开始正式 UI 实现，现有 HTML 只作 brainstorming 证据。

详细工程基线与分发完成标准见 `docs/research/TECH_STACK_DISTRIBUTION_BASELINE.md`。

## 10. 技术选型

| 选择 | 采用原因 | 第一版限制 |
| --- | --- | --- |
| Windows x64 单文件原生二进制（已确认方向） | 与真实本机课件、浏览器和 Credential Manager 边界一致；不要求开发环境 | macOS/Linux 延期；冻结工具须先核验许可证、单文件资源加载与干净机行为 |
| Python + FastAPI | 文件处理生态、类型化 API 与可测试依赖注入适合 M1/X1/X2 | 精确 Python/FastAPI 版本须通过依赖矩阵；不对 LAN 监听 |
| React + Vite + TypeScript | 满足响应式 WebUI、状态密集导入/学习流程和可访问性测试 | 构建后作为静态资源随本地二进制/OCI 镜像分发，不要求最终用户安装 Node |
| SQLite | 单用户、本地事务、版本化证据和迁移可复现 | 单写者边界；不作为多用户服务数据库 |
| keyring + Windows Credential Manager | secret 不进入 config/SQLite/浏览器，支持状态/更新/清除 | 只验证 Windows 后端；无 `.env` 正式兼容路径 |
| 内置 OpenAI adapter + shared contract/mock | 一条真实 P/F 路径，同时保持领域状态可在无网络下确定性测试 | local production 只暴露 OpenAI；mock 仅 test/demo；无任意 endpoint/plugin |
| Hugging Face Spaces Docker SDK 上的 OCI public demo（已确认方向，待官方复核） | 便携部署相同 WebUI/领域合同并强制无密钥、临时状态 | 当前配额/费用/临时存储未现场复核；只用许可夹具/mock，与本地私有版隔离，不获授权不创建 Space |

精确 Python/Node 版本、框架/SDK/解析/索引/冻结依赖、SQLite schema 和构建集成仍需以兼容性、许可证、成本和可复现验证固化；Hugging Face Spaces Docker SDK 条款须重核。后续工程证据不得改变已确认的单用户本地优先、Windows x64、凭据后端、内置 adapter、双 CI、单文件分发与 OCI/HF 方向；PLAN 不得静默改写。Python 3.13 只是兼容性候选，不是唯一版本。

**已确认：第一版采用受约束 AI 功能，不包含课程定义的 agent。** 模型只能通过具名、结构化且有来源范围的端口生成候选知识映射、适配解释、练习、反馈和期末资料分析；应用状态机、版本化规则、确定性 oracle 与用户确认拥有权威写入权。若未来加入自主多轮决策、自主工具调用和反馈自修正，必须重新取得学生确认，并自行编码可用 mock/stub 确定性测试的主循环、工具分发和治理护栏。方案比较与延期理由见 `docs/research/AGENT_BOUNDARY_OPTIONS.md`，端口合同见 `docs/research/CONSTRAINED_AI_PORT_CONTRACT.md`。

## 11. 候选验收标准

| ID | 客观判定 |
| --- | --- |
| AC-01 | 首次导入只做元数据检查；未选择策略时正文解析调用与远端调用均为 0。 |
| AC-02 | 用户能在桌面/移动 WebUI 比较可用处理模式；扩大外发范围时必须产生新的确认记录。 |
| AC-03 | 每个被标为“基于材料”的解释都能打开存在且版本匹配的 `SourceLocator`（PDF 页/区域、图片、文本行范围或手工 entry）；抽取内容不覆盖原始单元。 |
| AC-04 | 解释会话不能直接产生“已掌握”；至少一次学生产生的理解/复习证据才可提高掌握估计。 |
| AC-05 | 每个复习任务显示知识点、到期原因和证据；完成后追加尝试并可解释下一次安排。 |
| AC-06 | 删除材料后本地检索不再返回其正文/单元；历史只保留不能重建内容的 tombstone/失效 locator。远端删除失败显示 `delete_incomplete` 而非假报成功。 |
| AC-07 | 凭据状态、日志、错误、快照和 Git 扫描均不含凭据明文或课程正文。 |
| AC-08 | 320 px、390 × 844、1440 × 900 下无页面级横向滚动、文字裁切或控件重叠；四阶段均保持 X 轴时间线。 |
| AC-09 | 完成页以高于普通说明的视觉权重展示“课程设置 › 材料与隐私”，最终主操作名为“开始学习”。 |
| AC-10 | 一条本地命令运行核心测试；GitLab 名称严格为 `unit-test` 的 job 与 GitHub Actions 调用同一入口，两个平台的实际 CI 及最终课程提交对应记录均通过。 |
| AC-11 | 第一版本地服务默认仅绑定 loopback；非受信 `Host`/`Origin` 和无有效 CSRF 证明的状态变更请求均被拒绝，且不存在注册/多租户入口。 |
| AC-12 | 互斥/竞态起点诊断至多使用 3 个探针，并能把失败归因到概念条件、事件展开或错误交错；诊断本身不直接写入永久“未掌握”。 |
| AC-13 | 对固定参数种子的合成两线程轨迹，确定性 oracle 可重放合法交错与终值；provider mock 的反馈变化不改变正确性或掌握判定。 |
| AC-14 | `demonstrated_now` 至少关联一个同构检查和一个迁移检查；只有由可注入时钟标记为后续会话的变式主动提取证据才能产生 `retained`。 |
| AC-15 | 同一文件重复导入不创建重复材料、覆盖或远端计费任务；批次部分失败时成功/失败文件分别可见且可独立重试。 |
| AC-16 | 新材料产生的候选知识覆盖在用户确认前不进入权威课程知识或计划；确认后生成新 `LearningPlan` / `PlanRevision` 并显示变更来源与原因。 |
| AC-17 | 新批次、计划修订和材料删除均不删除历史 `Attempt`、`LearningEvidence`、用户修正或旧计划；失效来源被明确标记。 |
| AC-18 | 仅录入考试日期时课程仍为 `continuous`；只有日期有效且用户显式操作后才进入 `finals`，修改/清除日期或退出只重排未来任务。 |
| AC-19 | 往年卷和老师重点必须先生成带来源/置信度的候选映射并经用户确认；未确认映射、provider 输出或 provider 失败均不得改变权威优先级、计划和掌握状态。 |
| AC-20 | 往年卷处理测试能证明不存在训练/微调、自动上传或“预测原题”路径；任何远端请求仍满足课程处理策略与有效同意记录。 |
| AC-21 | 每次模型调用都包含已知端口/版本、允许来源范围、预算/超时和幂等键；未知端口、越界来源、任意本地路径或缺失 schema 被调用前拒绝。 |
| AC-22 | provider 返回坏 schema、注入文本、超时、限流、取消或预算耗尽时，权威知识覆盖、计划版本、`due_at`、掌握状态、授权与删除结果保持不变。 |
| AC-23 | 无网络、真实 LLM 和凭据时，provider mock 可确定性覆盖成功、低置信、无来源、坏 schema、失败和重复响应；模型措辞变化不改变 oracle/rubric 与领域状态结果。 |
| AC-24 | 第一版不存在自主 agent loop 或模型可调用的任意工具分发；模型输出只能进入候选校验、用户确认或解释展示路径。 |
| AC-25 | 第一版 WebUI 显示并支持 L/P/F 三种能力；没有用户选择和精确文件/批次 `ConsentRecord` 时，不产生远端上传调用。 |
| AC-26 | 模式 F 的文件/索引状态至少可观察 `awaiting_consent`、`uploading`、`indexing`、`ready`、失败、删除中、`deleted` 与 `delete_incomplete`；部分失败不假报全成功。 |
| AC-27 | 模式 F 用内容哈希/本地幂等键避免重复本地 job；进程重启、响应丢失、取消、离线恢复和新增批次不会丢失远端对象追踪。若 OpenAI 无已证明的 exactly-once/幂等接口，重复远端对象会被发现、隔离、对账并清理，界面不承诺“绝不重复计费”。 |
| AC-28 | 从 F 切回 L/P 或撤销授权后，新请求立即拒绝 F 远端来源；对象进入删除流程，删除未确认时显示 `delete_incomplete`，历史本地证据不被删除。 |
| AC-29 | provider 适配器若不能声明对象追踪、引用定位或删除/过期语义，模式 F 不可启用；界面不能把未知清理状态显示为 `deleted`。 |
| AC-30 | 未配置 profile、adapter ID 未知、配置 schema 无效、凭据缺失或能力不足时，P/F 在网络调用前失败关闭且 L 仍可用；普通 config、日志、错误、快照和浏览器存储均不含 secret。 |
| AC-31 | adapter/profile、模型/config 或政策指纹变化后，旧 `ConsentRecord` 不可授权新调用；新调用等待精确确认，旧 profile 的远端对象与删除状态继续独立追踪。 |
| AC-32 | 内置 OpenAI reference adapter 与 provider mock 都通过同一 provider-neutral contract suite；真实 adapter 的措辞、ID 和 SDK 异常不会泄漏到领域状态或改变确定性 oracle。 |
| AC-33 | 第一版只接受白名单材料角色/格式。用户声明的答案 key、个人笔记、作业题目/提交和未知角色在正文处理/外发前返回 `unsupported_role`；本地解析后发现疑似答案/泄露迹象时进入 `needs_user_review`，远端调用与权威写入为 0，界面明确“不保证自动识别全部泄露内容”。 |
| AC-34 | 固定课程、证据、目标、时钟和策略版本时，确定性调度重复运行得到相同任务/原因；provider mock 的成功、失败或措辞变化不改变权威 `due_at`/priority，首版没有 FSRS/BKT 或模型权威调度路径。 |
| AC-35 | 每日预算可留空；界面显示所用默认容量及策略版本。新证据、预算、日期或覆盖变化只自动替换未开始任务并显示 diff/原因；撤销创建新的 `PlanRevision`，历史任务、修订和证据仍可读取。 |
| AC-36 | `today_local <= target_local_date` 时不提前暂停；仅考试本地日期完整结束（`today_local > target_local_date`）后，本次 `finals` 计划归档并进入 `post_exam_paused`，不再自动生成未来任务；新目标不会自动进入 `finals`，历史证据不删除。 |
| AC-37 | File Search request 使用当前 consent 派生的 `scope_token in [...]` metadata filter，并对结果 File ID 做二次 allowlist；越界结果使整次响应失败。只有经 v1 规范化后不少于 32 字符且只匹配同一 content hash 唯一一页的 chunk 才生成 locator；重复页、跨页、过短或视觉-only 均 `source_insufficient`。 |
| AC-38 | OpenAI profile schema 遇到任意 `base_url`、自定义 endpoint、动态 adapter/plugin 或未知字段时拒绝，网络调用为 0；local production registry 只暴露内置 OpenAI，mock 仅在 test/demo profile 注册。 |
| AC-39 | P/F consent/policy snapshot 明确展示 Responses application state、最长 30 天 abuse monitoring、最长 24 小时 prompt cache、文件安全审查例外，以及 Files/Vector Stores 的训练、ZDR、区域和删除/过期事实；不得用“默认不训练”覆盖任一留存语义。 |
| AC-40 | Windows x64 本地版用 keyring/Windows Credential Manager 完成隐藏录入、状态、更新、清除和失败关闭；config、SQLite、`.env`、前端状态、浏览器存储、日志、错误、测试快照与 Git 均不含 secret。存在清理任务时强制清除会保留 `delete_incomplete` 和恢复入口。 |
| AC-41 | 公开 demo 只加载内置合成/明确许可夹具和 deterministic provider mock；任意上传、真实凭据录入、真实 provider 出站调用与私人材料持久化路径均被禁用，隔离/到期 session 中的核心导入、确认、学习和复习流程仍可操作。 |
| AC-42 | NJU Git/GitLab 主仓与 GitHub 镜像针对同一 commit 保存可核验的测试记录；GitLab `unit-test`、GitHub Actions、PR/MR 和最终提交证据不得由本地日志替代。 |
| AC-43 | 单个 Windows x64 `ProjectB.exe` 在干净环境中无需 Python/Node/Docker即可完成获取、启动 localhost WebUI、SQLite 初始化、凭据状态操作和卸载/数据保留说明；签名/SmartScreen 状态如实记录。 |
| AC-44 | 正式 UI task 开始前已记录可调用 Open Design 版本、MCP/skill 与实际 design system；实现后使用真实浏览器在 AC-08 视口逐项截图/交互验证，现有 brainstorming HTML 不算该证据。 |
| AC-45 | M1 对每种 MIME/扩展名、编码、单文件/批次大小、页数/像素/文本长度、空/损坏/加密/伪装文件逐项执行 v1 限制；provider 限制更低时在 consent 前失败关闭，未授权正文/网络调用为 0。 |
| AC-46 | 在 5.3 参考环境上，真实私有样本的元数据首屏/状态、完整本地解析、峰值 RSS、取消和重启恢复均达到给定阈值；命令、环境、开始/结束时间和原始结果随本次运行留证，真实课件不进入产物。 |
| AC-47 | OCI demo 可由单条 `docker build` 与单条 `docker run` 启动；从外部干净浏览器通过 HTTPS URL 完成核心流程。跨 session 读取为 0，30 分钟不活动/2 小时总寿命后状态清除，上传、并发、存储和速率上限可复现。 |
| AC-48 | 学生执行时明确批准后，使用其 Credential Manager 凭据和最多 5 页/20k 输入 tokens 的合成或许可夹具完成一次 P、一次 F 全生命周期。单次套件最多 20 个 HTTP 请求、2 个 Responses、每个最多 1,500 输出 tokens、状态轮询最多 5 次；非幂等 create 自动重试 0 次，GET/status 最多重试 1 次，总时长 10 分钟。当前官方价格无法取得或预估超过 US$1.00 时调用为 0；任何真实 key/正文不进 CI、日志或仓库。 |
| AC-49 | 所有首版 Responses 请求可捕获证明 `store:false`、非 background、未使用 Conversations/远程 MCP/Hosted Shell/Code Interpreter；policy snapshot 同时保留 abuse monitoring/cache/文件审查例外，不能把 `store:false` 呈现为 ZDR。 |
| AC-50 | 每个课程/profile/config 使用独占 Vector Store；两份材料中只有获准 token 可被检索，撤销/删除中的另一份命中为 0。删一份只清理该 association/File且另一份仍可检索；仅删除课程/F、无剩余关联时删 store。filter/attributes/results 能力无法证明时 store 为 `source_disabled`、F 调用为 0。 |

这些验收标准需随模块行为、技术栈和部署决策继续细化；目前没有正式实现测试证据。

## 12. 风险与未决问题

| 问题 | 状态/影响 |
| --- | --- |
| SPEC 整体签字已完成 | 学生于 2026-07-20 明确回复“已确认spec.md”；阶段 B 可在正式调用 `writing-plans` 后开始 |
| OpenAI File Search 页码/视觉保真不足 | 只有通过本地 `SourceLocator` 校验才能称为材料事实；失败时 coverage/exam-analysis 空内容关闭，解释/练习/反馈仅可标 `model_supplement`，不得伪造页码或进入计划 |
| OpenAI 动态政策、模型、容量、费用和 SDK 许可证 | Provider 方向已确认；运行前 policy snapshot 必须覆盖 Responses/abuse monitoring/cache/文件安全审查/Files/Vector Stores；支持目录、SDK 许可证与兼容性仍需真实核验 |
| 模式 F 重复对象、所有权与远端残留 | OpenAI 未提供已证明的上传 exactly-once；只能本地幂等、发现/对账/清理重复对象。每课程独占 store，File/association/store 分层删除，无法确认时保留 `delete_incomplete` |
| ReviewPolicy v1 默认值尚无真实学习效果证据 | 纯函数/fixtures 已随整体签字成为 v1 工程合同。实施后只能通过新 policy/SPEC 版本调整，不能宣传为科学最优 |
| 公开 WebUI 尚无平台/URL | demo profile 已确认为合成/许可夹具 + mock；具体账号、托管平台和部署动作需要执行时授权，最终必须提供真实可访问 URL/CI-CD 证据 |
| Hugging Face Spaces 官方复核受网络阻塞 | Docker SDK 已确认为首选方向；2026-07-20 web 502/curl 超时，部署前必须重核费用、Docker/HTTPS、休眠与临时存储 |
| Windows x64 分发尚未验证 | 单文件 `ProjectB.exe` 已确认为分发方向；冻结工具仍须通过许可证、干净机、Credential Manager、SmartScreen 和数据边界验证 |
| 双远程平台尚未执行 | NJU Git/GitLab 主仓 + GitHub 镜像及双 CI 已确认；建仓、push、PR/MR、镜像与部署需执行时授权，当前本地记录不能代替远程证据 |
| Open Design daemon/skill/design system 未完成 | MCP 配置已写入且工具已暴露，但 daemon 当前不可达；`skillId`/实际 design system/项目位置均未确认。恢复 daemon、复验工具、由学生确认候选并记录选择是正式 UI 前的门禁 |
| Superpowers 阶段 B skill 未注册 | v6.1.1 缓存已检测，但当前会话未暴露 `writing-plans`；SPEC 签字后须在已注册的新会话正式调用，不能以手工计划代替 |
| 冷启动智能体类型 | D-005 尚待学生在阶段 C 前决定；不阻塞当前 SPEC 签字或阶段 B 计划编写 |
| brainstorming 个人反思尚缺 | 课程审计要求学生本人评价过程优点、不足与关键取舍；AI 可提供问题框架但不得伪造学生观点或代写 `REFLECTION.md` |
| 操作系统课件许可证未知 | 私人本地学习可继续核验；阻塞把真实课件放入 Git、CI、分发包或公开 demo，也要求每次远端整份处理由用户确认其权利与风险 |

尚需学生决定、外部安装或执行时授权的事项统一维护在 `DECISIONS_NEEDED.md`；已确认项保留为过程证据，不再作为开放问题。

D-011 已采用互斥与竞态条件作为首个纵向切片。三套候选、选择依据和共同评分边界见 `docs/research/FIRST_LEARNING_LOOP_CANDIDATES.md`。

D-012/D-019/D-020 已确认双模式、材料白名单和保守确定性方向；ReviewPolicy v1/fixtures 已随整体 SPEC 签字成为 v1 工程合同。候选比较和时间测试见 `docs/research/REVIEW_SCHEDULING_OPTIONS.md`，增量流程见 `docs/research/INCREMENTAL_COURSE_WORKFLOW.md`。

## 13. 阶段门禁

- 学生已于 2026-07-20 对本文做整体确认；阶段 A 的 placeholder/矛盾/歧义/范围静态自审已有证据。该证据只证明整体签字，不虚构逐段口述审阅。
- `SPEC.md` 签字门禁已解除；必须在正式应用 Superpowers `writing-plans` 后创建 `PLAN.md`，当前会话若未注册该 skill 不得把手工草稿冒充正式调用。
- 在 `PLAN.md`、陌生智能体冷启动验证、缺陷修订与学生实现批准完成前，不得编写正式实现代码。
- `REFLECTION.md` 只能由学生本人撰写；AI 仅可在学生初稿后按声明范围辅助。
