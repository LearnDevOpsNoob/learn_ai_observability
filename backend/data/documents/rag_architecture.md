# Retrieval-Augmented Generation

Retrieval-Augmented Generation (RAG) combines vector search with large language models.

Instead of relying only on the model's training data, RAG retrieves relevant documents before generating an answer.

The basic pipeline consists of four stages.

## Document Loading

Documents are collected from one or more sources such as Markdown files, PDFs, databases, or internal documentation.

The loader reads these files and prepares them for processing.

## Chunking

Large documents are divided into smaller chunks before embeddings are generated.

Chunking improves retrieval accuracy because each embedding represents a focused piece of information.

Many systems use overlapping chunks to preserve context between adjacent sections.

## Embeddings

Embeddings convert text into dense numerical vectors.

Similar pieces of text produce vectors that are close together in vector space.

OpenAI's text-embedding-3-small model produces vectors with 1536 dimensions.

## Vector Database

Embeddings are stored inside a vector database such as Qdrant.

When a user asks a question, the query is embedded using the same model.

The vector database performs a similarity search and returns the most relevant chunks.

## Generation

The retrieved chunks are added to the prompt sent to the language model.

The model generates an answer using both its own knowledge and the retrieved context.

This process significantly reduces hallucinations when working with private knowledge bases.