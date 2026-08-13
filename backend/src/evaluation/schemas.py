from pydantic import BaseModel, Field


class EvaluationInput(BaseModel):
    question: str
    retrieved_context: list[str]
    answer: str

    ground_truth: str | None = None

    trace_id: str | None = None
    request_id: str | None = None

    model: str | None = None
    provider: str | None = None

class EvaluationResult(BaseModel):
    metric: str
    score: float = Field(ge=0.0, le=1.0)

    trace_id: str | None = None
    request_id: str | None = None

    provider: str
    model: str | None = None

    metadata: dict[str, str | int | float | bool | None ] = Field(
        default_factory=dict
    )



