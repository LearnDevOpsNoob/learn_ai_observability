from src.observability.tracing import get_current_trace_id
from src.api.schemas import (
    ChatResponse,
    SourceResponse,
    ChatMetadataResponse,
    TokenUsageResponse,
)
from src.rag.pipeline import RAGPipeline

from opentelemetry.trace import Status, StatusCode
from src.observability.tracing import get_tracer

from time import perf_counter

from src.config.logging import get_logger

logger = get_logger(__name__)

tracer = get_tracer()

class ChatService:
    def __init__(self, pipeline: RAGPipeline):
        self.pipeline = pipeline

    def chat(self, question: str) -> ChatResponse:

        start = perf_counter()

        with tracer.start_as_current_span("chat_service") as span:
            span.set_attribute("question.length", len(question))

            logger.info("Chat request started.")    

            try:
                response = self.pipeline.ask(question)

                duration = (perf_counter() - start) * 1000

                span.set_attribute("chat.duration_ms", duration)
                span.set_attribute("llm.model", response.model)
                span.set_attribute(
                    "retrieval.results",
                    len(response.retrieved_chunks),
                )

                span.set_status(Status(StatusCode.OK))
                logger.info("Chat request completed in %.2f ms.", duration)


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
            except Exception as e:
                span.record_exception(e)
                span.set_status(Status(StatusCode.ERROR))

                logger.exception("Chat request failed.")
                raise