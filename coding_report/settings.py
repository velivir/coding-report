from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Validates values from environment variables."""

    owner_timezone: str = Field(env='OWNER_TIMEZONE')


def get_settings() -> Settings:
    """Gets values from environment variables."""
    return Settings()
