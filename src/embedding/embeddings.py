#from langchain.embeddings.huggingface import HuggingFaceEmbeddings
#from langchain.document_loaders import PyPDFLoader
#from langchain.vectorstores import Qdrant
#from qdrant_client.models import Distance, VectorParams
#from qdrant_client import QdrantClient
import os
import pickle
from src.vector_store_client.vector_store_client_logic import VectorStoreManager
from src.commons.models.response_logic import ResponseLogic
from src.commons.enums.type_message import TypeMessage

vectorStoreManager = VectorStoreManager()

def set_embeddings(chuncks) -> ResponseLogic:
    
    resp:ResponseLogic
    try:
        texts = [chunck for chunck in chuncks]
        chunck_embeddings = vectorStoreManager.embedding_model.embed(texts)
        resp = ResponseLogic(message="Generated embeddings", response=chunck_embeddings, typeMessage=TypeMessage.INFO)
    except (ValueError, KeyError) as e:
        resp = ResponseLogic(message="Error to generate embeddings", typeMessage=TypeMessage.ERROR, response=None)
    return resp

def store_qdrant_embeddings(embeddings, chuncks, ):
    try:
        texts = [chunck for chunck in chuncks]
        vectorStoreManager.vector_store.add_texts(texts=texts, embeddings=embeddings)
    except (ValueError, KeyError) as e:
        print(e)

def save_embeddings(embeddings, page):
    # Guardar los embeddings en un archivo .pkl dentro de la carpeta "embeddings"
    os.makedirs(
        "embeddings", exist_ok=True
    )  # Crear la carpeta "embeddings" si no existe
    embeddings_file_path = "embeddings/embeddings.pkl"

    try:
        with open(embeddings_file_path, "wb") as f:
            pickle.dump(embeddings, f)
        print(f"Embeddings guardados en {embeddings_file_path}.")
    except Exception as e:
        print(f"Error al guardar los embeddings: {e}")
        exit()

    # Realizar una consulta sobre los documentos indexados
    query = "¿Cuáles son las regulaciones sobre etiquetado de alimentos?"
    try:
        query_embedding = embedding_model.embed([query])[0]
        results = client.search(
            collection_name=collection_name, query_vector=query_embedding, limit=5
        )
        print("Resultados de la consulta:")
        for result in results:
            print(result.payload["text"])
    except Exception as e:
        print(f"Error al realizar la consulta: {e}")
