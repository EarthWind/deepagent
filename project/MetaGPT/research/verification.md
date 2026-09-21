# 调研方法、版本差异与验证边界

调研日期：2026-09-21。源码固定到 [`11cdf466d042aece04fc6cfd13b28e1a70341b1f`](https://github.com/FoundationAgents/MetaGPT/tree/11cdf466d042aece04fc6cfd13b28e1a70341b1f)。`git ls-remote` 在调研时返回 HEAD 与 main 均为该提交。提交时间是 2026-01-21，不是本次调研日期。

## 调研方法

1. 克隆官方仓库到研究用临时目录，读取固定提交的活动代码。
2. 阅读 MetaGPT 原论文 v7、Data Interpreter 论文摘要与官方通信、配置文档。
3. 从 CLI 到 Team、环境、角色、Action、Provider 与执行工具追踪调用链。
4. 阅读相关上游测试辅助理解意图；不将测试文件存在或静态阅读报告为通过测试。
5. 在固定源码上运行方法体隔离实验，单独运行原创教学示例。
6. 生成源码哈希、行号索引与七幅 SVG 图，并检查文档引用和图表布局。

源码未整体复制进博客目录。公开引用固定到提交，阅读不依赖研究用 `/tmp` checkout。

## 核对出的重要版本差异

| 问题 | 该提交实际行为 |
| --- | --- |
| `Team()` 默认是什么环境 | `use_mgx=True`，默认 MGXEnv |
| 默认 CLI 团队 | TeamLeader、ProductManager、Architect、Engineer2、DataAnalyst |
| 经典 PRD→设计→任务流程是否仍在 | 在，但要显式选择环境与固定 SOP 分支 |
| `run_tests` 是否聘用 QaEngineer | 对应经典聘用代码已注释；不能依赖该开关 |
| `generate_repo` 是否返回 ProjectRepo | 活动代码返回 Context kwargs 中的 project_path |
| 环境是否按 watch 投递 | 先按 send_to 地址投递，Role._observe 再按 watch/名字筛选 |
| observe_all 是否让角色响应全部消息 | 允许保存全部消息；news 仍受触发条件筛选 |
| RoleZero 是否依赖原生 tool_calls | 主路径解析 aask 返回文本中的 JSON 命令 |
| 工具推荐是否每次都 BM25 检索 | RoleZero 使用 force=True 的分支，通常返回配置工具集合 |
| 长期记忆和经验池是否默认启动 | 两者默认均关闭 |
| memory_k 是否自动限制全部存储容量 | 用于近期上下文和检索窗口；不能推导 storage 自动淘汰 |
| investment 是否模型调用中的硬限额 | Team 在环境轮次开始前检查已累计成本 |
| 序列化是否保存一切执行状态 | RoleContext 排除队列等字段；进程和内核状态需独立处理 |

以上是固定源码范围内的结论，不对未来提交或托管产品 MGX/Atoms 的内部架构作推断。

## 15 项方法体隔离实验

运行命令：

```bash
python3 project/MetaGPT/research/source_probes.py /path/to/MetaGPT \
  --output /tmp/metagpt-probe-results.json
```

脚本要求 checkout 的 commit 与基线一致。从 AST 提取指定上游函数/方法体，移除装饰器并延迟类型注解解析。Message、Memory、RoleContext 等外围对象使用测试替身；没有导入整个 MetaGPT 包。因此测试**不覆盖** Pydantic 验证器、模型连接、装饰器异常行为和真实工具资源生命周期。

实测 15 项全部通过，详见 [probe-results.json](probe-results.json)：广播、定向排除、Action 订阅、名字定向、类地址与触发差异、仅记忆不行动、相等消息去重、新 ID 消息、轮次中的唤醒、下一轮调度、run_project 的未使用参数、工具异常中止、未知工具中止、MGX 追加 Leader、Leader 占位消息抑制。

源码哈希记录在 [sources.json](sources.json)，具体方法锚点见 [source-map.md](source-map.md)。重新运行前应保持 checkout 干净，必要时与哈希核对。

## 原创离线示例

运行 `mini_sop.py` 实际得到 6 条事件，QA 第一轮失败、第二轮通过，结果 `stop=idle; accepted=True`。两次运行的是作者预定义代码片段，未执行模型或外部仓库生成的程序。运行轨迹保存在 [demo-trace.json](demo-trace.json)。

本机 Python 为 3.14.4；这满足原创教学脚本需求，但不符合上游 MetaGPT `<3.12` 的安装要求，因此没有直接在该解释器安装完整框架。首次沙盒运行中，线程完成通知没有唤醒异步循环；使用相同脚本在授权的沙盒外执行后正常完成。这是本地执行环境现象，不作为 MetaGPT 问题。

## 文档与图表检查

正文包含 17 节、约 1.2 万汉字，不包含在此数字中的英文代码和链接；源码索引覆盖 57 个文件。文章产物检查结果见 [artifact-checks.json](artifact-checks.json)。

- 本地文件链接和显式章节锚点检查通过；检查范围包含正文、附属说明和 HTML。
- 7 张 SVG 的 XML、viewBox、辅助标题和描述检查通过。
- 无头 Chrome 实际渲染全部图表，检查文字边界；修正一处委派图框内文字溢出后，结果为零溢出，见 [diagram-checks.json](diagram-checks.json)。
- 人工查看图表总览，以及 HTML 在 1440×1100 和 390×844 视口的截图。窄屏表格与图表允许横向滚动，点击图表可以打开原图。
- 所有附带 Python 文件通过 AST 语法解析；实际模型示例未被冒充为运行成功。

重建与自检（在本仓库根目录）：

```bash
python3 project/MetaGPT/assets/generate_diagrams.py
python3 project/MetaGPT/research/build_sources.py /path/to/MetaGPT
python3 project/MetaGPT/research/build_blog.py
python3 project/MetaGPT/research/verify_artifacts.py
```

后两个脚本依赖 `markdown-it-py`；本次使用本机已有模块。阅读已生成的 HTML 和 SVG 不需要这些依赖，也不需要网络。自检不逐一请求外部网站；源码链接根据已克隆文件及固定 commit 构造。

## 未执行的工作

- 完整 MetaGPT 安装、上游 pytest 全套或选定集成测试。
- 真实模型调用、当前 CLI 软件生成、浏览器交互与部署。
- 真实 Notebook 内核、长期向量记忆、经验池端到端运行。
- 原论文 HumanEval/MBPP 等性能复现。
- 对所有扩展目录、托管 MGX 产品及依赖生态的全面审计。

正文中的示意时序、工程建议与教学输出均明确标识，不作为上述未执行项目的实验结果。

## 原始资料

- [官方固定源码](https://github.com/FoundationAgents/MetaGPT/tree/11cdf466d042aece04fc6cfd13b28e1a70341b1f)：正文实现结论的首要依据。
- [MetaGPT 论文 v7](https://arxiv.org/html/2308.00352v7)：SOP、结构化通信与执行反馈的研究背景。
- [Data Interpreter 论文](https://arxiv.org/abs/2402.18679)：数据任务 Agent 的研究背景。
- [官方通信文档](https://docs.deepwisdom.ai/main/en/guide/in_depth_guides/agent_communication.html)：辅助理解消息协议；细节以固定源码为准。
- [官方配置文档](https://docs.deepwisdom.ai/main/en/guide/get_started/configuration.html)：配置入口参考。
- [上游 MIT 许可证](https://github.com/FoundationAgents/MetaGPT/blob/11cdf466d042aece04fc6cfd13b28e1a70341b1f/LICENSE)：原项目许可；本目录图表和教学模型为原创说明材料。

OpenReview 页面在访问时触发浏览器验证，因此论文阅读使用 arXiv 固定版本。网页与 README 可能继续变化，不能替代 commit 固定的实现证据。
