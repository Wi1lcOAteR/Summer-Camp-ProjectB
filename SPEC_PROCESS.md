# SPEC_PROCESS

## 2026-08-03 G-03 同字节双评审完成

- 冻结字节：SPEC `AEA67BB5544AD22932DC4304964F7FD266FE8A5DE7AA396EA8974D30867E8381`；PLAN `910A3AEC9B4CEDCC119675C5D862879D178E3FE062CEE39C2AD62AF07219E923`。
- 规约合规评审：`PASS`，Critical=0、Major=0、Minor=0。确认 39 个可派发 task；`QA-RELEASE` 明确为非派发验证门禁，不计入台账。
- 质量/安全/许可证评审：`PASS`，Critical=0、Major=0。非阻塞 Minor：CR-only 行计数、未知 tool 事件负例、1 MiB 输出上限的直接运行级测试；当前不阻塞 G-03 资料冻结。
- 机械与运行证据：`PLAN_MECHANICAL_PASS Tasks=39 Ledger=39 Fields=5 AcRows=24 Placeholders=0 Unknown=0 Self=0 Cycle=0 DependencyEdges=38`；`AGENT_CAPSULE_PASS documents=2`；`AGENT_CAPSULE_CONTRACT_PASS cases=9`；`G03_SNAPSHOT_CONTRACT_PASS`；`G03_RUNNER_CONTRACT_PASS cases=13`；`G03_RUNNER_ENTRYPOINT_PASS cases=5`。正式非 Codex intake/execution 尚未重跑，G-03 仍为 NOT PASS。

## 2026-08-03 G-03 原子计划确认与评审修订

- 学生明确确认原子化 SPEC，并要求尽快完成冷启动后进入实际实现。随后使用 `writing-plans` 将原 F-01S1 拆为 `F-01S1A` 与串行 `F-01S1B`；当前权威文件为 SPEC `AEA67BB5...E8381`、PLAN `910A3AEC...9E923`，先前 `5ABC65A4...C598A` / `D111B729...C5706` 仅保留为被取代的候选历史。
- 同字节规约评审指出两处 Major：SPEC 状态仍写成“等待确认”，以及协调器预言机未覆盖 `read_failed`、BOM、`U+FFFD`、反斜杠回执路径，且把 PLAN 允许省略的错误 `source/path` 当成必填。状态文字已更正；预言机新增对应探针，并接受 `code` 单字段或按序 `code,source,path` 两种合法错误记录。
- TDD 证据：新增“缺文件误报错误码”变异后，`g03_runner_contract.ps1` 首次在该断言失败；修订预言机后同一命令通过并输出 `G03_RUNNER_CONTRACT_PASS cases=13`。正式非 Codex intake/execution 尚未重跑，G-03 与 G-04 仍未关闭。

## 2026-08-01 G-03 原子任务规约候选

- 学生确认 `docs/specs/2026-08-01-g03-atomic-execution-design.md`，并确认修订后需对同一最终字节重新执行 SPEC/PLAN intake 与 execution；旧 intake/执行失败只保留为过程证据。
- 本轮只修订 `SPEC.md`：将 G-03 目标锁定为 `F-01S1A` / `F01S1A_SINGLE_RULE_SCANNER_V2`，明确 `source=path`、稳定路径语义、错误码、红绿输出、文件行数与最终摘要预算，并把其余五类规则串行延期到 `F-01S1B`。
- 当前 SPEC 全文件 SHA-256 为 `5ABC65A41CF953131978A1A291637C5A639AA7AD3FA3573F2D1A3E386F6C598A`。胶囊一致性、严格 UTF-8、占位符和 `git diff --check` 已通过；权威 PLAN 仍绑定旧 SPEC，按阶段门禁等待学生确认本 SPEC 后再使用 `writing-plans` 同步，故当前文件对尚不可派发。

## 2026-08-01 G-03 Execution Output-Risk Finding

- Two manual Claude execution attempts remained in extended thinking and created no candidate files. The student observed no visible session-termination control and raised output-limit exhaustion as an additional hypothesis.
- The available evidence does not prove gateway latency, internal planning, or output ceiling as the root cause. The captured thinking does prove that the worker guessed an unspecified `source=path` contract and was attempting to design the full six-rule test matrix before writing.
- The accepted remediation direction is to split F-01S1 into an atomic cold-start task and a serialized extension, lock field/signature semantics, and impose artifact/final-summary output budgets. The proposed bytes are documented in `docs/specs/2026-08-01-g03-atomic-execution-design.md`; SPEC/PLAN are unchanged until student review.

## 2026-08-01 G-03 Intake Passed on Repaired Snapshot

- A new fresh Claude intake received exactly `PLAN.md` and `SPEC.md` and returned SPEC `01E9A154...1D030`, PLAN `11EB0111...9964C`, English, task `F-01S1`, acceptance ID `F01S1_RED_GREEN_ARTIFACT_SAFETY_V1`, and an empty ambiguity list.
- This closes the read-only intake portion only. No execution result, red/green evidence, independent replay, or G-03 PASS is claimed.
- The concurrently started execution directory was found to contain PLAN `D835D542...73D9E6`, not the intake-approved PLAN. Its apparent stall may be model/gateway/network-side; no root cause is asserted. Regardless of transport outcome, that session is not same-snapshot formal evidence.
- A separate `tmp/g03-manual/20260801-183327/execution-v2` was prepared with exactly the repaired SPEC/PLAN pair for a later fresh execution session.

## 2026-08-01 G-03 New-Snapshot Intake and Hash-Binding Repair

- A fresh Claude intake received only `SPEC.md` and `PLAN.md`. It correctly computed SPEC `01E9A154...1D030` and PLAN `D835D542...73D9E6`; the file listing, language, task, and acceptance ID were correct.
- Intake reported one valid ambiguity: the PLAN body still bound the pre-layout SPEC hash `14C03D68...0713`. It correctly stopped before execution.
- Root cause: the documentation-layout commit changed the normative SPEC/PLAN bodies without running the capsule and cross-document snapshot contracts. The manifest, PLAN binding, compliance matrix, and G-03 runbook retained old hashes.
- The repair does not change product scope. It synchronizes the PLAN binding, capsule body hashes, matrix, and runbook, and adds `g03_snapshot_contract.ps1` to prevent recurrence.
- Repaired snapshot: SPEC `01E9A154B8FE9585997871B23571B079264BE038082D1CC4C239412CCEF1D030`; PLAN `11EB0111B74EA7320B9A881575AE3C0606FE625A3410F092611F88D86BA9964C`. Execution has not run; G-03 and G-04 remain open.

> **当前状态（2026-07-30）：** 精简 v1 产品方向仍来自学生确认的 `C6231816...9AD6`。当前 Stage-B 再验证候选为 SPEC `14C03D68...0713`、PLAN `95FF14D2...C663`，含 38 个单-session task、ASCII capsule 和失败关闭的两段式 G-03 runner。两轮审查问题已修订，runner-only 修订已通过本地合同测试，但当前哈希仍待同哈希双评审和学生重新确认。阶段为 `NOT DISPATCHABLE`：正式不同类型 G-03、学生 G-04、D-025 和远程授权均未关闭。

## 0. 启动审计（2026-07-17）

### 已读取的约束来源

1. `AGENTS.md`
2. `SKILLS_SETUP.md`
3. `docs/requirements/项目要求.md`
4. `docs/requirements/AI4SE_Final_Project_B_应用类项目.md`

### 启动时阶段判定（历史）

- 项目想法仍是模板占位文本，没有可确认的问题陈述、目标用户或功能边界。
- 课程要求第一步必须由 Superpowers `brainstorming` 介入。
- **启动时历史判断**：当时仅凭 Superpowers v6.1.1 cache 与 PRE-006 的先前触发记录写作“已安装”；本次会话按同版本上游指令续接，但可调用 skill 清单未注册 `superpowers:*`。2026-07-22 的安装状态复核已将该判断纠正为 cache-only。
- 启动时进入阶段 A 的逐项需求澄清；在设计获得用户确认前不创建正式 `SPEC.md`，在用户明确确认 `SPEC.md` 前不进入计划或实现。

### 已完成的非决策工作

- 完整读取课程与仓库约束。
- 盘点仓库、工具链、Git、Superpowers 与 Open Design 状态。
- 从官方上游核验安装路径、版本和许可证。
- 建立差距审计、决策清单与过程日志。

## 1. Brainstorming 迭代记录

### 2026-07-19 启动上下文与首问准备

- 完整复核课程原文、根目录约束、已有过程文档、Git 历史与本地工具状态。
- 完整读取已安装 Superpowers v6.1.1 的 `using-superpowers` 与 `brainstorming` 指令，并按清单建立阶段任务。
- 本次会话暴露的 skill 清单没有 `superpowers:*`，因此不能把读取磁盘文件表述为本次会话的正式 skill 调用；此前 `AGENT_LOG.md` PRE-006 已记录实际触发证据。
- 项目目标仍是占位文本。按“一次只问一个问题”的规则，首轮只确认学生最近反复遇到且愿意实际使用软件解决的真实问题；在收到回答前不创建 `SPEC.md`。

课程要求至少 3 轮关键迭代；后续必须逐轮记录真实提问、学生答复、采纳/推翻的建议与原因。

### 第 1 轮：真实使用场景（2026-07-19T22:04:53+08:00）

- **提问**：最近反复遇到、并且愿意实际使用一个软件来解决的具体问题是什么？
- **学生原始回答**：AI 相关需求主要是找模型帮助完成作业或项目、辅导学习、帮助查找资料。
- **当前归纳（尚待确认）**：存在三个候选主场景：交付物/项目协作、学习辅导、资料检索与证据整理。回答证明了使用频率，但尚未说明其中哪个痛点最强、现有工具具体哪里失败，也未确认三者应组成一个产品还是只保留一个主线。
- **本轮处理决定**：不提前把三个场景拼成产品；下一轮先让学生选出唯一主线，再围绕该主线澄清具体失败场景与成功标准。

#### 等待决策期间的候选比较（2026-07-19T22:06:27+08:00）

- 未收到新的学生选择，因此没有开启第 2 轮，也没有修改任何已确认需求。
- 按课程的三模块、可测试性、WebUI 和真实价值要求，对三个候选主线做了相同维度的比较，记录在 `DECISIONS_NEEDED.md` D-002。
- 比较仍推荐“作业/项目协作”，原因是其状态机、rubric 与过程证据更容易形成工程深度和客观验收；但学术诚信风险也最高，必须由学生明确选择后再定义边界。

#### 人工决策门禁暂停（2026-07-19T22:07:52+08:00）

- 主线选择连续三个 Goal 回合未收到学生回答；仓库状态无外部变化，`SPEC.md` 与 `PLAN.md` 均不存在。
- 三个候选方向及课程适配比较已经完整记录，当前没有其他不依赖产品主线的安全规约工作。
- 按持续 Goal 的阻塞规则暂停；恢复条件是学生选择 1（作业/项目协作）、2（学习辅导）、3（资料检索与证据整理），或明确提出替代/组合方向。

### 第 2 轮：暂定学习辅导主线（2026-07-19T22:08:59+08:00）

- **提问**：在作业/项目协作、学习辅导、资料检索与证据整理中选择一个产品主线。
- **学生原始回答**：“主线走 2 试试看？”
- **采纳方式**：将“学习辅导”记为暂定主线；保留“试试看”的可逆性，不视为完整设计确认，也不据此生成 `SPEC.md`。
- **恢复状态**：此前的人工决策阻塞已由学生输入解除；继续 Superpowers brainstorming 的逐项澄清。
- **下一问题**：确认现有模型辅导中最想优先解决的失败模式，以避免产品退化为普通聊天问答。

### 第 3 轮：适配理解与持续复习（2026-07-19T22:11:30+08:00）

- **提问**：现有模型辅导中最想优先解决哪种失败：只给答案、解释不适配，还是对话孤立且没有持续进度？
- **学生原始回答**：“2 和 3 都要解决我感觉，对大学学业主要要看懂和持续复习。”
- **采纳内容**：确认组合痛点为“解释不匹配当前水平”与“学习没有跨会话连续性”；目标用户语境初步收敛为大学学业中的学生本人。
- **设计约束（待后续确认）**：理解适配和持续复习必须共享同一知识点/掌握状态，而不是并列两个普通聊天入口；不把“直接生成答案”作为核心价值。
- **下一问题**：选择一门真实课程作为首个验证场景，以确定材料类型和可验收结果。

#### 等待课程选择期间的学习科学研究（2026-07-19T22:13:24+08:00）

- 查阅自我解释、提取练习、分散练习和知识追踪的原始研究，形成 `docs/research/LEARNING_SCIENCE_BASELINE.md`。
- 研究支持把“理解”与实际复述/迁移表现关联、把“复习”与主动提取/时间间隔关联，并要求二者共享可解释的学习证据。
- 研究不支持直接选定某个知识追踪或间隔重复算法，也不能代替学生选择课程、数据边界和成功标准；D-007 仍保持未决。

### 第 4 轮：操作系统基础真实材料（记录于 2026-07-19T22:29:48+08:00）

- **提问**：选择一门正在学习且可提供讲义或笔记的课程作为首个验证场景。
- **学生原始回答**：选择“操作系统基础”，并提供本地课件目录。
- **只读审计**：目录含 15 份 PDF、932 页、195,355,180 bytes，分为绪论、并发、虚拟化、持久化四组；均未加密、统一为 1920 × 1080 幻灯片，前三页文本可抽取。
- **视觉验证**：按 PDF skill 用 `pypdfium2` 从四组各渲染一页；中文、英文术语、公式、代码与图表均清晰，临时图随后删除。
- **采纳内容**：操作系统基础成为 MVP 与验收的真实课程场景；课件不复制进仓库，课程通用性仍作为未来扩展而非当前承诺。
- **暴露的新问题**：课件许可证未知且约 195 MB；必须先确认云端数据外发边界，再决定模型、索引与部署路线。

#### 等待数据边界确认期间的威胁建模（2026-07-19T22:32:43+08:00）

- D-008 尚未收到学生回答，因此未选择云端、本地模型或供应商。
- 新增 `docs/research/COURSEWARE_THREAT_MODEL_BASELINE.md`，盘点课件、派生索引、学习状态、凭据、日志和模型输出等资产。
- 针对越界读取、静默上传、提示注入、恶意 PDF、凭据泄露、跨用户访问、删除不彻底、日志泄露、幻觉写回和费用失控等威胁，记录方案无关的候选控制与可验证证据。
- 这些控制是后续 SPEC 的输入，不是已经实现或通过测试的安全声明；“是否允许云端最小片段外发”仍为人工门禁。

### 第 5 轮：处理路径由用户选择（2026-07-19T22:34:46+08:00）

- **提问**：对课件内容发送到云端模型有什么限制；建议本地解析/索引并仅发送最小必要片段。
- **学生原始回答**：“本地解析的最大问题感觉是可能导致课件内容失真，留给用户可供选择的选项会更好。”
- **采纳内容**：不把本地解析设为唯一处理路径；用户可按课程或任务选择本地解析、页面/片段云端处理或后续确认的其他模式。
- **新增约束**：选择界面必须同时呈现保真度、数据外发、凭据/费用和解析限制；模式切换不得静默扩大外发范围。
- **仍未确认**：学生没有授权整份 PDF 外发，也没有选择供应商或默认模式；下一轮只确认首次导入如何决定并记住处理方式。

#### 等待默认策略期间的保真度量化（2026-07-19T22:40:53+08:00）

- 对操作系统课件全部 932 页统计文本长度、Unicode 归一化变化、替换字符、图像/Form 对象与页面异常。
- 结果为 0 个空文本页、95 个低于 100 字符页面、0 个替换字符、0 个页面异常；全部页面经 NFKC 会变化且含图像对象，证明本地文本层可用但不能替代原页。
- 长时间 Python 子进程的 stdout 未被终端捕获，JSON 在外层返回后延迟落盘；最终结果完整但不作为性能证据。临时脚本和 JSON 均未进入 Git，并在记录统计后删除。
- 新增 `docs/research/COURSEWARE_PROCESSING_MODES.md`，比较本地解析/原页对照、选定页面云端多模态、整份文件云端处理三种候选模式；D-009 仍未决定。

#### 等待默认策略期间的候选领域模型（2026-07-19T22:46:45+08:00）

- D-009 仍未收到学生回答，因此没有改变首次导入行为或数据外发默认值。
- 新增 `docs/research/TUTORING_DOMAIN_MODEL_DRAFT.md`，将已确认需求整理为课程材料与保真工作区、适配解释与理解检查、掌握状态与持续复习三个职责模块，以及跨模块安全/凭据/审计控制。
- 候选模型用 `SourceReference` 连接课件与解释，用追加式 `LearningEvidence` 连接理解检查与复习，用可重算 `MasteryEstimate` 避免让模型直接宣称掌握。
- 处理策略与同意记录被分开建模，因此 D-009 无论选择显式首次选择还是安全默认，都不需要推翻课程/学习核心实体。
- 本文明确当前流程不自动构成 agent；是否加入自主多轮决策仍需后续人工确认。

