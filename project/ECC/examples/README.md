# 直接调用 ECC 源码的五组实验

这些实验是博客配套原创代码，调用固定提交中的真实模块。它们用于解释实现，不是一个仿写的 ECC，也不是模型性能基准。

## 准备

需要 Node.js、Python 3、Git。本次使用 Node `v24.18.0`、Python `3.14.4`、Linux。首先在自己的研究目录准备上游源码：

```bash
git clone https://github.com/affaan-m/ECC.git ecc-source
git -C ecc-source checkout 8321021c54d670126ce3b2969d5deb880b4b0c2a
```

然后从 deepagent 仓库根目录运行：

```bash
node project/ECC/examples/probe.cjs /absolute/path/to/ecc-source
```

脚本会检查 commit，并在操作系统临时目录中创建独立 fixture；退出时删除该 fixture。不会安装插件、修改日常 Agent 配置或调用真实模型。

## 实验对应关系

| 实验 | 上游实现 | 检查内容 |
| --- | --- | --- |
| Hook 开关 | `scripts/lib/hook-flags.js` | 默认档位、允许档位、总开关 |
| Hook 拦截 | `run-with-flags.js` + `config-protection.js` | 新建配置允许，已有配置拒绝；关闭 Hook 后允许 |
| Memory Vault | `scripts/lib/memory-vault.js` | unreviewed、同路径拒绝覆盖、模拟密钥拒绝、目标宿主过滤、词法分数 |
| Instinct 演化 | `instinct-cli.py evolve` | 三条英文 / 三条纯中文经验的聚类差异 |
| Eval Gate | `scripts/eval-harness.js gate run` | 在读配置前返回 `gate.isolation_required` |

Memory 示例的 `retry` 分数为 35：标题完整 query 命中 20，标题 token 命中 8，tag 命中 6，正文出现 1 次。模拟密钥是脚本即时生成的假数据，不是真实凭证，也不会出现在结果日志中。

Instinct CLI 要求至少三条经验才运行分析，因此两组都使用两条相关经验加一条不相关经验。中文零簇反映当前 `[a-z0-9]+` 分词器的边界。

结果：[probe-results.json](../research/probe-results.json)。

## 复现上游选定测试

选定测试包含 MCP 等模块，需要按锁文件安装上游生产依赖：

```bash
npm ci --prefix /absolute/path/to/ecc-source --ignore-scripts --omit=dev
python3 project/ECC/research/run_upstream_checks.py /absolute/path/to/ecc-source \
  --output /tmp/ecc-reproduced-checks
```

执行器按顺序运行 16 个测试文件，保留 stdout/stderr、退出码和耗时，单文件超时上限 180 秒。测试使用上游自己的 fixture；不会运行整个 `npm test`。输出范围和局限见 [验证记录](../research/verification.md)。

若受限环境禁止 Node 创建子进程，需要获得相应执行权限；不要把环境的 `spawnSync EPERM` 误判成 ECC 逻辑失败。

## 重新生成配图和网页

配图脚本仅使用 Python 标准库；网页生成需要 `markdown-it-py`（本次环境已提供）。已生成的 HTML 阅读时不需要 Python、Node 或网络。

```bash
python3 project/ECC/tools/build_assets.py
python3 project/ECC/tools/build_html.py
```
