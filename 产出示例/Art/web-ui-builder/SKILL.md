---
name: web-ui-builder
description: >-
  Design-driven frontend UI page generator that produces distinctive,
  production-grade HTML/CSS/JS pages avoiding generic AI aesthetics.
  Integrates design direction framework (purpose, tone, constraints,
  differentiation) before coding. Creates responsive single-file HTML
  viewable directly in browser without build tools or npm.
  Triggered by: "生成前端UI", "写个网页", "创建页面", "做个界面",
  "生成一个页面", "HTML页面", "浏览器查看", "web UI", "frontend page",
  "仪表板", "表单页面", "产品页", "landing page", "生成网页",
  "设计风格", "网页设计", "前端设计", "UI设计", "landing page",
  "dashboard", "现代风格", "独特设计", "design system".
version: 2.0.0
allowed-tools: Read Write Edit Bash Glob WebSearch
---

# Web UI Builder

## Purpose

根据用户需求生成**具有设计品质**的单文件前端 UI 页面（纯 HTML + 内嵌 CSS + 内嵌 JS），在编码前通过设计方向框架（目的/基调/约束/差异化）确保产出具有独特视觉风格，避免通用的 AI 美学痕迹。无需任何构建工具、框架 CLI 或 npm 依赖，生成的页面可直接在浏览器中打开。

## When to Use

- 用户要求"生成一个网页"、"写个前端页面"、"做个界面"
- 用户需要一个可直接在浏览器中查看的 HTML 页面
- 用户想快速创建仪表板、表单、产品展示页、Landing Page 等
- 用户需要原型页面用于演示或验证
- 用户描述了 UI 需求但不想配置构建环境

## When NOT to Use

- 用户需要 React/Vue/Angular 等框架项目 —— 应使用对应的框架脚手架
- 用户需要后端 API 集成或数据库 —— 本 Skill 仅生成纯前端页面
- 用户需要复杂的 SPA 路由 —— 单文件 HTML 不适合多页面应用
- 用户已有现成的设计稿/组件库而只需简单拼装

## Workflow

### Step 1: 建立设计方向（Design Direction）

在编写任何代码之前，使用以下四部分框架确定设计方向。**与用户对话协商**，而非单向决定。

**① 目的（Purpose）** — 这个界面解决什么问题？目标用户是谁？核心使用场景是什么？

**② 基调（Tone）** — 从以下方向中选择一个**极致**的基调（而非中庸），指导后续所有设计决策：

| 基调 | 视觉特征 | 适用场景 |
|------|---------|---------|
| 极简主义（Brutally Minimal） | 极致留白、极细边框、克制用色、大字号 | 高端品牌、设计工具、作品集 |
| 奢华精致（Luxury/Refined） | 深色背景、金色/暖色点缀、大字号、宽间距 | 奢侈品牌、高端产品、邀约页面 |
| 编辑/杂志（Editorial/Magazine） | 大标题展示字体、多栏布局、图文混排、密集信息 | 内容平台、新闻站点、博客 |
| 粗野主义（Brutalist/Raw） | 粗边框、超大字号、非传统配色、无装饰 | 创意个人站、实验性项目、艺术展览 |
| 趣味玩具（Playful/Toy-like） | 明亮色彩、圆润元素、微动画、非对称 | 儿童产品、休闲应用、游戏化 |
| 复古未来（Retro-futuristic） | 霓虹色、网格背景、发光效果、斜向元素 | 科技品牌、游戏化应用、活动页 |
| 有机自然（Organic/Natural） | 暖色调、不规则形状、柔和阴影、圆润 | 环保健康、生活方式、食品饮料 |
| 工业实用（Industrial/Utilitarian） | 单色系、高对比度、无装饰、功能优先 | 工具型产品、仪表板、管理后台 |
| 极致丰富（Maximalist） | 多色彩、多纹理、多层次、大胆重叠 | 创意展示、娱乐平台、时尚品牌 |
| 柔和粉彩（Soft/Pastel） | 低饱和度、轻盈质感、大圆角、半透明 | 社交应用、个人博客、生活方式 |

