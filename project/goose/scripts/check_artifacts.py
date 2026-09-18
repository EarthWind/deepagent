#!/usr/bin/env python3
"""Check local blog assets/references and optionally the pinned upstream checkout."""
import argparse
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def check(source_root=None):
    errors = []
    metadata = json.loads((ROOT / "research.json").read_text())
    sources = json.loads((ROOT / "sources.json").read_text())
    for path in ROOT.rglob("*.md"):
        text = path.read_text()
        definitions = dict(re.findall(r"^\[([^\]]+)\]:\s*(\S+)", text, re.M))
        references = re.findall(r"\]\[([^\]]+)\]", text)
        for key in references:
            if key not in definitions:
                errors.append(f"{path.name}: undefined reference {key}")
        # Only Markdown links/images, not arbitrary paths in prose or code.
        for target in re.findall(r"!?\[[^\]\n]*\]\(([^)\n]+)\)", text):
            target = target.strip("<>")
            url = urlsplit(target)
            if url.scheme or target.startswith("#"):
                continue
            local = path.parent / unquote(url.path)
            if not local.exists():
                errors.append(f"{path.name}: missing local link {target}")
        if len(re.findall(r"^```", text, re.M)) % 2:
            errors.append(f"{path.name}: unmatched code fence")

    svgs = sorted((ROOT / "assets").glob("*.svg"))
    for path in svgs:
        tree = ET.parse(path)
        ns = {"svg": "http://www.w3.org/2000/svg"}
        if tree.find("svg:title", ns) is None or tree.find("svg:desc", ns) is None:
            errors.append(f"{path.name}: missing accessible title/description")
        if tree.findall(".//svg:script", ns):
            errors.append(f"{path.name}: unexpected SVG script")

    assert len({s['id'] for s in sources}) == len(sources), "duplicate source IDs"
    for item in sources:
        if metadata["commit"] not in item["url"]:
            errors.append(f"Source {item['id']}: URL is not pinned")

    if source_root:
        source_root = Path(source_root).resolve()
        head = subprocess.check_output(
            ["git", "-C", str(source_root), "rev-parse", "HEAD"], text=True
        ).strip()
        if head != metadata["commit"]:
            errors.append(f"Upstream HEAD {head} differs from pinned commit")
        for item in sources:
            path = source_root / item["path"]
            if not path.exists():
                errors.append(f"Missing source path {item['path']}")
            elif item["line"]:
                lines = path.read_text().splitlines()
                line = item["line"]
                if line > len(lines) or item["anchor_text"] not in lines[line - 1]:
                    errors.append(f"Source anchor mismatch: {item['id']}")

    if errors:
        raise SystemExit("\n".join(errors))
    print(f"OK: Markdown links/fences, {len(svgs)} SVGs, {len(sources)} pinned sources")
    if source_root:
        print("OK: upstream commit, source paths and anchored lines")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path)
    check(parser.parse_args().source_root)
