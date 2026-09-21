# 示例使用说明

| 文件 | 类型 | 依赖与验证范围 |
| --- | --- | --- |
| [mini_sop.py](mini_sop.py) | 原创教学实现 | Python 3.10+ 标准库；已实际运行完整反馈闭环 |
| [metagpt_custom_team.py](metagpt_custom_team.py) | 实际 MetaGPT API 示例 | 固定提交 MetaGPT 与兼容 Python、模型配置；本次仅语法和静态接口核对 |

从仓库根目录运行：

```bash
python3 project/MetaGPT/examples/mini_sop.py --output /tmp/metagpt-blog-demo
```

输出规范、最终代码与消息轨迹。第一版故意产生减法，QA 的 Python 断言失败后触发第二版加法，最终得到 `accepted=True`。实际运行输出副本见 [demo-trace.json](../research/demo-trace.json)。

教学模型与上游的区别：它没有 LLM、ActionNode、MGX、持久化或费用统计；逐条处理消息，而上游基类 Role 一次接收整批 news。子进程只执行示例中固定的作者代码，不是用于运行任意不可信代码的沙盒。

真实 MetaGPT 示例请先按[正文安装步骤](../README.md#sec-16)准备独立环境，再用该环境的 Python 执行 `metagpt_custom_team.py`。这会调用模型并可能产生费用。示例显式设置 `use_mgx=False`，构造两个基类 Role，展示 Action 订阅交接。
