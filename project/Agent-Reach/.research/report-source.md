# Agent-Reach 调研记录

> 本文件保存博客的复核基线、方法与关键证据，便于后续更新；对外阅读入口为 [`../README.md`](../README.md)。

## 研究基线

- 仓库：`https://github.com/Panniantong/Agent-Reach.git`
- 分支：`main`
- 提交：`da5044d26fc6adddb6554d5679c94ac22e76e428`
- 提交时间：2026-09-01T16:09:56+08:00
- 调研时间：2026-09-12（Asia/Shanghai）
- 项目元数据版本：`1.5.0`
- 最近 tag：`v1.5.0`（`f65526cbaaad3879473acc1ba6dbefd195caf2be`）

## 方法

1. 克隆官方仓库，记录 commit 与 tag。
2. 阅读产品代码、Skill、测试、CI、打包和提交历史。
3. 统计跟踪文件与 Python 物理行数。
4. 在隔离的 uv 环境解析全部 extras。
5. 运行 pytest、Ruff、mypy 与 MCP 构造 smoke test。
6. 对涉及的上游工具仅采用官方仓库/官方文档交叉验证。
7. 不以实时 Star 数、一次网络可达性或营销文案推断架构质量。

## 本地复核结果

```text
git rev-parse HEAD
da5044d26fc6adddb6554d5679c94ac22e76e428

git rev-list --count HEAD
375

tracked files
120

Python physical lines
agent_reach: 6,874
tests:       10,105
total:       16,979

pytest -q
586 passed, 16 subtests passed in 1.20s

ruff check agent_reach tests
All checks passed!

mypy agent_reach
agent_reach/integrations/mcp_server.py:43:
  "Server" has no attribute "list_tools"
agent_reach/integrations/mcp_server.py:46:
  Unexpected keyword argument "inputSchema" for "Tool"
agent_reach/integrations/mcp_server.py:51:
  "Server" has no attribute "call_tool"
Found 3 errors in 1 file

resolved optional dependency
mcp==2.2.0

MCP smoke test
from agent_reach.integrations.mcp_server import create_server
create_server()
AttributeError: 'Server' object has no attribute 'list_tools'
```

## 核心证据索引

| 结论 | 首要证据 |
|---|---|
| Agent-Reach 是控制面，不代理内容数据面 | `agent_reach/core.py`、`integrations/mcp_server.py`、2026-02-26 重构提交 |
| 15 个 Channel | `agent_reach/channels/__init__.py` |
| 有序 backend 与显式覆盖 | `agent_reach/channels/base.py` |
| Doctor 保守且隔离单平台错误 | `agent_reach/doctor.py` 与各 Channel `check` |
| OpenCLI probe 无副作用设计 | `agent_reach/backends/opencli.py` |
| 安装默认 safe | `agent_reach/cli.py` 中 `args.safe or not args.system` |
| 配置原子写入与路径安全 | `agent_reach/config.py`、`utils/paths.py` |
| Cookie 平台限制 | `agent_reach/cookie_extract.py` |
| URL 与 SSRF 防护 | `agent_reach/utils/url.py`、`transcribe.py` |
| 媒体预算与供应商回退授权 | `agent_reach/transcribe.py` |
| MCP 测试未验证真实 SDK | `tests/test_mcp_server.py`、`.github/workflows/pytest.yml` |
| PyPI 同名包冲突 | 固定快照 README 与 `https://pypi.org/project/agent-reach/` |

## 解释边界

- `doctor=ok` 表示通过该 Channel 当前实现的 probe，不是平台 SLA。
- `active_backend=null` 可能是未安装，也可能是为了避免副作用而未实时验证。
- 通用 Web Channel 的 `ok` 是本地零依赖声明，不包含 Jina 远端网络探测。
- MCP 问题描述的是本文日期下“当前快照 + 最新可解析 extra”，不外推到所有历史环境。
- URL 字面值过滤不等于 DNS/网络层 SSRF 防护。
- Skill 的只读规则是提示策略，不是操作系统级权限边界。
- 平台内容访问受账号、地区、条款、限流和上游版本影响。

## 更新清单

后续重跑本文时至少应更新：

- commit、tag、版本与 Python 支持范围；
- Registry 中 Channel 数与 backend 顺序；
- 全量测试、Ruff、mypy、真实 MCP smoke test；
- optional dependencies 的解析版本；
- README 与 PyPI 名称冲突状态；
- yt-dlp 的 YouTube JS runtime 要求；
- OpenCLI daemon/status contract；
- 图中的数字上限与平台矩阵。
