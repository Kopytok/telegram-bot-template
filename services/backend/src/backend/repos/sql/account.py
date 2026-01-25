from datetime import datetime, timezone

from sqlalchemy import insert, select
from sqlalchemy.engine import Engine

from backend.db import account_table


class SqlAccountRepo:

    def __init__(self, engine: Engine):
        self.engine = engine

    def ensure_exists(self, chat_id: int) -> None:
        with self.engine.begin() as conn:
            exists = conn.execute(
                select(account_table.c.chat_id)
                .where(account_table.c.chat_id == chat_id)
            ).first()

            if exists is None:
                conn.execute(
                    insert(account_table).values(
                        chat_id=chat_id,
                        created_at=datetime.now(timezone.utc)
                    )
                )
