# AGENT_LOG

> 本文件只记录实际发生的过程。未执行的步骤明确标为“尚未执行”。

## 2026-07-17T18:14:41+08:00 — PRE-001 启动审计

- **Task 编号**：PRE-001
- **主智能体**：OpenAI Codex（GPT-5；Codex App 的精确构建版本未向当前会话暴露）
- **触发的 Superpowers skill**：无。课程要求当前必须触发 `superpowers:brainstorming`，但当前会话技能目录、插件缓存与已暴露技能清单均未检测到 Superpowers，故未伪装或替代调用。
- **关键 prompt / context**：读取根目录 `AGENTS.md`、`SKILLS_SETUP.md`、`docs/requirements/项目要求.md`、`docs/requirements/AI4SE_Final_Project_B_应用类项目.md`；用户要求在不越过人工门禁的前提下持续推进。
- **检查结果**：
  - 仓库仅包含流程与课程文档，无既有源码或产品规约。
  - `SPEC.md`、`PLAN.md`、`SPEC_PROCESS.md`、`README.md`、`REFLECTION.md`、`.gitlab-ci.yml` 均不存在（本次仅创建真实过程所需的 `SPEC_PROCESS.md`，不创建虚假的 SPEC/PLAN/CI 证据）。
  - Superpowers 未安装/未暴露；所需核心 skills 均不可用。
  - Open Design 的 `od` 命令、skill 与 MCP 均未检测到。
  - 已从官方上游核验：Superpowers 最新 release 为 v5.1.0（commit `f2cbfbe`，MIT）；Open Design 最新 release 为 v0.15.0（commit `79e257d`，Apache-2.0）。
  - Open Design 官方当前支持 `od mcp install codex`；Windows x64 提供安装器。安装/运行新软件属于必须由用户在操作时确认或亲自完成的系统级操作，本次未执行。
  - 本地工具：Git 2.53.0.windows.3、Node 24.14.0、pnpm 11.9.0、Python 3.14.3、uv 0.11.14、Docker CLI 29.1.2。`npm.ps1` 被 PowerShell 执行策略阻止；可在后续使用 `npm.cmd`。`gh`、`gitleaks`、`claude`、`od` 未找到。
  - 已执行 `git init`。Git 随后因沙箱账号与目录所有者不同报告 `dubious ownership`；未修改用户全局 Git 配置，后续可使用 `git -c safe.directory=...` 做局部操作。
- **subagent 输出 / commit hash**：未派发 subagent；课程规定的冷启动阶段尚未到达。启动基线 commit：`4b72ced9ecfc3da0ee5691f4dbfebf8e9b593390`（课程原文、约束、Codex 配置与 `.gitignore`；commit message 已标注 Codex GPT-5）。
- **人工修改及原因**：尚无学生人工修改记录。
- **偏离、替代措施与影响**：
  - 无法调用 mandatory `brainstorming`。替代措施仅限启动审计、差距梳理和文档骨架；不得据此产出或声称产出合规 `SPEC.md`。
  - 无法自动操作 Codex App 插件界面：电脑控制规则禁止自动化 Codex 桌面应用及其扩展。需用户手动安装 Superpowers 并新建会话。
  - Open Design 未安装；在其可用前不得进行正式 UI 方向设计。
- **经验教训**：搜索摘要可能滞后；Open Design 版本必须以完整 Releases 页面为准。本次将初步摘要中的 v0.8.0 更正为 v0.15.0，未把错误版本写入正式状态。

## 2026-07-17T18:14:41+08:00 — PRE-002 提交前验证

- **Task 编号**：PRE-002
- **触发的 Superpowers skill**：无；`verification-before-completion` 同样不可用，故仅执行明确列出的手工验证，不能声称完成 Superpowers 验证步骤。
- **关键 prompt / context**：在首次本地提交前进行凭据与格式检查，不访问或输出真实凭据。
- **验证结果**：
  - 使用只返回文件名的启发式规则扫描 OpenAI/GitHub/AWS key 与私钥头：`POTENTIAL_SECRET_FILES: none`。
  - `npm.cmd --version`：11.9.0；这确认可绕过被执行策略拦截的 `npm.ps1`。
  - `git diff --cached --check` 首次指出 `.gitignore` 末尾多一个空行；已在后续过程文档提交前修正。
  - Gitleaks 尚未安装，因此本次结果是有限启发式扫描，不替代实现阶段的正式凭据扫描。
- **subagent 输出 / commit hash**：无 subagent。启动基线 commit 为 `4b72ced9ecfc3da0ee5691f4dbfebf8e9b593390`。
- **人工修改及原因**：尚无学生人工修改记录。
- **经验教训**：即使仓库只有文档，也应在首次提交前运行凭据模式扫描与 Git whitespace 检查，并明确工具能力边界。

## 2026-07-17T18:14:41+08:00 — PRE-003 过程文档提交

- **Task 编号**：PRE-003
- **触发的 Superpowers skill**：无；原因同 PRE-001。
- **关键 prompt / context**：提交当前阶段所有不依赖产品决策的过程证据。
- **subagent 输出 / commit hash**：无 subagent。过程文档 commit：`d16d3e9`。
- **人工修改及原因**：尚无学生人工修改记录。
- **验证结果**：提交前凭据模式扫描无命中文件；`git diff --cached --check` 仅报告三份 Markdown 的 EOF 空行，随后已移除。
- **经验教训**：过程日志可以引用已完成的前序 commit；本条自身的格式收尾 commit 由最终状态输出提供证据，避免递归追加日志。

## 尚未执行

- `superpowers:brainstorming` 与项目需求逐项澄清
- `SPEC.md` 的生成与用户确认
- `writing-plans`、`PLAN.md`、陌生智能体冷启动验证
- 任何实现、测试、构建、静态检查、UI 验证、凭据扫描或 CI
- 远程仓库、PR/MR、push、部署与发布

## 2026-07-17T18:19:47+08:00 — PRE-004 外部状态复查

- **Task 编号**：PRE-004
- **触发的 Superpowers skill**：无。再次检查后，插件缓存与 skills 目录仍未检测到 Superpowers。
- **关键 prompt / context**：持续 Goal 自动推进；要求以当前工作区和外部状态为准，不沿用旧结论。
- **复查结果**：
  - Git 工作区干净，HEAD 为 `1cd4427`。
  - Superpowers 插件目录：无；核心 skill 目录：无。
  - Open Design `od` 命令：无。
  - `SPEC_PROCESS.md`、`AGENT_LOG.md`、`DECISIONS_NEEDED.md` 存在；`SPEC.md`、`PLAN.md`、`README.md`、`REFLECTION.md`、`.gitlab-ci.yml` 不存在。
  - 后五项缺失并非可在当前阶段随意补空壳：`SPEC.md` 必须来自 mandatory brainstorming；`PLAN.md` 必须在用户确认 SPEC 后生成；README/CI 依赖已确认产品和技术栈；REFLECTION 仅能由学生本人撰写。
- **subagent 输出 / commit hash**：未派发 subagent；冷启动阶段尚未开放。
- **人工修改及原因**：无学生输入或外部状态变化。
- **经验教训**：持续任务每次恢复都应重新检查门禁依赖；“文件不存在”既可能是缺口，也可能是遵守阶段顺序的正确状态。

## 2026-07-17T18:21:22+08:00 — PRE-005 第三次门禁复查

