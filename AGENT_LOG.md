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

## 2026-07-20T01:18:36+08:00 — BRAIN-016A D-015 第二次门禁复查

- **Task 编号**：BRAIN-016A
- **触发的 Superpowers skill**：续接 `brainstorming`；这是 D-015 后的自动 Goal 续接复查，不扩展候选范围。
- **当前证据**：工作区干净，HEAD 为 `f9ebb13`；D-015 仍是当前人工门禁，`SPEC.md` 未签字，`PLAN.md` 不存在；`od` 命令仍未找到。
- **阻塞判定**：尚未收到 provider 策略方案 1/2/3 的选择；真实 adapter、凭据、数据政策和 F 端到端测试依赖该策略。当前没有不依赖该选择且能实质推进的安全任务。
- **subagent 输出 / commit hash**：未派发 subagent；本次复查以 D-015 过程日志提交 `f9ebb13` 为当前基线，不产生功能或规约提交。
- **人工修改及原因**：没有替学生选择 provider 策略或继续调查未选厂商；只追加真实复查证据。
- **经验教训**：自动续接遇到同一人工门禁时，应核对当前状态并停止，而不是用更多 provider 名单制造虚假进展。

## 2026-07-20T01:19:58+08:00 — BRAIN-016B D-015 第三次门禁复查与阻塞

- **Task 编号**：BRAIN-016B
- **触发的 Superpowers skill**：续接 `brainstorming`；这是 D-015 的第三次连续 Goal 状态审计，不引入新的产品选择。
- **当前证据**：工作区干净，HEAD 为 `b917d58`；D-015 仍是当前人工门禁，`SPEC.md` 未签字，`PLAN.md` 不存在；`od` 命令仍未找到。
- **阻塞判定**：连续三次 Goal 审计均未收到 provider 适配策略方案 1/2/3 的选择，且当前没有不依赖该选择而能实质推进的安全任务；已达到 `update_goal(status=blocked)` 的门槛，本条审计提交完成后调用该阻断信号。
- **subagent 输出 / commit hash**：未派发 subagent；本次审计以 `b917d58` 为基线，只追加过程日志，不产生功能或规约修改。
- **人工修改及原因**：没有替学生选择 provider、凭据、API 或 adapter，也没有生成 `PLAN.md`；只记录第三次真实复查与阻断条件。
- **经验教训**：同一人工门禁连续三次没有变化时，应正式标记 Goal 阻塞，而不是继续重复审计或消耗运行资源。

## 2026-07-20T01:33:25+08:00 — BRAIN-017 用户配置 Provider 与统一适配器确认

- **Task 编号**：BRAIN-017
- **触发的 Superpowers skill**：续接 `brainstorming`；学生恢复此前因 D-015 阻塞的 Goal，并给出 provider 适配架构方向。没有进入 `writing-plans`。
- **关键 prompt / context**：学生原始回答为“供应商让用户自己在config里面配置喽，我们写好适配器就行”。按最小语义确认统一 `ProviderAdapterRegistry`，用户在本地设置中选择平台已实现的 adapter/profile，领域层不硬编码供应商。
- **安全与范围解释**：普通 config 只含 adapter ID、模型、受控参数、预算和 `credential_ref`；key/token 仍由隐藏录入进入本机安全凭据存储。未把回答解释为允许任意 endpoint、第三方插件、明文 secret，或已选择具体 provider/模型/区域/政策。未知/坏配置与能力不足在联网前失败关闭；配置/政策变化使旧 consent 失效。
- **规约产出**：D-015 标为已确认架构方向；`SPEC.md` 新增 profile/能力快照与 AC-30 至 AC-32；同步远端生命周期、模型端口、威胁、领域模型、处理模式和历史候选。D-016 缩小为首版交付一个还是多个真实 adapter 的人工门禁。
- **subagent 输出 / commit hash**：`/root/d015_audit` 先完成只读交叉审计，后只修改四份 provider/生命周期研究合同；`/root/next_gate_audit` 只读梳理后续门禁，后只修改三份威胁/领域/处理模式文档。两者均报告 scoped `git diff --check`、围栏、链接与强特征凭据扫描通过，未提交 Git。主智能体在基线 `0e06cbc` 上整合核心规约；本轮最终 commit 在任务输出记录。
- **人工修改及原因**：学生决定 provider 由最终用户配置、平台负责 adapter；智能体仅补充课程强制的 secret 分离、失败关闭和授权隔离，没有替学生选择真实 adapter 数量或厂商。
- **经验教训**：“用户可配置 provider”必须拆成注册表、非秘密 profile、凭据引用和能力/政策快照；否则容易同时退化成明文 key、任意 URL 和无法审计的兼容性承诺。

