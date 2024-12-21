import os
import logging
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance
from langchain_community.vectorstores import Qdrant
from src.commons.enums.type_message import TypeMessage
from src.commons.logging_messages import LOGG_MESSAGES
from src.commons.models.response_logic import ResponseLogic
from langchain_openai import OpenAIEmbeddings

# from langchain_ollama import OllamaEmbeddings
# from langchain.embeddings import HuggingFaceEmbeddings
logging.basicConfig(level=logging.INFO)


class VectorStoreClient:
    def __init__(self):
        # getting or setting name collection
        self.collection_name = os.getenv("VECTOR_STORE_NAME", "regulaciones_mx")
        # getting or setting qdrant port
        self._port = os.getenv("QDRANT_PORT", "6333")
        # getting or setting model embedding
        self.model_name = os.getenv("MODEL_EMBEDDING", "text-embedding-ada-002")
        self.api_key = os.getenv("OPENAI_API_KEY", "XXXX")
        # getting or setting qdrant host
        self._host = os.getenv("QDRANT_HOST", "localhost")
        # getting or setting model embedding size
        self.vector_size = os.getenv("VECTOR_SIZE", "512")
        # setting vector params
        self._vectors_params = VectorParams(
            size=self.vector_size, distance=Distance.COSINE
        )

        # Initialize Qdrant client
        self.client = QdrantClient(host=self._host, port=self._port)

        # Initialize embedding model
        self.embedding_model = OpenAIEmbeddings(
            model=self.model_name, api_key=self.api_key
        )
        # ---- hugging embeddings
        # HuggingFaceEmbeddings(model_name=self.model_name)
        # ---- OLLAMA embeddings
        # self.embedding_model = OllamaEmbeddings(model="llama3")

    def create_collection(self) -> ResponseLogic:
        """
        Creates or verifies the existence of a collection in the Qdrant vector store.

        Returns
        -------
        ResponseLogic:
            A ResponseLogic object indicating the status of the operation, with
            additional context such as messages and type of response.
        """
        response_logic: ResponseLogic
        try:
            # get collection name from qdrant vector store
            existing_collections = [
                collection.name
                for collection in self.client.get_collections().collections
            ]
            logging.info(f"existent collectisons: {existing_collections}")

            if self.collection_name not in existing_collections:
                # Create collection when it doesn't exist
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=self._vectors_params,
                )
                # return response
                response_logic = ResponseLogic(
                    response=None,
                    type_message=TypeMessage.INFO,
                    message=LOGG_MESSAGES["VECTOR_STORE_COLLECTION_CREATED"].format(
                        collection_name=self.collection_name
                    ),
                )
            else:
                # collection exists
                response_logic = ResponseLogic(
                    response=None,
                    type_message=TypeMessage.WARNING,
                    message=LOGG_MESSAGES["VECTOR_STORE_COLLECTION_EXISTS"].format(
                        collection_name=self.collection_name
                    ),
                )
        except (ValueError, KeyError) as e:
            # error when creating a collection
            response_logic = ResponseLogic(
                response=None,
                type_message=TypeMessage.ERROR,
                message=LOGG_MESSAGES["VECTOR_STORE_COLLECTION_CREATION_FAILED"].format(
                    error=e
                ),
            )
        logging.info(f"creation of vector store: {response_logic}")
        return response_logic

    def create_vector_store(self):
        """
        Creates and initializes a vector store for storing and retrieving vector embeddings.

        Returns:
            Qdrant: An instance of the Qdrant vector store, configured with the provided
                    client, collection name, and embedding model.
        """
        vector_store = Qdrant(
            client=self.client,
            collection_name=self.collection_name,
            embeddings=self.embedding_model,
        )
        return vector_store

    def test_qdrant_connection(self) -> ResponseLogic:
        """
        Tests the connection to the Qdrant vector store.

        Returns
        -------
        ResponseLogic:
            A ResponseLogic object containing the status of the connection test, including:
            - Response data from the Qdrant client if successful.
            - Type of message (INFO or ERROR).
            - A descriptive message about the operation result.
        """
        response_logic: ResponseLogic
        try:
            # success connection to qdrant
            client_conn = self.client.info()
            response_logic = ResponseLogic(
                response=client_conn,
                type_message=TypeMessage.INFO,
                message=LOGG_MESSAGES["VECTOR_STORE_SUCCESS_QDRANT_CONN"],
            )
        except (ValueError, KeyError) as e:
            # error to connect to qdrant
            response_logic = ResponseLogic(
                response=None,
                type_message=TypeMessage.ERROR,
                message=LOGG_MESSAGES["VECTOR_STORE_FAILED_QDRANT_CONN"].format(
                    error=e
                ),
            )
        logging.info(f"test qdrant connection {response_logic}")
        return response_logic

    def delete_qdrant_collection(self) -> ResponseLogic:
        """
        delete a collection from qdrant store

        Returns
        -------
        ResponseLogic
            An instance of ResponseLogic containing details about the upload operation.
        """
        response_logic: ResponseLogic
        try:
            # delete qdrant collection
            self.client.delete_collection(collection_name=self.collection_name)
            response_logic = ResponseLogic(
                response=None,
                type_message=TypeMessage.INFO,
                message=LOGG_MESSAGES["VECTOR_STORE_COLLECTION_SUCCESS_DELETED"],
            )
        except (ValueError, KeyError) as e:
            # error when deleting qdrant collection
            response_logic = ResponseLogic(
                response=None,
                type_message=TypeMessage.ERROR,
                message=LOGG_MESSAGES["VECTOR_STORE_COLLECTION_FAILED_DELETED"].format(
                    error=e
                ),
            )
        logging.info(f"delete qdrant collection: {response_logic}")
        return response_logic
