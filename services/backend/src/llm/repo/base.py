from typing import List, Protocol
from .models import Message


class ConversationRepo(Protocol):

    async def get_messages(self, conversation_id: str) -> List[Message]: ...

    async def append_message(
        self,
        conversation_id: str,
        message: Message,
    ) -> None: ...

    async def clear(self, conversation_id: str) -> None: ...