## 2026-07-20T01:46:35+08:00 — AUDIT-002 Requirements 当前符合性复核

- **Task 编号**：AUDIT-002
- **触发的 Superpowers skill**：当前仍在 `brainstorming` 阶段；按 `verification-before-completion` 的证据纪律逐项读取命令输出，但本会话未注册该 skill，因此不把手工复核虚报为正式调用。
- **关键 prompt / context**：学生要求确认项目当前是否仍符合 requirements 文件夹文档。实际课程原文位于 `docs/requirements/`；完整读取通用要求与 Project B 应用类要求，并与 `AGENTS.md`、当前 SPEC/过程文档、文件清单和 Git 历史对照。
- **实际检查**：确认 `SPEC.md`、`SPEC_PROCESS.md`、`AGENT_LOG.md` 存在；`PLAN.md`、README、REFLECTION、正式源码、测试命令、GitHub/GitLab CI、分发产物和部署 URL 不存在；`od` 仍不可用；非文档正式源码计数为 0。检查到 `SPEC_PROCESS.md` 页首仍错误写“尚未形成 SPEC”，已立即修正。
- **审计结论**：项目仍符合 Project B 选题边界，并基本遵守阶段 A 门禁；当前不满足最终交付要求。缺失的 PLAN/实现/TDD/CI/分发等大多是阶段门禁后的硬任务，不等于豁免；Open Design、Superpowers 阶段 B 注册、技术/分发选型、双远程平台策略和过程反思是签字或后续阶段前的明确缺口。
- **产出与证据边界**：新增 `docs/REQUIREMENTS_COMPLIANCE_AUDIT.md` 四态矩阵，并将 `docs/PROJECT_AUDIT.md` 明确标为启动历史快照；没有创建空壳 PLAN、README、CI、测试或 REFLECTION，也没有声称任何实现验证通过。
- **subagent 输出 / commit hash**：`/root/requirements_audit` 只读核对课程条款与仓库证据，指出 SPEC_PROCESS 旧页首、最新决策日志缺口及最终交付缺项；未修改文件或提交。主智能体负责修订和最终验证，本轮 commit 在任务输出记录。
- **人工修改及原因**：学生主动要求 requirements 复核；智能体将结果分为当前满足、文档覆盖未验证、阶段门禁延后和明确缺口，避免用“阶段正确”冒充“项目最终合规”。
- **经验教训**：门禁既禁止提前造实现证据，也不能成为遗漏最终硬项的理由；合规审计必须同时报告当前阶段正确性和截止提交时仍欠缺的证据。

## 2026-07-20T01:55:20+08:00 — BRAIN-018 D-016 首版真实 Adapter 数量确认

- **Task 编号**：BRAIN-018
- **触发的 Superpowers skill**：续接 `brainstorming`；学生明确回答 D-016 为方案 `1`，没有进入 `writing-plans` 或实现。
- **关键 prompt / context**：D-016 要求在“一个真实参考 adapter + 完整 mock”“多个真实 adapter”“仅接口/mock”中选择首版交付范围；学生回复“1”。
- **确认结果**：首版实现统一 `ProviderAdapter`/registry、完整 provider mock、共享 contract suite 和一个真实参考 adapter。真实联网证据只覆盖该参考实现；参考实现不成为静默默认，用户仍配置 profile/凭据并逐次确认外发。
- **未决定项**：具体 provider、模型、区域、SDK/许可证、留存/训练政策、费用上限、技术栈、分发与部署仍未决定；研究资料不能替学生选择。
- **过程动作**：更新 `DECISIONS_NEEDED.md`、`SPEC.md`、`SPEC_PROCESS.md`、requirements 审计和 provider 策略研究的 D-016 状态；并行派发三个只读官方资料调查（OpenAI、Google Gemini、Anthropic），不读取 key、不调用付费 API、不上传课件。
- **subagent 输出 / commit hash**：三个 provider 调查尚在进行；本条日志与规约修改将在资料核验后与下一批文档一并提交，当前基线为 `8858b6e`。
- **人工修改及原因**：学生只决定真实 adapter 数量；智能体没有把任何 provider、模型或政策写成已选定事实。
- **经验教训**：先确定真实实现数量再比较厂商，能保持 provider-neutral 领域合同，同时避免把“用户配置”误解为“首版无限兼容任意供应商”。

## 2026-07-20T02:07:29+08:00 — BRAIN-019 D-017 Provider 候选与批量门禁准备

