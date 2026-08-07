# UI-01 Open Design 运行记录

状态：`PASS`

执行时间：2026-08-07 10:37:05 至 10:48:47（Asia/Shanghai）

## 运行身份

| 字段 | 值 |
| --- | --- |
| Project ID | `projectb-learning-workbench-v1` |
| Conversation ID | `11b09121-069a-48e4-a866-1f8e1114ed52` |
| Run ID | `1fec5e0c-ef5b-4960-982a-2e374ef739ff` |
| Open Design | `0.18.0` |
| 生成智能体 | `codex` / Codex CLI `0.144.4` |
| Skill | `frontend-design` |
| Design system | `default` / Neutral Modern |
| Design system digest | `6D09C7FB4495B56474CCC06572BC02E58A66F9E3282AAAC10E598ECB383546EC` |
| Prompt digest | `AB8E426EA6759503F87F888F352F6F402551EA79D833A16951FF64D24D3166EA` |
| 结果 | `succeeded`，exit 0，`deliverableValid=true` |

## 产物与截图

| 类型 | 仓库路径 | SHA-256 |
| --- | --- | --- |
| Open Design HTML 快照 | `docs/engineering/open-design/projectb-learning-workbench.html` | `C68BB20258A04C214CA4C34D3BA7EA16DD2E14095A58F84722C12B46FD8FB7C7` |
| Open Design 原始预览 | `docs/engineering/open-design/projectb-workbench-preview.png` | `77CEBF0A38B24EFB589AA7651093C5EE751C177541699640E619F6E9C790332F` |
| 生产实现 360px | `docs/engineering/open-design/ui01-360.png` | `02AB5DB80255807CCCE509D2DB1C9CDCF827A4E696546F871F47B1D5E32621BD` |
| 生产实现 768px | `docs/engineering/open-design/ui01-768.png` | `AD07C0D12045647000C5CDDAD5DA839A8F27978F9767FBE25CD2BB3347B6B83C` |
| 生产实现 1440px | `docs/engineering/open-design/ui01-1440.png` | `3346F8B9F75A702690DEFC598F9C18FE448D730A6B31C1DC1A728D2620CBFB9E` |

Open Design 原始路径位于其用户数据项目目录；仓库内保存的是本次运行结束后的字节快照。生产截图由 UI-01 Playwright GREEN 在三个冻结视口生成，不把外部原型源码当作生产实现。

## 设计输入与资产

- 设计目标是本地优先的中文操作系统学习工作台，不是营销页。
- 主导航固定为“导入、映射、学习、复习”，设置为次级入口。
- 使用系统字体、CSS 颜色与布局、Lucide 图标；没有网络图片、自定义字体、股票素材或外部 CDN。
- Open Design HTML 为本次生成证据，不作为第三方运行时依赖。生产所用 `lucide-react` 已在项目锁文件和第三方许可清单中登记。
- 生产 token 将圆角上限冻结为 8px，并保留可见焦点、语义地标、状态文字和本地隐私标识。

## 评审与修订

1. Open Design 自检先观察到产物缺失 RED，再生成 HTML；结构检查、JavaScript 语法、外部 URL、占位内容和页面溢出检查均通过。
2. 外部原型定义了未使用的 12px/16px 默认圆角 token，与课程上限冲突。生产实现未复制这些 token，只保留 4px/8px。
3. 首轮生产 E2E 在 360px/768px 分别观察到 20px/6px 页面溢出。根因为设置入口保留 `min-width:80px`；窄屏清除该下限后 12 项 E2E 全部通过。
4. 首轮 360px 截图只显示步骤编号，且错误横幅出现孤字换行。修订为保留两字阶段名并把重试按钮移动到下一行；重新生成截图并复验通过。
5. 最终三档均无页面级横向溢出，首个 Tab 焦点落在“导入”，axe 未发现 serious/critical 违规。Critical=0，Major=0。

## 边界

本记录只关闭 UI-01 的设计与壳层证据。导入、映射、学习、复习和设置页面的业务交互分别由 UI-02 至 UI-06 实现和验收；当前截图中的任务数据是壳层层级示例，不宣称后续页面已完成。
