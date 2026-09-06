"""A small production-shaped LangChain v1 agent.

The external ticket system is deliberately replaced with an in-memory Store.  The
important parts are real: typed runtime context, injected ToolRuntime, bounded
model calls, selective retry, human approval, checkpoint/resume, and structured
output.
"""

from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Literal
from uuid import uuid4

from langchain.agents import create_agent
from langchain.agents.middleware import (
    HumanInTheLoopMiddleware,
    ModelCallLimitMiddleware,
    ModelRetryMiddleware,
    ToolRetryMiddleware,
)
from langchain.agents.structured_output import ToolStrategy
from langchain.tools import ToolRuntime, tool
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore
from langgraph.types import Command
from pydantic import BaseModel, Field


@dataclass(frozen=True)
class RequestContext:
    """Immutable, request-scoped identity and authorization context."""

    tenant_id: str
    user_id: str
    can_create_ticket: bool = True


class IncidentAssessment(BaseModel):
    """The business object expected from the agent."""

    summary: str = Field(description="One-sentence incident summary")
    severity: Literal["sev1", "sev2", "sev3", "sev4"]
    evidence: list[str]
    recommended_actions: list[str]
    ticket_id: str | None = None


RUNBOOKS = {
    "checkout": "Check payment-provider latency, DB pool saturation, and recent deploys.",
    "search": "Check index freshness, query timeout rate, and shard imbalance.",
}


def _context(runtime: ToolRuntime) -> RequestContext:
    context = runtime.context
    if not isinstance(context, RequestContext):
        raise TypeError("RequestContext was not injected")
    return context


@tool
def lookup_runbook(service: Literal["checkout", "search"], runtime: ToolRuntime) -> str:
    """Read the approved operations runbook for a service."""

    context = _context(runtime)
    return f"tenant={context.tenant_id}; runbook={RUNBOOKS[service]}"


@tool
def create_incident_ticket(
    title: str,
    severity: Literal["sev1", "sev2", "sev3", "sev4"],
    runtime: ToolRuntime,
) -> str:
    """Create an incident ticket after a human has approved the action."""

    context = _context(runtime)
    if not context.can_create_ticket:
        raise PermissionError("caller is not allowed to create tickets")
    if runtime.store is None:
        raise RuntimeError("a persistent store is required")

    ticket_id = f"INC-{uuid4().hex[:8].upper()}"
    runtime.store.put(
        ("incident-tickets", context.tenant_id),
        ticket_id,
        {
            "title": title,
            "severity": severity,
            "created_by": context.user_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
        },
    )
    return ticket_id


def build_agent(model_id: str):
    """Build and compile the graph once; reuse it across requests."""

    return create_agent(
        model=model_id,
        tools=[lookup_runbook, create_incident_ticket],
        system_prompt=(
            "You are an incident triage agent. Inspect the relevant runbook before "
            "making a recommendation. Create a ticket only when the user explicitly "
            "asks for one. Never invent evidence or ticket IDs."
        ),
        middleware=[
            ModelCallLimitMiddleware(run_limit=8, exit_behavior="error"),
            ModelRetryMiddleware(max_retries=2, on_failure="error"),
            # Reads may be retried. A write tool is deliberately excluded.
            ToolRetryMiddleware(
                tools=["lookup_runbook"], max_retries=2, on_failure="error"
            ),
            HumanInTheLoopMiddleware(
                interrupt_on={
                    "create_incident_ticket": {
                        "allowed_decisions": ["approve", "edit", "reject"]
                    }
                }
            ),
        ],
        # ToolStrategy is portable across providers and validates with Pydantic.
        response_format=ToolStrategy(IncidentAssessment),
        context_schema=RequestContext,
        checkpointer=InMemorySaver(),
        store=InMemoryStore(),
        name="incident-triage-agent",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "question",
        nargs="?",
        default="Checkout errors doubled after the last deploy. Investigate and create a ticket.",
    )
    parser.add_argument(
        "--approve-ticket",
        action="store_true",
        help="Automatically approve the demo ticket action (never do this in production).",
    )
    args = parser.parse_args()

    model_id = os.environ.get("LANGCHAIN_MODEL")
    if not model_id:
        parser.error("set LANGCHAIN_MODEL to a provider:model identifier")

    agent = build_agent(model_id)
    config = {"configurable": {"thread_id": f"demo:{uuid4().hex}"}}
    context = RequestContext(tenant_id="acme", user_id="engineer-42")

    result = agent.invoke(
        {"messages": [{"role": "user", "content": args.question}]},
        config=config,
        context=context,
    )

    if "__interrupt__" in result:
        print("Approval required:", result["__interrupt__"])
        if not args.approve_ticket:
            print("Run again with --approve-ticket to exercise the resume path.")
            return
        result = agent.invoke(
            Command(resume={"decisions": [{"type": "approve"}]}),
            config=config,
            context=context,
        )

    assessment = result.get("structured_response")
    if isinstance(assessment, IncidentAssessment):
        print(assessment.model_dump_json(indent=2))
    else:
        raise RuntimeError(f"agent did not produce IncidentAssessment: {result!r}")


if __name__ == "__main__":
    main()
