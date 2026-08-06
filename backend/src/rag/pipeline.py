from opentelemetry import trace

from src.prompt.builder import PromptBuilder
from src.retrieval.retrieval import RetrievalPipeline
from src.llm.llm_provider import LLMService
from src.models.chat import ChatResponse
from src.models.rag import RAGResponse

from src.config.metrics import RAG_QUERIES_TOTAL
from src.observability.tracing import get_tracer

from src.config.logging import get_logger

logger = get_logger(__name__)

class RAGPipeline:
    def __init__(self):
        self.retrieval_pipeline = RetrievalPipeline()
        self.prompt_builder = PromptBuilder()
        self.llm = LLMService()
        self.tracer = get_tracer()

    def ask(self, question: str) -> ChatResponse:
        logger.info("Starting RAG pipeline.")

        RAG_QUERIES_TOTAL.inc()
        
        try:
            with self.tracer.start_as_current_span("retrieve_documents"):
                logger.info("Retrieving relevant documents.")
                chunks = self.retrieval_pipeline.search(question)

            with self.tracer.start_as_current_span("build_prompt"):
                logger.info("Building prompt.")
                messages = self.prompt_builder.build(question=question, chunks=chunks)

            with self.tracer.start_as_current_span("llm_generation"):
                logger.info("Generating LLM response.")
                llm_response = self.llm.generate(messages)

            with self.tracer.start_as_current_span("build_response"):
                logger.info("Building response.")
                response = RAGResponse(
                    answer=llm_response.answer,
                    model=llm_response.model,
                    prompt_tokens=llm_response.prompt_tokens,
                    completion_tokens=llm_response.completion_tokens,
                    total_tokens=llm_response.total_tokens,
                    retrieved_chunks=chunks,
                )
            logger.info("RAG pipeline completed.")
            return response

        except Exception:
            logger.exception("RAG pipeline execution failed.")
            raise
