"""
/api/email — AI-assisted email reply suggestions and direct send.
"""
import json
from typing import List, Optional

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User

router = APIRouter(prefix="/email", tags=["email"])


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


class EmailReplyRequest(BaseModel):
    email_from: str
    email_subject: str
    email_body: str
    email_id: Optional[str] = None


class EmailReplySuggestion(BaseModel):
    type: str  # "quick" | "standard" | "detailed"
    subject: str
    body: str


class EmailReplyResponse(BaseModel):
    suggestions: List[EmailReplySuggestion]


class SendEmailRequest(BaseModel):
    to: str
    subject: str
    body: str
    reply_to_message_id: Optional[str] = None


@router.post("/suggest-replies", response_model=EmailReplyResponse)
async def suggest_email_replies(
    request: EmailReplyRequest,
    user: User = Depends(get_current_user),
):
    """Generate three AI reply drafts for an incoming email (quick / standard / detailed)."""
    from app.agent.nodes import get_llm_plain
    from langchain_core.messages import HumanMessage

    prompt = f"""Draft 3 professional reply options for this email.

ORIGINAL EMAIL:
From: {request.email_from}
Subject: {request.email_subject}

{request.email_body}

Return JSON exactly:
{{
  "quick":    {{"subject": "Re: ...", "body": "..."}},
  "standard": {{"subject": "Re: ...", "body": "..."}},
  "detailed": {{"subject": "Re: ...", "body": "..."}}
}}

Rules: professional tone, address main points, natural language, no AI boilerplate."""

    try:
        llm = get_llm_plain()
        response = await llm.ainvoke([HumanMessage(content=prompt)])
        content = response.content.strip()
        # Strip markdown fences
        import re
        content = re.sub(r"^```(?:json)?\s*|\s*```$", "", content, flags=re.MULTILINE).strip()
        replies = json.loads(content)
        suggestions = [
            EmailReplySuggestion(type="quick", subject=replies["quick"]["subject"], body=replies["quick"]["body"]),
            EmailReplySuggestion(type="standard", subject=replies["standard"]["subject"], body=replies["standard"]["body"]),
            EmailReplySuggestion(type="detailed", subject=replies["detailed"]["subject"], body=replies["detailed"]["body"]),
        ]
        return EmailReplyResponse(suggestions=suggestions)
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=500, detail=f"Failed to parse LLM response: {exc}")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Reply generation failed: {exc}")


@router.post("/send")
async def send_email(
    request: SendEmailRequest,
    user: User = Depends(get_current_user),
):
    """Send an email via the user's connected Gmail account."""
    if not user.access_token_enc:
        raise HTTPException(status_code=400, detail="Gmail not connected")

    from app.services import gmail as gmail_service
    from app.core.config import settings

    creds = {
        "access_token": user.access_token_enc,
        "refresh_token": user.refresh_token_enc,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
    }
    svc = gmail_service._build_service(creds)
    gmail_service.set_service(svc)

    result = gmail_service.send_email(
        to=request.to,
        subject=request.subject,
        body=request.body,
        reply_to_message_id=request.reply_to_message_id,
    )

    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])

    return {"status": "sent", "to": request.to, "subject": request.subject}
