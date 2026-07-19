# 首版真实参考 Provider 候选

## 状态与证据边界

D-016 已确认首版只交付一个真实参考 adapter，外加统一接口、完整 mock 和 contract suite。本文件只比较参考实现候选，不把任何一家写成已选择，也不读取真实 key、不调用付费 API、不上传课程材料。

OpenAI 的 File Search、Files/Vector Stores 删除和 Data controls 已通过官方开发文档核验；Google 和 Anthropic 的官方链接已定位，但本轮部分页面因官方检索 503/TLS 失败未能取得完整现场快照。所有候选的模型版本、SDK 许可证、区域、留存/训练政策和费用在实现前仍须重新核验。

## 共同硬门槛

参考 adapter 必须在真实实现前声明并测试：

- P：已确认页面/片段的 PDF、图像或文本输入；
- F：文件上传、异步处理/索引状态、引用定位、对象追踪、删除/过期和失败对账；
- 结构化模型端口：schema、拒答/错误、超时、预算和幂等；
- 安全：服务端凭据、无任意模型工具、政策快照和未知能力失败关闭。

当前课程合同要求“课件事实可回到本地 `source_id` 与页码”。provider 原生引用如果只有文件名、URI 或文本片段，不能直接升级为权威页码；必须本地映射并校验，或禁用依赖该能力的 F 路径。

## 候选比较

| 候选 | P（页/片段） | F 生命周期 | 页码/视觉引用 | 政策与许可证风险 | 与当前合同的匹配 |
| --- | --- | --- | --- | --- | --- |
| OpenAI API | PDF/图像输入和结构化输出路径清晰；适合按批准页面调用 | Files + Vector Stores/File Search 有上传、异步 ready、删除和过期语义；需追踪 base file 与 vector-store association | 原生 File Search citation 主要是 file ID/filename；PDF 页码和 File Search 视觉保真不能直接假定，需本地页映射或降级 | API 数据默认不用于训练（除非 opt-in），但文件/向量库应用状态通常直到删除；SDK 许可证和具体政策需实现前复核 | **最高，但有页码/视觉缺口** |
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

## 工程推荐（不是学生选择）

按当前已经写入的 F 状态机，OpenAI 的上传/索引/删除/过期对象最接近现有合同，因此暂列为推荐候选；但必须把“原生页码引用不足、File Search 视觉保真未验证、删除 eventually consistent”写成 capability snapshot 和失败关闭测试。若学生选择 Gemini 或 Claude，需先修订 F 合同与相应验收，不得只替换 SDK 名称。
