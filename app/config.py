from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    GEMINI_API_KEY: Optional[str] = None
    FLASK_ENV: str = "development"
    FLASK_PORT: int = 9000
    ALLOWED_EXTENSIONS: set = {"png", "jpg", "jpeg"}
    MAX_CONTENT_LENGTH: int = 16 * 1024 * 1024  # 16MB max file size

    class Config:
        env_file = ".env"

settings = Settings()
