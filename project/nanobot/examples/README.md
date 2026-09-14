# 使用真实 nanobot Runner 的离线示例

`runner_demo.py` 导入 nanobot 的真实执行内核，只将 LLM provider 换成脚本响应。它不需要 API key，不调用模型或外部工具，不加载用户配置，也不读取个人会话。

它验证三个行为：非法参数不会执行工具；合法参数经过 registry 的转换后执行；工具观察会回到下一轮模型输入，并生成预期的 checkpoint。

## 准备源码与后端依赖

要求 Python 3.11+。以下命令使用 `/tmp` 下的独立 checkout 与虚拟环境，在 Linux/macOS 的 Bash 中运行。安装依赖需要网络，但执行示例本身不需要网络。请在新的目录执行，避免覆盖已有同名目录。

```bash
git clone https://github.com/HKUDS/nanobot.git /tmp/nanobot-demo-source
git -C /tmp/nanobot-demo-source checkout 499bf903022f429dd4501fdfbeeccadcb99dd51f
python3 -m venv /tmp/nanobot-demo-env

# 只安装 Python 后端依赖；不运行项目打包 hook，也不构建 WebUI / TUI。
python3 - <<'PY'
import tomllib
from pathlib import Path
source = Path('/tmp/nanobot-demo-source')
config = tomllib.loads((source / 'pyproject.toml').read_text())
Path('/tmp/nanobot-demo-requirements.txt').write_text(
    '\n'.join(config['project']['dependencies']) + '\n'
)
PY

/tmp/nanobot-demo-env/bin/python -m pip install -r /tmp/nanobot-demo-requirements.txt
```

该方法适用于研究和单独执行后端模块，不会安装 `nanobot` 命令。正常使用产品时，请按上游安装说明安装完整软件包。

## 运行

在本仓库根目录执行：

```bash
PYTHONPATH=/tmp/nanobot-demo-source \
  /tmp/nanobot-demo-env/bin/python project/nanobot/examples/runner_demo.py
```

预期输出包含 `19 + 23 = 42。`、`completed`、三轮模型响应以及仅一次实际工具执行。完整已验证输出见 [runner-demo-output.json](../research/runner-demo-output.json)。

示例内断言会检查非法调用未执行、状态为 `error → ok`，以及 checkpoint 顺序：

```text
awaiting_tools → tools_completed → awaiting_tools → tools_completed → final_response
```

注意：错误纠正和最终答案由脚本 provider 预设，不是模型智能评测；usage 也是合成值。示例验证的是运行时数据流，不覆盖网络、真实模型、会话持久化和副作用恢复。

## 二次开发时可替换的部分

- 用自己的 `Tool` 替换 `AddTool`，明确 schema、错误结果和副作用属性。
- 用真实 provider 替换 `ScriptedProvider`，并通过适合模型的 `LLMRuntime` 提供上下文窗口和生成参数。
- 若需要完整的会话、记忆、MCP 生命周期与配置加载，优先使用高层 `Nanobot` SDK；直接 Runner 属于较底层的嵌入接口。

示例绑定本文 commit 的内部接口，后续版本可能需要调整。
