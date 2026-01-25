from typing import Tuple

from sqlalchemy import insert, select, update
from sqlalchemy.engine import Engine

from backend.db import answer_config_table


class SqlAnswerConfigRepo:

    def __init__(self, engine: Engine):
        self.engine = engine

    def set_config(self, chat_id: int, left: bool, right: bool) -> None:
        with self.engine.begin() as conn:
            exists = conn.execute(
                select(answer_config_table.c.chat_id)
                .where(answer_config_table.c.chat_id == chat_id)
            ).first()

            if isinstance(exists, type(None)):
                conn.execute(
                    insert(answer_config_table).values(
                        chat_id=chat_id,
                        left=left,
                        right=right,
                    )
                )
            else:
                conn.execute(
                    update(answer_config_table)
                    .where(answer_config_table.c.chat_id == chat_id)
                    .values(left=left, right=right)
                )

    def get_config(self, chat_id: int) -> Tuple[bool, bool]:

        with self.engine.begin() as conn:
            row = conn.execute(
                select(answer_config_table.c.left, answer_config_table.c.right)
                .where(answer_config_table.c.chat_id == chat_id)
            ).first()

        if row is None:
            return (False, False)

        return (row.left, row.right)
