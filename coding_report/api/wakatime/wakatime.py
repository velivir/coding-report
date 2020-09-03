import requests

from coding_report.api.wakatime.settings import get_settings

settings = get_settings()
WAKATIME_API_TOKEN = settings.wakatime_api_token


def fetch_durations_from_wakatime(date: str):
    """
    Get coding statistics for the desired date.

    Date format - %Y-%M-%D. Example - 2020-09-02
    """
    response = requests.get(
        f'https://wakatime.com/api/v1/users/current/durations?date={date}&api_key={WAKATIME_API_TOKEN}',
    )
    response.raise_for_status()
    return response.json()
