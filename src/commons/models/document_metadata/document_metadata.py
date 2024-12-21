from pydantic import BaseModel
from typing import Optional


class DocumentMetadata(BaseModel):
    """
    Represents metadata information for a document.

    Attributes
    ----------
    title : Optional[str]
        Title of the document. Default is an empty string.
    source : Optional[str]
        Source of the document (e.g., URL or publication). Default is an empty string.
    author : Optional[str]
        Author of the document. Default is an empty string.
    file_name : Optional[str]
        Name of the file associated with the document. Default is an empty string.
    creation_date : Optional[str]
        Creation date of the document in string format (e.g., "YYYY-MM-DD"). Default is an empty string.
    page : Optional[int]
        Number of pages in the document or the page number for a chunk. Default is `None`.
    """

    title: Optional[str] = ""
    source: Optional[str] = ""
    author: Optional[str] = ""
    file_name: Optional[str] = ""
    creation_date: Optional[str] = ""
    page: Optional[int]
