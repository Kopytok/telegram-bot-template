from typing import Protocol


class AccountRepo(Protocol):
    def ensure_exists(self, chat_id: int) -> None: ...


class UserMessageRepo(Protocol):
    def persist(self, chat_id: int, text: str) -> None: ...


class BotMessageRepo(Protocol):
    def create(self, message_id: int, chat_id: int, text: str) -> None: ...
    def get_text(self, message_id: int) -> str: ...
