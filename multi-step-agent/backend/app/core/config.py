from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:password@postgres:5432/agent"
    REDIS_URL: str = "redis://localhost:6379/0"
    GEMINI_API_KEY: str = ""
    OPENAI_API_KEY: Optional[str] = None
    ACTIVE_LLM_PROVIDER: str = "gemini"
    GEMINI_MODEL: str = "gemini-2.0-flash"
    OPENAI_MODEL: str = "gpt-4o"

    class Config:
        env_file = ".env"


settings = Settings()
