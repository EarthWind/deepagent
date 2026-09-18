# 跟着文章观察一次执行与恢复

本目录包含两个不同层次的例子。`state_machine_demo.py` 是受 Goose 状态机思想启发的原创教学代码；`repository-map.yaml` 是按固定源码快照编写的 Goose Recipe。

## 1. 无需账号的状态机实验

需要 Python 3.10+，仅使用标准库。从 `deepagent` 仓库根目录运行：

```bash
python3 project/goose/examples/state_machine_demo.py
python3 -m unittest discover -s project/goose/examples -p 'test_*.py' -v
```

默认运行会创建临时 SQLite 文件，结束后自动清理。它依次执行：

1. 记录用户文本；假 Provider 发出 `count_words` 请求。
2. 保存审批请求并返回 `waiting_for_approval`。
3. 关闭数据库连接，销毁该次 Machine，重新创建 Store。
4. 保存批准决定，新 Machine 从数据库推导剩余动作。
5. 执行纯函数，保存 observation，生成最终消息。
6. 输入一段预先给定的摘要，展示用户可见历史与模型可见上下文的区别。

关键输出：

```text
First run: waiting_for_approval
After reconstruct + approve: completed
...
Agent-visible kinds: ['summary']
```

工具结果为 `{"count": 5}`。这里按空白分词，只用于英文演示，不是中文分词器。

### 对照上游抽象

| 教学实现 | 对应思想 | 与 Goose 的区别 |
| --- | --- | --- |
| `Machine.operations` | 有序 Operation 列表 | 只有 Stop、Approve、Execute、Fake Inference |
| `Store.load()` | 每轮重新读取会话 | 只支持单会话、单进程所有者 |
| `StepResult / Effect` | 操作返回效果 | Python 简化结构，不是上游 API |
| `approval_requested / decision` | 审批持久化后恢复 | 没有 ACP/UI 确认路由 |
| `count_words` | Tool observation | 纯函数，没有 MCP 和外部副作用 |
| visibility 字段 | 模型与用户视图分离 | 摘要由调用方提供，仅允许完成后演示 |

**示例限制：**没有真实 LLM、流式网络、Provider formatter、并发工具、Hooks、取消运行中阻塞工具、跨进程会话租约或外部幂等。它在提交完工具结果后不会再次运行该调用；若实际外部动作成功后、结果保存前崩溃，仍需专门的幂等与核对设计。测试“重启不重复已完成调用”不等于证明 exactly-once。

## 2. 用 Goose 运行目录分析 Recipe

先安装与文章版本相容的 Goose，并执行 `goose configure` 配置模型。该操作需要真实模型环境，本次调研没有代用户配置账号或执行模型请求。

```bash
goose recipe validate project/goose/examples/repository-map.yaml
GOOSE_MODE=approve goose run \
  --recipe project/goose/examples/repository-map.yaml \
  --params focus="Agent 内核与模型 Provider 的目录关系" \
  --interactive
```

参数 `focus` 是自然语言阅读重点；真正分析的是启动 Goose 时的 cwd。切换到其他仓库后，请为 `--recipe` 提供绝对路径。

配方显式只安装 platform Developer，并通过非空 `available_tools: [tree]` 缩小到目录工具；Recipe 的 structured-output 机制另外提供 `final_output`。它不自动增加 Summon 或其他工具。

`tree` 可接受路径，因此本配方也不是一个 OS 目录沙箱。这里减少的是可执行动作种类：没有 shell、写文件、任意代码执行。严格的文件读取范围仍应交给受限工具实现或操作系统策略。

期望输出结构如下，内容由实际观察生成，以下仅是形状示例：

```json
{
  "summary": "观察到 Rust crate 与桌面 UI 目录。",
  "observations": [{"path": "crates", "evidence": "tree 返回了该目录。"}],
  "hypotheses": ["可能按 crate 划分运行时；需要读 Cargo.toml 验证。"],
  "limitations": ["只查看目录，没有读取源码、验证调用关系或运行测试。"]
}
```

本地检查仅验证 YAML 可解析、字段与源码模型相符、JSON schema 有效。`goose recipe validate` 和真实模型执行仍应在安装 Goose 后运行。
