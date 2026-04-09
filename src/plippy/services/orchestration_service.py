from __future__ import annotations

import asyncio

from plippy.agents import Agent, DEFAULT_AGENT_REGISTRY, AgentContext
from plippy.schemas.orchestration import (
    AgentTaskRequest,
    AgentTaskResult,
    OrchestrationRequest,
    OrchestrationResponse,
)


class OrchestrationService:
    def __init__(self, registry: dict[str, Agent] | None = None) -> None:
        self._registry = registry or DEFAULT_AGENT_REGISTRY

    async def execute(self, request: OrchestrationRequest) -> OrchestrationResponse:
        results_by_id: dict[str, dict[str, object]] = {}
        ordered_results: list[AgentTaskResult] = []

        for step in request.steps:
            if step.execution == "parallel":
                step_results = await asyncio.gather(
                    *(self._run_task(task, results_by_id) for task in step.tasks)
                )
                for result in step_results:
                    ordered_results.append(result)
                    results_by_id[result.id] = {
                        "agent": result.agent,
                        "output": result.output,
                    }
            else:
                for task in step.tasks:
                    result = await self._run_task(task, results_by_id)
                    ordered_results.append(result)
                    results_by_id[result.id] = {
                        "agent": result.agent,
                        "output": result.output,
                    }

        return OrchestrationResponse(results=ordered_results)

    async def _run_task(
        self,
        task: AgentTaskRequest,
        results_by_id: dict[str, dict[str, object]],
    ) -> AgentTaskResult:
        agent = self._registry.get(task.agent)
        if agent is None:
            raise ValueError(f"Unknown agent: {task.agent}")

        context = AgentContext(results=results_by_id)
        agent_result = await agent.run(task.payload, context)
        return AgentTaskResult(id=task.id, agent=task.agent, output=agent_result.output)
