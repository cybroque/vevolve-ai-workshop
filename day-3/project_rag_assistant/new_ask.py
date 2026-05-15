"""Conversational RAG assistant."""

from __future__ import annotations

from common import get_openai_client
from ingest import COLLECTION_NAME, DB_DIR
from qdrant_client import QdrantClient


client = get_openai_client()


def embed_texts(texts: list[str]) -> list[list[float]]:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts,
    )
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
        {
            "text": hit.payload.get("text", ""),
            **{
                k: v
                for k, v in hit.payload.items()
                if k != "text"
            },
        }
        for hit in results.points
    ]


def answer_question(
    question: str,
    messages: list[dict],
    *,
    top_k: int = 3,
) -> dict:
    chunks = retrieve(question, top_k=top_k)
    context = "\n\n".join(
        f"Source: {chunk['source']} chunk {chunk['chunk_index']}\n{chunk['text']}"
        for chunk in chunks
    )
    system_prompt = f"""
You are a helpful conversational RAG assistant.
Use the retrieved context to answer the user.
If the answer exists in the context,
answer clearly and naturally.
If the answer does not exist,
say:
"I do not have enough information."
Retrieved Context:
{context}
"""
    conversation = [
        {
            "role": "system",
            "content": system_prompt,
        }
    ]
    conversation.extend(messages)
    conversation.append(
        {
            "role": "user",
            "content": question,
        }
    )
    response = client.responses.create(
        model="gpt-5.4-nano",
        input=conversation,
        max_output_tokens=500,
        temperature=0.7,
    )
    assistant_response = response.output_text
    return {
        "answer": assistant_response,
        "sources": chunks,
    }


def main():
    messages = []
    print("RAG Chatbot Started (type 'exit' to quit)")
    while True:
        question = input("You: ")
        if question.lower() == "exit":
            break
        result = answer_question(
            question,
            messages,
            top_k=3,
        )
        print("Bot:", result["answer"])
        messages.append(
            {
                "role": "user",
                "content": question,
            }
        )
        messages.append(
            {
                "role": "assistant",
                "content": result["answer"],
            }
        )
if __name__ == "__main__":
    main()