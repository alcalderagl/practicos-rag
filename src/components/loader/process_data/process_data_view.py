import streamlit as st
from src.commons.files_logic import upload_file
from src.loaders.loaders_logic import file_loader
from src.commons.logging_messages import LOGG_MESSAGES
from src.commons.enums.type_message import TypeMessage
from src.components.loader.process_data.cleanin_expander_view import cleaning_expander
from src.components.loader.process_data.chuncking_expander_view import chuncking_expander

st.title(LOGG_MESSAGES["APP_LABEL_LOADER_TITLE"])
# upload files st component
uploaded_files = st.file_uploader(
    LOGG_MESSAGES["APP_LABEL_CHOOSE_FILES"],
    type=["pdf"], #"csv", "xlsx", "xls", "docx", "txt"],
    accept_multiple_files=True,
)

for uploaded_file in uploaded_files:
    if uploaded_file is not None:
        # get file binary data
        bytes_data:bytes = uploaded_file.read()
        # get file name
        file_name:str = uploaded_file.name
        # directory path
        dir_path:str = "data/regulaciones"
        with st.spinner(LOGG_MESSAGES["APP_LABEL_PROCESSING_FILE"]):
            # store document
            uploadResp = upload_file(dir_path=dir_path, document=bytes_data, filename=file_name)
            if uploadResp.typeMessage == TypeMessage.INFO and uploadResp.response:
                # if document was sucessfully stored then
                # 1. loader process
                respLoader = file_loader(uploadResp.response, file_name)
                # show a message depending on type message response loader
                if respLoader.typeMessage == TypeMessage.INFO:
                    # 2. CLEANING EXPANDER
                    clean_docs = cleaning_expander(respLoader, file_name)
                    # 3. CHUNCKING EXPANDER
                    chuncking_expander(clean_docs, file_name)
                elif respLoader.typeMessage == TypeMessage.ERROR:
                    # otherwise show an error message
                    st.error(respLoader.message, icon="🚨")
                elif respLoader.typeMessage == TypeMessage.WARNING:
                    # or show a warning message
                    st.warning(respLoader.message, icon="⚠️")
            else:
                # otherwise show an error message
                st.warning(uploadResp.message, icon="⚠️")