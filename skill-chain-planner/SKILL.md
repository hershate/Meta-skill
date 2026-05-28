---
name: skill-chain-planner
description: >-
  Decompose complex tasks into multi-skill chains. Generates step-by-step
  plans for using `skill-for-skills` to construct each skill and compose
  them into a working pipeline. Triggered by: "任务分解", "skill链规划",
  "复杂任务拆分", "多skill协作", "chain planner", "工作流拆分",
  "多步骤任务", "skill pipeline", "架构规划", "多步工作流",
  "pipeline设计", "skill依赖分析", "skill编排", "任务流水线".
version: 1.3.0
metadata:
  tags: planning, architecture, workflow, skill-chain, decomposition
allowed-tools: Read Write Glob WebSearch
context: fork
agent: Plan
---

# Skill Chain Planner

## Purpose
根据用户描述的复杂任务，输出一份完整的 **Skill 链创建规划**：将任务拆解为多个单一职责的子 Skill，设计各 Skill 之间的数据流转与执行顺序，并指导用户如何使用 `skill-for-skills` 逐个创建这些 Skill，最终组合为可工作的 Skill 链。

本 Skill **不直接生成任何 Skill 文件**，它只输出规划文档，让用户拿着规划去使用 `skill-for-skills`。

## When to Use
- 用户描述了一个多步骤的复杂任务，需要一个以上 Skill 协作完成
- 用户发现单个 Skill 无法高效完成某个工作流，需要拆分为多个专注的子 Skill
- 用户需要将一个现有的大流程拆解为多个 Skill 的流水线
- 用户不清楚如何组合使用多个 Skill 解决实际问题
- 用户需要一份"先创建什么、再创建什么、最后如何串联"的行动指南

## When NOT to Use
- 用户只想创建一个简单的单 Skill 任务 —— 应直接使用 `skill-for-skills`
- 用户询问 Skill 概念或规范本身 —— 应引导阅读 `skill-for-skills/sum.md`
- 用户描述的已经是单一职责的简单功能 —— 不需要链式分解

## Workflow / Steps

### Step 1: 系统化任务分析
使用 **5W1H + C** 框架系统化解析用户描述的复杂任务，将分析结果记录在分析草稿中：

**1.1 Why（动机）**
- 用户最终要解决什么根本问题？
- 不做会有什么后果？衡量标准是什么？

**1.2 What（目标与产出）**
- 核心目标是什么？用一句话概括。
- 最终产出物是什么？（文件、数据、报告、通知等）
- 产出物的格式和质量标准是什么？

**1.3 Where（范围与边界）**
- 任务涉及的范围是什么？（哪些文件/系统/数据）
- 明确的不在范围的内容是什么？
- 输出文件应保存在哪个目录下？

**1.4 When（时效性）**
- 是否有时间要求？（一次性任务/定期执行/实时响应）
- 数据的新鲜度要求是什么？

**1.5 Who（用户与受众）**
- 谁是最终用户或受众？
- 他们对输出格式有什么偏好？

**1.6 How（已知方法与工具）**
- 用户已经知道要使用什么方法或工具？
- 已经有哪些现成的资源可用？（已有 Skill、已有脚本、已有数据）

**1.7 Constraints（约束条件）**
- **技术约束**：平台限制、可用工具、网络环境
- **数据约束**：数据量级（<100条 / 100-10000条 / >10000条）、格式、敏感级别
- **安全约束**：是否需要处理敏感信息？输出是否可以公开？
- **质量约束**：准确率要求、容错要求

**1.8 初步节点识别**
- 从用户描述中提取自然出现的流程节点
- 标记节点之间的关系（顺序、并行、循环、条件）
- 记录用户已明确说出的步骤和暗示存在的步骤

**1.9 完整性检查**
如果以上信息存在模糊或缺失（特别是 Why、What、Constraints），**先输出你的理解并向用户确认**，确认后再继续。确认内容应包含：

```
## 我对任务的理解

**核心目标**：...
**输入**：...
**输出**：...
**流程节点**：A → B → C → D
**关键约束**：...
**需要确认**：❓ 以下内容需要您补充确认——
1. 产出物格式是否有特定要求？...
2. 数据量级大约多少？...
3. ...
```

**1.10 隐含假设验证**
主动识别用户描述中隐含但未声明的假设，逐条检验其合理性：

```
## 隐含假设清单

### 假设 1：[描述]
- **来源**：用户说"X"但隐含假设了"Y"
- **风险**：如果这个假设不成立，会导致什么后果？
- **验证方式**：如何确认这个假设是真的？
- **结论**：✅ 合理｜⚠️ 需确认｜❌ 需修正
```

常见隐含假设类型：
- **工具可用性假设**：用户假设 markitdown/某个库已安装 → 验证：检查是否有安装检测机制
- **格式兼容性假设**：用户假设 A 格式可以直接转换为 B 格式 → 验证：是否存在信息丢失风险
- **性能假设**：用户假设"很快就能完成" → 验证：数据量级 × 处理速度 = 预估耗时
- **环境假设**：用户假设文件在某个路径 → 验证：路径是否存在？权限是否足够？
- **知识假设**：用户假设你了解某个领域术语 → 验证：该术语是否需要澄清？

**1.11 任务可行性预判**
在开始分解前，对整体任务做一次可行性快速评估：

```
## 可行性预判

### 工具可行性
- 任务需要的所有工具是否在 Claude Code 能力范围内？ ✅ ⚠️ ❌
- 如果涉及外部工具，是否有安装/配置指导？ ✅ ⚠️ ❌

### 数据可行性
- 输入数据量是否在合理处理范围内？ ✅ ⚠️ ❌
- 数据格式是否明确且可访问？ ✅ ⚠️ ❌

### 复杂度评估
- 预估需要多少个子 Skill？ [1-3] [4-6] [7+]
- 是否有明显的技术难点？ 说明：...
- 任务是否可在一轮会话中完成？ ✅ ⚠️ ❌
```

如果可行性评估出现 ❌，**在向用户输出的理解确认中包含风险警告**。

### Step 2: 任务分解
基于 Step 1 的分析结果，将复杂任务按功能边界拆分为多个子任务。每个子任务遵循 **单一职责原则**——只做一件事，并且做好。

**2.1 识别节点类型**
从 Step 1.8 的初步节点出发，使用四种节点类型标注每个候选子任务：

| 节点类型 | 特征 | 典型例子 |
|---------|------|---------|
| **转换** | 数据/文件从一种形态变为另一种形态 | docx→md, JSON→CSV, 非结构化→结构化 |
| **分析** | 需要理解、总结、判断、提取 | 内容总结、分类、质量审查、差异对比 |
| **生成** | 需要创作、撰写、组合、产出 | 写报告、生成图表、构造回复、组装模板 |
| **操作** | 读写文件、调用 API、执行命令、触发流程 | 下载文件、发送通知、清理缓存、备份 |

**2.2 选择分解模式**
根据任务特征选择合适的分解模式：

| 模式 | 适用场景 | 分解方式 |
|------|---------|---------|
| **管道分解** | 处理流程有明显的线性阶段 | 按处理阶段切分：A_raw → A_clean → A_analyzed → A_report |
| **扇出分解** | 同一输入需要多种不同处理 | 输入同时进入多个并行子任务：A → (B1, B2, B3) |
| **分层分解** | 任务包含不同抽象层次 | 底层操作 → 中层逻辑 → 上层策略 |
| **关注点分解** | 任务混合了不同领域知识 | 按知识领域拆分：数据部分 / 算法部分 / 展示部分 |
| **阶段分解** | 任务周期长、各阶段差异大 | 准备期 / 执行期 / 验证期 / 交付期 |

**2.3 分解启发式规则**

- **经验法则#1** — 每个子任务的 Workflow 不超过 5 步。如果需要超过 5 步，说明该子任务可能还可以进一步拆分。
- **经验法则#2** — 每个子任务的 description 应能在 1-2 句话内说清。如果说不清，说明粒度太大。
- **经验法则#3** — 如果两个子任务总是同时出现且顺序固定，考虑是否应合并。
- **经验法则#4** — 如果某个子任务需要多个不同领域的专业知识，考虑进一步拆分。
- **经验法则#5** — 输出物作为拆分的锚点：每个子任务应该产出 1 个明确的输出物。

