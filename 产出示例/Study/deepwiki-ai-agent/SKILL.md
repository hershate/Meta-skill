---
name: deepwiki-ai-agent
description: >-
  A pure-AI replacement for the entire DeepWiki pipeline: analyze code
  repositories, generate structured Wiki documentation, answer codebase
  questions via simulated RAG, perform deep multi-turn research, and
  export documentation — all using only Claude's built-in capabilities
  with zero external dependencies. No servers, no FAISS, no LLM providers,
  no Docker. Triggered by: "deepwiki", "wiki project", "analyze repo",
  "codebase wiki", "document code", "repo analysis", "代码分析",
  "项目文档", "仓库 wiki", "code Q&A", "deep research", "研究代码库".
allowed-tools: Read Write Edit Grep Glob Bash WebSearch WebFetch
context: fork
agent: general-purpose
---

# DeepWiki AI Agent

## Purpose

完全替代 DeepWiki 项目的全套功能 — 仓库分析、Wiki 自动生成、代码问答、深度研究、文档导出 — 全部使用纯 AI 工作流，无需运行任何后端服务、数据库或第三方依赖。Claude 本身即充当**代码理解引擎**、**检索系统**和**生成器**三位一体的角色。

## When to Use

- 需要为一个代码仓库自动生成 Wiki 文档（替代 DeepWiki 的 Wiki 生成功能）
- 需要问答式探索一个仓库的代码结构和逻辑（替代 DeepWiki 的 RAG Q&A 和 Deep Research）
- 需要将仓库分析结果导出为结构化的 Markdown 或 JSON 文档（替代 Wiki 导出功能）
- 需要多轮深度研究一个代码库的设计模式、数据流和架构决策（替代 Deep Research）
- 需要比较多个仓库的架构和实现方式

## When NOT to Use

- 只需要查看单个文件的内容 — 应直接使用 Read 工具
- 需要运行或调试代码 — 这不是 CI/CD 工具
- 需要实时协作编辑 Wiki — 导出是一次性快照
- 用户已有可运行的后端基础设施 — DeepWiki 项目本身仍适合生产部署

## Workflow / Steps

### 模式选择

本 Skill 根据用户意图自动选择以下工作模式之一：

| 模式 | 适用场景 | 对应 DeepWiki 功能 |
|------|---------|-------------------|
| 模式 A — Wiki 生成 | 用户要求"分析仓库""生成文档""创建 Wiki" | Wiki Generation |
| 模式 B — 代码问答 | 用户对仓库提出具体问题 | RAG Q&A + Chat |
| 模式 C — 深度研究 | 用户要求"深入研究""全面分析" | Deep Research |
| 模式 D — 文档导出 | 用户要求"导出""下载文档" | Wiki Export |
| 模式 E — 代码审查 | 用户要求"审查代码""评估质量" | (增强功能) |

---

### 模式 A — Wiki 自动生成

替代 DeepWiki 的仓库克隆 → 分块 → 嵌入 → 索引 → 生成 Wiki 的完整管道。

#### Step A1: 获取仓库

从用户输入中解析仓库 URL（支持 GitHub、GitLab、Bitbucket）。

- 如果仓库在本地已有路径，直接使用 Glob 扫描
- 如果是远程 URL，使用 `rtk git clone --depth 1 <url> /tmp/deepwiki-analysis/` 浅克隆到临时目录
- 验证克隆成功，如果失败则提示用户检查 URL 或使用本地路径

#### Step A2: 扫描仓库结构

使用 Glob 和 Grep 扫描仓库的文件结构：

```
文件清单：
├── 入口文件（package.json, Cargo.toml, pyproject.toml 等）
├── 源代码（src/, lib/, api/ 等）
├── 配置文件（config/, .env.example, docker-compose.yml 等）
├── 测试文件（tests/, *_test.go, *.spec.ts 等）
└── 文档（README*, docs/, *.md 等）
```

识别项目的**技术栈**：读取构建配置文件确定语言、框架和依赖。

#### Step A3: 深度阅读关键文件

使用 Read 工具按优先级顺序读取关键文件：

