"""Verify document links, citations, SVG metadata and stored probe results."""
import json
import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
errors = []
checked_links = 0


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.ids, self.images, self.remote_assets = [], [], [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.append(a["id"])
        for field in ("href", "src"):
            if field in a:
                self.links.append(a[field])
        if tag == "img":
            self.images.append(a)
        if tag in ("script", "link", "img"):
            resource = a.get("src", a.get("href", ""))
            if resource.startswith(("https:", "http:", "//")):
                self.remote_assets.append(resource)


for document in sorted(ROOT.rglob("*.md")):
    text = document.read_text()
    # Explicit markdown links/images, excluding reference definitions.
    for destination in re.findall(r'\]\(([^)]+)\)', text):
        target = urlsplit(destination)
        if target.scheme or destination.startswith("#"):
            continue
        checked_links += 1
        path = document.parent / unquote(target.path)
        if not path.exists():
            errors.append(f"Broken link: {document.relative_to(ROOT)} -> {destination}")

main = (ROOT / "README.md").read_text()
manifest = json.loads((ROOT / "research/sources.json").read_text())
definitions = dict(re.findall(r'^\[(S\d+)\]: (.+)$', main, re.M))
uses = set(re.findall(r'\[(S\d+)\](?!:)', main))
if uses - definitions.keys():
    errors.append(f"Undefined sources: {uses - definitions.keys()}")
for item in manifest["sources"]:
    if definitions.get(item["id"]) != item["url"]:
        errors.append(f"Drifted source reference: {item['id']}")
    if manifest["commit"] not in item["url"]:
        errors.append(f"Unpinned source: {item['id']}")

page = Links()
page.feed((ROOT / "index.html").read_text())
if len(page.ids) != len(set(page.ids)):
    errors.append("Duplicate HTML ids")
for url in page.links:
    parsed = urlsplit(url)
    if parsed.scheme:
        continue
    if not parsed.path and parsed.fragment:
        if parsed.fragment not in page.ids:
            errors.append(f"Missing HTML anchor {url}")
    elif parsed.path and not (ROOT / unquote(parsed.path)).exists():
        errors.append(f"Broken HTML link {url}")
if page.remote_assets:
    errors.append(f"Remote runtime assets: {page.remote_assets}")
if any(not img.get("alt") for img in page.images):
    errors.append("Image without alt text")

svgs = sorted((ROOT / "assets").glob("*.svg"))
for svg in svgs:
    parsed = ET.parse(svg).getroot()
    ns = "{http://www.w3.org/2000/svg}"
    if parsed.find(f"{ns}title") is None or parsed.find(f"{ns}desc") is None:
        errors.append(f"SVG without title/desc: {svg.name}")
    if parsed.findall(f".//{ns}script"):
        errors.append(f"SVG script: {svg.name}")
probes = json.loads((ROOT / "research/probe-results.json").read_text())
assert len(svgs) == 9
assert len(page.images) == 9
assert len([x for x in page.ids if x.startswith("sec-")]) == 20
assert len(manifest["sources"]) == 69
assert probes["passed"] == 13 and probes["failed"] == 0
result = {"local_markdown_links_checked": checked_links, "chapters": 20,
          "source_files": len(manifest["sources"]), "source_references_used": len(uses),
          "svg_diagrams": len(svgs), "html_images": len(page.images),
          "remote_runtime_assets": len(page.remote_assets), "source_probes_passed": probes["passed"],
          "errors": errors}
(ROOT / "research/artifact-checks.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(result, ensure_ascii=False, indent=2))
raise SystemExit(bool(errors))
