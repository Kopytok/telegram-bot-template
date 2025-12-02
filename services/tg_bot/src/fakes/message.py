from dataclasses import dataclass
from typing import List


@dataclass
class FakeMessageCall:
    reply_text: str
    kwargs: dict


@dataclass
class FakeUser:
    id: int


@dataclass
class FakeMessage:
    from_user: FakeUser
    text: str

    def __init__(self, from_user: FakeUser, text: str) -> None:
        self.from_user = from_user
        self.text = text
        self.calls: List[FakeMessageCall] = []

    @classmethod
    def create(cls, user_id: int, text: str) -> "FakeMessage":
        return cls(from_user=FakeUser(id=user_id), text=text)

    async def answer(self, text: str, **kwargs) -> None:
        _ = text, kwargs
        self.calls.append(FakeMessageCall(text, kwargs))
