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
- **产出**：`docs/mockups/course-import-onboarding.html`、`course-import-onboarding-desktop.png`、`course-import-onboarding-mobile.png`；`.superpowers/` 已加入 `.gitignore`，会话密钥和失败会话文件不提交。
- **浏览器验证**：bundled Playwright 缺少 Chromium executable，未下载；使用 Microsoft Edge 150.0.4078.83。桌面 1440 × 900：body overflow=false、clipped=[]、mode overlap=false；移动 390 × 844：body overflow=false、outside=[]、mode overlap=false；page/console errors=[]。
- **交互验证**：默认 `page-cloud`；连续点击“继续”后 `permission-mode` 与 `ready-mode` 均为“按页云端处理”。
- **全路径验证**：`local`、`page-cloud`、`full-cloud` 三条路径的权限名称、外发范围和完成页名称均与选择一致；三条路径在取消课程级记忆后均显示“仅本次导入”。
- **subagent 输出 / commit hash**：未派发 subagent；阶段 A 无 PLAN task。首次导入决策与 mockup 提交：`a5b1dcf`。
- **人工修改及原因**：学生确认用多步引导并要求视觉展示；mockup 只验证信息架构与交互节奏，不替代 Open Design design system/skill 选择。
- **经验教训**：安全同意页不能只讲隐私；将真实课程规模与解析证据放在模式选择前，用户更容易理解为什么存在不同处理方式。
