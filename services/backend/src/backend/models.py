from pydantic import BaseModel
from typing import Optional


class MessageIn(BaseModel):
    user_id: int
    text: str


class MessageOut(BaseModel):
    reply: str
    keyboard_type: Optional[str] = None


class BotMessage(BaseModel):
    message_id: int
    user_id: int
    text: str
