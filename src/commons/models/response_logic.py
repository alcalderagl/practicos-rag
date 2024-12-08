from pydantic import BaseModel
from src.commons.enums import type_message


class ResponseLogic(BaseModel):
    """
    Response
    """

    response: any
    """
    Type of message
    """
    type_message: type_message
    """
    Message
    """
    message: str

    class Config:
        arbitrary_types_allowed = True
