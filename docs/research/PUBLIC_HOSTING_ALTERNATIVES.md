# 公开 OCI WebUI 托管替代方案调查

调查时间：2026-07-22（Asia/Shanghai）

## 状态与边界

本文只为 D-025 提供可核验的候选证据，**不选择平台，也不构成账号、付款方式、镜像推送、部署或公开 URL 证据**。当前已确认的交付合同保持不变：

- 公开实例运行 `linux/amd64` OCI 镜像，并与本地版共享 WebUI、领域合同和核心测试；
- 只包含合成或明确许可的夹具与 deterministic provider mock；
- 不接受任意上传，不保存私人课件，不录入真实凭据，不产生真实 provider egress；
- 使用 HTTPS、隔离且到期清除的访客 session，以及 `SPEC.md` 已确认的并发、存储、材料和速率上限；
- 任何托管账号、付款方式、远程 registry、镜像 push 和部署动作仍需学生在执行时授权。

Hugging Face Docker Spaces 的付费账号冲突仍然成立。下面的候选不会自动替换它；学生选择后仍须更新 `SPEC.md` 的托管段落，完成所选平台的全部 `host-*` 证据行并重新确认。

## 候选比较

| 路线 | OCI 与 HTTPS | 账号/费用边界 | 可用性与数据边界 | 当前结论 |
| --- | --- | --- | --- | --- |
| 已有学生/NJU 控制的 x64 Docker 主机 + 既有域名/反向代理 | 可直接运行已选 `linux/amd64` 镜像；HTTPS 由现有入口提供 | 不新增付费资源，但学生必须证明主机、域名和运维权限确实存在 | 可保持相同镜像和 demo profile；可用性、补丁、证书、监控和期限内在线由学生承担 | **若已有资源，仍是改动最小的首选**。目前未提供主机或域名证据，不能标记可用 |
| 已有 x64 Docker 主机 + Tailscale Funnel | Funnel 把本机服务公开为 `https://<device>.<tailnet>.ts.net`；只暴露指定服务，自动配置有效 HTTPS 证书 | Funnel 对所有方案可用；官方当前 Personal 方案为 `US$0` 且标注长期免费。仍需创建/使用 Tailscale 账号并批准 tailnet policy | Funnel 仍为 beta，只支持 TLS、指定端口和非可配置带宽上限；Docker、Tailscale 与主机必须持续在线，项目没有托管 SLA | **无现成域名时的条件候选**。不新增云计算费用，但会新增公网隧道、安全策略和在线运维责任，必须由学生选择 |
| Azure for Students + Azure Container Apps Consumption | Container Apps 支持任意 `linux/amd64` 镜像及公有/私有 registry；外部 HTTP ingress 提供 FQDN、TLS 1.2/1.3 和 HTTP 到 HTTPS 重定向 | Azure for Students 面向符合条件的全日制大学生，无需信用卡，含 12 个月内使用的 `US$100` credit；未主动转为按量付费时，credit 用尽后订阅/资源会停用。Container Apps 每订阅每月有免费计算与请求额度，超额部分按量计费或消耗 credit | 可缩容到零并保留 URL，但有冷启动；容器/副本存储是临时的，关闭或重启会丢失。registry、日志、网络、区域和 30 分钟 session 保活策略仍需预算/行为验证 | **托管式候选**。无需信用卡不等于无需学生决定：会创建云账号和资源并消耗学生 credit，且必须先确认学生资格、区域和零付费升级边界 |
| 继续 Hugging Face Docker Spaces | 技术合同已验证 | 创建新的 Docker/Gradio Space 需要付费方案 | 原有睡眠、临时盘和配额证据仍有效 | 仅在学生明确批准方案、周期费用上限和执行动作后可用；当前授权下不可执行 |

## 已筛除为当前最终托管方案的路线

### Cloudflare Quick Tunnels

