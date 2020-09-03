import datetime
from typing import List

import apprise

from coding_report.api.github.github import fetch_repos_list
from coding_report.api.wakatime.wakatime import fetch_durations_from_wakatime
from coding_report.settings import get_settings
from coding_report.statistics.github_statistics import (
    RepositoryStatistics,
    collect_coding_statistics_for_today,
    get_repositories_updated_today,
)
from coding_report.statistics.wakatime_statistics import calculate_coding_duration


def main() -> None:  # noqa: WPS210
    """Entry point."""
    settings = get_settings()
    raw_repos_content = fetch_repos_list()
    repositories_updated_today = get_repositories_updated_today(raw_repos_content)
    github_statistics = collect_coding_statistics_for_today(repositories_updated_today)
    wakatime_statistics = calculate_coding_duration(
        fetch_durations_from_wakatime(
            date=datetime.datetime.today().strftime('%Y-%m-%d'),
        ),
    )
    report_message = create_report_message(github_statistics, wakatime_statistics)
    send_report_message_to_telegram(
        telegram_token=settings.telegram_token,
        report_message=report_message,
        date=str(datetime.datetime.today().date()),
    )


def convert_seconds_to_hours(seconds: float) -> str:
    """Converts seconds to hours and minutes."""
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return '%dч:%02dм:%02dс' % (hours, minutes, seconds)


def create_report_message(github_statistics: List[RepositoryStatistics], wakatime_statistics: float) -> str:
    """Creates a message for sending statistics to Telegram."""
    message = []
    commits_msg: List[str] = []
    for repository_statistics in github_statistics:
        commits_msg.clear()
        for commit_text in repository_statistics.commits:
            commits_msg.append(
                f'\n 🔹 {commit_text}'.format(
                    commit_text=commit_text,
                ),
            )
        message.append(
            'Репозиторий - {repository_name}\nСделано {commit_count} коммитов: \n{commit_names}\n\n'.format(
                repository_name=repository_statistics.name,
                commit_count=len(commits_msg),
                commit_names=''.join(commits_msg),
            ),
        )
    message.append(
        'Wakatime - {duration}'.format(
            duration=convert_seconds_to_hours(wakatime_statistics),
        ),
    )
    return ''.join(message)


def send_report_message_to_telegram(telegram_token: str, report_message: str, date: str) -> None:
    """Sends coding statistics to Telegram."""
    apobj = apprise.Apprise()
    apobj.add(f'tgram://{telegram_token}/')
    apobj.notify(
        body=report_message,
        title=f'Статистика кодинга за {date}',
    )


if __name__ == '__main__':
    main()