**2.4 分解粒度检查**
完成初步分解后，逐条检查：

- [ ] 每个子任务是否只做一件事？（如果描述包含"和"字，可能需要拆分）
- [ ] 每个子任务是否有清晰的输入和输出？
- [ ] 子任务的总数是否在 2-8 个之间？
- [ ] 是否存在没有明确输出的子任务？（这类子任务往往是冗余的）
- [ ] 子任务之间的边界是否清晰，不会互相干扰？
- [ ] 是否每个子任务都能独立测试？

**停止条件判断：**
- **子任务数 < 2**：说明该任务实际上不需要链式分解 → **终止规划流程**，告知用户"此任务适合作为单个 Skill 实现，建议直接使用 `skill-for-skills` 创建"，输出简化报告后结束
- **子任务数 > 8**：说明分解粒度过细 → **返回 2.2 重新选择更粗粒度的分解模式**（如将管道分解改为分层分解），或建议用户分组分阶段实施
- **子任务数 2-8**：继续进入 Step 3

**2.5 输出——子任务清单（记录在分析草稿中）**
使用以下结构化的子任务模板。字段说明中的 `[类型]` 标记遵循统一类型系统：`text`=自由文本, `enum(A|B)`=枚举, `int`=整数, `bool`=true/false, `ref`=交叉引用。

```
### 子任务 1: {task-name}           // kebab-case, 如 doc-converter
- **类型**: [enum(转换|分析|生成|操作)] (required)
- **描述**: [text, max=200] (required) — 一句话描述该子任务做什么
- **输入**: [text] (required)
  - 来源: ref(用户|上游Skill名|文件系统)
  - 格式: [text] (required) — 如 .md, .json, .csv
- **输出**: [text] (required)
  - 产物: [text] (required) — 如 "转换后的markdown文件"
  - 路径: [path] (required) — 如 ./<skill-name>/output/
  - 格式: [text] (required)
- **上游依赖**: [ref(null|子任务名)] (required) — null=起始任务
- **下游影响**: [ref(子任务名)] (optional)
- **Tags**: [list<text>] (optional) — 如 ["文档处理", "格式转换"]

### 子任务 2: {task-name}
// ... 同上结构
```

**2.6 隐式耦合检测**
检查子任务之间是否存在"看不到却相互依赖"的隐式耦合：

```
## 隐式耦合检查清单

### 文件级耦合
- [ ] 是否有两个子任务读写了同一文件？（→ 存在竞态风险）
- [ ] 是否有子任务依赖特定文件名但该文件名未被契约约束？（→ 命名冲突风险）
- [ ] 是否有子任务修改了共享目录下的文件但不负责清理？（→ 残留文件风险）

### 环境级耦合
- [ ] 是否有子任务依赖特定的工作目录？（→ 路径假设风险）
- [ ] 是否有子任务依赖环境变量或配置文件？（→ 环境不一致风险）
- [ ] 是否有子任务依赖系统命令或 PATH？（→ 跨平台风险）

### 时序级耦合
- [ ] 是否有子任务假设某个文件在特定时间点已存在？（→ 时序风险）
- [ ] 是否有子任务假设其他子任务已完成特定操作？（→ 隐式顺序依赖）
- [ ] 并行执行的子任务是否可能互相干扰？（→ 并发风险）

### 语义级耦合
- [ ] 是否有两个子任务使用不同命名但指代同一概念？（→ 术语不一致风险）
- [ ] 是否有子任务假设了其他子任务内部的实现细节？（→ 封装破坏风险）
- [ ] 是否有子任务依赖的数据格式标准未在契约中明确定义？（→ 隐含格式假设）
```

发现耦合时：
- **文件级/环境级耦合** → 在 Step 3 契约中明确定义共享资源的访问协议
- **时序级耦合** → 在 Step 4 架构中明确串行化或加锁
- **语义级耦合** → 建立公共术语表，统一命名

**2.7 边界任务推断**
主动推断用户未提及但逻辑上必需的边界任务：

``` 
## 边界任务推断

### 初始化类任务
- 是否需要创建输出目录？谁负责创建？何时创建？
- 是否需要检查依赖是否已安装？谁负责检查？
- 是否需要下载原始数据？从哪里下载？

### 清理类任务
- 中间文件是否需要清理？何时清理？谁负责清理？
- 临时下载的文件是否需要删除？
- 失败时是否需要回滚已产生的中间结果？

### 验证类任务
- 每个子任务的输出是否需要格式验证？
- 链的最终结果是否需要整体验证？
- 是否需要对比预期输出和实际输出？

### 通知类任务
- 任务完成时是否需要通知用户？
- 任务失败时是否需要输出详细的错误报告？
- 长时间运行的任务是否需要进度通知？
```

**推断原则：** 如果某个边界任务对于链的正确运行是必需的，则将其作为独立子任务加入清单（返回 2.1 重新标记）。如果只是"锦上添花"的优化，则在 Step 4 架构设计的 Notes 中记录。

### Step 3: 定义 Skill 接口契约
在进入架构设计之前，先为每个子 Skill 定义清晰的接口契约。接口契约是 Skill 之间协作的合同，必须先于架构设计确定。

**3.1 定义输入契约**
对每个子任务，明确回答：

```
输入来源：
- 上游 Skill 名称：...
- 用户直接提供：...
- 从文件系统读取：...（路径格式）

输入格式：
- 文件格式：.md / .json / .csv / .txt / ...
- 数据结构：字段列表、类型、是否必填
- 数据量预期：<1KB / 1KB-1MB / >1MB

输入验证规则：
- 必填字段缺失时怎么办？
- 格式不正确时怎么办？
- 数据为空时怎么办？
```

**3.2 定义输出契约**
对每个子任务，明确回答：

```
输出物名称：...
输出格式：.md / .json / .csv / ...
保存路径：./<skill-name>/<分类目录>/<文件名>
关键字段：...
输出验证标准：
- 如何判断输出是正确的？
- 如何判断输出是完整的？
```

**3.3 定义错误契约**
每个子 Skill 必须定义以下三种情况的行为：

| 情况 | 行为要求 |
|------|---------|
| 输入不合法 | 记录错误信息后终止，向前端输出明确的错误信息 |
| 执行过程中异常 | 尽可能输出已处理的部分结果 + 错误信息 |
| 下游依赖不可用 | 重试 X 次（默认 3 次）后报错，给出替代建议 |

**3.4 契约一致性校验**

逐对检查上下游 Skill 的接口契约是否匹配：
- [ ] 上游的输出格式是否 = 下游的输入格式？
- [ ] 上游的输出字段是否覆盖下游的必填字段？
- [ ] 上游的命名约定是否与下游一致？
- [ ] 如果存在格式不匹配，是否需要添加一个转换 Skill？

**循环依赖检测：** 检查整个依赖图中是否存在 A → B → C → A 的循环。发现循环时：
1. 识别循环链中的各个 Skill
2. 检查是否有 Skill 可以合并以打破循环
3. 如果无法合并，返回 Step 2 重新审视分解方式，消除不必要的交叉依赖

**3.5 输出——接口契约文档（记录在分析草稿中）**
每个 Skill 的接口契约使用以下精确模板。扩展字段可通过 `x-` 前缀追加。

```
### Skill: {skill-name}              // ref: 子任务清单中的名称
- **schema_version**: "1.0"          // 接口契约版本号

- **input**:
  - source: [enum(upstream|user|filesystem)] (required)
  - upstream_skill: [ref(null|skill-name)] — 当 source=upstream 时必填
  - format: [enum(.md|.json|.csv|.txt|.yaml|.xml|binary)] (required)
  - encoding: [text] (optional, default="utf-8")
  - schema: [text] (optional) — 字段列表、类型、是否必填
  - validation_rules: [list<text>] (optional)
    - 空值: [text] — 数据为空时的行为
    - 格式错误: [text] — 格式不匹配时的行为
    - 字段缺失: [text] — 必填字段缺失时的行为

- **output**:
  - artifact: [text] (required) — 输出物名称，如 "清洗后的数据文件"
  - format: [enum(.md|.json|.csv|.txt|.yaml|.xml|binary)] (required)
  - path: [path] (required) — 如 ./<skill-name>/output/<file>.<ext>
  - fields: [list<text>] (optional) — 输出包含的关键字段列表
  - verification: [list<text>] (optional)
    - correctness: [text] — 如何判断输出是正确的（如 "抽样验证 JSON schema"）
    - completeness: [text] — 如何判断输出是完整的（如 "行数与输入一致"）

- **error_handling**: [object] (required)
  - on_invalid_input: [text] — 输入不合法时的行为
  - on_execution_error: [text] — 执行中异常时的行为
  - on_dependency_failure: [text] — 下游不可用时的行为（含重试次数和间隔）

- **stability**: [enum(stable|candidate|experimental)] (optional, default="stable")
  // stable=已固化, candidate=可能微调, experimental=可能大改
- **extensions**: [object] (optional) — 自定义扩展字段
```

