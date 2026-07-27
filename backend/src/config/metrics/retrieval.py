from prometheus_client import Counter, Histogram

RETRIEVAL_DURATION = Histogram(
    "retrieval_duration_seconds",
    "Vector retrieval duration",
)

RETRIEVED_CHUNKS_TOTAL = Counter(
    "retrieved_chunks_total",
    "Total retrieved chunks",
)