# Skill Chain 数据交换格式规范

> **角色**: 本文件定义了 `skill-chain-planner`（输出方）与 `skill-chain-executor`（消费方）之间的**显式数据契约**。
> **版本**: 1.0.0 — 与 planner v1.3.0 / executor v1.0.0 对齐
> **维护规则**: 修改 planner 或 executor 中任一方的输出/解析逻辑后，必须同步更新本文件。

---

## 一、交换概览

```
skill-chain-planner                  skill-chain-executor
     │                                       │
     │  写入规划目录 $PLAN_DIR                 │  读取解析
     ▼                                       ▼
┌─────────────────────────────────────────────────────────┐
│                    $PLAN_DIR/                            │
│  ┌──────────────────────────────────────────────────┐   │
│  │ chain-overview.md    [必需] — 依赖矩阵 + 流转表    │   │
│  │ risk-register.md     [可选] — 结构化风险登记表     │   │
│  │ skills/              [必需] — 子 Skill 三层规格    │   │
│  │   skill-P{0|1|2}-{name}.md                       │   │
│  │ usage-guide.md       [可选] — 创建/组合/验证指南   │   │
│  │ implementation-roadmap.md [可选] — 分阶段实施路线  │   │
│  │ rollback-guide.md    [可选] — 故障恢复指南         │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

**Planner 的职责**: 按本规范**完整、准确**地生成所有必需文件，Executor 解析失败的首因是 Planner 输出格式偏离。

**Executor 的职责**: 按本规范**容错解析**——必需字段缺失时报错终止，可选字段缺失时使用默认值继续。

---

## 二、类型系统

本规范中所有字段采用统一类型标注。类型标注出现在字段描述中，格式为 `[type]`。

### 2.1 基础类型

| 类型 | 定义 | 示例值 |
|------|------|--------|
| `text` | 自由文本字符串 | `"将 PDF 转换为 Markdown"` |
| `int` | 整数 | `3` |
| `bool` | 布尔值 | `true` / `false` |
| `float` | 浮点数 | `2.0` |

### 2.2 枚举类型

| 类型 | 定义 | 可选值 |
|------|------|--------|
| `enum(A\|B\|C)` | 从固定集合中取一值 | 按各字段定义 |

**全局枚举值定义**：

| 枚举名 | 可选值 | 适用场景 |
|--------|--------|---------|
| **Priority** | `P0` / `P1` / `P2` | 子 Skill 优先级 |
| **SkillStatus** | `需新建` / `已有` / `需升级` | 子 Skill 当前状态 |
| **NodeType** | `转换` / `分析` / `生成` / `操作` | 子任务节点类型 |
| **ArchMode** | `pipeline` / `fanout` / `layered` / `orchestrator` / `chain` / `cqrs` / `pubsub` | 链架构模式 |
| **ExecType** | `serial` / `parallel` / `hybrid` / `conditional` | 执行顺序类型 |
| **FormatType** | `.md` / `.json` / `.csv` / `.txt` / `.yaml` / `.xml` / `binary` | 文件格式 |
| **Protocol** | `file` / `arg` / `mixed` | 数据传递协议 |
| **Idempotency** | `full` / `conditional` / `none` | 幂等性级别 |
| **Observability** | `full` / `partial` / `manual` | 可观测性级别 |
| **RecoveryStrategy** | `restart` / `skip` / `fallback` / `compensate` | 恢复策略 |
| **RiskSeverity** | `critical` / `high` / `medium` / `low` | 风险综合评分 |
| **RiskProbability** | `high` / `medium` / `low` | 风险发生概率 |
| **RiskImpact** | `severe` / `moderate` / `minor` | 风险影响程度 |
| **RiskCategory** | `dependency` / `data` / `format` / `cascade` / `resource` / `external` / `silent` | 风险类别 |
| **Stability** | `stable` / `candidate` / `experimental` | 接口稳定性 |
| **DataSource** | `upstream` / `user` / `filesystem` | 输入数据来源 |
| **MilestoneStatus** | `not_started` / `in_progress` / `completed` | 里程碑状态 |

### 2.3 复合类型

| 类型 | 定义 | 示例值 |
|------|------|--------|
| `ref(name)` | 对另一个实体的交叉引用 | `ref(doc-converter)` |
| `ref(null)` | 空引用（无依赖） | `null` |
| `path` | 相对路径字符串 | `./doc-converter/output/` |
| `list<T>` | T 类型的有序列表 | `["文档处理", "格式转换"]` |
| `object` | 键值对映射 | `{ key: value }` |

---

## 三、chain-overview.md 模板（[必需]）

> Executor Step 2 解析此文件。**此文件是 Planner 与 Executor 之间最关键的契约**。

```markdown
---
schema_version: "1.0"
generated_at: "YYYY-MM-DD HH:MM:SS"
chain_name: "<task-name>"                          # [text] kebab-case, 与 $PLAN_DIR 目录名一致
total_skills: <N>                                  # [int] 链中 Skill 总数
extensions: {}                                     # [object] 自定义扩展字段
---

