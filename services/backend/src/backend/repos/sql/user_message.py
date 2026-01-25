from datetime import datetime, timezone
from typing import List

from sqlalchemy import insert, select
from sqlalchemy.engine import Engine

from backend.db import message_table


class SqlUserMessageRepo:

    def __init__(self, engine: Engine):
        self.engine = engine

    def persist(self, chat_id: int, text: str) -> None:
        with self.engine.begin() as conn:
            conn.execute(
                insert(message_table).values(
                    chat_id=chat_id,
                    text=text,
                    created_at=datetime.now(timezone.utc),
                )
            )

    def get_texts(self, chat_id: int) -> List[str]:

        with self.engine.begin() as conn:
            rows = conn.execute(
                select(message_table.c.text)
                .where(message_table.c.chat_id == chat_id)
            )

        texts = []
        for r in rows:
            texts.append(r.text)
        return texts
