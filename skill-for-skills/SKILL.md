---
name: skill-for-skills
description: >-
  Automatically generate, upgrade, or self-update standards for Claude Code
  skills based on user requirements. Reads sum.md for writing standards, searches
  the web to verify external APIs and tools, and creates or updates production-ready
  SKILL.md and README.md files with proper frontmatter, workflow instructions,
  and examples. Can also search official docs to update its own skill writing
  standards (sum.md).
  Triggered by: "编写skill", "生成skill", "创建skill", "写skill",
  "自动生成skill", "skill生成", "create skill", "generate skill",
  "升级skill", "更新skill", "修改skill", "添加功能", "upgrade skill",
  "更新规范", "更新sum.md", "同步官方文档", "update standards",
  "帮我写一个skill", "帮我生成一个skill", "skill-for-skills".
version: 1.0.0
allowed-tools: Read Write Edit Glob Bash Grep WebSearch
---

# Skill-for-Skills — 自动生成 Claude Code Skill

## Purpose

根据用户需求，在当前 VSCode 项目根目录下自动生成完整的、符合官方规范的 Claude Code Skill。生成的 Skill 包含正确的目录结构、完备的 Frontmatter 元数据、清晰的 Workflow 指令、Do/Not This 对比示例，以及面向使用者的 README.md 说明文档。

## When to Use

- 用户要求"编写一个 skill"、"生成一个 skill"、"创建一个 skill"
- 用户要求"升级 skill"、"更新 skill"、"修改 skill"、"为某个 skill 添加功能"
- 用户要求"更新规范"、"更新 sum.md"、"同步官方文档"、"更新编写标准"
- 用户提到"官方文档变了"、"Skill 规范有更新"、"标准变了"
- 用户描述了一个需求并希望将其封装为可复用的 Skill
- 用户需要将重复性工作流转化为 Skill
- 用户输入以 `/skill-for-skills` 开头

## When NOT to Use

- 用户仅询问 Skill 概念或规范本身 —— 应引导阅读 `sum.md`
- 需求过于模糊，无法确定 Skill 的核心职责
- 用户要求修改 `skill-for-skills` 的 `SKILL.md` 自身（允许更新 `sum.md`，但不应修改元技能的行为逻辑）

## Workflow

### Step 1: 读取编写规范

首先使用 `Read` 工具读取同目录下的规范文档：

`Read skill-for-skills/sum.md`

`sum.md` 包含了 Skill 编写的完整规范（frontmatter 字段详解、目录结构要求、体量控制、安全注意事项等），后续所有生成步骤均需严格遵循其中的标准。

### Step 2: 分析需求与合理推断

解析 `$ARGUMENTS`，提取用户明确提到的信息，并**依据逻辑推断未说明但不可或缺的细节**。

#### 2a. 提取用户明确信息

| 提取项 | 说明 | 示例 |
|--------|------|------|
| 核心功能 | Skill 要解决什么问题 | 从互联网自动搜索文献论文 |
| 触发场景 | 用户在什么情况下会使用 | 查文献、找论文、学术搜索 |
| 关键约束 | 有什么特殊限制 | 需支持中英文搜索 |
| 技术选型 | 需要什么工具或依赖 | Python, requests, arxiv API |

如果 `$ARGUMENTS` 为空或过于模糊，**先输出对需求的理解并向用户确认**，再进行后续步骤。

#### 2b. 合理推断补全

根据提取的核心功能，按照下表进行推断补全。**这是生成高质量 Skill 的关键步骤。**

| 功能类型 | 用户常提但不够的 | 必须推断补全的内容 |
|----------|------------------|-------------------|
| **搜索/采集类** | "搜索论文""爬取数据""查资料" | ① 将结果保存到 `<skill-name>/<领域相关目录>/` 下（如 `papers/`、`articles/`），每条结果一个独立文件 ② 每个文件头部包含来源链接、时间戳、内容摘要 ③ 生成一个汇总索引文件，方便概览 ④ 处理网络超时、API 限流等异常 |
| **代码生成类** | "生成代码""写一个函数" | ① 提供可直接复制运行的完整代码块 ② 包含必要的错误处理（try-catch、Result 等） ③ 添加类型注解或类型声明 ④ 说明运行环境和依赖安装方式 |
| **分析/处理类** | "分析数据""处理日志" | ① 输入合法性校验（空值、格式错误） ② 输出结构化结果（表格、JSON、Markdown） ③ 边界情况处理（空数据集、异常值） ④ 性能建议（大数据量时的处理策略） |
| **API 集成类** | "调用某某 API""接入某服务" | ① API 密钥/认证的安全处理（环境变量而非硬编码） ② 请求重试与退避策略 ③ 响应解析与错误处理 ④ 调用频率限制说明 |
| **文档/报告类** | "生成报告""写文档" | ① 包含元数据头（日期、版本、作者） ② 自动生成目录 ③ 引用来源记录 ④ 输出格式标准化（模板） |
| **转换/格式化类** | "格式转换""批量重命名" | ① 处理前后对比预览 ② 批量操作的事务性（失败回滚或继续） ③ 支持通配符/正则等灵活匹配 ④ 输出操作日志 |

**推断原则：**
- 用户说"搜索" → 推断还需要"保存结果、组织输出、错误处理"
- 用户说"生成" → 推断还需要"可直接用、有错误处理、有说明"
- 用户说"分析" → 推断还需要"输入校验、边界处理、结构化输出"
- 用户说"调用 API" → 推断还需要"密钥安全、重试、限流"

**跨类别处理：** 如果用户需求匹配多个类别（如"调用 API 搜索论文"同时涉及"搜索/采集类"和"API 集成类"），**合并所有匹配类别的推断项**，去重后一起写入生成的 SKILL.md。

在生成的 SKILL.md 中，**将推断出的细节在 Workflow 步骤和 Constraints 中明确写出**，而非笼统带过。

#### 2c. 联网核实与信息验证

在生成 Skill 之前，对以下类型的信息使用 `WebSearch` 进行联网核实：

| 需要核实的情况 | 原因 | 搜索示例 |
|---------------|------|---------|
| 用户提到的特定 API 或服务 | API 可能已更新、废弃或变更认证方式 | "arXiv API documentation 2026" |
| 用户提到的框架或库的最新版本 | 确保生成的依赖版本准确 | "pandas latest version 2026" |
| 第三方服务的配置方式 | 确保生成的配置代码可运行 | "GitHub Actions workflow syntax" |
| 协议或标准的最新规范 | 确保生成的 Skill 符合当前标准 | "OAuth 2.0 best practices 2026" |
| 用户需求中涉及的可信数据 | 验证关键事实而非直接采信单一来源 | "arxiv API rate limit" |

**执行核实时的操作规范：**

1. **多源搜索**：对同一问题至少搜索 2 次，使用不同的关键词组合
2. **来源对比**：比较不同来源的信息是否一致。一致则采信；不一致则标记差异
3. **优先级排序**：官方文档 > 权威技术博客 > 社区讨论 > 个人博客
4. **标注来源**：在生成 SKILL.md 的 Notes 或 references/ 中注明关键信息的来源链接
5. **冲突处理**：如果不同来源信息冲突，在生成的 SKILL.md 中用 Note 注明冲突情况，让用户决策
6. **时效性检查**：优先采用当前年份的信息，过时信息（3 年以上）标注年份并谨慎使用

**无需联网核实的情况：**
- 通用的编程概念（循环、条件、函数定义等）
- 用户项目本地的代码结构和约定
- sum.md 中已明确的 Skill 编写规范

#### 2d. 判断操作类型

根据 `$ARGUMENTS` 判断当前任务是**创建新 Skill**、**升级已有 Skill** 还是**更新编写规范**：

| 判断依据 | 创建（CREATE） | 升级（UPGRADE） | 更新规范（UPDATE_SUM） |
|---------|---------------|----------------|---------------------|
| 包含"为...添加""为...升级""给...增加" | ❌ | ✅ | ❌ |
| 包含现有 Skill 名称（如 `article-search`） | ❌ | ✅ | ❌ |
| 包含"更新规范""更新sum.md""同步官方" | ❌ | ❌ | ✅ |
| 核心意图是"做一个新的" | ✅ | ❌ | ❌ |
| 核心意图是"在已有的基础上加功能" | ❌ | ✅ | ❌ |
| 核心意图是"更新编写标准" | ❌ | ❌ | ✅ |

**判断规则：**
1. 首先检查是否包含"更新规范""更新sum.md""同步官方""标准变了"等更新规范关键词
2. 如果是 → **UPDATE_SUM** 路径，跳转到 Step 3S
   > **重要：UPDATE_SUM 仅在用户明确要求更新规范时触发**，不会在任何 CREATE 或 UPGRADE 操作中自动附带执行。执行完成后必须向用户详细报告变更内容。
3. 否则，从 `$ARGUMENTS` 中提取可能的 Skill 名称（"为 X 添加 Y"中的 X）
4. 用 `Bash` 执行 `ls <可能的名称>/SKILL.md 2>/dev/null` 检查目录是否存在
5. 如果目录存在 → **UPGRADE** 路径
6. 如果目录不存在且需求明确是新建 → **CREATE** 路径
7. 如果不明确，先输出理解并向用户确认操作类型

- **CREATE 路径**：继续执行 Step 3 → 4 → 5 → 6 → 7
- **UPGRADE 路径**：跳转到 Step 3U → 4U → 5U → 6U → 7U
- **UPDATE_SUM 路径**：跳转到 Step 3S → 4S → 5S → 6S
- 三条路径在 Step 8 汇合

### Step 3: 确定 Skill 名称

将用户描述的核心功能转换为 kebab-case 名称：

- 中文含义 → 英文 kebab-case：`文章搜索` → `article-search`
- 保持简短（2-4 个单词）
- 只包含小写字母、数字、连字符
- **建议与目录名一致**

### Step 4: 创建目录结构

在 VSCode 打开的项目根目录下创建：

```
<skill-name>/
├── SKILL.md            # [必需] 入口文件
├── README.md           # [必需] 项目说明文档
├── references/         # [可选] 补充文档
├── scripts/            # [可选] 可执行脚本
└── templates/          # [可选] 模板文件
```

使用 `Bash` 工具执行以下命令创建目录结构：

```bash
mkdir -p <skill-name>/{references,scripts,templates}
```

### Step 5: 编写 Frontmatter

生成完整的 YAML frontmatter，包含：

**必需字段：**
- `name` — kebab-case，不超过 64 字符，与目录名一致
- `description` — 具体描述 + 至少 3-5 个触发关键词，遵循"略微激进"原则

**可选字段（根据情况添加）：**
- `version` — 初始为 `1.0.0`
- `allowed-tools` — 按最小权限原则列出技能所需的工具。**根据 Step 2b 推断的功能反推所需工具集：**
  - 搜索/采集 → `Read Write WebSearch WebFetch`
  - 代码生成 → `Read Write Edit Bash`
  - 分析处理 → `Read Write Bash`
  - API 集成 → `Read Write Edit Bash WebFetch`
  - 文档报告 → `Read Write`
  - 转换格式化 → `Read Write Edit Bash Glob`
- `dependencies` — 如果有脚本依赖
- `metadata.tags` — 分类标签
- `context` + `agent` — 如果需要在子 Agent 中运行
- `disable-model-invocation` — 如果包含破坏性操作

### Step 6: 编写 SKILL.md 正文

正文结构必须包含以下章节：

````
## Purpose
一句话概括技能的用途。

## When to Use
- 触发场景列表（3-5 条）

## When NOT to Use
- 排除场景（2-3 条）

## Workflow / Steps
1. **Step 1**：具体指令
2. **Step 2**：具体指令
3. **Step 3**：具体指令

## Constraints
- Always [必须遵守的规则]
- Never [禁止的行为]
- 输出格式要求

## Examples

### ✅ Do This
    输入 → 期望输出

### ❌ Not This
    输入 → 错误输出

## Notes
- 边界情况
- 已知限制
- 依赖说明
````

每条指令必须以**祈使句 + 动词开头**（如"解析""创建""生成"），而非"你应该…"。

**关键：** 将 Step 2b 中推断出的细节**直接嵌入 Workflow 步骤中**，以具体可操作的形式写出。例如：
- 不要只写"搜索论文" → 要写"使用 WebSearch 从 arXiv、Google Scholar 搜索，每个来源失败时自动降级到下一个"
- 不要只写"保存结果" → 要写"在 `<skill-name>/papers/` 下为每篇论文创建独立 .md 文件，文件头部包含 link、source、date、authors 等元数据"
- 不要只写"处理错误" → 要写"API 返回 429 时等待 5 秒后重试，最多重试 3 次"

**输出路径规范：** Workflow 中涉及的所有输出文件路径必须以 `./<skill-name>/<分类目录>/` 开头（如 `./article-search/papers/`），且 `<skill-name>/` 必须与目录名一致。禁止将输出文件写到项目根目录、`.claude/` 或 git 追踪不到的临时位置。

### Step 7: 编写 README.md

在生成的 Skill 目录中创建 `README.md`，向用户详细说明该 Skill 的使用方式。README.md 是用户接触该 Skill 的第一份文档，必须完整、准确、清晰。

README.md 必须包含以下章节：

````markdown
# <Skill 名称>

## 简介
一句话概括该 Skill 的功能和适用场景。

## 目录结构
```
<skill-name>/
├── SKILL.md            # 技能主文件
├── README.md           # 本文件
├── references/         # 补充文档
├── scripts/            # 可执行脚本
└── templates/          # 模板文件
```

（根据实际生成的目录结构调整）

## 安装方式
1. 将 `<skill-name>/` 目录复制到项目 `.claude/skills/` 下
2. 重新启动 Claude Code
3. 使用 `/skill-name` 或触发关键词激活

## 使用方式
### 斜杠命令
`/<skill-name> <参数>` — 描述命令的作用

### 自动触发
当用户输入以下关键词时自动激活：
- <关键词 1>
- <关键词 2>
- <关键词 3>

## Workflow 说明
简要描述该 Skill 的执行流程（3-5 句话），让用户在使用前了解整体过程。

## 技术细节

### 依赖
- <依赖名称> — 用途说明（如需要安装，附安装命令）

### 使用的工具
- `Read` — 读取文件
- `Write` — 写入文件
- （根据实际 `allowed-tools` 列出）

### 输出说明
- 生成的输出文件位置和格式
- 如何查看和使用输出结果

## 注意事项
- 已知限制
- 可能需要的额外配置
- 安全注意事项

## 参考
- 外部 API 文档链接
- 相关资源链接
````

**编写要点：**
- 使用与用户需求一致的语言（用户说中文则 README 用中文，用户说英文则用英文）
- 不要简单复制 SKILL.md 内容，而是从用户视角重新组织信息
- 技术细节部分必须准确反映 SKILL.md 中定义的 `allowed-tools`、`dependencies` 和 Workflow
- 依赖的安装命令需要通过 Step 2c 联网核实后写入，确保命令可执行

---

## 升级路径

以下步骤仅在 Step 2d 判定为 **UPGRADE** 时执行，替换 Step 3→7（CREATE 路径）。所有路径在 Step 8 汇合。

### Step 3U: 确定目标 Skill

从 `$ARGUMENTS` 中提取要升级的 Skill 名称：

| 用户输入 | 提取的目标名称 |
|---------|---------------|
| "为 article-search 添加按时间筛选功能" | `article-search` |
| "给论文搜索 skill 增加导出功能" | `article-search`（需通过目录存在性确认） |
| "升级 data-analyzer 支持 CSV 输入" | `data-analyzer` |

**操作规范：**
1. 提取潜在名称后，用 `Bash` 执行 `ls <名称>/SKILL.md 2>/dev/null` 确认目录存在
2. 如果目录不存在，搜索根目录下所有 `*/SKILL.md` 匹配最接近的 Skill
3. 如果找不到匹配的 Skill，**向用户报告并询问正确的 Skill 名称**，不要猜测

### Step 4U: 读取现有文件

在开始修改前，全面理解现有 Skill 的完整状态：

1. `Read <skill-name>/SKILL.md` — 完整读取当前 SKILL.md
2. `Read <skill-name>/README.md` — 完整读取当前 README.md（如果存在）
3. `Glob <skill-name>/**/*` — 了解目录下所有文件
4. 确认 `allowed-tools`、`dependencies`、当前 Workflow 步骤数量

**输出理解确认：** 用一两句话向用户总结你对现有 Skill 的理解，例如：
> "已读取 article-search，当前有 5 个 Workflow 步骤，使用 Read/Write/WebSearch 工具。你要添加按时间筛选论文的功能，对吗？"

用户确认后再继续。

### Step 5U: 划定升级范围

基于 `$ARGUMENTS` 和已读取的现有内容，精确划定改动范围：

**确定变更项：**
- **新增内容**：需要添加的新 Workflow 步骤、新 Constraint、新触发关键词
- **修改内容**：需要修改的现有步骤描述、工具权限、依赖列表
- **不变量**：现有功能必须完整保留，**不得修改或删除**已有的 Workflow 步骤逻辑
- **新增推断**：使用 Step 2b 推断表对新增功能进行推断补全
- **联网核实**：如果新增功能引入新的 API 或工具，执行 Step 2c 联网核实

**变更粒度控制：**
- 单次升级只做一件事（单一职责），如果用户一次提了多个需求，拆分为独立升级任务
- 如果用户的需求需要修改超过 50% 的现有内容，建议重新创建而非升级

### Step 6U: 执行精确升级

使用 `Edit` 工具对 SKILL.md 进行精确修改。**核心原则：只改需要改的地方，不动不需要改的地方。**

**操作规范：**

1. **版本号递增**：更新 frontmatter 中的 `version` 字段（如 `1.0.0` → `1.1.0`）
2. **更新 description**：如果新增了触发关键词，追加到 description 中
3. **更新 allowed-tools**：如果新功能需要新增工具权限，追加到 `allowed-tools`
4. **更新 Workflow**：
   - 如果新增功能是一个独立步骤：根据功能逻辑位置**插入或追加**到 Workflow 中
     - 插入在中间：新步骤插入到对应位置，**后续步骤编号全部递延**
     - 追加到末尾：新步骤编号延续（如当前到 Step 5，则新增 Step 6）
   - 如果新增功能是增强现有步骤：用 `Edit` 修改该步骤的描述，**不要重写整个步骤**
   - 保持步骤之间的前后衔接逻辑完整
