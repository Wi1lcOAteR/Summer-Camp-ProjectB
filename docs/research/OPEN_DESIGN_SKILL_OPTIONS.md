# Open Design Skill and Design-System Options

调查时间：2026-07-20T19:56:11+08:00（追加 daemon 复验与计划粒度复审）
调查对象：本机 Open Design 0.15.0 bundled resources、当前 Codex MCP 暴露状态、ProjectB 已确认 UI 规约
结论状态：候选建议，等待学生确认；不是正式 Open Design run 或 UI 实现证据

## 1. 当前运行状态

- `C:\Users\22078\.codex\config.toml` 已包含 `mcp_servers.open-design`，当前 Codex 会话也已暴露 `mcp__open_design__*` 工具。
- 配置通过 `OD_SIDECAR_IPC_PATH` 发现桌面 daemon 的动态端口；当前桌面端没有可枚举窗口，daemon 日志最后记录 shutdown，因此发现失败并回退到 `http://127.0.0.1:7456`。
- `list_skills`、`list_projects`、`list_agents`、`get_active_context` 的直接调用均返回 `cannot reach the Open Design daemon at http://127.0.0.1:7456`。无需重复注册 MCP；需正常重开并保持 Open Design 桌面端运行后复验。
- 当前三个 `Open Design.exe` 进程没有任何 TCP listen socket；daemon 日志最后记录 `shutdown requested` 和正常退出。读取完整进程 command line 的只读 CIM 查询被系统拒绝，未请求提权或重复尝试。
- Computer Use 对 Open Design 的启动动作未获批准，本轮立即停止 UI 输入，没有修改应用设置。

## 2. “按需获取”的准确含义

Open Design 的两类选择职责不同：

| 类型 | 作用 | ProjectB 应用方式 |
| --- | --- | --- |
| Skill | 传给 `start_run` 的生成或审查配方 | 原型/正式界面生成时选择一个主 skill；实现后可用另一个审查 skill |
| Design system | 颜色、字体、间距、组件和交互状态合同 | 一个项目固定一个首选系统，并记录项目级覆盖，不按页面随意切换 |

本机 bundled 目录当前有 162 个 skill 条目和 152 个 design-system 条目。条目存在不等于完整工作流已安装：只有一个 `SKILL.md` 且正文要求另装 upstream bundle 的条目只是 catalog stub。

## 3. Skill 比较

| Skill | 本地状态 | 适配度 | 结论 |
| --- | --- | --- | --- |
| `frontend-design` | 完整 bundled workflow；自带 Apache-2.0 `LICENSE.txt` | 明确覆盖 React/app/dashboard、密集操作界面、真实 loading/error/empty 状态、响应式、键盘/焦点/对比度和自审 | **首选生成 skill** |
| `web-design-guidelines` | 完整 bundled 规则和固定 reference snapshot | 适合实现后按文件审查布局、交互和可访问性，不负责从零生成 | **后续审查 skill** |
| `design-brief` | 完整 bundled workflow | 可生成自定义 `DESIGN.md`，但会新增一次视觉合同和覆盖风险 | 仅在拒绝现有 design system 时使用 |
| `ui-ux-pro-max` | catalog stub；缺 data/scripts/templates | 不能执行完整搜索工作流 | 不选 |
| `platform-design` | catalog stub；要求另装 upstream | 首版不是 iOS/Android/Web 三端统一 | 不选 |
| `ui-skills` | catalog stub；要求另装 upstream | 只有发现元数据 | 不选 |
| `shadcn-ui` | catalog stub；要求另装 upstream | 不等于 bundled `shadcn` design system | 不选 |
| `design-review` | catalog stub；要求另装 upstream | 当前不可声称完整审查流程可用 | 不选 |

## 4. Design-system 比较

| Design system | 优点 | 主要风险 | 结论 |
| --- | --- | --- | --- |
| `default` / Neutral Modern | 明确面向 B2B tools、dashboards 和 utility pages；浅色、内容优先、响应式；bundled 组件参考覆盖 buttons/inputs/cards/badges/keyboard/icons | 原始 token 有 12px card radius 与负 display tracking | **首选**，必须记录 ProjectB 覆盖 |
| `shadcn` | utility-first、8px 默认 radius、清晰 focus/error/state 规范、适合 React 控件 | 黑白主色偏单一，个性弱；`shadcn-ui` skill 本身仍是 stub | **备选** |
| `application` | 表面上面向 app | DESIGN prose 为紫色/glass，而 normalized token 是浅色蓝，来源内部不一致 | 排除 |
| `dashboard` | 表面上面向 dashboard | DESIGN prose 为深色/glass，而 normalized token 是浅色蓝，来源内部不一致 | 排除 |
| `notion` | 知识工作区语义接近 | 暖米色主导、过大留白、负 tracking、12px card，不符合紧凑工作台约束 | 排除 |
| `linear-app` | 精确的生产力工具语言 | 深色紫/冷灰单色、强负 tracking，与 ProjectB 阅读和配色约束冲突 | 排除 |

若选择 `default`，正式验证文档必须写入以下 ProjectB 优先覆盖：

1. 卡片、面板和工具容器最大圆角 8px；只有 pill/status chip 可使用完全圆角。
2. 所有字距为 0，不使用 design-system 原始负 display tracking。
3. 工作台采用 compact/balanced 密度，不生成营销 hero；首屏直接是可用流程。
4. 使用中性底色、一个克制主 accent 和 success/warn/danger 语义色，避免单一紫色、深蓝、米色或玻璃风主导。
5. 首次导入和最终确认使用桌面/移动均可读的 X 轴四阶段时间线；主要结论用字号、字重和颜色形成二级层次，配置入口在“开始学习”前高强调。

## 5. 推荐组合

- 生成：`skillId=frontend-design`
- 视觉合同：`designSystemId=default`
- 实现后审查：`web-design-guidelines`
- 备选视觉合同：`designSystemId=shadcn`

该组合无需安装 catalog-only 的 upstream 包。正式记录前仍须学生确认，且必须先恢复 daemon，使用 MCP `list_skills`/`list_projects` 观察到真实结果。

## 6. 来源与证据限制

本轮读取的主要本地证据：

- `C:\Users\22078\AppData\Local\Programs\Open Design\resources\open-design\skills\frontend-design\SKILL.md` 与同目录 `LICENSE.txt`
- `C:\Users\22078\AppData\Local\Programs\Open Design\resources\open-design\skills\web-design-guidelines\SKILL.md` 和 vendored references
- 相关 catalog-only `SKILL.md`
- `C:\Users\22078\AppData\Local\Programs\Open Design\resources\open-design\design-systems\{default,shadcn,application,dashboard,notion,linear-app}\DESIGN.md`、相应 `tokens.css`、manifest 与 source evidence
- packaged CLI 对 `OD_SIDECAR_IPC_PATH` discovery 和默认 `127.0.0.1:7456` fallback 的实现

官方站点与 GitHub 的三轮查询均返回 HTTP 503（最近一次同时检索 Open Design、Anthropic `frontend-design` 与 Vercel guidelines）。因此本文件不声称已重新核验线上最新版、上游完整许可证链或品牌官方来源；G-02 仍须在依赖/资产接入前完成许可证和来源复核。
