# 课程材料数据与凭据威胁模型基线

记录时间：2026-07-19T22:32:43+08:00

## 状态

本文最初是在 D-008 尚未确认时形成的方案无关基线；D-014 现已确认第一版实现 L/P/F 三种能力。D-017/D-018 又确认领域层保留 provider-neutral port，但首版 local production 只注册平台内置 OpenAI adapter；deterministic mock 仅注册于 test/demo，普通配置不接受 `base_url`、任意 endpoint、动态 adapter 或第三方 plugin。

后续学生反馈确认：纯本地解析可能损失公式、代码、图表或版面语义，因此产品应允许用户选择处理路径。第一版提供 L/P/F，但没有隐式默认外发；每次实际文件范围仍需授权。该选择不会取消本文件中的数据最小化、外发可见性和凭据保护要求。具体 OpenAI 模型由支持 profile 显式配置；动态能力、区域资格、留存/训练政策和费用必须在调用前形成快照，未知或能力不足时失败关闭，不能被当成已经兼容。

后续 D-010 确认第一版采用单用户、本地优先 WebUI，不实现账号或多租户。T-07 仍作为未来扩展和 owner scope 的回归约束，但不要求第一版实现多用户认证。

本轮 brainstorming 又确认课程资料按批次增量到达；D-019 将第一版材料白名单固定为 `lecture`、无答案 `past_paper` 和 `teacher_focus`，支持 PDF/图片/文本及手工重点，答案、个人笔记和作业提交延期。D-020 将第一版调度固定为版本化简单规则、可选每日预算、自动但可撤销的未来任务重排，以及考试本地日期完整结束后的归档/暂停和新目标询问。上述材料沿用课件的最小外发、来源追踪和不可信输入边界，不获得额外工具权限，也不表示模型训练或原题预测。

D-021/D-022 已确认 Windows x64 本地版通过 keyring 使用 Windows Credential Manager；公开 demo 仅使用合成/明确许可夹具和 deterministic mock。隔离、限时访客 session 以及 OCI/Hugging Face 部署方向已随整体 SPEC 确认，仍须工程与官方条款验证。以下项目将已确认边界转为可验证控制，不再把 provider、凭据后端或 demo 数据策略列为未决选择。

## 保护目标

1. 未经学生明确动作，不把课件、笔记、作答或掌握状态发送到本机之外。
2. 即使允许云端处理，也只处理用户在当前 L/P/F 模式和实际文件级授权中明确可见的范围；P 默认最小化，F 必须展示整份文件范围与生命周期风险。
3. API key、token 与密码不进入源码、Git、浏览器持久化、日志、错误消息或测试快照。
4. 学生能查看每类数据的保存/外发状态，并能清除本地数据、远端任务引用和 Windows Credential Manager 凭据；强制清除后新远端调用立即失败关闭。
5. 课程材料中的文本、链接、代码和指令始终作为不可信内容，不获得工具执行权。
6. 系统不能把不完整解析、模型猜测或过期掌握状态呈现为确定事实。
7. 每次远端授权和远端对象都能追溯到当时的 provider profile、非敏感配置版本、能力/政策快照和凭据引用；配置变化不能扩大旧授权或复用旧远端引用。

## 资产与敏感级别

| 资产 | 敏感级别 | 主要风险 |
| --- | --- | --- |
| 原始课件 PDF 与页面图像 | 课程受限内容 | 未授权上传/再分发、公共缓存、跨用户泄露 |
| 抽取文本、切片、向量与 `SourceLocator` | 课程受限派生数据 | 可重建原文、错误页码/版本、供应商留存；删除后 tombstone 过量 |
| 学生笔记、提问、作答与自我解释 | 个人学习数据（个人笔记材料首版延期） | 暴露学习困难、身份或作业内容 |
| 知识点掌握状态与复习历史 | 个人画像 | 错误推断、长期画像泄露、不可解释评分 |
| 考试日期、课程目标与提醒 | 个人日程 | 时间信息泄露、错误提醒影响学习 |
| 无答案往年卷、老师重点与题目映射 | 课程受限内容/个人学习数据 | 未授权再分发、错误的“重点”推断、提示注入、学术诚信风险；答案材料首版不接收 |
| 材料批次、覆盖决定与计划版本 | 学习过程元数据 | 串改、丢失历史、未经确认把新知识排入计划 |
| Provider profile、非敏感配置与政策快照 | 安全/合规元数据 | 注入 `base_url`/plugin、能力虚报、政策过期、旧授权被错误复用 |
| API key、访问 token、主密码 | 凭据 | 账号滥用、费用损失、数据越权 |
| 运行日志、错误与追踪数据 | 运维数据 | 间接包含路径、片段、凭据或用户输入 |
| 模型输出与工具参数 | 不可信派生数据 | 幻觉、提示注入传播、危险命令或 URL |

