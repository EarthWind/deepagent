# 调研与验证记录

## 基线与方法

- 日期：2026-09-16（Asia/Shanghai）。
- 仓库：<https://github.com/code-yeongyu/oh-my-openagent.git>。
- 本次浅克隆的分支：`dev`。
- 提交：`bee849b228d1cb076a8f2ac839335f43399febe1`。
- 提交信息：`Merge pull request #8388 from code-yeongyu/fix/8328-ulw-loop-projection`。
- 提交时间：`2026-09-16T23:46:32+09:00`，折合北京时间为当日 22:46:32。
- 根 package：`oh-my-opencode@5.0.0-beta.67`；Native：`omo-ai@5.0.0-0.beta.67`。

先访问官方 GitHub 页面确认当前形态，再克隆固定源代码，沿注册链阅读实现。Web 首页可能在调研过程中继续变化，正文证据链接全部使用固定提交路径。

## 已完成的源码验证

直接运行以下命令，退出码为 0，10 组实验全部通过：

```bash
node --experimental-transform-types project/oh-my-openagent/examples/source-probes.mjs /tmp/oh-my-openagent-research
```

本机 Node 为 `v24.18.0`。结果 JSON 根据这次实际 stdout 保存到 [probe-results.json](probe-results.json)；仅调整了排版，没有把未执行的结果补成通过。源码实验范围和复现方式见 [examples/README.md](../examples/README.md)。

首次调用时，受限环境阻止了 Node 启动 Git 子进程，报 `spawnSync git EPERM`；获准在沙盒外执行后继续。另一次预检查发现克隆中的一份 `.omo/evidence/.../transcript-ansi.txt` 历史证据文件被 Git 报为已修改；该文件不参与任何实验，也没有被本次工具改写或恢复。随后将干净状态检查限定到实际测试的五个源码目录，检查通过。没有把这些预检查失败算作行为测试失败或忽略行为断言。

### 各结论的证据等级

| 结论 | 证据 |
| --- | --- |
| 三种产品入口、共享包分层 | 包清单、真实导出和宿主接线 |
| 10 个工厂角色与额外 Prometheus 装配 | `builtin-agents.ts` 与 `agent-config-assembly.ts` |
| 模型配额覆盖使用独立键 | 源码 + 直接执行实验 |
| 旧 attempt 不覆盖新 Task 投影 | 源码 + 直接执行实验 |
| DAG 拒绝坏图、计算 waves | 源码 + 编译器实验 |
| DAG 按依赖前沿而非整批屏障推进 | `scheduler.ts` 阅读，未运行完整调度器 |
| DAG 的公开工具名为 workflow | 工具常量、描述和注册点 |
| Hashline 新旧锚点与短哈希碰撞 | 源码 + 字符串核心实验 |
| 词法搜索与查询规划语义 | 源码 + 内存数据集实验 |
| Git 反思合并、记忆绑定和关闭协调 | 源码阅读，未调用反思模型 |
| 多 Agent 收益、成本和长期记忆效果 | 仅提出评测方法，没有实测结论 |

## 文档与图示构建

```bash
python3 project/oh-my-openagent/research/capture_snapshot.py /tmp/oh-my-openagent-research
python3 project/oh-my-openagent/build_blog.py
python3 project/oh-my-openagent/research/validate_artifacts.py
```

`capture_snapshot.py` 生成 69 个源码证据文件的指纹、固定提交链接与索引；`build_blog.py` 用本地 Python 生成 8 张原创 SVG、补全 Markdown 引用并构建静态 HTML。构建 HTML 依赖 `markdown-it-py`；当前环境已存在，无需安装。换环境时可在独立 Python 环境安装该依赖。

HTML 不引用外部脚本、字体或图像 CDN，可直接通过 `file://` 打开；源码链接需要网络。SVG 有标题与描述，正文图片有中文替代文本；移动端表格和代码可横向滚动，目录可折叠。

图中的关系根据源码重绘，DAG 时间轴是明确标注的假设算例。没有使用生成式模型绘制源码细节，也没有把概念图伪装成运行截图。

### 已完成的产物检查

- Markdown 引用定义、相对文件链接、显式章节锚点及 HTML 本地资源检查通过，结果见 [artifact-validation.json](artifact-validation.json)。远程链接只解析并固定提交，没有声称逐个发起 HTTP 可达性检测。
- 8 张 SVG 均可被 XML 解析，包含标题与描述。
- 使用本机 Headless Chrome 实际渲染 8 张图，通过 `getBBox()` 检查 225 个文字节点，未发现超出 SVG 画布边界的文字，见 [svg-render-validation.json](svg-render-validation.json)。这一自动检查针对画布边界；另外通过图示合览人工查看布局，并修正了英文单词中间换行等问题。
- 查看了桌面 `1500×1150` 和手机 `412×915` 的真实页面截图：标题、目录、正文和图片正常渲染；手机端目录可折叠，图可点击单独打开。首屏截图检查不等同于对全部浏览器和交互做端到端自动测试。
- `git diff --check` 通过；新目录的文本文件另做了行尾空白检查。工作区原有的 `project/claude-code/interactive-report/` 未被修改。

浏览器首次执行图示 DOM 导出时也遇到沙盒 socket 限制；在获准的沙盒外运行中完成了上述检查。页面未引入网络渲染依赖。

## 未执行的验证

- 未安装完整 Bun 工具链和上游全部依赖，未运行上游全量测试或 typecheck。
- 未安装或更改本机 OpenCode、Codex、Senpi、MCP 和模型提供商配置。
- 未启动真实模型子任务、团队或 workflow，未验证完整宿主升级矩阵。
- 未执行跨进程崩溃恢复、网络故障、完整邮箱压力或文件副作用幂等测试。
- 未测量成本、任务成功率、延迟、长期记忆增益或 telemetry 实际出站内容。

上述限制在正文相应位置说明；本次结果是固定提交源码研究与局部机制验证。
