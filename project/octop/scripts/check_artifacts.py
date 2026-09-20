#!/usr/bin/env python3
"""Check local links, HTML anchors, diagram XML and Python syntax."""
import ast
import json
import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[1]


class Document(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.links = []
        self.images = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "a" and "href" in attrs:
            self.links.append(attrs["href"])
        if tag == "img" and "src" in attrs:
            self.images.append(attrs["src"])
            if not attrs.get("alt"):
                raise AssertionError("Image missing alt text")


def main():
    errors = []
    count = 0
    html_docs = {}
    for path in ROOT.glob("*.html"):
        doc = Document()
        doc.feed(path.read_text())
        if len(doc.ids) != len(set(doc.ids)):
            errors.append(f"Duplicate HTML ids: {path.name}")
        html_docs[path.resolve()] = doc
    documents = list(ROOT.rglob("*.md")) + list(ROOT.glob("*.html"))
    for path in documents:
        source = path.read_text()
        doc = Document()
        if path.suffix == ".md":
            source = re.sub(r"\A---\n.*?\n---\n", "", source, count=1, flags=re.S)
            rendered = MarkdownIt("commonmark", {"html": True}).enable("table").render(source)
            # Undefined full reference links survive into rendered text.
            if re.search(r"\]\[[a-z][a-z-]+\]", rendered):
                errors.append(f"Unresolved reference in {path.relative_to(ROOT)}")
            doc.feed(rendered)
        else:
            doc = html_docs[path.resolve()]
        for link in doc.links + doc.images:
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc:
                continue
            target = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path.resolve()
            if not target.exists():
                errors.append(f"Missing link: {path.relative_to(ROOT)} → {link}")
                continue
            if parsed.fragment:
                fragment = unquote(parsed.fragment)
                if target.suffix == ".html" and target in html_docs and fragment not in html_docs[target].ids:
                    errors.append(f"Missing HTML anchor: {link}")
                if target.suffix == ".md" and f'id="{fragment}"' not in target.read_text():
                    errors.append(f"Missing explicit Markdown anchor: {link}")
            count += 1
    svgs = list((ROOT / "assets").glob("*.svg"))
    for path in svgs:
        svg = ET.parse(path).getroot()
        ns = {"s": "http://www.w3.org/2000/svg"}
        if svg.find("s:title", ns) is None or svg.find("s:desc", ns) is None:
            errors.append(f"Missing SVG accessibility labels: {path.name}")
        if "viewBox" not in svg.attrib:
            errors.append(f"Missing SVG viewBox: {path.name}")
    python_files = list(ROOT.rglob("*.py"))
    for path in python_files:
        ast.parse(path.read_text(), filename=str(path))
    report = {"passed": not errors, "documents": len(documents), "local_links_checked": count,
              "svg_diagrams": len(svgs), "python_files_parsed": len(python_files), "errors": errors}
    (ROOT / "research/artifact-checks.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
