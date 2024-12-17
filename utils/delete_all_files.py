# Function to delete all uploaded files
import os
import shutil
import streamlit as st


def handle_file_delete(save_folder):
    # Button to delete all uploaded files
    if st.sidebar.button('Delete All Files',use_container_width=True):
        if os.path.exists(save_folder):
            # Delete the entire folder and its contents
            shutil.rmtree(save_folder)
            os.makedirs(save_folder)  # Recreate the empty folder
            st.sidebar.success("All files have been deleted.")
    # Refresh the file list after deletion
    return os.listdir(save_folder)