- **Task 编号**：PRE-005
- **触发的 Superpowers skill**：无；第三次连续检查仍未发现 Superpowers 插件或核心 skills。
- **关键 prompt / context**：持续 Goal 的阻塞审计要求同一阻塞连续出现至少三轮，并以当前外部状态为准。
- **复查结果**：Git 工作区在复查前干净，HEAD 为 `4489e46`；Superpowers 插件目录为 `none`；核心 skills 为 `none`；Open Design 为 `none`。
- **subagent 输出 / commit hash**：未派发 subagent；阶段 C 尚未开放。
- **人工修改及原因**：连续三轮没有收到学生决策或观察到插件安装状态变化。
- **阻塞判定**：mandatory `superpowers:brainstorming` 无法调用；项目方向仍是占位文本，禁止替学生猜测；所有不依赖该门禁的审计、环境检查、过程证据与决策清单均已完成。符合持续 Goal 的第三次同条件阻塞阈值，应将 Goal 标记为 blocked，等待用户安装 Superpowers 后恢复。
- **经验教训**：无人值守流程应在真实外部依赖未变化时停止并留下可恢复入口，而不是通过重复检查制造虚假进展。

## 2026-07-17T22:05:24+08:00 — PRE-006 Superpowers 恢复与 Open Design 安装尝试

- **Task 编号**：PRE-006
- **触发的 Superpowers skill**：`using-superpowers`、`brainstorming`。已完整读取插件 v6.1.1 对应的两份 `SKILL.md`；brainstorming 的实现硬门禁继续生效。
- **关键 prompt / context**：用户要求自行安装 Open Design；只允许官方来源，不使用第三方镜像，不录入 API Key。
- **外部状态变化**：检测到官方 Codex 插件缓存已出现 Superpowers v6.1.1，包含 `brainstorming`、`writing-plans`、worktree、TDD、评审、调试与验证等核心 skills。此前的 Superpowers 阻塞已解除。
- **Open Design 官方核验**：最新版 v0.15.0（release commit `79e257d`），Windows x64，Apache-2.0；官方安装器与 `.sha256` 均由 GitHub Release 提供。
- **安装尝试与证据**：
  - 沙箱内 `curl` 无法连接 GitHub；按规则提升网络权限后仍无法连接 `github.com:443`。
  - Codex 内置浏览器打开官方下载页时超时并重置，未触发下载。
  - 成功从 `open-design.ai/install.sh` 下载并检查官方包装脚本，SHA-256 为 `5866B8465CC3475A0CE63BE379F04A3E5E9A01BA579E6E7FB54304C82EDE06B3`；脚本明确要求本机先已有 `od`，不能替代桌面安装，因此已删除临时副本。
  - 项目中不存在残留或零字节安装器。
- **人工恢复入口**：用户将从官方 GitHub Release 下载 `open-design-0.15.0-win-x64-setup.exe` 及同名 `.sha256`；安装完成后由智能体验证并执行 `od mcp install codex`。
- **subagent 输出 / commit hash**：未派发 subagent；当前仍处于阶段 A。
- **人工修改及原因**：用户选择在自动下载受阻时手动下载官方安装器。
- **经验教训**：Open Design 的 hosted `install.sh` 只是已有 CLI 的 MCP 包装器，不是桌面/CLI bootstrap；应避免把“接入 agent”和“安装产品”混为一谈。

## 2026-07-19T21:57:09+08:00 — PRE-007 阶段 A 恢复审计与 brainstorming 续接

- **Task 编号**：PRE-007
- **触发的 Superpowers skill**：沿用 PRE-006 已触发的 `using-superpowers`、`brainstorming` 流程。本次会话可调用 skill 清单未注册 `superpowers:*`；已完整读取官方缓存 v6.1.1 的两份 `SKILL.md` 并按 checklist 续接，但不把磁盘读取虚报为本次正式调用。
- **关键 prompt / context**：用户要求完整复读课程/仓库、检查 Superpowers 与 Open Design、完成当前阶段所有无决策工作，并在人工确认门禁停止；项目方向仍为占位文本。
- **检查结果**：
  - 根目录约束、`SKILLS_SETUP.md`、两份课程原文、全部已有过程文档、`.codex/config.toml`、`.gitignore` 与最近 Git 历史均已重新读取。
  - 官方插件缓存存在 Superpowers v6.1.1（MIT）及 14 个 skills；当前会话未注册这些 skills，因此阶段 B 前仍须新建/确认可调用插件的会话。
  - Open Design 官方 release v0.15.0（commit `79e257d`，Apache-2.0）与 Windows x64 资产存在。本地 309,298,247-byte 安装器的 SHA-256 与同名校验文件一致：`63fc2e609489474e99187cdf94d01d063c1dbee733aaf2464d835cdc1e96f6b5`。Authenticode 为 `NotSigned`，与上游 Windows 未签名说明一致。
  - `od`、Open Design skill/MCP、MCP resources/templates 均未检测到。安装会写入项目外目录且可能触发 SmartScreen；当前环境只允许写项目目录，未运行安装器，也未反复申请提权。
  - 当前工具版本：Git 2.55.0.windows.3、Node 24.14.0、npm 11.9.0、pnpm 11.9.0、Python 3.13.5、uv 0.11.14、Docker CLI 29.1.2；`gh`、`gitleaks`、`claude`、`od` 未找到。Docker 因用户配置读取权限警告，daemon 未验证。
- **subagent 输出 / commit hash**：未派发 subagent；当前阶段 A 且尚无 PLAN task。commit hash 将在本条过程文档提交后记录于任务输出，不递归修改本条。
- **人工修改及原因**：用户已把 Open Design 安装器和校验文件放入项目根目录；为防止 309 MB 第三方二进制误提交，智能体将这两个精确命名模式加入 `.gitignore`。
- **偏离、替代措施与影响**：本次会话不能正式调用 `superpowers:brainstorming`；替代措施是按已安装的同版本上游指令续接 PRE-006 已开始的流程并明确证据边界。此限制不阻塞需求提问，但 `writing-plans` 前必须恢复正式 skill 注册。
- **经验教训**：插件“缓存已安装”、会话“skill 已注册”和流程“实际调用”是三种不同证据，过程文档必须分别记录。

## 2026-07-19T22:00:55+08:00 — PRE-008 提交后完成验证

- **Task 编号**：PRE-008
- **触发的 Superpowers skill**：`verification-before-completion`。本次会话未注册该 skill；完整读取已安装 v6.1.1 上游指令后执行其“识别命令、全量运行、读取输出、再陈述状态”门禁，证据限制同 PRE-007。
- **关键 prompt / context**：验证 PRE-007 审计提交、阶段门禁、Superpowers 安装内容与 Open Design 状态，不验证尚不存在的业务功能。
- **验证结果**：
  - `git status --short --branch`：仅输出 `## master`；工作区干净。
  - `git show --oneline --stat HEAD`：`e29d235 docs: resume phase A audit [agent: Codex GPT-5]`，5 个文件变更，61 行新增、27 行删除。
  - `git diff HEAD^ HEAD --check`：退出码 0，无 whitespace 错误。
  - 门禁文件检查：`SPEC.md`、`PLAN.md`、`README.md`、`REFLECTION.md`、`.gitlab-ci.yml` 均不存在；当前阶段这是预期状态，不作为最终交付完成证据。
  - Superpowers manifest 版本为 6.1.1，skills 目录计数 14，必需核心项均存在。
  - Open Design：安装器哈希与 `.sha256` 匹配；Authenticode 为 `NotSigned`；`od` 命令不存在；安装器已被 Git 忽略。
