# Reasonix Code Skills — 元技能集合

一套用于**创建、编排、优化和管理** Claude Code / Reasonix Code 技能（Skill）的元技能（Meta-Skill）工具链。

---

## 什么是「元技能」？

普通 Skill 教 AI 做某件事（搜论文、写报告、审代码）。元技能本身也是 Skill，但它的任务是**生成别的 Skill**——分析需求、逆向代码库、拆解复杂任务，最终产出可复用的 `SKILL.md`。

---

## 项目结构

```
.
├── skill-for-skills/          # 核心引擎 — 根据需求描述生成/升级 Skill
│   ├── SKILL.md               # 元技能主文件（三条路径：CREATE / UPGRADE / UPDATE_SUM）
│   ├── sum.md                 # Skill 编写规范参考手册（被所有生成流程引用）
│   └── README.md
│
├── project-to-skill/          # 逆向分析 — 从现有代码库提取架构并转化为 Skill
│   ├── SKILL.md               # 技能主文件（v2.1.0，含过程式忠实保证）
│   ├── references/
│   │   └── step-precision-rules.md   # 步骤精度参考手册（动词/名词速查、验证单）
│   ├── scripts/               # 可执行脚本（预留）
│   ├── templates/             # 模板文件（预留）
│   └── README.md
│
├── skill-chain-planner/       # 任务分解 — 将复杂任务规划为多 Skill 协作链
│   ├── SKILL.md               # 技能主文件（v1.3.0，含三层接口契约 + 风险分析）
│   ├── references/            # 补充文档（预留）
│   ├── scripts/               # 可执行脚本（预留）
│   ├── templates/             # 模板文件（预留）
│   └── README.md
│
├── skill-chain-executor/      # 链执行器 — 按规划批量调用 skill-for-skills 创建子 Skill
│   ├── SKILL.md               # 技能主文件（v1.0.0）
│   └── README.md
│
├── prompt-optimizer/          # 提示词优化 — 12 维定量分析 + 14 种反模式检测
│   ├── SKILL.md               # 技能主文件（v3.0.0）
│   ├── references/            # 补充文档（预留）
│   └── README.md
│
├── LICENSE                    # Apache License 2.0
└── README.md                  # 本文件
```

---

## 各技能可用状态

| 技能 | 版本 | 状态 | 说明 |
|------|------|------|------|
| **skill-for-skills** | v1.0.0 | ✅ **可用** | 完全可用，后续仍会持续优化 |
| **prompt-optimizer** | v3.0.0 | ✅ **可用** | 完全可用 |
| **project-to-skill** | v2.1.0 | 🚧 **测试中** | 仍在测试阶段，**实际不可用** |
| **skill-chain-planner** | v1.3.0 | ⚠️ **已知问题** | 与 skill-chain-executor 的协作问题尚未解决 |
| **skill-chain-executor** | v1.0.0 | ⚠️ **已知问题** | 与 skill-chain-planner 的协作问题尚未解决 |

## 五个技能速览

| 技能 | 版本 | 一句话 | 运行模式 | 触发词示例 |
|------|------|--------|---------|-----------|
| **skill-for-skills** | v1.0.0 | ✅ 根据自然语言描述自动生成符合规范的 SKILL.md（完全可用，后续仍会持续优化） | 内联 | "编写skill" "创建skill" "升级skill" |
| **project-to-skill** | v2.1.0 | 🚧 分析现有代码库，从 6 维度评估适用性后提取架构并生成 Skill（测试中，不可用） | `context: fork` 隔离 | "项目转skill" "codebase to skill" |
| **skill-chain-planner** | v1.3.0 | ⚠️ 用 5W1H+C 框架将复杂任务拆分为多 Skill 链（与 executor 协作问题未解决） | `context: fork` + `agent: Plan` | "任务分解" "skill链规划" |
| **skill-chain-executor** | v1.0.0 | ⚠️ 读取 planner 的规划输出，委托 skill-for-skills 逐个创建（与 planner 协作问题未解决） | 内联 | "执行skill链" "批量创建skill" |
| **prompt-optimizer** | v3.0.0 | ✅ 12 维度定量评分（0-5）+ 14 种反模式检测 + 回归验证的工业级提示词优化 | 内联 | "优化提示词" "prompt engineering" |

---

## 技能之间的关系

<div align="center">

<!-- ===== CORE ENGINE ===== -->
<div style="
  display: inline-block;
  background: #1a1a2e; border: 2px solid #4fc3f7;
  border-radius: 12px; padding: 14px 28px; margin-bottom: 8px;
">
  <div style="font-size: 15px; font-weight: 700; color: #4fc3f7;">skill-for-skills</div>
  <div style="font-size: 12px; color: #90a4ae; margin-top: 2px;">CREATE / UPGRADE / UPDATE_SUM</div>
  <div style="margin-top: 6px;">
    <span style="background: #2e7d32; color: #fff; padding: 2px 8px; border-radius: 4px; font-size: 11px;">✅ 可用</span>
    <span style="color: #90a4ae; font-size: 11px; margin-left: 6px;">核心生成引擎</span>
  </div>
