# 第一版用户与运行边界对比基线

记录时间：2026-07-19
最近决策更新：2026-07-20（D-021 至 D-024）

## 状态与目的

本文为 D-010 提供工程证据。学生随后确认采用“单用户、本地优先”作为第一版路线；比较仍保留用于说明选择依据和未来迁移代价。比较对象是：

1. 单用户、本地优先 WebUI；
2. 单用户、云端个人实例；
3. 多用户 Web 服务。

三种路线都必须保留已经确认的 M1 课程材料与保真、M2 适配解释与理解检查、M3 掌握状态与持续复习，以及跨模块安全/凭据/审计控制。差异主要发生在信任边界、数据位置、身份、凭据和运维责任。

## 决策结果

- 第一版只服务学生本人，私有课件、索引和学习状态默认留在本机；
- 课程硬性要求 WebUI，因此基线是浏览器访问 localhost 应用；桌面窗口可作为后续可选壳，但不能替代 WebUI；
- 第一版不实现注册、登录、多租户、课件分享、资料协作、教师视角或跨设备同步；
- 核心实体仍使用本地 actor/owner scope，目的是明确归属、支持测试和降低未来迁移风险，不代表实现多用户；
- D-021 已确认 Windows x64、React/Vite/TypeScript + Python/FastAPI + SQLite 和 Windows Credential Manager；整体 SPEC 进一步确认单文件 `ProjectB.exe` 分发方向；
- D-022 已确认公开演示只用合成/许可材料与 provider mock、无真实 key；整体 SPEC 进一步确认 OCI、隔离到期 session/限额与 Hugging Face Spaces Docker SDK 方向，当前官方复核仍受 502/超时阻塞；
- D-023 已确认 NJU Git/GitLab 为主仓、GitHub 为镜像，并保留 GitLab `unit-test` 与 GitHub Actions 双 CI 证据；任何远程 push、PR/MR 或镜像操作仍需执行当时的用户授权；
- D-024 已确认安装并使用 Open Design。桌面端 0.15.0 已安装，Codex MCP 已注册且工具已暴露；当前缺口是 daemon 恢复/复验及实际 design system/skill 选择，正式 UI 设计与实现仍受该运行/选择门禁约束。

## 共同硬约束

无论选择哪条路线，以下要求不变：

- 提供可访问的 WebUI；
- 首次导入必须显式选择课程处理方式；
- 没有同意记录时远端课件内容调用为零；
- 原始页面、抽取文本、来源引用和学习证据保持可追溯；
- 凭据不进入 Git、日志、前端持久化或状态回显；
- 删除结果必须覆盖派生数据和适用的远端对象；
- 核心行为可用确定性测试和 provider mock 验证；
- 不把学生私人课件或真实 key 放入公开演示、测试夹具或 CI。

## 总体比较

| 维度 | 单用户、本地优先 | 单用户、云端个人实例 | 多用户 Web 服务 |
| --- | --- | --- | --- |
| 真实目标用户 | 当前学生本人 | 当前学生本人，可跨设备 | 多个独立学生，可能扩展教师 |
| 私有课件位置 | 用户本机 | 受控服务器/对象存储 | 多租户服务器/对象存储 |
| 学习状态位置 | 本地数据库 | 服务器数据库 | 带 owner/tenant 的服务器数据库 |
| 身份边界 | 本机操作系统会话 | 一个已认证 owner | 每请求认证 + 每对象授权 |
| 凭据 | Windows Credential Manager（keyring） | 服务端 secret store 或 owner 级加密记录 | 平台密钥或每用户密钥，按租户隔离 |
| 公开 WebUI | 同构的公开演示部署，使用授权样例 | 同一实例或独立演示账号 | 主服务本身 |
| 私人数据暴露面 | 最小；仅确认片段外发 | 课件、状态、日志均进入服务端边界 | 再增加跨用户与滥用风险 |
| 离线能力 | 可保留导入、原页和本地状态 | 通常不可用 | 通常不可用 |
| 运维责任 | 本地升级 + 演示部署 | 备份、认证、服务器安全 | 再增加注册、配额、隔离、滥用防护 |
| 第一版测试新增面 | 本地路径/端口、钥匙串、演示模式 | 登录、会话、服务端存储、备份/恢复 | 多租户隔离、并发、配额与水平越权 |
| 对学习核心的资源占用 | 最低 | 中 | 最高 |