**3.6 隐式状态传递检测**
识别契约中未明确定义但实际存在的状态传递路径：

```
## 隐式状态检测清单

### 文件系统状态
- [ ] 下游 Skill 是否假设输入文件在某个特定绝对路径？（→ 应在契约中显式定义路径）
- [ ] 下游 Skill 是否假设工作目录与上游相同？（→ 应在契约中约定工作目录）
- [ ] 下游 Skill 是否依赖上游在输出文件之外创建的任何文件？（→ 应显式加入契约）

### 环境状态
- [ ] 是否有子任务依赖之前步骤设置的环境变量？（→ 环境变量应记录在契约中）
- [ ] 是否有子任务依赖系统默认编码/时区/语言？
- [ ] 是否有子任务依赖特定的 Shell 状态（如$? 退出码）？

### 内存状态
- [ ] Skill 之间是否传递了文件名之外的任何隐式状态？（如"第一个文件的第 X 行"）
- [ ] 是否假设了"数据已排序""数据已去重"等未被契约保证的状态？

### 修复策略
发现隐式状态传递时：
- 如果是必需的依赖 → 显式加入契约（Step 3），作为输入字段
- 如果不是必需但存在风险 → 在契约中注明"注意：下游不应假设 XXX"
```

**3.7 静默降级识别**
检查接口契约中"看起来正常但实际异常"的场景——这是最难排查的问题来源：

```
## 静默降级检查表

### 内容层面
- 输出格式正确但内容为空 → 下游是否得到正确的空数据标记？
- 输出字段都存在但值异常（如全部为 null）→ 是否有字段级校验？
- 输出是一个合法文件但实际是错误提示（如"404 Not Found"写入 out.md）→ 输出是否实际可消费？

### 边界层面
- 上游输出 0 行数据 → 下游能否正确处理空数据集？
- 上游输出 1 行数据 → 下游算法是否需要至少 2 行才能运行？
- 上游输出超过 10000 行数据 → 下游是否有性能风险？

### 数据类型层面
- JSON 字段类型自动转换（如 "123" → 123）→ 下游是否期望字符串？
- 浮点数精度损失 → 下游是否需要精确值？
- 日期格式不一致 → 下游是否接受多种格式？
- 特殊字符/转义问题 → 下游能否正确处理包含引号、换行符的数据？

### 修复策略
每个识别出的静默降级风险应在契约中增加显式验证步骤：
"如果上游输出 X 条件，则输出明确的状态标记（如 status: empty_data），而不是让下游收到一个看似正常的空文件"
```

**3.8 接口版本兼容性标注**
预见未来接口变更的可能性，提前规划兼容策略：

```
## 接口兼容性标注

每个 Skill 的输出契约应标注：

### 稳定字段（Stable）
- 字段名、类型、语义在未来版本中保持不变的字段
- 下游可以安全依赖

### 候选字段（Candidate）
- 当前存在但未来可能调整的字段
- 下游应使用"防御性读取"（检查字段是否存在）

### 扩展字段（Extension）
- 预留给未来功能但当前可能为空的字段
- 下游应忽略空值
```

**兼容性原则：** 仅增加新字段，不修改或删除已有字段。如果必须修改，则提升接口版本号并在 usage-guide 中说明迁移方案。

### Step 4: 设计 Skill 链架构
基于子任务清单和接口契约，设计完整的 Skill 链架构。

**4.1 架构模式选择**
根据 Step 2.2 选择的分解模式和 Step 3 定义的接口契约，选择合适的架构模式：

| 模式 | 结构 | 适用场景 | 优点 | 缺点 |
|------|------|---------|------|------|
| **严格管道** | A → B → C → D | 处理流程严格线性、每步依赖上一步 | 简单清晰、易于推理 | 整体延迟 = 各步之和 |
| **扇出/扇入** | A → (B,C) → D | 同一输入需要多种独立处理后再合并 | 并行提升效率 | 需要合并步骤，增加复杂度 |
| **CQRS 分离** | 读链与写链独立 | 查询操作和写入操作差异大 | 读写互不影响 | 需要维护两条链 |
| **编排器模式** | Coordinator → (A,B,C) | 需要一个总控调度多个子 Skill | 集中控制、灵活调度 | 编排器自身较复杂 |
| **职责链** | A → B 或 A → C（条件分支） | 根据条件走不同路径 | 灵活应对多分支 | 分支条件需在契约中明确定义 |
| **发布-订阅** | A → 广播 → (B,C,D) | 同份输出供多个下游独立使用 | 松耦合 | 需要约定数据格式标准 |
| **分层架构** | 基础层 → 业务层 → 展现层 | 有明显抽象层次差异 | 关注点分离清晰 | 层级间调用开销 |
| **重试/补偿** | A → (失败→重试/补偿) → B | 关键步骤不能失败 | 高可用 | 补偿逻辑实现复杂 |

**选择原则：** 优先选择最简单的模式。管道模式是最安全的起点，仅在明确需要时才切换到复杂模式。

**4.2 设计执行顺序**
绘制 Skill 链执行顺序图：

```
# 严格串行（管道模式）
[Skill A] → [Skill B] → [Skill C] → [Skill D]

# 混行模式（扇出 + 管道）
         ┌→ [Skill B] ─┐
[Skill A] ┤             ├→ [Skill D] → [Skill E]
         └→ [Skill C] ─┘

# 条件分支
[Skill A] → 判断条件 ─┬→ [Skill B] ─┐
                      └→ [Skill C] ─┴→ [Skill D]
```

**4.3 定义数据流转**
明确每个环节的数据流转方式：

- **文件传递**：上游写入文件 → 下游读取文件。最简单可靠的方式。
  - 中间文件统一存放在 `./skill-chain-planner/plans/<task-name>/intermediate/` 下
  - 文件名格式：`<步骤号>-<Skill名>-<输出物名称>.md`
- **参数传递**：通过 `$ARGUMENTS` 或位置参数传递。适合简单数据和标记。
- **混合传递**：大块数据走文件，控制参数走命令行。最灵活的方式。

**4.4 识别复用与合并机会**

- **直接复用**：是否已有现成的 Skill 可以替代某个子任务？
- **调整后复用**：现有 Skill 是否需要小幅修改才能复用？→ 记录升级需求
- **合并建议**：是否有多个小 Skill 适合合并为一个？（参考经验法则#3）
- **拆分建议**：是否有 Skill 仍然太复杂需要进一步拆分？→ 回到 Step 2

**4.5 输出——架构设计文档（记录在分析草稿中）**
架构文档统一格式。通过 `notes` 字段承载扩展信息。

```
## Skill 链架构
- **schema_version**: "1.0"

### 架构模式
- **primary**: [enum(pipeline|fanout|layered|orchestrator|chain|cqrs|pubsub)] (required)
- **fallback**: [enum(...)] (optional) — 主模式不可用时的备选
- **rationale**: [text] (required) — 选择该模式的原因

### 执行顺序
- **type**: [enum(serial|parallel|hybrid|conditional)] (required)
- **flow_diagram**: [text] (required) — 文字版流程图
  ```
  // 示例严格串行
  [A:doc-converter] → [B:md-formatter] → [C:summarizer] → [D:report-writer]
  ```

### 数据流转表
| Step | Skill | Input Source | Output Path | Format | Protocol |
|------|-------|-------------|-------------|--------|----------|
| 1 | A | [ref] | [path] | [enum] | [enum(file|arg|mixed)] |
| 2 | B | [ref] | [path] | [enum] | [enum(file|arg|mixed)] |

### 复用决策
- **skills_existing**: [list<ref>] (optional) — 可复用的已有 Skill
- **skills_new**: [list<ref>] (required) — 需新建的 Skill
- **upgrade_needed**: [list<ref>] (optional) — 需升级的现有 Skill

### 架构质量属性
- **idempotency**: [enum(full|conditional|none)] (required)
- **observability**: [enum(full|partial|manual)] (required)
- **max_concurrency**: [int, min=1, max=16] (required) — 最大并行数
- **recovery_strategy**: [enum(restart|skip|fallback|compensate)] (required)

### extensions: [object] (optional)
  // 自定义扩展，如部署约束、环境需求等
```

