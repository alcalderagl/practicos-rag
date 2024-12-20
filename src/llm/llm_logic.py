import os
import logging
from langchain_ollama import OllamaLLM
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

logging.basicConfig(level=logging.INFO)


class LageLangueModel:
    def __init__(self) -> None:
        """
        Initialize LLM
        """
        # ollama hostname
        self.ollama_host = os.getenv("OLLAMA_HOST", "localhost")
        # ollama port
        self.ollama_port = os.getenv("OLLAMA_PORT", "11434")
        self.ollama_model = os.getenv("OLLAMA_MODEL", "llama3")
        # OPENAI api key
        self.api_key = os.getenv("OPENAI_API_KEY", "XXXX")
        # gpt-4-turbo-preview
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

        
    def connect_to_ollama(self) -> OllamaLLM:
        llm = OllamaLLM(
            model="llama3", base_url=f"http://{self.ollama_host}:{self.ollama_port}"
        )
        return llm
    
    def connect_chat_openAI(self) -> ChatOpenAI:
        openai_llm = ChatOpenAI(api_key=self.api_key, model=self.openai_model)
        return openai_llm
    
    def connect_chat_ollama(self):
        pass
    

    def prompter(self, input_variables: list[str], template: str) -> str:
        """
        Creates a prompter to LLM

        Parameters
        ----------
        input_variables : list[str]
            if the prompter templates requires of variables
        template: str
            the prompter template

        Returns
        -------
        string
            returns a LLM response
        """
        try:
            # initialize prompter template
            prompt_template = PromptTemplate(
                input_variables=input_variables, template=template
            )
            # get key, value input variables
            variables = dict(zip(prompt_template.input_variables, input_variables))
            # formatted prompt with template and input variables
            formatted_prompt = prompt_template.format(**variables)
            # return llm response
            return formatted_prompt
        except (ValueError, KeyError) as e:
            # if there's an error then
            logging.info(f"Error with prompter: {e}")
            return ""
