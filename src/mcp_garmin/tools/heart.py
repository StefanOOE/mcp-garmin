"""Heart tools: daily heart rate, HRV, resting heart rate."""

from __future__ import annotations

from typing import Any

from .base import register
from ..garmin_service import GarminService


@register
def get_daily_heart_rate(service: GarminService, day: str | None = None) -> dict[str, Any]:
    """Daily heart rate for a day (YYYY-MM-DD): max, min, resting."""
    return service.daily_heart_rate(day=day)


@register
def get_hrv(service: GarminService, end: str | None = None, days: int = 28) -> list[dict[str, Any]]:
    """HRV history for the last N days (period=days, up to end, YYYY-MM-DD)."""
    return service.hrv(end=end, days=days)


@register
def get_resting_heart_rate(service: GarminService, end: str | None = None, days: int = 1) -> list[dict[str, Any]]:
    """Resting heart rate history for the last N days (up to end, YYYY-MM-DD)."""
    return service.resting_heart_rate(end=end, days=days)