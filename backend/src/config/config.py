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

    embedding_provider: str
    embedding_api_key: str
    embedding_api_endpoint: str
    embedding_model: str
    vector_size: int

    qdrant_url: int
    collection_name: str

    langfuse_public_key: str
    langfuse_secret_key: str
    langfuse_host: str


settings = Settings(
    # LLM
    llm_provider=os.getenv("LLM_PROVIDER", "groq"),
    llm_api_key=os.getenv("GROQ_API_KEY", ""),
    llm_api_endpoint="https://api.groq.com/openai/v1",
    llm_model=os.getenv(
        "LLM_MODEL",
        "openai/gpt-oss-120b",
    ),

    # Embeddings
    embedding_provider=os.getenv("EMBED_PROVIDER", "voyage"),
    embedding_api_key=os.getenv("VOYAGE_API_KEY", ""),
    embedding_api_endpoint="https://api.voyageai.com/v1",
    embedding_model=os.getenv(
        "EMBEDDING_MODEL",
        "voyage-3-lite",
    ),
    vector_size=int(
        os.getenv("EMBEDDING_DIMENSIONS", 1024)
    ),

    qdrant_url=os.getenv("QDRANT_URL", "http://localhost:6333"),
    collection_name=os.getenv("QDRANT_COLLECTION", "research_docs")    

    # Langfuse Settup
    langfuse_public_key=os.getenv("LANGFUSE_PUBLIC_KEY", ""),
    langfuse_secret_key=os.getenv("LANGFUSE_SECRET_KEY", ""),
    langfuse_host=os.getenv("LANGFUSE_BASE_URL", ""),


)    


CHUNK_SIZE: int = 500
CHUNK_OVERLAP: int = 100

TOP_K = 3
SCORE_THRESHOLD = 0.0



