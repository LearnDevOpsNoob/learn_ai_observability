from fastapi import APIRouter, Depends

from src.api.dependencies import get_document_service
from src.services.document_service import DocumentService

from src.config.logging import get_logger

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

logger = get_logger(__name__)


@router.post("/ingest")
async def ingest(
    document_service: DocumentService = Depends(get_document_service),
):
    logger.info("Received POST /documents/ingest request.")

    try:
        return document_service.ingest()

    except Exception:
        logger.exception("Document ingestion failed.")
        raise

@router.delete("")
async def delete_documents(
    document_service: DocumentService = Depends(get_document_service),
):
    logger.info("Received DELETE /documents request.")

    try:
        return document_service.delete()

    except Exception:
        logger.exception("Document deletion failed.")
        raise
