"""Streamlit UI for the Day 3 RAG assistant."""

import shutil
import sys
from pathlib import Path

import streamlit as st

# -----------------------------
# Path setup
# -----------------------------
sys.path.append(str(Path(__file__).resolve().parents[2]))
sys.path.append(str(Path(__file__).parent))

from ask import answer_question
from ingest import PROJECT_DIR, ingest_directory

# -----------------------------
# Upload directory
# -----------------------------
UPLOAD_DIR = PROJECT_DIR / "uploaded_docs"
UPLOAD_DIR.mkdir(exist_ok=True)

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="RAG Assistant",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 RAG Knowledge Base Assistant")

# -----------------------------
# Sidebar settings
# -----------------------------
with st.sidebar:

    st.header("Settings")

    uploaded_files = st.file_uploader(
        "Upload .txt or .pdf documents",
        type=["txt", "pdf"],
        accept_multiple_files=True,
    )

    chunk_size = st.number_input(
        "Chunk size",
        min_value=200,
        max_value=1500,
        value=500,
        step=100,
    )

    top_k = st.slider(
        "Retrieved chunks",
        min_value=1,
        max_value=5,
        value=3,
    )

    # -----------------------------
    # Ingest documents
    # -----------------------------
    if st.button("Ingest documents"):

        if uploaded_files:

            shutil.rmtree(UPLOAD_DIR, ignore_errors=True)
            UPLOAD_DIR.mkdir(exist_ok=True)

            for uploaded_file in uploaded_files:
                (UPLOAD_DIR / uploaded_file.name).write_bytes(
                    uploaded_file.getbuffer()
                )

            source_dir = UPLOAD_DIR

        else:
            source_dir = PROJECT_DIR / "sample_docs"

        with st.spinner("Ingesting documents..."):

            count = ingest_directory(
                source_dir,
                chunk_size=chunk_size,
            )

        st.success(f"Ingested {count} chunks")


# -----------------------------
# Chat session state
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []


# -----------------------------
# Display chat history
# -----------------------------
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        # Show sources if available
        if "sources" in message:

            with st.expander("Sources"):

                for source in message["sources"]:

                    st.markdown(
                        f"**{source.get('source', 'unknown')}** "
                        f"chunk `{source.get('chunk_index', '?')}`"
                    )

                    st.caption(source["text"])


# -----------------------------
# Chat input
# -----------------------------
prompt = st.chat_input(
    "Ask something about your documents..."
)

# -----------------------------
# Generate response
# -----------------------------
if prompt:

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    # Display user message
    with st.chat_message("user"):

        st.markdown(prompt)

    # Assistant response
    with st.chat_message("assistant"):

        with st.spinner("Retrieving and answering..."):

            result = answer_question(
                prompt,
                top_k=top_k,
            )

            answer = result["answer"]

            st.markdown(answer)

            # Show sources
            with st.expander("Sources"):

                for source in result["sources"]:

                    st.markdown(
                        f"**{source.get('source', 'unknown')}** "
                        f"chunk `{source.get('chunk_index', '?')}`"
                    )

                    st.caption(source["text"])

    # Save assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "sources": result["sources"],
        }
    )