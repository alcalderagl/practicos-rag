import streamlit as st
from uuid import uuid4
from src.chunking.chunking_logic import ChunkingManager
from src.commons.models.response_logic import ResponseLogic
from src.commons.enums.type_message import TypeMessage
from src.commons.logging_messages import LOGG_MESSAGES
from src.chunking.process_document_logic import ProcessDocument
from src.commons.models.loaders.loader_response import LoaderResponse
from src.commons.models.embedding.embedding import Embedding
from src.commons.models.chunking.chunking import ChunkingMetada
from src.embedding.embeddings_logic import EmbeddingManager

def chunking_expander(
    cleaned_documents: list[str], loader_response: LoaderResponse
) -> None:
    """
    Generates a expander component to show chunking information

    Parameters:
    - cleaned_documents (List[str]): The cleaned pages of the document to chunk.
    - file_name (str): The name of the file being processed.
    - output_file (str): The path to the JSON file where chunks will be saved.

    Returns:
    - Displays chunks in Streamlit and saves them to a JSON file.
    """
    process_document = ProcessDocument()
    chunking_manager = ChunkingManager()
    embedding_manager = EmbeddingManager()
    
    file_name = loader_response.response.file_name
    with st.expander(
        LOGG_MESSAGES["APP_LABEL_CHUNKING_FILE"].format(file_name=file_name)
    ):
        metadata = loader_response.response.loader[0].metadata
        embeddings = []
        # Iterate over the cleaned pages and their indices
        for i, page in enumerate(cleaned_documents, start=1):
            # Call the `chunking_doc` function with the correct page number
            chunks: ResponseLogic = chunking_manager.chunking_doc(page)

            if chunks.type_message == TypeMessage.INFO:
                st.header(
                    LOGG_MESSAGES["APP_LABEL_CHUNK_PROCESS"].format(no_page=str(i))
                )
                # Display each chunk
                for j, chunk in enumerate(chunks.response, start=1):
                    # set uuid chunk
                    uuid = str(uuid4())
                    # chunk position
                    st.subheader(f"Chunk_ID: chunk_{j}")
                    # chunk title
                    title = process_document.get_summary_title(chunk)
                    st.write(f"Title: {title}")
                    # chunk keywords
                    keywords = process_document.getKeywords(chunk)
                    st.pills(
                        LOGG_MESSAGES["APP_LABEL_CHUNK_KEYWORDS"],
                        keywords,
                        selection_mode="single",
                        disabled=True,
                    )
                    # chunk page_content
                    st.write(chunk)
                    st.divider()
                    # chunk metadata
                    metadata_chunk = ChunkingMetada(
                        uuid=uuid,
                        document_title=metadata.title,
                        keywords=keywords,
                        source=metadata.source,
                        author=metadata.author,
                        file_name=loader_response.response.file_name,
                        chunk_position=j,
                        chunk_title=title,
                        page=i,
                        creation_date=metadata.creation_date
                    )
                    # vector embedding 
                    vector_embedding = embedding_manager.set_embedding(text=chunk)
                    # instance of embedding
                    embedding = Embedding(metadata=metadata_chunk, page_content=chunk, vector_embedding=vector_embedding)
                    # append embedding into embeddings list
                    embeddings.append(embedding)
            else:
                st.error(chunks.message, icon="🚨")
        st.write(embeddings)
        
