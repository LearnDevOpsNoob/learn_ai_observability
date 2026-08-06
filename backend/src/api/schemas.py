from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    question: str = Field(min_length=3) 

class SourceResponse(BaseModel):
    source: str
    score: float


class TokenUsageResponse(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatMetadataResponse(BaseModel):
    model: str
    token_usage: TokenUsageResponse
    trace_id: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceResponse]
    metadata: ChatMetadataResponse

class IngestResponse(BaseModel):
    message: str
    indexed_points: int
    trace_id: str
    
class HealthResponse(BaseModel):
    status: str