## 候选信任边界

无论最终技术栈如何，至少需要区分：

- **用户与 WebUI**：用户选择课程材料、查看外发预览、回答练习、管理删除。
- **本地文件与解析器**：读取用户明确选择的文件；不得扫描其他目录；解析器运行需有类型、页数、大小和时间限制。
- **本地索引/状态库**：保存页面引用、知识点、学习证据和复习计划；应按用户/课程隔离。
- **应用后端或本地服务**：决定检索、模型调用和状态更新；不得信任前端传来的文件路径、页码或工具参数。
- **Provider adapter registry 与配置层**：local production registry 只登记内置 OpenAI adapter；provider profile 只保存支持的模型、受控参数、预算和 `credential_ref`，不保存 secret、`base_url`、任意 endpoint 或 plugin。mock 只存在于 test/demo profile。
- **模型/embedding 供应商**：一旦跨越此边界，就必须记录 profile/config/policy snapshot、发送范围、目的、时间与删除/留存能力。
- **日志、备份与部署平台**：默认不记录正文、作答和凭据；公开部署必须防止跨用户访问与静态文件暴露。

## 主要威胁与候选控制

| ID | 威胁 | 候选控制 | 可验证证据 |
| --- | --- | --- | --- |
| T-01 | 导入目录时越界读取其他个人文件 | 只接受用户显式选择的文件句柄/上传；规范化路径并限制到本次选择集合 | 给定越界路径时拒绝；访问日志只含允许文件 ID |
| T-02 | 课件在用户不知情时上传 | 无政策/文件级 consent 时上传为 0；P 展示页面/片段，F 展示整份文件清单、大小、OpenAI profile、政策快照与成本并要求明确动作 | contract spy 断言无确认时调用次数为 0；请求范围、profile/config/policy snapshot 与 consent 精确相等 |
| T-03 | P 模式检索切片过大或包含无关页面 | 按知识点/页码限定最小片段；设字符、图像和页数上限 | 捕获请求只包含被引用页面及规定上限 |
| T-04 | PDF 中的提示注入诱导模型泄密或调用工具 | 课件内容标记为数据；系统指令与材料隔离；模型不能直接获得任意工具；工具参数做独立校验 | 注入测试不能读取凭据、文件或触发未授权工具 |
| T-05 | 恶意/损坏/伪装输入消耗资源或攻击解析器 | v1 校验扩展名、MIME/魔数、编码与解码：`.pdf` + `application/pdf`/PDF 魔数为 256 MiB/2,000 页；PNG/JPEG/WebP 对应标准扩展名/MIME 为 20 MiB/50 megapixels；UTF-8/UTF-8 BOM TXT/Markdown 对应 `text/plain`/`text/markdown` 为 2 MiB；手工重点 1-10,000 code points；单批 50 文件/1 GiB/5,000 PDF 页；空/损坏/加密/冲突输入失败关闭 | 各边界前后值、伪装/损坏/加密夹具在正文处理前得到稳定错误；provider 更低限制在 consent 前失败且网络调用为 0 |
| T-06 | API key 出现在 Git、日志、前端、`.env` 或 provider config | secret 只由后端通过 keyring 写入 Windows Credential Manager；config 只保存 `credential_ref`；正式版/开发默认/demo 不读取 `.env`；状态只返回“已配置/未配置”和更新时间 | 凭据扫描、配置 schema 拒绝 secret/`.env` 路径、日志测试、查看/更新/清除端到端测试；浏览器/SQLite 无 key |
| T-07 | 多用户部署时课程/学习状态串读 | 每个对象绑定 owner；服务端逐次授权；不可猜测 ID；缓存按用户分区 | 用户 A 无法读取或检索用户 B 的任意对象 |
| T-08 | 删除只隐藏 UI，缓存/索引仍存在或 tombstone 可重建内容 | 级联删除原文、页面图、抽取、切片和可重建索引；停止后台任务；历史只保留不含正文、路径或 provider ID 的 tombstone/失效 locator | 删除后本地查询、检索与后台任务均不可访问；历史仍可解释但无法重建内容 |
| T-09 | 日志或错误回显全文、路径、作答和 key | 结构化白名单日志；内容摘要使用内部 ID；错误统一脱敏 | 测试异常路径后扫描日志无敏感模式或正文 |
| T-10 | 模型幻觉、坏 schema 或无 locator 输出被写入权威状态 | 只允许具名模型端口并校验 schema/来源/大小；coverage/exam 无有效 locator 时返回空候选 + `source_insufficient`；解释/练习/反馈至多返回 `model_supplement`，不作为材料事实或权威证据 | 无引用/坏 schema 输出不能进入覆盖、计划或掌握；三类补充端口标签固定且每次状态更新可追溯 |
| T-11 | 重试或隐式循环调用模型导致费用失控 | 每端口 token/次数/时间预算、速率限制、取消、本地幂等键与费用提示；真实 OpenAI 请求按 at-least-once 对账，第一版无自主 agent loop | 超预算自动停止；不重复本地逻辑 job；响应丢失后的重复远端对象/可能额外费用可见并进入隔离清理；不存在无限工具循环 |
| T-12 | OpenAI 留存/训练政策、能力或配置与用户预期不一致 | profile/config 与版本化能力/政策快照绑定；拒绝 `base_url`、任意 endpoint、动态 adapter/plugin 和未知字段；界面只展示已核验信息，未知能力禁用对应 P/F | 配置、政策快照与调用一致；政策变化生成新版本并要求重新确认；非法字段在联网前拒绝；动态政策合同见 `REFERENCE_PROVIDER_OPTIONS.md` |
| T-13 | 恶意网页通过浏览器访问 localhost 应用 | 默认仅绑定 loopback；校验 `Host`/`Origin`；拒绝开放 CORS；状态变更使用 CSRF 防护和本地会话随机量 | 非受信来源无法读取状态或触发导入、外发、删除和凭据操作 |
| T-14 | 往年卷/老师重点中的提示注入改变系统规则或诱导上传 | 将材料角色和正文作为不可信数据；系统指令、策略层和材料隔离；模型不能直接调用工具；输出必须经过结构化 schema 与白名单校验 | 注入样本不能修改 `ProcessingPolicy`、`CoverageDecision`、计划或触发未授权外发 |
| T-15 | 模型把老师重点、往年卷频度或猜测误当成权威课程事实 | 区分来源类型、候选映射、用户确认和系统推断；显示置信度与原页/题号；未确认项不得进入计划 | 未确认/低置信映射不改变权威覆盖、优先级或掌握状态；可追溯纠正 |
| T-16 | 新批次导入或计划重排抹去既有学习历史 | 批次、覆盖决定、`LearningPlan` 和 `PlanRevision` 追加式版本化；只重排未开始未来任务 | 新批次、日期变更、删除材料后 `Attempt`/`LearningEvidence`/旧计划仍可读取 |
| T-17 | 期末“拟合往年卷”被误实现为训练模型、预测泄露试题或自动上传 | 在产品语义和代码接口中将其限定为结构/题型/知识点/难度分析与同类练习；禁用训练/微调/自动上传路径；显式审计远端请求 | 固定测试断言无训练 API、无预测承诺、无同意时远端调用为 0 |
| T-18 | 整份上传/索引部分失败、错误引用或删除失败造成孤儿对象 | 每文件对象/job 状态、每课程独占 Vector Store、幂等键与三层删除对账；OpenAI citation 必须映射并校验本地 `SourceLocator`，否则 `source_insufficient`；未知状态禁止检索并显示 `delete_incomplete` | 重启/取消/部分失败/离线恢复后对象仍可追踪；无有效 locator 时不产生材料事实/计划；删除未确认不显示成功 |
| T-19 | 切换 OpenAI profile/config 后复用旧远端引用或授权 | profile/config 版本不可变；模型、受控参数、预算或政策指纹变化创建新快照和 consent；旧引用只由创建它的 profile 做对账/删除，不得迁移 | 切换模型/config 后旧引用不能进入新请求；配置未确认或能力不足时远端调用为 0 |
| T-20 | 含答案往年卷、个人笔记或作业被伪装成首版允许角色 | 白名单只允许 `lecture`、无答案 `past_paper`、`teacher_focus`；明确延期角色返回 `unsupported_role`；本地解析后发现疑似答案/泄露进入 `needs_user_review`，远端/权威写入为 0，自动检测不声称完备 | 错误角色夹具不进入权威覆盖/计划；`needs_user_review` 只能经用户改正/移除/取消恢复；未知角色不产生远端调用 |
| T-21 | 自动调度重排不可解释、不可撤销或过早暂停 | 整体确认的 `ReviewPolicy v1` 固定纯函数、数值、稳定排序和 golden fixtures；自动修订只影响未开始任务并可撤销；考后条件严格 | 以固定时钟/tzdata/策略/证据重放 fixtures；撤销保留历史；考试当天仍可学习 |
| T-22 | 公开 demo 接收私人材料、真实 key、真实 provider 或串读访客状态 | 只加载内置合成/明确许可夹具和 deterministic mock；禁用上传、凭据入口、provider 出站和持久私人状态；随机隔离 session，30 分钟无活动/2 小时总寿命；每 session 1 课程/20 夹具/2 并发/64 MiB，每 IP 60 请求/分钟 | 构建/运行无真实 provider 网络权限或 credential store；跨 session 读取为 0；到期/重置清除；界面标明演示数据/模拟模型 |

