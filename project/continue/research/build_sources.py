"""Collect a pinned, hashed source inventory; never copies upstream source files."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMIT = "5522c6f44ca0ac3528b37244818fbfa39b5af470"
SOURCE = Path(sys.argv[1]).resolve()
actual = subprocess.check_output(["git", "-C", str(SOURCE), "rev-parse", "HEAD"], text=True).strip()
if actual != COMMIT:
    raise SystemExit(f"Expected {COMMIT}, received {actual}")

SOURCES = [
    ("README.md", "What is Continue?", "维护状态、最终版本声明、三个客户端"),
    ("extensions/vscode/src/extension/VsCodeExtension.ts", "const inProcessMessenger", "VS Code 装配 Core 与 IDE"),
    ("binary/src/index.ts", "program.action", "JetBrains 复用 Core 的独立进程入口"),
    ("core/protocol/messenger/index.ts", "export interface Message", "消息信封与双向协议"),
    ("gui/src/redux/thunks/streamResponse.ts", "export const streamResponse", "IDE 用户输入入口"),
    ("gui/src/redux/thunks/streamNormalInput.ts", "export const streamNormalInput", "IDE 模型流、策略与工具调度"),
    ("gui/src/redux/thunks/callToolById.ts", "export const callToolById", "客户端与 Core 工具分发"),
    ("gui/src/redux/thunks/streamResponseAfterToolCall.ts", "function areAllToolsDoneStreaming", "工具批次完成后继续生成"),
    ("gui/src/redux/selectors/selectActiveTools.ts", "export const selectActiveTools", "Chat/Plan/Agent 工具暴露规则"),
    ("gui/src/redux/thunks/evaluateToolPolicies.ts", "async function evaluateToolPolicy", "IDE 动态权限收紧与编辑例外"),
    ("core/core.ts", 'on("llm/compileChat"', "Core 消息处理：编译、生成、工具、历史"),
    ("core/llm/streamChat.ts", "export async function* llmStreamChat", "Core 一次模型流服务"),
    ("extensions/cli/src/stream/streamChatResponse.ts", "export async function streamChatResponse", "CLI 独立 Agent 循环"),
    ("extensions/cli/src/stream/handleToolCalls.ts", "export async function handleToolCalls", "CLI 工具结果写回与可见工具过滤"),
    ("extensions/cli/src/stream/streamChatResponse.helpers.ts", "export async function executeStreamedToolCalls", "逐一审批、重叠执行、按索引整理结果"),
    ("core/config/ConfigHandler.ts", "export class ConfigHandler", "配置选择、缓存、重载和监听"),
    ("core/config/yaml/loadYaml.ts", "export async function configYamlToContinueConfig", "YAML 到运行时模型、规则、MCP"),
    ("core/config/yaml/models.ts", "async function modelConfigToBaseLLM", "模型角色、参数、能力映射"),
    ("gui/src/redux/util/constructMessages.ts", "export function constructMessages", "上下文装配、工具配对、规则、摘要"),
    ("core/llm/rules/getSystemMessageWithRules.ts", "export const shouldApplyRule", "Rules 应用条件与目录匹配"),
    ("core/config/markdown/loadMarkdownSkills.ts", "export async function loadMarkdownSkills", "IDE Skills 发现与校验"),
    ("core/tools/definitions/readSkill.ts", "export const readSkillTool", "技能摘要写入工具描述"),
    ("core/llm/index.ts", "async *streamChat(", "BaseLLM 模型统一层"),
    ("packages/openai-adapters/src/index.ts", "export function constructLlmApi", "跨供应商 API 适配工厂"),
    ("core/llm/countTokens.ts", "function compileChatMessages", "消息预算、最小输出预留、历史裁剪"),
    ("core/util/conversationCompaction.ts", "export async function compactConversation", "IDE 摘要生成和历史标记"),
    ("extensions/cli/src/compaction.ts", "export function shouldAutoCompact", "CLI 压缩阈值、历史裁剪"),
    ("core/config/loadContextProviders.ts", "export function loadConfigContextProviders", "默认上下文与 IDE 差异"),
    ("core/indexing/CodebaseIndexer.ts", "protected async getIndexesToBuild", "按依赖构建索引"),
    ("core/indexing/refreshIndex.ts", "getComputeDeleteAddRemove", "增量索引和分支标签"),
    ("core/context/retrieval/retrieval.ts", "const DEFAULT_N_FINAL", "检索参数的实际默认值"),
    ("core/context/retrieval/pipelines/RerankerRetrievalPipeline.ts", "export default class", "多路召回、去重与重排"),
    ("core/context/retrieval/pipelines/NoRerankerRetrievalPipeline.ts", "export default class", "无重排路径及非硬上限"),
    ("core/tools/index.ts", "export const getBaseToolDefinitions", "当前默认和实验工具集合"),
    ("core/tools/callTool.ts", "export async function callTool", "内建、HTTP 和 MCP 工具调用"),
    ("core/context/mcp/MCPConnection.ts", "async connectClient", "MCP 连接、发现、传输和超时"),
    ("core/tools/mcpToolName.ts", "export function getToolNameFromMCPServer", "MCP 名称规范化"),
    ("gui/src/util/clientTools/multiEditImpl.ts", "export const multiEditImpl", "IDE 编辑前重新读取与校验"),
    ("extensions/vscode/src/apply/ApplyManager.ts", "async applyToFile", "Apply、即时 Diff 与模型辅助合并"),
    ("core/edit/lazy/applyCodeBlock.ts", "export async function applyCodeBlock", "确定性匹配、Unified Diff 与生成式应用"),
    ("gui/src/redux/thunks/handleApplyStateUpdate.ts", "export const handleApplyStateUpdate", "Diff 审阅与 Agent 续跑"),
    ("core/edit/searchAndReplace/findSearchMatch.ts", "const matchingStrategies", "匹配策略顺序及模糊匹配边界"),
    ("core/edit/searchAndReplace/performReplace.ts", "export function executeFindAndReplace", "重复匹配拒绝、缩进修正与顺序多编辑"),
    ("core/autocomplete/CompletionProvider.ts", "public async provideInlineCompletionItems", "补全专用管道"),
    ("core/autocomplete/snippets/getAllSnippets.ts", "export const getAllSnippetsWithoutRace", "补全上下文真实启用项"),
    ("core/tools/policies/fileAccess.ts", "export function evaluateFileAccessPolicy", "工作区内外访问策略"),
    ("packages/terminal-security/src/evaluateTerminalCommandSecurity.ts", "export function evaluateTerminalCommandSecurity", "Shell 字符串与 token 安全检查"),
    ("extensions/cli/src/permissions/defaultPolicies.ts", "export function getDefaultToolPolicies", "CLI 默认、Plan、Auto 权限"),
    ("extensions/cli/src/permissions/permissionChecker.ts", "export function checkToolPermission", "首个策略命中与动态 disabled 优先"),
    ("extensions/cli/src/subagent/executor.ts", "export async function executeSubAgent", "子 Agent 的共享服务覆盖"),
    ("extensions/cli/src/tools/index.tsx", "export async function getAllAvailableTools", "CLI 工具构造与 beta 门控"),
    ("extensions/cli/src/tools/toolsConfig.ts", "let betaSubagentToolEnabled", "Subagent 默认关闭"),
    ("core/util/history.ts", "save(session: Session)", "JSON 会话与独立索引文件"),
    ("extensions/cli/src/session.ts", "export function saveSession", "CLI 会话保存、恢复、远端 stub"),
    ("extensions/cli/src/telemetry/telemetryService.ts", "private loadConfig", "显式 OTEL 配置与本地运行指标"),
    ("extensions/cli/src/tools/edit.ts", "export function validateAndResolveFilePath", "CLI 先读后改与路径解析"),
    ("extensions/cli/src/tools/multiEdit.ts", "preprocess: async", "预计算多编辑及写盘时机"),
    ("extensions/cli/src/services/ToolPermissionService.ts", "export class ToolPermissionService", "模式策略装配与切换"),
    ("extensions/cli/src/index.ts", "const program", "CLI 入口和本地命令"),
    ("extensions/cli/src/tools/skills.ts", "export const skillsTool", "CLI 技能目录与按需加载"),
    ("core/llm/toolSupport.ts", "export function modelSupportsNativeTools", "原生工具支持判断"),
    ("core/tools/systemMessageTools/interceptSystemToolCalls.ts", "export async function*", "文本工具协议拦截"),
    ("core/index.d.ts", "export interface IDE", "宿主、模型、上下文和工具类型契约"),
    ("extensions/vscode/package.json", '"version"', "扩展包内版本"),
    ("extensions/cli/package.json", '"version"', "CLI 包内开发版本"),
    (".nvmrc", "v20.20.1", "源码开发 Node 基线"),
    ("core/tools/builtIn.ts", "export enum", "内建工具 ID 与客户端工具清单"),
    ("core/util/errors.ts", "export class ContinueError", "编辑错误类别"),
    ("gui/src/redux/slices/uiSlice.ts", "export const DEFAULT_TOOL_SETTING", "IDE 默认审批策略"),
]

entries = []
for number, (path, symbol, claim) in enumerate(SOURCES, 1):
    data = (SOURCE / path).read_bytes()
    lines = data.decode().splitlines()
    matches = [n for n, line in enumerate(lines, 1) if symbol in line]
    if not matches:
        raise SystemExit(f"Missing anchor: {path}: {symbol}")
    line = matches[0]
    entries.append(dict(id=f"S{number:02}", path=path, line=line, symbol=symbol,
                        claim=claim, lines=len(lines), sha256=hashlib.sha256(data).hexdigest(),
                        url=f"https://github.com/continuedev/continue/blob/{COMMIT}/{path}#L{line}"))

report = dict(repository="https://github.com/continuedev/continue.git", commit=COMMIT,
              researched_on="2026-09-23", commit_time="2026-07-20T21:00:09-07:00",
              method="Pinned checkout; static call-chain reading and isolated source probes",
              sources=entries)
(ROOT / "research/sources.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
rows = ["# Continue 源码地图", "", f"固定提交：`{COMMIT}`。调研日期：2026-09-23。",
        "", "以下位置是阅读入口，不表示整个结论仅由该单行证明。完整文件 SHA-256 保存在 [sources.json](sources.json)。",
        "", "| 编号 | 研究内容 | 固定源码入口 |", "| --- | --- | --- |"]
for e in entries:
    rows.append(f'| {e["id"]} | {e["claim"]} | [{e["path"]}:{e["line"]}]({e["url"]}) |')
rows += ["", "## 复核路径", "", "1. 从 S02 / S03 验证宿主边界。", "2. 沿 S05 → S06 → S07 → S08 追踪 IDE；沿 S13 → S14 → S15 追踪 CLI。", "3. 用 S19 / S25 核验模型真正收到的上下文。", "4. 用 S09 / S48 / S49 核验权限，勿将模式名称当成隔离承诺。", "5. 用 S38—S43 核验编辑器修改与 Agent 恢复的连接。", "", "在线文档仅作交叉核对，发生冲突时本文以固定源码为准：", "", "- [官方入口](https://docs.continue.dev/)", "- [Agent 使用说明](https://docs.continue.dev/ide-extensions/agent/quick-start)", "- [CLI 快速开始（仍有已退役登录描述）](https://docs.continue.dev/cli/quickstart)", "- [已弃用 Codebase 文档](https://docs.continue.dev/reference/deprecated-codebase)", "- [YAML 参考](https://docs.continue.dev/reference)", ""]
(ROOT / "research/source-map.md").write_text("\n".join(rows))
print(f"Recorded {len(entries)} source files at {COMMIT}")
