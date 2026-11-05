"""Streamlit interface for database-wide PostgreSQL RAG."""

from __future__ import annotations

import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import text
load_dotenv(override=True)

from rag_core import (
    DEFAULT_EMBEDDING_MODEL,
    build_database_url,
    create_chat_model,
    create_db_engine,
    create_embeddings,
    create_vector_store,
    stream_rag_answer,
    sync_database_to_vector_store,
)


load_dotenv()

DB_HOST = "quantamv.c7a8gmqscnvy.ap-northeast-1.rds.amazonaws.com"
DB_PORT = 5432
DB_NAME = "postgres"
DB_USER = "quantam"
CHAT_MODEL = "openai/gpt-oss-120b"

st.set_page_config(
    page_title="PostgreSQL RAG Assistant",
    page_icon="🧠",
    layout="wide",
)


@st.cache_resource(show_spinner=False)
def load_embedding_model():
    """Load and reuse the local embedding model for this app process."""
    return create_embeddings()


def connect_and_sync(password: str, groq_api_key: str) -> None:
    """Connect to PostgreSQL and index all eligible database tables."""
    groq_api_key = groq_api_key.strip()
    if not password:
        st.error("Enter the PostgreSQL password to connect.")
        return
    if not groq_api_key:
        st.error("Enter a valid Groq API key to connect.")
        return

    database_url = build_database_url(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        username=DB_USER,
        password=password,
    )

    with st.status(
        "Connecting and indexing database tables...",
        expanded=True,
    ) as status:
        progress = st.empty()
        progress.write("Checking PostgreSQL connection...")
        engine = create_db_engine(database_url)
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        progress.write(
            "Loading Hugging Face model (first run may download it)..."
        )
        embeddings = load_embedding_model()
        progress.write("Initializing pgvector...")
        vector_store = create_vector_store(
            connection=engine,
            embeddings=embeddings,
        )

        def report_progress(message: str) -> None:
            progress.write(message)

        progress.write("Scanning and indexing database tables...")
        stats = sync_database_to_vector_store(
            engine=engine,
            vector_store=vector_store,
            progress_callback=report_progress,
        )
        progress.write("Initializing Groq chat model...")
        llm = create_chat_model(
            provider="groq",
            api_key=groq_api_key,
            model=CHAT_MODEL,
            temperature=0,
        )
        status.update(
            label="Database indexing completed.",
            state="complete",
            expanded=False,
        )

    st.session_state.rag = {
        "engine": engine,
        "vector_store": vector_store,
        "llm": llm,
        "chat_model": CHAT_MODEL,
        "embedding_model": DEFAULT_EMBEDDING_MODEL,
        "top_k": 5,
    }
    st.session_state.sync_stats = stats


def render_sources(documents) -> None:
    """Show the database tables and rows that support an answer."""
    if not documents:
        return

    with st.expander(f"Retrieved Sources ({len(documents)} chunks)"):
        for index, document in enumerate(documents, start=1):
            metadata = document.metadata
            st.markdown(
                f"**[S{index}]** "
                f"Table: `{metadata.get('source_schema', 'unknown')}."
                f"{metadata.get('source_table', 'unknown')}` · "
                f"Record ID: `{metadata.get('source_pk', 'unknown')}`"
            )
            st.code(document.page_content, language="text")


def render_chat() -> None:
    """Render chat history and stream Groq RAG responses."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Ask a question about your PostgreSQL data...")
    if not question:
        return

    st.session_state.messages.append(
        {"role": "user", "content": question}
    )
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        try:
            rag = st.session_state.rag
            documents, token_stream = stream_rag_answer(
                question=question,
                vector_store=rag["vector_store"],
                llm=rag["llm"],
                top_k=rag["top_k"],
            )
            answer = st.write_stream(token_stream)
            render_sources(documents)
            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )
        except Exception as exc:
            st.error(f"Could not answer the question: {exc}")


def main() -> None:
    """Render the PostgreSQL RAG application."""
    st.title("🧠 PostgreSQL RAG Assistant")
    st.caption(
        "PostgreSQL | pgvector | Hugging Face Embeddings | Groq"
    )
    st.write(
        f"Database: `{DB_NAME}` on `{DB_HOST}:{DB_PORT}` "
        f"(user `{DB_USER}`)"
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    with st.form("database_connection"):
        password = st.text_input(
            "PostgreSQL password",
            type="password",
        )
        groq_api_key = st.text_input(
            "Groq API key",
            type="password",
        )
        submitted = st.form_submit_button(
            "Connect and index all tables",
            type="primary",
        )

    if submitted:
        try:
            connect_and_sync(password, groq_api_key)
        except Exception as exc:
            st.error(f"Connection or indexing failed: {exc}")

    if "sync_stats" in st.session_state:
        stats = st.session_state.sync_stats
        st.success("Database indexing completed.")
        st.caption(
            f"Tables indexed: {stats['indexed_tables']} · "
            f"Tables skipped (no indexable columns): "
            f"{stats['skipped_tables']}"
        )
        changed, unchanged, deleted = st.columns(3)
        changed.metric("Changed Rows", stats["changed_rows"])
        unchanged.metric("Unchanged Rows", stats["unchanged_rows"])
        deleted.metric("Deleted Rows", stats["deleted_rows"])

    if "rag" not in st.session_state:
        st.info(
            "Enter the PostgreSQL password and Groq API key, then connect "
            "to index all tables in the database."
        )
        return

    st.caption(
        f"Model: Groq `{CHAT_MODEL}` · "
        f"Embeddings: `{DEFAULT_EMBEDDING_MODEL}`"
    )
    render_chat()


if __name__ == "__main__":
    main()
