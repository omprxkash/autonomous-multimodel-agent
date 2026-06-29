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
    GEMINI_MODEL: str = "gemini-2.0-flash"
    GOOGLE_API_KEY: str = ""

    # OpenAI (optional — used when ACTIVE_LLM_PROVIDER=openai)
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4-turbo-preview"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"

    # LLM provider switch: "gemini" (default) or "openai"
    ACTIVE_LLM_PROVIDER: str = "gemini"

    # Redis (session cache, optional — falls back to in-process dict)
    REDIS_URL: str = "redis://localhost:6379/0"

    # JWT
    JWT_EXPIRE_MINUTES: int = 10080  # 7 days

    # LangSmith tracing (optional)
    LANGSMITH_API_KEY: Optional[str] = None
    LANGSMITH_PROJECT: str = "deskpilot"

    FRONTEND_URL: str = "http://localhost:3000"
    DEBUG: bool = False
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"


settings = Settings()
