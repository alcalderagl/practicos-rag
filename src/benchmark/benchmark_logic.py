from datasets import Dataset
import random
import os
import logging
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain_ollama import OllamaEmbeddings
from langchain_openai import OpenAIEmbeddings
import pandas as pd
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_recall,
    context_precision,
)
from src.benchmark.models.evaluation import Evaluation
from src.benchmark.models.question_answer import QuestionAnswer
from src.llm.llm_logic import OllamaLlm
from src.vector_store_client.vector_store_client_logic import VectorStoreClient
from src.commons.files_logic import FileManager
from src.commons.models.response_logic import ResponseLogic
from src.commons.enums.type_message import TypeMessage
from langchain_openai import ChatOpenAI

logging.basicConfig(level=logging.INFO)

class Benchmark:
    def __init__(self):
        self.dir_path="data/questions/"
        self.file_name="questions.csv"
        pass
    
    def generate_questions(self, no_question:int)->bool:
        qa_generation_prompt = ChatPromptTemplate.from_template("""
        Your task is to write a factoid question and an answer given a context.
        Your factoid question should be answerable with a specific, concise piece of factual information from the context.
        Your factoid question should be formulated in the same style as questions users could ask in a search engine.
        This means that your factoid question avoid something like "according to the passage" or "context" or "en el contexto".

        Provide your answer and factoid in spanish must no mention "Here is the factoid question and answer in Spanish" it must be as follows:

        Output:::
        Factoid question: (your factoid question)
        Answer: (your answer to the factoid question)

        Now here is the context.

        Context: {context}
        """)
        
        ollama = OllamaLlm()
        
        question_chain = ({"context": RunnablePassthrough()}
                          | qa_generation_prompt
                          | ollama.llm
                          | StrOutputParser()
        )
        
        vector_store_client = VectorStoreClient()
        all_points = vector_store_client.client.scroll(collection_name=vector_store_client.collection_name, with_payload=True, limit=1000)
        
        all_docs = [point.payload for point in all_points[0]]
        sampled_docs = random.sample(all_docs, no_question)
        sampled_docs_processed = [doc["page_content"] for doc in sampled_docs if "page_content" in doc]
        
        logging.info(f"sampled_docs => {sampled_docs_processed}")
        
        faqs = [question_chain.invoke({"context": sampled_context}) for sampled_context in sampled_docs_processed]
        logging.info(f"questions => {faqs}")
        file_manager = FileManager()
        # file_manager.save_json_file("data/questions/", "questions", faqs)
        
        data = self._parse_qa(qas=faqs)
        if len(data) > 0:
            file_manager.save_csv_file(dir_path=self.dir_path,file_name=self.file_name, data=data,headers=["question", "answer"])
        return True
    
    def _parse_qa(self, qas:list[str]) -> list[any]:
        parsed_data:list[any] = []
        try:
            for qa in qas:
                question, answer = qa.split("Answer: ")
                question = question.replace("Factoid question: ", "").strip()
                answer = answer.strip()
                parsed_data.append(QuestionAnswer(question=question, answer=answer).model_dump())
        except (ValueError, KeyError) as e:
            logging.info(f"Error with parsed questions & answers {e}")
        return parsed_data
                
            
    
    def evaluate(self, evaluation_data: Evaluation):
        try:
            ollama = OllamaLlm()
            vector_store_client = VectorStoreClient()
            retriever = vector_store_client.vector_store.as_retriever()
            embeddings = OllamaEmbeddings(model="llama3")
            openai_embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
            api_key = os.getenv("OPENAI_API_KEY", "")
            openai_llm= ChatOpenAI(api_key=api_key, model="gpt-4-turbo-preview")
            
            logging.info(f"api_key -> {api_key}")
            
            # Define prompt template
            template = """Utilize the retrieved context below to answer the question.
            If you're unsure of the answer, simply state you don't know and apologies
            Keep your response concise, limited to two sentences.
            Question: {question}
            Context: {context}
            """
            # input_variables=["context", "question"], template=t 
            prompt = ChatPromptTemplate.from_template(
                template
            )

        

            # Setup RAG pipeline
            rag_chain = (
                {"context": retriever, "question": RunnablePassthrough()}
                | prompt
                | openai_llm
                | StrOutputParser()
            )

            # Inference
            for index, query in enumerate(evaluation_data.question):
                
                evaluation_data.answer.append(rag_chain.invoke(query))
                evaluation_data.retrieved_contexts.append([
                    docs.page_content
                    for docs in retriever.get_relevant_documents(query)
                ])
            
            # Convert dict to dataset
            data = evaluation_data.model_dump()
            logging.info(f"benchmark type {type(data)} OK {data}")
            dataset = Dataset.from_dict(data)
            
            
            # result = evaluate(
            #     dataset=dataset,
            #     llm=openai_llm,
            #     embeddings=openai_embeddings,
            #     metrics=[
            #         context_precision,
            #         context_recall,
            #         faithfulness,
            #         answer_relevancy,
            #     ],
            # )
            # logging.info(f"benchmark OK {result.to_pandas()}")
            
            
            # if isinstance(result, pd.DataFrame):            
            #     # Specify the local folder and file name
            #     dir_path = "data/benchmark"
            #     os.makedirs(dir_path, exist_ok=True)  # Create folder if it doesn't exist
            #     file_path = os.path.join(dir_path, "evaluation.csv")
            #     result.to_csv(file_path, index=False, encoding="utf-8")
                
            # return result.to_pandas()
            return "OK"
        except (ValueError, KeyError) as e:
            logging.info("Error with benchmark %", e)
            return []
        
    def qa_dataset(self)-> ResponseLogic:
        response = ResponseLogic(response=[], type_message=TypeMessage.ERROR, message="")
        try:
            file_manager = FileManager()
            items = file_manager.read_csv(dir_path=self.dir_path,file_name=self.file_name)
            response.message="OK"
            response.response = items
            response.type_message = TypeMessage.INFO
        except FileNotFoundError:
            response.message=f"Error: File {self.file_name} not found."
            response.type_message = TypeMessage.WARNING
        except (ValueError, KeyError) as e:
            response.message=f"There's an error with the file {e}"
        return response
        
        
        