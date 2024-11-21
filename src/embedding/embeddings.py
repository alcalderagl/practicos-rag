from langchain.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore, RetrievalMode
from dotenv import load_dotenv
import os
import pickle

# Cargar las variables de entorno si es necesario 
load_dotenv()

# Definir la ubicación del archivo PDF 
file_path = "archivo.pdf"

# Cargar y dividir el documento en fragmentos
loader = PyPDFLoader(file_path)
docs = loader.load_and_split()

# Elegir el modelo de embeddings 
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-MiniLM-L6-v2")

# Generar los embeddings y almacenar en un VectorStore de Qdrant
qdrant = QdrantVectorStore.from_documents(
    docs,
    embedding=embedding_model,
    location=":memory:",  # Usando almacenamiento en memoria, puedes configurar una ruta si prefieres persistencia.
    collection_name="regulaciones_alimentarias",
    retrieval_mode=RetrievalMode.DENSE
)

# Guardar los embeddings en un archivo .pkl dentro de la carpeta "embeddings"
os.makedirs("embeddings", exist_ok=True)  # Crear la carpeta "embeddings" si no existe
embeddings_file_path = "embeddings/embeddings.pkl"

# Guardar el vector store de Qdrant (que contiene los embeddings) en un archivo
with open(embeddings_file_path, "wb") as f:
    pickle.dump(qdrant.vector_store, f)

print(f"Embeddings guardados en {embeddings_file_path}")

# Realizar una consulta sobre los documentos indexados
query = "¿Cuáles son las regulaciones sobre etiquetado de alimentos en Mexico?"
found_docs = qdrant.similarity_search(query)

# Mostrar los documentos encontrados
for doc in found_docs:
    print(doc)