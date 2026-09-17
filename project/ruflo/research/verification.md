# 调研与验证记录

## 固定基线

- 仓库：<https://github.com/ruvnet/ruflo>。
- 提交：`6f0ed7112873eedc7cfe17281a2585188190b790`，main 浅克隆。
- 提交时间：2026-09-16 16:36:46 UTC；研究日期：2026-09-17，Asia/Shanghai。
- 源码中的 root / ruflo / cli 版本均为 `3.42.0`。
- 本地 Node：`v24.18.0`；网页构建使用 Python 3、markdown-it-py `3.0.0`。
- 网页入口用于发现项目与确认当前方向，详细实现以本地固定提交为准。网络页面缓存可能滞后，例如首次读取的 CLI package 页面显示了较早版本，未将其混入研究基线。

## 证据层次

1. **源码观察**：沿入口、调用、状态文件、外部依赖检查；52 个固定提交源码链接和 SHA-256 见 [source-inventory.json](source-inventory.json)。
2. **源码行为实验**：使用上游真实 TypeScript handler，类型转换与源码路径解析由本地 loader 提供；Provider 网络边界使用 fixture。
3. **上游检查**：选择依赖范围较小、能够支撑本文主张的四组检查，不代表全仓测试通过。
4. **工程推断**：JSON 旧快照覆盖风险、检索窗口对召回的影响、奖励信号偏差等，已在正文注明推断或评估建议。

## 源码行为结果

[probe-results.json](probe-results.json)：7 组通过，真实模型调用 0 次，fixture 请求 3 次。

- 注册 Agent 不发送模型请求。
- execute 请求不包含 tools，一次请求返回后 taskCount 增加、状态回到 idle。
- workflow task/wait 能执行，parallel/loop 被 skipped。
- `lastStepOutput` 可替换，自动生成的 `step-1.output` 因连字符不匹配而保持原样。
- 在没有活动 runner 的构造场景，resume 只修改为 running；后续 execute 返回 already running。
- 独立 hybrid tokenizer 对纯中文返回空数组；英文关键词 BM25 样例工作。
- 原始签名验证通过，篡改 payload 后失败。
- 生成器路由器对测试关键词返回 tester 与 0.6。

以上结果由 7 组实验中的多个断言给出，不能把断言数和实验分组数混用。

## 上游检查

运行器：[run_upstream_checks.py](run_upstream_checks.py)。结果：[upstream-checks.json](upstream-checks.json)。

| 命令 / 脚本 | 结果 | 原始输出 |
| --- | --- | --- |
| `node --test tests/hook-handler-runwithtimeout.test.cjs` | 5/5 | [日志](logs/hook-handler-runwithtimeout.test.cjs.txt) |
| `node scripts/smoke-pre-bash-hook.mjs` | 14 个场景通过 | [日志](logs/smoke-pre-bash-hook.mjs.txt) |
| `node --import <source-loader> scripts/smoke-router-regex.mjs` | 11/11 + 锚点检查 | [日志](logs/smoke-router-regex.mjs.txt) |
| `node scripts/smoke-agent-execute-providers.mjs` | 5 项静态检查通过 | [日志](logs/smoke-agent-execute-providers.mjs.txt) |

初次沙箱执行出现 `spawnSync git EPERM` 与子进程标准输出异常，未把这些异常误记为上游缺陷。允许在沙箱外执行本地检查后重新运行，表格与日志记录的是有效复测结果。路由测试使用同一个源码 loader 补充 monorepo 的模块解析；没有安装 tsx，也没有修改测试内容。

## 没有验证的范围

- 没有安装 npm 发布 tarball，未验证源码与发布产物完全一致。
- 没有运行完整 monorepo 的 build/lint/test，也没有安装完整可选原生依赖。
- 没有运行真实 Claude Code/Codex 会话或调用真实模型。
- 没有下载并评估 ONNX 模型，未测语义召回质量、HNSW 加速或 token 节省。
- 没有部署真实 Federation 集群或做网络分区、掉线、重放的端到端实验。
- 没有验证 WASM、Managed Agent 或所有安全开关的完整隔离效果。
- 不根据宣传、命名、注释或单项检查推断生产可用性与合规认证。

## 文档与图片

`build_blog.py` 从 README 构建离线 HTML，生成 8 张原创 SVG，并对卡片文字高度进行检查。`validate_artifacts.py` 检查本地链接、文档锚点、源文件哈希与图文件结构，结果见 [artifact-checks.json](artifact-checks.json)。

本地浏览器检查覆盖桌面、窄屏网页与架构图。页面不依赖 CDN、外部脚本或字体下载。浏览器诊断与图文字边界结果另见生成后的 [browser-checks.json](browser-checks.json)。
