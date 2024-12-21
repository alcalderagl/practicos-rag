import streamlit as st
from typing import List
from langchain_core.documents import Document
from src.commons.logging_messages import LOGG_MESSAGES
from src.chunking.process_document_logic import ProcessDocument
from src.commons.models.response_logic import ResponseLogic


def cleaning_expander(loader_response: ResponseLogic, file_name: str) -> list[str]:
    """
    Generates a expander component to load & clean documents

    Parameters
    ----------
    loader_response : LoaderResponse
        Loader PDF from langchain

    Returns
    -------
    List[str]
        The documents cleaned
    """
    # cleaning documents list
    cleaning_docs = list()
    st.write(loader_response)
    with st.expander(
        LOGG_MESSAGES["APP_LABEL_CLEANING_FILE"].format(file_name=file_name)
    ):
        process_document = ProcessDocument()
        documents: List[Document] = loader_response.response
        # iterate document loaded
        for index, document in enumerate(documents):
            # cleaned page
            st.subheader(LOGG_MESSAGES["APP_LABEL_PAGE"].format(no_page=str(index + 1)))
            # get the tokens
            tokens = process_document.clean_doc(document.page_content)
            text = ""
            for token in tokens:
                # join text
                if not token.is_stopword:
                    text += f"{token.text} "
            # print the cleaned document
            st.markdown(
                f"<p style='font-size: 16px;'>{text}</p>",
                unsafe_allow_html=True,
            )
            cleaning_docs.append(text)
        # return cleaned documents
        return cleaning_docs
