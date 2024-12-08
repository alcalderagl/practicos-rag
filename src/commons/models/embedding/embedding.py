from pydantic import BaseModel
from src.commons.models.chunking.chunking import ChunkingMetada

class Embedding(BaseModel):
    metadata: ChunkingMetada
    page_content: str
    vector_embedding: list[float]