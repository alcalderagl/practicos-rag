from pydantic import BaseModel


class QuestionAnswer(BaseModel):
    """
    Represents a simple Question and Answer pair.

    Attributes
    ----------
    question : str
        The text of the question.
    answer : str
        The text of the answer corresponding to the question.
    """

    question: str
    answer: str
