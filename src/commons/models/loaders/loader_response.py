from typing import List, Optional
from pydantic import BaseModel
from src.commons.enums.type_message import TypeMessage
from src.commons.models.loaders.file import File


class LoaderResponse(BaseModel):
    """
    Represents a response from a document loader containing processed file data and message information.

    Attributes
    ----------
    response : File
        The processed document file, typically containing the result of loading and processing.
    type_message : TypeMessage
        An enumeration or custom type representing the type of message (e.g., success, error).
    message : str
        A detailed message associated with the loader response, providing additional information.
    """

    response: File
    type_message: TypeMessage
    message: str
