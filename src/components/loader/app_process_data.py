import streamlit as st
from src.commons.files_logic import FileManager
from src.loaders.loaders_logic import LoaderManager
from src.commons.logging_messages import LOGG_MESSAGES
from src.commons.enums.type_message import TypeMessage
from src.components.loader.app_cleaning_expander import cleaning_expander
from src.components.loader.app_chunking_expander import chunking_expander

# APP TITLE
st.title(LOGG_MESSAGES["APP_LABEL_LOADER_TITLE"])
# upload files st component
uploaded_files = st.file_uploader(
    LOGG_MESSAGES["APP_LABEL_CHOOSE_FILES"],
    type=["pdf"],  # "csv", "xlsx", "xls", "docx", "txt"],
    accept_multiple_files=True,
)

file_manager = FileManager()

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
                loader_manager = LoaderManager(
                    dir_path=upload_response.response, file_name=file_name
                )
                # loader response from loader_manager file loader
                loader_response = loader_manager.file_loader()
                # show a message depending on type message response loader
                if loader_response.type_message == TypeMessage.INFO:
                    metadata = loader_response.response.loader[0].metadata
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.text_input(
                            label="Title", value=metadata.author, disabled=True
                        )
                    with col2:
                        st.text_input(
                            label="Author", value=metadata.author, disabled=True
                        )
                    with col3:
                        st.text_input(
                            label="creation_date",
                            value=metadata.creation_date,
                            disabled=True,
                        )
                    # embeddingManager = EmbeddingManager()
                    # 2. CLEANING EXPANDER
                    cleaned_documents = cleaning_expander(loader_response)
                    # 3. CHUNKING EXPANDER
                    chunking_expander(
                        cleaned_documents=cleaned_documents,
                        loader_response=loader_response,
                    )
                elif loader_response.type_message == TypeMessage.ERROR:
                    # otherwise show an error message
                    st.error(loader_response.message, icon="🚨")
                elif loader_response.type_message == TypeMessage.WARNING:
                    # or show a warning message
                    st.warning(loader_response.message, icon="⚠️")
            else:
                # otherwise show an error message
                st.warning(upload_response.message, icon="⚠️")
