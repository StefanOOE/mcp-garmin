"""Thin wrapper for stress tools."""

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
def get_daily_stress(day: str | None = None) -> list[dict]:
    """Daily stress data for a day (YYYY-MM-DD)."""
    from garth.data import DailyStressData
    client = get_client()
    result = DailyStressData.get(day=day, client=client)
    return [_to_dict(entry) for entry in result]


@register
@_handle_garmin_error
def get_weekly_stress(start_date: str | None = None) -> list[dict]:
    """Weekly stress data starting from a date (YYYY-MM-DD)."""
    from garth.data import WeeklyStressData
    client = get_client()
    result = WeeklyStressData.get(start_date=start_date, client=client)
    return [_to_dict(entry) for entry in result]


@register
@_handle_garmin_error
def get_training_status_daily(day: str | None = None) -> dict:
    """Training status for a day (YYYY-MM-DD)."""
    from garth.data import TrainingStatusDaily
    client = get_client()
    result = TrainingStatusDaily.get(day=day, client=client)
    return _to_dict(result)


@register
@_handle_garmin_error
def get_training_status_weekly(start_date: str | None = None) -> dict:
    """Training status for a week starting from a date (YYYY-MM-DD)."""
    from garth.data import TrainingStatusWeekly
    client = get_client()
    result = TrainingStatusWeekly.get(start_date=start_date, client=client)
    return _to_dict(result)


@register
@_handle_garmin_error
def get_training_status_monthly(start_date: str | None = None) -> dict:
    """Training status for a month starting from a date (YYYY-MM-DD)."""
    from garth.data import TrainingStatusMonthly
    client = get_client()
    result = TrainingStatusMonthly.get(start_date=start_date, client=client)
    return _to_dict(result)


@register
@_handle_garmin_error
def get_training_readiness(day: str | None = None) -> dict:
    """Training readiness for a day (YYYY-MM-DD)."""
    from garth.data import TrainingReadiness
    client = get_client()
    result = TrainingReadiness.get(day=day, client=client)
    return _to_dict(result)


@register
@_handle_garmin_error
def get_morning_readiness(day: str | None = None) -> dict:
    """Morning readiness for a day (YYYY-MM-DD)."""
    from garth.data import MorningReadiness
    client = get_client()
    result = MorningReadiness.get(day=day, client=client)
    return _to_dict(result)