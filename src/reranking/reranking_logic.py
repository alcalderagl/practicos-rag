from rerankers import Reranker


class Reranking:
    def __init__(self) -> None:
        pass

    def reranker(self, query: str, retrieved_docs):
        _reranker = Reranker("colbert", verbose=0)
        retrieved_docs = [doc.page_content for doc in retrieved_docs]
        reranked_docs = _reranker.rank(query, retrieved_docs)
        return reranked_docs