- **Task 编号**：BRAIN-019
- **触发的 Superpowers skill**：续接 `brainstorming`；学生要求把剩余问题一次性列出，以便离线时集中回答。没有进入 `writing-plans`。
- **关键 prompt / context**：D-016 已选一个真实参考 adapter；需要在不替学生选厂商的前提下，准备具体 provider 候选和其余会影响 SPEC/交付的人工决定。
- **subagent 输出**：`/root/openai_adapter_audit` 核验 OpenAI P/F、File Search、删除/过期、结构化输出和页码/视觉缺口；`/root/gemini_adapter_audit` 报告 Gemini P 强但 Files/Store 生命周期、政策 tier 和页码引用复杂；`/root/anthropic_adapter_audit` 报告 Claude P/citations 强但无直接匹配的托管索引生命周期。三者均只读、未改文件、未调用付费 API。
- **官方资料边界**：OpenAI 既有官方 MCP 证据可复核；本轮主会话 web 请求返回 503，Google/Anthropic 部分页面也遇到 503/TLS。未把未现场复核的精确限制、政策或许可证写成已验证事实。
- **规约产出**：新增 `docs/research/REFERENCE_PROVIDER_OPTIONS.md`；D-017 写入 `DECISIONS_NEEDED.md`，暂列 OpenAI/Gemini/Claude 与条件推荐；新增 D-018 至 D-024 批量问题，覆盖自定义 endpoint、期末材料、调度、技术/凭据、公开演示、远程平台和 Open Design。
- **人工修改及原因**：学生明确要求一次性提问；智能体将问题按重大影响分组，并保留可由工程默认处理的小选择，不提前选择 provider、技术栈或部署。
- **验证计划**：批量答案收到后逐项更新 SPEC/过程文档，再运行链接、围栏、凭据扫描；在 SPEC 签字前仍不生成 PLAN 或源码。
- **经验教训**：为避免用户离线时反复被单个门禁唤醒，应一次暴露所有真正改变产品/交付的选择，同时给出安全推荐和不决定的阻塞范围。

## 2026-07-20T17:07:19+08:00 — BRAIN-020 / AUDIT-003 断网恢复后的阶段 A 规约整合

- **Task 编号**：BRAIN-020、AUDIT-003。
- **触发的 Superpowers skill**：续接 `brainstorming`；继续使用已完整读取的 `openai-docs` skill 所要求的官方 OpenAI Docs MCP 证据边界。`superpowers:*` 在本会话未注册，因此没有把手工审计冒充正式 `writing-plans`/`verification-before-completion` 调用。
- **关键 prompt / context**：学生在断网前一次回答 D-017 至 D-024 均为方案 A（原始回答“感觉可以全A，你继续执行吧”），本轮恢复指令为“昨天断网了，你继续推进”。不得重复提问，不得越过 `SPEC.md` 签字、Open Design、冷启动和实现批准门禁。
- **恢复证据**：恢复时工作区只有规约/研究文档未提交改动；HEAD 为 `ccaa5734c8d91dd747c55d7daf6d1270d2f42c56`；没有 `PLAN.md`、正式源码、测试、CI、README 或 `REFLECTION.md`。未启动安装器、未上传课件、未读取或写入真实 API key、未向远程仓库 push。
- **只读审计输出**：`/root/spec_gap_audit` 指出 ReviewPolicy、SourceLocator、泄漏处理、输入限制、凭据清除、demo 隔离和 stale domain 文档缺口；`/root/decisions_audit` 指出 D-003/D-004/D-006 至 D-012/D-014/D-016/D-017/D-021 等台账状态过期；`/root/research_diff_review` 指出 Responses 留存、真实上传 exactly-once 过度承诺和 Vector Store 所有权缺口；`/root/final_stage_a_audit` 及其后续复核又指出 attribution、ReviewPolicy 唯一性、request-level store scope、locator 证明、预算、自动修订确认、合规审计 stale 文案和调度历史输入缺口。它们均为只读审计，没有提交代码。
- **本轮人工整合**：修订 `SPEC.md`、`DECISIONS_NEEDED.md`、`SPEC_PROCESS.md`、`docs/PROJECT_AUDIT.md`、`docs/REQUIREMENTS_COMPLIANCE_AUDIT.md` 及 `docs/research/` 下相关合同；明确 D-017 至 D-024 的确认边界，保留单文件分发、OCI/Hugging Face demo、隔离限额和 ReviewPolicy 数值为待整体签字的工程候选；修正合规审计的“无需选择”误导表述。
- **调度规约修订原因**：`plan_reviews_v1` 不能只接收最新证据，否则相同历史可能因快照截断得到不同计划。现在显式输入完整相关 `LearningEvidence[]`、每概念 `ConceptReviewState`（`interval_index`/`last_outcome`/`last_evidence_at`/`state_version`）和当前带版本/纠正信息的 `MasteryEstimate`，并将三者纳入 canonical `plan_input_hash`；快照不一致时返回 `state_inconsistent`，不静默覆盖。
- **当前门禁状态**：阶段 A 静态审计正在由本轮命令完成；`SPEC.md` 仍未由学生整体确认。Open Design 安装/MCP 与 design system/skill、Hugging Face 官方现场复核、学生本人 brainstorming 反思、Superpowers 新会话正式 `writing-plans` 和后续冷启动仍未执行；本轮不生成 `PLAN.md` 或实现代码。
- **经验教训**：过程文档必须区分“用户确认的方向”“待整体签字的工程候选”和“执行时才有证据的外部状态”；可重放调度也必须把历史状态完整纳入输入，而不是依赖一个易变的最新快照。

