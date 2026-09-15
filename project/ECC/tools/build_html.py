#!/usr/bin/env python3
"""Render README.md as a standalone article; requires markdown-it-py.

Rebuild: python3 project/ECC/tools/build_html.py
The generated HTML embeds the SVGs and needs no network requests to read.
"""

import base64
from html import escape
from pathlib import Path
import re

from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "README.md").read_text(encoding="utf-8")
source = re.sub(r"\A---\n.*?\n---\n", "", source, count=1, flags=re.S)
md = MarkdownIt("commonmark", {"html": True}).enable("table")
body = md.render(source)


def embed(match):
    original = match.group(1)
    image = ROOT / original
    if not image.is_file():
        raise FileNotFoundError(image)
    encoded = base64.b64encode(image.read_bytes()).decode("ascii")
    return 'src="data:image/svg+xml;base64,' + encoded + '"'


body = re.sub(r'src="(assets/[^" ]+\.svg)"', embed, body)
body = re.sub(
    r'<p>(<img [^>]*alt="([^"]*)"[^>]*>)</p>',
    lambda match: '<figure><button type="button" class="diagram-button" aria-label="放大：'
    + match[2] + '">' + match[1] + '</button><figcaption>'
    + match[2] + ' · 点击放大</figcaption></figure>',
    body,
)
body = re.sub(r"(<table>.*?</table>)", r'<div class="table-wrap">\1</div>', body, flags=re.S)
sections = re.findall(r'<a id="([a-z-]+)"></a>\s*\n## (.+)', source)
navigation = "\n".join(f'<a href="#{anchor}">{escape(title)}</a>' for anchor, title in sections)
style = r"""
:root{color-scheme:light;--ink:#183146;--muted:#586c7c;--teal:#087e82;--line:#dce5ed;--bg:#f4f7fa}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:80px}body{margin:0;background:var(--bg);color:var(--ink);font-family:system-ui,-apple-system,'Noto Sans CJK SC','Microsoft YaHei',sans-serif;line-height:1.9;font-size:16px}
a{color:#086e8c;text-decoration:none;text-underline-offset:3px}a:hover{text-decoration:underline}a:focus-visible,summary:focus-visible{outline:3px solid #df9548;outline-offset:4px}
.top{position:sticky;top:0;z-index:5;display:flex;justify-content:space-between;align-items:center;gap:20px;padding:13px 32px;background:#142d42;color:#edf5fa;border-bottom:4px solid #149396;font-size:13px;letter-spacing:.05em}.top a{color:#edf5fa}.brand{font-weight:750;letter-spacing:.14em}.version{color:#bfd4e4}
.layout{display:grid;grid-template-columns:252px minmax(0,900px);gap:36px;max-width:1252px;margin:32px auto;padding:0 24px 70px}aside{position:sticky;top:92px;height:calc(100vh - 120px);overflow:auto;padding:8px 12px 24px 0;scrollbar-width:thin}aside h2{font-size:12px;color:var(--teal);letter-spacing:.12em;margin:0 0 12px}nav a{display:block;font-size:13px;line-height:1.65;color:#526879;padding:7px 10px;border-left:2px solid transparent}nav a:hover,nav a.active{background:#e6f1f2;border-left-color:var(--teal);color:#05676b;text-decoration:none}.aside-note{font-size:12px;line-height:1.8;color:var(--muted);margin:20px 10px}
main{min-width:0;background:#fff;border:1px solid var(--line);border-radius:16px;padding:38px 44px 50px;box-shadow:0 12px 32px #18314605}h1{font-size:32px;line-height:1.5;letter-spacing:-.02em;margin:0 0 26px}h2{font-size:25px;line-height:1.5;margin:48px 0 18px;padding-top:10px;border-top:1px solid var(--line)}h3{font-size:20px;line-height:1.55;margin:32px 0 14px}p{margin:15px 0}strong{font-weight:720;color:#123d50}blockquote{margin:22px 0;padding:12px 20px;border-left:4px solid #1d9295;background:#edf6f5;color:#446373;font-size:14px;overflow-wrap:anywhere}blockquote p{margin:7px 0}ul,ol{padding-left:1.5em}li{margin:7px 0}
code{font-family:'DejaVu Sans Mono',Consolas,monospace;font-size:.84em;background:#edf2f6;padding:.16em .32em;border-radius:4px;overflow-wrap:anywhere}pre{max-width:100%;overflow:auto;padding:21px 23px;background:#142d42;color:#e1edf5;border-radius:11px;line-height:1.75;font-size:14px}pre code{padding:0;background:transparent;color:inherit;border-radius:0;overflow-wrap:normal;font-size:inherit}img{max-width:100%;height:auto;display:block;margin:26px auto;border-radius:12px}main a{overflow-wrap:anywhere}.table-wrap{max-width:100%;overflow:auto;margin:22px 0;border:1px solid var(--line);border-radius:9px}table{border-collapse:collapse;min-width:100%;font-size:14px;line-height:1.8}th,td{padding:12px 14px;text-align:left;vertical-align:top;border-bottom:1px solid var(--line);min-width:115px}th{background:#edf4f8;font-weight:700;color:#24465d}tr:last-child td{border-bottom:0}tbody tr:nth-child(even){background:#f9fbfc}hr{border:0;border-top:1px solid var(--line);margin:38px 0}.mobile-toc{display:none}.footer{font-size:12px;color:var(--muted);text-align:center;margin-top:42px}progress{position:fixed;top:0;left:0;z-index:10;width:100%;height:3px;border:0;background:transparent;appearance:none}progress::-webkit-progress-bar{background:transparent}progress::-webkit-progress-value{background:#f2b769}
@media(min-width:1450px){.layout{grid-template-columns:260px minmax(0,970px);max-width:1330px}main{padding:42px 52px}}
@media(max-width:1000px){.layout{display:block;max-width:890px;margin-top:20px;padding:0 18px 35px}aside{display:none}.mobile-toc{display:block;background:#edf5f6;border:1px solid var(--line);border-radius:9px;padding:12px 16px;margin-bottom:22px}.mobile-toc summary{cursor:pointer;font-weight:650;color:var(--teal)}main{padding:28px}h1{font-size:29px}}
@media(max-width:560px){body{font-size:15px}.top{padding:12px 16px;gap:10px}.version{font-size:11px}.layout{padding:0 10px;margin-top:12px}main{padding:23px 17px;border-radius:11px}h1{font-size:25px}h2{font-size:22px;margin-top:35px}h3{font-size:18px}blockquote{padding:10px 14px}pre{padding:15px;font-size:12px}th,td{padding:10px;min-width:110px}table{font-size:13px}}
@media print{.top,aside,.mobile-toc,progress{display:none}.layout{display:block;max-width:none;padding:0;margin:0}main{padding:0;border:0;box-shadow:none}body{background:#fff;font-size:11pt}a{color:inherit}h2,h3{break-after:avoid}img,pre,tr{break-inside:avoid}.table-wrap{overflow:visible}pre{white-space:pre-wrap;background:#f3f5f7;color:#162f43}h1{font-size:23pt}h2{font-size:18pt}}
figure{margin:26px 0}.diagram-button{display:block;width:100%;padding:0;border:0;border-radius:12px;background:transparent;cursor:zoom-in}.diagram-button img{margin:0}.diagram-button:focus-visible{outline:3px solid #df9548;outline-offset:5px}figcaption{font-size:12px;color:var(--muted);text-align:center;margin-top:8px}dialog{padding:0;width:min(1400px,96vw);max-width:96vw;max-height:94vh;border:1px solid var(--line);border-radius:12px;background:var(--bg);color:var(--ink)}dialog::backdrop{background:#071827c9}.zoom-bar{display:flex;justify-content:space-between;gap:15px;align-items:center;padding:12px 18px;background:#fff;border-bottom:1px solid var(--line);font-size:14px}.zoom-bar button{font:inherit;padding:5px 16px;cursor:pointer;border:1px solid var(--line);border-radius:6px;color:var(--ink);background:#f4f7fa;flex:none}.zoom-body{overflow:auto;max-height:calc(94vh - 90px);padding:12px}.zoom-body img{max-width:none;width:1280px;margin:0 auto}.zoom-hint{font-size:12px;margin:5px 15px 9px;color:var(--muted)}
"""
script = r"""
const progress = document.querySelector('progress');
function updateProgress(){const span=document.documentElement.scrollHeight-innerHeight;progress.value=span>0?scrollY/span:0;}
addEventListener('scroll',updateProgress,{passive:true});addEventListener('resize',updateProgress);updateProgress();
const navLinks=[...document.querySelectorAll('aside nav a')];
const observer=new IntersectionObserver(entries=>{for(const e of entries){if(e.isIntersecting){for(const a of navLinks)a.classList.toggle('active',a.hash==='#'+e.target.id)}}},{rootMargin:'-10% 0px -70% 0px'});
for(const element of document.querySelectorAll('main a[id]'))observer.observe(element);
const viewer=document.querySelector('#diagram-viewer');
for(const button of document.querySelectorAll('.diagram-button'))button.addEventListener('click',()=>{const img=button.querySelector('img');viewer.querySelector('img').src=img.src;viewer.querySelector('img').alt=img.alt;viewer.querySelector('.zoom-title').textContent=img.alt;viewer.showModal();});
viewer.querySelector('button').addEventListener('click',()=>viewer.close());
viewer.addEventListener('click',event=>{if(event.target===viewer)viewer.close();});
"""
html = f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="ECC 2.2.1 源码研究：安装、Hooks、持续学习、Memory Vault、跨宿主适配、编排与评估，附源码实验和 7 张架构图。">
<title>ECC 源码深度解读 · Agent 工程研究</title><style>{style}</style></head>
<body><progress max="1" value="0" aria-label="阅读进度"></progress>
<header class="top"><span class="brand">ECC / ENGINEERING NOTES</span><span class="version">2.2.1 · 8321021 · 2026-09-15</span><a href="README.md">Markdown</a></header>
<div class="layout"><aside><h2>源码研究 / 17 个主题</h2><nav aria-label="章节导航">{navigation}</nav><p class="aside-note">固定提交研究<br>7 张原创架构图<br>16 组上游测试<br>5 组源码实验</p></aside>
<main><details class="mobile-toc"><summary>打开章节目录</summary><nav aria-label="移动版章节导航">{navigation}</nav></details>{body}
<p class="footer">ECC 源码研究 · 本页图像与样式已嵌入，可离线阅读。源码链接需联网，实验文件位于旁边的目录。</p></main></div>
<dialog id="diagram-viewer" aria-label="架构图原尺寸查看器"><div class="zoom-bar"><span class="zoom-title">架构图</span><button type="button">关闭</button></div><div class="zoom-body"><img alt="放大的架构图"></div><p class="zoom-hint">可横向、纵向滚动查看；按 Esc 关闭。</p></dialog>
<script>{script}</script></body></html>'''
(ROOT / "index.html").write_text(html, encoding="utf-8")
print(f"Rendered {ROOT / 'index.html'} ({len(html.encode('utf-8')):,} bytes)")
