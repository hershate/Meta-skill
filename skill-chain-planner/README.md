# Skill Chain Planner

## 简介
将复杂任务拆解为多 Skill 协作链的规划工具。分析用户描述的多步骤任务，将其分解为多个单一职责的子 Skill，设计数据流转与执行顺序，并指导用户如何使用 `skill-for-skills` 逐个创建并组合这些 Skill。

本 Skill **不直接生成 Skill 文件**，它只输出规划文档。

## 目录结构
```
skill-chain-planner/
├── SKILL.md            # 技能主文件
├── README.md           # 本文件
├── plans/              # 规划报告输出目录（运行时自动生成）
│   └── <task-name>/    # 每次规划生成一个子目录
│       ├── chain-overview.md         # 链架构总览
│       ├── risk-register.md          # 风险登记表
│       ├── skills/                   # 子 Skill 创建规格
│       │   ├── skill-P0-<name>.md
│       │   ├── skill-P1-<name>.md
│       │   └── ...
│       ├── usage-guide.md            # 创建与组合使用指南
│       ├── implementation-roadmap.md # 实施路线图
│       └── rollback-guide.md         # 回滚指南
├── references/         # 补充文档（预留）
├── scripts/            # 可执行脚本（预留）
└── templates/          # 模板文件（预留）
```

## 安装方式
1. 将 `skill-chain-planner/` 目录复制到项目 `.claude/skills/skill-chain-planner/` 下
2. 重新启动 Claude Code
3. 使用 `/skill-chain-planner` 或触发关键词激活

## 使用方式

### 斜杠命令
`/skill-chain-planner <描述复杂任务>` — 输入你要分解的复杂任务，自动生成 Skill 链规划

### 自动触发
当用户输入以下关键词时自动激活：
- "任务分解"
- "skill链规划" / "skill chain"
- "复杂任务拆分"
- "多skill协作" / "多步骤任务"
- "工作流拆分"
- "skill pipeline"

### 使用流程
1. **描述你的复杂任务** — 详细说明你要完成的工作，包括输入、输出、中间步骤
2. **获得 Skill 链规划** — Claude 会输出一份完整的规划报告到 `plans/<task-name>/` 目录
3. **使用 `skill-for-skills` 创建各子 Skill** — 按规划中的 `usage-guide.md` 指引，逐个创建
4. **组合使用** — 所有子 Skill 创建完成后，按规划中的执行顺序组合调用

## Workflow 说明
系统化任务分析（5W1H+C + 隐含假设验证 + 可行性预判）→ 任务分解（模式选择 + 粒度检查 + 隐式耦合检测 + 边界任务推断）→ 定义接口契约（输入/输出/错误契约 + 隐式状态传递检测 + 静默降级识别）→ 架构设计（模式库 + 幂等性 + 可观测性 + 资源竞争分析）→ 风险评估（风险登记表 + 静默错误分析 + 连锁故障推演）→ 编写创建规格（自洽性检查 + 可复用性标记 + 歧义消除）→ 生成规划报告（含回滚指南）→ 输出规划总结（含假设验证清单）

每个主步骤后紧跟推理验证层，形成"执行 → 验证 → 推断"的双层结构。

## 技术细节

### 运行模式
本 Skill 使用 `context: fork` + `agent: Plan` 在隔离子 Agent 中运行，确保复杂的规划分析工作不污染主会话上下文。

### 依赖
无外部依赖，仅需 Claude Code 内置工具。

### 使用的工具
- `Read` — 读取用户输入和现有文件
- `Write` — 写入规划报告文件
- `Glob` — 检查目录结构
- `WebSearch` — 在必要时核实外部工具/API 信息（可选）

### 模板体系（spec v2.0）
所有输出文件采用统一的**三层模板架构**：
- **身份层** — Skill 名称、触发词、分类（给 `skill-for-skills` 的元数据）
- **接口层** — 类型化输入/输出契约（含 `source`, `format`, `validation`, `verification` 等类型化字段）
- **实现层** — Workflow 步骤、工具集、依赖、优先级（给 `skill-for-skills` 的指令）

