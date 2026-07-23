from typing import List
from src.config import CHUNK_OVERLAP, CHUNK_SIZE

class TextChunker:
    """Splits text into fixed-size overlapping chunks."""

    
    def __init__(self, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP):
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size")
        
        self.chunk_size = CHUNK_SIZE
        self.chunk_overlap = CHUNK_OVERLAP

    def chunk(self, text: str) -> List[str]:
        """Split text into overlapping chunks."""

        chunks = []

        start = 0

        while start < len(text):
            end = start + self.chunk_size

            chunks.append(text[start:end])

            start += self.chunk_size - self.chunk_overlap

        return chunks    








