# Claude Code Skill 编写指南

> 综合整理自 Anthropic 官方文档、Agent Skills 开放标准 (agentskills.io) 及社区最佳实践 (2025–2026)

---

## 一、什么是 Skill

Skill 是一个自包含的指令包（一个包含 `SKILL.md` 的目录），为 Claude 提供领域专业知识、工作流和工具使用指南。Skill 将 Claude 从通用 Agent 转变为具备特定领域能力的专用 Agent。

### Skill vs CLAUDE.md

| 维度 | CLAUDE.md | SKILL.md |
|------|-----------|----------|
| 用途 | 项目级系统提示（始终加载） | 按需技能（触发时加载） |
| 位置 | 项目根目录 | `.claude/skills/<name>/SKILL.md` |
| 加载时机 | 每个会话自动加载 | 仅 Claude 判定相关时触发 |
| 适合内容 | 构建命令、代码规范、架构 | 领域知识、工作流、可复用能力 |

---

## 二、官方 Skill 规范

### 2.1 目录结构

```
my-skill/
├── SKILL.md            # [必需] 入口文件：frontmatter + Markdown 指令
├── references/         # [可选] 补充文档，Claude 按需加载
│   └── advanced.md
├── scripts/            # [可选] 可执行脚本 (Python/Bash/Node.js)
│   └── helper.py
├── assets/             # [可选] 模板、图片等资源
└── templates/          # [可选] 模板文件
```

### 2.2 存放位置（优先级从高到低）

| 位置 | 作用域 | 是否可提交 |
|------|--------|-----------|
| `.claude/skills/<name>/` | **项目级** — 团队共享 | ✅ 可提交到 Git |
| `~/.claude/skills/<name>/` | **用户级** — 所有项目可用 | ❌ 个人配置 |
| 企业级部署 | **组织级** — 全公司可用 | 取决于部署方式 |

项目级优先于用户级。

### 2.3 渐进式加载（Progressive Disclosure）

Skill 采用**三层加载模型**以节省上下文窗口：

| 层级 | 内容 | 加载时机 | Token 预算 |
|------|------|----------|-----------|
| L1 — 元数据 | `name` + `description` | Agent 启动时发现 | ~100 tokens/技能 |
| L2 — 指令 | 完整的 `SKILL.md` 正文 | 技能被激活时 | < 5000 tokens |
| L3 — 资源 | `references/` `scripts/` `assets/` | 按需加载 | 按需 |

**原则：保持 SKILL.md 精简，将详细信息移到 `references/` 目录。**

---

## 三、SKILL.md 完整模板

```markdown
---
name: my-skill
description: >-
  Use this skill when [具体场景]。Handles [任务类型] and [任务类型]。
  Triggered by: [触发关键词列表]。
---

# My Skill

## Purpose
简要描述本技能的目的和适用场景。

## When to Use
- 当用户要求 [场景 A] 时
- 当涉及 [领域 B] 的工作时
- 当需要 [任务 C] 时

## When NOT to Use
- 当 [排除场景] 时 —— 应使用其他技能
- 在 [不适用条件] 下

## Workflow / Steps
1. **Step 1**：描述第一步
2. **Step 2**：描述第二步
3. **Step 3**：描述第三步

## Constraints
- Always [必须遵守的规则]
- Never [禁止的行为]
- 输出必须使用 [格式要求]

## Examples

### ✅ Do This（正确做法）
```text
输入示例 → 期望的输出示例
```

### ❌ Not This（错误做法）
```text
输入示例 → 错误的输出示例
```

## Notes
- 边界情况说明
- 已知限制
- 与其他技能的交互注意事项
```

---

## 四、Frontmatter 字段详解

### 4.1 必需字段

| 字段 | 说明 | 约束 |
|------|------|------|
| `name` | 技能名称，同时也是斜杠命令（`/my-skill`） | 最多 64 字符，小写字母+数字+连字符，不能以连字符开头/结尾，**建议与目录名一致** |
| `description` | 技能描述，Claude 据此判断何时自动触发 | 最多 200 字符（官方建议），要包含具体触发关键词 |