Quick Tunnel 不要求先把站点加入 Cloudflare DNS，能够生成临时公网 HTTPS URL，但官方文档明确把它限定为测试和开发用途。当前限制还包括最多 200 个并发在途请求且不支持 Server-Sent Events。它可在未来作为本地 OCI 的短期人工预检工具，但不能作为课程截止前需要稳定访问的最终公开 URL。若改用正式 Cloudflare Tunnel，则还要单独验证 Cloudflare 账号、受管域名/区、DNS、方案和长期可用性；本轮没有把这些条件当作已满足。

### Northflank Developer Sandbox

官方文档证明它可以从外部 container registry 连续运行镜像，并为公开 HTTP 端口分配 `code.run` 域名和自动 TLS；当前 Sandbox 标注两项免费 service 且不休眠。不过同一官方计费文档明确要求所有用户在创建资源前添加付款方式，并说明免费层不应用于 production。它因此不满足当前“无需新增付款责任即可产生最终公开资源”的保守边界，只能在学生另行批准付款方式和平台适用性后重新评估。

### Oracle Cloud Always Free

Oracle 官方文档仍列出 Always Free VM，但多数用户注册需要手机和信用卡。Always Free A1 是 Arm，而当前镜像已固定为 `linux/amd64`；x64 E2 micro 资源更小。官方还明确保留回收连续 7 天低 CPU、网络及（A1）内存使用的 idle VM 的权利。该路线需要自管 Docker、补丁、网络与 HTTPS，并同时引入架构或容量风险，因此不作为本轮推荐候选。

### 静态站点托管

GitLab Pages、GitHub Pages 等静态托管无法运行 FastAPI、受约束 AI port、隔离 session 和学习/复习状态机。采用它们会把当前动态应用合同降为静态展示，属于新的重大 SPEC 变更，不是 OCI 托管替代品。

Render 与 Koyeb 域名此前被浏览器安全策略明确禁止。本轮没有绕过该策略，也没有把它们列为候选。

## 选择后的最小 SPEC diff

### 若选择已有主机或 Tailscale Funnel

- 将托管商从 Hugging Face 改为“学生控制的 x64 Docker 主机”；若使用 Funnel，再记录其 beta、端口、带宽和 tailnet policy 边界；
- 保持已选 OCI digest、同构 WebUI、demo profile、mock、无上传/无 key/无 provider egress 和 session 限额不变；
- 新增可用性验收：评分窗口前启动容器和隧道、外部干净浏览器复验 HTTPS、重启恢复、过期清理及主机离线提示；
- 新增安全验收：只转发 demo 端口，主机其他端口不可达，Tailscale policy 最小化，日志不包含私人路径或内容。

### 若选择 Azure for Students + Container Apps

- 将托管商改为 Azure Container Apps Consumption，并记录学生 subscription、区域、默认 FQDN、外部 ingress 和 scale-to-zero；
- 明确只允许 Azure for Students credit/free grant，不升级按量付费，不添加其他付款方式；用预算告警和资源清单验证 registry、日志、网络及计算不会静默扩大；
- 保持 demo 数据/模型/隔离合同不变，并验证副本停止或重启后的临时状态清除、30 分钟 session 行为和冷启动恢复；
- 远程 registry 创建、镜像 push、Container Apps resource 创建与公开部署仍须执行时授权。

## 官方证据

