from prometheus_client import Counter, Histogram

RAG_QUERIES_TOTAL = Counter(
    "rag_queries_total",
    "Total RAG queries processed",
)

INGESTION_DURATION = Histogram(
    "ingestion_duration_seconds",
    "Total document ingestion duration",
)

DOCUMENTS_INGESTED_TOTAL = Counter(
    "documents_ingested_total",
    "Total documents ingested",
)

CHUNKS_CREATED_TOTAL = Counter(
    "chunks_created_total",
    "Total chunks created during ingestion",
)

VECTORS_INDEXED_TOTAL = Counter(
    "vectors_indexed_total",
    "Total vectors indexed during ingestion",
)