- **subagent 输出 / commit hash**：无 subagent；被验证的过程提交为 `e29d235`。
- **人工修改及原因**：无。
- **经验教训**：阶段 A 的“完成验证”只证明启动审计和门禁状态，不能外推为 SPEC、实现、测试、CI 或部署完成。

## 2026-07-19T22:04:53+08:00 — BRAIN-001 真实使用场景澄清

- **Task 编号**：BRAIN-001
- **触发的 Superpowers skill**：续接 `brainstorming`；遵守一次只问一个问题、先理解目的再提出方案、用户批准设计前不实现的门禁。当前会话的 skill 注册限制见 PRE-007。
- **关键 prompt / context**：首问要求学生描述最近反复遇到且愿意用软件解决的问题；学生回答主要使用模型协助作业/项目、学习辅导和资料查找。
- **subagent 输出 / commit hash**：未派发 subagent；阶段 A 不存在 PLAN task。提交 hash 将在任务输出中记录。
- **人工修改及原因**：学生提供了三个真实使用场景；智能体仅归纳为候选主线，未替学生选择产品方向，也未创建 `SPEC.md`。
- **经验教训**：宽泛的“AI 帮我做事”能证明需求频率，但不能直接成为问题陈述；需要先确定唯一主线，再追问现有工作流的具体失败点。

## 2026-07-19T22:06:27+08:00 — BRAIN-001A 候选主线课程适配比较

- **Task 编号**：BRAIN-001A
- **触发的 Superpowers skill**：续接 `brainstorming`；未把无人值守分析计作新的对话迭代，也未跳过用户选择门禁。
- **关键 prompt / context**：用户尚未在作业/项目协作、学习辅导、资料检索三个场景中选定主线；Goal 允许等待期间开展候选方案比较。
- **分析输出**：按三模块一致性、区别于普通聊天的机制、确定性测试空间、主要风险和 WebUI 展示力形成对比矩阵；记录于 `DECISIONS_NEEDED.md` D-002。
- **subagent 输出 / commit hash**：未派发 subagent；无 PLAN task。提交 hash将在任务输出中记录。
- **人工修改及原因**：无新的学生输入；没有将分析结果写入 `SPEC.md` 或视为用户确认。
- **经验教训**：在产品方向未定时，可以比较选项的工程属性，但不能用“更容易实现/测试”替代学生对真实痛点的选择。

## 2026-07-19T22:07:52+08:00 — BRAIN-001B 人工产品决策门禁暂停

- **Task 编号**：BRAIN-001B
- **触发的 Superpowers skill**：续接 `brainstorming`；遵守目标用户、核心功能和产品主线不得由智能体代决策的门禁。
- **关键 prompt / context**：学生尚未在三个候选主线中作出选择；无人值守期间已完成课程适配比较，没有新的外部状态。
- **验证结果**：Git 工作区在记录前干净，HEAD 为 `3580eee`；`SPEC.md`、`PLAN.md` 均不存在；D-002 仍是当前未决问题。
- **subagent 输出 / commit hash**：未派发 subagent；无 PLAN task。提交 hash 将在任务输出中记录。
- **人工修改及原因**：无新的学生输入；未生成规约或实现。
- **阻塞判定**：同一产品主线决策连续三个 Goal 回合未解决，且所有无决策工作已经完成；持续 Goal 应标记为 blocked，等待学生选择后恢复。
- **经验教训**：持续执行不等于重复检查；到达人工产品门禁后应留下明确恢复入口并停止。

## 2026-07-19T22:08:59+08:00 — BRAIN-002 暂定学习辅导主线

- **Task 编号**：BRAIN-002
- **触发的 Superpowers skill**：续接 `brainstorming`；按一次一个问题和可逆假设原则继续需求澄清。
- **关键 prompt / context**：学生在三个候选主线中回复“主线走 2 试试看？”，即暂定学习辅导，但尚未确认具体痛点或完整设计。
- **subagent 输出 / commit hash**：未派发 subagent；阶段 A 无 PLAN task。提交 hash 将在任务输出中记录。
- **人工修改及原因**：学生选择了候选 2；智能体保留“试试看”的暂定语义，没有把它升级为不可逆产品承诺。
- **恢复判定**：BRAIN-001B 的产品主线阻塞已解除；从第 2 轮继续，旧 blocked 计数不沿用。
- **经验教训**：探索性选择应被记录为可验证假设，下一轮要用具体失败场景检验，而不是立即围绕标签堆功能。

## 2026-07-19T22:11:30+08:00 — BRAIN-003 理解适配与持续复习组合痛点

- **Task 编号**：BRAIN-003
- **触发的 Superpowers skill**：续接 `brainstorming`；一次只确认一个问题，并把学生选择写成可追溯的需求假设。
- **关键 prompt / context**：学生选择“解释不符合当前水平”和“对话孤立、缺少持续进度”，并明确大学学业的目标是看懂与持续复习。
- **subagent 输出 / commit hash**：未派发 subagent；阶段 A 无 PLAN task。提交 hash 将在任务输出中记录。
- **人工修改及原因**：学生把两个失败模式组合为同一主线；智能体据此要求两者共享学习状态，但未决定具体实现或技术栈。
- **阶段证据**：这是第 3 轮真实 brainstorming 迭代；已经达到课程对“至少 3 轮关键迭代”的数量下限，但 SPEC 所需内容仍远未澄清，不能提前结束阶段 A。
- **经验教训**：用户价值可能来自两个环节的闭环，而不是单点功能；关键是定义它们共享的状态与反馈，而不是简单增加功能数量。

## 2026-07-19T22:13:24+08:00 — BRAIN-003A 学习科学证据基线

- **Task 编号**：BRAIN-003A
- **触发的 Superpowers skill**：续接 `brainstorming`；在等待人工课程选择期间只开展不改变产品方向的背景研究。
- **关键 prompt / context**：暂定解决大学学业中的解释适配与持续复习；课程 D-007 尚未选择。检索并阅读自我解释、提取练习、分散练习和知识追踪的原始研究页面/摘要。
- **研究输出**：新增 `docs/research/LEARNING_SCIENCE_BASELINE.md`，分别记录研究对象、可支持的产品启发和禁止外推的边界；没有把论文结论写成已确认需求。
- **来源**：Chi et al. (1989), DOI `10.1207/s15516709cog1302_1`；Karpicke & Roediger (2008), DOI `10.1126/science.1152408`；Cepeda et al. (2006), DOI `10.1037/0033-2909.132.3.354`；Corbett & Anderson (1995), DOI `10.1007/BF01099821`。
- **subagent 输出 / commit hash**：未派发 subagent；无 PLAN task。提交 hash 将在任务输出中记录。
- **人工修改及原因**：无新的学生输入；未创建 `SPEC.md`。
- **经验教训**：学习科学证据适合约束交互和验收，但经典实验的任务、学科与人群边界必须保留，不能直接等同于产品有效性。

## 2026-07-19T22:29:48+08:00 — BRAIN-004 操作系统课件材料审计

