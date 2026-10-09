import os
from click import prompt
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st

st.title("Chat with Ollama")

temperature = st.slider("Temperature",0.0,1.0,0.7) #start end defualt

# Prompt 
prompt = ChatPromptTemplate.from_messages(
    [
        ("system","you are helpfull assitnat"),
        ("user","Question: {question}")
    ]
)

# llm model initilisation

llm = Ollama(
    model = "mistral:latest",
    temperature=temperature,
)

# Controling output format
output = StrOutputParser()

chain =  prompt|llm|output

input_text = st.text_input("Ask your questions.....")

if input_text:
    response = chain.invoke({"question":input_text})
    st.write(response)



