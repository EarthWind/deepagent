"""Run a bounded selection of upstream checks; no install or real LLM calls."""
import json
import os
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
out = Path(__file__).resolve().parent
env = {**os.environ, "RUFLO_SOURCE": str(root), "RUFLO_FUNNEL": "0"}
loader = out.parent / "examples/source-loader.mjs"
commands = [
    ["node", "--test", "tests/hook-handler-runwithtimeout.test.cjs"],
    ["node", "scripts/smoke-pre-bash-hook.mjs"],
    ["node", "--import", str(loader), "scripts/smoke-router-regex.mjs"],
    ["node", "scripts/smoke-agent-execute-providers.mjs"],
]
records = []
for command in commands:
    result = subprocess.run(command, cwd=root, env=env, text=True,
                            capture_output=True, timeout=45)
    log = Path(command[-1]).name + ".txt"
    (out / "logs" / log).write_text(result.stdout + "\n" + result.stderr)
    records.append({"command": command, "exit_code": result.returncode,
                    "log": "logs/" + log})
    print(command[-1], result.returncode, result.stdout[-350:], flush=True)
(out / "upstream-checks.json").write_text(json.dumps(records, indent=2) + "\n")
sys.exit(0 if all(r["exit_code"] == 0 for r in records) else 1)