**③ 约束（Constraints）** — 技术限制（兼容性、性能）、可访问性要求（WCAG）、品牌规范

**④ 差异化（Differentiation）** — 这个页面让人记住的**唯一要素**是什么？

> **设计原则**：选择明确的方向并精确执行。大胆的极繁主义和精致的极简主义同样有效——关键是**有意为之**，而非程度强弱。

### Step 2: 收集需求与设计确认

在确定设计方向的基础上，进一步明确以下具体需求。若用户未提供完整，**主动询问**：

| 维度 | 需明确的内容 | 默认值（用户未指定时） |
|------|-------------|---------------------|
| 页面类型 | 仪表板 / 表单 / 列表页 / 产品展示 / Landing Page / 数据可视化 / 其他 | 通用内容页 |
| 布局结构 | 导航栏 / 侧边栏 / 网格 / 非对称 / Hero 区 / 页脚 | 根据设计基调自动选择 |
| 配色偏好 | 主色调方向、浅色/深色模式 | 根据设计基调自动匹配调色板 |
| 字体风格 | 展示字体 + 正文字体 | 根据设计基调自动选择配对 |
| 核心元素 | 标题、表格、图表、按钮、表单、图片、列表等 | 根据页面类型推断 |
| 数据内容 | 展示什么数据或内容 | 使用示例占位数据 |
| 交互需求 | 点击、切换、模态框、表单验证、搜索过滤 | 根据页面类型添加基础交互 |

### Step 3: 设计驱动的 HTML 生成

基于 Step 1 确定的设计方向和 Step 2 收集的需求，生成具有设计品质的 HTML 页面。

使用 `Write` 工具在 `./web-ui-builder/output/` 目录下生成单个 `.html` 文件。

文件命名规则：`<page-type>-<design-tone>-<descriptor>.html`。例如：`product-landing-editorial.html`、`dashboard-industrial.html`、`signup-playful.html`。

---

#### 3.1 排版系统（Typography）

**核心原则：** 避免 AI 风格的通用字体（Inter、Roboto、Arial、系统默认字体），选择有性格的字体组合。

**字体配对指南（根据设计基调选择）：**

| 基调 | 展示字体（Display） | 正文字体（Body） | 数据/代码 |
|------|-------------------|-----------------|----------|
| 编辑/杂志 | Playfair Display, Cormorant Garamond | Source Serif 4, Newsreader | JetBrains Mono |
| 极简/现代 | Syne, Bricolage Grotesque | IBM Plex Sans, Outfit | Fira Code |
| 高端奢华 | Cinzel, Bodoni Moda | Cormorant, EB Garamond | — |
| 创意有趣 | Fredoka, Baloo 2 | Nunito, Quicksand | — |
| 粗野主义 | Rubik Glitch, Bungee | Space Grotesk, Archivo | JetBrains Mono |
| 工业实用 | Archivo, Josefin Sans | IBM Plex Mono, DM Sans | IBM Plex Mono |
| 有机自然 | Fraunces, Kalam | DM Serif Display, Source Sans 3 | — |
| 复古未来 | Orbitron, Rajdhani | Exo 2, Share Tech Mono | Share Tech Mono |

**配对原则：** 高对比度 = 有趣。展示字体 + 正文字体差异要大，字号跳跃 3 倍+而非 1.5 倍。衬线体 + 无衬线体组合通常效果最好。

**字体加载策略：**
- 使用 Google Fonts CDN（`<link>` 方式），仅加载所需字重，`display=swap` 确保文字立即可见
- 系统字体栈作为 fallback
- 避免加载超过 2 个字体族（含 3–4 个字重）

