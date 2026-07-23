from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct


from src.config import settings

class VectorDB:
    def __init__(self):
        self.client = QdrantClient(
            host=settings.qdrant_host,
            port=settings.qdrant_port
        )

        self.collection_name = settings.collection_name

    def create_collection(self, vector_size: int):
        """Create the collection if it doesn't already exist."""

        if self.client.collection_exists(self.collection_name):
            print(f"Collection '{self.collection_name}' already exists.")
            return
        
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE
            )
        )

        print(f"Created collection '{self.collection_name}'.")        

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
            ]
        )        