# <任务名称> — Skill 链架构总览

## 1. 链摘要
- **核心目标**: [text] — 一句话描述整个链要达成的目标
- **最终产出**: [text] — 链执行完成后产出的具体文件/数据/结果
- **目标用户**: [text] — 谁将使用这个链的输出

## 2. 架构模式
- **主模式**: [enum(ArchMode)] — 如 `pipeline`
- **备选模式**: [enum(ArchMode)] (optional) — 主模式不可用时的回退
- **选择理由**: [text] — 为什么选择该架构模式

## 3. 执行顺序
- **类型**: [enum(ExecType)] — `serial` / `parallel` / `hybrid` / `conditional`
- **最大并行数**: [int, min=1, max=16] — 当 type=parallel 或 hybrid 时生效
- **流程图**:
  ```
  // 示例 — 严格管道:
  [A:doc-converter] → [B:md-formatter] → [C:summarizer] → [D:report-writer]

  // 示例 — 扇出 + 管道:
           ┌→ [B:analyzer-1] ─┐
  [A:loader] ┤                 ├→ [D:merger] → [E:reporter]
           └→ [C:analyzer-2] ─┘

  // 示例 — 条件分支:
  [A:classifier] → 判断条件 ─┬→ [B:path-a] ─┐
                             └→ [C:path-b] ─┴→ [D:finalizer]
  ```

## 4. 依赖关系矩阵

> Executor 解析此表获取: 名称(name)、类型(type)、优先级(priority)、上游(upstream)、下游(downstream)、**状态(status)**。
> **status 字段由 Planner 评估后填写**，Executor 据此决定 `ACTION_CREATE` / `ACTION_VERIFY` / `ACTION_UPGRADE`。

| Skill | 类型 | 优先级 | 上游依赖 | 下游影响 | 状态 |
|-------|------|--------|---------|---------|------|
| <skill-name> | [enum(NodeType)] | [enum(Priority)] | [ref(null\|skill-name)] 多个用 `, ` 分隔 | [ref(skill-name)] 多个用 `, ` 分隔 | [enum(SkillStatus)] |

> **规则**:
> - 表头字段名固定（Executor 按列名定位，不依赖列顺序）
> - `上游依赖` 为 `null` 时表示无依赖（起始节点）
> - `状态` 为 `需新建` → Executor 标记为 `ACTION_CREATE`
> - `状态` 为 `已有` → Executor 标记为 `ACTION_VERIFY`
> - `状态` 为 `需升级` → Executor 标记为 `ACTION_UPGRADE`

## 5. 数据流转表

> Executor Step 7 使用此表检查上下游接口一致性。

| Step | Skill | 输入来源 | 输出路径 | 格式 | 协议 |
|------|-------|---------|---------|------|------|
| <N> | [ref(skill-name)] | [ref(user\|upstream-skill\|filesystem)] | [path] | [enum(FormatType)] | [enum(Protocol)] |

> **规则**:
> - Step 从 1 开始递增
> - `输入来源` 为 `user` 表示用户直接提供；`filesystem` 表示从文件系统读取
> - `协议` = `file` 表示通过文件传递；`arg` 表示通过 `$ARGUMENTS` 传递；`mixed` 表示混合

## 6. 复用决策
- **已有可复用的 Skill**: [list<ref(skill-name)>] (optional) — 标注为 `状态: 已有` 的 Skill
- **需新建的 Skill**: [list<ref(skill-name)>] — 标注为 `状态: 需新建` 的 Skill
- **需升级的 Skill**: [list<ref(skill-name)>] (optional) — 标注为 `状态: 需升级` 的 Skill

## 7. 架构质量属性
- **幂等性**: [enum(Idempotency)] — `full`(天然幂等) / `conditional`(部分操作需注意) / `none`(每次执行不同)
- **可观测性**: [enum(Observability)] — `full`(每步可追踪) / `partial`(关键步骤可追踪) / `manual`(需手动检查)
- **恢复策略**: [enum(RecoveryStrategy)] — `restart`(从头重试) / `skip`(跳过失败步骤) / `fallback`(降级执行) / `compensate`(补偿操作)
- **备注**: [text] (optional) — 补充说明