**排版缩放：**
```css
:root {
  --fs-display: clamp(2.5rem, 6vw, 5rem);    /* Hero 标题 */
  --fs-h1: clamp(1.75rem, 4vw, 3rem);         /* 一级标题 */
  --fs-h2: clamp(1.25rem, 2.5vw, 1.75rem);    /* 二级标题 */
  --fs-body: clamp(0.95rem, 1.2vw, 1.1rem);   /* 正文 */
  --fs-small: clamp(0.8rem, 1vw, 0.9rem);     /* 辅助文字 */
  --lh-tight: 1.1;   /* 标题行高 */
  --lh-normal: 1.6;  /* 正文行高 */
}
```

---

#### 3.2 色彩与主题（Color & Theme）

**色彩策略：** 使用主色调 + 尖锐强调色，避免平淡和中庸。

**❌ 禁止使用的配色方案（AI 风格）：**
- 紫色渐变 + 白色背景（"AI 风格终极标志"）
- 青色 + 深色背景（典型的科技模板感）
- 蓝色 + 白色企业通用配色
- 霓虹色强调 + 深色背景（过于游戏化）

**✅ 推荐配色策略：**

从以下来源提取色彩灵感：
- **品牌规范**：如果用户提供品牌色，以此为核心展开
- **IDE 主题**：Dracula、Nord、Catppuccino、Tokyo Night 的色彩理论经过验证
- **文化美学**：日式极简（和色）、北欧设计（冷色调）、包豪斯（原色）、孟菲斯（亮色碰撞）
- **自然色板**：海洋、森林、日落、矿物等自然色系

**使用 CSS 现代颜色函数：**
```css
:root {
  /* OKLCH — 更符合人眼感知的色彩空间，色相一致性更好 */
  --primary: oklch(45% 0.24 265);        /* 主色：色相 265° 的蓝色 */
  --accent: oklch(65% 0.28 30);           /* 强调色：暖色点缀（橙/红） */
  --surface: oklch(98% 0.01 265);         /* 浅色表面 */
  --text-primary: oklch(20% 0.02 265);    /* 主文本 */
  --text-secondary: oklch(45% 0.03 265);  /* 次要文本 */

  /* 使用 color-mix 派生变体 */
  --primary-hover: color-mix(in oklch, var(--primary), black 15%);
  --primary-subtle: color-mix(in oklch, var(--primary), var(--surface) 85%);

  /* 使用 light-dark 实现双模式 */
  --bg: light-dark(oklch(98% 0.01 265), oklch(12% 0.015 265));
  --card: light-dark(oklch(100% 0 0), oklch(18% 0.02 265));
  --text: light-dark(oklch(20% 0.02 265), oklch(88% 0.01 265));
}

/* 降级方案：不支持 light-dark 的浏览器使用媒体查询 */
@supports not (color: light-dark(white, black)) {
  @media (prefers-color-scheme: dark) {
    :root { --bg: oklch(12% 0.015 265); --card: oklch(18% 0.02 265); --text: oklch(88% 0.01 265); }
  }
}
```

**调色板结构（每个页面至少包含）：**
- 主色 × 1（品牌/核心色调）
- 强调色 × 1–2（按钮、链接、高亮）
- 表面色 × 2–3（背景、卡片、边框）
- 文本色 × 2–3（主文本、次要文本、禁用色）
- 语义色 × 4（成功 `oklch(55% 0.2 145)`、警告 `oklch(60% 0.2 85)`、错误 `oklch(50% 0.25 30)`、信息 `oklch(50% 0.2 245)`）

**对比度保障：** 确保文本与背景的对比度 ≥ 4.5:1（WCAG AA 标准），可使用 WebAIM 对比度检查工具验证。大文本（≥24px/19px bold）≥ 3:1。

---

#### 3.3 布局与构成（Layout & Composition）

