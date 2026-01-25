class InMemoryBotMessageRepo:

    def __init__(self):
        self._data: dict[int, str] = {}

    def create(self, message_id: int, user_id: int, text: str) -> None:
        _ = user_id
        self._data[message_id] = text

    def get_text(self, message_id: int) -> str:
        try:
            return self._data[message_id]
        except KeyError:
            raise KeyError("Bot message not found")
