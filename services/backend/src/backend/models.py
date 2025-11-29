from datetime import datetime
from pydantic import BaseModel


class MessageIn(BaseModel):
    user_id: int
    text: str


class MessageOut(BaseModel):
    reply: str


class StoredMessage(BaseModel):
    id: int
    chat_id: int
    text: str
    created_at: datetime
