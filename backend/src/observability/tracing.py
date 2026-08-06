from fastapi import FastAPI

from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter,
)
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

from functools import wraps
from typing import Callable, Any


SERVICE_NAME = "ai-gateway"

def setup_tracing(app: FastAPI) -> None:
    """
    Configure OpenTelemetry tracing for the application.
    """
    resource = Resource.create(
         {
            "service.name": SERVICE_NAME,
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
        tracer_provider=tracer_provider,
        exclude_spans=["send", "receive"]
    )

    HTTPXClientInstrumentor().instrument(tracer_provider=tracer_provider)

def get_tracer():
    return trace.get_tracer(SERVICE_NAME)

def get_current_trace_id() -> str:
    span = trace.get_current_span()
    context = span.get_span_context()

    if not context.is_valid:
        return ""

    return format(context.trace_id, "032x")


def trace_step(name: str, attributes: dict[str, Any] | None = None):
    """
    Decorator to create a business-level span.
    """
    def decorator(func: Callable[..., Any]):
        @wraps(func)
        def wrapper(*args, **kwargs):
            tracer = get_tracer()

            print(f"DECORATOR HIT -> {name}")

            print(tracer)

            with tracer.start_as_current_span(name):
                print(f"SPAN CREATED -> {name}")
                return func(*args, **kwargs)

            with tracer.start_as_current_span(name) as span:
                if attributes:
                    for key, value in attributes.items():
                        span.set_attribute(key, value)

                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    span.record_exception(e)
                    span.set_status(Status(StatusCode.ERROR, str(e)))
                    raise
        return wrapper
    return decorator    






