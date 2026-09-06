"""Hydration tools: daily fluid intake and history."""

from __future__ import annotations

from typing import Any

from .base import register
from ..garmin_service import GarminService


@register
def get_daily_hydration(service: GarminService, day: str | None = None) -> dict[str, Any]:
    """Fluid intake including daily goal for a day (YYYY-MM-DD)."""
    return service.daily_hydration(day=day)


@register
def get_hydration_history(service: GarminService, end: str | None = None, days: int = 1) -> list[dict[str, Any]]:
    """Fluid intake history for the last N days (period=days, up to end, YYYY-MM-DD)."""
    return service.hydration_history(end=end, days=days)