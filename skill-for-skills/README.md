# Skill-for-Skills — 自动生成与维护 Claude Code Skill 的元技能

skill-for-skills 是一个 **元技能（Meta-Skill）**，即"用于生成技能的技能"。它能够根据用户自然语言描述，自动创建完整的、符合官方规范的 Claude Code Skill（`.claude/skills/<name>/SKILL.md`），并能升级已有 Skill、甚至通过搜索官方文档更新自身的编写标准（`sum.md`）。

---

## 项目结构

```
skill-for-skills/           # 元技能根目录
├── SKILL.md                # [核心] 元技能的指令文件（Claude 加载后激活本技能）
├── sum.md                  # [参考] Skill 编写规范总览（SKILL.md 引用该标准进行生成）
└── README.md               # 本文件

# 由本技能生成的目标 Skill 示例（位于项目根目录）：
article-search/             # 生成的论文搜索技能
├── SKILL.md                # 生成的目标技能主文件
└── README.md               # 生成的目标技能说明文档
```

### 关键文件说明

| 文件 | 角色 | 说明 |
|------|------|------|
| `SKILL.md` | 元技能本体 | 包含 frontmatter 元数据 + 完整工作流指令。被 Claude Code 加载后激活 |
| `sum.md` | 编写规范 | Skill 格式标准参考文档。SKILL.md 在 Step 1 中读取它，用于指导生成 |
| 生成的 `SKILL.md` | 目标技能 | 由元技能根据用户需求自动生成，可直接复制到 `.claude/skills/` 使用 |

---

## 技术原理

### 什么是 Claude Code Skill？

Skill 是一个自包含的指令包（一个包含 `SKILL.md` 的目录），为 Claude 提供领域专业知识、工作流和工具使用指南。Skill 采用**渐进式加载**模型：

```
L1 — 元数据（~100 tokens）：name + description → Agent 启动时发现
L2 — 指令（< 5000 tokens）：SKILL.md 正文 → 技能激活时加载
L3 — 资源（按需）：references/ scripts/ → 按需调用
```

### 元技能的工作机制

`skill-for-skills` 本身也是一个 Skill。当 Claude 检测到用户输入匹配其 `description` 中的触发词时（如"编写 skill"、"创建 skill"），自动加载 `SKILL.md`，执行其中的 Workflow 指令来生成新的 Skill。

核心能力链：

```
用户需求 → 需求分析 → 合理推断 → 联网核实 → 生成 SKILL.md + README.md → 质量检查 → 审查验证 → 交付
```

### 三条操作路径

本技能支持三种独立操作，通过 Step 2d 自动判断用户意图：

```
Step 2d 判断
├── CREATE（创建）    → 用户说"编写一个skill"
├── UPGRADE（升级）   → 用户说"为某个skill添加功能"
└── UPDATE_SUM（更新）→ 用户说"更新sum.md"
         ↓
   Step 8 质检 → Step 9 审查 → Step 10 报告
```

---

## 运行流程

### CREATE — 创建新 Skill

```
用户输入: /skill-for-skills 请帮我编写一个能够联网搜索论文的skill

Step 1  读取 sum.md 规范         → Read skill-for-skills/sum.md
Step 2a 提取用户需求              → 核心功能、触发场景、关键约束、技术选型
Step 2b 合理推断补全              → 按功能类型表推断 4 项必备细节
Step 2c 联网核实                  → WebSearch 验证 arXiv API 状态、限频等
Step 2d 判断操作类型              → CREATE 路径
Step 3  确定 Skill 名称           → article-search
Step 4  创建目录结构              → mkdir -p article-search/{references,scripts,templates}
Step 5  编写 Frontmatter          → name、description、allowed-tools、version
Step 6  编写 SKILL.md 正文        → Purpose → When to Use → Workflow → Constraints → Examples → Notes
Step 7  编写 README.md            → 面向用户的说明文档
Step 8  质量检查                  → 格式合规、推断补全、联网核实 3 类检查
Step 9  审查验证                  → 逻辑、清晰度、安全性、可行性、一致性审查
Step 10 输出报告                  → 生成完成报告
```

### UPGRADE — 升级已有 Skill

