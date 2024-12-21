from typing import Any, Dict, List
from langchain_core.documents import Document
from langchain.retrievers.self_query.base import SelfQueryRetriever


class CustomSelfQueryRetriever(SelfQueryRetriever):
    def _get_docs_with_query(
        self, query: str, search_kwargs: Dict[str, Any]
    ) -> List[Document]:
        """
        Retrieves documents based on a query, adding score information to each document.

        Parameters
        ----------
        query : str
            The search query used to retrieve documents.
        search_kwargs : Dict[str, Any]
            Additional arguments for the search operation, such as filtering or ranking criteria.

        Returns
        -------
        List[Document]
            A list of documents with associated scores stored in their metadata.
        """
        # Perform similarity search with scores
        docs, scores = zip(
            *self.vectorstore.similarity_search_with_score(query, **search_kwargs)
        )
        # Attach the score to each document's metadata
        for doc, score in zip(docs, scores):
            doc.metadata["score"] = score
        return docs