## 路线 1：单用户、本地优先 WebUI

### 候选拓扑

```text
Windows x64 browser
  -> single-file ProjectB.exe
       -> embedded React/Vite/TypeScript WebUI
       -> Python/FastAPI bound to loopback
            -> SQLite / local page cache / index
            -> keyring -> Windows Credential Manager
            -> parser and renderer
            -> built-in OpenAI adapter for confirmed scope

Public HTTPS URL (preferred: Hugging Face Spaces Docker SDK)
  -> OCI container / same WebUI and domain contracts
       -> licensed/synthetic fixtures only
       -> isolated expiring sessions + provider mock only
       -> no upload, private courseware, secret entry or provider egress
```

### 优点

- 与当前真实材料和用户控制外发的证据最一致；
- 私有课件不需要先上传到项目服务器；
- 本地数据库、页面缓存和索引的删除语义更容易验证；
- 不需要在第一版承担账号找回、跨用户授权、租户配额和公共上传滥用；
- 可把工程深度投入保真、来源引用、理解证据和复习调度。

### 代价与风险

- 本地服务、浏览器打开、端口冲突、系统钥匙串和跨平台打包都要测试；
- 公开 URL 需要单独的演示配置，必须证明它仍是可体验应用而非静态截图；
- 公开演示与本地真实模式可能发生配置漂移，必须由同一核心测试套件约束；
- 正式 UI 前必须重开并保持 Open Design daemon 可用，在 Codex 会话复验 MCP 后记录实际所选 design system 与 skill；当前需求 mockup 不能替代这项证据；
- 跨设备同步不是第一版能力，备份由用户承担或另行设计。

### 课程 URL 的保守处理

公开部署必须使用同一 WebUI、领域合同与业务状态机，并在许可夹具范围内完整体验导入、覆盖确认、学习检查、计划修订/撤销和考后暂停。模型路径固定 mock；任意上传、真实凭据/provider egress 和私人材料持久化均关闭。每浏览器随机隔离 session，30 分钟无活动/2 小时总寿命后清除，并执行 `SPEC.md` 中的资源/速率上限。首选 Hugging Face Spaces Docker SDK；官方 Docker/HTTPS/费用/临时存储条款在网络恢复后重核，不满足无付费边界时必须走 SPEC 变更。

## 路线 2：单用户、云端个人实例

### 候选拓扑

```text
Browser
  -> HTTPS application
       -> owner authentication
       -> server database / object storage / index
       -> server-side credential store
       -> parser worker
       -> remote model provider
```

### 优点

- 公网 URL 与真实运行形态一致；
- 跨设备访问、服务器任务和集中备份更直接；
- 仍可通过单一 owner 约束避免注册与多租户产品范围；
- CI/CD、容器分发和线上可观察性证据相对集中。

### 代价与风险

- 原始课件、页面图、抽取、学习状态和日志全部进入服务器信任边界；
- 需要真正的认证、TLS、会话安全、对象存储权限、备份和恢复；
- 服务器侧 API key 或 owner key 必须有明确的安全存储与轮换；
- 课程材料许可证未知，服务器持久化与远端处理的合规风险高于本地路线；
- 即使只有一个用户，也不能依赖“没人知道 URL”作为访问控制。

## 路线 3：多用户 Web 服务

### 候选拓扑

```text
Browsers
  -> HTTPS application
       -> authentication / session / account lifecycle
       -> per-request authorization
       -> tenant-partitioned database, object store, cache and jobs
       -> quota / abuse / audit controls
       -> parser workers and model providers
```