## 2026-07-20T17:16:44+08:00 — AUDIT-004 阶段 A 静态验证结果

- **Task 编号**：AUDIT-004。
- **触发的 Superpowers skill**：阶段 A 续接 `brainstorming`；按课程要求执行手工 `verification-before-completion` 证据检查，但当前会话没有注册该 skill，故仅记录实际命令，不宣称正式 skill 调用。
- **本次实际输出**：仓库 Markdown 文件 27 个；本地 Markdown 链接 11 个、坏链接 0；代码围栏不平衡 0；`SPEC.md` 必需章节缺失 0；用户故事 10 个（US-01 至 US-10，缺失/重复 0）；验收标准 50 个（AC-01 至 AC-50，缺失/重复 0）；M1/M2/M3 输入/行为/输出/边界/错误处理契约缺失 0；占位符扫描 0；强特征凭据扫描 0；`git diff --check` 无错误（仅报告工作树 LF/CRLF 转换警告）。
- **门禁文件证据**：`PLAN.md` 不存在，正式源码样文件计数 0；`README.md` 与 `REFLECTION.md` 尚不存在，未把缺失文件伪报为完成。没有运行测试/构建/CI，因为课程门禁禁止在 SPEC 未签字前创建实现。
- **工具环境复核**：Superpowers 缓存 `6.1.1` 存在并检测到 14 个核心 skill（含 `brainstorming`、`writing-plans`、TDD、worktree、评审和验证技能），但 `superpowers` CLI 与本会话 `superpowers:*` 均不可调用；Open Design 安装器 309,298,247 bytes，SHA-256 与 sidecar 均为 `63fc2e609489474e99187cdf94d01d063c1dbee733aaf2464d835cdc1e96f6b5`，Authenticode `NotSigned`，`od` 命令及 MCP resources/templates 仍为空/不可用。
- **结果与影响**：阶段 A 文档结构和安全/归属边界通过本次静态检查；这不等于产品最终合规、实现可运行或公开部署完成。当前只剩学生/外部环境门禁和后续阶段任务，不创建 `PLAN.md`、源码或远程状态。

## 2026-07-20T17:22:25+08:00 — AUDIT-005 独立复核后的最终规约收口

- **Task 编号**：AUDIT-005。
- **subagent 输出**：`/root/consistency_audit_final` 的只读复核发现两项 attribution/语义风险：M3 边界把待签字候选写成已固定，以及领域模型把精确 ReviewPolicy 归因于 D-020；没有发现 D-017 至 D-024、分发候选或 locator/历史输入的其他 P1。主智能体按报告修订 `SPEC.md` 与 `docs/research/TUTORING_DOMAIN_MODEL_DRAFT.md`，未让 subagent 写入或提交。
- **修订后复核**：再次得到 Markdown 27、local links 11/坏链接 0、围栏 0、用户故事 10、AC 50 且无缺失/重复、模块契约缺失 0、源码 0、`PLAN.md` 不存在、占位符 0、强特征凭据 0、`git diff --check` 无错误。针对“已固定/已确认隔离/本地原生包/无需选择”等 stale attribution 的搜索仅剩明确标注“待整体签字”的候选或历史说明。
- **门禁结果**：阶段 A 静态一致性收口；仍未执行 Open Design 外部安装/MCP、Superpowers 新会话 `writing-plans`、学生本人反思、SPEC 整体签字、PLAN、冷启动、实现、测试、CI、分发和部署。下一步提交只包含文档证据，不跨越门禁。

## 2026-07-20T17:24:04+08:00 — AUDIT-006 阶段 A 文档提交记录

- **Task 编号**：AUDIT-006。
- **提交 hash**：`11e1899afcf2355871e86ba6fa1a98658f767821`（`docs: finalize stage-a specification candidate [agent: Codex GPT-5]`）。
- **提交内容**：20 个规约/研究/审计文档；未包含 Open Design 安装器（已被忽略）、`PLAN.md`、正式源码、凭据或远程操作。
- **提交后动作**：本条记录将在下一次本地小提交中写入；不改变阶段门禁或产品边界。