- **Task 编号**：BRAIN-004
- **触发的 Superpowers skill**：续接 `brainstorming`；同时使用 `pdf` skill 做只读材料结构与视觉检查。
- **关键 prompt / context**：学生选择“操作系统基础”并给出本地课件目录；访问范围严格限制在该指定目录。
- **材料证据**：15 份 PDF、932 页、195,355,180 bytes；绪论 138 页、并发 279 页、虚拟化 296 页、持久化 219 页。所有文件未加密，首页为 1920 × 1080，前三页有非空文本。
- **工具与故障**：bundled Poppler 包装器找不到内部路径；MiKTeX `pdftotext` 因沙箱禁止写用户配置目录而报拒绝访问。未修改用户配置或申请提权，改用 bundled `pypdf`/`pypdfium2`。`pypdf` 报告可恢复的交叉引用对象警告，但 15 份文件均成功读取。
- **视觉验证**：临时渲染绪论、并发、虚拟化、持久化各一页为 1440 × 810 PNG，人工检查均清晰；临时文件已删除。
- **产出**：新增 `docs/research/OPERATING_SYSTEMS_MATERIAL_AUDIT.md`；只记录元数据、可读性与产品约束，不复制课件正文或图像。
- **subagent 输出 / commit hash**：未派发 subagent；阶段 A 无 PLAN task。提交 hash 将在任务输出中记录。
- **人工修改及原因**：学生提供课程名称与本地目录；智能体没有把课件加入 Git，因为许可证未知且文件仅限本地验证。
- **经验教训**：真实课件同时包含文本、代码、公式和图表；只做纯文本 RAG 会丢失关键上下文。解析器的容错警告也必须进入产品错误模型，而不是被隐藏。

## 2026-07-19T22:32:43+08:00 — BRAIN-004A 课程材料威胁模型基线

- **Task 编号**：BRAIN-004A
- **触发的 Superpowers skill**：续接 `brainstorming`；等待 D-008 人工决策期间只做不预设供应商/架构的安全分析。
- **关键 prompt / context**：操作系统课件许可证未知，材料约 195 MB；学生尚未决定是否允许最小必要片段发送到云端模型。
- **分析输出**：新增 `docs/research/COURSEWARE_THREAT_MODEL_BASELINE.md`，记录资产敏感级别、候选信任边界、12 类威胁、方案无关控制、三种数据边界影响和候选测试证据。
- **subagent 输出 / commit hash**：未派发 subagent；阶段 A 无 PLAN task。提交 hash 将在任务输出中记录。
- **人工修改及原因**：无新的学生输入；没有选择供应商、模型、存储或部署架构，也没有创建 `SPEC.md`。
- **经验教训**：数据最小化必须转化为可测不变量，例如“无确认时远端调用为零”和“请求仅含被引用页面”，否则容易停留在隐私口号。

## 2026-07-19T22:34:46+08:00 — BRAIN-005 用户可选的课件处理路径

- **Task 编号**：BRAIN-005
- **触发的 Superpowers skill**：续接 `brainstorming`；记录学生对候选方案的修正，不替其补全尚未表达的云端授权。
- **关键 prompt / context**：学生认为本地解析可能使课件内容失真，希望向用户提供可选择的处理选项。
- **采纳内容**：确认处理路径可按课程或任务选择，选择界面需呈现保真度、外发范围、凭据/费用和解析限制；模式切换不得静默扩大外发。
- **未采纳/未推断**：没有把反馈解释为允许整份 PDF 上传，也没有选择云供应商、模型或默认模式。
- **subagent 输出 / commit hash**：未派发 subagent；阶段 A 无 PLAN task。提交 hash 将在任务输出中记录。
- **人工修改及原因**：学生推翻“本地解析 + 最小片段云端调用作为单一推荐路径”的隐含收敛；智能体将其改为用户可选模式。
- **经验教训**：隐私默认不能忽视材料保真度；安全设计需要让取舍可见、可选择、可撤销，而不是用一个全局策略覆盖所有课程。

## 2026-07-19T22:40:53+08:00 — BRAIN-005A 课件解析保真度量化

- **Task 编号**：BRAIN-005A
- **触发的 Superpowers skill**：续接 `brainstorming`；使用 `pdf` skill 对已授权目录做只读全量统计，为 D-009 提供证据而不替学生选择默认模式。
- **关键 prompt / context**：学生担心本地解析使内容失真。审计脚本用 bundled `pypdf` 逐页统计文本与 PDF 资源结构，不保存课件正文。
- **验证结果**：932/932 页完成；空文本页 0，少于 100 个非空白字符的页面 95，文本中位数 226、均值 247.1 字符/页；932 页 NFKC 归一化会变化，`U+FFFD` 为 0；932 页含图像 XObject，87 页含 Form XObject；页面异常 0。
- **工具异常与恢复**：长时间 Python 子进程的 stdout 没有被外层终端捕获，前两次运行没有即时结果；改为临时 JSON 后，文件在外层进程返回后延迟落盘并包含完整统计。没有把无输出误记为成功，也不把本次时长当性能基准。
- **产出**：新增 `docs/research/COURSEWARE_PROCESSING_MODES.md`，并补充课程材料审计；临时 Python/JSON 未提交且已删除。
- **subagent 输出 / commit hash**：未派发 subagent；阶段 A 无 PLAN task。提交 hash 将在任务输出中记录。
- **人工修改及原因**：无新的学生输入；默认模式仍未决定。
- **经验教训**：文本“可抽取”与页面“保真”是不同断言。产品需要原页对照、质量报告和显式模式选择，不能只依据解析器退出码判断完整性。

## 2026-07-19T22:46:45+08:00 — BRAIN-005B 候选模块与领域模型

- **Task 编号**：BRAIN-005B
- **触发的 Superpowers skill**：续接 `brainstorming`；等待 D-009 时整理已确认信息，不把候选模型冒充已批准设计。
- **关键 prompt / context**：已确认操作系统真实课件、理解适配、持续复习、用户可选处理模式与安全约束；首次导入默认行为仍未决。
- **分析输出**：新增 `docs/research/TUTORING_DOMAIN_MODEL_DRAFT.md`，提出 M1 课程材料与保真、M2 适配解释与理解检查、M3 掌握状态与持续复习，以及跨模块安全/凭据/审计控制；记录候选实体、关系、状态流、不变量和测试种子。
- **agent 边界**：当前候选设计可以是确定性应用流程，尚未宣称 agent。若后续加入自主多轮决策/工具调用/反馈修正，需另行确认并实现可 mock 的主循环与护栏。
- **subagent 输出 / commit hash**：未派发 subagent；阶段 A 无 PLAN task。提交 hash 将在任务输出中记录。
- **人工修改及原因**：无新的学生输入；未创建 `SPEC.md`、未选择数据库/框架/模型/部署，也未决定 D-009。
- **经验教训**：跨模块合同应围绕可追溯来源和学习证据，而不是共享聊天文本；这样保真、学习与复习才能形成可测试闭环。

## 2026-07-19T22:50:40+08:00 — BRAIN-006 首次导入规则解释与确认

- **Task 编号**：BRAIN-006
- **触发的 Superpowers skill**：续接 `brainstorming`；对不清楚的候选规则先解释，不把困惑当作同意；首次真正适合视觉呈现时按 just-in-time 规则提供 visual companion 邀请。
- **关键 prompt / context**：学生询问 D-009 推荐规则的详细含义。智能体以操作系统课件为例说明三种处理模式、课程级设置、逐次外发预览、扩大授权和远端删除。
- **澄清结果**：学生确认首次导入直接询问用户，通过多个引导步骤/对话框完成说明与选择；课程级记住设置，扩大外发仍需确认。D-009 已解除。
- **subagent 输出 / commit hash**：未派发 subagent；阶段 A 无 PLAN task。首次导入决策与 mockup 提交：`a5b1dcf`。
- **人工修改及原因**：学生采纳显式首次引导，并要求提供界面展示；仍未创建 `SPEC.md` 或正式 UI 实现。
- **经验教训**：用户提出“是什么意思”说明抽象安全规则不足以支持决策；解释必须落到具体数据流。即便解释充分，也不能把没有反对当作默认同意。

