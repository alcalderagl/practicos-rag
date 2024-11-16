from pydantic import BaseModel
from src.commons.enums import type_message


class ResponseLogic(BaseModel):
    """
    Response model to streamlit app
    """

    response: any
    typeMessage: type_message
    message: str

    class Config:
        arbitrary_types_allowed = True
