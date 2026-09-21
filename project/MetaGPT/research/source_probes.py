"""隔离执行固定上游源码中的方法体；外围对象用替身，不是完整 MetaGPT 集成测试。"""
from __future__ import annotations

import argparse
import ast
import asyncio
import copy
import inspect
import json
import subprocess
import traceback
from dataclasses import dataclass, field
from pathlib import Path
from types import SimpleNamespace as NS

COMMIT = "11cdf466d042aece04fc6cfd13b28e1a70341b1f"


class NullLogger:
    def __getattr__(self, name):
        return lambda *args, **kwargs: None


@dataclass
class Message:
    content: str = ""
    id: str = "1"
    cause_by: str = "UserRequirement"
    send_to: set = field(default_factory=lambda: {"<all>"})
    sent_from: str = ""
    role: str = "user"

    def dump(self):
        return repr(self)


class Memory:
    def __init__(self):
        self.items = []

    def get(self):
        return self.items[:]

    def add(self, item):
        if item not in self.items:
            self.items.append(item)

    def add_batch(self, items):
        for item in items:
            self.add(item)


class Buffer:
    def __init__(self, items):
        self.items = list(items)

    def pop_all(self):
        items, self.items = self.items, []
        return items


def load_method(root, relative, owner, method):
    """从原始 AST 提取方法体，只移除装饰器并延迟解析类型注解。"""
    tree = ast.parse((root / relative).read_text())
    nodes = tree.body
    if owner:
        nodes = next(node for node in nodes if isinstance(node, ast.ClassDef) and node.name == owner).body
    node = copy.deepcopy(next(node for node in nodes if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == method))
    node.decorator_list = []
    module = ast.Module(body=[ast.ImportFrom(module="__future__", names=[ast.alias(name="annotations")], level=0), node], type_ignores=[])
    scope = {"logger": NullLogger(), "asyncio": asyncio, "Message": Message, "MESSAGE_ROUTE_TO_ALL": "<all>", "inspect": inspect, "traceback": traceback, "TEAMLEADER_NAME": "Mike"}
    exec(compile(ast.fix_missing_locations(module), str(root / relative), "exec"), scope)
    return scope[method]


def role(message, watch=(), observe_all=False, old=()):
    memory = Memory()
    memory.add_batch(old)
    return NS(name="Bob", _setting="Bob", recovered=False, latest_observed_msg=None,
              enable_memory=True, observe_all_msg_from_buffer=observe_all,
              rc=NS(memory=memory, msg_buffer=Buffer([message]), watch=set(watch), news=[]))


async def probe(root: Path):
    results = []

    def check(name, condition):
        if not condition:
            raise AssertionError(name)
        results.append({"name": name, "status": "passed"})

    route = load_method(root, "metagpt/utils/common.py", None, "is_send_to")
    observe = load_method(root, "metagpt/roles/role.py", "Role", "_observe")
    check("broadcast reaches any address", route(Message(), {"Bob"}))
    check("unicast excludes unrelated address", not route(Message(send_to={"Alice"}), {"Bob"}))

    r = role(Message(cause_by="WritePRD"), watch={"WritePRD"})
    check("watched cause triggers reaction", await observe(r) == 1)
    r = role(Message(cause_by="Other", send_to={"Bob"}))
    check("explicit name bypasses watch", await observe(r) == 1)
    message = Message(cause_by="Other", send_to={"metagpt.roles.architect.Architect"})
    r = role(message)
    check("class address delivers but does not itself trigger observe", route(message, message.send_to) and await observe(r) == 0)
    r = role(Message(cause_by="Other"), observe_all=True)
    check("observe_all stores unwatched message without triggering", await observe(r) == 0 and len(r.rc.memory.get()) == 1)
    message = Message(cause_by="WritePRD")
    r = role(message, watch={"WritePRD"}, old=[message])
    check("equal existing message is ignored", await observe(r) == 0)
    r = role(Message(cause_by="WritePRD", id="2"), watch={"WritePRD"}, old=[message])
    check("new id with same content is not deduplicated", await observe(r) == 1)

    env_run = load_method(root, "metagpt/environment/base_env.py", "Environment", "run")
    events = []
    later = NS(is_idle=True)

    async def later_run():
        events.append("B")
        later.is_idle = True

    async def first_run():
        events.append("A")
        later.is_idle = False
        first.is_idle = True

    later.run = later_run
    first = NS(is_idle=False, run=first_run)
    env = NS(roles={"A": first, "B": later}, is_idle=False)
    await env_run(env)
    check("idle role awakened during a sweep waits for next sweep", events == ["A"])
    await env_run(env)
    check("next sweep runs awakened role", events == ["A", "B"])

    start = load_method(root, "metagpt/team.py", "Team", "run_project")
    sent = []
    team = NS(env=NS(publish_message=sent.append))
    start(team, "example", send_to="Bob")
    check("run_project ignores its send_to argument in this snapshot", sent[0].send_to == {"<all>"})

    commands = load_method(root, "metagpt/roles/di/role_zero.py", "RoleZero", "_run_commands")
    effects = []

    def fail():
        raise ValueError("intentional tool failure")

    executor = NS(_is_special_command=lambda cmd: False, tool_execution_map={"first": lambda: effects.append("first"), "fail": fail, "last": lambda: effects.append("last")})
    output = await commands(executor, [{"command_name": name, "args": {}} for name in ("first", "fail", "last")])
    check("failed tool stops remaining commands without rolling back first", effects == ["first"] and "ValueError" in output)
    effects.clear()
    await commands(executor, [{"command_name": name, "args": {}} for name in ("missing", "last")])
    check("unknown command stops the command batch", effects == [])

    publish = load_method(root, "metagpt/environment/mgx/mgx_env.py", "MGXEnv", "publish_message")
    deliveries = []
    mgx = NS(attach_images=lambda msg: msg, get_role=lambda name: NS(name="Mike", profile="Team Leader"), direct_chat_roles=set(), is_public_chat=True, history=Memory(), _publish_message=deliveries.append)
    publish(mgx, Message(cause_by="RunCommand", send_to={"Bob"}))
    check("ordinary MGX message also targets team leader", deliveries[0].send_to == {"Mike", "Bob"})
    deliveries.clear()
    publish(mgx, Message(send_to={"no one"}), publicer="Team Leader")
    check("team leader dummy output is suppressed", deliveries == [])
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    actual = subprocess.check_output(["git", "-C", str(args.source), "rev-parse", "HEAD"], text=True).strip()
    if actual != COMMIT:
        raise SystemExit(f"需要固定提交 {COMMIT}，实际为 {actual}")
    results = asyncio.run(probe(args.source))
    report = {"commit": actual, "scope": "isolated upstream method bodies with test doubles; not upstream integration tests", "passed": len(results), "results": results}
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))
