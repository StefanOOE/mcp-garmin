"""Heart tools: daily heart rate, HRV, resting heart rate."""
from __future__ import annotations

from .client import _handle_garmin_error, _to_dict, get_client


@_handle_garmin_error
def get_daily_heart_rate(day: str | None = None) -> dict:
    """Daily heart rate for a day (YYYY-MM-DD): max, min, resting."""
    client = get_client()
    from garth.data import DailyHeartRate

    result = DailyHeartRate.get(day=day, client=client)
    return _to_dict(result)


@_handle_garmin_error
def get_hrv(end: str | None = None, days: int = 28) -> list[dict]:
    """HRV history for the last N days (period=days, up to end, YYYY-MM-DD)."""
    client = get_client()
    from garth.data.hrv import HRVData

    result = HRVData.list(end=end, period=days, client=client)
    return [_to_dict(entry) for entry in result]


@_handle_garmin_error
def get_resting_heart_rate(end: str | None = None, days: int = 1) -> list[dict]:
    """Resting heart rate history for the last N days (up to end, YYYY-MM-DD)."""
    client = get_client()
    from garth.data import DailyHeartRate

    result = DailyHeartRate.list(end=end, days=days, client=client)
    return [_to_dict(entry) for entry in result]
