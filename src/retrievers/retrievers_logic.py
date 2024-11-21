import os
from src.vector_store_client.vector_store_client_logic import VectorStoreManager
from src.commons.logging_messages import LOGG_MESSAGES
from src.commons.models.response_logic import ResponseLogic
from src.commons.enums.type_message import TypeMessage


def vector_retriever(
    question: str, search_type: str = "mmr", k_search: int = 10
) -> ResponseLogic:
    resp: ResponseLogic
    try:
        vectorStoreManager = VectorStoreManager()
        retriever = vectorStoreManager.vector_store.as_retriever(
            search_type=search_type, search_kwargs={"k": k_search}
        )

        docs = retriever.invoke(question)
        resp = ResponseLogic(
            response=docs,
            typeMessage=TypeMessage.ERROR,
            message=LOGG_MESSAGES["RETRIEVER_SUCCESS"],
        )
    except (ValueError, KeyError) as e:
        resp = ResponseLogic(
            response=None,
            typeMessage=TypeMessage.ERROR,
            message=LOGG_MESSAGES["RETRIEVER_FAILED"].format(error=e),
        )
    return resp
