import streamlit as st
import time
from src.loaders.loaders_logic import upload_document

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
        dir = "data/regulaciones"
        loaded_data = upload_document(dir=dir, document=bytes_data, filename=file_name)
        st.write("", loaded_data.message)
