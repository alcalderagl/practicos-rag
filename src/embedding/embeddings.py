from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Qdrant
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
import os
import pickle
from src.vector_store_client.vector_store_client_logic import VectorStoreManager

def embeddings_logic(chuncks, file_name: str):
    
    vectorStoreManager = VectorStoreManager()

    print("Qdrant Client instalado correctamente.")

    # Conectar con Qdrant (debe estar en ejecución)
    try:
        client = QdrantClient(host="localhost", port=6333)  # Cambiar host/puerto si es necesario
        print("Conectado a Qdrant correctamente.")
    except Exception as e:
        print(f"Error al conectar con Qdrant: {e}")
        exit()

    # Crear una colección en Qdrant si no existe
    collection_name = "regulaciones_alimentarias"
    try:
        collections = client.get_collections().collections
        if not any(col.name == collection_name for col in collections):
            client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE)
            )
            print(f"Colección '{collection_name}' creada.")
        else:
            print(f"Colección '{collection_name}' ya existe.")
    except Exception as e:
        print(f"Error al verificar/crear colección: {e}")
        exit()

    # Cargar el archivo PDF y procesar el texto
    file_path = "/Users/ignaciomoreda/Desktop/Applied Project/2-REP23_FICSs.pdf"  # Reemplazar con la ruta a tu archivo PDF
    if not os.path.exists(file_path):
        print(f"El archivo {file_path} no existe.")
        exit()

    # try:
    #     loader = PyPDFLoader(file_path)
    #     docs = loader.load_and_split()
    #     print(f"Documento cargado y dividido en {len(docs)} fragmentos.")
    # except Exception as e:
    #     print(f"Error al cargar o dividir el archivo PDF: {e}")
    #     exit()

    # Elegir el modelo de embeddings
    # try:
    #     embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-MiniLM-L6-v2")
    #     print("Modelo de embeddings cargado correctamente.")
    # except Exception as e:
    #     print(f"Error al cargar el modelo de embeddings: {e}")
    #     exit()

   
    # Generar los embeddings para los fragmentos
    try:
        texts = [doc.page_content for doc in chuncks]
        embeddings = vectorStoreManager.embedding_model.embed(texts)
        print(f"Embeddings generados para {len(texts)} fragmentos.")
    except Exception as e:
        print(f"Error al generar embeddings: {e}")
        exit()

    # Cargar los embeddings en Qdrant
    try:
        qdrant = Qdrant(client=client, collection_name=collection_name)
        #vectorStoreManager.vector_store.add_texts()
        qdrant.add_texts(texts=texts, embeddings=embeddings)
        print("Embeddings cargados en Qdrant correctamente.")
    except Exception as e:
        print(f"Error al cargar embeddings en Qdrant: {e}")
        exit()

    # Guardar los embeddings en un archivo .pkl dentro de la carpeta "embeddings"
    os.makedirs("embeddings", exist_ok=True)  # Crear la carpeta "embeddings" si no existe
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
            collection_name=collection_name,
            query_vector=query_embedding,
            limit=5
        )
        print("Resultados de la consulta:")
        for result in results:
            print(result.payload["text"])
    except Exception as e:
        print(f"Error al realizar la consulta: {e}")
