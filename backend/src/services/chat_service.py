from src.observability.tracing import get_current_trace_id
# from src.observability.langfuse import get_langfuse
from src.api.schemas import (
    ChatResponse,
    SourceResponse,
    ChatMetadataResponse,
    TokenUsageResponse,
)
from src.rag.pipeline import RAGPipeline
from src.config.config import settings
from src.observability.tracing import trace_step

from opentelemetry import trace

from time import perf_counter

from src.config.logging import get_logger

logger = get_logger(__name__)

class ChatService:
    def __init__(self, pipeline: RAGPipeline):
        self.pipeline = pipeline
        # self.langfuse = get_langfuse()

    @trace_step("chat_request")
    def chat(self, question: str) -> ChatResponse:

        start = perf_counter()

        span = trace.get_current_span()
        span.set_attribute("question.length", len(question))
        
        logger.info("Chat request started.")

        # with self.langfuse.propagate_attributes(
        #     metadata={
        #         "provider": settings.llm_provider,
        #         "model": settings.llm_model
        #     }
        # ):
        response = self.pipeline.ask(question)

        duration = (perf_counter() - start) * 1000

        span.set_attribute("chat.duration_ms", duration)
        span.set_attribute("llm.model", response.model)
        span.set_attribute("retrieval.results", len(response.retrieved_chunks))
        span.set_attribute("llm.total_tokens", response.total_tokens)

        logger.info(
            "Chat request completed | endpoint=/chat | provider=%s | model=%s | retrieval=%d | duration=%.2f ms",
            settings.llm_provider,
            response.model,
            len(response.retrieved_chunks),
            duration,
        )

        # print('=================TRACE ID=================')
        # print("IN SERVICE:", get_current_trace_id())

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
                trace_id=get_current_trace_id()
            ),
        )