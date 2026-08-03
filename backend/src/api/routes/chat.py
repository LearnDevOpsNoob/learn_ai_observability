from fastapi import APIRouter, Depends
from src.api.schemas import ChatRequest, ChatResponse
from src.services.chat_service import ChatService
from src.api.dependencies import get_chat_service

from src.config.logging import get_logger

router = APIRouter(prefix="/chat", tags=["Chat"])

logger = get_logger(__name__)

@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest, chat_service: ChatService = Depends(get_chat_service)):
    logger.info("Received POST /chat request.")

    # return chat_service.chat(request.question)
    try:
        return chat_service.chat(request.question)
        
    except Exception as e:
        logger.exception("Failed while generating AI response.")
        raise    



