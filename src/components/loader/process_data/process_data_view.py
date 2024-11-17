import streamlit as st
from src.loaders.loaders_logic import upload_document
from src.chunking.cleaning_doc_logic import clean_doc
from src.chunking.chunking_logic import chuck_doc
from src.commons.logging_messages import LOGG_MESSAGES
from src.commons.enums.type_message import TypeMessage

st.title("Load data")
uploaded_files = st.file_uploader(
    "Choose a file",
    type=["pdf", "csv", "xlsx", "xls", "docx", "txt"],
    accept_multiple_files=True,
)
for uploaded_file in uploaded_files:
    if uploaded_file is not None:
        bytes_data = uploaded_file.read()
        file_name = uploaded_file.name
        dir_path = "data/regulaciones"

        with st.spinner("Wait for it..."):
            loaded_data = upload_document(
                dir_path=dir_path, document=bytes_data, filename=file_name
            )
            resp_msg = loaded_data.message
            resp_loader = loaded_data.response
        st.success(resp_msg)

        if loaded_data.typeMessage == TypeMessage.INFO:
            # CLEANING EXPANDER
            with st.expander(
                LOGG_MESSAGES["APP_LABEL_CLEANING_FILE"].format(filename=file_name)
            ):

                cleaning_docs = list()
                for index, page in enumerate(resp_loader["response"]):
                    with st.container(height=500):
                        col1, col2 = st.columns(
                            2, vertical_alignment="top", gap="medium"
                        )
                        with col1:
                            if index == 0:
                                st.header("load document")
                            st.markdown(
                                f"<h2>Page {str(index + 1)}</h2>",
                                unsafe_allow_html=True,
                            )
                            st.write(page["pageContent"])
                        with col2:
                            if index == 0:
                                st.header("clean document")
                            document = clean_doc(page["pageContent"])
                            cleaning_docs.append(document)
                            st.markdown(
                                f"<h2>Page {str(index + 1)}</h2>",
                                unsafe_allow_html=True,
                            )
                            st.write(document)

            # CHUNCKING EXPANDER
            chunck_expander = st.expander(
                LOGG_MESSAGES["APP_LABEL_CHUNCKING_FILE"].format(filename=file_name)
            )
            chunck_expander.write("djksjkd")
