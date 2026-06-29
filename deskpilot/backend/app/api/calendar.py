"""
/api/calendar — create events and list upcoming events via Google Calendar.
"""
from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User

router = APIRouter(prefix="/calendar", tags=["calendar"])


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


class CreateEventRequest(BaseModel):
    summary: str
    start_time: str   # ISO 8601: YYYY-MM-DDTHH:MM:SS
    end_time: str
    location: Optional[str] = ""
    description: Optional[str] = ""
    attendees: Optional[str] = ""  # comma-separated email addresses


def _get_calendar_service(user: User):
    if not user.access_token_enc:
        raise HTTPException(status_code=400, detail="Google Calendar not connected")
    from app.services import calendar as calendar_service
    from app.core.config import settings

    creds = {
        "access_token": user.access_token_enc,
        "refresh_token": user.refresh_token_enc,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
    }
    svc = calendar_service._build_service(creds)
    calendar_service.set_service(svc)
    return calendar_service


@router.post("/create")
async def create_event(
    request: CreateEventRequest,
    user: User = Depends(get_current_user),
):
    """Create a calendar event after user confirms a draft proposal."""
    cal = _get_calendar_service(user)
    result = cal.create_event(
        summary=request.summary,
        start=request.start_time,
        end=request.end_time,
        location=request.location,
        description=request.description,
        attendees=[a.strip() for a in (request.attendees or "").split(",") if a.strip()],
    )
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return {
        "status": "created",
        "summary": request.summary,
        "start": request.start_time,
        "end": request.end_time,
    }


@router.get("/events")
async def get_events(
    days: int = 7,
    user: User = Depends(get_current_user),
):
    """Return upcoming calendar events for the next N days."""
    cal = _get_calendar_service(user)
    events = cal.get_upcoming_events(days=days)
    if isinstance(events, dict) and "error" in events:
        raise HTTPException(status_code=500, detail=events["error"])
    return events
