from src.ingestion.loader import DocumentLoader
from src.ingestion.chunker import TextChunker
from src.db.vectordb import VectorDB
from src.embeddings.llm_embeddings import OpenAIEmbedding

from src.config.config import CHUNK_OVERLAP, CHUNK_SIZE
from src.config.logging import get_logger

from src.observability.tracing import trace_step, get_tracer

logger = get_logger(__name__)

class IngestionPipeline:
    """Coordinates the document ingestion process."""

    def __init__(self, documents_path: str, embedder: OpenAIEmbedding):
        self.loader = DocumentLoader(documents_path)
        self.chunker = TextChunker(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
        )
        self.embedder = embedder
        self.vectordb = VectorDB()
        self.tracer = get_tracer()


    @trace_step("ingest_documents")
    def run(self):
        """Load, chunk, embed and index documents."""

        logger.info("=== INGESTION PIPELINE STARTED ===")
        
        with self.tracer.start_as_current_span("load_documents"):

            logger.info("Loading documents...")

            try:
                documents = self.loader.load()
            except Exception:
                logger.exception("Loader failed.")
                raise

        point_id = 0
        chunk_count = 0
        document_count = len(documents)

        logger.info("Loaded %d document(s).", document_count)

        for document in documents:
            with self.tracer.start_as_current_span("process_document") as span:
                span.set_attribute("document.source", document["source"])

                with self.tracer.start_as_current_span("chunk_documents"):
                    chunks = self.chunker.chunk(document["content"])

                    logger.info("Processing '%s' (%d chunks).",
                        document["source"],
                        len(chunks),
                    )

                with self.tracer.start_as_current_span("generate_embeddings"):
                # Generate embeddings for all chunks in a single request
                    embeddings = self.embedder.embed_batch(chunks)

                with self.tracer.start_as_current_span("upsert_vectors"):

                    for chunk_index, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                        payload = {
                            "source": document["source"],
                            "chunk_id": chunk_index,
                            "content": chunk,
                        }

                        logger.info(
                            "Upserting point %d (%d dims).", point_id, len(embedding))

                        self.vectordb.upsert(point_id=point_id, vector=embedding, payload=payload)

                        point_id += 1
                        
        logger.info(
                    "Ingestion completed successfully. "
                    "Documents=%d | Chunks=%d | Vectors=%d",
                    document_count,
                    chunk_count,
                    point_id,
                )
        return {
            "documents": document_count,
            "chunks": chunk_count,
            "vectors": point_id,
        }