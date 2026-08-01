# Remote F and Durable Jobs v2 Archive
Status: ARCHIVED / NOT DISPATCHABLE

本文件保存能力恢复边界，不是实现计划，也不授权 provider 调用或生产代码。

## 目标

增加整文件/课程模式 F，以及持久 job、上传/索引/检索、重启对账、取消和分层删除，且不把 provider 对象当成本地来源权威。

## 延期原因

远端留存、版权、费用、Files/Vector Store 生命周期、at-least-once 重复对象、凭据丢失和删除不可证明等风险远超 v1 的请求级 P；旧 F/durable-job 草稿没有最终同快照评审。

## v1 边界

v1 只有本地 `L` 与请求级片段 `P`。P 只发送用户当次确认且 hash 有效的 locator 片段，使用 `store:false`，不使用 hosted File、Vector Store、File Search、background job 或任意工具；不存在可调用的远端材料对象或 durable-job 权威模型。

## 重新启用前置依赖

- v1 consent/hash/source/delete、Credential Manager、provider port 和本地 persistence 合同均已通过验证。
- 重新核验 provider 能力、区域、保留/删除政策、费用、SDK 版本与许可证；确认真实材料外发权利。
- 先冻结 job migration/repository、lease/heartbeat/cancel/recovery 和故障注入合同。
- 学生明确选择 F 的 provider/profile、预算和凭据清除后的人工清理责任。

## 预计接口/文件

候选接口为 `DurableJobManager.enqueue/claim/heartbeat/recover_incomplete` 和 `RemoteMaterialService.enqueue_upload/reconcile_job/request_delete`。候选路径为 `backend/src/projectb/domain/jobs.py`、`domain/remote.py`、`application/jobs.py`、`application/remote.py`、`infrastructure/repositories/job_repo.py`、`remote_repo.py`、`infrastructure/providers/openai_files.py` 及对应 contract/integration tests。最终路径和 ownership 只能由新的 `writing-plans` 确认。

## 首个失败测试

`test_restart_reconciles_response_lost_upload_without_second_create`：deterministic provider stub 在创建对象后丢失响应；进程重启必须先对账，不得盲目第二次创建，发现多个候选时全部隔离并进入可观察清理状态。恢复时首次运行应因 durable repository/reconciliation service 不存在而失败。

## 验证命令

```powershell
& $env:PROJECTB_PYTHON_EXE -m pytest backend/tests/contract/test_remote_lifecycle.py backend/tests/integration/test_remote_recovery.py backend/tests/integration/test_remote_deletion.py -q
& $env:PROJECTB_PYTHON_EXE scripts/test_all.py
```

## 验收标准

- 缺失、撤销或过期 consent 时网络调用为 0；范围精确绑定 file/hash/profile/config/policy。
- job state、lease、进度、取消和重启可观察；实现只承诺 at-least-once，不宣称 provider exactly-once。
- 每个 course/profile/config 隔离，检索结果二次 allowlist；没有有效本地 locator 时不进入 coverage、evidence 或 plan。
- association、File 和空 store 分层对账；无法证明删除时对象不可用且 UI 保持 `delete_incomplete`。

## 重新启用时人工决定

学生必须决定 F 是否仍有核心价值、具体 provider/model/区域/预算/保留政策、poll/retry 上限、凭据清除后的恢复与人工删除流程，以及 durable jobs 是否也服务本地 OCR/批量导入。

恢复顺序固定为：重新执行 `brainstorming` -> 写出明确 SPEC diff -> 学生确认完整 SPEC -> 调用 `writing-plans`。不得从历史 L/P/F 决定或旧 task 直接进入实现。
