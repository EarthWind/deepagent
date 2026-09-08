# Autoresearch 源码调研：内部研究底稿

> 本文件保存范围、证据映射、推导与限制，不是面向读者的最终博客。最终成文见 [`../README.md`](../README.md)。

## 任务定义

- 目标：从专业大模型 Agent 工程角度，调研并详细解释 `karpathy/autoresearch` 的当前实现，以中文图文博客交付。
- 受众：理解 LLM 训练、Git、Coding Agent 与基本实验方法的工程师。
- 上游：<https://github.com/karpathy/autoresearch.git>。
- 固定基线：`master` / `228791fb499afffb54b46200aca536f79142f117`。
- 上游提交时间：2026-03-25T17:07:37-07:00；调研时间：2026-09-09（Asia/Shanghai）。
- 重点：Agent 边界、Prompt 协议、实验状态机、数据与 BPB、默认模型、优化器、时间语义、Git/TSV 记忆、安全与生产化。
- 不覆盖：第三方 fork 全量比较、外部 Coding Agent 排名、真实 H100 benchmark、多卡移植。
- 证据优先级：固定提交源码 > 项目 README/issue > 算法原论文与官方依赖文档 > 社区讨论。

## 直接结论

Autoresearch 不是一个自带 Agent Loop 的框架。它以 `program.md` 为轻量 Skill，利用外部 Coding Agent 的推理、文件编辑、Shell、Git 和会话能力执行一条 winner-only 实验协议。仓库自身实现的是一个单卡 nanochat 派生训练赛道：固定 `prepare.py` 提供数据、tokenizer、300 秒 steady-state 预算与 BPB；可变 `train.py` 提供约 50.3M 参数 GPT、FA3、MuonAdamW 与训练循环；Git branch 和未跟踪的 `results.tsv` 保存状态。

它作为最小自主实验协议非常出色，但默认“冻结评测”只是 Prompt policy，并未形成对抗性隔离。单次指标、验证集可见、动态 kernel 未固定 revision、负结果 artifact 不耐久、无 watchdog/总预算/多 Agent 调度，是把它升级为可信生产系统时最重要的缺口。

## 固定快照事实

| 项目 | 结果 | 获取方式 |
|---|---|---|
| HEAD | `228791fb499afffb54b46200aca536f79142f117` | `git rev-parse HEAD` |
| Branch | `master` | `git branch --show-current` |
| HEAD 时间 | `2026-03-25T17:07:37-07:00` | `git log -1 --format=%aI` |
| Tags | 无 | `git tag` |
| Commit 数 | 36 | `git rev-list --count HEAD` |
| 核心文件行数 | 114 + 389 + 630 = 1,133 | `wc -l` |
| Python 依赖 | PyTorch 2.9.1 cu128；kernels、rustbpe、tiktoken、pyarrow 等 | `pyproject.toml` |

## 主张—证据账本

