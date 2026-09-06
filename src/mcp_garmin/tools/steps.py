"""Steps tools: daily/weekly steps, daily summary."""

from __future__ import annotations

from typing import Any

from .base import register
from ..garmin_service import GarminService


@register
def get_daily_steps(service: GarminService, end: str | None = None) -> list[dict[str, Any]]:
    """Step count for the last day (period=1, up to end, YYYY-MM-DD)."""
    return service.daily_steps(end=end)


@register
def get_weekly_steps(service: GarminService, end: str | None = None) -> list[dict[str, Any]]:
    """Step count for the last 7 days (period=7, up to end, YYYY-MM-DD)."""
    return service.weekly_steps(end=end)


@register
def get_daily_summary(service: GarminService, day: str | None = None) -> dict[str, Any]:
    """Daily summary for a day (YYYY-MM-DD): steps, calories, heart rate."""
    return service.daily_summary(day=day)


@register
def get_daily_summary_history(service: GarminService, end: str | None = None, days: int = 7) -> list[dict[str, Any]]:
    """Daily summary history for the last N days (up to end, YYYY-MM-DD)."""
    return service.daily_summary_history(end=end, days=days)