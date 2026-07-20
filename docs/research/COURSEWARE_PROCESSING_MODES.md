# 课程材料处理模式比较

记录时间：2026-07-19T22:40:53+08:00

## 状态

本文响应学生提出的“本地解析可能使课件失真，应让用户选择”这一要求。它比较处理模式并定义共同质量证据。D-009 已确认首次导入必须显式选择并按课程记住，低保真检测不能静默升级；D-014 已确认第一版正式提供 L/P/F 三种模式；D-015 已确认平台提供 provider-neutral adapter registry，用户从已支持且能力检查通过的非敏感配置中选择 provider；D-016 确认首版一个真实 adapter + 完整 mock；D-017 选择 OpenAI 作为唯一真实参考 adapter；D-018 确认只允许平台内置 adapter，不开放任意自定义 endpoint 或第三方 plugin。具体 OpenAI 模型、SDK、区域和费用仍未选择。

## 操作系统课件量化证据

对 15 份 PDF 的 932 页使用 bundled `pypdf` 做全量文本/资源结构检查，结果如下：

| 指标 | 结果 | 含义与限制 |
| --- | ---: | --- |
| 成功检查页数 | 932 | 与文件页数合计一致，页面级异常为 0 |
| 空文本页 | 0 | 所有页面都有可抽取文字，但不证明阅读顺序、公式或图表语义正确 |
| 少于 40 个非空白字符的页面 | 0 | 没有完全依赖图片的极低文本页 |
| 少于 100 个非空白字符的页面 | 95 | 约 10.2% 页面文字较少，视觉内容可能更重要 |
| 每页文本字符中位数 | 226 | 课件整体有较丰富的文字层 |
| 每页文本字符均值 | 247.1 | 不能单独用于判断页面难度或完整性 |
| NFKC 归一化会改变文本的页面 | 932 | PDF 字体映射产生兼容字符；需要同时保留原始抽取与归一化文本 |
| Unicode replacement character | 0 | 未出现明显的 `U+FFFD` 解码替换，但仍可能有顺序/符号语义问题 |
| 含图像 XObject 的页面 | 932 | 可能包含校徽、背景或内容图片，不能推断每个图像都承载教学语义 |
| 含 Form XObject 的页面 | 87 | 存在额外的矢量/复合页面结构，需要保留原页视觉引用 |

分组文本中位数：绪论 209、并发 272、虚拟化 200.5、持久化 215 个非空白字符/页。所有组都同时具有文本与视觉处理需求。

统计过程出现一个工具编排问题：长时间 Python 子进程的 stdout 未被外层终端捕获，且 JSON 在外层返回后才落盘。最终 JSON 完整覆盖 932 页并报告 0 个页面错误，但这次运行不能作为产品性能基准。

## 第一版正式模式目录

### 模式 L：本地解析与原页对照

**数据流**：PDF 留在本机；提取原始文本、归一化文本、页码与页面图；本地索引用于检索和复习状态。

**优点**：课程内容不外发；无需云端文件生命周期；可离线浏览和检索。

**主要失真风险**：

- 公式、代码、分栏文本和阅读顺序可能错误；
- 图片/图表语义不会自动进入纯文本；
- NFKC 归一化可能改变技术符号，不能覆盖原始文本；
- 解析器“成功”不等于课程内容被完整理解。

**最低 UI 要求**：解释旁显示原始幻灯片与页码；提供原始/归一化文本对照；标记低文本、解析警告和视觉依赖页面；用户可纠正知识点/页码关联。

### 模式 P：选定页面的云端多模态处理

**数据流**：本地保存课程结构；每次学习任务把学生明确选择或系统检索后由学生确认的少量页面图像、文本和问题，经用户选定的 provider profile/config/policy snapshot 发送给能力匹配的云端模型。

