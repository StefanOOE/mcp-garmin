"""Stress tools: daily/weekly stress, training status, morning readiness."""

from __future__ import annotations

from typing import Any

from .base import register
from ..garmin_service import GarminService


@register
def get_daily_stress(service: GarminService, end: str | None = None, days: int = 1) -> list[dict[str, Any]]:
    """Stress history for the last N days (period=days, up to end, YYYY-MM-DD)."""
    return service.daily_stress(end=end, days=days)


@register
def get_weekly_stress(service: GarminService, end: str | None = None) -> list[dict[str, Any]]:
    """Stress history for the last 7 days (up to end, YYYY-MM-DD)."""
    return service.weekly_stress(end=end)


@register
def get_training_status_daily(service: GarminService, day: str | None = None) -> list[dict[str, Any]]:
    """Training status for a day (YYYY-MM-DD)."""
    return service.training_status_daily(day=day)


@register
def get_training_status_weekly(service: GarminService, end: str | None = None) -> list[dict[str, Any]]:
    """Training status for the last week (up to end, YYYY-MM-DD)."""
    return service.training_status_weekly(end=end)


@register
def get_training_status_monthly(service: GarminService, end: str | None = None) -> list[dict[str, Any]]:
    """Training status for the last month (up to end, YYYY-MM-DD)."""
    return service.training_status_monthly(end=end)


@register
def get_training_readiness(service: GarminService, day: str | None = None) -> dict[str, Any]:
    """Morning Training Readiness for a day (YYYY-MM-DD)."""
    return service.training_readiness(day=day)


@register
def get_morning_readiness(service: GarminService, day: str | None = None) -> dict[str, Any]:
    """Morning Readiness for a day (YYYY-MM-DD) — alias for get_training_readiness."""
    return service.morning_readiness(day=day)