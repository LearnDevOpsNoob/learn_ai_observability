from prometheus_client import Counter, Histogram

LLM_REQUESTS_TOTAL = Counter(
    "llm_requests_total",
    "Total LLM requests",
)

LLM_DURATION = Histogram(
    "llm_duration_seconds",
    "LLM response latency",
)

PROMPT_TOKENS_TOTAL = Counter(
    "llm_prompt_tokens_total",
    "Prompt tokens consumed",
)

COMPLETION_TOKENS_TOTAL = Counter(
    "llm_completion_tokens_total",
    "Completion tokens consumed",
)