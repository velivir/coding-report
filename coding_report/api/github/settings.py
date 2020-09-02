from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Validates values from environment variables."""

    github_login: str = Field(env='GITHUB_LOGIN')
    github_token: str = Field(env='GITHUB_TOKEN')
    repo_owner: str = Field(env='REPO_OWNER')


def get_settings() -> Settings:
    """Gets values from environment variables."""
    return Settings()
