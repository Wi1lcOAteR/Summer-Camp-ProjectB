# Stage B 旧计划归档索引

Status: ARCHIVED / NOT DISPATCHABLE

## 使用边界

本目录保存 2026-07-23 旧 113-unit / 14-plan 体系的原始计划证据。归档动作不把任何旧任务变成可派发任务，也不延续旧 hash 上的局部 PASS。所有文件统一按 **NOT PASS / NOT DISPATCHABLE** 处理，不得用于 G-03、worktree 创建或正式实现。

下表的字节数和 SHA-256 于 2026-07-25 对当前归档字节只读核对。评审摘要明确区分“当前归档 hash 的结论”和“前一个受评审 hash 的历史 finding”；不能把后续未复审修订推断为已修复。

## 文件完整性清单

| ID | 原路径 | 当前归档路径 | 字节数 | SHA-256 |
| --- | --- | --- | ---: | --- |
| A01 | `PLAN.md` | `docs/superpowers/plans/archive/superseded-2026-07-23/PLAN.not-pass.md` | 463731 | `D55007B1C6E0A56E5F3C342439BC53E4C2867F98643CAE27A34507854770E127` |
| A02 | `docs/superpowers/plans/2026-07-22-foundation-scaffold.md` | `docs/superpowers/plans/archive/superseded-2026-07-23/2026-07-22-foundation-scaffold.md` | 234078 | `27BB653A8D5FFFBED37C0DDA3724524EFE1CC1264C869E3CDE15FC7E78E00E09` |
| A03 | `docs/superpowers/plans/2026-07-22-domain-primitives-source.md` | `docs/superpowers/plans/archive/superseded-2026-07-23/2026-07-22-domain-primitives-source.md` | 137520 | `40C48BB62A87F17BFCFB635871F51C350EA2EC9F1AAFEE5ED2D9B7A7C7629C0B` |
| A04 | `docs/superpowers/plans/2026-07-23-persistence-repositories.md` | `docs/superpowers/plans/archive/superseded-2026-07-23/2026-07-23-persistence-repositories.md` | 349782 | `DCF8868850B8A65FCB952F4FFB916C8DA219825CC9D5FB29C7FD234CEFA69C28` |
| A05 | `docs/superpowers/plans/2026-07-23-local-trust-and-provider-control-plane.md` | `docs/superpowers/plans/archive/superseded-2026-07-23/2026-07-23-local-trust-and-provider-control-plane.md` | 221763 | `46E56C37E63AE900638C38DD85C5E7A06C94094C676CE91B606F1DBD3A28F115` |
| A06 | `docs/superpowers/plans/2026-07-23-ci-docs-and-release-preparation.md` | `docs/superpowers/plans/archive/superseded-2026-07-23/2026-07-23-ci-docs-and-release-preparation.md` | 83989 | `8267AC954EE5A667B8816A87E06F37E13452EAAB1F20A20885EC14D7AD1AE17B` |
| A07 | `docs/superpowers/plans/2026-07-23-windows-oci-distribution.md` | `docs/superpowers/plans/archive/superseded-2026-07-23/2026-07-23-windows-oci-distribution.md` | 157042 | `AB0920689358F616E189FB7C4DC0C03598BAC8EB89584A0248FFC37504566C0A` |
| A08 | `docs/engineering/DETAILED_PLAN_AUTHORING_CONTRACT.md` | `docs/superpowers/plans/archive/superseded-2026-07-23/engineering/DETAILED_PLAN_AUTHORING_CONTRACT.md` | 9322 | `B93F949DE36CD89C7101160F237D4FEBCD7305F411C55B20429D62A282DBBFEF` |
| A09 | `docs/engineering/PLAN_SUBSYSTEM_PARTITION.md` | `docs/superpowers/plans/archive/superseded-2026-07-23/engineering/PLAN_SUBSYSTEM_PARTITION.md` | 5958 | `BF3D971765486031E8CB54353B4B366BFB2146861B03540EE57D41A385A2D7F8` |
| A10 | `docs/engineering/plan_fragments/M2-01.md` | `docs/superpowers/plans/archive/superseded-2026-07-23/plan_fragments/M2-01.md` | 60180 | `30D3744A1929F254DAEFFF4ED643CAF556B518026EFC0EC3EA7DF532C54944BA` |
| A11 | `docs/engineering/plan_fragments/T-01.md` | `docs/superpowers/plans/archive/superseded-2026-07-23/plan_fragments/T-01.md` | 86843 | `33D67D3BE30528B0174BC43C5593D003228A980164A44379191790681C8468BB` |
| A12 | `docs/engineering/plan_fragments/T-02.md` | `docs/superpowers/plans/archive/superseded-2026-07-23/plan_fragments/T-02.md` | 72076 | `889AA9C9FDF24C6B376A15529D8C7510BEA7C674DA0744E9908CDC6D0D3C6D94` |

