# CyberReader

🚀 A Super chatbot powered by Cyber. Based on AI Agent, it is more in line with cybernetics and ergonomics

## 0x00 Before Running
* Step 1: Get Google Gemini API key from [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey) or change the LLM model by editing `chat_model()` in the file [/robot/chatmodel.py](./robot/chatmodel.py)
* Step 2: Setup Conda Environment
```bash
conda create --name CyberReader python=3.11
conda activate CyberReader
# pip install packages
pip install -r requirements.txt
```

## 0x01 Run the Cyber Reader
```bash
streamlit run main.py
```