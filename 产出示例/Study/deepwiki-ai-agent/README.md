# DeepWiki AI Agent

## 简介

一个纯 AI 驱动的代码仓库 Wiki 生成和分析工具。完全替代 DeepWiki 项目的全套功能 — 仓库分析、Wiki 自动生成、代码问答、深度研究、文档导出 — 全部使用 Claude 的内置能力，**零外部依赖**。无需运行 FastAPI 服务器、无需 FAISS 向量数据库、无需配置 LLM Provider。

## 与原 DeepWiki 的对比

| 维度 | 原 DeepWiki | DeepWiki AI Agent |
|------|------------|------------------|
| 架构 | Next.js + FastAPI + Adalflow + FAISS + Docker | **纯 Claude，无服务** |
| 代码理解 | Git clone → TextSplitter → Embedding → FAISS 检索 | Claude 直接读取和理解代码 |
| RAG 检索 | FAISS top_k=20 相似度检索 | Claude 全局代码理解 + 精确搜索 |
| 问答 | simple_chat.py + rag.py + LLM Provider | Claude 原生代码分析能力 |
| Provider 支持 | 8 个 LLM Provider + 4 个 Embedder | Claude 本身（无需配置） |
| 部署 | Docker Compose (3 个容器) | **不需要部署** |
| 安装依赖 | Python 3.11 + Node.js + Ollama + 20+ pip 包 | **零依赖** |
| 导出 | FastAPI 端点 + Content-Disposition | Write 工具直接输出文件 |

## 目录结构

```
deepwiki-ai-agent/
├── SKILL.md                    # 技能主文件（5 种工作模式）
├── README.md                   # 本文件
├── references/                 # 分析过程中生成的知识结构（分类文件）
├── wikis/<repo-name>/          # 生成的 Wiki 文档
├── reports/<repo-name>/        # 深度研究报告
├── reviews/                    # 代码审查报告
└── exports/                    # 导出的文档（Markdown/JSON/HTML）
```

## 安装方式

1. 将 `deepwiki-ai-agent/` 目录复制到 `.claude/skills/` 下
2. 重新启动 Claude Code
3. 使用 `/deepwiki-ai-agent` 或触发关键词激活

无需安装任何依赖、无需启动任何服务、无需任何环境变量配置。

## 使用方式

### 自动触发

当用户输入以下关键词时自动激活：
- "deepwiki"、"wiki project"、"analyze repo"
- "codebase wiki"、"document code"、"repo analysis"
- "代码分析"、"项目文档"、"仓库 wiki"
- "code Q&A"、"deep research"、"研究代码库"

### 5 种工作模式

#### 模式 A — Wiki 自动生成
```
用户: "分析这个 Go 项目并生成 Wiki 文档"
→ 输出: references/ + wikis/<repo-name>/ 下的结构化文档
```

#### 模式 B — 代码问答
```
用户: "这个仓库中的认证模块是如何工作的？"
→ 输出: 含代码引用和数据流图的精准回答
```

#### 模式 C — 深度研究
```
用户: "全面分析这个项目的架构设计和质量"
→ 输出: 5 轮递进分析 + reports/<repo-name>/ 综合报告
```

#### 模式 D — 文档导出
```
用户: "将生成的 Wiki 导出为 Markdown 格式"
→ 输出: exports/<repo-name>_wiki_<timestamp>.md
```

#### 模式 E — 代码审查
```
用户: "审查这个项目的安全性"
→ 输出: reviews/ 下的结构化审查报告
```

## Workflow 说明

本 Skill 根据用户意图自动选择工作模式。Wiki 生成流程：获取仓库 → 扫描结构 → 深度阅读关键文件 → 构建知识结构（references/） → 生成 Wiki 页面（wikis/）。代码问答流程：理解问题 → 直接搜索和阅读相关代码 → 输出含引用的回答。深度研究流程：自动执行最多 5 轮递进分析，每轮基于前一轮发现深入。

## 技术细节

### 依赖

**零外部依赖。** 仅使用 Claude Code 内置工具：
- `Read` / `Write` / `Edit` — 文件读写
- `Grep` / `Glob` — 代码搜索和文件定位
- `Bash` — 仅用于 `git clone --depth 1` 获取远程仓库
- `WebSearch` / `WebFetch` — 获取外部上下文（如框架文档）

### 输出说明

所有输出文件按分类保存在 `deepwiki-ai-agent/` 下的子目录中：
- `references/` — 分析过程知识结构
- `wikis/<repo-name>/` — 生成的 Wiki 文档
- `reports/<repo-name>/` — 深度研究报告
- `reviews/` — 代码审查报告
- `exports/` — 导出的文档

## 注意事项

- 分析大型仓库时，Claude 上下文窗口有限，建议指定关键目录分析
- 私有仓库需要先在本地克隆，然后使用本地路径分析
- 远程仓库使用 `git clone --depth 1` 浅克隆以加速
- 分析完成后会询问是否清理临时克隆
- 发现的敏感信息（API Key、Token）会自动标记