## 文件结论与恢复条件

### A01: 旧 root PLAN

- **覆盖任务/主题：** G-01 至 G-04、T/M/X/API/UI/DEMO/QA/DIST/CI/DOC/FIN，共 113 个 dispatch unit 和 37 个不可派发 Task Group；依赖旧 14-plan 分区。
- **最后已知结论：** 正式 `writing-plans` 门禁为 `ACTIVE REMEDIATION / NOT PASS`；G-03、G-04 和实现批准均未完成。
- **主要 Critical/Major 摘要：** 只有 6 份详细计划存在，完整 14-plan 集未形成或未在同一 root hash 上双评审；旧 task body 曾存在粒度过大、完整代码不足、共享文件 owner、远程证据和 release candidate 绑定问题。后期机械修订不构成最终 PASS。
- **恢复条件：** 不原地恢复。先对目标范围重新执行 `brainstorming`，由学生确认新 `SPEC.md`，再调用 `writing-plans` 生成唯一权威 DAG，并完成同快照双评审、冷启动和学生实现批准。

### A02: Foundation scaffold

- **覆盖任务/主题：** T-01A 至 T-01F3；运行时锁、后端/前端脚手架、secret scanner、统一测试入口和 gate registry。
- **最后已知结论：** 当前归档 hash 绑定旧 root，后续修订没有最终 root 上的 fresh review，因此为 NOT PASS。
- **主要 Critical/Major 摘要：** 最近受评审的前一 hash `837F1E...A59` 曾有 Critical：显示代码缺 import、各 unit 未完整验证 unit/base/worktree/Git root/HEAD；Major 涉及可执行文件身份、环境/输出脱敏、raw-lock 字节身份、reparse/TOCTOU、40-hex 校验、裸命令、Ruff 和子进程清理。它们是前一 hash 的历史 finding，不能直接证明当前归档字节已修复或仍失败。
- **恢复条件：** 按已确认的新 SPEC 重新缩小 foundation ownership 和任务粒度；对新 hash 实际重建显示代码并执行静态/安全检查，再由两个 fresh reviewer 绑定同一 root/plan/tree/packet。

### A03: Domain primitives and source

- **覆盖任务/主题：** T-02A、T-02B1、T-02B2A、T-02B2B、T-02C；ID、材料限制、hash、locator/catalog、unique-page proof 和 facade。
- **最后已知结论：** 当前归档 hash 曾在旧 root `4BCFE8...F08` 上获得 subsystem-only PASS；root 随后改变且完整计划集未通过，因此本归档统一为 NOT PASS / NOT DISPATCHABLE。
- **主要 Critical/Major 摘要：** 对该精确 hash 的旧评审没有未解决 Critical/Major，只有一个非阻断的 cached-diff 检查顺序观察；真正阻断是 root/接口绑定失效和 Stage B 整体未闭合。
- **恢复条件：** 不继承旧 PASS。用学生确认后的 SPEC 和最终 root 重新决定 locator/hash 接口，更新直接前后继合同，并在新 hash 上重新做 SPEC 与质量/安全/许可证评审。

### A04: Persistence repositories

