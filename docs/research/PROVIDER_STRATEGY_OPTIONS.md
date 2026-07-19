# Provider 适配策略候选

记录时间：2026-07-20T01:02:00+08:00

## 状态与证据边界

D-014 已确认平台实现 L/P/F 三种材料能力，但尚未选择实际 provider、模型或数据政策。本文件只比较第一版适配策略，不把任何 provider 写成已批准部署。

本轮通过 OpenAI Developer Docs MCP 核验到：

- [File search guide](https://developers.openai.com/api/docs/guides/tools-file-search) 展示了先上传文件、创建 vector store、等待文件完成，再通过 File Search 检索；响应可包含文件引用，文档示例使用 PDF。
- [Files delete reference](https://developers.openai.com/api/reference/resources/files/methods/delete) 和 [Vector Stores delete reference](https://developers.openai.com/api/reference/resources/vector_stores/methods/delete) 提供删除入口。
- [Data controls](https://developers.openai.com/api/docs/guides/your-data) 说明 API 数据默认不用于训练（除非显式选择分享）；文档列出 `/v1/files` 与 `/v1/vector_stores` 的应用状态保留为“直到删除”，并说明文件可手动删除或设置 `expires_after`。具体资格、区域和其他政策仍需在实现前复核。

Google/Anthropic 官方站点在 2026-07-20 本轮调查中连接失败，未把其能力或政策当作已验证事实；需要在 provider 选择后重新核验。

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
| 安全 | 服务端凭据调用；不接受模型自由生成的文件路径、URL 或工具参数 |

适配器返回统一的 provider-neutral 状态和错误码；领域层不依赖 provider 文件 ID、SDK 异常或供应商术语。

## 三种策略

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

## 推荐与选择影响

推荐策略 1。它与用户“平台实现能力、外发由用户决定”的要求一致：平台提供 L/P/F，用户选择课程模式和 provider；adapter/政策层保证每次实际文件范围仍需授权。

- 选择策略 1：下一步需再选一个参考 provider；PLAN 拆分 adapter、mock、政策快照和 F 生命周期测试。
- 选择策略 2：SPEC/PLAN 可缩小，但 provider 特性会进入领域层，替换成本更高。
- 选择策略 3：需要在 PLAN 中为每家 provider 分配独立任务、凭据和端到端测试，并先完成官方资料核验。

## 不应由 provider 决定的事项

- 课程模式、是否上传、实际 payload 范围和用户确认；
- 知识覆盖、计划、优先级、掌握状态和删除成功语义；
- 是否把模型输出当作课件事实；
- 是否绕过本地原页、页码引用和学术诚信边界。
