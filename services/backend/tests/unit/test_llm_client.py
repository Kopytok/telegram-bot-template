import pytest
from llm import (
    LLMClientFactory,
    DialogueService,
)
from llm.repo.in_memory import InMemoryConversationRepository


@pytest.mark.asyncio
async def test_dialogue_service():
    # Setup
    user_id = "USER_ID"
    expected_response = "The answer"
    system_prompt = "The system prompt"
    llm = LLMClientFactory.create("fake", response=expected_response)
    repo = InMemoryConversationRepository()
    service = DialogueService(llm, repo, system_prompt)

    # Run
    message_text = "The message"
    result = await service.handle_user_message(user_id, message_text)

    # Check
    assert result == expected_response, "Not expected response from llm client"
    assert len(llm.calls) == 1, "Wrong number of client calls"
    assert llm.calls[0] == {
        "messages": [
            {
                "content": system_prompt,
                "role": "system",
            },
            {
                "content": message_text,
                "role": "user",
            },
        ],
        "temperature": 0.3,
    }, "Not expected llm call arguments"
