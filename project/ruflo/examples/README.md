# Ruflo 源码实验

这组实验直接调用固定提交 `6f0ed7112873eedc7cfe17281a2585188190b790` 的处理器和辅助函数，验证博客所述的真实行为。上游源码不复制到博客，也不作业务修改。

## 运行

需要 Git 和 Node.js 24+。无需安装 Ruflo 的全部 npm 依赖。`source-loader.mjs` 使用 Node 的实验性 TypeScript 转换与模块钩子，解析 `.js` 指向的 `.ts` 源文件，以及两个 CLI Core re-export 路径。

```bash
git clone https://github.com/ruvnet/ruflo.git /tmp/ruflo-source
git -C /tmp/ruflo-source checkout 6f0ed7112873eedc7cfe17281a2585188190b790

# 当前目录设为 project/ruflo
RUFLO_SOURCE=/tmp/ruflo-source node \
  --import ./examples/source-loader.mjs ./examples/probe.mjs
```

如需记录 JSON，可在脚本后增加一个**绝对路径**。脚本会切换到新建临时工作目录，防止覆盖真实项目的 Ruflo 状态。

## 实验边界

- 保留上游注册、执行、工作流与检索函数；不以自己的实现替代被研究对象。
- 覆盖 `fetch` 网络边界，使用固定模型响应；没有真实 API 调用，也不会消耗模型额度。
- 临时设置 `ANTHROPIC_API_KEY` 为无效 fixture 字符串，仅用于选中被测试分支；不读取或输出真实密钥。
- 直接调用处理器，绕过 MCP 协议及统一策略入口。因此不验证协议传输、MCP 授权或完整发布包安装。
- 默认保留 `/tmp/ruflo-probe-*` 中的实验状态，便于检查；不写真实项目的 `.claude-flow` 或 `.swarm`。
- `workflow_resume` 实验人为构造 paused 持久化状态，验证没有活动 runner 时的行为；不是 live runner 的暂停/恢复测试。
- BM25 样例验证局部评分与分词；消息签名样例验证密码辅助函数，均不代替系统级检索或分布式测试。

7 组实验涵盖注册与执行的区别、单次 Provider 请求、Workflow 支持类型、模板插值、恢复语义、BM25/中文分词、消息签名与生成的路由器（相关断言按 7 个实验对象分组）。完整结果见 [probe-results.json](../research/probe-results.json)。

部分上游模块在 import 时会打印 CLI 信息，所以标准输出不保证只有 JSON；传入结果文件路径可获得纯 JSON 文件。
