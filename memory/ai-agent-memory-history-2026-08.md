# AI Agent Memory 发展史与论文清单（截至 2026-08-16）

> 调研日期：2026-08-16（Asia/Shanghai）
>
> 口径：以论文首次公开时间（通常为 arXiv v1）排序；覆盖截至当日可核实的论文，因此不包含 2026-08-17 至 2026-08-31 可能出现的工作。
>
> 范围：重点讨论 Foundation Model / LLM Agent 在运行期形成、维护和使用记忆的机制。清单是高覆盖的代表性文献表，不宣称穷尽所有含有 “memory” 关键词的论文。

## 1. 先给结论

AI Agent Memory 的发展并不是单纯把上下文窗口做长，而是把智能体从“每次调用都重新开始的生成器”变成一个有状态、能积累经验并能持续适应的系统。其主线可概括为：

1. **认知模型奠基（1968—1990s）**：人类记忆被区分为感觉/短期/长期、情景/语义、工作记忆等子系统，后来成为 Agent 记忆类型设计的主要隐喻。
2. **可微外部记忆（2014—2017）**：Memory Networks、Neural Turing Machine、DNC 等让神经网络能够学习“读/写”外部存储；Neural Episodic Control 展示了直接复用经验对快速学习的价值。
3. **长上下文与非参数检索（2019—2022）**：Transformer-XL、kNN-LM、RAG、RETRO、Memorizing Transformers 证明参数之外的检索记忆能够扩展知识和上下文，但它们大多还是“静态语料库 + 查询”。
4. **LLM Agent 记忆成形（2023）**：Reflexion 把失败反思存入情景记忆，Generative Agents 建立“观察—检索—反思—规划”循环，Voyager 把成功行为编译为技能，MemGPT 把上下文管理抽象成虚拟内存。记忆由“模型组件”变为“Agent 控制循环”。
5. **结构化与可评测化（2024）**：图、树、层次化摘要和认知启发式记忆快速发展；LoCoMo、LongMemEval 开始测多会话、时间推理、信息更新和拒答，而不只是针尖检索。
6. **系统化与自进化（2025）**：A-MEM、Zep、Mem0、MemoryOS、MemOS、MIRIX 等把形成、更新、合并、遗忘、检索做成完整生命周期；MEM1、MemAgent、Memory-R1、Memento、ReasoningBank 开始学习记忆管理或将经验压缩为可迁移策略。
7. **记忆策略学习与工程科学（2026）**：AgeMem、MemRL、SelfMem、MemCon 等把“何时写、写什么、何时取、何时删”视作可训练策略；评测扩展到环境经验、视觉世界状态、未来意图（prospective memory）、成本/延迟和文件系统长期健康度。

截至 2026-08，领域的核心问题已从“能否存取历史”转成：

- 能否把历史压缩成**事实、经验、策略和技能**，并保留出处与时间；
- 能否在信息变化时**更新、消歧、合并和遗忘**；
- 能否让 Agent 自己决定**何时、为何、以何种粒度**操作记忆；
- 检索到的记忆能否真正改善**推理和行动**，而非只提高静态问答分数；
- 能否同时满足**正确性、延迟、成本、隐私、安全和可审计性**。

## 2. 什么算 Agent Memory

本文采用一个操作性定义：

> **Agent Memory 是由智能体与用户或环境的历史交互所形成、可跨时间保留，并在未来感知—推理—行动循环中被选择性更新和使用的状态。**

一个完整记忆系统至少包含如下闭环：

```text
交互/观察 → 选择与编码（write） → 组织与演化（manage）
          → 查询与召回（read） → 推理/行动 → 新反馈
```

需要区分三个相邻概念：

- **长上下文不是长期记忆**：长上下文只是一次调用可看到更多 token；它通常缺少跨会话持久化、更新、遗忘和主动控制。
- **RAG 不天然等于 Agent Memory**：对静态文档库做检索是 RAG；当知识来自 Agent 自己的交互、会持续变化，并由 Agent 的控制循环读写时，才进入 Agent Memory 范畴。
- **上下文工程不等于记忆**：上下文工程负责构造当前输入；记忆还必须解释状态从何而来、如何长期维护，以及如何影响之后的行为。

## 3. 一个实用的统一分类

### 3.1 按“载体”分类

| 载体 | 例子 | 优点 | 主要问题 |
|---|---|---|---|
| Token-level / 显式记忆 | 原始轨迹、摘要、卡片、图、文件、代码技能 | 可读、可编辑、可审计，易接入任意模型 | token 成本、抽取误差、检索噪声 |
| Parametric / 参数记忆 | 微调、LoRA、模型编辑、外置小模型 | 调用快，可形成内化能力 | 更新昂贵、来源不透明、灾难性遗忘 |
| Latent / 潜在记忆 | hidden state、memory token、KV/连续向量 | 密度高，适合端到端优化和多模态 | 难解释、难编辑、跨模型迁移困难 |

