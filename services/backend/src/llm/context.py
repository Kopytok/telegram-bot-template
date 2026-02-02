from dataclasses import dataclass, field
from typing import Dict
from llm.models import LeftRightStep


@dataclass
class LLMContext:
    user_message: str
    results: Dict[LeftRightStep, str] = field(default_factory=dict)
