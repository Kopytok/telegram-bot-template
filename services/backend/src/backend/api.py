from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

from backend.db import lifespan
from backend.models import (
    MessageIn,
    MessageOut,
)
from backend.storage import (
    persist_incoming_message,
    get_conversation_repo,
    get_message_text,
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
        keyboard_type = "inline_flow"

    else:
        reply = triple_message(msg.text)
        keyboard_type = None

    return MessageOut(reply=reply, keyboard_type=keyboard_type)


class InlineActionRequest(BaseModel):
    message_id: int
    left: bool = False
    right: bool = False


class InlineActionResponse(BaseModel):
    text: str


@app.post("/some_endpoint", response_model=InlineActionResponse)
async def handle_inline_action(
    payload: InlineActionRequest,
) -> InlineActionResponse:
    try:
        text = get_message_text(payload.message_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Message not found")

    new_text = text
    if payload.left:
        new_text = "Left " + new_text

    if payload.right:
        new_text = new_text + " Right"

    return InlineActionResponse(text=new_text)
