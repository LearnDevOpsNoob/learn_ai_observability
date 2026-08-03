from fastapi import FastAPI

from src.api.routes.documents import router as documents_router 
from src.api.routes.chat import router as chat_router
from src.api.routes.health import router as health_router

from src.config.logging import configure_logging, get_logger

from src.middleware.request_id import RequestIdMiddleware
from src.middleware.metrics import MetricsMiddleware

from src.config.metrics import get_metrics_app


configure_logging()
logger = get_logger(__name__)

app = FastAPI(
    title="Observe & Understand",
    description="Production-grade RAG API",
    version="1.0.0"
)

logger.info("🚀 FastAPI application initialized.")

app.add_middleware(RequestIdMiddleware)
app.add_middleware(MetricsMiddleware)

app.include_router(health_router)
app.include_router(documents_router)
app.include_router(chat_router)


app.mount("/metrics", get_metrics_app())

