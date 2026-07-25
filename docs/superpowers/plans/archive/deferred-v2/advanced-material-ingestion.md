# Advanced Material Ingestion v2 Archive
Status: ARCHIVED / NOT DISPATCHABLE

本文件保存能力恢复边界，不是实现计划，也不授权生产代码。

## 目标

在 v1 M1 之上增加独立图片、扫描 PDF/OCR、页内区域 locator 和可恢复的大批量导入，同时保留原始字节 hash、版本和来源可追溯性。

## 延期原因

OCR/视觉质量、第三方引擎许可证、Windows 分发体积、资源上限、批处理恢复和人工纠错会显著扩大精简纵向切片；当前没有这些选择的学生确认或同快照计划评审。

## v1 边界

v1 只接收可提取文本的数字 PDF、UTF-8 `.txt` 和 `.md`；每次最多 5 个文件、单文件 20 MiB、批次 50 MiB、PDF 200 页。整份 PDF 无可提取文本时返回 `unsupported_scanned_pdf`；OCR、独立图片和扫描件均不进入权威写入。

## 重新启用前置依赖

- v1 `Material`、raw hash、PDF page/text-lines locator、事务回滚和删除失效合同已经实现并验证。
- 选定 OCR 引擎、模型/语言包、许可证、离线策略、图片格式/像素上限及 Windows/OCI 打包方式。
- 准备可再分发的合成扫描/图片夹具和经授权的私有 benchmark；明确 timeout、内存、并发与清理边界。
- 若采用异步导入，先人工决定是否复用 remote/durable-job v2 基础层。

## 预计接口/文件

候选接口为 `OcrAdapter.extract_pages`、`SourceLocator.image` 和 `import_material_batch`。候选路径为 `backend/src/projectb/infrastructure/ocr.py`、`backend/src/projectb/application/material_import.py`、`backend/src/projectb/infrastructure/repositories/material_repo.py`、`backend/tests/unit/test_advanced_material_ingestion.py`、`backend/tests/integration/test_advanced_material_import.py` 及对应导入 UI。重新执行 `writing-plans` 时可重命名或拆分，本文不授予 ownership。

## 首个失败测试

`test_scanned_pdf_ocr_preserves_raw_hash_page_region_and_commits_no_partial_version`：使用许可合成扫描 PDF 和 deterministic OCR stub，断言 locator 仍绑定原始 hash/page/region；OCR 超时或部分页失败时不提交半个材料版本。恢复时首次运行应因 OCR adapter/image locator 尚不存在而失败。

## 验证命令

```powershell
& $env:PROJECTB_PYTHON_EXE -m pytest backend/tests/unit/test_advanced_material_ingestion.py backend/tests/integration/test_advanced_material_import.py -q
& $env:PROJECTB_PYTHON_EXE scripts/test_all.py
```

## 验收标准

- 许可夹具可确定性重放，格式/像素/页数/批次边界前后值均失败关闭。
- 原图、OCR 文本、质量标记和 locator 一一对应；低质量结果不可伪装为已确认 coverage。
- 重复导入幂等，部分失败不污染成功项，删除或 hash 变化使旧 locator 失效。
- 依赖许可证、分发体积、性能和凭据扫描均有本次运行证据。

## 重新启用时人工决定

学生必须决定支持格式、OCR 本地或远端、语言/准确度与人工纠错阈值、批量上限/SLO、是否复用 durable jobs，以及真实私有样本 benchmark 的授权范围。

恢复顺序固定为：重新执行 `brainstorming` -> 写出明确 SPEC diff -> 学生确认完整 SPEC -> 调用 `writing-plans`。随后仍须完成冷启动验证和学生实现批准；不得从本归档直接实现。
