import email
import email.policy
from email.message import EmailMessage
from typing import Any
import hashlib


def parse_email(raw_bytes: bytes) -> dict[str, Any]:
    msg: EmailMessage = email.message_from_bytes(raw_bytes, policy=email.policy.default)

    parts = []
    attachments = []

    for part in msg.walk():
        ct = part.get_content_type()
        disposition = part.get_content_disposition() or ""

        if disposition == "attachment":
            filename = part.get_filename() or "unnamed"
            payload = part.get_payload(decode=True) or b""
            attachments.append({
                "filename": filename,
                "content_type": ct,
                "size": len(payload),
                "sha256": hashlib.sha256(payload).hexdigest(),
                "has_executable": _is_executable(filename),
                "has_macro": _has_macro_extension(filename),
                "double_extension": _has_double_extension(filename),
            })
        elif ct in ("text/plain", "text/html"):
            payload = part.get_payload(decode=True)
            if payload:
                parts.append({
                    "content_type": ct,
                    "content": payload.decode(part.get_content_charset() or "utf-8", errors="replace"),
                })

    return {
        "subject": str(msg.get("Subject", "")),
        "from": str(msg.get("From", "")),
        "to": str(msg.get("To", "")),
        "reply_to": str(msg.get("Reply-To", "")),
        "date": str(msg.get("Date", "")),
        "message_id": str(msg.get("Message-ID", "")),
        "headers": dict(msg.items()),
        "body_parts": parts,
        "attachments": attachments,
        "raw_size": len(raw_bytes),
    }


def _is_executable(filename: str) -> bool:
    exts = {".exe", ".bat", ".cmd", ".com", ".vbs", ".js", ".ps1", ".scr", ".pif"}
    return any(filename.lower().endswith(e) for e in exts)


def _has_macro_extension(filename: str) -> bool:
    exts = {".doc", ".docm", ".xls", ".xlsm", ".ppt", ".pptm", ".xlsb"}
    return any(filename.lower().endswith(e) for e in exts)


def _has_double_extension(filename: str) -> bool:
    parts = filename.split(".")
    return len(parts) > 2
