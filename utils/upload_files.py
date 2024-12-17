import streamlit as st
import os
# Define a function to handle file uploads and display


def handle_file_upload(save_folder):
    # Ensure the folder exists
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # File uploader widget
    uploaded_file = st.sidebar.file_uploader(
        "File Uploading Part",
        type=["pdf"],
        help="Scanned documents are not supported yet!",
    )

    # Handle the uploaded file
    if uploaded_file is not None:
        # Get the file details
        file_name = uploaded_file.name
        file_path = os.path.join(save_folder, file_name)

        # Save the uploaded file to the specified folder
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Display success message
        st.success(
            f"File '{file_name}' has been saved to '{save_folder}' successfully!")

    # Return the list of files in the folder after file upload
    return os.listdir(save_folder)
