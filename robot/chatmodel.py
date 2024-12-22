from langchain_google_genai import ChatGoogleGenerativeAI
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.messages import HumanMessage
from langchain_core.messages import AIMessage
from typing import Sequence
from langchain_core.messages import BaseMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages
from typing_extensions import Annotated, TypedDict
from langchain_core.output_parsers import StrOutputParser
from robot.system_prompt import sys_prompt


def chat_model():
    # --------------- Network Configuration --------------------
    # if using v2rayn as proxy, set the following environment variables
    os.environ["HTTP_PROXY"] = "http://127.0.0.1:10809"
    os.environ["HTTP_PROXYS"] = "http://127.0.0.1:10809"

    api_key = os.getenv("GOOGLE_GEMINI_API")
    model = 'gemini-2.0-flash-exp'

    chat = ChatGoogleGenerativeAI(model=model,
                                  google_api_key=api_key,
                                  temperature=0.5)

    return chat


class State(TypedDict):
    input: str
    chat_history: Annotated[Sequence[BaseMessage], add_messages]
    answer: None


prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", sys_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
    ]
)

# Define a new graph
# workflow = StateGraph(state_schema=State)
workflow = StateGraph(state_schema=State)


def call_model(state: State):
    model = prompt_template | chat_model() | StrOutputParser()
    # print(state["chat_history"])
    state["chat_history"].append(HumanMessage(state["input"]))
    response = model.invoke(state["chat_history"])
    return {
        "chat_history": [AIMessage(response)],
        "answer": response
    }


workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)


def get_chat_response(query, thread_id):
    config = {"configurable": {"thread_id": thread_id}}
    llm_res = app.invoke({"input": query}, config)
    return llm_res
