from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GEMINI_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: Optional[str] = None
    DEFAULT_PROVIDER: str = "gemini"

    class Config:
        env_file = ".env"


settings = Settings()