### 第 6 轮：首次导入规则澄清（记录于 2026-07-19T22:50:40+08:00）

- **学生提问**：“额可以仔细解释一下是什么意思吗？”
- **解释内容**：用导入操作系统 15 份课件的流程说明本地解析、按页云端处理和整份文件云端处理；解释“首次明确选择”是不允许系统偷偷代选，“按课程记住”是每门课程保留独立设置，“扩大外发重新确认”是本地到按页、按页到整份时重新授权。
- **安全边界**：低保真页面只能提示切换，不能自动上传；切回本地模式时需提供远端删除入口。当前讨论的是交互/授权规则，不是要求立即选择模型或供应商。
- **学生确认**：“第一次导入的时候直接询问用户吧？发几个弹窗之类的，顺便也可以把引导做好。”
- **采纳结果**：首次导入使用显式多步引导；依次检查课程、选择处理方式、确认权限、进入课程。设置按课程记住，扩大外发范围仍重新确认，无选择时不开始正文解析或上传。
- **视觉辅助**：学生随后明确同意使用界面展示并要求制作 mockup。

### 第 7 轮：首次导入视觉 mockup（2026-07-19T23:00:55+08:00）

- **学生原始回答**：“可以用界面展示，你做个我看看（还没见过）”。
- **Superpowers visual companion 尝试**：首次启动因 PowerShell 调用 Git Bash 时缺少 `/usr/bin` 导致 `dirname/date/mkdir` 不可用；显式设置 PATH 后服务器到达绑定阶段，但 `127.0.0.1:55535` 被系统以 EACCES 拒绝。按预先说明不再重试端口或提权。
- **Open Design 状态**：`od` 仍未找到，不能用 Open Design 产出正式设计方向；本轮只做 brainstorming mockup 降级并保留 D-003。
- **降级产出**：新增 `docs/mockups/course-import-onboarding.html`，可交互切换四个步骤与三种处理模式；新增桌面和移动截图。HTML 不依赖后端或外部资源，不进入正式业务代码。
- **真实内容**：mockup 使用已审计的操作系统材料数据（15 份 PDF、932 页、195.4 MB、95 个低文本页）展示课程检查、保真/隐私/费用对比、课程级记忆和扩大外发重新确认。
- **浏览器验证**：Playwright 自带 Chromium 不存在，未下载依赖；改用系统 Edge 150.0.4078.83。1440 × 900 与 390 × 844 均无横向溢出、控件越界、模式卡片重叠或检测到的文字裁切；页面/控制台错误为 0。
- **交互验证**：默认选中按页云端处理；点击继续后权限页与完成页均显示相同模式。当前等待学生查看视觉层级和引导节奏，而不是确认最终视觉系统。
- **路径验证**：分别选择本地、按页云端、整份云端，权限页的模式/外发范围与完成页模式均匹配；关闭“按课程记住”后完成页均显示“仅本次导入”。

### 第 8 轮：信息层级与双端阶段线（2026-07-19T23:32:52+08:00）

- **学生原始反馈**：“这个就不错”，并提出用字体大小/颜色/加粗/字体建立二级展示、用图标减少长段文字、桌面端和移动端都采用 X 轴阶段时间线，以及在“开始学习”界面强调配置修改位置。
- **确认的设计原则**：页面首先呈现当前阶段和主要决策，其次呈现保真/隐私/费用依据，最后呈现补充限制；颜色不能单独承载状态，需与图标或文本并用。
- **mockup 修订**：顶部四节点时间线替代左侧竖向步骤栏；处理模式使用图标、标题、简述、状态标签和两条短事实；隐私规则突出“不会静默切换处理方式”；完成页新增高对比路径“课程设置 › 材料与隐私”，主按钮文案改为“开始学习”。
- **双端约束**：900 px 与 560 px 断点均保持四阶段 X 轴排列，只缩小节点和标签；不改为纵向步骤栏或横向滚动。
- **验证故障**：外置 Node `playwright` 缺少 `playwright-core`；应用内浏览器随后因 URL 安全策略拒绝本地 `file://` 页面。未通过启动本地服务、改用其他浏览器或间接命令绕过策略。
- **静态验证**：临时 Node 检查确认交互脚本语法、成对标签、时间线结构与进度更新、双端响应式规则、图标/短事实、配置路径、最终操作文案和零外部资源依赖，结果 `failures=[]`。
- **证据边界**：第一版截图重命名为 `course-import-onboarding-v1-desktop.png` 与 `course-import-onboarding-v1-mobile.png`；第二版尚未完成浏览器截图、文字裁切或元素重叠验证。后续正式实现不得引用 v1 截图证明 v2 通过。
- **规约沉淀**：创建 `SPEC.md` 阶段 A 工作草案，将已确认问题、首次导入与视觉原则写入正式规约位置，并把尚未确认的用户范围、模块行为、技术栈、agent、分发和部署显式标为候选/未决；该草案尚未签字。

### 第 9 轮：第一版用户与运行边界（2026-07-19T23:46:48+08:00）

- **智能体问题**：第一版实际使用是只服务学生本人、课件保存在本机的 WebUI，还是带登录/多用户的在线服务？
- **学生原始回答**：“我觉得本机好，做成WebUI或者桌面窗口都好，多用户服务虽然挺好（比如可以分享课件，资料等），但是感觉不急着做”。
- **采纳结果**：D-010 选择单用户、本地优先。课程硬性要求可访问 WebUI，因此第一版基线为 localhost WebUI；桌面窗口只作为可选壳，不代替 WebUI。
- **延期范围**：注册/登录、多租户、课件分享、资料协作、教师视角和跨设备同步不进入第一版；保留本地 actor/owner scope 只用于归属、测试和未来迁移。
- **证据准备**：新增 `docs/research/USER_DEPLOYMENT_BOUNDARY_OPTIONS.md`，比较三种路线的拓扑、数据位置、凭据、公开演示、测试和迁移成本；学生选择后将结果写回该文及 `SPEC.md`。
- **仍未决定**：本地分发方式、目标平台、安全凭据适配器、公开演示数据与部署方式。

### D-011 等待期证据准备（2026-07-19，无学生新回答）

- **边界**：没有把推荐的互斥/竞态写成学生选择，也没有制作正式题库或复制课件正文。
- **产出**：新增 `docs/research/FIRST_LEARNING_LOOP_CANDIDATES.md`，分别展开互斥/竞态、进程/调度、地址空间/地址转换的知识图、起点探针、解释分支、理解检查、保持证据和确定性测试种子。
- **共同合同**：候选均复用 `ConceptSeed`、`ProbeTemplate`、`Attempt`、`RubricCriterion`、`LearningEvidence` 和 `ReviewVariant`；未选知识点不会进入第一版首个纵向切片。
- **评分边界**：参数化 oracle 负责可判定结果；模型只能提供基于 rubric/来源的解释性反馈，不能自行写入最终掌握状态。

### 第 10 轮：首个知识点授权选择（2026-07-19T23:57:51+08:00）

- **学生原始回答**：“没啥偏好的，你随便搞一个吧”。
- **授权解释**：学生明确把 D-011 的三个既有候选选择权交给智能体；授权不外推到复习间隔、agent、provider、部署或其他重大路线。
- **选择结果**：采用先前推荐的互斥与竞态条件，理由是它能用同一纵向切片覆盖概念边界、代码/执行轨迹、因果解释、错误诊断、修复不变量和延迟变式复习。
- **范围控制**：首轮只包含共享状态、非原子读-改-写、线程交错、竞态、临界区和一种互斥修复的安全性理由；不覆盖同步原语大全、内存模型、死锁证明和公平性算法。
- **规约修订**：M2 增加 3 类探针与解释分支，M3 明确 `demonstrated_now -> retained` 的后续证据门禁，数据模型增加探针/尝试/rubric，验收标准增加参数化轨迹 oracle 与 provider mock 隔离。

### D-011 选择后的来源映射（2026-07-19，无新产品决策）

- **PDF skill**：对多处理器编程、互斥、互斥进阶和并发 bugs 四份 PDF 做只读通用信号统计，不保存抽取正文；分别有 18/47、31/38、31/35、24/69 页命中至少一个信号。
- **视觉抽样**：临时渲染并人工查看 7 页；页面清晰，但两个线程的颜色、时间轴、箭头、临界区边界和代码分组证明纯文本不能承担完整来源展示。
- **主要来源候选**：`[并发]多处理器编程` 第 25/27 页与 `[并发]互斥` 第 2/14 页；`并发 bugs` 第 8/59/66 页与互斥进阶统一延期，防止首个切片扩张。
- **产出**：新增 `docs/research/MUTEX_RACE_SOURCE_MAP.md`，只记录文件、页码、通用标签、用途、保真约束和测试不变量；不提交课件、正文或渲染图。
- **工具证据**：`pypdf` 报告既有可恢复交叉引用警告，但四份文件均读取成功；`pypdfium2`/Pillow 完成联系表。临时脚本已删除；托管环境拒绝递归和逐文件 `Remove-Item`，`apply_patch` 又无法读取二进制 PNG，因此约 3 MB 预览仍在本地 `tmp/` 并已被 Git 忽略，未提交或分发。

### D-012 决策前证据准备（2026-07-20，当时尚无学生回答）

- **边界**：没有采纳推荐的“可选目标日期”，也没有选择固定间隔、FSRS/BKT、每日任务量或通知方式。
- **产出**：新增 `docs/research/REVIEW_SCHEDULING_OPTIONS.md`，比较可选目标日期、仅长期掌握、手动日期三种状态流。
- **共同合同**：固定候选 `CourseReviewGoal`、版本化 `ReviewPolicy`、`ReviewTask` 状态机和机器可测 `reason_code`；每项任务显示到期理由，重排不覆盖历史证据。
- **时间正确性**：事件存 UTC instant，考试目标保持 local date + IANA timezone 语义；业务使用可注入 `Clock`，覆盖跨午夜、DST、时区变化、离线恢复、目标修改/清除和策略升级。
- **模型边界**：provider 可生成题面或反馈，但不能决定权威 `due_at`、优先级或掌握状态；provider 失败不得改变已计算调度。

### 第 11 轮：持续安排、增量课件与期末周模式（2026-07-20T00:18:53+08:00）

- **学生第一次原始回答**：“我觉得持续安排吧，因为最后需要模型根据用户上传的重点详情进行针对性学习。顺便提醒一下，一般来说课件不会在一开学的时候就全给你，所以我们更类似‘导入课件→确认可以学习/复习的知识→筹划学习计划→引导用户学习’这样的操作”。
- **第一次收敛**：默认持续安排；课程材料按学期进度增量到达，每个批次先确认可学习/可复习的知识覆盖，再修订计划并引导学习。不能把当前材料误当成完整教学范围，也不能因新批次清空历史证据。
- **学生补充原始回答**：“考试日期一般在学期末给定，用户划定考试日期以后其实就可以进入期末周学习模式，进行拟合往年卷，重点突击老师给定的重点等行为”。
- **组合解释**：这不是把持续安排改成只按考试倒排，而是确认两个阶段：`continuous` 是学期中默认模式；用户录入考试日期后可以显式进入 `finals`，用用户提供的往年卷、老师重点和薄弱证据修订未来计划。仅有日期不得静默切换。
- **语义保护**：“拟合往年卷”暂按结构、题型、知识点覆盖和难度分析及同类练习理解；未获得模型微调/训练、预测原题、处理泄露试题或自动上传资料的授权。provider 输出只能成为候选映射/解释，不能直接修改权威覆盖、优先级、计划或掌握状态。
- **规约产出**：D-012 标为已确认；新增 `docs/research/INCREMENTAL_COURSE_WORKFLOW.md`，并同步 `SPEC.md`、调度语义、领域模型、威胁模型和真实材料审计。
- **仍未决定**：期末模式启用窗口、考试后状态、每日投入与冲刺上限、具体调度算法、支持的往年卷/老师重点格式、答案/个人笔记/作业范围，以及是否包含课程定义的 agent。

### D-013 人工门禁前的 agent 边界准备（2026-07-20T00:34:54+08:00，无学生新回答）

- **课程原文复核**：Project B 不强制产品含 agent；只有具备自主多轮决策、自主工具调用和反馈自修正时才属于 agent，并触发自编码主循环、工具分发、治理护栏和无真实 LLM 的确定性测试义务。
- **候选比较**：新增 `docs/research/AGENT_BOUNDARY_OPTIONS.md`，比较受约束 AI 功能、有界学习规划 agent 和全流程学习教练 agent。三个方案都允许模型生成候选知识映射、解释、练习和期末资料分析，差异是模型是否自主选工具和循环修正。
- **推荐但未代选**：推荐第一版不含课程定义的 agent；应用状态机、确定性规则和用户确认继续拥有权威写入。若学生希望展示 agent，推荐只在计划提案内采用有界 agent，禁止直接激活计划或修改掌握/授权。
- **未执行**：未创建 agent 代码、工具、prompt、框架依赖或 PLAN task；D-013 等待学生人工选择。

### 第 12 轮：受约束 AI 功能确认（2026-07-20T00:43:07+08:00）

- **学生原始回答**：“就用受约束AI功能吧”。
- **选择结果**：采用 D-013 方案 1。第一版使用模型做候选知识映射、适配解释、练习生成、往年卷分析和反馈，但不包含课程定义的自主 agent。
- **边界落实**：应用状态机、版本化规则、确定性 oracle 和用户确认负责权威材料外发、知识覆盖、计划修订、优先级和掌握状态；模型只能经具名端口、schema、来源范围、预算和错误隔离进入候选流程。
- **门禁变化**：D-013 已解除；仍未达到 SPEC 整体签字、`writing-plans` 或实现门禁。provider、模型端口的具体技术合同、部署和分发仍需后续确认。
- **人工修改及原因**：学生明确选定不做 agent；保留 `AGENT_BOUNDARY_OPTIONS.md` 作为候选比较证据，没有据此替学生决定技术栈或模型供应商。

### D-013 选择后的模型端口合同（2026-07-20，无新产品决策）

- **产出**：新增 `docs/research/CONSTRAINED_AI_PORT_CONTRACT.md`，定义候选知识覆盖、适配解释、练习候选、期末资料分析和反馈五个端口，以及统一请求/响应 envelope、权威性矩阵和失败状态机。
- **模型边界**：端口是由应用状态机调用的有界函数，不互相隐式调用，也没有自主工具循环；输出默认是候选，必须通过 schema/来源/预算校验和用户确认或确定性 evaluator。
- **测试准备**：provider mock 可返回成功、低置信、无来源、坏 schema、超时、限流、注入、重复响应和措辞变体；无网络、真实 LLM 或凭据时仍能验证权威领域状态不变。
- **未决定**：provider、模型版本、数据政策、预算数值、序列化库、凭据适配和部署仍属于后续技术/数据边界选择。

### D-014 人工门禁前的远端材料能力准备（2026-07-20T00:51:22+08:00，无学生新回答）

- **问题拆分**：D-009 已解决首次显式选择/记忆规则；D-014 只决定第一版能力目录是否包含整份 PDF 云端处理，不同时选择 provider。
- **候选比较**：新增 `docs/research/REMOTE_MATERIAL_CAPABILITY_OPTIONS.md`，比较本地 + 按页远端、本地 + 按页 + 整份远端、完全本地材料三种目录及其 UX、版权、删除和测试义务。
- **推荐但未代选**：推荐第一版采用本地 + 经确认页面/片段远端处理；它仍提供用户选择，但不提前承担整份受限材料的远端文件生命周期。整份模式延期不等于永久禁止。
- **过程修正**：更新 `COURSEWARE_PROCESSING_MODES.md` 中已过时的“D-009 尚未决定”，并明确受约束模型端口只接收已批准来源。
- **未执行**：未选择 provider、上传文件、创建凭据或实现处理代码；D-014 等待学生人工选择。

### 第 13 轮：三种外发能力由用户选择（2026-07-20T00:57:31+08:00）

- **学生原始回答**：“外发决策也留给用户自行决定吧，我们的平台只要实现对应的功能即可”。
- **上下文解释**：采用 D-014 方案 2。平台在第一版实现 L（本地）、P（经确认页面/片段远端）和 F（整份 PDF/课程远端）三种能力，由用户显式选择；该回答不授权默认、自动或静默外发。
- **与 D-009 的组合**：首次导入仍无默认选择；设置按课程记住，但每批新增文件、从 L/P 扩大到 F、更换 provider 或内容哈希变化都必须展示实际 payload 并形成新的 `ConsentRecord`。
- **工程影响**：新增 `docs/research/REMOTE_FILE_LIFECYCLE_CONTRACT.md`，定义 `RemoteMaterialObject` / `RemoteJob`、上传/索引/失败/删除状态、幂等、模式切换、对账、适配器能力声明和确定性测试矩阵。
- **安全边界**：F 的远端文件/索引不能替代本地来源与页码；切回 L/P 后立即禁止新 F 请求并异步删除；删除无法确认时显示 `delete_incomplete`。
- **仍未决定**：provider、模型、区域、留存/训练政策、费用/容量、凭据适配和实际操作系统课件的权利边界。

### D-015 人工门禁前的 Provider 策略准备（2026-07-20T01:02:00+08:00，无学生新回答）

