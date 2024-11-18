from langchain_community.document_loaders import PyPDFLoader
from src.commons.models.loaders.loader_response import LoaderModel


def PDFLoader(file_path: str):
    """
    Load document into PyPDFLoader langchain library

    Parameters
    ----------
    file_path : str
        Directory path

    Returns
    -------
    PDFLoaderModel
        returns a generator object to yields one item at time (lazy-evaluated)
    """
    loader = PyPDFLoader(file_path)
    document = loader.load_and_split()
    pages = _PDFPages(document)
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
    PDFLoaderModel
        this returns a generator object (lazy-evaluated).
    """
    pdfPageResp = (
        LoaderModel(
            pageContent=page.page_content,
            source=page.metadata["source"],
            page=page.metadata["page"],
        )
        for page in pages
    )
    return pdfPageResp
