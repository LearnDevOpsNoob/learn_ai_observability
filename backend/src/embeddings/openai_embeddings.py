from openai import OpenAI

from src.config.config import settings


class OpenAIEmbedding:
    """Service responsible for generating text embeddings."""

    MODEL_NAME = settings.openai_embed_model
    DIMENSIONS = 1536

    def __init__(self):
        self.client = OpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.openai_api_endpoint
        )

    def embed(self, text: str) -> list[float]:
        """
        Generate an embedding for the given text.
        """

        response = self.client.embeddings.create(
            model=self.MODEL_NAME,
            input=text,
        )

        return response.data[0].embedding

    @property
    def dimensions(self) -> int:
        return self.DIMENSIONS




    