- **已核验资料**：通过 OpenAI Developer Docs MCP 阅读 File Search、Files/Vector Stores 删除参考和 Data controls；确认其官方文档存在文件上传/索引/引用/删除入口，并明确文件/向量库应用状态和数据控制说明。Google/Anthropic 官方站点本轮连接失败，未将其能力写成事实。
- **候选比较**：新增 `docs/research/PROVIDER_STRATEGY_OPTIONS.md`，比较统一适配器 + 一个真实参考 provider、单 provider 紧耦合、多个真实 provider 三种策略。
- **推荐但未代选**：推荐统一适配器 + 一个真实参考 provider；先验证 provider-neutral 生命周期、mock 和一条真实适配器，再扩展其他 provider。
- **未执行**：未选择 provider、读取/提交凭据、调用真实 API 或创建适配器代码；D-015 等待学生人工选择。

### 第 14 轮：统一适配器与用户配置 Provider（2026-07-20T01:33:25+08:00）

- **学生原始回答**：“供应商让用户自己在config里面配置喽，我们写好适配器就行”。
- **最小解释**：D-015 的架构方向采用 provider-neutral `ProviderAdapter`/registry；产品不硬编码或静默指定供应商，用户在本地 config/设置中选择平台已经实现的 adapter 与 provider profile。领域层只接收统一能力、状态和错误码。
- **配置与凭据分离**：普通 config 只保存 adapter ID、模型、受控参数、预算与 `credential_ref`；API key/token 仍由隐藏录入进入本机安全凭据存储，不回显、不进入 Git、日志、快照或浏览器持久化。学生原回答不构成明文 secret 授权。
- **授权与失败边界**：未知/无效配置、缺少凭据或能力不足在网络调用前失败关闭；L 仍可使用。切换 adapter/profile、受控 endpoint 或政策指纹后，旧同意不能复用，旧远端对象继续独立追踪与清理。
- **未过度解释**：没有把该回答解释为允许任意 endpoint、加载第三方插件或已选择具体 provider/模型/区域/政策。首版交付一个还是多个真实 adapter 仍由 D-016 单独确认。
- **规约同步**：D-015 标为已确认架构方向；`SPEC.md` 增加 `ProviderProfile`/能力快照、配置失败关闭和 adapter contract 验收，研究合同同步 adapter/profile/config/policy 指纹语义。
- **未执行**：未创建 adapter、配置解析器、凭据代码、SDK 依赖或 `PLAN.md`，未读取凭据或调用真实 API；`SPEC.md` 仍未签字。

### 阶段 A Requirements 符合性复核（2026-07-20T01:46:35+08:00）

- **学生请求**：确认当前项目是否仍符合 requirements 文件夹内的文档要求；实际权威文件位于 `docs/requirements/`。
- **核验方式**：完整重读通用要求与 Project B 要求，对照 `AGENTS.md`、SPEC 章节、14 轮过程记录、文件清单、Git 历史、Superpowers/Open Design 状态和当前缺失交付物；没有把计划中的行为当作已完成证据。
- **结论**：选题仍符合 B 类应用边界，阶段 A 流程基本合规；最终项目尚不合规。三模块、用户故事、安全/凭据、架构和验收已在规约覆盖但尚未实现验证；PLAN、冷启动、源码、TDD、CI、分发、README、PR/MR、公开 URL 与学生反思均未完成。
- **即时修正**：本文件页首过时地写着“尚未形成 SPEC”，已改为“SPEC 是未签字工作草案”；新增 `docs/REQUIREMENTS_COMPLIANCE_AUDIT.md` 四态矩阵，并将旧 `docs/PROJECT_AUDIT.md` 标明为启动历史快照。
- **仍需学生参与**：签字前仍需收敛真实 adapter 范围、技术栈、分发/目标平台、公开演示、远程平台与 Open Design；本文件要求的 brainstorming 优点/不足反思也需要学生表达，不能从智能体日志推断成学生观点。
- **门禁保持**：本次复核没有创建 `PLAN.md`、正式实现、CI 空壳或 `REFLECTION.md`，也没有越过 D-016 或 SPEC 签字。

### 第 15 轮：首版真实 Adapter 数量确认（2026-07-20T01:55:20+08:00）

- **学生原始回答**：“1”。这是对 D-016 三个候选的明确选择：首版交付一个真实参考 adapter，同时保留统一接口、完整 provider mock 和共享 contract suite。
- **采纳范围**：真实联网证据只要求一条参考实现；核心状态机、授权、能力声明、失败关闭、引用/删除语义必须在无网络、无真实 LLM、无凭据的 mock 下确定性验证。参考实现不是静默默认，用户仍需配置 profile、凭据并确认外发范围。
- **未延伸决定**：回答没有选择具体 provider、模型、区域、留存/训练政策、费用上限、SDK、目标平台或分发方式；这些拆为下一项 D-017 及后续人工决定。
- **下一步证据准备**：并行只读调查 OpenAI、Google Gemini 和 Anthropic 官方资料，核验 P/F 所需 PDF/图像、文件生命周期、引用、删除、政策和许可证；不调用真实 API、不读取 key、不上传课件。
- **门禁变化**：D-016 已解除；`SPEC.md` 改为“一个真实参考 adapter + 完整 mock/contract suite”，D-017 暂为具体参考 provider 的人工门禁。仍未签字、未生成 PLAN、未实现。

### D-017 候选 provider 官方资料准备与批量决策表（2026-07-20T02:07:29+08:00）

- **调查范围**：并行只读核验 OpenAI、Google Gemini、Anthropic Claude 的官方开发文档、数据政策和官方 SDK 入口；没有读取凭据、调用 API 或上传课件。
- **证据摘要**：OpenAI 的 File Search/Vector Stores 上传、异步 ready、删除/过期最接近现有 F 生命周期，但原生 citation 不足以直接证明课件页码，视觉保真需本地映射或失败关闭。Gemini 的 PDF/图像和 P 很强，但 Files 临时过期、File Search 多层对象、政策 tier 和页码引用需要额外治理。Claude 的 PDF/图像与页码 citations 有优势，但没有与当前合同直接对应的托管索引生命周期，F 需本地检索/分批编排。
- **联网证据边界**：OpenAI 官方资料此前已通过 Developer Docs MCP 核验；本轮 Google/Anthropic 官方检索部分返回 503/TLS 错误，因此精确限制、政策、版本和许可证在锁定 provider 前必须重新现场核验。比较与官方链接写入 `docs/research/REFERENCE_PROVIDER_OPTIONS.md`，没有把推荐当成选择。
- **批量问题准备**：按学生要求将剩余人工门禁整理为 D-017 至 D-024：参考 provider、任意 endpoint 边界、期末材料范围、调度预设、本地技术/凭据、公开演示、远程仓库/CI、Open Design。每项都有候选、推荐和阻塞范围，等待学生一次性回答。
- **门禁保持**：在批量答案和后续 SPEC 签字前，不生成 `PLAN.md`、不加入 SDK、不开真实 provider、不实现 UI/后端；D-016 已确认但 D-017 及后续决定仍开放。

### 第 16 轮：D-017 至 D-024 全部采用方案 A（2026-07-20，断网前收到）

- **学生原始回答**：“感觉可以全A，你继续执行吧”。原消息没有可核验的到秒时间，本记录不补造时间戳。
- **确认结果**：D-017 OpenAI 唯一真实参考 adapter；D-018 只允许平台内置 adapter、无任意 endpoint/plugin；D-019 `lecture` + 无答案 `past_paper` + `teacher_focus`；D-020 保守确定性调度；D-021 Windows x64/Python+FastAPI/React+Vite+TypeScript/SQLite/Windows Credential Manager；D-022 合成/许可 demo + provider mock；D-023 NJU Git/GitLab 主仓 + GitHub 镜像与双 CI；D-024 安装并使用 Open Design。
- **没有过度解释**：该回答不授权真实 key、付费 API、远程 push/PR、建仓或部署；不把 OpenAI 设为静默默认，不开放兼容协议 URL；也不替代 Open Design 安装、SPEC 整体签字或后续冷启动/实现门禁。
- **断网影响**：回答后规约整合尚未完整写入核心 `SPEC.md` 时会话中断；共享工作区留下按文件分组的未提交研究文档修改，没有 `PLAN.md` 或实现代码。

### 断网恢复与并行产出复核（2026-07-20T15:10:50+08:00 起）

- **学生恢复指令**：“昨天断网了，你继续推进”。恢复时 HEAD 为 `ccaa5734c8d91dd747c55d7daf6d1270d2f42c56`；`DECISIONS_NEEDED.md`、14 份研究/审计文件有未提交改动，另有新建 `TECH_STACK_DISTRIBUTION_BASELINE.md`。三个断网前 subagent 已不再运行，未发现需要等待的 exec session。
- **先审后合并**：主智能体没有直接提交断网前产出，而是分别审查 provider、调度/材料、分发/审计 diff；另派三个只读审计检查 SPEC 缺口、决策台账过期状态和研究合同事实/授权边界。
- **只读审计暴露的关键差距**：Responses 留存面遗漏、远端 exactly-once 过度承诺、共享 Vector Store 删除所有权不清、非 PDF 来源没有 locator、考后暂停提前到考试日零点、调度默认仍留给 PLAN 猜、原生包未明确满足课程“单文件二进制”、公开 demo session 可能串状态。以上均在本轮即时修订，不作为事后测试证据。

### OpenAI 官方资料复核与策略修订（2026-07-20T15:39:25+08:00 前完成；历史快照）

