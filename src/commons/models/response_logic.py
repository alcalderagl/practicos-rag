from pydantic import BaseModel
from src.commons.enums import type_message


class ResponseLogic(BaseModel):
    """
    Represents a structured response with a message and optional response data.

    Attributes
    ----------
    response : any
        The actual response data associated with the operation.
    type_message : type_message
        Enum or custom type representing the type of message (e.g., success, error).
    message : str
        Detailed message associated with the response.
    """

    response: any
    type_message: type_message
    message: str

    class Config:
        arbitrary_types_allowed = True