**布局创新原则：**
- 非对称布局 > 对称布局（对称容易显平庸）
- 元素重叠和网格打破 > 严格对齐
- 斜向/对角视觉流 > 水平或垂直流水布局
- 变化间距 > 统一间距（使用 `clamp()` 创建流畅变化）
- 内容断行和文字绕排 > 固定宽度的卡片

**布局模式库：**
```css
/* 非对称网格 */
.page-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  gap: clamp(1rem, 3vw, 3rem);
}
@media (max-width: 768px) {
  .page-grid { grid-template-columns: 1fr; }
}

/* Hero 区：打破网格 */
.hero {
  display: grid;
  grid-template-columns: 1fr 1fr;
  align-items: center;
  min-height: min(80vh, 600px);
}
.hero-image {
  grid-column: 1 / -1;
  grid-row: 1;
  margin: 0 calc(-1 * clamp(1rem, 5vw, 4rem));
}

/* 重叠布局 */
.overlap-grid {
  display: grid;
  gap: 0;
}
.overlap-grid > .front {
  grid-row: 1;
  grid-column: 1;
  z-index: 2;
  margin-right: -15%;
}
.overlap-grid > .back {
  grid-row: 1;
  grid-column: 1;
  z-index: 1;
  margin-left: 15%;
  margin-top: 10%;
  opacity: 0.85;
}

/* 斜向分割 */
.section-diagonal {
  background: linear-gradient(
    160deg,
    var(--surface) 0%,
    var(--surface) 55%,
    var(--primary-subtle) 55%,
    var(--primary-subtle) 100%
  );
}

/* 动态间距 */
.content-area {
  padding: clamp(1.5rem, 5vw, 4rem);
}

/* 全屏覆盖 */
.page-wrapper {
  min-height: 100dvh;
  display: flex;
  flex-direction: column;
}
```

---

#### 3.4 视觉细节与纹理（Visual Details & Texture）

**背景处理原则：** 避免纯色背景，使用多层渐变或重复图案增加深度。

**渐变背景模板：**
```css
/* 双径向渐变 + 基础色 */
.section-textured {
  background:
    radial-gradient(ellipse at 20% 50%, var(--gradient-color-1) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 20%, var(--gradient-color-2) 0%, transparent 50%),
    var(--bg);
}

/* 网格图案覆盖 */
.pattern-dots {
  background-image: radial-gradient(circle, var(--border) 1px, transparent 1px);
  background-size: 24px 24px;
}

.pattern-grid {
  background-image:
    linear-gradient(var(--border) 1px, transparent 1px),
    linear-gradient(90deg, var(--border) 1px, transparent 1px);
  background-size: 40px 40px;
  opacity: 0.3;
  pointer-events: none;
}

/* 噪点纹理（使用极小的 data:uri PNG 或 SVG） */
.noise-overlay {
  position: relative;
}
.noise-overlay::after {
  content: '';
  position: absolute;
  inset: 0;
  opacity: 0.03;
  background-image: url("data:image/svg+xml,...");
  pointer-events: none;
  mix-blend-mode: multiply;
}
@media (prefers-color-scheme: dark) {
  .noise-overlay::after { mix-blend-mode: screen; opacity: 0.05; }
}
```

**阴影层级规范：**
```css
:root {
  --shadow-sm: 0 1px 3px rgb(0 0 0 / 0.06), 0 1px 2px rgb(0 0 0 / 0.04);
  --shadow-md: 0 4px 6px rgb(0 0 0 / 0.05), 0 10px 15px rgb(0 0 0 / 0.03);
  --shadow-lg: 0 10px 25px rgb(0 0 0 / 0.08), 0 20px 40px rgb(0 0 0 / 0.04);
  --shadow-xl: 0 20px 50px rgb(0 0 0 / 0.1);
}
```

---

#### 3.5 动效与动画（Motion & Animation）

**动画设计原则：**
- 优先纯 CSS 动画（`@keyframes`），仅在必要时使用 JS（Intersection Observer）
- 聚焦高影响时刻：页面加载的错落展开动画
- 每个页面最多 1 个主要动画序列（避免动画过多）
- 使用 `animation-delay` 实现错落节奏

