"""Thin wrapper for heart tools."""

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
def get_daily_heart_rate(day: str | None = None) -> list[dict]:
    """Daily heart rate data for a day (YYYY-MM-DD)."""
    from garth.data import HeartRateData

    client = get_client()
    result = HeartRateData.get(day=day, client=client)
    return [_to_dict(entry) for entry in result]


@register
@_handle_garmin_error
def get_hrv(day: str | None = None) -> list[dict]:
    """HRV (Heart Rate Variability) data for a day (YYYY-MM-DD)."""
    from garth.data import HrvData

    client = get_client()
    result = HrvData.get(day=day, client=client)
    return [_to_dict(entry) for entry in result]


@register
@_handle_garmin_error
def get_resting_heart_rate(day: str | None = None) -> dict:
    """Resting heart rate for a day (YYYY-MM-DD)."""
    from garth.data import RestingHeartRateData

    client = get_client()
    result = RestingHeartRateData.get(day=day, client=client)
    return _to_dict(result)
