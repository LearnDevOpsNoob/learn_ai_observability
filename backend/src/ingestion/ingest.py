from src.ingestion.loader import DocumentLoader
from src.ingestion.chunker import TextChunker
from src.embeddings.openai_embeddings import OpenAIEmbedding
from src.db.vectordb import VectorDB

from src.config.config import CHUNK_OVERLAP, CHUNK_SIZE

from src.config.logging import get_logger

logger = get_logger(__name__)
class IngestionPipeline:
    """Coordinates the document ingestion process."""

    def __init__(self, documents_path: str):
        self.loader = DocumentLoader(documents_path)
        self.chunker = TextChunker(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
        self.embedder = OpenAIEmbedding()
        self.vectordb = VectorDB()

    def run(self) -> list[dict]:
        """
        Load documents and split them into chunks.

        Returns:
            List of chunk dictionaries.
        """

        documents = self.loader.load()

        self.vectordb.delete_collection()
        self.vectordb.create_collection(self.embedder.dimensions)

        point_id = 0  

        for document in documents:
            chunks = self.chunker.chunk(document["content"])

            for chunk_index, chunk in enumerate(chunks):

                embedding = self.embedder.embed(chunk)

                payload = {
                    "source": document["source"],
                    "chunk_id": chunk_index,
                    "content": chunk
                }       

                self.vectordb.upsert(
                    point_id=point_id,
                    vector=embedding,
                    payload=payload
                )

                point_id += 1

                # print(f"Indexed {point_id} chunk(s) into Qdrant.")
