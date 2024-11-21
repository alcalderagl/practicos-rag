import os
import json
from langchain.text_splitter import CharacterTextSplitter
from src.commons.models.response_logic import ResponseLogic
from src.commons.enums.type_message import TypeMessage
from src.commons.logging_messages import LOGG_MESSAGES
from src.commons.files_logic import existsFile

def chuncking_doc(page:str, file_name: str, output_file='data/chunks/chunks.json') -> ResponseLogic:
    """
    Function to chunk a document and save the chunks as a JSON file.
    
    Parameters:
    - document (str): The text document to chunk.
    - output_file (str): The path to the JSON file where chunks will be saved.
    
    Returns:
    - List of chunks (str).
    """
    resp: ResponseLogic
    try:
        # Configure the text splitter
        text_splitter = CharacterTextSplitter(
            chunk_size=35, chunk_overlap=5, separator=" ", strip_whitespace=True
        )
        
        # Chunk the document
        chunks = text_splitter.split_text(page)
        #Document(metadata={}, page_content='This is the text I would like to ch'),

        # Prepare the data for JSON
        # chunks_data = [{"chunk_id": i + 1, "content": chunk, "document": path} for i, chunk in enumerate(chunks)]

        # Ensure the output directory exists
        
        # os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # # Save chunks to a JSON file
        # with open(output_file, "w", encoding="utf-8") as file:
        #     json.dump(chunks_data, file, indent=4, ensure_ascii=False)
        
        # print(f"Chunks saved successfully to {output_file}.")
        resp = ResponseLogic(response=chunks, typeMessage=TypeMessage.INFO, message=f"Chunks saved successfully to {output_file}.")
        return resp

    except (ValueError, KeyError) as e:
        resp = ResponseLogic(response=None, typeMessage=TypeMessage.ERROR, message=LOGG_MESSAGES["CHUNCKING_ERROR"].format(error=e))
        
    return resp