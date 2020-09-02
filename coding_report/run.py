from typing import List

from coding_report.api.github.github import fetch_repos_list
from coding_report.statistics import (
    RepositoryStatistics,
    collect_coding_statistics_for_today,
    get_repositories_updated_today,
)


def main() -> None:
    """Entry point."""
    raw_repos_content = fetch_repos_list()
    repositories_updated_today = get_repositories_updated_today(raw_repos_content)
    github_statistics = collect_coding_statistics_for_today(repositories_updated_today)
    create_report_message(github_statistics)


def create_report_message(github_statistics: List[RepositoryStatistics]) -> str:
    """Creates a message for sending statistics to Telegram."""
    message = []
    commits_msg: List[str] = []
    for repository_statistics in github_statistics:
        commits_msg.clear()
        for commit_text in repository_statistics.commits:
            commits_msg.append(
                f'\n{commit_text}'.format(
                    commit_text=commit_text,
                ),
            )
        message.append(
            '**{repository_name}**\n{commit_names}\n\n'.format(
                repository_name=repository_statistics.name,
                commit_names=''.join(commits_msg),
            ),
        )
    return ''.join(message)


if __name__ == '__main__':
    main()