## 8. 扩展字段
- **extensions**: [object] (optional) — 项目特定的自定义扩展，如部署约束、环境需求等。Executor 会忽略不识别的扩展字段。
```

---

## 四、skills/skill-P{优先级}-{name}.md 模板（[必需]）

> Executor Step 5.1 读取此文件的**完整原始内容**后原样传递给 `skill-for-skills`。
> **因此此文件必须同时满足两个消费者的需求**:
> 1. Executor 能从文件名提取优先级(`P0`/`P1`/`P2`)和 Skill 名
> 2. skill-for-skills 能解析 frontmatter 和正文生成 SKILL.md

### 4.1 文件命名规则

```
skills/skill-P{0|1|2}-{skill-name}.md
```

- `P{0|1|2}` — 必须大写，与链规划中的优先级一致
- `{skill-name}` — kebab-case，与依赖关系矩阵中的 Skill 列一致
- 示例: `skills/skill-P0-doc-converter.md`

### 4.2 三层规格模板

```markdown
---
spec_schema: "2.0"
skill_name: "<skill-name>"                          # [text] kebab-case
priority: "<P0|P1|P2>"                              # [enum(Priority)]
node_type: "<转换|分析|生成|操作>"                    # [enum(NodeType)]
status: "<需新建|已有|需升级>"                       # [enum(SkillStatus)]
upstream: "<skill-name>"                            # [ref(null|skill-name)] null 表示无上游
downstream:                                         # [list<ref(skill-name)>] (optional)
  - "<skill-name>"
tags:                                               # [list<text>] (optional)
  - "<tag>"
extensions: {}                                      # [object] (optional)
---

# Skill: <skill-name>

## 身份层（Identity Layer）

> 提供给 `skill-for-skills` 的元数据，用于生成 frontmatter。

- **name**: [text] — 与文件名中的 skill-name 一致
- **触发关键词**: [list<text>] — 至少 3 个，用于填充 `description` 和触发自动加载
  - 示例: `"转换文档"`, `"doc to md"`, `"文档格式转换"`
- **分类标签**: [list<text>] — 如 `["文档处理", "格式转换"]`
- **建议工具集**: [list<text>] — 最小权限原则下的工具列表
  - 可选值: `Read`, `Write`, `Edit`, `Glob`, `Grep`, `Bash`, `WebSearch`, `WebFetch`
- **建议运行模式**: [text] (optional) — 如 `context: fork, agent: general-purpose`

## 接口层（Interface Layer）

> 定义本 Skill 的输入/输出契约。Executor Step 7 使用此信息做接口一致性检查。

### 输入契约
- **来源**: [enum(DataSource)] — `upstream`(上游 Skill) / `user`(用户) / `filesystem`(文件系统)
- **上游 Skill**: [ref(null\|skill-name)] — 当 source=upstream 时必填
- **格式**: [enum(FormatType)] — 期望的输入文件格式
- **编码**: [text] (optional, default="utf-8")
- **数据结构**: [text] (optional) — 字段列表、类型说明
- **数据量预期**: [text] (optional) — `<1KB` / `1KB-1MB` / `>1MB`
- **验证规则**:
  - **空值处理**: [text] — 输入为空时做什么
  - **格式错误处理**: [text] — 格式不匹配时做什么
  - **字段缺失处理**: [text] — 必填字段缺失时做什么

### 输出契约
- **产物名称**: [text] — 如 "转换后的 Markdown 文件"
- **格式**: [enum(FormatType)] — 输出文件格式
- **保存路径**: [path] — 如 `./<skill-name>/output/<file>.<ext>`
- **关键字段**: [list<text>] (optional) — 输出包含的关键字段
- **验证标准**:
  - **正确性**: [text] — 如何判断输出正确（如 "抽样验证 JSON schema"）
  - **完整性**: [text] — 如何判断输出完整（如 "行数与输入一致"）

### 错误契约
- **输入不合法时**: [text] — 行为描述
- **执行中异常时**: [text] — 行为描述
- **下游依赖不可用时**: [text] — 含重试次数和间隔

### 接口稳定性
- **稳定性**: [enum(Stability)] (optional, default="stable")
  - `stable` = 已固化，下游可安全依赖
  - `candidate` = 可能微调，下游应防御性读取
  - `experimental` = 可能大改，下游不应强依赖

