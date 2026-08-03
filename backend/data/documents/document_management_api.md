# Document Management API

## Purpose

Manage the document lifecycle independently from chat requests.

## Responsibilities

-   Expose ingestion endpoints
-   Trigger document indexing
-   Delete or recreate the vector collection
-   Return ingestion status

## Endpoints

``` http
POST /documents/ingest
DELETE /documents
```

## Flow

``` text
Client
  ↓
DocumentService
  ↓
Delete Collection
Create Collection
  ↓
IngestionPipeline
  ↓
Loader → Chunker → Embedder → VectorDB
```

## Design Notes

-   Keep routes thin.
-   Keep orchestration inside `DocumentService`.
-   Keep ingestion logic inside `IngestionPipeline`.
