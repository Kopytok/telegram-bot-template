import os
from datetime import datetime, timezone
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    BigInteger,
    DateTime,
    Text,
)
from sqlalchemy.engine import Engine
from sqlalchemy.pool import StaticPool

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///:memory:")

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        future=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    engine: Engine = create_engine(DATABASE_URL, future=True)

metadata = MetaData()

account_table = Table(
    "account",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("chat_id", BigInteger, nullable=False, index=True),
    Column(
        "created_at",
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    ),
)

message_table = Table(
    "message",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("chat_id", BigInteger, nullable=False, index=True),
    Column("text", Text, nullable=False),
    Column(
        "created_at",
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    ),
)


def init_db() -> None:
    metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    _ = app
    init_db()
    yield
