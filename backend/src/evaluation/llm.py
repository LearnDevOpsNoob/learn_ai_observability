from openai import AsyncOpenAI
from ragas.llms import llm_factory

from src.config.config import settings

client = AsyncOpenAI(
    api_key=settings.evaluation_llm_api_key,
    base_url=settings.evaluation_llm_api_endpoint
)

evaluation_llm = llm_factory(
    settings.evaluation_llm_model,
    provider="openai",
    client=client
)