# DeepSeek Harness 调研底稿（内部）

> 调研日期：2026-09-07（Asia/Shanghai）<br>
> 上游仓库：`deepseek-ai/deepseek-harness`<br>
> 固定基线：`b0a7d2ce3b4c19d7452e364b2d7acbfa87e707ed`（`0.1.3-alpha.2`）

## 问题与结论

1. **它的核心是什么？** 不是一个写死的 ReAct 循环，而是 Cordis 承载的插件运行时；LLM、工具、会话、循环、沙箱、UI 都是可替换插件。
2. **请求如何运行？** `dsh` 解析 profile 与 patch，Loader 激活依赖图；Agent 通过 durable inbox 接收消息，一个 turn 包含一个或多个 step；每个 step 组装请求、流式调用模型、持久化 settlement、执行工具并决定是否继续。
3. **状态如何可靠？** `Session` 是只追加事件日志；模型历史是日志上的 surface 投影。JSONL 后端按 generation 保存，默认以带校验和的 Zstd 帧追加，并在模型调用、顶层工具副作用、下一 step 前设置持久性检查点。
4. **工具有什么独特设计？** Native/PTC/both 三种呈现；统一 pre/guard/execute/post/finalize/result 管线；并发安全工具可重叠执行，但结果按模型调用顺序提交。
5. **安全边界在哪里？** 内置沙箱是“同一宿主世界”的文件副作用约束，不覆盖网络，也不是容器/microVM；PTC Worker Thread 也不是多租户安全边界。官方明确建议使用专用 VM/容器。
6. **工程评价？** 架构一致性、崩溃语义、可替换能力和测试纪律强；代价是包数量与概念密度高，配置 patch 为整行替换容易踩坑，而且项目仍是 Developer Preview。

## Claim → Source ledger

| Claim | Primary source | Corroboration / notes |
|---|---|---|
| Everything is a plugin; no privileged core | `docs/architecture.zh.md` | Official landing page and README |
| Cordis uses reversible effects and reactive dependencies | arXiv:2608.25512 | `docs/cordis-primer.zh.md`, vendored Cordis source |
| Profile layering and whole-config replacement | `apps/cli/src/profile-boot.ts`, `packages/bundle/base/cordis.patch.yml` | `docs/architecture.zh.md` |
| Turn/step flow and durable/live split | `packages/core/agent-loop/src/agent.ts`, `assistant-stream.ts`, `tool-calls.ts` | `docs/architecture.zh.md` |
| Immutable append-only session and surface projection | `packages/core/session/src/index.ts`, `types.ts` | `docs/subsystems/session.zh.md` |
| JSONL/Zstd generation, fsync, recovery and single writer | `packages/session/session-persistence-jsonl/README.zh.md` and `src/` | persistence contract tests |
| Checkpoints fail closed before model and top-level tool body | `packages/session/session-checkpoint-policy/README.zh.md`, `src/index.ts` | base bundle row |
| Tool pipeline and PTC | `packages/core/tools/src/index.ts`, `ptc.ts` | `docs/tool-execution-pipeline.zh.md` |
| DeepSeek adapter route and request snapshot | `packages/llm/llm/src/index.ts`, `packages/llm/llm-deepseek/src/` | base bundle default selection |
| Compaction as a transaction over surface replacement | `packages/compaction/compaction-basic/README.zh.md`, `src/index.ts` | tool-result-pruner package |
| Sandbox limits and platform backends | `packages/sandbox/**/README.zh.md`, source | official safety policy |
| Subagent provider/continuation semantics | `docs/subsystems/subagent.zh.md`, `packages/subagent/subagent/src/` | base bundle wiring |
| Web/API/SDK share the same harness | `docs/api-gateway.zh.md`, `docs/subsystems/web-client.zh.md`, `python/sdk/README.zh.md` | web/sdk bundle patches |
| Quality gates include per-file 100% coverage and real API/browser/benchmark lanes | `docs/testing.zh.md`, root `package.json` | CI/run-gates sources |

## Research gaps / handling

- No external model call or full dependency install was performed; conclusions are source- and documentation-level, fixed to the commit above.
- Mutable popularity metrics (stars/forks/downloads) are intentionally excluded because they do not explain implementation and age quickly.
- DeepSeek adapter model sizes in source are treated as adapter defaults at this commit, not as a general API product promise.
- Security claims are deliberately bounded to the exact documented file-effect policy; no claim of process, network, kernel, or multi-tenant isolation is made.

## Source set

- Official repository: <https://github.com/deepseek-ai/deepseek-harness>
- Fixed source tree: <https://github.com/deepseek-ai/deepseek-harness/tree/b0a7d2ce3b4c19d7452e364b2d7acbfa87e707ed>
- Official docs: <https://deepseek-harness.github.io/deepseek-harness/>
- Official product page: <https://www.deepseek.com/harness/en/>
- Cordis paper: <https://arxiv.org/abs/2608.25512>
- Official safety policy: <https://www.deepseek.com/harness/privacy/>
- Official data-processing statement: <https://www.deepseek.com/harness/en/data-processing/>
