from typing import List, Optional
from pydantic import BaseModel
from src.commons.models.document_metadata.document_metadata import DocumentMetadata


class Loader(BaseModel):
    """
    Represents a loader for processing document content and metadata.

    Attributes
    ----------
    page_content : str
        The textual content of the document.
    metadata : DocumentMetadata
        Metadata associated with the document, such as title, author, etc.
    """

    page_content: str
    metadata: DocumentMetadata
