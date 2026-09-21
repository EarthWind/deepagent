"""Create temporary Chrome review pages; writes no browser output into the blog.

Usage: python3 project/cline/research/prepare_visual_checks.py /tmp/cline-visual
Then run Chrome headless --dump-dom on diagrams.html and page.html at desktop
and mobile sizes, redirect stdout to diagrams.dom.html / desktop.dom.html /
mobile.dom.html. Pass that directory to collect_visual_checks.py.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
out = Path(sys.argv[1]).resolve()
out.mkdir(parents=True, exist_ok=True)
svgs = sorted((ROOT / "assets").glob("*.svg"))
cards = "\n".join(f'<article data-name="{path.name}">{path.read_text()}</article>' for path in svgs)
diagram_script = r'''
<script>
document.fonts.ready.then(() => {
  const issues = [];
  let textNodes = 0;
  document.querySelectorAll('article').forEach(article => {
    const svg = article.querySelector('svg');
    const size = svg.viewBox.baseVal;
    svg.querySelectorAll('text').forEach(text => {
      textNodes++;
      const b = text.getBBox();
      if (b.x < 0 || b.y < 0 || b.x + b.width > size.width || b.y + b.height > size.height)
        issues.push({image: article.dataset.name, type:'canvas-overflow', text:text.textContent});
    });
    svg.querySelectorAll('[data-card]').forEach(card => {
      const r = card.querySelector('rect').getBBox();
      card.querySelectorAll('text').forEach(text => {
        const b = text.getBBox();
        if (b.x < r.x + 8 || b.x + b.width > r.x + r.width - 8 || b.y < r.y || b.y+b.height > r.y+r.height)
          issues.push({image:article.dataset.name, type:'card-overflow', text:text.textContent,
            right: b.x+b.width, limit:r.x+r.width-8});
      });
    });
  });
  document.querySelector('#check-result').textContent = JSON.stringify({diagramCount:8,textNodes,issues,passed:issues.length===0});
});
</script>'''
(out / "diagrams.html").write_text(f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>Cline diagrams review</title>
<style>body{{margin:0;background:#e5edf2}}main{{display:grid;grid-template-columns:1fr 1fr;gap:12px;padding:12px}}svg{{display:block;width:100%;height:auto}}pre{{font-size:11px;white-space:pre-wrap}}</style>
<main>{cards}</main><pre id="check-result">pending</pre>{diagram_script}</html>''')
page_script = r'''
<script>
const imgs = [...document.querySelectorAll('img')];
imgs.forEach(img => img.loading = 'eager');
Promise.all([document.fonts.ready, ...imgs.map(img => img.complete ? Promise.resolve() : new Promise(r => { img.onload=r; img.onerror=r; }))]).then(() => {
  const r = {viewportWidth:innerWidth,documentWidth:document.documentElement.scrollWidth,
    headingCount:document.querySelectorAll('main h2').length,imageCount:imgs.length,
    brokenImages:imgs.filter(img=>!img.complete||img.naturalWidth===0).map(img=>img.getAttribute('src')),
    mobileTocVisible:getComputedStyle(document.querySelector('.mobile-toc')).display!=='none'};
  r.passed = r.documentWidth<=r.viewportWidth && r.headingCount===19 && r.imageCount===8 && r.brokenImages.length===0;
  const pre=document.createElement('pre'); pre.id='check-result';pre.hidden=true;pre.textContent=JSON.stringify(r);document.body.append(pre);
});
</script>'''
page = (ROOT / "index.html").read_text().replace('<head>', '<head><base href="'+ROOT.as_uri()+'/">')
(out / "page.html").write_text(page.replace('</body>', page_script+'</body>'))
print(f"Created diagrams.html and page.html in {out}")
