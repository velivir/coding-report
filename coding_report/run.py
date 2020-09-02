import datetime
from dataclasses import dataclass
from typing import Generator, List

import pytz
from dateutil import parser

from coding_report.api.github.github import fetch_commits, fetch_repos_list
from coding_report.api.github.models.commit import Commit
from coding_report.api.github.models.repository import Repository
from coding_report.settings import get_settings


@dataclass
class RepositoryStatistics:  # noqa: WPS306
    """Repository statistics data."""

    name: str
    url: str
    commits: List[str]


def main() -> None:
    """Entry point."""
    raw_repos_content = fetch_repos_list()
    repositories_updated_today = get_repositories_updated_today(raw_repos_content)
    collect_coding_statistics_for_today(repositories_updated_today)


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


def get_repositories_updated_today(raw_repos_content) -> Generator[Repository, None, None]:
    """Get a list of repositories that are pushed to today."""
    return (
        Repository(**raw_repo_content)
        for raw_repo_content in raw_repos_content
        if is_updated_today(Repository(**raw_repo_content).pushed_at)
    )


def get_commits_for_today(repository_name: str) -> List[Commit]:
    """Gets the commits made today."""
    commits_for_today = [
        Commit(**raw_commit)
        for raw_commit in fetch_commits(repository_name)
        if is_updated_today(Commit(**raw_commit).commit.author.date)
    ]
    commits_for_today.reverse()
    return commits_for_today


def collect_coding_statistics_for_today(
    repositories_updated_today: Generator[Repository, None, None],
) -> List[RepositoryStatistics]:
    """Collects commit names across all repositories updated today."""
    return [
        RepositoryStatistics(
            name=repository_updated_today.name,
            url=repository_updated_today.url,
            commits=[
                commit.commit.message.split('\n\n')[0]
                for commit in get_commits_for_today(repository_updated_today.name)
            ],
        )
        for repository_updated_today in repositories_updated_today
    ]


if __name__ == '__main__':
    main()
