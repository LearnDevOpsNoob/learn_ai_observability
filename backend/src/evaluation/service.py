from src.evaluation.metrics import EvaluationMetric
from src.evaluation.providers.base import EvaluationProvider
from src.evaluation.schemas import EvaluationInput, EvaluationResult

from src.observability.tracing import get_tracer
class EvaluationService:
    def __init__(self, provider: EvaluationProvider):
        self.provider = provider

    async def evaluate(self, evaluation_input: EvaluationInput, metric: EvaluationMetric) -> EvaluationResult:

        tracer = get_tracer()

        with tracer.start_as_current_span("evaluation") as span:
            span.set_attribute("evaluation.metric", metric.value)

            if evaluation_input.trace_id:
                span.set_attribute("evaluation.trace_id", evaluation_input.trace_id)

            evaluation_result = await self.provider.evaluate(evaluation_input, metric)

            span.set_attribute("evaluation.score", evaluation_result.score)

            return evaluation_result    