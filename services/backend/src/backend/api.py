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
    return MessageOut(reply=triple_message(msg.text))
