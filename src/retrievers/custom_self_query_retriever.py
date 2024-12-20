from typing import Any, Dict
from typing import List
from langchain_core.documents import Document
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.base import AttributeInfo


class CustomSelfQueryRetriever(SelfQueryRetriever):
    def _get_docs_with_query(
        self, query: str, search_kwargs: Dict[str, Any]
    ) -> List[Document]:
        """Get docs, adding score information."""
        docs, scores = zip(
            *self.vectorstore.similarity_search_with_score(query, **search_kwargs)
        )
        for doc, score in zip(docs, scores):
            doc.metadata["score"] = score

        return docs