**缓动函数（禁止使用 bounce/elastic）：**
```css
:root {
  --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-out: cubic-bezier(0.33, 1, 0.68, 1);
  --ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);
}
```

**入场动画模板：**
```css
/* 错落展开入场 */
.animate-stagger {
  animation: fadeUp 0.6s var(--ease-out-expo) both;
}
.animate-stagger:nth-child(1) { animation-delay: 0s; }
.animate-stagger:nth-child(2) { animation-delay: 0.08s; }
.animate-stagger:nth-child(3) { animation-delay: 0.16s; }
.animate-stagger:nth-child(4) { animation-delay: 0.24s; }
.animate-stagger:nth-child(5) { animation-delay: 0.32s; }
/* 超过 5 个元素时增量 0.08s */

@keyframes fadeUp {
  from {
    opacity: 0;
    transform: translateY(24px) scale(0.98);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* Hero 区渐入序列 */
.hero-title   { animation: heroIn 1s var(--ease-out-expo) both; }
.hero-subtitle { animation: heroIn 0.8s var(--ease-out-expo) 0.2s both; }
.hero-cta     { animation: heroIn 0.6s var(--ease-out-expo) 0.4s both; }

@keyframes heroIn {
  from { opacity: 0; transform: translateY(30px) }
  to   { opacity: 1; transform: translateY(0) }
}

/* 滚动触发入场（使用 Intersection Observer） */
document.addEventListener('DOMContentLoaded', () => {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });
  document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
});
```

