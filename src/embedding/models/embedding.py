from pydantic import BaseModel
from src.chunking.models.chunk_metadata import ChunkMetadata
from typing import Optional


class Embedding(BaseModel):
    """
    Represents the embedding of a chunk of text.

    Attributes
    ----------
    payload : ChunkMetadata
        Metadata associated with the chunk, including details like position and page number.
    id : str
        Embedding ID.
    vector : list[float]
        Numerical embedding vector representing the chunk in a high-dimensional space.
    """

    payload: ChunkMetadata
    id: str
    vector: Optional[list[float]]
