from llm.context import LLMContext
from llm.tasks.base import LLMTask


class LLMWorkFlow:

    def __init__(self, tasks: list[LLMTask], aggregator):
        self.tasks = tasks
        self.aggregator = aggregator

    async def run(self, user_message: str) -> str:
        ctx = LLMContext(user_message=user_message)

        for task in self.tasks:
            await task.run(ctx)

        return self.aggregator.aggregate(ctx)