### 3.2 按“功能”分类

| 功能 | 保存内容 | 典型用途 |
|---|---|---|
| 事实记忆（factual / semantic） | 用户偏好、人物、对象、世界状态、时间关系 | 个性化、一致性、状态跟踪 |
| 情景记忆（episodic / case-based） | 一次任务的观察、行动、结果、成功/失败轨迹 | 案例复用、反思、错误规避 |
| 程序性记忆（procedural / skill） | 工作流、策略、代码、工具/API 调用方法 | 技能迁移、组合执行、自我改进 |
| 工作记忆（working） | 当前目标、中间变量、计划、被压缩的活跃上下文 | 长程推理、上下文预算管理 |
| 前瞻记忆（prospective） | “未来遇到某条件时做某事”的意图 | 提醒、日程、延迟任务执行 |

### 3.3 按“生命周期”分类

- **形成**：原文保存、摘要、事实/事件抽取、经验蒸馏、图构建、技能编译。
- **演化**：合并、聚类、冲突解决、版本化、强化/衰减、删除、遗忘。
- **检索**：稠密/稀疏检索、时间过滤、图遍历、重排、迭代式 Agent 搜索。
- **使用**：把记忆作为证据、计划、示例、工具或策略参与推理和行动。
- **控制**：固定规则、LLM 自主调用、学习型控制器、监督学习或强化学习策略。

## 4. 发展历史与代表论文

### 4.1 认知科学与可微记忆基础（1968—2018）