```css
.reveal { opacity: 0; transform: translateY(30px); transition: opacity 0.6s var(--ease-out-expo), transform 0.6s var(--ease-out-expo); }
.reveal.visible { opacity: 1; transform: translateY(0); }

/* 尊重用户动画偏好 */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

#### 3.6 交互模式（Interaction Patterns）

**表单交互：**
- 实时字段验证（输入时即时校验，而非提交后一次性显示）
- 密码强度可视化指示器（弱/中/强 + 颜色编码）
- 提交按钮加载状态（CSS 骨架动画或 Spinner）
- 成功/错误的非侵入式提示（toast 通知而非 alert 弹窗）

**导航交互：**
- 响应式菜单：桌面端水平导航，移动端汉堡菜单 + 平滑展开/折叠
- 滚动高亮：使用 Intersection Observer 高亮当前区域对应的导航项
- 固定导航补偿：`scroll-margin-top: 80px` 确保锚点定位准确
- 悬浮菜单：hover + focus 双重支持键盘可访问性

**数据交互：**
- Tab 切换：CSS-only 实现（`:target` 伪类或单选按钮 hack）或轻量 JS
- 搜索过滤：`input` 事件 + 防抖（`setTimeout` 300ms debounce）
- 排序切换：点击表头升序/降序切换，带方向箭头指示
- 分页模拟：仅当前页 + 前后 2 页显示，其余用 "..."

**通用交互：**
- 返回顶部按钮：页面滚动超过一屏后显示，点击平滑滚动至顶部
- 深色模式切换：使用 `prefers-color-scheme` 自动适配 + 用户手动切换
- 响应式表格：水平滚动（`overflow-x: auto`）而非隐藏列

#### 3.7 内外资源使用规范

**内嵌优先原则：** 所有内容自包含于单个 HTML 文件中。

**可选 CDN 资源（仅在明确需要时引入，最多 2 个）：**

| 用途 | 资源 | 适用场景 |
|------|------|---------|
| 图标 | Lucide Icons（ESM 方式）或内嵌 SVG/Unicode | 需要图标时优先内嵌 SVG |
| 图表 | Chart.js 4.x CDN | 仅数据可视化类页面 |
| 字体 | Google Fonts CDN | 使用非系统字体时 |

**系统字体栈（作为 fallback）：**
```
-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Microsoft YaHei", sans-serif
```

**CDN 使用要求：**
- 每次使用 CDN 前必须使用 `WebSearch` 验证 CDN URL 是否有效
- 在 HTML 注释中标注 CDN 来源 URL，方便用户离线时替换

### Step 4: 在浏览器中打开

生成文件后，使用 Bash 执行 Windows 命令在默认浏览器中打开：

```bash
start "" "./web-ui-builder/output/<文件名>.html"
```

如果页面需要从 CDN 加载资源（如 Chart.js、Google Fonts），提醒用户需要网络连接。

### Step 5: AI Slop 测试与输出报告

**AI Slop 测试：** 在向用户报告之前，对照以下清单检查生成页面：

- [ ] 是否使用了 Inter、Roboto、Arial 或纯系统字体作为主要字体？
- [ ] 是否使用了紫色渐变 + 白色背景或青色 + 深色背景等 AI 模板配色？
- [ ] 布局是否全部是等宽卡片网格，缺乏非对称或打破网格的元素？
- [ ] 背景是否为纯色，缺少纹理、渐变或图案？
- [ ] 动画是否使用了 bounce/elastic 等过度缓动？
- [ ] 整个页面是否一眼就能看出是 AI 生成的？（**AI Slop 测试核心**）

> **AI Slop 测试核心**：如果用户看到这个页面后问"这是哪个 AI 做的" → 这是一份失败的 AI 风格设计。设计应当让人问"这是怎么做的"而不是"这是哪个 AI 做的"。
>
> 以上任何一项为"是"，必须重新生成相应部分。

**输出报告内容：**

向用户报告生成结果：

- **文件信息**：文件路径、命名
- **设计方向总结**：
  - 基调选择及理由
  - 配色策略（主色 + 强调色，oklch 值）
  - 字体组合（展示字体 + 正文 + fallback）
  - 动画和交互亮点
- **核心功能清单**：页面包含的组件和交互
- **自定义修改指引**：
  - CSS 变量位置（`:root` 中的配色、字体、间距变量）
  - 设计调整方向（"要改为深色模式，修改 `light-dark()` 值"、"要更换字体，修改 Google Fonts 链接和 `--font-*` 变量"）
  - 典型自定义操作（修改间距、替换图片、调整动画时长）
- **CDN 依赖说明**：列出所有外部资源及离线替换方案

## Constraints

- **Always** 生成纯静态 HTML 文件，无需任何构建工具或 npm install
- **Always** 将 CSS 和 JS 内嵌在单个 HTML 文件中，确保双击即可查看
- **Always** 使用语义化 HTML5 标签（`<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`）
- **Always** 生成响应式布局，适配桌面和移动端
- **Always** 在编码前执行设计方向四步框架（目的/基调/约束/差异化）
- **Always** 选择极致的设计基调并一致性执行，避免中庸风格
- **Always** 使用有性格的字体组合，避免 AI 风格的通用字体
- **Always** 使用现代 CSS 颜色函数（`oklch`、`color-mix`、`light-dark`）管理配色
- **Always** 在布局中引入非对称、重叠或网格打破等视觉张力
- **Always** 使用 CSS 渐变、几何图案或噪点纹理增加深度（避免纯色背景）
- **Always** 实现错落展开的入场动画（staggered reveals）提升页面质感
- **Always** 使用 exponent/ease-out 缓动函数，禁止 bounce/elastic
- **Always** 尊重用户动画偏好（`prefers-reduced-motion`）
- **Always** 执行 AI Slop 测试并确保通过
- **Always** 将输出文件保存到 `./web-ui-builder/output/` 目录
- **Always** 生成后自动在浏览器中打开供用户查看
- **Always** 在 HTML 文件中添加注释标注关键区域（如 `<!-- 导航栏 -->`、`<!-- Hero 区 -->`），方便用户定位修改
- **Always** 在输出报告中提供设计方向总结和自定义修改指引
- **Never** 要求用户安装 Node.js、npm 或任何构建工具
- **Never** 使用 AI 风格配色（紫色渐变 + 白色背景、青色 + 深色背景、霓虹色 + 深色背景）
- **Never** 使用 Inter、Roboto、Arial 或纯系统字体作为主要展示字体
- **Never** 引入超过 2 个 CDN 外部依赖（保持简洁，优先内嵌实现）
- **Never** 在 HTML 中使用 `file://` 协议加载跨域资源（会导致浏览器安全策略阻止）
- **Never** 生成空白的占位页面 —— 始终填充示例数据让用户看到实际效果
- **Never** 使用 glassmorphism 仅作为装饰（必须有功能目的）
- **Never** 使用渐变文字（gradient text）用于指标或标题的"视觉冲击"
- 如果有用户提供的数据，必须使用真实数据而非占位文本
- CSS 动画和过渡效果保持克制，聚焦关键交互时刻
- 所有中文内容使用 `lang="zh-CN"` 声明
- 确保色彩对比度满足 WCAG AA 标准（文本 ≥ 4.5:1，大文本 ≥ 3:1）

