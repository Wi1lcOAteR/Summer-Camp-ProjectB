# G-03 原子执行与输出预算修订设计

**状态：PROPOSED / REQUIRES STUDENT CONFIRMATION**

## 1. 已观察问题

修复哈希后，Claude intake 已在 SPEC `01E9A154...1D030`、PLAN
`11EB0111...9964C` 上通过。随后两次 execution 长时间停留在 thinking，未创建任何候选文件；界面没有可见终止按钮。现有证据不能区分网关延迟、模型内部规划循环和输出上限，但 thinking 已暴露两个确定问题：

- 模型把未定义的单路径 `source` 自行猜为 `path`，违反“有歧义就停止”。
- `F-01S1` 同时要求测试框架、六类 token、边界、UTF-8、JSON 顺序、错误码、自扫描和完整红绿证据，不符合单 session 小任务要求，也容易超过模型输出预算。

当前 execution 只作为失败/差距证据，不算 G-03 PASS。

## 2. 方案比较

1. **原样重试**：不改哈希，但会重复相同歧义和输出风险，不采用。
2. **只补字段说明**：能消除 `source` 猜测，但任务体量仍过大，不采用。
3. **拆成原子任务并锁定输出预算**：推荐。冷启动验证较小的完整行为，正式实现再串行扩展其余规则。

## 3. 任务拆分

### F-01S1A：单路径协议与一个直接规则

只创建：

- `scripts/tests/bootstrap_scanner_contract.ps1`
- `scripts/bootstrap_scan_credentials.ps1`

只实现：

- `Write-ScanRecord([string]$Source, [string]$FilePath, [string]$Rule)`
- `Convert-SourceText([byte[]]$Bytes)`
- `Find-DirectSecret([string]$Text, [string]$Source, [string]$FilePath)`
- `-Path` 单文件入口
- `provider_api_key`：字面量 `sk-` 加 20--200 个 `[A-Za-z0-9_-]`，并执行既有邻接边界

固定语义：

- `source` 永远是字面量 `path`。
- 输出 `path` 是调用方传入的 `-Path` 字符串，将反斜杠替换为 `/` 并移除一个开头的 `./`；读取时可解析绝对路径，但不得把临时目录绝对路径写入稳定收据。
- 缺少 `-Path`：exit 3，且唯一输出为 `CREDENTIAL_SCAN_ERROR {"code":"usage_missing_scope"}`。
- 不存在、非普通文件或读取失败：exit 3，`code=read_failed`，可按固定键序追加 `source`、`path`。
- 非严格 UTF-8、BOM 或 U+FFFD：exit 3，`code=decode_failed`。
- 命中：exit 2；干净：exit 0，唯一输出 `CREDENTIAL_SCAN_PASS files=1`。

合同只包含 `usage_and_output`、`provider_rule` 两组。正例必须由两个各自不匹配的片段在运行时拼接；固定覆盖最短正例、过短负例、允许标点边界和禁止邻接字符。红灯仍为 exit 1 且唯一输出 `CONTRACT_RED scanner_missing`；绿灯最后输出 `BOOTSTRAP_SCANNER_PATH_PASS`。

### F-01S1B：其余直接规则与产物安全

在同两文件上串行增加 GitHub、AWS、Google、Slack 和 private-key 规则，以及 `artifact_direct_safety`、去重和稳定排序。它依赖 F-01S1A，不进入本轮冷启动 execution。

## 4. 冷启动与输出预算

- Intake 目标改为 `F-01S1A`，acceptance ID 改为 `F01S1A_SINGLE_RULE_SCANNER_V2`。
- Execution 仍使用第二个全新非 Codex session，初始目录只有最终 SPEC/PLAN。
- 合同文件上限 180 行，scanner 文件上限 140 行；超过上限必须停止并报告 plan defect，不能继续生成。
- 每次只写一个完整文件并立即执行对应命令；禁止先在最终自然语言回复中拼装整份源码。
- 最终摘要不超过 300 个英文词，只报告问题、文件、红绿命令/退出码/输出、扫描结果和费用。
- 20 分钟或预算上限保持失败关闭；空输出、无工具写入、输出截断或没有终止结果均记录为 execution incomplete。

## 5. 验证与门禁

修订将同步 `SPEC.md`、`PLAN.md`、英文 capsule、课程矩阵、G-03 手册和快照合同。随后必须依次完成：

1. capsule、快照、UTF-8、placeholder 和任务映射机械检查；
2. 同一新哈希的 SPEC 合规评审与质量/安全/许可证评审；
3. 学生确认新 SPEC/PLAN；
4. 新鲜 Claude intake；
5. 只有 intake 无歧义时才运行新的 F-01S1A execution。

本修订不改变产品功能范围，不授权正式实现，也不关闭 G-03/G-04。
