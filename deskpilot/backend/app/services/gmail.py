import base64
import re
from typing import Any
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials


def _build_service(creds_dict: dict):
    creds = Credentials(
        token=creds_dict["access_token"],
        refresh_token=creds_dict.get("refresh_token"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=creds_dict["client_id"],
        client_secret=creds_dict["client_secret"],
        scopes=["https://www.googleapis.com/auth/gmail.modify"],
    )
    return build("gmail", "v1", credentials=creds)


def search_emails(service, query: str, max_results: int = 10) -> str:
    try:
        results = service.users().messages().list(
            userId="me", q=query, maxResults=max_results
        ).execute()
        messages = results.get("messages", [])
        if not messages:
            return "No emails found matching that query."

        summaries = []
        for msg in messages[:5]:
            detail = service.users().messages().get(
                userId="me", id=msg["id"], format="metadata",
                metadataHeaders=["Subject", "From", "Date"]
            ).execute()
            headers = {h["name"]: h["value"] for h in detail.get("payload", {}).get("headers", [])}
            summaries.append(
                f"ID: {msg['id']} | From: {headers.get('From', '?')} | "
                f"Subject: {headers.get('Subject', '(no subject)')} | Date: {headers.get('Date', '?')}"
            )
        return "\n".join(summaries)
    except Exception as e:
        return f"Gmail search error: {e}"


def read_email(service, message_id: str) -> str:
    try:
        msg = service.users().messages().get(
            userId="me", id=message_id, format="full"
        ).execute()
        headers = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}
        body = _extract_body(msg.get("payload", {}))
        return (
            f"From: {headers.get('From', '?')}\n"
            f"Subject: {headers.get('Subject', '?')}\n"
            f"Date: {headers.get('Date', '?')}\n\n"
            f"{body[:3000]}"
        )
    except Exception as e:
        return f"Gmail read error: {e}"


def send_email(service, to: str, subject: str, body: str, thread_id: str | None = None) -> str:
    try:
        raw = base64.urlsafe_b64encode(
            f"To: {to}\r\nSubject: {subject}\r\n\r\n{body}".encode()
        ).decode()
        msg_body: dict[str, Any] = {"raw": raw}
        if thread_id:
            msg_body["threadId"] = thread_id
        service.users().messages().send(userId="me", body=msg_body).execute()
        return f"Email sent to {to} with subject '{subject}'."
    except Exception as e:
        return f"Gmail send error: {e}"


def _extract_body(payload: dict) -> str:
    if payload.get("body", {}).get("data"):
        return base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8", errors="replace")
    for part in payload.get("parts", []):
        if part.get("mimeType") in ("text/plain", "text/html"):
            data = part.get("body", {}).get("data", "")
            if data:
                text = base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")
                if part["mimeType"] == "text/html":
                    text = re.sub(r"<[^>]+>", " ", text)
                return text
    return "(no body)"


# Sync wrappers for tool use (tools are called synchronously by LangGraph)
_current_service = None


def set_service(service):
    global _current_service
    _current_service = service


def search_emails_sync(query: str, max_results: int = 10) -> str:
    if not _current_service:
        return "Gmail not connected. Please sign in with Google."
    return search_emails(_current_service, query, max_results)


def read_email_sync(message_id: str) -> str:
    if not _current_service:
        return "Gmail not connected. Please sign in with Google."
    return read_email(_current_service, message_id)


def send_email_sync(to: str, subject: str, body: str, thread_id: str | None = None) -> str:
    if not _current_service:
        return "Gmail not connected. Please sign in with Google."
    return send_email(_current_service, to, subject, body, thread_id)
