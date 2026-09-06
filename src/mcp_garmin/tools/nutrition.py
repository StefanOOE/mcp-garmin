"""Thin wrapper for nutrition tools."""

from __future__ import annotations

from .base import register
from ..client import GarminClient

# Create a singleton client instance
_client_instance = GarminClient()


def get_client():
    """Get the Garmin client instance."""
    return _client_instance.get_client()


def _to_dict(obj):
    """Convert object to dict."""
    return _client_instance._to_dict(obj)


def _handle_garmin_error(func):
    """Handle Garmin errors."""
    return _client_instance._handle_garmin_error(func)


@register
@_handle_garmin_error
def get_nutrition_log(day: str | None = None) -> list[dict]:
    """Nutrition log for a day (YYYY-MM-DD)."""
    from garth.data import NutritionLog

    client = get_client()
    result = NutritionLog.get(day=day, client=client)
    return [_to_dict(entry) for entry in result]


@register
@_handle_garmin_error
def get_nutrition_status(day: str | None = None) -> dict:
    """Nutrition status for a day (YYYY-MM-DD)."""
    from garth.data import NutritionStatus

    client = get_client()
    result = NutritionStatus.get(day=day, client=client)
    return _to_dict(result)
