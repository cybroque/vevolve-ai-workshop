"""Ask questions against the Day 3 RAG knowledge base."""

from __future__ import annotations

from common import get_openai_client, ask_model
from ingest import COLLECTION_NAME, DB_DIR
from qdrant_client import QdrantClient


def embed_texts(texts: list[str]) -> list[list[float]]:
    client = get_openai_client()
    response = client.embeddings.create(model="text-embedding-3-small", input=texts)
    return [item.embedding for item in response.data]


def get_client() -> QdrantClient:
    return QdrantClient(path=str(DB_DIR))


def retrieve(question: str, *, top_k: int = 3) -> list[dict]:
    question_embedding = embed_texts([question])[0]
    results = get_client().query_points(
        collection_name=COLLECTION_NAME,
        query=question_embedding,
        limit=top_k,
    )
    return [
        {"text": hit.payload.get("text", ""), **{k: v for k, v in hit.payload.items() if k != "text"}}
        for hit in results.points
    ]


def format_chat_history(history: list[dict]) -> str:
    """Format chat history for the prompt."""
    if not history:
        return "No previous conversation."

    formatted = []
    for msg in history[-6:]:  # Keep last 6 messages (3 turns) for context
        role = "User" if msg["role"] == "user" else "Assistant"
        formatted.append(f"{role}: {msg['content']}")
    return "\n".join(formatted)


def answer_question(
    question: str,
    *,
    top_k: int = 3,
    chat_history: list[dict] | None = None
) -> dict:
    """Answer a question with optional chat history for context."""
    chunks = retrieve(question, top_k=top_k)

    context = "\n\n".join(
        f"Source: {chunk['source']} chunk {chunk['chunk_index']}\n{chunk['text']}"
        for chunk in chunks
    )

    history_text = format_chat_history(chat_history or [])

    prompt = f"""You are a helpful assistant answering questions based on a knowledge base.
Use the retrieved context to answer questions. If the context doesn't contain enough 
information, say so clearly. You can reference previous conversation when relevant.

## Conversation History:
{history_text}

## Retrieved Context:
{context}

## Current Question:
{question}

Answer the question conversationally. If you use information from the context, 
mention the source briefly at the end."""

    return {"answer": ask_model(prompt, max_output_tokens=600), "sources": chunks}


def main():
    question = "Why is metadata useful in a RAG system?"
    result = answer_question(question)
    print(result["answer"])
    print("\nRetrieved chunks:")
    for source in result["sources"]:
        print(f"- {source['source']} chunk {source['chunk_index']}")


if __name__ == "__main__":
    main()