5. **更新 Constraints**：新增功能所需的约束追加到 Constraints 列表
6. **更新 Examples**：追加新的 ✅ Do This / ❌ Not This 示例
7. **更新 Notes**：如有必要，追加新的注意事项
8. **更新 README.md**：同步到 Step 7U
9. **记录变更清单**：在输出报告前，整理本次升级的全部变更，每条包含：修改位置、修改前后的内容对比。不得笼统概括为"升级了若干内容"

**禁止行为：**
- ❌ 不得使用 `Write` 重写整个 SKILL.md（会丢失上下文）
- ❌ 不得修改与升级请求无关的现有步骤
- ❌ 不得删除或重命名现有的 Workflow 步骤（只允许追加或修改描述）
- ❌ 不得改变现有命令名称或触发方式（除非用户明确要求）

**每次编辑后**，立即重新读取修改区域确认上下文未被破坏。

### Step 7U: 更新 README.md

使用 `Edit` 对 README.md 进行同步更新：

- **目录结构**：如果新增了文件或目录，更新目录结构部分
- **技术细节**：如果新增了工具或依赖，更新"使用的工具"和"依赖"部分
- **Workflow 说明**：如果新增了步骤，更新 Workflow 说明
- **使用方式**：如果新增了命令参数或触发词，更新使用方式

确保 README.md 与修改后的 SKILL.md 完全一致。

---

## 规范更新路径

以下步骤仅在 Step 2d 判定为 **UPDATE_SUM** 时执行，替换所有其他路径。该路径用于在官方规范更新后，通过搜索权威来源对 `sum.md` 进行严谨更新，使 skill-for-skills 自身保持精准。

### Step 3S: 搜索权威来源

从多个渠道搜索最新的 Skill 编写规范和官方变更：

**必搜来源：**
1. `WebSearch("Claude Code SKILL.md specification 2026")` — Anthropic 官方 Skill 规范
2. `WebSearch("agentskills.io specification frontmatter fields")` — Agent Skills 开放标准
3. `WebSearch("Anthropic Claude Code custom skills documentation")` — Anthropic 官方文档
4. `WebSearch("Claude Code hooks tool use settings 2026")` — 工具和钩子最新变更

**补充来源（根据变化幅度决定是否搜索）：**
- `WebSearch("skill-creator Anthropic eval test")` — Skill 创建器的最新 eval 功能
- `WebSearch("Claude Code allowed-tools MCP")` — 工具权限的最新扩展

**操作规范：**
- 每个来源至少打开 2 个不同搜索结果进行交叉验证
- 优先采信 Anthropic 官方文档，其次是 agentskills.io 标准，最后是社区实践
- 保存所有采信信息的来源 URL，用于 Step 5S 标注

### Step 4S: 对比分析

将搜索结果与当前 `sum.md` 进行逐节对比，识别差异：

1. `Read skill-for-skills/sum.md` — 完整读取当前规范文档

**对比维度：**

| 对比项 | 检查内容 | 发现差异时的处理 |
|-------|---------|----------------|
| frontmatter 字段 | 是否有新增/废弃/改名的字段 | 更新第 四 节字段表 |
| 目录结构要求 | 是否有新的标准目录结构 | 更新第 二 节目录结构 |
| 模板章节 | SKILL.md 正文模板是否有新章节要求 | 更新第 三 节模板 |
| 触发词规范 | description 的触发词写法是否有新要求 | 更新第 五 节描述编写 |
| 体量控制 | Token/行数限制是否有变化 | 更新第 五 节体量控制 |
| allowed-tools | 工具列表是否有新增或弃用 | 更新第 四 节工具语法 |
| context: fork | 子 Agent 类型是否有新增 | 更新第 四 节 fork 用法 |
| 参考链接 | 官方文档 URL 是否变更 | 更新第 七 节参考资源 |

**差异分级：**
- **P0 — 错误信息**：sum.md 中的内容与官方文档明显矛盾 → 必须立即修正
- **P1 — 过时信息**：sum.md 引用了已废弃的字段或工具 → 标注废弃并替换
- **P2 — 新增信息**：官方有新增功能但 sum.md 未包含 → 追加到对应章节
- **P3 — 格式优化**：表达可更精确但不影响功能 → 按需优化

**输出差异报告：** 向用户输出一个简短的差异摘要，例如：
> "发现 3 处差异：agentskills.io 新增了 `effort` 字段（P2），Anthropic 文档中 `allowed-tools` 示例更新（P2），参考链接中有一处 URL 跳转（P1）。开始更新。"

### Step 5S: 精确更新 sum.md

使用 `Edit` 工具对 `sum.md` 进行精确更新。**核心原则：每条修改都必须有权威来源支撑。**

**操作规范：**

1. **逐项更新**：每个 P0/P1/P2 差异单独编辑，编辑后立即确认上下文未被破坏
2. **标注来源**：每条新增或修改的内容旁注明来源，格式为 `（来源：[标题](URL)）`
3. **更新参考资源**：如果官方文档 URL 已变更，更新第 七 节的参考链接列表
4. **版本备注**：在 sum.md 文件头部或末部添加更新备注，格式为：
   > `> 上次更新：2026-05-14 — 更新内容：effort 字段说明、allowed-tools 示例 — 来源：Anthropic 官方文档`
5. **不修改的内容**：不修改 sum.md 中与搜索结果一致的部分，不修改 sum.md 的整体结构和排版风格

**禁止行为：**
- ❌ 不得仅靠自身知识更新 sum.md — 每条修改必须有搜索结果支撑
- ❌ 不得删除 sum.md 中的内容除非有确凿证据表明官方已废弃
- ❌ 不得改变 sum.md 的章节编号和结构体系

### Step 6S: 验证更新质量

更新完成后，进行最终验证：

1. `Read skill-for-skills/sum.md` — 重读整个文件确保可读性
2. 验证每条修改是否确实有对应的来源标注
3. 验证章节编号是否连续、目录是否匹配正文
4. 如果更新涉及模板结构变化，确认示例 SKILL.md 的生成逻辑是否需要同步调整
5. 向用户输出更新总结报告，**逐条列出每一项具体变更**，包括：修改位置、修改前后的内容对比、修改依据的权威来源链接。不得笼统概括为"更新了若干内容"

---

### Step 8: 质量检查

对照以下清单逐项确认：

