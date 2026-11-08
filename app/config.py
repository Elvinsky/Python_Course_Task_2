"""Typed configuration read from environment variables and an optional .env file (Twelve-Factor)."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+asyncpg://inventory:inventory@localhost:5432/inventory"
    echo_sql: bool = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
