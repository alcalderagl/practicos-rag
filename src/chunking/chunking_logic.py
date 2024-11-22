import os
import json
from langchain.text_splitter import CharacterTextSplitter
from src.commons.models.response_logic import ResponseLogic
from src.commons.enums.type_message import TypeMessage
from src.commons.logging_messages import LOGG_MESSAGES

def chuncking_doc(page: str, file_name: str, page_number: int, output_file='data/chunks/chunks.json') -> ResponseLogic:
    """
    Function to chunk a document and save the chunks in a structured JSON format with unique page numbers.
    
    Parameters:
    - page (str): The text content of the page to chunk.
    - file_name (str): Name of the file being processed.
    - page_number (int): The page number being processed.
    - output_file (str): The path to the JSON file where chunks will be saved.
    
    Returns:
    - ResponseLogic: Object with the result of the operation.
    """
    resp: ResponseLogic
    try:
        # Configure the text splitter
        text_splitter = CharacterTextSplitter(
            chunk_size=35, chunk_overlap=5, separator=" ", strip_whitespace=True
        )
        
        # Chunk the page text
        chunks = text_splitter.split_text(page)
        
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Load existing data if the file already exists
        if os.path.exists(output_file):
            with open(output_file, "r", encoding="utf-8") as file:
                existing_data = json.load(file)
        else:
            existing_data = {"documents": []}
        
        # Check if the document already exists
        document = next((doc for doc in existing_data["documents"] if doc["file_name"] == file_name), None)
        if not document:
            # If the document does not exist, add a new one
            document = {"file_name": file_name, "paginas": []}
            existing_data["documents"].append(document)
        
        # Check if the page number already exists to avoid duplicates
        if any(p["pagina"] == page_number for p in document["paginas"]):
            raise ValueError(f"Page {page_number} already exists in the JSON for {file_name}.")
        
        # Add data for the current page
        page_data = {
            "pagina": page_number,
            "chuncks": chunks
        }
        document["paginas"].append(page_data)
        
        # Save the updated data back to the JSON file
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(existing_data, file, indent=4, ensure_ascii=False)
        
        resp = ResponseLogic(
            response=chunks,
            typeMessage=TypeMessage.INFO,
            message=f"Chunks for page {page_number} of '{file_name}' saved successfully in {output_file}."
        )
        return resp

    except (ValueError, KeyError, json.JSONDecodeError) as e:
        resp = ResponseLogic(
            response=None,
            typeMessage=TypeMessage.ERROR,
            message=LOGG_MESSAGES["CHUNCKING_ERROR"].format(error=e)
        )
        
    return resp    
