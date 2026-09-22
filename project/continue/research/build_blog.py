"""Render the offline blog. Rebuild dependency: markdown-it-py==3.0.0."""
from html import escape
from pathlib import Path
import re
from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "README.md").read_text()
body = MarkdownIt("commonmark", {"html": True}).enable("table").render(source)
chapters = re.findall(r'<a id="(sec-\d+)"></a>\s*\n## (.+)', source)
toc = "\n".join(f'<a href="#{key}">{escape(title)}</a>' for key, title in chapters)
body = re.sub(r'<img src="(assets/[^\"]+\.svg)" alt="([^\"]*)"\s*/?>',
              r'<a class="diagram" href="\1" target="_blank" rel="noopener"><img src="\1" alt="\2"><span>点击查看原尺寸工程图 ↗</span></a>', body)
body = body.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")
page = '''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Continue 固定源码深读：IDE 与 CLI Agent、模型适配、上下文、RAG、MCP、权限、编辑、补全和恢复。9 张工程图，13 组源码实验。">
<title>Continue 源码深读 · Deep Agent</title>
<style>
:root{color-scheme:light;--ink:#16362f;--muted:#62756a;--green:#147a60;--line:#dce6da}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:28px}body{margin:0;color:var(--ink);background:#f4f6f0;font:17px/1.95 system-ui,-apple-system,"Noto Sans CJK SC","Microsoft YaHei",sans-serif}
a{color:#087b63;text-decoration:none;text-underline-offset:4px}a:hover{text-decoration:underline}a:focus-visible,summary:focus-visible{outline:3px solid #319371;outline-offset:4px}
.shell{max-width:1540px;padding:34px;margin:auto;display:grid;grid-template-columns:264px minmax(0,1fr);gap:36px}aside{position:sticky;top:28px;max-height:calc(100vh - 56px);overflow:auto;align-self:start;padding-right:12px}.brand{font-size:13px;font-weight:800;letter-spacing:.14em}.edition{font-size:12px;line-height:1.8;color:var(--muted);margin:12px 0 22px}
nav a{font-size:13px;line-height:1.65;display:block;padding:7px 8px;border-left:2px solid transparent}nav a:hover{background:#e6eee2;border-left-color:var(--green);text-decoration:none}.side-links{border-top:1px solid var(--line);padding-top:18px;margin-top:20px;font-size:13px;display:grid;gap:8px}
main{min-width:0;background:#fff;border:1px solid var(--line);border-top:6px solid var(--green);border-radius:12px;padding:40px 52px;box-shadow:0 12px 30px #23433306}.kicker{font-size:12px;letter-spacing:.12em;color:var(--muted);margin-bottom:18px}.badges{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:28px}.badges span{font-size:12px;color:#23684d;background:#eaf2e5;border-radius:18px;padding:4px 12px}
h1{font-size:clamp(28px,3vw,40px);line-height:1.55;letter-spacing:-.025em;margin:0 0 25px}h2{font-size:27px;line-height:1.6;margin:62px 0 22px;padding-bottom:12px;border-bottom:1px solid var(--line)}h3{font-size:21px;line-height:1.7;margin:34px 0 16px}p{margin:19px 0}li{margin:8px 0}strong{color:#123c2c}blockquote{margin:24px 0;border-left:4px solid #70a86f;background:#f1f6ed;padding:1px 22px;color:#4b6958}
code{font-family:ui-monospace,"DejaVu Sans Mono",monospace;font-size:.86em;background:#eef3eb;padding:2px 5px;border-radius:4px;overflow-wrap:anywhere}pre{overflow:auto;background:#153b30;color:#e4eee4;border-radius:10px;padding:22px;line-height:1.8}pre code{background:transparent;color:inherit;padding:0;overflow-wrap:normal}
.table-wrap{overflow-x:auto;margin:25px 0}table{border-collapse:collapse;width:100%;font-size:14px;line-height:1.85}th,td{padding:13px 14px;text-align:left;vertical-align:top;border:1px solid var(--line)}th{background:#edf3e8;color:#25573d}tr:nth-child(even) td{background:#fafcf8}td a{overflow-wrap:anywhere}
.diagram{display:block;margin:32px -16px;border:1px solid var(--line);border-radius:10px;overflow:hidden;background:#f5f8f3}.diagram:hover{outline:2px solid #147a6030;text-decoration:none}.diagram img{display:block;width:100%;height:auto}.diagram span{display:block;padding:7px 15px;font-size:12px;border-top:1px solid var(--line);color:var(--muted)}.mobile-toc{display:none}footer{border-top:1px solid var(--line);padding-top:20px;margin-top:50px;font-size:13px;color:var(--muted)}
@media(max-width:1100px){.shell{grid-template-columns:212px minmax(0,1fr);padding:22px;gap:22px}main{padding:32px}.diagram{margin:26px 0}}
@media(max-width:760px){.shell{display:block;padding:12px}aside{position:static;max-height:none;padding:8px 8px 20px}aside nav{display:none}.edition{margin:6px 0}.side-links{display:flex;flex-wrap:wrap;gap:15px;padding-top:10px;margin-top:12px}.mobile-toc{display:block;background:#eef4e8;padding:12px;border-radius:8px;margin:20px 0}.mobile-toc summary{cursor:pointer}main{padding:24px 20px}body{font-size:16px}h2{font-size:23px;margin-top:44px}pre{font-size:13px;padding:16px}th,td{min-width:124px}.diagram{overflow-x:auto}.diagram img{min-width:800px}.diagram span{min-width:800px}}
@media print{.shell{display:block;padding:0}aside,.kicker,.badges,.mobile-toc,.diagram span{display:none}main{border:0;padding:0;box-shadow:none}body{font-size:10.5pt;background:#fff}.diagram{margin:20px 0;break-inside:avoid}h2,h3{break-after:avoid}pre{white-space:pre-wrap}table{font-size:9pt}a{color:inherit}.diagram img{min-width:0!important}}
</style></head><body><div class="shell"><aside><div class="brand">DEEP AGENT / RESEARCH</div><div class="edition">CONTINUE · 2026-09-23<br>Source: 5522c6f44ca0</div><nav aria-label="章节导航">@@TOC@@</nav><div class="side-links"><a href="README.md">Markdown 正文</a><a href="research/source-map.md">源码地图</a><a href="examples/README.md">复现实验</a><a href="research/verification.md">验证记录</a></div></aside><main>
<div class="kicker">CODING AGENT ENGINEERING / IMPLEMENTATION NOTES</div><div class="badges"><span>20 个章节</span><span>9 张原创图</span><span>13 组源码实验</span><span>固定提交 · 可复核</span></div><details class="mobile-toc"><summary>展开章节目录</summary><nav aria-label="移动端章节导航">@@TOC@@</nav></details>
@@BODY@@
<footer>依据官方固定源码独立整理。图示为原创工程图，实验为隔离源码探针。页面没有远程脚本、字体或 CDN 依赖；源码引用联网后可查看。</footer></main></div></body></html>
'''.replace("@@TOC@@", toc).replace("@@BODY@@", body)
(ROOT / "index.html").write_text(page)
print(f"Rendered {len(chapters)} chapters to index.html")
