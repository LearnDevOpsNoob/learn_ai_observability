from pathlib import Path

class DocumentLoader:
    def __init__(self, documents_path: str):
        self.documents_path = Path(documents_path)

    def load(self) -> list[dict]:
        """
        Load all Markdown documents from the configured directory.

        Returns:
            List of dictionaries containing:
            - source: filename
            - content: file contents
        """

        if not self.documents_path.exists():
           raise FileNotFoundError(
                f"Documents directory not found: {self.documents_path}"
            ) 
        
        markdown_files = list(self.documents_path.glob("*md"))

        if not markdown_files:
           raise ValueError(
                f"No Markdown (.md) files found in {self.documents_path}"
            )

        # print(f"Found {len(markdown_files)} document(s).") 


        documents = []   

        for file_path in markdown_files:
            documents.append(
                {
                    "source": file_path.name,
                    "content": file_path.read_text(encoding="utf-8")
                }
            )
        # print(f"DOCS: {documents}")
        return documents






