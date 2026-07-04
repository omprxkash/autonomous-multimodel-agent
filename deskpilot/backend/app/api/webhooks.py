"""
Gmail push notifications via Google Cloud Pub/Sub.
Google POSTs to /api/webhooks/gmail when new emails arrive.
"""
import base64
import json
import logging
from fastapi import APIRouter, Request, HTTPException
from sqlalchemy import select
from app.core.database import async_session_maker
from app.models.user import User

router = APIRouter(prefix="/webhooks", tags=["webhooks"])
logger = logging.getLogger(__name__)


@router.post("/gmail")
async def gmail_push(request: Request):
    try:
        body = await request.json()
        message = body.get("message", {})
        data_b64 = message.get("data", "")
        if not data_b64:
            return {"status": "no_data"}

        data = json.loads(base64.b64decode(data_b64).decode())
        email_address = data.get("emailAddress")
        history_id = data.get("historyId")

        logger.info(f"Gmail push: email={email_address} historyId={history_id}")
        # Future: fetch new messages using historyId and process them
        return {"status": "received", "email": email_address, "historyId": history_id}
    except Exception as e:
        logger.error(f"Gmail webhook error: {e}")
        return {"status": "error"}


@router.post("/gmail/setup")
async def setup_gmail_watch(
    topic_name: str,
    request: Request,
):
    from app.core.security import decode_access_token
    from app.services import gmail as gmail_service

    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")

    user_id = decode_access_token(auth[7:])

    async with async_session_maker() as db:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user or not user.access_token_enc:
            raise HTTPException(status_code=400, detail="Gmail not connected")

        from app.core.config import settings
        creds = {
            "access_token": user.access_token_enc,
            "refresh_token": user.refresh_token_enc,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
        }
        svc = gmail_service._build_service(creds)

        try:
            watch_response = svc.users().watch(
                userId="me",
                body={"topicName": topic_name, "labelIds": ["INBOX"]},
            ).execute()
            return {"status": "watching", "expiration": watch_response.get("expiration"), "historyId": watch_response.get("historyId")}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Watch setup failed: {e}")
