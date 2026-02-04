from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional

from backend.db import lifespan
from backend.repos import (
    AccountRepo,
    UserMessageRepo,
    BotMessageRepo,
    AnswerConfigRepo,
    ConversationRepo,
    get_account_repo,
    get_user_message_repo,
    get_bot_message_repo,
    get_answer_config_repo,
    get_conversation_repo,
)
from domain import (
    triple_message,
    left_right_switch,
)
from llm import DialogueService, get_llm_client
from llm.factory import build_workflow
from llm.models import LeftRightStep

app = FastAPI(lifespan=lifespan)


class MessageIn(BaseModel):
    chat_id: int
    text: str


class MessageOut(BaseModel):
    reply: str
    keyboard_type: Optional[str] = None


STEPS = [
    LeftRightStep.MAIN,
    LeftRightStep.LEFT,
    LeftRightStep.RIGHT,
]


@app.post("/message", response_model=MessageOut)
async def handle_message(
    msg: MessageIn,
    conversation_repo: ConversationRepo = Depends(get_conversation_repo),
    account_repo: AccountRepo = Depends(get_account_repo),
    user_message_repo: UserMessageRepo = Depends(get_user_message_repo),
) -> MessageOut:

    account_repo.ensure_exists(msg.chat_id)
    user_message_repo.persist(msg.chat_id, msg.text)

    if msg.text.startswith("Dialogue:"):

        llm = get_llm_client("chatgpt")
        service = DialogueService(
            llm,
            repo=conversation_repo,
            system_prompt="The system prompt",
        )
        reply = await service.handle_user_message(
            chat_id=str(msg.chat_id),
            text=msg.text[4:],
        )
        keyboard_type = "inline_flow"

    elif msg.text.startswith("Pipeline:"):

        llm = get_llm_client("chatgpt")
        workflow = build_workflow(llm)
        reply = await workflow.run(msg.text[9:], STEPS)
        keyboard_type = None

    else:

        reply = triple_message(msg.text)
        keyboard_type = None

    return MessageOut(reply=reply, keyboard_type=keyboard_type)


class SaveAnswerRequest (BaseModel):
    message_id: int
    chat_id: int
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
        chat_id=payload.chat_id,
        text=payload.text,
    )
    return SaveAnswerResponse(status="OK")


class LeftRightSwitchRequest(BaseModel):
    message_id: int
    chat_id: int
    toggle_left: bool = False
    toggle_right: bool = False


class LeftRightSwitchResponse(BaseModel):
    text: str


@app.post("/left_right_switch", response_model=LeftRightSwitchResponse)
async def handle_left_right_switch(
    payload: LeftRightSwitchRequest,
    bot_message_repo: BotMessageRepo = Depends(get_bot_message_repo),
    answer_config_repo: AnswerConfigRepo = Depends(get_answer_config_repo)
) -> LeftRightSwitchResponse:
    try:
        message_text = bot_message_repo.get_text(payload.message_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Message not found")

    chat_id = payload.chat_id
    answer_config = answer_config_repo.get_config(chat_id)

    text, config = left_right_switch(
        message_text, answer_config,
        payload.toggle_left, payload.toggle_right
    )
    answer_config_repo.set_config(chat_id, *config)

    return LeftRightSwitchResponse(text=text)
