# Continue 源码地图

固定提交：`5522c6f44ca0ac3528b37244818fbfa39b5af470`。调研日期：2026-09-23。

以下位置是阅读入口，不表示整个结论仅由该单行证明。完整文件 SHA-256 保存在 [sources.json](sources.json)。

| 编号 | 研究内容 | 固定源码入口 |
| --- | --- | --- |
| S01 | 维护状态、最终版本声明、三个客户端 | [README.md:17](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/README.md#L17) |
| S02 | VS Code 装配 Core 与 IDE | [extensions/vscode/src/extension/VsCodeExtension.ts:265](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/extensions/vscode/src/extension/VsCodeExtension.ts#L265) |
| S03 | JetBrains 复用 Core 的独立进程入口 | [binary/src/index.ts:19](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/binary/src/index.ts#L19) |
| S04 | 消息信封与双向协议 | [core/protocol/messenger/index.ts:6](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/core/protocol/messenger/index.ts#L6) |
| S05 | IDE 用户输入入口 | [gui/src/redux/thunks/streamResponse.ts:18](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/gui/src/redux/thunks/streamResponse.ts#L18) |
| S06 | IDE 模型流、策略与工具调度 | [gui/src/redux/thunks/streamNormalInput.ts:72](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/gui/src/redux/thunks/streamNormalInput.ts#L72) |
| S07 | 客户端与 Core 工具分发 | [gui/src/redux/thunks/callToolById.ts:19](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/gui/src/redux/thunks/callToolById.ts#L19) |
| S08 | 工具批次完成后继续生成 | [gui/src/redux/thunks/streamResponseAfterToolCall.ts:17](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/gui/src/redux/thunks/streamResponseAfterToolCall.ts#L17) |
| S09 | Chat/Plan/Agent 工具暴露规则 | [gui/src/redux/selectors/selectActiveTools.ts:7](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/gui/src/redux/selectors/selectActiveTools.ts#L7) |
| S10 | IDE 动态权限收紧与编辑例外 | [gui/src/redux/thunks/evaluateToolPolicies.ts:19](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/gui/src/redux/thunks/evaluateToolPolicies.ts#L19) |
| S11 | Core 消息处理：编译、生成、工具、历史 | [core/core.ts:591](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/core/core.ts#L591) |
| S12 | Core 一次模型流服务 | [core/llm/streamChat.ts:9](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/core/llm/streamChat.ts#L9) |
| S13 | CLI 独立 Agent 循环 | [extensions/cli/src/stream/streamChatResponse.ts:423](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/extensions/cli/src/stream/streamChatResponse.ts#L423) |
| S14 | CLI 工具结果写回与可见工具过滤 | [extensions/cli/src/stream/handleToolCalls.ts:36](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/extensions/cli/src/stream/handleToolCalls.ts#L36) |
| S15 | 逐一审批、重叠执行、按索引整理结果 | [extensions/cli/src/stream/streamChatResponse.helpers.ts:469](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/extensions/cli/src/stream/streamChatResponse.helpers.ts#L469) |
| S16 | 配置选择、缓存、重载和监听 | [core/config/ConfigHandler.ts:31](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/core/config/ConfigHandler.ts#L31) |
| S17 | YAML 到运行时模型、规则、MCP | [core/config/yaml/loadYaml.ts:156](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/core/config/yaml/loadYaml.ts#L156) |
| S18 | 模型角色、参数、能力映射 | [core/config/yaml/models.ts:50](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/core/config/yaml/models.ts#L50) |
| S19 | 上下文装配、工具配对、规则、摘要 | [gui/src/redux/util/constructMessages.ts:37](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/gui/src/redux/util/constructMessages.ts#L37) |
| S20 | Rules 应用条件与目录匹配 | [core/llm/rules/getSystemMessageWithRules.ts:205](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/core/llm/rules/getSystemMessageWithRules.ts#L205) |
| S21 | IDE Skills 发现与校验 | [core/config/markdown/loadMarkdownSkills.ts:45](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/core/config/markdown/loadMarkdownSkills.ts#L45) |
| S22 | 技能摘要写入工具描述 | [core/tools/definitions/readSkill.ts:5](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/core/tools/definitions/readSkill.ts#L5) |
| S23 | BaseLLM 模型统一层 | [core/llm/index.ts:1095](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/core/llm/index.ts#L1095) |
| S24 | 跨供应商 API 适配工厂 | [packages/openai-adapters/src/index.ts:84](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/packages/openai-adapters/src/index.ts#L84) |
| S25 | 消息预算、最小输出预留、历史裁剪 | [core/llm/countTokens.ts:422](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/core/llm/countTokens.ts#L422) |
| S26 | IDE 摘要生成和历史标记 | [core/util/conversationCompaction.ts:19](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/core/util/conversationCompaction.ts#L19) |
| S27 | CLI 压缩阈值、历史裁剪 | [extensions/cli/src/compaction.ts:266](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/extensions/cli/src/compaction.ts#L266) |
| S28 | 默认上下文与 IDE 差异 | [core/config/loadContextProviders.ts:22](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/core/config/loadContextProviders.ts#L22) |
| S29 | 按依赖构建索引 | [core/indexing/CodebaseIndexer.ts:146](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/core/indexing/CodebaseIndexer.ts#L146) |
| S30 | 增量索引和分支标签 | [core/indexing/refreshIndex.ts:395](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/core/indexing/refreshIndex.ts#L395) |
| S31 | 检索参数的实际默认值 | [core/context/retrieval/retrieval.ts:9](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/core/context/retrieval/retrieval.ts#L9) |
| S32 | 多路召回、去重与重排 | [core/context/retrieval/pipelines/RerankerRetrievalPipeline.ts:12](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/core/context/retrieval/pipelines/RerankerRetrievalPipeline.ts#L12) |
| S33 | 无重排路径及非硬上限 | [core/context/retrieval/pipelines/NoRerankerRetrievalPipeline.ts:11](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/core/context/retrieval/pipelines/NoRerankerRetrievalPipeline.ts#L11) |
| S34 | 当前默认和实验工具集合 | [core/tools/index.ts:6](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/core/tools/index.ts#L6) |
| S35 | 内建、HTTP 和 MCP 工具调用 | [core/tools/callTool.ts:235](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/core/tools/callTool.ts#L235) |
| S36 | MCP 连接、发现、传输和超时 | [core/context/mcp/MCPConnection.ts:122](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/core/context/mcp/MCPConnection.ts#L122) |
| S37 | MCP 名称规范化 | [core/tools/mcpToolName.ts:6](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/core/tools/mcpToolName.ts#L6) |
| S38 | IDE 编辑前重新读取与校验 | [gui/src/util/clientTools/multiEditImpl.ts:8](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/gui/src/util/clientTools/multiEditImpl.ts#L8) |
| S39 | Apply、即时 Diff 与模型辅助合并 | [extensions/vscode/src/apply/ApplyManager.ts:28](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/extensions/vscode/src/apply/ApplyManager.ts#L28) |
| S40 | 确定性匹配、Unified Diff 与生成式应用 | [core/edit/lazy/applyCodeBlock.ts:14](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/core/edit/lazy/applyCodeBlock.ts#L14) |
| S41 | Diff 审阅与 Agent 续跑 | [gui/src/redux/thunks/handleApplyStateUpdate.ts:21](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/gui/src/redux/thunks/handleApplyStateUpdate.ts#L21) |
| S42 | 匹配策略顺序及模糊匹配边界 | [core/edit/searchAndReplace/findSearchMatch.ts:303](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/core/edit/searchAndReplace/findSearchMatch.ts#L303) |
| S43 | 重复匹配拒绝、缩进修正与顺序多编辑 | [core/edit/searchAndReplace/performReplace.ts:85](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/core/edit/searchAndReplace/performReplace.ts#L85) |
| S44 | 补全专用管道 | [core/autocomplete/CompletionProvider.ts:150](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/core/autocomplete/CompletionProvider.ts#L150) |
| S45 | 补全上下文真实启用项 | [core/autocomplete/snippets/getAllSnippets.ts:220](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/core/autocomplete/snippets/getAllSnippets.ts#L220) |
| S46 | 工作区内外访问策略 | [core/tools/policies/fileAccess.ts:10](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/core/tools/policies/fileAccess.ts#L10) |
| S47 | Shell 字符串与 token 安全检查 | [packages/terminal-security/src/evaluateTerminalCommandSecurity.ts:32](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/packages/terminal-security/src/evaluateTerminalCommandSecurity.ts#L32) |
| S48 | CLI 默认、Plan、Auto 权限 | [extensions/cli/src/permissions/defaultPolicies.ts:7](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/extensions/cli/src/permissions/defaultPolicies.ts#L7) |
| S49 | 首个策略命中与动态 disabled 优先 | [extensions/cli/src/permissions/permissionChecker.ts:128](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/extensions/cli/src/permissions/permissionChecker.ts#L128) |
| S50 | 子 Agent 的共享服务覆盖 | [extensions/cli/src/subagent/executor.ts:58](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/extensions/cli/src/subagent/executor.ts#L58) |
| S51 | CLI 工具构造与 beta 门控 | [extensions/cli/src/tools/index.tsx:79](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/extensions/cli/src/tools/index.tsx#L79) |
| S52 | Subagent 默认关闭 | [extensions/cli/src/tools/toolsConfig.ts:7](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/extensions/cli/src/tools/toolsConfig.ts#L7) |
| S53 | JSON 会话与独立索引文件 | [core/util/history.ts:111](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/core/util/history.ts#L111) |
| S54 | CLI 会话保存、恢复、远端 stub | [extensions/cli/src/session.ts:279](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/extensions/cli/src/session.ts#L279) |
| S55 | 显式 OTEL 配置与本地运行指标 | [extensions/cli/src/telemetry/telemetryService.ts:68](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/extensions/cli/src/telemetry/telemetryService.ts#L68) |
| S56 | CLI 先读后改与路径解析 | [extensions/cli/src/tools/edit.ts:20](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/extensions/cli/src/tools/edit.ts#L20) |
| S57 | 预计算多编辑及写盘时机 | [extensions/cli/src/tools/multiEdit.ts:105](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/extensions/cli/src/tools/multiEdit.ts#L105) |
| S58 | 模式策略装配与切换 | [extensions/cli/src/services/ToolPermissionService.ts:43](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/extensions/cli/src/services/ToolPermissionService.ts#L43) |
| S59 | CLI 入口和本地命令 | [extensions/cli/src/index.ts:171](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/extensions/cli/src/index.ts#L171) |
| S60 | CLI 技能目录与按需加载 | [extensions/cli/src/tools/skills.ts:29](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/extensions/cli/src/tools/skills.ts#L29) |
| S61 | 原生工具支持判断 | [core/llm/toolSupport.ts:513](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/core/llm/toolSupport.ts#L513) |
| S62 | 文本工具协议拦截 | [core/tools/systemMessageTools/interceptSystemToolCalls.ts:24](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/core/tools/systemMessageTools/interceptSystemToolCalls.ts#L24) |
| S63 | 宿主、模型、上下文和工具类型契约 | [core/index.d.ts:831](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/core/index.d.ts#L831) |
| S64 | 扩展包内版本 | [extensions/vscode/package.json:5](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/extensions/vscode/package.json#L5) |
| S65 | CLI 包内开发版本 | [extensions/cli/package.json:3](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/extensions/cli/package.json#L3) |
| S66 | 源码开发 Node 基线 | [.nvmrc:1](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/.nvmrc#L1) |
| S67 | 内建工具 ID 与客户端工具清单 | [core/tools/builtIn.ts:1](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/core/tools/builtIn.ts#L1) |
| S68 | 编辑错误类别 | [core/util/errors.ts:14](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/core/util/errors.ts#L14) |
| S69 | IDE 默认审批策略 | [gui/src/redux/slices/uiSlice.ts:34](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/gui/src/redux/slices/uiSlice.ts#L34) |

## 复核路径

1. 从 S02 / S03 验证宿主边界。
2. 沿 S05 → S06 → S07 → S08 追踪 IDE；沿 S13 → S14 → S15 追踪 CLI。
3. 用 S19 / S25 核验模型真正收到的上下文。
4. 用 S09 / S48 / S49 核验权限，勿将模式名称当成隔离承诺。
5. 用 S38—S43 核验编辑器修改与 Agent 恢复的连接。

在线文档仅作交叉核对，发生冲突时本文以固定源码为准：

- [官方入口](https://docs.continue.dev/)
- [Agent 使用说明](https://docs.continue.dev/ide-extensions/agent/quick-start)
- [CLI 快速开始（仍有已退役登录描述）](https://docs.continue.dev/cli/quickstart)
- [已弃用 Codebase 文档](https://docs.continue.dev/reference/deprecated-codebase)
- [YAML 参考](https://docs.continue.dev/reference)
