# Cline 固定提交源码地图

基线 `4a56a43f39c2c75f941220989d4c65db006ee531`；调研于 2026-09-22。

表中行号定位关键入口；每项链接打开固定提交的完整文件，不随 main 漂移。SHA-256 见 [sources.json](sources.json)。

| 引用 | 模块及关键问题 | 文件与定位 |
| --- | --- | --- |
| S01 | monorepo 与构建工具链 | [package.json:4](https://github.com/cline/cline/blob/4a56a43f39c2c75f941220989d4c65db006ee531/package.json#L4) |
| S02 | VS Code 激活 | [apps/vscode/src/extension.ts:67](https://github.com/cline/cline/blob/4a56a43f39c2c75f941220989d4c65db006ee531/apps/vscode/src/extension.ts#L67) |
| S03 | Controller 转发入口 | [apps/vscode/src/core/controller/index.ts:7](https://github.com/cline/cline/blob/4a56a43f39c2c75f941220989d4c65db006ee531/apps/vscode/src/core/controller/index.ts#L7) |
| S04 | VS Code 本地后端与执行器注入 | [apps/vscode/src/sdk/vscode-session-host.ts:115](https://github.com/cline/cline/blob/4a56a43f39c2c75f941220989d4c65db006ee531/apps/vscode/src/sdk/vscode-session-host.ts#L115) |
| S05 | Core 会话门面 | [sdk/packages/core/src/ClineCore.ts:285](https://github.com/cline/cline/blob/4a56a43f39c2c75f941220989d4c65db006ee531/sdk/packages/core/src/ClineCore.ts#L285) |
| S06 | 后端选择与存储降级 | [sdk/packages/core/src/runtime/host/host.ts:137](https://github.com/cline/cline/blob/4a56a43f39c2c75f941220989d4c65db006ee531/sdk/packages/core/src/runtime/host/host.ts#L137) |
| S07 | 真实 Agent 主循环 | [sdk/packages/agents/src/agent-runtime.ts:724](https://github.com/cline/cline/blob/4a56a43f39c2c75f941220989d4c65db006ee531/sdk/packages/agents/src/agent-runtime.ts#L724) |
| S08 | 配置与并发模式映射 | [sdk/packages/core/src/runtime/config/agent-runtime-config-builder.ts:191](https://github.com/cline/cline/blob/4a56a43f39c2c75f941220989d4c65db006ee531/sdk/packages/core/src/runtime/config/agent-runtime-config-builder.ts#L191) |
| S09 | 工具、模型与运行上下文装配 | [sdk/packages/core/src/runtime/orchestration/session-runtime-orchestrator.ts:305](https://github.com/cline/cline/blob/4a56a43f39c2c75f941220989d4c65db006ee531/sdk/packages/core/src/runtime/orchestration/session-runtime-orchestrator.ts#L305) |
| S10 | 统一模型网关 | [sdk/packages/llms/src/providers/gateway.ts:115](https://github.com/cline/cline/blob/4a56a43f39c2c75f941220989d4c65db006ee531/sdk/packages/llms/src/providers/gateway.ts#L115) |
| S11 | AI SDK 与供应商流式适配 | [sdk/packages/llms/src/providers/ai-sdk.ts:41](https://github.com/cline/cline/blob/4a56a43f39c2c75f941220989d4c65db006ee531/sdk/packages/llms/src/providers/ai-sdk.ts#L41) |
| S12 | UI 工具策略及动态自动批准 | [apps/vscode/src/sdk/sdk-tool-policies.ts:13](https://github.com/cline/cline/blob/4a56a43f39c2c75f941220989d4c65db006ee531/apps/vscode/src/sdk/sdk-tool-policies.ts#L13) |
| S13 | 人工交互 Promise | [apps/vscode/src/sdk/sdk-interaction-coordinator.ts:94](https://github.com/cline/cline/blob/4a56a43f39c2c75f941220989d4c65db006ee531/apps/vscode/src/sdk/sdk-interaction-coordinator.ts#L94) |
| S14 | Plan / Act / YOLO 工具预设 | [sdk/packages/core/src/extensions/tools/presets.ts:20](https://github.com/cline/cline/blob/4a56a43f39c2c75f941220989d4c65db006ee531/sdk/packages/core/src/extensions/tools/presets.ts#L20) |
| S15 | 审批前的 Plan command guard | [sdk/packages/core/src/extensions/tools/command-guard-extension.ts:39](https://github.com/cline/cline/blob/4a56a43f39c2c75f941220989d4c65db006ee531/sdk/packages/core/src/extensions/tools/command-guard-extension.ts#L39) |
| S16 | 无副作用的虚拟 Diff 预览 | [apps/vscode/src/sdk/sdk-diff-edit-coordinator.ts:78](https://github.com/cline/cline/blob/4a56a43f39c2c75f941220989d4c65db006ee531/apps/vscode/src/sdk/sdk-diff-edit-coordinator.ts#L78) |
| S17 | 编辑器路径、唯一匹配与换行 | [sdk/packages/core/src/extensions/tools/executors/editor.ts:42](https://github.com/cline/cline/blob/4a56a43f39c2c75f941220989d4c65db006ee531/sdk/packages/core/src/extensions/tools/executors/editor.ts#L42) |
| S18 | Patch 解析与文件执行 | [sdk/packages/core/src/extensions/tools/executors/apply-patch.ts:59](https://github.com/cline/cline/blob/4a56a43f39c2c75f941220989d4c65db006ee531/sdk/packages/core/src/extensions/tools/executors/apply-patch.ts#L59) |
| S19 | 内建工具、超时与反馈 | [sdk/packages/core/src/extensions/tools/definitions.ts:265](https://github.com/cline/cline/blob/4a56a43f39c2c75f941220989d4c65db006ee531/sdk/packages/core/src/extensions/tools/definitions.ts#L265) |
| S20 | Shell 子进程执行 | [sdk/packages/core/src/extensions/tools/executors/bash.ts:4](https://github.com/cline/cline/blob/4a56a43f39c2c75f941220989d4c65db006ee531/sdk/packages/core/src/extensions/tools/executors/bash.ts#L4) |
| S21 | MCP 工具到 AgentTool 的转换 | [sdk/packages/core/src/extensions/mcp/tools.ts:16](https://github.com/cline/cline/blob/4a56a43f39c2c75f941220989d4c65db006ee531/sdk/packages/core/src/extensions/mcp/tools.ts#L16) |
| S22 | 规则与技能的文件发现 | [sdk/packages/core/src/extensions/config/user-instruction-config-loader.ts:36](https://github.com/cline/cline/blob/4a56a43f39c2c75f941220989d4c65db006ee531/sdk/packages/core/src/extensions/config/user-instruction-config-loader.ts#L36) |
| S23 | Agent Plugin 技能格式验证 | [sdk/packages/core/src/extensions/agent-plugin/agent-skill.ts:126](https://github.com/cline/cline/blob/4a56a43f39c2c75f941220989d4c65db006ee531/sdk/packages/core/src/extensions/agent-plugin/agent-skill.ts#L126) |
| S24 | 上下文压缩策略与恢复 | [sdk/packages/core/src/extensions/context/compaction.ts:281](https://github.com/cline/cline/blob/4a56a43f39c2c75f941220989d4c65db006ee531/sdk/packages/core/src/extensions/context/compaction.ts#L281) |
| S25 | 压缩预算常量与模型限制 | [sdk/packages/core/src/extensions/context/compaction-shared.ts:13](https://github.com/cline/cline/blob/4a56a43f39c2c75f941220989d4c65db006ee531/sdk/packages/core/src/extensions/context/compaction-shared.ts#L13) |
| S26 | 确定性的基本压缩 | [sdk/packages/core/src/extensions/context/basic-compaction.ts:452](https://github.com/cline/cline/blob/4a56a43f39c2c75f941220989d4c65db006ee531/sdk/packages/core/src/extensions/context/basic-compaction.ts#L452) |
| S27 | 模型总结式压缩 | [sdk/packages/core/src/extensions/context/agentic-compaction.ts:116](https://github.com/cline/cline/blob/4a56a43f39c2c75f941220989d4c65db006ee531/sdk/packages/core/src/extensions/context/agentic-compaction.ts#L116) |
| S28 | 新用户轮次的 Git 检查点 | [sdk/packages/core/src/hooks/checkpoint-hooks.ts:497](https://github.com/cline/cline/blob/4a56a43f39c2c75f941220989d4c65db006ee531/sdk/packages/core/src/hooks/checkpoint-hooks.ts#L497) |
| S29 | 工作树恢复与 HEAD 防护 | [sdk/packages/core/src/session/checkpoint-restore.ts:409](https://github.com/cline/cline/blob/4a56a43f39c2c75f941220989d4c65db006ee531/sdk/packages/core/src/session/checkpoint-restore.ts#L409) |
| S30 | 会话索引与工件路径 | [sdk/packages/core/src/services/storage/sqlite-session-store.ts:25](https://github.com/cline/cline/blob/4a56a43f39c2c75f941220989d4c65db006ee531/sdk/packages/core/src/services/storage/sqlite-session-store.ts#L25) |
| S31 | Hub 持久事件日志 | [sdk/packages/core/src/hub/server/hub-event-log.ts:80](https://github.com/cline/cline/blob/4a56a43f39c2c75f941220989d4c65db006ee531/sdk/packages/core/src/hub/server/hub-event-log.ts#L80) |
| S32 | 团队运行与队列 | [sdk/packages/core/src/extensions/tools/team/multi-agent.ts:135](https://github.com/cline/cline/blob/4a56a43f39c2c75f941220989d4c65db006ee531/sdk/packages/core/src/extensions/tools/team/multi-agent.ts#L135) |
| S33 | 委派工具与子 Agent 配置 | [sdk/packages/core/src/extensions/tools/team/spawn-agent-tool.ts:117](https://github.com/cline/cline/blob/4a56a43f39c2c75f941220989d4c65db006ee531/sdk/packages/core/src/extensions/tools/team/spawn-agent-tool.ts#L117) |
| S34 | VS Code 的真实会话默认值 | [apps/vscode/src/sdk/cline-session-factory.ts:1070](https://github.com/cline/cline/blob/4a56a43f39c2c75f941220989d4c65db006ee531/apps/vscode/src/sdk/cline-session-factory.ts#L1070) |
| S35 | 模型事件到 Webview 状态 | [apps/vscode/src/sdk/webview-grpc-bridge.ts:33](https://github.com/cline/cline/blob/4a56a43f39c2c75f941220989d4c65db006ee531/apps/vscode/src/sdk/webview-grpc-bridge.ts#L33) |
| S36 | 连续错误跟踪 | [sdk/packages/core/src/runtime/safety/mistake-tracker.ts:33](https://github.com/cline/cline/blob/4a56a43f39c2c75f941220989d4c65db006ee531/sdk/packages/core/src/runtime/safety/mistake-tracker.ts#L33) |
| S37 | 进程生命周期隔离的实际边界 | [sdk/packages/core/src/runtime/tools/subprocess-sandbox.ts:265](https://github.com/cline/cline/blob/4a56a43f39c2c75f941220989d4c65db006ee531/sdk/packages/core/src/runtime/tools/subprocess-sandbox.ts#L265) |
| S38 | 工具工厂与元数据 | [sdk/packages/shared/src/tools/create.ts:81](https://github.com/cline/cline/blob/4a56a43f39c2c75f941220989d4c65db006ee531/sdk/packages/shared/src/tools/create.ts#L81) |
| S39 | 规则与技能目录统一解析 | [sdk/packages/shared/src/storage/paths.ts:578](https://github.com/cline/cline/blob/4a56a43f39c2c75f941220989d4c65db006ee531/sdk/packages/shared/src/storage/paths.ts#L578) |
| S40 | 技能内容的按需加载 | [sdk/packages/core/src/extensions/config/user-instruction-plugin.ts:32](https://github.com/cline/cline/blob/4a56a43f39c2c75f941220989d4c65db006ee531/sdk/packages/core/src/extensions/config/user-instruction-plugin.ts#L32) |
| S41 | VS Code MCP、终端与无完成工具 | [apps/vscode/src/sdk/vscode-runtime-builder.ts:62](https://github.com/cline/cline/blob/4a56a43f39c2c75f941220989d4c65db006ee531/apps/vscode/src/sdk/vscode-runtime-builder.ts#L62) |
| S42 | Webview RPC 分发 | [apps/vscode/src/core/controller/grpc-handler.ts:53](https://github.com/cline/cline/blob/4a56a43f39c2c75f941220989d4c65db006ee531/apps/vscode/src/core/controller/grpc-handler.ts#L53) |
| S43 | VS Code 模式切换约束 | [apps/vscode/src/sdk/sdk-session-config-builder.ts:19](https://github.com/cline/cline/blob/4a56a43f39c2c75f941220989d4c65db006ee531/apps/vscode/src/sdk/sdk-session-config-builder.ts#L19) |
| S44 | 工具与供应商能力路由 | [sdk/packages/core/src/extensions/tools/runtime.ts:12](https://github.com/cline/cline/blob/4a56a43f39c2c75f941220989d4c65db006ee531/sdk/packages/core/src/extensions/tools/runtime.ts#L12) |
| S45 | Plan 命令过滤的已知局限 | [sdk/packages/core/src/extensions/tools/command-guard.ts:10](https://github.com/cline/cline/blob/4a56a43f39c2c75f941220989d4c65db006ee531/sdk/packages/core/src/extensions/tools/command-guard.ts#L10) |
| S46 | 字符数 token 估算 | [sdk/packages/shared/src/llms/tokens.ts:8](https://github.com/cline/cline/blob/4a56a43f39c2c75f941220989d4c65db006ee531/sdk/packages/shared/src/llms/tokens.ts#L8) |
| S47 | 重复循环识别 | [sdk/packages/core/src/runtime/safety/loop-detection.ts:20](https://github.com/cline/cline/blob/4a56a43f39c2c75f941220989d4c65db006ee531/sdk/packages/core/src/runtime/safety/loop-detection.ts#L20) |
| S48 | 上游脚本化模型测试参考 | [sdk/packages/agents/src/agent-runtime.test.ts:28](https://github.com/cline/cline/blob/4a56a43f39c2c75f941220989d4c65db006ee531/sdk/packages/agents/src/agent-runtime.test.ts#L28) |

重建：`python3 project/cline/research/build_sources.py /path/to/cline`。脚本拒绝不同提交或已改动的证据文件。
