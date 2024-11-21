import streamlit as st
from typing import List

# from src.chunking.chunking_logic import chuck_doc
from src.commons.logging_messages import LOGG_MESSAGES


def chuncking_expander(docs: List[str], file_name):
    if len(docs) > 0:
        with st.expander(
            LOGG_MESSAGES["APP_LABEL_CHUNCKING_FILE"].format(filename=file_name)
        ):
            st.write("djksjkd")