## Examples

### ✅ Do This — 设计驱动风格

**输入**："帮我生成一个产品 Landing Page，风格要现代编辑感"
**设计方向**：
- 基调：Editorial/Magazine（编辑杂志风）
- 字体：Playfair Display（展示）+ IBM Plex Sans（正文）
- 配色：深蓝主色 + 琥珀色点缀，浅色背景 + 深色导航
- 差异化：非对称 Hero 布局，错落展开动画，网格图案背景
**生成**：
- 文件名：`product-landing-editorial.html`
- Hero 区：左侧大标题 + 右侧错落产品特性卡片，斜向背景分割
- 特性区：3×2 非对称网格，每个卡片延迟入场
- 页脚：简约深色，包含社交链接和版权
- CSS：oklch 配色、grid 打破、clamp() 间距、staggered reveals
- 自动在浏览器中打开后执行 AI Slop 测试并报告

**输入**："做一个工业风格的销售数据仪表板，展示 KPI 和趋势"
**设计方向**：
- 基调：Industrial/Utilitarian（工业实用风）
- 字体：Archivo（展示）+ IBM Plex Mono（数据）
- 配色：单色深灰 + 蓝色数据强调，深色模式
- 差异化：数据可视化优先，网格背景，极简装饰
**生成**：
- 文件名：`sales-dashboard-industrial.html`
- 布局：顶部 KPI 行（4 个指标）+ 左侧趋势图 + 右侧数据表格
- KPI 卡片：极简边框设计，大字指标，小字同比变化
- 交互：Tab 切换（日/周/月）、排序表格、图表 Chart.js
- CSS：oklch 单色调色板、等宽字体显示数据、grid 布局、细微入场动画

**输入**："帮我做一个有趣风格的注册表单页面"
**设计方向**：
- 基调：Playful/Toy-like（趣味玩具风）
- 字体：Fredoka（展示）+ Nunito（正文）
- 配色：珊瑚橙主色 + 天蓝点缀，浅色背景
- 差异化：圆润元素 + 微动画 + 彩色渐变几何背景
**生成**：
- 文件名：`signup-playful.html`
- 布局：两列（左侧表单 + 右侧彩色图形装饰）
- 字段：姓名、邮箱、密码（强度可视化）、兴趣选择
- 交互：实时字段验证、密码强度指示器、提交 toast 反馈
- CSS：大圆角、明亮渐变背景、弹性间距、表单聚焦动画

### ✅ Do This — 基础功能型（用户不指定设计方向时）

