import os
from src.vector_store_client.vector_store_client_logic import VectorStoreManager


def vector_retriever(question: str, search_type: str = "mmr", k_search: int = 10):
    vectorStoreManager = VectorStoreManager()
    retriever = vectorStoreManager.vector_store.as_retriever(
        search_type=search_type, search_kwargs={"k": k_search}
    )
    return retriever.invoke(question)