## 三种正式模式的风险影响

| 方案 | 课件外发 | 凭据 | 主要新增风险 | 主要工程负担 |
| --- | --- | --- | --- | --- |
| P：本地解析 + OpenAI 最小片段调用 | 仅学生确认的页面/片段 | Windows Credential Manager 中的 OpenAI key | 片段仍可能受供应商留存；选择范围错误 | 本地定位、请求预览、能力/政策快照与审计 |
| F：整份文件/课程上传 OpenAI | 大范围外发 | Windows Credential Manager 中的 OpenAI key | 版权、隐私、成本、供应商缓存与删除不确定性最高 | Files/Vector Stores 生命周期、locator 映射、成本与删除对账 |
| L：全本地解析与索引 | 不外发课程内容 | 不需云 key | 解析失真、恶意文件、CPU/内存资源 | 保真报告、来源定位、性能和解析器隔离 |

## 不随用户模式选择变化的安全不变量

- 默认拒绝外发；没有用户动作时远端调用为零。
- 原课件、派生文本、作答、掌握状态与凭据均不进入普通日志。
- 课程材料和模型输出均无工具权限，所有工具调用由应用代码白名单分发。
- 文件读取仅限用户明确选择的集合，并严格执行 M1 v1 MIME/魔数、编码、单文件/批次大小、页数/像素/文本长度与超时限制。
- 所有状态更新带来源与时间，学生可查看、纠正和撤销。
- 首次配置隐藏录入凭据；secret 只存 Windows Credential Manager，支持状态、更新、清除且不回显明文。正式版/默认开发测试/demo 均不读取 `.env`。
- Provider config 只保存内置 OpenAI adapter ID、支持模型、受控参数、预算和 `credential_ref`；secret、`base_url`、任意 endpoint、动态 adapter/plugin 和未知字段一律拒绝。
- local production 只允许内置 OpenAI；mock 只允许 test/demo。缺少 P/F 所需能力时保留 L，并对相应远端模式失败关闭。
- `ConsentRecord` 与 `RemoteMaterialObject` 必须同时绑定不可变 profile/config/policy snapshot；修改模型、受控配置或政策指纹后不得复用旧 consent 或远端引用。
- 错误向用户说明受影响文件/页面和恢复方式，不暴露路径、正文或供应商内部信息。
- 用户选择一种模式不等于永久授权更宽范围；按课程保存设置时仍要允许查看、修改和撤销，任何扩大外发范围的切换都需重新确认。
- 新材料先产生候选覆盖；没有 `CoverageDecision` 就不得修改权威知识或计划。
- `past_paper`、`teacher_focus`、`StudyFocus` 和计划版本都保留来源、置信度、确认状态和修订链。
- 考试日期与显式 `finals` 进入动作分开审计；日期本身不改变外发范围或自动触发模型调用。
- 模型只能通过白名单端口访问已批准的来源 ID；响应先做 schema、来源和大小校验，错误时不从自由文本猜测权威字段。
- deterministic provider mock 仅用于 test/demo，必须在无网络、无凭据和无真实 LLM 时覆盖坏 schema、注入、超时、限流、取消、预算和重复响应。
- 模式 F 必须通过文件级 consent、哈希幂等、上传/索引/删除状态和 provider 能力声明；不能用“模型接受 PDF”替代生命周期证据。
- 第一版材料角色和输入形式实行白名单：`lecture`、无答案 `past_paper`、`teacher_focus`（PDF/图片/文本，重点可手工录入）；答案、个人笔记、作业提交和其他角色保持 `unsupported_role`。疑似答案/泄露进入 `needs_user_review` 且远端/权威写入为 0。
- `SourceLocator.kind` 统一为：`pdf_page` = `{kind, material_id, content_hash, page, region?}`，`image` = `{kind, material_id, content_hash, image_id, region?}`，`text_lines` = `{kind, material_id, content_hash, line_start, line_end}`，`manual_entry` = `{kind, entry_id, version}`。无有效 locator 不得称为材料事实；coverage/exam 返回空结果 + `source_insufficient`，解释/练习/反馈只能返回 `model_supplement`。
- `ReviewPolicy v1` 精确纯函数已随整体 SPEC 确认；自动修订只影响未开始任务并可撤销，仅 `today_local > target_local_date` 后暂停。
- 删除后本地检索不能返回正文/单元；历史只保留不能重建正文、路径或 provider ID 的 tombstone 与失效 locator。强制清除凭据后新远端调用失败关闭，遗留对象显示 `delete_incomplete` 与恢复入口。
- 公开 demo 只用许可夹具/mock、隔离限时 session，并禁用上传、真实凭据、真实 provider 出站和私人材料持久化。

