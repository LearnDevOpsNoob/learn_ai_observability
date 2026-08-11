from src.models.chat import ChatMessage
from src.models.retrieval import RetrievedChunk
from src.prompt.prompts import SYSTEM_PROMPT, CONTEXT_SEPARATOR

from opentelemetry import trace

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
            return False

        for chunk in chunks:
            sections.append(
                f"Source: {chunk.source}\n"
                f"{chunk.content}"
            )

        return CONTEXT_SEPARATOR.join(sections)    
            

    def build(self, question: str, chunks: list[RetrievedChunk]) -> list[RetrievedChunk]:
        span = trace.get_current_span()

        system_prompt = self._build_system_prompt()
        user_prompt = self._build_user_prompt(question, chunks)

        span.set_attribute("prompt.chunk_count", len(chunks))
        span.set_attribute("prompt.question_length", len(question))
        span.set_attribute("prompt.system_length", len(system_prompt))
        span.set_attribute("prompt.user_length", len(user_prompt))
        span.set_attribute(
            "prompt.total_length",
            len(system_prompt) + len(user_prompt),
        )

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

