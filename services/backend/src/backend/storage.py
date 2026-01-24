from datetime import datetime, timezone

from fastapi import Request
from sqlalchemy import (
    insert,
    select,
)

from backend.db import (
    engine,
    account_table,
    message_table,
    bot_message_table,
)
from backend.models import MessageIn
from llm.repo.redis import RedisConversationRepository
from llm.repo.in_memory import InMemoryConversationRepository
from llm.repo.base import ConversationRepository


def persist_incoming_message(msg: MessageIn) -> None:
    with engine.begin() as conn:
        now = datetime.now(timezone.utc)

        # Create account if not exists
        any_account = conn.execute(
            select(account_table)
            .where(account_table.c.user_id == msg.user_id)
        ).first()

        if any_account is None:
            stmt = (
                insert(account_table)
                .values(user_id=msg.user_id, created_at=now)
            )
            conn.execute(stmt)

        # Save message
        stmt = (
            insert(message_table)
            .values(user_id=msg.user_id, text=msg.text, created_at=now)
        )
        conn.execute(stmt)


def store_bot_message(
    message_id: int,
    user_id: int,
    text: str,
) -> None:
    with engine.begin() as conn:
        stmt = insert(bot_message_table).values(
            message_id=message_id,
            user_id=user_id,
            text=text,
            created_at=datetime.now(timezone.utc),
        )
        conn.execute(stmt)


def get_bot_message_text(
    message_id: int,
) -> str:
    with engine.begin() as conn:
        stmt = (
            select(bot_message_table.c.text)
            .where(bot_message_table.c.message_id == message_id)
        )
        row = conn.execute(stmt).first()
        if row is None:
            raise KeyError("Bot message not found")

        return row.text


def get_conversation_repo(request: Request) -> ConversationRepository:
    """
    FastAPI dependency.
    Creates a repository bound to the app Redis instance.
    """
    try:
        redis = request.app.state.redis
        return RedisConversationRepository(redis)
    except Exception:
        return InMemoryConversationRepository()
