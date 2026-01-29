from typing import Protocol
from llm.context import LLMContext


class LLMTask(Protocol):
    async def run(self, ctx: LLMContext) -> None:
        ...
