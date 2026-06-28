from datetime import datetime, timezone
from dateutil import parser as dateutil_parser
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials


def _build_service(creds_dict: dict):
    creds = Credentials(
        token=creds_dict["access_token"],
        refresh_token=creds_dict.get("refresh_token"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=creds_dict["client_id"],
        client_secret=creds_dict["client_secret"],
        scopes=["https://www.googleapis.com/auth/calendar"],
    )
    return build("calendar", "v3", credentials=creds)


def check_free_busy(service, start_iso: str, end_iso: str) -> str:
    try:
        body = {
            "timeMin": start_iso,
            "timeMax": end_iso,
            "items": [{"id": "primary"}],
        }
        result = service.freebusy().query(body=body).execute()
        busy = result.get("calendars", {}).get("primary", {}).get("busy", [])
        if not busy:
            return f"You are free between {start_iso} and {end_iso}."
        slots = "\n".join(f"  Busy: {b['start']} → {b['end']}" for b in busy)
        return f"Busy periods between {start_iso} and {end_iso}:\n{slots}"
    except Exception as e:
        return f"Calendar error: {e}"


def create_event(service, title: str, start_iso: str, end_iso: str,
                 description: str = "", attendees: list[str] | None = None) -> str:
    try:
        event = {
            "summary": title,
            "description": description,
            "start": {"dateTime": start_iso, "timeZone": "UTC"},
            "end": {"dateTime": end_iso, "timeZone": "UTC"},
        }
        if attendees:
            event["attendees"] = [{"email": a} for a in attendees]
        result = service.events().insert(calendarId="primary", body=event).execute()
        return f"Event '{title}' created. Link: {result.get('htmlLink', 'N/A')}"
    except Exception as e:
        return f"Calendar create error: {e}"


_current_service = None


def set_service(service):
    global _current_service
    _current_service = service


def check_free_busy_sync(start_iso: str, end_iso: str) -> str:
    if not _current_service:
        return "Calendar not connected. Please sign in with Google."
    return check_free_busy(_current_service, start_iso, end_iso)


def create_event_sync(title: str, start_iso: str, end_iso: str,
                      description: str = "", attendees: list[str] | None = None) -> str:
    if not _current_service:
        return "Calendar not connected. Please sign in with Google."
    return create_event(_current_service, title, start_iso, end_iso, description, attendees)
