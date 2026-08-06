# Langfuse Infrastructure

> AI Observability Platform for the Observe & Understand RAG System

---

# Overview

Langfuse provides end-to-end observability specifically for Large Language Model (LLM) applications.

Unlike Grafana, which focuses on infrastructure telemetry (metrics, logs, traces), Langfuse understands AI-native concepts such as:

- Prompts
- Completions
- Retrieval
- Token Usage
- Costs
- Evaluations
- User Feedback
- Prompt Versioning

Together, the Grafana Stack and Langfuse provide complete observability for the platform.

---

# Architecture

```
                   FastAPI Backend
                          │
                    Langfuse SDK
                          │
                ┌─────────┴─────────┐
                │                   │
           Langfuse Web      Langfuse Worker
                │                   │
                └─────────┬─────────┘
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
   PostgreSQL       ClickHouse          Redis
     Metadata        Analytics         Queue
                          │
                          ▼
                       MinIO
                 Event Upload Storage
```

---

# Components

## PostgreSQL

Stores application metadata.

Responsible for:

- Users
- Organizations
- Projects
- API Keys
- Prompt Metadata
- Trace Metadata

Container

```
langfuse-postgres
```

---

## ClickHouse

Primary analytics database.

Responsible for storing:

- Traces
- Generations
- Events
- Token Usage
- Latency
- Cost Information
- Evaluation Data

Container

```
langfuse-clickhouse
```

---

## MinIO

S3-compatible object storage.

Responsible for:

- Event Uploads
- Attachments
- Future Evaluation Datasets
- Prompt Artifacts

Container

```
langfuse-minio
```

---

## Redis

Acts as the internal message broker.

Responsible for:

- Background Jobs
- Event Processing
- Queue Management

Container

```
langfuse-redis
```

---

## Langfuse Web

Frontend + REST API.

Provides:

- Dashboard
- Prompt Management
- Traces
- Sessions
- Users
- Analytics

Accessible at

```
http://localhost:3001
```

Container

```
langfuse-web
```

---

## Langfuse Worker

Background processing service.

Responsible for:

- Event Processing
- ClickHouse Writes
- Async Tasks
- Evaluation Processing

Container

```
langfuse-worker
```

---

# Environment Configuration

Configuration is isolated into

```
.langfuse.env
```

to keep Langfuse independent from the backend application.

A corresponding

```
.langfuse.env.example
```

is committed for onboarding and documentation.

---

# Docker Volumes

| Volume | Purpose |
|----------|---------|
| langfuse_postgres | PostgreSQL Data |
| langfuse_clickhouse | ClickHouse Data |
| langfuse_minio | MinIO Storage |
| langfuse_redis | Redis Persistence |

---

# Exposed Ports

| Service | Port |
|----------|------|
| Langfuse Web | 3001 |
| MinIO API | 9000 |
| MinIO Console | 9001 |

All remaining services communicate internally over Docker networking.

---

# Relation with Grafana Stack

Infrastructure Observability

- Prometheus
- Grafana
- Loki
- Tempo
- Alloy

Provides

- Metrics
- Logs
- Distributed Traces
- Infrastructure Health

---

AI Observability

- Langfuse

Provides

- Prompt Tracking
- Retrieval Monitoring
- Token Usage
- Cost Tracking
- Prompt Versioning
- Sessions
- User Feedback
- AI Evaluations

---

# Current Integration Plan

## Phase 1

- [x] Infrastructure Setup
- [x] PostgreSQL
- [x] ClickHouse
- [x] Redis
- [x] MinIO
- [x] Langfuse Deployment

---

## Phase 2

Backend SDK Integration

- [ ] Install Langfuse SDK
- [ ] Configure Client
- [ ] Authentication
- [ ] Health Check

---

## Phase 3

LLM Instrumentation

- [ ] Chat Requests
- [ ] Prompt Tracking
- [ ] Completion Tracking
- [ ] Token Usage
- [ ] Latency
- [ ] Cost Tracking

---

## Phase 4

RAG Instrumentation

- [ ] Retrieval Span
- [ ] Retrieved Documents
- [ ] Similarity Scores
- [ ] Embedding Metadata
- [ ] Source Attribution

---

## Phase 5

Advanced AI Observability

- [ ] Prompt Versioning
- [ ] User Sessions
- [ ] Custom Metadata
- [ ] Evaluations
- [ ] Human Feedback
- [ ] Quality Monitoring

---

# Project Structure

```
infra/
└── langfuse/
    ├── README.md
    ├── .langfuse.env.example

docker-compose.yml
.langfuse.env
```

---

# References

- https://langfuse.com/docs
- https://langfuse.com/self-hosting
- https://github.com/langfuse/langfuse

---

This infrastructure provides AI-native observability for the Observe & Understand RAG platform and complements the existing Grafana monitoring stack by enabling prompt, retrieval, generation, and evaluation tracking.