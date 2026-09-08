# Claim-to-source ledger

| Claim family | Primary source | Publisher / author | Date / version | URL | Access note | Confidence |
|---|---|---|---|---|---|---|
| 项目目标、角色分工、研究用途声明 | TradingAgents README | Tauric Research | commit `be952b8` | https://github.com/TauricResearch/TradingAgents/tree/be952b8eccb49720509af544c6675233bc1f10d0 | cloned and read | High |
| 论文组织结构、通信协议、实验设计与结果 | TradingAgents: Multi-Agents LLM Financial Trading Framework | Yijia Xiao, Edward Sun, Di Luo, Wei Wang | arXiv v7, 2025-06-03 | https://arxiv.org/pdf/2412.20138 | web PDF, 38 pages | High for reported claims; Medium for generalization |
| 当前 graph 节点、边、串行分析师、模型分配 | `tradingagents/graph/setup.py` | Tauric Research | commit `be952b8` | https://github.com/TauricResearch/TradingAgents/blob/be952b8eccb49720509af544c6675233bc1f10d0/tradingagents/graph/setup.py | cloned and line-read | High |
| 当前共享状态契约 | `agent_states.py` | Tauric Research | commit `be952b8` | https://github.com/TauricResearch/TradingAgents/blob/be952b8eccb49720509af544c6675233bc1f10d0/tradingagents/agents/utils/agent_states.py | cloned and line-read | High |
| 主运行、memory、checkpoint、输出 signal | `trading_graph.py` | Tauric Research | commit `be952b8` | https://github.com/TauricResearch/TradingAgents/blob/be952b8eccb49720509af544c6675233bc1f10d0/tradingagents/graph/trading_graph.py | cloned and line-read | High |
| 条件循环与辩论轮数公式 | `conditional_logic.py` | Tauric Research | commit `be952b8` | https://github.com/TauricResearch/TradingAgents/blob/be952b8eccb49720509af544c6675233bc1f10d0/tradingagents/graph/conditional_logic.py | cloned and line-read | High |
| 结构化决策 schema 与 fallback | `schemas.py`, `structured.py` | Tauric Research | commit `be952b8` | https://github.com/TauricResearch/TradingAgents/tree/be952b8eccb49720509af544c6675233bc1f10d0/tradingagents/agents | cloned and line-read | High |
| Vendor routing 与失败语义 | `interface.py`, `errors.py` | Tauric Research | commit `be952b8` | https://github.com/TauricResearch/TradingAgents/tree/be952b8eccb49720509af544c6675233bc1f10d0/tradingagents/dataflows | cloned and line-read | High |
| Point-in-time 与防泄漏修复是持续演进 | CHANGELOG and dataflow implementation | Tauric Research | v0.3.1–main | https://github.com/TauricResearch/TradingAgents/blob/be952b8eccb49720509af544c6675233bc1f10d0/CHANGELOG.md | cloned and web-read | High |
| Checkpointer/thread 官方语义 | LangGraph Persistence | LangChain | accessed 2026-09-08 | https://docs.langchain.com/oss/python/langgraph/persistence | official docs | High |
| StateGraph/edge/reducer/Send 官方语义 | LangGraph Graph API | LangChain | accessed 2026-09-08 | https://docs.langchain.com/oss/python/langgraph/graph-api | official docs | High |
| CLI 未走完整 decision-log 生命周期 | `cli/main.py` compared with `trading_graph.py` | Tauric Research; analysis inference | commit `be952b8` | https://github.com/TauricResearch/TradingAgents/blob/be952b8eccb49720509af544c6675233bc1f10d0/cli/main.py#L1004-L1299 | negative-path static analysis | High |
| 当前代码不含 broker/ledger/execution path | repository-wide search; `_run_graph` terminal return | Tauric Research; analysis inference | commit `be952b8` | https://github.com/TauricResearch/TradingAgents/blob/be952b8eccb49720509af544c6675233bc1f10d0/tradingagents/graph/trading_graph.py#L509-L574 | no Backtrader import or order API in non-test Python | High |

## Searches performed

- Official GitHub repository, releases, pinned source files and changelog.
- Official arXiv paper, with targeted reads for framework, communication, experiments, table values and authors' Sharpe caveat.
- Targeted paper searches for transaction cost, commission, initial capital, ablation, seed, statistical, frequency and limitations.
- Official LangGraph Graph API, tool and persistence documentation.
- Repository-wide searches for memory lifecycle, broker/execution/portfolio state, tests and CI.
