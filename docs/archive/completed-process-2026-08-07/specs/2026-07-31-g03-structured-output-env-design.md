# G-03 结构化输出与本地测试 `.env` 设计

> 状态：待学生复核书面设计。学生已批准在仓库根目录使用被 Git 忽略的 `.env`，并将其作为后续本地测试变量合集；本文固定安全边界和实现范围。

## 1. 问题与根因

最新正式收据 `13a02748-6e78-4f06-abb3-64b9982b2d40` 显示 Claude Code 运行 107 秒并以 0 退出，stdout 是单行合法 JSON，stderr 非空。因此 WSL、CLI 路径、认证、端点、模型请求和 bubblewrap preflight 已进入可运行路径；失败不是外层 JSON 或提示行污染。

runner 使用 `--output-format json` 得到 Claude Code envelope，却只靠自然语言要求模型把 `envelope.result` 写成 JSON。该选项只约束外层输出，不约束 result。当前 Claude Code 2.1.220 本地帮助明确提供 `--json-schema`，runner 未使用它；同时 exit 44 把外层解析失败和内层 result 解析失败合并，导致此前诊断追错层。

## 2. 目标与非目标

目标：

- intake 和 execution 使用 CLI 原生 JSON Schema 约束最终 result。
- 外层 envelope、内层结构化 result、业务契约不匹配使用不同诊断码。
- 根目录 `.env` 可保存多个本地测试变量，runner 只读取自己显式声明的变量。
- 学生填入一次 key 后，后续受控运行不再等待隐藏输入。
- 保持 G-03 两个新 session、冻结 SPEC/PLAN、预算、沙箱、产物和人工门禁不变。

非目标：

- 不把 `.env` 变成产品凭据方案；产品仍使用 Windows Credential Manager。
- 不提交真实 key，不把 `.env` 复制到冷启动目录、证据或分发物。
- 不允许 `.env` 改写正式 G-03 的端点、模型、哈希、预算或任务。
- 不增加自动 API 重试、fallback model 或后台无限循环。

## 3. `.env` 合同

根目录 `.env` 是本机明文兼容配置，已被 `.gitignore` 的 `.env`/`.env.*` 规则排除。提交 `.env.example`，其中只放空占位和中文安全说明；首个变量为：

```dotenv
PROJECTB_G03_CLAUDE_API_KEY=
```

解析器不得执行 `source`、shell 展开、命令替换或变量插值。它接受无 BOM 的 UTF-8、LF/CRLF、空行、以 `#` 开头的注释，以及 `PROJECTB_[A-Z0-9_]+=` 赋值；拒绝 BOM、NUL、重复变量、非法名称、超限文件/行和语法行。不同消费者必须显式选择变量，不得把整份 `.env` 注入环境或把它作为产品运行时配置源。

G-03 仅消费 `PROJECTB_G03_CLAUDE_API_KEY`。该值必须非空、单行、无首尾空白；base URL、模型、预算和哈希继续由受审 runner/命令固定。`.env` 存在时 runner 先证明它仍被 Git 忽略且未被跟踪；否则在联网前失败关闭。

新增 `CredentialSource=Auto|Prompt|DotEnv`：

- `Auto`：存在有效 G-03 变量时使用 `.env`，否则回退隐藏输入。
- `Prompt`：始终隐藏输入，保持现有兼容路径。
- `DotEnv`：必须从 `.env` 取得有效值；缺失或无效时受控退出，不等待交互。

测试只使用运行时拼接的假 key。runner 读取真实值后只保存在进程内存和 Claude 父进程认证环境中，继续在 `finally` 清除；日志、异常、诊断和状态不得包含值或可逆片段。

## 4. 结构化输出

提交两个小型 schema：

- `scripts/cold_start/schemas/g03-intake.schema.json`
- `scripts/cold_start/schemas/g03-execution.schema.json`

两者使用对象类型、完整 required、`additionalProperties:false` 和稳定字段类型。intake schema 包含两个 SHA-256、文件数组、language、task、acceptance_id、ambiguities；execution schema 包含 task、acceptance_id、ambiguities、questions、red_command、green_command。精确哈希、文件顺序、固定 ID、空歧义和命令仍由 coordinator 二次校验，不能只信 schema。

两个 Claude 调用都增加 `--json-schema <schema-json>`。`--output-format json`/`stream-json` 继续负责外层 envelope/事件传输，schema 负责最终 result。提示词保留任务语义，但不再承担唯一格式保证。

## 5. 状态与诊断

完成状态继续使用 `INTAKE_FAILED`、`INTAKE_AMBIGUOUS`、`EXECUTION_FAILED` 等课程门禁枚举；脱敏 `process-diagnostic.json.code` 细分：

- `outer_output_protocol`：stdout 不是预期 Claude envelope/stream。
- `envelope_protocol`：subtype、is_error、费用或 result 字段无效。
- `structured_result_protocol`：result 不符合 JSON/schema 形状。
- `intake_contract_mismatch`：结构正确但哈希、文件、语言、任务或 ID 不匹配。
- 已有 auth、504、timeout、startup 和 MCP 分类保持独立。

诊断可记录 envelope/result 的布尔值、计数和固定枚举，不保存 result、stderr 或任意原文。提示行兼容逻辑只处理已证明的外层传输情况，不再作为当前故障假设。

## 6. 自动执行边界

学生填好 `.env` 后，正式命令使用 `-CredentialSource DotEnv`，因此不再弹出 key 输入。当前 Codex shell 直接创建 WSL 实例受环境策略拒绝；后续优先使用 Computer Use 在学生现有 WSL 终端中执行固定命令。若该通道不可用，学生仍只需运行命令，不再输入 key。

每次正式运行固定总预算上限 `$1.00`、零自动重试、无 fallback。不得建立自动循环或因失败连续付费重跑；一次代码修订后最多发起一次验证，再根据新证据决定下一步。

## 7. 测试与验收

先写失败合同，再实现：

- `.env` 解析覆盖多变量、注释、CRLF、重复项、非法语法、BOM/NUL、超限和无原文泄露。
- `DotEnv` 缺失/无效、`.env` 被跟踪或未忽略时在 CLI 启动前失败。
- 无关测试变量不会进入 Claude 子进程；只有 G-03 key/base URL/model 等明确 allowlist 环境存在。
- CLI 参数对 intake/execution 均包含与文件字节一致的 `--json-schema`。
- 合法外层 envelope + prose result 被分类为 `structured_result_protocol`，不得再归为外层 JSON 错误。
- 合法 schema result 进入现有 intake/执行契约；错误哈希、额外文件、非空歧义和错误命令仍失败。
- 原有 core、entrypoint、capsule、严格 UTF-8、凭据形状、证据矩阵和 `git diff --check` 全部通过。
- `.env` 不在 `git status --untracked-files=all`、index、commit 或证据文件中；`.env.example` 不含 secret 形状。

本设计实现成功只说明 runner 可再次正式验证，不自动关闭 G-03。最终仍需 `G03_EVIDENCE_READY`、独立 replay、中文过程记录和后续学生 G-04 批准。
