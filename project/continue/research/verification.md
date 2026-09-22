# 调研与验证记录

调研日期：2026-09-23。源码提交：`5522c6f44ca0ac3528b37244818fbfa39b5af470`。

## 来源与方法

- 实际克隆官方仓库并读取源码，未将网页摘要当成全部证据。
- 交叉核对官方 README、Agent、CLI、YAML 和已弃用 Codebase 文档。
- 69 个关键源文件记录路径、入口行号、符号和完整 SHA-256，见 [sources.json](sources.json)。
- 将事实、局部实验观察、并发风险推断和建议分别标明。
- 上游源码没有复制进入本文目录；本地临时 checkout 不属于交付内容。

## 已执行的源码实验

Node.js 24.18.0；13 组实验通过，0 组失败。见 [probe-results.json](probe-results.json)。

实验运行原函数主体，以显式依赖注入隔离外部环境：Redux 替代 memoization 外壳，动态工具 evaluator 使用 fixture，token 计数使用 fixture。实验不启动模型、不连接 MCP、不运行终端命令、不修改测试项目文件，也不代表上游全量测试。

## 图文产物检查

结构检查与浏览器检查已执行，机器可读结果见 [artifact-checks.json](artifact-checks.json)、[browser-checks.json](browser-checks.json)。

| 检查 | 实际结果 |
| --- | --- |
| Markdown 本地链接与源码引用 | 无断链或未定义引用 |
| 章节与图像 | 20 个章节锚点，9 张 SVG，全部加载 |
| 桌面页面 | Chrome 152，1440 × 1100，无页面横向溢出 |
| 移动宽度页面 | Chrome 152，390 × 844，独立目录及局部滚动容器正常 |
| 配图文字边界 | 9 张 SVG 均无画布或卡片越界 |
| 离线资源 | 页面没有 HTTP(S) 运行资源请求 |

另外人工查看了桌面、移动宽度首页和全部 9 张配图截图。移动宽度检查使用桌面 Chrome 的视口模拟，不等价于真实 iOS / Android 设备测试。

## 明确未验证

没有安装或启动完整 Continue 扩展／CLI 产品；没有真实模型 API 和 MCP 服务集成、全量上游测试、跨平台终端测试、性能或成本评测。

文件审批期间覆盖风险、子 Agent 全局状态竞争等属于代码评审发现和推断，没有在真实工作区执行破坏性竞争复现。RAG、Autocomplete 和 Next Edit 也没有进行端到端质量评测。

## 重建

从 deepagent 仓库根目录执行：

```bash
# 准备固定 checkout，路径可自行选择。
git clone https://github.com/continuedev/continue.git /tmp/continue-research
git -C /tmp/continue-research checkout 5522c6f44ca0ac3528b37244818fbfa39b5af470

python3 project/continue/research/build_sources.py /tmp/continue-research
node project/continue/examples/source-probes.mjs /tmp/continue-research \
  > project/continue/research/probe-results.json
python3 project/continue/assets/generate_diagrams.py

# HTML 重建需要 markdown-it-py==3.0.0；已生成页面不需要 Python。
python3 project/continue/research/build_blog.py
python3 project/continue/research/verify_artifacts.py
```

浏览器检查使用系统 Chrome 的 CDP 接口，脚本不安装浏览器、不访问模型，也不启动 Continue。具体运行方式见 [browser_checks.mjs](browser_checks.mjs) 文件头说明。截图输出到临时目录，不进入正文。

直接打开 [index.html](../index.html) 即可离线阅读；移动端表格和大图在各自容器内横向滚动，点击图可独立查看原始 SVG。