- [ ] `name` 是否为 kebab-case 且与目录名一致？
- [ ] `description` 是否包含至少 3 个触发关键词？
- [ ] SKILL.md 正文是否控制在 500 行 / 2000 词以内？
- [ ] README.md 是否已生成？
- [ ] README.md 是否包含：简介、目录结构、安装方式、使用方式、Workflow 说明、技术细节、注意事项？
- [ ] README.md 中的 `allowed-tools`、`dependencies`、目录结构与 SKILL.md 一致？
- [ ] 是否包含 When to Use / When NOT to Use 章节？
- [ ] 是否包含 Workflow / Steps 章节？
- [ ] 是否包含 Constraints 章节？
- [ ] 是否包含 ✅ Do This / ❌ Not This 对比示例？
- [ ] 指令是否都以动词祈使句开头？
- [ ] 是否遵循了"单一职责"原则（一个 Skill 只做一件事）？
- [ ] `allowed-tools` 是否按最小权限原则配置，且与推断的功能所需工具集匹配？
  - 搜索类 → 应有 WebSearch/WebFetch
  - 代码类 → 应有 Bash
  - API 类 → 应有 WebFetch
- [ ] 是否对用户需求进行了合理推断补全？（用户说"搜索"→推断"保存+容错"，用户说"生成"→推断"可直接运行"等）
- [ ] 推断出的细节是否已作为具体 Workflow 步骤写入，而非仅在 Notes 中提及？
- [ ] 是否考虑了异常处理、输出组织等"用户没提但不可或缺"的部分？
- [ ] 是否对涉及的外部 API、服务、工具进行了联网核实？（至少搜索 2 次，对比不同来源）
- [ ] 核实结果是否标注了来源？来源冲突时是否在 Notes 中注明？

**UPGRADE 路径额外检查项：**
- [ ] 是否只修改了需要改的部分？（没有破坏现有功能）
- [ ] 版本号是否已递增？
- [ ] Workflow 步骤编号是否连续？（新追加的步骤编号正确接续）
- [ ] 新增功能是否已推断了必要的异常处理和输出组织？
- [ ] 如果用 `Edit` 修改了现有步骤，前后文的逻辑衔接是否依然完整？

**UPDATE_SUM 路径额外检查项：**
- [ ] 每条修改是否都有权威来源支撑？（Anthropic 官方 > agentskills.io > 社区）
- [ ] 是否标注了来源链接？
- [ ] P0（错误信息）和 P1（过时信息）是否已全部处理？
- [ ] sum.md 章节编号是否依然连续？
- [ ] 参考资源链接是否已更新？

### Step 9: 审查验证与修正

生成 SKILL.md 和 README.md 后，在向用户报告之前，必须先进行一轮完整的审查验证。这是对用户负责的最后一道防线。

使用 `Read` 工具重新读取生成的 SKILL.md 和 README.md，逐项审查以下维度：

#### 9a. 逻辑审查

逐条阅读 Workflow 步骤，检查是否存在以下问题：

- **步骤遗漏**：从输入到输出是否完整覆盖？是否存在跳跃？
  - 例：写了"搜索论文"和"保存结果"，但没写中间的"筛选与去重"
- **循环依赖**：步骤 A 依赖步骤 B 的输出，但步骤 B 在步骤 A 之后执行
- **死路分支**：某个条件分支没有最终输出或终止条件
- **路径矛盾**：两个步骤给出的路径或目录结构不一致
  - 例：Step 2 说保存到 `output/`，Step 4 引用 `results/`

发现逻辑问题 → **直接修正**，修正后重新执行 Step 8 格式合规检查。

#### 9b. 清晰度审查

检查每条指令是否足够清晰，不会产生歧义：

- **模糊动词**：是否使用了"处理""分析""管理"等过于笼统的动词？
  - 修复：替换为具体动词，如"提取""过滤""合并""转换"
- **未定义术语**：是否使用了未在 SKILL.md 中定义的缩写或专业术语？
  - 修复：在术语首次出现时添加括号注释
- **无主语指令**：每条指令是否以明确的主语+动词开头？
  - 修复：补全缺失的主语
- **边界未定义**："大量数据""较长时间"等模糊量词是否给出了具体阈值？
  - 修复：替换为具体数值，如"超过 1000 条时自动分页"

#### 9c. 安全性审查

逐一排查可能造成不良影响的风险点：

| 风险类型 | 检查项 | 修复要求 |
|---------|--------|---------|
| 破坏性操作 | 是否包含删除、覆盖、修改文件的操作？ | 添加确认步骤或 `disable-model-invocation: true` |
| 依赖风险 | 是否推荐了来源不明的第三方脚本或库？ | 添加来源说明和安全警告 |
| 权限风险 | 是否请求了不必要的工具权限？ | 缩小 `allowed-tools` 范围 |
| 数据风险 | 是否输出到项目根目录之外？ | 限制输出到项目目录内 |
| 无限操作 | 是否存在无终止条件的循环或递归？ | 添加最大次数限制 |
| 静默失败 | 失败时是否无任何提示地继续执行？ | 添加明确的错误输出 |

#### 9d. 可行性审查

从用户视角判断生成的 Skill 是否真的可用：

- **环境假设**：是否假设了用户安装了特定工具/库而没有提供安装方式？
- **路径正确性**：Workflow 中引用的每个目录和文件都确实会在对应步骤之前被创建吗？
- **时效性**：引用的 API 地址、工具版本是否已通过 Step 2c 联网核实？
- **可恢复性**：如果某一步失败，用户能否从失败点重试而不必从头开始？

#### 9e. 一致性审查

核对 SKILL.md 和 README.md 之间的信息是否一致：

- `allowed-tools` 在两处是否一致？
- Workflow 步骤描述是否矛盾？
- 目录结构描述是否匹配？
- 安装和使用方式是否一致？

#### 9f. 回归审查（UPGRADE 路径）

仅在 UPGRADE 路径下执行，检查升级是否破坏了现有功能：

- 升级前存在的 Workflow 步骤是否依然完整且逻辑正确？
- 新增步骤是否与现有步骤的输入输出衔接？
- 原有 `allowed-tools` 是否被移除？（只应添加不应移除）
- 原有触发关键词依然存在于 description 中？
- 原有 Examples 是否被修改或删除？（不应修改，只应追加）
- README.md 中关于原有功能的描述是否被覆盖或删除？

