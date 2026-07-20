# 首版真实参考 Provider：候选与最终选择

## 状态与证据边界

D-016 已确认首版只交付一个真实参考 adapter，外加统一接口、完整 mock 和 contract suite。D-017 已选择 OpenAI 作为该唯一真实参考 adapter；D-018 已选择只允许平台内置 adapter，不开放任意自定义 endpoint 或第三方 plugin。下方 Google/Anthropic 内容保留为 brainstorming 历史候选，不属于首版支持承诺。本轮不读取真实 key、不调用付费 API、不上传课程材料。

OpenAI 的 PDF file inputs、File Search、Files/Vector Stores 生命周期、Structured Outputs 和 Data controls 已通过官方开发文档核验。Google 和 Anthropic 的官方链接保留为历史入口，但本轮部分页面因官方检索 503/TLS 失败未能取得完整现场快照。所有候选的模型版本、区域、费用和动态政策在实现前仍须重新核验；OpenAI Python SDK 的许可证本轮也尚未现场读取/核验，不能提前写成已确认许可证。

## D-017/D-018 最终选择：OpenAI 内置参考 adapter

local production registry 只注册平台实现的 OpenAI reference adapter；deterministic mock 只注册在 test/demo profile。用户可在 config 中选择平台提供的 OpenAI profile、允许的模型/预算等非秘密字段以及 `credential_ref`；config 不接受任意 `base_url`、任意 endpoint、动态模块路径或第三方 plugin。未注册字段/adapter、坏配置、能力不足或政策未知均在读取材料正文前失败关闭，不能回退到 mock。

截至 2026-07-20 的官方能力/政策快照：