1. **1968 — [Human Memory: A Proposed System and Its Control Processes](https://doi.org/10.1016/S0079-7421(08)60422-3)** — Atkinson–Shiffrin 多存储模型区分感觉、短期与长期记忆，为后来的分层存储设计提供了最常用的认知隐喻。
2. **1972 — [Episodic and Semantic Memory](https://doi.org/10.1016/B978-0-12-370509-9.50017-2)** — Tulving 区分亲历事件与一般知识，直接对应今日 Agent 的 episodic / semantic memory。
3. **1974 — [Working Memory](https://doi.org/10.1016/S0079-7421(08)60452-1)** — Baddeley–Hitch 将短期存储改写为支持任务执行的多组件工作空间，是现代 Agent working memory 的理论源头。
4. **1997 — [Long Short-Term Memory](https://doi.org/10.1162/neco.1997.9.8.1735)** — LSTM 以门控机制缓解长依赖训练问题，建立“学习何时记、何时忘”的神经化范式。
5. **2014 — [Memory Networks](https://arxiv.org/abs/1410.3916)** — 将可长期读写的外部记忆与推理模块联合起来，是神经记忆系统的重要起点。
6. **2014 — [Neural Turing Machines](https://arxiv.org/abs/1410.5401)** — 用可微注意力控制外部矩阵的读写，使网络能够学习复制、排序、关联回忆等算法。
7. **2015 — [End-To-End Memory Networks](https://arxiv.org/abs/1503.08895)** — 以多跳注意力将 Memory Networks 端到端化，奠定从记忆条目中多步检索与推理的基本模式。
8. **2016 — [Hybrid Computing Using a Neural Network with Dynamic External Memory](https://doi.org/10.1038/nature20101)** — Differentiable Neural Computer 引入位置/内容寻址和动态分配，把外部存储变成更通用的可学习计算资源。
9. **2017 — [Neural Episodic Control](https://arxiv.org/abs/1703.01988)** — 通过快速写入和近邻召回高价值经验提高强化学习样本效率，预示了后来的案例记忆和运行期学习。

### 4.2 长上下文、检索与非参数记忆（2019—2022）

10. **2019-01 — [Transformer-XL: Attentive Language Models Beyond a Fixed-Length Context](https://arxiv.org/abs/1901.02860)** — 用段级递归缓存跨段隐藏状态，证明语言模型可以复用先前计算而突破固定窗口。
11. **2019-11 — [Generalization through Memorization: Nearest Neighbor Language Models](https://arxiv.org/abs/1911.00172)** — 用隐状态近邻数据存储补充参数模型，形成“参数记忆 + 非参数记忆”的经典组合。
12. **2020-02 — [REALM: Retrieval-Augmented Language Model Pre-Training](https://arxiv.org/abs/2002.08909)** — 将可微检索器纳入预训练，使模型学习何时从外部知识库取证。
13. **2020-05 — [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)** — 系统化提出生成模型与稠密向量库结合的 RAG，成为后来显式 Agent Memory 的工程底座。
14. **2021-12 — [Improving Language Models by Retrieving from Trillions of Tokens (RETRO)](https://arxiv.org/abs/2112.04426)** — 展示超大规模外部语料检索可替代一部分参数规模，强化了“外部记忆可扩展”的路线。
15. **2022-03 — [Memorizing Transformers](https://arxiv.org/abs/2203.08913)** — 在 Transformer 上加入跨批次 kNN 记忆，探索训练与推理期的大规模记忆访问。
16. **2022-10 — [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)** — 虽非专门的记忆论文，但其 Thought–Action–Observation 轨迹成为 Agent 工作记忆、经验记录和反思记忆的标准数据形态。

### 4.3 LLM Agent Memory 正式成形（2023）

17. **2023-03 — [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366)** — 将任务反馈写成自然语言反思并保存在情景记忆中，不改权重也能通过试错改进。
18. **2023-04 — [Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442)** — 建立完整的记忆流、重要性/新近性/相关性检索、反思与规划机制，是 Agent Memory 架构的标志性工作。
19. **2023-05 — [MemoryBank: Enhancing Large Language Models with Long-Term Memory](https://arxiv.org/abs/2305.10250)** — 面向长期陪伴，把会话摘要、人物理解与受遗忘曲线启发的强化/衰减结合起来。
20. **2023-05 — [RET-LLM: Towards a General Read-Write Memory for Large Language Models](https://arxiv.org/abs/2305.14322)** — 以可更新、可解释的三元组存储为 LLM 提供通用读写记忆，并处理时间相关问答。
21. **2023-05 — [Voyager: An Open-Ended Embodied Agent with Large Language Models](https://arxiv.org/abs/2305.16291)** — 将成功行为编译为可执行、可组合的代码技能库，确立程序性记忆对终身 Agent 的价值。
22. **2023-06 — [Augmenting Language Models with Long-Term Memory (LongMem)](https://arxiv.org/abs/2306.07174)** — 用冻结主干和可训练侧网络解耦记忆编码与读取，避免缓存陈旧并扩展长期上下文。
23. **2023-08 — [MemoChat: Tuning LLMs to Use Memos for Consistent Long-Range Open-Domain Conversation](https://arxiv.org/abs/2308.08239)** — 训练模型执行“记忆—检索—回答”循环，用结构化 memo 维持长对话一致性。
24. **2023-08 — [ExpeL: LLM Agents Are Experiential Learners](https://arxiv.org/abs/2308.10144)** — 从多次成功与失败轨迹中对比提炼可泛化 insight，并在新任务中同时召回经验与原则。
25. **2023-08 — [Recursively Summarizing Enables Long-Term Dialogue Memory in Large Language Models](https://arxiv.org/abs/2308.15022)** — 以递归摘要控制随会话增长的上下文，代表早期轻量级长对话记忆路线。
26. **2023-09 — [Cognitive Architectures for Language Agents (CoALA)](https://arxiv.org/abs/2309.02427)** — 用工作、情景、语义和程序性记忆统一描述语言 Agent，并把内部记忆操作纳入 Agent 动作空间。
27. **2023-10 — [Memoria: Resolving Fateful Forgetting Problem through Human-Inspired Memory Architecture](https://arxiv.org/abs/2310.03052)** — 以 engram、工作记忆和长期记忆的相互作用模拟首因、近因及时间邻接效应。
28. **2023-10 — [MemGPT: Towards LLMs as Operating Systems](https://arxiv.org/abs/2310.08560)** — 借鉴虚拟内存，在主上下文与外部存储间分页，并允许 Agent 主动调用记忆工具。
29. **2023-11 — [JARVIS-1: Open-World Multi-task Agents with Memory-Augmented Multimodal Language Models](https://arxiv.org/abs/2311.05997)** — 在 Minecraft 中保存计划与环境反馈，展示多模态开放世界 Agent 的经验记忆。
30. **2023-11 — [Think-in-Memory: Recalling and Post-thinking Enable LLMs with Long-Term Memory](https://arxiv.org/abs/2311.08719)** — 保存“思考结果”而非反复从原始历史重推，并提供插入、合并和遗忘操作。

### 4.4 结构化记忆与长程评测（2024）

31. **2024-01 — [RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval](https://arxiv.org/abs/2401.18059)** — 递归聚类并摘要形成多层树，使检索可在细节和全局抽象之间切换；它本身偏 RAG，但深刻影响后续层次记忆。
32. **2024-02 — [MEMORYLLM: Towards Self-Updatable Large Language Models](https://arxiv.org/abs/2402.04624)** — 在 Transformer 潜在空间中设置固定容量、可反复更新的记忆池，代表 latent memory / 模型编辑交叉路线。
33. **2024-02 — [Evaluating Very Long-Term Conversational Memory of LLM Agents (LoCoMo)](https://arxiv.org/abs/2402.17753)** — 提供跨最多 35 个 session 的长对话、事件图与图像，评估问答、时间/因果理解、摘要和多模态生成。
34. **2024-04 — [Memory Sharing for Large Language Model based Agents](https://arxiv.org/abs/2404.09982)** — 让多个 Agent 过滤、存储和共享经验，并用增长中的记忆池反过来训练检索器。
35. **2024-04 — [A Survey on the Memory Mechanism of Large Language Model based Agents](https://arxiv.org/abs/2404.13501)** — 较早系统梳理 LLM Agent 记忆定义、设计、评测与应用，标志该方向开始形成独立研究版图。
36. **2024-04 — [From Local to Global: A Graph RAG Approach to Query-Focused Summarization](https://arxiv.org/abs/2404.16130)** — 用实体图、社区发现和分层摘要回答全局问题，成为图结构记忆的重要技术来源。
37. **2024-05 — [HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models](https://arxiv.org/abs/2405.14831)** — 以海马索引理论、知识图和 Personalized PageRank 实现高效多跳关联召回。
38. **2024-06 — [Buffer of Thoughts: Thought-Augmented Reasoning with Large Language Models](https://arxiv.org/abs/2406.04271)** — 维护可更新的高层 thought-template 库，将成功推理模式转为策略记忆。
39. **2024-07 — [AriGraph: Learning Knowledge Graph World Models with Episodic Memory for LLM Agents](https://arxiv.org/abs/2407.04363)** — 把语义图与情景轨迹融合为可更新世界模型，服务交互式环境中的规划。
40. **2024-09 — [Agent Workflow Memory](https://arxiv.org/abs/2409.07429)** — 从历史轨迹归纳可复用 workflow，并按任务检索，推动经验记忆向程序性记忆演进。
41. **2024-10 — [LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory](https://arxiv.org/abs/2410.10813)** — 将长期记忆分为信息抽取、跨会话推理、时间推理、知识更新和拒答五项能力，并揭示长上下文本身仍显著退化。

### 4.5 记忆操作系统、生产化与自进化（2025）

42. **2025-01 — [Zep: A Temporal Knowledge Graph Architecture for Agent Memory](https://arxiv.org/abs/2501.13956)** — 用带有效时间和历史关系的知识图融合会话与业务数据，突出企业场景中的时间更新与低延迟。
43. **2025-02 — [Do LLMs Recognize Your Preferences? (PrefEval)](https://arxiv.org/abs/2502.09597)** — 用 3,000 组显式/隐式偏好检验长期个性化，显示仅靠提示和 RAG 仍难主动遵循用户偏好。
44. **2025-02 — [A-MEM: Agentic Memory for LLM Agents](https://arxiv.org/abs/2502.12110)** — 借鉴卡片盒笔记法，把记忆做成会自动建立链接、重写属性并随新信息演化的网络。
45. **2025-04 — [Dynamic Cheatsheet: Test-Time Learning with Adaptive Memory](https://arxiv.org/abs/2504.07952)** — 让黑盒模型在推理期自我维护简洁的策略、代码与经验片段，展示跨题累积学习而不更新权重。
46. **2025-04 — [Know Me, Respond to Me (PersonaMem)](https://arxiv.org/abs/2504.14225)** — 测试跨最多 60 个会话的动态用户画像及其变化，揭示先进模型对“当前偏好状态”的识别仍不稳定。
47. **2025-04 — [From Human Memory to AI Memory: A Survey on Memory Mechanisms in the Era of LLMs](https://arxiv.org/abs/2504.15965)** — 将人类记忆分类映射到 LLM 系统，并从对象、形式和时间三个维度组织 AI 记忆。
48. **2025-04 — [Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory](https://arxiv.org/abs/2504.19413)** — 以 LLM 抽取、增删改合并、向量/图检索组成生产级长时记忆，重点报告精度、延迟和 token 成本。
49. **2025-05 — [Rethinking Memory in AI: Taxonomy, Operations, Topics, and Future Directions](https://arxiv.org/abs/2505.00675)** — 用 consolidation、updating、indexing、forgetting、retrieval、compression 六种原子操作统一不同记忆路线。
50. **2025-05 — [Memory OS of AI Agent (MemoryOS)](https://arxiv.org/abs/2506.06326)** — 以短期—中期—长期三层存储及页面化更新机制支持个性化长对话。
51. **2025-06 — [MEM1: Learning to Synergize Memory and Reasoning for Efficient Long-Horizon Agents](https://arxiv.org/abs/2506.15841)** — 用强化学习让 Agent 每轮更新固定大小的潜在状态，把推理与记忆压缩联合优化到常量空间。
52. **2025-06 — [MemBench: Towards More Comprehensive Evaluation on the Memory of LLM-based Agents](https://arxiv.org/abs/2506.21605)** — 同时覆盖事实/反思记忆、参与/观察场景，并从效果、效率、容量多维评估。
53. **2025-07 — [MemAgent: Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent](https://arxiv.org/abs/2507.02259)** — 让模型分段阅读并覆写有限记忆，通过多会话强化学习把 8K 训练外推到百万 token 级任务。
54. **2025-07 — [MemOS: A Memory OS for AI System](https://arxiv.org/abs/2507.03724)** — 以 MemCube 统一明文、激活和参数记忆，并用调度、版本、迁移与融合管理异构记忆资源。
55. **2025-07 — [Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions (MemoryAgentBench)](https://arxiv.org/abs/2507.05257)** — 以增量多轮输入测准确检索、测试时学习、长程理解和选择性遗忘四项核心能力。
56. **2025-07 — [Agent KB: Leveraging Cross-Domain Experience for Agentic Problem Solving](https://arxiv.org/abs/2507.06229)** — 将不同 Agent 框架的轨迹汇总为共享知识库，通过计划种子、诊断反馈和干扰门控实现跨框架经验迁移。
57. **2025-07 — [MIRIX: Multi-Agent Memory System for LLM-Based Agents](https://arxiv.org/abs/2507.07957)** — 用多个管理 Agent 协调 core、episodic、semantic、procedural、resource 和 knowledge vault 六类记忆，并支持屏幕级多模态历史。
58. **2025-08 — [Memp: Exploring Agent Procedural Memory](https://arxiv.org/abs/2508.06433)** — 把轨迹蒸馏为逐步指令和脚本级抽象，并研究程序性记忆的构建、检索、修正与废弃。
59. **2025-08 — [Memento: Fine-tuning LLM Agents without Fine-tuning LLMs](https://arxiv.org/abs/2508.16153)** — 将 Agent 形式化为记忆增强 MDP，用可学习案例选择和记忆重写实现不改基础 LLM 的在线适应。
60. **2025-08 — [Building Self-Evolving Agents via Experience-Driven Lifelong Learning](https://arxiv.org/abs/2508.19005)** — 提出探索、长期记忆、技能学习和知识内化四阶段框架，并用 StuLife 测持续成长。
61. **2025-08 — [Memory-R1: Enhancing Large Language Model Agents to Manage and Utilize Memories via Reinforcement Learning](https://arxiv.org/abs/2508.19828)** — 分别训练 Memory Manager 执行 ADD/UPDATE/DELETE/NOOP，并训练 Answer Agent 选择和使用记忆。
62. **2025-09 — [ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory](https://arxiv.org/abs/2509.25140)** — 从成功和失败经验蒸馏可泛化推理策略，并提出 memory-aware test-time scaling 让更多试验反哺更好的记忆。
63. **2025-10 — [MemoryBench: A Benchmark for Memory and Continual Learning in LLM Systems](https://arxiv.org/abs/2510.17281)** — 用多领域、多语言用户反馈流评估服务期持续学习，而非仅做长文阅读理解。
64. **2025-11 — [HaluMem: Evaluating Hallucinations in Memory Systems of Agents](https://arxiv.org/abs/2511.03506)** — 在抽取、更新、问答三个操作层定位记忆幻觉，指出早期写入错误会在长期交互中累积并传播。
65. **2025-12 — [Hindsight is 20/20: Building Agent Memory that Retains, Recalls, and Reflects](https://arxiv.org/abs/2512.12818)** — 以事实、经验、实体摘要和信念四个逻辑网络区分证据与推断，并统一 retain / recall / reflect。
66. **2025-12 — [Memory in the Age of AI Agents: A Survey](https://arxiv.org/abs/2512.13564)** — 以 forms–functions–dynamics 统一 token/参数/潜在载体、事实/经验/工作功能和形成/演化/检索生命周期，是截至 2025 年末覆盖面最广的综述之一。

### 4.6 策略学习、系统成本与新型评测（2026-01—2026-08-16）

67. **2026-01 — [Agentic Memory: Learning Unified Long-Term and Short-Term Memory Management for Large Language Model Agents (AgeMem)](https://arxiv.org/abs/2601.01885)** — 将存、取、更新、摘要和删除作为 Agent 工具动作，用分阶段强化学习统一长短期记忆控制。
68. **2026-01 — [EverMemOS: A Self-Organizing Memory Operating System for Structured Long-Horizon Reasoning](https://arxiv.org/abs/2601.02163)** — 以 MemCell、MemScene 和重构式回忆模拟痕迹形成、语义巩固与场景引导检索。
69. **2026-01 — [MemRL: Self-Evolving Agents via Runtime Reinforcement Learning on Episodic Memory](https://arxiv.org/abs/2601.03192)** — 将语义相关性与由反馈更新的 Q-value 分开，用非参数 RL 学习哪些经验真正有用。
70. **2026-01 — [MAGMA: A Multi-Graph based Agentic Memory Architecture for AI Agents](https://arxiv.org/abs/2601.03236)** — 把同一记忆投影到语义、时间、因果和实体图，并按查询意图进行策略引导遍历。
71. **2026-01 — [Memory Matters More: Event-Centric Memory as a Logic Map for Agent Searching and Reasoning](https://arxiv.org/abs/2601.04726)** — CompassMem 将连续经历切分为事件并显式连接逻辑关系，使检索成为沿事件图的目标导向导航。
72. **2026-02 — [ActMem: Bridging the Gap Between Memory Retrieval and Reasoning in LLM Agents](https://arxiv.org/abs/2603.00026)** — 用因果/语义图、反事实推理和常识补全把“找得到记忆”推进到“能据此行动”，并发布 ActMemEval。
73. **2026-03 — [Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers](https://arxiv.org/abs/2603.07670)** — 以 write–manage–read 闭环总结上下文压缩、检索存储、反思、虚拟上下文和学习型管理五类机制。
74. **2026-04 — [Lightweight LLM Agent Memory with Small Language Models](https://arxiv.org/abs/2604.07798)** — 用小模型负责短/中/长期记忆的重排、写入和离线巩固，系统性降低在线延迟与大模型调用成本。
75. **2026-05 — [From Storage to Experience: A Survey on the Evolution of LLM Agent Memory Mechanisms](https://arxiv.org/abs/2605.06716)** — 以 Storage → Reflection → Experience 三阶段解释领域演化，强调主动探索和跨轨迹抽象。
76. **2026-05 — [LongMemEval-V2: Evaluating Long-Term Agent Memory Toward Experienced Colleagues](https://arxiv.org/abs/2605.12493)** — 从聊天历史转向专业 Web 环境经验，测静态状态、动态状态、工作流、环境陷阱和前提意识。
77. **2026-05 — [WorldMemArena: Evaluating Multimodal Agent Memory Through Action-World Interaction](https://arxiv.org/abs/2605.29341)** — 以 400 个多会话多模态任务把错误定位到写入、维护、检索和使用四阶段，并显式测试过时视觉状态更新。
78. **2026-06 — [Agent Memory: Characterization and System Implications of Stateful Long-Horizon Workloads](https://arxiv.org/abs/2606.06448)** — 首次从系统角度剖析十种记忆实现的构建、检索和生成开销，提出新鲜度、摊销和集群管理建议。
79. **2026-06 — [Infini Memory: Maintainable Topic Documents for Long-Term LLM Agent Memory](https://arxiv.org/abs/2606.10677)** — 不把事实拆成孤立碎片，而以可维护主题文档聚合证据和修订事实，并通过迭代工具调用读取。
80. **2026-07 — [SelfMem: Self-Optimizing Memory for AI Agents](https://arxiv.org/abs/2607.03726)** — 不预设固定记忆格式，给 Agent 记忆工具与反馈，让其探索、评估并改进自己的记忆策略。
81. **2026-07 — [PM-Bench: Evaluating Prospective Memory in LLM Agents](https://arxiv.org/abs/2607.12385)** — 首次集中评估 Agent 在持续活动中保留并于未来条件触发时执行意图的能力。
82. **2026-07 — [Memory as a Controlled Process: Learned Adaptive Memory Management for LLM Agents](https://arxiv.org/abs/2607.13591)** — MemCon 把取多少、是否重检索、何时注入计划、合并或遗忘建模为在线控制问题，并兼容不同后端。
83. **2026-07 — [LazyMem: Retrieve Broadly, Construct Selectively for Efficient Long-Term Agent Memory](https://arxiv.org/abs/2607.22690)** — 延迟到查询时再从宽召回候选中选择和压缩，避免写入期不可逆丢失未知未来问题所需细节。
84. **2026-07 — [Filesystem-Based Memory for LLM Agents: Organization, Evolution, and Sustainability](https://arxiv.org/abs/2607.26637)** — 首次系统研究 Agent 自主管理 Markdown 目录树的长期健康度，发现组织可降低搜索成本，但不必然提升答案质量。
85. **2026-08 — [Towards a Formal Definition of Agent Memory: Basis, Span, Optimality, and the Sequential Memory Problem](https://arxiv.org/abs/2608.11654)** — 把记忆定义为知识生成的“基”、可回答性定义为覆盖问题，并以容量约束 MDP 形式化连续写入策略。

## 5. 关键范式如何变化

| 阶段 | 记忆单元 | 主要读写控制 | 主要目标 | 典型代表 |
|---|---|---|---|---|
| 神经外部记忆 | 向量槽位 | 可微注意力 | 学会算法与长依赖 | NTM、DNC、Memory Networks |
| 检索增强模型 | 文档块、hidden-state 邻居 | 固定检索器/相似度 | 扩知识、扩上下文 | kNN-LM、RAG、RETRO |
| 第一代 Agent Memory | 原始轨迹、摘要、反思 | 手写规则 + LLM prompt | 连贯、个性化、避免重错 | Reflexion、Generative Agents、MemoryBank |
| 结构化记忆 | 事件、卡片、实体图、树 | 索引 + 图遍历 + LLM | 多跳、时间、冲突和全局理解 | HippoRAG、AriGraph、A-MEM、Zep |
| 经验/技能记忆 | insight、workflow、代码、工具 | 蒸馏 + 检索复用 | 跨任务学习和自我改进 | Voyager、ExpeL、AWM、Memp、ReasoningBank |
| Memory OS | 多层、多载体记忆对象 | 调度器与生命周期管理 | 生产可用、可迁移、可版本化 | MemGPT、MemoryOS、MemOS、EverMemOS |
| 学习型 Agentic Memory | 记忆操作本身 | SFT/RL/bandit/自优化 | 联合优化效果、成本和长期成长 | MEM1、Memory-R1、AgeMem、MemRL、SelfMem、MemCon |

## 6. 评测体系的演进

### 6.1 从“找回一个事实”到“维护变化中的状态”

早期常用 needle-in-a-haystack 或普通 QA，只能证明某段文字能否被找到。LoCoMo 与 LongMemEval 把评测推进到跨会话、多跳、时间关系、知识更新和拒答；PersonaMem / PrefEval 再引入变化中的用户偏好。

### 6.2 从“记住对话”到“从环境经验中成长”

MemoryAgentBench 增加测试时学习与选择性遗忘；MemBench / MemoryBench 覆盖反思记忆、交互场景和持续用户反馈；LongMemEval-V2 直接测试 Agent 是否记住专业环境的操作规律、工作流与陷阱。

### 6.3 从文本终局分数到生命周期诊断

HaluMem 将错误定位到抽取、更新和问答；WorldMemArena 将多模态记忆分解为写入、维护、检索和使用；PM-Bench 测量延迟意图能否在正确未来状态触发。到 2026 年，评测对象已经从“记忆库答案”扩展为“整个有状态 Agent 的行为”。

### 6.4 尚未解决的评测缺口

- 不同论文使用的 backbone、judge、检索预算和历史长度不同，绝对分数通常不可横向直接比较。
- LLM-as-a-judge 可能偏好冗长回答，且无法完全识别记忆证据被错误推断的情况。
- 许多 benchmark 的问题在记忆写入时已知或分布相似，低估了真正开放世界中的未来查询不确定性。
- 隐私删除、被遗忘权、恶意记忆注入、跨用户隔离和长期漂移仍缺少统一基准。
- 目前多数结果仍是离线/模拟环境结果，真实部署中的月级、年级记忆健康度证据有限。

## 7. 2026-08 的技术判断

### 7.1 最稳定的工程基线仍是“显式文本 + 混合检索 + 生命周期规则”

显式文本、结构化事实或文件最容易检查、迁移和删除。向量检索需要叠加时间、实体、关键词与重排；仅取 top-k 相似片段很难处理事实更新、因果依赖与例外。

### 7.2 图不是银弹，关键是结构与检索策略必须一致

只把内容写成图、读取时仍做普通 embedding top-k，收益有限。Zep、MAGMA、CompassMem 和 ActMem 的共同方向，是让时间/因果/实体关系真正参与查询规划和证据组合。

### 7.3 写入质量比存储容量更关键

错误抽取、把推断当事实、丢失时间范围或主体，会被后续更新和检索放大。HaluMem 表明记忆幻觉会从写入/更新阶段传播；因此来源、时间、置信度、版本和“事实/推断”标签应成为一等元数据。

### 7.4 经验记忆正在成为测试时学习的主要载体

Reflexion 只保存语言反思；ExpeL、AWM、ReasoningBank、Memp 逐步提高抽象层级，从案例变为原则、工作流和可执行技能。Memento、MemRL、MemCon 则进一步学习“哪段经验值得复用”。这条路线在不修改闭源基础模型时尤其重要。

### 7.5 强化学习正在内化记忆管理，但仍依赖外部可审计存储

MEM1、MemAgent、Memory-R1、AgeMem 和 SelfMem 说明记忆压缩与操作策略可以被训练。然而完全潜在化会降低可编辑性和安全性；短期内更可能出现“外部显式记忆 + 学习型控制器”的混合架构。

### 7.6 成本已经成为与准确率同级的指标

长历史会同时增加写入、检索、重排和生成成本。LightMem、LazyMem、文件系统记忆和系统表征研究分别探索小模型分工、查询时构建、组织化搜索与读写路径摊销。生产系统必须报告延迟、token、存储增长和查询量，而不只报告 QA 分数。

## 8. 推荐阅读路径（16 篇）

若希望用最少论文建立完整认识，建议依次阅读：

1. [Memory Networks (2014)](https://arxiv.org/abs/1410.3916) — 外部读写记忆的神经基础。
2. [RAG (2020)](https://arxiv.org/abs/2005.11401) — 参数与非参数记忆组合。
3. [ReAct (2022)](https://arxiv.org/abs/2210.03629) — Agent 交互轨迹的基本形态。
4. [Reflexion (2023)](https://arxiv.org/abs/2303.11366) — 语言反思作为经验记忆。
5. [Generative Agents (2023)](https://arxiv.org/abs/2304.03442) — 第一个影响广泛的完整 Agent 记忆循环。
6. [Voyager (2023)](https://arxiv.org/abs/2305.16291) — 程序性/技能记忆。
7. [CoALA (2023)](https://arxiv.org/abs/2309.02427) — 认知架构视角的统一概念。
8. [MemGPT (2023)](https://arxiv.org/abs/2310.08560) — OS/虚拟内存视角。
9. [LongMemEval (2024)](https://arxiv.org/abs/2410.10813) — 长期交互记忆的核心评测。
10. [A-MEM (2025)](https://arxiv.org/abs/2502.12110) — 可演化的结构化笔记网络。
11. [Mem0 (2025)](https://arxiv.org/abs/2504.19413) — 生产化准确率/成本折中。
12. [MemoryAgentBench (2025)](https://arxiv.org/abs/2507.05257) — 检索、学习、理解、遗忘四能力。
13. [ReasoningBank (2025)](https://arxiv.org/abs/2509.25140) — 推理经验与测试时扩展。
14. [Memory in the Age of AI Agents (2025)](https://arxiv.org/abs/2512.13564) — forms–functions–dynamics 全景综述。
15. [AgeMem (2026)](https://arxiv.org/abs/2601.01885) — 记忆管理成为可训练的 Agent 策略。
16. [Filesystem-Based Memory (2026)](https://arxiv.org/abs/2607.26637) — 检验现实默认载体的组织、演化和可持续性。

## 9. 面向实现者的最小设计检查表

若要在工程中实现 Agent Memory，至少应明确：

- **作用域**：当前线程、用户、Agent、团队还是组织；是否严格隔离租户。
- **记忆模式**：事实、事件、偏好、策略、技能分别有哪些 schema。
- **写入门**：哪些内容值得存；如何去重；如何区分用户原话、环境观察和模型推断。
- **时间语义**：事件时间、写入时间、有效起止时间和版本是否分开。
- **冲突策略**：覆盖、软删除、并存、置信度加权，还是请求用户确认。
- **召回策略**：语义、关键词、时间、实体、图关系和任务效用如何组合。
- **后处理**：是否重排、压缩、聚合，并保留可引用出处。
- **遗忘机制**：容量、时间、效用、隐私删除和法规要求分别如何触发。
- **失败保护**：防止 prompt injection、记忆投毒、跨用户泄漏和错误反思固化。
- **评测**：同时测答案/任务成功率、更新正确性、拒答、延迟、token、存储增长和删除彻底性。

## 10. 资料来源与方法说明

本清单以论文原始页面为主，并用以下综述/维护列表交叉检查覆盖范围：

- [A Survey on the Memory Mechanism of Large Language Model based Agents (2024)](https://arxiv.org/abs/2404.13501)
- [From Human Memory to AI Memory (2025)](https://arxiv.org/abs/2504.15965)
- [Rethinking Memory in AI (2025)](https://arxiv.org/abs/2505.00675)
- [Memory in the Age of AI Agents (2025/2026 v2)](https://arxiv.org/abs/2512.13564) 及其 [持续维护的论文列表](https://github.com/Shichun-Liu/Agent-Memory-Paper-List)
- [Memory for Autonomous LLM Agents (2026)](https://arxiv.org/abs/2603.07670)
- [From Storage to Experience (2026)](https://arxiv.org/abs/2605.06716)

筛选规则：

1. 优先收录提出新记忆架构、记忆操作/控制策略、关键评测或统一分类的工作。
2. 只收录少量对 Agent Memory 影响显著的长上下文、RAG、模型编辑或 KV/latent memory 论文。
3. 同一项目如论文题名后来改名，以当前 arXiv 页面题名为准；日期仍按 v1 首发。
4. arXiv 预印本不等同于已同行评审成果；表中未特别标注接收状态，避免把预印本误写成会议定论。
5. 论文中的 SOTA、提升比例等结论来自各自实验设置，不应脱离 backbone、预算和评测器直接横向比较。
