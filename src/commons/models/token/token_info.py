from pydantic import BaseModel
from typing import Union


class TokenInfo(BaseModel):
    """
    The original text of the token.
    """

    text: str
    """
    The base form (lemma) of the token.
    """
    lemma: str
    """
    The part-of-speech tag of the token, which indicates its grammatical role.
    """
    pos: Union[str, int]
    """
    The syntactic dependency of the token in the sentence.
    """
    dep: str
    """
    The entity type of the token, if it belongs to a named entity.
    """
    ent_type: str
    """
    Indicates whether the token is a stopword 
    """
    is_stopword: bool
