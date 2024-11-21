import streamlit as st

pages = {
    "Load files and process data": [
        st.Page(
            "src/components/loader/process_data/app_process_data.py",
            title="Load and process data",
        ),
        st.Page("src/components/loader/directory/app_directory.py", title="Directory"),
    ],
    "retriever": [
        st.Page("src/components/retrievers/app_retriever.py", title="Retriever")
    ],
}

pg = st.navigation(pages)
pg.run()
