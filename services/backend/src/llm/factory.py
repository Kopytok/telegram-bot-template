from llm.workflow import LLMWorkFlow
from llm.aggregator import SimpleAggregator
from llm.tasks.initial_answer import InitialAnswerTask
from llm.tasks.joke import JokeTask
from llm.tasks.math import MathTask
from llm.client import LLMClient


def build_workflow(llm: LLMClient) -> LLMWorkFlow:
    return LLMWorkFlow(
        tasks=[
            InitialAnswerTask(llm),
            JokeTask(llm),
            MathTask(llm),
        ],
        aggregator=SimpleAggregator(),
    )
