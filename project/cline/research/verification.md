# 验证范围与复现

调研日期：2026-09-22。固定提交 `4a56a43f39c2c75f941220989d4c65db006ee531`；已通过官方仓库 `git ls-remote` 核对当次 main HEAD。后续 main 变化不会改变正文链接。

## 已实际验证

- **48 个证据源文件**：哈希、关键符号、行号及内容与固定 Git 提交一致，见 [sources.json](sources.json) 与 [source-map.md](source-map.md)。
- **13 组离线源码实验通过**：Node v24.18.0，实际加载上游 AgentRuntime、VS Code policies、Plan guard 和文件 editor。使用脚本化模型及明确的依赖替身，见 [runtime-results.json](runtime-results.json) 和 [实验边界说明](../examples/README.md)。
- **文档工件检查**：Markdown / HTML 的本地链接与锚点、图像引用、SVG XML、示例语法、报告及源码哈希对应关系，机器结果见 [artifact-checks.json](artifact-checks.json)。
- **图形和页面检查**：Chrome 实际渲染原创 SVG 与离线页面；文字边界检查见 [diagram-checks.json](diagram-checks.json)，页面检查见 [page-checks.json](page-checks.json)。

实验第一次在执行器测试中使用了旧式字段，按当前源码 `old_text` / `new_text` 修正后，全部通过。Node 的子进程校验受到环境沙箱限制，完整实验使用已获批准的沙箱外运行；没有真实模型请求。输出中的 TypeScript stripping experimental warning 属于 Node API 提示。

## 未执行的验证

- 未安装整个上游 monorepo；环境没有 Bun，未运行上游全量 Vitest、VS Code 扩展启动、打包或完整 E2E。
- 未连接真实模型 API、MCP server、Hub、插件子进程或 CLI/桌面会话；也未测模型完成质量、真实 token 成本与延迟。
- 未在实际仓库运行 checkpoint 创建 / 恢复；相关结论来自固定源码审查。
- `sdk-agent.mjs` 仅语法与接口审查，未验证 npm 该版本发布、安装和执行。源码隔离实验不等价于公开包集成测试。
- SVG 与博客的阅读检查不能验证文章中所有工程建议的生产效果。

## 重建命令

在本仓库根目录执行。`/tmp/cline-research` 须是正文指定提交；Python 构建 HTML 需要 `markdown-it-py==3.0.0`，源码地图、SVG 生成只需标准库。阅读成品无需任何依赖。

```bash
python3 project/cline/research/build_sources.py /tmp/cline-research
python3 project/cline/assets/generate_diagrams.py
python3 project/cline/research/build_blog.py
node project/cline/examples/runtime-lab.mjs /tmp/cline-research \
  project/cline/research/runtime-results.json
python3 project/cline/research/verify_artifacts.py
```

浏览器检查工件生成到临时目录；页面内置 SVG 文字边界测量。使用 Chrome DevTools Protocol 明确设置 1440 和 390 像素视口，避免 Chrome 将窄窗口自动放大到 500 像素。截图与临时浏览器配置保留在该临时目录，不进入博客。

```bash
python3 project/cline/research/prepare_visual_checks.py /tmp/cline-visual
node project/cline/research/run_browser_checks.mjs /tmp/cline-visual
python3 project/cline/research/collect_visual_checks.py /tmp/cline-visual
python3 project/cline/research/verify_artifacts.py
```

浏览器脚本要求可启动本地 `google-chrome` 并连接其 localhost 调试端口；它只打开本地生成页，不访问 Cline 服务。

## 主要版本差异

1. 当前扩展的 Controller 使用 SDK 适配层，不能以旧 Task 类解释默认主循环。
2. 当前 VS Code local 后端、不暴露完成工具、禁用 spawn-agent / teams，均由实际装配代码确认。
3. 官方检查点页面保留 shadow Git / 每工具快照描述；当前内建 SDK 路径是新用户轮次前的项目 Git 私有 refs。文章明确两者差异，没有据文档推翻源码。
4. 底层工具策略默认允许；VS Code 通过 callback 落实当前自动批准配置；两者不能互相替代。
