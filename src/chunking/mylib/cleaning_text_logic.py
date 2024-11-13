# nl library
import spacy
from .Document import Document

def clean_doc(document:Document):
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
    doc = nlp.tokenizer(document.doc)
    # cleaning text
    doc = [token.text.lower() for token in doc if not token.is_stop and token.is_alpha and len(token.text) > 2]
    doc = " ".join(doc)
    return doc