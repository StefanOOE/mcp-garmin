"""Thin wrapper for steps tools."""

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
def get_daily_steps(day: str | None = None) -> dict:
    """Daily steps data for a day (YYYY-MM-DD)."""
    from garth.data import StepsData

    client = get_client()
    result = StepsData.get(day=day, client=client)
    return _to_dict(result)


@register
@_handle_garmin_error
def get_weekly_steps(start_date: str | None = None) -> list[dict]:
    """Weekly steps data starting from a date (YYYY-MM-DD)."""
    from garth.data import WeeklyStepsData

    client = get_client()
    result = WeeklyStepsData.get(start_date=start_date, client=client)
    return [_to_dict(entry) for entry in result]


@register
@_handle_garmin_error
def get_daily_summary(day: str | None = None) -> dict:
    """Daily summary for a day (YYYY-MM-DD)."""
    from garth.data import DailySummary

    client = get_client()
    result = DailySummary.get(day=day, client=client)
    return _to_dict(result)


@register
@_handle_garmin_error
def get_daily_summary_history(end: str | None = None, days: int = 7) -> list[dict]:
    """Daily summary history for the last N days (up to end)."""
    from garth.data import DailySummary

    client = get_client()
    result = DailySummary.list(end=end, days=days, client=client)
    return [_to_dict(entry) for entry in result]
