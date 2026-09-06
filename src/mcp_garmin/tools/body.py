"""Body tools: weight, blood pressure, body battery."""

from __future__ import annotations

from typing import Any

from .base import register
from ..garmin_service import GarminService


@register
def get_body_weight(service: GarminService, day: str | None = None) -> dict[str, Any]:
    """Body weight for a day (YYYY-MM-DD) — grams, BMI, body fat, etc."""
    return service.weight(day=day)


@register
def get_weight_history(service: GarminService, end: str | None = None, days: int = 7) -> list[dict[str, Any]]:
    """Weight history for the last N days (up to end, YYYY-MM-DD)."""
    return service.weight_history(end=end, days=days)


@register
def get_blood_pressure(service: GarminService, day: str | None = None) -> dict[str, Any]:
    """Blood pressure reading for a day (YYYY-MM-DD)."""
    return service.blood_pressure(day=day)


@register
def get_body_battery(service: GarminService, day: str | None = None) -> list[dict[str, Any]]:
    """Body Battery readings for a day (YYYY-MM-DD)."""
    return service.body_battery(day=day)


@register
def get_body_battery_stress(service: GarminService, day: str | None = None) -> dict[str, Any]:
    """Body Battery + stress summary for a day (YYYY-MM-DD)."""
    return service.body_battery_stress(day=day)


@register
def get_body_battery_stress_history(service: GarminService, end: str | None = None, days: int = 7) -> list[dict[str, Any]]:
    """Body Battery + stress history for the last N days (up to end)."""
    return service.body_battery_stress_history(end=end, days=days)