1. **项目元文件**：README.md、package.json/Cargo.toml/pyproject.toml — 理解项目身份
2. **架构入口**：main.rs、main.py、src/index.ts、app.py — 理解启动流程
3. **核心模块**：API 路由定义、核心数据结构、主要业务逻辑 — 理解功能
4. **配置文件**：Dockerfile、CI/CD、环境变量 — 理解部署模式

对于每个文件，同时使用 Read 和相关上下文工具提取：
- 函数签名和类型定义
- 数据流接口（输入/输出）
- 外部依赖和 API 调用
- 错误处理模式

#### Step A4: 构建知识结构

在 `./deepwiki-ai-agent/references/` 下创建分类知识文件：

```
references/
├── 01-project-overview.md     # 项目概览、技术栈、架构图（Mermaid）
├── 02-core-architecture.md    # 核心架构分层、模块依赖、数据流
├── 03-api-endpoints.md        # API 路由表、请求/响应格式
├── 04-data-models.md          # 核心数据结构和类型定义
├── 05-workflows.md            # 关键业务流程的状态机/序列图
├── 06-configuration.md        # 配置项、环境变量、部署模式
└── 07-dependencies.md         # 外部依赖及其用途
```

每个文件使用结构化格式：
```markdown
---
module: <模块名>
file: <源文件路径>
line: <行号区间>
---

## <功能名>

**签名/接口**：`<类型签名>`

**职责**：<一句话描述>

**数据流**：<输入 → 处理 → 输出>

**依赖关系**：<调用的内部模块和外部服务>

**代码引用**：<关键代码片段或位置>
```

#### Step A5: 生成 Wiki 页面

基于 references/ 中的分析数据，在 `./deepwiki-ai-agent/wikis/<repo-name>/` 下生成结构化的 Wiki 文档：

```
wikis/<repo-name>/
├── index.md                 # Wiki 首页：项目简介 + 目录
├── getting-started.md       # 快速开始：安装、配置、运行
├── architecture.md          # 架构设计：分层、模块、数据流图
├── api-reference.md         # API 参考：端点、参数、示例
├── data-model.md            # 数据模型：核心类型、关系
├── development.md           # 开发指南：如何贡献、测试
├── deployment.md            # 部署指南：环境、配置
├── faq.md                   # 常见问题
└── glossary.md              # 术语表
```

每个 Wiki 页面包含：
- YAML 元数据头（标题、来源文件、生成时间）
- Mermaid 图表（架构图、流程图）
- 核心文件路径引用（方便用户定位源码）
- 相关页面的交叉链接

#### Step A6: 交互式确认

向用户输出 Wiki 生成报告，确认覆盖率后可进行补充分析或导出。

---

### 模式 B — 代码问答

替代 DeepWiki 的 RAG + LLM 问答管道。Claude 直接使用其代码理解能力回答问题，无需向量检索。

#### Step B1: 理解问题范围

解析用户问题，确定需要的信息类型：

| 问题类型 | 需要的信息 | 对应 DeepWiki RAG 检索 |
|---------|-----------|----------------------|
| "这个函数是做什么的？" | 函数定义、调用者、被调用者 | FAISS top_k 相似文档 |
| "认证流程是怎样的？" | 中间件链、路由保护、token 验证 | Wiki Structure |
| "如何添加新 API？" | 路由注册、请求验证、响应格式 | 项目代码分析 |
| "性能瓶颈在哪？" | 资源使用、循环/递归、I/O 操作 | 代码整体理解 |

#### Step B2: 检索相关信息

使用 Claude 的本机「多文件协同阅读」能力 — 同时读取多个相关文件：

- 使用 `Grep` 搜索相关函数/类/模块的定义和引用
- 使用 `Glob` 定位相关文件
- 使用 `Read` 读取关键代码片段（每段 30-50 行，聚焦于接口和数据流）
- 使用 `WebSearch`（仅当需要外部上下文时，如框架文档）

#### Step B3: 构建回答

生成包含以下结构的回答：
1. **直接回答** — 针对问题的结论
2. **代码引用** — 关键文件/行号位置
3. **上下文说明** — 数据流、调用链、设计决策
4. **相关链接** — 其他相关文件或 Wiki 页面的交叉引用

#### Step B4: 支持多轮对话

