#import streamlit as st

#from src.chunking.chunking_logic import chuck_doc
#from src.commons.logging_messages import LOGG_MESSAGES
#from langchain.text_splitter import CharacterTextSplitter
# import json
#import os
import streamlit as st
from typing import List
from src.chunking.chunking_logic import chuncking_doc
from src.commons.models.response_logic import ResponseLogic
from src.commons.enums.type_message import TypeMessage

'''
def chuncking_expander(docs: List[str], file_name):
    if len(docs) > 0:
        with st.expander(
            LOGG_MESSAGES["APP_LABEL_CHUNCKING_FILE"].format(filename=file_name)
        ):
            st.write("djksjkd")
'''



def chuncking_expander(pagesCleaned: str, file_name:str):
    """
    Function to chunk a document and save the chunks as a JSON file.
    
    Parameters:
    - document (str): The text document to chunk.
    - output_file (str): The path to the JSON file where chunks will be saved.
    
    Returns:
    - List of chunks (str).
    """
    with st.expander("chuncking"):
        st.write("Chuncking doc ...")
         
        for i, page in enumerate(pagesCleaned):
            st.write(f"Pagina {i}" )
            chuncks: ResponseLogic = chuncking_doc(page, file_name)
            if chuncks.typeMessage == TypeMessage.INFO:
                for i, chunck in enumerate(chuncks.response):
                    st.write(chunck)
            
        
