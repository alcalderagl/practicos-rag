from uuid import uuid4
import json
from src.vector_store_client.vector_store_client_logic import VectorStoreManager
#from src.commons.files_logic import createFolder, generate_file_path
from src.commons.models.response_logic import ResponseLogic
from src.commons.enums.type_message import TypeMessage


class EmbeddingManager:
    def __init__(self):
        # Inicializar the VectorStoreManager
        self.vectorStoreManager = VectorStoreManager()

    def set_embedding(self, text: str)->list[float]:
        """Generate embeddings from texts and return them."""
        embeddings = self.vectorStoreManager.embedding_model.embed_documents([text])
        return embeddings[0]

    def store_embeddings_in_qdrant(
        self, texts: list[str], embeddings: list, metadata: list = None
    ):
        """Store the embeddings and corresponding texts into Qdrant."""
        points = []
        for i, (text, embedding) in enumerate(zip(texts, embeddings)):
            doc_metadata = metadata[i] if metadata else {}
            point = {
                "id": str(uuid4()),
                "vector": embedding,
                "metadata": {
                    "text": text,
                    "doc": doc_metadata.get("doc", ""),  # Optional document metadata
                    "author": doc_metadata.get("author", ""),
                    "date": doc_metadata.get("date", ""),
                },
            }
            points.append(point)

        # Upload embeddings to Qdrant
        self.vectorStoreManager.client.upsert(
            collection_name=self.vectorStoreManager.collection_name, points=points
        )
        print(f"Stored {len(points)} embeddings in Qdrant.")

        #self.save_embeddings_to_file(points, "mx_embedding_regulations.json")

    # def save_embeddings_to_file(self, points: list, file_name: str):
    #     """Save embeddings to a local file (json)"""
    #     path_dir = "data/embeddings"
    #     createFolder(path_dir)  # Create embeddings folder if it doesn't exist
    #     embeddings_file_path = generate_file_path(path_dir, file_name)
    #     try:
    #         with open(embeddings_file_path, "w", encoding="utf-8") as f:
    #             json.dump(points, f, indent=4)
    #         print(f"Embeddings saved to {embeddings_file_path}.")
    #     except (ValueError, KeyError, json.JSONDecodeError) as e:
    #         print(f"Error saving embeddings: {e}")

    def query_qdrant(self, query_text: str, top_k: int = 5) -> ResponseLogic:
        """Query Qdrant with a query text and return top_k similar results."""
        resp: ResponseLogic
        try:
            query_embedding = self.vectorStoreManager.embedding_model.embed_query(
                query_text
            )

            results = self.vectorStoreManager.client.search(
                collection_name=self.vectorStoreManager.collection_name,
                query_vector=query_embedding,
                limit=top_k,
            )
            resp = ResponseLogic(
                response=results,
                message=" i have the data",
                type_message=TypeMessage.INFO,
            )
        except (ValueError, KeyError) as e:
            resp = ResponseLogic(
                response="I don't have data",
                message="I don't have data",
                type_message=TypeMessage.ERROR,
            )

        return resp
