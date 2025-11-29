from fastapi import FastAPI

from backend.db import lifespan
from backend.models import (
    MessageIn,
    MessageOut,
)
from backend.services import process_message

app = FastAPI(lifespan=lifespan)


@app.post("/message", response_model=MessageOut)
async def handle_message(msg: MessageIn) -> MessageOut:
    return process_message(msg)
