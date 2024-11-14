from langchain_community.document_loaders import PyPDFLoader, OnlinePDFLoader


def load_pfd(path: str, islocal: bool = True):
    """
    this function could load online or local pdf
    @path: it could be an URL if it's not loca and a path if it is local
    @isLocal: it determines if it's local o remote load
    returns a generator object to yields one item at time (lazy-evaluated)
    """

    try:
        # catch an error in a friendly way to dont stop program execution
        if islocal:
            # if it is local then
            _load_local_pdf(path)
        else:
            # otherwise
            _load_online_pdf(path)
    except Exception as e:
        # catching the exception error
        print(f"Error while loading PDF: {e}")
        return []


def _load_local_pdf(path_route: str):
    """
    this function loads a local pdf by path_route
    returns an object structured to be processed by chuncking
    """
    loader = PyPDFLoader(path_route)
    data = loader.load_and_split()
    return _builderObject(data)


def _load_online_pdf(pdf_URL: str):
    """
    this function loads an online pdf by webURL
    returns an object structured to be processed by chuncking
    """
    loader = OnlinePDFLoader(pdf_URL)
    data = loader.load_and_split()
    return _builderObject(data)


def _builderObject(data):
    """
    this returns a generator object (lazy-evaluated)
    """
    pages = (
        {"page_content": page.page_content, "source": page.metadata["source"]}
        for page in data
    )
    return pages


# if __name__ == '__main__':
#     test_it = "https://aragohv.com/wp-content/uploads/2019/06/comportamientofelino.pdf"
#     load_pfd(test_it, False)
