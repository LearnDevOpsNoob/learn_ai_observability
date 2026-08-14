from src.evaluation.metrics import EvaluationMetric
from src.evaluation.providers.base import EvaluationProvider
from src.evaluation.schemas import EvaluationInput, EvaluationResult

from ragas.llms import BaseRagasLLM
from ragas.metrics.collections import Faithfulness

# from src.evaluation.llm import 

class RagasEvaluationProvider(EvaluationProvider):
    def __init__(self, llm: BaseRagasLLM):
        self.llm = llm

    async def evaluate(self, evaluation_input: EvaluationInput, metric: EvaluationMetric) -> EvaluationResult:
        if metric != EvaluationMetric.FAITHFULNESS:
            raise ValueError(f"Unsupported RAGAS metric: {metric}")

        scorer = Faithfulness(llm=self.llm)

        result = await scorer.ascore(
            user_input=evaluation_input.question,
            response=evaluation_input.answer,
            retrieved_contexts=evaluation_input.retrieved_context
        )

        evaluation_result = EvaluationResult(
            metric=metric.value,
            score=float(result.value),
            trace_id=evaluation_input.trace_id,
            request_id=evaluation_input.request_id,
            provider="ragas",
            model=evaluation_input.model,
            metadata={
                "reason": result.reason
            }
        )

        return evaluation_result






    