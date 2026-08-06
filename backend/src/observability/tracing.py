from fastapi import FastAPI

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter,
)
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from opentelemetry.trace import get_current_span

def setup_tracing(app: FastAPI) -> None:
    """
    Configure OpenTelemetry tracing for the application.
    """

    resource = Resource.create(
         {
            "service.name": "ai-gateway",
            "service.version": "1.0.0"          
         }
    ) 

    tracer_provider = TracerProvider(resource=resource)

    span_exporter = OTLPSpanExporter(
        endpoint="alloy:4317",
        insecure=True
    )

    span_processor = BatchSpanProcessor(span_exporter)
    tracer_provider.add_span_processor(span_processor)

    trace.set_tracer_provider(tracer_provider)

    FastAPIInstrumentor.instrument_app(
        app,
        tracer_provider=tracer_provider
    )

    HTTPXClientInstrumentor().instrument(tracer_provider=tracer_provider)

def get_tracer():
    return trace.get_tracer("ai-gateway")

def get_current_trace_id() -> str:
    span = trace.get_current_span()
    context = span.get_span_context()

    # print("=" * 50)
    # print("HELPER")
    # print("SPAN:", span)
    # print("VALID:", context.is_valid)
    # print("TRACE:", context.trace_id)

    if not context.is_valid:
        return ""

    return format(context.trace_id, "032x")







