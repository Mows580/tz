from pydantic_settings import BaseSettings, SettingsConfigDict
import os
import dotenv

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )
    DATABASE_URL: str = os.environ.get("DATABASE_URL", "sqlite+aiosqlite:///./database.db")
    DATABASE_ECHO: bool = os.environ.get("DATABASE_ECHO", False)
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "default-secret-key")
    JWT_ALGORITHM: str = os.environ.get("JWT_ALGORITHM", "HS256")


def get_settings():
    return Settings()