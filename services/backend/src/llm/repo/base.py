from abc import ABC, abstractmethod
from typing import List
from .models import Message


class ConversationRepo(ABC):
    @abstractmethod
    async def get_messages(self, conversation_id: str) -> List[Message]:
        pass

    @abstractmethod
    async def append_message(
        self,
        conversation_id: str,
        message: Message,
    ) -> None:
        pass

    @abstractmethod
    async def clear(self, conversation_id: str) -> None:
        pass
