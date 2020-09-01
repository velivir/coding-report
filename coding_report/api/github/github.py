from typing import Any, Mapping, Optional

from requests import get
from requests.auth import HTTPBasicAuth


def fetch_data_from_github(  # type: ignore
    github_login: str, github_api_token: str, relative_url: str,
) -> Optional[Mapping[str, Any]]:
    """Fetch data from github."""
    raw_response = get(
        f'https://api.github.com{relative_url}',
        auth=HTTPBasicAuth(github_login, github_api_token),
    )
    return raw_response.json() if raw_response else None


def fetch_repos_list(github_login: str, github_api_token: str) -> Optional[Mapping[str, Any]]:  # type: ignore
    """Fetch repositories list from github owner."""
    return fetch_data_from_github(
        github_login=github_login,
        github_api_token=github_api_token,
        relative_url=f'/users/{github_login}/repos',
    )


def fetch_repo_info(github_login: str, github_api_token: str, owner: str, repo_name: str):
    """Fetches detailed information about a repository."""
    return fetch_data_from_github(
        github_login=github_login,
        github_api_token=github_api_token,
        relative_url=f'/repos/{owner}/{repo_name}',
    )


def fetch_commits(github_login: str, github_api_token: str, owner: str, repo_name: str):
    """Fetches detailed information about repository commits."""
    return fetch_data_from_github(
        github_login=github_login,
        github_api_token=github_api_token,
        relative_url=f'/repos/{owner}/{repo_name}/commits',
    )
