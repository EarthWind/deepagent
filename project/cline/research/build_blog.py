"""将 Markdown 正文渲染为离线图文博客。重建需要 markdown-it-py==3.0.0。"""
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
body = re.sub(r'<img src="(assets/[^\"]+\.svg)" alt="([^\"]*)"\s*/?>', r'<a class="diagram" href="\1" target="_blank" rel="noopener"><img src="\1" alt="\2" loading="lazy"></a>', body)
body = body.replace("<table>", '<div class="table-scroll"><table>').replace("</table>", "</table></div>")
html = '''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Cline 固定源码深读：SDK 架构、Agent 循环、审批、编辑、上下文、恢复，8 张工程图与 13 组离线源码实验。">
<title>Cline 源码深读 · Deep Agent</title>
<style>
:root{color-scheme:light;--ink:#183149;--muted:#5a7082;--accent:#087f8c;--line:#dbe4ec}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:24px}
body{margin:0;background:#f3f6fa;color:var(--ink);font:17px/1.95 system-ui,-apple-system,"Noto Sans CJK SC","Microsoft YaHei",sans-serif}
a{color:#087682;text-decoration:none;text-underline-offset:4px}a:hover{text-decoration:underline}
.shell{max-width:1510px;margin:auto;display:grid;grid-template-columns:276px minmax(0,1fr);gap:34px;padding:36px}
aside{position:sticky;top:24px;max-height:calc(100vh - 48px);overflow:auto;align-self:start;padding:12px 12px 20px 0}
.brand{font-size:14px;font-weight:800;letter-spacing:.15em;color:var(--accent)}.edition{font-size:12px;color:var(--muted);margin:8px 0 24px}
nav a{display:block;font-size:13px;line-height:1.65;padding:7px 8px;border-left:2px solid transparent}nav a:hover{border-left-color:var(--accent);background:#e5f0f2;text-decoration:none}
.sidebar-links{border-top:1px solid var(--line);padding-top:18px;margin-top:22px;font-size:13px}
main{min-width:0;background:white;border:1px solid var(--line);border-radius:16px;padding:48px 52px;box-shadow:0 12px 40px #142d4406}
h1{font-size:clamp(28px,3vw,40px);line-height:1.5;letter-spacing:-.02em;margin:0 0 24px;font-weight:800}h2{margin:64px 0 20px;padding-bottom:13px;border-bottom:1px solid var(--line);font-size:27px;line-height:1.5}h3{margin-top:32px;font-size:20px;line-height:1.6}
p{margin:18px 0}li{margin:8px 0}blockquote{margin:24px 0;border-left:4px solid var(--accent);padding:1px 22px;background:#f1f8f9;color:var(--muted)}strong{color:#112e45}
code{font-family:ui-monospace,"DejaVu Sans Mono",monospace;font-size:.86em;background:#eef3f8;padding:2px 5px;border-radius:4px;overflow-wrap:anywhere}pre{padding:22px;background:#122d43;color:#dfedf5;border-radius:10px;overflow:auto;line-height:1.7}pre code{color:inherit;background:none;padding:0;overflow-wrap:normal}
.table-scroll{overflow-x:auto;margin:24px 0}table{border-collapse:collapse;width:100%;font-size:14px;line-height:1.85}th,td{text-align:left;padding:13px 15px;vertical-align:top;border:1px solid var(--line)}th{background:#eaf3f5;color:#155260}tr:nth-child(even) td{background:#f9fbfd}td a{overflow-wrap:anywhere}
img{max-width:100%;height:auto;display:block}.diagram{display:block;margin:30px -16px;border:1px solid var(--line);border-radius:10px;overflow:hidden}.diagram:hover{outline:2px solid #087f8c33}
.topline{color:var(--muted);font-size:12px;margin-bottom:20px;letter-spacing:.08em}.metrics{display:flex;gap:10px;flex-wrap:wrap;margin:0 0 28px}.metrics span{font-size:12px;padding:4px 12px;background:#edf6f5;color:#116b73;border-radius:20px}footer{margin-top:50px;padding-top:20px;border-top:1px solid var(--line);font-size:13px;color:var(--muted)}
.mobile-toc{display:none}a:focus-visible,summary:focus-visible{outline:3px solid #16a2ad;outline-offset:3px}
@media(max-width:1050px){.shell{grid-template-columns:215px minmax(0,1fr);gap:20px;padding:24px}main{padding:32px}.diagram{margin:24px 0}}
@media(max-width:760px){.shell{display:block;padding:12px}aside{position:static;max-height:none;padding:8px 8px 20px}aside nav{display:none}.edition{margin:6px 0}.sidebar-links{display:flex;gap:18px;margin-top:12px;padding-top:10px}.sidebar-links br{display:none}.mobile-toc{display:block;margin:22px 0;padding:12px;background:#f0f6f8;border-radius:8px}.mobile-toc summary{cursor:pointer}main{padding:26px 20px;border-radius:10px}body{font-size:16px}h2{font-size:24px;margin-top:42px}th,td{min-width:130px}pre{font-size:13px;padding:16px}.diagram{overflow:auto}.diagram img{min-width:760px}}
@media print{body{background:white;font-size:11pt}.shell{display:block;padding:0}aside,.topline,.mobile-toc{display:none}main{border:0;box-shadow:none;padding:0}.diagram,table,pre{break-inside:avoid}h2,h3{break-after:avoid}a{color:inherit}pre{white-space:pre-wrap}img{min-width:0!important}}
</style></head><body><div class="shell"><aside>
<div class="brand">DEEP AGENT / RESEARCH</div><div class="edition">Cline · 2026-09-22<br>Source: 4a56a43f39c2</div>
<nav aria-label="章节导航">TOC</nav><div class="sidebar-links"><a href="README.md">Markdown 正文</a><br><a href="research/source-map.md">源码地图</a><br><a href="research/verification.md">验证记录</a></div>
</aside><main><div class="topline">SOURCE CODE NOTES · CODING AGENT ENGINEERING</div>
<div class="metrics"><span>19 个章节</span><span>8 张原创图</span><span>13 组源码实验</span><span>固定提交 · 可复现</span></div>
<details class="mobile-toc"><summary>展开章节目录</summary><nav aria-label="移动端章节导航">TOC</nav></details>
BODY
<footer>依据 Cline 官方固定源码独立整理。代码事实、隔离实验与工程建议分别标注。页面无远程脚本、字体或 CDN 依赖。点击图像可打开完整 SVG。</footer>
</main></div></body></html>
'''.replace("TOC", toc).replace("BODY", body)
(ROOT / "index.html").write_text(html)
print(f"Rendered {len(chapters)} chapters to index.html")
