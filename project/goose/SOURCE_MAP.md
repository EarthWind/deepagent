# Goose 源码导航与证据索引

所有链接固定到 `1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1`。表中的“关注点”是阅读入口，不代表我们执行过对应测试。

建议按下列顺序追踪一次请求：

1. Desktop `prompt.ts` 与 `settings.ts` → ACP `server.rs`：先确认循环选择。
2. `Agent::reply` → 传统 loop 或 `create_state_machine`：确认执行语义。
3. Provider → Tool Inspection → ExtensionManager：确认能力与权限路径。
4. Context management → SessionManager：确认模型看到什么、磁盘记录什么。
5. Summon / Code Mode：重新检查间接调用的权限和取消边界。

| ID | 源码文件 / 目录 | 阅读关注点 |
| --- | --- | --- |
| `repo` | [README.md](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/README.md) | 项目定位与治理信息 |
| `commit` | [固定 commit 根目录](https://github.com/aaif-goose/goose/tree/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1) | 固定提交快照 |
| `workspace` | [Cargo.toml:9](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/Cargo.toml#L9) | workspace 版本、MSRV 与依赖 |
| `license` | [LICENSE](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/LICENSE) | Apache-2.0 许可 |
| `sm-mod` | [crates/goose/src/agents/state_machine/mod.rs:72](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/agents/state_machine/mod.rs#L72) | 环境开关的真值与默认值 |
| `acp-server` | [crates/goose/src/acp/server.rs:421](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/acp/server.rs#L421) | ACP metadata 覆盖环境默认值 |
| `upstream-agents` | [AGENTS.md:39](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/AGENTS.md#L39) | 双路径迁移与公共 API 边界 |
| `sdk` | [crates/goose-sdk/README.md](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose-sdk/README.md) | GDK 绑定范围与可观测接口 |
| `machine` | [crates/goose-agent/src/machine.rs:48](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose-agent/src/machine.rs#L48) | 通用状态机、step/apply/run |
| `agent-assembly` | [crates/goose/src/agents/agent.rs:1643](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/agents/agent.rs#L1643) | Goose 操作顺序与条件性安装 |
| `desktop-serve` | [ui/desktop/src/gooseServe.ts:364](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/ui/desktop/src/gooseServe.ts#L364) | Desktop 启动 goose serve |
| `desktop-acp` | [ui/desktop/src/acp/acpConnection.ts:131](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/ui/desktop/src/acp/acpConnection.ts#L131) | WebSocket ACP 初始化和连接管理 |
| `desktop-chat` | [ui/desktop/src/hooks/useChatSession.ts:57](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/ui/desktop/src/hooks/useChatSession.ts#L57) | 会话 UI 与 controller/store |
| `desktop-settings` | [ui/desktop/src/utils/settings.ts:100](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/ui/desktop/src/utils/settings.ts#L100) | Desktop 默认使用新循环 |
| `desktop-prompt` | [ui/desktop/src/acp/prompt.ts:6](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/ui/desktop/src/acp/prompt.ts#L6) | 每次请求发送 unrolledAgentLoop |
| `acp-provider` | [crates/goose/src/acp/provider.rs](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/acp/provider.rs) | 外部 Agent 的 ACP Provider 适配 |
| `agent` | [crates/goose/src/agents/agent.rs:212](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/agents/agent.rs#L212) | Agent 依赖和配置 |
| `agent-reply` | [crates/goose/src/agents/agent.rs:2044](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/agents/agent.rs#L2044) | 公共回复入口与消息 ID |
| `agent-loop` | [crates/goose/src/agents/agent.rs:2416](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/agents/agent.rs#L2416) | 传统 loop 实现入口 |
| `tool-execution` | [crates/goose/src/agents/tool_execution.rs:37](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/agents/tool_execution.rs#L37) | session/cwd/request ID 与工具流 |
| `agent-tools` | [crates/goose/src/agents/agent.rs:2838](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/agents/agent.rs#L2838) | 传统工具检查、执行与结果配对 |
| `sm-tools` | [crates/goose/src/agents/state_machine/ops_toolcalling.rs:315](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/agents/state_machine/ops_toolcalling.rs#L315) | 状态机工具执行与并发流 |
| `agent-persist` | [crates/goose/src/agents/agent.rs:3500](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/agents/agent.rs#L3500) | 传统循环积累消息后的持久化点 |
| `operation` | [crates/goose-agent/src/operation.rs](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose-agent/src/operation.rs) | Operation/Inference/Effect 协议 |
| `sm-session` | [crates/goose/src/agents/state_machine/session.rs:39](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/agents/state_machine/session.rs#L39) | 效果写入 SessionManager |
| `sm-approval` | [crates/goose/src/agents/state_machine/ops_tool_approval.rs](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/agents/state_machine/ops_tool_approval.rs) | 工具审批操作 |
| `sm-tests` | [crates/goose/src/agents/state_machine/tests](https://github.com/aaif-goose/goose/tree/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/agents/state_machine/tests) | 状态机生命周期测试目录 |
| `provider` | [crates/goose-provider-types/src/base.rs:464](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose-provider-types/src/base.rs#L464) | 统一推理与能力契约 |
| `provider-capabilities` | [crates/goose-provider-types/src/base.rs:631](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose-provider-types/src/base.rs#L631) | 自管上下文和权限路由 |
| `reply-parts` | [crates/goose/src/agents/reply_parts.rs:244](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/agents/reply_parts.rs#L244) | 工具披露与推理请求准备 |
| `providers-tree` | [crates/goose-providers/src](https://github.com/aaif-goose/goose/tree/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose-providers/src) | 模型适配与格式转换目录 |
| `extension` | [crates/goose/src/agents/extension.rs:156](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/agents/extension.rs#L156) | 扩展类型、配置和 available_tools |
| `builtin-connect` | [crates/goose/src/agents/extension_manager/builtin.rs:10](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/agents/extension_manager/builtin.rs#L10) | 内存 duplex 与容器分支 |
| `platform-registry` | [crates/goose/src/agents/platform_extensions/mod.rs](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/agents/platform_extensions/mod.rs) | platform 注册和 unprefixed_tools |
| `extension-manager` | [crates/goose/src/agents/extension_manager/mod.rs:750](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/agents/extension_manager/mod.rs#L750) | 工具缓存与版本更新 |
| `extension-dispatch` | [crates/goose/src/agents/extension_manager/mod.rs:1270](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/agents/extension_manager/mod.rs#L1270) | 最终扩展路由与工具可用性约束 |
| `developer` | [crates/goose/src/agents/platform_extensions/developer/mod.rs](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/agents/platform_extensions/developer/mod.rs) | 当前五个 Developer 工具 |
| `code-mode` | [crates/goose/src/agents/platform_extensions/code_execution.rs:33](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/agents/platform_extensions/code_execution.rs#L33) | pctx registry 与 Deno 运行时 |
| `code-disclosure` | [crates/goose/src/agents/platform_extensions/code_execution.rs:454](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/agents/platform_extensions/code_execution.rs#L454) | Catalog/Filesystem/Sidecar 三种模式 |
| `code-callback` | [crates/goose/src/agents/platform_extensions/code_execution.rs:359](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/agents/platform_extensions/code_execution.rs#L359) | 内部 callback 直接进入 manager |
| `prompt-manager` | [crates/goose/src/agents/prompt_manager.rs:108](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/agents/prompt_manager.rs#L108) | 排序、模板、额外指令与固定时间 |
| `hints` | [crates/goose/src/hints/load_hints.rs](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/hints/load_hints.rs) | 项目与子目录提示词加载 |
| `skills` | [crates/goose/src/skills/mod.rs](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/skills/mod.rs) | SKILL.md 发现、路径和 supporting files |
| `skills-client` | [crates/goose/src/skills/client.rs:71](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/skills/client.rs#L71) | load_skill 按需加载接口 |
| `context` | [crates/goose/src/context_mgmt/mod.rs:70](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/context_mgmt/mod.rs#L70) | 摘要与可见性投影 |
| `context-default` | [crates/goose-context-management/src/lib.rs:32](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose-context-management/src/lib.rs#L32) | 默认阈值 0.8 |
| `context-check` | [crates/goose/src/context_mgmt/mod.rs:225](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/context_mgmt/mod.rs#L225) | 使用率触发与关闭条件 |
| `agent-recovery` | [crates/goose/src/agents/agent.rs:3124](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/agents/agent.rs#L3124) | 传统上下文超限恢复 |
| `context-tool-pairs` | [crates/goose/src/context_mgmt/mod.rs:27](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/context_mgmt/mod.rs#L27) | 默认关闭、cutoff 和批处理 |
| `large-response` | [crates/goose/src/agents/large_response_handler.rs:5](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/agents/large_response_handler.rs#L5) | 200000 字符外置与失败回退 |
| `memory` | [crates/goose-mcp/src/memory/mod.rs](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose-mcp/src/memory/mod.rs) | 全局和局部分类 Memory MCP |
| `chatrecall` | [crates/goose/src/agents/platform_extensions/chatrecall.rs](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/agents/platform_extensions/chatrecall.rs) | 历史检索与片段 |
| `todo` | [crates/goose/src/agents/platform_extensions/todo.rs](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/agents/platform_extensions/todo.rs) | session extension data 中的工作计划 |
| `sessions` | [crates/goose/src/session/session_manager.rs:938](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/session/session_manager.rs#L938) | WAL、busy timeout、schema 与迁移 |
| `session-append` | [crates/goose/src/session/session_manager.rs:1919](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/session/session_manager.rs#L1919) | 事务追加与时间顺序修正 |
| `session-replace` | [crates/goose/src/session/session_manager.rs:1964](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/session/session_manager.rs#L1964) | 事务替换会话消息 |
| `mode` | [crates/goose-provider-types/src/goose_mode.rs:22](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose-provider-types/src/goose_mode.rs#L22) | 四种模式及 Auto 默认值 |
| `permission` | [crates/goose/src/permission/permission_inspector.rs:159](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/permission/permission_inspector.rs#L159) | Auto/Approve/SmartApprove 的真实分支 |
| `agent-inspectors` | [crates/goose/src/agents/agent.rs:768](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/agents/agent.rs#L768) | 检查器注册顺序 |
| `inspection` | [crates/goose/src/tool_inspection.rs:75](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/tool_inspection.rs#L75) | 检查器启用、失败处理与结果合并 |
| `security-config` | [crates/goose/src/security/mod.rs:58](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/security/mod.rs#L58) | SECURITY_PROMPT_ENABLED 默认关闭 |
| `egress` | [crates/goose/src/security/egress_inspector.rs](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/security/egress_inspector.rs) | 出站目的地提取和日志 |
| `adversary` | [crates/goose/src/security/adversary_inspector.rs](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/security/adversary_inspector.rs) | 配置驱动的模型审查 |
| `hooks` | [crates/goose/src/hooks/mod.rs:55](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/hooks/mod.rs#L55) | 生命周期事件和失败策略 |
| `cli` | [crates/goose-cli/src/cli.rs:134](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose-cli/src/cli.rs#L134) | container 范围、各入口命令 |
| `summon` | [crates/goose/src/agents/platform_extensions/summon.rs:724](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/agents/platform_extensions/summon.rs#L724) | load/delegate 接口 |
| `summon-defaults` | [crates/goose/src/agents/platform_extensions/summon.rs:559](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/agents/platform_extensions/summon.rs#L559) | 5 个后台任务、600 秒 TTL |
| `subagent` | [crates/goose/src/agents/subagent_handler.rs:120](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/agents/subagent_handler.rs#L120) | 新 Agent 和独立对话的启动 |
| `summon-task-config` | [crates/goose/src/agents/platform_extensions/summon.rs:1652](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/agents/platform_extensions/summon.rs#L1652) | 扩展、Provider、轮数和目录配置 |
| `summon-working-dir` | [crates/goose/src/agents/platform_extensions/summon.rs:2309](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/agents/platform_extensions/summon.rs#L2309) | canonicalize 和父路径检查 |
| `summon-auto` | [crates/goose/src/agents/platform_extensions/summon.rs:1393](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/agents/platform_extensions/summon.rs#L1393) | 子 Agent 固定 Auto 的原因与代码 |
| `subagent-config` | [crates/goose/src/agents/subagent_task_config.rs:9](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/agents/subagent_task_config.rs#L9) | 子任务默认 25 轮 |
| `recipe` | [crates/goose/src/recipe/mod.rs:43](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/recipe/mod.rs#L43) | Recipe 字段与设置 |
| `recipe-template` | [crates/goose/src/recipe/template_recipe.rs](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/recipe/template_recipe.rs) | 参数模板加载与渲染 |
| `final-output` | [crates/goose/src/agents/final_output_tool.rs:24](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/agents/final_output_tool.rs#L24) | JSON schema 验证与修正闭环 |
| `scheduler` | [crates/goose/src/scheduler_trait.rs:9](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/scheduler_trait.rs#L9) | 定时 Recipe 生命周期接口 |
| `telemetry` | [crates/goose/src/agents/gen_ai_telemetry.rs](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/agents/gen_ai_telemetry.rs) | Agent 遥测与内容采集 |
| `tests-tree` | [crates/goose/tests](https://github.com/aaif-goose/goose/tree/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/tests) | 上游集成和权限等测试目录 |
| `moim` | [crates/goose/src/agents/moim.rs](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/agents/moim.rs) | 动态 turn context 与 system 说明 |
| `recipe-validation` | [crates/goose/src/recipe/validate_recipe.rs](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/recipe/validate_recipe.rs) | 上游 Recipe 校验 |
| `recipe-adapter` | [crates/goose/src/recipe/recipe_extension_adapter.rs](https://github.com/aaif-goose/goose/blob/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1/crates/goose/src/recipe/recipe_extension_adapter.rs) | Recipe extension 字段反序列化 |

## 可机器复核的索引

`sources.json` 保存路径、行号和锚点原文；`research.json` 保存版本基线。已有源码 checkout 时运行：

```bash
python3 project/goose/scripts/check_artifacts.py --source-root /path/to/goose
```

检查程序会要求 checkout 的 HEAD 与调研 commit 一致，并验证路径、锚点行和文档引用。它不联网，也不执行 Goose 工具。

## 在线官方资料

在线页面可能更新，和固定提交不同步时以正文注明的源码分支为准。

- [项目主页](https://goose-docs.ai/)
- [架构说明](https://goose-docs.ai/docs/goose-architecture/)
- [上下文管理](https://goose-docs.ai/docs/guides/sessions/smart-context-management/)
- [权限模式](https://goose-docs.ai/docs/guides/managing-tools/goose-permissions/)
- [工具权限](https://goose-docs.ai/docs/guides/managing-tools/tool-permissions/)
- [Code Mode](https://goose-docs.ai/docs/guides/managing-tools/code-mode/)
- [Recipe Reference](https://goose-docs.ai/docs/guides/recipes/recipe-reference/)
- [Subrecipes](https://goose-docs.ai/docs/guides/recipes/subrecipes/)
- [Custom Agents](https://goose-docs.ai/docs/guides/context-engineering/custom-agents/)
