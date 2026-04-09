from fastapi import APIRouter

from plippy.schemas.orchestration import OrchestrationRequest, OrchestrationResponse
from plippy.services.orchestration_service import OrchestrationService


router = APIRouter(prefix="/orchestrations", tags=["orchestrations"])


@router.post("/execute", response_model=OrchestrationResponse)
async def execute_orchestration(payload: OrchestrationRequest) -> OrchestrationResponse:
    service = OrchestrationService()
    return await service.execute(payload)
