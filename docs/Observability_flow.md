# Observability Flow


```
                   User
                     │
                     ▼
                FastAPI Gateway
                     │
        ┌────────────┴────────────┐
        ▼                         ▼
 OpenTelemetry              Langfuse SDK
        │                         │
        ▼                         ▼
     Alloy                  Langfuse Server
        │                         │
   ┌────┼────┐              ┌─────┼────────────┐
   ▼    ▼    ▼              ▼     ▼            ▼
Prom  Loki Tempo      PostgreSQL ClickHouse  MinIO
        │
        ▼
     Grafana


```