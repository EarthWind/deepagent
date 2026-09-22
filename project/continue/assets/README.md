# 原创工程图

9 张 SVG 均由本次调研依据固定提交手工设计，使用 Python 标准库生成。不是官方产品截图，也没有虚构运行日志或性能数值。图中 Sxx 编号对应 [源码地图](../research/source-map.md)。

1. `01-architecture.svg`：三个客户端与两条 Agent 编排主线。
2. `02-ide-loop.svg`：GUI 状态与 Core 工具执行。
3. `03-cli-loop.svg`：CLI 的独立循环与压缩检查。
4. `04-context.svg`：上下文编译与预算。
5. `05-retrieval.svg`：已弃用入口背后的 RAG 实现。
6. `06-editing.svg`：IDE 与 CLI 编辑生命周期对照。
7. `07-autocomplete.svg`：补全专用管道。
8. `08-permissions.svg`：模式、审批和子 Agent 边界。
9. `09-persistence.svg`：消息恢复与外部副作用的区别。

重建：`python3 project/continue/assets/generate_diagrams.py`。

SVG 自带 title/desc，可直接在浏览器打开。字体使用系统中文字体；为保持离线可用，没有远程字体或脚本。
