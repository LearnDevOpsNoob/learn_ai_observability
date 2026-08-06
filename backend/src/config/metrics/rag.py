from prometheus_client import Counter

RAG_QUERIES_TOTAL = Counter(
    "rag_queries_total",
    "Total RAG queries processed",
)