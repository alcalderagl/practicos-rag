import streamlit as st
from src.commons.logging_messages import LOGG_MESSAGES
from src.chunking.cleaning_doc_logic import clean_doc
from src.commons.models.loaders.loader_response import LoaderResponse


def cleaning_expander(resp_loader: LoaderResponse, file_name: str):
    """
    generates a expander component to load & clean documents

    Parameters
    ----------
    file_path : str
        Location of document folder

    Returns
    -------
    List[str]
        The documents cleaned
    """
    # cleaning documents list
    cleaning_docs = list()
    with st.expander(
        LOGG_MESSAGES["APP_LABEL_CLEANING_FILE"].format(filename=file_name)
    ):
        st.write("")
        # iterate document loaded
        for index, page in enumerate(resp_loader.response.response):
            # expander pages load & clean
            st.title(LOGG_MESSAGES["APP_LABEL_PAGE"].format(no_page=str(index + 1)))
            with st.container():
                col1, col2 = st.columns(2, vertical_alignment="top", gap="medium")
                with col1:
                    # this column present load document #n_page
                    if index == 0:
                        # title
                        st.header(LOGG_MESSAGES["APP_LABEL_DOCUMENT_LOADED"])
                    # show page content of document loaded
                    st.write(page.pageContent)
                    with col2:
                        # this column present clean document #n_page
                        if index == 0:
                            # title
                            st.header(LOGG_MESSAGES["APP_LABEL_DOCUMENT_CLEANED"])
                        # clean process
                        document = clean_doc(page.pageContent)
                        # store into list the document cleaned
                        cleaning_docs.append(document)
                        # show document page cleaned
                        st.write(document)
        return cleaning_docs
