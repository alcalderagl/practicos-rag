from pydantic import BaseModel
from typing import Optional


class Evaluation(BaseModel):
    """
    Represents an evaluation containing various elements related to a question and its context.

    Attributes
    ----------
    question : list[str]
        The main question(s) being evaluated. Each question is represented as a string.
    answer : Optional[list[str]]
        An optional list of possible answers for the question. Default is None.
    reference : list[str]
        A list of references used in the evaluation, where each reference is a string.
    retrieved_contexts : Optional[list[list[str]]]
        An optional list of contexts retrieved as part of the evaluation process, where each context is a list of strings.
    """

    question: list[str]
    answer: Optional[list[str]]
    reference: list[str]
    retrieved_contexts: Optional[list[list[str]]]
