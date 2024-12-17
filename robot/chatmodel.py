from langchain_google_genai import ChatGoogleGenerativeAI

api_key = 'AIzaSyCkrfnoNPdLr_a65cmVDkUNQxQbD4ZrPrc'
model = 'gemini-1.5-flash'

chat = ChatGoogleGenerativeAI(model=model,
                              google_api_key=api_key,
                              temperature=0.5)
