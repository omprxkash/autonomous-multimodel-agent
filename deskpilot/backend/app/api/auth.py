import logging
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, HTTPException, Depends, Header, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
import httpx
from app.core.config import settings
from app.core.database import get_db
from app.core.security import create_access_token, decode_access_token
from app.models.user import User

logger = logging.getLogger("deskpilot")
router = APIRouter(prefix="/auth", tags=["auth"])

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

SCOPES = [
    "openid",
    "email",
    "profile",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/calendar",
]


class SetupRequest(BaseModel):
    user_id: str
    name: str
    job_title: str
    main_goal: str
    work_hours: str
    personalization: str = ""


class ProfileUpdate(BaseModel):
    name: str
    job_title: str
    personalization: str
    main_goal: str
    work_hours: str


async def get_current_user(
    authorization: str = Header(""),
    db: AsyncSession = Depends(get_db),
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


@router.get("/login")
async def login():
    if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_CLIENT_SECRET:
        raise HTTPException(status_code=500, detail="Google OAuth not configured")
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": " ".join(SCOPES),
        "access_type": "offline",
        "prompt": "consent",
    }
    query = "&".join(f"{k}={v}" for k, v in params.items())
    # Return auth_url as JSON so frontend can redirect
    return {"auth_url": f"{GOOGLE_AUTH_URL}?{query}"}


@router.get("/callback")
async def callback(code: str = Query(...), db: AsyncSession = Depends(get_db)):
    if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_CLIENT_SECRET:
        raise HTTPException(status_code=500, detail="Google OAuth not configured")

    try:
        async with httpx.AsyncClient() as client:
            token_resp = await client.post(
                GOOGLE_TOKEN_URL,
                data={
                    "code": code,
                    "client_id": settings.GOOGLE_CLIENT_ID,
                    "client_secret": settings.GOOGLE_CLIENT_SECRET,
                    "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                    "grant_type": "authorization_code",
                },
            )
            if token_resp.status_code != 200:
                raise ValueError(f"Token exchange failed: {token_resp.text}")
            tokens = token_resp.json()

            userinfo_resp = await client.get(
                GOOGLE_USERINFO_URL,
                headers={"Authorization": f"Bearer {tokens['access_token']}"},
            )
            userinfo = userinfo_resp.json()

        email = userinfo.get("email")
        google_id = userinfo.get("sub")
        if not email or not google_id:
            raise ValueError("Missing user info from Google")

        result = await db.execute(select(User).where(User.google_id == google_id))
        user = result.scalar_one_or_none()

        if user:
            if tokens.get("refresh_token"):
                user.refresh_token = tokens["refresh_token"]
            user.updated_at = datetime.utcnow()
        else:
            user = User(
                email=email,
                name=userinfo.get("name", ""),
                picture=userinfo.get("picture"),
                google_id=google_id,
                refresh_token=tokens.get("refresh_token"),
            )
            db.add(user)

        await db.commit()
        await db.refresh(user)

        jwt_token = create_access_token(user.id)
        redirect_url = (
            f"{settings.FRONTEND_URL}/auth/callback"
            f"?token={jwt_token}"
            f"&user_id={user.id}"
            f"&is_setup_complete={1 if user.is_setup_complete else 0}"
        )
        if not user.refresh_token:
            redirect_url += "&warning=Sign+in+again+to+enable+Gmail+and+Calendar"

        return RedirectResponse(url=redirect_url)

    except HTTPException:
        raise
    except Exception as exc:
        logger.error("Auth callback error: %s", exc)
        return RedirectResponse(url=f"{settings.FRONTEND_URL}?error={str(exc)[:200]}")


@router.get("/verify")
async def verify(token: str = Query(...)):
    try:
        user_id = decode_access_token(token)
        return {"user_id": user_id}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.get("/user/{user_id}")
async def get_user(user_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "picture": user.picture,
        "is_setup_complete": bool(user.is_setup_complete),
        "job_title": user.job_title,
        "personalization": user.personalization,
        "main_goal": user.main_goal,
        "work_hours": user.work_hours,
    }


@router.get("/me")
async def me(user: User = Depends(get_current_user)):
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "picture": user.picture,
        "is_setup_complete": bool(user.is_setup_complete),
        "job_title": user.job_title,
        "personalization": user.personalization,
        "main_goal": user.main_goal,
        "work_hours": user.work_hours,
    }


@router.post("/setup")
async def setup_user(req: SetupRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == req.user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.name = req.name
    user.job_title = req.job_title
    user.main_goal = req.main_goal
    user.work_hours = req.work_hours
    user.personalization = req.personalization
    user.is_setup_complete = 1

    # Persist profile to memory so the agent knows about the user immediately
    from app.services.memory_service import MemoryService
    profile_fact = (
        f"User Profile: name={req.name}, role={req.job_title}, "
        f"goal={req.main_goal}, work hours={req.work_hours}. "
        f"AI instructions: {req.personalization}"
    )
    try:
        await MemoryService.store_fact(req.user_id, profile_fact, "personal", 1.0, {}, db)
    except Exception as exc:
        logger.warning("Could not store profile fact: %s", exc)

    await db.commit()
    return {"status": "success"}


@router.post("/profile/{user_id}")
async def update_profile(user_id: str, req: ProfileUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.name = req.name
    user.job_title = req.job_title
    user.personalization = req.personalization
    user.main_goal = req.main_goal
    user.work_hours = req.work_hours

    from app.services.memory_service import MemoryService
    profile_fact = (
        f"Updated profile: name={req.name}, role={req.job_title}. "
        f"AI instructions: {req.personalization}"
    )
    try:
        await MemoryService.store_fact(user_id, profile_fact, "preference", 1.0, {}, db)
    except Exception as exc:
        logger.warning("Could not store updated profile fact: %s", exc)

    await db.commit()
    return {"status": "success", "user": {"name": user.name, "job_title": user.job_title}}