**4.6 幂等性分析**
检查链中每个 Skill 被重复执行时的行为——这是链的健壮性基石：

```
## 幂等性评估

### 天然幂等（可安全重复执行）
- 读取操作不会产生副作用
- 覆盖式写入（每次写同一路径，覆盖上次结果）
- 纯转换操作（相同的输入 → 相同的输出）

### 需注意（重复执行可能产生不同结果）
- 追加式写入（每次执行在文件末尾追加内容 → 分次执行会产生重复数据）
- 调用外部 API（第二次执行时 API 返回可能不同）
- 时间戳/随机数生成（每次执行结果不同）
- 发送通知（每次执行都会发送一次通知，可能造成骚扰）

### 修复策略
- 追加式写入 → 改为覆盖式写入，或在契约中声明"每次执行从头开始"
- API 调用 → 缓存上游 API 响应以确保重用时一致性
- 通知类 Skill → 添加重放检测机制：检查是否已在本次会话中发送过
```

**4.7 可观测性设计**
确保链中各步骤的执行状态对用户是透明的——没有"黑盒":

```
## 可观测性检查清单

### 进度可见性
- 用户能否知道链的执行到了哪一步？（→ 每步应有唯一标识符，执行时输出）
- 长时间运行的步骤是否有进度指示？（→ 超过 30 秒的步骤应有中间进度输出）
- 并行步骤的执行顺序是否可理解？（→ 应标明并行组关系）

### 失败可见性
- 某步失败时，用户能否获得足够的信息定位原因？（→ 错误信息必须包含：步骤名、失败原因、输入来源引用）
- 失败时是否能区分"输入错误"、"系统错误"和"未知错误"？（→ 三类错误应有不同标识）

### 结果可见性
- 用户能否方便地查看每步的中间输出？（→ 中间文件路径应在报告中列出）
- 最终产出的来源是否可追溯？（→ 每个输出字段应可追溯到来源步骤）

### 日志标准
规划中定义统一的日志格式标准供各 Skill 使用：
```
[Step N/<SkillName>] 开始｜进度: X/Y｜成功｜失败(原因)
```
```

**4.8 资源竞争分析**
当链中包含并行执行的分支时，检查是否存在资源竞争隐患：

```
## 资源竞争检查

### 文件写入冲突
- [ ] 并行分支是否写入同一文件？（→ 竞态条件，必须串行化）
- [ ] 并行分支是否写入同一目录的同名文件？（→ 文件覆盖，必须使用唯一文件名）
- [ ] 并行分支是否读取一个正在被另一个分支写入的文件？（→ 脏读风险）

### 资源耗尽风险
- [ ] 并行执行的分支总数 × 单步内存需求是否接近内存上限？（→ 限制并行数）
- [ ] 是否有分支下载大文件的同时其他分支也在大量读写磁盘？（→ I/O 争用）
- [ ] 是否有分支使用独占资源（如不可重入的 API）？（→ 加锁或串行化）

### 修复策略
- 文件冲突 → 每个分支写入独立子目录，命名包含分支标识
- 资源耗尽 → 使用扇出控制（最大并行数 = min(CPU核数, 4)）
- 独占资源 → 改为串行访问或添加排队机制
```
### Step 5: 风险评估与容错设计
在架构设计完成后，系统性地评估风险并设计容错策略。

**5.1 单点故障识别**
逐链检查，识别可能使整个链中断的关键节点：

| 风险类型 | 检查问题 | 严重程度 |
|---------|---------|---------|
| 上游依赖 | 某个 Skill 是否唯一的数据来源？ | 高 |
| 外部依赖 | 是否依赖外部 API 或网络服务？ | 中-高 |
| 数据量风险 | 是否存在处理超大数据量的步骤？ | 中 |
| 格式风险 | 是否存在格式转换丢失信息的风险？ | 中 |
| 级联失败 | 某个 Skill 失败是否会导致后续所有步骤失败？ | 高 |

**5.2 容错策略设计**
对每个识别出的风险，设计应对策略：

```
## 风险登记表

### 风险 1：[名称]
- **场景**：...
- **概率**：高｜中｜低
- **影响**：严重｜中等｜轻微
- **应对策略**：
  - 降级方案：...
  - 重试策略：最多重试 3 次，间隔 5 秒
  - 替代路径：...
  - 告知用户：...
```

**5.3 关键节点防护**
对于单点故障风险高的节点（如"唯一的格式转换器"），设计以下保护措施：

- **输入快照**：在进入关键节点前备份原始输入
- **阶段性输出**：关键节点每完成一个子任务就输出中间结果
- **人工确认点**：在不可逆操作前设置暂停，等待用户确认
- **跳过选项**：如果某步骤不是必选的，提供跳过机制

**5.4 输出——风险登记表（记录在分析草稿中）**
结构化风险登记。每种风险包含完整的分类、评估和应对方案。`related_skill` 字段将风险关联到具体 Skill。

```
## 风险登记表
- **schema_version**: "1.0"

### 风险 1: {risk-name}              // kebab-case, 如 api-rate-limit
- **category**: [enum(dependency|data|format|cascade|resource|external|silent)] (required)
- **related_skill**: [ref(skill-name)] (required) — 风险出现在哪个 Skill
- **scenario**: [text] (required) — 风险的具体触发场景
- **probability**: [enum(high|medium|low)] (required) — 发生概率
- **impact**: [enum(severe|moderate|minor)] (required) — 影响程度
- **risk_score**: [enum(critical|high|medium|low)] (computed) — probability × impact

- **mitigation**:
  - fallback: [text] (optional) — 降级方案
  - retry: [text] (optional, default="3次, 间隔5s") — 重试策略
  - alternative: [text] (optional) — 替代路径
  - user_notification: [text] (optional) — 如何告知用户

- **cascade_analysis**: [text] (optional) — 连锁传播路径推演
  // 参考 Step 5.6 的连锁故障推演结果

- **extensions**: [object] (optional)
  // 自定义扩展字段
```

**5.5 静默错误分析**
识别那些"程序正常运行、退出码为 0、但结果错误"的场景——这是最难调试的问题类别：

```
## 静默错误场景推演

### 数据层静默错误
- **场景：** API 返回了 200 OK，但响应体是 {"error": "rate_limit"} 而不是正常数据
  → 检查：响应体内容是否与预期 schema 匹配，而非仅检查 HTTP 状态码
- **场景：** 转换后文件大小不为 0，但所有内容都是乱码或不相关的错误信息
  → 检查：输出内容是否包含可预期的标记（如 markdown 标题、JSON 结构关键字）
- **场景：** 数据被截断但没有收到截断通知
  → 检查：输出行数/大小是否与输入行数/大小对应

### 逻辑层静默错误
- **场景：** 日期"06/07/2025"被解释为 6月7日（月/日）而不是7月6日（日/月）
  → 检查：所有日期解析是否明确指定了格式，而非依赖系统默认
- **场景：** 正则匹配时由于编码问题遗漏了某些匹配项
  → 检查：是否对输入编码进行了统一转换
- **场景：** 去重操作误删了非重复项（如两行看起来相同但实际意义不同）
  → 检查：去重逻辑的键选择是否准确

### 工具层静默错误
- **场景：** markitdown 转换成功，但 mathjax/代码块/表格等复杂元素被遗漏
  → 检查：是否对关键内容类型做了抽样验证
- **场景：** 外部工具在非英文环境下输出不同格式的内容
  → 检查：工具运行时的 LOCALE/语言环境是否被固定

### 修复策略
每类静默错误应至少设置一道"检测门"：
1. 输出内容的结构化验证（格式是否正确）
2. 输出内容的语义化验证（内容是否合理）
3. 对可逆操作进行"往返校验"（A→B→A 是否能还原）
```

**5.6 连锁故障推演**
从链的起点开始，逐级推演故障传播路径：

