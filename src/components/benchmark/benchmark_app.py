import streamlit as st
import pandas as pd
from src.benchmark.benchmark_logic import Benchmark
from src.benchmark.models.evaluation import Evaluation
from src.commons.enums.type_message import TypeMessage
from src.commons.logging_messages import LOGG_MESSAGES

benchmark = Benchmark()
st.title("Benchmark")

if len(st.session_state["generated_questions"]) < 0:
    questions=[]
    ground_truths:list[str] = []
    for generated_question in st.session_state.generated_questions:
        questions.append(generated_question["question"])
        ground_truths.append(generated_question["answer"])
                
    evaluation = Evaluation(question=questions, reference=ground_truths, retrieved_contexts=[], answer=[])
    
    if st.button("Evaluate retrievers"):
        with st.container():
            st.subheader("Initial RAG")
            # evaluation_df = benchmark.evaluate(evaluation_data=evaluation)
            # st.dataframe(evaluation_df)
        with st.container():
            st.subheader("Advance RAG")
else:
    st.warning("You dont have any generated question, create generate questions")
    st.markdown("[Go to generated questions Page](/generated_questions_app)")


