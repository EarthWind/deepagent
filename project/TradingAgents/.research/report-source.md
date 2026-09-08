# TradingAgents 源码调研：内部规范稿

## 元信息

- 日期：2026-09-08
- 受众：熟悉 Python、LLM Agent 或 LangGraph 的工程师与技术负责人
- 交付：`../README.md` 中文技术博客与 `../assets/*.svg` 原创配图
- 源码范围：TauricResearch/TradingAgents `main` @ `be952b8eccb49720509af544c6675233bc1f10d0`
- 论文范围：arXiv 2412.20138v7（2025-06-03）
- 排除项：不提供投资建议；不以未运行的在线行情或 LLM 输出评价个股；不把论文回测当作本地复现结果

## 直接结论

TradingAgents 当前开源实现是以 LangGraph StateGraph 编排的单标的投研决策与报告流水线。它的主要工程贡献是显式共享状态、分析师工具循环、有限轮对抗辩论、关键裁决结构化输出、数据 vendor 契约、point-in-time 防线、运行 checkpoint 和延迟 outcome reflection。它不包含完整的 broker/OMS、现金和持仓账本、确定性组合风控或可一键复现论文结果的回测执行器，因此不应描述为开箱即用的全自动交易系统。

## 关键分析

1. `GraphSetup` 将四类分析师、Bull/Bear、Research Manager、Trader、三类风险角色和 Portfolio Manager 放入一张 StateGraph。
2. 当前四类分析师按选择顺序串行；论文 Figure 1 描述为并发。这是设计/实现差异。
3. 当前只有 Research Manager 与 Portfolio Manager 使用 Deep LLM；其他角色使用 Quick LLM。论文第 4.3 节对模型分配的描述不同。
4. `AgentState` 用独立 report 字段完成跨团队交接，消息只作为分析师局部工具循环的 scratchpad。
5. Market/News/Fundamentals 使用 Agent→ToolNode→Agent 循环；Sentiment 直接预取三类来源再结构化生成，常规路径不进入其已注册 ToolNode。
6. Pydantic 结构化输出覆盖 SentimentReport、ResearchPlan、TraderProposal、PortfolioDecision，失败后回退自由文本。
7. 数据层用显式 vendor chain、类型化错误、日期窗、stale guard、symbol normalization 和 verified snapshot 把事实边界放在模型外。
8. Checkpoint 与 decision log 是两种不同持久化：前者恢复同一次图运行，后者在未来 Run 中注入已结算经验。
9. Python `propagate()` 走完整 decision-log 生命周期；CLI 直接 stream 图，当前控制流未调用 pending 结算、past_context 注入和 store_decision。此项是源码控制流推断。
10. 论文报告 AAPL/GOOGL/AMZN 三个月回测收益与 Sharpe 显著领先简单规则基线，但样本短、未报告多 seed/统计显著性/消融/完整交易成本，且仓库没有复现 harness。

## 局限与分歧

- 官方最新正式 tag 为 v0.4.0，但调研时 `main` 已合并 v0.4.1/v0.4.2 分支提交，包版本仍是 0.4.0。因此所有代码结论固定到 commit，而非笼统称“v0.4.2”。
- 论文关于并行分析师、LLM 分配和模拟执行的描述与当前开源代码存在差异；博客并列呈现，不用一方覆盖另一方。
- 未安装项目依赖，无法在本地运行 pytest 或需要 API key 的端到端分析；只执行 Python 语法编译和静态源码核对。不能声称本地测试套件通过。
- 论文 PDF 中未检索到 transaction cost、commission、ablation、seed、statistical 等详细设置；博客将其列为证据缺口，而不是断言一定没有任何隐含实验设置。

## 建议

生产化优先建设统一 Runner、typed Evidence、并行分析、确定性风险门、独立 OMS/账本和冻结数据的 walk-forward 评测，不优先增加更多角色。

## 停止条件

已覆盖官方论文、固定 commit 源码、变更日志和 LangGraph 官方文档；关键实现结论都有一手来源；论文/代码差异和无法本地完整验证的部分均已披露。继续搜索较难改变核心结论，停止广泛检索并进入交付校验。
