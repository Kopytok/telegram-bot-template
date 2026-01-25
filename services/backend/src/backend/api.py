from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

from backend.db import lifespan
from backend.models import (
    MessageIn,
    MessageOut,
)
from domain.tripled import triple_message
from llm import DialogueService, LLMClientFactory

from backend.repos import (
    AccountRepo,
    UserMessageRepo,
    BotMessageRepo,
    ConversationRepository,
    get_account_repo,
    get_user_message_repo,
    get_bot_message_repo,
    get_conversation_repo,
)

app = FastAPI(lifespan=lifespan)


@app.post("/message", response_model=MessageOut)
async def handle_message(
    msg: MessageIn,
    conversation_repo: ConversationRepository = Depends(get_conversation_repo),
    account_repo: AccountRepo = Depends(get_account_repo),
    user_message_repo: UserMessageRepo = Depends(get_user_message_repo),
) -> MessageOut:
    account_repo.ensure_exists(msg.user_id)
    user_message_repo.persist(msg.user_id, msg.text)

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
    bot_message_repo: BotMessageRepo = Depends(get_bot_message_repo),
) -> InlineActionResponse:
    try:
        text = bot_message_repo.get_text(payload.message_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Message not found")

    new_text = text
    if payload.left:
        new_text = "Left " + new_text

    if payload.right:
        new_text = new_text + " Right"

    return InlineActionResponse(text=new_text)


class SaveAnswerRequest (BaseModel):
    message_id: int
    user_id: int
    text: str


class SaveAnswerResponse (BaseModel):
    status: str


@app.post("/save_answer", response_model=SaveAnswerResponse)
async def handle_save_answer(
    payload: SaveAnswerRequest,
    bot_message_repo: BotMessageRepo = Depends(get_bot_message_repo),
) -> SaveAnswerResponse:
    bot_message_repo.create(
        message_id=payload.message_id,
        user_id=payload.user_id,
        text=payload.text,
    )
    return SaveAnswerResponse(status="OK")
