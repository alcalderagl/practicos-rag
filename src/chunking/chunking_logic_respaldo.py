# chuncking with langchaing library
from langchain.text_splitter import CharacterTextSplitter


def chuck_doc(document: str):
    """
    function to chuck loader pages
    """

    # return a generator object (lazy-evaluated)
    try:
        text_splitter = CharacterTextSplitter(
            chunk_size=35, chunk_overlap=0, separator="", strip_whitespace=True
        )
        # chucking docs
        chuncks = text_splitter.create_documents([document])
        print(chuncks)
    except (ValueError, KeyError) as e:
        print(e)

    # document_dicts = (
    #    {"metadata": chunck.metadata, "pageContent": chunck.page_content}
    #    for chunck in chuncks
    # )
    # return document_dicts

    return "hello"


