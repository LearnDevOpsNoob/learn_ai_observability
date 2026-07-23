from src.ingestion.ingest import IngestionPipeline

def main():
    print("Observe & Understand")

    pipeline = IngestionPipeline(documents_path="data/documents")

    pipeline.run()

    # for chunk in chunks:
    #     print("-" * 50)
    #     print(f"Source : {chunk['source']}")
    #     print(f"Chunk  : {chunk['chunk_id']}")
    #     print(chunk["content"][:150])



if __name__ == "__main__":
    main()
