# 插图说明

本目录的七张 SVG 是根据调研 commit `1e83e89` 手工设计、由 Python 标准库生成的原创工程示意图。它们不依赖外部图片、JavaScript、CDN 或 Mermaid 渲染器，GitHub 和普通浏览器均可查看。

| 文件 | 说明 |
| --- | --- |
| [architecture.svg](architecture.svg) | 客户端、Agent、Provider、Extension、状态边界 |
| [turn-lifecycle.svg](turn-lifecycle.svg) | 传统 loop 的一次工具往返与持久化位置 |
| [state-machine.svg](state-machine.svg) | 每步重载会话的 Operation / Effect 状态机 |
| [mcp-codemode.svg](mcp-codemode.svg) | 普通调用与 Code Mode 内部 callback 路径 |
| [context-memory.svg](context-memory.svg) | 用户历史、模型窗口与多种记忆机制 |
| [security-boundaries.svg](security-boundaries.svg) | 审批、检查器、间接调用和 OS 执行边界 |
| [subagent-recipes.svg](subagent-recipes.svg) | Recipe、Summon 与父子会话关系 |

从仓库根目录重新生成：

```bash
python3 project/goose/scripts/render_diagrams.py
```

布局与文字源文件位于 [render_diagrams.py](../scripts/render_diagrams.py)，可直接修改后重绘。优先字体是 Noto Sans CJK SC，缺失时回退到系统中文字体。所有图均附带 SVG title/description；图下的“边界提醒”是正文结论的简写。
