from .base import ConversationRepo
from .models import Message
from backend.settings import settings


class RedisConversationRepo(ConversationRepo):
    def __init__(self, redis):
        self.redis = redis

    @staticmethod
    def _key(conversation_id: str) -> str:
        return f"conversation:{conversation_id}"

    async def get_messages(self, conversation_id: str):
        raw = await self.redis.lrange(self._key(conversation_id), 0, -1)
        return [Message.from_json(x) for x in raw]

    async def append_message(
        self,
        conversation_id: str,
        message: Message,
    ) -> None:
        key = self._key(conversation_id)
        await self.redis.rpush(key, message.to_json())
        await self.redis.expire(key, settings.redis_ttl_seconds)

    async def clear(self, conversation_id: str):
        await self.redis.delete(self._key(conversation_id))
