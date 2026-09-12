"""Thin wrapper for body tools."""

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
def get_body_weight(day: str | None = None) -> dict:
    """Body weight for a day (YYYY-MM-DD) — grams, BMI, body fat, etc."""
    from garth.data import WeightData

    client = get_client()
    result = WeightData.get(day=day, client=client)
    return _to_dict(result)


@register
@_handle_garmin_error
def get_weight_history(end: str | None = None, days: int = 7) -> list[dict]:
    """Weight history for the last N days (up to end, YYYY-MM-DD)."""
    from garth.data import WeightData

    client = get_client()
    result = WeightData.list(end=end, days=days, client=client)
    return [_to_dict(entry) for entry in result]


@register
@_handle_garmin_error
def get_blood_pressure(day: str | None = None) -> dict:
    """Blood pressure reading for a day (YYYY-MM-DD).

    No garth.data accessor exists (S1 spike-api-mapping.md \u00a71.4);
    endpoint-fallback via client.connectapi().
    """
    from ..serialization import camel_to_snake_dict

    client = get_client()
    raw = client.connectapi(f"/bloodpressure-service/bloodpressure/dayview/{day}")
    return camel_to_snake_dict(raw) if raw else {}


@register
@_handle_garmin_error
def get_body_battery(day: str | None = None) -> list[dict]:
    """Body Battery readings for a day (YYYY-MM-DD)."""
    from garth.data import BodyBatteryData

    client = get_client()
    result = BodyBatteryData.get(day=day, client=client)
    return [_to_dict(entry) for entry in result]


@register
@_handle_garmin_error
def get_body_battery_stress(day: str | None = None) -> dict:
    """Body Battery + stress summary for a day (YYYY-MM-DD)."""
    from garth.data import DailyBodyBatteryStress

    client = get_client()
    result = DailyBodyBatteryStress.get(day=day, client=client)
    return _to_dict(result)


@register
@_handle_garmin_error
def get_body_battery_stress_history(
    end: str | None = None, days: int = 7
) -> list[dict]:
    """Body Battery + stress history for the last N days (up to end)."""
    from garth.data import DailyBodyBatteryStress

    client = get_client()
    result = DailyBodyBatteryStress.list(end=end, days=days, client=client)
    return [_to_dict(entry) for entry in result]
