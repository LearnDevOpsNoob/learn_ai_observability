from src.api.schemas import (
    ChatResponse,
    SourceResponse,
    ChatMetadataResponse,
    TokenUsageResponse,
)
from src.rag.pipeline import RAGPipeline

from time import perf_counter

from src.config.logging import get_logger

logger = get_logger(__name__)

class ChatService:
    def __init__(self, pipeline: RAGPipeline):
        self.pipeline = pipeline

    def chat(self, question: str) -> ChatResponse:
        logger.info("Chat request started.")

        start = perf_counter()

        response = self.pipeline.ask(question)

        duration = perf_counter() - start

        logger.info(
            "Chat request completed in %.2f ms.",
            duration * 1000,
        )
        
        return ChatResponse(
            answer=response.answer,
            sources=[
                SourceResponse(
                    source=chunk.source,
                    score=chunk.score,
                )
                for chunk in response.retrieved_chunks
            ],
            metadata=ChatMetadataResponse(
                model=response.model,
                token_usage=TokenUsageResponse(
                    prompt_tokens=response.prompt_tokens,
                    completion_tokens=response.completion_tokens,
                    total_tokens=response.total_tokens,
                ),
            ),
        )