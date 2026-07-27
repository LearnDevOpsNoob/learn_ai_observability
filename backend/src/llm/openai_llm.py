from openai import OpenAI

from src.config.config import settings
from src.models.chat import ChatMessage, ChatResponse

from src.config.logging import get_logger

logger = get_logger(__name__)
class OpenAIChat:
    def __init__(self):
        self.client = OpenAI(base_url=settings.openai_api_endpoint, api_key=settings.openai_api_key)

    def generate(self, messages: list[ChatMessage]) -> ChatResponse:

        logger.info(
           "Preparing %d messages for model request.", len(messages)
        )
        formatted_messages = self._format_messages(messages)
        logger.info(
            "Sending completion request to model '%s'.",
            settings.openai_model,
        )
        response = self._call_completion(formatted_messages)
        chat_response = self._build_chat_response(response)
        logger.info("AI response generated successfully.")
        return chat_response

    def _build_chat_response(self, response):

        answer = response.choices[0].message.content or ""
        usage = response.usage
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

    def _call_completion(self, messages):
        return self.client.chat.completions.create(
            model=settings.openai_model,
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