### 优点

- 产品形态和公开 WebUI 完全一致；
- 可展示账号、跨设备和真实用户隔离；
- 若未来验证多人需求，扩展路径直接。

### 代价与风险

- 每个材料、页面、概念、来源、证据、复习任务和审计记录都要绑定 owner/tenant；
- 文件 URL、缓存键、搜索索引、后台任务、导出与删除都可能产生水平越权；
- 需要注册/登录、密码或第三方身份、找回、会话撤销、速率限制、配额和滥用处理；
- 公开上传 PDF 会扩大恶意文件、版权、存储成本和拒绝服务风险；
- 多用户需求尚无用户证据，可能把课程时间从学习闭环转移到平台基础设施。

## 可保持稳定的核心合同

为避免 D-010 选择推翻学习核心，候选组件接口只依赖明确上下文，不直接依赖某种部署：

| 合同 | 稳定输入/输出 | 路线差异封装位置 |
| --- | --- | --- |
| `ActorContext` | 当前 actor/owner 身份与权限范围 | 本地固定 actor、个人实例 owner session、多用户 tenant session |
| `MaterialRepository` | 按 owner/course 保存和读取材料身份、页面与质量 | 本地文件/数据库或服务器对象存储/数据库 |
| `CredentialStore` | `status`, `set`, `clear`, provider scope；从不返回明文给 WebUI | 首版由成熟 keyring 适配 Windows Credential Manager；未来部署可替换服务端 secret store |
| `ProcessingPolicyService` | 当前课程策略、追加式同意记录、外发判定 | 三条路线行为相同，持久化不同 |
| `ProviderGateway` | 有界、可取消的页面/片段请求与脱敏结果 | 本地进程调用或服务端调用 |
| `AuditSink` | 白名单事件元数据 | 本地审计或 tenant 分区审计 |

这些合同边界不依赖精确依赖版本。D-021 已确认 Windows x64、Python/FastAPI + React/Vite/TypeScript、SQLite 和 Windows Credential Manager；单文件 `ProjectB.exe` 已随整体 SPEC 确认为分发方向。精确版本/冻结工具在 PLAN 前按许可证与验证要求固化。

## 数据位置对比

| 数据类别 | 本地优先 | 云端个人实例 | 多用户服务 |
| --- | --- | --- | --- |
| 原始 PDF/页面图 | 本机 | owner 私有对象存储 | tenant 私有对象存储 |
| 抽取/索引 | 本机 | owner 私有存储 | tenant 分区存储与缓存 |
| 学习证据/复习任务 | 本机数据库 | owner 数据库 | 每对象 owner/tenant 约束 |
| 同意/审计 | 本机追加记录 | owner 审计 | tenant 分区、管理员不可见正文 |
| 云端 provider payload | 经确认页面/片段 | 经确认页面/片段或待决定整份文件 | 同上，并需每请求 owner 授权 |
| API 凭据 | keyring 引用的 Windows Credential Manager 项；config 仅存 adapter/profile 与 `credential_ref` | 服务端 secret store | 平台级或用户级隔离 secret |
| 普通日志 | 无正文、作答、路径、key | 同左 | 同左，并去除可跨用户关联信息 |

## 测试影响

### 三条路线共同测试

- 无同意记录时捕获式 adapter/contract spy 调用为 0；
- 扩大外发范围必须追加新的 `ConsentRecord`；
- 原页、抽取和来源引用不互相覆盖；
- 无学习证据时不能提升掌握状态；
- 删除后检索不可返回材料，远端失败显示不完整状态；
- 日志、错误、快照和 Git 扫描不含凭据或课件正文。

### 本地优先新增测试