### 4.2 可选字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `version` | string | 版本号，如 `1.0.0` |
| `license` | string | 许可证名称或引用 |
| `dependencies` | string | 依赖的软件包，如 `python>=3.8, pandas>=1.5.0` |
| `compatibility` | string | 环境兼容性要求（最多 500 字符） |
| `metadata` | mapping | 任意键值对，如 `author`, `tags` |
| `allowed-tools` | string | **权限豁免**：空格分隔的工具列表，技能激活时免审批使用 |
| `disable-model-invocation` | boolean | `true` = 仅用户可通过 `/name` 手动调用，Claude 不自动触发 |
| `user-invocable` | boolean | `false` = 从 `/` 菜单隐藏，仅作为后台知识 |
| `context` | string | `inherit`（默认，主会话中运行）或 `fork`（隔离子 Agent 中运行） |
| `agent` | string | 与 `context: fork` 配合，指定子 Agent 类型（`Explore`/`Plan`/`general-purpose`） |
| `model` | string | 覆盖模型，如 `haiku` / `sonnet` / `opus` |
| `effort` | string | 覆盖推理努力程度：`low` / `medium` / `high` / `xhigh` / `max` |
| `argument-hint` | string | CLI 自动补全提示文字，如 `[issue-number]` |
| `hooks` | object | 技能作用域内的生命周期钩子 |
| `paths` | string/list | Glob 模式，限定技能仅在匹配文件时自动激活 |
| `shell` | string | `` !`command` `` 块的 shell 类型：`bash`（默认）或 `powershell` |
| `when_to_use` | string | 附加触发短语/场景描述（与 description 合并，总共约 1536 字符） |

### 4.3 `allowed-tools` 语法

```yaml
# 基础用法：列出工具名
allowed-tools: Read Grep Glob Write

# 带 Bash 命令模式匹配
allowed-tools: Read Write Bash(git *) Bash(npm run *)

# 带 MCP 工具（双下划线格式）
allowed-tools: Read mcp__linear__create_issue
```

常用工具名（大小写敏感）：`Read`, `Write`, `Edit`, `Grep`, `Glob`, `Bash`, `WebFetch`, `WebSearch`

### 4.4 `context: fork` 用法

```yaml
---
name: research-task
description: Perform deep research in isolated context
context: fork
agent: Explore
model: haiku
---
```

适用场景：长时间分析、子任务派发、研究探索、任何不希望污染主会话上下文的工作。

### 4.5 完整 Frontmatter 示例

```yaml
---
name: code-reviewer
description: >-
  Review code changes for bugs, security issues, and best practices.
  Triggered by: "review this", "check my code", "code review", "CR".
version: 2.0.0
license: MIT
metadata:
  author: team-engineering
  tags: code-quality, review, best-practices
allowed-tools: Read Grep Glob
disable-model-invocation: false
context: fork
agent: general-purpose
model: sonnet
argument-hint: "[file or directory]"
hooks:
  PreToolUse:
    - command: rtk git diff
shell: bash
---
```

---

## 五、Skill 编写注意事项

### 5.1 描述（Description）是最关键的字段

- Claude 通过 `description` 判断是否自动加载技能
- **要具体**：列出用户可能说的触发短语
  - ❌ "Handles code review"
  - ✅ "Review code for bugs, security issues. Triggered by: 'review this', 'CR', 'check my code'"
- **略微激进（slightly pushy）**：宁可误触发也不要漏触发
- **第三人称**：描述技能做什么，而非"我"做什么

### 5.2 指令编写风格

- **祈使句 + 动词开头**："Extract text with pdfplumber" 而非 "You should extract text..."
- **用 Always/Never 明确约束**：
  - "Always use full-color logo on light backgrounds"
  - "Never modify files under `components/ui/`"
- **提供 Do This / Not This 对比**：比抽象规则更有效
- **包含具体示例**：输入/输出对校准 Claude 的输出格式

### 5.3 SKILL.md 体量控制

- **正文保持在 500 行 / 2000 词以内**
- 详细信息移到 `references/` 子目录
- 所有引用文件应从 SKILL.md 直接链接（最多一层深度，避免深层嵌套）
- 信息要么在 SKILL.md 中，要么在引用文件中，**不要重复**

### 5.4 技能粒度

- **单一职责**：一个技能只做一件事
- 多个小型技能比一个大型技能更灵活
- 可以组合使用（一个技能引用另一个技能）

### 5.5 参数传递

在 SKILL.md 正文中使用 `$ARGUMENTS` 占位符：

