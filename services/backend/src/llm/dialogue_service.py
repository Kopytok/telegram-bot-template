from datetime import datetime
from llm.repo.base import ConversationRepository
from .client import LLMClient
from .repo.models import Message


class DialogueService:

    def __init__(
        self,
        llm: LLMClient,
        repo: ConversationRepository,
        system_prompt: str,
    ):
        self.llm = llm
        self.repo = repo
        self.system_prompt = system_prompt

    async def handle_user_message(
        self,
        user_id: str,
        text: str,
    ) -> str:
        await self.repo.append_message(
            user_id,
            Message("user", text, datetime.now()),
        )
        history = await self.repo.get_messages(user_id)
        messages = [
            {"role": "system", "content": self.system_prompt},
            *(h.__dict__ for h in history)
        ]
        reply = await self.llm.chat(messages)

        await self.repo.append_message(
            user_id,
            Message("assistant", reply, datetime.now()),
        )

        return reply
