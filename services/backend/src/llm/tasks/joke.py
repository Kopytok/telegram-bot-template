from llm.context import LLMContext
from llm.client import LLMClient
from llm.models import LeftRightStep


class LeftTask:

    def __init__(self, llm: LLMClient):
        self.llm = llm

    async def run(self, ctx: LLMContext) -> None:
        response = await self.llm.chat(
            messages=[
                {"role": "user", "content": "Tell me a joke"},
            ]
        )
        ctx.results[LeftRightStep.LEFT] = response
