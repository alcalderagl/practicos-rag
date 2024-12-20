import streamlit as st
import pandas as pd
from src.benchmark.benchmark_logic import Benchmark
from src.benchmark.models.evaluation import Evaluation
from src.components.alerts.alerts_app import get_alert_message
from src.commons.enums.type_message import TypeMessage
from src.components.dialog.dialog_app import show_dialog
from src.commons.logging_messages import LOGG_MESSAGES

benchmark = Benchmark()
st.title("Benchmark")

if "generated_questions" not in st.session_state:
    st.session_state.generated_questions = []
if "evaluate" not in st.session_state:
    st.session_state.evaluate = False
    

def initialized_benchmark():
    file_response = benchmark.qa_dataset()
    update_dataset(data=file_response.response)
    return file_response

def generate_question(btn_label:st):
    if st.button(btn_label):
        generated_questions = benchmark.generate_questions()
        if generated_questions:
            file_response = benchmark.qa_dataset()
            update_dataset(data=file_response.response)
            
def update_dataset(data):
    data = benchmark.qa_dataset().response
    st.session_state["generated_questions"]=data

file_response = initialized_benchmark()

if len(st.session_state.generated_questions) > 0:
    st.subheader("Generated questions")
    content_data = st.session_state.generated_questions
    df = pd.DataFrame(content_data)
    st.dataframe(df)
else:
    st.write(LOGG_MESSAGES["APP_LABEL_BENCHMARK_MSG_NOT_GENERATE"])

if file_response.type_message == TypeMessage.WARNING:
    generate_question("Generate questions")
    get_alert_message(file_response.type_message, file_response.message)
elif file_response.type_message == TypeMessage.INFO:
    col1, col2 = st.columns(2)
    with col1:
        generate_question("Generate more questions")
    with col2:
        if st.button("Evaluate RAG"):
            st.session_state.evaluate = True
            questions=[]
            ground_truths:list[str] = []
            for generated_question in st.session_state.generated_questions:
                # st.write(generated_question)
                questions.append(generated_question["question"])
                ground_truths.append(generated_question["answer"])
                
            evaluation = Evaluation(question=questions, reference=ground_truths, retrieved_contexts=[], answer=[])
            
    if st.session_state.evaluate:
        with st.container():
            st.subheader("Initial RAG")
            evaluation_df = benchmark.evaluate(evaluation_data=evaluation)
            st.dataframe(evaluation_df)
            #st.write(benchmark.evaluate(evaluation))
        with st.container():
            st.subheader("Advance RAG")
            # st.write(benchmark.evaluate(evaluation))
else:
    pass


