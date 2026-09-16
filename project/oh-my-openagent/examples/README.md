# 直接调用上游源码的机制实验

这些实验用于支持博客中的具体实现结论，不构建一个相似的模拟 Agent，也不启动真实模型会话。

## 环境与基线

- 实测运行时：Node `v24.18.0`。
- 上游提交：`bee849b228d1cb076a8f2ac839335f43399febe1`。
- 无 npm 安装步骤；使用 Node 内建断言和 TypeScript 转换。
- 不安装插件，不改写用户的 OpenCode / Codex / OMO 配置，不访问模型 API。

## 复现

在本仓库根目录执行；克隆目录可自行替换：

```bash
git clone https://github.com/code-yeongyu/oh-my-openagent.git /tmp/omo-source-study
git -C /tmp/omo-source-study checkout --detach bee849b228d1cb076a8f2ac839335f43399febe1
node --experimental-transform-types project/oh-my-openagent/examples/source-probes.mjs /tmp/omo-source-study
```

选择完整克隆是为了让固定提交可获取；后续仓库 HEAD 已变更时，浅克隆未必包含该提交。脚本会验证 HEAD 和所测源码目录的干净状态，版本不符直接失败。

成功时输出 JSON，包含 `passed: 10`。需要保存自己运行的记录时，可以重定向到自己的结果文件：

```bash
node --experimental-transform-types project/oh-my-openagent/examples/source-probes.mjs /tmp/omo-source-study > /tmp/omo-probe-results.json
```

Node 可能在 stderr 输出实验性 TypeScript 转换警告。这不影响 stdout 中的 JSON 结果。旧版 Node 未必支持所需的 `registerHooks` 与类型转换能力，应使用本次已验证的运行时或兼容版本。

## 运行方式的边界

`source-probes.mjs` 直接从上游 checkout 导入：

| 模块 | 覆盖行为 |
| --- | --- |
| `background-agent/concurrency.ts` | 配额键、队列交接、取消、0 与默认值 |
| `background-agent/attempt-lifecycle.ts` | 新旧 attempt 的状态投影 |
| `senpi-task/src/dag/graph.ts` | 合法 DAG 编译与坏图拒绝 |
| `hashline-core/src/*` | 锚点格式、核心编辑、陈旧引用与碰撞 |
| `memory-core/src/search/*` | 词法 AND、短语和隐藏会话过滤 |
| `memory-core/src/recall/planner.ts` | 确定性、Unicode 与工具文本查询 |

相对路径解析 Hook 仅为实验补齐上游 TypeScript 的无扩展名导入，不替换任何被测函数。测试不经过官方 Bun 构建与包解析路径，因此不证明发行包构建正确、所有宿主适配正确，或真实模型能完成任务。

特别注意，DAG 实验运行的是**编译器**，没有运行完整 scheduler；依赖前沿调度的结论来自源码检查。Hashline 实验运行的是**字符串编辑核心**，不验证真实文件系统写入原子性。记忆实验运行的是**检索和查询规划**，不验证后台模型反思质量。

本次保留的输出：[probe-results.json](../research/probe-results.json)。
