from datetime import datetime, timezone

from sqlalchemy import insert
from sqlalchemy.engine import Engine

from backend.db import message_table


class SqlUserMessageRepo:

    def __init__(self, engine: Engine):
        self.engine = engine

    def persist(self, user_id: int, text: str) -> None:
        with self.engine.begin() as conn:
            conn.execute(
                insert(message_table).values(
                    user_id=user_id,
                    text=text,
                    created_at=datetime.now(timezone.utc),
                )
            )
