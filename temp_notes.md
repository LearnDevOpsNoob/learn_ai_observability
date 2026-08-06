## Phase 5 Flow

My Proposed Learning Order

This follows the natural evolution of an AI service:

- ✅ Backend + Docker + Qdrant (completed)
- Structured Logging
- Prometheus Metrics
- OpenTelemetry Instrumentation
- Docker Compose additions (Prometheus, Grafana, Tempo, Loki)
- Grafana dashboards
- AI-specific metrics
- Langfuse integration
- Security & Guardrails (Prompt injection, OWASP LLM, NeMo Guardrails)

## Timeline

Realistically, given your current progress:

- Structured Logging – 2–3 hours
- Prometheus Metrics – 2–3 hours
- OpenTelemetry Tracing – 4–6 hours
- Grafana + Prometheus + Tempo + Loki (Docker Compose + Dashboards) – 4–6 hours
- AI-specific Observability (token usage, retrieval latency, etc.) – 3–5 hours
- Langfuse Integration – 2–3 hours

Total: 18–25 hours (roughly 5–7 focused sessions of 3–4 hours each).


### Log Levels

We'll stick to the standard levels:

DEBUG – Detailed developer information (e.g., prompt preview, retrieved chunk IDs).
INFO – Normal application flow.
WARNING – Recoverable issues.
ERROR – Exceptions that affect the current request.
CRITICAL – Application cannot continue.

Most of our application logs will be INFO.


### Architecture Evolution

```
                    Client
                       │
                       ▼
                 FastAPI Router
                       │
                       ▼
                 Chat Service
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
     Logging        Metrics       Tracing
                       │
                       ▼
                 RAG Pipeline
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
    Retriever      Prompt Builder     LLM
                       │
                       ▼
                 Qdrant / OpenAI


```


### Tooling Stack

| Component       | Tool                | Purpose                        |
| --------------- | ------------------- | ------------------------------ |
| Logging         | Python `logging`    | Structured application logs    |
| Metrics         | `prometheus-client` | Expose counters and histograms |
| Tracing         | OpenTelemetry       | Distributed tracing            |
| Trace Storage   | Tempo               | Store traces                   |
| Metrics Storage | Prometheus          | Scrape metrics                 |
| Visualization   | Grafana             | Dashboards                     |
| Log Aggregation | Loki                | Centralized logs               |


```

✅ Phase 1
Basic Logging
(Completed)

↓

✅ Phase 2
Exception Logging

↓

✅ Phase 3
Request IDs

↓

[not yet] Phase 4
Structured JSON Logging

↓

[CURR] Phase 5
Prometheus Metrics

↓

Phase 6
OpenTelemetry Traces

↓

Phase 7
Grafana + Loki + Tempo

↓

Phase 8
Langfuse AI Observability

```


=======


Why these metric types?

This is worth understanding now because you'll use them everywhere.

Counter

Only goes up.

1
2
3
4
5

Examples:

Requests
Errors
OpenAI calls
Tokens consumed
Gauge

Can go up and down.

2
3
1
4
2

Examples:

Active requests
Queue size
Connected users
Histogram

Measures distributions.

Instead of one value, it builds latency buckets.

5 ms

12 ms

19 ms

45 ms

900 ms

Later Grafana can answer:

"What's the P95 latency?"

without us writing any code.


===

```
How is the order decided?

FastAPI (Starlette) executes middleware in reverse order of registration on the incoming request.

For example:

app.add_middleware(RequestIdMiddleware)
app.add_middleware(MetricsMiddleware)
app.add_middleware(AuthMiddleware)

Incoming request:

Request
   │
   ▼
AuthMiddleware
   ▼
MetricsMiddleware
   ▼
RequestIdMiddleware
   ▼
Route

Outgoing response unwinds in the opposite direction:

Route
   ▲
RequestIdMiddleware
   ▲
MetricsMiddleware
   ▲
AuthMiddleware
   ▲
Response

It's like stacking plates—the last one you put on is the first one you take off (LIFO).


```