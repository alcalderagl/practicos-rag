import logging
from langchain.prompts import ChatPromptTemplate
from langchain.chains.llm import LLMChain
from src.llm.llm_logic import LageLangueModel
from src.query_rewriting.models.query_rewriting import QuestionRewriting

logging.basicConfig(level=logging.INFO)


class QueryRewriting:
    def __init__(self):
        pass

    def rewriting(self, question: str) -> QuestionRewriting:
        """
        Refines a given query for better search results.

        Parameters
        ----------
        question : str
            The input query string to be refined.

        Returns
        -------
            QuestionRewriting
                An object containing the original query and the rewritten query.
        """
        try:

            LLM_model = LageLangueModel()

            template = """Provide a better search query for \
            web search engine to answer the given question, end \
            the queries with ’**’. Remember to respond in Spanish . Question: \
            {x} Answer:"""
            query_rewriting_prompt = ChatPromptTemplate.from_template(template=template)

            # OLLAMA
            # ollama = LLM.connect_to_ollama()
            # query_rewriting_chain = LLMChain(llm=ollama, prompt=query_rewriting_prompt)

            # CHATGPT
            open_ai_llm = LLM_model.connect_chat_openAI()
            query_rewriting_chain = LLMChain(
                llm=open_ai_llm, prompt=query_rewriting_prompt
            )
            rewriting_query = query_rewriting_chain.invoke(question)

            logging.info(f"response rewriting query: {rewriting_query}")
            re_query: str = rewriting_query["text"]
            re_query = (
                re_query.replace('Consulta: "', "")
                .replace('Consulta mejorada: "', "")
                .replace("Consulta", "")
                .replace('**"', "")
                .replace("**", "")
                .strip()
            )
            response = QuestionRewriting(query=question, rewriting_query=re_query)
            return response
        except (ValueError, KeyError) as e:
            logging.info(f"error when rewriting_query: {e}")
            return QuestionRewriting(query="", rewriting_query="")
