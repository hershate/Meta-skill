---
name: study-planner
description: >-
  Plan structured learning paths for beginners who want to learn new
  technologies or subjects. Assesses current level, decomposes topics
  into progressive stages, and generates comprehensive study plans with
  resource recommendations and practice exercises.
  Triggered by: "我想学", "学习路线", "怎么学", "从零开始", "入门",
  "学习计划", "study plan", "learning path", "how to learn",
  "getting started", "从零开始学", "学习规划", "新手".
version: 1.2.0
allowed-tools: Read Write WebSearch WebFetch
---

# Study Planner — 学习路线规划

## Purpose
Plan structured, beginner-friendly learning paths for users who want to learn new
technologies or subjects. Analyze the user's input ($ARGUMENTS) to determine the
target topic and generate a comprehensive learning plan. Lowers the technical
barrier by decomposing complex topics into progressive stages with clear
prerequisites, resource recommendations, and hands-on practice.

## When to Use
- User says "我想学xxx" / "I want to learn XXX" and needs a complete learning plan
- User asks "学习路线" / "learning path" or "怎么学" / "how to learn"
- User asks "从零开始学" / "learn from scratch" or "入门" / "getting started"
- User asks "学习计划" / "study plan" or "学习规划" / "learning plan"
- User has no prior experience with the technology and needs guidance on where to start

## When NOT to Use
- User already has a clear learning plan and only needs study materials organized from existing outlines — use `self-study-guide` instead
- User asks about academic exam preparation (e.g., "计算机原理考试复习") — use `computer-principles-outline` instead
- User only asks for a simple definition or explanation of a technology — answer directly instead
- User requests a specific project implementation rather than a learning route — handle as a coding task instead

## Workflow / Steps

### Step 1: Parse the User's Request
Extract from the user's input:
- **Target technology/topic** to learn (e.g., "我想学前端开发" → 前端开发)
- **Current level** — ask if not mentioned: "你之前有接触过相关技术吗？目前是什么基础？"
- **Learning goal** — ask if unclear: "你想学到什么程度？找工作、做项目、还是兴趣了解？"
- **Time availability** — ask if not mentioned: "你每天大概能投入多少时间学习？"

If the target is too broad (e.g., "我想学编程"), ask a clarifying question to narrow it down
(e.g., "你想学哪方面的编程？网页开发、数据科学、还是移动 App？不同的方向学习路线不同。").

If the user's response remains vague (e.g., "随便" or "都行"), propose 2-3 concrete
options with brief descriptions to help them decide, and ask them to pick one.
If they still don't choose, default to the most beginner-friendly/common option
(e.g., web development for programming topics) and note the assumption.

Record these details for use in Step 5.

### Step 2: Decompose the Topic into a Knowledge Map
Break down the target topic into a dependency graph of prerequisite knowledge:

- **Core prerequisites**: What must be learned first (e.g., HTML before CSS, Python basics before Django)
- **Core knowledge**: The essential parts of the target topic itself
- **Advanced extensions**: Optional deeper topics for later stages
- **Practical projects**: Milestone projects that integrate learned knowledge

For each node in the knowledge map, assess:
- Difficulty level (beginner / intermediate / advanced)
- Estimated study time (weeks)
- Whether it's "must-learn" or "nice-to-have"

If any knowledge node depends on another, document the dependency relationship
(e.g., "must learn JavaScript basics before React").

### Step 3: Design 3-5 Progressive Learning Stages
Organize the knowledge map into progressive stages. A typical structure:

| Stage | Focus | Description |
|-------|-------|-------------|
| Stage 1 | Foundation | Prerequisites and essential background |
| Stage 2 | Core Concepts | The key ideas and basic skills of the target topic |
| Stage 3 | Applied Practice | Building real projects with guided exercises |
| Stage 4 | Deep Dive | Advanced topics and optimization techniques |
| Stage 5 | Mastery | Independent projects and best practices |

For each stage, define:
- **Goal**: A clear, achievable outcome (e.g., "能独立搭建一个个人博客")
- **Topics**: 3-6 specific knowledge points
- **Milestone**: A concrete deliverable (e.g., "用 HTML/CSS 完成个人主页")

