from typing import List, Optional
from pydantic import BaseModel
from src.commons.enums.type_message import TypeMessage


class LoaderModel(BaseModel):
    pageContent: str
    source: str
    page: int

class FileModel(BaseModel):
    fileExt: str
    response: List[LoaderModel]

class LoaderResponse(BaseModel):
    """
    Response model to streamlit app
    """

    response: FileModel
    typeMessage: TypeMessage
    message: str

    # class Config:
    #     arbitrary_types_allowed = True
        

    
    