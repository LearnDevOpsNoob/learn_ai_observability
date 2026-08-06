from openai import OpenAI

from src.config.config import settings

from src.config.logging import get_logger

logger = get_logger(__name__)

class OpenAIEmbedding:
    """Service responsible for generating text embeddings."""

    MODEL_NAME = settings.embedding_model
    DIMENSIONS = settings.vector_size

    def __init__(self):
        self.client = OpenAI(
            api_key=settings.embedding_api_key,
            base_url=settings.embedding_api_endpoint
        )

    def embed(self, text: str) -> list[float]:
        """
        Generate an embedding for the given text.
        """

        response = self.client.embeddings.create(
            model=self.MODEL_NAME,
            input=text
        )

        embedding = response.data[0].embedding

        logger.info(
            "Embedding model=%s length=%d",
            self.MODEL_NAME,
            len(embedding),
        )
        return embedding

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        response = self.client.embeddings.create(
            model=self.MODEL_NAME,
            input=texts,
        )

        embeddings = [item.embedding for item in response.data]

        logger.info(
            "Embedding model=%s batch_size=%d dimensions=%d",
            self.MODEL_NAME,
            len(embeddings),
            len(embeddings[0]) if embeddings else 0,
        )

        return embeddings

    @property
    def dimensions(self) -> int:
        return self.DIMENSIONS




    