"""Thin wrapper for heart tools.

garth-ng 1.1.0 target mapping (S1 spike-api-mapping.md \u00a71.5):
- get_daily_heart_rate: garth.data.DailyHeartRate.get(day, client) (Remap: class name only).
- get_hrv: garth.data.HRVData.list(end, days, client) -- NO .get, only .list.
- get_resting_heart_rate: no dedicated accessor. Composed from
  DailyHeartRate.list(end=day, days=1)[0].resting_heart_rate.
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
def get_daily_heart_rate(day: str | None = None) -> dict:
    """Daily heart rate data for a day (YYYY-MM-DD)."""
    from garth.data import DailyHeartRate

    client = get_client()
    result = DailyHeartRate.get(day=day, client=client)
    return _to_dict(result) if result else {}


@register
@_handle_garmin_error
def get_hrv(end: str | None = None, days: int = 28) -> list[dict]:
    """HRV (Heart Rate Variability) data for a day (YYYY-MM-DD)."""
    from garth.data import HRVData

    client = get_client()
    result = HRVData.list(end=end, days=days, client=client)
    return [_to_dict(entry) for entry in result]


@register
@_handle_garmin_error
def get_resting_heart_rate(end: str | None = None, days: int = 1) -> list[dict]:
    """Resting heart rate for a day (YYYY-MM-DD)."""
    from garth.data import DailyHeartRate

    client = get_client()
    result = DailyHeartRate.list(end=end, days=days, client=client)
    return [_to_dict(entry) for entry in result]
