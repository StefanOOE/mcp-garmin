"""Thin wrapper for sleep tools."""

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
    return [_to_dict(entry) for entry in result]


@register
@_handle_garmin_error
def get_sleep_detail(day: str | None = None) -> dict:
    """Detailed sleep data for a day (YYYY-MM-DD)."""
    from garth.data import SleepDetailData

    client = get_client()
    result = SleepDetailData.get(day=day, client=client)
    return _to_dict(result)


@register
@_handle_garmin_error
def get_sleep_summary(day: str | None = None) -> dict:
    """Sleep summary for a day (YYYY-MM-DD)."""
    from garth.data import SleepSummaryData

    client = get_client()
    result = SleepSummaryData.get(day=day, client=client)
    return _to_dict(result)
