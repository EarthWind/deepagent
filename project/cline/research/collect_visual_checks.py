"""Read real Chrome DOM measurements, fail on missing results or overflow."""
import json
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ResultParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.active = False
        self.result = ""

    def handle_starttag(self, tag, attrs):
        if tag == "pre" and dict(attrs).get("id") == "check-result":
            self.active = True

    def handle_endtag(self, tag):
        if tag == "pre":
            self.active = False

    def handle_data(self, data):
        if self.active:
            self.result += data


out = Path(sys.argv[1])
checks = {}
for kind in ["diagrams", "desktop", "mobile"]:
    parser = ResultParser()
    parser.feed((out / f"{kind}.dom.html").read_text())
    checks[kind] = json.loads(parser.result)
    if not checks[kind]["passed"]:
        print(json.dumps(checks[kind], ensure_ascii=False, indent=2))
        raise SystemExit(f"Failed visual check: {kind}")
(ROOT / "research/diagram-checks.json").write_text(json.dumps(checks["diagrams"], ensure_ascii=False, indent=2)+"\n")
(ROOT / "research/page-checks.json").write_text(json.dumps({k:v for k,v in checks.items() if k!='diagrams'}, ensure_ascii=False, indent=2)+"\n")
print("All SVG card/canvas bounds and desktop/mobile page checks passed")
