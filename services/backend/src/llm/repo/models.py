import json
from dataclasses import dataclass
from datetime import datetime
from typing import Literal


@dataclass
class Message:
    role: Literal["system", "user", "assistant"]
    content: str
    timestamp: datetime

    @classmethod
    def from_json(cls, data: str) -> 'Message':
        try:
            d = json.loads(data)
            return cls(d["role"], d["content"], d["timestamp"])
        except Exception:
            raise NotImplementedError(f"{data}")

    def to_json(self) -> str:
        return (
            '{'
            f'"role":"{self.role}",'
            f'"content":"{self.content}",'
            f'"timestamp":"{self.timestamp}"'
            '}'
        )


@dataclass
class Conversation:
    id: str              # chat_id / user_id
    messages: list[Message]
