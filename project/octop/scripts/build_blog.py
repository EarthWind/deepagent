#!/usr/bin/env python3
"""Build local HTML reading editions from the Markdown source."""
import re
from html import escape
from pathlib import Path

from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[1]
PAGES = {"README.md": "index.html", "SOURCE_MAP.md": "source-map.html", "RESEARCH_NOTES.md": "research-notes.html"}
CSS = """
:root{color-scheme:light;--ink:#183449;--muted:#607281;--green:#087b69;--line:#dce5e7}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:28px}
body{margin:0;background:#f3f6f5;color:var(--ink);font-family:system-ui,-apple-system,'Noto Sans CJK SC','Microsoft YaHei',sans-serif;font-size:17px;line-height:1.95}
header{background:#123b3c;color:#eefaf6;padding:42px max(28px,calc((100vw - 1330px)/2));border-bottom:5px solid #57bd9b}
header .eyebrow{font-size:13px;letter-spacing:.16em;color:#a7dcca}header .name{font-size:32px;line-height:1.4;margin:8px 0 12px;font-weight:750}
header p{margin:0;color:#c8e0d9;font-size:14px}header a{color:#c8e0d9}
.layout{max-width:1390px;margin:32px auto 70px;display:grid;grid-template-columns:260px minmax(0,1fr);gap:34px;padding:0 24px}
aside{position:sticky;top:24px;align-self:start;max-height:calc(100vh - 48px);overflow:auto;font-size:13px;line-height:1.65;padding:14px 0}
aside summary{font-size:14px;font-weight:700;margin-bottom:14px;cursor:pointer;color:var(--green)}aside a{display:block;padding:6px 12px;border-left:2px solid var(--line);color:#516775;text-decoration:none}
aside a:hover{color:var(--green);border-color:var(--green);background:#e7f0eb}
main{min-width:0;background:#fff;padding:40px 48px 54px;border:1px solid var(--line);border-radius:12px;box-shadow:0 7px 28px #18344906}
h1{font-size:31px;line-height:1.5;letter-spacing:-.02em;margin:0 0 30px}h2{font-size:25px;margin:60px 0 22px;line-height:1.55;padding-top:24px;border-top:1px solid var(--line);color:#0f655a}h3{font-size:20px;line-height:1.6;margin:32px 0 15px}
p{margin:18px 0}a{color:var(--green);text-underline-offset:3px;overflow-wrap:anywhere}strong{font-weight:720;color:#153c48}
img{display:block;max-width:100%;height:auto;margin:30px auto;border:1px solid #e4eaed;border-radius:9px;background:#f8fafc;cursor:zoom-in}
figure{margin:0}code{font-family:ui-monospace,SFMono-Regular,Consolas,monospace;font-size:.85em;background:#edf3f4;color:#205266;padding:.13em .36em;border-radius:4px;overflow-wrap:anywhere}
pre{background:#132e3b;color:#def2ee;border-radius:9px;padding:22px;overflow:auto;line-height:1.8;font-size:14px}pre code{color:inherit;background:none;padding:0;white-space:pre;overflow-wrap:normal;font-size:inherit}
.table-wrap{overflow:auto;margin:24px 0}table{border-collapse:collapse;min-width:100%;font-size:14px;line-height:1.8}th{background:#edf5f2;color:#15574e;text-align:left}td,th{padding:13px 15px;border:1px solid var(--line);vertical-align:top}td{min-width:110px}tr:nth-child(even) td{background:#fafcfc}
ul,ol{padding-left:1.6em}li{margin:9px 0}blockquote{margin:25px 0;padding:7px 20px;border-left:4px solid #40a78b;background:#edf7f2;color:#3b605c}
hr{border:0;border-top:1px solid var(--line);margin:36px 0}.footer{font-size:13px;color:var(--muted);margin-top:45px;border-top:1px solid var(--line);padding-top:20px}
@media(max-width:1050px){.layout{grid-template-columns:210px minmax(0,1fr);gap:20px}main{padding:30px}}
@media(max-width:760px){body{font-size:16px}header{padding:28px 20px}header .name{font-size:25px}.layout{display:block;margin:16px auto;padding:0 12px}aside{position:static;max-height:none;padding:8px 12px 20px}aside details{max-height:220px;overflow:auto}main{padding:25px 20px;border-radius:8px}h1{font-size:25px}h2{font-size:22px;margin-top:42px}h3{font-size:19px}pre{font-size:12px;padding:16px}img{margin:25px 0}.table-wrap{margin:20px 0}td,th{padding:10px;min-width:130px}}
@media print{header,aside,.footer{display:none}.layout{display:block;margin:0;padding:0}main{padding:0;border:0;box-shadow:none}body{background:white;font-size:11pt}h2,h3{break-after:avoid}img,table{break-inside:avoid}pre{white-space:pre-wrap}}
"""


def render_page(source_name, target_name):
    source = (ROOT / source_name).read_text()
    source = re.sub(r"\A---\n.*?\n---\n", "", source, count=1, flags=re.S)
    md = MarkdownIt("commonmark", {"html": True}).enable("table")
    tokens = md.parse(source)
    toc = []
    used = set()
    for i, token in enumerate(tokens):
        if token.type == "heading_open":
            title = tokens[i + 1].content
            slug = "section-" + re.sub(r"[^\w-]+", "-", title.lower()).strip("-")
            while slug in used:
                slug += "-2"
            used.add(slug)
            token.attrSet("id", slug)
            if token.tag == "h2":
                toc.append(f'<a href="#{escape(slug)}">{escape(title)}</a>')
    body = md.renderer.render(tokens, md.options, {})
    for original, replacement in PAGES.items():
        body = body.replace(f'href="{original}', f'href="{replacement}')
    body = body.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")
    # A normal link opens each vector at original resolution, with no JavaScript.
    body = re.sub(r'<img src="(assets/[^\"]+)"([^>]*)>', r'<a href="\1" target="_blank" rel="noopener"><img src="\1"\2></a>', body)
    title = re.search(r"^# (.+)$", source, re.M).group(1)
    page = f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Octop 固定版本源码调研：架构、执行图、Memory、RAG、多 Agent、MCP/ACP 与工程边界。"><title>{escape(title)}</title><style>{CSS}</style></head>
<body><header><div class="eyebrow">DEEP AGENT · ENGINEERING FIELD NOTES</div><div class="name">OCTOP / 从源码理解 Agent 产品</div><p>2026.09.20 · commit 757fd12 · 8 张原创工程图 · <a href="index.html">正文</a> / <a href="source-map.html">源码索引</a> / <a href="research-notes.html">验证记录</a></p></header>
<div class="layout"><aside><details open><summary>阅读目录</summary>{''.join(toc)}</details></aside><main>{body}<div class="footer">离线阅读版 · 由 <a href="{source_name}">{source_name}</a> 生成 · 图示可点击查看原始 SVG · 无在线字体与第三方脚本</div></main></div></body></html>'''
    (ROOT / target_name).write_text(page)
    print(f"Built {target_name}: {len(toc)} sections")


if __name__ == "__main__":
    for source_name, target_name in PAGES.items():
        render_page(source_name, target_name)
