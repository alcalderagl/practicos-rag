#import streamlit as st
#from typing import List
#from src.chunking.chunking_logic import chuck_doc
#from src.commons.logging_messages import LOGG_MESSAGES
import json
from langchain.text_splitter import CharacterTextSplitter
import os

'''
def chuncking_expander(docs: List[str], file_name):
    if len(docs) > 0:
        with st.expander(
            LOGG_MESSAGES["APP_LABEL_CHUNCKING_FILE"].format(filename=file_name)
        ):
            st.write("djksjkd")
'''



def chuncking_expander(document: str, output_file='data/chunks/chunks.json'):
    """
    Function to chunk a document and save the chunks as a JSON file.
    
    Parameters:
    - document (str): The text document to chunk.
    - output_file (str): The path to the JSON file where chunks will be saved.
    
    Returns:
    - List of chunks (str).
    """
    try:
        # Configure the text splitter
        text_splitter = CharacterTextSplitter(
            chunk_size=35, chunk_overlap=0, separator=" ", strip_whitespace=True
        )
        
        # Chunk the document
        chunks = text_splitter.split_text(document)

        # Prepare the data for JSON
        chunks_data = [{"chunk_id": i + 1, "content": chunk} for i, chunk in enumerate(chunks)]

        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # Save chunks to a JSON file
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(chunks_data, file, indent=4, ensure_ascii=False)
        
        print(f"Chunks saved successfully to {output_file}.")
        return chunks

    except Exception as e:
        print(f"Error while chunking the document: {e}")
        return []


'''
# Example usage
if __name__ == "__main__":
    example_document = """
    This is a sample text to test chunking functionality. It will be split into chunks of size 35.
    The goal is to ensure that chunks are saved correctly in a JSON file. Each chunk is identified by an ID.
    """
    
    chunks = chuncking_expander(example_document)
    print("Generated Chunks:")
    for i, chunk in enumerate(chunks, 1):
        print(f"Chunk {i}: {chunk}")
'''

#python src/components/loader/process_data/chuncking_expander_view.py 
