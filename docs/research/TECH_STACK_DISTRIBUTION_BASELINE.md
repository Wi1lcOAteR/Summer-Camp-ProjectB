# 技术栈、分发与公开演示基线

记录时间：2026-07-20

## 状态

本文记录学生对 D-017、D-018、D-021 至 D-024 选择方案 A 后的已确认边界，以及智能体为满足课程分发/部署硬项提出的工程候选。学生已整体确认 `SPEC.md`，因此单文件 `ProjectB.exe`、OCI/Hugging Face 和精确 ReviewPolicy 已成为 v1 工程合同；本文不把它们误记为 D-021/D-022 原答案逐字确认，也不代表实现或工程验证已完成。

## 已确认边界与整体 SPEC 确认的工程方向

| 主题 | 已确认方向 | 尚需证据 |
| --- | --- | --- |
| 目标平台 | Windows x64 优先；macOS/Linux 延后 | 干净 Windows x64 环境的安装、启动、升级/卸载与限制说明 |
| 本地形态 | 浏览器访问 loopback WebUI；SQLite 保存本地权威状态 | 端口冲突、Host/Origin、CORS、CSRF、路径与并发测试 |
| 实现栈 | Python/FastAPI 后端 + React/Vite/TypeScript 前端 | 精确版本、许可证、构建集成、性能和单文件冻结验证后才能固化 |
| 凭据 | 成熟 keyring 适配 Windows Credential Manager | 隐藏录入、仅状态回显、更新、清除、错误脱敏和失败关闭测试 |
| 本地分发（已确认方向） | Windows x64 单文件原生二进制 `ProjectB.exe`；前端资源内嵌，最终用户无需 Python、Node 或 Docker | 冻结工具许可证、单文件构建、干净机、Credential Manager、签名/SmartScreen |
| 公开 WebUI（已确认方向） | 同一合同的 OCI demo；首选 Hugging Face Spaces Docker SDK；内置许可夹具与 HTTPS | 官方 Docker/HTTPS/休眠/临时存储/费用重核及 build/run/隔离/CI-CD 实测 |
| 公开 provider | 只使用确定性 provider mock；不接受上传、真实 key 或真实 provider egress | mock 场景覆盖，以及上传、secret、provider 网络和私人材料持久化路径均关闭的测试 |
| 远程仓库 | NJU Git/GitLab 主仓 + GitHub 镜像 | 用户当时授权后才可 push、建立 PR/MR 或配置镜像 |
| CI | GitLab 精确 job 名 `unit-test` + GitHub Actions，每次 push 运行同一测试入口 | 两个平台的实际成功运行和最后提交对应记录 |
| UI 工作流 | Open Design 0.15.1 daemon 健康；学生已选择 `frontend-design` + `default`（Neutral Modern）；Codex MCP 已注册 | 当前 task 的 MCP 仍缓存旧 7456；须保持桌面端开启并在 fresh task 复验三项 MCP，尚无 project/run/artifact 或正式 UI 证据 |

## 本地运行拓扑

```text
Windows x64 browser
  -> ProjectB.exe -> FastAPI bound to loopback
       -> embedded React/Vite WebUI assets
            -> SQLite / local files / page cache / index
            -> keyring adapter -> Windows Credential Manager
            -> ProviderAdapter registry
                 -> built-in OpenAI adapter for configured local use
                 -> deterministic mock for tests
```

本地配置可以保存 adapter ID、模型、受控非秘密参数、预算与 `credential_ref`，但不能保存 API key。只有后端凭据服务可以调用 keyring；WebUI、SQLite、日志、异常和状态接口都不得收到 secret 明文。

## 公开演示拓扑

```text
Public HTTPS URL
  -> OCI container -> same WebUI and domain contracts in demo profile
       -> built-in synthetic or explicitly licensed fixtures only
       -> deterministic provider mock; no provider egress
       -> isolated, expiring, quota-bound browser sessions
       -> no upload, private courseware persistence, secret entry or credential store
```

公开实例必须可完成可观察的导入、确认、学习与复习核心流程，而不是静态页面。demo profile 与本地真实模式共享领域合同和核心测试，但使用独立配置，以免任何真实凭据、私人课件或远端费用路径进入公开信任边界。每个浏览器使用随机、不含身份信息的隔离 session；30 分钟无活动或创建满 2 小时后清除。单 session 上限为 1 个活动课程、20 个材料夹具、2 个并发任务和 64 MiB 临时状态；每 IP 每分钟最多 60 个请求。

## 分发完成标准

为满足课程“容器/单文件二进制/包”硬项，当前 SPEC 已确认 **Windows x64 单文件原生二进制** 方向。具体冻结工具属于后续工程选择：

