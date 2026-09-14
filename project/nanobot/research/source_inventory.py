"""Reproduce source size and provenance; no third-party dependency required."""

import argparse
import hashlib
import json
import subprocess
import tomllib
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("checkout", type=Path)
args = parser.parse_args()
root = args.checkout.resolve()


def git(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(root), *args], text=True).strip()


areas = ["agent", "providers", "session", "channels", "webui"]
counts = {}
for area in areas + [""]:
    files = sorted(p for p in (root / "nanobot" / area).rglob("*.py") if "tests" not in p.relative_to(root).parts)
    counts[f"nanobot/{area}".rstrip("/")] = {
        "python_files": len(files),
        "physical_lines_including_comments_and_blanks": sum(len(p.read_text().splitlines()) for p in files),
    }
key_files = [
    "nanobot/agent/loop.py", "nanobot/agent/runner.py", "nanobot/agent/context.py",
    "nanobot/agent/context_governance.py", "nanobot/agent/memory.py",
    "nanobot/agent/subagent.py", "nanobot/agent/tools/execution.py",
    "nanobot/agent/tools/registry.py", "nanobot/agent/tools/mcp.py",
    "nanobot/session/manager.py", "nanobot/session/recovery.py",
    "nanobot/session/turn_continuation.py", "nanobot/config/schema.py",
]
print(json.dumps({
    "repository": "https://github.com/HKUDS/nanobot",
    "research_date": "2026-09-14",
    "commit": git("rev-parse", "HEAD"),
    "commit_date": git("show", "-s", "--format=%cI", "HEAD"),
    "package_version": tomllib.loads((root / "pyproject.toml").read_text())["project"]["version"],
    "counts": counts,
    "tests_test_files": len(list((root / "tests").rglob("test_*.py"))),
    "key_files": {p: {
        "sha256": hashlib.sha256((root / p).read_bytes()).hexdigest(),
        "physical_lines": len((root / p).read_text().splitlines()),
    } for p in key_files},
}, ensure_ascii=False, indent=2))
