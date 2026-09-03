# OpenClaude 调研源档（内部工作文件）

> 该文件用于保存调研范围、证据卡片和 claim-to-source ledger。对外成文见 `README.md`。

## 调研目标

从专业大模型 Agent 工程视角解释 OpenClaude 的实际实现，而不是复述 README：定位入口、Agent loop、工具 runtime、权限、Provider adapter、上下文、会话、子 Agent、MCP 和构建期开关，并区分事实、仓库自述与工程判断。

## 固定快照

- Repository: `https://github.com/Gitlawb/openclaude.git`
- Branch: `main`
- Commit: `aceacf0e590a7d84447a8c44f3aa61eba781a542`
- Commit timestamp: `2026-09-02T08:15:08+08:00`
- Package/tag: `0.30.0` / `v0.30.0`
- 调研日期: `2026-09-03`

本地快照统计：1,196 commits；3,444 tracked files；`src` 下 3,189 个 TS/TSX，其中 688 个测试文件。以上数字不是长期稳定的项目指标。

## 来源卡片

### S1 — README

- URL: https://github.com/Gitlawb/openclaude/blob/aceacf0e590a7d84447a8c44f3aa61eba781a542/README.md
- 类型: 仓库一方文档
- 支持: 产品定位、安装条件、Provider 表、后台会话、配置目录、Repo Map 和开发命令入口。
- 限制: 功能/性能描述是项目自述；不能单独证明运行时实现或兼容质量。

### S2 — LICENSE/NOTICE

- URL: https://github.com/Gitlawb/openclaude/blob/aceacf0e590a7d84447a8c44f3aa61eba781a542/LICENSE
- 类型: 仓库法律声明
- 支持: 派生来源、MIT 仅覆盖修改、未获 Anthropic 授权的明确警告。
- 限制: 不是独立法律意见。

### S3 — CLI 与构建

- URLs:
  - https://github.com/Gitlawb/openclaude/blob/aceacf0e590a7d84447a8c44f3aa61eba781a542/bin/openclaude
  - https://github.com/Gitlawb/openclaude/blob/aceacf0e590a7d84447a8c44f3aa61eba781a542/src/entrypoints/cli.tsx
  - https://github.com/Gitlawb/openclaude/blob/aceacf0e590a7d84447a8c44f3aa61eba781a542/scripts/build.ts
- 支持: Node launcher、8 GB heap、动态 import 快速路径、feature flag、CLI/SDK bundles 和 stubs。

### S4 — Agent loop

- URLs:
  - https://github.com/Gitlawb/openclaude/blob/aceacf0e590a7d84447a8c44f3aa61eba781a542/src/query.ts
  - https://github.com/Gitlawb/openclaude/blob/aceacf0e590a7d84447a8c44f3aa61eba781a542/src/services/api/claude.ts
- 支持: async generator、状态变量、模型调用、流式工具、压缩、fallback、continuation、step limit、terminal semantics。

### S5 — Tool runtime 与权限

- URLs:
  - https://github.com/Gitlawb/openclaude/blob/aceacf0e590a7d84447a8c44f3aa61eba781a542/src/Tool.ts
  - https://github.com/Gitlawb/openclaude/blob/aceacf0e590a7d84447a8c44f3aa61eba781a542/src/tools.ts
  - https://github.com/Gitlawb/openclaude/blob/aceacf0e590a7d84447a8c44f3aa61eba781a542/src/services/tools/toolExecution.ts
  - https://github.com/Gitlawb/openclaude/blob/aceacf0e590a7d84447a8c44f3aa61eba781a542/src/services/tools/StreamingToolExecutor.ts
  - https://github.com/Gitlawb/openclaude/blob/aceacf0e590a7d84447a8c44f3aa61eba781a542/src/utils/permissions/permissions.ts
- 支持: Tool contract、工具池、校验/hooks/权限/执行管线、并发纪律、权限 mode 和默认值风险。

### S6 — Provider 系统

