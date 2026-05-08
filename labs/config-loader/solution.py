from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    api_key: str
    database_url: str
    debug: bool = False
    log_level: str = "INFO"
    max_retries: int = 3
    timeout: float = 30.0

    class Config:
        env_file = ".env"

_settings: Optional[Settings] = None

def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
