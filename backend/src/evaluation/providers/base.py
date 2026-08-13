from abc import ABC, abstractmethod

from src.evaluation.schemas import EvaluationInput, EvaluationResult
from src.evaluation.metrics import EvaluationMetric

class EvaluationProvider(ABC):

    @abstractmethod
    async def evaluate(self, evaluation_input: EvaluationInput, metric: EvaluationMetric) -> EvaluationResult:
        """Evaluate a single metric."""
        raise NotImplementedError