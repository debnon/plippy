from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class AgentTaskRequest(BaseModel):
    id: str = Field(min_length=1)
    agent: str = Field(min_length=1)
    payload: dict[str, Any] = Field(default_factory=dict)


class OrchestrationStepRequest(BaseModel):
    execution: Literal["parallel", "sequential"]
    tasks: list[AgentTaskRequest] = Field(min_length=1)


class OrchestrationRequest(BaseModel):
    steps: list[OrchestrationStepRequest] = Field(min_length=1)


class AgentTaskResult(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    agent: str
    output: dict[str, Any]


class OrchestrationResponse(BaseModel):
    results: list[AgentTaskResult]