维护对话上下文，支持追问和深入：
- "继续深入" → 进一步阅读相关实现细节
- "那错误处理呢？" → 切换到相关代码路径
- "和 XXX 有什么关系？" → 跨模块关联分析

---

### 模式 C — 深度研究

替代 DeepWiki 的 Deep Research 多轮迭代功能。自动进行多轮递进式分析，每轮基于前一轮发现深入。

#### Step C1: 初始扫描

执行仓库的全面初步分析（同模式 A 的 Step A2-A3），生成初始知识文件到 `references/`。

#### Step C2: 多轮递进分析

自动执行最多 5 轮分析，每轮聚焦不同维度：

| 轮次 | 分析维度 | 关键问题 | 输出文件 |
|------|---------|---------|---------|
| 1 | **项目身份** | 项目定位、技术栈、社区活跃度 | `references/01-project-overview.md` |
| 2 | **架构设计** | 分层、模块划分、接口契约 | `references/02-core-architecture.md` |
| 3 | **数据流** | 核心路径的数据变换、状态管理 | `references/03-data-flow.md` |
| 4 | **质量评估** | 测试覆盖、错误处理、安全实践 | `references/04-quality.md` |
| 5 | **改进建议** | 架构问题、技术债务、优化机会 | `references/05-recommendations.md` |

**轮次间逻辑**：
- 每轮开始时，自动读取上一轮生成的分析文件作为上下文
- 每轮结束时，判断是否已经达到分析充分性标准：
  - 覆盖了全部核心模块
  - 无重大未解答问题
  - 分析深度满足用户初始要求
- 如果达到标准，提前终止后续轮次

#### Step C3: 生成研究报告

在 `./deepwiki-ai-agent/reports/<repo-name>/` 下生成综合研究报告：

```
reports/<repo-name>/
├── executive-summary.md     # 执行摘要（3-5 段）
├── architecture.md          # 架构深度分析
├── data-flow-analysis.md    # 数据流分析
├── quality-assessment.md    # 质量评估
├── recommendations.md       # 改进建议
└── full-report.md           # 完整报告（合成所有章节）
```

#### Step C4: 输出摘要

向用户输出研究报告的要点摘要和高价值发现。

---

### 模式 D — 文档导出

替代 DeepWiki 的 Wiki Export 功能。将生成的 Wiki 或分析结果导出为指定格式。

#### Step D1: 解析导出需求

- 确定导出内容范围（全部 Wiki、单章节、分析报告）
- 确定导出格式（Markdown、JSON、HTML）
- 确定输出位置

#### Step D2: 生成 Markdown 导出

- 创建包含仓库名称、生成时间、页面数量的元数据头
- 生成目录（Table of Contents）— 按标题层级自动构建
- 遍历所有 Wiki 页面，生成完整文档：
  - 页面锚点：`<a id='{page-id}'></a>`
  - 页面标题、内容、交叉链接
  - 页面间分隔线

#### Step D3: 生成 JSON 导出（可选）

- 构建包含 metadata（repository、generated_at、page_count）的结构
- 将所有 Wiki 页面序列化为结构化 JSON
- 使用 indent=2 格式化

#### Step D4: 生成 HTML 导出（可选）

- 将所有 Markdown 转换为单页 HTML
- 包含导航侧边栏
- 嵌入样式使其可直接在浏览器中打开

#### Step D5: 写入输出文件

将导出内容写入 `./deepwiki-ai-agent/exports/` 目录，包含文件名 `{repo-name}_wiki_{timestamp}.{fmt}`。

---

### 模式 E — 代码审查（增强功能）

利用 Claude 的代码理解能力提供超越原 DeepWiki 的代码审查功能。

#### Step E1: 理解审查范围

确定审查焦点：安全、性能、架构、风格或全量。

#### Step E2: 执行审查

- 使用 Grep 搜索常见反模式
- 使用 Read 阅读关键代码段
- 识别：未处理的错误、潜在 NPE、资源泄漏、并发问题、类型安全漏洞

#### Step E3: 输出审查报告

在 `./deepwiki-ai-agent/reviews/` 下输出结构化审查报告，包含问题分类、严重级别、文件位置和修复建议。

---

### 通用步骤（所有模式共享）

