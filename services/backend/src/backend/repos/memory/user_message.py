class InMemoryUserMessageRepo:

    def __init__(self):
        self.messages: list[tuple[int, str]] = []

    def persist(self, user_id: int, text: str) -> None:
        self.messages.append((user_id, text))