- 课程分发产物为单个可直接启动的 `ProjectB.exe`，React/Vite 构建资源及运行所需应用代码均内嵌；运行时创建的 SQLite、缓存与用户材料属于用户数据，不冒充额外分发文件；
- 一次获取后可在干净 Windows x64 环境启动 localhost WebUI，前后端资源、SQLite 初始化和浏览器打开流程均可复现；
- 最终用户不需要预装 Python、Node 或 Docker；开发/构建依赖不泄漏为运行时前提；
- Windows Credential Manager 在目标机器上可完成录入、状态、更新与清除；
- 卸载/删除行为明确区分程序文件、用户数据库、缓存和凭据；
- README 记录获取、运行、安全配置 key、平台/架构限制和已知问题；
- 若产物未做代码签名，README 与发布页如实说明发布者、未签名状态和可能出现的 SmartScreen 提示，不得暗示已有签名或信誉。

OCI container 只用于公开 demo 和相应 CI/CD，不取代 Windows 单文件 `ProjectB.exe`，也不把 Docker 变成真实用户处理本地私有课件的前提。

## 公开 demo 完成标准

- 使用单条 `docker build` 构建镜像，并以单条 `docker run` 在干净环境启动；
- 最终通过 HTTPS URL 从外部干净浏览器完成导入、覆盖确认、学习检查、计划修订/撤销和考后暂停；
- 镜像只含合成或明确许可夹具与 deterministic provider mock，不提供任意上传、路径或 URL 输入；
- 构建和运行环境均不含真实 key、credential store 或真实 provider 出站权限；
- 隔离 session 的跨访客读取为零，到期清理和上述并发、存储、材料及速率限额可复现；
- 首选托管平台为 Hugging Face Spaces Docker SDK。2026-07-20 现场官方复核因 web 上游返回 502、`curl` 连接超时未完成；在部署前必须重新核验 Docker、HTTPS、休眠、临时存储、费用与账号条款，不能把历史印象当作当前证据。若不满足无付费资源边界，必须通过 SPEC 变更选择其他 OCI 平台；创建 Space、push 镜像和部署仍需执行时外部写入授权。

## 依赖与许可证门禁

候选框架名称不是安装授权。引入每个运行时、SDK、打包器、前端包、字体、图标或演示资产前必须：

1. 锁定精确依赖与版本，记录官方来源和许可证；
2. 检查许可证与最终分发方式是否兼容，并保留必要 notice；
3. 优先复用技术栈已有能力，避免为同一职责引入重复库；
4. 对传递依赖与二进制打包内容执行许可证清单；
5. 最终在 README 的第三方依赖/许可证章节汇总；
6. 公开演示材料只使用自行合成或权利范围明确的资产，未知许可证课件不得进入 Git、CI、分发包或公网实例。

当前只确认 OpenAI 是唯一真实参考 adapter，**尚未现场核验 OpenAI Python SDK 的许可证、精确版本及二进制分发兼容性**；在选择、锁定或打包该 SDK 前必须补齐官方许可证证据。此状态不得写成“依赖许可证完整”。

每次 P/F 外发还必须保存并展示当次 OpenAI Responses 能力/政策快照，至少覆盖 application state、abuse monitoring、prompt cache、文件安全审查例外以及 Files/Vector Stores 的训练、ZDR、区域、删除与过期语义。首版 Responses 使用 `store:false`，但不能据此宣称 ZDR；运行前须刷新动态政策并把快照纳入 consent 与审计测试。

## 双 CI 与远程操作边界

GitLab 与 GitHub 必须调用同一条一键测试入口，避免双平台产生不同通过标准。GitLab 配置必须包含名称严格为 `unit-test` 的 job；GitHub Actions 必须在每次 push 运行测试。若分发方案使用构建产物，两边至少验证源码测试，课程主仓的 CI 还须验证最终选定的分发构建。

D-023 只批准了仓库与证据策略，不批准当前会话执行远程动作。向 NJU Git/GitLab 或 GitHub push、创建 PR/MR、启用镜像、写入远程 secret 或部署公网服务，均须在执行当时取得用户授权，并保留真实 URL/运行记录；本地文件不能冒充远程证据。

## Open Design 外部门禁

学生已选择并安装 Open Design；2026-07-21 桌面端版本为 0.15.1，composer 已实际选择 `frontend-design` + `default`（Neutral Modern）并链接 `ProjectB`。daemon 的直接只读 API 健康且返回相同标识。全局配置中的 `skillId=null` 不与该事实冲突，因为 skill 绑定在单次 composer turn；MCP 注册也无需重复。

当前 Codex task 的 MCP 进程在最新 daemon 前启动并缓存了 fallback `127.0.0.1:7456`。正式 UI 前须保持 Open Design 运行，在 fresh Codex task 复验 `list_skills`、`list_projects` 与 `get_active_context`；不得重复注册或把动态端口写入配置。选择已写入 `SPEC.md`，但现有需求 mockup 与直接 daemon API 都不能替代 Open Design MCP run/artifact 或正式 UI 验收证据。
