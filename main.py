import os
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
import pandas as pd
from utils.upload_files import handle_file_upload
from utils.delete_all_files import handle_file_delete
from robot.chatmodel import get_chat_response
import uuid


# ---------- Define Folder Paths ---------------------------
save_folder = "./store"


# ----------------- Main Streamlit App ---------------------
st.set_page_config(page_title="Cyber Reader",
                   page_icon="./static/icon/cyberhammer.webp", layout="wide")
st.header("Cyber Reader")


# Sidebar title
st.sidebar.image("./static/icon/cyberhammer.webp", use_container_width=True)
st.sidebar.title("Cyber Hammer Project")

# Sidebar menu

# --------- add a file uploader and file deleter ------------
st.sidebar.markdown("### File Upload and Delete")
# Call the file upload handler function and get the list of uploaded files
uploaded_files_list = handle_file_upload(save_folder)
# Call the file delete handler function and remove all of uploaded files
uploaded_files_list = handle_file_delete(save_folder)
# Display the file list as a table in the sidebar
if uploaded_files_list:
    file_df = pd.DataFrame(uploaded_files_list, columns=["Uploaded Files"])
    st.sidebar.dataframe(file_df, width=600, hide_index=True)
else:
    st.sidebar.warning("No files uploaded yet.")


# ---------------- add Chat Part ---------------------------
st.caption("🚀 A Super chatbot powered by Cyber. Based on AI Agent, it is more in line with cybernetics and ergonomics")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "How can I help you?"}
    ]


for msg in st.session_state['messages']:
    st.chat_message(msg["role"]).write(msg["content"])

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = str(uuid.uuid4())


if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    st.session_state["messages"].append({"role": "user", "content": prompt})

    res = get_chat_response(prompt, st.session_state['thread_id'])

    st.chat_message("assistant").write(res['answer'])
    st.session_state["messages"].append(
        {"role": "assistant", "content": res['answer']})

# ----------------- Document Processing ---------------------
st.sidebar.markdown("### Document Processing")

if "references" not in st.session_state:
    st.session_state["references"] = ''

if st.sidebar.button("Process Document", use_container_width=True) and len(uploaded_files_list) > 0:
    doc_full = ''
    # Load the PDF document
    pdf_paths = [os.path.join(save_folder, file)
                 for file in uploaded_files_list]
    # print(pdf_paths)

    for pdf_path in pdf_paths:
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()
        for doc in docs:
            doc_full += doc.page_content

    # print(doc_full)
    st.session_state["references"] = 'I just upload a document for you, please answer my question based on the doc content: \n\n' + doc_full + '\n\n'

    res = get_chat_response(
        st.session_state["references"], st.session_state['thread_id'])

    st.chat_message("user").write('Upload files!')
    st.chat_message("assistant").write(res['answer'])
    st.session_state["messages"].append(
        {"role": "user", "content": 'Upload files!'})
    st.session_state["messages"].append(
        {"role": "assistant", "content": res['answer']})
