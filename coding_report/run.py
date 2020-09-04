import datetime

from coding_report.api.github.github import fetch_repos_list
from coding_report.api.wakatime.wakatime import fetch_durations_from_wakatime
from coding_report.message import (
    create_report_message,
    send_report_message_to_telegram,
)
from coding_report.settings import get_settings
from coding_report.statistics.github_statistics import (
    collect_coding_statistics_for_today,
    get_repositories_updated_today,
)
from coding_report.statistics.wakatime_statistics import (
    calculate_coding_duration,
)


def main() -> None:  # noqa: WPS210
    """Entry point."""
    settings = get_settings()
    raw_repos_content = fetch_repos_list()
    repositories_updated_today = get_repositories_updated_today(raw_repos_content)
    github_statistics = collect_coding_statistics_for_today(repositories_updated_today)
    coding_duration_by_wakatime = calculate_coding_duration(
        fetch_durations_from_wakatime(
            date=datetime.datetime.today().strftime('%Y-%m-%d'),
        ),
    )
    report_message = ''.join(create_report_message(github_statistics, coding_duration_by_wakatime))
    send_report_message_to_telegram(
        telegram_token=settings.telegram_token,
        report_message=report_message,
        date=str(datetime.datetime.today().date()),
    )


if __name__ == '__main__':
    main()