**输入**："帮我生成一个团队绩效仪表板，包含 KPI 卡片、最近任务列表和进度图表"
**默认设计方向**：
- 基调：Industrial/Utilitarian
- 字体：Archivo + IBM Plex Mono
- 配色：单色深蓝 + 暖色强调
- 差异化：数据层级清晰 + 微动效
**生成**：
- 文件名：`team-performance-dashboard.html`
- 布局：顶部导航 + 4 个 KPI 指标卡片（网格布局）+ 任务列表表格 + 柱状图区域
- 配色：专业深蓝商务风格
- CSS：Grid 布局、卡片阴影、表格行 hover 效果、响应式折叠为单列
- JS：Tab 切换（本周/本月/本季度）、数据刷新模拟按钮
- 数据：填充示例团队成员和任务数据，图表用 Chart.js CDN 绘制
- 自动在浏览器中打开

**输入**："做一个用户注册表单页面"
**默认设计方向**：
- 基调：Brutally Minimal
- 字体：Syne + Outfit
- 配色：灰白主色 + 单色强调
- 差异化：极致简洁 + 精确交互反馈
**生成**：
- 文件名：`user-registration-form.html`
- 布局：居中卡片式表单，带品牌 Logo 区域
- 字段：姓名、邮箱、密码（含强度指示）、确认密码、手机号、同意条款复选框
- 验证：邮箱格式、密码强度（弱/中/强）、密码一致性、手机号格式、必填项检查
- 交互：实时验证反馈、提交按钮 loading 状态、成功提示动画
- 自动在浏览器中打开

### ❌ Not This

- 生成一个 `index.js` + `style.css` + `index.html` 三文件分离的项目（用户无法双击直接查看）
- 要求用户先执行 `npm install` 或 `npm run dev`
- 生成使用 React JSX / Vue SFC 的代码
- 生成空白页面只有标题和一段文字，没有实际内容和交互
- 引入大量 CDN 依赖（Bootstrap + jQuery + Font Awesome + Animate.css...）
- 使用 `file://` 加载 JSON 数据文件
- 忘记添加 `<meta name="viewport">` 导致移动端显示异常
- 使用 Inter/Roboto 字体 + 紫色渐变配色（一眼 AI 风格）
- 布局全部是等大卡片网格，无一例外
- 页面全部纯色背景，没有纹理或渐变
- 使用 bounce easing 的动画（显得廉价）
- 生成前没有与用户确认设计方向，直接采用默认模板

## Notes

- 生成的页面在项目 `web-ui-builder/output/` 目录下，可随时复制到任意位置双击打开
- 如需离线使用含 CDN 资源的页面，可后续手动下载对应资源并修改引用路径
- 如果用户对生成的页面不满意，可以继续通过对话调整（如"把配色改成深色"、"换一个字体组合"、"增加一个搜索框"）
- Windows 下 `start "" "path/to/file.html"` 会在默认浏览器中打开，如果默认浏览器未设置可能弹出选择窗口
- 图表类页面依赖 Chart.js CDN，首次加载需要网络连接，加载后浏览器会缓存
- 生成页面不包含任何跟踪代码、分析脚本或遥测
- Google Fonts 加载需要网络连接，所有字体均设置了 `font-display: swap` 确保文字立即可见
- 设计基调选择直接影响所有后续决策——基调一致比单个元素完美更重要
- 在引入 Google Fonts 或任何 CDN 资源前，使用 WebSearch 确认 CDN URL 当前有效
- `oklch()` 在现代浏览器（Chrome 111+、Firefox 113+、Safari 15.4+）中受支持。需要兼容旧浏览器时，在 `oklch` 后提供 hex 后备色
- `light-dark()` 函数在 Chrome 123+、Firefox 120+、Safari 17.5+ 中受支持，推荐配合 `@supports` 降级使用
- 如果用户需要 React/Vue/Next.js 等框架项目，应使用其他合适的工具或 skill
- 如果用户提供的品牌有现成的设计系统（配色、字体、间距规范），优先遵循品牌规范而非设计基调的默认值
