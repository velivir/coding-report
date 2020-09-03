from coding_report.api.wakatime.models.duration import Duration


def calculate_coding_duration(wakatime_response) -> float:
    """Gets general statistics for the day."""
    return sum((
        Duration(**chunk).duration
        for chunk in wakatime_response['data']
    ))
