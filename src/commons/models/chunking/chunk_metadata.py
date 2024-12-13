from pydantic import BaseModel
from typing import Optional
from src.commons.models.document_metadata.document_metadata import DocumentMetadata


class ChunkMetadata(DocumentMetadata):
    """
    Metadata for a text chunk.

    Attributes
    ----------
    uuid : Optional[str]
        Unique identifier for the chunk. Default is an empty string.
    keywords : Optional[list[str]]
        List of keywords associated with the chunk. Default is an empty list.
    chunk_position : Optional[int]
        The position of the chunk within the document.
    chunk_title : Optional[str]
        Title of the chunk. Default is an empty string.
    page : Optional[int]
        The page number where the chunk is located.
    """

    uuid: Optional[str] = ""
    keywords: Optional[list[str]] = []
    chunk_position: Optional[int]
    chunk_title: Optional[str] = ""
    page: Optional[int]
    chunk: str
