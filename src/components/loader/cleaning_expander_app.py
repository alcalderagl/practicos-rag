import streamlit as st
from src.commons.logging_messages import LOGG_MESSAGES
from src.chunking.process_document_logic import ProcessDocument
from src.commons.models.loaders.loader_response import LoaderResponse


def cleaning_expander(loader_response: LoaderResponse) -> list[str]:
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
    file_name = loader_response.response.file_name
    with st.expander(
        LOGG_MESSAGES["APP_LABEL_CLEANING_FILE"].format(file_name=file_name)
    ):
        process_document = ProcessDocument()
        # iterate document loaded
        for index, page in enumerate(loader_response.response.loader):
            # cleaned page
            st.subheader(LOGG_MESSAGES["APP_LABEL_PAGE"].format(no_page=str(index + 1)))
            # get the tokens
            tokens = process_document.clean_doc(page.page_content)
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
