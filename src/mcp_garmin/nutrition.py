"""Nutrition tools: nutrition log and nutrition status."""
from __future__ import annotations

from .client import _handle_garmin_error, _to_dict, get_client


@_handle_garmin_error
def get_nutrition_log(day: str | None = None) -> dict:
    """Nutrition log for a day (YYYY-MM-DD) — calories, macros, meals."""
    client = get_client()
    from garth.data import NutritionLog

    result = NutritionLog.get(day=day, client=client)
    return _to_dict(result) if result is not None else {}


@_handle_garmin_error
def get_nutrition_status() -> dict:
    """Nutrition status: current calorie goals and consumption."""
    client = get_client()
    from garth.data import NutritionStatus

    result = NutritionStatus.get(client=client)
    return _to_dict(result) if result is not None else {}
