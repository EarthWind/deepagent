#!/usr/bin/env python3
"""Run small, isolated probes of pinned upstream code without installing Octop.

Loads the original stdlib-only PathLayout, chunk and index modules. Parent
package shells avoid executing Octop's optional dependency imports. The
Deep Agents defaults function is extracted via AST, without rewriting its body.
This is NOT the upstream pytest suite or a live Agent integration test.
"""
import argparse
import ast
import hashlib
import importlib.util
import json
import os
import sys
import tempfile
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("checkout", type=Path)
    parser.add_argument("dependencies", type=Path)
    args = parser.parse_args()
    snapshot = json.loads((ROOT / "research/snapshot.json").read_text())
    # Verify all indexed research sources before making claims about the probes.
    for row in snapshot["files"]:
        if row["package"] == "octop":
            base = args.checkout
        else:
            dep = next(d for d in snapshot["dependencies"] if d["name"] == row["package"])
            base = args.dependencies / dep["url"].rsplit("/", 1)[-1].removesuffix(".tar.gz")
        assert hashlib.sha256((base / row["path"]).read_bytes()).hexdigest() == row["sha256"], row["path"]

    for name in ["octop", "octop.infra", "octop.infra.utils", "octop.infra.knowledge"]:
        pkg = types.ModuleType(name)
        pkg.__path__ = []
        sys.modules[name] = pkg
    load("octop.infra.utils.paths", args.checkout / "src/octop/infra/utils/paths.py")
    chunk = load("octop.infra.knowledge.chunk", args.checkout / "src/octop/infra/knowledge/chunk.py")
    index = load("octop.infra.knowledge.index", args.checkout / "src/octop/infra/knowledge/index.py")
    checks = []

    def check(name, condition, observed):
        assert condition, name
        checks.append({"name": name, "passed": True, "observed": observed})

    text = "".join(chr(0x4e00 + i) for i in range(1600))
    chunks = chunk.chunk_text(text)
    check("default_character_windows", [len(c) for c in chunks] == [800, 800, 240], [len(c) for c in chunks])
    check("overlap_is_120_characters", chunks[0][-120:] == chunks[1][:120], 120)
    try:
        chunk.chunk_text("x", size=3, overlap=3)
    except ValueError:
        check("invalid_overlap_rejected", True, "ValueError")
    else:
        raise AssertionError("invalid overlap accepted")

    old_home = os.environ.get("OCTOP_HOME")
    try:
        with tempfile.TemporaryDirectory(prefix="octop-probe-") as temp:
            os.environ["OCTOP_HOME"] = temp
            idx = index.KnowledgeIndex("test-kb")
            idx.replace_doc_chunks("doc-a", ["aligned", "orthogonal"], [[1, 0], [0, 1]])
            hits = idx.search([1, 0], 2)
            check("cosine_ranking", [h.text for h in hits] == ["aligned", "orthogonal"], [{"text": h.text, "score": h.score} for h in hits])
            try:
                idx.replace_doc_chunks("doc-a", ["bad"], [])
            except ValueError:
                check("bad_replacement_preserves_data", len(idx.search([1, 0], 10)) == 2, "2 old chunks retained")
            else:
                raise AssertionError("invalid replacement accepted")
            idx.replace_doc_chunks("doc-a", ["replacement"], [[0, 1]])
            check("replace_does_not_append", len(idx.search([0, 1], 10)) == 1, "1 replacement chunk")
            idx.replace_doc_chunks("doc-b", ["wrong dimension"], [[1, 0, 0]])
            check("mismatched_dimensions_skipped", len(idx.search([0, 1], 10)) == 1, "3D vector skipped for 2D query")
            try:
                idx.search([0, 0], 1)
            except ValueError:
                check("zero_query_rejected", True, "ValueError")
            else:
                raise AssertionError("zero query accepted")
    finally:
        if old_home is None:
            os.environ.pop("OCTOP_HOME", None)
        else:
            os.environ["OCTOP_HOME"] = old_home

    summary_path = args.dependencies / "deepagents-0.7.9/deepagents/middleware/summarization.py"
    node = next(n for n in ast.parse(summary_path.read_text()).body if isinstance(n, ast.FunctionDef) and n.name == "compute_summarization_defaults")
    scope = {}
    exec(compile("from __future__ import annotations\n" + ast.unparse(node), str(summary_path), "exec"), scope)
    defaults = scope["compute_summarization_defaults"]
    profile = defaults(types.SimpleNamespace(profile={"max_input_tokens": 128000}))
    fallback = defaults(types.SimpleNamespace(profile=None))
    check("profile_summarization_defaults", profile["trigger"] == ("fraction", 0.85) and profile["keep"] == ("fraction", 0.10), profile)
    check("no_profile_summarization_defaults", fallback["trigger"] == ("tokens", 170000) and fallback["keep"] == ("messages", 6), fallback)

    report = {"commit": snapshot["commit"], "source_hashes_verified": len(snapshot["files"]),
              "scope": "Isolated upstream functions; no LLM, external tools, server, or full test suite", "python": sys.version.split()[0], "checks": checks}
    target = ROOT / "research/probe-results.json"
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(f"PASS: {len(checks)} isolated upstream probes; {len(snapshot['files'])} source hashes verified.")


if __name__ == "__main__":
    main()
