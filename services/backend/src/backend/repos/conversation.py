from fastapi import Request
from llm.repo.redis import RedisConversationRepo
from llm.repo.in_memory import InMemoryConversationRepo
from llm.repo.base import ConversationRepo


def get_conversation_repo(request: Request) -> ConversationRepo:
    try:
        redis = request.app.state.redis
        return RedisConversationRepo(redis)
    except Exception:
        return InMemoryConversationRepo()