```
用户输入: /skill-for-skills 请为 article-search 添加按年份筛选功能

Step 2d 判断操作类型              → UPGRADE 路径（目录存在 + "为…添加"）
Step 3U 确定目标 Skill            → article-search（ls 确认目录存在）
Step 4U 读取现有文件              → Read SKILL.md + README.md
Step 5U 划定升级范围              → 新增内容、不变量、推断补全
Step 6U 执行精确升级              → Edit 工具逐项修改（不得用 Write 重写）
Step 7U 更新 README.md            → 同步更新说明文档
Step 8-10 质量检查+审查+报告      → 含回归审查（检查原有功能是否被破坏）
```

### UPDATE_SUM — 更新编写规范

```
用户输入: /skill-for-skills 请更新 sum.md，查看最新的官方规范是否有变更

Step 2d 判断操作类型              → UPDATE_SUM 路径（显式关键词触发）
Step 3S 搜索权威来源              → WebSearch 多个官方渠道
Step 4S 对比分析                  → 7 个维度 × 4 级严重度（P0/P1/P2/P3）
Step 5S 精确更新 sum.md           → Edit 逐项修改 + 来源标注
Step 6S 验证更新质量              → 重读 + 来源审计 + 章节完整性检查
Step 8-10 质量检查+审查+报告      → 含规范审查 + 逐条变更报告
```

**重要：UPDATE_SUM 仅在用户明确要求时触发**，不会在 CREATE 或 UPGRADE 中自动附带执行。

---

## 安装方式

### 前提条件

- Claude Code 已安装并可用
- 项目根目录下存在 `.claude/` 目录（如不存在，可手动创建）

### 安装步骤

**方式一：直接使用（推荐开发调试）**

将 `skill-for-skills/` 整个目录放入项目根目录，然后通过 `/skill-for-skills` 命令调用。

**方式二：注册为系统 Skill（推荐正式使用）**

```bash
# 将 skill-for-skills 复制到项目 skills 目录
cp -r skill-for-skills .claude/skills/skill-for-skills/

# 重启 Claude Code 后即可识别
```

### 验证安装

在 Claude Code 中输入：

```
/skill-for-skills 帮我创建一个skill
```

如果 Claude 响应并开始询问需求细节，则安装成功。

---

## 使用方式

### 斜杠命令

```bash
/skill-for-skills <需求描述>
```

### 常见使用场景

#### 场景 1：创建新 Skill

```
/skill-for-skills 请帮我编写一个能够从互联网上自动搜索相关文献论文的skill
```

系统将：
1. 分析搜索论文的核心需求
2. 推断需要保存结果、处理错误、生成索引
3. 联网核实 arXiv API 当前状态
4. 在项目根目录生成 `article-search/` 目录，内含 SKILL.md + README.md

#### 场景 2：升级已有 Skill

```
/skill-for-skills 请为 article-search 添加按年份筛选论文的功能
```

系统将：
1. 读取 `article-search/SKILL.md` 现有内容
2. 分析改动范围（插入新 Step，递延后续编号）
3. 使用 Edit 精确修改，不动原有功能
4. 同步更新 README.md
5. 回归审查确认升级未破坏现有功能

#### 场景 3：更新编写规范

```
/skill-for-skills 请更新 sum.md，查看最新的官方规范是否有变更
```

系统将：
1. 搜索 Anthropic 官方文档、agentskills.io 等多个权威来源
2. 与当前 sum.md 逐节对比，识别差异
3. 按 P0-P3 分级处理，逐项更新
4. 每条变更附带来源链接
5. 输出逐条变更报告

### 触发关键词

本技能可通过以下关键词自动激活（无需斜杠命令）：

- **创建类**："编写skill"、"生成skill"、"创建skill"、"写skill"、"帮我写一个skill"
- **升级类**："升级skill"、"更新skill"、"修改skill"、"添加功能"
- **更新规范类**："更新规范"、"更新sum.md"、"同步官方文档"、"update standards"

---

## 核心设计原则

### 1. 需求推断（合理补全）

用户说"搜索"，系统推断还需要"保存结果、组织输出、错误处理"。推断覆盖 6 大功能类型：

| 功能类型 | 推断内容 |
|---------|---------|
| 搜索/采集 | 保存到文件 + 头部元数据 + 汇总索引 + 异常处理 |
| 代码生成 | 完整可运行 + try-catch + 类型注解 + 环境说明 |
| 分析/处理 | 输入校验 + 结构化输出 + 边界处理 + 性能建议 |
| API 集成 | 密钥安全 + 重试退避 + 响应解析 + 频率限制 |
| 文档/报告 | 元数据头 + 目录 + 引用来源 + 模板标准化 |
| 转换/格式化 | 对比预览 + 事务性 + 通配符 + 操作日志 |

