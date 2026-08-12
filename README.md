# ProjectB

ProjectB 是面向操作系统课程材料的本地学习工作台。它把用户导入的讲义转成可追溯的概念与来源，提供确定性的理解练习，并按掌握度生成连续复习或期末复习计划。真实模型只在本地模式下由用户显式启用；没有真实模型时，核心学习流程仍可运行。

当前产品规约见 [SPEC.md](SPEC.md)，任务与验收状态见 [PLAN.md](PLAN.md)，文档入口见 [docs/INDEX.md](docs/INDEX.md)。

- 源码仓库：<https://github.com/Wi1lcOAteR/Summer-Camp-ProjectB>
- GitHub Actions：<https://github.com/Wi1lcOAteR/Summer-Camp-ProjectB/actions>
- Release 入口：<https://github.com/Wi1lcOAteR/Summer-Camp-ProjectB/releases>（发布附件创建前请按下方命令从源码构建）

## 功能模块

- **材料与来源**：导入课程材料，保存材料版本、内容哈希和精确 locator，映射结果可确认、拒绝或重新检查。
- **理解与练习**：围绕 mutex、race、deadlock 等概念生成来源绑定的解释与练习；确定性 evaluator 负责评分，模型文本不成为权威答案。
- **复习计划**：根据掌握度、时间预算和截止时间生成连续或期末计划，保留已完成任务并记录修订差异。
- **设置与凭据**：查看本地/演示 profile、配置或清除提供方凭据、启停真实提供方，并显示不回显明文的状态。

## 安装与开发运行

开发环境锁定为 Python 3.14.6、Node.js 24.18.0 和 npm 11.16.0。Windows PowerShell 示例：

```powershell
$Py = "C:\Python314\python.exe"
& $Py -m pip install --require-hashes -r backend/requirements-windows-x64.lock
npm.cmd --prefix frontend ci --ignore-scripts
npm.cmd --prefix frontend run build
$env:PYTHONPATH = (Resolve-Path backend).Path
& $Py packaging/windows/launcher.py --data-dir tmp/dev-data --port 4173
```

浏览器访问 `http://127.0.0.1:4173/`。`tmp/dev-data` 仅用于本地开发；打包版默认把数据写到 `%LOCALAPPDATA%\ProjectB`。

## 测试

一键测试命令：

```powershell
python scripts/test_all.py
```

该命令运行后端测试、前端 Vitest/TypeScript/Vite、Ruff、mypy、凭据扫描和许可证验证。也可使用 `--backend` 或 `--frontend` 限定范围。当前源码快照的主进程复验结果为后端 `284 passed`、前端 `60 passed`；后续提交仍应以当次输出为准。

## Windows 单文件分发

