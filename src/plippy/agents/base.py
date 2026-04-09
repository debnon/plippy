from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(slots=True)
class AgentContext:
    results: dict[str, dict[str, Any]]


@dataclass(slots=True)
class AgentResult:
    output: dict[str, Any]


class Agent(Protocol):
    async def run(self, payload: dict[str, Any], context: AgentContext) -> AgentResult:
        ...