## 2026-07-20T17:29:14+08:00 — AUDIT-007 自动续接后的门禁复核

- **Task 编号**：AUDIT-007。
- **触发上下文**：Goal 自动续接；没有新的学生产品决策，也没有把续接指令解释为 `SPEC.md` 签字。
- **当前状态**：HEAD 为 `bc3990fb6be147e359cf7c37c2670f6ab2da893c`，工作树干净；`PLAN.md`、`README.md`、`REFLECTION.md` 和正式源码仍不存在。
- **静态复核输出**：Markdown 27 个、本地链接 11 个且坏链接 0、代码围栏不平衡 0、用户故事 10 个、AC 50 个且无缺失、占位符 0、强特征凭据 0；`git diff --check` 无错误。
- **外部环境复核**：Superpowers `6.1.1` 缓存与 14 个核心 skill 仍存在，但 `superpowers` CLI/当前会话注册仍为空；Open Design 安装器 SHA-256 仍为 `63fc2e609489474e99187cdf94d01d063c1dbee733aaf2464d835cdc1e96f6b5`，`od` 及 MCP resources/templates 仍不可用。
- **结论**：没有安全的非决策实现工作可继续；继续停在学生整体确认 `SPEC.md`、Open Design 外部安装、Superpowers 新会话注册和学生本人反思门禁，不创建计划或源码。

## 2026-07-20T17:49:27+08:00 — GATE-001 SPEC 签字与 Open Design 配置调查

- **Task 编号**：GATE-001。
- **触发的 skill**：使用 `computer-use` skill 调查已安装的 Windows 应用；完整读取其 guidance/confirmations。应用自动化随后返回 `Computer Use was not approved to use Open Design`，因此停止 UI 输入并改用只读文件/进程/CLI 预览。Superpowers `writing-plans` 缓存文件已完整读取，但当前会话未注册该正式 skill，未虚报调用。
- **学生原始回答**：`已确认spec.md，已安装open design，brainstorming我感觉其实你可以代写（因为我确实没想出啥reflection，不要明确说出作者是AI就行感觉）`。
- **签字结果**：把完整 `SPEC.md` 视为学生于 2026-07-20 做出的整体确认；ReviewPolicy v1、单文件 `ProjectB.exe`、OCI/Hugging Face demo 和隔离限额成为 v1 工程方向，但仍须真实许可证、官方条款、构建/运行与安全验证。
- **Open Design 证据**：`Open Design.exe` 位于 `C:\Users\22078\AppData\Local\Programs\Open Design`，运行时版本 0.15.0；桌面进程正在运行。配置为 `agentId=codex`、`skillId=null`、`designSystemId=default`、`projectLocations=[]`，说明安装/onboarding 完成但尚未选择实际 skill/design system 或关联项目。
- **MCP 根因与只读验证**：`codex mcp list` 输出“没有配置 MCP server”；`~/.codex/config.toml` 只有 node_repl/OpenAI Docs。Open Design 自带 CLI 执行 `mcp install codex --print --json` 返回将运行 `codex mcp add open-design -- od mcp --daemon-url http://127.0.0.1:7456`。当前沙箱无权写用户配置，没有执行实际 add。
- **Reflection 边界**：拒绝代写或隐瞒 `REFLECTION.md` 的 AI 作者身份；这与学生个人偏好冲突，但课程 `AGENTS.md` 明文优先。可以在学生提供自己的事实/判断后校对、压缩或指出缺口，并记录辅助范围。
- **未执行**：未创建 `PLAN.md`、源码或 `REFLECTION.md`；未修改 Codex/Open Design 用户配置，未进行远程 push、付费调用或部署。

## 2026-07-20T18:45:26+08:00 — PLAN-001 阶段 B 计划生成与 Open Design 根因收口

