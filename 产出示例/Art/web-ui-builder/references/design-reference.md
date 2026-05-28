# Design Reference — Web UI Builder

本文件提供详细的排版、配色、设计基调和动画参考，供 Claude 在生成设计驱动型页面时使用。SKILL.md 中引用了本文件的部分内容，便于保持工作流的简洁。

---

## 一、排版系统深度指南

### 1.1 字体分类选择表

| 分类 | 字体名 | 性格 | 建议字重 | 适合基调 |
|------|--------|------|---------|---------|
| **衬线展示** | Playfair Display | 优雅、编辑感 | 700–900 | Editorial, Luxury |
| **衬线展示** | Cormorant Garamond | 古典、精致 | 300–700 | Luxury, Organic |
| **衬线展示** | Bodoni Moda | 高对比度、时尚 | 700–900 | Luxury, Editorial |
| **衬线展示** | Cinzel | 庄重、雕刻感 | 400–700 | Luxury, Brutalist |
| **衬线正文** | Source Serif 4 | 易读、温暖 | 400–600 | Editorial, Organic |
| **衬线正文** | DM Serif Display | 个性格较强 | 400 | Organic, Editorial |
| **衬线正文** | EB Garamond | 经典、省眼 | 400–500 | Luxury |
| **无衬线展示** | Syne | 现代、几何感 | 600–800 | Minimal, Industrial |
| **无衬线展示** | Bricolage Grotesque | 独特、宽体 | 700–900 | Minimal, Playful |
| **无衬线展示** | Archivo | 紧凑、实用 | 700–900 | Industrial, Brutalist |
| **无衬线展示** | Bungee | 粗犷、有力 | 400 | Brutalist, Playful |
| **无衬线展示** | Fredoka | 圆润、友好 | 500–700 | Playful, Pastel |
| **无衬线展示** | Orbitron | 未来感、科技 | 400–900 | Retro-futuristic |
| **无衬线展示** | Rubik Glitch | 故障效果 | 400 | Brutalist |
| **无衬线正文** | IBM Plex Sans | 清晰、技术感 | 300–600 | Minimal, Editorial |
| **无衬线正文** | Outfit | 现代、圆润 | 300–600 | Minimal, Pastel |
| **无衬线正文** | Nunito | 友好、平衡 | 300–700 | Playful, Pastel |
| **无衬线正文** | Quicksand | 现代、柔和 | 300–600 | Playful |
| **无衬线正文** | Exo 2 | 科技、动态 | 300–600 | Retro-futuristic |
| **无衬线正文** | Space Grotesk | 现代、略有特色 | 300–700 | Brutalist, Minimal |
| **等宽** | JetBrains Mono | 开发感、清晰 | 400–700 | Editorial, Brutalist |
| **等宽** | Fira Code | 开发感、连字 | 400–600 | Minimal, Industrial |
| **等宽** | IBM Plex Mono | 实用、不抢眼 | 400–600 | Industrial |
| **等宽** | Share Tech Mono | 复古科技 | 400 | Retro-futuristic |

### 1.2 字体配对矩阵

| 基调 | 推荐配对 | 说明 |
|------|---------|------|
| Editorial | Playfair Display 700 + Source Serif 4 400 | 经典的编辑体组合 |
| Editorial | Cormorant Garamond 600 + IBM Plex Sans 400 | 衬线+无衬线对比 |
| Luxury | Cinzel 700 + EB Garamond 400 | 全衬线的高端感 |
| Luxury | Bodoni Moda 800 + Cormorant 400 | 高对比度时尚感 |
| Minimal | Syne 700 + Outfit 400 | 几何感现代组合 |
| Minimal | Bricolage Grotesque 700 + IBM Plex Sans 400 | 独特展示+实用正文 |
| Brutalist | Rubik Glitch 400 + Space Grotesk 500 | 粗野+现代 |
| Brutalist | Bungee 400 + Archivo 600 | 大字号冲击力 |
| Playful | Fredoka 600 + Nunito 400 | 圆润友好组合 |
| Retro-futuristic | Orbitron 700 + Exo 2 400 | 科技感双人组 |
| Organic | Fraunces 700 + DM Serif Display 400 | 有机衬线组合 |
| Industrial | Archivo 800 + IBM Plex Mono 500 | 实用+数据美学 |

