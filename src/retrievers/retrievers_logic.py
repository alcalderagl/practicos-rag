import os
import logging
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.retrievers.self_query.base import SelfQueryRetriever
from src.vector_store_client.vector_store_client_logic import VectorStoreClient
from src.commons.logging_messages import LOGG_MESSAGES
from src.commons.models.response_logic import ResponseLogic
from src.commons.enums.type_message import TypeMessage
from langchain.retrievers.self_query.qdrant import QdrantTranslator
from src.llm.llm_logic import LageLangueModel
from src.retrievers.custom_self_query_retriever import CustomSelfQueryRetriever
from src.reranking.reranking_logic import Reranking
from src.summarization.summarization_logic import Summarization
from langchain_qdrant import RetrievalMode, QdrantVectorStore
from src.benchmark.benchmark_logic import Benchmark
from src.benchmark.models.question_answer import QuestionAnswer

logging.basicConfig(level=logging.INFO)


class Retrievers:
    def __init__(self) -> None:
        self.model_embedding_name = os.getenv(
            "MODEL_EMBEDDING", "distiluse-base-multilingual-cased-v2"
        )
        
        
    def advance_query_retrieval(self, query:str)-> ResponseLogic:
        
        response_logic = ResponseLogic(
                response=["No cuento con la informacion"],
                message="No cuento con la informacion",
                type_message=TypeMessage.ERROR,
        )
        try:
            query_retrieval_docs = self._self_query_retrieval(query=query)
            if len(query_retrieval_docs) > 0:
                reranking = Reranking()
                ranked_docs = reranking.reranker(query, query_retrieval_docs)
                if len(ranked_docs) > 0:
                    # docs = []
                    # for doc in ranked_docs:
                    #     doc_txt = doc.document.text
                    #     docs.append({"page_content":doc_txt})
                    # response_logic.response = docs
                    summarization = Summarization()
                    summarized_answer =  summarization.summarize(query=query,ranked_results=query_retrieval_docs)
                    if summarized_answer != "":
                        benchmark = Benchmark()
                        response_logic.type_message=TypeMessage.INFO
                        response_logic.response = summarized_answer
                        qa = QuestionAnswer(question=query, answer=summarized_answer).model_dump()
                        benchmark.save_qa(data=[qa])
                    else:
                        response_logic.response = ""
                        response_logic.message="THERE ARE NOT A SUMMARIZATION ANSWER"
                else:
                    response_logic.message="THERE WAS A PROBLEM WITH RERANKIN"
            else:
                response_logic.message="DOCUMENTS NOT FOUND FROM SELF QUERY RETRIEVAL"

        except(ValueError, KeyError) as e:
            logging.info(f"Error with advance query retrieval: {e}")
            
        return response_logic
    
    def _hybrid_query_retrieval(self, query:str)-> ResponseLogic:
        vector_store_client = VectorStoreClient()
        qdrant = QdrantVectorStore.from_existing_collection(
        embedding=vector_store_client.embedding_model,
        location=":memory:",  # Or the URL of your Qdrant instance (e.g., "http://localhost:6333")
        collection_name=qdrant,
        retrieval_mode=RetrievalMode.HYBRID,
        )


    def _self_query_retrieval(self, query: str):
        """
        Retrieves relevant documents based on a self-query mechanism.

        Parameters
        ----------
        query : str
            The input query string to retrieve relevant documents.

        Returns
        ----------
        ResponseLogic: 
            An object containing the retrieved results, a status message, and a type message.
        """

        try:
            
            vector_store_client = VectorStoreClient()
            LLM_model = LageLangueModel()
            
            metadata_fields = [
                AttributeInfo(name="author", description="", type="string"),
                AttributeInfo(name="creation_date", description="", type="date"),
                AttributeInfo(name="title", description="", type="string"),
                AttributeInfo(name="keywords", description="", type="list[string]"),
                AttributeInfo(name="topic", description="", type="list[string]"),
            ]

            document_content_description = "A collection of regulations, laws, and standards governing the production, distribution, and quality of food and beverages in Mexico."
            structured_query_translator = QdrantTranslator(metadata_key="payload")
            
            vector_store = vector_store_client.create_vector_store()
            
            openai_llm = LLM_model.connect_chat_openAI()
            # ollama_llm = LLM_model.connect_to_ollama()
            retriever= CustomSelfQueryRetriever.from_llm(
                llm=openai_llm,
                vectorstore=vector_store,
                document_contents=document_content_description,
                metadata_field_info=metadata_fields,
                verbose=True,
                structured_query_translator=structured_query_translator
            )
            results = retriever.invoke(query)
            logging.info(f"∫elf query retrieval: {results}")
            return results
        except (ValueError, KeyError) as e:
            logging.info(f"Error with self query retrieval: {e}")
            return []

    def initial_query_retrieval(self, query_text: str, top_k: int = 3) -> ResponseLogic:
        """
        Retrieves the most relevant responses for a given query using vector-based search.

        Parameters
        ----------
        query_text : str
            The input query text to retrieve relevant responses for.
        top_k : int
            The number of top results to retrieve. Defaults to 3.

        Returns:
        ----------
        ResponseLogic: 
            An object containing the response, message, and type of message.
        """
        
        response_logic = ResponseLogic(
                response=["No cuento con la informacion"],
                message="No cuento con la informacion",
                type_message=TypeMessage.ERROR,
        )
        try:
            vector_store_client = VectorStoreClient()
            
            query_embedding = vector_store_client.embedding_model.embed_query(
                query_text
            )

            results = vector_store_client.client.search(
                collection_name=vector_store_client.collection_name,
                query_vector=query_embedding,
                limit=top_k,
            )

            response_logic.message="OK"
            response_logic.type_message=TypeMessage.INFO
            response_logic.response =results
            logging.info(f"initial query retrieval: {response_logic}")
        except (ValueError, KeyError) as e:
            logging.info(f"Error with initial query retrieval: {e}")
        return response_logic
    
    