```markdown
# In SKILL.md
分析以下数学建模问题并给出解决方案：$ARGUMENTS
```

用户输入 `/my-skill 2024年美赛C题` → Claude 收到："分析以下数学建模问题并给出解决方案：2024年美赛C题"

也支持位置参数：`$0`, `$1`, `$2` 或 `$ARGUMENTS[0]`, `$ARGUMENTS[1]`。

### 5.6 动态预处理

使用 `` !`shell command` `` 语法在 Claude 看到技能前执行命令并插入输出：

```markdown
当前 Git 分支：!`git branch --show-current`
```

### 5.7 安全注意事项

- 对于破坏性操作（部署、提交、删除），设置 `disable-model-invocation: true`，仅允许手动调用
- 使用 `allowed-tools` 限制技能可用的工具范围
- 敏感操作放在 `scripts/` 中并需要显式确认

### 5.8 测试与迭代

1. 用 `/skills` 检查技能是否显示并已启用
2. 用显式命令测试：`/your-skill-name`
3. 用自然语言测试：检查描述中的触发词是否能自动激活
4. 如果不触发，**收紧描述**：添加更多触发短语
5. 使用 Anthropic 的 skill-creator 的 eval 功能跟踪通过率和回归

### 5.9 已知问题

- VS Code 扩展的验证器（v2.1.39）只识别基础 Agent Skills 标准字段，会误报 `allowed-tools`、`context: fork`、`agent`、`model` 等扩展字段的警告，但不影响运行时功能。

---

## 六、Skill 结构总结

```
                  ┌─────────────────────────────────────┐
                  │           SKILL.md                   │
                  │  ┌───────────────────────────────┐   │
                  │  │  ---                          │   │
                  │  │  name: my-skill              │   │  L1: 元数据
                  │  │  description: ...            │   │  (~100 tokens)
                  │  │  ---                          │   │
                  │  ├───────────────────────────────┤   │
                  │  │  # 正文（< 5000 tokens）     │   │  L2: 指令
                  │  │  ## When to Use               │   │  (触发时加载)
                  │  │  ## Constraints               │   │
                  │  │  ## Examples                  │   │
                  │  │  ...                          │   │
                  │  └───────────────────────────────┘   │
                  └─────────────────────────────────────┘
                              │
            ┌─────────────────┼─────────────────┐
            ▼                 ▼                 ▼
    ┌────────────┐   ┌──────────────┐   ┌──────────────┐
    │references/ │   │  scripts/   │   │   assets/    │  L3: 资源
    │ 补充文档   │   │ 可执行脚本  │   │ 模板/素材    │  (按需加载)
    └────────────┘   └──────────────┘   └──────────────┘
```

### 核心设计原则

1. **描述驱动触发**：description 是 Claude 判断是否加载技能的唯一依据，必须包含具体触发词
2. **渐进式加载**：元数据 → 指令 → 资源，三层递进节省上下文
3. **指令优先于信息**：教 Claude "如何做"而非"是什么"
4. **示例优于抽象**：具体的 Do/Not This 对比比抽象规则更有效
5. **单一职责**：每个技能只聚焦一个领域

---

## 七、参考资源

- [Anthropic 官方 — How to create custom Skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)
- [Agent Skills 开放标准 (agentskills.io)](https://agentskills.io) — 跨平台兼容规范
- [Agent Skills 规范 GitHub 仓库](https://github.com/agentskills/agentskills) — 完整规范文档
- [Anthropic 官方 Skill 示例库](https://github.com/anthropics/skills)
- [Claude Code 官方文档](https://docs.anthropic.com/en/docs/claude-code)
- [freeCodeCamp — How to Build Your Own Claude Code Skill](https://www.freecodecamp.org/news/how-to-build-your-own-claude-code-skill/)
- [SitePoint — Claude Agent Skills Tutorial](https://www.sitepoint.com/claude-agent-skills-tutorial/)
- [Sherlock — How to Write Skills for Claude Code and Cowork](https://sherlock.xyz/post/how-to-write-skills-for-claude-code-and-cowork)
- [Anthropic Skill-Creator 改进博客](https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills)
- [Awesome Claude Code Skills (社区合集)](https://github.com/robertguss/claude-code-toolkit)
- [CLAUDE.md 完整配置指南](https://www.morphllm.com/claude-md-guide)
