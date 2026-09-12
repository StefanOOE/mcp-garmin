"""Nutrition tools: nutrition log and nutrition status.

garth-ng 1.1.0 has no ``NutritionLog`` / ``NutritionStatus`` accessors, so both
tools use the Endpoint-Fallback pattern (S1 §1.7, live-verified 2026-09):
``client.connectapi(path)`` + ``camel_to_snake_dict()``. Paths carry **no**
``/connectapi``/``/proxy`` prefix -- ``connectapi()`` builds the URL itself.

Live payload shapes (verified against a real profile):
* log    -- single day-log dict (``mealDate``, ``dailyNutritionGoals``,
  ``mealDetails``, ``loggedFoodsWithServingSizes`` ...).
* status -- current status dict (``currentStatus``, ``hasUsedNutrition``,
  ``hasUsedMFP``) -- *no* day parameter (current status, not per-day).
"""

from __future__ import annotations

from datetime import date

from .client import _handle_garmin_error, get_client


@_handle_garmin_error
def get_nutrition_log(day: str | None = None) -> dict:
    """Nutrition log for a day (YYYY-MM-DD) — calories, macros, meals."""
    client = get_client()
    from garth.utils import camel_to_snake_dict

    if day is None:
        day = date.today().isoformat()
    raw = client.connectapi(f"/nutrition-service/food/logs/{day}")
    return camel_to_snake_dict(raw) if raw else {}


@_handle_garmin_error
def get_nutrition_status() -> dict:
    """Nutrition status: current calorie goals and consumption."""
    client = get_client()
    from garth.utils import camel_to_snake_dict

    raw = client.connectapi("/nutrition-service/user/nutritionCurrentStatus")
    return camel_to_snake_dict(raw) if raw else {}
