from functools import lru_cache
from src.rag.pipeline import RAGPipeline
from src.services.chat_service import ChatService
from src.services.document_service import DocumentService

@lru_cache
def get_rag_pipeline() -> RAGPipeline:
    return RAGPipeline()

@lru_cache
def get_chat_service() -> ChatService:
    return ChatService(get_rag_pipeline())

def get_document_service() -> DocumentService:
    return DocumentService()
