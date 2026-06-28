"""
CalendarService — builds credentials on demand from user's stored refresh token.
"""
import asyncio
import logging
from datetime import datetime, timedelta
from typing import List

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from app.core.config import settings

logger = logging.getLogger("deskpilot")


def _build_credentials(user) -> Credentials:
    creds = Credentials(
        token=None,
        refresh_token=user.refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET,
    )
    creds.refresh(Request())
    return creds


class CalendarService:

    @staticmethod
    async def _service(user):
        creds = await asyncio.get_event_loop().run_in_executor(None, _build_credentials, user)
        return build("calendar", "v3", credentials=creds)

    @staticmethod
    async def get_events(user, days_ahead: int = 7) -> List[dict]:
        try:
            service = await CalendarService._service(user)
            now = datetime.utcnow().isoformat() + "Z"
            end = (datetime.utcnow() + timedelta(days=days_ahead)).isoformat() + "Z"
            events_result = service.events().list(
                calendarId="primary",
                timeMin=now,
                timeMax=end,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            ).execute()
            event_list = []
            for ev in events_result.get("items", []):
                start = ev["start"].get("dateTime", ev["start"].get("date"))
                end_t = ev["end"].get("dateTime", ev["end"].get("date"))
                event_list.append({
                    "id": ev["id"],
                    "title": ev.get("summary", "No Title"),
                    "start": start,
                    "end": end_t,
                    "description": ev.get("description", ""),
                    "location": ev.get("location", ""),
                })
            return event_list
        except Exception as exc:
            raise ValueError(f"Error fetching calendar events: {exc}")

    @staticmethod
    async def create_event(
        user,
        title: str,
        start_time: str,
        end_time: str,
        description: str = "",
        location: str = "",
    ) -> str:
        try:
            service = await CalendarService._service(user)
            event = {
                "summary": title,
                "description": description,
                "location": location,
                "start": {"dateTime": start_time},
                "end": {"dateTime": end_time},
            }
            created = service.events().insert(calendarId="primary", body=event).execute()
            return created["id"]
        except Exception as exc:
            raise ValueError(f"Error creating calendar event: {exc}")