- URLs:
  - https://github.com/Gitlawb/openclaude/blob/aceacf0e590a7d84447a8c44f3aa61eba781a542/src/integrations/descriptors.ts
  - https://github.com/Gitlawb/openclaude/blob/aceacf0e590a7d84447a8c44f3aa61eba781a542/docs/architecture/integrations.md
  - https://github.com/Gitlawb/openclaude/blob/aceacf0e590a7d84447a8c44f3aa61eba781a542/src/services/api/client.ts
  - https://github.com/Gitlawb/openclaude/blob/aceacf0e590a7d84447a8c44f3aa61eba781a542/src/services/api/openaiShim.ts
- 支持: descriptor-first、transport kinds、client routing、OpenAI shim、原生云 SDK、凭证 header 清理和已知例外。

### S7 — Prompt、上下文与 Repo Map

- URLs:
  - https://github.com/Gitlawb/openclaude/blob/aceacf0e590a7d84447a8c44f3aa61eba781a542/src/constants/prompts.ts
  - https://github.com/Gitlawb/openclaude/blob/aceacf0e590a7d84447a8c44f3aa61eba781a542/src/utils/systemPrompt.ts
  - https://github.com/Gitlawb/openclaude/blob/aceacf0e590a7d84447a8c44f3aa61eba781a542/src/context.ts
  - https://github.com/Gitlawb/openclaude/blob/aceacf0e590a7d84447a8c44f3aa61eba781a542/docs/repo-map.md
- 支持: system prompt 分层、上下文来源、Repo Map 算法和 gate。
- 限制: Repo Map 性能数字只按仓库文档归因，未独立 benchmark。

### S8 — 会话、子 Agent、MCP

- URLs:
  - https://github.com/Gitlawb/openclaude/blob/aceacf0e590a7d84447a8c44f3aa61eba781a542/src/utils/sessionStorage.ts
  - https://github.com/Gitlawb/openclaude/blob/aceacf0e590a7d84447a8c44f3aa61eba781a542/src/tools/AgentTool/runAgent.ts
  - https://github.com/Gitlawb/openclaude/blob/aceacf0e590a7d84447a8c44f3aa61eba781a542/src/tools/MCPTool/MCPTool.ts
  - https://github.com/Gitlawb/openclaude/blob/aceacf0e590a7d84447a8c44f3aa61eba781a542/src/services/mcp/client.ts
- 支持: append-only transcript、parentUuid/DAG 恢复、sidechain、Agent 上下文派生、MCP schema/annotations/call。

## Claim-to-source ledger

| 关键结论 | 证据 | 置信度/限定 |
| --- | --- | --- |
| Agent 内核是 `query()` 异步生成器状态机 | S4 | 高，直接源码 |
| 内部 canonical protocol 偏 Anthropic Messages | S4 + S6 | 高；“canonical”是对类型与 shim 边界的架构归纳 |
| 非 Anthropic Provider 主要在 shim 边界适配 | S6 | 高；Bedrock/Vertex/Foundry 是专用路径 |
| 工具执行包含 schema → hooks → permission → call → post hooks | S5 | 高，直接源码 |
| 并发安全工具并行，危险/非安全工具独占且结果保序 | S5 | 高，直接源码 |
| Prompt 在请求前经历多级压缩与 hard cap | S4 + S7 | 高，直接源码 |
| Transcript 是 append-only JSONL + parentUuid chain | S8 | 高，直接源码 |
| 子 Agent 复用同一个 `query()` | S8 | 高，直接源码 |
| Repo Map 使用 tree-sitter + IDF graph + PageRank | S7 | 中高，仓库设计文档；未做性能复测 |
| open build 中多项源码能力被关闭或 stub | S3 | 高，构建脚本 |
| 许可证不能简单视为全仓 MIT | S2 | 高，仓库明确声明；具体法律结论需法务 |
| MCP readOnlyHint 构成需要额外信任治理的边界 | S5 + S8 | 中高，事实来自源码，风险评级为工程判断 |
| 巨型模块提高维护复杂度 | 本地行数 + S4/S8 | 中高，行数客观；影响是工程判断 |

## 未验证与排除项

- 未逐一对每个远端 Provider 发真实 API 请求，不声称所有模型都可用。
- 未独立复测 Repo Map 的 20–30 秒冷启动和低于 100 ms 缓存数据。
- 未对许可证作司法辖区级法律分析。
- 未把 feature-gated、internal 或 stubbed 代码当作默认可用能力。
- 未修改上游仓库源码；交付物只有研究博客与原创 SVG 图。
