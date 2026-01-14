from openai import AsyncOpenAI
from typing import Optional, List, Dict

from .base import LLMClient


class ChatGPTClient(LLMClient):

    def __init__(
        self,
        api_key: str,
        model: Optional[str] = None,
        timeout: Optional[float] = None,
    ):
        model = model or "openai/gpt-4o-mini"
        timeout = timeout or 30.0

        self.client = AsyncOpenAI(api_key=api_key, timeout=timeout)
        self.model = model

    async def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.3,
    ) -> str:
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
        )
        response_text = response.choices[0].message.content or ""
        return response_text
