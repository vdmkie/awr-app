from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    APP_NAME: str = "AWR API"
    API_V1_PREFIX: str = "/api/v1"

    SECRET_KEY: str = "change_me"  # поменять в проде
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/awr"

    TELEGRAM_BOT_TOKEN: str | None = None
    SUPERGROUP_CHAT_ID: str | None = None

    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost",
        "https://your-render-web.onrender.com",
    ]

    class Config:
        env_file = ".env"

settings = Settings()
