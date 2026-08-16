#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""validate-markdown.py — Markdown 渲染安全性校验脚本（codebase-analyzer v2.1）

纯 Python 标准库实现，零第三方依赖。递归校验目录下所有 .md 文件，
按 "文件:行号: [ERROR|WARN] 描述" 输出问题清单，存在 ERROR 时以退出码 1 结束。

校验项
------
ERROR 级（阻断交付）：
  E1 代码围栏未闭合 —— 文件结束时围栏状态未归零
  E2 表格列不一致 —— 数据行/分隔行的单元格数与表头不一致（含未转义竖线导致的错列）
  E3 Mermaid 语法基检 —— 双引号不配对；() [] {} 不配对；flowchart 的 subgraph 与 end 数量不匹配
  E4 相对链接无效 —— 本地链接目标文件不存在
  E5 frontmatter 未闭合 —— 文件以 --- 开头但缺少闭合 ---

WARN 级（提示修复）：
  W1 嵌套围栏未升级 —— 3 反引号的 markdown 围栏内部含围栏线，内层围栏会提前闭合外层
  W2 疑似误写的闭合围栏 —— 围栏线带附加文字（如闭合线误加语言标记），无法闭合上方围栏
  W3 标题层级跳跃 —— 如一级标题之后直接三级标题
  W4 Mermaid 未引号标签 —— [] 或 {} 节点标签含圆括号（含全角），部分渲染器会解析失败

已知限制：
  - 单引号不配对不检查（序列图备注中的英文撇号会造成误报，故仅检查双引号）
  - Mermaid 仅做词法级基检，不做完整语法解析

用法：
  python validate-markdown.py <目录或文件> [更多路径...]

