import os
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Qdrant
from src.commons.enums.type_message import TypeMessage
from src.commons.logging_messages import LOGG_MESSAGES
from src.commons.models.response_logic import ResponseLogic


class VectorStoreManager:
    def __init__(self):
        self.collection_name = os.getenv("VECTOR_STORE_NAME", "regulaciones_mx")
        self._port = os.getenv("QDRANT_PORT", "6333")
        self.model_name = os.getenv(
            "MODEL_EMBEDDING", "sentence-transformers/all-MiniLM-L6-v2"
        )
        self._host = os.getenv("QDRANT_HOST", "localhost")
        self.vector_size = os.getenv("VECTOR_SIZE", "384")

        self._vectors_params = VectorParams(
            size=self.vector_size, distance=Distance.COSINE
        )

        # Initialize Qdrant client
        self._client = QdrantClient(host=self._host, port=self._port)

        # Initialize embedding model
        self.embedding_model = HuggingFaceEmbeddings(model_name=self.model_name)

        self.create_collection()

        self.vector_store = Qdrant(
            client=self._client,
            collection_name=self.collection_name,
            embeddings=self.embedding_model,
        )

    def create_collection(self) -> ResponseLogic:
        """
        Get qdrant collections

        Returns
        -------
        ResponseLogic:
            Returns response logic
        """
        resp: ResponseLogic
        try:
            if self.validate_collection():
                resp = ResponseLogic(
                    response=None,
                    typeMessage=TypeMessage.WARNING,
                    message=LOGG_MESSAGES["VECTOR_STORE_COLLECTION_EXISTS"].format(
                        collection_name=self.collection_name
                    ),
                )
            else:
                self._client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=self._vectors_params,
                )
                resp = ResponseLogic(
                    response=None,
                    typeMessage=TypeMessage.INFO,
                    message=LOGG_MESSAGES["VECTOR_STORE_COLLECTION_CREATED"].format(
                        collection_name=self.collection_name
                    ),
                )
        except (ValueError, KeyError) as e:
            resp = ResponseLogic(
                response=None,
                typeMessage=TypeMessage.ERROR,
                message=LOGG_MESSAGES["VECTOR_STORE_COLLECTION_CREATION_FAILED"].format(
                    error=e
                ),
            )
        return resp

    def test_qdrant_connection(self):
        """
        Get qdrant collections

        Returns
        -------
        ResponseLogic:
            Returns response logic
        """
        resp: ResponseLogic
        try:
            client_conn = self._client.info()
            resp = ResponseLogic(
                response=client_conn,
                typeMessage=TypeMessage.INFO,
                message=LOGG_MESSAGES["VECTOR_STORE_SUCCESS_QDRANT_CONN"],
            )
        except (ValueError, KeyError) as e:
            resp = ResponseLogic(
                response=None,
                typeMessage=TypeMessage.ERROR,
                message=LOGG_MESSAGES["VECTOR_STORE_FAILED_QDRANT_CONN"].format(
                    error=e
                ),
            )
        return resp

    def get_qdrant_collections(self):
        """
        Get qdrant collections

        Returns
        -------
        array:
            Returns qdrant collections
        """
        qdrant_collections = self._client.get_collections().collections
        return qdrant_collections

    def validate_collection(self) -> bool:
        """
        Validates if collection exists in qdrant store

        Returns
        -------
        bool
            Returns `True` if the collection exists, otherwise `False`.
        """
        if any (
            self.collection_name == collection for collection in self.get_qdrant_collections()
        ):
            return True
        else:
            return False

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
            self._client.delete_collection(collection_name=self.collection_name)
            resp = ResponseLogic(
                response=None,
                typeMessage=TypeMessage.INFO,
                message=LOGG_MESSAGES["VECTOR_STORE_COLLECTION_SUCCESS_DELETED"],
            )
        except (ValueError, KeyError) as e:
            resp = ResponseLogic(
                response=None,
                typeMessage=TypeMessage.ERROR,
                message=LOGG_MESSAGES["VECTOR_STORE_COLLECTION_FAILED_DELETED"].format(
                    error=e
                ),
            )
        return resp
