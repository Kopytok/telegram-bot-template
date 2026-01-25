from typing import Tuple, Dict


class InMemoryAnswerConfigRepo:

    def __init__(self):
        self.memory: Dict[int, Tuple[bool, bool]] = {}

    def set_config(self, chat_id: int, left: bool, right: bool) -> None:
        self.memory[chat_id] = (left, right)

    def get_config(self, chat_id: int) -> Tuple[bool, bool]:
        try:
            return self.memory[chat_id]
        except KeyError:
            return (False, False)
