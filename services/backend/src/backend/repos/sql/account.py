from datetime import datetime, timezone

from sqlalchemy import insert, select
from sqlalchemy.engine import Engine

from backend.db import account_table


class SqlAccountRepo:

    def __init__(self, engine: Engine):
        self.engine = engine

    def ensure_exists(self, chat_id: int) -> None:
        if self.exists(chat_id):
            with self.engine.begin() as conn:
                conn.execute(
                    insert(account_table).values(
                        chat_id=chat_id,
                        created_at=datetime.now(timezone.utc)
                    )
                )

    def exists(self, chat_id: int) -> bool:
        with self.engine.begin() as conn:
            exists = conn.execute(
                select(account_table.c.chat_id)
                .where(account_table.c.chat_id == chat_id)
            ).first()
        return not isinstance(exists, type(None))
