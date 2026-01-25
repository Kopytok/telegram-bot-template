from datetime import datetime, timezone

from sqlalchemy import insert, select
from sqlalchemy.engine import Engine

from backend.db import bot_message_table


class SqlBotMessageRepo:

    def __init__(self, engine: Engine):
        self.engine = engine

    def create(self, message_id: int, chat_id: int, text: str) -> None:
        with self.engine.begin() as conn:
            conn.execute(insert(bot_message_table).values(
                message_id=message_id,
                chat_id=chat_id,
                text=text,
                created_at=datetime.now(timezone.utc),
            ))

    def get_text(self, message_id: int) -> str:
        with self.engine.begin() as conn:
            row = conn.execute(
                select(bot_message_table.c.text)
                .where(bot_message_table.c.message_id == message_id)
            ).first()

        if row is None:
            raise KeyError("Bot message not found")

        return row.text
