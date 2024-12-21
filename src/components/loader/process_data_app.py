import streamlit as st
from typing import List
from langchain_core.documents import Document
from src.commons.files_logic import FileManager
from src.loaders.loaders_logic import Loading
from src.embedding.embeddings_logic import EmbeddingManager
from src.commons.logging_messages import LOGG_MESSAGES
from src.commons.enums.type_message import TypeMessage
from src.components.loader.cleaning_expander_app import cleaning_expander
from src.components.loader.chunking_expander_app import chunking_expander
from src.commons.models.embedding.embedding import Embedding


# APP TITLE
st.title(LOGG_MESSAGES["APP_LABEL_LOADER_TITLE"])
# upload files st component
uploaded_files = st.file_uploader(
    LOGG_MESSAGES["APP_LABEL_CHOOSE_FILES"],
    type=["pdf"],  # "csv", "xlsx", "xls", "docx", "txt"],
    accept_multiple_files=True,
)

file_manager = FileManager()
embedding_manager = EmbeddingManager()

# For every document into uploader file
for uploaded_file in uploaded_files:
    # if file is not None then
    if uploaded_file is not None:
        # get file binary data
        bytes_data: bytes = uploaded_file.read()
        # get file name
        file_name: str = uploaded_file.name

        with st.spinner(LOGG_MESSAGES["APP_LABEL_PROCESSING_FILE"]):
            # store document into a folder
            upload_response = file_manager.upload_file(
                document=bytes_data, file_name=file_name
            )

            # if document was sucessfully stored then
            if (
                upload_response.type_message == TypeMessage.INFO
                and upload_response.response
            ):

                # 1. LOADER DOCUMENT
                loader_manager = Loading(
                    dir_path=upload_response.response, file_name=file_name
                )
                # loader response from loader_manager file loader
                loader_response = loader_manager.file_loader()
                # show a message depending on type message response loader
                if loader_response.type_message == TypeMessage.INFO:
                    document: List[Document] = loader_response.response
                    metadata = document[0].metadata
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.text_input(
                            label="Title",
                            value=metadata.get("author", ""),
                            disabled=True,
                        )
                    with col2:
                        st.text_input(
                            label="Author",
                            value=metadata.get("author", ""),
                            disabled=True,
                        )
                    with col3:
                        st.text_input(
                            label="creation_date",
                            value=metadata.get("creation_date"),
                            disabled=True,
                        )

                    # 2. CLEANING EXPANDER
                    cleaned_documents = cleaning_expander(
                        loader_response=loader_response, file_name=file_name
                    )
                    # 3. CHUNKING EXPANDER
                    chunks_metadata = chunking_expander(
                        cleaned_documents=cleaned_documents,
                        loader_response=loader_response,
                        file_name=file_name,
                    )
                    # 4. VECTOR_EMBEDDING
                    embeddings = embedding_manager.set_embedding(
                        chunks_metadata=chunks_metadata
                    )
                    # embedding_manager.store_embeddings_in_qdrant(embeddings=embeddings)
                    # embedding_manager.save_embeddings_to_file(
                    #     embeddings=embeddings, file_name=file_name
                    # )
                elif loader_response.type_message == TypeMessage.ERROR:
                    # otherwise show an error message
                    st.error(loader_response.message, icon="🚨")
                elif loader_response.type_message == TypeMessage.WARNING:
                    # or show a warning message
                    st.warning(loader_response.message, icon="⚠️")
            else:
                # otherwise show an error message
                st.warning(upload_response.message, icon="⚠️")
