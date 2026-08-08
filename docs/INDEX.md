# 文档入口

这是项目文档的单一导航页。先按下面的顺序阅读，不需要遍历整个 `docs/`。

## 当前必读

1. `../SPEC.md`：当前产品规约与范围边界。
2. `../PLAN.md`：课程阶段门禁、任务状态和下一步顺序。
3. `REQUIREMENTS_COMPLIANCE_AUDIT.md`：课程硬要求追踪矩阵。
4. `../DECISIONS_NEEDED.md`：仍需学生确认的门禁和外部授权。

## 文档分区

| 目录 | 内容 | 是否可作为当前实现依据 |
| --- | --- | --- |
| `archive/completed-process-2026-08-07/` | Completed setup, audit, G-03 planning, and handoff records with byte hashes | Historical only; not dispatch authority |
| `requirements/` | 课程原文与要求摘录 | 是，课程原文优先 |
| `cold-start/` | G-03 冷启动运行手册与证据说明 | 是，执行 G-03 时使用 |
| `engineering/` | 过程审计、交接、质量与安全记录 | 仅按当前任务选择性阅读 |
| `research/` | 方案调查、威胁模型和技术选型依据 | 仅按当前任务选择性阅读 |
| `mockups/` | UI 草图和设计参考 | UI 任务需要时阅读 |
| `plans/` | 当前或近期的详细 Superpowers 计划记录 | 只读；是否可派发以根 `PLAN.md` 为准 |
| `specs/` | 详细设计记录 | 只读；权威规约以根 `SPEC.md` 为准 |
| `archive/` | 被取代计划、延期功能和失败证据 | 不可直接派发，恢复必须重新走门禁 |

## 归档说明

`archive/` 保留历史文件的原始字节、哈希和评审结论。它们从旧的
`docs/superpowers/plans/archive/` 横向迁移而来，内容没有删除或改写；旧路径只在
归档表和历史证据中出现，不代表当前目录仍应创建该路径。

延期功能位于 `archive/deferred-v2/`，统一标记为 `ARCHIVED / NOT DISPATCHABLE`。
被取代的旧计划位于 `archive/superseded-2026-07-23/`，统一标记为 `NOT PASS`。

## 目录约束

- 根目录只放课程要求的入口文档、项目元数据和必要配置。
- 持久化文档只放在本页列出的一级分区；不要新增按日期或智能体继续嵌套的目录。
- 临时运行输出放在根 `tmp/<用途>/<会话 ID>/`，不放入 `docs/` 或 worktree 的 `tmp/` 下的完整仓库。
- `.worktrees/` 只保存需要保留的活动或诊断 checkout；删除前必须检查其 Git 状态。
