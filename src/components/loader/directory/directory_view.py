import streamlit as st
import os

# Specify the path to the folder you want to display
folder_path = "data/regulaciones"

# Check if the folder exists
if os.path.exists(folder_path):
    # List the files in the folder
    files = os.listdir(folder_path)
    st.write(f"Files in `{folder_path}`:")

    # Display each file
    for file in files:
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            st.write(file)

        with open(file_path, "rb") as file:
            btn = st.download_button(
                label="Download image",
                data=file,
                file_name=file.name,
                mime="text/pdf",
            )
else:
    st.error(f"The folder `{folder_path}` does not exist.")
