"""Ingest text and PDF documents into a Qdrant collection."""

from __future__ import annotations

import re
import uuid
from pathlib import Path

import pypdf
from common import get_openai_client
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

PROJECT_DIR = Path(__file__).parent
DB_DIR = PROJECT_DIR / ".qdrant"
COLLECTION_NAME = "workshop_rag"


def embed_texts(texts: list[str]) -> list[list[float]]:
    client = get_openai_client()
    response = client.embeddings.create(model="text-embedding-3-small", input=texts)
    return [item.embedding for item in response.data]


def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def chunk_text(text: str, *, chunk_size: int = 500, overlap: int = 80) -> list[str]:
    if chunk_size <= overlap:
        raise ValueError("chunk_size must be larger than overlap")
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def load_text_file(path: Path) -> list[tuple[str, dict]]:
    text = clean_text(path.read_text(encoding="utf-8"))
    return [(text, {"source": path.name, "page": "text"})]


def load_pdf_file(path: Path) -> list[tuple[str, dict]]:
    pages = []
    with path.open("rb") as file:
        reader = pypdf.PdfReader(file)
        for index, page in enumerate(reader.pages, start=1):
            text = clean_text(page.extract_text() or "")
            if text:
                pages.append((text, {"source": path.name, "page": index}))
    return pages


def load_documents(directory: Path) -> list[tuple[str, dict]]:
    documents = []
    for path in sorted(directory.glob("*")):
        if path.suffix.lower() == ".txt":
            documents.extend(load_text_file(path))
        elif path.suffix.lower() == ".pdf":
            documents.extend(load_pdf_file(path))

    print(f"Loaded {len(documents)} documents from {directory}")
    return documents


def get_client() -> QdrantClient:
    # Use local file-based persistence (equivalent to ChromaDB's PersistentClient)
    return QdrantClient(path=str(DB_DIR))


def get_collection(qdrant: QdrantClient, dim: int, reset: bool = True):
    if reset and qdrant.collection_exists(COLLECTION_NAME):
        qdrant.delete_collection(COLLECTION_NAME)

    qdrant.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=dim, distance=Distance.COSINE),
    )


def ingest_directory(
    directory: Path, *, chunk_size: int = 500, overlap: int = 80
) -> int:
    records = []
    for text, metadata in load_documents(directory):
        chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)
        print(f" {chunks}")
        for chunk_index, chunk in enumerate(chunks):
            records.append(
                {
                    # Qdrant requires UUID or integer IDs, not arbitrary strings
                    "id": str(uuid.uuid4()),
                    "text": chunk,
                    "metadata": {
                        **metadata,
                        "chunk_index": chunk_index,
                        # Preserve the original string ID as a payload field for traceability
                        "original_id": f"{metadata['source']}:{metadata['page']}:{chunk_index}",
                    },
                }
            )

    if not records:
        raise ValueError(f"No .txt or .pdf documents found in {directory}")

    embeddings = embed_texts([record["text"] for record in records])
    dim = len(embeddings[0])

    qdrant = get_client()
    get_collection(qdrant, dim=dim, reset=True)

    points = [
        PointStruct(
            id=record["id"],
            vector=embeddings[i],
            payload={"text": record["text"], **record["metadata"]},
        )
        for i, record in enumerate(records)
    ]

    qdrant.upsert(collection_name=COLLECTION_NAME, points=points)
    return len(records)


def main():
    count = ingest_directory(PROJECT_DIR / "sample_docs")
    print(f"Ingested {count} chunks into {DB_DIR}")


if __name__ == "__main__":
    main()