发现回归问题 → **立即撤销该修改并用更精确的方式重新编辑**。

#### 9g. 规范审查（UPDATE_SUM 路径）

仅在 UPDATE_SUM 路径下执行，检查 sum.md 更新的完整性和准确性：

- 每个更新点是否都有权威来源链接标注？
- 更新的字段描述是否与官方文档完全一致？（无自行演绎）
- 如果官方有示例代码，sum.md 中的示例是否与官方一致？
- 版本备注是否已更新？（上次更新日期和内容）
- 参考资源部分是否有 URL 已失效但未被更新？
- sum.md 整体风格和章节编号是否与更新前保持一致？

发现规范问题 → **补充搜索更多来源确认后修正**。

#### 9h. 修正与闭环

- 如果在审查中发现任何问题，**立即使用 `Edit` 工具修正**，不要留给用户
- 修正后，重新执行 Step 8 格式合规检查，确保修正没有引入新的格式问题
- 审查通过后进入 Step 10

### Step 10: 输出报告

向用户输出 Markdown 格式的生成报告。**CREATE**、**UPGRADE** 和 **UPDATE_SUM** 路径使用不同的报告模板：

**CREATE 路径报告模板：**
````markdown
## ✅ Skill 生成完成

**名称**：`<skill-name>`
**路径**：`<skill-name>/`（项目根目录）

### 目录结构
    <skill-name>/
    ├── SKILL.md
    ├── README.md
    └── ...

### 功能概述
<简要描述生成的 Skill 的功能>

### 触发方式
- 斜杠命令：`/<skill-name>`
- 自动触发关键词：<关键词列表>

### 使用方式
将 `<skill-name>/` 目录复制到 `.claude/skills/<skill-name>/` 即可注册使用。
````

**UPGRADE 路径报告模板（必须逐条明细，不得笼统概括）：**
````markdown
## ✅ Skill 升级完成

**名称**：`<skill-name>`

### 变更明细

1. **新增 Step 2：按年份筛选**
   - 位置：在 Step 1 和旧 Step 2 之间插入
   - 变更前：Step 1 搜索后直接进入去重
   - 变更后：Step 1 搜索 → Step 2 年份筛选 → Step 3 去重（后续步骤编号递延）

2. **description 追加触发词**
   - 位置：Frontmatter description
   - 追加：`"年份筛选", "按年份过滤"`

3. **版本号递增**
   - 从 `1.0.0` → `1.1.0`

### 已升级文件
- `<skill-name>/SKILL.md`
- `<skill-name>/README.md`

### 未变更部分
- 原有 5 个 Workflow 步骤功能不变
- 原有触发关键词不变
- 原有 Constraints 不变

### 使用方式
该 Skill 已升级完成，无需重新安装，下次使用即可体验到新功能。
````

**UPDATE_SUM 路径报告模板（必须逐条明细，不得笼统概括）：**
````markdown
## ✅ 规范更新完成

**更新文件**：`skill-for-skills/sum.md`

### 变更明细

1. **[P2] 新增 effort 字段说明**
   - 位置：第四节 frontmatter 字段表
   - 变更：追加 `effort` 字段及说明
   - 来源：[Anthropic 官方 Skill 规范](URL)

2. **[P1] 更新 hooks 用法描述**
   - 位置：第四节 hooks 段落
   - 变更前：`hooks 仅支持 PreToolUse`
   - 变更后：`hooks 支持 PreToolUse 和 PostToolUse`
   - 来源：[Anthropic 官方文档](URL)

### 来源列表
- [Anthropic 官方 Skill 文档](URL)
- [agentskills.io 规范](URL)

### 未变更确认
- 第三节模板结构：与官方一致，无需更新
- 第五节体量控制：限制未变化
- 参考资源中 6 个链接：全部有效
````

**注意：** 变更明细的每条必须包含"位置、变更前后对比、来源链接"三项。不允许"更新了若干内容"这类模糊表述。

## Constraints

- **Always** 第一步使用 `Read` 工具读取 `skill-for-skills/sum.md`，将规范文档内容加载到上下文中再开始生成
- **Always** 严格执行 `sum.md` 中的 frontmatter 字段规范、目录结构要求和体量控制标准
- **Always** 对用户的需求进行合理推断补全：用户说"搜索"就推断需要"保存+组织+容错"，用户说"生成"就推断需要"完整+可用+注释"
- **Always** 将推断出的细节作为具体 Workflow 步骤写入生成的 SKILL.md，而非仅在 Notes 中一笔带过
- **Always** 使用 `$ARGUMENTS` 占位符接收用户输入
- **Always** 生成的文件保存在 VSCode 项目根目录下（`<skill-name>/`）
- **Always** 生成的 Skill 在执行任务时，所有输出文件必须定位到 VSCode 项目根目录下的 `<skill-name>/<合理分类目录>/` 中，如 `article-search/papers/<论文名>.md`、`data-analyzer/reports/<报告名>.md`。禁止输出到 `<skill-name>/` 之外的位置，也禁止堆砌在 `<skill-name>/` 根目录下不加分类
- **Always** 为生成的每个 Workflow 步骤考虑异常路径：输入为空怎么办、网络超时怎么办、依赖缺失怎么办
- **Always** 在引用外部 API、服务或第三方工具前，先使用 `WebSearch` 联网核实其当前状态和正确用法，并标注信息来源
- **Always** 生成 SKILL.md 和 README.md 后必须执行 Step 9 审查验证，使用 `Read` 重读生成的文件，逐项排查逻辑、清晰度、安全性、可行性和一致性问题，发现问题立即修正
- **Always** 执行 UPGRADE 时使用 `Edit` 而非 `Write` 修改已有文件，只改动与需求直接相关的部分
- **Never** 在 UPGRADE 中修改或删除与升级请求无关的现有 Workflow 步骤、Examples 或触发关键词
- **Never** 修改 `skill-for-skills/` 或项目其他位置已有文件（UPGRADE 路径下正在升级的目标 Skill 目录除外）
- **Always** 执行 UPDATE_SUM 时每条修改必须有权威来源支撑，编辑后立即标注来源 URL
- **Never** 执行 UPDATE_SUM 时仅凭自身知识修改 sum.md（必须经过 Step 3S 搜索验证）
- **Never** 修改 `skill-for-skills/SKILL.md` 自身（元技能的行为逻辑不应被修改）
- **Never** 生成不符合 frontmatter 规范的 SKILL.md
- **Never** 在 SKILL.md 中留下占位符或未完成的内容
- **Never** 在 description 中使用"我"作主语 —— 用第三人称描述 Skill 做什么
- 保持 SKILL.md 正文在 500 行 / 2000 词以内
- 详细信息应放在 `references/` 子目录中
- 如果用户需求涉及网络搜索、API 调用等，在生成 Skill 时包含相应的 `allowed-tools` 和 `dependencies`

