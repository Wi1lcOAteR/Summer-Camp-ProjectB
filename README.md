# ProjectB 本地智能学习工作台

ProjectB 面向需要从课程材料中建立知识结构、完成理解练习并持续复习的学生。它将 PDF、TXT 或 Markdown 讲义保存在本机，记录材料版本和精确来源，提供确定性练习与证据，再依据这些证据生成可完成、跳过和恢复的复习任务。

项目以 **Windows 本地应用** 交付：`ProjectB.exe` 在本机启动 FastAPI、SQLite 和 WebUI，仅监听 `127.0.0.1`。浏览器只是应用界面，不需要公网服务器，也不会把课程材料自动上传到远端。

- 源码仓库：[GitHub](https://github.com/Wi1lcOAteR/Summer-Camp-ProjectB)
- 自动化检查：[GitHub Actions](https://github.com/Wi1lcOAteR/Summer-Camp-ProjectB/actions)
- 发布页：[GitHub Releases](https://github.com/Wi1lcOAteR/Summer-Camp-ProjectB/releases)
- 详细规约：[SPEC.md](SPEC.md)
- 文档索引：[docs/INDEX.md](docs/INDEX.md)

## 功能模块

1. **材料导入**：创建课程并导入数字版 PDF、TXT、Markdown；保存材料版本、内容哈希和精确 locator。
2. **概念映射**：把讲义片段映射到知识点，确认或拒绝来源覆盖，避免无来源解释成为权威答案。
3. **学习与证据**：对互斥、竞态和死锁运行本地确定性检查；答案和结果形成可追踪 evidence。
4. **复习计划**：按当前课程、来源和学习证据生成真实 revision；支持连续/期末模式、每日预算、完成、跳过和恢复，状态写入本地 SQLite。
5. **设置与凭据**：查看本地运行状态；可选配置 OpenAI 提供方。密钥写入 Windows Credential Manager，界面和 API 不回显明文。

核心学习闭环在没有 API key、没有真实模型、没有网络服务时仍可运行。

## 最快体验

课程提交包中的 Windows x64 单文件应用位于：

```text
dist/ProjectB.exe
```

双击运行后访问：

```text
http://127.0.0.1:4173/
```

## 完整使用流程

### 1. 导入课程材料

1. 打开“导入”页；首次运行时先创建课程。
2. 点击“选择文件”，选择数字版 PDF、UTF-8 TXT 或 Markdown。扫描件和图片不会进行 OCR。
3. 检查“已选文件”，点击“开始导入”。每个文件会独立显示成功或失败，成功材料出现在右侧列表。

### 2. 映射知识点与原文

映射用于告诉系统“这个知识点具体依据讲义的哪一页或哪几行”。没有经过确认的原文不会被当作权威来源，也不能进入确定性学习和复习计划。

1. 打开“映射”页，在左侧选择材料。
2. 在右侧输入知识点名称，例如“互斥”。
3. 选择检查方式：互斥、竞态、死锁或仅解释，然后点击“新增”。
4. 选中刚创建的知识点，并在左侧勾选对应的原文行或 PDF 页。
5. 点击“确认来源”。状态变为“已确认”后，该来源才会进入学习与计划。
6. 如果片段不适合该知识点，点击“拒绝映射”；删除材料会让相关来源立即失效。

### 3. 完成学习练习

1. 打开“学习”页，从“选择知识点”中选择已确认来源的概念。
2. 核对来源原文、页码/行号、材料版本和内容 hash。
3. 阅读题目和右侧“确定性规则”，选择结论并在“我的答案”中写下理由。
4. 点击“提交确定性检查”。右侧会显示每条规则是否通过，并生成 evidence ID。
5. “仅解释”知识点没有确定性 rubric，只能查看来源与解释，不会伪造评分或 evidence。
6. OpenAI 辅助是可选功能；普通本地学习不需要 API key。外部候选不会参与确定性评分。

### 4. 生成和执行复习计划

1. 打开“复习”页。页面会根据当前课程和已确认来源生成 revision 与任务。
2. 选择“连续复习”或“最终复习”，设置每日预算；最终复习还需要考试日期。
3. 修改设置后点击“更新计划”，查看新增、移除、变更和保留任务。
4. 点击“开始复习”，系统会选中最早的待复习任务并显示当前知识点。
5. 当前版本不会自动跳转到学习题：需要时打开“学习”页完成练习，再回到“复习”页点击“完成当前任务”。
6. 暂时不做可点击跳过图标；之后可用“恢复已跳过任务”恢复。完成、跳过和恢复都会写入本地 SQLite。

### 5. 可选提供方设置

本地闭环无需配置凭据。需要外部解释候选时，在“设置”页隐藏录入自己的 API key、启用提供方，并在每次发送前核对来源、模型、token 与费用上限预览。

应用数据默认保存在 `%LOCALAPPDATA%\ProjectB`。关闭应用后再次启动，课程和任务状态仍会保留。

## 安装与开发运行

开发环境基线为 Python 3.14.6、Node.js 24.18.0、npm 11.16.0。PowerShell 示例：

```powershell
$Py = "C:\Python314\python.exe"
& $Py -m pip install --require-hashes -r backend/requirements-windows-x64.lock
npm.cmd --prefix frontend ci --ignore-scripts
npm.cmd --prefix frontend run build
$env:PYTHONPATH = (Resolve-Path backend).Path
& $Py packaging/windows/launcher.py --data-dir tmp/dev-data --port 4173
```

## 测试

一键执行后端、前端、静态检查、凭据扫描和许可证验证：

```powershell
python scripts/test_all.py --all
```

也可分别运行：

```powershell
python scripts/test_all.py --backend
python scripts/test_all.py --frontend
python scripts/scan_credentials.py --tracked
python scripts/verify_licenses.py
```

## Windows 单文件分发

构建 Windows 单文件应用：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File packaging/windows/build.ps1 `
  -Python C:\Python314\python.exe `
  -Output dist/ProjectB.exe
```

产物内嵌 WebUI、后端、SQLite 迁移和第三方许可证文件，最终用户不需要安装 Python、Node.js 或 Docker。

当前最终构建产物为 `29,225,145` 字节，SHA-256：

```text
CB463E179FE2D3367ED0BA96B0621A5E32CF01319F39DB0AB74FC9FCC237F6A3
```

## OCI 本地演示

OCI 镜像仅用于无上传、无真实凭据和无真实提供方网络访问的确定性演示：

```powershell
docker build --platform linux/amd64 --file packaging/oci/Dockerfile --tag projectb-demo:local .
docker run --rm --read-only --tmpfs /tmp/projectb-demo:rw,size=64m -p 127.0.0.1:7860:7860 projectb-demo:local
```

它不是主要分发方式，也不替代 Windows 本地应用。

## 安全与凭据

- 服务固定监听 `127.0.0.1`，拒绝转发头，并使用 session cookie 与 CSRF 保护写操作。
- 课程材料、答案、学习证据和 SQLite 数据默认只保存在本机。
- API key 通过隐藏输入写入 Windows Credential Manager；状态接口只返回是否配置和更新时间。
- 真实提供方默认关闭。启用时，每次调用预览会绑定 profile、模型、来源版本/哈希、token 上限和费用上限，并要求一次性确认。
- 上传文件、locator、模型输出和工具参数均作为不可信输入处理，执行类型、大小、路径、超时和错误脱敏检查。
- 提交前运行凭据扫描；仓库和测试夹具不得包含真实密钥。

## 目录结构

```text
ProjectB.exe / launcher
        |
        +-- React WebUI
        +-- FastAPI API
        +-- domain services: materials / mapping / learning / review
        +-- local SQLite + Windows Credential Manager
```

| 路径 | 职责 |
| --- | --- |
| `backend/projectb/` | API、领域规则、存储、凭据与可选提供方端口 |
| `frontend/src/` | React WebUI、路由、视图与 API client |
| `backend/tests/`, `frontend/e2e/` | 单元、集成、合同和浏览器测试 |
| `packaging/windows/` | Windows 单文件构建与 smoke |
| `packaging/oci/` | 可选的本地确定性演示镜像、SBOM 与 notice |
| `scripts/` | 一键测试、凭据扫描、许可证和 CI 合同验证 |
| `docs/` | 工程证据、设计记录、计划和历史归档 |
| `licenses/` | 第三方依赖与许可证清单 |

## CI/CD

- `.github/workflows/ci.yml` 在 GitHub push/PR 时运行当前测试和构建合同。
- `.gitlab-ci.yml` 保留课程要求的 `unit-test` job；尚未在课程 GitLab 平台执行时，不把本地合同验证写成远端通过。
- 主要分发方式是未签名的 Windows x64 单文件应用。Windows SmartScreen 可能因发行者未签名而提示警告。
- OCI 镜像仅用于无上传、无真实凭据、无真实提供方网络访问的本地演示，不是本项目的主要交付入口。
- 本项目没有远程业务服务端。根据课程“如做带服务端项目才需要远程部署”的适用范围，当前选择本地应用交付，不需要远程服务端或公网部署。
- GitHub Actions 已启用；GitLab CI 尚未执行。最终远端状态仍以对应平台页面为准。

## 已知限制与交付状态

- 支持数字版 PDF、TXT 和 Markdown；暂不支持扫描件 OCR、图片材料和批量文件夹导入。
- 确定性 evaluator 当前覆盖互斥、竞态和死锁；其他知识点可保存来源并查看解释，但不会伪造自动评分。
- 当前界面默认操作本地数据库中的第一个课程，尚未提供多用户、账号体系或跨设备同步。
- 复习页已经连接真实 review revision/task API，完成、跳过和恢复会持久化；它不是科学最优的记忆算法，而是可解释、可复现的课程项目调度规则。
- OpenAI 路径为可选能力，需要用户自备凭据并承担费用；自动化测试使用 mock transport，不发起付费调用。
- Windows 可执行文件未做 Authenticode 签名；学生通过 D-026 豁免当前 29.22 MB 产物的再次干净机复测，该豁免不等于性能 PASS，也不宣称满足内部 `<=10s` 指标。
- GitHub Actions 状态以仓库 Actions 页面为准；课程 GitLab CI 在实际运行前仍记为“尚未执行”。

## 第三方依赖与许可证

直接依赖声明在 `pyproject.toml` 和 `frontend/package.json`，精确版本与哈希记录在锁文件中。完整依赖闭包、许可证和再分发义务见 [licenses/THIRD_PARTY_NOTICES.md](licenses/THIRD_PARTY_NOTICES.md)；OCI 的 SPDX SBOM 位于 `packaging/oci/`。

```powershell
python scripts/verify_licenses.py
```

## 课程过程材料

- `SPEC.md`：产品规约与验收标准
- `PLAN.md`：任务与验证状态
- `SPEC_PROCESS.md`：规约演进与冷启动记录
- `AGENT_LOG.md`：实现、测试、评审和人工决策记录
- `REFLECTION.md`：项目反思
