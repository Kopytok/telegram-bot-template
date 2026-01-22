from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class MessageIn(BaseModel):
    user_id: int
    text: str


class MessageOut(BaseModel):
    reply: str
    keyboard_type: Optional[str] = None


class StoredMessage(BaseModel):
    id: int
    user_id: int
    text: str
    created_at: datetime