- **覆盖任务/主题：** T-03A 至 T-03C；SQLite migration、课程/材料、learning、remote、audit 和 tombstone repositories。
- **最后已知结论：** 当前归档 hash 是旧 root 上的未复审修订稿；最后独立结论仍为 NOT PASS。
- **主要 Critical/Major 摘要：** 最近受评审的前一 hash `2F6728...810` 曾有 Critical：撤销对象可在 `delete_incomplete` 后重新获得 scope token、仅凭 reason 即可写入 deleted tombstone；Major 涉及 Ruff/mypy、hash/UTC 校验、超大步骤、T-03C AC 范围、native timeout 和 staged packet 绑定。当前归档 hash 没有 fresh disposition。
- **恢复条件：** 依据新 v1 移除延期的 F/durable-job ownership，只规划当前 SQLite 实体和删除语义；新 migration/repository 合同必须从 failing tests 开始，并在同一新 hash 上重做两阶段评审。

### A05: Local trust and provider control plane

- **覆盖任务/主题：** T-04A/B/C、T-05A/B/C、T-06、T-07；loopback/Host/Origin/CSRF、凭据、provider profile、consent、ports 和 audit。
- **安全归档说明：** 提交前扫描在两处 synthetic OpenAI-token 测试字面量上命中。可提交副本只把这两处替换为 `[REDACTED_FAKE_TEST_TOKEN]`；其余内容不变。原始字节本地保存在被忽略的 `tmp/stage-b-archive-20260725/superseded-originals/2026-07-23-local-trust-and-provider-control-plane.original.md`，原 SHA-256 为 `394490C0E64AC96C0B7709DA9977C81D9F8D7E21DACE463F3455555FF1B6DC64`，不得 stage 或输出原值。
- **最后已知结论：** 修订冻结稿，仍引用旧 root、旧 predecessor hash 和未物化的 G-04 v2 map；没有 fresh review，结论为 NOT PASS。
- **主要 Critical/Major 摘要：** 文件自身声明 `G04_SCHEMA_AMENDMENT_REQUIRED`；机器可验证 worktree row/validator 不存在，foundation/persistence 终态 hash 未绑定。旧依赖变更后所有 cross-plan review 均失效。
- **恢复条件：** 以新 v1 的 L/P、三个具名端口和 Credential Manager 边界重新规划；先确认新的 dispatch/worktree 合同，再冻结当前依赖 hash 并取得两个独立评审。

### A06: CI, docs, and release preparation

- **覆盖任务/主题：** CI-01A/B/C、DOC-01、FIN-01A1；license/CI contract、GitLab/GitHub workflow、README 和本地 release evidence。
- **最后已知结论：** 修订 subagent 中断，当前 hash 未 fresh review，且 authoring root 已过期；NOT PASS。
- **主要 Critical/Major 摘要：** 直接 YAML parser pin/lock/license 未闭合，CI-01A/B 的 verifier path ownership 与旧 root map 不一致，immutable packet/map 和双 reviewer binding 未形成；不得把草稿中的 expected PASS 当作 CI 事实。
- **恢复条件：** 在新计划中按当前课程要求重新划分 CI、文档和外部证据 owner；依赖锁、`unit-test` job、候选 commit 与双平台 observation 必须有实际验证和独立评审。

### A07: Windows and OCI distribution

- **覆盖任务/主题：** DIST-01、DIST-02；Windows x64 单文件、clean-host smoke、OCI demo、网络隔离和 evidence schema。
- **最后已知结论：** 修订 subagent 中断，当前 hash 未 fresh review、绑定旧 root；NOT PASS。
- **主要 Critical/Major 摘要：** predecessor terminal hashes 未提供，D-025 仍阻塞 host-specific OCI/public delivery，未执行干净 Windows、Docker、发布或部署验证；草稿不能证明 PyInstaller/OCI 可分发。
- **恢复条件：** 先确认新 SPEC 的分发合同与 D-025，再用当前锁、许可和目标环境重新写计划；Windows/OCI 各自需要可复现 build/run、干净环境证据和同 hash 双评审。

### A08: Detailed plan authoring contract

- **覆盖任务/主题：** 旧 14-plan 集的通用格式、runtime prelude、exact staged-set、private review packet、TDD 和 cross-plan review 规则。
- **最后已知结论：** 仅为 Stage B 规则输入，从未是 plan PASS、测试结果或实现授权；随旧体系归档后为 NOT PASS / NOT DISPATCHABLE。
- **主要 Critical/Major 摘要：** 没有该精确文件的独立 PASS receipt；它依赖未物化的 `WORKTREE_MAP.v2.json` 和旧 root/subplan hash 模型，且不能弥补旧计划集缺失或未复审的问题。
- **恢复条件：** 可只读提取仍适用的 TDD、staged-set 和 reviewer-binding 安全原则；必须针对新 SPEC、单一 DAG 和实际工具链重新写入新计划并复审，不能直接把本合同当执行脚本。