构建目标是 Windows x64 单文件 `ProjectB.exe`，最终用户不需要安装 Python、Node.js 或 Docker：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File packaging/windows/build.ps1 -Python C:\Python314\python.exe -Output dist/ProjectB.exe
```

产物内嵌 WebUI、后端、SQLite 迁移和许可证文件，只监听 `127.0.0.1`。当前重新构建产物 SHA-256 为 `6A6A6C890EDD434798A0CB016A13463B2B4414ED4035230683A979B872704A98`，大小为 `29,215,426` 字节。它未进行 Authenticode 签名，Windows 可能显示 SmartScreen 警告；不要把该制品描述为已签名正式发布版。

## OCI 本地演示

OCI 镜像只提供无上传、无真实凭据、无真实提供方网络访问的确定性演示 profile：

```powershell
docker build --platform linux/amd64 --file packaging/oci/Dockerfile --tag projectb-demo:local .
docker run --rm --read-only --tmpfs /tmp/projectb-demo:rw,size=64m -e PROJECTB_DEMO_LOCAL_SMOKE=1 -p 127.0.0.1:7860:7860 projectb-demo:local
```

镜像以 UID/GID `10001:10001` 运行，根文件系统只读，临时状态位于 64 MiB tmpfs，并在进程内拒绝外发网络。已验证的本地镜像与 smoke 证据见 [DIST-02_EVIDENCE.md](docs/engineering/DIST-02_EVIDENCE.md)。本项目按 D-025 作为本地应用交付，不创建公网部署。

## 安全与凭据

- 本地服务固定监听 `127.0.0.1`，拒绝转发头，并使用 session cookie 与 CSRF 保护写操作。
- API key 只通过隐藏输入写入 Windows Credential Manager；状态接口只返回是否配置和更新时间，不回显明文。
- 正式路径不读取 `.env`，仓库、日志、SQLite、浏览器状态和测试快照不得包含真实凭据。
- 真实提供方默认关闭。启用时，预览绑定 profile、模型、来源哈希、token 上限和费用上限；每次同意只能使用一次。
- 上传文件、模型输出、locator 和工具参数均按不可信输入处理，包含大小、类型、路径、超时和错误脱敏限制。

## 目录结构

| 路径 | 职责 |
| --- | --- |
| `backend/projectb/` | FastAPI API、领域规则、存储、凭据与提供方端口 |
| `frontend/src/` | React WebUI、路由、视图和 API client |
| `backend/tests/`, `frontend/e2e/` | 后端、前端和浏览器合同测试 |
| `packaging/windows/` | Windows 单文件构建与 smoke |
| `packaging/oci/` | 本地演示镜像、SBOM、notice 与 smoke |
| `scripts/` | 一键测试、扫描、许可证及 CI 合同验证 |
| `docs/` | 当前工程证据、研究材料和历史归档 |
| `licenses/` | 完整第三方 notice |
| `tmp/` | 可删除的本地运行输出，不是课程证据或产品源码 |

## CI/CD

- `.gitlab-ci.yml` 保留名称严格为 `unit-test` 的 job，并包含后端、前端和 OCI 构建合同。
- `.github/workflows/ci.yml` 保留对应的 GitHub Actions 检查及 Windows 单文件构建合同。
- 两份配置均由 `scripts/verify_ci_contract.py` 做结构化校验；本地验证通过不等于远端平台已运行。
- GitHub Actions 已在每次 push 自动运行，当前提交的最终状态以[仓库 Actions 页](https://github.com/Wi1lcOAteR/Summer-Camp-ProjectB/actions)为准。GitLab CI 尚未执行，也未推送 registry 或创建公网部署。

## 第三方依赖与许可证

直接依赖记录在 `pyproject.toml` 和 `frontend/package.json`，精确版本与哈希记录在锁文件中。完整依赖闭包、许可证和再分发义务见 [licenses/THIRD_PARTY_NOTICES.md](licenses/THIRD_PARTY_NOTICES.md)；OCI 额外 notice 与 SPDX SBOM 位于 `packaging/oci/`。运行：

```powershell
python scripts/verify_licenses.py
```

## 已知限制与交付状态

- 上一版 36.64 MB 产物曾在无 Python/Node/Docker 的 Windows 11 VM 启动，最低实测为 `11.487` 秒。学生已通过 D-026 豁免当前 29.22 MB 产物的再次干净机复测及 `<=10` 秒内部指标；当前产物已通过确定性构建、归档检查和开发机 smoke，但该豁免不等于性能 PASS。
- Windows 产物未签名；SmartScreen 的实际表现依机器信誉而异。
- 项目决策 D-025 将 `ProjectB.exe` 归类为本地应用；浏览器访问 loopback WebUI，不需要远程服务端或公网部署。OCI 只作为本地确定性演示，不接受材料上传或真实提供方凭据。
- GitHub Actions 已启用；课程提交仍应确认最终 commit 的远端流水线为绿色。GitLab CI 尚未执行，本地 CI 合同通过不能替代课程平台要求的最终流水线。
- 真实 OpenAI 路径需要用户自备凭据并承担费用；自动测试只使用 mock transport，不进行付费调用。
