from typing import List, Optional
from pydantic import BaseModel
from src.commons.enums.type_message import TypeMessage


class Metadata(BaseModel):
    author: str
    title: str
    creation_date: str
    page: int
    source: str


class LoaderModel(BaseModel):
    page_content: str
    metadata: Metadata

    class Config:
        arbitrary_types_allowed = True


class FileModel(BaseModel):
    file_ext: str
    file_name: str
    loader: List[LoaderModel]


class LoaderResponse(BaseModel):
    """
    Response model to streamlit app
    """

    response: FileModel
    type_message: TypeMessage
    message: str
