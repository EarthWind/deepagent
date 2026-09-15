# ECC 调研验证记录

## 1. 源码基线与环境

| 项目 | 值 |
| --- | --- |
| 官方仓库 | https://github.com/affaan-m/ECC |
| 固定提交 | `8321021c54d670126ce3b2969d5deb880b4b0c2a` |
| 提交时间 | `2026-09-12T07:45:40-04:00` |
| 提交主题 | `fix(memory): classify directory traversal failures` |
| 包 | `ecc-universal 2.2.1` |
| 调研日期 | 2026-09-15（Asia/Shanghai） |
| 执行环境 | Linux、Node `v24.18.0`、Python `3.14.4` |
| 源码工作目录 | `/tmp/ecc-research-source`，属于本次临时研究目录 |

网页浏览用于核对官方仓库和当前公开说明；具体实现判断来自固定 Git 提交。正文引用的 70 个不同文件，其路径、行数和 SHA-256 位于 [snapshot.json](snapshot.json)。这些哈希用于核对所读源码，不是供应链安全背书。

## 2. 安装了什么，执行了什么

运行依赖按上游 `package-lock.json` 安装，使用 `--ignore-scripts --omit=dev`；下载到临时源码目录，并使用临时 npm cache。没有向用户的日常 Agent 配置安装 ECC 插件。

```bash
npm ci --ignore-scripts --omit=dev --no-audit --no-fund \
  --cache /tmp/ecc-research-npm-cache --prefix /tmp/ecc-research-source
python3 project/ECC/research/run_upstream_checks.py /tmp/ecc-research-source
node project/ECC/examples/probe.cjs /tmp/ecc-research-source
```

环境沙箱最初阻止 npm 网络访问（`EPERM`），并使 Node `spawnSync` 报 `EPERM`。在获得执行权限后重跑。这个过程没有改变上游源码或放宽 ECC 产品中的安全配置。

## 3. 上游测试结果

**选定的 16 个测试文件全部退出 0，日志合计报告 260 个通过、0 个失败。** 这里的用例计数来自各测试自己的输出格式，执行器没有将它们统一改写为另一套测试框架。

| 测试文件（`tests/` 下） | 通过数 | 失败数 |
| --- | ---: | ---: |
| `hooks/hook-flags.test.js` | 63 | 0 |
| `hooks/bash-hook-dispatcher.test.js` | 6 | 0 |
| `hooks/posttooluse-dispatcher.test.js` | 14 | 0 |
| `hooks/run-with-flags-truncation.test.js` | 7 | 0 |
| `hooks/config-protection.test.js` | 9 | 0 |
| `hooks/session-end.test.js` | 7 | 0 |
| `hooks/pre-compact.test.js` | 9 | 0 |
| `hooks/observer-memory.test.js` | 32 | 0 |
| `lib/memory-vault.test.js` | 35 | 0 |
| `scripts/memory-mcp.test.js` | 14 | 0 |
| `scripts/instinct-cli-evolve.test.js` | 4 | 0 |
| `scripts/instinct-cli-evolve-generate.test.js` | 10 | 0 |
| `scripts/install-plan.test.js` | 11 | 0 |
| `lib/tmux-worktree-orchestrator.test.js` | 14 | 0 |
| `lib/eval-harness/gate.test.js` | 8 | 0 |
| `lib/eval-harness/receipt.test.js` | 17 | 0 |

每项的退出码、耗时和日志路径见 [test-results.json](test-results.json)；完整 stdout/stderr 位于 [logs](logs/)。计数口径示例：有些测试输出 `Passed: 7`，有些输出 `7 passed`，执行器同时支持这两种格式。

测试涵盖固定输入的开关、拦截、上下文注入、Vault 文件边界与 MCP 请求、聚类和产物生成、安装计划、编排辅助、评估执行拒绝和收据验证。MCP 测试包含启动本地 stdio 服务；编排测试使用 fixture 和测试替身，不代表启动真实 Agent 团队。

## 4. 五组源码实验

实验脚本：[probe.cjs](../examples/probe.cjs)，最终输出：[probe-results.json](probe-results.json)。

1. **Hook 开关**：默认 standard；`pre:config-protection` 在 standard/strict 的允许列表下，minimal 返回 false，strict 返回 true；总开关关闭返回 false。
2. **真实 Hook Runner**：对新建配置退出 0，对已存在 `eslint.config.js` 退出 2；关闭 Hook 后退出 0。
3. **Memory Vault**：创建 unreviewed 对象；拒绝同 kind、同 ID 的既有目标覆盖；拒绝模拟密钥；目标为 Claude 的记忆对 Codex 查询不可见；固定 query 的词法分数为 35。
4. **Instinct 聚类**：两个相关 trigger 加一个无关 trigger，英文组形成一个簇，对应纯中文组没有簇。
5. **Gate 执行边界**：传入一个不存在的配置文件，程序先返回 `gate.isolation_required`，退出 1。

实验开发期间修正了两处 fixture 假设：create-only 针对实际目标路径（kind 参与目录），而非假定 ID 存在全局唯一写入索引；`evolve` 至少需要三条经验才开始分析。最终实验保留符合源码契约的输入，不改变上游逻辑。

## 5. 文档与图像检查

- 生成 7 张原始 SVG，并嵌入独立 `index.html`；图像不依赖外部 CDN。
- 博客源码引用固定到同一 commit，本地引用路径与章节锚点做完整性检查。
- 用 headless Chrome 检查 1440 像素桌面视口与 390 像素窄屏视口；无页面横向溢出，17 个章节目标存在，7 个图像放大按钮及关闭操作正常。窄屏 DOM 检查使用 390 像素 iframe 视口，避免 Chrome 最小外部窗口宽度影响测量。
- SVG 使用中文系统字体，7 张图的全部文本经过浏览器边界检查，没有超出画布或所属卡片；另做了图像渲染目视检查。
- 原始检查结果见 [artifact-checks.json](artifact-checks.json)。

图像与网页的生成代码位于 [tools](../tools/)，不使用生成式绘图来决定技术图的箭头或文字内容。

## 6. 没有执行的范围

- 整个上游 `npm test`、ESLint、Markdownlint、覆盖率门槛。
- 真实 Claude/Codex 等宿主的端到端插件安装与全部事件行为。
- Observer 的真实模型调用、付费摘要或模型完成率/Token 节约对照。
- AgentShield 独立仓库的扫描和模型对抗流程。
- Rust `ecc2/` 构建与实机 daemon/多会话测试。
- Windows/macOS、网络文件系统、多租户和生产负载验证。

所以，本文结论支持“源码如何实现、所测局部机制表现如何”，不支持“ECC 在所有平台全功能可用”或“模型性能已经提升某个百分比”。