| 事实 | 官方来源 | 当前性记录 |
| --- | --- | --- |
| Funnel 为 beta、对所有方案可用；公网 URL、TLS、端口和带宽限制 | [Tailscale Funnel](https://tailscale.com/docs/features/tailscale-funnel) | 页面标注 `Last validated Jan 20, 2026`；2026-07-22 读取 |
| Personal 方案当前 `US$0`、长期免费 | [Tailscale pricing](https://tailscale.com/pricing) | 2026-07-22 动态页面读取；选择后须再次刷新 |
| Azure for Students 无需信用卡、`US$100`/12 个月及 credit 用尽后的停用/升级选择 | [Azure for Students](https://azure.microsoft.com/en-us/free/students/) | 2026-07-22 动态页面读取；账号资格尚未验证 |
| Container Apps 免费 grant、按秒计费、scale-to-zero 无使用费 | [Azure Container Apps pricing](https://azure.microsoft.com/en-us/pricing/details/container-apps/) | 2026-07-22 动态页面读取；价格/额度选择后须刷新 |
| 外部 ingress、FQDN、TLS 1.2/1.3 与 HTTPS 重定向 | [Azure Container Apps ingress](https://learn.microsoft.com/en-us/azure/container-apps/ingress-overview) | 官方 metadata commit `3c91d9f322765a020958d5e980e953950f3cecbe`，2026-07-22 读取 |
| 支持任意 `linux/amd64` 镜像及公有/私有 registry | [Azure Container Apps containers](https://learn.microsoft.com/en-us/azure/container-apps/containers) | 官方 metadata commit `e2507938b2a97d1c5db073fc57046b84254900a0`，2026-07-22 读取 |
| 容器/副本临时存储在关闭或重启时丢失 | [Azure Container Apps storage](https://learn.microsoft.com/en-us/azure/container-apps/storage-mounts) | 官方 metadata commit `c56f0359c86fad8f5625f74cd1d7c5eb50f6658a`，2026-07-22 读取 |
| Quick Tunnel 的测试用途、200 在途请求与无 SSE 限制 | [Cloudflare Quick Tunnels](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/do-more-with-tunnels/trycloudflare/) | 页面标注 `Last updated Apr 20, 2026`；2026-07-22 读取 |
| Northflank Sandbox 免费资源及不休眠；所有用户创建资源前需付款方式且免费层非 production | [Northflank pricing](https://northflank.com/pricing), [Northflank billing](https://northflank.com/docs/v1/application/billing/pricing-on-northflank) | 2026-07-22 读取 |
| Northflank 外部镜像、公开域名和自动 TLS | [Run an image from a registry](https://northflank.com/docs/v1/application/run/run-an-image-from-a-container-registry), [Configure ports](https://northflank.com/docs/v1/application/network/configure-ports) | 2026-07-22 官方 Markdown 读取 |
| Oracle 注册、Always Free compute 与 idle 回收 | [OCI Free Tier](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier.htm), [Always Free resources](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm) | 2026-07-22 读取 |

## 调查方法与失败边界

- 官方搜索接口本轮返回 HTTP 503。
- `curl.exe` 访问官方 HTTPS 时返回 `schannel: AcquireCredentialsHandle failed: SEC_E_NO_CREDENTIALS`；PowerShell `Invoke-WebRequest` 返回“基础连接已经关闭: 接收时发生错误”。没有反复提权或关闭 TLS 校验。
- 同一官方 URL 通过项目现有 Node.js 24.14.0 `fetch` 只读访问成功；Cloudflare、Tailscale 和 Northflank 的官方 Markdown 端点以及 Microsoft Learn metadata 用于交叉核对。没有保存 cookie、登录、账号状态或私有响应。
- 本轮没有运行 Docker、创建 registry/host、接受服务条款、添加付款方式、消耗 credit、push 镜像或部署。

## D-025 仍需学生回答

1. 是否已有可在评分期持续在线、可运行 `linux/amd64` Docker 且由你控制的主机？若有，是否已有 HTTPS 域名，还是接受 Tailscale Funnel 的 beta/在线运维边界？
2. 若没有现成主机，是否符合并愿意使用 Azure for Students，允许创建免费 subscription/resource 并消耗学生 credit，但禁止升级按量付费？
3. 若前两项都不接受，是否明确批准付费 Hugging Face 方案及周期费用上限？

没有答案前，`host-cost` 与 `host-account` 继续保持 `explicitly-blocked`，G-02C 不得标记完成。
