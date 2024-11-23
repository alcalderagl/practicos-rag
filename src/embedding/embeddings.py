import os
import pickle
from src.vector_store_client.vector_store_client_logic import VectorStoreManager
from src.commons.models.response_logic import ResponseLogic
from src.commons.enums.type_message import TypeMessage

# Inicializar el VectorStoreManager
vectorStoreManager = VectorStoreManager()


def set_embeddings(chuncks) -> ResponseLogic:
    """Generar embeddings a partir de los fragmentos."""
    try:
        texts = [chunck for chunck in chuncks]
        chunck_embeddings = vectorStoreManager.embedding_model.embed(texts)
        return ResponseLogic(
            message="Generated embeddings",
            response=chunck_embeddings,
            typeMessage=TypeMessage.INFO,
        )
    except (ValueError, KeyError) as e:
        return ResponseLogic(
            message=f"Error to generate embeddings: {str(e)}",
            typeMessage=TypeMessage.ERROR,
            response=None,
        )


def store_qdrant_embeddings(embeddings, chuncks):
    """Almacenar embeddings en Qdrant."""
    try:
        texts = [chunck for chunck in chuncks]
        vectorStoreManager.vector_store.add_texts(texts=texts, embeddings=embeddings)
        print("Embeddings almacenados correctamente en Qdrant.")
    except (ValueError, KeyError) as e:
        print(f"Error al almacenar embeddings en Qdrant: {e}")


def save_embeddings(embeddings, file_name):
    """Guardar los embeddings en un archivo local."""
    os.makedirs(
        "embeddings", exist_ok=True
    )  # Crear la carpeta "embeddings" si no existe
    embeddings_file_path = f"embeddings/{file_name}_embeddings.pkl"

    try:
        with open(embeddings_file_path, "wb") as f:
            pickle.dump(embeddings, f)
        print(f"Embeddings guardados en {embeddings_file_path}.")
    except Exception as e:
        print(f"Error al guardar los embeddings: {e}")


def query_qdrant(collection_name, query):
    """Realizar una consulta sobre los documentos indexados en Qdrant."""
    try:
        query_embedding = vectorStoreManager.embedding_model.embed([query])[0]
        results = vectorStoreManager.vector_store.client.search(
            collection_name=collection_name, query_vector=query_embedding, limit=5
        )
        print("Resultados de la consulta:")
        for result in results:
            print(result.payload["text"])
    except Exception as e:
        print(f"Error al realizar la consulta: {e}")


# Flujo completo de generación, almacenamiento y consulta
def main(chuncks, file_name, collection_name, query):
    """Flujo principal para generar, almacenar y consultar embeddings."""
    # Generar embeddings
    response = set_embeddings(chuncks)
    if response.typeMessage == TypeMessage.ERROR:
        print(response.message)
        return

    # Almacenar embeddings en Qdrant
    embeddings = response.response
    store_qdrant_embeddings(embeddings, chuncks)

    # Guardar embeddings localmente
    save_embeddings(embeddings, file_name)

    # Realizar una consulta
    query_qdrant(collection_name, query)


# Ejemplo de uso
if __name__ == "__main__":
    # Ejemplo de fragmentos de texto
    example_chuncks = [
        "Fragmento 1 del documento.",
        "Fragmento 2 del documento.",
        "Fragmento 3 del documento.",
    ]

    # Nombre del archivo para guardar embeddings
    file_name = "documento_ejemplo"

    # Nombre de la colección en Qdrant
    collection_name = "regulaciones_alimentarias"

    # Consulta de ejemplo
    query = "¿Cuáles son las regulaciones sobre etiquetado de alimentos?"

    # Ejecutar el flujo principal
    main(example_chuncks, file_name, collection_name, query)
