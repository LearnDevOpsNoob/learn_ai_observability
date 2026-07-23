from src.embeddings.openai_embeddings import OpenAIEmbedding
from src.db.vectordb import VectorDB
from src.config import TOP_K, SCORE_THRESHOLD


class RetrievalPipeline:
    def __init__(self):
        self.embedder = OpenAIEmbedding()
        self.vectordb = VectorDB()


    def search(self, question: str):
        embedding = self.embedder.embed(question)

        results = self.vectordb.similarity_search(
            query_vector=embedding,
            limit=TOP_K,
            score_threshold=SCORE_THRESHOLD
        )    
        
        return results