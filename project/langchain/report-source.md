# LangChain v1 源码调研：内部研究底稿

> 本文件是研究过程、证据映射和边界说明，不是面向读者的最终文章。最终成文见 [`README.md`](README.md)。

## 任务定义

- 目标：从专业大模型 Agent 工程角度解释 LangChain 当前实现，并提供可运行实现，不做简单 API 罗列。
- 读者：熟悉 Python、LLM tool calling 和基本状态机概念的工程师。
- 上游仓库：`https://github.com/langchain-ai/langchain.git`。
- 源码基线：默认分支 `master`，提交 `eef3eaeac8ff2646c43b37ac2a755a5e7978e8b4`。
- 提交时间：2026-09-05T22:44:11-04:00；调研时间：2026-09-06（Asia/Shanghai）。
- 固定快照版本：`langchain==1.4.0`、`langchain-core==1.6.2`、`langchain-classic==1.0.8`。
- 证据优先级：固定提交源码 > 同期官方文档/发布页 > 仓库 README。未使用社区博客或搜索摘要支撑架构结论。

## 核心结论

LangChain v1 是一层高层 Agent 工程 API：它用 `langchain-core` 的 Runnable、message、model、tool 协议规范组件，再由 `create_agent` 把 model、tools、middleware、state/context schema 和 structured output 编译成 LangGraph `CompiledStateGraph`。模型与工具之间的循环、并行路由、interrupt/resume、checkpoint 和 store 由 LangGraph 执行。`langchain-classic` 承接旧 chains/retrievers，不应拿旧 `AgentExecutor` 解释 v1 主路径。

## 主张—证据账本

| 主张 | 一手证据 | 置信度 | 说明 |
|---|---|---:|---|
| 主包 v1.4.0 直接依赖 core 1.6+ 与 LangGraph 1.2.11+ | `libs/langchain_v1/pyproject.toml` | 高 | 固定源码 package metadata |
| v1 命名空间收敛，旧能力移至 classic | v1 release/migration 官方文档；`libs/langchain` metadata | 高 | 文章明确限定 Python v1 主路径 |
| `create_agent` 返回 `CompiledStateGraph` | `agents/factory.py` signature、docstring、compile | 高 | 不是概念推断，是函数返回类型与实现 |
| Agent 通过最新 AIMessage/tool calls 路由 | `factory.py` model-to-tools 与 tools-to-model routing | 高 | 包含 jump、structured response、return_direct |
| 多个待处理 tool calls 用 `Send` fan-out | `factory.py` `_make_model_to_tools_edge` | 高 | 具体并发度仍受图/config 执行器限制 |
| middleware 工具与普通工具进入 ToolNode，provider built-ins 只绑定模型 | `factory.py` ToolNode 构造 | 高 | 区分客户端执行和 provider 服务端执行 |
| middleware wrappers 是洋葱式，首项最外层 | `_chain_model_call_handlers` 与 async/tool variants | 高 | 顺序直接影响 retry、计费和审计语义 |
| AgentState 的 messages 使用 reducer | `middleware/types.py` AgentState | 高 | jump_to 为 ephemeral/private，structured response output-only |
| 模型 string 通过 provider registry 延迟加载 | `chat_models/base.py` | 高 | 支持 provider:model 解析与能力 profile |
| configurable_fields="any" 有密钥/base_url 风险 | `chat_models/base.py` 警告 | 高 | 已放入安全章节 |
| BaseTool 从签名生成 schema 并排除注入参数 | `core/tools/base.py` 与 `convert.py` | 高 | ToolRuntime 等不会交给模型填充 |
| Tool 执行做 Pydantic 校验、callback 和 ToolMessage 格式化 | `core/tools/base.py` | 高 | 工具自身仍需做业务授权 |
| ProviderStrategy 与 ToolStrategy 是两种不同模型协议 | `agents/structured_output.py`、factory binding | 高 | AutoStrategy 在绑定期决策 |
| 原始 JSON Schema dict 不做本地 TypeAdapter 校验 | `_parse_with_schema` | 高 | 这是源码中的显式分支 |
| checkpoint 是 thread-scoped 短期状态，store 可跨 thread | create_agent docstring + 官方 memory/runtime 文档 | 高 | 生产后端选择不在本仓库主包实现范围内 |
| streaming 是 graph execution 的多种事件投影 | 官方 streaming 文档、CompiledStateGraph 返回值 | 高 | updates/messages/custom 是常用模式 |
| MCPAdapter 在 v1.4 加入且当前为 beta | release 页面、`mcp/__init__.py`、adapter/tools | 高 | 只描述固定快照能力 |
| HostExecutionPolicy 不提供 fs/network sandbox | `_execution.py` 与 `shell_tool.py` | 高 | 安全结论直接来自源码注释/默认值 |
| 标准测试让 provider 兼容成为可执行合约 | `libs/standard-tests/README.md` 与 suites | 高 | 不等于所有 provider 功能完全一致 |

## 固定提交源码索引

基址：`https://github.com/langchain-ai/langchain/blob/eef3eaeac8ff2646c43b37ac2a755a5e7978e8b4/`

