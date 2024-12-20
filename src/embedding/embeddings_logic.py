import os
import json
import logging
from uuid import uuid4
from src.vector_store_client.vector_store_client_logic import VectorStoreClient
from src.commons.files_logic import FileManager
from src.commons.models.response_logic import ResponseLogic
from src.commons.enums.type_message import TypeMessage
from src.commons.models.chunking.chunk_metadata import ChunkMetadata
from src.commons.models.embedding.embedding import Embedding

logging.basicConfig(level=logging.INFO)


class EmbeddingManager:
    def __init__(self) -> None:
        pass

    def set_embedding(self, chunks_metadata: list[ChunkMetadata]) -> list[Embedding]:
        """Generate embeddings from texts and return them."""
        try:
            # Inicializar the vector store client
            vector_store_client = VectorStoreClient()
            embeddings: list[Embedding] = []
            for chunk in chunks_metadata:
                vector_embedding = (
                    vector_store_client.embedding_model.embed_documents(
                        texts=[chunk.page_content]
                    )
                )
                uuid = str(uuid4())
                embedding = Embedding(
                    id=uuid, vector=vector_embedding[0], payload=chunk
                )
                embeddings.append(embedding)
            return embeddings
        except (ValueError, KeyError) as e:
            logging.info("setting embedding error %", e)
            return []

    def store_embeddings_in_qdrant(self, embeddings: list[Embedding]) -> None:
        """Store the embeddings and corresponding texts into Qdrant."""
        # Upload embeddings to Qdrant
        try:
            vector_store_client = VectorStoreClient()
            embeddings = [embedding.model_dump() for embedding in embeddings]
            logging.info(embeddings)
            vector_store_client.client.upsert(
                collection_name=vector_store_client.collection_name,
                points=embeddings,
            )
        except (ValueError, KeyError) as e:
            logging.info("Error when storing embeddings into qdrant %", e)
            
    def save_embeddings_to_file(
        self, embeddings: list[Embedding], file_name: str
    ) -> None:
        """Save embeddings to a local file (json)"""
        data = {"data": [embedding.model_dump() for embedding in embeddings]}
        try:
            file_manager = FileManager()
            # get file name without extension
            file_name = file_manager.get_file_name(file=file_name)
            # directory path
            dir_path: str = os.getenv("EMBEDDINGS_FOLDER", "data/embeddings")
            # save document
            file_manager.save_json_file(
                dir_path=dir_path, file_name=f"{file_name}.json", data=data
            )
        except (ValueError, KeyError, json.JSONDecodeError) as e:
            logging.info(f"error saving the embedidng {e}")
