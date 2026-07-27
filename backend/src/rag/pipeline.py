from src.prompt.builder import PromptBuilder
from src.retrieval.retrieval import RetrievalPipeline
from src.llm.openai_llm import OpenAIChat
from src.models.chat import ChatResponse
from src.models.rag import RAGResponse

from src.config.logging import get_logger

logger = get_logger(__name__)

class RAGPipeline:
    def __init__(self):
        self.retrieval_pipeline = RetrievalPipeline()
        self.prompt_builder = PromptBuilder()
        self.llm = OpenAIChat()

    def ask(self, question: str) -> ChatResponse:
        logger.info("Starting RAG pipeline.")

        try:
            logger.info("Retrieving relevant documents.")
            chunks = self.retrieval_pipeline.search(question)
    
            logger.info("Building prompt.")
            messages = self.prompt_builder.build(question=question, chunks=chunks)
    
            logger.info("Generating LLM response.")
            llm_response = self.llm.generate(messages)
    
            logger.info("RAG pipeline completed.")
            return RAGResponse(
                answer=llm_response.answer,
                model=llm_response.model,
                prompt_tokens=llm_response.prompt_tokens,
                completion_tokens=llm_response.completion_tokens,
                total_tokens=llm_response.total_tokens,
                retrieved_chunks=chunks,
            )

        except Exception:
            logger.exception("RAG pipeline execution failed.")
            raise


        