### A09: Detailed plan partition record

- **覆盖任务/主题：** 将旧 113 个 unit 分成 14 份详细计划、12 个 root 人工/外部 unit，并记录共享路径 owner 顺序和 authoring batches。
- **最后已知结论：** Stage B planning input only；记录时多数计划未生成，未形成全套 review，NOT PASS。
- **主要 Critical/Major 摘要：** 没有该精确文件的 standalone PASS；系统性 Major 是 14-plan 集不完整、状态很快陈旧、同接口需跨多文件同步。它不能证明 unit 可执行或 shared-path handoff 已验证。
- **恢复条件：** 新 v1 明确要求一个权威 active DAG；除非新的 brainstorming 和学生决策重新扩大范围，否则只保留为历史分解证据，不恢复旧 14-plan 拓扑。

### A10: M2-01 fragment

- **覆盖任务/主题：** 互斥/竞态参数化 oracle 与起点探针的早期草稿。
- **最后已知结论：** `INCOMPLETE DRAFT - DO NOT DISPATCH`；未链接 root ledger，未通过 `writing-plans`。
- **主要 Critical/Major 摘要：** drafting 在 T-01/T-02 Critical 到达后中止；旧机械审计还发现引用未定义 test helper/import。文件没有完整 task、评审或集成合同。
- **恢复条件：** 不补写该 fragment。若当前 confirmed SPEC 仍需要相关 evaluator，应在新的 M2 计划中按一个 evaluator/小任务重写 red-green 合同并 fresh review。

### A11: T-01 fragment

- **覆盖任务/主题：** 早期可复现项目与测试脚手架草稿。
- **最后已知结论：** frozen FAIL；不是正式详细计划，也不可派发。
- **主要 Critical/Major 摘要：** 42 个路径、82 个 checkbox 超出单 fresh worker；与 root file set/ledger 不一致；scanner 漏 `.lock`/`.sql`/`.sh` 和 NUL/reparse 风险；Windows 裸 `npm` 可失败，且引用缺失的 `e2e` script/G-02C owner。
- **恢复条件：** 仅保留失败证据。新 foundation plan 必须按当前 SPEC 和真实工具链重新拆分，并用新 hash 完成重建、静态检查、scanner 与双评审。

### A12: T-02 fragment

- **覆盖任务/主题：** 早期 immutable material primitives、SourceLocator 和 unique-page proof 草稿。
- **最后已知结论：** `DRAFT / UNREVIEWED / NOT DISPATCHABLE`，frozen FAIL。
- **主要 Critical/Major 摘要：** 13 个路径、63 个步骤仍过大；package layout/proof signature 与 root 冲突；catalog/member runtime type 校验可泄漏异常或错误拆分字符串；声明的 21/72 测试数与重建的 23/74 不一致。
- **恢复条件：** 不合并该 fragment 与后来的 domain plan。新 M1/source 合同必须由 confirmed SPEC 重新定义，并在 root、public exports、tests 和 downstream imports 同一快照上评审。

## `.r5` 重建树摘要

- **位置：** `tmp/stage-b-archive-20260725/r5-verify-final-20260723`
- **文件数：** `1021`
- **总字节数：** `35989967`
- **Manifest-v1 SHA-256：** `50187D07B1BC03226B26AD3DD8873C01C6EDD2E244D069116CC60FD728277C3D`
- **算法：** 按 `/` 形式的相对路径升序，为每个文件生成 UTF-8 行 `relative_path<TAB>byte_length<TAB>file_sha256<LF>`，连接所有行后计算 SHA-256；文件内容未拼成单个产品源码包。

文件数和总字节数已只读复核；SHA-256 保留归档时记录的 tree 摘要。该目录是旧计划显示代码的临时重建、测试缓存和验证产物，不是 ProjectB 正式源码、实现进度、计划 PASS 或发布产物。它必须留在 `tmp/` 的本地归档边界内，不得作为源码提交、stage、打包或分发。
