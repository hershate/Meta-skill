# Project to Skill

## 简介

自动分析工作目录下的任何项目，深入理解其组成结构、运行原理、数据流方向和工作步骤，然后将其完整转化为可复用的 Claude Code Skill。如果项目不适合 Skill 化（如纯文档仓库、硬件依赖项目、游戏等），会明确告知用户原因并终止转换。

本 Skill 填补了从"代码分析"到"Skill 生成"之间的鸿沟：
- **codebase-analyzer** 负责深度分析并生成报告，但不创建 Skill
- **deepwiki-ai-agent** 负责生成 Wiki 文档，也不创建 Skill
- **本 Skill 直接输出可注册使用的 `SKILL.md` + `README.md`**

## 目录结构

```
project-to-skill/
├── SKILL.md                        # 技能主文件（完整工作流和指令）
├── README.md                       # 本文件（用户文档）
├── references/
│   └── step-precision-rules.md     # 步骤精度参考手册（动词对照、自测卡、验证单）
├── scripts/                        # 可执行脚本（预留）
└── templates/                      # 模板文件（预留）
```

## 安装方式

1. 将 `project-to-skill/` 目录复制到项目的 `.claude/skills/` 下：

   ```bash
   cp -r project-to-skill /path/to/your/project/.claude/skills/
   ```

2. 重新启动 Claude Code
3. 使用 `/project-to-skill` 或触发关键词激活

> 也可放置在用户级目录 `~/.claude/skills/` 下使其对所有项目可用。

## 使用方式

### 斜杠命令

| 命令 | 说明 |
|------|------|
| `/project-to-skill` | 分析当前工作目录下的项目并转为 Skill |
| `/project-to-skill <路径>` | 分析指定路径下的项目并转为 Skill |

### 自动触发

当用户输入以下关键词时自动激活：
- 项目转 skill、项目转技能、从项目创建 skill
- 从代码生成 skill、根据项目生成 skill、代码转技能
- 仓库生成 skill、项目自动生成 skill、项目转化为技能
- 仓库转化为 skill、project to skill、convert project to skill
- codebase to skill、repo to skill

## Workflow 说明

本 Skill 在隔离子 Agent 中运行，执行流程分为五个阶段共 12 个步骤：

1. **项目发现与适用性评估**（Step 1-3）→ 扫描目标项目、建立画像，从 6 个维度评估是否适合 Skill 化。不适合则终止并告知原因
2. **深度理解**（Step 4-6）→ 分析架构和结构、提取工作流与数据流（含**循环/重试/错误恢复过程式检测**）、将代码逻辑抽象为语义步骤（功能降维），同时提取**参数映射表**和**边界条件**。对于含循环/重试的代码强制使用**过程式忠实模式**
3. **Skill 蓝图设计**（Step 7）→ 设计 Skill 名称、触发词、工具权限、Workflow 步骤（**五要素格式：输入/处理/输出/异常/衔接**）、约束条件
4. **Skill 生成**（Step 8-9）→ 在项目根目录下生成 `SKILL.md` 和 `README.md`，强制检查动词/名词规范和信息密度
5. **验证与交付**（Step 10-11）→ 自我审查生成的 Skill + **精度交叉验证**（对照源代码逐条核对参数完整性和分支覆盖）+ 输出交付报告

## 技术细节

### 核心机制：适用性评估

本 Skill 最关键的创新点是在转换前进行**6 维度系统评估**：

| 维度 | 评估内容 | 不通过的后果 |
|------|---------|------------|
| 功能完整性 | 项目是否有可执行的代码逻辑 | ❌ 终止 |
| 环境独立性 | 是否依赖特定硬件/OS | ❌ 终止 |
| AI 可执行性 | 功能能否用 Claude 工具完成 | ❌ 终止 |
| 输入输出明确性 | 是否有清晰的功能边界 | ⚠️ 警告 |
| 封装价值 | 封装为 Skill 是否比直接运行更好 | ⚠️ 警告 |
| 规模可控性 | 功能是否能在上下文窗口内表达 | ⚠️ 警告 |

### 核心机制：功能降维提取

将代码从"实现细节"抽象为"Skill 语义步骤"是关键转化步骤。但**抽象不等于简化**——本 Skill v2.1.0 升级新增了**过程式忠实保证**，当项目包含循环/重试/错误恢复时强制使用忠实模式。当前精度保障体系：

**1. 精度保留提取（Step 6）**：提取时强制保留 L1（功能摘要）+ L2（步骤参数）+ L3（异常路径）三层信息，禁止遗漏参数名/类型/默认值/边界条件。

**2. 五要素步骤模板（Step 7d）**：每个生成的 Workflow 步骤强制包含 **输入**、**处理过程**、**输出**、**异常处理**、**步骤衔接** 五个部分，任何少于五要素的步骤视为不完整。

**3. 精度交叉验证（Step 10b）**：生成后对照源代码进行三点验证——参数完整性核对、分支覆盖核对、幻觉检测。任一标准不通过则回退修正。

