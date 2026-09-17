"""Local headless Chrome checks at desktop/mobile widths plus SVG text bounds.
Only temporary copies are instrumented. Screenshots go to a temporary directory.
"""
import html
import json
from pathlib import Path
import re
import subprocess
import tempfile

base = Path(__file__).resolve().parent.parent
work = Path(tempfile.mkdtemp(prefix='ruflo-browser-'))
records = []

def chrome_check(name, document, width, height):
    path = work / (name + '.html')
    path.write_text(document)
    command = ['google-chrome', '--headless=new', '--no-sandbox', '--disable-gpu',
               '--disable-dev-shm-usage', '--no-first-run',
               '--user-data-dir='+str(work/name), f'--window-size={width},{height}',
               '--virtual-time-budget=1500', '--screenshot='+str(work/(name+'.png')),
               '--dump-dom', path.as_uri()]
    run = subprocess.run(command,text=True,capture_output=True,timeout=30,check=True)
    match = re.search(r'<pre id="research-check">(.*?)</pre>',run.stdout,re.S)
    if not match:
        raise RuntimeError(run.stderr+'\nBrowser check output missing')
    result = json.loads(html.unescape(match.group(1)))
    records.append({'name':name,**result})

measurement = '''<pre id="research-check"></pre><script>
addEventListener('load',()=>{const r={viewport:document.documentElement.clientWidth,documentWidth:document.documentElement.scrollWidth,imageCount:document.images.length,brokenImages:[...document.images].filter(i=>!i.complete||i.naturalWidth===0).map(i=>i.src)};r.passed=r.documentWidth<=r.viewport&&r.brokenImages.length===0;document.getElementById('research-check').textContent=JSON.stringify(r)})
</script>'''
page = (base/'index.html').read_text().replace('<head>','<head><base href="'+base.as_uri()+'/">',1)
page = page.replace('loading="lazy"','loading="eager"').replace('</body>',measurement+'</body>')
chrome_check('desktop',page,1440,1100)
chrome_check('mobile',page,420,1000)

svgs=''.join('<section>'+p.read_text()+'</section>' for p in sorted((base/'assets').glob('*.svg')))
diagram_measurement='''<pre id="research-check"></pre><script>
addEventListener('load',()=>{const errors=[];let cards=0;document.querySelectorAll('svg').forEach(s=>{const v=s.viewBox.baseVal;const name=s.querySelector('title').textContent;s.querySelectorAll('text').forEach(t=>{const b=t.getBBox();if(b.x<0||b.y<0||b.x+b.width>v.width||b.y+b.height>v.height)errors.push({name,text:t.textContent,kind:'viewport'})});s.querySelectorAll('[data-card]').forEach(g=>{cards++;const x=+g.dataset.x,y=+g.dataset.y,w=+g.dataset.w,h=+g.dataset.h;g.querySelectorAll('text').forEach(t=>{const b=t.getBBox();if(b.x<x||b.y<y||b.x+b.width>x+w||b.y+b.height>y+h)errors.push({name,card:g.dataset.card,text:t.textContent,kind:'card'})})})});document.getElementById('research-check').textContent=JSON.stringify({svgCount:document.querySelectorAll('svg').length,cardsChecked:cards,textOverflows:errors,passed:errors.length===0})})
</script>'''
chrome_check('figures','<!doctype html><meta charset="utf-8"><style>body{margin:10px;background:#dce5e7}main{display:grid;grid-template-columns:1fr 1fr;gap:10px}section{min-width:0}svg{width:100%;height:auto;display:block}</style><main>'+svgs+'</main>'+diagram_measurement,1300,2000)
output={'engine':'Headless Google Chrome','screenshots_directory':str(work),'checks':records,'passed':all(r['passed'] for r in records)}
(base/'research/browser-checks.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(output,ensure_ascii=False,indent=2))
raise SystemExit(0 if output['passed'] else 1)