## 2026-07-19T23:00:55+08:00 — BRAIN-007 首次导入可交互 mockup

- **Task 编号**：BRAIN-007
- **触发的 Superpowers skill**：续接 `brainstorming` 的 visual companion just-in-time 流程；使用 `visualize` skill 制作可交互 UI mockup，并按前端视觉 QA 要求检查桌面/移动视图。
- **关键 prompt / context**：学生从未见过 visual companion，明确要求用界面展示已确认的首次导入引导。
- **工具故障与替代**：visual companion 第一次因 Git Bash PATH 缺少标准工具失败，第二次到端口绑定时因 `127.0.0.1:55535` EACCES 失败；未继续重试或申请提权。Open Design `od` 仍不存在。替代为项目内自包含 HTML mockup和本地截图，影响是无法通过 companion 事件文件收集点击数据，需以聊天反馈为准。
- **产出**：`docs/mockups/course-import-onboarding.html`、`course-import-onboarding-v1-desktop.png`、`course-import-onboarding-v1-mobile.png`；`.superpowers/` 已加入 `.gitignore`，会话密钥和失败会话文件不提交。截图在 BRAIN-008 更新界面后加上 `v1` 标识，以免被误认为新版视觉证据。
- **浏览器验证**：bundled Playwright 缺少 Chromium executable，未下载；使用 Microsoft Edge 150.0.4078.83。桌面 1440 × 900：body overflow=false、clipped=[]、mode overlap=false；移动 390 × 844：body overflow=false、outside=[]、mode overlap=false；page/console errors=[]。
- **交互验证**：默认 `page-cloud`；连续点击“继续”后 `permission-mode` 与 `ready-mode` 均为“按页云端处理”。
- **全路径验证**：`local`、`page-cloud`、`full-cloud` 三条路径的权限名称、外发范围和完成页名称均与选择一致；三条路径在取消课程级记忆后均显示“仅本次导入”。
- **subagent 输出 / commit hash**：未派发 subagent；阶段 A 无 PLAN task。首次导入决策与 mockup 提交：`a5b1dcf`。
- **人工修改及原因**：学生确认用多步引导并要求视觉展示；mockup 只验证信息架构与交互节奏，不替代 Open Design design system/skill 选择。
- **经验教训**：安全同意页不能只讲隐私；将真实课程规模与解析证据放在模式选择前，用户更容易理解为什么存在不同处理方式。

## 2026-07-19T23:32:52+08:00 — BRAIN-008 导入引导信息层级修订

- **Task 编号**：BRAIN-008
- **触发的 Superpowers skill**：续接 `brainstorming` 与 visual companion 迭代；使用 `visualize` skill 修改已批准的需求阶段 mockup，并使用 `browser:control-in-app-browser` 尝试双端验证。
- **关键 prompt / context**：学生认可第一版，并要求用字体大小、颜色、字重和字体建立二级展示，使用图标减少冗余文字；桌面端与移动端均采用 X 轴时间线；“开始学习”页需强调配置修改位置。
- **采纳内容**：将左侧竖向阶段栏改为顶部四节点横向时间线；在桌面端和移动端保持同一 X 轴阅读方向；处理模式改为“图标 + 标题 + 简述 + 短事实”；强调“不会静默切换”；完成页突出路径“课程设置 › 材料与隐私”，最终主操作改为“开始学习”。
- **验证故障与替代**：项目外置 Node 依赖暴露 `playwright` 但缺少配套 `playwright-core`，首次自动化脚本未启动。随后按 Browser skill 使用应用内浏览器，但 `file://` 页面被其 URL 安全策略拒绝；遵守策略未改用本地端口、其他浏览器或间接绕过。
- **本次验证证据**：临时 Node 静态检查通过，覆盖交互脚本语法、成对标签、四列横向时间线与进度更新、900/560 px 响应式规则、模式图标/短事实、设置路径、最终按钮文案及无外部资源依赖；`failures=[]`。这只能证明结构与脚本约束，不证明新版视觉没有裁切或重叠。
- **截图证据边界**：旧桌面/移动截图重命名为 `course-import-onboarding-v1-*.png`，只保留第一版历史证据；新版尚无浏览器截图或视觉验收，不得引用 v1 截图证明 v2。
- **规约沉淀**：创建 `SPEC.md` 阶段 A 工作草案，并更新候选领域模型中已经过时的 D-009 状态；未决产品/部署/技术选择仍明确保留，没有作为已批准设计写入。
- **subagent 输出 / commit hash**：未派发 subagent；阶段 A 无 PLAN task。第二版 mockup、阶段 A `SPEC.md` 草案与过程修订提交：`64a1cde`。
- **人工修改及原因**：学生直接确认视觉方向并给出具体修订，不涉及正式框架、模型、数据库或部署选择；仍未进入正式 UI 实现。
- **经验教训**：阶段进度、关键风险和后续配置入口属于不同视觉层级；把它们都写成正文会增加扫描负担，应该分别用时间线、强调条与位置路径承载。

## 2026-07-19T23:40:56+08:00 — BRAIN-009 第一版用户边界提问

- **Task 编号**：BRAIN-009
- **触发的 Superpowers skill**：续接 `brainstorming`；在阶段 A 工作草案形成后选择影响面最大的未决问题，并保持一次只询问一项。
- **关键 prompt / context**：当前证据以学生本人、本地操作系统课件和用户控制外发为中心，但课程最终要求可访问 WebUI；单用户本地优先、单用户云端实例和多用户服务会导致不同的认证、凭据、存储、部署与删除模型。
- **候选与推荐**：在 `DECISIONS_NEEDED.md` D-010 比较三种边界，推荐单用户、本地优先 WebUI，并使用不含私人课件/真实 key 的公开演示满足课程 URL；该推荐不等于学生确认。
- **subagent 输出 / commit hash**：未派发 subagent；阶段 A 无 PLAN task。D-010 候选比较提交：`cfdc6d1`。
- **人工修改及原因**：尚未收到学生对 D-010 的回答；未选择认证、数据库、凭据后端、部署或分发技术。
- **经验教训**：把“网页界面”等同于“多用户云服务”会过早扩大安全与运维范围；应先确认真实用户和数据所在位置，再选框架。

## 2026-07-19T23:46:48+08:00 — BRAIN-009A 单用户本地优先边界确认

