import streamlit as st
from typing import List
from src.chunking.chunking_logic import chuncking_doc
from src.commons.models.response_logic import ResponseLogic
from src.commons.enums.type_message import TypeMessage

def chuncking_expander(pagesCleaned: List[str], file_name: str, output_file: str = "data/chunks/chunks.json"):
    """
    Function to chunk a document and save the chunks as a JSON file.
    
    Parameters:
    - pagesCleaned (List[str]): The cleaned pages of the document to chunk.
    - file_name (str): The name of the file being processed.
    - output_file (str): The path to the JSON file where chunks will be saved.
    
    Returns:
    - Displays chunks in Streamlit and saves them to a JSON file.
    """
    with st.expander("Chunking Document"):
        st.write(f"Processing document: {file_name}")

        # Iterate over the cleaned pages and their indices
        for i, page in enumerate(pagesCleaned, start=1):  # `start=1` for human-readable page numbers
            st.write(f"Processing Page {i}...")

            # Call the `chuncking_doc` function with the correct page number
            chuncks: ResponseLogic = chuncking_doc(page, file_name, page_number=i, output_file=output_file)

            if chuncks.typeMessage == TypeMessage.INFO:
                st.write(f"Chunks for Page {i}:")
                # Display each chunk
                for j, chunck in enumerate(chuncks.response, start=1):
                    st.write(f"Chunk {j}: {chunck}")
            else:
                st.error(f"Error processing page {i}: {chuncks.message}")
        
        st.success(f"The document '{file_name}' has been successfully saved to {output_file}.")    
