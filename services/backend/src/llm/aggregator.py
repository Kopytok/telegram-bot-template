from llm.context import LLMContext
from llm.models import LeftRightStep


class SimpleAggregator:
    def aggregate(self, ctx: LLMContext) -> str:
        parts = [ctx.results[LeftRightStep.MAIN]]

        if LeftRightStep.LEFT in ctx.results:
            parts.append("Left")

        if LeftRightStep.RIGHT in ctx.results:
            parts.append("Right")

        return "\n---\n".join(parts)