| 主张 | 一手证据 | 置信度 | 说明 / 反证检查 |
|---|---|---:|---|
| 仓库不实现 Agent Runtime | README 运行方式；全仓文件树无模型 API/调度器 | 高 | Agent 是外部 Claude/Codex；`program.md` 由其直接阅读 |
| `program.md` 是 114 行轻量 Skill | `program.md`；README L44-L53 | 高 | 没有 parser/DSL runtime |
| 唯一允许修改 `train.py` | `program.md` L25-L31 | 高 | 只是指令约束，不是文件权限 |
| 首轮必须 baseline | `program.md` L39 | 高 | 明确规则 |
| 每轮先 commit 后运行 | `program.md` L96-L104 | 高 | 给候选分配 SHA；discard 后 reset |
| Git HEAD 表示 champion | 实验 loop 的 keep/reset 语义 | 高 | 属于对代码行为的直接抽象 |
| rejected commit 不一定长期存在 | Git reset + 无专用 ref/tag | 高 | Git 通用语义推论；短期仍可能存在于 reflog |
| `results.tsv` 不提交 | `program.md` L102；`.gitignore` | 高 | 负结果账本不是仓库耐久历史 |
| `run.log` 未被 ignore | `.gitignore` 全文 | 高 | 可能被 `git add .` 误提交 |
| 数据为 ClimbMix，验证固定 shard 6542 | `prepare.py` L38-L45 | 高 | HF dataset repo 交叉验证 |
| 默认下载 10 train + 1 val shard | `prepare.py` main default + `download_data` | 高 | 用户可用参数改变 train shard 数，所以 run metadata 应记录 |
| tokenizer 为 8192 vocab | `prepare.py` L45、L161-L175 | 高 | 8188 mergeable + 4 reserved |
| tokenizer cache 不校验 provenance | `train_tokenizer` early return | 高 | 文件存在即复用 |
| packing 无 padding、BOS-aligned | `make_dataloader` | 高 | best-fit 与 crop 直接来自实现 |
| 数据顺序无 shuffle | `_document_batches` | 高 | sorted file/row group 顺序循环 |
| BPB 是总 nats / ln2 / 总 UTF-8 bytes | `evaluate_bpb` | 高 | special token byte=0 且 numerator masked |
| 默认评估 80 batches | 常量与 batch/seq 默认值复算 | 高 | 20,971,520 / 262,144 = 80 |
| 默认模型 8L/512d/4H/50.3M | `build_model_config`、参数结构复算 | 高 | 精确复算 50,332,176 |
| 默认无 GQA | `n_kv_head=num_heads` | 高 | 类本身支持 GQA，但默认配置没有启用 |
| pattern 为 SSSL 且末层 full | `_compute_window_sizes` | 高 | 默认实际窗口 1024×6、2048×2 |
| VE 在 1/3/5/7 层 | `has_ve` 和 depth=8 | 高 | 每层独立 embedding + gate，不等同原始 ResFormer |
| optimizer 分 Muon/AdamW | `setup_optimizer` | 高 | Block params 进 Muon，其余指定 AdamW |
| Muon 含 Polar Express、NorMuon、cautious WD | `muon_step_fused` | 高 | 原论文用于解释算法背景，不替代码本身作证 |
| 前 11 step 不计入训练时间但会更新 | loop `if step > 10` 位于 update 后 | 高 | “排除 startup/compile”并非不运行这些 steps |
| schedule 使用 step 前累计时间 | progress 先算，dt 后累加 | 高 | 会有一个 step 的轻微滞后 |
| 300 秒会略超 | 完整 step 后检查停止 | 高 | 不是精确硬中断 |
| MFU 分母写死 H100 峰值 | `H100_BF16_PEAK_FLOPS` 与 summary | 高 | 非 H100 上不是真实设备 MFU |
| 动态 Kernel revision 未固定 | `get_kernel(repo)` 无 revision/version；HF API 文档 | 中高 | uv.lock 可固定 Python package，不能从调用点证明 Hub artifact 固定 |
| 上游图 83 次/15 keep | `progress.png` 标题 | 高（图示事实） | 原始 results.tsv 未提交，单点不可独立复核 |
| “NEVER STOP”不保证生命周期 | `program.md` + issue #57 | 高 | 作者本人提交 issue，仓库无 watchdog/scheduler |
| 当前没有 swarm 编排 | 文件树和源码 | 高 | README 是愿景表达；无 worker queue/lease/orchestrator |
| evaluator 不是安全边界 | 同一文件系统/进程/权限；Python import 关系 | 高 | 属于源码安全分析；没有声称已发现实际作弊 |

## 关键推导

### 默认参数量

- `wte = 8192 × 512 = 4,194,304`
- `value_embeds = 4 × 8192 × 512 = 16,777,216`
- `lm_head = 512 × 8192 = 4,194,304`
- 每个 block 主矩阵：Q/K/V/O `4 × 512²`，MLP `2 × 512 × 2048`，合计 `3,145,728`
- 8 blocks 主矩阵：`25,165,824`
- 4 个 gate：`4 × (4 × 32) = 512`
- 16 个 scalar
- 总计：`50,332,176`

### 默认 batch 与评估

- 单 micro-batch token：`128 × 2048 = 262,144`
- optimizer batch：`524,288`
- gradient accumulation：`2`
- eval tokens：`40 × 524,288 = 20,971,520`
- eval steps：`20,971,520 / 262,144 = 80`

### 默认 AdamW 宽度缩放

- `dmodel_lr_scale = (512 / 768)^-0.5 = sqrt(1.5) ≈ 1.224744871`
- lm_head 实际初始 LR ≈ `0.00489898`
- token/value embedding 实际初始 LR ≈ `0.73484692`
- scalar groups 不使用该宽度缩放。

## 不确定性、矛盾与边界

1. **README 的“固定 5 分钟”与源码计时。** 对外概念是 5 分钟训练；源码实际排除前 11 step，并在整步结束后检查 300 秒。成文同时保留产品语义和精确实现。
2. **“Frozen evaluator”。** `program.md` 语义上冻结 `prepare.py`，但没有 OS/容器/进程隔离。文章用“Prompt-level read-only”而不是“防篡改”。
3. **ResFormer 名称。** 代码注释提 ResFormer，但实现是独立 token value embeddings + gate，不等价于论文的 first-layer V residual。文章只称“受 value residual 思路影响”。
4. **结果图。** 图可证明作者展示的轨迹和计数，不能证明每个点可复现；仓库无原始 TSV。文章明确披露。
5. **Kernel pinning。** HF 当前文档说明可用 revision/version，源码未传；没有在目标 GPU 上实际解析 artifact，因此只提出复现风险，不声称运行一定拉取不安全代码。
6. **非确定性。** 固定随机种子不等于 bitwise deterministic；没有运行硬件实测，因此文章只把 GPU、Kernel、clock 与 seed 列为潜在噪声源。
7. **Git reset 具体模式。** Prompt 只写 `git reset`，没有明确 `--hard`。文章不假装存在精确自动实现，只描述意图和风险。
8. **上游 commit 时间早于调研日。** 截至调研时 clone 得到该 HEAD；不根据搜索摘要推断项目停止维护。

