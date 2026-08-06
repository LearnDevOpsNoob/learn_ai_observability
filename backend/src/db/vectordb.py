from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from src.config.config import settings

from src.models.retrieval import RetrievedChunk

class VectorDB:
    def __init__(self):
        self.client = QdrantClient(url=settings.qdrant_url)

        self.collection_name = settings.collection_name

    def create_collection(self, vector_size: int):
        """Create the collection if it doesn't already exist."""

        if self.client.collection_exists(self.collection_name):
            # print(f"Collection '{self.collection_name}' already exists.")
            return
        
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE
            )
        )


    def upsert(self, point_id: int, vector: list[float], payload: dict) -> None:
        """Insert or update a point in the collection."""

        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=point_id,
                    vector=vector,
                    payload=payload
                )
            ],
            wait=True
        )   


    def similarity_search(self, query_vector: list[float], limit: int = 3, score_threshold: float = 0.7):
        response = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=limit,
            score_threshold=score_threshold
        )

        # print(f"Points: {len(response.points)} ")    
        
        return [
            RetrievedChunk(
                id=point.id,
                score=point.score,
                source=point.payload["source"],
                chunk_id=point.payload["chunk_id"],
                content=point.payload["content"]
            )
            for point in response.points
        ]

    def delete_collection(self):
        if self.client.collection_exists(self.collection_name):
            self.client.delete_collection(collection_name=self.collection_name)         




