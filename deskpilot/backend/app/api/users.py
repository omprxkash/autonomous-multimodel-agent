"""
/users endpoints — backward-compatibility shim for older frontends.
New frontends should use /api/auth/me.
"""
from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User

router = APIRouter(prefix="/users", tags=["users"])


class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    picture: str | None
    gmail_connected: bool
    calendar_connected: bool


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


@router.get("/me", response_model=UserResponse)
async def get_me(user: User = Depends(get_current_user)):
    """DEPRECATED — use /api/auth/me. Kept for frontend compatibility."""
    return UserResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        picture=user.picture,
        gmail_connected=bool(user.access_token_enc),
        calendar_connected=bool(user.access_token_enc),
    )
