from typing import List, Optional
from pydantic import BaseModel
from src.commons.models.loaders.loader import Loader


class File(BaseModel):
    """
    Represents a file with its associated extensions, name, and loader information.

    Attributes
    ----------
    file_ext : str
        The file extension (e.g., ".txt", ".pdf").
    file_name : str
        The name of the file (e.g., "document_1").
    loader : List[Loader]
        A list of `Loader` objects representing the processing of different content chunks of the file.
    """

    file_ext: str
    file_name: str
    loader: List[Loader]
