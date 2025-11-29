from datetime import datetime, timezone
from sqlalchemy import (
    insert,
    select,
)

from backend.models import (
    MessageIn,
    MessageOut,
)
from backend.db import (
    message_table,
    account_table,
    engine,
)


def process_message(msg: MessageIn) -> MessageOut:

    with engine.begin() as conn:
        now = datetime.now(timezone.utc)

        # Create account if not exists
        any_account = conn.execute(
            select(account_table)
            .where(account_table.c.chat_id == msg.user_id)
        ).first()

        if any_account is None:
            stmt = (
                insert(account_table)
                .values(chat_id=msg.user_id, created_at=now)
            )
            conn.execute(stmt)

        # Save message
        stmt = (
            insert(message_table)
            .values(chat_id=msg.user_id, text=msg.text, created_at=now)
        )
        conn.execute(stmt)

    tripled = " ".join([msg.text] * 3)
    return MessageOut(reply=tripled)
