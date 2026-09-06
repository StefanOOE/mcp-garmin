"""Nutrition tools: nutrition log and nutrition status."""

from __future__ import annotations

from typing import Any

from .base import register
from ..garmin_service import GarminService


@register
def get_nutrition_log(service: GarminService, day: str | None = None) -> dict[str, Any]:
    """Nutrition log for a day (YYYY-MM-DD) — calories, macros, meals."""
    return service.nutrition_log(day=day)


@register
def get_nutrition_status(service: GarminService) -> dict[str, Any]:
    """Nutrition status: current calorie goals and consumption."""
    return service.nutrition_status()