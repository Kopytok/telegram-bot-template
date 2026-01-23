from datetime import datetime, timezone

from fastapi import Request
from sqlalchemy import (
    insert,
    select,
)

from backend.db import (
    message_table,
    account_table,
    engine,
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


def get_message_text(message_id: int) -> str:
    try:
        _ = message_id
        return "YO"
    except KeyError:
        raise ValueError("Message not found")