Stage design principles:
- Each stage builds naturally on the previous stage
- Stages progress from **concrete → abstract**: start with what the user already understands
- Use **analogies and real-world comparisons** for abstract concepts
- Include **hands-on practice** in every stage (passive learning alone is insufficient)
- Estimated duration: 1-4 weeks per stage (adjust based on user's available study time)

### Step 4: Search for Learning Resources per Stage
Use WebSearch to find quality learning resources for each stage. For each candidate, check:
- Is it free or paid? (prefer free for early stages)
- Is it beginner-friendly? (avoid advanced resources for early stages)
- Primary language? (prefer the user's native language for foundational stages)
- Last updated? (prefer within last 2 years for tech topics)

Search for at least 2 resource types per stage:
- **Interactive tutorials** (e.g., freeCodeCamp, MDN, W3Schools for web dev)
- **Video courses** (e.g., YouTube playlists, Coursera, Bilibili for Chinese users)
- **Reference materials** (e.g., official docs, cheatsheets, books)

**After finding candidate URLs, verify each link via WebFetch before embedding:**

1. **Accessibility check** — Fetch the URL and confirm HTTP 200 (not 404/403/500/connection timeout).
   - If the page fails to load: discard this URL and search for an alternative.
   - If the page redirects: record the final destination URL, not the shortened/redirecting URL.
   - If the site blocks automated fetching: mark as `⚠️ 无法自动验证` and note for manual check.

2. **Self-study suitability check** — Scan the fetched page content (title, headings, first paragraph):
   - Is the content at the right difficulty level for this stage? (beginner stage → should not link to advanced documentation)
   - Is it readable and well-structured? (tutorial format with examples > raw spec/docs)
   - Does the content actually match the described topic? (reject misleading/off-topic pages)

3. **Assign verification status**:
   - `✅ 已验证` = URL loaded (HTTP 200), content confirmed suitable for this stage
   - `⚠️ 存疑` = URL loaded but content level/quality uncertain (include with caution note)
   - `❌ 无效` = URL failed to load → discard entirely, search for alternative

**Strict link verification rules (no exceptions):**
- Only embed `✅ 已验证` links directly into the plan as confirmed resources
- For `⚠️ 存疑` links, include them only with an explicit caution label explaining the uncertainty
- `❌ 无效` links must be entirely omitted and replaced with alternatives
- Never include a URL that hasn't been fetched and verified — no guessing, no extrapolation from similar URLs

**Fallback when verification fails:**
- If a specific URL fails (404/timeout), search for an alternative resource covering the same topic
- If no verified resource can be found for a stage at all, note recommended search keywords and platform names (e.g., "在 Bilibili 搜索 'CSS 入门教程'") rather than including unverified URLs
- Never fabricate a URL just to fill space — a note about what to search for is always preferable to a broken or hallucinated link

### Step 5: Generate the Learning Plan File
First ensure the `study-planner/plans/` directory exists (create with Bash `mkdir -p`
if missing). Then create a structured plan file at `study-planner/plans/<topic-slug>.md`:

```markdown
---
title: "<Topic> 学习路线"
created: <current-date>
level: <user's current level>
goal: <user's learning goal>
estimated_duration: <total estimated time>
stages: <number of stages>
---

## 学习路线总览

<One-paragraph overview — what this path covers and why it's designed this way>

## 前置知识

- <Prerequisite> — <why it's needed and how long to learn>

## 学习路线

### Stage 1: <中文阶段名> (~X 周)
**目标**: <clear achievable goal>

#### 学什么
- <Topic>：<why this matters and what to understand>

#### 推荐资源
- ✅ [Resource](URL) — <what it covers, why it's good for this stage>（已验证链接有效，内容适合自学）
- ⚠️ [Resource](URL) — <what it covers>（无法完全验证，建议自行确认）

#### 动手练习
- <Exercise 1>（~X 小时）
- <Exercise 2>（~X 小时）

✅ **里程碑**：<concrete deliverable>

---

### Stage 2: <中文阶段名> (~X 周)
...
```

### Step 6: Validate Learning Curve and Stage Progression
Before presenting the plan to the user, run a structured self-check on the
generated plan file. Read through every stage and apply the following checks:

**Check 1 — Dependency Closure**
For each stage, verify that ALL prerequisite knowledge required by that stage
was introduced in prior stages. If a stage requires concept X but X first
appears in the same or a later stage: move X to an earlier stage or add a
bridge topic.
- Example: "React hooks" in Stage 3 → verify "JavaScript functions" and
  "state management" were covered in Stage 2.

**Check 2 — Difficulty Step**
Rate each stage's difficulty on a scale of 1–5 (1 = no new concepts, 5 =
expert level). Adjacent stages must NOT differ by more than 2 levels.
- If a jump of 3+ is detected: insert a bridge stage, or redistribute
  content to smooth the transition.
- Example: Stage 2 = level 2, Stage 3 = level 5 → BAD. Restructure so
  Stage 3 = level 3–4.

**Check 3 — Cognitive Load**
Count topics per stage. 3–6 is ideal.
- 7+ topics → overloaded. Split into sub-stages or reduce scope.
- 0–2 topics → too thin. Merge with adjacent stage or expand.
- Each topic should be learnable within the stage's time budget (1–2
  hours/day × days per stage).

