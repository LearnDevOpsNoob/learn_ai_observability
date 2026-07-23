from src.ingestion.ingest import IngestionPipeline
from src.rag.pipeline import RAGPipeline

def main():
    print("Observe & Understand")

    ingest_pipeline = IngestionPipeline(documents_path="data/documents")

    ingest_pipeline.run()

    print("Ingestion Complete")

    rag_pipeline = RAGPipeline()

    while True:
        question = input("\nAsk a question (or 'exit'): ")

        if question.lower() == "exit":
            break

        response = rag_pipeline.ask(question)

        print("\nAnswer")
        print(response.answer)

        print("\nSources")
        for chunk in response.retrieved_chunks:
            print(f"- {chunk.source} ({chunk.score:.4f})")
        
if __name__ == "__main__":
    main()
