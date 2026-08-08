# ProjectB 会话交接

**更新时间：** 2026-07-25T12:29:39+08:00
**用途：** 仅提供最小恢复索引；产品约束以 `SPEC.md` 为准，执行门禁以 `PLAN.md` 和课程要求矩阵为准。

## 当前状态

- 分支：`codex/stage-b-scope-reset`；范围重置前基线：`519b3000336d18f8b89628fdc14691d3b700002c`；归档 checkpoint：`ccd1dfe`；活跃文档 checkpoint：`5f54431`。
- 阶段：Stage B `ACTIVE REMEDIATION / NOT PASS`。
- 当前 `SPEC.md` 是精简 v1 待学生重新确认稿；旧签字不适用于重写后的文本。
- 当前 `PLAN.md` 只是范围重置门禁台账，不是可派发实现计划。
- 正式源码、冷启动、实现 worktree、测试/构建、CI、分发验证和部署均未开始。

## 最小阅读集

1. `SPEC.md`：精简 v1 的完整候选规约。
2. `PLAN.md`：当前阶段门禁和下一步顺序。
3. `docs/REQUIREMENTS_COMPLIANCE_AUDIT.md`：课程硬要求唯一追踪矩阵。
4. `DECISIONS_NEEDED.md`：当前人工门禁；顶部事项优先。
5. `docs/archive/README.md`：旧计划和延期功能的恢复索引。

只有在恢复历史问题或延期功能时，才按归档索引选择性读取旧草稿；不要默认加载全部历史计划。

## 本次范围重置

- 活跃 v1 保留 M1 数字材料导入与定位、M2 通用概念模型及互斥/竞态/死锁确定性检查、M3 学习证据和复习规划。
- 模型范围缩为本地 `L` 与逐次确认片段外发 `P`；保留 OpenAI adapter、Credential Manager 和 deterministic mock。
- OCR/图片/扫描件、远端整文件 F 与持久任务、考试材料智能、扩展 rubric 进入 `ARCHIVED / NOT DISPATCHABLE` 延期计划。
- WebUI、Open Design、Windows 单文件、OCI demo、GitLab `unit-test`、GitHub CI、公网 HTTPS URL、README 和学生本人 `REFLECTION.md` 仍是当前课程要求，没有被归档。

## 存档边界

- 被取代的根计划、六份详细计划、三个片段和两份工程合同保存在 `docs/archive/superseded-2026-07-23/`。
- 四份可恢复延期计划保存在 `docs/archive/deferred-v2/`。
- `.r5-verify-final-20260723` 只保存在被忽略的 `tmp/stage-b-archive-20260725/`，是计划代码重建物，不是产品源码。
- 旧 local-trust 计划中的两个模拟凭据字面量已在可提交副本中安全替换；原始字节只保存在被忽略的本地存档，归档索引同时记录原始和可提交哈希。

## 下一门禁

学生必须先通读并明确确认当前完整 `SPEC.md`。确认后才可调用 `writing-plans`，把门禁台账替换为最多约 30 个单会话 task 的唯一实现计划。随后还必须完成同一 SPEC/PLAN 哈希的双评审、Claude Code 陌生会话冷启动、修订和学生实现批准，才可创建实现 worktree 或编写生产代码。

## 禁止误读

- 归档计划中的旧 PASS/NOT PASS 只描述历史快照，不能授权当前实现。
- 标准证据脚本通过不等于 Stage B PASS；严格分发校验在 D-025 未解决时必须失败。
- 不得 reset、clean、checkout 或覆盖工作树中与本次范围重置无关的既有修改。
- 不得代写 `REFLECTION.md`，不得未经授权 push、建 PR、运行远程 CI、发布镜像或部署。
