# nl library
import spacy


def clean_doc(document: str):
    """
    @param<doc>: it is a document string
    this functions its called to clean the chunkings applying
    1. sentence lowercasing
    2. sentence removal of puntuation
    3. removing stopwords
    5. filtering if token lenght is higher than 2 characteres
    """
    # if you have more computational ressources use es_core_news_lg or es_dep_news_trf
    nlp = spacy.load("es_core_news_sm")
    spacy_stopwords = spacy.lang.es.stop_words.STOP_WORDS
    # tokenization of document
    doc = nlp.tokenizer(document)
    # cleaning text
    doc = (
        token.text.lower()
        for token in doc
        if token.is_alpha and len(token.text) > 2
        # if not spacy_stopwords and token.is_alpha and len(token.text) > 2
    )
    # join the tokens into one string
    doc = " ".join(doc)
    # returning the doc preprocessed
    return doc
