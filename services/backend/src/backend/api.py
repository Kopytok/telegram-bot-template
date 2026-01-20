from fastapi import FastAPI, Depends

from backend.db import lifespan
from backend.models import (
    MessageIn,
    MessageOut,
)
from backend.storage import (
    persist_incoming_message,
    get_conversation_repo,
)
from domain.tripled import triple_message
from llm import DialogueService, LLMClientFactory
from llm.repo.base import ConversationRepository

app = FastAPI(lifespan=lifespan)


@app.post("/message", response_model=MessageOut)
async def handle_message(
    msg: MessageIn,
    conversation_repo: ConversationRepository = Depends(get_conversation_repo),
) -> MessageOut:
    persist_incoming_message(msg)

    if msg.button_id == "Cancel":
        reply = "Back to main menu"
        keyboard_type = "main"

    elif msg.button_id == "A":
        reply = "Button A was pressed!"
        keyboard_type = "cancel"

    elif msg.button_id == "B":
        reply = "Button B was pressed!"
        keyboard_type = "cancel"

    else:
        if msg.text.startswith("LLM:"):
            llm = LLMClientFactory.create("chatgpt")
            service = DialogueService(
                llm,
                repo=conversation_repo,
                system_prompt="The system prompt",
            )
            reply = await service.handle_user_message(
                user_id=str(msg.user_id),
                text=msg.text[4:],
            )

        else:
            reply = triple_message(msg.text)

        keyboard_type = "main"

    return MessageOut(reply=reply, keyboard_type=keyboard_type)
