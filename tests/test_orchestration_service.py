import asyncio

from plippy.schemas.orchestration import OrchestrationRequest
from plippy.services.orchestration_service import OrchestrationService


def test_orchestration_service_runs_parallel_then_combines_results() -> None:
    request = OrchestrationRequest.model_validate(
        {
            "steps": [
                {
                    "execution": "parallel",
                    "tasks": [
                        {"id": "agent_a", "agent": "echo", "payload": {"text": "alpha"}},
                        {"id": "agent_b", "agent": "echo", "payload": {"text": "beta"}},
                    ],
                },
                {
                    "execution": "sequential",
                    "tasks": [
                        {
                            "id": "combine",
                            "agent": "join",
                            "payload": {"task_ids": ["agent_a", "agent_b"], "separator": ", "},
                        }
                    ],
                },
            ]
        }
    )

    service = OrchestrationService()
    response = asyncio.run(service.execute(request))

    assert len(response.results) == 3
    assert response.results[2].output["text"] == "alpha, beta"


def test_orchestration_service_supports_template_fan_in() -> None:
    request = OrchestrationRequest.model_validate(
        {
            "steps": [
                {
                    "execution": "sequential",
                    "tasks": [
                        {"id": "first", "agent": "echo", "payload": {"text": "research"}},
                        {"id": "second", "agent": "template", "payload": {"template": "Result: {{first.text}}"}},
                    ],
                }
            ]
        }
    )

    service = OrchestrationService()
    response = asyncio.run(service.execute(request))

    assert response.results[-1].output["text"] == "Result: research"