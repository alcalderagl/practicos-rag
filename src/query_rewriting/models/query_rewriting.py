from pydantic import BaseModel


class QuestionRewriting(BaseModel):
    """
    Represents a question rewriting model.

    Attributes
    ----------
    query : str
        The original question.
    rewriting_query : str
        The rewritten version of the original question.
    """

    query: str
    rewriting_query: str
