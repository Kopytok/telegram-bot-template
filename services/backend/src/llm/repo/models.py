import json
from dataclasses import dataclass
from datetime import datetime
from typing import Literal, Dict


@dataclass
class Message:
    role: Literal["system", "user", "assistant"]
    content: str
    timestamp: datetime

    @classmethod
    def from_json(cls, data: str) -> 'Message':
        try:
            d = json.loads(data)
        except Exception:
            raise NotImplementedError(f"{data}")

        try:
            return cls(d["role"], d["content"], d["timestamp"])
        except Exception:
            raise NotImplementedError(f"{d}")

    @property
    def role_content(self) -> Dict[str, str]:
        return {"role": self.role, "content": self.content}

    def to_json(self) -> str:
        return json.dumps({
            "role": self.role,
            "content": self.content,
            "timestamp": str(self.timestamp),
        })
