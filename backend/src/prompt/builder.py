from src.models.chat import ChatMessage
from src.models.retrieval import RetrievedChunk
from src.prompt.prompts import SYSTEM_PROMPT, CONTEXT_SEPARATOR

class PromptBuilder:
    """
    Builds chat messages for the LLM from retrieved context.
    """
    def _build_system_prompt(self) -> str:
        return SYSTEM_PROMPT

    def _build_user_prompt(self, question: str, chunks: list[RetrievedChunk]) -> str:
        context = self._build_context(chunks)

        return (
            f"Context:\n"
            f"{context}\n\n"
            f"Question:\n"
            f"{question}"
        )

    def _build_context(self, chunks: list[RetrievedChunk]) -> str:
        sections = []

        if not chunks:
            print('No chunks')
            return False

        for chunk in chunks:
            sections.append(
                f"Source: {chunk.source}\n"
                f"{chunk.content}"
            )

        return CONTEXT_SEPARATOR.join(sections)    
            

    def build(self, question: str, chunks: list[RetrievedChunk]) -> list[RetrievedChunk]:
        system_prompt = self._build_system_prompt()
        user_prompt = self._build_user_prompt(question, chunks)

        return [
            ChatMessage(
                role="system",
                content=system_prompt
            ),
            ChatMessage(
                role="user",
                content=user_prompt
            )
        ]

