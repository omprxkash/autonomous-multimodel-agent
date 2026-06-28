import logging
import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.services.gmail_service import GmailService
from app.services.calendar_service import CalendarService

logger = logging.getLogger("deskpilot")
router = APIRouter(tags=["integrations"])


async def _get_user(user_id: str, db: AsyncSession) -> User:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.refresh_token:
        raise HTTPException(status_code=400, detail="Google account not connected. Please sign in again.")
    return user


class EmailSendRequest(BaseModel):
    user_id: str
    to: str
    subject: str
    body: str
    thread_id: str | None = None


class EventCreateRequest(BaseModel):
    user_id: str
    title: str
    start_time: str
    end_time: str
    description: str = ""
    location: str = ""


class AnalyzeEmailRequest(BaseModel):
    user_id: str
    message_id: str
    question: str = "Summarize this email and any attachments"


# --- Gmail endpoints ---

@router.get("/gmail/inbox/{user_id}")
async def get_inbox(user_id: str, db: AsyncSession = Depends(get_db)):
    user = await _get_user(user_id, db)
    try:
        emails = await GmailService.get_inbox(user, db)
        return {"emails": emails}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/gmail/search/{user_id}")
async def search_inbox(user_id: str, q: str = "in:inbox", max_results: int = 10, db: AsyncSession = Depends(get_db)):
    user = await _get_user(user_id, db)
    try:
        emails = await GmailService.search_messages(user, q, max_results)
        return {"emails": emails}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/gmail/send")
async def send_email(req: EmailSendRequest, db: AsyncSession = Depends(get_db)):
    user = await _get_user(req.user_id, db)
    try:
        msg_id = await GmailService.send_email(user, req.to, req.subject, req.body, thread_id=req.thread_id)
        return {"message_id": msg_id, "status": "sent"}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/gmail/analyze")
async def analyze_email(req: AnalyzeEmailRequest, db: AsyncSession = Depends(get_db)):
    user = await _get_user(req.user_id, db)
    try:
        message = await GmailService.get_message_with_attachments(user, req.message_id)
        content = (
            f"Subject: {message['subject']}\n"
            f"From: {message['from']}\n"
            f"Date: {message['date']}\n\n"
            f"Body:\n{message['body']}\n"
        )
        for att in message.get("attachments", []):
            content += f"\n--- Attachment: {att['filename']} ---\n{att['text']}\n"
        content += f"\n\nQuestion: {req.question}"

        from langchain_google_genai import ChatGoogleGenerativeAI
        from langchain_core.messages import HumanMessage
        llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=os.getenv("GEMINI_API_KEY"))
        response = await llm.ainvoke([HumanMessage(content=content)])
        return {
            "message": {"subject": message["subject"], "from": message["from"], "date": message["date"]},
            "analysis": response.content,
        }
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


# --- Calendar endpoints ---

@router.get("/calendar/events/{user_id}")
async def get_events(user_id: str, days_ahead: int = 7, db: AsyncSession = Depends(get_db)):
    user = await _get_user(user_id, db)
    try:
        events = await CalendarService.get_events(user, days_ahead)
        return {"events": events}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/calendar/create")
async def create_event(req: EventCreateRequest, db: AsyncSession = Depends(get_db)):
    user = await _get_user(req.user_id, db)
    try:
        event_id = await CalendarService.create_event(
            user, req.title, req.start_time, req.end_time, req.description, req.location
        )
        return {"event_id": event_id, "status": "created"}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))