</div>

<div style="margin: 2px 0;">
  <span style="color: #90a4ae; font-size: 13px;">▲ 被委托调用 ▲</span>
</div>

<!-- ===== BRANCHES ===== -->
<table style="margin: 0 auto; border-collapse: collapse;"><tr>

<!-- Left: project-to-skill -->
<td style="vertical-align: top; padding: 0 16px;">
  <div style="
    background: #1a1a2e; border: 2px dashed #ffb74d;
    border-radius: 10px; padding: 12px 18px;
  ">
    <div style="font-size: 14px; font-weight: 700; color: #ffb74d;">project-to-skill</div>
    <div style="font-size: 11px; color: #90a4ae; margin-top: 2px;">从代码库逆向提取</div>
    <div style="margin-top: 6px;">
      <span style="background: #e65100; color: #fff; padding: 2px 8px; border-radius: 4px; font-size: 11px;">🚧 测试中</span>
    </div>
  </div>
  <div style="text-align: center; margin-top: 4px;">
    <span style="color: #78909c; font-size: 10px;">自行生成，不委托 s-f-s</span>
  </div>
</td>

<!-- Center: chain-executor -->
<td style="vertical-align: top; padding: 0 16px;">
  <div style="
    background: #1a1a2e; border: 2px solid #ffb74d;
    border-radius: 10px; padding: 12px 18px;
  ">
    <div style="font-size: 14px; font-weight: 700; color: #ffb74d;">chain-executor</div>
    <div style="font-size: 11px; color: #90a4ae; margin-top: 2px;">按规划批量编排</div>
    <div style="margin-top: 6px;">
      <span style="background: #e65100; color: #fff; padding: 2px 8px; border-radius: 4px; font-size: 11px;">⚠️ 已知问题</span>
    </div>
  </div>
  <div style="text-align: center; margin-top: 4px;">
    <span style="color: #78909c; font-size: 10px;">委托 s-f-s 逐个生成</span>
  </div>
  <div style="text-align: center; margin-top: 6px;">
    <span style="color: #90a4ae; font-size: 13px;">▲ 读取规划输出 ▲</span>
  </div>
  <div style="
    background: #1a1a2e; border: 2px solid #ffb74d;
    border-radius: 10px; padding: 12px 18px; margin-top: 2px;
  ">
    <div style="font-size: 14px; font-weight: 700; color: #ffb74d;">chain-planner</div>
    <div style="font-size: 11px; color: #90a4ae; margin-top: 2px;">复杂任务 → 多 Skill 链规划</div>
    <div style="font-size: 11px; color: #78909c;">只输出规划文档，不生成 Skill</div>
    <div style="margin-top: 6px;">
      <span style="background: #e65100; color: #fff; padding: 2px 8px; border-radius: 4px; font-size: 11px;">⚠️ 已知问题</span>
    </div>
  </div>
</td>

</tr></table>

<!-- ===== INDEPENDENT ===== -->
<div style="margin-top: 20px;">
  <div style="
    display: inline-block;
    background: #1a1a2e; border: 2px solid #66bb6a;
    border-radius: 10px; padding: 12px 22px;
  ">
    <div style="font-size: 14px; font-weight: 700; color: #66bb6a;">prompt-optimizer</div>
    <div style="font-size: 11px; color: #90a4ae; margin-top: 2px;">12 维定量分析 + 14 种反模式检测</div>
    <div style="margin-top: 6px;">
      <span style="background: #2e7d32; color: #fff; padding: 2px 8px; border-radius: 4px; font-size: 11px;">✅ 可用</span>
      <span style="color: #90a4ae; font-size: 11px; margin-left: 6px;">独立工具，不依赖其他技能</span>
    </div>
  </div>
</div>

</div>

### 推荐工作流

```
创建单个 Skill（✅ 可用）：
  用户需求 ──→ skill-for-skills ──→ SKILL.md + README.md

提示词优化（✅ 可用）：
  原始提示词 ──→ prompt-optimizer ──→ 优化后提示词 + 质量对比报告

代码库转 Skill（🚧 测试中，暂不可用）：
  代码库 ──→ project-to-skill ──→ SKILL.md + README.md

复杂多 Skill 任务（⚠️ planner 与 executor 协作问题未解决）：
  chain-planner ──→ chain-executor ──→ skill-for-skills（× N）
```

---

## 核心技术特性

### 渐进式加载

所有生成的 Skill 遵循三层渐进式加载模型：

| 层级 | 内容 | Token 预算 | 加载时机 |
|------|------|-----------|---------|
| L1 — 元数据 | `name` + `description` | ~100 tokens | Agent 启动时发现 |
| L2 — 指令 | `SKILL.md` 正文 | < 5000 tokens | 技能被激活时加载 |
| L3 — 资源 | `references/` `scripts/` 等 | 按需 | 运行时按需拉取 |

