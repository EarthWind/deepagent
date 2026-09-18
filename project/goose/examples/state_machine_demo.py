#!/usr/bin/env python3
"""Goose-inspired teaching example, not an implementation of the Goose API.

Run with Python 3.10+. Uses a fake provider, a pure tool and a temporary SQLite
database. There are no model requests, shell tools or third-party dependencies.
One process owns the session; this demo does not guarantee exactly-once effects.
"""
from __future__ import annotations

import json
import sqlite3
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


@dataclass(frozen=True)
class Message:
    seq: int
    kind: str
    payload: dict
    user_visible: bool
    agent_visible: bool


@dataclass(frozen=True)
class Effect:
    kind: str
    payload: dict
    user_visible: bool = True
    agent_visible: bool = True


@dataclass(frozen=True)
class StepResult:
    effects: tuple[Effect, ...] = ()
    status: str | None = None


class Store:
    """A single-session store; each operation's effects commit together here."""

    def __init__(self, path: Path):
        self.db = sqlite3.connect(path)
        self.db.execute("""CREATE TABLE IF NOT EXISTS messages (
            seq INTEGER PRIMARY KEY AUTOINCREMENT,
            kind TEXT NOT NULL,
            payload TEXT NOT NULL,
            user_visible INTEGER NOT NULL,
            agent_visible INTEGER NOT NULL
        )""")
        self.db.commit()

    def close(self):
        self.db.close()

    def load(self) -> list[Message]:
        return [
            Message(seq, kind, json.loads(payload), bool(user), bool(agent))
            for seq, kind, payload, user, agent in self.db.execute(
                "SELECT seq, kind, payload, user_visible, agent_visible "
                "FROM messages ORDER BY seq"
            )
        ]

    def apply(self, effects: tuple[Effect, ...]):
        with self.db:
            self.db.executemany(
                "INSERT INTO messages(kind,payload,user_visible,agent_visible) "
                "VALUES (?,?,?,?)",
                [(e.kind, json.dumps(e.payload, ensure_ascii=False),
                  e.user_visible, e.agent_visible) for e in effects],
            )

    def answer(self, call_id: str, allow: bool):
        turn = current_turn(self.load())
        if not any(m.kind == "approval_requested" and
                   m.payload["call_id"] == call_id for m in turn):
            raise ValueError("No pending approval for this call in the active turn")
        if any(m.kind in {"decision", "tool_result"} and
               m.payload["call_id"] == call_id for m in turn):
            raise ValueError("This tool call was already answered")
        self.apply((Effect("decision", {"call_id": call_id, "allow": allow},
                           agent_visible=False),))

    def compact_completed_turn(self, summary: str):
        """Demonstrate visibility only; summary is supplied, not model-generated."""
        if not any(m.kind == "final" for m in current_turn(self.load())):
            raise ValueError("Demo compaction is limited to completed turns")
        with self.db:
            self.db.execute("UPDATE messages SET agent_visible = 0")
            self.db.execute(
                "INSERT INTO messages(kind,payload,user_visible,agent_visible) "
                "VALUES ('summary',?,0,1)",
                (json.dumps({"text": summary}, ensure_ascii=False),),
            )


def current_turn(messages: list[Message]) -> list[Message]:
    for i in range(len(messages) - 1, -1, -1):
        if messages[i].kind == "user":
            return messages[i:]
    return []


def pending_requests(turn: list[Message]) -> list[Message]:
    answered = {m.payload["call_id"] for m in turn if m.kind == "tool_result"}
    return [m for m in turn if m.kind == "tool_request"
            and m.payload["call_id"] not in answered]


def count_words(arguments: dict) -> dict:
    text = arguments.get("text")
    if not isinstance(text, str):
        raise ValueError("text must be a string")
    return {"count": len(text.split())}


class Machine:
    def __init__(self, store: Store, tools: dict[str, Callable] | None = None,
                 cancelled: Callable[[], bool] = lambda: False):
        self.store = store
        self.tools = {"count_words": count_words} if tools is None else tools
        self.cancelled = cancelled
        self.operations = (self.stop, self.approve, self.execute, self.infer)

    def run(self, max_steps: int = 20) -> str:
        for _ in range(max_steps):
            if self.cancelled():
                return "cancelled"
            turn = current_turn(self.store.load())
            for operation in self.operations:
                result = operation(turn)
                if result is None:
                    continue
                self.store.apply(result.effects)
                if result.status:
                    return result.status
                break
            else:
                return "idle"
        raise RuntimeError("Step budget exhausted")

    @staticmethod
    def stop(turn):
        if any(m.kind == "final" for m in turn):
            return StepResult(status="completed")
        return None

    @staticmethod
    def approve(turn):
        decisions = {m.payload["call_id"] for m in turn if m.kind == "decision"}
        for request in pending_requests(turn):
            call_id = request.payload["call_id"]
            if call_id in decisions:
                continue
            asked = any(m.kind == "approval_requested" and
                        m.payload["call_id"] == call_id for m in turn)
            effects = () if asked else (
                Effect("approval_requested", {"call_id": call_id},
                       agent_visible=False),
            )
            return StepResult(effects, "waiting_for_approval")
        return None

    def execute(self, turn):
        decisions = {m.payload["call_id"]: m.payload["allow"]
                     for m in turn if m.kind == "decision"}
        for request in pending_requests(turn):
            data = request.payload
            call_id = data["call_id"]
            if call_id not in decisions:
                continue
            if self.cancelled():
                return StepResult(status="cancelled")
            if not decisions[call_id]:
                output = {"error": "User denied this call"}
            else:
                try:
                    output = self.tools[data["name"]](data["arguments"])
                except Exception as exc:
                    output = {"error": f"{type(exc).__name__}: {exc}"}
            # A real external side effect could succeed before this result commits.
            return StepResult((Effect("tool_result", {
                "call_id": call_id, "output": output,
            }),))
        return None

    @staticmethod
    def infer(turn):
        """A deterministic fake provider: request count_words, then report result."""
        if not turn:
            return None
        if not any(m.kind == "tool_request" for m in turn):
            return StepResult((Effect("tool_request", {
                "call_id": f"call-{turn[0].seq}",
                "name": "count_words",
                "arguments": {"text": turn[0].payload["text"]},
            }),))
        results = [m for m in turn if m.kind == "tool_result"]
        if results:
            output = results[-1].payload["output"]
            return StepResult((Effect("final", {"text": json.dumps(output)}),))
        return None


def demo():
    with tempfile.TemporaryDirectory(prefix="goose-state-demo-") as directory:
        path = Path(directory) / "session.db"
        store = Store(path)
        store.apply((Effect("user", {"text": "agents recover from persisted state"}),))
        print("First run:", Machine(store).run())
        call_id = next(m.payload["call_id"] for m in store.load()
                       if m.kind == "approval_requested")
        store.close()

        store = Store(path)
        store.answer(call_id, allow=True)
        print("After reconstruct + approve:", Machine(store).run())
        print("Persisted messages:")
        for message in store.load():
            print(f"  {message.seq}: {message.kind}: {message.payload}")
        store.compact_completed_turn("Word count finished: 5. No external changes.")
        messages = store.load()
        print("User-visible kinds:", [m.kind for m in messages if m.user_visible])
        print("Agent-visible kinds:", [m.kind for m in messages if m.agent_visible])
        store.close()


if __name__ == "__main__":
    demo()
