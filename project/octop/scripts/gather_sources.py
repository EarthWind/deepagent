#!/usr/bin/env python3
"""Record a pinned source inventory; reads checkouts, never installs or executes them."""
import argparse
import ast
import hashlib
import json
import subprocess
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMIT = "757fd12e5dcae7f9303dbfbbf6321a6986694a8b"
REPO = "https://github.com/TencentCloud/Octop"
FILES = {
    "project": "pyproject.toml",
    "lock": "uv.lock",
    "readme": "README.md",
    "architecture": "docs/architecture.md",
    "adr": "docs/adr/001-single-process-model.md",
    "server": "src/octop/infra/server.py",
    "launch": "src/octop/launch.py",
    "manager": "src/octop/infra/agents/manager.py",
    "processor": "src/octop/infra/gateway/process/processor.py",
    "request": "src/octop/infra/gateway/process/harness_request.py",
    "gateway": "src/octop/infra/gateway/gateway.py",
    "threads": "src/octop/infra/gateway/threads.py",
    "chat-ws": "src/octop/api/routers/chat/ws.py",
    "chat-turn": "src/octop/api/routers/chat/turn.py",
    "chat-routes": "src/octop/api/routers/chat/routes.py",
    "access": "src/octop/api/common/agent.py",
    "limits": "src/octop/infra/agents/runtime_limits.py",
    "security": "src/octop/infra/agents/security/policy_store.py",
    "backend": "src/octop/infra/backend/resolver.py",
    "memory-backend": "src/octop/infra/agents/memory_backend.py",
    "paths": "src/octop/infra/utils/paths.py",
    "kb-tools": "src/octop/infra/knowledge/tools.py",
    "kb-hint": "src/octop/infra/knowledge/hint.py",
    "kb-jobs": "src/octop/infra/knowledge/jobs.py",
    "kb-chunk": "src/octop/infra/knowledge/chunk.py",
    "kb-index": "src/octop/infra/knowledge/index.py",
    "kb-retrieve": "src/octop/infra/knowledge/retrieve.py",
    "kb-params": "src/octop/infra/knowledge/params.py",
    "kb-embed": "src/octop/infra/knowledge/embed.py",
    "connectors": "src/octop/infra/connectors/builder.py",
    "crypto": "src/octop/infra/connectors/crypto.py",
    "plugins": "src/octop/infra/agents/plugins/manager.py",
    "quota": "src/octop/infra/agents/middleware/token_quota.py",
    "cron": "src/octop/infra/cron/manager.py",
    "delivery": "src/octop/infra/cron/delivery.py",
    "frontend": "dashboard/src/pages/Chat/hooks/chatStore.ts",
    "frontend-package": "dashboard/package.json",
    "compose": "docker/docker-compose.yml",
    "acp-cli": "src/octop/cli/commands/acp.py",
    "acp-settings": "src/octop/infra/agents/acp_settings.py",
    "team-doc": "docs/agent-interop-mailbox.md",
    "delegation-doc": "docs/agent-delegation.md",
    "db": "src/octop/infra/db/factory.py",
    "license": "LICENSE",
}
DEPENDENCY_FILES = {
    "orcakit-harness-agent": {
        "h-agent": "src/harness_agent/agent.py",
        "h-config": "src/harness_agent/config/__init__.py",
        "h-memory": "src/harness_agent/memory/runtime.py",
        "h-memory-mw": "src/harness_agent/middleware/memory.py",
        "h-team": "src/harness_agent/teams/team_manager.py",
        "h-inbox": "src/harness_agent/teams/inbox.py",
        "h-peer": "src/harness_agent/middleware/peer.py",
        "h-policy": "src/harness_agent/security/models.py",
        "h-guard": "src/harness_agent/middleware/tool_guard.py",
        "h-backend": "src/harness_agent/backends/__init__.py",
        "h-acp": "src/harness_agent/acp/client.py",
        "h-acp-service": "src/harness_agent/acp/service.py",
    },
    "harness-memory": {
        "m-service": "src/harness_memory/service.py",
        "m-recall": "src/harness_memory/pipeline/recall/__init__.py",
        "m-router": "src/harness_memory/pipeline/recall/router.py",
        "m-readme": "README_CN.md",
    },
    "harness-gateway": {"g-manager": "src/harness_gateway/manager.py"},
    "deepagents": {
        "d-graph": "deepagents/graph.py",
        "d-summary": "deepagents/middleware/summarization.py",
    },
}


