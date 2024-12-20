import os
import logging
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate

logging.basicConfig(level=logging.INFO)


class OllamaLlm:
    def __init__(self) -> None:
        """
        Initialize LLM
        """
        # ollama hostname
        self.ollama_host = os.getenv("OLLAMA_HOST", "localhost")
        # ollama port
        self.ollama_port = os.getenv("OLLAMA_PORT", "11434")
        # instance of OllamaLLM with model llama3
        self.llm = OllamaLLM(
            model="llama3", base_url=f"http://{self.ollama_host}:{self.ollama_port}"
        )

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
            response = self.llm(prompt=formatted_prompt)
            return response
        except (ValueError, KeyError) as e:
            # if there's an error then
            logging.info("llm-prompt-error %", e)
            return "No se pudo generar respuesta"
