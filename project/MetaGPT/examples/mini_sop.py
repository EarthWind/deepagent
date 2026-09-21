"""原创教学模型：标准库实现消息订阅、结构化交付和 QA 反馈；不是 MetaGPT。"""
from __future__ import annotations

import argparse
import asyncio
import json
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Awaitable, Callable


@dataclass(frozen=True)
class Message:
    id: int
    content: dict
    cause_by: str
    sent_from: str
    send_to: frozenset[str] = frozenset({"<all>"})


@dataclass
class Role:
    name: str
    watch: set[str]
    action: Callable[[Message], Awaitable[tuple[str, dict]]]
    inbox: asyncio.Queue = field(default_factory=asyncio.Queue)
    memory: list[Message] = field(default_factory=list)

    async def run(self, env: Environment) -> None:
        fresh = []
        while not self.inbox.empty():
            message = self.inbox.get_nowait()
            if (message.cause_by in self.watch or self.name in message.send_to) and message not in self.memory:
                fresh.append(message)
                self.memory.append(message)
        # 教学模型逐条处理；上游 Role 把一批 news 交给一次 react。
        for message in fresh:
            event, content = await self.action(message)
            env.publish(event, self.name, content)


class Environment:
    def __init__(self, roles: list[Role]):
        self.roles = roles
        self.history: list[Message] = []

    def publish(self, event: str, sender: str, content: dict) -> None:
        message = Message(len(self.history) + 1, content, event, sender)
        self.history.append(message)
        for role in self.roles:
            if "<all>" in message.send_to or role.name in message.send_to:
                role.inbox.put_nowait(message)

    async def run(self, limit: int = 12) -> str:
        for _ in range(limit):
            active = [role for role in self.roles if not role.inbox.empty()]
            if not active:
                return "idle"
            await asyncio.gather(*(role.run(self) for role in active))
        return "round_limit"


async def demo(output: Path) -> dict:
    output.mkdir(parents=True, exist_ok=True)

    async def write_spec(message: Message) -> tuple[str, dict]:
        spec = {"function": "add(a, b)", "examples": [[2, 3, 5], [-1, 1, 0]], "requirement": message.content}
        (output / "spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n")
        return "WriteSpec", spec

    revision = 0

    async def write_code(message: Message) -> tuple[str, dict]:
        nonlocal revision
        revision += 1
        # 固定脚本故意注入一次缺陷，模拟模型吸收测试反馈后修复。
        operator = "-" if revision == 1 else "+"
        code = f"def add(a, b):\n    return a {operator} b\n"
        (output / "candidate.py").write_text(code)
        return "WriteCode", {"revision": revision, "file": "candidate.py", "feedback": message.content}

    async def run_tests(message: Message) -> tuple[str, dict]:
        # 只运行本文件中固定生成的示例，不接受任意外部代码；subprocess 不是安全沙盒。
        checks = "\nassert add(2, 3) == 5\nassert add(-1, 1) == 0\nprint('2 assertions passed')\n"
        code = (output / "candidate.py").read_text() + checks
        result = await asyncio.to_thread(
            subprocess.run, [sys.executable, "-I", "-c", code],
            capture_output=True, text=True, timeout=5, check=False,
        )
        passed = result.returncode == 0
        return ("Accepted" if passed else "TestFailed"), {
            "revision": message.content["revision"],
            "passed": passed,
            "output": (result.stdout + result.stderr).strip(),
        }

    team = Environment([
        Role("PM", {"UserRequirement"}, write_spec),
        Role("Engineer", {"WriteSpec", "TestFailed"}, write_code),
        Role("QA", {"WriteCode"}, run_tests),
    ])
    team.publish("UserRequirement", "User", {"text": "实现两个数相加，必须通过正数和相消测试"})
    stop_reason = await team.run()
    trace = []
    for message in team.history:
        item = asdict(message)
        item["send_to"] = sorted(message.send_to)
        trace.append(item)
    accepted = any(message.cause_by == "Accepted" for message in team.history)
    report = {"kind": "original_teaching_model", "stop_reason": stop_reason, "accepted": accepted, "trace": trace}
    (output / "trace.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = asyncio.run(demo(args.output))
    for event in report["trace"]:
        print(f"{event['id']:02d} {event['sent_from']:8s} → {event['cause_by']}")
    print(f"stop={report['stop_reason']}; accepted={report['accepted']}")
    if not report["accepted"]:
        raise SystemExit(1)