- **Task 编号**：BRAIN-009A
- **触发的 Superpowers skill**：续接 `brainstorming`；接收 D-010 人工决定后同步设计，不把“桌面窗口也可以”用于绕过课程 WebUI 硬要求。
- **关键 prompt / context**：学生回答“我觉得本机好，做成WebUI或者桌面窗口都好，多用户服务虽然挺好（比如可以分享课件，资料等），但是感觉不急着做”。
- **确认结果**：第一版采用单用户、本地优先 WebUI；桌面窗口仅作为可选壳。注册、登录、多租户、分享、教师视角和跨设备同步延期，不进入第一版。
- **分析与安全补充**：新增 `docs/research/USER_DEPLOYMENT_BOUNDARY_OPTIONS.md`，比较三种路线的拓扑、数据、凭据、测试和迁移；本地 WebUI 增补 loopback、`Host`/`Origin`、CORS 与 CSRF 风险/验收，避免把无登录误解为无访问控制。
- **subagent 输出 / commit hash**：未派发 subagent；阶段 A 无 PLAN task。D-010 结果、研究基线与规约同步提交：`0b3ed66`。
- **人工修改及原因**：学生作出用户/运行边界决定；智能体只依据课程硬要求将 WebUI 定为交付基线，没有选择语言、框架、数据库、provider、分发或公开部署。
- **经验教训**：本地优先减少服务器数据风险，但会引入 localhost 浏览器攻击面和公开演示双配置；这些不能因为“只有一个用户”而省略测试。

## 2026-07-19T23:52:05+08:00 — BRAIN-010 首个学习闭环知识点提问

- **Task 编号**：BRAIN-010
- **触发的 Superpowers skill**：续接 `brainstorming`；D-010 收敛后回到产品核心，一次只询问一个能把“看懂”转为客观验收的知识点。
- **关键 prompt / context**：操作系统课件真实包含并发/互斥/同步/并发 bugs、进程/调度、地址空间等主题；目前 M2/M3 仍缺少首个具体知识点、题型和延迟复习成功标准。
- **候选与推荐**：在 `DECISIONS_NEEDED.md` D-011 比较互斥与竞态、进程与调度、地址空间与地址转换；推荐互斥/竞态，因为可同时覆盖概念、代码轨迹、错误诊断、修复比较和变式复习。推荐不等于学生确认。
- **subagent 输出 / commit hash**：未派发 subagent；阶段 A 无 PLAN task。D-011 候选比较提交：`26ba7a2`。
- **人工修改及原因**：尚未收到学生对 D-011 的回答；未创建题目、复制课件正文或选择实现技术。
- **经验教训**：只有把“看懂”绑定到学生产出的可观察行为和延迟后的变式表现，才能避免把阅读解释或模型自评误当成学习效果。

## 2026-07-19T23:57:51+08:00 — BRAIN-010A 互斥与竞态纵向切片确认

- **Task 编号**：BRAIN-010A
- **触发的 Superpowers skill**：续接 `brainstorming`；在学生明确授权从 D-011 既有候选中选择后采用已推荐方案，并限制授权外延。
- **关键 prompt / context**：学生回答“没啥偏好的，你随便搞一个吧”，随后要求今后提问时使用阻断信号以便及时发现。
- **选择与范围**：采用互斥与竞态条件；首轮只包含共享状态、非原子读-改-写、线程交错、竞态、临界区和一种互斥修复的安全性理由。同步原语大全、内存模型、死锁证明和公平性算法延期。
- **规约与研究输出**：新增 `docs/research/FIRST_LEARNING_LOOP_CANDIDATES.md`；M2 写入三类起点探针、适配解释与轨迹/迁移检查；M3 写入 `demonstrated_now -> retained` 的后续证据门禁；新增参数化 oracle/provider mock 隔离验收。
- **subagent 输出 / commit hash**：未派发 subagent；阶段 A 无 PLAN task。D-011 结果、候选闭环与规约提交：`84e84ac`。
- **人工修改及原因**：学生授权该知识点选择；智能体没有借此决定复习间隔、agent、provider、整份云端处理、分发或部署。
- **经验教训**：无偏好授权仍应绑定已公开的候选、推荐依据和排除范围；“随便”不能被解释为对所有后续产品决定的空白授权。

## 2026-07-20T00:08:54+08:00 — BRAIN-010B 互斥/竞态本地来源页映射

- **Task 编号**：BRAIN-010B
- **触发的 Superpowers skill**：续接 `brainstorming`；使用 `pdf` skill 在 D-011 已确认后定位真实来源，不创建正式题库或复制受限材料。
- **关键 prompt / context**：首个纵向切片需要可追溯来源，但课件许可未知且纯文本无法保留线程颜色、时间轴、箭头、临界区和代码分组。
- **只读扫描**：对多处理器编程、互斥、互斥进阶、并发 bugs 四份 PDF 做通用信号统计，命中页分别为 18/47、31/38、31/35、24/69；`pypdf` 的既有交叉引用警告可恢复，四份均完成。
- **视觉验证**：用 `pypdfium2`/Pillow 临时渲染 7 页并检查；主要候选收敛为多处理器编程第 25/27 页和互斥第 2/14 页；并发 bugs 第 8/59/66 页与互斥进阶延期。
- **产出与许可证边界**：新增 `docs/research/MUTEX_RACE_SOURCE_MAP.md`，只提交文件名、页码、通用标签、用途、保真约束和测试不变量；课件、正文与图像均未加入 Git。
- **清理故障**：临时 Python 脚本已删除。托管环境拒绝递归及逐文件 `Remove-Item`，`apply_patch` 无法读取二进制 PNG；停止继续绕过并将 `tmp/` 加入 `.gitignore`。8 个预览文件共 3,538,417 bytes 留在本机 ignored 目录，不提交或分发。
- **subagent 输出 / commit hash**：未派发 subagent；阶段 A 无 PLAN task。来源映射、过程证据与忽略规则提交：`25c4070`。
- **人工修改及原因**：无新产品决定；未选择 provider、处理模式目录、复习间隔或实现技术。
- **经验教训**：页面关键词只能缩小人工复核范围；代码与时序图的视觉语义必须由原页对照承担。清理失败也必须如实记录，不能把 Git 忽略冒充物理删除。

## 2026-07-20T00:10:58+08:00 — BRAIN-011 复习时间语义人工门禁

- **Task 编号**：BRAIN-011
- **触发的 Superpowers skill**：续接 `brainstorming`；互斥/竞态切片与来源完成后，一次只询问 M3 中影响最大的目标日期语义。
- **关键 prompt / context**：学生要求今后需要回答问题时发出阻断信号，以免问题被普通进度淹没。当前 `Course.target_date`、`ReviewTask.due_at/reason` 和复习成功窗口仍未定义。
- **候选与推荐**：在 `DECISIONS_NEEDED.md` D-012 比较“可选目标日期 + 自适应安排”、仅长期掌握、手动日期；推荐可选目标日期，在没有日期时退化为长期复习，不预设普适间隔算法。
- **subagent 输出 / commit hash**：未派发 subagent；阶段 A 无 PLAN task。D-012 候选比较提交：`aea59e0`。
- **人工修改及原因**：尚未收到学生对 D-012 的回答；未选择调度算法、固定间隔、通知渠道或日历集成。
- **经验教训**：复习“何时发生”是产品语义而不只是 cron 参数；如果不先确定目标日期角色，调度算法和 UI 都会把未经确认的学习策略固化。

## 2026-07-20T00:18:53+08:00 — BRAIN-011A 增量课程与期末周模式收敛

