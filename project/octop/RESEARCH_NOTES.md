# 调研记录、版本差异与复现

调研日期：2026-09-20。Octop 提交：`757fd12e5dcae7f9303dbfbbf6321a6986694a8b`。

## 方法与证据等级

本次先查阅官方 GitHub 页面，再克隆 `main` 的源码并固定提交。正文中涉及运行内核的结论，还追踪了 `uv.lock` 指定的四个发行源码包：`orcakit-harness-agent 1.0.11`、`harness-memory 0.9.10`、`harness-gateway 0.9.8`、`deepagents 0.7.9`。下载包已逐一与锁文件的 SHA-256 对照，没有安装或执行这些包的安装脚本。

`harness-browser 0.7.9` 和 `langgraph 1.2.11` 的版本来自锁文件；本次没有单独下载和审查它们的完整内部实现。有关浏览器的说明限于 Octop/Harness 的集成边界。

正文区分三种内容：源码中的实现事实；单进程扩展性、预算超额窗口等基于代码结构的工程推论；持久任务队列、幂等与检索改造等作者建议。没有用建议填补现有实现，也没有将旧设计文档视为可执行行为。

源码证据共 63 份，文件路径、SHA-256、符号行号及出处保存在 [snapshot.json](research/snapshot.json)；人工阅读入口为 [SOURCE_MAP.md](SOURCE_MAP.md)。索引不是源码副本，固定链接和发行包散列可用于重新取得相同内容。

## 文档与代码之间的重要差异

| 主题 | 容易读到的旧描述 | 本次采用的实现证据 |
| --- | --- | --- |
| AgentManager 归属 | README 图为每用户 manager | `server._boot_runtime` 创建全局 `AgentManager`；`manager.py` 明确为 process-wide |
| 普通聊天传输 | 遗留 SSE stream / 旧 `chat.py` | `api/routers/chat/ws.py` 为普通聊天；HITL resume 仍为 SSE |
| “所有入口同一 Processor” | 产品概述中的统一流水线 | Cron 的 `delivery.py` 直接 stream；ACP 取得 HarnessAgent；peer 通过 TeamManager |
| `@专家` 调度 | 旧 `apply_mentions` 并行预调用并注入结果 | 锁定 Harness 的 `PeerAgentMiddleware` 追加名单与指引，由模型调用 `ask_agent` |
| peer 工具注册 | 文档示例直接扩展 `config.tools` | 当前 manager 注释与 Harness 构图显示由 PeerAgentMiddleware 挂载 |
| peer 子线程 | 旧 inbox 图写每次新 thread | 当前可由父 thread 与 target ID 派生，宿主还注册 peer session/history |
| 默认存储/执行 backend | 架构文档写 workspace-scoped filesystem | POSIX 实际取 local_shell + root `/`；Windows 有 workspace 分支 |
| “重启可恢复” | 配置重建被容易扩大解释为任务恢复 | Gateway queue、Teams inbox、WS 订阅在内存；KB 索引任务则有单独恢复逻辑 |
| PostgreSQL 的作用 | 容易推断所有状态都迁移到远端 | KB `KnowledgeIndex` 仍是本地 SQLite；可选 history_v2 归档当前限制 SQLite 控制面 |
| 默认安全性 | 功能表列出工具审批与 guard | Octop 默认 HITL false、ToolGuard warn；敏感路径与 PII 另外启用 |

这些差异反映文档、设计稿和代码更新节奏不同。它们不是逐项漏洞结论。尤其 shared Agent、ACP、沙盒和恢复语义，需要真实部署环境中的集成测试进一步验证。

## 已执行的验证

