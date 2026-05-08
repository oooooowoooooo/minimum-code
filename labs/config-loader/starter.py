"""Config Loader Lab
Goal: Build a config loader using pydantic-settings that reads from .env
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables / .env file.

    TODO: Add the following fields:
    - api_key: str (required)
    - database_url: str (required)
    - debug: bool = False
    - log_level: str = "INFO"
    - max_retries: int = 3
    - timeout: float = 30.0
    """
    pass


# Singleton pattern
_settings: Optional[Settings] = None

def get_settings() -> Settings:
    """Return cached Settings instance. Create on first call."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
