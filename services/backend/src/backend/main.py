from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class MessageIn(BaseModel):
    user_id: int
    text: str


class MessageOut(BaseModel):
    reply: str


@app.post("/message", response_model=MessageOut)
async def handle_message(msg: MessageIn) -> MessageOut:
    tripled = " ".join([msg.text] * 3)
    return MessageOut(reply=tripled)
