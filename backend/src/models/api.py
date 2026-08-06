from pydantic import BaseModel

class ChatRequest(BaseModel):
    question: str

class ChatApiResponse(BaseModel):
    answer: str
    sources: list[str]