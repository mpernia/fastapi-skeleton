from functools import lru_cache
from typing import Any, Dict, Optional

from pydantic import PostgresDsn, RedisDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="allow"
    )

    # Application
    APP_NAME: str = "FastAPI Skeleton"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    SECRET_KEY: SecretStr
    API_PREFIX: str = "/api/v1"
    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    # Database
    DATABASE_URL: PostgresDsn
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10

    # Redis
    REDIS_URL: Optional[RedisDsn] = None
    
    # Security
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    
    # Monitoring
    SENTRY_DSN: Optional[str] = None


@lru_cache()
def get_settings() -> Settings:
    return Settings()
