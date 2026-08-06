from fastapi import APIRouter
from src.api.schemas import HealthResponse

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("", response_model=HealthResponse)
async def health_check():
    return HealthResponse(status="healthy")
