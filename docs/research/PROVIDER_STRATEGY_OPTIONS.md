# Provider 适配策略候选

记录时间：2026-07-20T01:02:00+08:00

## 状态与证据边界

D-014 已确认平台实现 L/P/F 三种材料能力。D-015 随后确认：平台采用统一 `ProviderAdapterRegistry`，由用户在配置/设置中选择平台已实现且声明能力的 provider adapter；平台不硬编码或静默指定默认供应商。本文件保留当时的三种候选比较作为过程证据，不把任何具体 provider 写成已批准部署。

D-015 只确认适配边界和选择权，不选择具体 provider、模型、SDK、区域、数据政策、适配器目录或任意自定义 endpoint。用户配置一个名称并不能让未实现的供应商自动兼容；只有注册表中通过配置校验和能力合同的 adapter 才能进入远端调用路径。

本轮通过 OpenAI Developer Docs MCP 核验到：

- [File search guide](https://developers.openai.com/api/docs/guides/tools-file-search) 展示了先上传文件、创建 vector store、等待文件完成，再通过 File Search 检索；响应可包含文件引用，文档示例使用 PDF。
- [Files delete reference](https://developers.openai.com/api/reference/resources/files/methods/delete) 和 [Vector Stores delete reference](https://developers.openai.com/api/reference/resources/vector_stores/methods/delete) 提供删除入口。
- [Data controls](https://developers.openai.com/api/docs/guides/your-data) 说明 API 数据默认不用于训练（除非显式选择分享）；文档列出 `/v1/files` 与 `/v1/vector_stores` 的应用状态保留为“直到删除”，并说明文件可手动删除或设置 `expires_after`。具体资格、区域和其他政策仍需在实现前复核。

Google/Anthropic 官方站点在 2026-07-20 本轮调查中连接失败，未把其能力或政策当作已验证事实；任何此后纳入支持目录的 adapter 都必须在实现前重新核验官方能力与政策。

## 共同适配器合同

任何真实 provider 都必须声明或实现 `REMOTE_FILE_LIFECYCLE_CONTRACT.md` 要求的能力：

| 能力 | 最低要求 |
| --- | --- |
| 文件上传 | 接受允许的 PDF/材料类型；返回可追踪不透明引用；支持大小/并发错误 |
| 索引/处理 | 可查询处理中、完成、失败；完成前不能用于 F 检索 |
| 引用定位 | 尽可能返回页码/段落；无法定位时明确降级或禁用来源型解释 |
| 删除/过期 | 能明确报告删除、过期或不支持；未知状态不能显示 `deleted` |
| 幂等/重试 | 支持客户端幂等键或可安全对账，避免重复对象/计费 |
| 数据政策 | 提供区域、留存、训练/人工审查、缓存和删除说明的版本快照 |
| 计量/预算 | 返回可用的用量/费用信号，或明确“不提供估算” |
| 配置 | 提供版本化的非秘密配置 schema、能力快照与政策快照；未知字段、未知 adapter 或不满足端口能力时失败关闭 |
| 安全 | adapter 只通过 `credential_ref` 从安全存储解析凭据；不接受模型自由生成的文件路径、URL、凭据或工具参数 |

适配器返回统一的 provider-neutral 状态和错误码；领域层不依赖 provider 文件 ID、SDK 异常或供应商术语。

## 已确认的配置边界

用户配置保存为 provider profile，至少区分：

- `profile_id` 与平台注册的 `adapter_id`；
- adapter 允许的模型、区域、预算及其他非秘密配置；
- `config_fingerprint`、`capability_snapshot_id` 与 `policy_snapshot_id`；
- 指向本机安全存储的 `credential_ref`，而不是 API key、token 或密码明文。

`config_fingerprint` 只覆盖规范化后的非秘密有效配置和 adapter/schema 版本，不包含凭据值。凭据必须隐藏录入，配置页面只显示状态并支持更新/清除；普通配置文件、浏览器持久化、日志、快照和 Git 均不得出现凭据明文。

未知 adapter、无效配置、缺失凭据、无法核验的能力或不满足当前端口要求时，远端调用失败关闭；模式 L 仍可使用。更换 profile 或改变会影响 provider、endpoint、区域、模型路由、能力或政策的有效配置，必须形成新的配置/政策快照，并重新取得与实际 payload 绑定的 consent。

## 历史候选：三种策略

### 1. 统一适配器 + 一个真实参考 provider（推荐）

先实现 `ProviderAdapter` 接口、完整 mock 和一个经过官方文档/政策核验的参考 provider；其他 provider 只需满足同一能力声明后再接入。

优点：能真实验证 L/P/F 和凭据/删除链路，同时把供应商特性隔离；测试可在 mock 下完成；未来替换 provider 的返工范围可控。

风险：参考 provider 仍会影响首版体验；需要把其不支持的引用、删除或留存能力如实暴露，不能假装跨 provider 一致。

### 2. 单 provider 紧耦合

直接围绕一家 provider 的 SDK、文件接口和模型能力实现 L/P/F。

优点：初期代码和配置最少。

风险：供应商政策、区域、价格或 API 变化会直接改写领域层；整份模式和删除合同难以迁移；课程评审难区分业务逻辑与 SDK 偶然行为。

### 3. 第一版实现多个真实 provider

同时交付两家或更多 provider 的上传、索引、引用、删除和政策展示，并让用户选择。

优点：用户选择更广，能展示适配器价值。

风险：每家都有不同的文件生命周期、引用质量、数据政策和错误语义；会显著扩大凭据、成本、UI、测试和课程交付范围。当前 Google/Anthropic 官方证据尚未完成核验，不能直接承诺。

## 原推荐与最终选择

当时推荐策略 1。它与用户“平台实现能力、外发由用户决定”的要求一致：平台提供 L/P/F，用户选择课程模式和 provider；adapter/政策层保证每次实际文件范围仍需授权。

- 当时若选择策略 1：下一步需再选一个参考 provider，并拆分 adapter、mock、政策快照和 F 生命周期测试。
- 当时若选择策略 2：范围可缩小，但 provider 特性会进入领域层，替换成本更高。
- 当时若选择策略 3：需要为每家 provider 分配独立凭据、政策核验和端到端测试。

D-015 的最终回答没有指定参考 provider 或要求第一版同时支持多家真实供应商，而是确认统一 adapter registry 与用户配置。由此确定：

- 平台维护支持目录、adapter 代码、统一合同、mock 与适配器合同测试；
- 用户只从已支持、能力可见的 provider profile 中选择，未配置时不产生远端调用；
- 首版具体 adapter 目录及是否允许自定义 endpoint 仍未决定；在明确确认前，不能把任意 endpoint 当作已授权能力；
- 选择 provider profile 不代替材料外发 consent，配置切换也不能复用旧 consent 或远端对象引用。

## 不应由 provider 决定的事项

- 课程模式、是否上传、实际 payload 范围和用户确认；
- 知识覆盖、计划、优先级、掌握状态和删除成功语义；
- 是否把模型输出当作课件事实；
- 是否绕过本地原页、页码引用和学术诚信边界。
