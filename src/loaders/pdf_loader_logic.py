from langchain_community.document_loaders import PyPDFLoader
from src.commons.models.loaders.loader_response import LoaderModel
from PyPDF2 import PdfReader
import logging

logging.basicConfig(level=logging.INFO)


def PDFLoader(file_path: str):
    """
    Load document into PyPDFLoader langchain library

    Parameters
    ----------
    file_path : str
        Directory path

    Returns
    -------
    LoaderModel
        returns an array of LoaderModel
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
    pages = _PDFPages(document)
    logging.info(metadata)
    return pages


def _PDFPages(pages: any):
    """
    Load document into PDFLoader langchain library

    Parameters
    ----------
    pages : any
        Directory path

    Returns
    -------
    LoaderModel
        this returns an array of LoaderModel
    """
    pdfPageResp = [
        LoaderModel(page_content=page.page_content, metadata=page.metadata)
        for page in pages
    ]
    return pdfPageResp


def _extract_metadata(file_path: str):
    reader = PdfReader(file_path)
    # get metadata from PdfReader
    metadata = reader.metadata
    return metadata
