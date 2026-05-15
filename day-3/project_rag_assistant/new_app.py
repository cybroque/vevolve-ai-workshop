"""Simple conversational RAG Streamlit app."""

import shutil
import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[2]))
sys.path.append(str(Path(__file__).parent))

from new_ask import answer_question
from ingest import PROJECT_DIR, ingest_directory


UPLOAD_DIR = PROJECT_DIR / "uploaded_docs"
UPLOAD_DIR.mkdir(exist_ok=True)
st.set_page_config(page_title="RAG Chatbot")
st.title("RAG Chat Assistant")
if "messages" not in st.session_state:
    st.session_state.messages = []
with st.sidebar:
    st.header("Settings")
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
    uploaded_files = st.file_uploader(
        "Upload .txt or .pdf documents",
        type=["txt", "pdf"],
        accept_multiple_files=True,
    )
    if st.button("Ingest documents"):
        if uploaded_files:
            shutil.rmtree(UPLOAD_DIR, ignore_errors=True)
            UPLOAD_DIR.mkdir(exist_ok=True)
            for uploaded_file in uploaded_files:
                (
                    UPLOAD_DIR / uploaded_file.name
                ).write_bytes(uploaded_file.getbuffer())
            source_dir = UPLOAD_DIR
        else:
            source_dir = PROJECT_DIR / "sample_docs"
        with st.spinner("Ingesting documents..."):
            count = ingest_directory(
                source_dir,
                chunk_size=chunk_size,
            )
        st.success(f"Ingested {count} chunks")
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
user_input = st.chat_input("Ask a question")
if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = answer_question(
                user_input,
                st.session_state.messages,
                top_k=top_k,
            )
            answer = result["answer"]
            st.markdown(answer)
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )