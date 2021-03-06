from typing import Any, Mapping, Optional

from requests import get
from requests.auth import HTTPBasicAuth

from coding_report.api.github.settings import get_settings

settings = get_settings()
GITHUB_LOGIN = settings.github_login
GITHUB_API_TOKEN = settings.github_token
REPO_OWNER = settings.repo_owner


def fetch_data_from_github(relative_url: str) -> Optional[Mapping[str, Any]]:  # type: ignore
    """Fetch data from github."""
    raw_response = get(
        f'https://api.github.com{relative_url}',
        auth=HTTPBasicAuth(GITHUB_LOGIN, GITHUB_API_TOKEN),
    )
    return raw_response.json() if raw_response else None


def fetch_repos_list() -> Optional[Mapping[str, Any]]:  # type: ignore
    """Fetch repositories list from github owner."""
    return fetch_data_from_github(relative_url=f'/users/{REPO_OWNER}/repos')


def fetch_repo_info(repo_name: str):
    """Fetches detailed information about a repository."""
    return fetch_data_from_github(relative_url=f'/repos/{REPO_OWNER}/{repo_name}')


def fetch_commits(repo_name: str):
    """Fetches detailed information about repository commits."""
    return fetch_data_from_github(relative_url=f'/repos/{REPO_OWNER}/{repo_name}/commits')
