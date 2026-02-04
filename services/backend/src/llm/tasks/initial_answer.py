from llm.context import LLMContext
from llm.client import LLMClient
from llm.models import LeftRightStep


SYSTEM_PROMPT = "You're a helpful assistant."


class InitialAnswerTask:

    def __init__(self, llm: LLMClient):
        self.llm = llm

    async def run(self, ctx: LLMContext) -> None:
        response = await self.llm.chat(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": ctx.user_message},
            ]
        )
        ctx.results[LeftRightStep.MAIN] = response
