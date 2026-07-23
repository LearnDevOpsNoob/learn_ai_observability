from pydantic import BaseModel, ConfigDict

class RetrievedChunk(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: int
    score: float
    source: str
    chunk_id: int
    content: str