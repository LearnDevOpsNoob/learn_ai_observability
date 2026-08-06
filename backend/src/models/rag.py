from pydantic import BaseModel, ConfigDict
from src.models.retrieval import RetrievedChunk
 
class RAGResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    answer: str
    retrieved_chunks: list[RetrievedChunk]
    model: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

        