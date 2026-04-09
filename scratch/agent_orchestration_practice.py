"""Scratchpad for practicing agent orchestration concepts.

Run:
    /home/ben/Repos/plippy/.venv/bin/python scratch/agent_orchestration_practice.py

What this file demonstrates:
- Parallel vs sequential task execution
- Shared result synchronization across steps
- Simple agent registry and dispatch
- A place to experiment with conflict detection and review workflows
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(slots=True)
class AgentContext:
    # results[task_id] = {"agent": str, "output": dict[str, Any]}
    results: dict[str, dict[str, Any]]


@dataclass(slots=True)
class AgentResult:
    output: dict[str, Any]


class Agent(Protocol):
    async def run(self, payload: dict[str, Any], context: AgentContext) -> AgentResult:
        ...


@dataclass(slots=True)
class AgentTask:
    id: str
    agent: str
    payload: dict[str, Any]


@dataclass(slots=True)
class Step:
    execution: str  # "parallel" | "sequential"
    tasks: list[AgentTask]


class EchoAgent:
    async def run(self, payload: dict[str, Any], context: AgentContext) -> AgentResult:
        _ = context
        text = str(payload.get("text", ""))
        await asyncio.sleep(float(payload.get("sleep_seconds", 0)))
        return AgentResult(output={"text": text})


class JoinAgent:
    async def run(self, payload: dict[str, Any], context: AgentContext) -> AgentResult:
        task_ids = payload.get("task_ids", [])
        separator = str(payload.get("separator", "\n"))
        texts: list[str] = []
        for task_id in task_ids:
            item = context.results.get(str(task_id), {})
            output = item.get("output", {})
            texts.append(str(output.get("text", "")))
        return AgentResult(output={"text": separator.join(texts)})


class TemplateAgent:
    async def run(self, payload: dict[str, Any], context: AgentContext) -> AgentResult:
        template = str(payload.get("template", ""))
        rendered = template
        for task_id, item in context.results.items():
            output = item.get("output", {})
            rendered = rendered.replace(f"{{{{{task_id}.text}}}}", str(output.get("text", "")))
        return AgentResult(output={"text": rendered})


class Orchestrator:
    def __init__(self, registry: dict[str, Agent]) -> None:
        self.registry = registry

    async def execute(self, steps: list[Step]) -> list[dict[str, Any]]:
        results_by_id: dict[str, dict[str, Any]] = {}
        ordered: list[dict[str, Any]] = []

        for step in steps:
            if step.execution == "parallel":
                batch = await asyncio.gather(
                    *(self._run_task(task, results_by_id) for task in step.tasks)
                )
                for result in batch:
                    ordered.append(result)
                    results_by_id[result["id"]] = {
                        "agent": result["agent"],
                        "output": result["output"],
                    }
            elif step.execution == "sequential":
                for task in step.tasks:
                    result = await self._run_task(task, results_by_id)
                    ordered.append(result)
                    results_by_id[result["id"]] = {
                        "agent": result["agent"],
                        "output": result["output"],
                    }
            else:
                raise ValueError(f"Unknown execution mode: {step.execution}")

        return ordered

    async def _run_task(
        self,
        task: AgentTask,
        results_by_id: dict[str, dict[str, Any]],
    ) -> dict[str, Any]:
        agent = self.registry.get(task.agent)
        if agent is None:
            raise ValueError(f"Unknown agent: {task.agent}")

        context = AgentContext(results=results_by_id)
        result = await agent.run(task.payload, context)
        return {"id": task.id, "agent": task.agent, "output": result.output}


def build_default_registry() -> dict[str, Agent]:
    return {
        "echo": EchoAgent(),
        "join": JoinAgent(),
        "template": TemplateAgent(),
    }


async def demo() -> None:
    orchestrator = Orchestrator(build_default_registry())

    steps = [
        Step(
            execution="parallel",
            tasks=[
                AgentTask("research", "echo", {"text": "Found 3 key points", "sleep_seconds": 0.3}),
                AgentTask("calc", "echo", {"text": "Computed confidence 0.82", "sleep_seconds": 0.1}),
            ],
        ),
        Step(
            execution="sequential",
            tasks=[
                AgentTask(
                    "combined",
                    "template",
                    {
                        "template": "Summary: {{research.text}} | Metrics: {{calc.text}}",
                    },
                ),
                AgentTask(
                    "final",
                    "join",
                    {
                        "task_ids": ["research", "calc", "combined"],
                        "separator": "\n",
                    },
                ),
            ],
        ),
    ]

    results = await orchestrator.execute(steps)
    print("=== Ordered Results ===")
    for item in results:
        print(f"- {item['id']} ({item['agent']}): {item['output']}")

    print("\n=== Practice TODOs ===")
    print("1. Add a ConflictDetectorAgent that compares two task outputs.")
    print("2. Add a ReviewQueue list when outputs contain low confidence.")
    print("3. Add a WebFetchAgent and enforce host allowlist.")
    print("4. Add a PdfExtractAgent with path safety checks.")


if __name__ == "__main__":
    asyncio.run(demo())
