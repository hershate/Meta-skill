# PPT Slide Builder

## 简介

PPT 风格全屏网页演示文稿生成器。支持**统一样式管理**、**多页面增删改**、**元素入场动画**和**页面过渡动画**。生成纯静态 HTML，无需任何构建工具或外部依赖，双击即可在浏览器中全屏播放。

## 目录结构

```
ppt-slide-builder/
├── SKILL.md                       # 技能主文件
├── README.md                      # 本文件
├── templates/
│   └── base.html                  # 演示文稿基础模板
├── references/
│   └── animation-reference.md     # 动画与过渡效果完整参考
└── <project-name>/                # 生成的演示项目（在当前工作目录下）
    └── index.html                 # 单个完整的演示文件
```

## 安装方式

1. 将 `ppt-slide-builder/` 目录复制到项目 `.claude/skills/` 下
2. 重新启动 Claude Code
3. 使用 `/ppt-slide-builder` 或触发关键词激活

## 使用方式

### 斜杠命令

```
/ppt-slide-builder <操作描述>
```

示例：
```
/ppt-slide-builder 创建一个科技主题的 PPT，标题为"2025 年度技术回顾"
/ppt-slide-builder 在第 3 页后面添加一页产品路线图
/ppt-slide-builder 给第 1 页的标题添加淡入动画
/ppt-slide-builder 把翻页过渡改成缩放效果
/ppt-slide-builder 把主题改成深色模式
/ppt-slide-builder 删除第 2 页
```

### 自动触发

当用户输入包含以下关键词时自动激活：
- "制作PPT"、"PPT网页"、"幻灯片"、"演示页面"
- "presentation"、"slide deck"、"slide builder"
- "添加动画"、"页面过渡"、"翻页动画"
- "新建幻灯片"、"修改幻灯片"、"删除幻灯片"
- "演示文稿"、"slides"

## Workflow 说明

1. **初始化项目** — 逐轮提问收集需求（标题/风格/页数/内容）→ 12 维度系统性分析优化项目规约 → 严格按照规约从模板生成 HTML → 执行质量检查 + 输出生成报告（含设计摘要和修改指引）→ 浏览器预览
2. **添加幻灯片** — 向用户确认新幻灯片内容和布局后在末尾追加，自动编号
3. **修改幻灯片内容** — 通过 slide 标记精确定位，仅修改内容区域
4. **添加图片** — 支持本地图片（复制到项目目录 + 相对路径引用）和网络图床链接（WebSearch 验证），根据用户指定的页面位置精准插入
5. **添加入场动画** — 为指定 slide 中的元素添加 CSS 动画 class
6. **修改页面过渡** — 设置整体过渡类型（淡入、滑动、缩放、翻转等）
7. **修改主题样式** — 用户要求模糊时追问具体风格方向，通过 CSS 变量统一修改
8. **删除幻灯片** — 移除目标 slide 并重新编号所有后续 slide
9. **预览** — 在默认浏览器中打开，支持键盘方向键、鼠标滚轮、点击空白区域、触摸滑动四种 PPT 模拟导航方式

## 技术细节

### 动画系统

内置 12 种元素动画和 7 种页面过渡效果，无需编写 CSS：

| 动画类型 | 类名 | 效果 |
|---------|------|------|
| 淡入 | `anim-fade-in` | 透明度从 0 到 1 |
| 上滑 | `anim-slide-up` | 从下方 30px 滑入 |
| 放大 | `anim-scale-in` | 从 0.7 倍放大 |
| 模糊 | `anim-blur-in` | 从模糊到清晰 |
| 翻转 | `anim-flip-in` | 3D 翻转入场 |
| 打字机 | `anim-typewriter` | 逐字显示（短文本） |

支持 `anim-delay-1` 到 `anim-delay-10` 控制错落节奏。

| 过渡类型 | 类名 | 效果 |
|---------|------|------|
| 淡入淡出 | `trans-fade` | 交叉淡入淡出 |
| 左滑 | `trans-slide-left` | 页面向左推入 |
| 缩放 | `trans-zoom` | 缩放过渡 |
| 3D 翻转 | `trans-flip` | 带透视的翻页 |

完整参考见 `references/animation-reference.md`。

### 主题系统

通过 CSS 自定义属性在 `:root` 中统一控制：

```css
:root {
  --bg: #ffffff;              /* 背景色 */
  --text: #1a1a1a;            /* 主文字色 */
  --accent: #3b82f6;          /* 强调色 */
  --font-display: 'Georgia', serif;  /* 展示字体 */
  --font-body: system-ui, sans-serif; /* 正文字体 */
  --slide-padding: 4rem;      /* 幻灯片内边距 */
  --transition-duration: 0.6s; /* 过渡时长 */
}
```

修改主题后所有幻灯片自动生效。

### 使用的工具

- `Read` — 读取项目文件和模板
- `Write` — 创建新项目文件
- `Edit` — 精确修改已有内容
- `Glob` — 查找项目目录
- `Bash` — 在浏览器中打开预览
- `WebSearch` — 验证网络图床链接和外部图片 URL 的有效性

### 输出说明

- 生成的演示文件在当前工作目录的 `<project-name>/index.html`
- 完全自包含，无外部依赖，可离线使用
- 支持五种导航方式：键盘方向键、鼠标滚轮、点击空白区域、屏幕导航按钮、触摸滑动
- 支持 URL hash 定位到指定页（`index.html#slide-3`）

## 注意事项

- 所有操作严格遵循"精确匹配"原则：通过 `<!-- SLIDE: slide-N -->` 注释定位，不使用行号
- 删除幻灯片后会自动重新编号，确保编号连续无空洞
- 主题修改全局生效，不需要逐页调整
- 每个项目是独立文件，不影响其他项目
- **用户输入模糊时，本 skill 会主动逐轮提问**（一次只问 1-2 个问题），而不是自行假设生成
- **生成后自动执行质量检查**（PPT 质量检查清单），通过后输出结构化的**生成报告**（含设计摘要和自定义修改指引）
- 任何对外部 CDN 或占位图服务的引用，会自动先用 `WebSearch` 验证 URL 是否有效
- 生成的演示默认提供 2 页示例内容，可根据需求增删
- 如需占位图片，优先使用 CSS 纯色占位块（不依赖外部服务）
- 所有动画支持 `prefers-reduced-motion` 可访问性设置
- `color-mix()` 用于导航栏背景，需 Chrome 111+ / Firefox 113+ / Safari 16.2+
- 不支持 React/Vue 等框架，仅生成纯静态 HTML
- **添加图片**（Step 4）支持本地文件（自动复制到 `images/` 目录）和网络图床链接（WebSearch 验证后直接引用）
- 如需导出为 PowerPoint 格式，可复制到 Google Slides 或 Keynote 中重新编排
