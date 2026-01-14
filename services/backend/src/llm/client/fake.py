from typing import List, Dict, Optional

from .base import LLMClient


class FakeLLMClient(LLMClient):

    def __init__(self, response: Optional[str] = None):
        self.response = response or "Fake LLM Client response"
        self.calls = []

    async def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.3,
    ) -> str:
        self.calls.append(
            {"messages": messages, "temperature": temperature}
        )
        return self.response