**Check 4 — Milestone Feasibility**
For each milestone, verify it is achievable using ONLY knowledge from this
stage and all prior stages. If a milestone requires knowledge from a later
stage: move the prerequisite topic earlier.
- Example: "Build a full-stack blog" in Stage 2 when databases are in
  Stage 4 → downgrade to "Build a static blog with HTML/CSS".

**Check 5 — Beginner's Mind Gap Analysis**
Read through the entire plan as if you were a complete beginner with zero
context. Identify "missing links" — concepts or terms that appear without
prior introduction.
- Pay special attention to: unexplained jargon, assumed domain knowledge,
  skipped logical steps.
- Fill gaps by: adding a topic, adding a bridge stage, or adding a brief
  "what you need to know" note before the topic.

**If any check fails:**
- Use Edit to fix the plan file immediately. Do NOT proceed to Step 7
  until all checks pass at a "caution" level or better.
- If a check fails at "critical" level (cannot be resolved with minor
  edits), restart from Step 3 for the affected stages. When restarting:
  carry over verified resources from Step 4 that are still relevant to
  the new stage structure, and re-run Step 4 only for stages that were
  added or significantly changed.
- Document what was fixed when presenting to the user (e.g.,
  "调整了第 3 阶段的内容顺序，让学习曲线更平滑").

### Step 7: Present to the User
Summarize the generated plan to the user:

- **Total estimated duration** (e.g., "约 12 周，每天 1-2 小时")
- **Number of stages** and what each covers
- **Key resources** found (top 2-3 recommendations)
- **Plan file path**: `study-planner/plans/<topic-slug>.md`
- **If any adjustments were made during Step 6 validation**: briefly
  mention what was changed and why.
- **Offer adjustment**: "如果时间安排不合适，或者想侧重某些方面，告诉我，我可以调整计划。"

## Constraints
- Always start by identifying the user's **current level** before designing the plan — ask explicitly if not mentioned
- Always include **prerequisite knowledge** in the plan — never assume the user already knows "obvious" basics
- Always explain **WHY** each stage/topic is important, not just WHAT to learn
- Always include **hands-on practice/milestones** for each stage — passive learning alone is insufficient for skill acquisition
- Always use **simple language and analogies** for foundational stages — define all technical terms when first introduced
- Never use jargon without explanation — the user is a beginner by definition
- Never skip foundational stages even if they seem "too basic" for the person designing the plan
- Never recommend resources without considering whether they are beginner-friendly and up-to-date
- Output path must be `study-planner/plans/<topic-slug>.md` under the VSCode project root
- If the topic is extremely broad, **must** ask clarifying questions to narrow scope before planning
- For non-technical topics (photography, music, language learning), adjust the resource search accordingly but keep the same stage-based structure
- If WebSearch fails for a particular resource query, fall back to suggesting general search keywords rather than leaving gaps in the plan
- **Always verify each resource URL via WebFetch before embedding** — confirm HTTP 200 and scan content for self-study suitability
- **Never include a URL that failed verification** (non-200 HTTP status, wrong difficulty level, or irrelevant content) — search for an alternative instead
- **Mark verification status clearly** with ✅ (verified and suitable) or ⚠️ (uncertain, manually check) indicators next to each resource link
- **Never fabricate or hallucinate URLs** — if no verified resource exists for a topic, write a note with search keywords rather than inventing a link
- **Verify each URL individually** — do not assume a URL exists just because it follows a known pattern (e.g., do not assume `youtube.com/playlist?list=ABC123` exists without fetching it)
- **Always run the 5-step validation (Step 6) before presenting any plan** — never skip dependency closure, difficulty step, cognitive load, milestone feasibility, and gap analysis checks
- **Fix validation failures before presentation** — if a plan fails any check at "critical" level, it must not be shown to the user until fixed
- **Ensure adjacent stages differ by at most 2 difficulty levels** — a jump from level 2 to level 5 is not acceptable; restructure or insert bridge stages
- **Limit each stage to 3–6 topics** — more than 6 overwhelms beginners; fewer than 2 lacks substance
- **Verify every milestone is achievable with only prior + current stage knowledge** — no forward dependencies on untaught concepts