- 只绑定 loopback 或明确配置的安全地址；
- 非受信 `Host`/`Origin`、开放 CORS 和无 CSRF 证明的状态变更请求均被拒绝，防止恶意网页访问 localhost；
- 端口冲突给出可恢复错误，不随机暴露到局域网；
- WebUI 无法读取钥匙串明文；
- 钥匙串状态、更新和清除通过后端完成；config、SQLite、日志、错误和前端状态均不出现 secret；
- 本地数据库/缓存删除与重新导入幂等；
- 演示配置拒绝任意上传、私人文件持久化、真实凭据和 provider egress；跨 session 读取为 0，到期/限额可复现，模型路径只允许 mock。

### 云端个人实例新增测试

- 未认证请求不能读取任何课程对象；
- owner 会话撤销后访问立即失效；
- 对象存储 URL 不公开且过期；
- 备份/恢复维持同意、来源和删除状态一致；
- 服务端 secret 状态查询不回显值。

### 多用户新增测试

- 用户 A 对用户 B 的材料、索引、任务、导出和删除均返回拒绝或不可见；
- 不可通过可猜测 ID、缓存、搜索、后台 job 或错误信息侧信道跨租户；
- 配额和速率限制按 owner/tenant 计算；
- 账号删除级联数据并保留不含正文的必要审计；
- 并发导入和删除不会串写 owner。

## 迁移与返工风险

| 迁移 | 主要返工 |
| --- | --- |
| 本地优先 -> 云端个人实例 | 引入认证、远端存储、上传/同步、服务端凭据、备份和数据迁移 |
| 云端个人实例 -> 多用户 | 把隐含单一 owner 改成每请求授权；分区缓存/索引/job；账号生命周期和配额 |
| 本地优先 -> 多用户 | 同时承担上述两类返工，风险最高 |

即使选择本地优先，核心实体保留 `owner_id` 或等价 actor scope 仍有利于测试归属和未来迁移；这不等于第一版实现登录或多租户。

## 选择依据

当前证据只证明一个学生、一个真实课程和本地私有课件的需求，没有证明注册、多用户协作或教师端价值。学生据此采用方案 1，使第一版以最小的新信任边界满足真实自用，并把工程深度集中到项目独有难点。

D-017/D-018/D-021 至 D-024 确认内置 OpenAI、Windows 本地栈、许可夹具/mock、双远程 CI 和 Open Design；单文件/OCI/HF/隔离限额随后写入 `SPEC.md`，并已随整体 SPEC 确认成为 v1 工程方向。它们仍须通过许可证、官方条款、构建、运行和安全验证。详见 [`TECH_STACK_DISTRIBUTION_BASELINE.md`](TECH_STACK_DISTRIBUTION_BASELINE.md)。

选择方案 2 的充分理由应是“跨设备和统一公开实例是首版核心价值”，而不仅是部署看起来方便。选择方案 3 的充分理由应来自真实的第二类用户或多人隔离需求，而不是为了让项目显得更大。

## 已确认方向与后续验证

1. `SPEC.md` 已同步目标用户、数据位置、owner 语义及 D-017 至 D-024，并已由学生整体确认；当前等待外部工具/平台复核、学生本人反思和工程验证；
2. 凭据后端已选 Windows Credential Manager + 成熟 keyring 适配，但首次录入、状态、更新、清除和失败关闭仍需 TDD 证明；
3. 本地运行不引入登录；loopback、Host/Origin、CORS 与 CSRF 边界仍需实现和测试；
4. 首版 Windows x64 单文件 `ProjectB.exe` 已随整体 SPEC 确认；具体冻结工具按许可证与干净机证据选择；
5. 公开 demo 的 OCI + Hugging Face Spaces Docker SDK 方向已随整体 SPEC 确认；官方条款复核、账号、URL、CI/CD 和可访问性尚未执行；
6. 双平台仓库/CI 策略已定，但远程 push、PR/MR、镜像与部署仍需执行当时授权；
7. Open Design 0.15.0 与 Codex MCP 注册均已存在；必须先恢复 daemon、复验 MCP，并由学生选择 design system/skill 后才能开始正式 UI。
