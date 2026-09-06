# 生产形态最小示例

该示例不是“Hello World”：它演示了 LangChain v1 Agent 的关键工程边界，包括请求上下文注入、只读工具的选择性重试、写工具人工审批、checkpoint/resume、运行预算和 Pydantic 结构化输出。

使用 Python 3.10+，安装与运行：

```bash
python -m venv .venv
source .venv/bin/activate
pip install "langchain[openai]==1.4.0"

export OPENAI_API_KEY="..."
export LANGCHAIN_MODEL="openai:<your-model>"
python incident_agent.py
python incident_agent.py --approve-ticket
```

`InMemorySaver` 与 `InMemoryStore` 只适合演示和测试。生产环境应替换成持久化后端，并把 `thread_id`、store namespace 与租户身份绑定；真实审批应把 interrupt payload 交给 UI 或工单系统，不能自动 approve。

如果更换 Anthropic、Google 或其他 provider，安装相应 `langchain[...]` extra，并修改 `LANGCHAIN_MODEL`；Agent 代码和 `ToolStrategy` 无需改变。
