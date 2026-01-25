import os
from typing import Optional

from .base import LLMClient


def get_llm_client(
    mode: str,
    *,
    model: Optional[str] = None,
    timeout: Optional[float] = None,
    response: Optional[str] = None,
) -> LLMClient:

    if mode == "chatgpt":
        from .chatgpt import ChatGPTClient
        return ChatGPTClient(
            api_key=os.environ.get("OPENROUTER_API_KEY", ""),
            model=model, timeout=timeout,
        )

    elif mode == "fake":
        from .fake import FakeLLMClient
        return FakeLLMClient(response=response)

    else:
        raise NotImplementedError(
            f"Provided LLMClient mode is not supported: {mode}"
        )
