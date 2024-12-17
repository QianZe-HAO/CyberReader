import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
import pandas as pd
from utils.upload_files import handle_file_upload
from utils.delete_all_files import handle_file_delete
import os
from langchain_google_genai import ChatGoogleGenerativeAI


# ---------- Define Folder Paths ---------------------------
save_folder = "./store"

# --------------- Network Configuration --------------------
# if using v2rayn as proxy, set the following environment variables
os.environ["HTTP_PROXY"] = "http://127.0.0.1:10809"
os.environ["HTTP_PROXYS"] = "http://127.0.0.1:10809"

api_key = 'xxxxxxxxxxxxxxxxxxx'
model = 'gemini-1.5-flash'
chat = ChatGoogleGenerativeAI(model=model, google_api_key=api_key)
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


# ----------------- Document Processing ---------------------
st.sidebar.markdown("### Document Processing")

if "references" not in st.session_state:
    st.session_state["references"] = ''

doc_full = ''
if st.sidebar.button("Process Document", use_container_width=True) and len(uploaded_files_list) > 0:
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
    st.session_state["references"] = doc_full


# ---------------- add Chat Part ---------------------------
st.caption("🚀 A Super chatbot powered by Cyber. Based on AI Agent, it is more in line with cybernetics and ergonomics")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "How can I help you?"}
    ]


for msg in st.session_state['messages']:
    st.chat_message(msg["role"]).write(msg["content"])


if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    st.session_state["messages"].append({"role": "user", "content": prompt})

    if len(st.session_state["references"]) > 0:
        prompt = st.session_state["references"] + prompt

    res = chat.invoke(prompt)
    st.chat_message("assistant").write(res.content)
    st.session_state["messages"].append({"role": "assistant", "content": res.content})
