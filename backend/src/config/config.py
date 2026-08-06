from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()

@dataclass(frozen=True)
class Settings:
    llm_provider: str
    llm_api_key: str
    llm_api_endpoint: str
    llm_model: str

    llm_temperature: float
    llm_max_tokens: int
    llm_top_p: float

    embedding_provider: str
    embedding_api_key: str
    embedding_api_endpoint: str
    embedding_model: str
    vector_size: int

    qdrant_url: str
    collection_name: str

    langfuse_public_key: str
    langfuse_secret_key: str
    langfuse_base_url: str


settings = Settings(
    # LLM
    llm_provider=os.getenv("LLM_PROVIDER", "groq"),
    llm_api_key=os.getenv("GROQ_API_KEY", ""),
    llm_api_endpoint=os.getenv("LLM_API_ENDPOINT", ""),
    llm_model=os.getenv("LLM_MODEL", ""),

    llm_temperature=float(os.getenv("LLM_TEMPERATURE", "0.2")),
    llm_max_tokens=int(os.getenv("LLM_MAX_TOKENS", "2048")),
    llm_top_p=float(os.getenv("LLM_TOP_P", "1.0")),

    # Embeddings
    embedding_provider=os.getenv("EMBED_PROVIDER", ""),
    embedding_api_key=os.getenv("JINAAI_API_KEY", ""),
    embedding_api_endpoint=os.getenv("EMBEDDING_API_ENDPOINT", ""),
    embedding_model=os.getenv("EMBEDDING_MODEL", ""),
    vector_size=int(
        os.getenv("EMBEDDING_DIMENSIONS", 1024)
    ),

    qdrant_url=os.getenv("QDRANT_URL", "http://localhost:6333"),
    collection_name=os.getenv("QDRANT_COLLECTION", "research_docs"),   

    # Langfuse Setup
    langfuse_public_key=os.getenv("LANGFUSE_PUBLIC_KEY", ""),
    langfuse_secret_key=os.getenv("LANGFUSE_SECRET_KEY", ""),
    langfuse_base_url=os.getenv("LANGFUSE_BASE_URL", "")
)    


CHUNK_SIZE: int = 500
CHUNK_OVERLAP: int = 100

TOP_K = 3
SCORE_THRESHOLD = 0.0



