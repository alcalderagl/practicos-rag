import logging
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from PyPDF2 import PdfReader

logging.basicConfig(level=logging.INFO)


def PDFLoader(file_path: str)->List[Document]:
    """
    Load document into PyPDFLoader langchain library

    Parameters
    ----------
    file_path : str
        Directory path

    Returns
    -------
    List[Document]
        returns a list of Documents
    """
    loader = PyPDFLoader(file_path)
    document = loader.load_and_split()
    # getting the metadata using PyPDF2
    metadata = _extract_metadata(file_path)
    # into every document setting the properties of metadata
    for doc in document:
        doc.metadata.update(
            {
                "author": metadata.get("/Author", ""),
                "title": metadata.get("/Title", ""),
                "creation_date": metadata.get("/CreationDate", ""),
            }
        )
    # pages = _PDFPages(document)
    logging.info(metadata)
    return document

def _extract_metadata(file_path: str):
    """
    Extract document metadata using PdfReader

    Parameters
    ----------
    file_path : any
        file path

    Returns
    -------
    """
    reader = PdfReader(file_path)
    # get metadata from PdfReader
    metadata = reader.metadata
    return metadata
