from pydantic import BaseModel
from typing import Union


class TokenInfo(BaseModel):
    """
    Represents linguistic information for a single token.

    Attributes
    ----------
    text : str
        The original text of the token.
    lemma : str
        The lemma (base form) of the token.
    pos : Union[str, int]
        Part-of-speech tag for the token. This can be a string (e.g., "NOUN")
        or an integer (e.g., its corresponding numerical ID).
    dep : str
        Dependency relation of the token in the syntactic parse tree.
    ent_type : str
        Named entity type for the token (e.g., "PERSON", "ORG", or empty string if not applicable).
    is_stopword : bool
        Indicates whether the token is a stopword (common words that are often ignored, such as "and" or "the").
    """

    text: str
    lemma: str
    pos: Union[str, int]
    dep: str
    ent_type: str
    is_stopword: bool