退出码：0 = 通过（允许存在 WARN）；1 = 存在 ERROR 或未找到 .md 文件；2 = 参数错误。
"""

import re
import sys
from pathlib import Path

# Windows 控制台默认 GBK 编码会导致中文输出乱码，强制 stdout/stderr 使用 UTF-8
for _stream in (sys.stdout, sys.stderr):
    try:
        if _stream.encoding and _stream.encoding.lower().replace('-', '') != 'utf8':
            _stream.reconfigure(encoding='utf-8', errors='replace')
    except (AttributeError, ValueError):
        pass

FENCE_RE = re.compile(r'^[ \t]*(`{3,}|~{3,})(.*)$')
HEADING_RE = re.compile(r'^(#{1,6})\s')
DELIM_RE = re.compile(r'^\s*\|?\s*:?-{1,}:?\s*(\|\s*:?-{1,}:?\s*)*\|?\s*$')
LINK_RE = re.compile(r'\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+"[^"]*")?\)')
EXTERNAL_PREFIXES = ('http://', 'https://', 'mailto:', 'tel:', 'data:', '#', 'www.')


def cell_count(line):
    """统计 GFM 表格行的单元格数（以未转义竖线为分隔符，兼容省略首/尾竖线的写法）。"""
    s = line.strip()
    pipes = sum(1 for i, ch in enumerate(s) if ch == '|' and (i == 0 or s[i - 1] != '\\'))
    if pipes == 0:
        return 1
    lead = s.startswith('|')
    trail = s.endswith('|') and (len(s) < 2 or s[-2] != '\\')
    if lead and trail:
        return pipes - 1
    if lead or trail:
        return pipes
    return pipes + 1


def check_mermaid(start_line, content):
    """对一个 mermaid 代码块做词法级基检，返回 (行号, 级别, 描述) 列表。"""
    issues = []
    body = [l for l in content if not l.strip().startswith('%%')]
    text = '\n'.join(body)
    if text.count('"') % 2 == 1:
        issues.append((start_line, 'ERROR', 'E3 Mermaid 块内双引号数量为奇数（不配对）'))
    for o, c, name in (('(', ')', '圆括号'), ('[', ']', '方括号'), ('{', '}', '花括号')):
        if text.count(o) != text.count(c):
            issues.append((start_line, 'ERROR',
                           'E3 Mermaid 块内%s不配对（%d 个 "%s" vs %d 个 "%s"）'
                           % (name, text.count(o), o, text.count(c), c)))
    first = next((l.strip() for l in body if l.strip()), '')
    if first.lower().startswith(('flowchart', 'graph')):
        subs = len(re.findall(r'(?<![A-Za-z0-9_])subgraph(?![A-Za-z0-9_])', text))
        ends = len(re.findall(r'(?<![A-Za-z0-9_])end(?![A-Za-z0-9_])', text))
        if subs != ends:
            issues.append((start_line, 'ERROR',
                           'E3 Mermaid flowchart 的 subgraph（%d）与 end（%d）数量不匹配' % (subs, ends)))
    for k, line in enumerate(content):
        if line.strip().startswith('%%'):
            continue
        for m in re.finditer(r'\[([^"\]\n]*)\]|\{([^"\}\n]*)\}', line):
            seg = m.group(1) if m.group(1) is not None else m.group(2)
            if seg and re.search(r'[()（）]', seg):
                issues.append((start_line + 1 + k, 'WARN',
                               'W4 Mermaid 未引号节点标签含圆括号，建议用双引号包裹标签'))
    return issues


def check_file(path):
    """校验单个 Markdown 文件，返回 (行号, 级别, 描述) 列表；行号 0 表示文件级问题。"""
    issues = []
    try:
        text = path.read_text(encoding='utf-8-sig', errors='replace')
    except OSError as e:
        return [(0, 'ERROR', 'E0 无法读取文件：%s' % e)]
    lines = text.splitlines()

    # E5 frontmatter 完整性
    if lines and lines[0].strip() == '---':
        if not any(l.strip() == '---' for l in lines[1:]):
            issues.append((1, 'ERROR', 'E5 frontmatter 以 --- 开头，但全文缺少闭合的 ---'))

    fence = None          # {'char','count','info','line','content'}
    mermaid_blocks = []   # (start_line, content)
    prev_heading = 0
    in_table = False
    header_cells = 0

    for i, line in enumerate(lines):
        m = FENCE_RE.match(line)
        if fence is not None:
            can_close = (m and m.group(1)[0] == fence['char']
                         and len(m.group(1)) >= fence['count']
                         and not m.group(2).strip())
            if can_close:
                if fence['info'] == 'mermaid':
                    mermaid_blocks.append((fence['line'], fence['content']))
                elif fence['info'] == 'markdown' and fence['count'] == 3:
                    if any(FENCE_RE.match(cl) for cl in fence['content']):
                        issues.append((fence['line'], 'WARN',
                                       'W1 3 反引号的 markdown 围栏内部含围栏线，内层围栏会提前闭合外层，'
                                       '应将外层升级为 4 个及以上反引号'))
                fence = None
            else:
                fence['content'].append(line)
                if (m and m.group(1)[0] == fence['char']
                        and len(m.group(1)) >= fence['count']
                        and m.group(2).strip()):
                    issues.append((i + 1, 'WARN',
                                   'W2 围栏线带附加文字（疑似误写的闭合线），无法闭合上方围栏'))
            continue

        if m:
            fence = {'char': m.group(1)[0], 'count': len(m.group(1)),
                     'info': m.group(2).strip().lower(), 'line': i + 1, 'content': []}
            in_table = False
            continue

        # —— 围栏外的普通 Markdown 行 ——
        hm = HEADING_RE.match(line)
        if hm:
            lvl = len(hm.group(1))
            if prev_heading and lvl > prev_heading + 1:
                issues.append((i + 1, 'WARN', 'W3 标题层级跳跃：H%d 之后直接 H%d' % (prev_heading, lvl)))
            prev_heading = lvl

        has_pipe = '|' in line
        prev_line = lines[i - 1] if i > 0 else ''
        if in_table:
            if not line.strip() or not has_pipe:
                in_table = False
            else:
                c = cell_count(line)
                if c != header_cells:
                    issues.append((i + 1, 'ERROR',
                                   'E2 表格数据行列数（%d）与表头（%d）不一致' % (c, header_cells)))
        elif has_pipe and DELIM_RE.match(line) and prev_line.strip() and '|' in prev_line:
            header_cells = cell_count(prev_line)
            dcells = cell_count(line)
            if dcells != header_cells:
                issues.append((i + 1, 'ERROR',
                               'E2 表格分隔行列数（%d）与表头（%d）不一致' % (dcells, header_cells)))
            in_table = True

        # 相对链接有效性（含表格单元格内的链接）
        for lm in LINK_RE.finditer(line):
            target = lm.group(1)
            if target.startswith(EXTERNAL_PREFIXES) or '://' in target:
                continue
            t = target.split('#')[0]
            if t and not (path.parent / t).exists():
                issues.append((i + 1, 'ERROR', 'E4 相对链接目标不存在：%s' % target))

    if fence is not None:
        issues.append((fence['line'], 'ERROR',
                       'E1 代码围栏未闭合（第 %d 行由 %d 个 %s 开启，至文件结束未闭合）'
                       % (fence['line'], fence['count'], fence['char'])))

    for start_line, content in mermaid_blocks:
        issues.extend(check_mermaid(start_line, content))
    return issues


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    files = []
    for p in argv[1:]:
        pt = Path(p)
        if pt.is_dir():
            files.extend(sorted(pt.rglob('*.md')))
        elif pt.is_file():
            files.append(pt)
        else:
            print('警告: 路径不存在: %s' % p)
    if not files:
        print('未找到任何 .md 文件')
        return 1

    total_err = total_warn = 0
    for f in files:
        issues = check_file(f)
        for ln, lvl, msg in issues:
            print('%s:%d: [%s] %s' % (f, ln, lvl, msg))
        errs = sum(1 for _, l, _ in issues if l == 'ERROR')
        warns = sum(1 for _, l, _ in issues if l == 'WARN')
        total_err += errs
        total_warn += warns
        summary = 'OK' if errs == 0 else '%d ERROR' % errs
        if warns:
            summary += ', %d WARN' % warns
        print('-- %s: %s' % (f, summary))

    print('\n校验完成: %d 个文件, %d 个 ERROR, %d 个 WARN' % (len(files), total_err, total_warn))
    return 1 if total_err else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
