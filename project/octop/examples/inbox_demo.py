#!/usr/bin/env python3
"""Teaching model of Octop/Harness background collaboration, NOT their SDK.

Pure stdlib; no models, credentials, shell execution or network. A fake Agent
returns strings. The demo deliberately keeps its queue in memory and serial.
History below is also in memory: it does not simulate LangGraph persistence.
"""
import asyncio
import json
from dataclasses import dataclass, field


@dataclass
class Job:
    id: str
    source: str
    target: str
    parent_thread: str
    prompt: str
    status: str = "queued"
    error: str | None = None


@dataclass
class FakeRuntime:
    history: dict[str, list[str]] = field(default_factory=dict)
    calls: list[tuple[str, str]] = field(default_factory=list)
    active: int = 0
    max_active: int = 0

    async def call(self, agent, thread, prompt):
        self.active += 1
        self.max_active = max(self.max_active, self.active)
        self.calls.append((agent, thread))
        try:
            await asyncio.sleep(0)
            if agent == "failing-expert":
                raise RuntimeError("模拟专家失败")
            reply = f"{agent}: {prompt}"
            self.history.setdefault(thread, []).append(reply)
            return reply
        finally:
            self.active -= 1


class Inbox:
    def __init__(self, runtime):
        self.runtime = runtime
        self.queue = asyncio.Queue()
        self.pending = {}
        self.notifications = []
        self.transitions = []
        self.sequence = 0

    def submit(self, source, target, parent_thread, prompt):
        self.sequence += 1
        job = Job(f"job-{self.sequence}", source, target, parent_thread, prompt)
        self.pending[job.id] = job
        self.queue.put_nowait(job)
        self.transitions.append((job.id, "queued"))
        return job.id

    def transition(self, job, status):
        job.status = status
        self.transitions.append((job.id, status))

    async def drain(self):
        # One consumer models the pinned upstream's single inbox worker.
        while not self.queue.empty():
            job = self.queue.get_nowait()
            try:
                self.transition(job, "running")
                try:
                    child_thread = f"{job.parent_thread}/peer/{job.target}"
                    result = await self.runtime.call(job.target, child_thread, job.prompt)
                except RuntimeError as exc:
                    job.error = str(exc)
                    result = f"子任务失败：{job.error}"
                self.transition(job, "replying")
                reply = await self.runtime.call(job.source, job.parent_thread, f"结合原问题汇总：{result}")
                self.transition(job, "failed" if job.error else "done")
                self.notifications.append({"job": job.id, "thread": job.parent_thread, "status": job.status, "text": job.error or reply})
                del self.pending[job.id]
            finally:
                self.queue.task_done()


async def demo():
    runtime = FakeRuntime()
    inbox = Inbox(runtime)
    ids = [inbox.submit("主助手", expert, "thread-parent", f"整理{topic}") for expert, topic in [("检索专家", "源码证据"), ("架构专家", "实现边界")]]
    # Submission returns before any Agent call runs.
    print(json.dumps({"submitted": ids, "agent_calls_so_far": len(runtime.calls)}, ensure_ascii=False))
    await inbox.drain()
    print(json.dumps({"transitions": inbox.transitions, "calls": runtime.calls,
                      "max_concurrent_agent_calls": runtime.max_active, "notifications": inbox.notifications}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    asyncio.run(demo())
