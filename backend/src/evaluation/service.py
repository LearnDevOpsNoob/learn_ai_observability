from src.evaluation.metrics import EvaluationMetric
from src.evaluation.providers.base import EvaluationProvider
from src.evaluation.schemas import EvaluationInput, EvaluationResult

class EvaluationService:
    def __init__(self, provider: EvaluationProvider):
        self.provider = provider


    async def evaluate(self, evaluation_input: EvaluationInput, metric: EvaluationMetric) -> EvaluationResult:
        evaluation_result = await self.provider.evaluate(evaluation_input, metric)

        return evaluation_result    