## 实现层（Implementation Layer）

> 提供给 `skill-for-skills` 的 Workflow 指令。每条步骤需包含输入/处理/输出/异常/衔接五要素。

### Step 1: <动词性短语>
**输入**: [text] — 参数名(类型,必填/可选,默认值,取值范围)
**处理过程**: 
1. [text] — 具体操作
2. [text] — 边界条件说明
**输出**: [text] — 输出名(类型) → 传递给谁
**异常处理**: [text] — 错误场景 → 处理方式
**步骤衔接**: [text] — 下一步是什么

### Step 2: <动词性短语>
... (同上格式)

### Step N: <动词性短语>
...

## 附加约束
- **Always**: [list<text>] — 必须遵守的规则
- **Never**: [list<text>] — 禁止的行为
- **输出格式**: [text] — 整体输出格式要求

## 推断与假设
> 记录 Planner 在生成此规格时做的推断（供用户审阅确认）。

- **推断 1**: [text] — 推断内容 + 推断依据
- **假设 1**: [text] — 假设内容 + 风险说明

## 扩展字段
- **extensions**: [object] (optional) — `skill-for-skills` 会忽略不识别的字段
```

---

## 五、risk-register.md 模板（[可选]）

> Executor Step 8 引用此文件中的高风险项输出到最终报告。

```markdown
---
schema_version: "1.0"
generated_at: "YYYY-MM-DD HH:MM:SS"
chain_name: "<task-name>"
total_risks: <N>                                  # [int]
extensions: {}                                     # [object]
---

# <任务名称> — 风险登记表

## 风险 1: <risk-name>                              # [text] kebab-case
- **类别**: [enum(RiskCategory)]
- **关联 Skill**: [ref(skill-name)] — 风险出现在哪个 Skill
- **触发场景**: [text] — 描述具体的触发条件
- **发生概率**: [enum(RiskProbability)]
- **影响程度**: [enum(RiskImpact)]
- **综合评分**: [enum(RiskSeverity)] — probability × impact 综合判定

### 应对措施
- **降级方案**: [text] (optional) — 无法正常执行时的降低规格方案
- **重试策略**: [text] (optional) — 最多重试次数、间隔时间、退避方式
- **替代路径**: [text] (optional) — 绕过该风险的替代执行路径
- **人工确认点**: [bool] (optional) — 是否需要在执行到此步骤前暂停等待用户确认

### 连锁影响
- **下游影响**: [list<ref(skill-name)>] — 此风险触发后受影响的后续 Skill
- **级联风险**: [text] — 描述连锁故障路径

## 风险 2: <risk-name>
... (同上格式)
```

---

## 六、usage-guide.md 模板（[可选]）

```markdown
---
schema_version: "1.0"
generated_at: "YYYY-MM-DD HH:MM:SS"
chain_name: "<task-name>"
extensions: {}
---

# <任务名称> — 创建与组合使用指南

## 1. 前置准备
- [text] — 环境要求
- [text] — 需安装的依赖
- [text] — 需预先创建的目录或配置

## 2. 创建各子 Skill

按优先级和依赖顺序，使用 `skill-for-skills` 创建每个子 Skill:

```
# 第一步: 创建无依赖的 P0 Skill
/skill-for-skills <规格文件内容或需求描述>

# 第二步: 创建依赖第一步输出的 Skill
/skill-for-skills <规格文件内容或需求描述>

# ...
```

## 3. 组合使用

所有子 Skill 创建完成后，按以下顺序调用:

```
1. /skill-a <输入>
2. /skill-b <步骤1的输出>
3. /skill-c <步骤2的输出>
```

## 4. 验证方法

- [text] — 如何验证单个 Skill 是否正常工作
- [text] — 如何验证链的整体输出是否正确

## 5. 故障排除

| 常见问题 | 可能原因 | 解决方法 |
|---------|---------|---------|
| [text] | [text] | [text] |
```

---

## 七、implementation-roadmap.md 模板（[可选]）

```markdown
---
schema_version: "1.0"
generated_at: "YYYY-MM-DD HH:MM:SS"
chain_name: "<task-name>"
extensions: {}
---

# <任务名称> — 实施路线图

## 阶段 1: 核心链搭建（P0 Skill）
- **目标**: [text]
- **里程碑**: [text] — 如何判断阶段 1 完成
- **状态**: [enum(MilestoneStatus)]

| Skill | 预计耗时 | 验证标准 |
|-------|---------|---------|
| [ref(skill-name)] | [text] | [text] |

