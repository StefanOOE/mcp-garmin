"""Herz-Tools: Tages-Heart-Rate, HRV, Ruhepuls."""
from __future__ import annotations

from .client import _handle_garmin_error, _to_dict, get_client


@_handle_garmin_error
def get_daily_heart_rate(day: str | None = None) -> dict:
    """Tages-Herzfrequenz für einen Tag (YYYY-MM-DD): Max, Min, Ruhepuls."""
    client = get_client()
    from garth.data import DailyHeartRate

    result = DailyHeartRate.get(day=day, client=client)
    return _to_dict(result)


@_handle_garmin_error
def get_hrv(end: str | None = None, days: int = 28) -> list[dict]:
    """HRV-Verlauf der letzten N Tage (period=days, bis end, YYYY-MM-DD)."""
    client = get_client()
    from garth.data.hrv import HRVData

    result = HRVData.list(end=end, period=days, client=client)
    return [_to_dict(entry) for entry in result]


@_handle_garmin_error
def get_resting_heart_rate(end: str | None = None, days: int = 1) -> list[dict]:
    """Ruhepuls-Verlauf der letzten N Tage (bis end, YYYY-MM-DD)."""
    client = get_client()
    from garth.data import DailyHeartRate

    result = DailyHeartRate.list(end=end, days=days, client=client)
    return [_to_dict(entry) for entry in result]
