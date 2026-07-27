from fastapi import FastAPI

from src.api.routes.chat import router as chat_router
from src.api.routes.health import router as health_router

from src.config.logging import configure_logging, get_logger

configure_logging()
logger = get_logger(__name__)

app = FastAPI(
    title="Observe & Understand",
    description="Production-grade RAG API",
    version="1.0.0"
)

logger.info("🚀 FastAPI application initialized.")

app.include_router(health_router)
app.include_router(chat_router)
