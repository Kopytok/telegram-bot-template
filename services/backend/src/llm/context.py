from dataclasses import dataclass, field
from typing import Dict


@dataclass
class LLMContext:
    user_message: str
    results: Dict[str, str] = field(default_factory=dict)
