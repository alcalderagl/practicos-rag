import os
from src.vector_store_client.vector_store_client_logic import VectorStoreManager


def vector_retriever():
    # get collection name
    vectorStore = VectorStoreManager()
