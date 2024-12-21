import logging
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from src.llm.llm_logic import LageLangueModel
from src.commons.logging_messages import LOGG_MESSAGES

logging.basicConfig(level=logging.INFO)


class Summarization:
    def __init__(self):
        pass

    def summarize(self, query: str, ranked_results: any) -> str:
        """
        Summarizes content based on a query and context using a language model.

        Parameters
        ----------
        query : str
            The query string that provides the focus for the summary.
        ranked_results : any
            The context or ranked results to be summarized.

        Returns
        -------
        str
            A concise summary of the context based on the query, or an error message
            if the summarization process fails.
        """
        try:
            # instance of LLM
            LLM_model = LageLangueModel()
            # connection to openAI
            opeAI_llm = LLM_model.connect_chat_openAI()
            # if you want can use ollama
            # ollama_llm = LLM_model.connect_to_ollama()
            # promter template
            prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        "Write a concise summary of the following based on the query and context:{query}\\n\\n{context}",
                    )
                ]
            )
            # Create a document summarization chain using the OpenAI LLM and the prompt
            chain_summarize = create_stuff_documents_chain(opeAI_llm, prompt)
            # Invoke the summarization chain with the context and query
            summary = chain_summarize.invoke(
                {"context": ranked_results, "query": query}
            )
            logging.info(f"summarized docs {summary}")
            # return the generated summary
            return summary
        except (ValueError, KeyError) as e:
            # Handle specific exceptions and log the error
            logging.info(f"Error with summarization docs: {e}")
            return LOGG_MESSAGES["SUMMARIZATION_ERROR"].format(error=e)