#### 仓库清理

分析完成后，如果创建了临时克隆，询问用户是否清理：
```
rm -rf /tmp/deepwiki-analysis/
```

#### 错误处理

| 场景 | 处理方式 |
|------|---------|
| 仓库 URL 无效 | 提示用户检查 URL，提供备选方案（本地路径） |
| 克隆超时/失败 | 提示大仓库可只分析关键目录，使用 `--depth 1` 或 `--filter` |
| 文件读取编码问题 | 尝试多种编码（utf-8, latin-1, utf-16），跳过无法解析的文件 |
| 语言/框架不识别 | 基于常见构建文件启发式判断，未知时询问用户 |
| 私有仓库访问 | 提示用户本地克隆后使用本地路径分析 |

## Constraints

- Never install or require any external dependencies (no Python packages, no Node modules, no Docker). Use only Claude's built-in tools.
- Never start a server or daemon process — all work is done through direct file I/O and tool calls
- Always use `rtk` prefix for git clone and other shell commands
- Always organize output files under `./deepwiki-ai-agent/<category>/<repo-name>/` structure
- Always generate Mermaid diagrams for architecture and data flow visualization
- Always include file path and line number references when citing code
- Never delete or modify files in the analyzed repository
- Always clean up temporary cloned repositories unless the user asks to keep them
- Always handle encoding errors gracefully — log the issue and continue
- Always ask for clarification when the repository structure is ambiguous
- Never hardcode analysis depth — adapt based on repository size and user needs
- Always generate a summary report at the end of each analysis round
- Always limit deep research to maximum 5 rounds unless the user requests more
- Never expose potentially sensitive information (API keys, tokens found in files) — flag them to the user instead

## Examples

### ✅ Do This — 生成仓库 Wiki

```text
用户: "为这个 Go 项目生成 Wiki 文档"
结果:
  - deepwiki-ai-agent/references/ 下生成结构化知识文件（7 个模块）
  - deepwiki-ai-agent/wikis/go-project/ 下生成 Wiki 页面（index, architecture, API, data-model 等）
  - 所有页面包含 Mermaid 图表和源码引用
```

### ✅ Do This — 代码问答

```text
用户: "这个项目中的认证流程是怎样的？"
结果:
  - 使用 Grep 搜索 auth/login/token/middleware 相关代码
  - 读取关键文件中的认证逻辑
  - 输出包含调用链、关键文件位置、数据流的回答
  - 支持多轮追问
```

### ✅ Do This — 深度研究

```text
用户: "深入研究这个仓库的架构设计"
结果:
  - 第 1 轮：项目概览和技术栈识别
  - 第 2 轮：核心架构和模块依赖分析
  - 第 3 轮：数据流和状态管理
  - 第 4 轮：错误处理和安全评估
  - 第 5 轮：改进建议
  - 综合报告在 reports/ 目录
```

### ❌ Not This

```text
❌ pip install adalflow faiss-cpu  # 引入了外部依赖
❌ docker-compose up               # 启动了服务
❌ 回答问题时只给出笼统描述，不引用具体代码位置
❌ 分析完成后不清理临时克隆的仓库
❌ 在仓库根目录下创建大量文件，混入项目代码
```

## Notes

- 本 Skill **零外部依赖** — 所有功能基于 Claude 的内置工具（Read, Write, Grep, Glob, Bash, WebSearch, WebFetch）
- 模式 A（Wiki 生成）替代了原 DeepWiki 的 `data_pipeline.py` + `rag.py` + `api.py` 的完整管道
- 模式 B（代码问答）替代了原 DeepWiki 的 `simple_chat.py` + `rag.py` + LLM Provider 客户端
- 模式 C（深度研究）替代了原 DeepWiki 的 Deep Research 多轮迭代 + WebSocket 通信
- 模式 D（文档导出）替代了原 DeepWiki 的 `export_wiki` + `generate_markdown_export` + `generate_json_export`
- 所有输出文件路径为 `./deepwiki-ai-agent/<category>/<repo-name>/`，遵循分类组织原则
- 大型仓库（>1000 文件）应建议用户指定关键目录以加速分析
- WebSearch 仅用于获取外部上下文（如框架文档），不用于代码理解
