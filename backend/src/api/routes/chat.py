from fastapi import APIRouter, Depends

from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

from src.api.dependencies import get_chat_service
from src.api.schemas import ChatRequest, ChatResponse

from src.config.logging import get_logger
from src.observability.tracing import get_tracer
from src.observability.langfuse import get_langfuse

from src.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["Chat"])

logger = get_logger(__name__)
tracer = get_tracer()
# trace_id = get_current_trace_id()

@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest, chat_service: ChatService = Depends(get_chat_service)):
    logger.info("Received POST /chat request.")

    with tracer.start_as_current_span("chat_request") as span:
        span.set_attribute("question.length", len(request.question))

        try:
            response = chat_service.chat(request.question)

            span = trace.get_current_span()

            # print(span.get_span_context().is_valid)
            # print('=================TRACE ID=================')
            # current = trace.get_current_span()

            # print("INLINE:", format(current.get_span_context().trace_id, "032x"))
            # print("HELPER:", get_current_trace_id())

            span.set_status(Status(StatusCode.OK))
            return response
            
        except Exception as e:
            span.record_exception(e)
            span.set_status(Status(StatusCode.ERROR))

            logger.exception("Failed while generating AI response.")
            raise    