这些项目已在最新 `SPEC.md` 转化为验收标准；当前仍没有实现或测试证据。

## 仍待核验的风险

- OpenAI 模型目录、区域资格、费用与政策会变化；每次 P/F 必须绑定当时的能力/政策快照。Responses/Files/Vector Stores 的详细基线见 `REFERENCE_PROVIDER_OPTIONS.md` 与 `REMOTE_FILE_LIFECYCLE_CONTRACT.md`；
- 原 PDF、页面图、抽取文本和学习状态的具体保存期限；删除语义已固定为内容清除 + 非重建 tombstone，但默认期限尚需核验；
- D-019 已确认首版不导入个人笔记、作业答案、往年卷答案和其他考试资料；这些仍是未来扩展候选，需新增角色和治理；
- 操作系统课件权利人对远端处理与衍生练习的许可边界；
- 期末重点/往年卷的保存期限与展示粒度；公开 demo 已禁止导入真实材料，不依赖对私人材料做脱敏；
- Windows keyring 后端、打包兼容性和依赖许可证，以及 OpenAI SDK 许可证仍须在引入依赖前验证；
- 公开 OCI 首选 Hugging Face Spaces Docker SDK，但当前官方复核受 502/超时阻塞；网络恢复后须重核费用/Docker/HTTPS/临时存储，账号、URL 与隔离证据仍需部署阶段授权和真实验证。
