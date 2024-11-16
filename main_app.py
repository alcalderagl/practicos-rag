import streamlit as st

pages = {
    "Load files and process data": [
        st.Page("src/components/process_data_view.py", title="Load and process data"),
        # st.Page("src/components/query_data_view.py", title="Embedding query")
    ],
    "Chat": [st.Page("src/components/chat_view.py", title="RAG App")],
}

pg = st.navigation(pages)
pg.run()