### 1.3 排版缩放比例

```css
:root {
  /* 展示型：超大、有冲击力 */
  --fs-hero: clamp(3rem, 8vw, 6rem);
  --fs-display: clamp(2.5rem, 6vw, 5rem);

  /* 标题层级：3:1 跳跃 */
  --fs-h1: clamp(1.75rem, 4vw, 3rem);      /* ×3 vs body */
  --fs-h2: clamp(1.25rem, 2.5vw, 1.75rem);  /* ×1.75 vs body */

  /* 正文与辅助 */
  --fs-body: clamp(0.95rem, 1.2vw, 1.1rem);
  --fs-small: clamp(0.8rem, 1vw, 0.9rem);
  --fs-caption: clamp(0.7rem, 0.9vw, 0.8rem);

  /* 行高 */
  --lh-tight: 1.05;    /* 展示/大标题 */
  --lh-heading: 1.15;  /* h1-h2 */
  --lh-body: 1.6;      /* 正文 */
  --lh-loose: 1.8;     /* 引文/装饰文字 */

  /* 字距 */
  --ls-tight: -0.03em;
  --ls-normal: 0;
  --ls-wide: 0.05em;
  --ls-label: 0.08em;  /* 标签/按钮大写 */
}
```

---

## 二、色彩策略深度指南

### 2.1 色相情感映射

| 色相区间 (oklch H) | 情感联想 | 适用场景 | 基调匹配 |
|--------------------|---------|---------|---------|
| 0–30 (红/橙) | 热情、紧急、食欲 | CTA、错误提示、促销 | Playful, Maximalist |
| 30–60 (橙/黄) | 温暖、乐观、创意 | 强调色、评级、警告 | Playful, Organic |
| 60–90 (黄/黄绿) | 成长、自然、新鲜 | 成功、环保主题 | Organic, Pastel |
| 90–150 (绿/青) | 健康、稳定、财富 | 成功、金融、医疗 | Organic, Minimal |
| 150–200 (青/蓝绿) | 清新、科技、冷静 | 数据可视化、科技产品 | Industrial, Minimal |
| 200–280 (蓝) | 信任、专业、稳重 | 主色、企业、导航 | Editorial, Industrial |
| 280–330 (紫/品红) | 创意、奢华、神秘 | 品牌色、创意行业 | Luxury, Maximalist |
| 330–360 (品红/红) | 激情、亲密度 | 强调色、装饰 | Retro-futuristic |

### 2.2 色值转换参考

```css
/* oklch → hex 近似对照（用于不支持 oklch 的浏览器降级） */
:root {
  /* 蓝色系 */
  --blue-500: oklch(45% 0.22 260);    /* ≈ #3B82F6 */
  --blue-600: oklch(38% 0.20 260);    /* ≈ #2563EB */
  --blue-100: oklch(92% 0.04 260);    /* ≈ #DBEAFE */

  /* 灰色系 */
  --gray-900: oklch(18% 0.01 260);    /* ≈ #111827 */
  --gray-500: oklch(55% 0.02 260);    /* ≈ #6B7280 */
  --gray-100: oklch(97% 0.005 260);   /* ≈ #F3F4F6 */

  /* 暖色系 */
  --amber-500: oklch(62% 0.19 75);    /* ≈ #F59E0B */
  --rose-500: oklch(52% 0.22 20);     /* ≈ #F43F5E */
  --emerald-500: oklch(55% 0.18 150); /* ≈ #10B981 */
}

/* color-mix 使用示例 */
:root {
  --primary: oklch(45% 0.22 260);
  --primary-hover: color-mix(in oklch, var(--primary), black 15%);
  --primary-active: color-mix(in oklch, var(--primary), black 25%);
  --primary-light: color-mix(in oklch, var(--primary), white 85%);
  --primary-subtle: color-mix(in oklch, var(--primary), var(--surface) 90%);

  --text-on-primary: color-mix(in oklch, white, var(--primary) 10%);
}
```

