# 整份课程材料远端生命周期合同

记录时间：2026-07-20T00:57:31+08:00

## 状态与范围

D-014 已确认第一版实现整份 PDF/课程远端处理（模式 F），并由用户决定是否使用。D-015 确认平台使用统一 `ProviderAdapterRegistry`，用户在配置/设置中选择平台已实现的 provider adapter。本文件定义 provider 无关的配置、授权、上传、索引、使用、切换和删除合同；不选择具体 provider、SDK、模型、区域、留存政策、费用、适配器目录、任意 endpoint 或凭据存储实现。

## 核心原则

1. **能力不等于授权**：平台实现模式 F，不代表任何课程或文件默认外发。
2. **课程选择不等于未来文件授权**：课程记住 F 模式，但每个新增批次都要展示实际文件和范围并确认。
3. **远端对象不替代本地来源**：原 PDF、页码、原始抽取、用户修正和内容哈希仍是权威来源身份。
4. **外发与权威状态隔离**：上传/索引成功不能自动确认知识覆盖、提高掌握或激活计划。
5. **删除是可观察过程**：只有 provider 明确确认或合同定义的终态才能显示 `deleted`；否则显示 `delete_incomplete`。
6. **配置不等于凭据或授权**：provider profile 只保存非秘密配置和 `credential_ref`；选择或修改 profile 不自动获得材料外发 consent。

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
| `provider_index_ref` | 可空的远端索引/知识库引用 |
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

uploaded/indexing/ready/upload_failed/index_failed
  -> delete_requested -> deleting -> deleted
                                  -> delete_incomplete
delete_incomplete -> delete_requested
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

## 上传与索引

1. 校验 consent、文件哈希、类型、大小、配额、profile 配置指纹、provider 能力与政策快照。
2. 使用 `(adapter_id, provider_profile_id, config_fingerprint, policy_snapshot_id, material_id, content_hash, consent_record_id)` 生成幂等键。
3. 上传前再次确认文件当前哈希与授权哈希一致，防止授权后内容被替换。
4. provider 返回对象引用后先持久化，再进入索引；进程崩溃恢复时用 provider 请求引用对账，不盲目重复上传。
5. 多文件批次逐文件记录状态；部分成功不得假报全成功，也不能回滚时遗留未追踪对象。
6. 索引完成后建立本地来源到 provider 对象/页码的映射；无法定位页码时标为保真限制，不能伪造引用。

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

- 删除顺序遵循 provider 合同，通常先禁止新检索，再删除索引/知识库关联，最后删除文件对象；具体顺序由适配器显式声明。
- 应用启动、网络恢复和删除重试时对 `uploading/indexing/deleting` 超时状态进行一次性对账，不能无限轮询或产生任务风暴。
- provider 不支持删除、只支持过期或无法确认缓存清理时，界面显示限制和预计保留期，不得报告 `deleted`。
- 清除凭据前检查未完成删除任务；用户仍可强制清除，但应用要显示此举可能使远端清理无法继续，并保留脱敏恢复说明。
- 日志只记录本地对象 ID、job 类型、状态、时间、计量和脱敏错误，不记录 provider 文件名、正文、路径或凭据。

## Provider 适配器最低能力声明

适配器必须以机器可读方式声明：

- `adapter_id`、配置 schema 版本、允许的非秘密字段及其规范化规则；
- 支持的文件类型、单文件/批次大小和并发限制；
- 上传、索引/处理、状态查询、取消和删除能力；
- 文件、索引、缓存/请求的保留与训练/人工审查政策快照来源；
- 是否能返回页码/位置引用；
- 计量/费用可见性和请求幂等能力；
- 区域与数据驻留信息（若已知）；
- 不支持或无法证明的删除范围。

若 adapter 未注册、配置或快照无法验证，或适配器不能提供上传后的对象追踪及任何删除/过期语义，则不能启用模式 F；不得仅凭模型能接收文件就宣称满足本合同。能力不足必须在配置与导入界面显示并失败关闭，不能静默退回另一 provider。

## 确定性测试矩阵

| 场景 | 必须验证 |
| --- | --- |
| 无 consent | provider 上传调用为 0，状态保持 `awaiting_consent` |
| 未知 adapter/坏配置/缺失凭据 | provider 上传调用为 0；显示可恢复配置错误且不读取或外发正文 |
| profile/config/policy 切换 | 旧 consent 与远端引用不复用；旧对象退出来源范围，新对象等待新 consent |
| 授权后文件被替换 | 哈希不一致，上传前拒绝且要求重新确认 |
| 重复提交/进程重启 | 幂等键相同，不创建重复远端文件或重复计费 job |
| 多文件部分失败 | 每文件状态准确；成功对象可追踪，失败可重试/删除 |
| 上传成功、索引失败 | 保留文件引用并进入 `index_failed`，可删除且不能用于模型端口 |
| 取消发生在上传后 | 自动进入删除流程，不把 `cancelled` 冒充无远端对象 |
| F 切换到 L/P | 新请求立即拒绝 F 来源；远端对象全部排队删除 |
| 删除部分失败 | 课程/对象显示 `delete_incomplete`，其引用不可再调用 |
| provider 不支持删除 | 显示政策限制/过期语义，不产生 `deleted` 假证据 |
| 凭据被清除 | 新调用失败关闭；未完成删除显示可恢复限制，不泄露凭据 |
| 离线后恢复 | 一次性对账，无无限重试、轮询风暴或重复对象 |
| provider mock 注入/坏状态 | 不改变 consent、课程模式、知识覆盖、计划或掌握状态 |

## 尚未决定

- 首版支持的具体 adapter/provider 目录、SDK、模型、区域、数据政策和费用上限；
- 是否允许任意自定义 endpoint；D-015 未对此授权；
- 默认文件/批次容量与并发、超时和重试次数；
- 远端对象本地引用的加密/钥匙串实现；
- provider 不支持页码引用时模式 F 是否降级为仅候选上下文或禁用；
- 用户强制清除凭据但仍有未完成删除时的最终恢复 UX。
