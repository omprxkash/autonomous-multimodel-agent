from typing import Any
import google.generativeai as genai
from app.core.config import settings

_configured = False


def _ensure_configured():
    global _configured
    if not _configured:
        genai.configure(api_key=settings.GEMINI_API_KEY)
        _configured = True


async def embed_text(text: str) -> list[float]:
    _ensure_configured()
    result = genai.embed_content(
        model="models/embedding-001",
        content=text,
        task_type="retrieval_document",
    )
    return result["embedding"]


async def embed_query(text: str) -> list[float]:
    _ensure_configured()
    result = genai.embed_content(
        model="models/embedding-001",
        content=text,
        task_type="retrieval_query",
    )
    return result["embedding"]
