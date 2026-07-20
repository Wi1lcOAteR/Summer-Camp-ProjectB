# 整份课程材料远端生命周期合同

记录时间：2026-07-20T00:57:31+08:00

## 状态与范围

D-014 已确认第一版实现整份 PDF/课程远端处理（模式 F），并由用户决定是否使用。D-015 确认平台使用统一 `ProviderAdapterRegistry`，用户在配置/设置中选择平台已实现的 provider adapter；D-016 确认首版一个真实 adapter + 完整 mock；D-017 选择 OpenAI 作为唯一真实参考 adapter；D-018 确认只允许平台内置 adapter，不开放任意自定义 endpoint 或第三方 plugin。本文件继续定义 provider-neutral 的配置、授权、上传、索引、使用、切换和删除合同，并补充 OpenAI 首版映射；具体模型版本、SDK 包、区域、费用与凭据存储实现仍待后续核验。

## 核心原则

1. **能力不等于授权**：平台实现模式 F，不代表任何课程或文件默认外发。
2. **课程选择不等于未来文件授权**：课程记住 F 模式，但每个新增批次都要展示实际文件和范围并确认。
3. **远端对象不替代本地来源**：原 PDF、页码、原始抽取、用户修正和内容哈希仍是权威来源身份。
4. **外发与权威状态隔离**：上传/索引成功不能自动确认知识覆盖、提高掌握或激活计划。
5. **删除是可观察过程**：只有 provider 明确确认或合同定义的终态才能显示 `deleted`；否则显示 `delete_incomplete`。
6. **配置不等于凭据或授权**：provider profile 只保存非秘密配置和 `credential_ref`；选择或修改 profile 不自动获得材料外发 consent。
7. **真实 provider 不是 exactly-once 系统**：本地 job 使用幂等键和 at-least-once 恢复；响应丢失或进程崩溃时可能已创建远端对象。平台必须发现、隔离、对账和清理重复对象，不能承诺绝不重复创建或绝不重复计费。

## 首版 OpenAI 生命周期映射与政策快照

首版真实 adapter 必须把 OpenAI 对象映射到本合同，而不能让领域层直接依赖供应商 ID：

| 本合同阶段/对象 | OpenAI 官方能力映射 | 首版约束 |
| --- | --- | --- |
| 页面/PDF 直接输入 | Responses 的 PDF `input_file` 在具备视觉能力的模型上同时使用抽取文本与逐页图像 | 适合经授权的 P/受控直接请求；不把该能力推断为 File Search 的视觉保真 |
| 受约束生成 | `/v1/responses` | 首版全部前台请求显式发送 `store:false`；禁用 background、Conversations、远程 MCP，以及 Hosted Shell/Code Interpreter 等执行型 hosted tools；模式 F 的固定 File Search 只能由 adapter 按已授权 store 调用，不开放任意工具分发 |
| 基础文件对象 | Files API | 单独追踪、删除或设置 `expires_after`；不得只删除 vector store association 后宣称文件已删除 |
| 索引/知识库 | Vector Stores 与 vector-store file association | 每个 `(course_id, provider_profile_id, config_fingerprint)` 使用独占 Vector Store；文件关联达到 `completed` 前不得进入 `ready`；File、vector store 与 association 分别对账 |
| 检索 | Responses 的托管 File Search | 原生 `file_citation` 只有文件级信息；无有效 `SourceLocator` 时 coverage/exam-analysis 空 `source_insufficient`，其他三端口仅 `model_supplement`，均不能产生材料事实/计划输入 |
| 删除/过期 | Files/Vector Stores 删除入口；Files `expires_after`；Vector Stores 过期策略 | 删除请求成功与最终数据清理不得混同；UI 只按可证明状态显示 |
| 结构化输出 | Responses Structured Outputs/refusal 路径 | schema 只约束结构；仍须来源存在性、页码映射和领域规则校验 |

