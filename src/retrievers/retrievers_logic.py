import os
import logging
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.retrievers.self_query.base import SelfQueryRetriever
from src.vector_store_client.vector_store_client_logic import VectorStoreClient
from src.commons.logging_messages import LOGG_MESSAGES
from src.commons.models.response_logic import ResponseLogic
from src.commons.enums.type_message import TypeMessage
from src.llm.llm_logic import OllamaLlm

logging.basicConfig(level=logging.INFO)


class Retrievers:
    def __init__(self) -> None:
        self.model_embedding_name = os.getenv(
            "MODEL_EMBEDDING", "distiluse-base-multilingual-cased-v2"
        )
        self.llm = OllamaLlm()
        self.vector_store_client = VectorStoreClient()

    def self_query_retriever(self, query: str):
        try:
            metadata_fields = [
                AttributeInfo(name="author", description="", type="string"),
                AttributeInfo(name="creation_date", description="", type="date"),
                AttributeInfo(name="title", description="", type="string"),
                AttributeInfo(name="keywords", description="", type="list[string]"),
                AttributeInfo(name="topic", description="", type="list[string]"),
            ]

            document_content_description = "A collection of norms and laws for aliments"

            retriever = SelfQueryRetriever.from_llm(
                llm=self.llm,
                vectorstore=self.vector_store_client.vector_store,
                document_content_description=document_content_description,
                metadata_field_info=metadata_fields,
                verbose=True,
            )
            results = retriever.invoke(query)
            return results
        except (ValueError, KeyError) as e:
            return []

    def initial_query_qdrant(self, query_text: str, top_k: int = 3) -> ResponseLogic:
        """Query Qdrant with a query text and return top_k similar results."""
        resp: ResponseLogic
        try:
            query_embedding = self.vector_store_client.embedding_model.embed_query(
                query_text
            )

            results = self.vector_store_client.client.search(
                collection_name=self.vector_store_client.collection_name,
                query_vector=query_embedding,
                limit=top_k,
            )

            resp = ResponseLogic(
                response=results,
                message="hello",
                type_message=TypeMessage.INFO,
            )
            logging.info("query %", resp)
        except (ValueError, KeyError) as e:
            logging.info("Error when querying into qdrant %", e)
            resp = ResponseLogic(
                response="I don't have data",
                message="I don't have data",
                type_message=TypeMessage.ERROR,
            )

        return resp
