import streamlit as st

pages = {
    "Load files and process data": [
        st.Page(
            "src/components/loader/process_data/app_process_data.py",
            title="Load and process data",
        )
    ],
    "Embeddings": [
        st.Page("src/components/retrievers/app_embeddings.py", title="Vector search")
    ],
}

pg = st.navigation(pages)
pg.run()