```
## 连锁故障推演

### 推演方法
从链的起点开始，逐级问自己："如果这一步以最坏方式失败，对下游的影响是什么？"

### 推演模板
```
### 故障起点：[Step N] [Skill 名称]

故障模式：数据格式错误 | 超时 | 空输出 | 部分输出 | 错误输出

┌─ 直接影响：
│  • 下游 Step N+1 收到异常输入 → [具体表现]
│  
├─ 一级传播（直接影响下游）：
│  • [Step N+1]：[具体影响]
│  • [Step N+2]：[具体影响]（如果 N+1 将错误传递下去）
│  
├─ 二级传播（影响下游的下游）：
│  • ...
│  
└─ 最终影响：
   • 用户可以感知的最终后果是什么？
   • 是否可以通过"跳过某步"或"使用备份"来恢复？
```

### 常见连锁故障模式

| 起始故障 | 传播路径 | 最终后果 | 阻断方案 |
|---------|---------|---------|---------|
| A 输出空文件 | B 读取后处理产生空结果 → C 基于空结果 → 最终输出空报告 | 全链输出为空 | B 增加空输入检查，输出明确标记 |
| A 输出格式偏移 | B 解析到错误字段 → C 使用错误数据 → 最终输出错误 | 错误结果看似正常 | 每步增加格式校验，不通过则终止 |
| A 超时未完成 | B 等待 A → C 等待 B → 链超时 | 全链失败 | 每步设置独立超时，超时后走降级 |
| A 使用错误版本工具 | B 拿到不符合预期的数据 → C 进一步处理 → 最终输出混合了新旧格式 | 难以定位 | 工具版本信息应写入输出元数据 |
```
### Step 6: 为每个子 Skill 编写创建规格
对于 Step 2 中识别出的每个**需要新建**的子任务，编写一份完整的创建规格。这些规格将直接作为用户使用 `skill-for-skills` 时的输入参数。

**6.1 规格模板** — 这是整套模板的核心。每个子 Skill 的规格将直接作为 `skill-for-skills` 的输入参数。模板采用三层结构：**身份层** → **接口层** → **实现层**，每层职责分离，通过 `extensions` 提供扩展能力。

```
### Skill: {skill-name}              // kebab-case, 与目录名一致
- **spec_version**: "2.0"            // 规格格式版本号

// ════════════════════════════════════════════
// 第一层：身份层 — 标识 Skill 是什么
// ════════════════════════════════════════════

- **core_function**: [text, max=200] (required)
  // 一句话核心功能，将直接作为 SKILL.md 的 description
  // 示例: "使用 markitdown 将 docx/pdf 文件转换为 markdown 格式"

- **triggers**: [list<text>, min=3, max=8] (required)
  // 触发关键词，将直接作为 SKILL.md description 的 Triggered by 部分
  // 示例: ["文档转换", "转markdown", "docx转md", "pdf转md", "file conversion"]

- **category**: [enum(conversion|analysis|generation|operation)] (required)
  // 子任务类型，用于推断默认 allowed-tools

// ════════════════════════════════════════════
// 第二层：接口层 — Skill 的输入输出契约
// ════════════════════════════════════════════

- **input**:
  - source: [enum(upstream|user|filesystem)] (required)
  - upstream_skill: [ref(null|skill-name)] — source=upstream 时必填
  - format: [text] (required) — 如 ".docx/.pdf"
  - description: [text] (optional) — 人类可读的输入描述
  - validation: [text] (optional) — 输入验证规则

- **output**:
  - artifact: [text] (required) — 如 "转换后的 markdown 文件"
  - format: [text] (required) — 如 ".md, UTF-8"
  - path_pattern: [path] (required) — 如 ./{skill-name}/output/{filename}.md
  - fields: [list<text>] (optional) — 输出包含的字段列表
  - verification: [text] (optional) — 如何验证输出正确性

- **contract_refs**: [object] (optional)
  // 引用 Step 3 的接口契约（如有）
  - input_contract: [ref] — 输入契约 ID
  - output_contract: [ref] — 输出契约 ID
  - error_contract: [ref] — 错误契约 ID

// ════════════════════════════════════════════
// 第三层：实现层 — 如何创建这个 Skill
// ════════════════════════════════════════════

- **suggested_workflow**: [list<text>, min=1, max=8] (required)
  // 给 skill-for-skills 的 Workflow 步骤建议，每条以动词开头
  // 示例:
  //   1. "使用 Read 工具读取用户输入的 .docx 文件路径"
  //   2. "调用 markitdown 命令行工具将文件转为 .md 格式"
  //   3. "将转换结果写入 ./doc-converter/output/ 目录"

- **suggested_tools**: [list<enum(Read|Write|Edit|Bash|Glob|Grep|WebSearch|WebFetch)>] (required)
  // 按子任务类型推断：
  //   conversion → [Read, Write, Bash]
  //   analysis   → [Read, Write, WebSearch]
  //   generation → [Read, Write]
  //   operation  → [Read, Write, Bash, Glob]

- **dependencies**: [list<text>] (optional)
  // 外部依赖，如 ["markitdown (pip install markitdown)"]

- **priority**: [enum(P0|P1|P2)] (required)
  // P0=必须先创建, P1=建议第二步, P2=可最后创建
- **depends_on**: [list<ref(skill-name)>] (optional)
  // 必须先于本 Skill 创建的 Skill 列表

- **notes**: [text] (optional)
  // 边界情况、特殊配置、测试建议

// ════════════════════════════════════════════
// 扩展层 — 为不同场景预留扩展点
// ════════════════════════════════════════════

- **extensions**: [object] (optional)
  // 用于承载项目特定信息或未来新字段
  // 示例: { "deploy_env": "docker", "timeout_sec": 300 }
  // 注意: skill-for-skills 会忽略不识别的扩展字段，不会报错
```

**6.2 规格编写原则**
- **对 skill-for-skills 友好**：规格中的"核心功能"和"触发场景"应能直接作为 SKILL.md 的 description 使用
- **完整但不冗余**：每个规格独立可读，但相似的规格应指出共性而非重复全部内容
- **可测试**：每个规格应隐含可验证的标准——如何判断 Skill 工作正常
- **接口对齐**：规格中的输入输出必须与 Step 3 中定义的接口契约一致

**6.3 依赖顺序标注**
为每个规格标注创建优先级：

```
创建优先级：P0（必须先创建）｜P1（建议第二步）｜P2（可最后创建）
理由：...
依赖的其他 Skill：skill-A, skill-B（须先于本 Skill 创建）
```

**重要：** 如果多个子任务具有相似性（如同为"转换类"），不要重复编写相同的规格——应提取共性并说明差异点。

**6.4 规格自洽性检查**
从"规格阅读者"视角逐条检查规格的完整性和自洽性：

```
## 规格自洽性检查清单

### 完整性检查
- [ ] 规格是否包含"输入为空时怎么办"的说明？
- [ ] 规格是否包含"输出格式变化时如何通知下游"的说明？
- [ ] 规格中的每个输入字段，是否有对应的验证规则？
- [ ] 规格中提到的每个文件路径，是否有对应的创建步骤？

### 一致性检查
- [ ] 规格中的"核心功能"与"Workflow 建议"是否对齐？（后者应是前者的展开）
- [ ] 规格中的"输入格式"与"输出格式"是否匹配上下游契约？
- [ ] 规格中的"allowed-tools"是否与"Workflow 建议"中的操作匹配？
  - 如果 Workflow 包含 Bash 命令但 allowed-tools 没有 Bash → 不一致
  - 如果 Workflow 包含 WebSearch 但 allowed-tools 没有 → 不一致

### 可理解性检查
- [ ] 一个不熟悉这个链的人，仅读这个规格能否理解 Skill 的职责？
- [ ] 规格中的每个专业术语是否都有定义或上下文明示？
- [ ] 规格是否可以在不引用其他文档的情况下独立理解？
```

**6.5 可复用性标记**
标记每个子 Skill 的潜在复用价值——这有助于用户在将来构建其他链时快速定位可用 Skill：

