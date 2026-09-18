# 调研记录、版本差异与验证范围

调研日期：2026-09-18。固定源码：[`1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1`](https://github.com/aaif-goose/goose/tree/1e83e89f556fc60fd396df1fd0f2992f8b2f2dc1)。产品 workspace 版本 `1.51.0`，不据此推断 stable release 标签。版本元数据见 [research.json](research.json)，完整源码锚点见 [SOURCE_MAP.md](SOURCE_MAP.md)。

## 1. 调研方法

从官方 GitHub 仓库浅克隆一个源码快照，记录 commit 后静态追踪：

1. CLI、Electron 启动逻辑、ACP 会话请求与循环选择。
2. `Agent::reply`、传统工具循环、`StateMachine::step/apply/run`。
3. Provider trait、扩展发现与 dispatch、Code Mode 的 callback。
4. 权限 Inspector、Hooks、子任务模式及 container 选项覆盖面。
5. 消息可见性、压缩、SQLite 写入、Recipe 和子会话生命周期。
6. 对照官方说明与上游测试代码，记录哪些是能力、哪些是默认行为。

上游源码保留在研究用临时目录，没有将几百 MB 的完整仓库复制进博客目录。本文无须临时 checkout 即可阅读，所有证据链接都固定到公开 commit。

“源码事实”仅指本快照中可以追踪到的实现；“工程建议”是作者依据实现做出的设计判断；“本地验证”仅涵盖本目录原创示例和文章产物。三者不互相替代。

## 2. 容易产生误读的十个事实

| 主题 | 容易出现的说法 | 固定源码实际说明 |
| --- | --- | --- |
| Agent loop 默认值 | 状态机关闭，所以所有入口默认传统循环 | 环境开关默认关；Desktop 的 `useLegacyAgentLoop=false`，通过 ACP metadata 默认选状态机 |
| Desktop 架构 | 所有版本都用旧 goose-server REST/SSE | 本快照启动 `goose serve`，聊天通过 WebSocket ACP；见 `gooseServe.ts`、`acpConnection.ts` |
| 后台工具摘要 | 文档介绍了摘要，所以默认开 | `GOOSE_TOOL_PAIR_SUMMARIZATION` 的源码默认值为 `false` |
| Code Mode | 只有固定三个元工具 | 默认 Catalog 是三个；Filesystem 是两个，Sidecar 是一个，并有不同直接工具披露策略 |
| 工具前置日志 | 有 SQLite 就能保证先记调用再执行 | 传统常规分支在工具执行后组装 request/result 再落盘，状态机的分步边界不同 |
| Approve | 读工具都一定免审批 | Approve 在未命中用户规则时要求确认；只读 annotation 的显式放行分支属于 SmartApprove |
| Auto | 自动批准安全动作 | PermissionInspector 的 Auto 分支直接 Allow；其他检查器是否启用、如何决策是另外的问题 |
| 安全检查 | 注册了检查器就代表全部默认开启且 fail closed | 提示注入检测默认关闭，Adversary 依赖配置，manager 遇检查错误记录后继续 |
| 子 Agent | 完全继承父审批模式和文件隔离 | 当前同步/异步委派显式设置 Auto；新上下文、cwd 检查不构成 OS 沙箱 |
| Code Mode 审批 | 每个内部 callback 都重新走普通调用的 Inspector | callback 直接进入 ExtensionManager；外层执行请求与内部函数的审批粒度不同 |

这些差异不是对其他版本的断言。尤其在迁移期，不能仅凭上游 `AGENTS.md` 的概括就覆盖客户端实际默认设置，也不能假设新旧循环的所有失败恢复次数完全相同。

## 3. 与在线文档交叉检查

在线文档会随项目更新。以下用于说明调研中的核对方向，最终实现判断仍以固定源码为准：

- [Smart Context Management](https://goose-docs.ai/docs/guides/sessions/smart-context-management/) 说明自动压缩、模型窗口和工具摘要；默认 0.8 与源码一致，工具对摘要的启用默认需另看 `context_mgmt/mod.rs`。
- [Permission Modes](https://goose-docs.ai/docs/guides/managing-tools/goose-permissions/) 的权限表和后续只读工具说明存在需要结合代码理解的地方；本文按 `PermissionInspector` 区分 Approve 与 SmartApprove。
- [Code Mode](https://goose-docs.ai/docs/guides/managing-tools/code-mode/) 主要介绍三个元工具的使用方式；本快照源码还存在 Filesystem 和 Sidecar 分支。
- [Recipe Reference](https://goose-docs.ai/docs/guides/recipes/recipe-reference/) 用于核对配方字段；示例的参数、扩展过滤和 response schema 又与 Rust 数据模型、adapter 和 final-output 校验交叉检查。
- [Subrecipes](https://goose-docs.ai/docs/guides/recipes/subrecipes/) 描述独立上下文；本文将它与实际共享目录、子任务 Auto 模式和 parent session 关联一起分析。

未使用第三方宣传文章来证明内部实现，也未把仓库 star 数、供应商数量或网站当前广告文案作为架构结论。

## 4. 本次实际完成的验证

| 验证 | 执行方法 | 结果与边界 |
| --- | --- | --- |
| 教学状态机运行 | `python3 project/goose/examples/state_machine_demo.py` | 审批挂起 → 重建 Store/Machine → 完成；得到 count=5 |
| 教学语义测试 | `python3 -m unittest discover -s project/goose/examples -p 'test_*.py' -v` | 8 项通过；涵盖拒绝、重建、重复等待/恢复、取消、错误 observation、过期审批和可见性 |
| Recipe 数据检查 | 本地 PyYAML 解析 + jsonschema 检查及示例输出验证 | YAML 可解析、schema 有效，显式 tree-only 配置与 focus 参数存在 |
| 源码与引用检查 | `scripts/check_artifacts.py --source-root <固定源码目录>` | 检查 commit、81 个源码链接、路径和锚点行，以及 Markdown 本地链接和代码围栏 |
| SVG 结构检查 | 同上，使用 XML parser | 7 张 SVG 可解析，具有 title/description，不含 script |
| 图形视觉检查 | Chrome headless 渲染本地 SVG 拼图并人工查看 | 七图中文、线条、箭头与文本完整，未发现裁切或内容遮挡 |
| 工作区检查 | `git diff --check`；只新增 `project/goose` 内容 | 不修改其他项目的未提交工作 |

### 没有执行的验证

- 没有安装 Goose 二进制或编译上游 Rust/Electron 工程。
- 没有运行上游 `cargo test`、MCP integration、ACP integration 或真实模型评测。
- 没有真正执行 `goose recipe validate`，该命令作为已安装 Goose 后的后续验证步骤提供。
- 没有真实 Provider 调用、API 成本测试、模型对比或性能压测。
- 没有将 Code Mode / 子 Agent 权限边界演示为已复现的安全漏洞。

因此本文适合回答“这个版本怎样实现、有什么边界、如何复用设计”，不适合直接作为运行质量、默认发行包功能集合或企业安全认证结论。

## 5. 复核与更新方法

将 Goose checkout 到记录的 commit 后，从 `deepagent` 根目录执行：

```bash
python3 project/goose/scripts/check_artifacts.py --source-root /path/to/goose
python3 project/goose/scripts/render_diagrams.py
```

`check_artifacts.py` 使用标准库，不联网；它验证链接和源码锚点，不自动判断文章自然语言结论是否正确。Recipe 的 YAML/schema 检查需要本地有 PyYAML 与 jsonschema；这不是无依赖教学示例的运行要求。

以后更新文章时，应重新核对客户端默认循环、源码模式开关、Code Mode callback、子任务模式和压缩默认值。这些是最容易让旧文章结论过时的地方。修改 `research.json` 或链接中的 SHA 并不足以完成版本升级。
