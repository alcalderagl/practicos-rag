from langchain.text_splitter import CharacterTextSplitter
from .Document import Document

def greeting(name="Alex"):
    return f"hello there, {name} !"

def chuck_doc(document:Document):
    text_splitter = CharacterTextSplitter(
        chunk_size = 35,
        chunk_overlap=0,
        separator='',
        strip_whitespace=True
    )
    # chucking docs
    docs = text_splitter.create_documents([document.doc])
    document_dicts = [{"metadata": doc.metadata, "page_content": doc.page_content} for doc in docs]
    return document_dicts