"""Sleep tools: sleep stages, detail data, daily summary (sleep part)."""

from __future__ import annotations

from typing import Any

from .base import register
from ..garmin_service import GarminService


@register
def get_sleep(service: GarminService, day: str | None = None) -> dict[str, Any]:
    """Sleep data for a day (YYYY-MM-DD) including sleep stage time blocks."""
    return service.sleep(day=day)


@register
def get_sleep_detail(service: GarminService, day: str | None = None) -> dict[str, Any]:
    """Sleep details (daily data) for a day (YYYY-MM-DD)."""
    return service.sleep_detail(day=day)


@register
def get_sleep_summary(service: GarminService, day: str | None = None) -> dict[str, Any]:
    """Daily summary for a day (YYYY-MM-DD).

    Returns only sleep-related fields if available, otherwise the
    full dict.
    """
    return service.sleep_summary(day=day)