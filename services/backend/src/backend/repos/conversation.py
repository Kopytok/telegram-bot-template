from fastapi import Request
from llm.repo.redis import RedisConversationRepository
from llm.repo.in_memory import InMemoryConversationRepository
from llm.repo.base import ConversationRepository


def get_conversation_repo(request: Request) -> ConversationRepository:
    try:
        redis = request.app.state.redis
        return RedisConversationRepository(redis)
    except Exception:
        return InMemoryConversationRepository()