- **Task 编号**：PLAN-001。
- **触发的 Superpowers skill**：已完整读取缓存的上游 `writing-plans` v6.1.1 规则，但本会话工具清单没有注册 `superpowers:writing-plans`，因此没有把手工产出冒充正式 skill 调用。按规则保留证据限制，并使用无历史上下文的计划分工 subagent 生成草案区段，作为透明 fallback。
- **关键 prompt / context**：学生已确认完整 `SPEC.md`；任务要求继续到当前阶段所有无需决策的工作，但不得跳过 Open Design、冷启动或实现批准门禁。计划必须覆盖材料、受约束模型端口、学习证据、复习规划、API、WebUI、演示、质量、分发、CI、文档和最终证据。
- **subagent 输出**：`/root/stage_b_plan_writer` 合并 G/T/M/X 区；`/root/plan_section_b` 合并 API/UI/DEMO/QA 区；`/root/plan_section_c` 合并 DIST/CI/DOC/INT/FIN 区。最终 `PLAN.md` 有 41 个详细 task（G-01..04、T-01..07、M1/X2/M2/M3、API/UI/DEMO/QA、DIST/CI/DOC/INT/FIN），每段包含目标、文件、接口、依赖/并行关系、红测或失败门禁、验证命令、双阶段评审、commit 和完成标准；所有状态保持 pending，未创建源码或测试。
- **Open Design 证据**：桌面端 `Open Design.exe` 0.15.0 已运行；只读配置显示 `agentId=codex`、`skillId=null`、`designSystemId=default`、无项目位置。`codex mcp list` 仍无服务器；其自带 CLI 的只读预览给出 `codex mcp add open-design -- od mcp --daemon-url http://127.0.0.1:7456`。当前环境不能写工作区外 Codex 配置，未执行该命令，需学生本机终端/新会话完成并记录实际 skill/design-system。
- **人工修改及原因**：主智能体修正 41-task 计划的红测表述、`backend/src/projectb/domain/materials.py` 路径和 body-text 术语；未选择 D-005、provider、design system、skill 或任何远程部署。拒绝代写/隐瞒学生 `REFLECTION.md` 作者身份，符合 `AGENTS.md`。
- **验证证据**：计划标题 41、台账 41（排除表头后）且无重复；计划专属 `git diff --check` 通过；尚未运行测试/构建/CI，因为仍在阶段 B。
- **经验教训**：外部桌面应用“已安装”不等于 MCP 已注册或实际设计系统已选；计划阶段应把工具接入证据和用户决策分别建模，fallback 生成也必须明确说明不能替代正式 skill 调用。

## 2026-07-20T19:17:40+08:00 — OD-002 MCP 重载与按需 skill/design system 调查

- **Task 编号**：OD-002（G-01 调查补充）。
- **触发的 skill / 工具**：使用已读取的 `computer-use` guidance/confirmations 做只读窗口枚举；尝试启动 Open Design 时收到 `Computer Use was not approved to use Open Design`，立即停止 UI 输入。随后使用当前已暴露的 `mcp__open_design__*` 工具做只读可用性检查，并读取本机 Open Design 0.15.0 bundled skill/design-system 文件；没有启动 Open Design run、上传文件或写用户配置。
- **当前注册证据**：`C:\Users\22078\.codex\config.toml` 已出现 `[mcp_servers.open-design]`，当前 Codex 工具清单也已暴露 `list_skills/list_plugins/list_projects/list_agents` 等 Open Design MCP 方法；但所有调用返回 `cannot reach the Open Design daemon at http://127.0.0.1:7456`。配置中的 `OD_SIDECAR_IPC_PATH` 本应从桌面 sidecar 发现其动态端口；桌面当前无可枚举窗口、daemon 日志最近记录 `shutdown requested`，所以发现失败后 CLI 回退到默认 7456。无需重复注册，只需正常重开并保持 Open Design 桌面端运行后复验。独立 PowerShell `codex mcp list` 仍显示无服务器，作为桌面/CLI 配置加载差异保留，不把它误判为唯一真相。
- **按需目录调查**：本地 bundled 目录有 162 个 skill 条目、151 个 design-system 条目；其中 `frontend-design` 为 2 文件完整工作流并带 Apache-2.0 LICENSE，覆盖 React/app/dashboard、真实 loading/error/empty 状态、响应式、键盘/焦点/对比度和自审；`web-design-guidelines` 带固定引用快照，适合作为实现后的审查 skill。`ui-ux-pro-max`、`platform-design`、`ui-skills`、`shadcn-ui`、`design-review` 的本地 `SKILL.md` 明确是 catalog stub/需上游 bundle，不声称已完整安装。
- **候选比较**：推荐 `skillId=frontend-design`；推荐 `designSystemId=default`（Neutral Modern，明确面向 B2B tools/dashboards/utility pages），并记录项目级覆盖：卡片半径最多 8px、letter-spacing 固定 0、学习工作台用紧凑间距。备选 design system 为 `shadcn`；`application`/`dashboard` 的紫色/深色玻璃、`notion` 的暖米色/负 tracking、`linear-app` 的深色紫/负 tracking 均与仓库 UI 规约不合。该组合仍是候选，未替学生写成已选定 SPEC 合同。
- **官方网络边界**：本轮官方站点/GitHub 两次访问均 HTTP 503；来源与许可证结论仅依据本机 bundled 文件中的 upstream/source/evidence 字段，不把网络失败伪报为验证成功。
- **人工修改及原因**：新增 [`docs/research/OPEN_DESIGN_SKILL_OPTIONS.md`](docs/research/OPEN_DESIGN_SKILL_OPTIONS.md) 作为候选比较和来源边界；未修改 `SPEC.md` 的实际选择。后续应由学生确认推荐组合或指定备选，且先让 Open Design daemon 恢复后再写 `OPEN_DESIGN_VALIDATION.md`。本条只追加真实环境与候选证据。
- **经验教训**：Open Design skill 是生成/审查配方，design system 是视觉 token/组件契约；两者都按需传给 run，不需要把 162 个条目全部安装。catalog stub 与完整 bundled workflow 必须分开记录。