### 2.3 主题色板模板

```css
/* ==================== 浅色模式 ==================== */
:root {
  /* 主色与强调 */
  --primary: oklch(42% 0.20 260);
  --accent: oklch(62% 0.22 30);

  /* 表面色 */
  --surface: oklch(98% 0.005 260);
  --surface-elevated: oklch(100% 0 0);
  --surface-inverse: oklch(15% 0.01 260);
  --border: oklch(88% 0.01 260);

  /* 文本色 */
  --text-primary: oklch(15% 0.015 260);
  --text-secondary: oklch(45% 0.02 260);
  --text-disabled: oklch(70% 0.01 260);
  --text-on-primary: oklch(98% 0.005 260);
  --text-on-accent: oklch(15% 0.015 260);

  /* 语义色 */
  --success: oklch(55% 0.18 145);
  --warning: oklch(62% 0.19 75);
  --error: oklch(50% 0.22 30);
  --info: oklch(50% 0.18 245);

  /* 阴影 */
  --shadow-sm: 0 1px 3px oklch(0% 0 0 / 0.06);
  --shadow-md: 0 4px 12px oklch(0% 0 0 / 0.05);
  --shadow-lg: 0 12px 40px oklch(0% 0 0 / 0.08);
}

/* ==================== 深色模式 ==================== */
@media (prefers-color-scheme: dark) {
  :root {
    --primary: oklch(58% 0.18 260);
    --accent: oklch(68% 0.20 30);

    --surface: oklch(12% 0.01 260);
    --surface-elevated: oklch(18% 0.015 260);
    --surface-inverse: oklch(95% 0.005 260);
    --border: oklch(25% 0.015 260);

    --text-primary: oklch(90% 0.01 260);
    --text-secondary: oklch(65% 0.015 260);
    --text-disabled: oklch(40% 0.01 260);
    --text-on-primary: oklch(12% 0.01 260);
    --text-on-accent: oklch(12% 0.01 260);

    --shadow-sm: 0 1px 3px oklch(0% 0 0 / 0.3);
    --shadow-md: 0 4px 12px oklch(0% 0 0 / 0.25);
    --shadow-lg: 0 12px 40px oklch(0% 0 0 / 0.2);
  }
}

/* ==================== 使用 light-dark 的合一写法 ==================== */
@supports (color: light-dark(white, black)) {
  :root {
    --primary: light-dark(oklch(42% 0.20 260), oklch(58% 0.18 260));
    --accent: light-dark(oklch(62% 0.22 30), oklch(68% 0.20 30));
    --surface: light-dark(oklch(98% 0.005 260), oklch(12% 0.01 260));
    --text-primary: light-dark(oklch(15% 0.015 260), oklch(90% 0.01 260));
    /* ... */
  }
}
```

### 2.4 基调对应配色方案

| 基调 | 主色 | 强调色 | 表面 | 氛围 |
|------|------|--------|------|------|
| Editorial | oklch(35% 0.15 260) 深蓝 | oklch(60% 0.18 45) 琥珀 | 暖白 | 沉稳可信 |
| Luxury | oklch(30% 0.10 280) 深紫 | oklch(65% 0.15 80) 金 | 米白 | 高端精致 |
| Brutalist | oklch(25% 0.02 0) 纯黑 | oklch(55% 0.25 360) 亮红 | 白或黑 | 极致对比 |
| Playful | oklch(60% 0.22 330) 品红 | oklch(65% 0.20 180) 天蓝 | 暖粉 | 活力趣味 |
| Minimal | oklch(45% 0.10 250) 灰蓝 | oklch(55% 0.25 30) 橙色 | 纯白 | 简洁安静 |
| Organic | oklch(50% 0.15 150) 翠绿 | oklch(55% 0.15 70) 暖黄 | 米白 | 自然舒适 |
| Retro-futuristic | oklch(45% 0.20 300) 紫 | oklch(70% 0.20 180) 青 | 深蓝 | 霓虹科幻 |
| Industrial | oklch(35% 0.02 260) 中性灰 | oklch(50% 0.18 260) 蓝 | 灰白 | 功能优先 |
| Maximalist | 多色碰撞 | 多色碰撞 | 白或黑 | 丰富层次 |
| Pastel | oklch(75% 0.06 250) 淡蓝 | oklch(80% 0.08 80) 淡黄 | 纯白 | 轻柔甜美 |

