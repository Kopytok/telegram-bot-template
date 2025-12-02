from datetime import datetime, timezone
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