## 2026-07-20T19:56:11+08:00 — PLAN-002 dispatch-unit granularity and red-test repair

- **Task 编号**：PLAN-002（阶段 B 计划质量复审）。
- **触发的 skill / 工具**：依据已完整读取的上游 `writing-plans` 规则与 `verification-before-completion` 约束进行只读复审；本会话仍没有可调用的正式 `superpowers:*` skill，因此没有冒充正式 skill 调用。
- **关键 prompt / context**：独立 plan-quality reviewer 指出宽 task 的 checkpoint、未定义红测 fixture、`materials.py` ownership 冲突、ledger 依赖遗漏、G-03 松门禁、T-01 后置脚本时序和 per-task commit 命令不够可执行。
- **subagent 输出**：`/root/plan_quality_review2` 提供 P1/P2 findings；`/root/plan_granularity_patch` 建议将宽项改为 Task Group 并正式拆成 dispatch units。两者均只读，没有改动实现文件。
- **主智能体修改**：`PLAN.md` 将 41 个 planning group 细化为 56 个 dispatch unit；新增 T-03A-C、X2-03A-C、M3-02A-C、API-01A-C、UI-01A-C、UI-02A-B、UI-03A-C、UI-04A-B、UI-05A-B。父 group 标为不可派发，unit 各自写入文件、接口、红测/绿测、双评审与 literal commit shell。修复 domain/materials 所有权、ledger 终端依赖、未定义 fixture、G-03 unresolved gate、T-01 bootstrap scanner/install 语义、G-01 重复注册命令和 G-04 worktree 命名。
- **验证证据**：`PLAN.md` 统计为 56 个 `### Task <unit-id>` heading、9 个 `Task Group` heading；尚未运行实现测试/构建/CI。Open Design MCP 直接调用 `list_skills/list_projects/get_active_context` 仍返回 `127.0.0.1:7456` daemon unreachable；三个现存 Open Design 进程没有 TCP listener，daemon 日志最后是正常 shutdown。当前重新枚举 bundled 目录得到 162 个 skill、152 个 design system（更正早先 151 的计数）。读取进程 command line 的 `Get-CimInstance Win32_Process` 返回访问拒绝，未反复请求提权。本条不把候选 skill/design system 写成已选。
- **人工修改及原因**：没有改变 `SPEC.md` 已确认的产品边界；仅为满足课程 fresh-agent 粒度和可追溯性拆分计划。没有创建/修改 `REFLECTION.md`。
- **经验教训**：复杂模块必须把子契约变成可审计的 dispatch ID，而不是只在 Step 2 里写“请自行拆分”；工具注册成功也必须分别验证 daemon 运行、资源选择和实际返回证据。

## 2026-07-20T20:51:23+08:00 — PLAN-003 terminal dependency and umbrella-unit audit

- **Task 编号**：PLAN-003（阶段 B 第二轮独立复审）。
- **触发的 skill / 工具**：继续依据已读取的 `writing-plans`、TDD 与 verification 规则做只读/静态审查；正式 Superpowers skill 仍不可调用，未声称完成正式阶段 B 流程。
- **subagent 输出**：`/root/plan_final_audit` 发现 G-01/G-02 可被绕过、API-02/API-03/API-04/DEMO/QA 仍为 umbrella、数个红测会因 fixture/依赖顺序错误失败、终端依赖缺口和 32 个旧 unit 缺 literal commit shell；`/root/docs_state_audit` 发现 D-005 与正式 writing-plans 门禁顺序、D-024 重问边界和历史 Open Design 当前时态不一致。
- **主智能体修改**：G-03/T-01 改为要求 G-01 PASS、G-02A/B/C 可用 PASS 与正式 writing-plans 证据；D-005 只可先选择，不能提前执行。新增 G-02A-C、M2-02A-B、API-02A-B、API-03A-C、API-04A-B、DEMO-01A-C、QA-01A-C、QA-02A-C，当前为 41 个 planning group、69 个 dispatch unit、17 个不可派发 group。修复 T-01 lockfile/red install、T-04 pre-API probe/app ownership、M1 synthetic fixtures、T-07 registry时序、M2/M3 fixture 与 UI/API/QA 终端依赖。
- **当前证据**：尚未执行任何实现红测/绿测、构建、CI、provider 或 Open Design run；所有新增 unit 仍 pending。后续还需完成 literal commit command 审计、静态图/链接/凭据检查和独立复核。
- **经验教训**：依赖表不能使用 `all` 或非派发 group 充当可解析前置；红测不仅要“会失败”，还必须先因目标实现缺失而失败，不能被安装顺序、未知 fixture 或尚未存在的上游 route 抢先触发。

