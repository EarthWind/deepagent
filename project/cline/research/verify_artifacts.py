"""检查本地 Markdown/HTML 资源、源码证据、SVG、脚本语法和实验报告。"""
import ast
import hashlib
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[1]
parser = MarkdownIt("commonmark", {"html": True}).enable("table")
issues = []
links = []
documents = {}


class Document(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.ids = set()
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            if attrs["id"] in self.ids:
                issues.append(f"Duplicate anchor: {self.path}:{attrs['id']}")
            self.ids.add(attrs["id"])
        for name in ["href", "src"]:
            if name in attrs:
                links.append((self.path, attrs[name]))


for path in sorted([*ROOT.rglob("*.md"), ROOT / "index.html"]):
    doc = Document(path)
    content = path.read_text()
    doc.feed(parser.render(content) if path.suffix == ".md" else content)
    documents[path.resolve()] = doc
for path, link in links:
    url = urlsplit(link)
    if url.scheme or url.netloc:
        continue
    target = (path.parent / unquote(url.path)).resolve() if url.path else path.resolve()
    # This report is the output of this check; it need not exist on first run.
    if not target.exists() and target != ROOT / "research/artifact-checks.json":
        issues.append(f"Missing local link: {path.relative_to(ROOT)} → {link}")
    if url.fragment and target in documents and unquote(url.fragment) not in documents[target].ids:
        issues.append(f"Missing anchor: {link}")
svgs = sorted((ROOT / "assets").glob("*.svg"))
for path in svgs:
    root = ET.parse(path).getroot()
    if root.find("{http://www.w3.org/2000/svg}title") is None:
        issues.append(f"SVG missing title: {path.name}")
    if root.find("{http://www.w3.org/2000/svg}desc") is None:
        issues.append(f"SVG missing description: {path.name}")
for path in ROOT.rglob("*.py"):
    ast.parse(path.read_text(), filename=str(path))
for path in ROOT.rglob("*.mjs"):
    subprocess.run(["node", "--check", str(path)], check=True, capture_output=True)
manifest = json.loads((ROOT / "research/sources.json").read_text())
lab = json.loads((ROOT / "research/runtime-results.json").read_text())
assert lab["upstreamCommit"] == manifest["commit"]
source_hashes = {f["path"]:f["sha256"] for f in manifest["files"]}
for file in lab["loadedSources"]:
    if file["path"] in source_hashes and file["sha256"] != source_hashes[file["path"]]:
        issues.append(f"Experiment / manifest hash mismatch: {file['path']}")
assert len(lab["tests"]) == 13 and all(x["passed"] for x in lab["tests"])
readme = (ROOT / "README.md").read_text()
body = readme.split("<!-- SOURCE_LINKS:")[0]
known_refs = {f["id"] for f in manifest["files"]}
for key in re.findall(r"\[(S\d+)\]", body):
    if key not in known_refs:
        issues.append(f"Unknown source reference: {key}")
diagram_checks = json.loads((ROOT / "research/diagram-checks.json").read_text())
page_checks = json.loads((ROOT / "research/page-checks.json").read_text())
assert diagram_checks["passed"] and all(x["passed"] for x in page_checks.values())
report = dict(passed=not issues, issues=issues, sourceFiles=len(manifest["files"]),
              diagrams=len(svgs), chapters=len(re.findall(r'^## \d+', readme, re.M)),
              chineseCharacters=len(re.findall(r'[\u4e00-\u9fff]', body)),
              localAndRemoteLinksCheckedForLocalResolution=len(links), runtimeTestGroups=len(lab["tests"]),
              readmeSha256=hashlib.sha256(readme.encode()).hexdigest(),
              htmlSha256=hashlib.sha256((ROOT / "index.html").read_bytes()).hexdigest())
(ROOT / "research/artifact-checks.json").write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n")
print(json.dumps(report, ensure_ascii=False, indent=2))
raise SystemExit(0 if not issues else 1)
