from abc import ABC, abstractmethod
from typing import List, Dict


class LLMClient(ABC):

    @abstractmethod
    async def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.3,
    ) -> str:
        """
        messages:
        [
            {"role": "system", "content": "..."},
            {"role": "user", "content": "..."}
        ]
        """
        pass
