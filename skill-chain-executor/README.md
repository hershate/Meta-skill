# Skill Chain Executor

## 简介
自动执行 `skill-chain-planner` 生成的 Skill 链规划。读取规划目录，按优先级和依赖顺序，逐一递归调用 `skill-for-skills` 为每个子 Skill 生成 SKILL.md 和 README.md。本 Skill 不自已创建任何文件——所有生成工作委托给 `skill-for-skills`。

## 目录结构
```
skill-chain-executor/
├── SKILL.md            # 技能主文件
└── README.md           # 本文件
```

## 安装方式
1. 将 `skill-chain-executor/` 目录复制到项目 `.claude/skills/skill-chain-executor/` 下
2. 重新启动 Claude Code
3. 使用 `/chain-executor` 或触发关键词激活

## 使用方式

### 斜杠命令
`/chain-executor <规划目录路径>` — 执行指定的 Skill 链规划

参数说明：
- `<规划目录路径>`：`skill-chain-planner` 输出的规划目录路径
- 示例：`/chain-executor skill-chain-planner/plans/pdf-to-study/`

### 自动触发
当用户输入以下关键词时自动激活：
- "执行skill链"
- "创建skill链"
- "批量创建skill"
- "按照规划创建"

## Workflow 说明
1. 读取规划目录，解析 `chain-overview.md` 获取子 Skill 清单和依赖关系
2. 按优先级（P0 → P1 → P2）和依赖顺序排序
3. 验证已有 Skill 是否就绪
4. 对每个需新建的子 Skill，将规格文件内容传递给 `skill-for-skills`，由后者生成 SKILL.md
5. 逐个验证创建结果，失败时暂停并询问用户
6. 输出完整执行报告

## 前置依赖

### 必须
- **skill-for-skills** — 本 Skill 的核心委托目标。必须已注册在 `.claude/skills/` 中。
- **skill-chain-planner**（或其输出的规划目录）— 本 Skill 读取的规划必须是 `skill-chain-planner` 的标准输出格式。

### 推荐工作流
```
skill-chain-planner → skill-chain-executor → 逐个 skill-for-skills
     (分解)               (编排/执行)            (生成)
```

## 技术细节

### 使用的工具
- `Read` — 读取链规划文件、子 Skill 规格文件
- `Glob` — 搜索已有 Skill 的 SKILL.md
- `Skill` — 调用 `skill-for-skills` 生成子 Skill

### Skill 调用链
```
skill-chain-executor
  └── skill-for-skills (递归调用，每子 Skill 一次)
       └── 生成子 Skill 的 SKILL.md + README.md
```

### 输出说明
- 本 Skill **不自已生成任何文件**——所有输出由 `skill-for-skills` 创建
- 新建的子 Skill 位于项目根目录的 `<skill-name>/` 下
- 执行报告在 Claude 会话中以 Markdown 格式输出

## 规划目录格式要求

本 Skill 读取的规划目录必须符合 `skill-chain-planner` 的输出标准：

```
<plan-dir>/
├── chain-overview.md        # [必需] 链架构总览（含依赖关系矩阵）
├── skills/                   # [必需] 子 Skill 创建规格
│   ├── skill-P0-<name>.md
│   ├── skill-P1-<name>.md
│   └── ...
├── usage-guide.md            # [可选]
├── risk-register.md          # [可选]
└── implementation-roadmap.md # [可选]
```

## 注意事项
- skill-for-skills 必须已注册，否则本 Skill 无法工作
- 创建完成后，仍需手动将新 Skill 目录复制到 `.claude/skills/` 完成注册
- 创建失败时流程会暂停，等待用户指示
- 已有 Skill 如果缺少 README.md 会记录警告但不中断流程
