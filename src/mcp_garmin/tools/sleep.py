"""Thin wrapper for sleep tools (garth-ng 1.1.0).

Class mapping vs. legacy garth 0.8:
- get_sleep          -> SleepData          (daily DTO + movement)
- get_sleep_detail   -> DailySleepData     (sleep_levels, SpO2, skin temp)
- get_sleep_summary  -> DailySleepData     (scores, SpO2, sleep_need)

Note: garth-ng 1.1.0 removed SleepDetailData / SleepSummaryData and
merged both into DailySleepData, so detail + summary now share a source.
"""

from __future__ import annotations

from .base import register
from ..client import GarminClient

# Create a singleton client instance
_client_instance = GarminClient()


def get_client():
    """Get the Garmin client instance."""
    return _client_instance.get_client()


def _to_dict(obj):
    """Convert object to dict."""
    return _client_instance._to_dict(obj)


def _handle_garmin_error(func):
    """Handle Garmin errors."""
    return _client_instance._handle_garmin_error(func)


@register
@_handle_garmin_error
def get_sleep(day: str | None = None) -> list[dict]:
    """Sleep data for a day (YYYY-MM-DD)."""
    from garth.data import SleepData

    client = get_client()
    result = SleepData.get(day=day, client=client)
    if result is None:
        return []
    dto = _to_dict(result.daily_sleep_dto)
    movement = [_to_dict(m) for m in (result.sleep_movement or [])]
    return [dict(dto, sleep_movement=movement)]


@register
@_handle_garmin_error
def get_sleep_detail(day: str | None = None) -> dict:
    """Detailed sleep data for a day (YYYY-MM-DD).

    Includes per-minute sleep_levels, SpO2 summary, skin temperature.
    """
    from garth.data import DailySleepData

    client = get_client()
    result = DailySleepData.get(day=day, client=client)
    if result is None:
        return {}
    return _to_dict(result)


@register
@_handle_garmin_error
def get_sleep_summary(day: str | None = None) -> dict:
    """Sleep summary for a day (YYYY-MM-DD).

    Scores, SpO2, sleep need, respiratory and stress values.
    """
    from garth.data import DailySleepData

    client = get_client()
    result = DailySleepData.get(day=day, client=client)
    if result is None:
        return {}
    return _to_dict(result)