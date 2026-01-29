import pytest
from llm.factory import build_workflow
from llm import get_llm_client


@pytest.mark.asyncio
async def test_llm_workflow():
    # Setup
    expected_response = "The answer"
    llm = get_llm_client("fake", response=expected_response)

    # Run
    workflow = build_workflow(llm)
    result = await workflow.run("Hello")

    # Check
    assert result == """The answer
---
The answer
---
The answer"""