## Examples

### ✅ Do This

**用户输入：**
```
/skill-for-skills 请帮我编写一个能够从互联网上自动搜索相关文献论文的skill
```

**正确做法 — 需求推断与联网核实：**
- 用户说"搜索论文" → 推断需要保存结果到本地文件
- 推断每条结果包含链接+摘要 → 方便回溯
- 推断需要多源搜索（arXiv、Google Scholar 等）→ 提高覆盖率
- 推断需要处理搜索失败、网络超时 → 健壮性
- 推断生成汇总索引文件 → 方便概览
- **联网核实**：`WebSearch("arXiv API rate limit 2026")`、`WebSearch("arxiv.org API documentation")` 确认当前接口限制
- **交叉验证**：对比 arXiv 官方文档和社区实践，确认 API 限频为每秒 1 次、无需认证
- **标注来源**：在生成的 SKILL.md Notes 中注明 arXiv API 官方文档链接

**生成结构：**
```
article-search/
├── SKILL.md
└── README.md
```

**生成的 SKILL.md（节选，展示推断细节）：**

```yaml
---
name: article-search
description: >-
  Search and compile academic papers/literature on a given research topic.
  Uses web search to find papers from arXiv, Google Scholar, PubMed, etc.
  Outputs structured markdown files.
  Triggered by: "找论文", "文献搜索", "查文献", "学术论文", "research papers".
allowed-tools: Read Write WebSearch
---

```

````markdown
## Workflow / Steps

### Step 1: 搜索论文
使用 WebSearch 工具从多个来源（arXiv、Google Scholar、PubMed）搜索论文。
如果某个来源不可用，自动降级到其他来源，不中断整体流程。

### Step 2: 筛选与整理
对搜索结果去重，按相关度排序。为每篇论文提取：标题、作者、发表年份、来源链接、摘要。

### Step 3: 保存论文文件
在 `article-search/papers/` 目录下，为每篇论文创建一个独立文件：

```
papers/
├── index.md                    # 汇总索引（论文列表+搜索概况）
├── 2024-大语言模型综述.md       # 每篇论文独立文件
├── Attention-Is-All-You-Need.md
└── ...
```

每个论文文件头部包含元数据块：
```markdown
---
title: "论文标题"
link: https://arxiv.org/abs/xxxx.xxxxx
source: arXiv
date: 2024-01
authors: ["作者1", "作者2"]
tags: [关键词]
---

## 概述
<200-300字摘要>

## 核心贡献
- 贡献点1
- 贡献点2

## 关键方法
...

## 备注
...
```

### Step 4: 生成汇总索引
在 `papers/index.md` 中生成搜索汇总：搜索关键词、时间、结果数量、每篇论文的快速链接和一句话简介。

### Step 5: 输出报告
向用户报告搜索完成的总篇数、保存路径和主要发现。
````

**同时生成的 README.md：**

```markdown
# Article Search

## 简介
自动从互联网搜索学术论文，保存为结构化 Markdown 文件。

## 目录结构
    article-search/
    ├── SKILL.md
    └── README.md

## 安装方式
1. 将 `article-search/` 复制到项目 `.claude/skills/` 下
2. 重新启动 Claude Code
3. 使用 `/article-search` 或触发关键词激活

## 使用方式
### 斜杠命令
`/article-search <研究主题>` — 搜索指定主题的学术论文

### 自动触发
"找论文"、"查文献"、"学术搜索"、"research papers"

## Workflow 说明
搜索 → 筛选去重 → 保存论文文件（含元数据头） → 生成汇总索引 → 输出报告

## 技术细节
### 依赖
无外部依赖，仅需 Claude Code 内置工具。

### 使用的工具
- `Read` — 读取文件
- `Write` — 写入论文文件
- `WebSearch` — 搜索学术论文

### 输出说明
论文文件保存在 `article-search/papers/` 下，每篇论文一个 `.md` 文件。
汇总索引在 `papers/index.md`。
```

**审查验证：**
- `Read article-search/SKILL.md` 和 `Read article-search/README.md` 重读
- **逻辑审查**：Step 1→2→3→4→5 流程完整，无跳跃、无循环依赖
- **清晰度审查**：动词具体（"搜索""去重""保存""生成""报告"），术语有定义，无模糊量词
- **安全性审查**：仅使用 Read/Write/WebSearch，无破坏性操作，有异常处理（来源降级）
- **可行性审查**：`article-search/papers/` 目录在 Step 3 创建，Step 4 引用正确；arXiv API 已通过联网核实；每步失败都有降级策略
- **一致性审查**：README.md 中的工具列表、目录结构与 SKILL.md 一致，安装方式与 Notes 一致
- **修正**：无需修正，审查通过

### ✅ Do This — 升级已有 Skill

**用户输入：**
```
/skill-for-skills 请帮我为 article-search 添加按年份筛选论文的功能
```

**正确做法：**

**Step 2d 判断：** UPGRADE 路径（`article-search/` 目录存在，`$ARGUMENTS` 包含"为…添加"）

**Step 3U 确定目标：** `article-search`

**Step 4U 读取现有文件：**
```
Read article-search/SKILL.md
Read article-search/README.md
```
→ 确认当前有 5 个 Workflow 步骤，使用 Read/Write/WebSearch 工具

**Step 5U 划定范围：**
- 新增内容：在 Step 1（搜索论文）之后插入新的筛选步骤，编号为 Step 2
- 向后递延：原 Step 2→3→4→5 变为 Step 3→4→5→6
- 推断细节：筛选需要用户提供起始年份和结束年份，需校验输入格式
- 联网核实：无需（不涉及新的 API 或工具）

**Step 6U 执行升级（用 Edit 精确修改）：**

