# nl library
import spacy
import re
import numpy as np
from src.commons.models.token.token_info import TokenInfo
from sklearn.feature_extraction.text import TfidfVectorizer
from transformers import pipeline
import language_tool_python


class ProcessDocument:

    def __init__(self):
        # if you have more computational ressources use es_core_news_lg or es_dep_news_trf
        self.nlp = spacy.load("es_core_news_sm")
        self.stopwords = list(spacy.lang.es.stop_words.STOP_WORDS)

    def clean_doc(self, document: str) -> list[TokenInfo]:
        """
        Function to clean document content

        Parameters
        ----------
        document : str
            The text content of a document.

        Returns
        -------
        list[TokenInfo]
        Returns a list of document tokens
        """
        # to lowercase document
        document = document.lower()
        # remove whitespace character: spaces, tabs, newlines
        document = re.sub(r"\s+", " ", document).strip()
        # Remove special characters
        document = re.sub(r"[^\w\s]", "", document)
        # fix misspelled words
        document = self.misspelled_words("es", document)
        # tokeniz document
        doc = self.nlp(document)

        # tokens list
        tokens: list = []

        # for every token into doc
        for token in doc:
            token_ent_type = token.ent_type_ if token.ent_type else "0"
            token_info = TokenInfo(
                text=token.text,
                lemma=token.lemma_,
                pos=token.pos_,
                dep=token.dep_,
                ent_type=token_ent_type,
                is_stopword=token.is_stop,
            )
            tokens.append(token_info)
        return tokens

    def getKeywords(self, document: str) -> list[str]:
        """
        Function to get keywords from a document

        Parameters
        ----------
        document : str
            The text content of a document.

        Returns
        -------
        list[str]
        Returns a list of keywords.
        """
        # Initialize TF-IDF vectorizer with spanish stop_words
        vectorizer = TfidfVectorizer(stop_words=self.stopwords)
        # fit the vectorizer to the document
        tfidf_matrix = vectorizer.fit_transform([document])
        # Get feature names (keywords)
        keywords = vectorizer.get_feature_names_out()
        # Get the corresponding TF-IDF scores
        tfidf_scores = tfidf_matrix.toarray().flatten()
        # Sort the indices of the TF-IDF scores in descending order
        sorted_indices = np.argsort(tfidf_scores)[::-1]
        top_n = 5
        # get the top N keywords
        top_keywords = [keywords[i] for i in sorted_indices[:top_n]]
        return top_keywords

    def get_summary_title(self, chunk) -> str:
        """
        Function to give a title of chunk

        Parameters
        ----------
        chunk : str
            chunking document

        Returns
        -------
        str
        returns the chunk's title
        """
        summarizer = pipeline("summarization", model="t5-base")
        # Generate a summary of the chunk (keeping it short for the title)
        summary = summarizer(chunk, max_length=50, min_length=30, do_sample=False)
        return summary[0]["summary_text"]

    def misspelled_words(self, lang: str, text: str) -> str:
        """
        Function to fix misspelled words with a given language

        Parameters
        ----------
        lang : str
            language to fix text misspelling words
        text : str
            text

        Returns
        -------
        str
        returns the misspelled text fixed
        """
        # instance of LanguageTool to spanish
        tool = language_tool_python.LanguageTool(lang)
        # make spanish corrections
        matches = tool.check(text=text)
        text = language_tool_python.utils.correct(text=text, matches=matches)
        return text
