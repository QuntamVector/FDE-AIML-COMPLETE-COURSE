import os
import streamlit as st
from dotenv import load_dotenv

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI

# ---------------------------------------------------------
# 1. Observability Configuration (LangSmith & Gemini)
# ---------------------------------------------------------
load_dotenv(override=True)

# Correct standard environment variables for LangChain / LangSmith
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGSMITH_PROJECT", "QUANTAM-FDE")

langsmith_key = os.getenv("LANGSMITH_API_KEY")
if langsmith_key:
    os.environ["LANGCHAIN_API_KEY"] = langsmith_key

google_key = os.getenv("GOOGLE_API_KEY")
if google_key:
    os.environ["GOOGLE_API_KEY"] = google_key

# ---------------------------------------------------------
# 2. Page & Styling Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Royal Gemini AI",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(circle at 10% 20%, #0d121d 0%, #05070b 90%);
        color: #E6E8EC;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    section[data-testid="stSidebar"] {
        background: #080c14;
        border-right: 1px solid rgba(212, 175, 55, 0.2);
    }
    
    h1, h2, h3 {
        color: #D4AF37 !important;
        font-weight: 700 !important;
    }

    .main-title-container {
        display: flex;
        align-items: center;
        gap: 12px;
        padding-bottom: 8px;
        border-bottom: 1px solid rgba(212, 175, 55, 0.2);
        margin-bottom: 24px;
    }

    div[data-testid="stChatMessage"] {
        background: rgba(18, 24, 38, 0.65);
        border: 1px solid rgba(212, 175, 55, 0.15);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }

    div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {
        border-left: 3px solid #D4AF37;
    }

    div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) {
        border-left: 3px solid #00C9A7;
    }

    .royal-badge {
        background: linear-gradient(135deg, #D4AF37 0%, #AA771C 100%);
        color: #07090E;
        font-weight: 700;
        font-size: 0.75rem;
        padding: 4px 10px;
        border-radius: 20px;
        display: inline-block;
        margin-bottom: 8px;
    }
    
    .token-pill {
        display: inline-flex;
        gap: 8px;
        background: rgba(212, 175, 55, 0.08);
        border: 1px solid rgba(212, 175, 55, 0.25);
        border-radius: 8px;
        padding: 4px 10px;
        font-size: 0.78rem;
        color: #D4AF37;
        margin-top: 6px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# 3. Session State Initialization
# ---------------------------------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "total_tokens_consumed" not in st.session_state:
    st.session_state.total_tokens_consumed = 0

if "prompt_tokens_consumed" not in st.session_state:
    st.session_state.prompt_tokens_consumed = 0

if "completion_tokens_consumed" not in st.session_state:
    st.session_state.completion_tokens_consumed = 0

if "message_metadata" not in st.session_state:
    st.session_state.message_metadata = []

# ---------------------------------------------------------
# 4. Sidebar Controls & Real-Time Token Analytics
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### 👑 Imperial Controls")
    
    model_name = st.selectbox(
        "Model Tier",
        ["gemini-2.5-flash", "gemini-2.5-pro"],
        index=0,
    )

    temperature = st.slider(
        "Creativity (Temperature)",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.05,
    )

    max_tokens = st.slider(
        "Max Response Tokens",
        min_value=128,
        max_value=4096,
        value=1024,
        step=128,
    )

    st.markdown("---")
    st.markdown("### 📊 Token Analytics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Prompt", f"{st.session_state.prompt_tokens_consumed:,}")
    with col2:
        st.metric("Output", f"{st.session_state.completion_tokens_consumed:,}")
    
    st.metric("Total Tokens Tracked", f"{st.session_state.total_tokens_consumed:,}")

    turn_count = len(st.session_state.chat_history) // 2
    st.caption(f"Retained Dialogs: **{turn_count}** turns")

    if st.button("🧹 Clear Chat & Metrics", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.message_metadata = []
        st.session_state.total_tokens_consumed = 0
        st.session_state.prompt_tokens_consumed = 0
        st.session_state.completion_tokens_consumed = 0
        st.rerun()

    st.markdown("---")
    st.caption(f"🛰️ LangSmith Trace: `{os.environ['LANGCHAIN_PROJECT']}`")

# ---------------------------------------------------------
# 5. Main Title & Interface
# ---------------------------------------------------------
st.markdown(
    """
    <div class="main-title-container">
        <div>
            <span class="royal-badge">MONITORED RUNTIME</span>
            <h1>Imperial Gemini Workspace</h1>
            <p style="color: #8C95A6; margin: 0; font-size: 0.95rem;">
                Stateful assistant backed by Google GenAI and full LangSmith telemetry traces.
            </p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# 6. LangChain Pipeline
# ---------------------------------------------------------
system_prompt_content = (
    "You are an elite, highly knowledgeable, and deeply creative AI companion. "
    "MANDATORY STYLE RULES:\n"
    "1. You MUST ALWAYS start every single response with the word 'broo' (or 'broo,' followed by an energetic opener).\n"
    "2. Enrich your responses with expressive, relevant emojis throughout the text.\n"
    "3. Maintain direct references to prior conversational context and continuity.\n"
    "4. Deliver answers that are insightful, structurally clean, and engagingly written."
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt_content),
        MessagesPlaceholder(variable_name="history"),
        ("user", "{question}"),
    ]
)

llm = ChatGoogleGenerativeAI(
    model=model_name,
    temperature=temperature,
    max_output_tokens=max_tokens,
)

# Pipe without StrOutputParser so AIMessageChunk metadata stays accessible
chain = prompt | llm

# ---------------------------------------------------------
# 7. Render Chat History with Attached Metadata
# ---------------------------------------------------------
ai_msg_idx = 0
for msg in st.session_state.chat_history:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user", avatar="👤"):
            st.markdown(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant", avatar="👑"):
            st.markdown(msg.content)
            # Display token breakdown badge if available
            if ai_msg_idx < len(st.session_state.message_metadata):
                meta = st.session_state.message_metadata[ai_msg_idx]
                if meta:
                    st.markdown(
                        f"""<div class="token-pill">
                            <span>In: <b>{meta.get('prompt', 0)}</b></span> |
                            <span>Out: <b>{meta.get('completion', 0)}</b></span> |
                            <span>Total: <b>{meta.get('total', 0)}</b></span>
                        </div>""",
                        unsafe_allow_html=True,
                    )
            ai_msg_idx += 1

# ---------------------------------------------------------
# 8. User Interaction, Streaming & Token Aggregation
# ---------------------------------------------------------
user_query = st.chat_input("Enter your message...")

if user_query:
    # Render user query
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_query)

    # Stream assistant response and gather usage chunks
    with st.chat_message("assistant", avatar="👑"):
        response_placeholder = st.empty()
        accumulated_text = ""
        prompt_tokens = 0
        completion_tokens = 0
        total_tokens = 0

        try:
            # LangSmith captures this execution via LANGCHAIN_TRACING_V2
            stream_gen = chain.stream(
                {
                    "question": user_query,
                    "history": st.session_state.chat_history,
                },
                config={"run_name": "RoyalGeminiTurn"},
            )

            for chunk in stream_gen:
                accumulated_text += chunk.content
                response_placeholder.markdown(accumulated_text + "▌")

                # Parse usage_metadata returned by ChatGoogleGenerativeAI
                if hasattr(chunk, "usage_metadata") and chunk.usage_metadata:
                    prompt_tokens = chunk.usage_metadata.get("input_tokens", prompt_tokens)
                    completion_tokens = chunk.usage_metadata.get("output_tokens", completion_tokens)
                    total_tokens = chunk.usage_metadata.get("total_tokens", total_tokens)

            # Finalize message render
            response_placeholder.markdown(accumulated_text)

            # Display individual message token card
            if total_tokens > 0:
                st.markdown(
                    f"""<div class="token-pill">
                        <span>In: <b>{prompt_tokens}</b></span> |
                        <span>Out: <b>{completion_tokens}</b></span> |
                        <span>Total: <b>{total_tokens}</b></span>
                    </div>""",
                    unsafe_allow_html=True,
                )

            # Update session-level aggregate metrics
            st.session_state.prompt_tokens_consumed += prompt_tokens
            st.session_state.completion_tokens_consumed += completion_tokens
            st.session_state.total_tokens_consumed += total_tokens

            # Save state
            st.session_state.chat_history.append(HumanMessage(content=user_query))
            st.session_state.chat_history.append(AIMessage(content=accumulated_text))
            st.session_state.message_metadata.append(
                {"prompt": prompt_tokens, "completion": completion_tokens, "total": total_tokens}
            )

        except Exception as exc:
            st.error(f"Runtime Exception: {str(exc)}")