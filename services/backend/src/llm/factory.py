from llm.workflow import LLMWorkFlow
from llm.aggregator import SimpleAggregator
from llm.models import LeftRightStep
from llm.tasks.initial_answer import InitialAnswerTask
from llm.tasks.joke import JokeTask
from llm.tasks.math import MathTask
from llm.client import LLMClient


def build_workflow(llm: LLMClient) -> LLMWorkFlow:
    return LLMWorkFlow(
        tasks={
            LeftRightStep.MAIN: InitialAnswerTask(llm),
            LeftRightStep.LEFT: JokeTask(llm),
            LeftRightStep.RIGHT: MathTask(llm),
        },
        aggregator=SimpleAggregator(),
    )