```diff
- ### Step 1: 搜索论文
+ ### Step 1: 搜索论文（指定年份范围）
- 使用 WebSearch 工具从多个来源（arXiv、Google Scholar、PubMed）搜索论文。
+ 解析用户指令中的年份范围参数（`from:2022 to:2024`），未指定时默认近 5 年。
+ 使用 WebSearch 工具从多个来源（arXiv、Google Scholar、PubMed）搜索论文。

+ ### Step 2: 按年份筛选
+ 对搜索结果按发表年份过滤，仅保留指定范围内的论文。
+ 如果某篇论文没有年份信息，标记为"年份未知"并保留在结果中供用户判断。

- ### Step 2: 筛选与整理
+ ### Step 3: 筛选与整理
  （原有内容不变，步骤编号递延）

- ### Step 3: 保存论文文件
+ ### Step 4: 保存论文文件
  （原有内容不变，步骤编号递延）

...（后续步骤编号依次递延）
```

允许的变更：追加步骤、修改现有步骤描述、递延编号。不移除任何原有功能。

**Step 6U 记录变更清单：**
> 变更 1：Step 1 增强 — 搜索时支持指定年份范围参数
> 变更 2：新增 Step 2 — 按年份筛选（原 Step 2→5 递延为 Step 3→6）
> 变更 3：description 追加触发词 "年份筛选"
> 变更 4：version 1.0.0 → 1.1.0

**审查验证 — 回归审查重点：**
- 原有 Step 1 的内容是否被删除？→ 否，仅增强了描述
- 原有 Step 2→5 是否完整保留？→ 是，仅编号递延
- 新增的 Step 2 是否与 Step 1 和 Step 3 逻辑衔接？→ 是（搜索→筛选→去重保存）
- description 是否保留了原有触发词并追加了新词？→ 是
- **修正**：无需修正，审查通过

### ✅ Do This — 更新编写规范

**用户输入：**
```
/skill-for-skills 请更新 sum.md，查看最新的官方规范是否有变更
```

**正确做法：**

**Step 2d 判断：** UPDATE_SUM 路径（`$ARGUMENTS` 包含"更新 sum.md"）

**Step 3S 搜索权威来源：**
```
WebSearch("Claude Code SKILL.md specification 2026")
WebSearch("agentskills.io specification frontmatter fields")
WebSearch("Anthropic Claude Code custom skills documentation")
```
→ 搜索到 Anthropic 官方文档中有新的 `effort` 字段说明和 `hooks` 用法更新

**Step 4S 对比分析：**
- `Read skill-for-skills/sum.md` → 当前 sum.md 没有 `effort` 字段说明（P2 新增信息）
- `Read skill-for-skills/sum.md` → `hooks` 用法描述与官方有细微差异（P1 过时信息）
- 参考链接中有一处已跳转到新 URL（P1 过时信息）
- **差异报告**：3 处差异，均为 P1/P2 级别，无 P0 错误

**Step 5S 精确更新：**
```
Edit: sum.md — 在 frontmatter 字段表追加 effort 字段（来源: Anthropic 官方文档）
Edit: sum.md — 更新 hooks 用法描述（来源: Anthropic 官方文档）
Edit: sum.md — 更新参考链接 URL（确认新跳转地址）
```

**Step 6S 验证 + 报告：**
- `Read skill-for-skills/sum.md` → 章节编号连续、来源标注完整、可读性良好
- **输出报告（逐条汇报给用户）：**
  > **变更 1** [P2]：第四节 frontmatter 字段表追加 `effort` 字段说明，来源：Anthropic 官方文档
  > **变更 2** [P1]：第四节 hooks 段落更新用法描述，来源：Anthropic 官方文档
  > **变更 3** [P1]：第七节参考链接更新失效 URL，确认新跳转地址
- **修正**：无需修正，验证通过

### ❌ Not This

**创建 skill 时的错误做法 — 缺乏合理推断：**
- 生成的 SKILL.md 只有"搜索论文"这一句话，没有任何关于结果如何保存、组织和使用的说明
- 用户搜索完论文后不知道结果在哪里、怎么查看
- 没有考虑网络搜索可能失败的情况
- 没有联网核实 arXiv API 的当前状态，直接假设接口地址和限制
- 生成后未经审查验证就直接交付，遗留了路径不一致和步骤遗漏问题
- 没有生成 README.md，用户不知道如何安装和使用该 Skill
- `description` 写为 "I can search for papers"（使用第一人称）
- 没有 When to Use / When NOT to Use 章节
- 没有提供 Do/Not This 示例
- SKILL.md 中残留了 `[填写说明]` 等占位符

**升级 skill 时的错误做法 — 缺乏精确性：**
- 用 `Write` 重写了整个 SKILL.md，导致原有格式和 Examples 丢失
- 新增步骤编号错误（如从 Step 5 直接跳到 Step 7），导致流程断裂
- 修改了原有的触发关键词，用户无法再通过旧关键词激活
- 删除了原有的 Constraint，导致安全防护缺失
- 没有递延后续步骤编号，出现两个 Step 2
- 修改了与升级请求无关的 Example，导致原有功能文档不准确

**更新规范时的错误做法 — 缺乏严谨性：**
- 未搜索官方文档，仅凭自身知识修改 sum.md，引入不准确的信息
- 修改了与官方变更无关的章节，扩大了变更范围
- 更新后未标注来源链接，后续无法追溯信息来源
- 删除了 sum.md 中已有的内容但官方并未废弃该字段
- 仅搜索单一来源未交叉验证，采信了过时或不准确的信息
- 更新后未重读 sum.md，导致章节编号断裂或格式混乱

## Notes

- 生成的 Skill 直接输出在项目根目录下，需手动将 `<skill-name>/` 复制到 `.claude/skills/<skill-name>/` 完成注册
- 升级已有 Skill 时，SKILL.md 和 README.md 会直接原地更新，无需重新复制目录
- 更新规范时，sum.md 直接原地修改，每条变更都附带权威来源链接
- 如果生成的 Skill 依赖外部 API 或工具，在 `dependencies` 中注明并在 `Notes` 中说明安装方式
- 对于复杂 Skill，建议在 `references/` 中提供详细文档以保持 SKILL.md 的精简
- 对于包含脚本的 Skill，确保脚本文件有正确的 shebang 和可执行权限
