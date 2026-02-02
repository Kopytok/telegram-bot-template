from llm.workflow import LLMWorkFlow
from llm.aggregator import SimpleAggregator
from llm.models import LeftRightStep
from llm.tasks.initial_answer import InitialAnswerTask
from llm.tasks.joke import LeftTask
from llm.tasks.math import RightTask
from llm.client import LLMClient


def build_workflow(llm: LLMClient) -> LLMWorkFlow:
    return LLMWorkFlow(
        tasks={
            LeftRightStep.MAIN: InitialAnswerTask(llm),
            LeftRightStep.LEFT: LeftTask(llm),
            LeftRightStep.RIGHT: RightTask(llm),
        },
        aggregator=SimpleAggregator(),
    )
