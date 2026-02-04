from typing import List, Dict

from llm.context import LLMContext
from llm.models import LeftRightStep
from llm.tasks.base import LLMTask


class LLMWorkFlow:

    def __init__(
        self,
        tasks: Dict[LeftRightStep, LLMTask],
        aggregator,
    ):
        self.tasks = tasks
        self.aggregator = aggregator

    async def run(
        self,
        user_message: str,
        steps: List[LeftRightStep],
    ) -> str:
        ctx = LLMContext(user_message=user_message)

        for step in steps:
            task = self.tasks[step]
            await task.run(ctx)

        return self.aggregator.aggregate(ctx)