### 精度保障（project-to-skill v2.1.0）

- **过程式忠实保证**：循环边界、重试次数、退避公式、错误恢复路径严格按源码记录，不简化
- **L1+L2+L3 三层提取**：功能摘要 + 步骤参数 + 异常路径逐层保留
- **精度交叉验证**：生成后对照源代码执行参数完整性、分支覆盖、幻觉检测三轮验证

### 定量闭环（prompt-optimizer v3.0.0）

- **12 维评分**：每维度 0-5 分，含 0/3/5 分锚点示例
- **14 种反模式**：万能提示词、冲突约束、幽灵输出、提示词注入漏洞等
- **回归验证**：优化后重新通过 12 维度分析，检测是否引入新问题

### 三层接口契约（skill-chain-planner v1.3.0）

- 每个子 Skill 必须定义输入/输出/错误契约
- 隐式耦合检测（文件级、环境级、时序级、语义级）
- 静默降级识别（内容层面、边界层面、数据类型层面）

---

## 安装与使用

### 安装

将需要的技能目录复制到项目的 `.claude/skills/` (Claude Code) 或 `.reasonix/skills/` (Reasonix Code) 下：

```bash
# 以 skill-for-skills 为例
cp -r skill-for-skills /path/to/your/project/.claude/skills/

# 或安装到用户级（所有项目可用）
cp -r skill-for-skills ~/.claude/skills/
```

重启 Claude Code / Reasonix Code 后即可通过斜杠命令或触发关键词激活。

### 使用示例

```bash
# 创建一个新 Skill
/skill-for-skills 帮我写一个能从 arXiv 搜索论文并生成摘要的 skill

# 从现有代码库生成 Skill
/project-to-skill ../my-tool

# 拆分复杂任务
/skill-chain-planner 我需要一个完整的实验报告自动生成流水线：
  输入 docx/pdf → 转 markdown → 格式化 → 内容总结 → 生成报告

# 执行规划
/chain-executor skill-chain-planner/plans/lab-report/

# 优化提示词
/prompt-optimizer Python代码审查 | 检查这段代码有什么问题
```

---

## 体系现状与已知局限

### 当前可用

目前只有两个技能可在生产环境中使用：

- **skill-for-skills** — 完全可用，从自然语言需求生成 Skill 的链路已跑通，后续仍会持续优化
- **prompt-optimizer** — 完全可用，12 维分析框架和回归验证均正常工作

### 暂不可用

- **project-to-skill** — 仍在测试阶段，代码库逆向分析到 Skill 生成的链路尚未稳定，**实际不可用**
- **skill-chain-planner + skill-chain-executor** — 两者的协作机制存在已知问题：planner 输出的规划格式与 executor 期望的输入格式之间存在不匹配，链式批量创建尚不能端到端运行

### 长期待补全

- **自动化测试**：缺少 Skill 的运行时验证工具（输入 → 执行 → 输出 → 校验）
- **分发与注册管理**：目前需手动复制目录到 `.claude/skills/`
- **运行监控**：无 Skill 使用频率、成功率、失败原因统计
- **持续维护**：无外部 API 变更检测、依赖版本过期提醒
- **冲突检测**：无 Skill 间的功能去重与合并分析

---

## 许可证

本项目基于 **Apache License 2.0** 开源。

```
Copyright 2025 Reasonix Code Skills Contributors

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

完整的许可证文本见仓库根目录下的 [LICENSE](./LICENSE) 文件。

---

## 免责声明

1. **按"原样"提供，不提供任何形式的保证。** 本项目中的技能（Skills）按"现状"（AS IS）提供，不附带任何明示或默示的保证，包括但不限于对适销性、特定用途适用性、或不侵权的默示保证。

2. **使用风险由您自行承担。** 在任何情况下，项目贡献者均不对因使用本项目而产生的任何直接、间接、附带、特殊、惩罚性或后果性损害承担责任，无论该等损害是否基于合同、侵权（包括过失）、严格责任或其他法律理论。

3. **AI 生成内容的验证责任。** 本项目中的元技能会**自动生成**下游技能（SKILL.md 文件）。这些生成物由 AI 模型自动产出，可能包含错误、过时信息或不准确的描述。用户有责任在使用前审查和验证任何自动生成的内容，特别是在涉及：
   - 生产环境操作
   - 破坏性命令（删除、覆盖、部署）
   - 外部 API 调用
   - 敏感数据处理

4. **第三方依赖。** 本项目生成的下游技能可能引用第三方 API、库或服务。项目贡献者不对这些第三方服务的可用性、安全性或合规性负责。

5. **不构成专业建议。** 本项目仅为自动化工具集合，不构成任何形式的专业建议（法律、医疗、金融、安全等）。

6. **贡献者免责。** "Reasonix Code Skills Contributors" 包括所有向本仓库提交代码、文档或其他内容的个人或实体。贡献者不因其贡献而承担超出 Apache 2.0 许可证条款的额外责任。
