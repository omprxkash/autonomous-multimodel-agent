"""
SSE streaming chat endpoint.
Runs the agent graph and streams the response word-by-word as Server-Sent Events.
"""
import asyncio
import json
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Depends, Header
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from langchain_core.messages import HumanMessage

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User
from app.models.conversation import Conversation, ChatMessage
from app.agent.graph import graph
from app.services import gmail as gmail_service
from app.services import calendar as calendar_service
from app.services.memory_service import retrieve_relevant_memories

router = APIRouter(prefix="/stream", tags=["stream"])


class StreamRequest(BaseModel):
    message: str
    conversation_id: str | None = None


async def get_current_user(
    authorization: str = Header(""), db: AsyncSession = Depends(get_db)
) -> User:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    try:
        user_id = decode_access_token(authorization[7:])
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def _sse(data: dict) -> str:
    return f"data: {json.dumps(data)}\n\n"


async def _stream_agent(body: StreamRequest, user: User, db: AsyncSession):
    """Run the graph and yield SSE events."""
    message = body.message[:4000].strip()
    if not message:
        yield _sse({"type": "error", "content": "Empty message"})
        return

    # Resolve or create conversation
    conv_id = body.conversation_id
    if not conv_id:
        conv = Conversation(id=str(uuid.uuid4()), user_id=user.id, title=message[:60])
        db.add(conv)
        await db.commit()
        conv_id = conv.id
    else:
        result = await db.execute(
            select(Conversation).where(
                Conversation.id == conv_id,
                Conversation.user_id == user.id,
            )
        )
        if not result.scalar_one_or_none():
            yield _sse({"type": "error", "content": "Conversation not found"})
            return

    yield _sse({"type": "start", "conversation_id": conv_id})

    # Persist user message
    db.add(ChatMessage(conversation_id=conv_id, role="user", content=message))
    await db.commit()

    # Set up Google services
    if user.access_token_enc:
        creds = {
            "access_token": user.access_token_enc,
            "refresh_token": user.refresh_token_enc,
            "client_id": "",
            "client_secret": "",
        }
        from app.core.config import settings
        creds["client_id"] = settings.GOOGLE_CLIENT_ID
        creds["client_secret"] = settings.GOOGLE_CLIENT_SECRET
        gmail_service.set_service(gmail_service._build_service(creds))
        calendar_service.set_service(calendar_service._build_service(creds))

    memory_ctx = await retrieve_relevant_memories(user.id, message, db)

    state = {
        "messages": [HumanMessage(content=message)],
        "user_id": user.id,
        "conversation_id": conv_id,
        "session_id": str(uuid.uuid4()),
        "memory_context": memory_ctx,
        "personalization": getattr(user, "personalization", "Be helpful and concise."),
        "current_time": datetime.now(timezone.utc).isoformat(),
        "intent": None,
        "needs_tools": False,
        "retrieved_memories": [],
        "user_preferences": {},
        "tool_calls_made": 0,
        "pending_draft": None,
        "new_memories": [],
        "response": None,
    }

    # Run the graph (non-streaming at graph level; we stream the reply word-by-word)
    try:
        result_state = await graph.ainvoke(state)
    except Exception as exc:
        yield _sse({"type": "error", "content": str(exc)})
        return

    reply = result_state.get("response") or ""
    if not reply:
        from langchain_core.messages import AIMessage
        for msg in reversed(result_state.get("messages", [])):
            if isinstance(msg, AIMessage) and msg.content:
                reply = msg.content
                break

    # Stream reply word-by-word
    words = reply.split(" ")
    for i, word in enumerate(words):
        chunk = word if i == len(words) - 1 else word + " "
        yield _sse({"type": "chunk", "content": chunk})
        await asyncio.sleep(0.01)  # slight delay for perceived streaming

    # Persist assistant message
    db.add(ChatMessage(conversation_id=conv_id, role="assistant", content=reply))
    await db.commit()

    has_draft = (
        "***EMAIL_DRAFT***" in reply
        or "***EVENT_PROPOSAL***" in reply
        or "--- DRAFT START ---" in reply
    )
    yield _sse({"type": "done", "has_draft": has_draft, "conversation_id": conv_id})


@router.post("/chat")
async def stream_chat(
    body: StreamRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Stream agent response as Server-Sent Events."""
    return StreamingResponse(
        _stream_agent(body, user, db),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
