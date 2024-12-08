from langchain.chat_models import ChatOpenAI
from datasets import Dataset
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from langchain_community.llms import huggingface_pipeline
from langchain.chains import RunnablePassthrough

from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline


def Evaluator(retriever):
    # Load tokenizer and model from Hugging Face
    model_name = "meta-llama/Llama-2-7b-chat-hf"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")

    llama_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer)

    llm = huggingface_pipeline(pipeline=llama_pipeline)

    # Define prompt template
    template = """You are an assistant for question-answering tasks. 
    Use the following pieces of retrieved context to answer the question. 
    If you don't know the answer, just say that you don't know. 
    Use two sentences maximum and keep the answer concise.
    Question: {question} 
    Context: {context} 
    Answer:
    """

    prompt = PromptTemplate(
        input_variables=["context", "question"], template=template
    )  # ChatPromptTemplate.from_template(template)

    # Setup RAG pipeline
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    questions = ["que necesita un gato para estar feliz"]
    ground_truths = [["que tenga un espacio limpio, no lo deje mucho tiempo"]]
    answers = []
    contexts = []

    # Inference
    for query in questions:
        answers.append(rag_chain.invoke(query))
        contexts.append(
            [docs.page_content for docs in retriever.get_relevant_documents(query)]
        )

    # To dict
    data = {
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truths": ground_truths,
    }

    # Convert dict to dataset
    dataset = Dataset.from_dict(data)

    return dataset
