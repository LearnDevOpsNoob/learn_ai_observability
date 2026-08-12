from src.config.logging import get_logger

from src.db.vectordb import VectorDB
from src.embeddings.llm_embeddings import OpenAIEmbedding
from src.ingestion.ingest import IngestionPipeline

from src.api.schemas import IngestResponse
from src.observability.tracing import get_current_trace_id

logger = get_logger(__name__)


class DocumentService:
    """Service responsible for document ingestion operations."""

    def __init__(self, documents_path: str = "data/documents"):
        self.documents_path = documents_path
        self.embedder = OpenAIEmbedding()

        self.pipeline = IngestionPipeline(documents_path=self.documents_path, embedder=self.embedder)
        self.vectordb = VectorDB()

    def ingest(self) -> dict:
        """Rebuild the vector database from all documents."""

        logger.info("Starting document ingestion.")

        self.vectordb.delete_collection()
        self.vectordb.create_collection(
            vector_size=self.embedder.dimensions
        )

        stats = self.pipeline.run()

        logger.info(
            "Document ingestion completed | "
            "endpoint=/documents/ingest | "
            "documents=%d | chunks=%d | vectors=%d",
            stats["documents"],
            stats["chunks"],
            stats["vectors"],
        )

        return IngestResponse(
            message="Documents indexed successfully.",
            indexed_points=stats,
            trace_id=get_current_trace_id()
        ) 

    
    def delete(self) -> dict:
        """Delete all indexed documents."""

        logger.info("Deleting document collection.")

        self.vectordb.delete_collection()

        logger.info("Document collection deleted.")

        return {
            "status": "success",
            "message": "Document collection deleted.",
        }