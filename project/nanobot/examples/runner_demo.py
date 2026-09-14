"""Offline demonstration using nanobot's real AgentRunner, not a rewritten loop.

Run with the pinned upstream checkout on PYTHONPATH; see README.md.
The provider is scripted. No API key, network, shell tool, or user data is used.
"""

from __future__ import annotations

import asyncio
import json
from typing import Any

from nanobot.agent.runner import AgentRunner, AgentRunSpec
from nanobot.agent.tools.base import Tool, tool_parameters
from nanobot.agent.tools.registry import ToolRegistry
from nanobot.providers.base import (
    GenerationSettings,
    LLMProvider,
    LLMResponse,
    LLMUsage,
    ToolCallRequest,
)
from nanobot.utils.llm_runtime import LLMRuntime


@tool_parameters({
    "type": "object",
    "properties": {"a": {"type": "integer"}, "b": {"type": "integer"}},
    "required": ["a", "b"],
    "additionalProperties": False,
})
class AddTool(Tool):
    """A deterministic, side-effect-free tool with an observable invocation log."""

    name = "demo_add"
    description = "Add two integers."
    read_only = True

    def __init__(self) -> None:
        self.calls: list[tuple[int, int]] = []

    async def execute(self, a: int, b: int, **kwargs: Any) -> str:
        self.calls.append((a, b))
        return str(a + b)


class ScriptedProvider(LLMProvider):
    """Three fixed responses exercise validation, correction, and completion."""

    def __init__(self) -> None:
        super().__init__(provider_name="offline_demo")
        self.round = 0

    def get_default_model(self) -> str:
        return "scripted-demo"

    def estimate_prompt_tokens(self, messages: Any, tools: Any = None) -> int:
        # Local synthetic count: avoids tokenizer downloads. This is not a benchmark.
        return max(1, len(json.dumps(messages, ensure_ascii=False)) // 3)

    async def chat(self, messages: list[dict[str, Any]], **kwargs: Any) -> LLMResponse:
        self.round += 1
        usage = LLMUsage.reported(input_tokens=100, output_tokens=20)
        if self.round == 1:
            return LLMResponse(
                content=None,
                tool_calls=[ToolCallRequest("bad", "demo_add", {"a": 19})],
                finish_reason="tool_calls",
                usage=usage,
            )
        if self.round == 2:
            assert "missing required b" in messages[-1]["content"]
            return LLMResponse(
                content=None,
                # The real registry safely casts "19" according to the integer schema.
                tool_calls=[ToolCallRequest("good", "demo_add", {"a": "19", "b": 23})],
                finish_reason="tool_calls",
                usage=usage,
            )
        assert self.round == 3
        assert messages[-1]["content"] == "42"
        return LLMResponse(content="19 + 23 = 42。", usage=usage)


async def main() -> None:
    tool = AddTool()
    registry = ToolRegistry()
    registry.register(tool)
    checkpoints: list[str] = []

    async def checkpoint(payload: dict[str, Any]) -> None:
        checkpoints.append(payload["phase"])

    provider = ScriptedProvider()
    runtime = LLMRuntime(
        provider=provider,
        model=provider.get_default_model(),
        generation=GenerationSettings(max_tokens=256, temperature=0),
        context_window_tokens=8192,
    )
    result = await AgentRunner().run(AgentRunSpec(
        initial_messages=[
            {"role": "system", "content": "Use demo_add to calculate the answer."},
            {"role": "user", "content": "计算 19 + 23。"},
        ],
        tools=registry,
        runtime=runtime,
        max_iterations=4,
        max_tool_result_chars=16000,
        checkpoint_callback=checkpoint,
    ))
    assert result.stop_reason == "completed"
    assert tool.calls == [(19, 23)], "Invalid arguments must never execute the tool"
    assert [e["status"] for e in result.tool_events] == ["error", "ok"]
    assert checkpoints == [
        "awaiting_tools", "tools_completed", "awaiting_tools",
        "tools_completed", "final_response",
    ]
    print(json.dumps({
        "final": result.final_content,
        "stop_reason": result.stop_reason,
        "model_rounds": provider.round,
        "actual_tool_calls": tool.calls,
        "tool_statuses": [e["status"] for e in result.tool_events],
        "checkpoints": checkpoints,
        "usage_note": "Synthetic provider usage; no real LLM was called.",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
