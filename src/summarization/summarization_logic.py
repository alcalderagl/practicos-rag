# from langchain.chains.summarize import 
import logging
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from src.llm.llm_logic import LageLangueModel
logging.basicConfig(level=logging.INFO)


class Summarization:
    def __init__(self):
        pass
    
    def summarize(self,query:str, ranked_results:any) -> any:
        try:
            LLM_model = LageLangueModel()
            opeAI_llm = LLM_model.connect_chat_openAI()
            # ollama_llm = LLM_model.connect_to_ollama()
            prompt = ChatPromptTemplate.from_messages(
                [("system", "Write a concise summary of the following based on the query and context:{query}\\n\\n{context}")]
            )
            chain_summarize = create_stuff_documents_chain(opeAI_llm, prompt)
            summary = chain_summarize.invoke({"context":ranked_results, "query": query})
            logging.info(f"summarized docs {summary}")
            return summary
        except (ValueError, KeyError) as e:
            logging.info(f"Error with summarization docs: {e}")
            return 'Ocurrio un error al realizar la sumarización'
            
