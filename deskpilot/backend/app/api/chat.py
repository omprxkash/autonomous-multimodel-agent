import logging
import os
import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Depends, Header, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, AIMessage
from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User
from app.models.conversation import Conversation, ChatMessage
from app.models.memory import MemoryFact, MemoryEmbedding
from app.agent.graph import graph
from app.services import gmail as gmail_svc
from app.services import calendar as cal_svc
from app.services.memory_service import MemoryService

logger = logging.getLogger("deskpilot")
router = APIRouter(prefix="/chat", tags=["chat"])


class MessageRequest(BaseModel):
    message: str
    conversation_id: str | None = None


async def get_current_user(
    authorization: str = Header(""),
    db: AsyncSession = Depends(get_db),
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


@router.post("/message")
async def send_message(
    body: MessageRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if not body.message.strip():
        raise HTTPException(status_code=422, detail="Message cannot be empty")

    message = body.message[:4000]

    # --- resolve / create conversation ---
    new_conversation = False
    conv_id = body.conversation_id

    if conv_id:
        result = await db.execute(
            select(Conversation).where(Conversation.id == conv_id, Conversation.user_id == user.id)
        )
        if not result.scalar_one_or_none():
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        conv = Conversation(id=str(uuid.uuid4()), user_id=user.id, title="New Chat")
        db.add(conv)
        await db.flush()
        conv_id = conv.id
        new_conversation = True

    # --- load history ---
    msgs_result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.conversation_id == conv_id)
        .order_by(ChatMessage.created_at.asc())
    )
    history = [{"role": m.role, "content": m.content} for m in msgs_result.scalars().all()]
    history.append({"role": "user", "content": message})

    # --- save user message ---
    db.add(ChatMessage(conversation_id=conv_id, role="user", content=message))
    await db.flush()

    # --- build agent state ---
    _setup_google_services(user)
    memory_ctx = await MemoryService.get_memory_context(user.id, db)

    lc_messages = []
    for h in history:
        if h["role"] == "user":
            lc_messages.append(HumanMessage(content=h["content"]))
        elif h["role"] == "assistant":
            lc_messages.append(AIMessage(content=h["content"]))

    state = {
        "messages": lc_messages,
        "user_id": user.id,
        "conversation_id": conv_id,
        "memory_context": memory_ctx,
        "personalization": user.personalization or "Be helpful, clear, and concise.",
        "current_time": datetime.now(timezone.utc).isoformat(),
        "pending_draft": None,
        "tool_calls_made": 0,
        "db": db,
    }

    try:
        result_state = await graph.ainvoke(state)
    except Exception as exc:
        logger.error("Agent error: %s", exc)
        # Debug: list available models if model-not-found
        if "404" in str(exc) or "not found" in str(exc).lower():
            _debug_list_models()
        raise HTTPException(status_code=500, detail=f"Agent error: {exc}")

    ai_msgs = [m for m in result_state["messages"] if isinstance(m, AIMessage)]
    reply = ai_msgs[-1].content if ai_msgs else "I could not process that request."

    db.add(ChatMessage(conversation_id=conv_id, role="assistant", content=reply))

    # --- auto-generate title for new conversations ---
    generated_title: str | None = None
    if new_conversation:
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash",
                google_api_key=os.getenv("GEMINI_API_KEY"),
            )
            title_prompt = (
                f"Based on this message: '{message}', "
                "generate a short 3-4 word title for the conversation. "
                "Return ONLY the title, no quotes."
            )
            title_res = await llm.ainvoke(title_prompt)
            generated_title = title_res.content.strip()[:80]
            result = await db.execute(select(Conversation).where(Conversation.id == conv_id))
            conv_obj = result.scalar_one_or_none()
            if conv_obj and generated_title:
                conv_obj.title = generated_title
        except Exception as exc:
            logger.warning("Title generation failed: %s", exc)

    await db.commit()

    return {
        "conversation_id": conv_id,
        "reply": reply,
        "has_draft": "--- DRAFT START ---" in reply or "--- CALENDAR START ---" in reply,
        "title": generated_title,
    }


@router.get("/conversations")
async def list_conversations(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Conversation)
        .where(Conversation.user_id == user.id)
        .order_by(Conversation.updated_at.desc())
        .limit(30)
    )
    return [{"id": c.id, "title": c.title, "updated_at": c.updated_at} for c in result.scalars().all()]


@router.get("/conversations/{conv_id}/messages")
async def get_messages(
    conv_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Conversation).where(Conversation.id == conv_id, Conversation.user_id == user.id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Conversation not found")

    msgs = await db.execute(
        select(ChatMessage).where(ChatMessage.conversation_id == conv_id).order_by(ChatMessage.created_at)
    )
    return [{"role": m.role, "content": m.content, "created_at": m.created_at} for m in msgs.scalars()]


@router.get("/memories")
async def get_memories(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(MemoryFact)
        .where(MemoryFact.user_id == user.id)
        .order_by(MemoryFact.importance.desc())
        .limit(30)
    )
    return [
        {"id": f.id, "category": f.category, "content": f.fact, "importance": f.importance}
        for f in result.scalars().all()
    ]


@router.delete("/history/{user_id}")
async def clear_history(user_id: str, db: AsyncSession = Depends(get_db)):
    """Delete all chat messages and conversations for a user."""
    await db.execute(delete(ChatMessage).where(ChatMessage.conversation_id.in_(
        select(Conversation.id).where(Conversation.user_id == user_id).scalar_subquery()
    )))
    await db.execute(delete(Conversation).where(Conversation.user_id == user_id))
    await db.commit()
    return {"status": "success", "message": "Chat history cleared"}


@router.delete("/user/data/{user_id}")
async def wipe_user_data(user_id: str, db: AsyncSession = Depends(get_db)):
    """Wipe all data for a user — chats, conversations, non-profile memories."""
    # Delete chat messages
    await db.execute(delete(ChatMessage).where(ChatMessage.conversation_id.in_(
        select(Conversation.id).where(Conversation.user_id == user_id).scalar_subquery()
    )))
    await db.execute(delete(Conversation).where(Conversation.user_id == user_id))

    # Delete non-profile memory facts and their embeddings
    fact_ids_result = await db.execute(
        select(MemoryFact.id).where(
            MemoryFact.user_id == user_id,
            ~MemoryFact.category.in_(["personal", "preference"]),
        )
    )
    fact_ids = fact_ids_result.scalars().all()
    if fact_ids:
        await db.execute(delete(MemoryEmbedding).where(MemoryEmbedding.memory_fact_id.in_(fact_ids)))
        await db.execute(
            delete(MemoryFact).where(
                MemoryFact.user_id == user_id,
                ~MemoryFact.category.in_(["personal", "preference"]),
            )
        )
    await db.commit()
    return {"status": "success", "message": "User data wiped"}


def _setup_google_services(user: User):
    if not user.refresh_token:
        return
    from app.core.config import settings
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    creds = Credentials(
        token=None,
        refresh_token=user.refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET,
    )
    try:
        creds.refresh(Request())
    except Exception as exc:
        logger.warning("Token refresh failed: %s", exc)
        return
    from googleapiclient.discovery import build
    gmail_svc.set_service(build("gmail", "v1", credentials=creds))
    cal_svc.set_service(build("calendar", "v3", credentials=creds))


def _debug_list_models():
    try:
        import google.generativeai as genai
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            for m in genai.list_models():
                if "generateContent" in m.supported_generation_methods:
                    logger.info("Available model: %s", m.name)
    except Exception as exc:
        logger.warning("Could not list models: %s", exc)
