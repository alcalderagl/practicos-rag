import os
import logging
from typing import List
from langchain.chains.query_constructor.base import AttributeInfo
from src.vector_store_client.vector_store_client_logic import VectorStoreClient
from langchain.retrievers.self_query.qdrant import QdrantTranslator
from langchain_core.documents import Document
from src.commons.logging_messages import LOGG_MESSAGES
from src.commons.models.response_logic import ResponseLogic
from src.commons.enums.type_message import TypeMessage
from src.llm.llm_logic import LageLangueModel
from src.retrievers.custom_self_query_retriever import CustomSelfQueryRetriever
from src.reranking.reranking_logic import Reranking
from src.summarization.summarization_logic import Summarization
from src.benchmark.benchmark_logic import Benchmark
from src.benchmark.models.question_answer import QuestionAnswer



logging.basicConfig(level=logging.INFO)


class Retrievers:
    def __init__(self) -> None:
        pass

    def advance_query_retrieval(self, query: str) -> ResponseLogic:
        """
        Performs an advanced query retrieval process, summarizes the results, and saves the information if successful.

        Parameters
        ----------
        query : str
            The user query for which to retrieve and summarize relevant documents.

        Returns
        -------
        ResponseLogic
            A ResponseLogic object containing the summarized answer or error message.
        """
        response_logic = ResponseLogic(
            response="",
            message=LOGG_MESSAGES["RETRIEVAL_DONT_HAVE_CONTEXT"],
            type_message=TypeMessage.ERROR,
        )
        try:
            # Perform self-query retrieval using the provided query
            query_retrieval_docs = self._self_query_retrieval(query=query)
            # Check if documents are retrieved
            if len(query_retrieval_docs) > 0:
                # instance of summarization
                summarization = Summarization()
                # Perform summarization on the retrieved documents
                summarized_answer = summarization.summarize(
                    query=query, retrieval_docs=query_retrieval_docs
                )

                # Check if summarization is successful
                if summarized_answer != "":
                    benchmark = Benchmark()
                    response_logic.type_message = TypeMessage.INFO
                    response_logic.response = summarized_answer
                    # Save the summarized answer along with the query in the benchmark
                    qa = QuestionAnswer(
                        question=query, answer=summarized_answer
                    ).model_dump()
                    benchmark.save_qa(data=[qa])
                else:
                    response_logic.message = LOGG_MESSAGES[
                        "RETRIEVAL_FAILED_TO_SUMMARIZED"
                    ]
                    response_logic.type_message = TypeMessage.INFO
                    response_logic.response = query_retrieval_docs
            else:
                response_logic.message = LOGG_MESSAGES["SELF_QUERY_RETRIEVAL_FAILED"]

        except (ValueError, KeyError) as e:
            # Log any errors encountered during the process
            logging.info(f"Error with advance query retrieval: {e}")
        return response_logic

    def _self_query_retrieval(self, query: str) -> List[Document]:
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
            # Initialize vector store client
            vector_store_client = VectorStoreClient()
            # Initialize larguange model
            LLM_model = LageLangueModel()

            # Define metadata fields for documents
            metadata_fields = [
                AttributeInfo(name="author", description="", type="string"),
                AttributeInfo(name="creation_date", description="", type="date"),
                AttributeInfo(name="title", description="", type="string"),
                AttributeInfo(name="keywords", description="", type="list[string]"),
                AttributeInfo(name="topic", description="", type="list[string]"),
            ]

            # Description of the document content
            document_content_description = "A collection of regulations, laws, and standards governing the production, distribution, and quality of food and beverages in Mexico"

            # Initialize structured query translator
            # TO DO
            structured_query_translator = QdrantTranslator(metadata_key="payload")
            # Create vector store
            vector_store = vector_store_client.create_vector_store()

            # CONNECT to LLM
            openai_llm = LLM_model.connect_chat_openAI()
            # ollama_llm = LLM_model.connect_to_ollama()

            # Create a custom self-query retriever
            retriever = CustomSelfQueryRetriever.from_llm(
                llm=openai_llm,
                vectorstore=vector_store,
                document_contents=document_content_description,
                metadata_field_info=metadata_fields,
                verbose=True,
                structured_query_translator=structured_query_translator,
            )

            # Perform self-query retrieval
            results = retriever.invoke(query)
            logging.info(f"self query retrieval: {results}")
            return results
        except (ValueError, KeyError) as e:
            # if there are any error then show this data
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
            response=[],
            message=LOGG_MESSAGES["RETRIEVAL_DONT_HAVE_CONTEXT"],
            type_message=TypeMessage.ERROR,
        )
        try:
            # connection to vector store
            vector_store_client = VectorStoreClient()
            # query embedded by the embedding model define in qdrant
            query_embedding = vector_store_client.embedding_model.embed_query(
                query_text
            )
            # results of vector search
            results = vector_store_client.client.search(
                collection_name=vector_store_client.collection_name,
                query_vector=query_embedding,
                limit=top_k,
            )
            # modify response logic to a success response logic
            response_logic.message = LOGG_MESSAGES["OK"]
            response_logic.type_message = TypeMessage.INFO
            response_logic.response = results
            logging.info(f"initial query retrieval: {response_logic}")
        except (ValueError, KeyError) as e:
            # if there are any error then show this data
            logging.info(f"Error with initial query retrieval: {e}")
        return response_logic    
