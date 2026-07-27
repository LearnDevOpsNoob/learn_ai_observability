from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()

@dataclass(frozen=True)
class Settings:
    openai_api_key: str
    openai_api_endpoint: str
    openai_model: str
    openai_embed_model: str

    qdrant_url: int
    collection_name: str

settings = Settings(
    openai_api_key=os.getenv("OPENAI_API_KEY", ""),
    openai_api_endpoint="https://models.github.ai/inference",

    openai_model=os.getenv("OPENAI_MODEL", "openai/gpt-4o"),
    openai_embed_model=os.getenv("EMBEDDING_MODEL", "openai/text-embedding-3-small"),

    qdrant_url=os.getenv("QDRANT_URL", "http://localhost:6333"),
    collection_name=os.getenv("QDRANT_COLLECTION", "research_docs")    
)    


CHUNK_SIZE: int = 500
CHUNK_OVERLAP: int = 100

TOP_K = 3
SCORE_THRESHOLD = 0.0



