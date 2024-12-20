from pydantic import BaseModel
from typing import Optional

class Evaluation(BaseModel):
    question: list[str]
    answer: Optional[list[str]]
    reference: list[str]
    retrieved_contexts: Optional[list[list[str]]]
