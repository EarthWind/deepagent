"""Validate local links, anchors, references and generated diagrams in the research artifact."""
import hashlib
import json
import re
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET
from markdown_it import MarkdownIt

BASE = Path(__file__).resolve().parent.parent
md = MarkdownIt('commonmark', {'html': True}).enable('table')
errors = []
local_links = 0
remote_links = 0


def check_link(origin, value):
    global local_links, remote_links
    parsed = urlsplit(value)
    if parsed.scheme or value.startswith('//'):
        remote_links += 1
        return
    local_links += 1
    target = (origin.parent / unquote(parsed.path)).resolve() if parsed.path else origin
    if not target.exists():
        errors.append(f'{origin.relative_to(BASE)}: missing {value}')
        return
    if parsed.fragment and target.suffix in {'.md', '.html'}:
        data = target.read_text()
        anchor = unquote(parsed.fragment)
        if not re.search(r'\bid=["\']' + re.escape(anchor) + r'["\']', data):
            errors.append(f'{origin.relative_to(BASE)}: missing explicit anchor {value}')


for file in BASE.rglob('*.md'):
    text = file.read_text()
    env = {}
    tokens = md.parse(text, env)
    references = env.get('references', {})
    for ref in re.findall(r'(?<!!)\[[^\]\n]+\]\[([^\]\n]+)\]', text):
        if ref.upper() not in references:
            errors.append(f'{file.relative_to(BASE)}: undefined reference {ref}')
    def visit(items):
        for token in items:
            if token.type == 'link_open':
                check_link(file, token.attrGet('href'))
            if token.type == 'image':
                check_link(file, token.attrGet('src'))
                if not token.content.strip():
                    errors.append(f'{file}: empty image alt')
            if token.children:
                visit(token.children)
    visit(tokens)


class PageParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        props = dict(attrs)
        for attr in ('href', 'src'):
            if props.get(attr):
                check_link(BASE / 'index.html', props[attr])
        if tag == 'script' or (tag in ('img', 'link') and props.get('src', props.get('href', '')).startswith('http')):
            errors.append('Unexpected external rendering dependency')


PageParser().feed((BASE / 'index.html').read_text())
svgs = sorted((BASE / 'assets').glob('*.svg'))
assert len(svgs) == 8
for file in svgs:
    root = ET.parse(file).getroot()
    ns = {'svg': 'http://www.w3.org/2000/svg'}
    if root.find('svg:title', ns) is None or root.find('svg:desc', ns) is None:
        errors.append(f'{file.name}: missing accessible title/desc')
    width, height = map(float, (root.attrib['width'], root.attrib['height']))
    for node in root.findall('.//svg:text', ns):
        x, y = float(node.attrib['x']), float(node.attrib['y'])
        if not (0 <= x <= width and 0 <= y <= height):
            errors.append(f'{file.name}: text origin outside viewBox')

snapshot = json.loads((BASE / 'research/snapshot.json').read_text())
results = json.loads((BASE / 'research/probe-results.json').read_text())
assert results['commit'] == snapshot['commit']
assert results['passed'] == len(results['results']) == 10
assert all(row['status'] == 'passed' for row in results['results'])
assert len(snapshot['evidence_files']) == 69

report = {
    'local_links_checked': local_links,
    'remote_links_parsed_not_fetched': remote_links,
    'svg_figures': len(svgs),
    'source_fingerprints': len(snapshot['evidence_files']),
    'source_probe_groups_passed': results['passed'],
    'readme_sha256': hashlib.sha256((BASE / 'README.md').read_bytes()).hexdigest(),
    'html_sha256': hashlib.sha256((BASE / 'index.html').read_bytes()).hexdigest(),
    'errors': errors,
}
(BASE / 'research/artifact-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(report, ensure_ascii=False, indent=2))
raise SystemExit(bool(errors))
