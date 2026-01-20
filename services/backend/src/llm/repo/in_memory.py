from .base import ConversationRepository
from .models import Message


class InMemoryConversationRepository(ConversationRepository):
    def __init__(self):
        self.storage: dict[str, list[Message]] = {}

    async def get_messages(self, conversation_id: str):
        return self.storage.get(conversation_id, [])

    async def append_message(self, conversation_id: str, message: Message):
        self.storage.setdefault(conversation_id, []).append(message)

    async def clear(self, conversation_id: str):
        self.storage.pop(conversation_id, None)