- [File inputs](https://developers.openai.com/api/docs/guides/file-inputs#how-it-works)：具备视觉能力的模型接收 PDF `input_file` 时，API 会抽取文本并把逐页图像一并送入模型。这为模式 P 或受控直接 PDF 请求提供视觉路径，但不等价于 File Search 的视觉保真。
- [File Search](https://developers.openai.com/api/docs/guides/tools-file-search)：Responses 可通过托管 File Search 对 vector store 中已上传文件做语义/关键词检索；文件关联需等待 `completed` 后才可用。示例 `file_citation` 只含 `file_id`、`filename` 和文本输出索引，未给出原 PDF 页码/页面区域。
- [Retrieval / vector stores](https://developers.openai.com/api/docs/guides/retrieval)：vector store 是 File Search/语义检索的索引对象，支持文件关联、状态和过期策略；适配器必须分别追踪 File、vector store 及其 association，不能把三者压成一个不可对账 ID。
- [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs)：Responses 支持按 schema 解析输出并有独立 refusal 路径；官方同时说明结构化输出仍可能存在内容错误，所以它只降低格式风险，不能替代来源存在性和领域不变量校验。
- [Data controls](https://developers.openai.com/api/docs/guides/your-data#storage-requirements-and-retention-controls-per-endpoint)：首版 `/v1/responses` 全部为前台请求并显式发送 `store:false`，但这只关闭 Responses application-state 存储，不消除默认最长 30 天、可能含 prompt/response 的 abuse-monitoring 日志，也不消除非 ZDR 组织支持模型最长 24 小时的 prompt cache；图像/文件还有特殊安全审查例外。`/v1/files` 与 `/v1/vector_stores` 的应用状态均为“直到删除”，二者均非 Zero Data Retention eligible。API 数据默认不用于训练（除非显式选择分享）不能替代上述留存说明。

因此 OpenAI adapter 的已知缺口不是“能否收 PDF”，而是**原生页码 citation 与 File Search 视觉保真没有被官方合同证明**。首版必须以本地版本匹配的 `SourceLocator` 为权威来源；无法映射时 coverage/exam-analysis 返回空 `source_insufficient`，解释/练习/反馈最多标为 `model_supplement`，均不得产生材料事实、进入知识覆盖/`StudyFocus`/计划。不能把 `file_id`/文件名伪装成 locator。

首版禁用 background、Conversations、远程 MCP，以及 Hosted Shell/Code Interpreter 等执行型 hosted tools；模式 F 的 File Search 只由 adapter 绑定已授权 Vector Store，不开放任意工具分发。每个 `(course_id, provider_profile_id, config_fingerprint)` 独占一个 Vector Store；删除单份材料只删除该 association 与 File，只有删除课程/F 且对账证明无剩余 association 时才删除 store。`policy_snapshot_id` 必须共同覆盖 Responses、abuse monitoring、prompt cache、图像/文件审查例外、Files 与 Vector Stores。

## 共同硬门槛

参考 adapter 必须在真实实现前声明并测试：

- P：已确认页面/片段的 PDF、图像或文本输入；
- F：文件上传、异步处理/索引状态、引用定位、对象追踪、删除/过期和失败对账；
- 结构化模型端口：schema、拒答/错误、超时、预算、本地幂等和 at-least-once 对账；真实 provider 不承诺 exactly-once/绝不重复计费；
- 安全：服务端凭据、无任意模型工具、政策快照和未知能力失败关闭。

当前课程合同要求“材料事实可回到本地 `SourceLocator`”。provider 原生引用如果只有文件名、URI 或文本片段，不能直接升级为权威 locator；必须本地映射并校验。失败时 coverage/exam-analysis 空内容关闭，其他三端口仅可 `model_supplement`，不能产生材料事实或进入计划。

## 候选比较

| 候选 | P（页/片段） | F 生命周期 | 页码/视觉引用 | 政策与许可证风险 | 与当前合同的匹配 |
| --- | --- | --- | --- | --- | --- |
| OpenAI API（D-017 已选） | Responses 的 PDF `input_file` 在视觉模型上同时使用抽取文本与逐页图像；Structured Outputs 可约束响应 schema | Files + Vector Stores/File Search 有上传、文件关联、异步 `completed`、删除和过期语义；需分别追踪 File、vector store 与 association | 原生 File Search citation 示例只有 file ID/filename；原 PDF 页码与 File Search 视觉保真未被证明，缺少本地 locator 时只能无权威引用补充或禁用端口 | API 数据默认不用于训练（除非 opt-in），但 Files/Vector Stores 非 ZDR 且应用状态直到删除；SDK 许可证尚未现场核验 | **首版唯一真实 adapter；有页码/视觉缺口** |
| Google Gemini API | PDF/图像理解和 structured output 强；适合 P | Files API 临时对象与 File Search Store/Document 是多层生命周期；需同时追踪过期、索引和删除 | 官方 grounding 元数据不能直接承诺原 PDF 页码/区域；需本地切页和二次校验 | unpaid/paid 数据政策不同，单凭 key 不能判定；官方 Python SDK 为 Apache-2.0（实现前复核） | P 强，F/政策匹配中等 |
| Anthropic Claude API | PDF/图像和 citations 适合 P | Files API 是可复用文件对象，但没有与当前合同直接对应的 provider 托管向量索引状态；F 需本地检索/分批编排 | 结构化 PDF `page_location` 是优势，但物理页仍需映射到本地来源；不能替代索引合同 | API 默认训练政策相对清晰，但留存、ZDR、缓存和文件删除仍需快照；官方 SDK 为 MIT（实现前复核） | P 强，F 需改变/扩展合同 |

## 官方资料入口

### OpenAI

- [File inputs](https://developers.openai.com/api/docs/guides/file-inputs)
- [File Search](https://developers.openai.com/api/docs/guides/tools-file-search)
- [Retrieval / vector stores](https://developers.openai.com/api/docs/guides/retrieval)
- [Structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs)
- [Your data](https://developers.openai.com/api/docs/guides/your-data)
- [Python SDK](https://github.com/openai/openai-python)

### Google Gemini

- [Document processing](https://ai.google.dev/gemini-api/docs/document-processing)
- [Files API](https://ai.google.dev/gemini-api/docs/files)
- [File Search](https://ai.google.dev/gemini-api/docs/file-search)
- [Structured output](https://ai.google.dev/gemini-api/docs/structured-output)
- [Terms and data policy](https://ai.google.dev/gemini-api/terms)
- [Python SDK](https://github.com/googleapis/python-genai)

### Anthropic Claude

- [PDF support](https://platform.claude.com/docs/en/build-with-claude/pdf-support)
- [Files API](https://platform.claude.com/docs/en/build-with-claude/files)
- [Citations](https://platform.claude.com/docs/en/build-with-claude/citations)
- [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
- [Commercial terms](https://www.anthropic.com/legal/commercial-terms)
- [Python SDK](https://github.com/anthropics/anthropic-sdk-python)

## 历史工程推荐与选择后的约束

历史推荐 OpenAI，因为其上传、索引、删除和过期对象最接近现有 F 状态机；D-017 已采纳该推荐。实现仍必须把“`store:false` 的边界、最长 30 天 abuse monitoring、最长 24 小时 prompt cache、图像/文件审查例外、原生页码引用不足、File Search 视觉保真未被官方合同证明、Files/Vector Stores 非 ZDR 且应用状态直到删除”写入 capability/policy snapshot 和失败关闭测试。真实 adapter 只能提供本地幂等与 at-least-once 恢复；响应丢失时先发现/隔离/对账/清理重复对象，不能承诺 provider exactly-once 或绝不重复计费。凭据被强制清除时，未完成删除保持隔离；仅在同 profile 凭据被重新录入并由用户显式恢复后做一次有界对账，否则显示人工控制台清理说明。D-018 同时排除把 Gemini、Claude 或兼容 OpenAI 协议的任意 URL 作为 config 即插即用；未来新增 provider 需先修订支持目录、完成许可证/政策核验和独立 contract suite，不得只替换 SDK 名称或 `base_url`。
