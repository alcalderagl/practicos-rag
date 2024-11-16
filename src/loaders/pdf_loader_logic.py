from langchain_community.document_loaders import PyPDFLoader


def PDFLoader(path_route: str):
    """
    this function could load online or local pdf
    @path: it could be an URL if it's not loca and a path if it is local
    @isLocal: it determines if it's local o remote load
    returns a generator object to yields one item at time (lazy-evaluated)
    """
    loader = PyPDFLoader(path_route)
    document = loader.load_and_split()
    pages = _PDFPages(document)
    return pages


def _PDFPages(pages):
    """
    this returns a generator object (lazy-evaluated)
    """
    pdfPageResp = (
        {
            "pageContent": page.page_content,
            "source": page.metadata["source"],
            "page": page.metadata["page"],
        }
        for page in pages
    )
    return pdfPageResp
