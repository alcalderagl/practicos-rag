import logging
from rerankers import Reranker

logging.basicConfig(level=logging.INFO)
class Reranking:
    def __init__(self) -> None:
        pass

    def reranker(self, query: str, retrieved_docs):
        try:
            _reranker = Reranker("colbert", verbose=0)
            retrieved_docs = [doc.page_content for doc in retrieved_docs]
            reranked_docs = _reranker.rank(query, retrieved_docs).results
            logging.info(f"reranker docs: {reranked_docs}")
            return reranked_docs
        except (ValueError, KeyError) as e:
            logging.info(f"Error with reranker: {e}")
            return []
