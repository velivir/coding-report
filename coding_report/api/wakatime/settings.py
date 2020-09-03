from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Validates values from environment variables."""

    wakatime_api_token: str = Field(env='WAKATIME_API_TOKEN')


def get_settings() -> Settings:
    """Gets values from environment variables."""
    return Settings()
