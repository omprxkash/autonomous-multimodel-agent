import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, AIMessage
from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User
from app.models.conversation import Conversation, ChatMessage
from app.models.memory import MemoryFact
from app.agent.graph import graph
from app.services import gmail as gmail_service
from app.services import calendar as calendar_service
from app.services.memory_service import retrieve_relevant_memories
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

router = APIRouter(prefix="/chat", tags=["chat"])


class MessageRequest(BaseModel):
    message: str
    conversation_id: str | None = None


async def get_current_user(authorization: str = Header(""), db: AsyncSession = Depends(get_db)) -> User:
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

    conv_id = body.conversation_id
    if not conv_id:
        conv = Conversation(id=str(uuid.uuid4()), user_id=user.id, title=message[:60])
        db.add(conv)
        await db.commit()
        conv_id = conv.id
    else:
        result = await db.execute(select(Conversation).where(
            Conversation.id == conv_id, Conversation.user_id == user.id
        ))
        if not result.scalar_one_or_none():
            raise HTTPException(status_code=404, detail="Conversation not found")

    user_msg = ChatMessage(
        conversation_id=conv_id, role="user", content=message
    )
    db.add(user_msg)
    await db.commit()

    _setup_google_services(user)
    memory_ctx = await retrieve_relevant_memories(user.id, message, db)

    state = {
        "messages": [HumanMessage(content=message)],
        "user_id": user.id,
        "conversation_id": conv_id,
        "memory_context": memory_ctx,
        "personalization": user.personalization,
        "current_time": datetime.now(timezone.utc).isoformat(),
        "pending_draft": None,
        "tool_calls_made": 0,
    }

    result_state = await graph.ainvoke(state)

    last_msg = result_state["messages"][-1]
    reply = last_msg.content if isinstance(last_msg, AIMessage) else str(last_msg)

    assistant_msg = ChatMessage(
        conversation_id=conv_id, role="assistant", content=reply
    )
    db.add(assistant_msg)
    await db.commit()

    return {
        "conversation_id": conv_id,
        "reply": reply,
        "has_draft": "--- DRAFT START ---" in reply or "--- EVENT DRAFT START ---" in reply,
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
    convs = result.scalars().all()
    return [{"id": c.id, "title": c.title, "updated_at": c.updated_at} for c in convs]


@router.get("/conversations/{conv_id}/messages")
async def get_messages(
    conv_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Conversation).where(
        Conversation.id == conv_id, Conversation.user_id == user.id
    ))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Conversation not found")

    msgs = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.conversation_id == conv_id)
        .order_by(ChatMessage.created_at)
    )
    return [{"role": m.role, "content": m.content, "created_at": m.created_at} for m in msgs.scalars()]


def _setup_google_services(user: User):
    if not user.access_token_enc:
        return
    creds_dict = {
        "access_token": user.access_token_enc,
        "refresh_token": user.refresh_token_enc,
        "client_id": "",
        "client_secret": "",
    }
    from app.core.config import settings
    creds_dict["client_id"] = settings.GOOGLE_CLIENT_ID
    creds_dict["client_secret"] = settings.GOOGLE_CLIENT_SECRET

    gmail_svc = gmail_service._build_service(creds_dict)
    calendar_svc = calendar_service._build_service(creds_dict)
    gmail_service.set_service(gmail_svc)
    calendar_service.set_service(calendar_svc)
