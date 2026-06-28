"""
GmailService — builds credentials on demand from the user's stored refresh token.
Used by integrations.py endpoints and the agent tools.
"""
import base64
import io
import logging
import os
import re
from email.mime.text import MIMEText
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


class GmailService:

    @staticmethod
    async def _service(user):
        import asyncio
        creds = await asyncio.get_event_loop().run_in_executor(None, _build_credentials, user)
        return build("gmail", "v1", credentials=creds)

    @staticmethod
    async def get_inbox(user, db=None, max_results: int = 10) -> List[dict]:
        return await GmailService.search_messages(user, "in:inbox", max_results)

    @staticmethod
    async def search_messages(user, query: str = "in:inbox", max_results: int = 10) -> List[dict]:
        try:
            service = await GmailService._service(user)
            results = service.users().messages().list(
                userId="me", maxResults=max_results, q=query
            ).execute()
            messages = results.get("messages", [])
            email_list = []
            for msg in messages:
                msg_data = service.users().messages().get(
                    userId="me", id=msg["id"], format="full"
                ).execute()
                headers = {h["name"]: h["value"] for h in msg_data["payload"]["headers"]}
                body = _extract_body(msg_data["payload"])
                email_list.append({
                    "id": msg["id"],
                    "thread_id": msg["threadId"],
                    "subject": headers.get("Subject", "(no subject)"),
                    "from": headers.get("From", "Unknown"),
                    "to": headers.get("To", "Unknown"),
                    "date": headers.get("Date", ""),
                    "preview": body[:300] + ("..." if len(body) > 300 else ""),
                })
            return email_list
        except Exception as exc:
            raise ValueError(f"Error searching messages: {exc}")

    @staticmethod
    async def send_email(user, to: str, subject: str, body: str, thread_id: str | None = None) -> str:
        try:
            service = await GmailService._service(user)

            # Extract bare email address from "Name <email>" format
            email_match = re.search(r"[\w.\-+]+@[\w.\-]+\.\w+", to)
            clean_to = email_match.group(0) if email_match else to.strip()

            message = MIMEText(body)
            message["to"] = clean_to
            message["subject"] = subject

            # Handle threading — set In-Reply-To and References headers
            if thread_id:
                try:
                    orig = service.users().messages().get(userId="me", id=thread_id).execute()
                    orig_headers = {h["name"].lower(): h["value"] for h in orig["payload"]["headers"]}
                    msg_id_val = orig_headers.get("message-id")
                    if msg_id_val:
                        message["In-Reply-To"] = msg_id_val
                        message["References"] = msg_id_val
                    if not subject.lower().startswith("re:"):
                        message["subject"] = "Re: " + subject
                except Exception as exc:
                    logger.warning("Threading header error (proceeding as new mail): %s", exc)

            raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
            send_body: dict = {"raw": raw}
            if thread_id:
                send_body["threadId"] = thread_id

            result = service.users().messages().send(userId="me", body=send_body).execute()
            return result["id"]
        except Exception as exc:
            raise ValueError(f"Error sending email: {exc}")

    @staticmethod
    async def get_message_with_attachments(user, message_id: str) -> dict:
        try:
            service = await GmailService._service(user)
            msg_data = service.users().messages().get(
                userId="me", id=message_id, format="full"
            ).execute()
            headers = {h["name"]: h["value"] for h in msg_data["payload"]["headers"]}

            attachments = []
            if "parts" in msg_data["payload"]:
                for part in msg_data["payload"]["parts"]:
                    if part["mimeType"] == "application/pdf":
                        att_id = part["body"].get("attachmentId")
                        if att_id:
                            text = await GmailService.get_attachment(service, message_id, att_id)
                            attachments.append({"filename": part.get("filename", "attachment.pdf"), "text": text})

            return {
                "id": message_id,
                "subject": headers.get("Subject", "(no subject)"),
                "from": headers.get("From", "Unknown"),
                "date": headers.get("Date", ""),
                "body": _extract_body(msg_data["payload"]),
                "attachments": attachments,
            }
        except Exception as exc:
            raise ValueError(f"Error getting message: {exc}")

    @staticmethod
    async def get_attachment(service, message_id: str, attachment_id: str) -> str:
        try:
            from pypdf import PdfReader
            att = service.users().messages().attachments().get(
                userId="me", messageId=message_id, id=attachment_id
            ).execute()
            data = base64.urlsafe_b64decode(att["data"])
            reader = PdfReader(io.BytesIO(data))
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception as exc:
            logger.warning("PDF extraction failed: %s", exc)
            return "(could not extract attachment text)"


def _extract_body(payload: dict) -> str:
    if payload.get("body", {}).get("data"):
        return base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8", errors="replace")
    for part in payload.get("parts", []):
        if part.get("mimeType") == "text/plain":
            data = part.get("body", {}).get("data", "")
            if data:
                return base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")
    # Fallback: try HTML and strip tags
    for part in payload.get("parts", []):
        if part.get("mimeType") == "text/html":
            data = part.get("body", {}).get("data", "")
            if data:
                html = base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")
                return re.sub(r"<[^>]+>", " ", html)
    return "(no body)"