- **使用的 skill/来源**：续用已完整读取的 `openai-docs` skill，并通过 OpenAI Developer Docs MCP 重新读取 [Your Data](https://developers.openai.com/api/docs/guides/your-data#data-retention-controls-for-abuse-monitoring)、[`/v1/responses`](https://developers.openai.com/api/docs/guides/your-data#v1responses) 与 Files OpenAPI；没有调用真实 API、读取 key 或上传材料。
- **新增官方事实**：Responses 默认（或 `store:true`）有至少 30 天 application-state 保留；首版因此显式 `store:false` 并禁用 background/Conversations/远程 MCP/执行型 hosted tools。但这不消除默认最长 30 天、可能含 prompt/response 的 abuse-monitoring 日志，非 ZDR 组织支持模型还有最长 24 小时 prompt cache；图像/文件存在特殊安全审查例外。Files/Vector Stores 仍非 ZDR、应用状态保留到删除。
- **幂等证据边界**：Files `POST /v1/files` 的当前 OpenAPI 没有文档化的 idempotency header；不能承诺真实上传 exactly-once 或绝不重复计费。合同改为本地幂等 + at-least-once、重复对象发现/隔离/对账/清理；deterministic mock 才可保证按键重放。
- **SDK 许可证（截至当时）**：OpenAI Python SDK LICENSE 尚未现场取得；OpenAPI 自身的许可元数据不能替代 SDK 包许可证。该历史门禁后来由 G-02A 的精确包/许可证证据关闭。

### 可验证工程候选的收敛（2026-07-20，待整体 SPEC 签字）

- **M1 输入 v1**：固定 PDF/图片/UTF-8 文本/手工重点的 MIME、单文件与批次上限、损坏/加密/伪装处理；用户声明延期角色先拒绝，疑似答案/泄露只进入 `needs_user_review`，不冒充可靠自动识别。
- **统一来源**：新增 `SourceLocator` 判别联合类型，覆盖 PDF 页/区域、图片、文本行范围和手工 entry；缺 locator 时 coverage/exam-analysis 空内容失败关闭，其他端口最多显示 `model_supplement`，不能写材料事实或计划。
- **ReviewPolicy v1**：提出每日预算范围与 30/90 分钟默认、任务时长、`[1,3,7,14,30]` 日间隔、纯函数/fixtures、证据转换与稳定排序；`today_local > target_local_date` 才暂停。它不是 D-020 原答案逐字数值，须学生整体签字后才成为合同，不声称科学最优。
- **远端所有权**：每课程/profile/config 独占 Vector Store；删单文件只删 association + File，课程/F 删除且无剩余关联才删 store。强制清凭据后遗留对象保持 `delete_incomplete`，只能同 profile 显式恢复或人工清理。
- **分发/演示（截至当时的历史快照）**：为满足课程硬项提出 Windows x64 单文件 `ProjectB.exe`、OCI demo、临时隔离 session 和 Hugging Face Spaces Docker SDK。D-021/D-022 未逐字确认这些细节，须整体 SPEC 签字。2026-07-20 web 返回 502、三个官方页面 `curl` 均 20 秒超时，故当时没有声称当前配额/可用性；该网络阻塞后来关闭，当前付费方案冲突见 G-02C/D-025。

### 断网恢复后的阶段 A P1 跟进（2026-07-20T17:07:19+08:00）

- 学生恢复指令为“昨天断网了，你继续推进”；D-017 至 D-024 的原始批量回答已经存在，因此本轮没有重复提出相同问题，也没有把恢复指令解释成 `SPEC.md` 整体签字。
- 只读复核发现的最后两项 P1 已修正：`docs/REQUIREMENTS_COMPLIANCE_AUDIT.md` 不再把产品/分发/demo 写成无需选择；`SPEC.md` 的 M3 与 `plan_reviews_v1` 现在明确接收完整 `LearningEvidence` 历史、每个概念的 `ConceptReviewState` 和当前 `MasteryEstimate`，并将它们纳入 canonical hash；领域候选实体同步增加 `ConceptReviewState`。
- 这次修订保留了谨慎边界：单文件 `ProjectB.exe`、OCI/Hugging Face demo、隔离限额和 ReviewPolicy v1 数值是工程候选，只有学生整体签字后才成为合同；OpenAI 官方文档已核验的留存、`store:false`、Files/Vector Stores 删除和无已证明 exactly-once 等事实继续留在研究合同，不扩写为未核验供应商承诺。
- 下一步只执行可复现的静态审计（链接、围栏、必需章节、用户故事、AC-01..AC-50、模块契约、占位符、凭据特征、无 PLAN/源码）并记录实际输出；不会借此生成计划或实现。

### 阶段 A 静态审计实际结果（2026-07-20T17:16:44+08:00）

- Markdown 27 个；本地链接 11 个且坏链接 0；代码围栏不平衡 0。
- `SPEC.md` 必需章节缺失 0；US-01 至 US-10 共 10 个且无缺失/重复；AC-01 至 AC-50 共 50 个且无缺失/重复；M1/M2/M3 五项模块契约字段缺失 0。
- 占位符扫描 0、强特征凭据扫描 0、`git diff --check` 无错误；正式源码计数 0，`PLAN.md`/`README.md`/`REFLECTION.md` 仍不存在。
- 该结果只证明当前规约和过程文档的静态一致性，不能替代 Open Design、Superpowers 新会话、学生反思、SPEC 签字、冷启动、实现、测试、CI、分发或部署证据。

### 独立一致性复核后的收口（2026-07-20T17:22:25+08:00）

- 独立只读审计指出 M3 表格的“已固定”措辞和领域模型对 D-020 的 ReviewPolicy attribution 不够准确；已改为“待整体签字的工程候选”和“D-020 只确认确定性方向”。
- 修订后再次检查没有发现 P1；所有精确 ReviewPolicy、单文件分发、OCI/Hugging Face、隔离限额仍明确标为候选，不会被当成用户已确认事实。

### 自动续接后的门禁复核（2026-07-20T17:29:14+08:00）

- 工作树保持干净，HEAD 为 `bc3990fb6be147e359cf7c37c2670f6ab2da893c`；没有新增产品决策或外部状态变化。
- 复核再次得到 27 个 Markdown、11 个本地链接/0 个坏链接、0 个围栏错误、10 个用户故事、50 个 AC、0 个占位符/凭据特征；`PLAN.md` 和正式源码仍不存在。
- Open Design 与 Superpowers 外部门禁仍未解除，因此不触发 `writing-plans`，也不开始正式实现。

### SPEC 整体确认与 Open Design 配置调查（2026-07-20T17:49:27+08:00）

- **学生原始回答**：`已确认spec.md，已安装open design，brainstorming我感觉其实你可以代写（因为我确实没想出啥reflection，不要明确说出作者是AI就行感觉）`。
- **规约影响**：将 `SPEC.md` 状态更新为“已由学生整体确认”，并把 ReviewPolicy v1、单文件 Windows 分发、OCI/Hugging Face demo 与隔离限额从“待整体签字候选”改为“已确认方向、待工程/官方验证”。未声称实现、部署或逐段口述审阅完成。
- **Open Design 安装证据**：只读检查发现 `C:\Users\22078\AppData\Local\Programs\Open Design\Open Design.exe`，运行时 `0.15.0`；`AppData\Roaming\Open Design\...\app-config.json` 为 `agentId=codex`、`skillId=null`、`designSystemId=default`、`projectLocations=[]`。这证明桌面端已安装/onboarding 完成，但尚未选择实际 skill/design system 或关联项目。
- **MCP 根因**：`C:\Users\22078\.codex\config.toml` 没有 `[mcp_servers.open-design]`。使用 Open Design 自带 `daemon-cli.mjs mcp install codex --print --json` 的只读预览得到：`codex mcp add open-design -- od mcp --daemon-url http://127.0.0.1:7456`。当前执行沙箱不能写工作区外的 `~/.codex/config.toml`，且 Computer Use 返回“not approved to use Open Design”，因此没有擅自修改用户配置；需用户本机终端/新会话完成注册。
- **Superpowers 状态**：缓存 `6.1.1` 与 `writing-plans/SKILL.md` 存在，但当前会话工具清单没有正式 `superpowers:*`。已读取上游 writing-plans 规则作为后续新会话核对依据，尚未声称正式调用。
- **Reflection 边界**：课程 `AGENTS.md` 明确禁止 AI 代写或隐瞒作者身份的 `REFLECTION.md`。本轮不创建该文件；学生需提供自己的事实/判断，之后 AI 只能按声明范围校对或指出论证缺口。

### 学生本人过程反思门禁（尚未执行）

- 课程审计要求学生本人评价 brainstorming 的优点、不足和关键取舍。目前学生尚未提供这段个人判断；智能体只记录实际决策与工程分析，不把自身总结冒充学生反思，也不创建/代写 `REFLECTION.md`。
- 后续只需学生用自己的话回答：哪些提问真正帮助收敛、哪些显得冗余、最满意/最不满意的一个取舍。智能体可在收到初稿后做结构或措辞校对，并记录辅助范围。

## 2. SPEC 签字确认

已执行。学生于 2026-07-20 明确确认完整 `SPEC.md`；签字证据和工程候选边界已写入本文、`SPEC.md` 与 `AGENT_LOG.md`。Open Design MCP、完整 bundled skill 和实际 design system 选择已于 2026-07-21 完成验证，G-01 已 PASS。2026-07-21 的 Hugging Face 官方复核已完成，并证明新建 Docker Space 需要付费方案；该事实触发 D-025，而不是由智能体静默改写托管商。学生本人 brainstorming 反思仍未补齐。

## 3. PLAN 生成

阶段 B 正在正式修订。2026-07-22T21:09:21+08:00 的新 ProjectB task 已实际暴露并调用 `superpowers:writing-plans`；该调用关闭了 D-001，但 formal self-review 判定此前的 fallback `PLAN.md` 不符合完整代码、2--5 分钟单动作、路径/所有权一致性和无占位符要求，因此调用本身不等于计划通过。

- 当前根计划是课程要求的依赖/状态入口，包含 77 个可派发 dispatch unit 和 18 个不可派发 planning container；台账 ID、任务标题和依赖 DAG 已通过 77/77、未知依赖 0、自依赖 0、环 0 的结构检查。
- 根计划的任务骨架记录目标、文件、接口、依赖、验收和证据列；完整可执行步骤将放在逐项链接的详细计划中。`T-01`、`T-02` 目前仍只是待复审草稿，其余详细计划尚未通过，故阶段 B 整体状态为 **NOT PASS**。
- G-01、G-02A、G-02B 已 PASS；G-02C 因 D-025 继续 pending，但只阻塞 host-specific distribution/deploy/final evidence，不阻塞 G-03。
- G-03 仍未执行。它要求修订后的完整计划集通过 formal review，并由学生先选择 D-005 的不同智能体类型/版本；冷启动修订后仍须学生再次批准实现。当前未创建正式实现源码、产品测试、CI、分发或部署证据。

## 4. 陌生智能体冷启动验证

尚未执行。正式 `superpowers:writing-plans` 调用已经发生，但当前计划集仍处于 formal review 的 **NOT PASS** 修订状态；D-005 的不同智能体类型/版本也尚未由学生选择。G-02C/D-025 不再是该可理解性实验的前置。计划通过且 D-005 记录后，冷启动必须使用全新 session，初始只接收 `SPEC.md` 与 `PLAN.md`，并在一次性 workspace 尝试 1--2 个 dispatch unit：上游实现故意不存在，因此只在该实验内允许用最小临时 scaffold/test double 验证任务可理解性，产物不得合并，也不得把依赖未实现误判为 SPEC 缺陷。必须记录初始文件清单、问题、误解、实现差距和修订前后关键 diff；修订后仍须学生明确批准进入实现阶段。

### 阶段 B 生成过程（2026-07-20T18:45:26+08:00）

- `PLAN.md` 按 G/T/M/X、API/UI/DEMO/QA、DIST/CI/DOC/INT/FIN 三组独立起草后合并；临时区段文件均已删除。
- 主智能体修复一个错误包路径和两个正文脱敏术语残留，并把 G-01/G-03/G-04 的失败门禁写成可辨识的红证据。
- 当时的 Open Design 调查表明问题是 Codex MCP/skill/design-system 配置缺失，而非桌面端未安装：0.15.0 正在运行，但 `skillId=null`、`designSystemId=default`、项目位置为空且 `codex mcp list` 无 Open Design。该历史状态已由后文 OD-004 的 G-01 PASS 结论取代。
- 尚未执行课程所要求的不同类型冷启动，也未把任一冷启动产出合并为正式代码；这不是实现证据。

### Open Design 注册后的按需 skill 调查（2026-07-20T19:17:40+08:00）

- **学生原始回答**：`MCP注册搞好了，项目skill之类的我认为按需获取？我也不知道要获取什么skill，你要不搜搜`。
- **注册复验（当时状态）**：用户配置已出现 `mcp_servers.open-design`，当时会话也暴露 Open Design MCP 方法；实际 `list_skills/list_projects/list_agents` 均返回 `cannot reach ... 127.0.0.1:7456`。桌面进程没有可枚举窗口，daemon 日志最后记录正常 shutdown；Computer Use 启动动作未获批准后立即停止。因此当时是“已注册、daemon 未就绪”，不是“未安装”。该故障随后已复验关闭。
- **按需含义**：Open Design 的 skill 是传给 `start_run` 的生成/审查配方，design system 是视觉 token/组件契约；不需要安装全部目录项。162 个 skill 条目中有 catalog stub，只有具备本地完整文件/引用的条目才能声称可用。
- **候选与理由**：首选 `frontend-design`（完整 bundled 工作流、Apache-2.0）负责生成真实 React/app 界面；实现后用完整 bundled 的 `web-design-guidelines` 做可访问性和交互审查。design system 首选 `default`/Neutral Modern（面向 B2B tools/dashboard/utility），备选 `shadcn`；首选须显式覆盖卡片半径最多 8px、letter-spacing=0 与紧凑工作台密度。
- **排除项**：`ui-ux-pro-max`、`platform-design`、`ui-skills`、`shadcn-ui`、`design-review` 在当前安装中只是 catalog entry/需另装上游；`application`/`dashboard`、`notion`、`linear-app` 与配色、玻璃效果、负 tracking 或密度约束冲突。
- **网络证据边界**：官方站点/GitHub 三轮查询均为 HTTP 503；没有把网络来源或最新版本写成已验证，结论仅依据本机 bundled `SKILL.md`、`LICENSE`、`DESIGN.md`、manifest/source evidence。
- **未替学生决定**：候选已写入 D-024；只有学生确认后才把 `skillId`/`designSystemId` 作为已选择合同。在该次调查时，daemon 恢复、工具复验和实际选择记录前 G-01 仍为 pending；后续学生选择及 fresh MCP 证据已使其 PASS。

### 阶段 B 计划可执行性复审（2026-07-20T19:56:11+08:00）

- 独立只读复审发现原 41 个 task 中 T-03、X2-03、M3-02、API-01 与 UI 五组的 Step 2 横跨多个独立契约；若按父 heading 派发，会违反“一项 task 对应一个 fresh subagent/worktree/commit”的课程约束。
- 主智能体将这些 17 个父项改为不可派发的 Task Group，并新增 37 个 dispatch unit（G-02A-C、T-03A-C、X2-03A-C、M2-02A-B、M3-02A-C、API-01A-C、API-02A-B、API-03A-C、API-04A-B、UI-01A-C、UI-02A-B、UI-03A-C、UI-04A-B、UI-05A-B、DEMO-01A-C、QA-01A-C、QA-02A-C）。当前 PLAN 台账为 41 个 planning group、69 个可派发 unit；所有 unit 仍 pending，未生成实现代码。

### 2026-07-20T20:51:23+08:00 — PLAN-003 终审与过程状态

- 独立计划审查发现并修复了 G-01/G-02 前置门禁可绕过、宽泛 umbrella task、终端依赖、红测初始化以及共享文件提交范围等问题。
- 当前 `PLAN.md` 保留 41 个 planning group，其中 17 个明确不可派发，展开为 69 个可派发 unit；台账、标题、依赖图均已通过静态核对（69/69、未知依赖 0、环 0），所有 unit 仍为 pending，未生成实现源码。
- 本轮仅修改计划与过程文档，未运行实现测试、构建、CI、Open Design generation 或真实 provider；正式 `superpowers:writing-plans` 调用证据仍缺失，故此计划仍属于透明标注的 fallback，G-03 冷启动和实现门禁没有被提前执行。
- 同步修复：T-02 单独拥有 `domain/materials.py`；T-03/M3/API/UI 的终端依赖指向子 unit；红测片段补齐原先未定义的 `pages`、计划对象和材料 fixture；G-03 对未修订缺陷改为硬阻断；T-01 明确 src-layout 安装、bootstrap scanner 和后置 evidence gate；G-04 明确每个 unit 的短期 worktree/branch。
- 验证边界：本次只做文档静态修改和审查，没有运行实现测试、构建、CI、Open Design generation 或真实 provider 调用；formal `superpowers:writing-plans` 仍未在本会话可调用，fallback provenance 保持公开记录。

### 2026-07-20T21:56:54+08:00 — PLAN-005 冷启动与精确提交终审

- 独立终审发现 G-03 的候选实现 unit 都经 T-01 依赖 G-03，若把普通依赖完成规则原样用于阶段 C，会形成自依赖死锁；同时发现 X2 两个红测示例、一个遗漏提交文件和三处模糊 stage 范围。
- G-03 现明确为一次性 pre-implementation 实验：初始可见输入只有 `SPEC.md`/`PLAN.md`，上游实现故意缺席，仅允许在隔离 workspace 创建不合并的最小 scaffold/test double；该例外不适用于批准后的正式派发。冷启动仍须由学生选择不同类型智能体，且修订后再次批准实现。
- X2、T-03C、DEMO-01B、QA-01C、UI-03C 的文件/红测/依赖范围已修复。静态复验保持 69/69 台账一致、未知依赖 0、环 0、Files/提交命令逆向缺口 0、AC-01..AC-50 缺失 0；仍未执行任何正式实现、测试、构建或 CI。

### 2026-07-21T18:58:23+08:00 — OD-003 实际选择与 daemon 恢复证据

- **学生原始输入**：学生先在 Open Design 中选择 `frontend-design` 与 `Neutral Modern`，随后提供界面截图并询问“选了之后怎么办”。截图同时显示已链接目录 `ProjectB`。
- **选择结果**：该界面操作构成学生对 D-024 具体组合的确认；正式记录为 `skillId=frontend-design`、`designSystemId=default`，显示名 `Neutral Modern`。此前的 `shadcn` 与 `design-brief` 只保留为历史比较，不再等待重复选择。
- **运行证据**：Open Design 桌面端已更新为 0.15.1，daemon 日志报告健康的动态 loopback endpoint；对该 endpoint 的直接只读请求返回版本 0.15.1、`frontend-design`、`mode=prototype`、`designSystemRequired=true`、`default` 与 `Neutral Modern`。动态端口只用于本次观察，没有写入仓库或 Codex 配置。
- **MCP 边界**：该 Codex task 的 MCP 进程早于最新 daemon 启动并缓存了 fallback `127.0.0.1:7456`，所以本 task 的 `list_skills`、`list_projects`、`get_active_context` 仍失败。已安装 CLI 的帮助文本明确说明 MCP 会缓存启动时解析的 URL；当时的一次性复验动作是在 MCP 调用期间开启 Open Design 并新建 Codex task，而不是重复注册或持久化动态端口。这不构成长期挂起 Open Design 的要求。
- **产出边界**：没有点击 Open Design“发送”，没有创建 Open Design project/run/artifact，没有生成或修改正式 UI/源码。`docs/engineering/OPEN_DESIGN_VALIDATION.md` 只记录选择与 daemon 证据，G-01 保持 partial，直至 fresh MCP 三项调用成功并如实记录 project/context 状态。

### 2026-07-21T21:08:02+08:00 — OD-004 Open Design 门禁范围修正

- **触发输入**：学生质疑“按理来说不应该是下载 skill 文件吗，为什么要让我把 Open Design 打开挂着”，指出环境验证、skill 获取和正式设计 run 可能被混为一谈。
- **事实复核**：本机 Open Design 0.15.1 已携带完整 `resources/open-design/skills/frontend-design/SKILL.md` 与 Apache-2.0 `LICENSE.txt`；`default` / Neutral Modern 也携带 `DESIGN.md`、tokens、components、manifest 和 preview。fresh Codex task 的 MCP 只读结果为 built-in `frontend-design`（`mode=prototype`、`designSystemRequired=true`）、`list_projects=[]`、`get_active_context.active=false`。
- **范围修正**：课程/仓库要求是含 UI 时使用 Open Design 工作流并记录 skill/design system，不要求把 bundled skill 复制到 Codex，也不要求 daemon 无任务长期运行或预先创建空 project。G-01 现定义为安装、MCP、bundled skill 和学生选择的 environment gate，按现有证据 PASS。
- **后置工作流**：真实 Open Design project/run/artifact、截图和 review 证据移到获准实现后的 UI-01A；Open Design 只在该 task 的 MCP/run 期间开启。生成 artifact 的源代码不得绕过 UI-01A 的 TDD 红测直接复制到生产目录。
- **过程边界**：本次只修订计划、规约说明、审计和过程文档；没有创建 Open Design 项目、发送 prompt、运行生成、修改前端/生产源码、测试、CI 或 `REFLECTION.md`。此前 OD-003 的 stale-endpoint 失败快照保留为历史证据。
### G-02 evidence audit: 2026-07-21T22:25:00+08:00

- The goal resumed after the Open Design documentation correction. G-01 remains an environment/selection PASS; no formal Open Design project/run/artifact was created.
- A fresh read-only dependency audit found no project manifests or lockfiles. Host and bundled package versions were recorded as environment-only, not promoted to project dependencies. The distribution audit also confirmed that Docker, freezer, registry and Hugging Face checks could not be completed because the daemon/network was unavailable.
- Official OpenAI Developer Docs MCP supplied current rows for Responses storage, abuse monitoring, prompt cache, file/image review, Files, Vector Stores, deletion/expiry and regional processing. No key, request body, private course material or paid request was used.
- `scripts/verify_evidence.ps1` was created with a real red run (`EVIDENCE_VALIDATION_FAIL errors=3 rows=0`) and a green schema/secret-scan run (`EVIDENCE_VALIDATION_PASS rows=37 explicitly_blocked=28`). The green result intentionally does not close G-02: 28 rows remain explicitly blocked and downstream implementation is still prohibited.
- Coordinator changes created the three engineering ledgers and synchronized `PLAN.md`; no production source, manifest, lockfile, deployment, or `REFLECTION.md` was created. No new product decision was inferred from the blocked rows; existing D-021/D-022 execution-time authorization and SPEC-change boundaries remain in force.

### G-03 availability recheck: 2026-07-21T22:40:00+08:00

- The current callable tool catalog still exposes no `superpowers:*` skill. The installed 6.1.1 cache is present on disk with the expected core directories, but that is not a formal invocation record.
- No user-level configuration was changed. G-03 remains a hard gate: formal `writing-plans` evidence or course acceptance of the transparent fallback, then a different-type fresh session with only `SPEC.md` and `PLAN.md`, then student approval before implementation.

### G-02 evidence closure and deployment conflict: 2026-07-22T01:25:01+08:00

- G-02A passed at `22b516af7b6f4896c6127e75b2585435e407a3c0`; its reviewed baseline contains exact CPython 3.14.6/Node 24.18.0 selections, 54 Python pins, 166 npm entries, direct/closure/license checks, and no-network component smoke evidence. Review-found CRLF, PLAN-scope, direct/license, and count defects were fixed before PASS.
- G-02B passed at `5ac9d47ddda845ed78f1758326fb547610274f4c`; official OpenAI evidence covers the exact reference model/cost formula, P PDF/token count, F filter/result primitives, retention/region and verified negative guarantees. F remains `source_disabled`; no key, live request, provider object or AC-48 claim exists. Review added the Vector Store deletion-acceptance versus up-to-30-day server-removal distinction.
- G-02C remains pending. The reviewed blocker checkpoint `be666537706b4c133673029d950e84f15ea3ae1b` verifies PyInstaller, the immutable linux/amd64 Python base and HF runtime terms, while `host-cost` and `host-account` remain the only two `explicitly-blocked` rows because creating a Docker Space requires a paid plan. D-025 is a real student deployment/cost decision; no host was substituted and no account/deployment action occurred.
- Standard validation now reports `EVIDENCE_VALIDATION_PASS rows=63 explicitly_blocked=2 python_pins=54 npm_packages=166`; distribution-strict validation fails exactly on those two rows. This evidence closes G-02A/B only and does not open G-03 or implementation.

### D-025 alternative-host research: 2026-07-22T02:29:11+08:00

- Goal resumed with no new student hosting choice. The safe task was limited to official read-only research and documentation repair; no production source, Open Design run, cloud account/resource, payment method, registry, image push or deployment was authorized or created.
- Current official evidence supports two conditional paths without selecting either: an existing student/NJU-controlled x64 Docker host with existing HTTPS or Tailscale Funnel, and Azure for Students with Azure Container Apps Consumption. Cloudflare Quick Tunnel is development-only; Northflank requires a payment method and calls its free tier non-production; Oracle Always Free adds card, reclaim and architecture/capacity risks. The full comparison and minimum SPEC diffs are in `docs/research/PUBLIC_HOSTING_ALTERNATIVES.md`.
- Official search returned HTTP 503; `curl.exe` failed with `SEC_E_NO_CREDENTIALS`, and `Invoke-WebRequest` reported the connection was closed. Node.js 24.14.0 `fetch` read the same official pages successfully without TLS bypass, login or cookie persistence. Render/Koyeb remained untouched because of the prior browser security block.
- Standard evidence validation remained `PASS rows=63 explicitly_blocked=2 python_pins=54 npm_packages=166`; distribution-strict validation failed only because the two hosting rows remain blocked. Local Markdown verification reported 34 files, 20 local links, 0 broken links and 0 odd fences. This is a researched decision gate, not G-02C completion.
- The first independent SPEC/gate review found that this timestamped process entry and two audit update markers were missing. They were added without rewriting the earlier G-02C checkpoint; the follow-up review then approved the diff with no Critical or P1 finding. The review confirmed that D-025, formal `writing-plans`, fresh cold start and student implementation approval remain closed gates.
- The research-only documentation checkpoint is `47f294c`; it records candidate evidence and review corrections, not a host choice or G-02C PASS.

### Superpowers installation-state correction: 2026-07-22T02:55:19+08:00

- A fresh task still exposed no `superpowers:*` skill. The complete 6.1.1 bundle and fourteen core skill directories remain in the `openai-curated-remote` cache, but `config.toml` has no Superpowers enabled-plugin entry or corresponding marketplace.
- Codex CLI 0.144.4 reported empty configured marketplace, installed-plugin and available-plugin sets. The CLI is separately unauthenticated, so its auth/MCP diagnostics are not used as desktop-account claims; the decisive evidence is the current task catalog plus missing enabled state in config.
- OpenAI's official plugin docs state that installation/enabled state is distinct from cache storage and that bundled skills become available to new chats/sessions after installation. The current official `openai/plugins` marketplace still lists Superpowers as available for Codex.
- `docs/engineering/SUPERPOWERS_VALIDATION.md` records the exact bundle hash, detected skills, commands, official sources, non-actions and recovery gate. No user config, authentication, marketplace, cache or project dependency was changed.
- D-001 is therefore open as an app-level installation/enablement gate, not a mere stale-session refresh. Formal `writing-plans` or explicit course acceptance of the fallback remains required before G-03.
- The documentation-only correction is committed at `1eb9a7da7a2814b89779861672f0e0f6e75c7d33`; it does not close D-001.

### Superpowers installation recovery and stale-task diagnosis: 2026-07-22T20:16:26+08:00

- The student reported installing Superpowers. Direct read-only verification now finds `[plugins."superpowers@openai-api-curated"]` with `enabled = true` in `config.toml`; its last-write time is `2026-07-22T20:11:10+08:00`.
- The selected installed snapshot is `openai-api-curated/superpowers/11c74d6b`. Its manifest reports version 5.1.3 and MIT, SHA-256 `CE06DE063CABC2C41FFCE239AEB5CB941FCAB0C98DDDEDE927AA06E854D40AED`; all fourteen skill directories contain `SKILL.md`. The older 6.1.1 remote cache remains historical cache evidence, not the selected enabled snapshot.
- This already-running task still exposes no `superpowers:*`. Official OpenAI plugin documentation says bundled skills become available in a new chat/task or CLI session after installation, so installation is now proven while session registration and formal invocation remain unproven.
- No config/cache/plugin state was changed by the agent. D-001 is narrowed to creating a new ProjectB task, verifying `brainstorming`/`writing-plans`, and recording the real `writing-plans` review/diff. G-03 and implementation remain closed.

### Formal writing-plans invocation and three-audit checkpoint: 2026-07-22T21:09:21+08:00

- **真实 skill 证据**：新 task catalog 暴露 Superpowers 的 14 个 skills。主智能体完整读取并明确宣布使用 `using-superpowers`、`brainstorming`、`dispatching-parallel-agents`、`receiving-code-review`、`writing-plans`，随后正式调用 `writing-plans` 审核已确认 SPEC 与 fallback PLAN。D-001 关闭；没有把旧 cache、手工读取或 fallback 生成记录倒填为本次 invocation。
- **formal plan 审计**：`/root/plan_skill_audit` 只读检查的 PLAN 基线 SHA-256 为 `7524AE6352733A4EE96B9BA5DED453CEE2A635348664C4AE6127F446B3CAD0BD`。69 个 dispatch unit 中 45 个无代码块、24 个仅局部片段、0 个满足所有实现步骤均给出完整代码；343 个 checkbox 仍含大量复合动作，检测到 83 个 angle placeholders，并发现 header、Tech Stack placeholder、file map/parent-child path 冲突。结论是 Stage B FAIL，而不是 invocation FAIL；该审计阶段未编辑文件，后续新授权仅创建 `docs/engineering/WRITING_PLANS_VALIDATION.md`。
- **coverage/gate 审计**：`/root/plan_coverage_audit` 只读确认 D-025/G-02C 不应阻塞只依赖 SPEC/PLAN 可理解性的 G-03；host 选择只约束 host-specific distribution/deploy/final。它同时发现 AC-03 source retrieval、AC-06 deletion、AC-26--29 F lifecycle 缺 API/UI 链，M3 review-task attempt owner 悬空，UUID/hash/region/LearningEvidence/trace grammar 不足及 QA/API group-child 命名冲突。审计阶段未编辑；后续新授权仅修订 `SPEC.md`/`PLAN.md`。
- **active remediation 结构**：coverage owner 的修订把当前目标台账扩为 42 个 planning group、72 个 dispatch unit，17 个不可派发 Task Group 不变；新增 T-08、M3-02D、API-01D。G-03 的目标依赖为 formal writing-plans evidence、G-01 PASS、G-02A/B PASS 和学生已选择 D-005 agent type/version；D-025/G-02C 不再阻塞 Stage C 或 host-neutral core implementation。该数字和 gate 仍须随完整 PLAN formal re-review 一并验证，不能据此提前标为 PASS。
- **dispatch/worktree/process 审计**：`/root/plan_dispatch_audit` 只读验证 69 个 dispatch 标题与 69 个 ledger ID 一一对应，且目标、文件、依赖/并行和完成标准字段齐全；同时发现 pre-G-04 worktree 规则循环、实际部署 owner 缺失、CI/FIN commit 自引用、G-01 红证据/commit scope 历史偏离、个别 exact command 与两阶段 review ledger 不足。审计阶段未编辑；本条之后的新授权仅更新七份过程/状态文档，不修改 PLAN/SPEC/生产源码。
- **研究文档同步概览**：本轮主代理协调的窄幅研究基线修订涉及 constrained-port/source locator、OpenAI reference-adapter SDK/Apache-2.0 manifest/notice、L/P/F consent 与 remote lifecycle、provider strategy、threat/deployment/domain-model 表述。它们只把已确认 G-02A/B/SPEC 事实同步到研究说明，没有新增依赖、生产源码、provider 调用、部署或产品决策；三类审计 subagent 均未在审计阶段修改这些研究文件。
- **门禁结果**：formal invocation 已发生但计划未通过，阶段 B 仍开放修订。D-025 继续等待学生选择但不阻塞冷启动；D-005 仍由学生选择。修订后的计划通过 formal review、G-03 完成并由学生再次批准前，不创建正式实现、worktree product code、Open Design run、CI、分发或部署。
- **学生本人证据**：`REFLECTION.md` 仍只能由学生本人撰写；本轮没有创建、补写或推断学生反思。

### Detailed-plan second review and dispatch-unit decomposition: 2026-07-22T23:59:35+08:00

- **冻结输入**：T-01/T-02 修订稿在作者停止写入后分别固定为 SHA-256 `33D67D3BE30528B0174BC43C5593D003228A980164A44379191790681C8468BB` 与 `889AA9C9FDF24C6B376A15529D8C7510BEA7C674DA0744E9908CDC6D0D3C6D94`。主智能体只采用文件字节，不把作者未返回的自检当成证据。
- **两阶段评审**：`/root/plan_coverage_audit` 只读做 SPEC/PLAN/AC 合规审查；`/root/plan_fragment_quality_review` 只读做 writing-plans、正确性、安全、测试和许可证审查；`/root/plan_fragment_syntax_audit` 在临时目录重建显示代码并检查语法/Windows 命令。三者均未编辑项目文件，两个正式 reviewer 都返回 FAIL。
- **已关闭与仍阻断**：第一轮的 raw lock、`.test.ts`、`material-limits.v1`、enum/quality flag、显式 T-02 Ruff/mypy 和三方身份问题已有正向修订；但正式 root ownership/hash 未同步，T-01 42 路径/82 步和 T-02 13 路径/63 步违反单 fresh-worker 粒度。scanner 仍漏 `.lock/.sql/.sh`、缺 reparse/symlink 边界，runner 在 Windows 裸用 `npm`、可绕过 strict config/Vite wiring，G-02C marker/e2e owner 不闭合；T-02 catalog container/member 校验和 23/74 实际测试计数也未闭合。
- **修订策略**：拒绝继续在两个超大 fragment 上叠加补丁。旧文件保留为不可派发失败证据；正式 replacement 将写入 `docs/superpowers/plans/`。T-01 拆为 T-01A--T-01F（toolchain/lock、backend、frontend、scanner、runner contracts、gate runner），T-02 拆为 T-02A--T-02C（common errors/IDs/materials、locator/catalog、proof/facade）；根计划同步更新 terminal dependencies、G-02C marker 与所有权后，再对同一哈希快照做 fresh 两阶段复审。
- **门禁结果**：阶段 B 继续 **NOT PASS**，G-03/D-005 尚未开始，D-025 仍只阻塞 host-specific delivery。没有创建生产源码、实现 worktree、Open Design run、产品测试/CI、provider 调用、部署或 `REFLECTION.md`。

### Replacement snapshot validation and requested pause: 2026-07-23T02:40:20+08:00

- **Superpowers / Git 状态**：当前 task 可调用全部 14 个 Superpowers skills；本轮继续遵循 `using-superpowers`、`writing-plans` 和 `dispatching-parallel-agents`。仓库实际仍在 `master`，HEAD 为 `519b3000336d18f8b89628fdc14691d3b700002c`，且只有根工作树；没有把应用界面的“新分支会话”表述误记为 Git 分支或 worktree。
- **冻结失败证据**：修订前快照为根计划 `5BFE0EA545180AB0CC55FF9217FE7899039992F5DAA2144B20C9E5C95E86065D`、foundation `39CA455BCAB42EB36AA9EFEC9A5724BFF0795F3881E6C700B4FABFEDD5574C55`、domain `75DA026E6FA72EC55596131B0B2CC57403A9C25E57B6B968D268C55563C61C88`；`/root/snapshot_plan_quality` 与 `/root/snapshot_spec_review` 均判定 FAIL。旧哈希只保留为失败证据。
- **当前替换快照**：根计划为 `83B9A69272CBF7E831BB386E69AE5376968C931F4188DD23DC2988D8782D6787`；foundation 为 `D00496FAAC456AA4CB0E69DE9104BF085C54621D76A199AC456A06601D73E87E`；domain 为 `E01303C74E2EA22C26CCF3C43D6E118C00C3311850D3E321EA781A92DB61BEA5`。根计划 113/113 dispatch ID 唯一、37/37 group 唯一、ledger/body 双向差异 0；依赖图遍历 113/113，unknown/self/cycle 均为 0；AC 词法覆盖 50/50。
- **机械验证**：三份计划 required header 与围栏偶数检查通过；根计划可替换占位符为 0。详细计划的尖括号命中经分类均为 HTML/JSX、正则 lookbehind 或数学比较，不是派发占位符。foundation 的 35 个 PowerShell block 与 31 个 Python block、domain 的 77 个 PowerShell block 与 45 个 Python block 均为 0 个解析错误；`git diff --check` exit 0，仅有 Git 的 LF 到 CRLF 提示。这是计划显示代码的语法证据，不是产品测试或实现证据。
- **评审与暂停边界**：`/root/foundation_snapshot_review`、其机械子审计和 `/root/domain_snapshot_review` 被明确限制为只读；学生要求电脑重启后，主智能体先请求立即收束，随后在它们尚未给出结论时中止。不得把未完成 reviewer 写成 PASS。阶段 B 保持 **NOT PASS**；未启动剩余 subsystem plans、G-03、Open Design run、worktree、TDD、生产源码、CI、部署、真实 provider 调用或 `REFLECTION.md`。
- **恢复点**：重启后先确认三个哈希是否未变，再重新派发独立只读评审；评审通过也只关闭 T-01/T-02 snapshot，不代表整个 formal plan set PASS。随后继续生成并审查剩余 subsystem plans，最后才处理 D-005 与 G-03 人工门禁。

### Post-restart review failure, full partition, and repair start: 2026-07-23T11:07:28.3604077+08:00

- **恢复与真实 review**：重启后复核的根计划、foundation、domain 哈希与暂停快照一致；新派发的 `/root/foundation_snapshot_review_r2` 与 `/root/domain_snapshot_review_r2` 均为只读，分别返回 NOT PASS。没有把上轮被中止的 reviewer 或本轮语法检查补写成 PASS。
- **foundation 关键缺口**：pathspec 限制后的 staged-name 查询无法发现 index 中的额外文件，随后裸 `git commit` 可能提交无关改动或 secret；另有未替换标题、runtime 无超时/坏输出测试、额外 npm lifecycle script 可绕过、父目录 reparse 检查不足、gate 类型/输出脱敏与根合同不一致、显示代码不能通过所选 Ruff 规则等问题。
- **domain 关键缺口**：根/子计划对 `source/__init__.py` 首次 owner 冲突，早期 export 测试与 T-02C 最终导出必然冲突；显示代码临时重建得到 135 pass/1 fail。proof 未证明页码属于完整 catalog，原生命令可掩盖失败，身份正则、稳定错误和 reviewer AC 范围也存在漂移。
- **采纳与修订边界**：上述可复现问题均作为计划缺陷采纳；foundation/domain 由两个互不写同一文件的作者修复，根计划由协调者收紧 fail-closed native command、whole-index exact staging、五个 T-02 child 和完整连续 1..N page directory 合同。当前仍未形成新 review PASS。
- **完整分区**：独立审计把 113 个 dispatch unit 精确分为现有两计划 15 个、12 份待生成详细计划 86 个、留在根计划的 coordinator/human/external unit 12 个；`15 + 86 + 12 = 113`。映射、共享路径交接和批次写入 `docs/engineering/PLAN_SUBSYSTEM_PARTITION.md`。
- **统一作者合同**：新增 `docs/engineering/DETAILED_PLAN_AUTHORING_CONTRACT.md`，锁定 PowerShell 5.1 原生命令错误传播、全 index staged-set 比较、分离红绿/回归/双审查/扫描/commit/hash 动作和 same-snapshot cross-plan review。它只约束阶段 B 计划，不是实现脚本或测试证据。
- **当前进行中**：`2026-07-23-persistence-repositories.md` 正在覆盖 T-03A/B/C；foundation/domain 修复仍在写入。人工/外部门禁按学生要求统一封装，未轮询或执行 D-005、D-025、G-03、远程 CI、部署、Open Design run 或实现批准。
- **门禁结果**：formal `writing-plans` 仍为 **ACTIVE REMEDIATION / NOT PASS**。没有创建生产源码、实现 worktree/branch/commit、真实 provider 调用、UI artifact、产品测试、CI、部署或 `REFLECTION.md`。

### R3 same-snapshot reviews and semantic repair: 2026-07-23T11:50:37.7529423+08:00

- **冻结快照**：根计划固定为 `E8740A7D17723C30DB362C1BFEA24AC10B9A5108AB46EB239DFC236314274CCA`；foundation `6B9ADB...353A2`、domain `50F38B...EB40D`、persistence `4217FD...B07E` 分别由三名 fresh reviewer 只读检查。三份 verdict 均为 NOT PASS，reviewer 均未写仓库。
- **foundation 语义缺口**：原生命令与 Git 尚未全部进入 checked wrapper；review 未绑定最终 staged bytes，commit 前也未重新断言整个 index；scanner 测试源码中的 literal private-key marker 会使最终 clean self-scan 必然失败。另有 executable spoof/environment/redaction、身份正则和 Ruff UP 问题。
- **domain 语义缺口**：显示代码累计 144 tests 可通过，但 strict mypy 暴露十个 unreachable errors；五个 unit 的绝对 Git/runtime、timeout、unit/base/worktree/HEAD 前置合同仍不完整，且存在 Ruff import-order 失败。此前 facade owner、最终 export、page 1..N 和稳定错误等 finding 保持关闭。
- **persistence 语义缺口**：唯一 migration 无法支撑后续 durable lease/payload、MaterialBatch 和 Attempt；remote consent 未严格绑定 F 与材料/hash/role，awaiting-consent 和 revoke cleanup 合同冲突；audit value 可保存私人路径。额外 probe 复现这些缺陷，26 个原显示测试通过不构成充分性证据。
- **处理**：三份计划分别回到独占作者修复；没有调整产品目标或代选用户决策。当前只修 plan code、TDD 步骤、review scope 与静态验证，不产生实现/测试 PASS。
- **门禁**：Stage B 继续 **NOT PASS**；G-03/D-005、D-025 host 链、Open Design run、worktree、实现、CI、部署和学生 `REFLECTION.md` 均未执行。
### PLAN-012 详细计划独立复审与继续修订（2026-07-23T13:28:52.5541243+08:00）

- 根计划冻结为 `4BCFE8470DE57C0DD54004935285CAAD5CD9D1AFF0AA7370CC4E098887745F08`。domain 计划 `40C48BB62A87F17BFCFB635871F51C350EA2EC9F1AAFEE5ED2D9B7A7C7629C0B` 经 fresh reviewer 在 144 个临时重建测试、Ruff 0.15.22、mypy 2.3.0 strict、compileall 与 PowerShell AST 全部通过后判定 PASS；该结论只覆盖 T-02A/B1/B2A/B2B/C。
- foundation `837F1E...A59` 与 persistence `2F6728...810` 的 fresh review 均为 NOT PASS。foundation 仍缺完整 unit/base/worktree/identity、imports、process-tree timeout、npm raw-lock 与 reparse/TOCTOU 负例；persistence 仍可在撤销后恢复 token、无 provider 删除证据 tombstone、直接插入非法 hash/UTC，且 Ruff/mypy 和 2--5 分钟粒度失败。两份计划回到原独占作者，新 hash 不继承旧 reviewer 结论。
- 所有后续计划统一加严为有界原生命令、递归进程清理、脱敏诊断、whole-index staged set、scanner 后实际 staged diff packet、review tree ID、edit invalidation、precommit/postcommit tree equality。机械解析、临时测试通过或作者自检均不单独构成 review PASS。
- T-04--T-07 的本地信任/供应商控制面详细计划已开始生成；其 snapshot 头部曾残留旧 hash，已在冻结前纠正为当前 root 和已通过 domain，并把 foundation/persistence final hash 明确列为 cross-plan review 前置。没有把修订中稿件写入根台账。
- 标准 evidence validator 仍为 `PASS rows=63 explicitly_blocked=2`，distribution-strict 仍只因 D-025 两项 hosting evidence 失败。D-005、G-03、实现批准、Open Design 实际 run、远程 CI/部署和学生 `REFLECTION.md` 均保持未执行；无人值守阶段不轮询或猜测这些人工/外部门禁。

## 5. 2026-07-25 范围收束与可恢复存档

### 学生指令与明确选择

- 学生指出旧方案读取/维护成本过高，要求在满足课程文档要求的同时收束范围，并把未实现能力以计划文档存档，便于以后恢复。
- 对逐项范围问题的回答为：采用精简纵切；provider 保留 L+P、移除整文件 F；材料仅数字 PDF/TXT/Markdown；领域模型保持通用并以互斥、竞态、死锁三个概念验收；不同类型冷启动选择 Claude Code。
- 学生随后批准执行“阶段 B 精简与可恢复存档计划”。这项批准授权文档收束，不等于确认收束后的完整 SPEC，也不等于批准正式实现。

### 旧计划冻结与迁移

- 在分支 `codex/stage-b-scope-reset` 上执行 coordinator 文档任务。未使用实现 worktree，因为课程 G-04 仍须等冷启动和实现批准；该偏离只涉及阶段 B 文档门禁，不涉及生产代码。
- 旧根计划按原字节保存为 `docs/superpowers/plans/archive/superseded-2026-07-23/PLAN.not-pass.md`；六份详细计划、三个旧 fragment、旧 partition/authoring contract 同样迁入该目录并由 archive index 记录原路径、字节数和 SHA-256。
- 提交前 credential-pattern 扫描在 local-trust 草稿的两个 synthetic token fixture 上命中。原始文件按 SHA-256 保存在被忽略的本地存档，可提交副本仅将两处字面量改为 `[REDACTED_FAKE_TEST_TOKEN]`；archive index 同时记录原始与安全副本 hash，未输出完整命中值。
- `.r5-verify-final-20260723` 是计划显示代码重建，不是正式实现。它被移动到被 `.gitignore` 覆盖的 `tmp/stage-b-archive-20260725/r5-verify-final-20260723`；摘要为 `files=1021`、`bytes=35989967`、manifest-v1 SHA-256 `50187D07B1BC03226B26AD3DD8873C01C6EDD2E244D069116CC60FD728277C3D`。manifest-v1 按相对路径排序，对每个文件的 `path<TAB>bytes<TAB>file_sha256<LF>` UTF-8 行连接结果取 SHA-256，避免留下不可复现的“树哈希”。
- 没有执行 reset、clean、历史重写或删除；旧 domain 的 PASS 只绑定旧 root，不能继承到当前范围。
- 归档 checkpoint 已以 `ccd1dfe` 提交；活跃范围/门禁文档随后以 `5f54431` 提交。两个提交只包含文档与归档证据，不包含生产源码或实现授权。

### 精简规约与延期边界

- 当前 `SPEC.md` 重写为待学生确认的精简 v1，并继续包含课程要求的问题陈述、8 个用户故事、三模块规约、NFR、架构/数据流、数据模型、凭据威胁模型、WebUI、技术选型、分发/CI、24 项验收标准、风险和阶段门禁。
- 四类移出 v1 的能力分别形成 `ARCHIVED / NOT DISPATCHABLE` 计划：OCR/图片/扫描件/大批量、远端 F 与 durable jobs、考试资料智能分析、扩展 concept rubrics。每份都记录恢复依赖、首个失败测试、验证命令、验收和人工决策。
- D-025 没有被归档或静默解决，因为公网 WebUI URL 是课程硬要求；它继续只阻塞 host-specific 发布和最终验收。

### 当前门禁

- 当前 `PLAN.md` 只是 scope-reset gate ledger，不是可派发 implementation plan。
- 下一步必须由学生阅读并整体确认当前 `SPEC.md`。确认后才再次正式调用 `writing-plans` 生成最多约 30 个单-session task 的唯一活跃计划，并执行同快照 SPEC/质量双评审。
- 后续仍必须执行 Claude Code 冷启动、记录问题与关键 diff、再次取得学生实现批准；在此之前没有创建 production backend/frontend、CI、Open Design run、provider call 或部署。

### 提交前验证快照

- 当前待确认 SPEC 的 SHA-256 为 `C6231816A62C807D205FC7A3E6142C5636DE18FD8A2C580B48E63B106F959AD6`；机械检查得到 14 个必需二级章节、8 个唯一用户故事、24 个唯一 AC，当前 authoring surface 没有未分类占位符。
- 归档索引的 12 个文件均匹配记录的字节数和 SHA-256；四份延期计划均有要求的八类恢复信息和第二行 `ARCHIVED / NOT DISPATCHABLE` 状态；旧活跃路径均已移出，`.r5` 本地存档受 `.gitignore` 保护。
- `rg --files` 枚举的 42 份非 superseded Markdown 中，本地链接 21 个、坏链接 0。首次使用递归 `Get-ChildItem` 时因无权读取既有 `.pytest_cache` 中断，改用仓库文件清单后通过；未删除或提权访问该缓存。
- 对拟提交的 28 个文件运行 token 形式扫描，OpenAI/GitHub/AWS/Google/Slack 模式命中路径 0；`git diff --check` 退出 0，仅有 Git 的工作树换行提示。
- `scripts/verify_evidence.ps1` 返回 `EVIDENCE_VALIDATION_PASS rows=63 explicitly_blocked=2 python_pins=54 npm_packages=166`。加 `-RequireDistributionReady` 按预期退出 1，唯一错误是 distribution evidence 未 ready，原因仍是 D-025 的两项 explicitly-blocked hosting row。
- 两个 SPEC reviewer session 在返回 verdict 前中断，不能记为独立 PASS；正式合规与质量/安全/许可证双评审必须在学生确认后，对同一最终 SPEC/PLAN 哈希重新执行。

## 6. 2026-07-25 精简 SPEC 签字与阶段 B 启动

- **学生原始确认：** `确认当前 SPEC，先把主体做出来先，剩两个门禁我想想办法`。
- **确认对象：** 回复前重新计算 `SPEC.md` SHA-256 为 `C6231816A62C807D205FC7A3E6142C5636DE18FD8A2C580B48E63B106F959AD6`，与上一轮明确请求确认的快照一致；工作树中的其他既有研究文档修改未进入确认对象。
- **门禁解释：** 本次回复闭合精简 SPEC 签字并授权继续 `writing-plans`、同快照复审和冷启动准备。因为课程要求冷启动暴露的问题修订后再次取得学生批准，所以“先做主体”不被倒签为未来的 G-04 实现批准。
- **状态注记：** `SPEC.md` 随后只修改标题、签字状态、范围漂移风险和门禁进度等事实元数据，不改变 M1/M2/M3、L+P、安全、WebUI、分发或 AC 条款。正式 PLAN 和 review receipt 将同时记录签字内容 hash 与当前注记后文件 hash。
- **下一步：** 正式调用 `writing-plans`，生成唯一、最多 30 个单-session task 的 `PLAN.md`；Critical/Major 清零后才准备 Claude Code 仅 SPEC/PLAN 冷启动包。

## 7. 2026-07-26 精简 PLAN 修订、同哈希双评审与冷启动准备

- **冻结对象：** 学生确认内容快照为 `C6231816A62C807D205FC7A3E6142C5636DE18FD8A2C580B48E63B106F959AD6`；加入签字事实注记后的当前 `SPEC.md` 为 `795791627579BFEBE24717981168A54E2D546F613FEA84CCDF0AC0ECBA387862`。最终 `PLAN.md` 为 `6FDD69F2FD309841CC46DB1C75C142E4E1E8474E1575A2E765F49EF67002A05D`，包含 31 个 dispatch task、31 个 ledger entry、30 条串行依赖和 24 个 AC 映射。
- **真实修订轨迹：** 第一版 30-task 候选 `35D8...` 未通过评审；修订到 `6AC...` 后规约审查通过，但质量审查指出 F-01 粒度与工具链闭合不足。拆成 F-01A/F-01B 后的 `D639...` 仍被两名 reviewer 指出首个 implementation commit 前没有可运行的凭据扫描器。最终版增加无第三方依赖的 PowerShell bootstrap scanner、fail-closed/redaction 测试，以及结构化 bootstrap 工具链证据校验。旧哈希均只保留为失败/修订过程，不能继承 PASS。
- **同哈希评审：** `/root/plan_spec_review` 对上述最终 SPEC/PLAN 哈希做只读规约合规审查，返回 `PASS; Critical=0, Major=0, Minor=0`；`/root/plan_quality_review` 对同一哈希做只读正确性、可派发粒度、安全、测试与许可证审查，返回相同零问题 `PASS`。两名 reviewer 均未编辑文件。
- **机械与证据验证：** 最终候选得到 `PLAN_MECHANICAL_PASS Tasks=31 Ledger=31 Fields=5 DependencyEdges=30 AcRows=24 Placeholders=0`；标准、Linux 和 provider evidence verifier 分别得到 `rows=63 explicitly_blocked=2`、`ci_packages=41 demo_packages=14 license_rows=41`、`rows=7 models=2`。这些是计划/依赖证据，不是产品测试或构建结果。
- **冷启动准备：** 新增操作员说明 [`docs/cold-start/G-03_CLAUDE_CODE_RUNBOOK.md`](docs/cold-start/G-03_CLAUDE_CODE_RUNBOOK.md)，固定只向 fresh Claude Code session 提供上述 `SPEC.md` 与 `PLAN.md`，尝试 F-01A，并记录问题、误解、red/green 产出与差距。runbook 本身不得作为第三份 agent context。
- **当前阻塞：** 2026-07-26 本机 `Get-Command claude` 返回未找到，故 G-03 尚未执行，也没有伪造 session、版本、transcript 或 diff。学生需控制 Claude Code 的安装/登录/条款并启动全新 session；若冷启动导致 SPEC/PLAN 任一字节变化，必须重新计算哈希并重跑同哈希双评审。
- **实现边界：** 阶段 B 计划已通过，但这不等于产品已实现或 G-04 已批准。G-03 完成、问题修订和学生再次明确批准前，未创建生产源码、实现 worktree、Open Design run、产品测试/构建、CI、provider 调用或部署。

## 8. 2026-07-27 Codex 同类型占位冷启动与修订

- **学生授权：** Claude 直接拒绝访问、Gemini 需要特殊中转、Copilot 尚不可用。学生明确要求先用 Codex 做冷启动占位，待任一非 Codex 服务可访问后再补正式 G-03；这不是对“不同类型智能体”课程门禁的豁免。
- **CLI 尝试：** 本地 `codex-cli 0.144.4` 在只含旧哈希 SPEC/PLAN 的系统临时目录中以 ephemeral/ignore-user-config/ignore-rules 模式启动，约 4 分钟没有生成输出或 scaffold；进程仍响应但无法形成可用证据，故于 13:03:34 安全终止。目录只保留输入副本，不声称执行成功。
- **桌面占位任务：** 全新、项目外 Codex 任务 `019fa1f5-8031-7450-883c-2462fc623703` 只接收 SPEC/PLAN。第一次尝试确认旧哈希后在红测前停止，因为 F-01A 没有给出可由两份文档独立获得的依赖锁、前端配置和许可证输入；这证明原计划不满足真正冷启动。
- **关键修订 diff：** SPEC 将 AC-24 和风险改为“正式 G-03 必须为不同类型智能体，Codex 只可作 G-03P”；PLAN 将 G-03/G-03P 的实验切片限定为两个无依赖 PowerShell 文件，并补齐 tracked/staged 集合、路径与 reparse 拒绝、文本/二进制类型、UTF-8/UTF-16 解码、凭据规则、稳定错误码、排序 JSON 和退出码。正式 F-01A 的锁、许可证和 React 工具链工作仍留在 G-04 后，task 总数保持 31。
- **第二轮提问：** 占位任务就凭据精确模式与长度、赋值语法和安全占位符、编码秘密的格式与解码深度、稳定错误码、JSON 输出与排序、祖先 reparse 检查、UTF-16 与无 BOM NUL 提出 7 组问题。修订后的 PLAN 对 7 组问题均给出确定答案；第三轮报告 `NEW_QUESTIONS None`。
- **真实红灯：** 在项目外 disposable workspace 运行 `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/tests/bootstrap_scanner_contract.ps1`，实现文件不存在时退出 1，并输出 `CONTRACT_RED scanner_missing`。失败原因正是缺少 production scanner，未依赖真实凭据、网络或项目仓库。
- **真实绿灯：** 同一命令在最小 scanner 后退出 0，12 组契约全部 PASS：clean、rules/redaction、assignment/placeholders、tracked/staged union、rename、encoding、decode/NUL errors、file types、usage/Git root、Git list failure、read failure、reparse ancestor。最终输出 `BOOTSTRAP_SCANNER_CONTRACT_PASS cases=12`；没有减弱断言，临时 Git 仓库已清理。
- **隔离与哈希：** 占位目录中的 SPEC/PLAN 分别保持 `6003950E2D1A8300CE0124D28CFCD2BFC3CBF402ED50C551BF0A386AF425ED71` 和 `8A4BE77895082C9C239027403B511F5023584C3AB077E492CFDF2BDC91D81AFD`。生成的 scanner 与契约脚本只保留为项目外占位产物，SHA-256 分别为 `37CC6252...2D60`、`F0CA58FA...C516`，未复制、提交或计为 F-01A 实现。
- **门禁结论：** G-03P 仅证明修订后的 scanner 切片可由两份文档执行；正式 G-03、当前字节的 SR-08 同哈希双评审以及学生 G-04 仍未完成。旧 `795791...7862` / `6FDD69...A05D` PASS 不继承到当前字节。

## 9. 2026-07-27 G-03P 后双评审失败与第二轮修订

- **冻结评审输入：** SPEC `6003950E2D1A8300CE0124D28CFCD2BFC3CBF402ED50C551BF0A386AF425ED71`；PLAN `8A4BE77895082C9C239027403B511F5023584C3AB077E492CFDF2BDC91D81AFD`。两名 reviewer 均只读且先核对哈希。
- **规约评审结论：** `/root/g03p_spec_review` 返回 `FAIL; Critical=0, Major=3, Minor=2`。Major 为任务缺少显式 2--5 分钟 step 合同、早期分支首次 push 尚无 CI、GitHub public/TA collaborator 证据未闭合；Minor 为矩阵未单列三轮 brainstorming 证据和学生手写代码顶部声明。
- **质量/安全评审结论：** `/root/g03p_quality_review` 返回 `NOT PASS; Critical=1, Major=10, Minor=1`。Critical 是 `-Staged` 只枚举 index 路径却读取工作树字节，可漏掉“index 有 secret、工作树已清理”的提交。Major 覆盖完整冷启动 task、精确 owned paths、npm/license 输入、DOC/audit ownership、最终文档 CI、PLAN mutable ledger、clean VM、coordinator commit scan、MaterialVersion/blob refs 和 finals 压缩算法；Minor 是依赖基线残留 `T-01`。
- **安全修订：** scanner 独立为完整 `F-01S`。`-Staged` 必须用 stage-0 OID 和 binary-safe `git cat-file` 扫描 index blob；`-Tracked` 扫工作树；两开关同时扫描两个 source/path pair。输出新增 `source`，并要求 staged-secret/clean-worktree、clean-index/dirty-worktree、index mode、边界/引号和无 OID 泄露回归。
- **计划修订：** ledger 变为 32 项；F-01A 只负责工具链、byte-pinned licenses、React harness 和初始 push CI，CI-01 扩展完整流水线。增加统一的 2--5 分钟逐 assertion step 算法、精确路径别名/文件、normative plan 与 evidence-only ledger 差异、每个 coordinator commit 扫描和学生手写代码声明。
- **发布闭环：** 远程流程拆为 `EXT-REMOTE-PREP` 与 `EXT-REMOTE-FINAL`；前者记录 GitHub public 或 TA collaborator、每个 branch tip 的 push CI 和 OCI digest，后者在 DOC-01 后把最终 commit 推入同一 PR/MR并观察最终 GitLab `unit-test`/GitHub Actions。Windows clean VM 改为独立 `DIST-01-VM-CLOSE`。
- **规约澄清：** 新增 `MaterialVersion` 和跨课程 `MaterialBlobRef`，最后引用消失前不得删共享 bytes；finals 固定 mastery 倍率表为 unknown 1/2、demonstrated 3/4、retained 1。两项都是对已签字“parser 升级不覆写、期末压缩”的可测试化，不新增产品模块。
- **许可证证据：** 直接 PowerShell/curl raw 下载因 Schannel `SEC_E_NO_CREDENTIALS` 失败，Python raw 请求超时；随后用 GitHub 官方 Contents/Refs API 解析 4 个 release tag 和 5 份 base64 原始文本，记录 commit/blob/byte/SHA-256 到 `docs/engineering/BOOTSTRAP_LICENSE_EVIDENCE.md`。失败 transport 未冒充证据。
- **当前重跑阻塞：** 旧 projectless Codex task 和新 task `019fa224-046d-7a41-9841-b6632be08057` 都因读取 ProjectB 中两份源文件触发桌面审批。未代替学生批准，也未把旧 12-case 绿灯继承给新 index 合同；当前 F-01S G-03P recheck 明确为 pending。

## 10. 2026-07-27 桌面审批事故核对、第二轮评审失败与第三轮修订

- **审批事故核对：** 学生误批两个项目外 Codex 任务的桌面请求后立即停止它们。复查确认 ProjectB 仓库只保留学生原有的 `docs/research/*` 与 `docs/engineering/SUPERPOWERS_VALIDATION.md` 未暂存修改，暂存区为空，SPEC/PLAN 当时哈希仍为 `69A534...855E` / `47624A...225A`。两个任务只复制了获准的 SPEC/PLAN；旧任务删除了自己先前的 `outputs/scripts`，因此旧文件证据丢失但线程收据仍在。没有发现仓库写入、额外 ProjectB 文件复制、reparse link 或提交。
- **恢复动作：** 旧任务保持停止；新项目外任务 `019fa224-046d-7a41-9841-b6632be08057` 只从已复制的两份文件继续，先得到真实 `CONTRACT_RED scanner_missing`，再调试 complete F-01S。由于本轮评审随后改变 SPEC/PLAN，该尝试无论结果如何都只能成为 superseded-hash remediation evidence。
- **第二轮同哈希评审：** 规约 reviewer 对 `69A534...855E` / `47624A...225A` 返回 `Critical=0, Major=3, Minor=0`：locator 缺 `material_version_id`、早期分支 push CI 不运行当前核心测试、最终 commit 未依赖学生反思。质量 reviewer 返回 `Critical=0, Major=6, Minor=2`：F-01S rule grammar、复合 F-01A、许可证输入链、CI runner、reflection 顺序和九分支 stacked closure 仍不完整；Open Design receipt 与缩写哈希为 Minor。两份 verdict 均为 NOT PASS。
- **第三轮修订：** locator 两种联合都显式加入 `material_version_id`；F-01A 拆为 runtime/lock、license、frontend harness、portable push CI 和 shared quality gate 五张卡，总 ledger 为 35。F-01S 固定每个 rule ID、字面前缀、PEM/shell-variable/encoded-boundary grammar。F-01D 固定 PowerShell/Python/Node 容器 digest、checkout full SHA、least permission 和 current-suite fail-closed 规则；CI-01 只在不削弱已有核心任务的前提下追加 distribution。
- **远程与学生边界：** 九个 worktree 固定为 stacked base chain；最终按依赖顺序把每个既有 PR/MR 逐个 retarget 到默认分支并使用普通 merge commit 闭合，禁止 squash/rebase/history rewrite，保留所有 terminal task commit 的祖先关系。`REFLECTION-CLOSE` 必须先由学生完成并声明 AI 辅助范围，之后才可进入 release source commit 和最终双 CI。D-025、远程授权、正式异类型 G-03、G-04 均未代选或绕过。
- **许可证 TDD：** 修改 `scripts/verify_evidence.ps1` 前的静态合同以 `CONTRACT_RED bootstrap_license_binding_missing=...`、exit 1 失败；最小实现绑定账本 raw SHA-256、五个 target、commit/raw URL/blob/bytes/hash/license shape 后同一合同 PASS。对临时副本追加一字节时，真实 verifier 以 `Bootstrap license evidence hash mismatch`、exit 1 拒绝；标准收据保持 `rows=63 explicitly_blocked=2`。
- **当前候选：** SPEC `6A0DB7CAD19533FE9A31EA81A6B30ED493C01BE59D4C98DEB6EC04A89BD11E56`（27188 bytes）；PLAN `7B13DB324B1AF0A0838A3CD568AB04486C691BB26CA58CC3D42ED55EFF8BA7EE`（76980 bytes）。机械检查为 `Tasks=35 Ledger=35 Fields=5 AcRows=24 Placeholders=0`。新双评审与当前哈希 G-03P 尚未完成，不声称 Stage B PASS。

## 11. 2026-07-27 最终 G-03P、self-scan 修订与 SR-08 闭合

- **fresh 占位输入：** projectless task `019fa331-3da1-7f80-a37c-ac7abb135a46` 只复制 SPEC `6A0DB7...11E56`（27188 bytes）与当时 PLAN `D574B8...1D742`（81902 bytes）；没有读取仓库其他文件、提交、网络、凭据或远程资源。歧义门返回 none。
- **真实执行：** 完整合同先以 exit 1、`CONTRACT_RED scanner_missing` 失败；十一 helper 按 PLAN 顺序加入，最终同一命令 exit 0，并依次输出 `usage_and_output`、`token_rules`、`assignment_quotes_boundaries`、`encodings_and_types`、`staged_vs_worktree`、`index_modes_and_rename`、`path_safety_and_errors`、`redaction` 和 `BOOTSTRAP_SCANNER_CONTRACT_PASS`。contract/scanner SHA-256 为 `E970C52C...3A79B` / `097F5683...9F64`，仅在项目外输出目录。
- **输出 gap：** 额外 tracked+staged self-scan exit 2，在 contract 的 index/worktree 两源都报告 `credential_assignment`；合同行为绿但产物不能通过提交门禁。独立 AST substitute 未另行取得输出，不伪造 PASS。该事实证明必须把 artifact self-scan 纳入 Green/Done，而不是只依赖 behavioral contract。
- **最终修订：** PLAN `E96C415A...972C1`（82442 bytes）要求两份脚本在新 disposable Git 中同时 tracked+staged，精确得到 `CREDENTIAL_SCAN_PASS files=4`；direct/assignment/private/encoded 正例都必须由非匹配碎片在运行时拼接。F-01S 正式 ledger 仍为 not started。
- **最终 SR-08：** 当前 SPEC/PLAN focused 课程/SPEC review 返回 `PASS; 0/0/0`；质量/安全/许可证 review 返回 `PASS; Critical=0, Major=0, Minor=1`。唯一 Minor 是 Pillow 12.3.0 在 v1 没有明确生产角色，F-01A 应证明必要性或通过受审 evidence/lock 更新移除。bootstrap license owner 修订后的 evidence hash 为 `FD65C5...4F310`，stale-hash red 与新 hash green 均真实运行。
- **门禁结论：** SR-08 已闭合，但 G-03P 不是不同类型智能体。正式 G-03 必须使用最终 `6A0DB7...11E56` / `E96C415A...972C1`，随后学生才能作 G-04 实现批准。未创建产品源码、实现 worktree、远程 CI、分发物、部署或 `REFLECTION.md`。

## 12. 2026-07-29 正式 G-03 认证失败收据

- **冻结输入与隔离：** 会话 `a7671467-4cdb-4473-a9ab-587c336ef68d` 使用 Claude Code `2.1.220`，初始目录精确包含 `SPEC.md` 和 `PLAN.md`。SHA-256 分别为 `6A0DB7CAD19533FE9A31EA81A6B30ED493C01BE59D4C98DEB6EC04A89BD11E56` 与 `E96C415AD716B002AD9B1EB3C2AFD7C78F693486CB83A795110B99B6755972C1`，与最终冻结输入一致。
- **运行结果：** CLI 初始化后当前中转端点连续返回 `401 authentication_failed`，最终 exit 1。模型没有收到 prompt token，也没有输出 token；报告费用为 0。隔离目录仍只有两份输入文件，没有问题、diff、红测、绿测、自扫描或 F-01S 产物。
- **安全处理：** 凭据由隐藏提示输入，只进入 runner/Claude 父进程；保存日志对 key 模式和服务端掩码后缀再次脱敏。后续 runner 明确启用 `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB=1`，防止 Bash、hooks 或 MCP 子进程继承认证信息；不记录或复述密钥。
- **暴露的执行器问题与修订：** 首次 runner 的内联 MCP JSON 经 Windows `.cmd` 后丢失引号，已删除；用户级 Claude `env` 会重新注入旧认证，已改为 `--setting-sources project` 并显式配置当前中转；增加 `--allowedTools`、API 120 秒超时和 2 次重试上限。PowerShell 5.1 对无 BOM UTF-8 的中文解析问题通过 UTF-8 BOM 修复并完成文件级语法复验。
- **门禁结论：** 这是同期、可核验的失败 transport/auth 收据，但没有执行冷启动 task，不能闭合 G-03。下一次运行前必须由学生确认凭据所属 API base URL、认证头类型和模型名；不得凭猜测反复发送。
- **学生端点修正：** 学生随后确认凭据对应 `https://ai2.1343263.xyz` 的直接 Claude 分组，并表示后续预计继续使用该服务。无凭据 Node TLS 探针得到根路径 200；`/v1/models` 无认证时返回 `API_KEY_REQUIRED`，明确接受 Bearer、`x-api-key` 或 `x-goog-api-key`；`/v1/messages` 对两种假凭据均返回结构化 `INVALID_API_KEY`。runner 因此改用该端点和 Bearer token，并在隐藏输入后先查询真实模型列表，不再硬编码旧服务的 `deepseek-v4-pro`。

## 13. 2026-07-29 正式 G-03 首次模型执行与空产物差距

- **冻结输入与陌生性：** 会话 `71a50d25-4cd7-48b1-9472-8107e82779ed` 使用 Claude Code `2.1.220` 与 `claude-sonnet-5`。runner 只复制最终 SPEC `6A0DB7...11E56` 和 PLAN `E96C415A...972C1`；metadata 的初始文件精确为两份。Claude 自行计算并报告了相同哈希与完整文件列表，没有访问仓库历史、第三份项目文档、远程仓库或产品凭据。
- **实际尝试：** Claude 读取两份文件和 F-01S 卡片，检查 Git、PowerShell 5.1 与目录状态，并创建空的 `scripts/tests` 目录。可用工具为 Bash、Edit、Read，但日志中没有 Edit 调用。它没有提出问题、没有声明歧义、没有写入两份脚本，也没有运行规定的 `CONTRACT_RED scanner_missing`、八组绿测或 `CREDENTIAL_SCAN_PASS files=4`。
- **结束差距：** 最终 API 结果为 `subtype=success`、`stop_reason=end_turn`、空 result、CLI exit 0、permission denial 0；模型用量记录 output 1168 token、费用约 `$0.4712`。隔离目录独立复查仍只有 SPEC/PLAN 两个文件。该结果说明 CLI 传输成功不等于 task 完成，也说明本次智能体没有遵守“遇到不确定处提问并停止”的输出协议。
- **修订 diff：** SPEC/PLAN 没有发现可归因于文本歧义的缺陷，因此保持字节和 SR-08 评审不变。Git 忽略的 runner 新增产物后置条件：最终必须恰好存在两份冻结输入与两份非空 F-01S 脚本，否则记录 `COLD_START_INCOMPLETE`。对应本地测试先因函数缺失失败，最小实现后输出 `G03_POSTCONDITION_TEST_PASS`；对本次隔离目录返回 `required_artifact_missing`。下一次只改变默认模型为端点已列出的 `claude-sonnet-4-6`，用于区分单模型异常与中转兼容性问题。
- **门禁结论：** 这是正式不同类型智能体在最终哈希上的真实失败收据，补足了“异类工具可访问并实际尝试”的事实，但没有 PLAN 要求的 diff/红/绿/自扫描，不能关闭 G-03。F-01S ledger 仍为 `not started`，G-04 和产品实现继续阻塞。

## 14. 2026-07-29 正式 G-03 第二次模型执行与网关超时

- **冻结输入与模型**：会话 `32b62490-7817-4d3d-8452-7a29a4de94ea` 使用 Claude Code `2.1.220`、端点 `ai2.1343263.xyz`、模型 `claude-sonnet-4-6`。metadata 记录 SPEC `6A0DB7...11E56`、PLAN `E96C415A...972C1`，初始文件仍精确为两份。
- **实际执行路径**：Claude 先尝试不存在的 `/mnt/data/...plugin-gateway-stack`，随后列出正确 Windows 临时目录的 `PLAN.md` 与 `SPEC.md`，读取两份文件，并用 `certutil` 重新计算出正确 SHA-256。Read 工具把中文按错误编码显示为 mojibake，但未读取仓库其他文件、远程仓库或凭据。
- **失败原因**：第 6 turn 后日志出现 `API Error: 504 Gateway Time-out`，提示检查 inference gateway `ai2.1343263.xyz`。Claude Code 结果为 `is_error=true`、`stop_reason=stop_sequence`、费用约 `$0.1818`；runner 写入 `CLAUDE_FAILED`、exit 1。隔离目录仍只有 SPEC/PLAN，没有问题、diff、脚本、红测、绿测或 self-scan。
- **门禁影响**：该尝试证明 `claude-sonnet-4-6` 也未能完成长 Claude Code agent run，问题更像当前网关稳定性/兼容性风险，而不是仅 Sonnet 5 alias 异常。SPEC/PLAN 不因网关 504 改字节；G-03 和 G-04 仍开放。继续付费重试前需要学生明确接受模型/端点选择和费用风险。

## 15. 2026-07-30 G-03 可执行性、英文 capsule 与 F-01S1 拆分修订

- **学生输入：** 学生提供并要求继续执行《G-03 冷启动可执行性与多语言摄取修订计划》。该计划保留精简 v1 产品范围，把旧 F-01S 拆为 F-01S1--F-01S4，正式 G-03 只尝试 F-01S1；SPEC 保持中文正文，SPEC/PLAN 内生成 ASCII 英文 capsule；旧两次 Claude 失败保留为历史证据。
- **中断恢复：** 起始工作树已有未提交 SPEC/PLAN 拆分稿和 `scripts/cold_start/` 半成品；11 份学生研究文档保持原样、未纳入本轮。首次 capsule 合同为 `cases=7`，但主仓库缺 manifest。审查发现三处旧 F-01S 引用及拆分卡片使用“formerly specified”而不自包含，先补回精确 token、assignment、encoded、source 和 format 合同。
- **真实 TDD：** runner core 首次以 `G03_RUNNER_CONTRACT_RED core_missing`、exit 1 失败，最小 core 后通过；入口首次以 `G03_RUNNER_ENTRYPOINT_RED runner_missing` 失败，跟踪版入口后通过；候选独立复验首次因 `Test-G03CandidateEvidence` 不存在失败，最小实现后通过；execution stream 证据首次因 `Get-G03ExecutionEvidence` 不存在失败，最小实现后通过。当前本地合同输出为 capsule `cases=9`、runner core `cases=8`、entrypoint `cases=4`。
- **第一轮同哈希前评审失败：** 课程/SPEC reviewer 对 SPEC `BE32CA...EFFF` / predecessor PLAN `D9AE82...7016` 返回 Critical=2、Major=1；质量/安全/许可证 reviewer 返回 Critical=2、Major=5。共同问题是英文 capsule 缺 F-01S1 精确规则、READY 只检查四个非空文件、测试路径可伪造正式 READY、原始子进程输出先落盘、Bash 网络/读取边界未强制、超时不杀进程树、模型可改、矩阵仍为旧哈希/35 tasks。
- **关键修订 diff：** PLAN capsule 现内含六类直接规则、边界、精确 contract 命令和 `-Path <file>` 直接扫描命令；intake 使用固定 acceptance ID。测试收据改为 `projectb.g03.test.v1` 和 `TEST_ONLY_*`，只能写系统临时目录。正式 runner 固定 Sonnet 4.6/既定端点，不持久化原始 stdout/stderr；只在 Linux/WSL2 启动，并要求 Claude sandbox、全域拒绝网络、禁止 unsandboxed escape、`pwsh/timeout/bwrap/socat`。正式 READY 前重新核对输入哈希/普通文件/严格 UTF-8/三个函数，在新目录重放红测、绿测和两次产物直接扫描，并解析实际费用、Bash/Edit 调用与 execution 歧义。
- **环境事实：** Claude 官方文档说明 OS sandbox 仅支持 macOS、Linux 和 WSL2；本机 `wsl.exe --list --verbose` 被环境策略以 `Wsl/EnumerateDistros/Service/E_ACCESSDENIED` 拒绝。故原生 Windows 只运行无网络合同，不会询问 key 或付费；正式 G-03 需要学生提供可用 WSL2/Linux 环境。
- **当前候选与门禁：** SPEC `BE32CA48386363412785BA2766B73997FAFAAD32C186640C47C14B38FABEEFFF`；PLAN `35D989931B276C5DC474E715DB42DD49E576228FB2C6A81E956FBC6221CDF48F`。机械审计为 `Tasks=38 Ledger=38 Fields=5 AcRows=24 Placeholders=0 Unknown=0 Self=0 Cycle=0`。第一轮失败 verdict 不转移；当前哈希仍需重新双评审和学生整体确认。没有执行正式复测、G-04、产品实现、远程操作、部署或 `REFLECTION.md`。

## 16. 2026-07-30 第二轮审查与 G-03 安全重放修订

- **第二轮审查事实：** SPEC reviewer 对 SPEC `BE32CA...EFFF` / PLAN `35D989...F48F` 返回 `Critical=1, Major=1`：SPEC capsule 使用“acceptance summary”，而 PLAN/runner 使用固定 `acceptance_id`；重放收据没有保存实际绿测/直接扫描输出和新增文件 diff。质量 reviewer 对同哈希返回 `Critical=2, Major=4, Minor=2`：候选脚本在 sandbox 外且父进程仍有 key 时执行，空实现可用固定 PASS 欺骗验证器；另有 Linux `powershell` 命令不成立、原生 Edit 不受文件沙箱控制、未证明真实红绿 tool result、缺少真实 Linux 预检和条款记录等问题。两名 reviewer 均只读，没有修改文件。
- **真实红灯与修订：** 新合同先因缺少 `CommandInvoker` 和 runner 仍授权 Edit 失败；增加空实现候选后，旧验证器错误接受，合同按预期红；增加错误 JSON 键顺序候选后再次按预期红。最小修订后，coordinator 自有 oracle 会检查六类直接规则、token 边界、严格 UTF-8、稳定键顺序、脱敏、缺参和产物字节；execution stream 必须含顺序正确且有对应 result 的精确红/绿 Bash 调用。
- **隔离修订：** execution 只允许 Bash，原生 Read/Edit 均禁用；精确命令统一为 Linux/Windows PowerShell 7 可执行的 `pwsh -NoProfile -File ...`。正式运行在询问 key 前真实执行 bubblewrap 预检；模型结束后先清除认证环境变量，再在 `--unshare-all`、最小只读 runtime mount、一次性可写目录和双层 timeout 下重放。bubblewrap 子进程环境由 coordinator 清空，不继承 key。
- **条款边界：** 本地安装包为 `@anthropic-ai/claude-code@2.1.220`，`package.json` 声明 `SEE LICENSE IN README.md`；README 指向 Anthropic Commercial Terms 与 Privacy Policy，而不是普通开源许可证。它仅是 G-03 过程工具，不进入产品分发；正式运行前新增学生接受条款门禁。
- **当时候选与门禁（历史）：** SPEC `14C03D688A09451DCA06F66507CE4510510A8A3BC550057376B0A1EF95270713`；PLAN `D6A0C79B6E891993B91DD25C8C1121859BB0BE3065F3668FBCA09C8C7A45879D`。本地 core/entrypoint 合同已重新变绿，但真实 bubblewrap 预检只能在 WSL2/Linux 执行；随后 runner-only 文档修订改变了 PLAN capsule，故该哈希不再代表当前输入。正式 G-03、G-04、产品实现、远程操作、部署或 `REFLECTION.md` 当时均未执行。

## 17. 2026-07-30 runner-only 兼容性与质量修复

- **根因证据：** 读取既有 Claude Code stream-json 失败收据后确认，Bash 失败 `tool_result.content` 的真实格式为 `Exit code 1` 加换行后的命令输出；这不是候选脚本的独立重放格式。旧解析器只接受裸 `CONTRACT_RED scanner_missing`，会把真实 Claude 红测误判为缺失。
- **TDD 修订：** 先把真实包装格式写入合同样例并观察 `tdd_evidence_missing` 红灯；随后最小修改 parser，仅白名单接受裸单行或 `Exit code 1` 加该单行，拒绝 `Exit code 2` 和任何额外行。绿色合同现额外断言规范化 `exit_code=1` 与单行输出持久化到有序 TDD receipt。
- **安全语义补强：** PLAN capsule、中文 G-03 手册同步记录候选 contract/scanner 原始 SHA-256 在每次重放和直接扫描前后核对；coordinator oracle 覆盖全部规则前缀、长度下限/上限/超限、标点与阻断邻接、严格解码、排序与 JSON 键序。没有改变 SPEC/PLAN 的产品范围或 G-04 门禁。
- **当前字节：** SPEC `14C03D688A09451DCA06F66507CE4510510A8A3BC550057376B0A1EF95270713`；PLAN `95FF14D23DB92692BA005C3AA42598ABB5DDCFEE2DEFC28B950B00617C3EC663`。本地合同和入口测试均重新通过；同哈希双评审、学生确认、Linux/WSL2 正式 G-03 和 G-04 仍未关闭。
- **最终同哈希双评审：** SPEC/课程合规 reviewer 与质量/安全/许可证 reviewer 均对上述精确字节返回 `PASS; Critical=0, Major=0, Minor=0`。这只闭合当前 SR-08 文档审查，不等于正式非 Codex G-03、学生确认或 G-04。

## 18. 2026-07-31 正式 G-03 intake 提示行差距与 runner 修订

- **正式失败收据：** 会话 `f195336c-e5fc-4366-9ad5-3c90fb106811` 在 WSL2 中通过 capsule、冻结输入、平台和 bubblewrap preflight；intake 运行 59 秒后 Claude Code exit 0，但 runner 以 `child_output_protocol`、exit 44 结束。没有产生 F-01S1 产物，因此不计为 G-03 完成。
- **根因证据：** 三份早期脱敏 Claude Code 日志的首个非空行均为固定 `Permission mode forced to default` 安全提示，后续才是合法 JSON/stream-json。当前失败发生在本地 stdout 解析边界；它不同于已记录的 401 鉴权失败和 504 网关超时，不能据此认定新 key 或 API 本身失效。
- **修订 diff：** intake 先剥离至多一次、精确枚举且大小写敏感的 Unicode/历史 mojibake 提示，再解析完整 JSON；execution 采用相同首行规则，任何其他非 JSON 行或重复提示均返回 `stream_output_protocol`。任意前缀、分隔符、ASCII 变体、大小写变化和重复 BOM 均失败关闭。
- **真实红绿与评审：** 合同先因 helper 缺失失败；第一版宽正则又被未观测 ASCII 变体负例击中。最小严格实现后 core `cases=13`、entrypoint `cases=5`、capsule `cases=9`、历史首行回放和标准 63 行证据校验均通过。首轮规约/质量评审分别为 Major 2/Major 1；修复后的只读复核为 `PASS Critical=0 Major=0 Minor=0`。
- **哈希与门禁：** SPEC/PLAN 仍为 `14C03D688A09451DCA06F66507CE4510510A8A3BC550057376B0A1EF95270713` / `95FF14D23DB92692BA005C3AA42598ABB5DDCFEE2DEFC28B950B00617C3EC663`。G-03、G-04、产品实现、远程授权、部署和学生本人反思仍未闭合；下一次正式运行必须重新产生完整证据，不能继承本次失败收据为 PASS。
- **第二次正式失败：** 会话 `49fa60fb-85ea-4728-bf86-b68b2a532423` 的 intake 在 25 秒后仍以 Claude 子进程 exit 0、`child_output_protocol` 结束，说明第一轮精确提示白名单没有覆盖实际 stdout 结构；没有保存原始输出，因此不猜测或继续扩大白名单。
- **安全诊断修订：** runner 仅在协议失败时记录 `output_shape`，内容限于 JSON/提示/ANSI/HTML/其他文本行计数、固定提示前缀和分隔符枚举、完整 JSON 布尔值及 stderr 是否存在。测试以运行时拼接的伪 key 证明诊断 JSON 不含任意原文。该修订不改变冻结 SPEC/PLAN、intake 验收、任务产物或 G-03/G-04 门禁。

## 19. 2026-08-03 正式 G-03 人工 Claude Code 冷启动闭合

- **学生选择与陌生性：** 学生明确停用历史 runner，改用 Claude Code 插件。Intake 与 execution 使用两个互相独立的新 session，初始目录均只含当前 `SPEC.md`、`PLAN.md`；未提供 AGENTS、历史计划、产品源码或第三份项目上下文。
- **Intake：** 返回 SPEC `AEA67BB5544AD22932DC4304964F7FD266FE8A5DE7AA396EA8974D30867E8381`、PLAN `910A3AEC9B4CEDCC119675C5D862879D178E3FE062CEE39C2AD62AF07219E923`、完整列表 `[PLAN.md, SPEC.md]`、语言 English、任务 `F-01S1A`、验收 `F01S1A_SINGLE_RULE_SCANNER_V2` 和空歧义；主智能体重新计算的哈希与文件集合一致。
- **分段 execution：** 为避免此前长 thinking 后中断，同一 execution session 按 `1/2A/2B/2C/2D/3A/3B/3C/3D-R` 分段。2D 在 scanner 不存在时得到唯一输出 `CONTRACT_RED scanner_missing`、exit 1；3D 首次暴露无 BOM fixture、缺参退出语义和空集合处理问题，Claude 在同一 session 修订候选。最终 3D-R 不再修改文件，PowerShell 7 返回 `GROUP usage_and_output`、`GROUP provider_rule`、`BOOTSTRAP_SCANNER_PATH_PASS`、exit 0。
- **产物复验：** disposable execution 目录最终恰含两份冻结输入和 `scripts/bootstrap_scan_credentials.ps1`、`scripts/tests/bootstrap_scanner_contract.ps1`。Scanner 为 95 行、SHA-256 `104085D3508C618A5DDC8AF18583825DE809A677575E95196DD1FD776F0B5C6E`；contract 为 161 行、SHA-256 `8BA08B9A6786D21C46312674334D818658688A8AFAA07481FEB90B79B63F161E`。冻结输入未变化。
- **独立检查与限制：** 主智能体静态核对函数、规则、严格 UTF-8、路径、稳定错误、脱敏和行数，并以不修改候选字节的 PowerShell 5.1 兼容副本得到相同三行 green、exit 0；当前工具沙箱调用 WSL 仍为 `E_ACCESSDENIED`，因此精确 PowerShell 7 输出采用学生转交的 3D-R 原始回执。插件未暴露可核验费用，旧 runner 的 bubblewrap/费用字段不补造。学生已明确选择人工插件流程，这些限制不冒充 runner 收据。
- **修订结论：** 冷启动发现的是执行分段和候选实现问题，不是当前 SPEC/PLAN 的规范歧义；因此两份冻结文档不改字节，也无需重新执行 SR-08。G-03 按学生指定的人工 Claude Code 替代流程闭合；候选脚本不合入产品，正式 F-01S1A 仍须在 G-04 后重新按 TDD 和双评审实现。

## 20. 2026-08-03 G-04 实现批准

- **学生原始决定：** “批准进入实现阶段”。
- **门禁结论：** G-04 已闭合；可以按 `PLAN.md` 创建 `codex/foundation-v1` worktree，并从正式 `F-01S1A` 开始逐 task 执行 TDD、规约评审、质量/安全/许可证评审和小提交。
- **不随本批准开放的操作：** 远程 push、PR/MR、发布、付费资源、公网投放和真实 provider 调用仍受各自命名门禁约束。
- **规范字节：** G-03 绑定的 SPEC/预派发 PLAN 哈希保持 `AEA67BB5...E8381` / `910A3AEC...E923`。批准后仅按 PLAN 3.1 允许范围把顶层执行状态改为 active、把 `F-01S1A` 标为 in progress；当前证据态 PLAN 哈希为 `382BCDB3...943F2`，不属于规范修订。

## 21. 2026-08-05 F-01A 依赖权威安全刷新

- **触发原因：** F-01A 质量评审当天重新运行 `npm audit`，旧权威锁出现 `undici 7.28.0` High 与 `postcss 8.5.21` Moderate；继续照抄旧哈希会把已知告警固化进正式项目。
- **受控修订：** 只更新传递依赖为 `undici 7.29.0`、`postcss 8.5.25`，并把一次性证据工作区身份改为正式私有 `projectb@0.1.0`。16 个直接 npm 选择、166 个非根包、115 个 Windows 安装包和全部许可证计数保持不变；未运行会改变直接版本的宽泛升级。
- **关键 diff：** npm canonical-LF hash 从 `071826d5...3c2f` 更新为 `8b793ee9...8354`；生产锁、权威锁、`PLAN.md`、`scripts/verify_evidence.ps1`、运行时合同和依赖基线同步绑定。当前证据态 PLAN hash 为 `91798DAFE433049B654ACE1D8638188730FA00DAFDA6FC23411F70643351812D`。
- **复验与边界：** fresh `npm ci`、`npm audit`、`npm ls`、运行时合同、63 行课程证据验证和凭据扫描均通过。该修订是同一 F-01A 范围内的安全维护，不新增产品能力、服务、许可证选择或远程发布授权。

## 22. 2026-08-05 F-01B 许可证传输合同修订

- **冷启动式误解/差距：** 初版实现正确使用 GitHub Contents API 和不可变 raw fallback，但测试只搜索脚本文本中的关键字，不能证明 API 优先、错误元数据拒绝、回退顺序和错误字节 fail-closed。
- **关键修订 diff：** 合同增加内存 transport harness，分别验证 API 成功不触发 raw、API 传输失败后逐项 raw 回退、API 元数据错误禁止回退、API/raw 错误字节、双传输失败、已有 partial 文件和 junction 输出根；实现区分“API 传输不可用”与“API 返回不可信元数据”，只对前者回退。
- **字节边界：** 五份许可证严格保持证据表的 byte count、SHA-256 和 Git blob ID。Node 上游许可证含合法 space-before-tab，仓库以 `-text -diff` 保存这组哈希产物；scanner 仅增加五个精确 extensionless 文件名，不放宽未知文件失败策略。
- **结果与范围：** F-01B 合同、标准证据验证、离线 bootstrap、全仓凭据扫描和 staged diff 均通过。该修订只闭合 bootstrap 许可证，不改变 SPEC、依赖版本、应用功能或远程授权门禁。

## 23. 2026-08-11 D-026 Windows 性能门禁收束

- **学生问题与决定：** 学生询问干净 VM 验证是否为课程硬性要求。协调器区分了课程要求的可分发/可运行证据与 SPEC 自设的 `<=10` 秒指标；学生随后明确回复“那就豁免，把其他的补完然后整理成课程要求的提交包”。
- **修订前：** 当前产物必须再次复制到指定干净 Windows VM，并取得 `<=10.0` 秒、SmartScreen 和 WinVault 同次收据，才能关闭 DOC-01。
- **修订后：** D-026 取消当前产物再次干净机复测和 `<=10` 秒提交门禁。保留上一版产物在无 Python/Node/Docker 的 Windows 11 VM 成功启动及最低 `11.487` 秒的真实记录，保留当前产物的确定性构建、归档检查、开发机 smoke、凭据测试和 README 限制；不把 waived 写成 PASS。
- **影响：** 本地提交包可闭合。学生进一步明确 ProjectB 是本地单文件应用，FastAPI 仅提供 loopback WebUI；按课程第 4.11 节“如做带服务端的项目”的条件条款，D-025 不要求公网部署。课程最终 CI 的真实远端 PASS 仍需 NJU GitLab/GitHub 外部仓库与 runner，未执行时必须继续标注 `not executed`。
