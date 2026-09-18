import base64
from pathlib import Path

import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage

st.set_page_config(page_title="ITKannadigaru | Groq LLM", page_icon="🥃", layout="wide")

MAP_IMAGE = base64.b64encode(
    (Path(__file__).parent / "assets" / "karnataka-map-glow.png").read_bytes()
).decode()

# ---------- ITKannadigaru theme ----------
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Kannada:wght@600;800&display=swap');

    .stApp {{
        background: #070b14;
        color: #ffffff;
        background-image:
            linear-gradient(rgba(255, 209, 0, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 209, 0, 0.05) 1px, transparent 1px);
        background-size: 42px 42px;
    }}
    .block-container {{ padding-top: 2rem; max-width: 1000px; }}
    h1 {{
        font-weight: 800;
        color: #ffd100;
        text-shadow: 0 0 18px rgba(255, 209, 0, 0.45);
    }}
    .subtitle {{ color: #9ca3af; margin-top: -0.6rem; margin-bottom: 1.5rem; }}

    [data-testid="stChatMessage"] {{
        background: #111827;
        border: 1px solid rgba(255, 209, 0, 0.15);
        border-radius: 14px;
        padding: 0.75rem 1rem;
        margin-bottom: 0.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.3);
    }}

    section[data-testid="stSidebar"] {{
        background: #0c1220;
        border-right: 1px solid rgba(255, 209, 0, 0.15);
    }}
    .map-slogan {{
        font-family: 'Noto Sans Kannada', sans-serif;
        font-weight: 800;
        font-size: 1.35rem;
        text-align: center;
        color: #ffd100;
        text-shadow: 0 0 10px rgba(255, 209, 0, 0.55), 0 0 22px rgba(255, 209, 0, 0.35);
        line-height: 1.4;
        margin-top: 0.5rem;
    }}
    .map-slogan-en {{
        text-align: center;
        color: #ffffff;
        font-size: 0.85rem;
        margin-top: 0.4rem;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🥃 ITKannadigaru Groq LLM Chat")
st.markdown('<p class="subtitle">Prompt engineering playground — ITK GenAI Series</p>', unsafe_allow_html=True)

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown(
        f'<img src="data:image/png;base64,{MAP_IMAGE}" style="width:100%;" />'
        '<p class="map-slogan">ಕನ್ನಡಿಗನಿಂದ<br/>ಕನ್ನಡಿಗರಿಗಾಗಿ</p>'
        '<p class="map-slogan-en">By a Kannadiga,<br/>For Kannadigas.</p>',
        unsafe_allow_html=True,
    )
    st.divider()

    st.header("⚙️ Groq LLM Configuration")

    groq_api_key = st.text_input("Enter your Groq API Key", type="password", placeholder="gsk_..........")

    model = st.selectbox("Select a model", ["openai/gpt-oss-120b", "qwen/qwen3.6-27b"])

    system_prompt = st.text_area(
        "System prompt",
        value="""
        You are a staff-level software engineer conducting a mentoring code review.

    Your style: Direct, educational, and encouraging. Point out issues clearly
    but explain WHY something is a problem. Always suggest the better approach.

Format every review as:
🟢 What's good
🟡 What could be improved (with explanation and fix)
🔴 What must be changed (with explanation and fix)

        Never rewrite the entire code — teach in kannada but use all english sentences to help them understand the concepts, don't do it for them.
        Also give answers only for code related questions, if the question is not related to code, 
        politely tell them that you can only answer code related questions.
        
""",
        height=100,
    )

    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.5, step=0.1)

    max_tokens = st.slider("Max Tokens", min_value=100, max_value=1000, value=500, step=100)

    st.divider()
    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ---------- Conversation history ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------- Chat input (Enter to send, Shift+Enter for new line) ----------
question = st.chat_input("Ask your question... (Shift+Enter for a new line)")

if question:
    if not groq_api_key:
        st.error("Please enter your Groq API Key in the sidebar")
    else:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        history = [
            HumanMessage(content=m["content"]) if m["role"] == "user" else AIMessage(content=m["content"])
            for m in st.session_state.messages[:-1]
        ]

        prompt = ChatPromptTemplate.from_messages(
            [("system", system_prompt), ("placeholder", "{history}"), ("user", "{question}")]
        )

        llm = ChatGroq(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            api_key=groq_api_key,
        )

        chain = prompt | llm | StrOutputParser()

        with st.chat_message("assistant"):
            response = st.write_stream(
                chain.stream({"question": question, "history": history})
            )

        st.session_state.messages.append({"role": "assistant", "content": response})