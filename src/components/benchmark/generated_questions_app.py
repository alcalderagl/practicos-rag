import streamlit as st
import pandas as pd
from src.benchmark.benchmark_logic import Benchmark
from src.components.alerts.alerts_app import get_alert_message
from src.commons.enums.type_message import TypeMessage
from src.commons.models.response_logic import ResponseLogic
from src.commons.logging_messages import LOGG_MESSAGES

benchmark = Benchmark()
st.title("Generated questions")


def initialized_benchmark() -> ResponseLogic:
    # get qa dataset
    file_response = benchmark.qa_dataset()
    st.session_state["generated_questions"] = file_response.response
    if file_response.type_message == TypeMessage.INFO:
        st.session_state["enabled_to_evaluate"] = True
    return file_response


def generate_question(no_question: int) -> ResponseLogic:
    # if st.button(btn_label):
    # generate questions
    generated_questions = benchmark.generate_questions(no_question=no_question)
    if generated_questions:
        return initialized_benchmark()
    else:
        return None


file_response = initialized_benchmark()

with st.form("generate_questions_form"):
    no_question = st.number_input(
        "Number of questions to generate", min_value=1, max_value=20
    )

    submitted = st.form_submit_button("Generate questions")

    if submitted:
        if file_response.type_message == TypeMessage.WARNING:
            generate_question(no_question=no_question)
            get_alert_message(file_response.type_message, file_response.message)
        elif file_response.type_message == TypeMessage.INFO:
            generated_question_resp = generate_question(no_question=no_question)
            if (
                generated_question_resp.type_message == TypeMessage.ERROR
                or generated_question_resp.type_message == TypeMessage.ERROR
            ):
                get_alert_message(
                    generated_question_resp.type_message,
                    generated_question_resp.message,
                )
        else:
            get_alert_message(file_response.type_message, file_response.message)


if len(st.session_state.generated_questions) > 0:
    content_data = st.session_state.generated_questions
    df = pd.DataFrame(content_data)
    st.dataframe(df)
else:
    st.write(LOGG_MESSAGES["APP_LABEL_BENCHMARK_MSG_NOT_GENERATED"])
