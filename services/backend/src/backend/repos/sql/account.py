from datetime import datetime, timezone

from sqlalchemy import insert, select
from sqlalchemy.engine import Engine

from backend.db import account_table


class SqlAccountRepo:

    def __init__(self, engine: Engine):
        self.engine = engine

    def ensure_exists(self, user_id: int) -> None:
        with self.engine.begin() as conn:
            exists = conn.execute(
                select(account_table.c.user_id)
                .where(account_table.c.user_id == user_id)
            ).first()

            if exists is None:
                conn.execute(
                    insert(account_table).values(
                        user_id=user_id,
                        created_at=datetime.now(timezone.utc)
                    )
                )
