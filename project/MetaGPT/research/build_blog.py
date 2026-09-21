"""把 README.md 渲染为离线 HTML。重建依赖 markdown-it-py；阅读成品不需要 Python。"""
import re
from html import escape
from pathlib import Path

from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[1]
markdown = (ROOT / "README.md").read_text()
renderer = MarkdownIt("commonmark", {"html": True}).enable("table")
body = renderer.render(markdown)
chapters = re.findall(r'<a id="(sec-\d+)"></a>\s*\n## (.+)', markdown)
toc = "\n".join(f'<a href="#{key}">{escape(title)}</a>' for key, title in chapters)
# 点击图像可直接打开原始 SVG，便于查看小字；无脚本、无远程字体。
body = re.sub(r'<img src="(assets/[^\"]+\.svg)" alt="([^\"]*)"\s*/?>', r'<a class="diagram" href="\1" target="_blank"><img src="\1" alt="\2" loading="lazy"></a>', body)
body = body.replace("<table>", '<div class="table-scroll"><table>').replace("</table>", "</table></div>")
html = '''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="MetaGPT 固定源码深读：经典 SOP、MGX、RoleZero、消息通信、工具执行、记忆与生产化。">
<title>MetaGPT 源码深读 · Deep Agent</title>
<style>
:root{color-scheme:light;--ink:#183149;--muted:#5a7082;--accent:#087f8c;--line:#dbe4ec}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:24px}
body{margin:0;background:#f3f6fa;color:var(--ink);font:17px/1.95 system-ui,-apple-system,"Noto Sans CJK SC","Microsoft YaHei",sans-serif}
a{color:#087682;text-decoration:none;text-underline-offset:4px}a:hover{text-decoration:underline}
.shell{max-width:1480px;margin:auto;display:grid;grid-template-columns:270px minmax(0,1fr);gap:36px;padding:36px}
aside{position:sticky;top:24px;max-height:calc(100vh - 48px);overflow:auto;align-self:start;padding:12px 12px 20px 0}
.brand{font-size:14px;font-weight:800;letter-spacing:.15em;color:var(--accent)}.edition{font-size:12px;color:var(--muted);margin:8px 0 24px}
nav a{display:block;font-size:13px;line-height:1.65;padding:7px 8px;border-left:2px solid transparent}nav a:hover{border-left-color:var(--accent);background:#e5f0f2;text-decoration:none}
.sidebar-links{border-top:1px solid var(--line);padding-top:18px;margin-top:22px;font-size:13px}
main{min-width:0;background:white;border:1px solid var(--line);border-radius:16px;padding:48px 56px;box-shadow:0 12px 40px #142d4406}
h1{font-size:clamp(28px,3vw,40px);line-height:1.5;letter-spacing:-.02em;margin:0 0 24px;font-weight:800}h2{margin:64px 0 20px;padding-bottom:13px;border-bottom:1px solid var(--line);font-size:27px;line-height:1.5}h3{margin-top:32px;font-size:20px;line-height:1.6}
p{margin:18px 0}li{margin:8px 0}blockquote{margin:24px 0;border-left:4px solid var(--accent);padding:1px 22px;background:#f1f8f9;color:var(--muted)}strong{color:#112e45}
code{font-family:ui-monospace,"DejaVu Sans Mono",monospace;font-size:.86em;background:#eef3f8;padding:2px 5px;border-radius:4px;overflow-wrap:anywhere}pre{padding:22px;background:#122d43;color:#dfedf5;border-radius:10px;overflow:auto;line-height:1.7}pre code{color:inherit;background:none;padding:0;overflow-wrap:normal}
.table-scroll{overflow-x:auto;margin:24px 0}table{border-collapse:collapse;width:100%;font-size:14px;line-height:1.85}th,td{text-align:left;padding:13px 15px;vertical-align:top;border:1px solid var(--line)}th{background:#eaf3f5;color:#155260}tr:nth-child(even) td{background:#f9fbfd}td a{overflow-wrap:anywhere}
img{max-width:100%;height:auto;display:block}.diagram{display:block;margin:30px -20px;border:1px solid var(--line);border-radius:10px;overflow:hidden}.diagram:hover{outline:2px solid #087f8c33}
.topline{color:var(--muted);font-size:12px;margin-bottom:20px;letter-spacing:.08em}footer{margin-top:50px;padding-top:20px;border-top:1px solid var(--line);font-size:13px;color:var(--muted)}
@media(max-width:1050px){.shell{grid-template-columns:205px minmax(0,1fr);gap:20px;padding:24px}main{padding:32px}.diagram{margin:24px 0}}
@media(max-width:760px){.shell{display:block;padding:12px}aside{position:static;max-height:none;padding:8px 8px 20px}nav{display:none}.edition{margin:6px 0}.sidebar-links{display:flex;gap:18px;margin-top:12px;padding-top:10px}main{padding:26px 20px;border-radius:10px}body{font-size:16px}h2{font-size:24px;margin-top:42px}th,td{min-width:130px}pre{font-size:13px;padding:16px}.diagram{overflow:auto}.diagram img{min-width:700px}}
@media print{body{background:white;font-size:11pt}.shell{display:block;padding:0}aside,.topline{display:none}main{border:0;box-shadow:none;padding:0}.diagram,table,pre{break-inside:avoid}h2,h3{break-after:avoid}a{color:inherit}pre{white-space:pre-wrap}img{min-width:0!important}}
</style></head><body><div class="shell"><aside>
<div class="brand">DEEP AGENT / RESEARCH</div><div class="edition">MetaGPT · 2026-09-21<br>Source: 11cdf466d042</div>
<nav aria-label="章节导航">TOC</nav><div class="sidebar-links"><a href="README.md">Markdown 正文</a><br><a href="research/source-map.md">源码地图</a><br><a href="research/verification.md">验证记录</a></div>
</aside><main><div class="topline">SOURCE CODE NOTES · MULTI-AGENT SYSTEMS</div>BODY
<footer>依据固定提交整理。图表为原创源码示意；实验范围见正文。可离线阅读，点击图表查看完整 SVG。</footer>
</main></div></body></html>'''
(ROOT / "index.html").write_text(html.replace("TOC", toc).replace("BODY", body), encoding="utf-8")
print(f"Rendered {len(chapters)} chapters to index.html")
