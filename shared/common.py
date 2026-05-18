"""Common utilities used by the daily workshop projects."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI


REPO_ROOT = Path(__file__).resolve().parents[1]


def load_workshop_env() -> None:
    """Load the repo-level .env file when present."""
    load_dotenv(REPO_ROOT / ".env")


def require_env(name: str) -> str:
    load_workshop_env()
    value = os.getenv(name)
    if not value:
        raise ValueError(f"{name} is not set. Add it to .env before running this.")
    return value


def get_openai_client() -> OpenAI:
    """Create an OpenAI-compatible client from .env settings."""
    load_workshop_env()
    return OpenAI(
        api_key=require_env("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL") or None,
    )


def get_chat_model(default: str = "gpt-4o-mini") -> str:
    load_workshop_env()
    return os.getenv("OPENAI_MODEL", default)


def get_embedding_model(default: str = "text-embedding-3-small") -> str:
    load_workshop_env()
    return os.getenv("OPENAI_EMBEDDING_MODEL", default)


def ask_model(prompt: str, *, max_output_tokens: int = 500) -> str:
    client = get_openai_client()
    response = client.responses.create(
        model=get_chat_model(),
        input=prompt,
        max_output_tokens=max_output_tokens,
    )
    return response.output_text


def ask_json(prompt: str, schema: dict[str, Any], *, name: str = "result") -> Any:
    client = get_openai_client()
    response = client.responses.create(
        model=get_chat_model(),
        instructions="Return only JSON that matches the provided schema.",
        input=prompt,
        text={
            "format": {
                "type": "json_schema",
                "name": name,
                "schema": schema,
                "strict": True,
            }
        },
    )
    return json.loads(response.output_text)


def embed_texts(texts: list[str]) -> list[list[float]]:
    client = get_openai_client()
    response = client.embeddings.create(model=get_embedding_model(), input=texts)
    return [item.embedding for item in response.data]
