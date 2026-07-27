from src.embeddings.openai_embeddings import OpenAIEmbedding
from src.db.vectordb import VectorDB
from src.config.config import TOP_K, SCORE_THRESHOLD

from time import perf_counter

from src.config.metrics import (
    RETRIEVAL_DURATION,
    RETRIEVED_CHUNKS_TOTAL
)


from src.config.logging import get_logger

logger = get_logger(__name__)

class RetrievalPipeline:
    def __init__(self):
        self.embedder = OpenAIEmbedding()
        self.vectordb = VectorDB()


    def search(self, question: str):
        embedding = self.embedder.embed(question)
        logger.info("Searching knowledge base.")

        start_time = perf_counter()

        try:
            results = self.vectordb.similarity_search(
                query_vector=embedding,
                limit=TOP_K,
                score_threshold=SCORE_THRESHOLD
            )    

            RETRIEVED_CHUNKS_TOTAL.inc(len(results))

            logger.info("Retrieved %d relevant chunks.", len(results))
            return results
        except Exception:
            logger.exception("Knowledge base retrieval failed.")
            raise
        finally:
            RETRIEVAL_DURATION.observe(perf_counter() - start_time)