```
## 可复用性评估

### Skill: <名称>

### 专用性评分（1-5，5=完全通用）
- [1-5] 这个 Skill 的功能是否与当前任务高度绑定？
  - 5 = 纯通用功能（如"文件格式转换"、"数据去重"）
  - 1 = 完全定制（如"XX 公司实验报告格式转换"）

### 可复用场景
- 这个 Skill 还能用在哪些其他任务中？
  - 例 "doc-converter" 可用于任何需要文档格式转换的场景
  - 例 "content-summarizer" 可用于任何需要文本摘要的场景

### 复用建议
- 如果评分 >= 3：建议将 Skill 存放在公用位置（如用户级 skills 目录）
- 如果评分 < 3：仅存放在当前项目的 .claude/skills/ 下即可
```

**6.6 歧义消除**
主动找出规格中可能产生多种解释的地方，并将其精确化：

```
## 歧义消除检查

### 常见歧义示例
| 模糊写法 | 可能的多种解释 | 精确写法 |
|---------|---------------|---------|
| "保存到 output 目录" | ./output/ 还是 ./skill-name/output/？ | "保存到 ./skill-name/output/report.md" |
| "处理大文件" | 多大算大？1MB 还是 1GB？ | "处理单个文件不大于 100MB 的数据" |
| "删除临时文件" | 删除多久之前的？全部还是特定后缀？ | "删除 ./temp/*.tmp 中创建时间超过 1 小时的文件" |
| "验证输出" | 格式验证还是内容验证？自动还是人工？ | "自动验证输出 JSON schema + 人工抽样验证内容准确性" |
| "向用户报告" | 以什么格式？在哪里报告？ | "在 Claude 会话中输出 Markdown 格式的报告" |

### 检查方法
对规格中的每个"宽泛动词"（处理、管理、操作、等方式、等操作）追问一次"具体如何做？"。
如果追问后无法给出明确的答案，说明该处存在歧义，需要精确化。
```
### Step 7: 生成 Skill 链规划报告
将以上所有分析结果整理为一份完整的规划报告，写入 `skill-chain-planner/plans/<task-name>/` 目录。**注意：在生成报告过程中，如果发现步骤之间存在逻辑断裂、接口不匹配或架构不合理，应回溯到对应 Step 进行修正后再继续生成。**

支持的反馈循环：
- 发现架构不合理 → 回溯 **Step 4** 重新设计
- 发现契约不匹配 → 回溯 **Step 3** 重新定义
- 发现遗漏子任务 → 回溯 **Step 2** 重新分解
- 发现任务理解偏差 → 回溯 **Step 1** 重新分析

```
plans/
└── <task-name>/
    ├── chain-overview.md        # 链架构总览
    ├── risk-register.md         # 风险登记表
    ├── skills/                   # 每个子 Skill 的创建规格
    │   ├── skill-P0-<name>.md
    │   ├── skill-P1-<name>.md
    │   └── ...
    ├── usage-guide.md            # 使用 skill-for-skills 创建与组合指南
    └── implementation-roadmap.md # 实施路线图
```

#### chain-overview.md 内容
文件元数据头 + 架构总览。采用 YAML 头 + Markdown 正文结构：

```markdown
---
plan_name: "{task-name}"
plan_version: "1.0.0"
generated_at: "{YYYY-MM-DD}"
schema_version: "1.0"
source: "skill-chain-planner v1.3"
extensions: {}
---

# {Task Name} — Skill 链架构总览

## 链路全景
- **子 Skill 总数**: [int] (required)
- **架构模式**: [enum(pipeline|fanout|layered|orchestrator|chain|cqrs|pubsub)]
- **执行顺序类型**: [enum(serial|parallel|hybrid|conditional)]
- **预估总工作量**: [text] (optional)

## 执行顺序图
```text
// 文字版架构图
[Skill A] → [Skill B] → [Skill C]
     ↘              ↗
  [Skill D] —— ———┘
```

## 依赖关系矩阵
| Skill | 类型 | 优先级 | 上游依赖 | 下游影响 | 状态 |
|-------|------|--------|---------|---------|------|
| {name} | {type} | P0/P1/P2 | {ref} | {ref} | {new/existing/upgrade} |

## 数据流转总览
| Step | Skill | 输入来源 | 输出路径 | 格式 | 协议 |
|------|-------|---------|---------|------|------|
| 1 | {name} | {ref} | {path} | {fmt} | file/arg/mixed |

## 接口契约概要
引用 Step 3 的关键契约，每个 Skill 列出：
- **输入**: 来源、格式、校验规则
- **输出**: 路径、格式、关键字段
- **错误处理**: 三类场景的处理方式

## 质量属性
- **幂等性**: full|conditional|none
- **可观测性**: full|partial|manual
- **最大并行数**: int
- **恢复策略**: restart|skip|fallback|compensate

## 扩展信息
```yaml
extensions:
  # 项目特定信息，如部署环境要求、性能基线等
```
```

#### risk-register.md 内容
结构化的风险登记表，每个风险记录独立。文件头 + 风险列表：

```markdown
---
plan_name: "{task-name}"
risk_count: {int}
generated_at: "{YYYY-MM-DD}"
schema_version: "1.0"
extensions: {}
---

# 风险登记表

## 风险汇总
| 严重度 | 数量 |
|--------|------|
| Critical | {int} |
| High | {int} |
| Medium | {int} |
| Low | {int} |

## 风险明细

### {risk-1}: {risk-name}
- **类别**: dependency|data|format|cascade|resource|external|silent
- **关联 Skill**: {skill-name}
- **场景**: {text}
- **概率**: high|medium|low
- **影响**: severe|moderate|minor
- **风险评分**: critical|high|medium|low
- **应对方案**:
  - 降级: {text}
  - 重试: {text}
  - 替代: {text}
  - 通知用户: {text}
- **连锁分析**: {text} (optional)
- **人工干预点**: {bool}

### {risk-2}: {risk-name}
// ...

## 扩展信息
```yaml
extensions: {}
```
```

#### skills/<优先级>-<名称>.md 内容
每份文件对应 Step 6 中编写的一份创建规格。文件名含优先级标记：`skill-P0-{name}.md`、`skill-P1-{name}.md`。

每份规格文件包含完整的 YAML 头 + 三层规格体：

```markdown
---
skill_name: "{skill-name}"
spec_version: "2.0"
priority: "P0|P1|P2"
depends_on: [{ref-list}]
generated_at: "{YYYY-MM-DD}"
extensions: {}
---

# {Skill Name}

## 身份层
- **core_function**: {text, max=200}
- **triggers**: [{list, min=3, max=8}]
- **category**: conversion|analysis|generation|operation

## 接口层
- **input**: {source, format, validation}
- **output**: {artifact, format, path, fields}
- **contract_refs**: {input, output, error}

## 实现层
- **suggested_workflow**: [{steps}]
- **suggested_tools**: [{tools}]
- **dependencies**: [{list}]
- **notes**: {text}

## 扩展信息
```yaml
extensions: {}
```
```

#### usage-guide.md 内容
用户实际操作指南。包含 YAML 元数据头，内容分创建、组合、验证、故障排除四部分：

```markdown
---
plan_name: "{task-name}"
guide_version: "1.0"
total_skills: {int}
creation_order: [{P0-list}] → [{P1-list}] → [{P2-list}]
generated_at: "{YYYY-MM-DD}"
extensions: {}
---

# 使用指南

## 创建步骤
按依赖顺序创建所有子 Skill：

### Phase 1: 核心链路 (P0)
| 顺序 | Skill | 规格文件 | 预估工作量 |
|------|-------|---------|-----------|
| 1 | {name} | skills/skill-P0-{name}.md | {text} |
| 2 | {name} | skills/skill-P0-{name}.md | {text} |

操作：打开 Claude Code → 输入 `/skill-for-skills` → 粘贴对应规格文件内容

### Phase 2: 增强功能 (P1)
| 顺序 | Skill | 规格文件 | 预估工作量 |
|------|-------|---------|-----------|
| 3 | {name} | skills/skill-P1-{name}.md | {text} |

### Phase 3: 优化完善 (P2)
...

## 组合使用
```
# 严格串行调用
/user {skill-A} <input>     # Step 1: 转换
/user {skill-B} <arg>       # Step 2: 处理（wait Step 1 done）
/user {skill-C} <arg>       # Step 3: 生成（wait Step 2 done）
```

## 验证方法
1. **单元测试** — 每个 Skill 单独测试，验证其输出符合契约格式
2. **集成测试** — 按链式顺序逐步串联 2-3 个 Skill 测试
3. **端到端测试** — 全链完整执行，验证最终产出

## 故障排除
| 症状 | 可能原因 | 解决步骤 |
|------|---------|---------|
| Skill 创建失败 | 输入格式不匹配 | 检查上游输出格式与当前 Skill 输入契约是否一致 |
| 输出不符合预期 | 依赖未安装 | 检查 dependencies 并安装 |
| 链中断 | 某步超时 | 参考 rollback-guide.md 恢复 |

## 扩展信息
```yaml
extensions: {}
```
```