**OpenAI 首版映射**：[File inputs](https://developers.openai.com/api/docs/guides/file-inputs#how-it-works) 说明具备视觉能力的模型通过 Responses 接收 PDF `input_file` 时会同时获得抽取文本与逐页图像，因此该 adapter 可为已授权页面/PDF 请求保留视觉上下文。所有 `/v1/responses` 请求固定为前台 `store:false`，禁用 background、Conversations、远程 MCP 和 Hosted Shell/Code Interpreter 等执行型 hosted tools；调用仍须由平台内置 endpoint 映射完成，用户 config 不能提供任意 `base_url` 或 plugin。

**优点**：模型能同时看到版面、图表、公式与文字；外发范围可控制到页面级；成本和审计相对可控。

**主要风险**：页面仍属于课程材料外发；选页错误会丢上下文；每个 endpoint 的多模态能力、留存、训练和区域政策需逐项核验；多模态请求成本更高。未知或能力不足的 profile 必须禁用 P，而不是尝试通用兼容。

**最低 UI 要求**：调用前显示 provider profile、endpoint 标识、配置/政策版本、页面缩略图、页码、文本片段和估算成本；允许删减；调用记录只保存内部引用与状态，不在普通日志复制正文。

### 模式 F：整份 PDF 或课程云端处理

**数据流**：把一份或多份原 PDF 经用户选定的 provider profile/config/policy snapshot 上传到能力声明完整的文件/知识库接口，由该配置对应的 adapter 执行解析、检索、对账和删除。

**OpenAI 首版映射**：[File Search](https://developers.openai.com/api/docs/guides/tools-file-search) 使用 Files/Vector Stores，并要求文件关联达到 `completed` 后再检索；File Search 只由 adapter 绑定已授权 store，不向模型开放任意工具分发。每个课程/profile/config 使用独占 Vector Store；删除单份材料只删除其 association + File，只有删除课程/F 且对账证明无剩余 association 时才删除 store。该托管检索的示例 citation 只有 `file_id`/`filename`，没有原 PDF 页码或页面区域，其视觉保真也未被证明。

**优点**：供应商可以获得完整文档上下文，减少本地解析实现负担；部分服务可能提供更好的多模态理解。

**主要风险**：外发与版权范围最大；195 MB/932 页可能触及 endpoint 的文件、token、费用和处理时长限制；远端文件删除、缓存和索引生命周期更复杂；难以证明模型实际引用了哪一页。截至 2026-07-20，[OpenAI Data controls](https://developers.openai.com/api/docs/guides/your-data#storage-requirements-and-retention-controls-per-endpoint) 说明 `store:false` 不消除默认最长 30 天 abuse-monitoring 日志、非 ZDR 组织支持模型最长 24 小时 prompt cache 或图像/文件安全审查例外；`/v1/files` 与 `/v1/vector_stores` 仍非 ZDR、应用状态保留到删除。policy snapshot 必须覆盖 Responses + Files + Vector Stores 的完整留存面，默认不用于训练不能被解释为请求后无留存。若上传、索引、引用、本地页映射、对象追踪或删除/过期语义未确认，F 必须失败关闭。

**最低 UI 要求**：导入前显示文件清单、总大小、provider profile、endpoint、能力/政策快照和预计成本；独立授权；显示上传/索引/删除状态；切换 profile/config 或离开该模式时提供旧配置下的远端删除并说明无法保证的部分。

模式 F 的对象、状态、幂等、切换和删除合同见 `docs/research/REMOTE_FILE_LIFECYCLE_CONTRACT.md`。

## 所有模式共有的合同

1. **模式作用域**：保存到课程级；每次学习任务可临时使用更严格模式。任何扩大外发范围的覆盖都要重新确认。
2. **来源可追溯**：解释、题目和知识状态都引用课件文件与页码；模型补充内容与课件内容分开标记。
3. **原页始终可见**：本地抽取或云端解释都不能取代用户查看原始幻灯片。
4. **质量报告**：导入后显示页数、解析错误/警告、低文本页、归一化变化与无法识别的视觉页。
5. **无静默升级**：本地模式遇到低置信度时只能提示切换，不能自行上传页面或文件。
6. **可撤销**：用户能修改课程模式，并看到需要清理的本地索引、远端文件和缓存状态。
7. **可测试**：供应商客户端使用 mock 验证无确认调用为零、请求只含已批准页面、模式变更不复用更宽授权。
8. **受约束模型端口**：远端模型只能接收当前端口允许的来源 ID 和页面/片段；响应是候选并经过 schema/来源校验，详见 `docs/research/CONSTRAINED_AI_PORT_CONTRACT.md`。
9. **Provider registry 与失败关闭**：首版真实路径只允许平台内置 OpenAI adapter；用户只能选择 registry 当前支持、endpoint 已确认且能力满足当前模式的 profile。未知 adapter、任意 `base_url`/plugin、未确认 endpoint 或能力不足时只保留可用模式，不尝试猜测 OpenAI 协议兼容性。
10. **配置、授权与引用隔离**：config 只保存非敏感字段和 `credential_ref`，不保存 secret；每个 `ConsentRecord` 和远端对象绑定不可变的 profile/config/policy snapshot，切换 adapter、endpoint、模型、区域或政策后不得复用旧授权、幂等键或远端引用。
11. **来源与计划隔离**：无版本匹配且可打开的本地 `SourceLocator` 时，不得产生“基于材料”的事实或进入知识覆盖/计划；coverage/exam-analysis 返回空 `source_insufficient`，解释/练习/反馈最多显示 `model_supplement`。
12. **真实重试边界**：真实 OpenAI adapter 只承诺本地幂等与 at-least-once job。响应丢失时先发现、隔离、对账和清理重复对象，不承诺 exactly-once 或绝不重复计费；deterministic mock 只用于 test/demo，local production 不注册 mock。
13. **凭据清除恢复**：强制清除凭据后，未完成删除退出来源范围并保持 `credential_unavailable`/`delete_incomplete`；只有同 profile 凭据重新录入并由用户显式恢复后才做一次有界对账，否则提供人工清理说明且不假报 `deleted`。

## 导入质量报告候选字段

- 文件名、文件哈希、页数、大小和解析器版本；
- 原始文本/归一化文本是否可用；
- 空文本页、低文本页与解析警告列表；
- 页面是否含图像/复合对象（仅作视觉依赖提示，不直接判定语义重要性）；
- 课件文件与渲染页的一致性抽样结果；
- 当前模式、provider profile/config/policy snapshot、允许外发范围与最近一次用户确认时间；
- 本地/远端派生数据的状态与清除入口。

## 尚未决定

- OpenAI reference adapter 的具体模型版本、SDK/HTTP 客户端、固定 endpoint 清单、区域、费用与用户组织数据控制资格；SDK 许可证尚未现场核验；
- 任意自定义 endpoint/plugin 已由 D-018 排除；未来新增 provider 必须走平台内置 adapter、许可证/政策核验与 contract suite，不是首版配置项；
- OpenAI File Search 缺少原生页码/视觉保真证明时，具体端口选择“无权威材料引用的补充”还是失败关闭；两者都不得产生材料事实或进入知识覆盖/计划；
- 自动标记“需要视觉理解”的准确规则；
- 质量报告的失败阈值和阻塞条件。
