"""生成固定提交源码地图、哈希与博客引用。仅依赖 Python 标准库。"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMIT = "4a56a43f39c2c75f941220989d4c65db006ee531"
BASE = f"https://github.com/cline/cline/blob/{COMMIT}/"
RECORDS = [
    ("S01", "package.json", "workspaces", "monorepo 与构建工具链"),
    ("S02", "apps/vscode/src/extension.ts", "export async function activate", "VS Code 激活"),
    ("S03", "apps/vscode/src/core/controller/index.ts", "export", "Controller 转发入口"),
    ("S04", "apps/vscode/src/sdk/vscode-session-host.ts", "static async create", "VS Code 本地后端与执行器注入"),
    ("S05", "sdk/packages/core/src/ClineCore.ts", "async start(", "Core 会话门面"),
    ("S06", "sdk/packages/core/src/runtime/host/host.ts", "export async function createRuntimeHost", "后端选择与存储降级"),
    ("S07", "sdk/packages/agents/src/agent-runtime.ts", "private async execute(", "真实 Agent 主循环"),
    ("S08", "sdk/packages/core/src/runtime/config/agent-runtime-config-builder.ts", "export function resolveToolExecution", "配置与并发模式映射"),
    ("S09", "sdk/packages/core/src/runtime/orchestration/session-runtime-orchestrator.ts", "class SessionRuntime", "工具、模型与运行上下文装配"),
    ("S10", "sdk/packages/llms/src/providers/gateway.ts", "class GatewayModelAdapter", "统一模型网关"),
    ("S11", "sdk/packages/llms/src/providers/ai-sdk.ts", "streamText", "AI SDK 与供应商流式适配"),
    ("S12", "apps/vscode/src/sdk/sdk-tool-policies.ts", "export function buildToolPolicies", "UI 工具策略及动态自动批准"),
    ("S13", "apps/vscode/src/sdk/sdk-interaction-coordinator.ts", "async handleRequestToolApproval", "人工交互 Promise"),
    ("S14", "sdk/packages/core/src/extensions/tools/presets.ts", "export const ToolPresets", "Plan / Act / YOLO 工具预设"),
    ("S15", "sdk/packages/core/src/extensions/tools/command-guard-extension.ts", "export function createPlanMode", "审批前的 Plan command guard"),
    ("S16", "apps/vscode/src/sdk/sdk-diff-edit-coordinator.ts", "export class SdkDiffEditCoordinator", "无副作用的虚拟 Diff 预览"),
    ("S17", "sdk/packages/core/src/extensions/tools/executors/editor.ts", "function resolveFilePath", "编辑器路径、唯一匹配与换行"),
    ("S18", "sdk/packages/core/src/extensions/tools/executors/apply-patch.ts", "function resolveFilePath", "Patch 解析与文件执行"),
    ("S19", "sdk/packages/core/src/extensions/tools/definitions.ts", "export function create", "内建工具、超时与反馈"),
    ("S20", "sdk/packages/core/src/extensions/tools/executors/bash.ts", "spawn", "Shell 子进程执行"),
    ("S21", "sdk/packages/core/src/extensions/mcp/tools.ts", "export async function createMcpTools", "MCP 工具到 AgentTool 的转换"),
    ("S22", "sdk/packages/core/src/extensions/config/user-instruction-config-loader.ts", "SKILL_FILE_NAME", "规则与技能的文件发现"),
    ("S23", "sdk/packages/core/src/extensions/agent-plugin/agent-skill.ts", "export function parseAgentSkillMarkdown", "Agent Plugin 技能格式验证"),
    ("S24", "sdk/packages/core/src/extensions/context/compaction.ts", "const userCompaction", "上下文压缩策略与恢复"),
    ("S25", "sdk/packages/core/src/extensions/context/compaction-shared.ts", "DEFAULT_MAX_INPUT_TOKENS", "压缩预算常量与模型限制"),
    ("S26", "sdk/packages/core/src/extensions/context/basic-compaction.ts", "export function runBasicCompaction", "确定性的基本压缩"),
    ("S27", "sdk/packages/core/src/extensions/context/agentic-compaction.ts", "export async function", "模型总结式压缩"),
    ("S28", "sdk/packages/core/src/hooks/checkpoint-hooks.ts", "export function createCheckpointHooks", "新用户轮次的 Git 检查点"),
    ("S29", "sdk/packages/core/src/session/checkpoint-restore.ts", "currentHead", "工作树恢复与 HEAD 防护"),
    ("S30", "sdk/packages/core/src/services/storage/sqlite-session-store.ts", "class SqliteSessionStore", "会话索引与工件路径"),
    ("S31", "sdk/packages/core/src/hub/server/hub-event-log.ts", "CREATE TABLE", "Hub 持久事件日志"),
    ("S32", "sdk/packages/core/src/extensions/tools/team/multi-agent.ts", "maxConcurrentRuns", "团队运行与队列"),
    ("S33", "sdk/packages/core/src/extensions/tools/team/spawn-agent-tool.ts", "export function createSpawnAgentTool", "委派工具与子 Agent 配置"),
    ("S34", "apps/vscode/src/sdk/cline-session-factory.ts", "const config: CoreSessionConfig", "VS Code 的真实会话默认值"),
    ("S35", "apps/vscode/src/sdk/webview-grpc-bridge.ts", "export class WebviewGrpcBridge", "模型事件到 Webview 状态"),
    ("S36", "sdk/packages/core/src/runtime/safety/mistake-tracker.ts", "export", "连续错误跟踪"),
    ("S37", "sdk/packages/core/src/runtime/tools/subprocess-sandbox.ts", "const child = spawn", "进程生命周期隔离的实际边界"),
    ("S38", "sdk/packages/shared/src/tools/create.ts", "export function createTool", "工具工厂与元数据"),
    ("S39", "sdk/packages/shared/src/storage/paths.ts", "export function resolveRulesConfigSearchPaths", "规则与技能目录统一解析"),
    ("S40", "sdk/packages/core/src/extensions/config/user-instruction-plugin.ts", "export function formatSkillInvocation", "技能内容的按需加载"),
    ("S41", "apps/vscode/src/sdk/vscode-runtime-builder.ts", "export async function createVscodeExtraTools", "VS Code MCP、终端与无完成工具"),
    ("S42", "apps/vscode/src/core/controller/grpc-handler.ts", "export async function", "Webview RPC 分发"),
    ("S43", "apps/vscode/src/sdk/sdk-session-config-builder.ts", "export class SdkSessionConfigBuilder", "VS Code 模式切换约束"),
    ("S44", "sdk/packages/core/src/extensions/tools/runtime.ts", "export", "工具与供应商能力路由"),
    ("S45", "sdk/packages/core/src/extensions/tools/command-guard.ts", "This is a simple blacklist", "Plan 命令过滤的已知局限"),
    ("S46", "sdk/packages/shared/src/llms/tokens.ts", "CHARS_PER_TOKEN", "字符数 token 估算"),
    ("S47", "sdk/packages/core/src/runtime/safety/loop-detection.ts", "export", "重复循环识别"),
    ("S48", "sdk/packages/agents/src/agent-runtime.test.ts", "class ScriptedModel", "上游脚本化模型测试参考"),
]


def main():
    source_root = Path(sys.argv[1]).resolve()
    def git(*args):
        return subprocess.check_output(["git", "-C", str(source_root), *args])
    assert git("rev-parse", "HEAD").decode().strip() == COMMIT, "上游提交不匹配"
    files = []
    versions = {}
    for package in ["apps/vscode", "apps/cli", "sdk/packages/sdk", "sdk/packages/core", "sdk/packages/agents"]:
        data = json.loads((source_root / package / "package.json").read_text())
        versions[data["name"]] = data["version"]
    for key, path, symbol, role in RECORDS:
        raw = (source_root / path).read_bytes()
        assert raw == git("show", f"{COMMIT}:{path}"), f"本地源码有改动: {path}"
        lines = raw.decode().splitlines()
        matches = [i for i, line in enumerate(lines, 1) if symbol in line]
        if not matches:
            raise ValueError(f"符号不存在: {key} {symbol}")
        files.append(dict(id=key, path=path, role=role, symbol=symbol, line=matches[0],
                          lines=len(lines), sha256=hashlib.sha256(raw).hexdigest(),
                          url=f"{BASE}{path}#L{matches[0]}"))
    manifest = dict(repository="https://github.com/cline/cline.git", commit=COMMIT,
                    research_date="2026-09-22", commit_date=git("show", "-s", "--format=%cI", "HEAD").decode().strip(),
                    versions=versions, files=files)
    (ROOT / "research/sources.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    rows = ["# Cline 固定提交源码地图", "", f"基线 `{COMMIT}`；调研于 2026-09-22。",
            "", "表中行号定位关键入口；每项链接打开固定提交的完整文件，不随 main 漂移。SHA-256 见 [sources.json](sources.json)。",
            "", "| 引用 | 模块及关键问题 | 文件与定位 |", "| --- | --- | --- |"]
    rows += [f"| {x['id']} | {x['role']} | [{x['path']}:{x['line']}]({x['url']}) |" for x in files]
    rows += ["", "重建：`python3 project/cline/research/build_sources.py /path/to/cline`。脚本拒绝不同提交或已改动的证据文件。", ""]
    (ROOT / "research/source-map.md").write_text("\n".join(rows))
    blog = ROOT / "README.md"
    body = blog.read_text().split("<!-- SOURCE_LINKS:")[0].rstrip()
    refs = "\n".join(f"[{x['id']}]: {x['url']}" for x in files)
    blog.write_text(body + "\n\n<!-- SOURCE_LINKS: generated by research/build_sources.py -->\n" + refs + "\n")
    print(f"Verified and linked {len(files)} upstream source files")


if __name__ == "__main__":
    main()
