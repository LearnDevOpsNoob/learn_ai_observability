# Embedding Batching Design

## Motivation

Embedding one chunk per request quickly hits provider rate limits.

## Old Flow

``` text
Chunk
 ↓
Embedding Request
 ↓
Repeat N times
```

## New Flow

``` text
Document
 ↓
Chunk
 ↓
Embed Batch
 ↓
Embeddings[]
 ↓
Upsert Each Vector
```

## Pipeline Changes

-   Chunk document.
-   Call `embed_batch(chunks)`.
-   Iterate through returned embeddings.
-   Upsert each vector with its payload.

## Benefits

-   Far fewer HTTP requests.
-   Better throughput.
-   Reduced chance of hitting RPM limits.
-   Cleaner provider abstraction.
