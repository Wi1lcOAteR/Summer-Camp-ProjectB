# Extended Concept Rubrics v2 Archive
Status: ARCHIVED / NOT DISPATCHABLE

本文件保存能力恢复边界，不是实现计划，也不批准任何新 evaluator。

## 目标

在三个 v1 evaluator 之外增加学生选定知识点的版本化确定性 evaluator/rubric 库，并复用统一的 evidence、mastery 和 source 合同。

## 延期原因

v1 已用互斥、竞态和死锁形成可验收纵向切片。每个新增概念都需要独立正确性权威、结构化答案 schema、边界/反例 fixture、教学范围确认和历史 evidence 兼容策略。

## v1 边界

仅注册 `os.mutex.v1`、`os.race.v1` 和 `os.deadlock.v1`。没有受支持 evaluator 的 `KnowledgeConcept` 必须保持 `explanation_only`，可以绑定来源和获得解释，但不得产生评分或掌握结论；模型措辞不能改变确定性结果。

## 重新启用前置依赖

- v1 `KnowledgeConcept.evaluator_id`、不可变 `LearningEvidence`、mastery 时间规则和 evaluator/provider 隔离已验证。
- 学生选择首个扩展知识点，并提供可审查的正确性来源、rubric 和许可 fixture。
- 定义 evaluator ID/version、输入 schema、criterion/result schema、迁移与旧 evidence replay 规则。
- 每个 evaluator 独立拆成小 task，并准备边界、near-miss、adversarial 和属性测试。

## 预计接口/文件

候选接口为版本化 `EvaluatorRegistry.evaluate`、`RubricCriterion` 和 `EvaluatorResult`。候选路径为 `backend/src/projectb/domain/learning.py`、`backend/src/projectb/application/evaluator_registry.py`、`backend/src/projectb/application/selected_evaluator.py`、`backend/tests/unit/test_extended_evaluators.py` 和许可 golden fixtures；具体领域文件名必须在学生选择知识点后由新计划固定。

## 首个失败测试

`test_selected_evaluator_replays_golden_boundary_and_adversarial_fixtures_without_provider_influence`：同一规范化输入重复运行得到完全相同、按 criterion ID 排序的结果；provider 输出变化不得改变评分。恢复时首次运行应因选定 evaluator 尚未注册而失败。

## 验证命令

```powershell
& $env:PROJECTB_PYTHON_EXE -m pytest backend/tests/unit/test_extended_evaluators.py -q
& $env:PROJECTB_PYTHON_EXE -m pytest backend/tests -q
& $env:PROJECTB_PYTHON_EXE scripts/test_all.py
```

## 验收标准

- 相同结构化输入和 evaluator version 的结果恒定，未知字段/版本失败关闭。
- 必需 criterion 失败不能被权重掩盖；criterion 结果和 evaluator/version 进入幂等 evidence。
- 模型只能解释结果，不能评分；未注册 evaluator 始终保持 `explanation_only`。
- 每个新增 evaluator 有权威来源、fixture 许可证、边界/反例覆盖和历史 replay 证据。

## 重新启用时人工决定

学生必须决定首批知识点、每项正确性来源和 rubric、题型/变体数量、fixture 许可证，以及是否改变 mastery 门槛；历史候选主题不等于已选择。

恢复顺序固定为：重新执行 `brainstorming` -> 写出明确 SPEC diff -> 学生确认完整 SPEC -> 调用 `writing-plans`。随后仍须完成冷启动验证和学生实现批准，不得从本归档直接实现。
