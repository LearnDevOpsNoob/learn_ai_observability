from openai import OpenAI

from src.config.config import settings

from opentelemetry import trace 

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
        span = trace.get_current_span()

        span.set_attribute("embedding.provider", settings.embedding_provider)
        span.set_attribute("embedding.model", self.MODEL_NAME)
        span.set_attribute("embedding.input_length", len(text))
        span.set_attribute("embedding.dimensions", self.DIMENSIONS)

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
        span = trace.get_current_span()

        span.set_attribute("embedding.provider", settings.embedding_provider)
        span.set_attribute("embedding.model", self.MODEL_NAME)
        span.set_attribute("embedding.batch_size", len(texts))
        span.set_attribute("embedding.dimensions", self.DIMENSIONS)

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




    