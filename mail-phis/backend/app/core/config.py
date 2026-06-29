from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    APP_NAME: str = "mailrecon"
    SECRET_KEY: str = "change-me-before-production"
    DATABASE_URL: str = "postgresql+asyncpg://mailrecon:mailrecon@postgres:5432/mailrecon"
    REDIS_URL: str = "redis://redis:6379/0"
    CELERY_BROKER_URL: str = "redis://redis:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/2"

    PHISHTANK_API_KEY: Optional[str] = None
    URLHAUS_AUTH_KEY: Optional[str] = None
    ABUSEIPDB_API_KEY: Optional[str] = None   # IP reputation (degrades gracefully if absent)

    MAX_FILE_SIZE_MB: int = 5
    DEBUG: bool = False
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"


settings = Settings()
