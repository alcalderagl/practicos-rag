import streamlit as st
from src.chunking.chunking_logic import ChunkingManager
from src.commons.models.response_logic import ResponseLogic
from src.commons.enums.type_message import TypeMessage
from src.commons.logging_messages import LOGG_MESSAGES
from src.commons.models.loaders.loader_response import LoaderResponse
from src.commons.models.chunking.chunk_metadata import ChunkMetadata

from src.chunking.chunking_logic import Chunking
from src.commons.models.embedding.embedding import Embedding


def chunking_expander(
    cleaned_documents: list[str], loader_response: LoaderResponse
) -> list[ChunkMetadata]:
    """
    Generates an expander component to display chunking information.

    Parameters
    ----------
    cleaned_documents : List[str]
        The cleaned pages of the document to chunk.
    file_name : str
        The name of the file being processed.
    output_file : str
        The path to the JSON file where chunks will be saved.

    Returns
    -------
    list[ChunkMetadata]
        return a list chunking with its metadata.
    """

    chunking_manager = ChunkingManager()

    file_name = loader_response.response.file_name
    with st.expander(
        LOGG_MESSAGES["APP_LABEL_CHUNKING_FILE"].format(file_name=file_name)
    ):

        chunks_response: list[Chunking] = []
        chunks_metadata: list[ChunkMetadata] = []
        # Iterate over the cleaned pages and their indices
        for i, page in enumerate(cleaned_documents, start=1):
            metadata = loader_response.response.loader[i - 1].metadata
            # Call the `chunking_doc` function with the correct page number
            chunks: ResponseLogic = chunking_manager.chunking_doc(
                page, metadata=metadata
            )

            if chunks.type_message == TypeMessage.INFO:
                # instance of chunking class
                chunk_response: Chunking = chunks.response
                # append chunk response
                chunks_response.append(chunk_response.model_dump())
                st.header(
                    LOGG_MESSAGES["APP_LABEL_CHUNK_PROCESS"].format(no_page=str(i))
                )
                # Display each chunk
                for j, chunk in enumerate(chunk_response.chunks, start=1):
                    # chunk metadata
                    chunk_metadata = chunking_manager.chunk_metadata(
                        page_content=chunk,
                        no_serie=j,
                        metadata=chunk_response.metadata,
                        file_name=file_name,
                    )
                    chunks_metadata.append(chunk_metadata)
                    # chunk position
                    st.subheader(f"Chunk_ID: chunk_{j}")
                    # chunk keywords
                    st.pills(
                        LOGG_MESSAGES["APP_LABEL_CHUNK_KEYWORDS"],
                        chunk_metadata.keywords,
                        selection_mode="single",
                        disabled=True,
                    )
                    # chunk page_content
                    st.write(chunk)
                    st.divider()
            else:
                st.error(chunks.message, icon="🚨")
        # save the chunking in a json file
        # chunking_response = chunking_manager.save_chunks_file(
        #     chunking=chunks_response, file_name=file_name
        # )
        # # validates its operation
        # if chunking_response.type_message == TypeMessage.INFO:
        #     st.success(chunking_response.message, icon="✅")
        # else:
        #     st.warning(chunking_response.message, icon="⚠️")
        # return the chunks
        return chunks_metadata
