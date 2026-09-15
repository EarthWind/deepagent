#!/usr/bin/env python3
"""Run a bounded set of upstream ECC tests and preserve their actual output.

Usage: python3 project/ECC/research/run_upstream_checks.py /path/to/ECC
Prepare the pinned checkout with npm ci --ignore-scripts --omit=dev first.
No model calls, plugin installation, or real agent sessions are started here.
"""

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

COMMIT = "8321021c54d670126ce3b2969d5deb880b4b0c2a"
SUITES = [
    "tests/hooks/hook-flags.test.js",
    "tests/hooks/bash-hook-dispatcher.test.js",
    "tests/hooks/posttooluse-dispatcher.test.js",
    "tests/hooks/run-with-flags-truncation.test.js",
    "tests/hooks/config-protection.test.js",
    "tests/hooks/session-end.test.js",
    "tests/hooks/pre-compact.test.js",
    "tests/hooks/observer-memory.test.js",
    "tests/lib/memory-vault.test.js",
    "tests/scripts/memory-mcp.test.js",
    "tests/scripts/instinct-cli-evolve.test.js",
    "tests/scripts/instinct-cli-evolve-generate.test.js",
    "tests/scripts/install-plan.test.js",
    "tests/lib/tmux-worktree-orchestrator.test.js",
    "tests/lib/eval-harness/gate.test.js",
    "tests/lib/eval-harness/receipt.test.js",
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, default=Path(__file__).parent)
    args = parser.parse_args()
    source = args.source.resolve()
    head = subprocess.check_output(
        ["git", "-C", str(source), "rev-parse", "HEAD"], text=True
    ).strip()
    if head != COMMIT:
        parser.error(f"expected {COMMIT}, found {head}; use the article's pinned source")
    output = args.output.resolve()
    logs = output / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    for key in ["GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_COMMON_DIR", "GIT_PREFIX"]:
        env.pop(key, None)
    report = {
        "source_commit": head,
        "started_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "node": subprocess.check_output(["node", "--version"], text=True).strip(),
        "python": sys.version.split()[0],
        "scope": "Selected upstream suites; not the full npm test suite or live model evaluation",
        "suites": [],
    }
    for suite in SUITES:
        started = time.monotonic()
        command = ["node", str(source / suite)]
        try:
            result = subprocess.run(command, cwd=source, env=env, text=True,
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                    timeout=180)
            text = result.stdout
            code = result.returncode
        except subprocess.TimeoutExpired as exc:
            raw = exc.stdout or b""
            text = raw.decode(errors="replace") if isinstance(raw, bytes) else raw
            text += "\nRESEARCH RUNNER: suite exceeded 180 seconds\n"
            code = 124
        filename = suite.removeprefix("tests/").replace("/", "__") + ".txt"
        (logs / filename).write_text(text, encoding="utf-8")
        passed = re.search(r"Passed:\s*(\d+)", text, re.I)
        failed = re.search(r"Failed:\s*(\d+)", text, re.I)
        passed = passed or re.search(r"(\d+)\s+passed", text, re.I)
        failed = failed or re.search(r"(\d+)\s+failed", text, re.I)
        item = {
            "suite": suite,
            "exit_code": code,
            "seconds": round(time.monotonic() - started, 3),
            "reported_passed": int(passed[1]) if passed else None,
            "reported_failed": int(failed[1]) if failed else None,
            "log": "logs/" + filename,
        }
        report["suites"].append(item)
        print(json.dumps(item), flush=True)
        (output / "test-results.json").write_text(
            json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return int(any(item["exit_code"] != 0 for item in report["suites"]))


if __name__ == "__main__":
    sys.exit(main())