#### implementation-roadmap.md 内容
分阶段实施路线图，含三阶段模板和里程碑标记：

```markdown
---
plan_name: "{task-name}"
roadmap_version: "1.0"
total_phases: 3
generated_at: "{YYYY-MM-DD}"
extensions: {}
---

# 实施路线图

## Phase 1: 核心链路 (P0) — [预估工作量: {text}]
**目标**: 核心流程可走通

| Skill | 类型 | 创建顺序 | 里程碑 |
|-------|------|---------|--------|
| {name} | {type} | 1st | ✅ P0 全部创建完成 |
| {name} | {type} | 2nd | ✅ 核心链路集成测试通过 |

**验证标准**:
- [ ] P0 所有 Skill 已创建
- [ ] 核心链路可完整执行
- [ ] 关键路径已覆盖端到端

## Phase 2: 增强功能 (P1) — [预估工作量: {text}]
**目标**: 完整流程可走通

| Skill | 类型 | 创建顺序 | 里程碑 |
|-------|------|---------|--------|
| {name} | {type} | 3rd | ✅ P1 全部创建完成 |

**验证标准**:
- [ ] 所有 P0+P1 Skill 已创建
- [ ] 完整链路可执行
- [ ] 异常路径已初步处理

## Phase 3: 优化完善 (P2) — [预估工作量: {text}]
**目标**: 异常路径得到覆盖

| Skill | 类型 | 创建顺序 | 里程碑 |
|-------|------|---------|--------|
| {name} | {type} | 4th | ✅ P2 全部创建完成 |

**验证标准**:
- [ ] 所有 Skill 已创建
- [ ] 回滚/降级方案已验证
- [ ] 风险登记表中的所有风险已覆盖

## 扩展信息
```yaml
extensions:
  custom_phases: []
```
```

#### rollback-guide.md 内容
结构化的回滚指南，按故障场景分类：

```markdown
---
plan_name: "{task-name}"
rollback_version: "1.0"
total_scenarios: 3
generated_at: "{YYYY-MM-DD}"
extensions: {}
---

# 回滚指南

## 场景 1: 单个 Skill 创建后不符合预期

### 诊断步骤
1. [text] — 检查该 Skill 的输入数据是否符合契约定义的格式
2. [text] — 检查该 Skill 的依赖是否全部安装
3. [text] — 检查上游 Skill 的输出是否已被更新（接口是否变更）

### 修复选项
| 选项 | 操作 | 适用条件 |
|------|------|---------|
| 升级 | 使用 `/skill-for-skills` 的升级功能修改 | 接口小幅变更 |
| 重建 | 删除后按规格重新创建 | 接口大幅变更 |
| 降级 | 从链中临时移除该 Skill | 非关键路径 |

## 场景 2: 链执行中某步失败

### 恢复步骤
1. **定位**：从错误信息中获取失败的 Step 编号和 Skill 名称
2. **快照**：从 `intermediate/` 目录获取失败步骤的输入快照
3. **修复**：修正输入数据或配置
4. **重试**：从失败步骤重新执行，无需从头开始

### 注意事项
- 确保修复后的输入与失败步骤的输入契约完全一致
- 如果失败步骤修改了共享文件，检查是否需要重置

## 场景 3: 全链结果不符合需求

### 根因分析
- [ ] 回顾 Step 1 的 5W1H+C 分析记录
- [ ] 检查 Step 5 风险登记表中的预警项是否被触发
- [ ] 验证 Step 8.4 假设清单中的假设是否成立

### 重规划流程
1. 保留 `intermediate/` 目录中的所有中间数据
2. 调整本规划文档中的对应规格
3. 重新使用 `/skill-for-skills` 生成修改后的 Skill
4. 复用未修改的中间数据，减少重复工作

## 扩展信息
```yaml
extensions:
  custom_scenarios: []
```
```

### Step 8: 输出规划总结
向用户输出完整的规划摘要，涵盖链路全景、实施建议和注意事项。

**8.1 链路全景**
输出给用户的完整规划摘要，作为 Claude 会话中的最终总结。使用 YAML 头 + 结构化 Markdown：

```markdown
---
plan_name: "{task-name}"
plan_path: "skill-chain-planner/plans/{task-name}/"
total_skills: {int}
architecture: "{pattern}"
risk_count: {int}
assumptions_identified: {int}
spec_version: "2.0"
extensions: {}
---

## Skill 链规划完成

### 链路全景
共设计 {int} 个子 Skill，采用 {enum(pipeline|fanout|layered|...)} 架构。
执行顺序: {enum(serial|parallel|hybrid|conditional)}

| Step | Skill | Category | Priority | Depends On |
|------|-------|----------|----------|------------|
| 1 | {name} | {type} | P0 | — |
| 2 | {name} | {type} | P0 | {skill} |
| 3 | {name} | {type} | P1 | {skill} |

### 关键指标
- **架构模式**: {pattern}
- **幂等性**: {full|conditional|none}
- **最大并行数**: {int}
- **最高风险**: {critical|high|medium|low}

### 创建顺序
Phase 1 (P0): [{list}] → Phase 2 (P1): [{list}] → Phase 3 (P2): [{list}]

### 风险预警
引用 risk-register.md 中的 top-3 高风险项。
```

**8.2 实施建议**

- **第一个创建的 Skill**：...（P0 中无上游依赖的起始 Skill）
- **建议的实施顺序**：阶段 1（核心链路）→ 阶段 2（增强）→ 阶段 3（优化）
- **预估总工作量**：...
- **风险预警**：引用 risk-register.md 中需要关注的高风险项

**8.3 下一步操作**

```
📋 您的下一步操作：
1. 打开 Claude Code
2. 输入 `/skill-for-skills`，粘贴 skills/skill-P0-<名称>.md 的内容
3. 创建第一个 Skill
4. 测试无误后，按 usage-guide.md 创建后续 Skill
```

**8.4 假设验证清单**
列出本规划中所有未经验证的关键假设，附带验证方法和失效预案。这是用户开始实施前应逐条确认的检查表：

```
---
total_assumptions: {int}
verification_required: true
extensions: {}
---

## 假设验证清单

### 🏗️ 环境假设
| # | 假设 | 验证方法 | 失效影响 | 严重度 |
|---|------|---------|---------|--------|
| 1 | 用户已安装所有外部依赖 | 运行 `pip list \| grep <pkg>` 或 `which <cmd>` | Skill 创建失败 | high |
| 2 | 文件系统权限充足 | 尝试 `touch <path>/test.tmp` | 写入失败 | high |
| 3 | 工具在当前 OS 上可用 | 查看工具文档确认 OS 兼容性列表 | 指令执行异常 | medium |

### 📊 数据假设
| # | 假设 | 验证方法 | 失效影响 | 严重度 |
|---|------|---------|---------|--------|
| 1 | 输入格式与规格完全匹配 | 抽样检查 3-5 个输入文件的格式 | 解析错误 | critical |
| 2 | 数据量级在预估范围内 | 运行 `wc -l` / `ls -lh` 检查 | 性能超预期 / OOM | medium |
| 3 | 无特殊字符/编码问题 | 使用 `file -i` 检查编码 | 处理结果异常 | medium |

### 🔗 接口假设
| # | 假设 | 验证方法 | 失效影响 | 严重度 |
|---|------|---------|---------|--------|
| 1 | 接口契约覆盖所有交换场景 | 逐对检查上下游契约字段 | 数据丢失 | critical |
| 2 | 格式直连无需人工转换 | 执行一次上下游直连测试 | 链中断 | high |

### ⚡ 性能假设
| # | 假设 | 验证方法 | 失效影响 | 严重度 |
|---|------|---------|---------|--------|
| 1 | 处理时间在可接受范围内 | 使用单步时间×步骤数估算 | 用户等待超时 | low |
| 2 | 临时磁盘空间充足 | `df -h` 检查可用空间 | 写入失败 | medium |

### 🔄 假设失效处理
如果上述任何假设不成立：
1. **评估影响范围** — 明确哪些步骤和 Skill 会受到影响
2. **回溯修正** — 回到对应的 Step 调整规划（参考 Step 7 反馈循环）
3. **更新风险登记表** — 将新发现的风险追加到 risk-register.md
4. **通知用户** — 在摘要中标注假设失效的后果和修正方案
```

