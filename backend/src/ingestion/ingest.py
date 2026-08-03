from src.ingestion.loader import DocumentLoader
from src.ingestion.chunker import TextChunker
from src.db.vectordb import VectorDB
from src.embeddings.llm_embeddings import OpenAIEmbedding

from src.config.config import CHUNK_OVERLAP, CHUNK_SIZE
from src.config.logging import get_logger

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

    def run(self) -> None:
        """Load, chunk, embed and index documents."""

        logger.info("=== INGESTION PIPELINE STARTED ===")
        logger.info("Loading documents...")

        try:
            documents = self.loader.load()
        except Exception:
            logger.exception("Loader failed.")
            raise

        logger.info("Loaded %d document(s).", len(documents))

        point_id = 0

        for document in documents:
            chunks = self.chunker.chunk(document["content"])

            logger.info(
                "Processing '%s' (%d chunks).",
                document["source"],
                len(chunks),
            )

            # Generate embeddings for all chunks in a single request
            embeddings = self.embedder.embed_batch(chunks)

            for chunk_index, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                payload = {
                    "source": document["source"],
                    "chunk_id": chunk_index,
                    "content": chunk,
                }

                logger.info(
                    "Upserting point %d (%d dims).",
                    point_id,
                    len(embedding),
                )

                self.vectordb.upsert(
                    point_id=point_id,
                    vector=embedding,
                    payload=payload,
                )

                point_id += 1

        logger.info(
            "Ingestion completed successfully. Indexed %d point(s).",
            point_id,
        )