from src.ingestion.ingest import IngestionPipeline
from src.retrieval.retrieval import RetrievalPipeline

def main():
    print("Observe & Understand")

    ingest_pipeline = IngestionPipeline(documents_path="data/documents")

    ingest_pipeline.run()
    print("Ingestio COmplete")

    retrieval_pipeline = RetrievalPipeline()

    results = retrieval_pipeline.search(
        "What is distributed tracing?"
    )

    if not results:
        print(f"Either retrive failed or no results")

    for result in results:
        print(result.score)
        print(result.source)
        print(result.content)
        print("-" * 50)

if __name__ == "__main__":
    main()