**8.5 边界提示**
- 如果规划中的某个子 Skill 在实际创建时发现不需要，可以直接跳过，不影响链的整体运行
- 如果某个子 Skill 的输出格式与预期不符，回到本规划文档调整对应规格后再使用 `skill-for-skills` 重新生成
- 对于特别复杂的子 Skill（Step 2 经验法则#1 检测到的问题），可以在创建时进一步拆分为子链
- 回滚方案请参考 `rollback-guide.md`

## Constraints
- **Always** 遵循 Step 1 的 5W1H+C 框架进行系统性任务分析，不跳步
- **Always** 在 5W1H+C 完成后执行隐含假设验证（Step 1.10）和可行性预判（Step 1.11），确认任务可行且假设合理后再进入分解
- **Always** 遵循单一职责原则分解子任务，每个子 Skill 只做一件事
- **Always** 在分解完成后检查隐式耦合（Step 2.6）和推断必要的边界任务（Step 2.7）
- **Always** 为每个子 Skill 定义清晰的输入/输出/错误接口契约（Step 3）
- **Always** 在契约中识别隐式状态传递（Step 3.6）和静默降级场景（Step 3.7），将它们显式化
- **Always** 先进行接口一致性校验（Step 3.4）和循环依赖检测，再进入架构设计
- **Always** 在架构中分析幂等性（Step 4.6）、设计可观测性（Step 4.7）、排查资源竞争（Step 4.8）
- **Always** 进行风险评估（Step 5）并记录风险登记表
- **Always** 在风险评估中额外分析静默错误场景（Step 5.5）和连锁故障传播路径（Step 5.6）
- **Always** 为每个子 Skill 提供完整的 `skill-for-skills` 输入模板
- **Always** 检查规格的自洽性（Step 6.4）、可复用性（Step 6.5）和歧义（Step 6.6）
- **Always** 将规划报告输出到 `skill-chain-planner/plans/<task-name>/` 目录
- **Always** 在报告中说明子 Skill 之间的依赖关系、数据流转方式和回滚方案
- **Always** 在输出规划总结时附带假设验证清单（Step 8.4），让用户逐条确认
- **Always** 先理解确认再分解——用户描述模糊时先输出理解并确认（Step 1.9）
- **Always** 在输出规划报告后，明确告知用户下一步应执行的操作
- **Never** 直接生成 Skill 文件——只输出规划文档
- **Never** 修改项目中的任何已有文件
- **Never** 跳过数据流转设计——只列 Skill 清单而不说明连接方式会导致规划不可执行
- **Never** 设计过于笼统的子 Skill（如"数据处理"）——每个子 Skill 必须有具体的动词描述
- **Never** 在用户描述模糊时直接进入分解——必须先确认理解
- **Never** 设计超过 2 层的嵌套架构——过于复杂的架构意味着分解不充分
- **Never** 跳过推理验证层——每个 Step 之后的隐含推理步骤（1.10/1.11/2.6/2.7/3.6/3.7/4.6/4.7/4.8/5.5/5.6/6.4/6.5/6.6）必须在对应的主步骤完成后执行，不可跳过或合并
- 详细信息应放在 `references/` 子目录中

## Examples

### ✅ Do This（正确做法）

**用户输入：**
```
我想创建一个实验报告自动生成的工作流。先要把各种格式的文档（docx/pdf）用 markitdown 转成 markdown，
但转换后的 markdown 很乱，需要整理成统一的模板格式。然后需要总结项目的核心内容，
最后基于模板和总结撰写实验报告。
```

**完整输出：**

```
## Skill 链规划完成

**任务名称**：实验报告自动生成
**规划路径**：skill-chain-planner/plans/experiment-report/

### 链路全景
共设计 4 个子 Skill，采用严格管道架构。

| 步骤 | Skill | 类型 | 优先级 | 创建依赖 |
|------|-------|------|--------|---------|
| 1 | doc-converter | 转换 | P0 | 无 |
| 2 | md-formatter | 转换 | P0 | doc-converter |
| 3 | content-summarizer | 分析 | P1 | md-formatter |
| 4 | report-writer | 生成 | P1 | content-summarizer |

执行顺序：doc-converter → md-formatter → content-summarizer → report-writer

### 风险评估
| 风险 | 概率 | 影响 | 应对策略 |
|------|------|------|---------|
| markitdown 未安装 | 中 | 高 | 在 doc-converter 中自动检测并提示安装命令 |
| 转换乱码 | 中 | 中 | md-formatter 中设置格式校验，检测到异常时报警 |
| 大文件处理超时 | 低 | 中 | 建议先分割再处理 |

### 实施路线图
- **阶段 1（P0）**：doc-converter + md-formatter（核心转换链路）
- **阶段 2（P1）**：content-summarizer + report-writer（分析生成链路）

规划已保存到 skill-chain-planner/plans/experiment-report/

📋 下一步：打开 Claude Code → 输入`/skill-for-skills` → 粘贴 skills/skill-P0-doc-converter.md 的内容
```

**报告中的接口契约示例（使用新版类型化模板 — skills/skill-P0-doc-converter.md）：**
```markdown
---
skill_name: "doc-converter"
spec_version: "2.0"
priority: "P0"
depends_on: []
generated_at: "{YYYY-MM-DD}"
extensions: {}
---

# Doc Converter

## 身份层
- **core_function**: "使用 markitdown 将 docx/pdf 文件转换为 markdown 格式"
- **triggers**: ["文档转换", "转markdown", "docx转md", "pdf转md", "file conversion"]
- **category**: conversion

## 接口层
- **input**:
  - source: user
  - format: ".docx / .pdf（文件存在且可读）"
  - validation: "格式不支持时提示支持格式列表"
- **output**:
  - artifact: "转换后的 markdown 文件"
  - format: ".md (UTF-8)"
  - path_pattern: "./doc-converter/output/{filename}.md"
- **contract_refs**:
  - error: "markitdown 缺失时提供安装命令; 大文件超时警告"

## 实现层
- **suggested_workflow**:
  1. "使用 Read 确认输入文件路径和格式"
  2. "调用 markitdown 命令行: `markitdown <input> > <output>`"
  3. "验证输出 .md 文件不为空且包含预期内容"
  4. "将文件写入 ./doc-converter/output/ 目录"
- **suggested_tools**: [Read, Write, Bash]
- **dependencies**: ["markitdown (pip install markitdown)"]
- **notes**: "大文件(>10MB)转换可能需要较长时间，建议先分割再处理"

## 扩展信息
```yaml
extensions: {}
```
```

### ❌ Not This（错误做法）

**用户输入：**
```
我想创建一个实验报告生成 tool
```

**错误回应 — 直接进入分解而不理解：**
```
你需要的 Skill 链：
1. conversion-skill — 转换
2. formatting-skill — 格式化  
3. summary-skill — 总结
4. report-skill — 写报告
```

**问题：**
- ❌ 没有输出规划报告到文件
- ❌ 没有说明 Skill 之间的数据流转方式
- ❌ 没有提供 `skill-for-skills` 输入模板
- ❌ 子 Skill 名称过于笼统（conversion-skill、formatting-skill）
- ❌ 没有说明依赖关系
- ❌ 没有给出使用 `skill-for-skills` 的步骤
- ❌ 没有对用户模糊的描述进行确认

## Notes
- 本 Skill 只产生规划报告，定位在 `skill-chain-planner/plans/<task-name>/` 下
- 用户拿到规划报告后，需按依赖顺序依次使用 `skill-for-skills` 创建各子 Skill
- 创建完成后，用户按照 `usage-guide.md` 中的说明组合调用各 Skill
- 如果用户对某个子 Skill 的规格不满意，可以调整对应规格文件后重新交给 `skill-for-skills`
- 对于复杂的链式任务（超过 5 个子 Skill），建议分阶段实施，先创建核心链再补充辅助 Skill
- 本 Skill 不依赖任何外部工具或 API
