"""Thin wrapper for stress tools.

garth-ng 1.1.0 target mapping (S1 spike-api-mapping.md \u00a71.10):
- get_daily_stress: no garth.data accessor -> garth.stats.DailyStress.list(end=day, period=1)[0].
- get_weekly_stress: garth.stats.WeeklyStress.list(end, period).
- get_training_status_daily/weekly/monthly: garth.stats.training_status.{Daily,Weekly,Monthly}TrainingStatus.list(end, period).
- get_training_readiness: garth.data.TrainingReadinessData.get(day) (class-name remap).
- get_morning_readiness: garth.data.MorningTrainingReadinessData.get(day) (class-name remap).
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
def get_daily_stress(day: str | None = None) -> dict:
    """Daily stress data for a day (YYYY-MM-DD)."""
    from garth.stats import DailyStress

    client = get_client()
    result = DailyStress.list(end=day, period=1, client=client)
    return _to_dict(result[0]) if result else {}


@register
@_handle_garmin_error
def get_weekly_stress(end: str | None = None, period: int = 1) -> list[dict]:
    """Weekly stress data starting from a date (YYYY-MM-DD)."""
    from garth.stats import WeeklyStress

    client = get_client()
    result = WeeklyStress.list(end=end, period=period, client=client)
    return [_to_dict(entry) for entry in result]


@register
@_handle_garmin_error
def get_training_status_daily(end: str | None = None, period: int = 1) -> list[dict]:
    """Training status for a day (YYYY-MM-DD)."""
    from garth.stats.training_status import DailyTrainingStatus

    client = get_client()
    result = DailyTrainingStatus.list(end=end, period=period, client=client)
    return [_to_dict(entry) for entry in result]


@register
@_handle_garmin_error
def get_training_status_weekly(end: str | None = None, period: int = 1) -> list[dict]:
    """Training status for a week starting from a date (YYYY-MM-DD)."""
    from garth.stats.training_status import WeeklyTrainingStatus

    client = get_client()
    result = WeeklyTrainingStatus.list(end=end, period=period, client=client)
    return [_to_dict(entry) for entry in result]


@register
@_handle_garmin_error
def get_training_status_monthly(end: str | None = None, period: int = 1) -> list[dict]:
    """Training status for a month starting from a date (YYYY-MM-DD)."""
    from garth.stats.training_status import MonthlyTrainingStatus

    client = get_client()
    result = MonthlyTrainingStatus.list(end=end, period=period, client=client)
    return [_to_dict(entry) for entry in result]


@register
@_handle_garmin_error
def get_training_readiness(day: str | None = None) -> list[dict]:
    """Training readiness for a day (YYYY-MM-DD)."""
    from garth.data import TrainingReadinessData

    client = get_client()
    result = TrainingReadinessData.get(day=day, client=client)
    return [_to_dict(entry) for entry in result] if result else []


@register
@_handle_garmin_error
def get_morning_readiness(day: str | None = None) -> dict:
    """Morning readiness for a day (YYYY-MM-DD)."""
    from garth.data import MorningTrainingReadinessData

    client = get_client()
    result = MorningTrainingReadinessData.get(day=day, client=client)
    return _to_dict(result) if result else {}