- 版本/依赖：`libs/langchain_v1/pyproject.toml`、`libs/core/pyproject.toml`、`libs/langchain/pyproject.toml`
- Agent 工厂：`libs/langchain_v1/langchain/agents/factory.py`
- Middleware 类型：`libs/langchain_v1/langchain/agents/middleware/types.py`
- HITL：`libs/langchain_v1/langchain/agents/middleware/human_in_the_loop.py`
- 执行 policy：`libs/langchain_v1/langchain/agents/middleware/_execution.py`
- Shell middleware：`libs/langchain_v1/langchain/agents/middleware/shell_tool.py`
- 结构化输出：`libs/langchain_v1/langchain/agents/structured_output.py`
- 模型工厂：`libs/langchain_v1/langchain/chat_models/base.py`
- 模型基类：`libs/core/langchain_core/language_models/chat_models.py`
- Runnable：`libs/core/langchain_core/runnables/base.py`
- Tool：`libs/core/langchain_core/tools/base.py`、`structured.py`、`convert.py`
- Messages：`libs/core/langchain_core/messages/base.py`、`ai.py`、`tool.py`
- MCP：`libs/langchain_v1/langchain/mcp/adapter.py`、`tools.py`
- 契约测试：`libs/standard-tests/README.md` 与 `libs/standard-tests/langchain_tests/`

## 官方网页来源

- 仓库：<https://github.com/langchain-ai/langchain>
- Releases：<https://github.com/langchain-ai/langchain/releases/>
- Overview：<https://docs.langchain.com/oss/python/langchain/overview>
- Agents：<https://docs.langchain.com/oss/python/langchain/agents>
- Models：<https://docs.langchain.com/oss/python/langchain/models>
- Tools：<https://docs.langchain.com/oss/python/langchain/tools>
- Middleware overview：<https://docs.langchain.com/oss/python/langchain/middleware/overview>
- Custom middleware：<https://docs.langchain.com/oss/python/langchain/middleware/custom>
- Structured output：<https://docs.langchain.com/oss/python/langchain/structured-output>
- Short-term memory：<https://docs.langchain.com/oss/python/langchain/short-term-memory>
- Long-term memory：<https://docs.langchain.com/oss/python/langchain/long-term-memory>
- Runtime：<https://docs.langchain.com/oss/python/langchain/runtime>
- Streaming：<https://docs.langchain.com/oss/python/langchain/streaming>
- Context engineering：<https://docs.langchain.com/oss/python/langchain/context-engineering>
- v1 release：<https://docs.langchain.com/oss/python/releases/langchain-v1>
- v1 migration：<https://docs.langchain.com/oss/python/migrate/langchain-v1>
- Changelog：<https://docs.langchain.com/oss/python/releases/changelog>

## 不确定性与矛盾处理

1. **master 与 release**：固定提交晚于 1.4.0 release，但 package version 仍为 1.4.0。文章称其为“master 快照与已发布版本基线”，不把 master 的每项行为承诺为稳定 API。
2. **LangChain 与 LangGraph 仓库边界**：主仓通过 PyPI 依赖 LangGraph，未 vendoring 其全部源码。关于运行时的公开语义以固定依赖约束、LangChain 调用点和官方文档交叉验证；文章不声称审计了 LangGraph 仓库所有内部实现。
3. **并行工具**：factory 用 `Send` 为 pending tool calls fan-out；实际并发受 executor、config、provider 与工具实现影响，因此表述为“可并行”，不承诺无上限并行。
4. **能力自动检测**：structured output 首选 model profile，另有模型名 fallback。文章把名称匹配描述为兼容兜底，而非可靠能力注册中心。
5. **原始 JSON Schema**：本地 `_parse_with_schema` 不验证原始 dict；供应商路径可能已经约束生成，但这不等于本地独立校验，文章保留这一区别。
6. **MCP**：release 与源码都表明该 namespace 新增且 beta；不把它写成成熟的安全边界或另一套运行时。
7. **安全沙箱**：框架提供 Docker/Codex sandbox policy，但默认 host policy 无隔离；文章不因存在可选 policy 就声称默认安全。

## 示例实现的验证边界

- 示例使用当前源码存在的公开 import：`create_agent`、middleware、`ToolStrategy`、`ToolRuntime`、LangGraph saver/store/Command。
- 工具副作用被替换为 InMemoryStore 写入，不接触真实外部系统。
- 代码通过 Python 语法编译；没有使用用户密钥调用真实 provider，因此不声称完成真实模型集成测试。
- `LANGCHAIN_MODEL` 由运行者显式提供，避免把快速变化的具体模型名写死。
- 演示的自动 approve 只能通过显式 CLI flag 开启，并在帮助与文档中标注不可用于生产。

## 停止条件与未覆盖项

已覆盖：包边界、Runnable、消息、模型、工具、Agent 构图与循环、middleware、结构化输出、状态/持久化、stream、MCP、测试、安全与生产实现。

未做：逐个 partner provider 深挖、LangGraph 独立仓库全量审计、真实 API/性能基准、LangSmith 服务端实现、所有 `langchain-classic` chain 的迁移对照。这些不改变本文关于 v1 Agent 主路径的核心结论。核心主张已有固定源码与官方材料支撑，继续扩大检索的边际收益低于成文和校验收益，因此结束调查。
