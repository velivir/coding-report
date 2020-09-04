from typing import List

import apprise

from coding_report.statistics.github_statistics import RepositoryStatistics


def generate_message_with_github_statistics(github_statistics) -> List[str]:
    """Generates a message with github statistics."""
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
            'Репозиторий - {repository_name}\nКоммитов - {commit_count}: \n{commit_names}\n\n'.format(
                repository_name=repository_statistics.name,
                commit_count=len(commits_msg),
                commit_names=''.join(commits_msg),
            ),
        )
    return message


def generate_message_with_wakatime_statistics(wakatime_statistics: float) -> str:
    """Generates a message with wakatime statistics."""
    return 'Продолжительность кодинга по Wakatime - {duration}'.format(
        duration=convert_seconds_to_hours(wakatime_statistics),
    )


def create_report_message(
    github_statistics: List[RepositoryStatistics], coding_duration_by_wakatime: float,
) -> List[str]:
    """Creates a message for sending statistics to Telegram."""
    message_with_github_statistics = generate_message_with_github_statistics(github_statistics)
    message_with_wakatime_statistics = generate_message_with_wakatime_statistics(coding_duration_by_wakatime)
    return [
        ''.join(message_with_github_statistics),
        message_with_wakatime_statistics if message_with_wakatime_statistics else '',
    ]


def send_report_message_to_telegram(telegram_token: str, report_message: str, date: str) -> None:
    """Sends coding statistics to Telegram."""
    apobj = apprise.Apprise()
    apobj.add(f'tgram://{telegram_token}/')
    apobj.notify(
        body=report_message,
        title=f'Статистика кодинга за {date}',
    )


def convert_seconds_to_hours(seconds: float) -> str:
    """Converts seconds to hours and minutes."""
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return '%dч:%02dм:%02dс' % (hours, minutes, seconds)