**扩展机制**：每个模板预留 `extensions` 字段，用于项目特定信息或未来字段扩展，`skill-for-skills` 会忽略不识别的扩展字段。

### 输出文件
所有文件含 YAML 元数据头（`schema_version`, `generated_at`, `extensions` 等），正文使用类型化字段标记 `[type] (required|optional)`。

- `chain-overview.md` — 链架构总览，含依赖矩阵、数据流转表、质量属性
- `risk-register.md` — 结构化风险登记表，含风险评分、连锁分析、人工干预标记
- `skills/` 目录 — 每个子 Skill 的三层规格文件（`skill-P0-{name}.md` / `skill-P1-{name}.md`）
- `usage-guide.md` — 创建/组合/验证/故障排除四部分指南
- `implementation-roadmap.md` — 三阶段实施路线图（含里程碑和验证标准）
- `rollback-guide.md` — 三类故障场景的结构化恢复指南

## 完整工作流示例

### 8 步工作流总览（含推理验证层）

| 步骤 | 主操作 | 推理验证层 | 核心产出 |
|------|-------|-----------|---------|
| Step 1 | 系统化任务分析（5W1H+C） | 隐含假设验证 + 可行性预判 | 分析记录 + 假设清单 |
| Step 2 | 任务分解 | 隐式耦合检测 + 边界任务推断 | 子任务清单 + 耦合报告 |
| Step 3 | 定义接口契约 | 隐式状态检测 + 静默降级识别 | 契约文档 + 兼容性标注 |
| Step 4 | 设计链架构 | 幂等性分析 + 可观测性 + 资源竞争 | 架构图 + 质量属性 |
| Step 5 | 风险评估 | 静默错误分析 + 连锁故障推演 | 风险登记表 + 故障树 |
| Step 6 | 编写创建规格 | 自洽性检查 + 可复用性 + 歧义消除 | 规格文件 + 评估报告 |
| Step 7 | 生成规划报告 | 回滚路径设计 | 完整文件集 + rollback-guide |
| Step 8 | 输出规划总结 | 假设验证清单 | 全景 + 实施建议 + 验证表 |

### 典型应用场景

#### 实验报告自动生成
```
docx/pdf → 转markdown → 模板格式化 → 内容总结 → 报告撰写
```
4 个子 Skill：`doc-converter` → `md-formatter` → `content-summarizer` → `report-writer`
- 架构模式：严格管道
- 关键风险：markitdown 依赖、格式兼容性

#### 数据分析流水线
```
原始数据 → 清洗转换 → 统计分析 → 可视化 → 报告生成
```
4 个子 Skill：`data-cleaner` → `data-analyzer` → `chart-generator` → `insight-reporter`
- 架构模式：扇出（统计 + 可视化可并行）
- 关键风险：数据量级、图表库兼容性

#### 代码审查与文档生成
```
PR代码 → 代码审查 → 问题分类 → 文档生成 → 通知发送
```
4 个子 Skill：`code-reviewer` → `issue-classifier` → `doc-generator` → `notification-sender`
- 架构模式：管道 + 扇出（doc-generator 和 notification-sender 可并行）
- 关键风险：代码仓库权限、通知渠道可用性

## 注意事项
- 本 Skill 只产生规划，不创建任何子 Skill
- 所有子 Skill 的创建需要用户手动使用 `skill-for-skills` 完成
- 规划报告中的创建规格是建议性质，用户可以根据实际情况调整
- 如果子 Skill 超过 5 个，建议分阶段实施（参考 implementation-roadmap.md）
- 创建子 Skill 时请按 P0 → P1 → P2 的优先级顺序
- 每个 Skill 生成后建议先单独测试再串联使用
- 参考 risk-register.md 中的风险应对策略
- 本 Skill 采用"执行 → 验证 → 推断"双层结构：每个主步骤后跟推理验证层，确保每一步的产出都经过逻辑检验
- 报告中的 `rollback-guide.md` 提供了常见失败场景的恢复步骤，建议在实施前阅读
- 开始实施前，请逐条确认 `假设验证清单`（规划总结的 8.4 节）中的假设是否成立
