import streamlit as st
from src.vector_store_client.vector_store_client_logic import VectorStoreClient

# REDUX STATE

def initialize_variables():
    vector_store_client = VectorStoreClient()
    vector_store_client.create_collection()
    vector_store_client.create_vector_store()
    st.session_state.generated_questions = []
    
pages = {
    "Load files and process data": [
        st.Page(
            "src/components/loader/process_data_app.py",
            title="Load and process data",
            icon="📄"
        )
    ],
    "Retrievers": [
        st.Page("src/components/retrievers/initial_retriever_app.py", title="Initial vector retriever", icon="🧩"),
        # st.Page("src/components/retrievers/advance_retriever_app.py", title="Advance vector retriever", icon="📡"),
        # st.Page("src/components/retrievers/compare_retrievers_app.py", title="Compare vector retrievers", icon="⚖️")
        # 
    ],
    "Benchmarks": [
        st.Page("src/components/benchmark/generated_questions_app.py", title="Generated questions", icon="🧠"),
        st.Page("src/components/benchmark/benchmark_app.py", title="Benchmark", icon="📈")
    ],
    "Settings": [
        st.Page("src/components/settings/settings_app.py", title="Settings", icon="🔧")
    ]
}

pg = st.navigation(pages)
initialize_variables()
pg.run()
