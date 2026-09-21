"""从固定 checkout 生成源文件哈希、方法锚点和博客引用。只使用 Python 标准库。"""
import argparse
import ast
import hashlib
import json
import re
import subprocess
from pathlib import Path

COMMIT = "11cdf466d042aece04fc6cfd13b28e1a70341b1f"
ROOT = Path(__file__).resolve().parents[1]
FILES = {
    "setup": "setup.py",
    "entry": "metagpt/software_company.py",
    "team": "metagpt/team.py",
    "env": "metagpt/environment/base_env.py",
    "mgx": "metagpt/environment/mgx/mgx_env.py",
    "role": "metagpt/roles/role.py",
    "schema": "metagpt/schema.py",
    "action": "metagpt/actions/action.py",
    "node": "metagpt/actions/action_node.py",
    "context": "metagpt/context.py",
    "context_mixin": "metagpt/context_mixin.py",
    "pm": "metagpt/roles/product_manager.py",
    "architect": "metagpt/roles/architect.py",
    "project_manager": "metagpt/roles/project_manager.py",
    "engineer": "metagpt/roles/engineer.py",
    "qa": "metagpt/roles/qa_engineer.py",
    "prepare": "metagpt/actions/prepare_documents.py",
    "prd": "metagpt/actions/write_prd.py",
    "prd_nodes": "metagpt/actions/write_prd_an.py",
    "design": "metagpt/actions/design_api.py",
    "design_nodes": "metagpt/actions/design_api_an.py",
    "tasks": "metagpt/actions/project_management.py",
    "write_code": "metagpt/actions/write_code.py",
    "run_code": "metagpt/actions/run_code.py",
    "rz": "metagpt/roles/di/role_zero.py",
    "leader": "metagpt/roles/di/team_leader.py",
    "engineer2": "metagpt/roles/di/engineer2.py",
    "analyst": "metagpt/roles/di/data_analyst.py",
    "di": "metagpt/roles/di/data_interpreter.py",
    "planner": "metagpt/strategy/planner.py",
    "notebook": "metagpt/actions/di/execute_nb_code.py",
    "registry": "metagpt/tools/tool_registry.py",
    "tool_convert": "metagpt/tools/tool_convert.py",
    "recommender": "metagpt/tools/tool_recommend.py",
    "terminal": "metagpt/tools/libs/terminal.py",
    "editor": "metagpt/tools/libs/editor.py",
    "rz_utils": "metagpt/utils/role_zero_utils.py",
    "memory": "metagpt/memory/memory.py",
    "long_memory": "metagpt/memory/role_zero_memory.py",
    "memory_config": "metagpt/configs/role_zero_config.py",
    "exp_config": "metagpt/configs/exp_pool_config.py",
    "exp_decorator": "metagpt/exp_pool/decorator.py",
    "project_repo": "metagpt/utils/project_repo.py",
    "file_repo": "metagpt/utils/file_repository.py",
    "dependency": "metagpt/utils/dependency_file.py",
    "common": "metagpt/utils/common.py",
    "config": "metagpt/config2.py",
    "llm_config": "metagpt/configs/llm_config.py",
    "base_llm": "metagpt/provider/base_llm.py",
    "provider_registry": "metagpt/provider/llm_provider_registry.py",
    "openai_provider": "metagpt/provider/openai_api.py",
    "cost": "metagpt/utils/cost_manager.py",
    "report": "metagpt/utils/report.py",
    "tests_env": "tests/metagpt/test_environment.py",
    "tests_team": "tests/metagpt/test_team.py",
    "tests_leader": "tests/metagpt/roles/di/test_team_leader.py",
    "tests_recovery": "tests/metagpt/serialize_deserialize/test_team.py",
}


def symbols(tree):
    result = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            result.append({"name": node.name, "line": node.lineno})
            if isinstance(node, ast.ClassDef):
                for method in node.body:
                    if isinstance(method, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        result.append({"name": f"{node.name}.{method.name}", "line": method.lineno})
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    args = parser.parse_args()
    actual = subprocess.check_output(["git", "-C", str(args.source), "rev-parse", "HEAD"], text=True).strip()
    if actual != COMMIT:
        raise SystemExit(f"Wrong commit: {actual}")
    records, references = [], []
    table = ["# 固定提交源码地图", "", f"调研日期：2026-09-21。提交：`{COMMIT}`。所有锚点从本地固定源码 AST 生成。", "", "下表列出取证文件及符号导航；哈希与完整符号表见 [sources.json](sources.json)。上游测试仅阅读，未声称运行。", "", "| 引用 | 文件 | 主要符号 / 源码行 |", "| --- | --- | --- |"]
    for key, path in FILES.items():
        blob = (args.source / path).read_bytes()
        syms = symbols(ast.parse(blob.decode()))
        url = f"https://github.com/FoundationAgents/MetaGPT/blob/{COMMIT}/{path}"
        record = {"id": key, "path": path, "url": url, "sha256": hashlib.sha256(blob).hexdigest(), "lines": len(blob.splitlines()), "symbols": syms}
        records.append(record)
        # 正文一般引用完整文件；源码地图提供具体方法行号，避免用一个错误锚点覆盖同文件不同方法。
        references.append(f"[{key}]: {url}")
        selected = [s for s in syms if s["name"].split(".")[-1] in {"run", "generate_repo", "_observe", "_think", "_act", "_react", "publish_message", "publish_team_message", "serialize", "deserialize", "_run_commands", "fill", "save", "recommend_tools", "update_cost", "aask", "_write_and_exec_code"}]
        if not selected:
            selected = syms[:4]
        links = " · ".join(f"[{s['name']}]({url}#L{s['line']})" for s in selected[:10])
        table.append(f"| `{key}` | [{path}]({url}) | {links} |")
    metadata = {"repository": "https://github.com/FoundationAgents/MetaGPT.git", "research_date": "2026-09-21", "commit": COMMIT, "commit_time": "2026-01-21T18:12:32+08:00", "package_version": "1.0.0", "python_requires": ">=3.9, <3.12", "files": records}
    (ROOT / "research/sources.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n")
    (ROOT / "research/source-map.md").write_text("\n".join(table) + "\n")
    readme = ROOT / "README.md"
    text = readme.read_text().split("<!-- SOURCE REFERENCES -->")[0].rstrip()
    used = set(re.findall(r"\]\[([a-z_0-9]+)\]", text))
    missing = used - FILES.keys()
    if missing:
        raise SystemExit(f"Missing references: {missing}")
    readme.write_text(text + "\n\n<!-- SOURCE REFERENCES -->\n" + "\n".join(references) + "\n")
    print(f"Indexed {len(records)} source files; resolved {len(used)} article references.")
