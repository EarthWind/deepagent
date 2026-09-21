# 原创图表

本目录包含 7 张 SVG 工程示意图，内容依据正文固定源码绘制，不包含性能统计数据或上游图片转载。

| 文件 | 内容 |
| --- | --- |
| [01-architecture.svg](01-architecture.svg) | 当前 MGX 与经典 SOP 的总架构 |
| [02-classic-sop.svg](02-classic-sop.svg) | 经典角色与文档交接 |
| [03-message-routing.svg](03-message-routing.svg) | 投递、观察、订阅与去重 |
| [04-mgx-delegation.svg](04-mgx-delegation.svg) | TeamLeader 委派示意时序 |
| [05-rolezero-loop.svg](05-rolezero-loop.svg) | 模型决策与工具执行循环 |
| [06-memory-recovery.svg](06-memory-recovery.svg) | 记忆、快照与外部执行状态 |
| [07-data-interpreter.svg](07-data-interpreter.svg) | 计划、代码执行与失败反馈 |

生成方式：

```bash
python3 project/MetaGPT/assets/generate_diagrams.py
```

只使用标准库。SVG 保留可搜索文字和辅助描述，使用本地系统中文字体，无远程资源。直接打开 SVG 可查看完整尺寸。
