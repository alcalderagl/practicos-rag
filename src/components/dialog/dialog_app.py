import streamlit as st

@st.dialog("INFO")
def show_dialog(msg:str, ):
    st.write(msg)
    
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Yes"):
            st.session_state.generated_questions = True
            st.rerun()
    with col2:
        if st.button("No"):
            st.session_state.generated_questions = False
            st.rerun()

