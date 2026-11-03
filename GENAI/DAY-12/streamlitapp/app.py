"""
Streamlit UI for the multimodal RAG backend (multimodal_rag.py).

Run:  streamlit run app.py
"""

import streamlit as st

import multimodal_rag as backend

st.set_page_config(page_title="Multimodal RAG", page_icon="🖼️", layout="wide")


# cache_resource: CLIP, FAISS indexes and the images are heavy; load them ONCE per server
# process instead of on every Streamlit rerun (which happens on every widget interaction).
@st.cache_resource(show_spinner="Loading models and indexes (first run builds the index)...")
def load_rag(rebuild: bool = False) -> backend.MultimodalRAG:
    return backend.MultimodalRAG(rebuild=rebuild)


st.title("🖼️ Multimodal RAG")
st.caption("Text + image retrieval (OpenAI text embeddings, CLIP, image captions, RRF fusion) "
           "answered by a vision LLM with citations.")

with st.sidebar:
    st.header("Settings")
    k_text = st.slider("Text passages (k)", 1, 10, 5)
    k_image = st.slider("Images (k)", 0, 6, 3)
    st.markdown(f"**Answer model:** `{backend.VISION_LLM}`  \n"
                f"**Text embedder:** `{backend.TEXT_EMBED_MODEL}`  \n"
                f"**Image encoder:** `{backend.CLIP_MODEL_NAME}`")
    if st.button("Rebuild index", help="Re-ingest data/ and re-caption images (uses API calls)"):
        st.cache_resource.clear()
        load_rag(rebuild=True)
        st.success("Index rebuilt")

rag = load_rag()

# Session state keeps the chat history across reruns.
if "history" not in st.session_state:
    st.session_state.history = []


def render_sources(docs) -> None:
    """Show exactly what the LLM saw, so answers are verifiable."""
    texts = [d for d in docs if d.metadata["type"] == "text"]
    images = [d for d in docs if d.metadata["type"] == "image"]

    if images:
        st.markdown("**Retrieved images**")
        cols = st.columns(len(images))
        for col, doc in zip(cols, images):
            meta = doc.metadata
            with col:
                st.image(rag.index.images[meta["image_id"]],
                         caption=f"{meta['source']}" + (f" p.{meta['page']}" if meta.get("page") else ""))
                with st.expander("Caption used for search"):
                    st.write(doc.page_content)
    if texts:
        st.markdown("**Retrieved text**")
        for n, doc in enumerate(texts, 1):
            meta = doc.metadata
            page = f", page {meta['page']}" if meta.get("page") else ""
            with st.expander(f"[T{n}] {meta['source']}{page}"):
                st.write(doc.page_content)


for turn in st.session_state.history:
    with st.chat_message("user"):
        st.write(turn["question"])
    with st.chat_message("assistant"):
        st.markdown(turn["answer"])
        with st.expander("Sources"):
            render_sources(turn["docs"])

if question := st.chat_input("Ask about your documents, charts or diagrams..."):
    with st.chat_message("user"):
        st.write(question)
    with st.chat_message("assistant"):
        with st.spinner("Retrieving and reasoning..."):
            try:
                result = rag.ask(question, k_text=k_text, k_image=k_image)
            except Exception as err:  # surface API/key errors in the UI instead of a stack trace
                st.error(f"Request failed: {err}")
                st.stop()
        st.markdown(result["answer"])
        with st.expander("Sources", expanded=True):
            render_sources(result["docs"])
    st.session_state.history.append(
        {"question": question, "answer": result["answer"], "docs": result["docs"]})