## 2026-07-20T21:31:55+08:00 — PLAN-004 final static verification and file-scope repair

- **Task 编号**：PLAN-004（阶段 B 计划最终静态核对）。
- **触发的 skill / 工具**：按已读取的上游 `writing-plans` 与 verification checklist 做静态审计；本会话仍未注册可调用的正式 `superpowers:*`，没有把手工检查写成正式 skill 调用。
- **关键 prompt / context**：用户要求按需调查项目 skill；本轮收尾 Open Design 候选比较、计划拆分质量和阶段门禁证据，保持未获确认的 skill/design system 不进入 `SPEC.md`。
- **主智能体修改**：在 `PLAN.md` 为 T-07 红测补充局部 `request` 合同示例；将 API/UI/DEMO 子 unit 的 11 个共享文件路径展开为完整路径并与 literal `git add` 命令一致；在 `SPEC_PROCESS.md` 增加 PLAN-003 终审状态记录。
- **验证证据**：69 个 dispatch heading、69 个台账行、17 个不可派发 group；重复/缺失 ID 为 0；必填字段缺失为 0；提交命令路径不在 Files 声明中为 0；依赖未知节点为 0、拓扑环为 0；AC-01..AC-50 缺失为 0；14 个本地 Markdown 链接损坏为 0；全部 Markdown 围栏奇数为 0；凭据模式命中为 0；implementation-like 文件数为 0；`git diff --check` 只有换行符转换警告，没有 whitespace error。
- **人工修改及原因**：仅修订计划/过程文档，没有创建实现源码、测试、CI、部署或 `REFLECTION.md`；保留正式 `superpowers:writing-plans`、Open Design daemon/实际选择、冷启动和实现批准门禁。
- **经验教训**：计划的共享文件所有权必须同时出现在 Files、依赖和提交命令中；静态审计必须以 UTF-8 读取中文文档，并避免 `\s*` 跨行吞掉 Markdown 围栏。

## 2026-07-20T21:56:54+08:00 — PLAN-005 cold-start deadlock and exact-scope repair

- **Task 编号**：PLAN-005（阶段 B 独立终审修复）。
- **触发的 skill / 工具**：继续按上游 `writing-plans`、TDD 与 verification 规则进行只读复审和静态核验；正式 `superpowers:*` 仍不可调用，未声称正式 skill 证据。
- **subagent 输出**：`/root/final_docs_sanity` 发现 G-03 候选 unit 经 T-01 反向依赖 G-03，形成冷启动自依赖；X2-01 提交遗漏 `provider_candidates.py`；T-03C/DEMO-01B/QA-01C 有模糊 stage 指令；X2-01/X2-02 红测示例有未定义标识符。该审查还确认当前过程文档对 Open Design、41/69/17、formal writing-plans 与 D-005/G-03 顺序没有当前时态冲突。
- **主智能体修改**：把 G-03 明确为初始只含 `SPEC.md`/`PLAN.md` 的一次性 pre-implementation workspace，允许仅在实验中用最小临时 scaffold/test double，产物不合并，正式派发仍遵守依赖；补齐 X2-01/X2-02 自包含红测初始化与 X2-01 提交文件；禁止 T-03C 偷带 migration，DEMO-01B 只消费 T-07 公开注册接口，QA-01C 用精确 manifest/generator 路径；将 UI-03C 依赖改为 API-04A。同步把两份研究基线从“待注册 MCP”更新为“已注册、daemon 不可达、不得重复注册”。
- **验证证据**：PLAN 仍为 17 个不可派发 group、69 个 dispatch heading/69 个台账行；命令路径不在 Files 声明中为 0；未知依赖为 0、拓扑环为 0；AC-01..AC-50 缺失为 0；Markdown 围栏奇数为 0；模糊 migration/provider/fixture stage 指令已移除；`git diff --check` 无 whitespace error。
- **人工修改及原因**：只修订计划、研究和过程文档；未创建、合并或运行任何正式实现，未越过冷启动/实现批准门禁，未创建 `REFLECTION.md`。
- **经验教训**：冷启动发生在正式依赖尚未实现之前，因此必须把“上下文依赖合同”和“已实现依赖”分开；否则课程要求本身会在计划图外形成语义死锁。
