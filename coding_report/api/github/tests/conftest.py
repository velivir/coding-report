import pytest

from coding_report.api.github.settings import get_settings


@pytest.fixture()
def settings():
    settings = get_settings()
    return settings.github_login, settings.github_token
