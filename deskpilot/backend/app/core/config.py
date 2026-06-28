from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    APP_NAME: str = "deskpilot"
    SECRET_KEY: str = "change-me-before-production"
    DATABASE_URL: str = "postgresql+asyncpg://deskpilot:deskpilot@postgres:5432/deskpilot"

    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/api/auth/callback"
    GEMINI_API_KEY: str = ""

    FRONTEND_URL: str = "http://localhost:3000"
    DEBUG: bool = False
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"


settings = Settings()
