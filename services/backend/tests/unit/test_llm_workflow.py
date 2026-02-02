import pytest

from llm.factory import build_workflow
from llm.models import LeftRightStep
from llm import get_llm_client


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "steps,expected",
    (
        (
            [LeftRightStep.MAIN, LeftRightStep.LEFT, LeftRightStep.RIGHT],
            """The answer
---
Left
---
Right"""
        ),
        (
            [LeftRightStep.MAIN,],
            """The answer"""
        ),
        (
            [LeftRightStep.MAIN, LeftRightStep.LEFT],
            """The answer
---
Left"""
        ),
        (
            [LeftRightStep.MAIN, LeftRightStep.RIGHT],
            """The answer
---
Right"""
        ),
    )
)
async def test_llm_workflow(steps, expected):
    # Setup
    expected_response = "The answer"
    llm = get_llm_client("fake", response=expected_response)

    # Run
    workflow = build_workflow(llm)
    result = await workflow.run("Hello", steps)

    # Check
    assert result == expected