## 阶段 2: 辅助功能（P1 Skill）
- **目标**: [text]
- **里程碑**: [text]
- **状态**: [enum(MilestoneStatus)]

| Skill | 预计耗时 | 验证标准 |
|-------|---------|---------|
| [ref(skill-name)] | [text] | [text] |

## 阶段 3: 善后与优化（P2 Skill）
- **目标**: [text]
- **里程碑**: [text]
- **状态**: [enum(MilestoneStatus)]

| Skill | 预计耗时 | 验证标准 |
|-------|---------|---------|
| [ref(skill-name)] | [text] | [text] |
```

---

## 八、rollback-guide.md 模板（[可选]）

```markdown
---
schema_version: "1.0"
generated_at: "YYYY-MM-DD HH:MM:SS"
chain_name: "<task-name>"
extensions: {}
---

# <任务名称> — 回滚与故障恢复指南

## 场景 1: 单个 Skill 创建失败

- **现象**: 某个子 Skill 在 `skill-for-skills` 创建时报错
- **恢复步骤**:
  1. [text] — 检查步骤
  2. [text] — 修复操作
  3. [text] — 验证操作
- **是否需要重建下游**: [bool] — 失败 Skill 的下游是否需要重新创建
- **数据完整性**: [text] — 已产生的中间数据如何处理

## 场景 2: 链执行中途失败

- **现象**: 上一步成功，当前步骤失败
- **恢复步骤**:
  1. [text]
  2. [text]
- **是否保留上游输出**: [bool]
- **断点续传**: [bool] — 是否支持从失败步骤继续执行

## 场景 3: 接口契约不匹配

- **现象**: 下游 Skill 无法消费上游输出
- **恢复步骤**:
  1. [text]
  2. [text]
- **应急方案**: [text] — 手动转换或调整的方法
```

---

## 九、Executor 解析规则参考

> 以下规则供 Executor 实现者和维护者参考。Planner 输出的文件应遵守此处定义的容错预期。

### 9.1 文件存在性检查

| 文件 | 必需性 | 缺失时的行为 |
|------|--------|------------|
| `chain-overview.md` | **必需** | ❌ 终止执行，输出 "规划目录不完整: 缺少 chain-overview.md" |
| `skills/` 目录 | **必需** | ❌ 终止执行，输出 "规划目录不完整: 缺少 skills/ 目录" |
| `skills/skill-P*-*.md` (至少 1 个) | **必需** | ❌ 终止执行，输出 "skills/ 目录下未找到任何子 Skill 规格文件" |
| `risk-register.md` | 可选 | ⚠️ 最终报告中标注 "未提供风险登记表" |
| `usage-guide.md` | 可选 | ⚠️ 最终报告中标注 "未提供使用指南" |
| `implementation-roadmap.md` | 可选 | ⚠️ 继续执行，不影响 |
| `rollback-guide.md` | 可选 | ⚠️ 继续执行，不影响 |

### 9.2 依赖关系矩阵解析规则

- Executor 按**列名**定位字段，不依赖列顺序
- 必需列: `Skill`、`优先级`、`上游依赖`、`状态`
- 可选列: `类型`、`下游影响`
- `状态` = `需新建` → `ACTION_CREATE`
- `状态` = `已有` → `ACTION_VERIFY`
- `状态` = `需升级` → `ACTION_UPGRADE`
- 如果 `状态` 列缺失 → Executor 回退检查文件系统（`ls <skill-name>/SKILL.md`）

### 9.3 排序规则

1. 先按优先级排序: P0 → P1 → P2
2. 同一优先级内按拓扑序: 无上游依赖的排前面
3. 同一优先级且无依赖关系时按数据流转表 Step 编号

### 9.4 skill-for-skills 传递规则

- Executor 读取 `skills/skill-P{priority}-{name}.md` 的**完整原始内容**
- **不做任何修改、截断、重新格式化**
- 将该内容作为参数传递给 `skill-for-skills`

---

## 十、版本演进公约

1. **向前兼容**: 新增字段使用 `optional` 标记，旧版 Executor 可以忽略
2. **废弃流程**: 字段不再使用时先标记 `[deprecated]`，一个版本后再移除
3. **schema_version 递增规则**:
   - 新增可选字段: 次版本号 (如 `1.0` → `1.1`)
   - 新增必需字段或移除字段: 主版本号 (如 `1.0` → `2.0`)
4. **同步更新**: Planner 或 Executor 升级后，检查本文件是否需要同步更新