## Examples

### ✅ Do This — Learning Web Development from Scratch

**User**: "我想学前端开发"

**Assistant's mental model**: User likely has zero programming experience. Start from absolute basics: what is a webpage, how does the internet work, then HTML → CSS → JavaScript.

**Generated output** (`study-planner/plans/frontend-development.md`):

Plan with 4 progressive stages:
1. **HTML & CSS 基础** (2 weeks) — "理解网页结构，能用 HTML 组织内容、CSS 美化页面"
2. **JavaScript 入门** (3 weeks) — "掌握变量、函数、DOM 操作，能写交互式页面"
3. **工具链与框架入门** (3 weeks) — "Git 版本控制、React 基础、构建个人项目"
4. **实战项目** (4 weeks) — "独立完成一个完整的前端项目并部署上线"

Each stage contains: topics with context ("why this matters"), curated free resources, practical exercises, and a clear milestone.

### ❌ Not This — Same Request, Poorly Handled

**User**: "我想学前端开发"

**Wrong response**: "学前端需要学 HTML、CSS、JavaScript、React、Node.js、Webpack..." (just listing tools and technologies without structure)

**Why it's wrong**:
- Lists technologies without explaining WHY each is needed
- No staging or progressive difficulty
- No estimated time commitment or practical milestones
- No resource recommendations
- Assumes the user already understands terms like "Node.js" and "Webpack"
- Overwhelming for a complete beginner

### ✅ Do This — Non-Technical Topic

**User**: "我想学摄影"

**Generated output**: Adjusted plan with practical photography stages:
1. **相机基础与曝光** (1 week) — "光圈、快门、ISO 的概念和配合"
2. **构图与光线** (2 weeks) — "三分法、自然光运用、常见构图技巧"
3. **题材实践** (2 weeks) — "人像/风光/街拍各自要点"
4. **后期与作品集** (2 weeks) — "Lightroom 基础操作、照片管理与筛选"

Each stage uses analogies (e.g., "ISO 就像收音机的音量旋钮——调太高会有噪点") and includes phone-photography alternatives for users without a dedicated camera.

### ❌ Not This — Same Request, Wrong Approach

**User**: "我想学摄影"

**Wrong response**: "先买一台全画幅相机，再看说明书学曝光三要素，然后学构图…" (no structure, no resource, assumes expensive gear)

**Why it's wrong**:
- Assumes the user has (or should buy) expensive equipment
- No stage-based progression with milestones
- No alternative entry points (phone photography)
- No time estimates or practice suggestions

### ✅ Do This — Verified Resource Links

**User**: "我想学 Python，零基础"

**Link verification flow**:
1. WebSearch finds candidate URLs: freeCodeCamp Python tutorial, W3Schools Python, Coursera Python for Everybody
2. WebFetch each URL:
   - `https://www.freecodecamp.org/learn/scientific-computing-with-python/` → HTTP 200, tutorial format with code examples → ✅
   - `https://www.w3schools.com/python/` → HTTP 200, interactive "Try it Yourself" features → ✅
   - `https://www.coursera.org/learn/python-for-everybody` → HTTP 200, syllabus matches beginner level → ✅
3. All three verified → embedded with ✅ badges

**Plan output excerpt**:
```
#### 推荐资源
- ✅ [freeCodeCamp Python 课程](https://www.freecodecamp.org/learn/scientific-computing-with-python/)（已验证，交互式编程练习，适合零基础）
- ✅ [W3Schools Python 教程](https://www.w3schools.com/python/)（已验证，支持在线运行代码）
- ✅ [Coursera - Python for Everybody](https://www.coursera.org/learn/python-for-everybody)（已验证，视频课程+作业）
```

### ❌ Not This — Hallucinated or Unverified Links

