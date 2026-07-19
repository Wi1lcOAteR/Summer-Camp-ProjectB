# SPEC_PROCESS

> 当前状态：阶段 A 的需求澄清已开始，尚未形成 `SPEC.md`。Superpowers v6.1.1 已安装且此前会话已记录触发 `brainstorming`；本次会话未将 `superpowers:*` 注册到可调用 skill 清单，因此仅按已安装的上游指令续接流程，并如实保留这一证据限制。

## 0. 启动审计（2026-07-17）

### 已读取的约束来源

1. `AGENTS.md`
2. `SKILLS_SETUP.md`
3. `docs/requirements/项目要求.md`
4. `docs/requirements/AI4SE_Final_Project_B_应用类项目.md`

### 当前阶段判定

- 项目想法仍是模板占位文本，没有可确认的问题陈述、目标用户或功能边界。
- 课程要求第一步必须由 Superpowers `brainstorming` 介入。
- Superpowers v6.1.1 已安装，PRE-006 已记录此前会话触发 `brainstorming`；本次会话按同版本上游指令续接，但可调用 skill 清单未注册 `superpowers:*`。
- 当前已进入阶段 A 的逐项需求澄清；在设计获得用户确认前不创建正式 `SPEC.md`，在用户明确确认 `SPEC.md` 前不进入计划或实现。

### 已完成的非决策工作

- 完整读取课程与仓库约束。
- 盘点仓库、工具链、Git、Superpowers 与 Open Design 状态。
- 从官方上游核验安装路径、版本和许可证。
- 建立差距审计、决策清单与过程日志。

## 1. Brainstorming 迭代记录

### 2026-07-19 启动上下文与首问准备

- 完整复核课程原文、根目录约束、已有过程文档、Git 历史与本地工具状态。
- 完整读取已安装 Superpowers v6.1.1 的 `using-superpowers` 与 `brainstorming` 指令，并按清单建立阶段任务。
- 本次会话暴露的 skill 清单没有 `superpowers:*`，因此不能把读取磁盘文件表述为本次会话的正式 skill 调用；此前 `AGENT_LOG.md` PRE-006 已记录实际触发证据。
- 项目目标仍是占位文本。按“一次只问一个问题”的规则，首轮只确认学生最近反复遇到且愿意实际使用软件解决的真实问题；在收到回答前不创建 `SPEC.md`。

课程要求至少 3 轮关键迭代；后续必须逐轮记录真实提问、学生答复、采纳/推翻的建议与原因。

## 2. SPEC 签字确认

尚未执行。`SPEC.md` 尚不存在，用户尚未确认。

## 3. PLAN 生成

尚未执行。必须等待用户明确确认 `SPEC.md` 后调用 `writing-plans`。

## 4. 陌生智能体冷启动验证

尚未执行。必须等待 `SPEC.md` 与 `PLAN.md` 完成后，使用不同类型、全新 session、仅接收这两个文件的智能体尝试 1–2 个 task。
