# 无密钥教学示例

`inbox_demo.py` 用 Python 标准库展示后台任务提交、单 worker 串行执行、目标 Agent 结果回到父 thread、失败通知四个机制。它是本文原创的教学模型，**不是 Octop SDK、源码移植或可部署服务**。模拟 Agent 只拼接字符串；没有真实推理、权限校验、工具调用或持久化。

在仓库根目录执行：

```bash
python3 project/octop/examples/inbox_demo.py
python3 -m unittest discover -s project/octop/examples -p 'test_*.py' -v
```

第一次输出的 `agent_calls_so_far` 为 `0`；执行顺序为「检索专家 → 主助手 → 架构专家 → 主助手」，最大同时运行的模拟调用为 `1`。新建 Inbox 后旧任务不会出现，用来说明内存队列的恢复边界。

与正式实现的差别包括：示例显式调用 `drain()`，没有常驻后台 task；peer thread 用可读字符串表示；历史只存在字典里；省略取消、审批、共享 Agent、回调错误、线程安全等功能。正式实现请看 [源码索引](../SOURCE_MAP.md#h-inbox)。
