import datetime
from typing import Generator

import pytz
from dateutil import parser

from coding_report.api.github.github import fetch_commits, fetch_repos_list
from coding_report.api.github.models.commit import Commit
from coding_report.api.github.models.repository import Repository
from coding_report.settings import get_settings


def main() -> None:
    """Entry point."""
    raw_repos_content = fetch_repos_list()
    repository_names_updated_today = get_repository_names_updated_today(raw_repos_content)
    get_commits_for_today(repository_names_updated_today)


def is_updated_today(last_push_time: str) -> bool:
    """Returns true if the passed time occurred today."""
    settings = get_settings()
    owner_timezone = pytz.timezone(settings.owner_timezone)
    now = datetime.datetime.now(tz=owner_timezone)
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    local_time_of_last_update_of_repo = pytz.utc.localize(
        parser.parse(last_push_time, ignoretz=True),
        is_dst=None,
    ).astimezone(owner_timezone)
    return midnight < local_time_of_last_update_of_repo < now


def get_repository_names_updated_today(raw_repos_content) -> Generator[str, None, None]:
    """Get a list of repositories that are pushed to today."""
    return (
        Repository(**raw_repo_content).name
        for raw_repo_content in raw_repos_content
        if is_updated_today(Repository(**raw_repo_content).pushed_at)
    )


def get_commits_for_today(repository_names_updated_today: Generator[str, None, None]) -> Generator[Commit, None, None]:
    """Gets the commits made today."""
    return (
        Commit(**raw_commit)
        for repo_name in repository_names_updated_today
        for raw_commit in fetch_commits(repo_name)
        if is_updated_today(Commit(**raw_commit).commit.author.date)
    )


if __name__ == '__main__':
    main()
