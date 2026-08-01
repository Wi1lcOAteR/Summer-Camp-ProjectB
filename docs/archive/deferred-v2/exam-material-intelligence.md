# Exam Material Intelligence v2 Archive
Status: ARCHIVED / NOT DISPATCHABLE

本文件保存能力恢复边界，不是实现计划，也不授权自动考试材料分析。

## 目标

把无答案往年卷和老师重点转换为带有效 locator、材料类型、难度和置信度的候选知识映射；只有学生确认后才允许影响期末复习优先级。

## 延期原因

精简 v1 先验证人工 concept/coverage。自动分析需要新增材料角色、候选端口、置信/冲突处理、答案泄露防护和 plan revision 联动，也需要合法可再分发的验收语料。

## v1 边界

用户手工创建或编辑 `KnowledgeConcept`，并从有效 locator 中确认 `CoverageDecision`。系统不自动分析往年卷、老师重点或整门课程；当前三个 provider 端口不包含 `analyze_exam_material`，finals 计划只消费已确认 concept、evidence 和考试日期。

## 重新启用前置依赖

- M1 角色/locator/coverage 历史、M2 candidate-only 边界和 M3 finals revision 接口已稳定并验证。
- 学生确认允许的材料角色、是否永久排除含答案材料，以及疑似答案的人工复核状态机。
- 准备许可 fixture，定义候选 schema、置信语义、冲突/拒绝/纠正历史和 provider consent 范围。
- 明确该能力只做结构/题型/知识点/难度分析，不训练、微调或预测原题。

## 预计接口/文件

候选接口为 `analyze_exam_material`、`propose_study_focus`、`confirm_study_focus` 和 `active_study_focus`。候选路径为 `backend/src/projectb/application/study_focus.py`、`backend/src/projectb/domain/review.py`、`backend/tests/contract/test_exam_material_analysis.py`、`backend/tests/integration/test_study_focus_confirmation.py` 及对应材料复核 UI。重新规划时必须重新确认命名、边界和 owner。

## 首个失败测试

`test_unconfirmed_exam_candidate_does_not_change_priority_or_plan`：即使 deterministic adapter 返回结构正确的候选，未确认或 locator 失效时，coverage、priority 和 plan revision 必须保持不变，provider failure 也不得伪装为学习失败。恢复时首次运行应因 exam candidate service 不存在而失败。

## 验证命令

```powershell
& $env:PROJECTB_PYTHON_EXE -m pytest backend/tests/contract/test_exam_material_analysis.py backend/tests/integration/test_study_focus_confirmation.py -q
& $env:PROJECTB_PYTHON_EXE scripts/test_all.py
```

## 验收标准

- 每个候选都绑定有效 locator、来源类型和可解释置信信息；老师明确重点与往年卷模式分开。
- 拒绝、纠正和确认可追溯；低置信、来源不足、provider failure 或疑似答案均零权威写入。
- 只有已确认候选能生成可比较的 finals revision，且不改写历史 attempt/evidence。
- 无训练、微调、原题预测、静默上传或模型直接决定 priority 的路径。

## 重新启用时人工决定

学生必须决定是否接收无答案往年卷和老师重点、支持的分析维度、置信阈值与重复次数上限、只影响 finals 还是也影响 continuous，以及含答案材料的永久排除或复核政策。

恢复顺序固定为：重新执行 `brainstorming` -> 写出明确 SPEC diff -> 学生确认完整 SPEC -> 调用 `writing-plans`。旧 M3-03 仅是历史候选，不得直接派发。
