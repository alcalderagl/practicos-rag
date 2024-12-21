import logging
from typing import List
from rerankers import Reranker
from rerankers.results import Result

logging.basicConfig(level=logging.INFO)


class Reranking:
    def __init__(self) -> None:
        pass

    def reranker(self, query: str, retrieved_docs) -> List[Result]:
        """
        Re-ranks a list of retrieved documents based on their relevance to the query.

        Parameters
        ----------
        query : str
            The query string used to determine the relevance of the documents.
        retrieved_docs : list
            A list of retrieved documents, where each document contains a `page_content` attribute.

        Returns
        -------
        list[Result]
            A list of reranked documents based on their relevance to the query.
            Returns an empty list if an error occurs.
        """
        try:
            # Initialize a reranking model using the ColBERT architecture
            _reranker = Reranker("colbert", verbose=0)
            # Extract the content of each retrieved document
            retrieved_docs = [doc.page_content for doc in retrieved_docs]
            # Rank the documents based on their relevance to the query
            reranked_docs = _reranker.rank(query, retrieved_docs).results
            logging.info(f"reranker docs: {reranked_docs}")
            return reranked_docs
        except (ValueError, KeyError) as e:
            logging.info(f"Error with reranker: {e}")
            return []
