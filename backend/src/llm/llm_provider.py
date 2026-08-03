from openai import OpenAI
from openai.types.chat import ChatCompletion

from src.config.config import settings
from src.models.chat import ChatMessage, ChatResponse

from time import perf_counter

from src.config.metrics import (
    LLM_REQUESTS_TOTAL,
    LLM_DURATION,
    PROMPT_TOKENS_TOTAL,
    COMPLETION_TOKENS_TOTAL,
)

from src.config.logging import get_logger

logger = get_logger(__name__)
class LLMService:
    def __init__(self):
        self.client = OpenAI(
                base_url=settings.llm_api_endpoint, 
                api_key=settings.llm_api_key
            )

    def generate(self, messages: list[ChatMessage]) -> ChatResponse:

        logger.info(
           "Preparing %d messages for model request.", len(messages)
        )

        LLM_REQUESTS_TOTAL.inc()

        formatted_messages = self._format_messages(messages)
        logger.info(
            "Sending completion request to model '%s'.", settings.llm_provider,
    settings.llm_model,
        )

        start_time = perf_counter()

        try:
            response = self._call_completion(formatted_messages)

            chat_response = self._build_chat_response(response=response)
            logger.info("AI response generated successfully.")

            return chat_response

        except Exception:
            logger.exception("LLM generation failed.")
            raise
        finally:
            LLM_DURATION.observe(perf_counter() - start_time)

    def _build_chat_response(self, response):

        answer = response.choices[0].message.content or ""
        usage = response.usage

        PROMPT_TOKENS_TOTAL.inc(usage.prompt_tokens)
        COMPLETION_TOKENS_TOTAL.inc(usage.completion_tokens)

        logger.info(
            "Token usage - Prompt: %d | Completion: %d | Total: %d",
            usage.prompt_tokens,
            usage.completion_tokens,
            usage.total_tokens,
        )
        return ChatResponse(
            answer=answer,
            model=response.model,
            prompt_tokens=usage.prompt_tokens,
            completion_tokens=usage.completion_tokens,
            total_tokens=usage.total_tokens
        )

    def _format_messages(self, messages: list[ChatMessage]) -> list[dict]:
        return [
            {
                "role": message.role,
                "content": message.content,
            }
            for message in messages
        ]

    def _call_completion(self, messages: list[dict]) -> ChatCompletion:
        return self.client.chat.completions.create(
            model=settings.llm_model,
            messages=messages,
        )


















# import OpenAI from "openai";
# import { env } from "./env.js";

# import dotenv from "dotenv";

# dotenv.config();

# const endpoint = "https://models.github.ai/inference";

# export const openai = new OpenAI({
#   baseURL: endpoint,
#   apiKey: process.env.OPENAI_API_KEY,
# });