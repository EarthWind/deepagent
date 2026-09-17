"""Check documentation artifacts and pinned source evidence; no network needed."""
import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET
from markdown_it import MarkdownIt

base = Path(__file__).resolve().parent.parent
md = MarkdownIt('commonmark', {'html': True}).enable('table')
errors = []

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.ids, self.images = [], set(), []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        if 'href' in attrs:
            self.links.append(attrs['href'])
        if 'src' in attrs:
            self.links.append(attrs['src'])
        if tag == 'img':
            self.images.append(attrs)

documents = [base / 'index.html', *base.rglob('*.md')]
link_count = 0
for doc in documents:
    raw = doc.read_text()
    rendered = md.render(raw) if doc.suffix == '.md' else raw
    parsed = Links(); parsed.feed(rendered)
    for image in parsed.images:
        if not image.get('alt'):
            errors.append(f'Missing image alt: {doc}')
    for value in parsed.links:
        url = urlsplit(value)
        if url.scheme or url.netloc:
            continue
        link_count += 1
        target = (doc.parent / unquote(url.path)).resolve() if url.path else doc
        # These two generated result files are produced by the verification steps.
        if not target.exists() and target.name not in ('artifact-checks.json', 'browser-checks.json'):
            errors.append(f'Broken link: {doc.relative_to(base)} -> {value}')
        if not url.path and url.fragment and unquote(url.fragment) not in parsed.ids:
            errors.append(f'Broken anchor: {doc.relative_to(base)} -> {value}')

for fig in (base / 'assets').glob('*.svg'):
    root = ET.parse(fig).getroot()
    ns = {'svg':'http://www.w3.org/2000/svg'}
    if root.find('svg:title', ns) is None or root.find('svg:desc', ns) is None:
        errors.append(f'Missing accessible SVG title/desc: {fig.name}')

source_checked = 0
if len(sys.argv) > 1:
    root = Path(sys.argv[1])
    for record in json.loads((base / 'research/source-inventory.json').read_text()):
        path = root / record['path']
        if hashlib.sha256(path.read_bytes()).hexdigest() != record['sha256']:
            errors.append(f'Source checksum mismatch: {record["path"]}')
        elif record['symbol'] not in path.read_text().splitlines()[record['line'] - 1]:
            errors.append(f'Source anchor mismatch: {record["id"]}')
        source_checked += 1

raw = (base / 'README.md').read_text()
rendered = md.render(re.sub(r'^---\n.*?\n---\n','',raw,count=1,flags=re.S))
unresolved = re.findall(r'\[[^\]\n]+\]\[[^\]\n]+\]', rendered)
if unresolved:
    errors.append('Unresolved Markdown references: ' + ', '.join(unresolved))
result = {'documents_checked':len(documents),'local_links_checked':link_count,
          'source_anchors_and_hashes_checked':source_checked,
          'svg_count':len(list((base/'assets').glob('*.svg'))),
          'chinese_characters_in_blog':len(re.findall(r'[\u4e00-\u9fff]',raw)),
          'errors':errors,'passed':not errors}
(base / 'research/artifact-checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
sys.exit(1 if errors else 0)
