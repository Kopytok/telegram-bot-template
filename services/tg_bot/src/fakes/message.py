from dataclasses import dataclass
from typing import List


@dataclass
class FakeMessageCall:
    reply_text: str
    kwargs: dict


@dataclass
class FakeChat:
    id: int


@dataclass
class FakeMessage:
    chat: FakeChat
    text: str

    def __init__(
        self,
        message_id: int,
        chat: FakeChat,
        text: str,
    ) -> None:
        self.message_id = message_id
        self.chat = chat
        self.text = text
        self.calls: List[FakeMessageCall] = []

    @classmethod
    def create(
        cls,
        message_id: int,
        user_id: int,
        text: str,
    ) -> "FakeMessage":
        return cls(
            message_id=message_id,
            chat=FakeChat(id=user_id),
            text=text,
        )

    async def answer(self, text: str, **kwargs) -> 'FakeMessage':
        _ = text, kwargs
        self.calls.append(FakeMessageCall(text, kwargs))
        return self

    async def delete(self) -> 'FakeMessage':
        return self
