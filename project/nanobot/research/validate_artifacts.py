"""Validate article-local links and source permalinks against a pinned checkout."""

import argparse
import ast
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote, urlparse

parser = argparse.ArgumentParser()
parser.add_argument("checkout", type=Path)
args = parser.parse_args()
base = Path(__file__).resolve().parents[1]
commit = "499bf903022f429dd4501fdfbeeccadcb99dd51f"
prefix = f"https://github.com/HKUDS/nanobot/blob/{commit}/"
errors = []
links = set()
source_links = set()
for file in base.rglob("*.md"):
    body = file.read_text()
    for target in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", body):
        links.add((str(file.relative_to(base)), target))
        if target.startswith(prefix):
            source_links.add(target)
            parsed = urlparse(target[len(prefix):])
            source = args.checkout / unquote(parsed.path)
            if not source.is_file():
                errors.append(f"Missing source: {target}")
            elif parsed.fragment:
                match = re.fullmatch(r"L(\d+)(?:-L(\d+))?", parsed.fragment)
                if not match or max(int(x) for x in match.groups() if x) > len(source.read_text().splitlines()):
                    errors.append(f"Invalid source line: {target}")
        elif target.startswith(("https://", "http://")):
            continue
        elif target.startswith("#"):
            if f'id="{target[1:]}"' not in body:
                errors.append(f"Missing explicit anchor in {file.name}: {target}")
        else:
            if not (file.parent / unquote(target.split('#')[0])).exists():
                errors.append(f"Missing local link in {file.name}: {target}")
svgs = sorted((base / "assets").glob("*.svg"))
for svg in svgs:
    root = ET.parse(svg).getroot()
    if root.find("{http://www.w3.org/2000/svg}title") is None:
        errors.append(f"Missing SVG title: {svg.name}")
for path in base.rglob("*.py"):
    ast.parse(path.read_text(), filename=str(path))
result = {
    "markdown_files": len(list(base.rglob("*.md"))),
    "unique_file_link_pairs": len(links),
    "unique_source_permalinks": len(source_links),
    "svg_files": len(svgs),
    "python_files_parsed": len(list(base.rglob("*.py"))),
    "errors": errors,
    "note": "Source links verified against local pinned checkout, not HTTP reachability of every GitHub URL.",
}
print(json.dumps(result, ensure_ascii=False, indent=2))
raise SystemExit(bool(errors))
