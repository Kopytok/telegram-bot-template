class InMemoryUserMessageRepo:

    def __init__(self):
        self.messages: list[tuple[int, str]] = []

    def persist(self, chat_id: int, text: str) -> None:
        self.messages.append((chat_id, text))
