from pydantic import BaseModel
from src.commons.models.document_metadata.document_metadata import DocumentMetadata


class Chunking(BaseModel):
    """
    Represents a chunked text document with metadata.

    Attributes
    ----------
    metadata : DocumentMetadata
        Metadata information about the document, such as title, author, or other properties.
    chunks : list[str]
        List of text chunks extracted from the document.
    """

    metadata: DocumentMetadata
    chunks: list[str]
