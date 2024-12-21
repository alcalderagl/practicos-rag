import os
import json
import logging
from uuid import uuid4
from src.vector_store_client.vector_store_client_logic import VectorStoreClient
from src.embedding.models.embedding import Embedding
from src.commons.files_logic import FileManager
from src.chunking.models.chunk_metadata import ChunkMetadata


logging.basicConfig(level=logging.INFO)


class EmbeddingManager:
    def __init__(self) -> None:
        pass

    def set_embedding(self, chunks_metadata: list[ChunkMetadata]) -> list[Embedding]:
        """
        Generate embeddings from text chunks and return them as a list of Embedding objects.

        Parameters
        ----------
        chunks_metadata : list[ChunkMetadata]
            A list of ChunkMetadata objects containing text content to be embedded.

        Returns
        -------
        list[Embedding]
            A list of Embedding objects generated from the provided text chunks.
        """
        try:
            # Inicializar the vector store client
            vector_store_client = VectorStoreClient()
            embeddings: list[Embedding] = []
            for chunk in chunks_metadata:
                vector_embedding = vector_store_client.embedding_model.embed_documents(
                    texts=[chunk.page_content]
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
        """
        Store the serialized embeddings and corresponding texts into Qdrant.
        
        Parameters
        ----------
        embeddings : list[Embedding]
            A list of embedding objects that need to be stored.

        Returns
        -------
        None
        """
        # Upload embeddings to Qdrant
        try:
            # Instance of VectorStoreClient
            vector_store_client = VectorStoreClient()
            # Serialize each embedding object into a dictionary using model_dump()
            embeddings = [embedding.model_dump() for embedding in embeddings]
            # Upsert (insert or update) the embeddings into the Qdrant collection
            vector_store_client.client.upsert(
                collection_name=vector_store_client.collection_name,
                points=embeddings,
            )
            logging.info(f"embeddings saved into qdrant: {embeddings[:3]}")
        except (ValueError, KeyError) as e:
            logging.info(f"Error when saving embeddings into qdrant {e}")

    def save_embeddings_to_file(
        self, embeddings: list[Embedding], file_name: str
    ) -> None:
        """
        Save embeddings to a local JSON file.

        Parameters
        ----------
        embeddings : list[Embedding]
            A list of embedding objects to be saved.
        file_name : str
            The desired name of the JSON file where embeddings will be saved.

        Returns
        -------
        None
        """
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
            logging.info(f"error saving the embedidng: {e}")
