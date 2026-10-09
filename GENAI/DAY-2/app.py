## website link: https://platform.openai.com/home

import os
from dotenv import load_dotenv
load_dotenv(override=True)

from numpy import tile
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


# ENABLING THE LANGSMITH TRACING
# https://smith.langchain.com/ HERE WE CAN TRACE OUR LLM CALLS OR SIMPLE TERMS WE CAN ENABLE MONITORING
LANGSMITH_TRACING=True
LANGSMITH_PROJECT="QUANTAM-FDE"
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")


# Configuring OPENAI API KEY
os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")



#streamlit configuration
st.set_page_config(page_title="OpenAI Chatbot")
st.title("OPENAI custom GPT with LAngsmith Monitoring")


st.sidebar.title("⚙️ Settings")
temperature = st.sidebar.slider(
    "Temperature", 0.0,1.0,0.7
)


max_tokens = st.sidebar.slider(
    "Max Token",100,10000,500
)

input_text = st.text_input("Ask your questions...")

# prompt template

prompt = ChatPromptTemplate.from_messages(
    [
        ("system","you are helpfull assitnat"),
        ("user","Question: {question}")
    ]
)

# llm model initilisation

llm = ChatOpenAI(
    model = "gpt-5-nano-2025-08-07",
    temperature=temperature,
    max_tokens = max_tokens
)

# Controling output format
output = StrOutputParser()

chain =  prompt|llm|output


if input_text:
    with st.spinner("generating response..."):
        response = chain.invoke({"question":input_text})
        st.write(response)