## 建议框架

生产级演进建议按优先级排序：

1. evaluator 独立进程 + 隐藏验证集 + 签名 metric；
2. candidate worker 容器/VM 隔离，候选目录外只读、网络默认拒绝；
3. append-only experiment DB 与对象存储，保存所有 patch/log/env；
4. 多 seed 重复、最小改善阈值与 champion 同条件复测；
5. Supervisor 控制总 GPU-hour、失败熔断、heartbeat 与 resume；
6. 多 Agent 使用独立 worktree/lease，由中央 promotion gate 决策；
7. 固化 CUDA/driver/kernel/data/tokenizer manifest；
8. 将 VRAM、复杂度、安全策略从自然语言变成机器规则。

## 来源索引

### 固定源码

- Repository: <https://github.com/karpathy/autoresearch/tree/228791fb499afffb54b46200aca536f79142f117>
- README: <https://github.com/karpathy/autoresearch/blob/228791fb499afffb54b46200aca536f79142f117/README.md>
- Program: <https://github.com/karpathy/autoresearch/blob/228791fb499afffb54b46200aca536f79142f117/program.md>
- Prepare: <https://github.com/karpathy/autoresearch/blob/228791fb499afffb54b46200aca536f79142f117/prepare.py>
- Train: <https://github.com/karpathy/autoresearch/blob/228791fb499afffb54b46200aca536f79142f117/train.py>
- Analysis: <https://github.com/karpathy/autoresearch/blob/228791fb499afffb54b46200aca536f79142f117/analysis.ipynb>
- Gitignore: <https://github.com/karpathy/autoresearch/blob/228791fb499afffb54b46200aca536f79142f117/.gitignore>
- Author lifecycle issue: <https://github.com/karpathy/autoresearch/issues/57>

### 官方依赖与原论文

- PyTorch 2.9 `torch.compile`: <https://docs.pytorch.org/docs/2.9/generated/torch.compile.html>
- PyTorch `fullgraph=True`: <https://docs.pytorch.org/docs/2.9/compile/programming_model.fullgraph_true.html>
- Hugging Face Kernels API: <https://huggingface.co/docs/kernels/api/kernels>
- ClimbMix dataset: <https://huggingface.co/datasets/karpathy/climbmix-400b-shuffle>
- Polar Express, ICLR 2026: <https://openreview.net/pdf?id=yRtgZ1K8hO>
- NorMuon: <https://arxiv.org/abs/2510.05491>
- Value Residual Learning: <https://arxiv.org/abs/2410.17897>

## 搜索记录与停止条件

完成的检索波次：

1. 克隆官方仓库并固定 HEAD；读取完整 README、program、prepare、train、pyproject、gitignore、notebook 与 Git 历史。
2. 针对模型技巧检索 nanochat、Polar Express、NorMuon、Value Residual 的一手资料。
3. 针对依赖行为检索 PyTorch 2.9 `torch.compile` 与 Hugging Face Kernels 官方文档。
4. 针对生命周期与记忆缺口查看作者 issue、分析 notebook 与上游 progress artifact。

停止原因：Agent 边界、loop、数据/评测、模型、optimizer、计时、状态、安全和复现均已有固定源码证据；关键外部算法只有背景性说明且已有原论文；剩余搜索主要会增加第三方 fork 或观点，不会改变实现结论，边际收益已低。

## 交付验证

- 已检查 `README.md` 的 6 个本地图片路径，文件均存在；外部上游进度图使用固定 Commit 的 raw URL。
- 已用 XML parser 解析 6 个 SVG，并分别用 Chromium 渲染为 1440px 截图做视觉检查；修正了总览图中 `train.py → GPU` 的箭头方向。
- 已通过浏览器打开固定 Commit 目录与 `program.md`、`prepare.py`、`train.py`，确认链接可访问。
- 已用 `python3 -m py_compile` 对上游 `prepare.py` / `train.py` 做语法编译，不导入或安装训练依赖。
- 已检查 Markdown code fence 成对、SVG alt/ARIA 描述存在、目标目录 Git 状态符合预期。
- 当前环境没有 Markdown→HTML/PDF renderer，因此正文采用结构检查，视觉检查覆盖全部本地图，不声称完成整篇页面渲染。