---

## 三、设计基调视觉特征详表

### 3.1 每一基调的核心特征

| 基调 | 字体 | 配色 | 布局特征 | 装饰 | 动画 |
|------|------|------|---------|------|------|
| Editorial | 衬线展示+无衬线正文 | 深蓝/暖色点缀 | 多栏、丰富间距 | 分割线、引文块 | 文字逐段入场 |
| Luxury | 衬线为主 | 暗色+金色 | 宽间距、中心对齐 | 渐变背景、光泽 | 缓入、不打扰 |
| Brutalist | 粗重无衬线 | 高对比单色+亮色 | 大留白或全出血 | 几何图形、粗线 | 硬切、无缓动 |
| Playful | 圆润无衬线 | 明快多色 | 非对称、不规则 | 圆点、弧线 | 弹性缓出（轻微） |
| Minimal | 几何无衬线 | 单色+单强调 | 密集内容或极简 | 少即是多 | 克制、功能性 |
| Organic | 衬线或手写 | 自然色（绿/棕/黄） | 柔性布局 | 不规则形状、植物 | 缓入缓出 |
| Retro-futuristic | 细长几何或未来风 | 霓虹+深色 | 网格对齐 | 发光、扫描线 | 闪烁、脉冲 |
| Industrial | 实用无衬线/等宽 | 中性色+蓝色 | 功能优先的效率布局 | 无或极少 | 无或极简 |
| Maximalist | 多字体混搭 | 丰富多色 | 密集重叠 | 图案、纹理叠加 | 丰富但有序 |
| Pastel | 柔和无衬线 | 低饱和粉彩 | 松散、轻盈 | 渐变圆角、光影 | 柔和过渡 |

### 3.2 基调交叉（混搭指导）

有时用户想要的风格介于两种基调之间。以下混搭经验：

- **Editorial × Minimal** = 杂志感的标题层级 + 极简的配色和留白 → 适用于内容驱动的高端品牌
- **Brutalist × Playful** = 粗野的边框和字号 + 有趣的配色和圆角 → 适用于创意个人站
- **Luxury × Industrial** = 高品质质感 + 功能布局 → 适用于高端工具型产品
- **Organic × Pastel** = 自然色系 + 柔和质感 → 适用于健康生活方式

**关键原则：** 混搭时保持最多 2 种基调的特征，其余维度回归中性。

---

## 四、动画与交互模式深度指南

### 4.1 缓动函数一览

```css
:root {
  /* 推荐：自然、专业 */
  --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);     /* 出场，缓慢减速 */
  --ease-out: cubic-bezier(0.33, 1, 0.68, 1);          /* 通用出场 */
  --ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);       /* 入场+出场 */

  /* 不推荐（除非有特殊理由） */
  --ease-bounce: cubic-bezier(0.34, 1.56, 0.64, 1);    /* 仅在 Playful 基调中轻微使用 */
}
```

### 4.2 动画时长规范

| 场景 | 时长 | 缓动 | 说明 |
|------|------|------|------|
| 页面入场（主要） | 600–1000ms | ease-out-expo | Hero 区域文字渐入 |
| 页面入场（错落） | 400–600ms | ease-out-expo | 卡片、列表项错落展开 |
| hover 状态 | 200–300ms | ease-out | 按钮、卡片悬浮 |
| 过渡/切换 | 300–400ms | ease-in-out | Tab/Toggle 切换 |
| 反馈/提示 | 250–350ms | ease-out | toast 出现/消失 |
| 加载态 | 持续循环 | linear | spinner/skeleton |

### 4.3 交互状态规范

