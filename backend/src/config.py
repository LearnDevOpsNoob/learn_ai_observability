from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()

@dataclass(frozen=True)
class Settings:
    openai_api_key: str
    openai_api_endpoint: str
    openai_model: str
    qdrant_host: str
    qdrant_port: int
    collection_name: str

settings = Settings(
    openai_api_key=os.getenv("OPENAI_API_KEY", ""),
    openai_api_endpoint="https://models.github.ai/inference",
    openai_model="openai/gpt-4o",
    qdrant_host=os.getenv("QDRANT_HOST", "localhost"),
    qdrant_port=int(os.getenv("QDRANT_PORT", "6333")),
    collection_name=os.getenv("QDRANT_COLLECTION", "research_docs")    
)    


CHUNK_SIZE: int = 500
CHUNK_OVERLAP: int = 100

TOP_K = 3
SCORE_THRESHOLD = 0.0