示例——从代码到精度步骤的完整转化：
```markdown
# 源代码片段（aggregator.py:20-55）
def aggregate(data, group_col="category", agg_col="value", agg_func="sum"):
    if not data:
        return {}
    # ...

# 精度步骤（完整保留参数信息）
### Step 3: 按分组列聚合数据
**输入**：data(list[dict]), group_col(str,默认"category"), agg_col(str,默认"value"), agg_func(str,默认"sum",可选值:sum/avg/count/min/max)
**处理过程**：按 group_col 分组 → 对每组的 agg_col 应用 agg_func → 空数据返回 {}
**输出**：aggregated(dict[str,float]) → 传递给 Step 4
**异常处理**：无效 agg_func → 报错列出可选值；列名不存在 → 报错列出可用列
**步骤衔接**：传递到 Step 4 输出 JSON
```

### 使用的工具

| 工具 | 用途 |
|------|------|
| `Read` | 读取项目源代码和配置文件 |
| `Write` | 写入生成的 SKILL.md 和 README.md |
| `Edit` | 修正验证中发现的问题 |
| `Grep` | 搜索代码中的函数定义、导入关系、错误处理 |
| `Glob` | 文件发现和目录树构建 |
| `Bash` | 目录列表、Git 日志、文件统计 |
| `WebSearch` | 核验外部 API 和第三方服务的当前状态 |
| `WebFetch` | 获取外部 API 文档辅助 Skill 编写 |

### 精度保障体系（v2.0.0 新增）

| 机制 | 所在步骤 | 作用 |
|------|---------|------|
| 精度保留提取 | Step 6a | 强制保留 L1+L2+L3 三层信息 |
| 参数映射表 | Step 6d | 每个参数逐条映射到 Skill 步骤 |
| 颗粒度校准 | Step 6e | 单一职责 + 信息密度 + 条件边界 三测试 |
| 五要素模板 | Step 7d | 输入/处理/输出/异常/衔接 强制格式 |
| 动词/名词规范 | Step 8 | 禁止使用模糊动词和泛化名词 |
| 精度交叉验证 | Step 10b | 对照源代码逐条核对参数和分支 |
| 过程式忠实保证 | Step 6f | 循环/重试/错误恢复严格按项目流程记录 |
| 无字数限制 | Step 8 | 生成的 Skill 不受篇幅限制 |

### 运行时行为

- 以 `context: fork` + `agent: general-purpose` 模式运行，隔离上下文避免污染主会话
- 大型项目（>1000 文件）自动切换到采样分析，只深入核心模块
- 每个分析步骤记录具体的文件路径引用，方便用户回溯
- 生成的 Skill 中所有指令以动词祈使句开头，包含完整的异常处理

## 输出说明

生成的 Skill 保存在目标项目的根目录下：

```
<目标项目根目录>/
└── <generated-skill-name>/
    ├── SKILL.md            # 技能主文件（可直接注册使用）
    └── README.md           # 用户文档（含安装和使用说明）
```

用户需要手动将 `<generated-skill-name>/` 复制到 `.claude/skills/` 完成注册：
```bash
cp -r <generated-skill-name> /path/to/target/.claude/skills/
```

## 与相关 Skill 的关系

| Skill | 做什么 | 不做什么 | 与本 Skill 的关系 |
|-------|--------|---------|-----------------|
| **codebase-analyzer** | 深度分析项目，生成函数级报告 | 不创建 Skill | 本 Skill 在其分析思路上增加了适用性评估和 Skill 生成 |
| **deepwiki-ai-agent** | 生成 Wiki 文档，代码问答 | 不创建 Skill | 本 Skill 在其文档化思路上增加了 Skill 格式化和输出 |
| **skill-for-skills** | 根据用户需求描述生成 Skill | 需要人工描述需求 | 本 Skill 从代码中自动提取需求，无需人工描述 |
| **本 Skill** | 从代码自动提取并生成 Skill | 不生成分析报告或 Wiki | — |

**组合使用建议**：
1. 先用 `codebase-analyzer` 对项目做全面深度分析
2. 再用 `project-to-skill` 将核心功能转化为 Skill
3. 最后用 `skill-for-skills` 对生成的 Skill 进行优化和增强

## 注意事项

- **适用性评估是本 Skill 的核心安全机制**：并非所有项目都适合 Skill 化。项目不适合被判定终止时并非"失败"，而是避免了生成一个不可用的 Skill
- **生成的 Skill 是"等价转换"而非"完整复制"**：提取的是项目的核心工作流语义，而非逐行翻译代码。边界情况和错误处理需要在实践中逐步完善
- **需要手动安装**：生成的 Skill 在项目根目录下，需要用户手动复制到 `.claude/skills/` 完成注册
- **外部 API 依赖**：如果项目依赖第三方 API，生成的 Skill 会在 Workflow 中通过 `WebFetch` 或 `Bash(gh)` 等方式调用，并在 Notes 中注明 API 认证方式。用户需要确保 API 密钥等凭证可用
- **大型项目**：超过 1000 文件的项目会自动采用采样分析，只分析核心模块路径。建议对大型 monorepo 指定子模块路径
- **不会修改源代码**：本 Skill 只读分析项目代码，所有输出只写入 `<skill-name>/` 目录
- **发现敏感信息会标记**：如果在项目中发现 API 密钥、令牌等敏感信息，会向用户标记而非写入生成的 Skill