```css
/* 按钮 */
.btn {
  transition: background 0.25s var(--ease-out),
              transform 0.2s var(--ease-out),
              box-shadow 0.25s var(--ease-out);
}
.btn:hover { transform: translateY(-1px); }
.btn:active { transform: translateY(0); }
.btn:focus-visible { outline: 2px solid var(--primary); outline-offset: 2px; }

/* 卡片 */
.card {
  transition: transform 0.4s var(--ease-out-expo),
              box-shadow 0.4s var(--ease-out-expo);
}
.card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

/* 表单输入 */
.form-input {
  transition: border-color 0.2s var(--ease-out),
              box-shadow 0.2s var(--ease-out);
}
.form-input:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 3px color-mix(in oklch, var(--primary), transparent 85%);
}
.form-input:user-invalid {
  border-color: var(--error);
}

/* 链接 */
a {
  transition: color 0.2s var(--ease-out);
  text-decoration-color: color-mix(in oklch, currentColor, transparent 50%);
  text-underline-offset: 2px;
}
a:hover { text-decoration-color: currentColor; }
```

---

## 五、可访问性指南

### 5.1 色彩对比度标准 (WCAG 2.1)

| 级别 | 文本对比度 | 大文本对比度 | UI 组件对比度 |
|------|-----------|-------------|-------------|
| AA | ≥ 4.5:1 | ≥ 3:1 | ≥ 3:1 |
| AAA | ≥ 7:1 | ≥ 4.5:1 | ≥ 3:1 |

> 大文本定义为 ≥ 24px 常规字重或 ≥ 19px 粗体。

### 5.2 焦点样式

```css
/* 始终提供可见的焦点指示 */
:focus-visible {
  outline: 2px solid var(--primary);
  outline-offset: 2px;
  border-radius: 2px;
}

/* 鼠标点击时不显示焦点环（保持默认行为） */
:focus:not(:focus-visible) {
  outline: none;
}
```

### 5.3 语义化 HTML 结构

```html
<!-- 正确的页面结构 -->
<header role="banner">
  <nav aria-label="主导航">
    <ul><!-- ... --></ul>
  </nav>
</header>

<main id="main-content">
  <section aria-labelledby="section1-title">
    <h2 id="section1-title">区块标题</h2>
    <!-- 内容 -->
  </section>
</main>

<footer role="contentinfo">
  <!-- 版权、链接 -->
</footer>
```

### 5.4 减少动画

```css
/* 尊重系统级动画偏好 */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

---

## 六、设计原则与反模式

### 6.1 核心设计哲学

1. **有意为之胜过随机选择** — 每个设计决策都有明确理由，源于设计基调和目的
2. **一致性胜过完美单体** — 基调一致的普通页面比混搭的精美页面更专业
3. **内容即设计** — 排版层级、间距和布局优先级由内容结构驱动
4. **克制是高阶** — 限制字体数(≤2)、颜色数(≤5)、装饰元素(≤2)，在限制中创造
5. **功能决定形式** — 仪表板的首要目标是信息传达，装饰不应干扰数据可读性

### 6.2 AI 风格检测清单（AI Slop Test）

**视觉层面：**
- 是否看起来像 "Bootstrap 默认主题"？
- 能否一眼认出是模板/通用的？
- 色彩是否"太安全"（中灰+浅蓝）？
- 布局是否"太整齐"（全是等宽卡片）？

**字体层面：**
- 是否使用了 Inter/Roboto/Arial/Space Grotesk？
- 所有文字是否都是一个字号层级？
- 标题和正文的对比是否不够？

**动效层面：**
- 动画是否让页面显得"廉价"（bounce、闪烁）？
- 是否有动画但没有目的（装饰性动画过多）？

**最终测试：**
> "如果你给别人看这个页面说'这是 AI 做的'，他们会立刻相信吗？如果是，那就是 AI 风格设计失败。"

---

## 七、外部参考资源

- [Anthropic frontend-design Skill](https://github.com/anthropics/skills/tree/main/skills/frontend-design) — 本 Skill 的设计哲学来源
- [Google Fonts Knowledge](https://fonts.google.com/knowledge) — 字体选择与配对指南
- [OKLCH Color Picker](https://oklch.com/) — OKLCH 色彩在线工具
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/) — 对比度验证工具
- [Coolors.co](https://coolors.co/) — 配色方案生成器
- [Cubic Bezier Generator](https://cubic-bezier.com/) — 缓动函数调试
