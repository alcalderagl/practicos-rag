import os
import json
from uuid import uuid4
from langchain.text_splitter import CharacterTextSplitter
from src.commons.models.response_logic import ResponseLogic
from src.commons.enums.type_message import TypeMessage
from src.commons.logging_messages import LOGG_MESSAGES
from src.commons.files_logic import FileManager
from src.commons.models.chunking.chunking import Chunking
from src.commons.models.document_metadata.document_metadata import DocumentMetadata
from src.chunking.process_document_logic import ProcessDocument
from src.commons.models.chunking.chunk_metadata import ChunkMetadata


class ChunkingManager:
    def __init__(self) -> None:
        self.process_document = ProcessDocument()

    def chunking_doc(self, page: str, metadata: DocumentMetadata) -> ResponseLogic:
        """
        Function to chunk a document

        Parameters
        ----------
        page : str
            The text content of the page to chunk
        metadata : DocumentMetadata
            Document metadata

        Returns
        -------
        ResponseLogic
            Object with the result of the operation.
        """
        response_logic: ResponseLogic
        try:
            # Configure the text splitter
            text_splitter = CharacterTextSplitter(
                chunk_size=500, chunk_overlap=50, separator=" ", strip_whitespace=True
            )
            # Chunk the page text
            chunks = text_splitter.split_text(page)
            chunks = Chunking(metadata=metadata, chunks=chunks)

            response_logic = ResponseLogic(
                response=chunks,
                type_message=TypeMessage.INFO,
                message=LOGG_MESSAGES["OK"],
            )
            return response_logic
        except (ValueError, KeyError, json.JSONDecodeError) as e:
            response_logic = ResponseLogic(
                response=None,
                type_message=TypeMessage.ERROR,
                message=LOGG_MESSAGES["CHUNKING_ERROR"].format(error=e),
            )
        return response_logic

    def save_chunks_file(self, chunking: any, file_name: str) -> ResponseLogic:
        """
        Function to save chunks into a file json

        Parameters
        ----------
        chunking : list[Chunking]
            list of chunks with metadata
        file_name : str
            file name of document

        Returns
        -------
        ResponseLogic
            Object with the result of the operation.
        """
        message: str
        data = {"data": chunking}
        try:
            file_manager = FileManager()
            # get file name without extension
            file_name = file_manager.get_file_name(file=file_name)
            # directory path
            dir_path: str = os.getenv("CHUNKING_FOLDER", "data/chunks")
            # save document
            file_manager.save_json_file(
                dir_path=dir_path, file_name=f"{file_name}.json", data=data
            )
            message = ""
        except (ValueError, KeyError, json.JSONDecodeError) as e:
            message = LOGG_MESSAGES["CHUNKING_SAVE_JSON"].format(error=e)
        return ResponseLogic(
            response=None,
            type_message=TypeMessage.ERROR,
            message=message,
        )

    def chunk_metadata(
        self, chunk: str, no_serie: int, metadata: DocumentMetadata, file_name: str
    ) -> ChunkMetadata:
        """
        Function to generate chunk metadata

        Parameters
        ----------
        chunk : str
            chunk document
        no_serie : int
            number chunk
        metadata : DocumentMetadata
            Document metadata
        file_name : str
            File name of document

        Returns
        -------
        ChunkMetadata
            a chunk metadata
        """
        # set uuid chunk
        uuid = str(uuid4())
        chunk_position = no_serie
        chunk_title = self.process_document.get_summary_title(chunk=chunk)
        chunk_keywords = self.process_document.getKeywords(document=chunk)
        metadata_chunk = ChunkMetadata(
            uuid=uuid,
            document_title=metadata.title,
            keywords=chunk_keywords,
            source=metadata.source,
            author=metadata.author,
            file_name=file_name,
            chunk_position=chunk_position,
            chunk_title=chunk_title,
            page=metadata.page,
            creation_date=metadata.creation_date,
            chunk=chunk,
        )
        return metadata_chunk