def inventory(path):
    raw = path.read_bytes()
    source = raw.decode()
    symbols = []
    if path.suffix == ".py":
        for node in ast.walk(ast.parse(source)):
            if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                symbols.append({"name": node.name, "line": node.lineno, "end": node.end_lineno})
    return {"sha256": hashlib.sha256(raw).hexdigest(), "lines": len(source.splitlines()), "symbols": symbols}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("checkout", type=Path)
    p.add_argument("dependencies", type=Path)
    args = p.parse_args()
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=args.checkout, text=True).strip()
    if head != COMMIT:
        raise SystemExit(f"Expected {COMMIT}; got {head}")
    lock = tomllib.loads((args.checkout / "uv.lock").read_text())
    packages = {p["name"]: p for p in lock["package"]}
    rows = []
    links = []
    page = ["# Octop 源码索引", "", f"调研日期：2026-09-20。Octop 固定提交：`{COMMIT}`。", "",
            "Octop 链接固定到提交；依赖按 `uv.lock` 的发行源码包和 SHA-256 固定。依赖条目的行号指解压后的原文件，不把 GitHub main 当成锁定版本。", ""]
    for key, rel in FILES.items():
        record = {"id": key, "package": "octop", "path": rel, "url": f"{REPO}/blob/{COMMIT}/{rel}", **inventory(args.checkout / rel)}
        rows.append(record)
        links.append(f"[{key}]: {record['url']}")
        page.extend([f'<a id="{key}"></a>', f"## {key}", "", f"[{rel}]({record['url']}) · {record['lines']} 行", ""])
        if record["symbols"]:
            page.append("；".join(f"`{s['name']}` L{s['line']}–{s['end']}" for s in record["symbols"]))
            page.append("")
    deps = []
    for package, mapping in DEPENDENCY_FILES.items():
        pkg = packages[package]
        archive_name = pkg["sdist"]["url"].rsplit("/", 1)[-1]
        archive = args.dependencies / archive_name
        sha = hashlib.sha256(archive.read_bytes()).hexdigest()
        assert f"sha256:{sha}" == pkg["sdist"]["hash"]
        base = args.dependencies / archive_name.removesuffix(".tar.gz")
        deps.append({"name": package, "version": pkg["version"], "url": pkg["sdist"]["url"], "sha256": sha})
        for key, rel in mapping.items():
            record = {"id": key, "package": package, "version": pkg["version"], "path": rel, "url": pkg["sdist"]["url"], **inventory(base / rel)}
            rows.append(record)
            links.append(f"[{key}]: SOURCE_MAP.md#{key}")
            page.extend([f'<a id="{key}"></a>', f"## {key}", "", f"**{package} {pkg['version']}** · `{rel}` · {record['lines']} 行", "",
                         f"[锁定源码包]({record['url']}) · 包 SHA-256：`{sha}`", ""])
            page.append("；".join(f"`{s['name']}` L{s['line']}–{s['end']}" for s in record["symbols"]))
            page.append("")
    snapshot = {"research_date": "2026-09-20", "repository": REPO, "commit": head,
                "commit_time": subprocess.check_output(["git", "show", "-s", "--format=%cI"], cwd=args.checkout, text=True).strip(),
                "project_version": tomllib.loads((args.checkout / "pyproject.toml").read_text())["project"]["version"],
                "dependencies": deps, "files": rows}
    (ROOT / "research/snapshot.json").write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n")
    (ROOT / "SOURCE_MAP.md").write_text("\n".join(page))
    (ROOT / "research/references.md").write_text("\n".join(links) + "\n")
    print(f"Recorded {len(rows)} source files; verified {len(deps)} dependency archives.")


if __name__ == "__main__":
    main()
