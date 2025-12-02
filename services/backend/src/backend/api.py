from fastapi import FastAPI

from backend.db import lifespan
from backend.models import (
    MessageIn,
    MessageOut,
)
from backend.storage import persist_incoming_message
from domain.tripled import triple_message

app = FastAPI(lifespan=lifespan)


@app.post("/message", response_model=MessageOut)
async def handle_message(msg: MessageIn) -> MessageOut:
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
        reply = triple_message(msg.text)
        keyboard_type = "main"

    return MessageOut(reply=reply, keyboard_type=keyboard_type)
