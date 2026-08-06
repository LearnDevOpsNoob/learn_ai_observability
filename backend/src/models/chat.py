from pydantic import BaseModel, ConfigDict
from src.models.retrieval import RetrievedChunk

class ChatResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    answer: str
    model: str

    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatMessage(BaseModel):
    role: str
    content: str    