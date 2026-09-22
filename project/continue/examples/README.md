# 源码行为实验

这些实验直接读取固定提交的 TypeScript 函数，验证博客中容易误读的实现细节。不是自建 Agent 的性能演示，也不是 Continue 全量集成测试。

```bash
git clone https://github.com/continuedev/continue.git /tmp/continue-research
git -C /tmp/continue-research checkout 5522c6f44ca0ac3528b37244818fbfa39b5af470
node project/continue/examples/source-probes.mjs /tmp/continue-research
```

从 deepagent 仓库根目录运行。实验需要 Node.js 22.13+（使用内置 TypeScript 转换）；本次使用 Node.js 24.18.0。**这是实验工具要求，Continue 源码的 `.nvmrc` 为 20.20.1。**无需安装 Continue 依赖、配置 API Key、下载模型或执行 Shell 工具。

脚本先校验 [源码清单](../research/sources.json) 中的文件 SHA-256，然后删除模块 import、转换 TypeScript 语法，将明确列出的依赖注入原函数。函数主体没有重写。Redux 只替代 memoization 外壳；CLI 动态策略注入了测试工具；压缩实验使用可控 token 计数，只验证阈值公式，不验证 tokenizer 精度。字符串编辑实验不读写项目文件。

13 组实验覆盖：IDE 模式过滤、显式排除、工作区访问、宽松字符串匹配、多匹配拒绝、顺序多编辑、CLI 首匹配权限、Plan 边界、动态权限优先级、压缩阈值、尾部裁剪、摘要后的历史视图、MCP 名称碰撞。

已执行结果：[probe-results.json](../research/probe-results.json)。每项结果均标注观察范围；通过实验不代表产品全链路已验证。
