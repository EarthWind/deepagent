# 研究与验证记录

- 研究日期：2026-09-14，Asia/Shanghai。
- 来源：[HKUDS/nanobot](https://github.com/HKUDS/nanobot)。
- 固定提交：`499bf903022f429dd4501fdfbeeccadcb99dd51f`。
- `pyproject.toml` 声明 `nanobot-ai 0.3.0`，不是对 PyPI 发布文件一致性的声明。
- 源码 checkout 在 `/tmp/nanobot-research-20260914`；没有将完整第三方源码复制进博客目录。
- 使用 Python 3.13.14，依赖安装到 `/tmp/nanobot-research-env`，不修改用户全局 Python。
- 未修改上游源码，未配置真实 provider、启动个人消息通道或运行真实模型任务。

## 1. 源码与统计复现

在本仓库根目录运行：

```bash
python3 project/nanobot/research/source_inventory.py /tmp/nanobot-research-20260914
```

已记录的 [source-inventory.json](source-inventory.json) 包含 commit、提交时间、包版本、代码统计口径及关键文件 SHA-256。统计的物理行数包含注释与空行，不代表有效代码行数，也不用于估计运行时内存或性能。

## 2. 上游测试

安装上游 `project.dependencies` 与 pytest、pytest-asyncio、aiohttp 后，在固定 checkout 根目录运行：

```bash
PYTHONPATH=/tmp/nanobot-research-20260914 \
TIKTOKEN_CACHE_DIR=/tmp/nanobot-tiktoken-cache \
/tmp/nanobot-research-env/bin/python -m pytest \
  tests/agent/test_runner_core.py \
  tests/agent/test_runner_tool_execution.py \
  tests/agent/test_context_governance.py \
  tests/agent/test_memory_store.py \
  tests/agent/test_dream_tools.py \
  tests/agent/test_session_atomic.py \
  tests/agent/test_runner_goal_continue.py \
  tests/security/test_workspace_policy.py \
  -q --tb=short
```

最终结果：**128 passed in 4.49s**。原始输出见 [upstream-tests.txt](upstream-tests.txt)，依赖版本见 [requirements-tested.txt](requirements-tested.txt)。这些是本次环境解析的版本，不是上游提供的 lockfile；其他系统与依赖组合的结果可能不同。

首次在沙盒内运行得到 127 passed、1 failed。`TestDreamCursor.test_git_restore_rolls_back_dream_cursor` 的失败原因是沙盒在 `/tmp/.git` 注入保护目录，GitStore 据此拒绝在子目录初始化 Git；在沙盒外重跑完整同组测试后通过，没有跳过或改写测试。

## 3. 博客示例

```bash
PYTHONPATH=/tmp/nanobot-research-20260914 \
  /tmp/nanobot-research-env/bin/python project/nanobot/examples/runner_demo.py
```

通过全部内置断言，实际输出保存为 [runner-demo-output.json](runner-demo-output.json)。三轮脚本模型响应中，真实工具只执行一次。模型选择、错误纠正与 usage 为人为设定，不能当作真实 LLM 能力或成本数据。

## 4. 文档与图示

图示由 [render_diagrams.py](render_diagrams.py) 使用 Python 标准库生成，SVG 自包含字体回退、标题和说明，不含外部图片依赖。

文档检查由 [validate_artifacts.py](validate_artifacts.py) 完成，输出见 [artifact-checks.json](artifact-checks.json)：检查本地链接、显式目录锚点、固定提交链接所对应的源码文件与行号、SVG XML 结构和示例语法。

Chrome 对七张 SVG 进行了渲染；使用浏览器 `getBBox()` 测量文字相对于画布和卡片的边界，并人工检查了浏览器生成的图示总览。布局测量结果见 [diagram-layout-checks.json](diagram-layout-checks.json)。截图只用于验证，博客直接引用可缩放的 SVG 原图。

## 5. 本次没有验证的内容

- 真实模型的输出效果、供应商 API 的实时行为、缓存收益与费用。
- 外部聊天平台认证、消息接收、限流和实际交付。
- 全量上游测试、前端构建、原生 TUI 或跨平台兼容性。
- 负载、长时间运行、跨进程恢复、断电持久性与副作用幂等。
- 完整安全审计或漏洞利用测试。

文章中关于多租户隔离、幂等、预算和生产部署的内容属于基于实现的工程判断与建议。