- **Task 编号**：BRAIN-011A
- **触发的 Superpowers skill**：续接 `brainstorming`；在 D-012 人工回答后，把新产品语义落实为阶段 A 研究与规约，不进入 `writing-plans` 或正式实现。
- **关键 prompt / context**：学生先回答“我觉得持续安排吧，因为最后需要模型根据用户上传的重点详情进行针对性学习。顺便提醒一下，一般来说课件不会在一开学的时候就全给你，所以我们更类似‘导入课件→确认可以学习/复习的知识→筹划学习计划→引导用户学习’这样的操作”，随后补充“考试日期一般在学期末给定，用户划定考试日期以后其实就可以进入期末周学习模式，进行拟合往年卷，重点突击老师给定的重点等行为”。
- **分析与规约结果**：确认 `continuous` 为默认学期中模式；新材料按 `MaterialBatch` 增量导入，候选知识覆盖需经 `CoverageDecision` 后才进入版本化 `LearningPlan`。有效考试日期只是进入条件之一，用户显式操作后才进入 `finals`；往年卷/老师重点作为显式材料角色映射到已确认知识，优先级保留来源、置信度和用户修正。将“拟合往年卷”限定为结构/题型/知识点/难度分析与同类练习，不推断训练、微调、原题预测或自动上传授权。
- **产出**：新增 `docs/research/INCREMENTAL_COURSE_WORKFLOW.md`；更新 `DECISIONS_NEEDED.md`、`SPEC.md`、`SPEC_PROCESS.md`、调度语义、领域模型、威胁模型和操作系统材料审计。新增 AC-15 至 AC-20，覆盖增量幂等、部分失败、历史保留、日期/模式分离、映射确认和无训练/自动上传路径。
- **验证证据**：`git diff --check`、本地 Markdown 链接目标检查、代码围栏平衡检查和强特征凭据正则扫描均通过；`gitleaks` 与 `detect-secrets` 未安装，未声称执行它们。无正式实现测试，符合阶段 A 门禁。
- **subagent 输出 / commit hash**：未派发 subagent；阶段 A 无 PLAN task。规约与研究文档提交：`adbac3d`。
- **人工修改及原因**：学生决定了双模式核心语义；智能体仅选择了与该语义一致的领域命名、状态、不变量和候选测试，未替学生决定期末窗口、每日上限、具体调度算法、答案/笔记范围、provider、部署或 agent。
- **经验教训**：考试日期不应成为开学时的硬依赖；把“材料到达”和“用户确认知识”分成两个版本化事件，才能同时支持不完整课件、持续复习和期末突击而不重写学习历史。

## 2026-07-20T00:34:54+08:00 — BRAIN-012 第一版 Agent 自主性人工门禁

- **Task 编号**：BRAIN-012
- **触发的 Superpowers skill**：续接 `brainstorming`；在双模式主流程明确后，准备“是否包含课程定义的 agent”这一重大产品/架构选择，一次只保留一个当前人工问题。
- **关键 prompt / context**：学生希望模型依据用户上传的重点详情做针对性学习，但尚未说明模型应由应用流程调用，还是要自主选择工具并循环修正。课程 Project B 原文明确无 agent 也合规；有 agent 时才触发自编码循环、工具分发、治理护栏和 mock/stub 确定性测试义务。
- **候选与推荐**：新增 `docs/research/AGENT_BOUNDARY_OPTIONS.md`，比较 1）受约束 AI 功能、无课程定义 agent；2）只生成可审查计划提案的有界规划 agent；3）全流程学习教练 agent。推荐方案 1；若学生明确希望展示 agent，方案 2 是可控折中，方案 3 延期。
- **共同边界**：三种方案都可使用模型做候选知识映射、适配解释、练习生成和期末资料分析；模型均不得扩大外发、读取凭据、绕过用户确认、给自己评分后写掌握状态或直接激活计划。
- **验证证据**：本地 Markdown 引用目标检查、代码围栏平衡、`git diff --check` 和强特征凭据正则扫描通过；无实现或测试代码，未跨越阶段 A 门禁。
- **subagent 输出 / commit hash**：未派发 subagent；阶段 A 无 PLAN task。D-013 候选边界提交：`5fd7a7a`。
- **人工修改及原因**：尚未收到学生对 D-013 的选择；未创建 agent 主循环、工具、prompt、依赖或 PLAN task，也未把推荐写成最终 SPEC 范围。
- **经验教训**：“使用 LLM”与“构建 agent”必须分别确认；否则很容易为了标签加入自主循环，却没有证明它比可测试的应用状态机解决了更多真实用户问题。

## 2026-07-20T00:40:04+08:00 — BRAIN-012A D-013 第二次门禁复查

- **Task 编号**：BRAIN-012A
- **触发的 Superpowers skill**：续接 `brainstorming`；这是 D-013 后的自动 Goal 续接复查，不引入新的产品问题。
- **当前证据**：工作区干净，HEAD 为 `ebec1cf`；`DECISIONS_NEEDED.md` 仍将 D-013 标为当前人工门禁，`SPEC.md` 未把 agent 推荐写成最终范围，`PLAN.md` 不存在；`od` 命令仍未找到。
- **阻塞判定**：尚未收到用户对方案 1/2/3 的选择；根据课程门禁，不能生成 PLAN、创建 agent 主循环或开始实现。当前没有不依赖该选择且能实质推进的安全任务。
- **subagent 输出 / commit hash**：未派发 subagent；本次复查以 D-013 过程日志提交 `ebec1cf` 为当前基线，不产生功能或规约提交。
- **人工修改及原因**：没有产品文档修改；保留 D-013 原问题和候选，避免把自动续接误记为人工确认。
- **经验教训**：人工门禁复查应核对外部状态和工作区，而不是重复提出新问题或用无关文档制造进度。

## 2026-07-20T00:42:01+08:00 — BRAIN-012B D-013 第三次门禁复查与阻塞

- **Task 编号**：BRAIN-012B
- **触发的 Superpowers skill**：续接 `brainstorming`；完成同一人工门禁的第三次连续状态审计。
- **当前证据**：工作区干净，HEAD 为 `54dbfaa`；D-013 仍是 `DECISIONS_NEEDED.md` 的当前人工门禁；`SPEC.md` 仍显示未签字确认；`PLAN.md` 不存在；`od` 命令仍未找到。
- **阻塞判定**：连续三次 Goal 复查均未收到方案 1/2/3 选择，且没有不依赖该选择而能实质推进的安全任务；当时已达到调用 `update_goal(status=blocked)` 的条件，但本轮尚未调用该工具即收到学生输入，故没有把未执行的状态写成已完成动作。
- **subagent 输出 / commit hash**：未派发 subagent；本次复查基于门禁提交 `54dbfaa`，不创建功能或规约提交。
- **人工修改及原因**：只追加本条审计记录；没有猜测 agent 范围、创建 PLAN 或开始实现。
- **经验教训**：达到三次相同门禁后应正式停止 Goal，而不是继续重复询问或消耗运行资源。

## 2026-07-20T00:43:07+08:00 — BRAIN-013 受约束 AI 功能确认

- **Task 编号**：BRAIN-013
- **触发的 Superpowers skill**：续接 `brainstorming`；学生在 D-013 门禁后明确选择模型自主性边界。
- **学生原始回答**：“就用受约束AI功能吧”。
- **选择结果**：采用方案 1。第一版使用模型完成候选知识映射、适配解释、练习生成、往年卷结构/题型/知识点/难度分析和反馈；不包含课程定义的自主 agent，不创建自主工具选择/循环修正主循环。
- **权威边界**：应用状态机、版本化规则、确定性 oracle 和用户确认负责材料外发、知识覆盖、计划修订、优先级和掌握状态；模型输出只能通过 schema、来源、预算、超时和错误隔离进入候选流程。
- **规约影响**：D-013 标为已确认；SPEC 的技术选型不再把 agent 边界写成未决，但仍保留 provider、模型端口和具体技术栈选择。`AGENT_BOUNDARY_OPTIONS.md` 作为被否决/延期方案的决策证据保留。
- **subagent 输出 / commit hash**：未派发 subagent；受约束模型端口合同与规约同步提交：`9a4db15`。
- **人工修改及原因**：学生明确选择方案 1；智能体没有据此替学生决定 provider、模型、分发、部署、间隔算法或 SPEC 整体签字。
- **经验教训**：确认“不做 agent”不是取消 AI，而是把模型能力限制在可审查候选和解释端口，以便继续验证学习效果与安全边界。

