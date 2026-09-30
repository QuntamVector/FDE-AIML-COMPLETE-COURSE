import os
from pydoc import resolve
from urllib import response
import streamlit as st

from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

st.title("QuantamVetcorChatbot")


input_text = st.text_input("Ask your questions...?")

prompt = ChatPromptTemplate.from_messages(
    [
        ("system","hey your gym guy answer only gym related question incase of other question say bro am gym trainer...."),
        ("user","Questions: {question}")
    ]
)

llm = Ollama(
    model = "llama3.1:latest"
)

output_parser = StrOutputParser()

chain = prompt|llm|output_parser


if input_text:
    response = chain.invoke({"question": input_text})
    st.write(response)