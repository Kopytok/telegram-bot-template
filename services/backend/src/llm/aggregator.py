from llm.context import LLMContext


class SimpleAggregator:
    def aggregate(self, ctx: LLMContext) -> str:
        return "\n---\n".join([
            ctx.results["initial_answer"],
            ctx.results["joke"],
            ctx.results["math"],
        ])
