# Animation & Transition Reference

本文件列出了 ppt-slide-builder 支持的所有元素动画和页面过渡效果。

---

## 一、元素动画（Element Animations）

所有元素动画通过 CSS class 添加到目标 HTML 元素上触发。当幻灯片变为 `.active` 时，其内部的动画元素自动播放。

### 动画类名一览

| 类名 | 效果 | 时长 | 适用元素 |
|------|------|------|---------|
| `anim-fade-in` | 淡入 | 0.6s | 所有元素 |
| `anim-slide-up` | 从下方滑入 | 0.6s | 所有元素 |
| `anim-slide-down` | 从上方滑入 | 0.6s | 标题、图片 |
| `anim-slide-left` | 从右侧滑入 | 0.6s | 列表、卡片 |
| `anim-slide-right` | 从左侧滑入 | 0.6s | 图片、装饰元素 |
| `anim-scale-in` | 从 0.7 放大 | 0.5s | 图标、图片、CTA 按钮 |
| `anim-rotate-in` | 旋转 -5deg 后归正 | 0.6s | 装饰元素、图片 |
| `anim-blur-in` | 从模糊到清晰 | 0.8s | 背景文字、大标题 |
| `anim-flip-in` | 3D 翻转 | 0.7s | 卡片、区块 |
| `anim-bounce-in` | 弹跳入场（克制） | 0.8s | 数字、指标、强调元素 |
| `anim-typewriter` | 打字机效果 | 1.5s | 短文本（一行内） |
| `anim-highlight` | 背景高亮扫过 | 0.8s | 关键词、引用 |

### 延迟类名

配合动画类名使用，控制错落入场节奏：

| 类名 | 延迟时间 |
|------|---------|
| `anim-delay-1` | 0.1s |
| `anim-delay-2` | 0.2s |
| `anim-delay-3` | 0.3s |
| `anim-delay-4` | 0.4s |
| `anim-delay-5` | 0.5s |
| `anim-delay-6` | 0.6s |
| `anim-delay-7` | 0.7s |
| `anim-delay-8` | 0.8s |
| `anim-delay-9` | 0.9s |
| `anim-delay-10` | 1.0s |

### 使用示例

```html
<h1 class="anim-fade-in">立即出现</h1>
<p class="anim-fade-in anim-delay-2">延迟 0.2s 后出现</p>
<img class="anim-slide-left anim-delay-4" src="..." alt="...">
<div class="anim-scale-in anim-delay-3">
  <h3>这个容器会整体放大入场</h3>
</div>
```

### 错落排行模式

```html
<ul>
  <li class="anim-slide-up">第一项（立即）</li>
  <li class="anim-slide-up anim-delay-1">第二项（延迟 0.1s）</li>
  <li class="anim-slide-up anim-delay-2">第三项（延迟 0.2s）</li>
  <li class="anim-slide-up anim-delay-3">第四项（延迟 0.3s）</li>
  <li class="anim-slide-up anim-delay-4">第五项（延迟 0.4s）</li>
</ul>
```

---

## 二、页面过渡（Slide Transitions）

页面过渡控制翻页时整页的切换动画。通过在 `.presentation` 容器上添加 CSS 类名实现。

### 过渡类名一览

| 类名 | 效果 | 说明 |
|------|------|------|
| `trans-fade` | 交叉淡入淡出 | 平滑切换，无位移 |
| `trans-slide-left` | 向左推入（下一页从右侧滑入） | 自然阅读方向 |
| `trans-slide-right` | 向右推入（上一页从左侧滑入） | 反向浏览方向 |
| `trans-slide-up` | 向上推入 | 垂直翻页感 |
| `trans-zoom` | 缩放过渡 | 当前页缩小退场，下一页放大入场 |
| `trans-flip` | 3D 翻转 | 带透视的翻页效果（有深度感） |
| `trans-none` | 无过渡（直接切换） | 演示模式切换 |

### 使用方式

在 `<div class="presentation">` 上添加过渡类名：

```html
<div class="presentation trans-slide-left" id="presentation">
```

修改过渡：

```html
<!-- 从 slide-left 改为 zoom -->
<div class="presentation trans-zoom" id="presentation">
```

---

## 三、最佳实践

### 动画原则
- 每页动画元素不超过 5 个（避免过于花哨）
- 延迟增量建议 0.1-0.2s（太小无错落感，太大显得拖沓）
- 标题使用 `anim-fade-in` 或 `anim-slide-up` 最自然
- 数据/数字使用 `anim-bounce-in` 或 `anim-scale-in`
- 装饰元素可以使用 `anim-rotate-in` 增加趣味性
- 避免 `anim-typewriter` 用于长文本（限于 1 行，30 字以内）

### 过渡原则
- 内容型演示（报告、教学）推荐 `trans-fade` 或 `trans-slide-left`
- 创意型演示（作品集、展示）可以使用 `trans-zoom` 或 `trans-flip`
- 混合使用：不在一个演示中混用多种过渡类型（除非特别要求）