### 2. 联网核实（信息验证）

在引用外部 API、服务或第三方工具前，先搜索确认其当前状态：

- 至少搜索 2 次，使用不同关键词组合
- 优先级：官方文档 > 权威博客 > 社区讨论
- 来源冲突时在 Notes 中注明，由用户决策
- 过时信息（3 年以上）标注年份并谨慎使用

### 3. 审查闭环（质量保障）

生成后的质量防线：

```
Step 2c 联网核实    → 外部信息验证
Step 8 质量检查     → 格式合规 + 路径专项检查
Step 9a-9e 五维审查 → 逻辑/清晰度/安全性/可行性/一致性
Step 9f 回归审查    → UPGRADE 路径专项
Step 9g 规范审查    → UPDATE_SUM 路径专项
Step 9h 修正闭环    → 发现问题就地修正，不留到用户手上
```

### 4. 最小修改（UPGRADE 路径）

- 使用 `Edit` 而非 `Write` 修改已有文件
- 只改动与需求直接相关的部分
- 插入新步骤时后续编号全部递延
- 绝不删除或修改与升级无关的内容

### 5. 来源可追溯（UPDATE_SUM 路径）

- 每条修改必须有权威来源支撑
- 修改旁标注 `（来源：[标题](URL)）`
- 输出逐条变更报告，含位置、变更前后对比、来源链接
- 不允许"更新了若干内容"这类模糊表述

---

## 注意事项

### 使用限制

1. **本技能不修改自身行为逻辑**：`skill-for-skills/SKILL.md` 不可被本技能修改。如需调整元技能行为，请手动编辑。
2. **UPGRADE 不跨项目**：升级路径只查找当前项目目录下的 Skill，不会跨项目操作。
3. **UPDATE_SUM 仅显式触发**：不会在创建或升级 Skill 时自动附带更新 sum.md。
4. **生成的 Skill 需手动注册**：生成的 Skill 目录在项目根目录下，需复制到 `.claude/skills/<name>/` 才能被 Claude Code 自动识别。

### 安全注意事项

- 生成含网络请求的 Skill 时，确保 `allowed-tools` 只包含最小必要工具集
- 升级时务必执行回归审查，确认新功能不破坏旧有逻辑
- 更新规范时每条修改必须有来源支撑，不得仅凭知识修改
- 生成的 Skill 如有破坏性操作（删除、覆盖文件），应设置 `disable-model-invocation: true`

### 已知限制

- VS Code 扩展的验证器（v2.1.39）对 `allowed-tools`、`context: fork`、`agent`、`model` 等扩展字段会误报警告，但不影响运行时功能（详见 sum.md 第 5.9 节）
- 当用户单次提出多个不相关的 Skill 需求时，建议拆分为多次请求

### 建议

- 创建新 Skill 时，尽量提供具体的功能描述和约束条件，描述越详细生成的 Skill 越精准
- 升级时一次只提一个需求，便于系统精确控制变更范围
- 定期执行 UPDATE_SUM 检查官方规范是否有变更，保持生成标准与时俱进

---

## 依赖

本技能运行在 Claude Code 环境中，无需额外安装包或库。所需工具已通过 `allowed-tools` 声明：

| 工具 | 用途 |
|------|------|
| `Read` | 读取 sum.md、已生成的 SKILL.md、README.md |
| `Write` | 创建新的 SKILL.md 和 README.md |
| `Edit` | 精确修改已有文件（升级路径、更新规范路径使用） |
| `Glob` | 检查目录结构、查找已有 Skill |
| `Bash` | 创建目录（`mkdir -p`）、检查文件存在性 |
| `Grep` | 搜索文件内容 |
| `WebSearch` | 联网核实 API 状态、搜索官方规范 |

---

## 相关资源

- [Anthropic 官方 — How to create custom Skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)
- [Agent Skills 开放标准 (agentskills.io)](https://agentskills.io)
- [Agent Skills 规范 GitHub 仓库](https://github.com/agentskills/agentskills)
- [Anthropic 官方 Skill 示例库](https://github.com/anthropics/skills)
- [Claude Code 官方文档](https://docs.anthropic.com/en/docs/claude-code)
- [CLAUDE.md 完整配置指南](https://www.morphllm.com/claude-md-guide)
