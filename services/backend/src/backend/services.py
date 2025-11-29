from datetime import datetime, timezone
from sqlalchemy import (
    insert,
)

from backend.models import (
    MessageIn,
    MessageOut,
)
from backend.db import (
    messages_table,
    engine,
)


def process_message(msg: MessageIn) -> MessageOut:

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
