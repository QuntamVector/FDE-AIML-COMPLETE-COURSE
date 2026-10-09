import os
from click import prompt
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
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

llm = ChatGroq(
    model = "qwen/qwen3.8-27b"
)

# Controling output format
output = StrOutputParser()

chain =  prompt|llm|output

input_text = st.text_input("Ask your questions.....")

if input_text:
    response = chain.invoke({"question":input_text})
    st.write(response)



