from typing import List


class InMemoryUserMessageRepo:

    def __init__(self):
        self.messages: list[tuple[int, str]] = []

    def persist(self, chat_id: int, text: str) -> None:
        self.messages.append((chat_id, text))

    def get_texts(self, chat_id: int) -> List[str]:
        texts = []
        for c, text in self.messages:
            if c == chat_id:
                texts.append(text)
        return texts