1. 固定 Octop 提交与项目版本；验证四个源码发行包哈希。
2. 校验索引中 63 份源文件的 SHA-256，避免读取路径或依赖版本漂移。
3. 执行 10 项小范围上游代码验证，结果见 [probe-results.json](research/probe-results.json)。
4. 执行 4 项随文教学示例测试：提交与串行顺序、父 thread 回写、失败处理、新实例不恢复旧内存队列。
5. 对最终 Markdown 链接、SVG XML、HTML 本地资源和文件结构做交付物检查，结果见 [artifact-checks.json](research/artifact-checks.json)。
6. 用无头 Chrome 检查离线网页的桌面/移动布局与 8 张 SVG，记录见 [visual-checks.json](research/visual-checks.json)。

第 3 项只加载上游的标准库模块；父包壳仅用于避免触发应用全量初始化，不替换分块或索引函数。Deep Agents 的默认值函数经 AST 提取原函数体。验证过程不请求模型、不访问外部工具，索引写到自动清理的临时目录。环境为 Python 3.14.4。

第 4 项测试的是原创教学代码，不能作为上游 inbox 已通过实跑测试的证据。inbox 的实现判断来自固定发行源码阅读。

**未执行：** Octop 全量依赖安装、上游完整 pytest / `make all`、控制台构建、真实模型任务、IM 平台接入、ACP runner 启动、Docker/bwrap/OpenSandbox 隔离验证、PostgreSQL 服务、负载测试、成本或准确率评测。未提交或发布上游代码，也未改动用户现有 Octop 数据。

## 复现源码与小范围验证

以下命令从本博客所在仓库根目录执行。路径可以自选，不要求使用本次临时目录。

```bash
git clone https://github.com/TencentCloud/Octop.git /tmp/octop-source
git -C /tmp/octop-source checkout 757fd12e5dcae7f9303dbfbbf6321a6986694a8b

# 需要网络；只下载、校验和解压锁定包，不安装依赖。
python3 project/octop/scripts/fetch_dependencies.py /tmp/octop-source /tmp/octop-deps

# 重建索引，并对固定代码执行隔离验证。
python3 project/octop/scripts/gather_sources.py /tmp/octop-source /tmp/octop-deps
python3 project/octop/scripts/probe_upstream.py /tmp/octop-source /tmp/octop-deps

# 教学示例只需 Python 标准库。
python3 -m unittest discover -s project/octop/examples -p 'test_*.py' -v
python3 project/octop/examples/inbox_demo.py
```

`gather_sources.py` 会拒绝不匹配的 Octop 提交；`probe_upstream.py` 会拒绝不匹配的源文件哈希。依赖源码包链接和校验值都记录在机器可读快照里。

## 重建插图与离线网页

所有插图源代码在 [render_diagrams.py](scripts/render_diagrams.py)，使用 Python 标准库输出 SVG。直接阅读 README 或 SVG 无需安装前端依赖。

```bash
python3 project/octop/scripts/render_diagrams.py

# 仅重建 HTML 时需要 markdown-it-py；建议在自己的虚拟环境安装。
python3 -m pip install -r project/octop/scripts/requirements.txt
python3 project/octop/scripts/build_blog.py
python3 project/octop/scripts/check_artifacts.py
```

打开 `project/octop/index.html` 即可离线阅读。网页无 CDN、无在线字体、无第三方脚本，图像都通过相对路径引用。源码与外部参考链接需要联网访问。

## 内容与资产说明

- `README.md`：正文，也是离线网页的内容源。
- `index.html`：静态博客，包含目录与移动端布局。
- `SOURCE_MAP.md` / `source-map.html`：固定源码索引。
- `RESEARCH_NOTES.md` / `research-notes.html`：本调研记录。
- `assets/*.svg`：8 张原创工程图；不是产品截图、官方设计图或实测图。
- `examples/`：不接模型和网络的教学示例与测试。
- `research/`：版本、来源与验证记录。
- `scripts/`：可复现的生成与检查脚本。

保留上游 MIT 及依赖各自许可证语义。正文只用必要的符号、配置名称和少量说明性伪代码，不把上游源码完整复制进本仓库。