该能力快照依据 [File inputs](https://developers.openai.com/api/docs/guides/file-inputs#how-it-works)、[File Search](https://developers.openai.com/api/docs/guides/tools-file-search)、[Retrieval](https://developers.openai.com/api/docs/guides/retrieval) 与 [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs)。截至 2026-07-20，[Data controls](https://developers.openai.com/api/docs/guides/your-data#storage-requirements-and-retention-controls-per-endpoint) 显示：`store:false` 只关闭 Responses application-state 存储，不消除默认最长 30 天、可能含 prompt/response 的 abuse-monitoring 日志，也不消除非 ZDR 组织支持模型最长 24 小时的 prompt cache；图像和文件还存在特殊安全审查例外。`/v1/files` 与 `/v1/vector_stores` 的应用状态均保留到删除，且二者均非 Zero Data Retention eligible；API 数据默认不用于训练（除非显式选择分享）不能替代这些留存说明。每个 `policy_snapshot_id` 与 consent UI 必须同时版本化覆盖 Responses、abuse monitoring、prompt cache、图像/文件审查例外、Files 和 Vector Stores。

首版 provider profile 不接受任意 `base_url`、自定义 endpoint、动态 adapter 路径或第三方 plugin。OpenAI Python SDK 是候选实现依赖，但本轮尚未现场核验其许可证；正式选包前须完成许可证核验并记录，不能把 SDK 许可证写成已确认事实。

## 候选实体

### `RemoteMaterialObject`

| 字段 | 语义 |
| --- | --- |
| `id` | 本地不透明 ID；UI/领域层不直接使用 provider ID |
| `course_id`, `material_id`, `batch_id` | 本地归属与原文件引用 |
| `adapter_id`, `provider_profile_id` | 平台注册的 adapter 与用户选择的本地不透明 profile ID |
| `config_fingerprint` | 规范化非秘密有效配置与 adapter/schema 版本的指纹，不包含凭据值 |
| `credential_ref` | 指向本机安全存储的引用；不保存或回显 API key、token、密码 |
| `provider_file_ref` | 加密/受限保存的远端文件引用，不进入普通日志 |
| `provider_association_ref` | 可空的 vector-store file association 引用；与 File、Vector Store 分层对账 |
| `provider_index_ref` | 课程/profile/config 独占 Vector Store 的引用；不得跨课程或配置共享 |
| `content_hash` | 与本地已确认上传版本绑定 |
| `consent_record_id` | 本次实际文件范围的授权证据 |
| `state` | 当前生命周期状态 |
| `created_at`, `updated_at` | UTC instant |
| `capability_snapshot_id` | 调用时 adapter 能力声明的版本化快照 |
| `policy_snapshot_id` | 上传时展示的区域、训练、人工审查、缓存、删除与保留期政策快照 |
| `failure_code` | 可空、白名单、脱敏的失败原因 |

### `RemoteJob`

记录上传、索引、删除或状态对账任务：`job_type`、`object_id`、`idempotency_key`、`attempt`、`not_before`、`deadline`、`state`、`provider_request_ref`。它不保存文件正文、页面图、学生作答或凭据。

## 授权合同

模式 F 的每次新增外发必须展示并记录：

- adapter/provider profile、`config_fingerprint`、目的、文件名/内部 ID、数量、总大小和内容哈希；
- 材料角色（课件、往年卷、老师重点等）与已知版权/敏感提示；
- 预计费用/配额（能估算时）和硬性预算上限；
- 已知区域、留存、训练/人工审查和删除能力；未知项必须明确显示“未知”；
- 允许创建的远端对象类型（文件、索引、缓存/任务）；
- 切换模式、撤销与删除的已知效果和无法保证项。

`ConsentRecord.payload_scope` 必须精确包含本批文件/哈希、`adapter_id`、`provider_profile_id`、`config_fingerprint`、`capability_snapshot_id` 与 `policy_snapshot_id`。更换文件内容、追加文件、更换 profile/adapter、修改影响 endpoint、区域、模型路由、能力或政策的有效配置、从 L/P 切到 F 或撤销后重新启用都需要新记录；不能复用更宽的旧授权。

## 状态机

```text
awaiting_consent -> upload_queued -> uploading -> uploaded -> indexing -> ready
                 -> cancelled
upload_queued -> cancelled

uploading -> upload_failed
uploaded/indexing -> index_failed
upload_failed/index_failed -> retry_queued -> uploading/indexing
uploading/indexing/deleting -> reconcile_required -> duplicate_quarantined
duplicate_quarantined -> ready/delete_requested/delete_incomplete

uploaded/indexing/ready/upload_failed/index_failed
  -> delete_requested -> deleting -> deleted
                                  -> delete_incomplete
delete_incomplete -> delete_requested
delete_requested/deleting/delete_incomplete -> credential_unavailable
credential_unavailable -> delete_requested
```

状态约束：

- `awaiting_consent` 时 provider 上传调用必须为 0。
- adapter/profile 未注册、配置 schema 无效、凭据不可用、能力或政策快照未知时，上传调用必须为 0；不得尝试猜测或自动切换 provider。
- `uploaded` 只表示文件对象存在，不表示索引可用；只有 `ready` 可被模型端口解析。
- `upload_failed` / `index_failed` 保留已知 provider 对象引用，以便对账/删除，不能假定不存在远端残留。
- `cancelled` 只适用于尚无远端对象或已完成清理；否则转入 `delete_requested`。
- `deleted` 后本地仍保留最小化审计与历史来源失效标记，不保留可用于调用的 provider 引用。
- `delete_incomplete` 阻止该对象重新用于模型调用，并展示重试/人工处理方式。
- `delete_incomplete` 只有在新的显式重试/对账动作后才能回到 `delete_requested`，不能后台无限自旋。
- `duplicate_quarantined` 表示对账发现多个可能代表同一逻辑上传的对象；所有候选均不得进入来源范围，直到选定 canonical 对象并对其余对象排队清理。
- `credential_unavailable` 是删除/对账 job 的可恢复阻塞态，不是远端删除证据；只有同 profile 凭据重新录入且用户显式恢复时才能回到 `delete_requested`。

## 上传与索引

1. 校验 consent、文件哈希、类型、大小、配额、profile 配置指纹、provider 能力与政策快照。
2. 使用 `(adapter_id, provider_profile_id, config_fingerprint, policy_snapshot_id, material_id, content_hash, consent_record_id)` 生成幂等键。
3. 上传前再次确认文件当前哈希与授权哈希一致，防止授权后内容被替换。
4. provider 返回对象引用后先持久化，再进入索引；进程崩溃恢复时用 provider 请求引用对账，不盲目重复上传。
5. 多文件批次逐文件记录状态；部分成功不得假报全成功，也不能回滚时遗留未追踪对象。
6. 每个 `(course_id, provider_profile_id, config_fingerprint)` 只创建一个独占 Vector Store；文件不得跨该边界复用 association。每个 association 写入 `scope_token = SHA256(course_id | material_id | content_hash | consent_record_id | config_fingerprint)` 属性。本地记录 token 与 File/association 引用；用户 config 和模型均不能写 token。
7. 每次 File Search 从有效 consent 生成精确 allowed File IDs/tokens，强制使用 `scope_token in [...]` metadata filter，并包含 `file_search_call.results`；返回后逐个验证 result/citation File ID。任一越界即丢弃整次响应并记 `provider_scope_violation`。撤销 token 立即退出 allowlist；attributes/filter/results 能力或范围上限无法证明时 store 进入 `source_disabled`、F 调用为 0。
8. `SourceLocator` 只通过可重放唯一文本匹配生成：provider chunk 与本地逐页文本执行 NFKC、CRLF→LF、去 soft hyphen、连续空白折叠/trim；不少于 32 normalized code points 的连续 span 必须只匹配同 content hash 的唯一一页。零/多页/跨页/过短/视觉-only 均 `source_insufficient`；coverage/exam-analysis 空内容失败，其他三端口仅 `model_supplement`。视觉事实须由已知 locator 的 P 页面/图像请求验证。
9. 本地 worker 以 at-least-once 执行上传/关联/删除 job。幂等键用于本地合并与对账，不视为 provider exactly-once 保证；超时或响应丢失后先查询/列举可见对象。发现同一课程/profile/config/content hash 的多个候选时，全部先退出可用来源范围，记录 `duplicate_quarantined`，确认 canonical 对象后再清理其余对象；无法确认时保持隔离并显示可能的额外费用，不自动重试创建。

## 模式切换

### L/P -> F

- 展示即将新增的文件级外发范围并创建新 consent；
- 既有本地材料、索引、证据和计划不被覆盖；
- 只有状态为 `ready` 的文件进入 F 模式端口来源范围。

### F -> P/L

- 新模型请求立即按更严格模式拒绝 F 远端对象，不等待删除完成；
- 所有适用远端文件/索引进入 `delete_requested`；
- 本地原页、抽取和既有学习证据保留，远端来源标为不可用于新请求；
- 删除全部确认后状态为 `deleted`；任一对象失败则课程显示 `delete_incomplete`，不能把课程设置页显示为“已完全清理”。

### F 中新增/替换材料

- 新增文件是新的 payload scope，必须确认；
- 内容哈希变化创建新 `RemoteMaterialObject`，旧对象先退出可用范围并进入删除流程；
- 不允许就地改写 provider 文件引用后继续沿用旧来源/授权。

### Provider profile 或配置切换

- 新 profile 或有效配置不能就地覆盖 `RemoteMaterialObject` 上的 adapter、指纹、快照或远端引用；
- 切换发生后，旧 profile 下的远端对象立即退出新请求来源范围，并按原 adapter/profile/`credential_ref` 进入删除或对账流程；
- 新 profile 必须先通过注册、schema、凭据状态、能力与政策校验，再展示新的实际 payload 并创建 consent；
- 新 profile 的对象、任务、幂等键和引用与旧 profile 隔离，不能因为文件哈希相同而复用；
- 仅轮换同一安全存储引用下的凭据值不把 secret 写入指纹；若实际账号、项目、区域或数据政策范围改变，则必须产生新 profile/指纹并重新确认。

## 删除与对账

- 删除单份材料时先禁止新检索，再删除其 vector-store file association，随后删除该材料的 base File；课程/profile/config 的独占 Vector Store 继续保留，其他材料仍可检索。删除任一层都不能自动把其他层标为 `deleted`。
- 只有用户删除课程、关闭该课程/profile/config 的 F 模式，且对账证明 store 已无剩余 association 时，才能删除对应 Vector Store。store 仍有任何已知或状态不明关联时必须保留并显示 `delete_incomplete`，不得为了清理单文件而删除整库。
- 若采用到期策略，也必须分别记录 File、association、Vector Store、锚点和预计到期时间，并在到期后逐层对账。
- 应用启动、网络恢复和删除重试时对 `uploading/indexing/deleting` 超时状态进行一次性对账，不能无限轮询或产生任务风暴。
- provider 不支持删除、只支持过期或无法确认缓存清理时，界面显示限制和预计保留期，不得报告 `deleted`。
- 清除凭据前必须列出未完成删除/对账任务并要求二次确认。用户仍可强制清除；此后新调用失败关闭，相关对象和 job 进入 `credential_unavailable`/`delete_incomplete`，远端引用保持隔离且不能用于检索。应用保留不含 secret 的 profile、对象、任务和恢复说明：用户为同一 profile 重新录入可用凭据并显式点击恢复后，只执行一次有界对账/清理；若不恢复凭据，则提供到 provider 控制台人工删除的说明，且在取得可验证删除证据前不得显示 `deleted`。不得自动改用其他 profile/凭据。
- 日志只记录本地对象 ID、job 类型、状态、时间、计量和脱敏错误，不记录 provider 文件名、正文、路径或凭据。

## Provider 适配器最低能力声明

适配器必须以机器可读方式声明：

- `adapter_id`、配置 schema 版本、允许的非秘密字段及其规范化规则；
- 支持的文件类型、单文件/批次大小和并发限制；
- 上传、索引/处理、状态查询、取消和删除能力；
- 文件、索引、缓存/请求的保留与训练/人工审查政策快照来源；
- 是否能返回页码/位置引用；
- 计量/费用可见性、provider 请求引用，以及可用于本地幂等和重复对象对账的能力；没有证据时必须声明不支持 provider exactly-once；
- 区域与数据驻留信息（若已知）；
- 不支持或无法证明的删除范围。

若 adapter 未注册、配置或快照无法验证，或适配器不能提供上传后的对象追踪及任何删除/过期语义，则不能启用模式 F；不得仅凭模型能接收文件就宣称满足本合同。能力不足必须在配置与导入界面显示并失败关闭，不能静默退回另一 provider。

local production registry 只允许平台内置 OpenAI adapter；deterministic mock 只注册在 test/demo profile。内置 OpenAI adapter 必须把 Responses `store:false`/禁用后台与任意托管工具、最长 30 天 abuse monitoring、最长 24 小时 prompt cache、图像/文件审查例外，以及 Files/Vector Stores 的非 ZDR、应用状态直到删除、分层删除和原生页码/视觉保真缺口声明为不可省略的能力/政策字段；config 不能覆盖或伪造这些事实。

## 确定性测试矩阵

| 场景 | 必须验证 |
| --- | --- |
| 无 consent | provider 上传调用为 0，状态保持 `awaiting_consent` |
| 未知 adapter/坏配置/缺失凭据 | provider 上传调用为 0；显示可恢复配置错误且不读取或外发正文 |
| profile/config/policy 切换 | 旧 consent 与远端引用不复用；旧对象退出来源范围，新对象等待新 consent |
| 授权后文件被替换 | 哈希不一致，上传前拒绝且要求重新确认 |
| 重复提交/进程重启/响应丢失 | 本地幂等键合并 at-least-once job；先对账再重试。若已出现重复远端对象，发现后全部隔离，选择 canonical 对象并清理其余对象；不承诺 provider exactly-once 或绝不重复计费 |
| 多文件部分失败 | 每文件状态准确；成功对象可追踪，失败可重试/删除 |
| 上传成功、索引失败 | 保留文件引用并进入 `index_failed`，可删除且不能用于模型端口 |
| 取消发生在上传后 | 自动进入删除流程，不把 `cancelled` 冒充无远端对象 |
| F 切换到 L/P | 新请求立即拒绝 F 来源；远端对象全部排队删除 |
| 删除部分失败 | 课程/对象显示 `delete_incomplete`，其引用不可再调用 |
| provider 不支持删除 | 显示政策限制/过期语义，不产生 `deleted` 假证据 |
| 删除独占 store 中的一份材料 | 只删除该 association + File；store 和其他材料继续可检索，不把课程标为已清理 |
| 删除课程/F 模式 | 先清理所有 association/File；仅在对账证明无剩余关联后删除该课程/profile/config 的独占 store |
| OpenAI File Search 只返回 file citation | 不伪造 locator；映射失败时 coverage/exam-analysis 空 `source_insufficient`，解释/练习/反馈仅 `model_supplement`，权威状态不变 |
| store 含已授权与已撤销材料 | request 必须用 scope-token metadata filter 且结果 File ID 全部属于 allowlist；已撤销命中为 0，越界结果使整次响应失败 |
| locator 文本证明 | 唯一 >=32 字符 span 映射成功；重复页、跨页、过短和视觉-only fixture 全部失败关闭，不猜页码 |
| Responses/Files/Vector Stores 政策快照 | consent 同时显示 `store:false` 的边界、最长 30 天 abuse monitoring、最长 24 小时 prompt cache、图像/文件审查例外，以及 Files/Vector Stores 非 ZDR/直到删除；默认不训练不得覆盖留存说明 |
| config 包含 `base_url`/plugin/未知 endpoint | schema 拒绝，远端调用为 0；不尝试兼容 OpenAI 协议的第三方服务 |
| 凭据被清除 | 新调用失败关闭；未完成删除保持隔离和 `credential_unavailable`/`delete_incomplete`。同 profile 重新录入后仅由用户显式触发一次有界对账；否则显示人工清理说明，不泄露凭据、不自动换 profile、不假报 `deleted` |
| 离线后恢复 | 一次性对账，无无限重试、轮询风暴或重复对象 |
| provider mock 注入/坏状态 | test/demo profile 可确定重放且不改变 consent、课程模式、知识覆盖、计划或掌握状态；local production 不注册 mock |

## 尚未决定

- OpenAI reference adapter 使用的具体模型版本、SDK/HTTP 客户端、区域、费用上限与用户组织资格；SDK 许可证尚未现场核验；
- 平台内置 OpenAI adapter 的非秘密配置字段和稳定 endpoint 清单；任意自定义 endpoint/plugin 已由 D-018 排除，不再作为首版未决项；
- 默认文件/批次容量与并发、超时和重试次数；
- 远端对象本地引用的加密/钥匙串实现；
- 无本地 `SourceLocator` 时的端口语义已固定：coverage/exam-analysis 空内容失败关闭；解释/练习/反馈最多显示 `model_supplement`，不得进入材料事实、覆盖、计划或来源证据；
- 凭据恢复/人工控制台清理的具体界面文案与 provider 控制台深链；上述失败关闭、隔离和显式恢复语义已确定。
