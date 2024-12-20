import os
import logging
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Qdrant
from src.commons.enums.type_message import TypeMessage
from src.commons.logging_messages import LOGG_MESSAGES
from src.commons.models.response_logic import ResponseLogic

logging.basicConfig(level=logging.INFO)


class VectorStoreClient:
    def __init__(self):
        # getting or setting name collection
        self.collection_name = os.getenv("VECTOR_STORE_NAME", "regulaciones_mx")
        # getting or setting qdrant port
        self._port = os.getenv("QDRANT_PORT", "6333")
        # getting or setting model embedding
        self.model_name = os.getenv(
            "MODEL_EMBEDDING", "distiluse-base-multilingual-cased-v2"
        )
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
        self.embedding_model = HuggingFaceEmbeddings(model_name=self.model_name)

    def create_collection(self) -> ResponseLogic:
        """
        Creates or verifies the existence of a collection in the Qdrant vector store.

        Returns
        -------
        ResponseLogic:
            A ResponseLogic object indicating the status of the operation, with
            additional context such as messages and type of response.
        """
        resp: ResponseLogic
        try:
            # get collection name from qdrant vector store
            existing_collections = [
                collection.name
                for collection in self.client.get_collections().collections
            ]
            print("Colecciones existentes:", existing_collections)

            if self.collection_name not in existing_collections:
                # Create collection when it doesn't exist
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=self._vectors_params,
                )
                resp = ResponseLogic(
                    response=None,
                    type_message=TypeMessage.INFO,
                    message=LOGG_MESSAGES["VECTOR_STORE_COLLECTION_CREATED"].format(
                        collection_name=self.collection_name
                    ),
                )
            else:
                # collection exists
                resp = ResponseLogic(
                    response=None,
                    type_message=TypeMessage.WARNING,
                    message=LOGG_MESSAGES["VECTOR_STORE_COLLECTION_EXISTS"].format(
                        collection_name=self.collection_name
                    ),
                )
        except (ValueError, KeyError) as e:
            resp = ResponseLogic(
                response=None,
                type_message=TypeMessage.ERROR,
                message=LOGG_MESSAGES["VECTOR_STORE_COLLECTION_CREATION_FAILED"].format(
                    error=e
                ),
            )
        # print into console
        logging.info(resp)
        return resp

    def create_vector_store(self):
        """
        Creates and initializes a vector store for storing and retrieving vector embeddings.

        Returns:
            Qdrant: An instance of the Qdrant vector store, configured with the provided
                    client, collection name, and embedding model.
        """
        self.vector_store = Qdrant(
            client=self.client,
            collection_name=self.collection_name,
            embeddings=self.embedding_model,
        )

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
        resp: ResponseLogic
        try:
            client_conn = self.client.info()
            resp = ResponseLogic(
                response=client_conn,
                type_message=TypeMessage.INFO,
                message=LOGG_MESSAGES["VECTOR_STORE_SUCCESS_QDRANT_CONN"],
            )
        except (ValueError, KeyError) as e:
            resp = ResponseLogic(
                response=None,
                type_message=TypeMessage.ERROR,
                message=LOGG_MESSAGES["VECTOR_STORE_FAILED_QDRANT_CONN"].format(
                    error=e
                ),
            )
        logging.info(resp)
        return resp

    def delete_qdrant_collection(self) -> ResponseLogic:
        """
        delete a collection from qdrant store

        Returns
        -------
        ResponseLogic
            An instance of ResponseLogic containing details about the upload operation.
        """
        resp: ResponseLogic
        try:
            self.client.delete_collection(collection_name=self.collection_name)
            resp = ResponseLogic(
                response=None,
                type_message=TypeMessage.INFO,
                message=LOGG_MESSAGES["VECTOR_STORE_COLLECTION_SUCCESS_DELETED"],
            )
        except (ValueError, KeyError) as e:
            resp = ResponseLogic(
                response=None,
                type_message=TypeMessage.ERROR,
                message=LOGG_MESSAGES["VECTOR_STORE_COLLECTION_FAILED_DELETED"].format(
                    error=e
                ),
            )
        logging.info(resp)
        return resp
