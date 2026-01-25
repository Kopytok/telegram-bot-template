from collections import defaultdict


class InMemoryAccountRepo:

    def __init__(self):
        self.called = defaultdict(lambda: False)

    def ensure_exists(self, chat_id: int) -> None:
        self.called[chat_id] = True

    def exists(self, chat_id:int) -> bool:
        return self.called[chat_id]
