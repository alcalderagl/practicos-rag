# nl library
import spacy

# chuncking with langchaing library
from langchain.text_splitter import CharacterTextSplitter


def chuck_doc(document: str):
    text_splitter = CharacterTextSplitter(
        chunk_size=35, chunk_overlap=0, separator="", strip_whitespace=True
    )
    # chucking docs
    docs = text_splitter.create_documents([document])
    # return a dict array with the chuncks
    document_dicts = (
        {"metadata": doc.metadata, "page_content": doc.page_content} for doc in docs
    )
    return document_dicts


def clean_doc(document: str):
    # if you have more computational ressources use es_core_news_lg or es_dep_news_trf
    nlp = spacy.load("es_core_news_sm")
    """
    @param<doc>: it is a document string
    this functions its called to clean the chunkings applying
    1. sentence lowercasing
    2. sentence removal of puntuation
    3. removing stopwords
    5. filtering if token lenght is higher than 2 characteres
    """
    # tokenization of document
    doc = nlp.tokenizer(document)
    # cleaning text
    doc = (
        token.text.lower()
        for token in doc
        if not token.is_stop and token.is_alpha and len(token.text) > 2
    )
    # join the tokens into one string
    doc = " ".join(doc)
    # returning the doc preprocessed
    return doc
