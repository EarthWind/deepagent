"""检查博客本地链接、章节锚点、SVG 结构、Python 语法与记录一致性。"""
import ast
import json
import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[1]
renderer = MarkdownIt("commonmark", {"html": True}).enable("table")


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.ids = [], []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.links.extend(attrs[key] for key in ("href", "src") if key in attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])


docs = {}
for path in sorted(ROOT.rglob("*.md")) + [ROOT / "index.html"]:
    parsed = Links()
    content = path.read_text()
    parsed.feed(renderer.render(content) if path.suffix == ".md" else content)
    docs[path.resolve()] = parsed
    assert len(parsed.ids) == len(set(parsed.ids)), f"Duplicate anchors: {path}"
    assert not re.search(r'\]\[[a-z_]+\]', renderer.render(content)), f"Unresolved references: {path}"

local_links = 0
for path, parsed in docs.items():
    for link in parsed.links:
        split = urlsplit(link)
        if split.scheme or split.netloc:
            continue
        target = (path.parent / unquote(split.path)).resolve() if split.path else path
        assert target.exists(), f"Missing target: {path}: {link}"
        if split.fragment and target in docs:
            assert unquote(split.fragment) in docs[target].ids, f"Missing anchor: {path}: {link}"
        local_links += 1

svgs = sorted((ROOT / "assets").glob("*.svg"))
assert len(svgs) == 7
for path in svgs:
    tree = ET.fromstring(path.read_text())
    assert tree.find("{http://www.w3.org/2000/svg}title") is not None
    assert tree.find("{http://www.w3.org/2000/svg}desc") is not None
    assert tree.attrib["viewBox"].startswith("0 0 1280 ")

scripts = list(ROOT.rglob("*.py"))
for path in scripts:
    ast.parse(path.read_text(), filename=str(path))

probes = json.loads((ROOT / "research/probe-results.json").read_text())
assert probes["passed"] == len(probes["results"]) == 15
assert all(result["status"] == "passed" for result in probes["results"])
trace = json.loads((ROOT / "research/demo-trace.json").read_text())
assert [message["cause_by"] for message in trace["trace"]] == ["UserRequirement", "WriteSpec", "WriteCode", "TestFailed", "WriteCode", "Accepted"]
assert trace["accepted"] and trace["stop_reason"] == "idle"

readme = (ROOT / "README.md").read_text()
report = {"local_links_checked": local_links, "documents": len(docs), "python_files_syntax_checked": len(scripts), "svg_files_xml_checked": len(svgs), "chapters": len(re.findall(r'<a id="sec-\d+"', readme)), "chinese_characters_in_article": len(re.findall(r'[\u4e00-\u9fff]', readme)), "source_files_indexed": len(json.loads((ROOT / "research/sources.json").read_text())["files"]), "isolated_source_probes_passed": probes["passed"], "teaching_trace_events": len(trace["trace"])}
(ROOT / "research/artifact-checks.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(report, ensure_ascii=False, indent=2))
