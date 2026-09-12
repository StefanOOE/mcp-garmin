"""Thin wrapper for nutrition tools.

garth-ng 1.1.0 has no ``NutritionLog`` / ``NutritionStatus`` accessors, so both
tools use the Endpoint-Fallback pattern (S1 §1.7, live-verified 2026-09):
``client.connectapi(path)`` + ``camel_to_snake_dict()``. Paths carry **no**
``/connectapi``/``/proxy`` prefix -- ``connectapi()`` builds the URL itself.
"""

from __future__ import annotations

from datetime import date

from .base import register
from ..client import GarminClient

# Create a singleton client instance
_client_instance = GarminClient()


def get_client():
    """Get the Garmin client instance."""
    return _client_instance.get_client()


def _handle_garmin_error(func):
    """Handle Garmin errors."""
    return _client_instance._handle_garmin_error(func)


@register
@_handle_garmin_error
def get_nutrition_log(day: str | None = None) -> dict:
    """Nutrition log for a day (YYYY-MM-DD) — calories, macros, meals."""
    from garth.utils import camel_to_snake_dict

    client = get_client()
    if day is None:
        day = date.today().isoformat()
    raw = client.connectapi(f"/nutrition-service/food/logs/{day}")
    return camel_to_snake_dict(raw) if raw else {}


@register
@_handle_garmin_error
def get_nutrition_status() -> dict:
    """Nutrition status: current calorie goals and consumption."""
    from garth.utils import camel_to_snake_dict

    client = get_client()
    raw = client.connectapi("/nutrition-service/user/nutritionCurrentStatus")
    return camel_to_snake_dict(raw) if raw else {}
