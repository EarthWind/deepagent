# ECC 研究源码索引

基线：[`8321021c54d670126ce3b2969d5deb880b4b0c2a`](https://github.com/affaan-m/ECC/tree/8321021c54d670126ce3b2969d5deb880b4b0c2a)，`ecc-universal 2.2.1`。所有链接固定到该提交。

正文将源码事实、文档描述、实验结果与工程建议分开。索引中的文件是被引用的证据范围，不代表每行源码均经过完整审计。文件 SHA-256 与统计口径见 [snapshot.json](snapshot.json)。

## 证据使用规则

- 当前入口以插件声明、Hook 注册和实际脚本为准。
- 路线图只说明方向，不据此宣称已经实现。
- 外部宿主的完整能力不从 ECC 单个适配文件推断。
- 测试退出码验证具体实现行为，不证明模型完成率和吞吐提升。
- AgentShield、真实付费模型调用、Rust 构建和多操作系统端到端安装未纳入本次执行验证。

## 项目与能力资产

| 文件 | 行数 |
| --- | ---: |
| [`README.md`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/README.md) | 2012 |
| [`package.json`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/package.json) | 532 |
| [`LICENSE`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/LICENSE) | 21 |
| [`agents/planner.md`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/agents/planner.md) | 221 |
| [`commands/plan.md`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/commands/plan.md) | 206 |
| [`skills/search-first/SKILL.md`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/skills/search-first/SKILL.md) | 183 |
| [`skills/verification-loop/SKILL.md`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/skills/verification-loop/SKILL.md) | 129 |
| [`skills/plan-orchestrate/SKILL.md`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/skills/plan-orchestrate/SKILL.md) | 263 |
| [`legacy-command-shims/commands/orchestrate.md`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/legacy-command-shims/commands/orchestrate.md) | 24 |
| [`skills/team-agent-orchestration/SKILL.md`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/skills/team-agent-orchestration/SKILL.md) | 111 |
| [`skills/dynamic-workflow-mode/SKILL.md`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/skills/dynamic-workflow-mode/SKILL.md) | 124 |
| [`skills/security-scan/SKILL.md`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/skills/security-scan/SKILL.md) | 166 |

## 安装与宿主适配

| 文件 | 行数 |
| --- | ---: |
| [`.claude-plugin/plugin.json`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/.claude-plugin/plugin.json) | 46 |
| [`.codex-plugin/plugin.json`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/.codex-plugin/plugin.json) | 50 |
| [`scripts/lib/install-manifests.js`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/scripts/lib/install-manifests.js) | 757 |
| [`scripts/lib/install/plan.js`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/scripts/lib/install/plan.js) | 358 |
| [`scripts/lib/install/apply.js`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/scripts/lib/install/apply.js) | 689 |
| [`scripts/lib/install/ownership-guard.js`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/scripts/lib/install/ownership-guard.js) | 159 |
| [`scripts/lib/install-state.js`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/scripts/lib/install-state.js) | 354 |
| [`manifests/install-profiles.json`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/manifests/install-profiles.json) | 106 |
| [`scripts/lib/install/hook-consent.js`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/scripts/lib/install/hook-consent.js) | 202 |
| [`.mcp.json`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/.mcp.json) | 8 |
| [`docs/architecture/cross-harness.md`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/docs/architecture/cross-harness.md) | 187 |
| [`.cursor/hooks/adapter.js`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/.cursor/hooks/adapter.js) | 81 |
| [`.opencode/plugins/ecc-hooks.ts`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/.opencode/plugins/ecc-hooks.ts) | 624 |

## 事件运行与上下文

| 文件 | 行数 |
| --- | ---: |
| [`hooks/hooks.json`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/hooks/hooks.json) | 254 |
| [`hooks/codex-hooks.json`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/hooks/codex-hooks.json) | 18 |
| [`scripts/lib/hook-flags.js`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/scripts/lib/hook-flags.js) | 153 |
| [`scripts/hooks/plugin-hook-bootstrap.js`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/scripts/hooks/plugin-hook-bootstrap.js) | 328 |
| [`scripts/hooks/run-with-flags.js`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/scripts/hooks/run-with-flags.js) | 275 |
| [`scripts/hooks/bash-hook-dispatcher.js`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/scripts/hooks/bash-hook-dispatcher.js) | 211 |
| [`scripts/hooks/posttooluse-dispatcher.js`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/scripts/hooks/posttooluse-dispatcher.js) | 290 |
| [`scripts/hooks/config-protection.js`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/scripts/hooks/config-protection.js) | 176 |
| [`scripts/hooks/block-no-verify.js`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/scripts/hooks/block-no-verify.js) | 579 |
| [`scripts/hooks/gateguard-fact-force.js`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/scripts/hooks/gateguard-fact-force.js) | 1347 |
| [`scripts/hooks/quality-gate.js`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/scripts/hooks/quality-gate.js) | 168 |
| [`scripts/hooks/post-edit-accumulator.js`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/scripts/hooks/post-edit-accumulator.js) | 78 |
| [`scripts/hooks/stop-format-typecheck.js`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/scripts/hooks/stop-format-typecheck.js) | 251 |
| [`scripts/hooks/session-start.js`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/scripts/hooks/session-start.js) | 798 |
| [`scripts/hooks/session-end.js`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/scripts/hooks/session-end.js) | 355 |
| [`scripts/lib/llm-summary.js`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/scripts/lib/llm-summary.js) | 177 |
| [`scripts/hooks/pre-compact.js`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/scripts/hooks/pre-compact.js) | 178 |
| [`scripts/hooks/suggest-compact.js`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/scripts/hooks/suggest-compact.js) | 276 |
| [`scripts/lib/observer-sessions.js`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/scripts/lib/observer-sessions.js) | 212 |
| [`scripts/hooks/observe-runner.js`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/scripts/hooks/observe-runner.js) | 199 |
| [`scripts/lib/instinct-relevance.js`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/scripts/lib/instinct-relevance.js) | 173 |
| [`scripts/hooks/cost-tracker.js`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/scripts/hooks/cost-tracker.js) | 257 |

## 持续学习

| 文件 | 行数 |
| --- | ---: |
| [`skills/continuous-learning-v2/SKILL.md`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/skills/continuous-learning-v2/SKILL.md) | 377 |
| [`skills/continuous-learning-v2/config.json`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/skills/continuous-learning-v2/config.json) | 8 |
| [`skills/continuous-learning-v2/hooks/observe.sh`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/skills/continuous-learning-v2/hooks/observe.sh) | 675 |
| [`skills/continuous-learning-v2/agents/start-observer.sh`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/skills/continuous-learning-v2/agents/start-observer.sh) | 252 |
| [`skills/continuous-learning-v2/agents/observer-loop.sh`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/skills/continuous-learning-v2/agents/observer-loop.sh) | 545 |
| [`skills/continuous-learning-v2/scripts/instinct-cli.py`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/skills/continuous-learning-v2/scripts/instinct-cli.py) | 2290 |

## 记忆服务

| 文件 | 行数 |
| --- | ---: |
| [`scripts/lib/memory-vault.js`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/scripts/lib/memory-vault.js) | 808 |
| [`scripts/lib/memory-vault-format.js`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/scripts/lib/memory-vault-format.js) | 309 |
| [`scripts/memory.js`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/scripts/memory.js) | 504 |
| [`scripts/memory-mcp.mjs`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/scripts/memory-mcp.mjs) | 688 |

## 编排、评估与其他模块

| 文件 | 行数 |
| --- | ---: |
| [`src/llm/core/interface.py`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/src/llm/core/interface.py) | 60 |
| [`scripts/orchestrate-worktrees.js`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/scripts/orchestrate-worktrees.js) | 108 |
| [`scripts/lib/tmux-worktree-orchestrator.js`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/scripts/lib/tmux-worktree-orchestrator.js) | 598 |
| [`scripts/lib/state-store/index.js`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/scripts/lib/state-store/index.js) | 367 |
| [`scripts/lib/state-store/migrations.js`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/scripts/lib/state-store/migrations.js) | 209 |
| [`scripts/lib/eval-harness/index.js`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/scripts/lib/eval-harness/index.js) | 24 |
| [`scripts/lib/eval-harness/capsule.js`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/scripts/lib/eval-harness/capsule.js) | 410 |
| [`scripts/lib/eval-harness/receipt.js`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/scripts/lib/eval-harness/receipt.js) | 180 |
| [`scripts/eval-harness.js`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/scripts/eval-harness.js) | 155 |
| [`scripts/lib/eval-harness/gate.js`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/scripts/lib/eval-harness/gate.js) | 258 |
| [`ecc2/Cargo.toml`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/ecc2/Cargo.toml) | 61 |
| [`ecc2/README.md`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/ecc2/README.md) | 114 |
| [`ecc2/src/harness_eval.rs`](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/ecc2/src/harness_eval.rs) | 579 |

## 运行证据

- [16 组上游测试结果](test-results.json) 与其中指向的原始日志。
- [五组源码实验结果](probe-results.json)。
- [实验代码](../examples/probe.cjs) 与 [测试执行器](run_upstream_checks.py)。
- [验证方法和限制](verification.md)。
