from pydantic import BaseModel


class ChunkingMetada(BaseModel):
    uuid: str
    document_title: str
    keywords: list[str]
    source: str
    author: str
    file_name: str
    chunk_position: int
    chunk_title: str
    page: int
    creation_date: str