## 2026-07-20T00:51:22+08:00 — BRAIN-014 远端课程材料能力人工门禁

- **Task 编号**：BRAIN-014
- **触发的 Superpowers skill**：续接 `brainstorming`；D-013 解除后审计阶段 A 未决项，把数据边界拆成“能力目录”和后续 provider 选择，一次只询问前者。
- **关键 prompt / context**：学生已要求本地解析失真时应有用户可选路径，且首次导入必须显式选择/按课程记住；但从未明确授权第一版提供整份 PDF/课程云端上传。真实操作系统材料许可证未知，样本为 195 MB/932 页。
- **候选与推荐**：新增 `docs/research/REMOTE_MATERIAL_CAPABILITY_OPTIONS.md`，比较 1）本地 + 经确认页面/片段远端；2）再增加整份 PDF/课程远端；3）课程材料完全本地。推荐方案 1，它仍给用户数据边界选择，同时把第一版远端生命周期限制在任务级页面/片段。
- **过程修正**：`COURSEWARE_PROCESSING_MODES.md` 不再把已确认的 D-009 写成未决，并链接受约束模型端口；D-008 明确默认交互已解除，整份能力由 D-014 单独确认。
- **验证证据**：本地 Markdown 链接、代码围栏、过时 D-009 表述、`git diff --check` 和强特征凭据正则扫描均通过；没有上传材料或调用 provider。
- **subagent 输出 / commit hash**：未派发 subagent；阶段 A 无 PLAN task。D-014 候选边界提交：`2b6e3b1`。
- **人工修改及原因**：尚未收到学生对 D-014 的回答；未选择 provider、模型、留存政策、凭据或实现技术。
- **经验教训**：让用户选择处理路径不等于产品必须在第一版实现所有可能的外发层级；能力上限本身需要明确授权和可验证的生命周期。

## 2026-07-20T00:55:17+08:00 — BRAIN-014A D-014 第二次门禁复查

- **Task 编号**：BRAIN-014A
- **触发的 Superpowers skill**：续接 `brainstorming`；这是 D-014 后的自动 Goal 续接复查，不引入新的产品问题。
- **当前证据**：工作区干净，HEAD 为 `5d943e1`；`DECISIONS_NEEDED.md` 仍将 D-014 标为当前人工门禁，`SPEC.md` 仍未签字，`PLAN.md` 不存在；`od` 命令仍未找到。
- **阻塞判定**：尚未收到用户对远端材料能力方案 1/2/3 的选择；处理模式目录、删除合同和 provider 筛选都依赖该上限，不能继续定稿或进入计划。当前没有不依赖该选择且能实质推进的安全任务。
- **subagent 输出 / commit hash**：未派发 subagent；本次复查以 D-014 过程日志提交 `5d943e1` 为当前基线，不产生功能或规约提交。
- **人工修改及原因**：没有修改 D-014 候选或替学生选择；只追加真实复查证据。
- **经验教训**：材料能力上限未确认时，提前选择 provider 会把供应商能力反向固化为未经授权的产品边界。

## 2026-07-20T00:57:31+08:00 — BRAIN-015 用户控制的三模式外发范围确认

- **Task 编号**：BRAIN-015
- **触发的 Superpowers skill**：续接 `brainstorming`；学生在 D-014 门禁后明确选择由平台提供能力、用户决定外发层级。
- **学生原始回答**：“外发决策也留给用户自行决定吧，我们的平台只要实现对应的功能即可”。
- **选择结果**：按上下文采用 D-014 方案 2。第一版正式提供 L（本地）、P（经确认页面/片段远端）和 F（整份 PDF/课程远端）；没有默认/静默外发。课程记住模式，但每批新增文件、内容哈希变化、扩大范围和更换 provider 均需新的精确 `ConsentRecord`。
- **规约与研究输出**：新增 `docs/research/REMOTE_FILE_LIFECYCLE_CONTRACT.md`，定义 `RemoteMaterialObject` / `RemoteJob`、文件级授权、上传/索引/失败/删除状态、幂等、切换、对账、适配器能力声明和 12 类确定性场景；同步 SPEC AC-25 至 AC-29、威胁 T-18、领域模型和处理模式目录。
- **安全边界**：F 文件只有 `ready` 才能进入模型端口；端口仍使用本地 `source_id` 并映射回页码。从 F 切回 L/P 后立即禁止新 F 请求；删除未知/失败显示 `delete_incomplete`，不能伪报成功。
- **验证证据**：`git diff --check`、本地 Markdown 链接、代码围栏、过时 D-014/F 未决表述和强特征凭据正则扫描通过；没有上传真实材料、创建凭据或调用 provider。
- **subagent 输出 / commit hash**：未派发 subagent；阶段 A 无 PLAN task。三模式与生命周期合同提交：`fe94963`。
- **人工修改及原因**：学生选择让平台实现全部外发层级；智能体没有据此替学生选择 provider、数据政策、容量/费用、凭据或实际课件权利结论。
- **经验教训**：课程级模式记忆不能代替新增文件的 payload 授权；否则“用户选择”会在后续增量导入时退化为静默整份上传。

## 2026-07-20T01:02:00+08:00 — BRAIN-016 Provider 适配策略人工门禁

- **Task 编号**：BRAIN-016
- **触发的 Superpowers skill**：续接 `brainstorming`；D-014 解除后将 provider 选择拆成适配策略问题，避免同时决定厂商、模型、区域和凭据。
- **关键 prompt / context**：平台已确认实现 L/P/F 三种能力，用户决定具体外发层级；模式 F 需要真实上传、索引、引用、删除和政策展示。Provider 仍未选。
- **官方资料核验**：OpenAI Developer Docs MCP 读取 File Search、Files/Vector Stores 删除参考与 Data controls；确认官方文档展示 PDF 文件上传、vector store 状态、文件引用、删除入口、`expires_after` 说明及文件/向量库应用状态保留规则。Google/Anthropic 官方站点本轮通过 web/PowerShell 均连接失败，未将其能力写成事实。
- **候选与推荐**：新增 `docs/research/PROVIDER_STRATEGY_OPTIONS.md`，比较统一适配器 + 一个真实参考 provider、单 provider 紧耦合、多个真实 provider；推荐方案 1。
- **验证证据**：本地 Markdown 链接、代码围栏、`git diff --check` 和强特征凭据正则扫描通过；未读取或提交任何 API key，未调用真实 API。
- **subagent 输出 / commit hash**：未派发 subagent；阶段 A 无 PLAN task。D-015 候选策略提交：`2444b87`。
- **人工修改及原因**：尚未收到学生对 D-015 的选择；未创建 adapter、凭据流程实现、provider SDK 依赖或 PLAN task。
- **经验教训**：先确定“适配器策略”再选择厂商，可以把用户外发控制和生命周期合同留在领域层，也能避免不完整的官方资料被误当成产品承诺。
