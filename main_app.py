import streamlit as st

pages = {
    "Load files and process data": [
        st.Page(
            "src/components/loader/process_data/process_data_view.py",
            title="Load and process data",
        ),
        st.Page("src/components/loader/directory/directory_view.py", title="Directory"),
    ],
    "Chat": [st.Page("src/components/chat_view.py", title="RAG App")],
}

pg = st.navigation(pages)
pg.run()
