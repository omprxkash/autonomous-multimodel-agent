import base64
import httpx
from app.core.config import settings


async def score_email(raw_mime_bytes: bytes) -> dict:
    if not settings.MAIL_PHIS_URL:
        return {"verdict": "UNKNOWN", "risk_score": None}
    try:
        encoded = base64.b64encode(raw_mime_bytes).decode()
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(
                f"{settings.MAIL_PHIS_URL}/api/analyze/email",
                json={"raw_email": encoded},
            )
            if resp.status_code == 200:
                data = resp.json()
                return {"verdict": data.get("verdict", "UNKNOWN"), "risk_score": data.get("risk_score")}
    except Exception:
        pass
    return {"verdict": "UNKNOWN", "risk_score": None}