**User**: "我想学 Python，零基础"

**Wrong behavior**: Assistant writes URLs without any verification:
```
#### 推荐资源
- [Python 入门教程](https://python-course.com/beginner)  ← ❌ 未验证，可能不存在
- [Best Python Tutorial](https://youtube.com/playlist?list=PL123)  ← ❌ 未验证，playlist ID 是编造的
```

**Why it's wrong**:
- URLs are fabricated based on knowledge of what might exist, not what was confirmed
- No WebFetch was performed to check if the pages actually load
- YouTube playlist ID could be entirely made up
- No content suitability check for beginner level
- If links are broken, the user has no way to tell and will waste time clicking dead ends

### ✅ Do This — Learning Curve Validation Catches Steep Jump

**User**: "我想学后端开发，零基础"

**Initial design (before validation)**:
1. Stage 1: Python 基础 (2 weeks) — variables, functions, loops
2. Stage 2: Django Web 框架 (3 weeks) — ORM, views, templates, REST API
3. Stage 3: 部署与运维 (2 weeks) — Docker, CI/CD, cloud deployment

**Validation Check 2 (Difficulty Step) finds a problem**:
- Stage 1 difficulty: level 1 (basic syntax, no prior knowledge needed)
- Stage 2 difficulty: level 4 (requires understanding HTTP, databases, MVC pattern, all at once)
- Jump: 1→4 = 3 levels ❌ (exceeds max 2-level jump)

**Fix**: Insert a bridge stage:
1. Stage 1: Python 基础 (2 weeks) — level 1
2. **Stage 2 (NEW): 编程进阶与 Web 基础** (2 weeks) — file I/O, HTTP 概念、JSON、简单 CLI 工具 → level 2
3. Stage 3: Django Web 框架 (3 weeks) — level 3
4. Stage 4: 部署与运维 (2 weeks) — level 4

**Validation after fix**: 1→2→3→4 all within 2-level step. ✅ Pass.

### ❌ Not This — Steep Curve Presented as-is

**User**: "我想学后端开发，零基础"

**Wrong behavior**: Present the steep plan without validation:

> "第1阶段学Python基础，第2阶段直接学Django框架，第3阶段学部署。"

**Why it's wrong**:
- Stage 1→2 jump is level 1→4, overwhelming for a beginner
- No validation step caught the issue
- User will struggle: expected to know HTTP, databases, and MVC after only basic Python
- No bridge stage to connect "programming basics" to "web framework"
- High dropout risk due to frustration in Stage 2

## Notes
- The generated plan file is saved to `study-planner/plans/<topic-slug>.md` in the project root
- WebSearch is used to find and verify learning resources; if a search returns no suitable results, suggest manual search keywords rather than leaving empty entries
- For rapidly evolving technologies (frontend frameworks, AI/ML tools), emphasize foundational concepts (programming logic, math basics) that remain relevant as tools change
- If the user wants to modify the plan after generation (e.g., "I have more time per week", "I want to focus on practical projects"), use Edit to update the existing plan file
- The skill works for both technical and non-technical topics, with resource search adapted accordingly
- For complete beginners, prioritize learning resources with interactive exercises and visual explanations over text-heavy documentation
- Daily study time assumption: default to 1-2 hours/day for time estimates; if user specifies different availability, adjust durations proportionally
- Link verification uses WebFetch to check HTTP status and scan page content. Some sites may block automated fetching (e.g., login-walled platforms, anti-bot protection); if a legitimate resource fails automated verification, note it for manual confirmation rather than excluding it entirely
- A single failed WebFetch attempt does not necessarily mean the URL is dead — some sites have transient issues. If a URL fails, try a second search for an alternative before marking the topic as having no resources
- The 5 checks in Step 6 (dependency closure, difficulty step, cognitive load, milestone feasibility, beginner's mind gap analysis) are designed to catch common learning-plan defects. They are not exhaustive — always use your judgment about progression quality
- If a plan has many stages (5+), the "Beginner's Mind Gap Analysis" becomes especially important: it's easy to accidentally skip a step when designing long learning paths
- The difficulty scale (1-5) is subjective. When in doubt, err on the side of rating a stage more difficult — this makes you more likely to catch steep jumps
- Validation may add time to plan generation (especially for multi-stage plans). This is intentional — it's better to spend extra time validating than to deliver a frustrating learning path
