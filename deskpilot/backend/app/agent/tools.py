from langchain_core.tools import tool
from typing import Optional


@tool
def gmail_search(query: str, max_results: int = 10) -> str:
    """Search Gmail for emails matching the query. Returns a list of email summaries."""
    from app.services.gmail import search_emails_sync
    return search_emails_sync(query, max_results)


@tool
def gmail_read(message_id: str) -> str:
    """Read the full content of a Gmail message by its ID."""
    from app.services.gmail import read_email_sync
    return read_email_sync(message_id)


@tool
def gmail_draft(to: str, subject: str, body: str, thread_id: Optional[str] = None) -> str:
    """
    Draft an email. Returns a structured draft block for user review.
    The email is NOT sent until the user confirms.
    Format: --- DRAFT START --- ... --- DRAFT END ---
    """
    draft = {
        "type": "email_draft",
        "to": to,
        "subject": subject,
        "body": body,
        "thread_id": thread_id,
    }
    return (
        f"--- DRAFT START ---\n"
        f"TO: {to}\n"
        f"SUBJECT: {subject}\n"
        f"THREAD: {thread_id or 'new'}\n\n"
        f"{body}\n"
        f"--- DRAFT END ---\n"
        f"Please review the draft above. Reply 'send' to send or 'cancel' to discard."
    )


@tool
def gmail_send(to: str, subject: str, body: str, thread_id: Optional[str] = None) -> str:
    """Send an email. Only call this after the user has explicitly confirmed a draft."""
    from app.services.gmail import send_email_sync
    return send_email_sync(to, subject, body, thread_id)


@tool
def calendar_free_busy(start_time: str, end_time: str) -> str:
    """Check calendar free/busy status between start_time and end_time (ISO 8601)."""
    from app.services.calendar import check_free_busy_sync
    return check_free_busy_sync(start_time, end_time)


@tool
def calendar_create_event(
    title: str,
    start_time: str,
    end_time: str,
    description: Optional[str] = None,
    attendees: Optional[list[str]] = None,
) -> str:
    """
    Create a calendar event. Returns a structured draft for user confirmation.
    The event is NOT created until the user confirms.
    """
    attendee_str = ", ".join(attendees or [])
    return (
        f"--- EVENT DRAFT START ---\n"
        f"TITLE: {title}\n"
        f"START: {start_time}\n"
        f"END: {end_time}\n"
        f"DESCRIPTION: {description or ''}\n"
        f"ATTENDEES: {attendee_str or 'none'}\n"
        f"--- EVENT DRAFT END ---\n"
        f"Reply 'confirm' to create this event or 'cancel' to discard."
    )


@tool
def save_memory(content: str, category: str = "preference", importance: float = 0.5) -> str:
    """
    Save a fact to long-term memory.
    category: preference | habit | project | contact
    importance: 0.0 to 1.0 (profile facts use 1.0)
    """
    return f"[Memory saved: {category}] {content}"


ALL_TOOLS = [gmail_search, gmail_read, gmail_draft, gmail_send, calendar_free_busy, calendar_create_event, save_memory]
