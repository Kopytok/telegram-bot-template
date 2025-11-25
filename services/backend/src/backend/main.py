import os
from datetime import datetime, timezone
from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel

from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    BigInteger,
    DateTime,
    Text,
    insert,
)
from sqlalchemy.engine import Engine

# --- Database setup ---

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///:memory:")

engine: Engine = create_engine(DATABASE_URL, future=True)
metadata = MetaData()

messages_table = Table(
    "messages",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("chat_id", BigInteger, nullable=False, index=True),
    Column("text", Text, nullable=False),
    Column(
        "created_at",
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    ),
)


def init_db() -> None:
    metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


# --- Models ---

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


# --- Fast API ---

app = FastAPI()


@app.post("/message", response_model=MessageOut)
async def handle_message(msg: MessageIn) -> MessageOut:

    with engine.begin() as conn:
        stmt = (
            insert(messages_table)
            .values(
                chat_id=msg.user_id,
                text=msg.text,
                created_at=datetime.now(timezone.utc),
            )
        )
        conn.execute(stmt)

    tripled = " ".join([msg.text] * 3)
    return MessageOut(reply=tripled)
