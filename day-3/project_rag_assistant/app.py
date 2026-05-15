"""Streamlit UI for the Day 3 RAG chatbot."""

import shutil
import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[2]))
sys.path.append(str(Path(__file__).parent))

from ask import answer_question
from ingest import PROJECT_DIR, ingest_directory

UPLOAD_DIR = PROJECT_DIR / "uploaded_docs"
UPLOAD_DIR.mkdir(exist_ok=True)

st.set_page_config(page_title="RAG Chatbot", page_icon="💬")
st.title("💬 RAG Knowledge Base Chatbot")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "sources_history" not in st.session_state:
    st.session_state.sources_history = []

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")

    uploaded_files = st.file_uploader(
        "Upload .txt or .pdf documents",
        type=["txt", "pdf"],
        accept_multiple_files=True,
    )

    chunk_size = st.number_input(
        "Chunk size", min_value=200, max_value=1500, value=500, step=100
    )

    top_k = st.slider("Retrieved chunks", min_value=1, max_value=5, value=3)

    if st.button("📥 Ingest Documents", use_container_width=True):
        if uploaded_files:
            shutil.rmtree(UPLOAD_DIR, ignore_errors=True)
            UPLOAD_DIR.mkdir(exist_ok=True)
            for uploaded_file in uploaded_files:
                (UPLOAD_DIR / uploaded_file.name).write_bytes(uploaded_file.getbuffer())
            source_dir = UPLOAD_DIR
        else:
            source_dir = PROJECT_DIR / "sample_docs"

        with st.spinner("Ingesting documents..."):
            count = ingest_directory(source_dir, chunk_size=chunk_size)
        st.success(f"✅ Ingested {count} chunks")

    st.divider()

    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.session_state.sources_history = []
        st.rerun()

    # Show sources toggle
    show_sources = st.checkbox("Show retrieved sources", value=False)

# Display chat history
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        # Show sources for assistant messages if enabled
        if show_sources and message["role"] == "assistant":
            if i // 2 < len(st.session_state.sources_history):
                sources = st.session_state.sources_history[i // 2]
                if sources:
                    with st.expander("📚 Sources"):
                        for source in sources:
                            st.markdown(f"**{source['source']}** chunk `{source['chunk_index']}`")
                            st.caption(source["text"][:200] + "..." if len(source["text"]) > 200 else source["text"])

# Chat input
if prompt := st.chat_input("Ask a question about your documents..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = answer_question(
                prompt,
                top_k=top_k,
                chat_history=st.session_state.messages[:-1]  # Exclude current message
            )

        st.markdown(result["answer"])

        # Store sources
        st.session_state.sources_history.append(result["sources"])

        # Show sources inline if enabled
        if show_sources and result["sources"]:
            with st.expander("📚 Sources"):
                for source in result["sources"]:
                    st.markdown(f"**{source['source']}** chunk `{source['chunk_index']}`")
                    st.caption(source["text"][:200] + "..." if len(source["text"]) > 200 else source["text"])

    # Add assistant message to history
    st.session_state.messages.append({"role": "assistant", "content": result["answer"]})